#!/usr/bin/env python3
"""Negative controls for the isolated Mathlib theorem track."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN_GUARD = ROOT / "tools" / "verify_pins.py"
THEOREM = ROOT / "MathBuild" / "IrrationalSqrt2.lean"
LAKEFILE = ROOT / "lakefile.lean"
TOOLCHAIN = ROOT / "lean-toolchain"
MATHLIB_PIN = "d568c8c09630de097a046763c17b9ea99f95f950"


def unresolved_proof_must_fail() -> None:
    source = THEOREM.read_text()
    old = "  simpa using irrational_sqrt_two"
    new = "  exact alphaOmegaDeliberatelyMissingProof"
    if source.count(old) != 1:
        raise SystemExit("theorem mutation target missing or ambiguous")

    with tempfile.TemporaryDirectory(prefix="mathlib-proof-mutant-") as tmp:
        path = Path(tmp) / "IrrationalSqrt2Mutation.lean"
        path.write_text(source.replace(old, new, 1))
        run = subprocess.run(
            ["lake", "env", "lean", "-DwarningAsError=true", str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=180,
        )
        if run.returncode == 0:
            raise SystemExit("unresolved-proof mutation SURVIVED")
        print("unresolved-proof mutation KILLED")


def changed_pin_must_fail_guard() -> None:
    lakefile = LAKEFILE.read_text()
    if lakefile.count(MATHLIB_PIN) != 1:
        raise SystemExit("pin mutation target missing or ambiguous")

    with tempfile.TemporaryDirectory(prefix="mathlib-pin-mutant-") as tmp:
        root = Path(tmp)
        (root / "lean-toolchain").write_text(TOOLCHAIN.read_text())
        (root / "lakefile.lean").write_text(
            lakefile.replace(MATHLIB_PIN, "0" * 40, 1)
        )
        run = subprocess.run(
            ["python3", str(PIN_GUARD), str(root)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if run.returncode == 0:
            raise SystemExit("changed-Mathlib-pin mutation SURVIVED")
        print("changed-Mathlib-pin mutation KILLED")


def main() -> None:
    unresolved_proof_must_fail()
    changed_pin_must_fail_guard()
    print("mathlib-track mutations PASS: 2/2 killed")


if __name__ == "__main__":
    main()
