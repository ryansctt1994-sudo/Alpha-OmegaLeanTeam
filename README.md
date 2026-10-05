# Alpha-OmegaLeanTeam

Canonical Lean build and theorem registry for the strongest formally checked
pieces of the project portfolio.

## Current canonical candidate

The review branch currently contains **66 theorem declarations**:

- **31** imported IntrospectionTwin core theorems at source commit
  `fcc63c085497a26bf1468294a3df53fdd6a56c9f`;
- **16** imported Weaver Lattice Core theorems from PR #66 source head
  `b162a7cea43959214bd9e928ea6c9965976cdcc2`;
- **19** new AlphaOmega separation, authority, claim-ceiling, recovery, and
  protected-state theorems.

The root project is pinned to **Lean 4.22.0**.

## What “proved” means here

A theorem is canonical only after this repository's clean CI compiles the pinned
source and audits its transitive axioms. The source guard rejects `sorry`,
`admit`, and new `axiom` declarations. The axiom audit permits only
`propext`, `Quot.sound`, and `Classical.choice` where a theorem actually
depends on them.

That proves the Lean statements in this repository. It does **not** prove that a
runtime implements those statements, that a receipt is authentic across a
process boundary, or that evidence grants authority.

## Build

```bash
lake build
lake env lean -DwarningAsError=true Audit.lean
```

## Corpus

- `AlphaOmega/` — portfolio-wide separation and fail-closed invariants.
- `LatticeCore/` — generic order/meet, attenuation, accumulation, and
  counterexample theorems.
- `IntrospectionTwin/` — receipt promotion, gate soundness, admission, and
  bounded state-transition theorems.
- `Audit.lean` — explicit theorem axiom inventory.
- `PROVENANCE.md` — exact source commits, exclusions, and claim ceilings.
- `FORMALIZATION_BACKLOG.md` — next proof obligations.

## Portfolio posture

Formal proof evidence and operational authority remain separate. A green build
raises confidence in these source-level statements only; production authority
is not implied.
