"""Targeted semantic mutation checks for the v0.3 Lean modules."""

from __future__ import annotations

import subprocess
import tempfile
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


def main() -> None:
    killed = 0
    with tempfile.TemporaryDirectory(prefix="alpha-omega-mutations-") as tmp:
        out = Path(tmp)
        for name, path, old, new in CASES:
            source = path.read_text()
            if source.count(old) != 1:
                raise SystemExit(
                    f"{name}: expected exactly one mutation target in {path}, "
                    f"found {source.count(old)}"
                )
            mutant = source.replace(old, new, 1)
            mutant_path = out / f"{name}.lean"
            mutant_path.write_text(mutant)
            run = subprocess.run(
                ["lake", "env", "lean", "-DwarningAsError=true", str(mutant_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if run.returncode == 0:
                raise SystemExit(f"{name}: SURVIVED (mutated semantics still compiled)")
            killed += 1
            print(f"{name}: KILLED")

    if killed != len(CASES):
        raise SystemExit(f"expected {len(CASES)} killed mutants, got {killed}")
    print(f"mutation controls PASS: {killed}/{len(CASES)} killed")


if __name__ == "__main__":
    main()
