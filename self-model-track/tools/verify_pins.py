#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.31.0-rc1"
EXPECTED_MATHLIB = "d568c8c09630de097a046763c17b9ea99f95f950"


def verify(root: Path) -> None:
    toolchain = (root / "lean-toolchain").read_text().strip()
    if toolchain != EXPECTED_TOOLCHAIN:
        raise SystemExit(
            f"toolchain pin mismatch: {toolchain!r} != {EXPECTED_TOOLCHAIN!r}"
        )
    lakefile = (root / "lakefile.lean").read_text()
    if lakefile.count(EXPECTED_MATHLIB) != 1:
        raise SystemExit("Mathlib commit pin missing, duplicated, or changed")
    print(f"pin guard PASS: {EXPECTED_TOOLCHAIN}, Mathlib {EXPECTED_MATHLIB}")


if __name__ == "__main__":
    verify(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("."))
