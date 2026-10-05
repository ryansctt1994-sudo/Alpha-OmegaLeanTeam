# Alpha-Omega v0.2+ canonical status

Canonical commit: `bae0bb53ab33ba8d4bb4d84a85ce5cff30b676b6`

## Corpus

- v0.2 baseline: 93 theorem declarations.
- v0.2+ LatticeCore integration: 18 theorem declarations.
- **Canonical total: 111 theorem declarations.**

## Verification

- Lean 4.22.0 pinned build: **PASS**
- Source theorem inventory: **111/111**
- Source `sorry` / `admit` / new `axiom`: **none permitted**
- Explicit axiom audit: **PASS**
- Semantic mutations: **8/8 killed**
- Post-merge `main` workflow: **PASS**

## New v0.2+ properties

- Evidence × Authority is a first-class `LatticeCore.MeetOrder`.
- Portfolio caps are deflationary, monotone, and idempotent.
- Tightening or relaxing constraints is ordered monotonically.
- Meet-based demotion preserves a lower authority tier when the tier is below
  both the current authority and the demotion ceiling.
- Promotion requires minimum evidence, a verified witness, green checks, and a
  separate authority grant.
- Governed promotion cannot exceed either portfolio ceiling.

## Claim ceiling

These are kernel-checked source-model governance properties. They do not grant
operational authority, prove runtime refinement, prove durable storage
correctness, or establish independent external reproduction.
