# Alpha-Omega v0.4 canonical status

Implementation commit:
`58c51f3cfaf02933bd0c26f98655a7a9dd04866e`

## Trust boundaries

### Root governance kernel

- Lean: **4.22.0**
- Canonical theorem declarations: **124**
- Root semantic mutations: **11/11 killed**
- Root post-merge main CI: **PASS**
- Toolchain changed by v0.4: **NO**

### Isolated Mathlib track

- Directory: `mathlib-track/`
- Lean: **4.31.0-rc1**
- Lean release archive SHA-256:
  `055f1780f20f9774bbe270d5d4cf7561fb26ee6734c0917ba6cfb867e33cb99e`
- Mathlib:
  `d568c8c09630de097a046763c17b9ea99f95f950`
- Isolated theorem declarations: **1**
- Isolated mutations: **2/2 killed**
- Isolated post-merge main CI: **PASS**

Current isolated theorem:

`MathBuild.sqrt2_irrational_real : Irrational (Real.sqrt 2)`

## Provenance

The theorem source is copied from
`Math_Build1994@41d2c9ae8a362a79de4f95733adf0fd8b53a151c`,
blob `d0e5e997327619231ed9a7039f6ca4295a7195a7`.

It reuses Mathlib's maintained `irrational_sqrt_two`.

## Claim ceiling

The isolated theorem is kernel-checked theorem reuse in a separately pinned
environment. It is not an independent mathematical derivation.

Neither trust boundary establishes runtime refinement, production safety,
operational authority, or independent external reproduction.
