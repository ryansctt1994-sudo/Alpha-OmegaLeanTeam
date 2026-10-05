# Alpha-OmegaLeanTeam

Canonical Lean build and theorem registry for the strongest formally checked
pieces of the project portfolio.

## Current canonical baseline

`main` is **Alpha-Omega v0.5**, implementation commit
`5b7e43fafc2cdd823071c46ffd407256129bdb11`.

The canonical corpus contains **124 theorem declarations**:

- **31** imported IntrospectionTwin core theorems;
- **16** imported Weaver Lattice Core theorems;
- **19** v0.1 AlphaOmega separation/authority/recovery/protected-state theorems;
- **6** nontrivial union-transition theorems over explicit pre/post states;
- **13** Weaver recovery/replacement theorems;
- **8** typed Evidence × Authority foundation theorems;
- **18** Evidence × Authority ↔ LatticeCore integration, promotion, cap, and demotion theorems;
- **13** AO-HISTORY-v1 append-only, ancestry, admission, and rejection-invariance theorems.

The root project is pinned to **Lean 4.22.0**.

The root governance corpus remains at **124 theorem declarations** on Lean 4.22.0 and requires **11/11 targeted semantic mutations** to fail. v0.4 keeps a separately verified one-theorem Mathlib track with **2/2 isolated mutations killed**. v0.5 adds a third, separate self-model research boundary with **9 theorem declarations** and **2/2 research mutations killed**.

## Isolated Mathlib track

`mathlib-track/` is a separate trust boundary, not an extension of the root
124-theorem inventory.

It pins:

- Lean `v4.31.0-rc1`;
- Lean Linux release SHA-256
  `055f1780f20f9774bbe270d5d4cf7561fb26ee6734c0917ba6cfb867e33cb99e`;
- Mathlib
  `d568c8c09630de097a046763c17b9ea99f95f950`;
- upstream theorem source
  `Math_Build1994@41d2c9ae8a362a79de4f95733adf0fd8b53a151c`.

The track currently contains exactly one theorem:

`MathBuild.sqrt2_irrational_real : Irrational (Real.sqrt 2)`

It is checked by the separate **Isolated Mathlib track** workflow. A failure in
that workflow does not change the root theorem count or root Lean 4.22.0
verification result.

## Quantitative self-model research track

`self-model-track/` is a third trust boundary. It does **not** increase the
root 124-theorem count and does **not** change the v0.4 one-theorem Mathlib
track.

It proves, over general pseudometric spaces and discrete-time dynamics, that if:

- world updates are Lipschitz with factor `L < 1`; and
- the boundary/model map is Lipschitz with constant `K`;

then successive observed self-model drift is bounded by:

```text
K * dist(x₀, f x₀) * L^n
```

The bound and the actual tracking drift both tend to zero. Two explicit
counterexamples and two hostile hypothesis-removal mutations are included.

The interpretation is mathematical only: no consciousness, personhood,
subjective identity, or deployed-system persistence claim is inferred.

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
- `mathlib-track/` — isolated newer Lean/Mathlib theorem track with its own
  pins, audit, provenance, and mutations.
- `self-model-track/` — isolated quantitative persistence research track with
  its own pins, audit, counterexamples, and mutations.
- `FORMALIZATION_BACKLOG.md` — issue-backed next proof obligations.

## Portfolio posture

Formal proof evidence and operational authority remain separate. A green build
raises confidence in these source-level statements only; production authority
is not implied.
