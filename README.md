# Alpha-OmegaLeanTeam

Canonical Lean build and theorem registry for the strongest formally checked
pieces of the project portfolio.

## Current canonical baseline

`main` v0.1 contains **66 theorem declarations** and is green under Lean 4.22.0.

## v0.2 candidate

Branch `formal/v0.2-transition-recovery` raises the candidate corpus to
**93 theorem declarations** by adding:

- **6 nontrivial union-transition theorems** over explicit pre/post member states;
- **13 Weaver recovery/replacement theorems** covering consumed IDs,
  indeterminate recovery, no automatic redispatch, exact replacement binding,
  distinct replacement IDs, and reconciliation/duplicate-effect-waiver basis;
- **8 typed Evidence × Authority theorems** covering product-order meet,
  evidence growth without authority growth, and authority caps;
- **6 targeted semantic mutation controls** that must all fail Lean after the
  corresponding invariant is removed.

The root project remains pinned to **Lean 4.22.0**.

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
python3 tools/check_v02_mutations.py
lake env lean -DwarningAsError=true Audit.lean
```

## Corpus

- `AlphaOmega/` — portfolio-wide separation, transition, recovery, and
  evidence/authority invariants.
- `LatticeCore/` — generic order/meet, attenuation, accumulation, and
  counterexample theorems.
- `IntrospectionTwin/` — receipt promotion, gate soundness, admission, and
  bounded state-transition theorems.
- `Audit.lean` — explicit theorem axiom inventory.
- `PROVENANCE.md` — exact source origins, exclusions, and claim ceilings.
- `FORMALIZATION_BACKLOG.md` — issue-backed next proof obligations.

## Portfolio posture

Formal proof evidence and operational authority remain separate. A green build
raises confidence in these source-level statements only; production authority
is not implied.
