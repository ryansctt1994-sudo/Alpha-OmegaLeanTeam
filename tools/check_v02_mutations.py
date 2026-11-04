"""Targeted semantic mutation checks for the v0.3 Lean modules."""

from __future__ import annotations

import subprocess
import tempfile
import os
import re
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    (
        "union-identity-rewrite",
        ROOT / "AlphaOmega" / "UnionTransition.lean",
        """  { before with
    role := nextRole
""",
        """  { before with
    identity := { before.identity with repo := before.identity.repo ++ "/mutated" }
    role := nextRole
""",
    ),
    (
        "recovery-leaves-id-unconsumed",
        ROOT / "AlphaOmega" / "RecoveryReplacement.lean",
        "{ r with consumed := true, outcome := .indeterminate }",
        "{ r with consumed := false, outcome := .indeterminate }",
    ),
    (
        "recovery-fabricates-pass",
        ROOT / "AlphaOmega" / "RecoveryReplacement.lean",
        "{ r with consumed := true, outcome := .indeterminate }",
        "{ r with consumed := true, outcome := .pass }",
    ),
    (
        "replacement-allows-same-id",
        ROOT / "AlphaOmega" / "RecoveryReplacement.lean",
        "  auth.replacementRequestId ≠ original.requestId ∧\n",
        "  True ∧\n",
    ),
    (
        "replacement-drops-resolution-basis",
        ROOT / "AlphaOmega" / "RecoveryReplacement.lean",
        "  auth.replacementRequestId ≠ original.requestId ∧\n  ∃ basis, auth.basis = some basis",
        "  auth.replacementRequestId ≠ original.requestId",
    ),
    (
        "evidence-silently-raises-authority",
        ROOT / "AlphaOmega" / "EvidenceAuthority.lean",
        "  { s with evidence := Nat.max s.evidence newEvidence }",
        "  { evidence := Nat.max s.evidence newEvidence, authority := s.authority + 1 }",
    ),
    (
        "governed-promotion-bypasses-cap",
        ROOT / "AlphaOmega" / "PortfolioLattice.lean",
        "  portfolioCap c (promote s p h)",
        "  promote s p h",
    ),
    (
        "promotion-drops-authority-grant",
        ROOT / "AlphaOmega" / "PortfolioLattice.lean",
        "  p.authorityGranted = true\n",
        "  True\n",
    ),
    (
        "history-drops-prev-link",
        ROOT / "AlphaOmega" / "History.lean",
        "  HashValid hash e ∧ LinkValid h e ∧ IndexValid h e",
        "  HashValid hash e ∧ True ∧ IndexValid h e",
    ),
    (
        "history-prepends-instead-of-appends",
        ROOT / "AlphaOmega" / "History.lean",
        "  { entries := h.entries ++ [e], head := e.eventDigest }",
        "  { entries := [e] ++ h.entries, head := e.eventDigest }",
    ),
    (
        "rejection-mutates-protected-head",
        ROOT / "AlphaOmega" / "History.lean",
        "def reject (h : History) (_e : Entry) : History :=\n  h",
        "def reject (h : History) (e : Entry) : History :=\n  appendEntry h e",
    ),
]



# Case metadata identifies the intended theorem, not merely the changed source.
EXPECTED = {
    "union-identity-rewrite": "apply_preserves_identity",
    "recovery-leaves-id-unconsumed": "recover_unclosed_consumes_id",
    "recovery-fabricates-pass": "recover_unclosed_is_indeterminate",
    "replacement-allows-same-id": "replacement_requires_distinct_id",
    "replacement-drops-resolution-basis": "replacement_requires_resolution_basis",
    "evidence-silently-raises-authority": "addEvidence_preserves_authority",
    "governed-promotion-bypasses-cap": "governed_promotion_is_capped",
    "promotion-drops-authority-grant": "promotion_requires_authority_grant",
    "history-drops-prev-link": "admissible_prev_matches_head",
    "history-prepends-instead-of-appends": "append_entries_prefix",
    "rejection-mutates-protected-head": "rejection_preserves_history",
    "gate-drops-kernel-accepted": "evaluateGate_sound",
}

CASES.append((
    "gate-drops-kernel-accepted",
    ROOT / "IntrospectionTwin" / "Gate.lean",
    "   | some w => w.clean c.allowedAxioms",
    "   | some w => w.isTheorem && (w.sorryCount == 0) &&\n"
    "     w.usedAxioms.all (c.allowedAxioms.contains ·)",
))

