# Alpha-OmegaLeanTeam

Canonical Lean build and theorem registry for the strongest formally checked
pieces of the project portfolio.

## Current canonical baseline

`main` is **Alpha-Omega v0.2+**, commit
`bae0bb53ab33ba8d4bb4d84a85ce5cff30b676b6`.

The canonical corpus contains **111 theorem declarations**:

- **31** imported IntrospectionTwin core theorems;
- **16** imported Weaver Lattice Core theorems;
- **19** v0.1 AlphaOmega separation/authority/recovery/protected-state theorems;
- **6** nontrivial union-transition theorems over explicit pre/post states;
- **13** Weaver recovery/replacement theorems;
- **8** typed Evidence × Authority foundation theorems;
- **18** Evidence × Authority ↔ LatticeCore integration, promotion, cap, and demotion theorems.

The root project is pinned to **Lean 4.22.0**.

v0.2+ requires **8/8 targeted semantic mutations** to fail Lean:
identity rewrite, unconsumed recovery, fabricated PASS, same-ID replacement,
missing resolution basis, evidence-driven authority growth, governed-promotion
cap bypass, and removal of the separate authority-grant requirement.

## What “proved” means here

A theorem is canonical only after this repository's clean CI compiles the pinned
source and audits its transitive axioms. The source guard rejects `sorry`,
`admit`, and new `axiom` declarations. The axiom audit permits only
`propext`, `Quot.sound`, and `Classical.choice` where a theorem actually
depends on them.

That proves the Lean statements in this repository. It does **not** prove that a
runtime implements those statements, that a receipt is authentic across a
process boundary, that recovery storage refines the model, or that evidence
grants authority.

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
