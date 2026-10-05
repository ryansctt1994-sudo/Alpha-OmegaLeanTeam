"""Pinned-runtime replay and generated kernel-checked snapshot certificates.

Assumptions A-F are normative in contracts/V0_6_FORWARD_SIMULATION_CONTRACT.md.
This harness is bounded executable evidence for the explicit Lean encoding.
It is not a universal derivation of Python semantics or a parser proof.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
import subprocess
import sys
import tempfile
import types
from pathlib import Path
from unittest.mock import patch

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from check_pins import ROOT, check_pins

VENDOR = ROOT / "vendor" / "Weaver_Os"
KEY = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
PUBLIC = KEY.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
FINGERPRINT = hashlib.sha256(PUBLIC).hexdigest()


def bind_function(fn, path, name):
    """A fake callable cannot satisfy the pinned callable check by returning True."""
    assert isinstance(fn, types.FunctionType), f"not a source-bound function: {name}"
    assert Path(fn.__code__.co_filename).resolve() == path.resolve(), f"wrong function origin: {name}"
    module_code = compile(path.read_bytes(), str(path), "exec", dont_inherit=True)

    def find(code):
        for item in code.co_consts:
            if isinstance(item, types.CodeType):
                if item.co_name == name:
                    return item
                nested = find(item)
                if nested is not None:
                    return nested
        return None

    expected = find(module_code)
    assert expected is not None, f"function missing from source: {name}"
    assert fn.__code__ == expected, f"substituted function: {name}"


def load_runtime():
    check_pins()
    sys.path.insert(0, str(VENDOR))
    ledger = importlib.import_module("triadic_controls.ledger")
    verifier = importlib.import_module("tools.verify_triad_ledger")
    assert Path(ledger.__file__).resolve() == VENDOR / "triadic_controls/ledger.py"
    assert Path(verifier.__file__).resolve() == VENDOR / "tools/verify_triad_ledger.py"
    for name in ["compute_event_hash", "canonical_json", "verify_chain", "validate_event_integrity"]:
        bind_function(getattr(ledger, name), VENDOR / "triadic_controls/ledger.py", name)
    for name in ["load_events", "append_event"]:
        bind_function(getattr(ledger.TriadLedger, name), VENDOR / "triadic_controls/ledger.py", name)
    bind_function(verifier.verify_bytes, VENDOR / "tools/verify_triad_ledger.py", "verify_bytes")
    assert verifier.verify_chain is ledger.verify_chain, "verifier chain substitution"
    return ledger, verifier


def strict(verifier, raw, head, fingerprint=FINGERPRINT):
    bind_function(verifier.verify_bytes, VENDOR / "tools/verify_triad_ledger.py", "verify_bytes")
    return verifier.verify_bytes(raw, head, fingerprint, hashlib.sha256(raw).hexdigest())


def event(ledger, index, prev, payload=None, signed=True):
    e = {
        "index": index, "timestamp": "2026-10-05T00:00:00Z", "event_type": "proposal",
        "actor": "fixture-operator", "public_key": PUBLIC.hex(),
        "payload": payload if payload is not None else {"id": f"event-{index}", "value": index},
        "prev_hash": prev, "event_hash": "", "policy_version": "AO-HISTORY-v1",
    }
    e["event_hash"] = ledger.compute_event_hash(e)
    if signed:
        e["signature"] = KEY.sign(e["event_hash"].encode()).hex()
    return e


def resign(ledger, e):
    e["event_hash"] = ledger.compute_event_hash(e)
    e["signature"] = KEY.sign(e["event_hash"].encode()).hex()
    return e


def abstract_entry(ledger, e):
    return {
        "input": {
            "index": e["index"], "timestamp": e["timestamp"], "eventType": e["event_type"],
            "actor": e["actor"], "publicKey": e["public_key"],
            "payloadCanonical": ledger.canonical_json(e["payload"]).decode(),
            "prevDigest": e["prev_hash"], "policyVersion": e["policy_version"],
        }, "eventDigest": e["event_hash"], "signature": e.get("signature"),
    }


def alpha(ledger, events):
    return {"entries": [abstract_entry(ledger, e) for e in events],
            "head": events[-1]["event_hash"] if events else "genesis"}


def snapshot(ledger, path):
    raw = path.read_bytes() if path.exists() else b""
    events = ledger.TriadLedger(path).load_events()
    return {"raw_utf8": raw.decode(), "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "events": events, "alpha": alpha(ledger, events)}


def must_reject(action, fragment=None):
    try:
        action()
    except ValueError as exc:
        if fragment is not None:
            assert fragment in str(exc), f"wrong rejection: {exc}"
        return str(exc)
    raise AssertionError("invalid operation accepted")


def run_suite(ledger, verifier):
    traces, boundaries = [], []
    with tempfile.TemporaryDirectory(prefix="ao-history-replay-") as folder:
        base = Path(folder)
        for depth in [0, 1, 3, 8]:
            path = base / f"depth-{depth}.jsonl"
            runtime = ledger.TriadLedger(path)
            for i in range(depth):
                before = snapshot(ledger, path)
                runtime.append_event(event(ledger, i, before["alpha"]["head"]))
            start = snapshot(ledger, path)
            if depth:
                strict(verifier, start["raw_utf8"].encode(), start["alpha"]["head"])

            def record(label, action, candidate=None, rejection=None):
                before = snapshot(ledger, path)
                if before["events"]:
                    strict(verifier, before["raw_utf8"].encode(), before["alpha"]["head"])
                if rejection:
                    error = must_reject(action, rejection)
                    result = None
                else:
                    result = action()
                    error = None
                after = snapshot(ledger, path)
                if label == "C_APPEND_OK":
                    expected = {"entries": before["alpha"]["entries"] + [abstract_entry(ledger, candidate)],
                                "head": candidate["event_hash"]}
                    assert after["alpha"] == expected, "append abstraction mismatch"
                    expected_line = json.dumps(candidate, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
                    assert after["raw_utf8"] == before["raw_utf8"] + expected_line, "protected prefix rewrite"
                    assert candidate["index"] == len(before["events"])
                    assert candidate["prev_hash"] == before["alpha"]["head"]
                    assert candidate["event_hash"] == ledger.compute_event_hash(candidate)
                else:
                    assert after == before, "rejected/read-only step changed protected snapshot"
                if after["events"]:
                    strict(verifier, after["raw_utf8"].encode(), after["alpha"]["head"])
                traces.append({"label": label, "before": before, "after": after,
                               "candidate": candidate, "error": error, "operation_result": result,
                               "assumptions": "A-F"})

            record("C_LOAD_OK", runtime.load_events)
            if depth:
                record("C_VERIFY_OK", lambda: strict(verifier, path.read_bytes(), start["alpha"]["head"]))
            good = event(ledger, depth, start["alpha"]["head"],
                         {"unicode": "Ω • café • 你好", "nested": {"z": [True, None, 1.25], "a": "first"}})
            bad_index = resign(ledger, dict(good, index=depth+1))
            record("C_APPEND_REJECT_INDEX", lambda: runtime.append_event(bad_index), bad_index, "event index mismatch")
            bad_prev = resign(ledger, dict(good, prev_hash="0"*64))
            record("C_APPEND_REJECT_PREV", lambda: runtime.append_event(bad_prev), bad_prev, "prev_hash mismatch")
            for kind in ["hash", "signature", "schema"]:
                bad = copy.deepcopy(good)
                if kind == "hash":
                    bad["event_hash"] = "0"*64
                elif kind == "signature":
                    bad["signature"] = "0"*128
                else:
                    bad["event_type"] = "invalid-type"
                    resign(ledger, bad)
                record("C_APPEND_REJECT_INTEGRITY", lambda: runtime.append_event(bad), bad,
                       {"hash": "event_hash mismatch", "signature": "signature verification failed", "schema": "schema validation failed"}[kind])
            record("C_STRICT_VERIFY_REJECT", lambda: strict(verifier, start["raw_utf8"].encode(), "0"*64), rejection="invalid line framing" if depth == 0 else "head mismatch")
            record("C_APPEND_OK", lambda: runtime.append_event(good), good)
            record("C_VERIFY_OK", lambda: strict(verifier, path.read_bytes(), good["event_hash"]))
            record("C_STRICT_VERIFY_REJECT", lambda: strict(verifier, path.read_bytes(), good["event_hash"], "0"*64), rejection="untrusted key")

        # EX-2: primitive accepts absent signature; strict verifier rejects it.
        path = base / "unsigned.jsonl"
        unsigned = event(ledger, 0, "genesis", signed=False)
        ledger.TriadLedger(path).append_event(unsigned)
        loaded = ledger.TriadLedger(path).load_events()
        assert loaded == [unsigned]
        reason = must_reject(lambda: strict(verifier, path.read_bytes(), unsigned["event_hash"]), "unsigned event")
        boundaries.append({"name": "EX-2", "outside": "R_strict, inside R_ok", "reason": reason,
                           "snapshot": snapshot(ledger, path), "assumptions": "A-F"})

        # EX-1: interrupt the REAL append at its second write, not a hand-made file.
        path = base / "torn.jsonl"
        signed = event(ledger, 0, "genesis")
        original_open = Path.open

        class InterruptedWrite:
            def __init__(self, handle):
                self.handle, self.writes = handle, 0
            def __enter__(self):
                return self
            def __exit__(self, *args):
                self.handle.close()
            def write(self, value):
                self.writes += 1
                if self.writes == 2:
                    raise OSError("EX-1 interruption before newline write")
                result = self.handle.write(value)
                self.handle.flush()
                return result

        def interrupted_open(p, mode="r", *args, **kwargs):
            handle = original_open(p, mode, *args, **kwargs)
            return InterruptedWrite(handle) if p == path and mode == "a" else handle

        with patch.object(Path, "open", interrupted_open):
            try:
                ledger.TriadLedger(path).append_event(signed)
            except OSError as exc:
                assert "EX-1 interruption" in str(exc)
            else:
                raise AssertionError("EX-1 interruption was not injected")
        raw = path.read_bytes()
        assert raw and not raw.endswith(b"\n")
        reason = must_reject(lambda: strict(verifier, raw, signed["event_hash"]), "invalid line framing")
        # Primitive loader accepts this complete JSON without its final newline.
        assert ledger.TriadLedger(path).load_events() == [signed]
        boundaries.append({"name": "EX-1", "outside": "assumption C; outside R_strict, still inside R_ok",
                           "reason": reason, "raw_utf8": raw.decode(), "raw_sha256": hashlib.sha256(raw).hexdigest()})
    return traces, boundaries


def q(value):
    # Lean accepts direct Unicode; JSON's quote/backslash/newline escapes agree.
    return json.dumps(value, ensure_ascii=False)


def event_term(ledger, e):
    mapping = {"index": str(e["index"]), "timestamp": q(e["timestamp"]), "event_type": q(e["event_type"]),
               "actor": q(e["actor"]), "public_key": q(e["public_key"]),
               "payloadCanonical": q(ledger.canonical_json(e["payload"]).decode()), "prev_hash": q(e["prev_hash"]),
               "policy_version": q(e["policy_version"]), "event_hash": q(e["event_hash"]),
               "signature": "none" if "signature" not in e else "some " + q(e["signature"])}
    return "{ " + ", ".join(f"{k} := {v}" for k, v in mapping.items()) + " }"


def history_term(h):
    def entry_term(e):
        fields = ", ".join(f"{k} := {v if k == 'index' else q(v)}" for k, v in e["input"].items())
        sig = "none" if e["signature"] is None else "some " + q(e["signature"])
        return "{ input := { " + fields + " }, eventDigest := " + q(e["eventDigest"]) + ", signature := " + sig + " }"
    return "{ entries := [" + ", ".join(entry_term(e) for e in h["entries"]) + "], head := " + q(h["head"]) + " }"


def emit_certificates(ledger, traces, target):
    lines = ["import ForwardSimulation", "open AOForward AlphaOmega.History", "set_option maxRecDepth 100000", "set_option maxHeartbeats 0"]
    for number, trace in enumerate(traces):
        lines.append(f"namespace Fixture{number}")
        before, after, candidate = trace["before"], trace["after"], trace["candidate"]
        for name, snap in [("before", before), ("after", after)]:
            terms = ", ".join(event_term(ledger, e) for e in snap["events"])
            lines += [f"def {name}Events : List Event := [{terms}]",
                      f"def {name}Raw : List UInt8 := ({q(snap['raw_utf8'])}).toUTF8.data.toList"]
        if candidate is not None:
            lines.append("def candidate : Event := " + event_term(ledger, candidate))
        table = []
        for e in before["events"] + after["events"] + ([candidate] if candidate else []):
            pair = f"((abstractEntry ({event_term(ledger, e)})).input, {q(ledger.compute_event_hash(e))})"
            if pair not in table:
                table.append(pair)
        lines.append("def H (input : DigestInput) : Digest :=\n  (([" + ", ".join(table) + "] : List (DigestInput × Digest)).find? (fun p => p.1 == input)).map Prod.snd |>.getD \"unmapped\"")
        invalid = candidate is not None and trace["label"] == "C_APPEND_REJECT_INTEGRITY"
        integrity = "fun e => decide (e ≠ candidate)" if invalid else "fun _ => true"
        serialize = ("fun _ => (" + q(after["raw_utf8"][len(before["raw_utf8"]):]) + ").toUTF8.data.toList") if trace["label"] == "C_APPEND_OK" else "fun _ => []"
        if trace["label"] == "C_VERIFY_OK":
            assert trace["operation_result"]["file_sha256"] == before["raw_sha256"]
            assert trace["operation_result"]["head"] == before["alpha"]["head"]
            assert trace["operation_result"]["events"] == len(before["events"])
        if trace["label"] == "C_STRICT_VERIFY_REJECT":
            assert trace["operation_result"] is None and trace["error"]
        strict_outcome = "false" if trace["label"] == "C_STRICT_VERIFY_REJECT" else "true"
        lines += ["def enc : Encoding := {",
                  "  decode := fun raw => if raw = beforeRaw then some beforeEvents else if raw = afterRaw then some afterEvents else none",
                  "  compute_event_hash := fun e => H (abstractEntry e).input",
                  "  integrity := " + integrity,
                  "  serializeLine := " + serialize,
                  "  strictVerify := fun _ => " + strict_outcome + " }",
                  "def pre : R_ok enc := ⟨⟨beforeRaw, beforeEvents⟩, ⟨by decide, by unfold ChainValid; decide⟩⟩",
                  "def post : R_ok enc := ⟨⟨afterRaw, afterEvents⟩, ⟨by decide, by unfold ChainValid; decide⟩⟩",
                  "theorem digest_bridge : DigestBridge enc H := by intro r e _ _ _ _; rfl",
                  "example : alpha pre = " + history_term(before["alpha"]) + " := by decide",
                  "example : alpha post = " + history_term(after["alpha"]) + " := by decide"]
        label = trace["label"]
        constructor = {
            "C_LOAD_OK": ".load pre post (by decide)",
            "C_VERIFY_OK": ".verify pre post (by decide) (by decide)",
            "C_APPEND_OK": ".append pre post candidate (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)",
            "C_APPEND_REJECT_INDEX": ".rejectIndex pre post candidate (by decide) (by decide)",
            "C_APPEND_REJECT_PREV": ".rejectPrev pre post candidate (by decide) (by decide) (by decide)",
            "C_APPEND_REJECT_INTEGRITY": ".rejectIntegrity pre post candidate (by decide) (by decide) (by decide) (by decide)",
            "C_STRICT_VERIFY_REJECT": ".strictReject pre post (by decide) (by decide)",
        }[label]
        lines += [f"theorem concrete_step : CStep enc .{label} pre post := {constructor}",
                  f"theorem replay : ForwardMatch H .{label} (alpha pre) (alpha post) := named_step_forward_simulation digest_bridge concrete_step",
                  f"end Fixture{number}"]
    for number in range(len(traces)):
        lines.append(f"#print axioms Fixture{number}.concrete_step")
        lines.append(f"#print axioms Fixture{number}.replay")
    target.write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "generated")
    parser.add_argument("--lean", action="store_true", help="kernel-check all generated snapshot certificates")
    args = parser.parse_args()
    ledger, verifier = load_runtime()
    traces, boundaries = run_suite(ledger, verifier)
    assert {t["label"] for t in traces} == {
        "C_LOAD_OK", "C_VERIFY_OK", "C_APPEND_OK", "C_APPEND_REJECT_INDEX", "C_APPEND_REJECT_PREV",
        "C_APPEND_REJECT_INTEGRITY", "C_STRICT_VERIFY_REJECT"}
    args.out.mkdir(parents=True, exist_ok=True)
    certificate = args.out / "Replay.lean"
    emit_certificates(ledger, traces, certificate)
    report = {"assumptions": "A-F", "source_pins": check_pins(), "traces": traces,
              "boundaries": boundaries, "certificate_sha256": hashlib.sha256(certificate.read_bytes()).hexdigest(),
              "certificate_kernel_checked": False}
    if args.lean:
        checked = subprocess.run(["lake", "env", "lean", "-s", "65536", "-DwarningAsError=true", str(certificate)],
                                 cwd=ROOT, check=True, capture_output=True, text=True, timeout=600)
        (args.out / "replay-axioms.log").write_text(checked.stdout + checked.stderr)
        if "sorryAx" in checked.stdout or "Lean.ofReduceBool" in checked.stdout:
            raise AssertionError("forbidden replay proof dependency")
        report["certificate_kernel_checked"] = True
    (args.out / "replay.json").write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print(f"pinned runtime replay PASS: {len(traces)} transitions; 7 labels; EX-1/EX-2 demonstrated; Lean checked={args.lean}")


if __name__ == "__main__":
    main()