LEDGER = Path(os.environ.get("MUTATION_LEDGER_PATH", ROOT / "mutation-witness-ledger.json"))
DECL = re.compile(r"(?m)^[ \t]*(theorem|lemma|def|structure|inductive|instance|abbrev|namespace|end)\b(?:[ \t]+([^\s:(]+))?")
ERROR = re.compile(r"(?m)^(?P<path>[^\n]*?\.lean):(?P<line>\d+):(?P<col>\d+):\s*error:")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def theorem_span(source: str, theorem: str) -> tuple[int, int]:
    declarations = [
        (source.count("\n", 0, m.start()) + 1, m.group(1), m.group(2))
        for m in DECL.finditer(source)
    ]
    selected = [(i, line) for i, (line, kind, name) in enumerate(declarations)
                if kind in ("theorem", "lemma") and name == theorem]
    if len(selected) != 1:
        raise RuntimeError(f"{theorem}: expected one theorem, found {len(selected)}")
    i, line = selected[0]
    end = declarations[i + 1][0] - 1 if i + 1 < len(declarations) else source.count("\n") + 1
    return line, end


def theorem_errors(output: str, file: Path, span: tuple[int, int]) -> list[dict]:
    errors = []
    for m in ERROR.finditer(output):
        p = Path(m.group("path"))
        if p != file and p.resolve() != file.resolve():
            continue
        line = int(m.group("line"))
        if span[0] <= line <= span[1]:
            message = output[m.end():].split("\n", 1)[0].strip()
            errors.append({"line": line, "column": int(m.group("col")), "message": message[:500]})
    return errors


def invoke(file: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", "-DwarningAsError=true", str(file)],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )


def main() -> int:
    ledger: dict = {
        "schema": "ao-mut-001-v1", "status": "INCOMPLETE",
        "criterion": "all original-source invocations green, then theorem-local Lean failures",
        "cases": [],
    }
    try:
        with tempfile.TemporaryDirectory(prefix="alpha-omega-mutations-") as tmp:
            folder = Path(tmp)
            prepared = []
            # C5 POSITIVE CONTROL: establish every original in the identical file
            # and invocation used for its mutant, BEFORE counting any kills.
            for name, path, old, new in CASES:
                source = path.read_text(encoding="utf-8")
                if source.count(old) != 1:
                    raise RuntimeError(f"{name}: expected one source target, found {source.count(old)}")
                mutant = source.replace(old, new, 1)
                theorem = EXPECTED[name]
                span = theorem_span(mutant, theorem)
                file = folder / (name + ".lean")
                file.write_text(source, encoding="utf-8")
                base = invoke(file)
                entry = {
                    "name": name, "source": str(path.relative_to(ROOT)), "theorem": theorem,
                    "theorem_span": span,
                    "baseline_sha256": sha(source), "mutant_sha256": sha(mutant),
                    "baseline_exit": base.returncode,
                    "baseline_stdout": base.stdout[-6000:],
                    "baseline_stderr": base.stderr[-6000:],
                    "status": "BASELINE_PASS" if base.returncode == 0 else "HARNESS_FAILURE",
                }
                ledger["cases"].append(entry)
                if base.returncode != 0:
                    raise RuntimeError(f"{name}: baseline red ({base.returncode}); no mutant kills counted")
                prepared.append((name, file, mutant, theorem, entry))

            for name, file, mutant, theorem, entry in prepared:
                file.write_text(mutant, encoding="utf-8")
                run = invoke(file)
                errors = theorem_errors(run.stdout + "\n" + run.stderr,
                                        file, theorem_span(mutant, theorem))
                entry.update({
                    "mutant_exit": run.returncode,
                    "mutant_stdout": run.stdout[-6000:],
                    "mutant_stderr": run.stderr[-6000:],
                    "theorem_errors": errors,
                })
                if run.returncode == 0:
                    entry["status"] = "SURVIVED"
                elif errors:
                    entry["status"] = "KILLED"
                else:
                    entry["status"] = "INCONCLUSIVE"
                print(f"{name}: {entry['status']} ({theorem})", flush=True)

            failed = [r["name"] for r in ledger["cases"] if r["status"] != "KILLED"]
            ledger["failed_cases"] = failed
            ledger["status"] = "PASS" if not failed else "FAIL"
    except (OSError, subprocess.TimeoutExpired, RuntimeError, ValueError) as error:
        ledger["status"] = "HARNESS_FAILURE"
        ledger["error"] = f"{type(error).__name__}: {error}"
    finally:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"mutation oracle {ledger['status']}: {LEDGER}", flush=True)
    return 0 if ledger["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
