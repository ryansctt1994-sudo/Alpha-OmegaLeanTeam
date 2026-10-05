"""Behavioral runtime mutants, provenance controls, and Lean semantic mutants.

MU-1..5 are executed after the ORIGINAL inputs pass the pin gate, in isolated
child processes. They must fail the replay semantics, not merely source hashes.
No mutation path is available on the positive replay CLI.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import types
from pathlib import Path

import replay
from check_pins import ROOT, check_pins

RUNTIME = {
    "MU-1-prev-bypass": (
        '        if event.get("prev_hash") != expected_prev_hash:',
        '        if False:', "invalid operation accepted"),
    "MU-2-index-bypass": (
        '        if event.get("index") != expected_index:',
        '        if False:', "invalid operation accepted"),
    "MU-3-integrity-bypass": (
        '        validate_event_integrity(event, validator=self.validator)',
        '        pass  # hostile integrity bypass', "invalid operation accepted"),
    "MU-4-write-on-reject": (
        '        if event.get("index") != expected_index:',
        '        self.path.parent.mkdir(parents=True, exist_ok=True)\n'
        '        with self.path.open("a", encoding="utf-8") as early:\n'
        '            early.write(json.dumps(event) + "\\n")\n'
        '        if event.get("index") != expected_index:', "event index mismatch"),
    "MU-5-prefix-rewrite": (
        '        with self.path.open("a", encoding="utf-8") as handle:',
        '        with self.path.open("w", encoding="utf-8") as handle:', "event index mismatch"),
}

LEAN = {
    "LEAN-prev-guard": (
        '(prev : e.prev_hash = concreteHead r.val.events)\n      (integrity',
        '(prev : True)\n      (integrity'),
    "LEAN-index-guard": (
        '(index : e.index = r.val.events.length)\n      (prev : e.prev_hash = concreteHead r.val.events)\n      (integrity',
        '(index : True)\n      (prev : e.prev_hash = concreteHead r.val.events)\n      (integrity'),
    "LEAN-digest-guard": (
        '(digest : e.event_hash = enc.compute_event_hash e)\n      (events',
        '(digest : True)\n      (events'),
    "LEAN-prefix-prepend": (
        '(events : r\'.val.events = r.val.events ++ [e])\n      (bytes',
        '(events : r\'.val.events = [e] ++ r.val.events)\n      (bytes'),
    "LEAN-wrong-head": (
        'head := concreteHead r.val.events }',
        'head := "external-expected-head" }'),
}


def replace_once(source, old, new):
    assert source.count(old) == 1, f"mutation target count {source.count(old)}"
    return source.replace(old, new, 1)


def worker(name):
    ledger, verifier = replay.load_runtime()
    if name in RUNTIME:
        old, new, _ = RUNTIME[name]
        path = replay.VENDOR / "triadic_controls/ledger.py"
        mutated = types.ModuleType("hostile_ledger")
        mutated.__file__ = str(path)
        sys.modules[mutated.__name__] = mutated
        exec(compile(replace_once(path.read_text(), old, new), str(path), "exec", dont_inherit=True), mutated.__dict__)
        replay.run_suite(mutated, verifier)
    elif name == "MU-6-wrong-head":
        original = replay.alpha
        def wrong_head(ledger, events):
            h = original(ledger, events)
            h["head"] = "0" * 64
            return h
        replay.alpha = wrong_head
        replay.run_suite(ledger, verifier)
    elif name == "MU-7-fake-verifier":
        verifier.verify_bytes = lambda *args, **kwargs: {"events": 999, "head": "fake"}
        replay.run_suite(ledger, verifier)
    else:
        raise ValueError(name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker")
    args = parser.parse_args()
    if args.worker:
        worker(args.worker)
        return
    check_pins()
    ledger, verifier = replay.load_runtime()
    replay.run_suite(ledger, verifier)  # positive control before negative tests
    results = []
    expectations = {name: case[2] for name, case in RUNTIME.items()}
    expectations.update({"MU-6-wrong-head": "prev_hash mismatch", "MU-7-fake-verifier": "wrong function origin"})
    for name, expected in expectations.items():
        run = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker", name], capture_output=True, text=True, timeout=90)
        assert run.returncode != 0 and expected in run.stderr, f"{name}: survived or wrong failure\n{run.stderr}"
        results.append({"name": name, "status": "KILLED", "detector": expected})
        print(name + ": KILLED")
    with tempfile.TemporaryDirectory(prefix="ao-pin-mutants-") as folder:
        temp = Path(folder)
        # Import a copied checker with an independent ROOT, never modify live inputs.
        script = temp / "check_pins.py"
        shutil.copy2(ROOT / "check_pins.py", script)
        for path in ["source-pins.json", *json.loads((ROOT / "source-pins.json").read_text())["git_blobs"]]:
            out = temp / path
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / path, out)
        targets = ["contracts/V0_6_FORWARD_SIMULATION_CONTRACT.md", "vendor/Weaver_Os/triadic_controls/ledger.py"]
        for target in targets:
            p = temp / target
            original = p.read_bytes()
            p.write_bytes(original + b"\n# MU-8 frozen pin drift\n")
            run = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=30)
            assert run.returncode != 0 and "source pin mismatch" in run.stderr, run.stderr
            p.write_bytes(original)
        results.append({"name": "MU-8-contract-and-source-drift", "status": "KILLED", "detector": "source pin mismatch (2 probes)"})
        print("MU-8-contract-and-source-drift: KILLED (2 probes)")
        source = (ROOT / "ForwardSimulation.lean").read_text()
        for name, (old, new) in LEAN.items():
            path = temp / f"{name}.lean"
            path.write_text(replace_once(source, old, new))
            run = subprocess.run(["lake", "env", "lean", "-DwarningAsError=true", str(path)], cwd=ROOT,
                                 capture_output=True, text=True, timeout=120)
            assert run.returncode != 0 and "error:" in run.stdout + run.stderr, f"{name}: survived or compiler not invoked"
            assert "type mismatch" in run.stdout or "unsolved goals" in run.stdout, f"{name}: wrong failure\n{run.stdout}"
            results.append({"name": name, "status": "KILLED", "detector": "Lean correspondence proof failure"})
            print(name + ": KILLED")
    (ROOT / "generated").mkdir(exist_ok=True)
    (ROOT / "generated/mutations.json").write_text(json.dumps(results, indent=2) + "\n")
    print("mutation controls PASS: MU-1..MU-8 (9 probes), 5 Lean semantic mutants")


if __name__ == "__main__":
    main()
