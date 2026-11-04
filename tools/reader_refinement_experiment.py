#!/usr/bin/env python3
"""AO-RR-001: controlled witness-reader mutation against the real pinned Lean project.

The checked-in Lean sources remain unchanged after this experiment. This script
intentionally makes a fabricated witness in a temporary CI worktree, rebuilds
the same theorem corpus, and tests the admission decision in each phase.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "IntrospectionTwin" / "Witness.lean"
OLD = "| none => return ⟨false, false, 0, []⟩"
NEW = "| none => return ⟨true, true, 0, []⟩"
OUT = ROOT / "reader-refinement-evidence"

PROBE = r'''import IntrospectionTwin

open Lean IntrospectionTwin

elab "#aoReaderProbe" : command => do
  let missingClaim : String := "AO_RR_001.provably_unregistered_sentinel"
  let present ← Lean.Elab.Command.liftCoreM do
    let env ← getEnv
    return (env.find? missingClaim.toName).isSome
  if present then
    throwError "AO-RR-001 invalid positive control: sentinel exists in environment"
  let subject : Subject := {
    repoUri := "local-probe"
    commitHash := "frozen-evaluator"
    toolchainHash := "pinned-lean"
  }
  let condition : GateCondition := {
    expectedSubject := subject
    expectedClaim := missingClaim
    allowedAxioms := []
  }
  let receipt := Receipt.sketch subject (.compilerDump "local") missingClaim "digest" "probe" []
  let decision ← Lean.Elab.Command.liftCoreM (IntrospectionTwin.admit condition receipt)
  let expected : Bool := EXPECTED_BOOL
  if decision != expected then
    throwError m!"AO-RR-001 wrong admission: expected {expected}, got {decision}"
  logInfo m!"AO-RR-001 admission witness: env.present={present}, admitted={decision}"

#aoReaderProbe
'''

TYPE_GOOD = r'''structure ReplayCertificate (observedAccepted : Bool) where
  evidence : observedAccepted = true

def validCertificate : ReplayCertificate true := ⟨rfl⟩
'''

TYPE_BAD = r'''structure ReplayCertificate (observedAccepted : Bool) where
  evidence : observedAccepted = true

def fabricatedCertificate : ReplayCertificate false := ⟨rfl⟩
'''


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def command(name: str, args: list[str], timeout: int = 120) -> dict:
    try:
        run = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        stdout, stderr, code = run.stdout, run.stderr, run.returncode
    except subprocess.TimeoutExpired as e:
        stdout = (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr = (e.stderr or b"").decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        code = 124
    (OUT / (name + ".stdout.log")).write_text(stdout, encoding="utf-8")
    (OUT / (name + ".stderr.log")).write_text(stderr, encoding="utf-8")
    return {
        "name": name, "args": args, "exit": code,
        "stdout_sha256": sha(stdout.encode()), "stderr_sha256": sha(stderr.encode()),
        "stdout_file": name + ".stdout.log", "stderr_file": name + ".stderr.log",
    }


def expect_green(receipt: dict) -> None:
    if receipt["exit"] != 0:
        raise RuntimeError(f"{receipt['name']} is red ({receipt['exit']})")


def phase(label: str, expected: str, file: Path, ledger: dict) -> None:
    results = []
    for name, argv, timeout in [
        ("clean", ["lake", "clean"], 90),
        ("build", ["lake", "build"], 180),
        ("axioms", ["lake", "env", "lean", "-DwarningAsError=true", "Audit.lean"], 120),
    ]:
        result = command(label + "-" + name, argv, timeout)
        results.append(result)
        expect_green(result)
    file.write_text(PROBE.replace("EXPECTED_BOOL", expected), encoding="utf-8")
    result = command(label + "-admit", ["lake", "env", "lean", "-DwarningAsError=true", str(file)])
    results.append(result)
    expect_green(result)
    output = (OUT / (label + "-admit.stdout.log")).read_text()
    if f"env.present=false, admitted={expected}" not in output:
        raise RuntimeError(f"{label}: expected explicit decision witness not present in Lean output")
    ledger[label] = {"expected_admitted": expected, "commands": results}


def run_type_prototype(folder: Path, ledger: dict) -> None:
    good = folder / "ReaderCertificateGood.lean"
    bad = folder / "ReaderCertificateBad.lean"
    good.write_text(TYPE_GOOD, encoding="utf-8")
    bad.write_text(TYPE_BAD, encoding="utf-8")
    a = command("type-good", ["lake", "env", "lean", "-DwarningAsError=true", str(good)])
    b = command("type-bad", ["lake", "env", "lean", "-DwarningAsError=true", str(bad)])
    badoutput = (OUT / "type-bad.stdout.log").read_text() + (OUT / "type-bad.stderr.log").read_text()
    ledger["type_prototype"] = {"construct_true": a, "construct_false": b}
    expect_green(a)
    if b["exit"] == 0 or "error:" not in badoutput or "ReaderCertificateBad.lean" not in badoutput:
        raise RuntimeError("certificate counterexample did not fail at expected Lean source")


def main() -> int:
    OUT.mkdir(exist_ok=True)
    original = SOURCE.read_bytes()
    text = original.decode("utf-8")
    ledger: dict = {
        "schema": "AO-RR-001-v1", "status": "INCOMPLETE",
        "source": "IntrospectionTwin/Witness.lean",
        "original_sha256": sha(original),
        "mutant": "fabricate a clean ReplayWitness for an absent declaration",
        "claim_ceiling": "Source mutation survival is not an independently verified kernel replay or a runtime refinement proof",
    }
    try:
        if text.count(OLD) != 1:
            raise RuntimeError(f"ambiguous mutation anchor, count={text.count(OLD)}")
        # Original and mutant use identical invocation, with complete clean rebuilds.
        with tempfile.TemporaryDirectory(prefix="ao-rr-", dir=ROOT) as tmp:
            probe = Path(tmp) / "AdmissionProbe.lean"
            phase("baseline", "false", probe, ledger)
            mutated = text.replace(OLD, NEW, 1).encode("utf-8")
            SOURCE.write_bytes(mutated)
            ledger["mutant_sha256"] = sha(mutated)
            phase("mutant", "true", probe, ledger)
            run_type_prototype(Path(tmp), ledger)
        ledger["status"] = "PASS"
    except Exception as error:
        ledger["status"] = "FAIL"
        ledger["error"] = repr(error)
        ledger["traceback"] = traceback.format_exc()
    finally:
        SOURCE.write_bytes(original)
        ledger["source_restored"] = sha(SOURCE.read_bytes()) == sha(original)
        if not ledger["source_restored"]:
            ledger["status"] = "FAIL"
        (OUT / "AO-RR-001.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(f"AO-RR-001 {ledger['status']}: baseline={ledger.get('baseline', {}).get('expected_admitted')} "
          f"mutant={ledger.get('mutant', {}).get('expected_admitted')}")
    if ledger["status"] != "PASS":
        print(ledger.get("error", "unknown failure"))
    return 0 if ledger["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
