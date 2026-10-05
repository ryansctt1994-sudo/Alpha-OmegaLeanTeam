#!/usr/bin/env python3
"""Hostile controls for the self-model persistence research track."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "SelfModelTrack" / "Persistence.lean"

CASES = [
    (
        "drop-contractivity",
        "  factor_lt_one : factor < 1",
        "  factor_lt_one : True",
    ),
    (
        "drop-boundary-lipschitz",
        "  lipschitz : LipschitzWith constant observe",
        "  lipschitz : True",
    ),
]


def main() -> None:
    source = SOURCE.read_text()
    killed = 0
    with tempfile.TemporaryDirectory(prefix="self-model-mutants-") as tmp:
        out = Path(tmp)
        for name, old, new in CASES:
            if source.count(old) != 1:
                raise SystemExit(
                    f"{name}: expected exactly one mutation target, "
                    f"found {source.count(old)}"
                )
            mutant = source.replace(old, new, 1)
            path = out / f"{name}.lean"
            path.write_text(mutant)
            run = subprocess.run(
                ["lake", "env", "lean", "-DwarningAsError=true", str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=180,
            )
            if run.returncode == 0:
                raise SystemExit(f"{name}: SURVIVED")
            killed += 1
            print(f"{name}: KILLED")

    print(f"self-model mutations PASS: {killed}/{len(CASES)} killed")


if __name__ == "__main__":
    main()
