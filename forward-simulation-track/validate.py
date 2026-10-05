"""Run the isolated v0.6 gate. Root governance runs in its own workflow."""
import hashlib
import json
import os
import re
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

from check_pins import ROOT, check_pins


def run(command, log):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=900)
    output = result.stdout + result.stderr
    log.write_text(output)
    print(output, end="", flush=True)
    if result.returncode:
        raise RuntimeError(f"gate command failed: {command[0]}; see {log.name}")
    return output


def check_axioms(output, expected_count):
    lines = [line for line in output.splitlines() if "depends on axioms" in line or "does not depend on any axioms" in line]
    assert len(lines) == expected_count, f"incomplete axiom audit: {len(lines)}/{expected_count}"
    allowed = {"propext", "Quot.sound", "Classical.choice"}
    used = {x.strip() for group in re.findall(r"depends on axioms: \[([^\]]*)\]", output) for x in group.split(",") if x.strip()}
    assert used <= allowed, f"unexpected axioms: {used - allowed}"
    assert "sorryAx" not in output and "Lean.ofReduceBool" not in output
    return sorted(used)


def main():
    check_pins()
    generated = ROOT / "generated"
    generated.mkdir(exist_ok=True)
    lean_version = run(["lean", "--version"], generated / "toolchain.log").strip()
    assert "version 4.22.0," in lean_version, "wrong Lean version"
    source = (ROOT / "ForwardSimulation.lean").read_text()
    assert len(re.findall(r"^theorem\s", source, re.M)) == 12
    assert not re.search(r"\b(sorry|admit|axiom|native_decide)\b", source)
    root_files = [ROOT.parent / name for name in ["AlphaOmega.lean", "LatticeCore.lean", "IntrospectionTwin.lean"]]
    for family in ["AlphaOmega", "LatticeCore", "IntrospectionTwin"]:
        root_files.extend((ROOT.parent / family).rglob("*.lean"))
    root_count = sum(len(re.findall(r"^\s*theorem\s+[A-Za-z0-9_'.]+", p.read_text(), re.M)) for p in root_files)
    assert root_count == 124, "root governance inventory changed"
    build = run(["lake", "build"], generated / "build.log")
    assert "warning:" not in build.lower(), "build warning"
    axioms = check_axioms(run(["lake", "env", "lean", "-DwarningAsError=true", "Audit.lean"], generated / "axioms.log"), 12)
    run([sys.executable, "check_mutations.py"], generated / "mutations.log")
    env = dict(os.environ, PYTHONPATH=str(ROOT / "vendor/Weaver_Os"))
    test = subprocess.run([sys.executable, "-m", "pytest", "-q", "vendor/Weaver_Os/tests/test_triad_multiblock.py"],
                          cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
    (generated / "upstream-tests.log").write_text(test.stdout + test.stderr)
    assert test.returncode == 0 and "38 passed" in test.stdout, test.stdout + test.stderr
    print(test.stdout, end="", flush=True)
    run([sys.executable, "replay.py", "--lean"], generated / "replay.log")
    replay_axioms = check_axioms((generated / "replay-axioms.log").read_text(), 86)
    replay = json.loads((generated / "replay.json").read_text())
    assert replay["certificate_kernel_checked"] and len(replay["traces"]) == 43
    frozen_fixtures = json.loads((ROOT / "fixture-pins.json").read_text())
    for name, expected in frozen_fixtures.items():
        assert hashlib.sha256((generated / name).read_bytes()).hexdigest() == expected, f"fixture drift: {name}"
    code = ["ForwardSimulation.lean", "Audit.lean", "check_pins.py", "replay.py", "check_mutations.py", "validate.py", "source-pins.json", "fixture-pins.json", "requirements.txt"]
    report = {
        "status": "PASS", "assumptions": "A-F", "root_theorems": root_count,
        "track_theorems": 12, "track_axioms": axioms, "replay_axioms": replay_axioms,
        "runtime_transitions": 43, "named_labels": 7, "upstream_tests": 38,
        "required_mutant_families": 8, "required_mutant_probes": 9, "extra_lean_mutants": 5,
        "boundary_witnesses": ["EX-1", "EX-2"], "independent_reproduction": False,
        "lean_version": lean_version, "python_version": sys.version,
        "dependencies": {name: version(name) for name in ["cryptography", "jsonschema", "pytest", "attrs", "referencing", "rpds-py", "jsonschema-specifications"]},
        "code_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in code},
        "fixture_sha256": frozen_fixtures,
    }
    (generated / "validation.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("isolated v0.6 gate PASS; root CI and review remain separate")


if __name__ == "__main__":
    main()
