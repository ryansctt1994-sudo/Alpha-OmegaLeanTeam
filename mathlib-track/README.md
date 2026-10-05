# Isolated Mathlib Track

This sibling Lake package exists so newer Mathlib-dependent mathematics can be
verified without changing the Alpha-Omega root governance toolchain.

## Pinned environment

- Lean: `v4.31.0-rc1`
- Mathlib:
  `d568c8c09630de097a046763c17b9ea99f95f950`
- Upstream theorem source:
  `Math_Build1994@41d2c9ae8a362a79de4f95733adf0fd8b53a151c`

## Current theorem inventory

Exactly one theorem is currently admitted to this track:

- `MathBuild.sqrt2_irrational_real : Irrational (Real.sqrt 2)`

## Build

```bash
cd mathlib-track
python3 tools/verify_pins.py .
lake build MathBuild
lake env lean -DwarningAsError=true Audit.lean
python3 tools/check_mutations.py
```

## Boundary

The root Lean 4.22.0 theorem corpus is independent of this package. A Mathlib
track failure does not alter the root theorem inventory or its canonical CI
result.
