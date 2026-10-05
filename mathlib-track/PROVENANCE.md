# Mathlib Track Provenance

Status: isolated theorem track for Alpha-Omega v0.4.

This directory is a **separate Lean/Lake trust boundary**. It does not change,
extend, or reclassify the root Lean 4.22.0 governance corpus.

## Upstream source

Repository: `ryansctt1994-sudo/Math_Build1994`  
Source commit: `41d2c9ae8a362a79de4f95733adf0fd8b53a151c`

Pinned source artifacts:

- `lean-toolchain`
  - blob SHA: `8c7e931aab0179018e3e987d8395daa4466fc3aa`
  - value: `leanprover/lean4:v4.31.0-rc1`
- `lakefile.lean`
  - blob SHA: `14525ef831661111106b26e9ee869140819da87e`
  - Mathlib commit:
    `d568c8c09630de097a046763c17b9ea99f95f950`
- `MathBuild/IrrationalSqrt2.lean`
  - blob SHA: `d0e5e997327619231ed9a7039f6ca4295a7195a7`

The theorem source is copied verbatim from that upstream blob:

`MathBuild.sqrt2_irrational_real : Irrational (Real.sqrt 2)`

with proof reuse through Mathlib's maintained `irrational_sqrt_two`.

## Isolation rule

CI acquires the Lean 4.31.0-rc1 Linux release archive directly and verifies
release SHA-256
`055f1780f20f9774bbe270d5d4cf7561fb26ee6734c0917ba6cfb867e33cb99e`
before extraction. `lake update` then resolves the exact Mathlib revision and
the workflow checks the generated manifest contains the required commit.

The root repository remains pinned to Lean 4.22.0 and its canonical theorem
inventory remains 124 declarations.

The theorem in this directory is counted only in the **Mathlib track**. It is
not added to the root 124-theorem source inventory and is verified by a separate
workflow.

## Proof meaning

A successful build establishes that the copied theorem elaborates and is kernel
checked in the pinned Lean + Mathlib environment.

It is theorem reuse. It is not an independent re-derivation of the irrationality
of √2 and is not evidence of runtime correctness, governance authority, or
production safety.
