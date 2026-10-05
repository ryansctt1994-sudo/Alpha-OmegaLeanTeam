# Formalization backlog

Nothing is counted as proved merely because it is listed here. Canonical work is
tracked by GitHub issues using **statement → assumptions → required artifact →
falsification test → promotion condition**.

## Completed

- #2 — nontrivial union transition preservation. **Completed** in canonical
  Alpha-Omega and repaired upstream in `lean-workers-union`.
- #3 — Weaver recovery and replacement semantics. **Completed** at the
  source-model claim ceiling.
- #4 — typed Evidence × Authority ↔ LatticeCore integration. **Completed** in
  v0.2+ at `bae0bb53ab33ba8d4bb4d84a85ce5cff30b676b6`:
  - `LatticeCore.MeetOrder` instance;
  - cap deflationarity / monotonicity / idempotence;
  - cap monotonicity in constraint parameters;
  - meet-based demotion with lower-tier preservation;
  - proof-carrying promotion requiring minimum evidence, verified witness,
    green checks, and separate authority grant;
  - governed promotion proven unable to exceed evidence or authority caps;
  - cap-bypass and missing-grant hostile mutations killed.

- #5 — AO-HISTORY-v1 tamper-evident history extension. **Completed** in v0.3 at `396706c7f9ab24bf3cca1505e018664cc093fd53`: frozen digest contract, 13 Lean theorems, 11/11 mutation controls, and post-merge main CI green.

- #6 — isolated Mathlib theorem subproject. **Completed** in v0.4 at
  `58c51f3cfaf02933bd0c26f98655a7a9dd04866e`:
  - root Lean 4.22.0 / 124-theorem boundary unchanged and independently green;
  - isolated Lean `v4.31.0-rc1` release checksum pinned;
  - Mathlib commit `d568c8c09630de097a046763c17b9ea99f95f950` resolved exactly;
  - upstream theorem source pinned to Math_Build1994 commit/blob;
  - one isolated theorem declaration builds and passes axiom audit;
  - unresolved-proof and changed-pin mutants killed 2/2;
  - isolated post-merge main CI green.

## Active v0.5 — issue #7

- New isolated `self-model-track/` research boundary.
- General pseudometric spaces; discrete-time dynamics.
- Explicit `ContractiveDynamics` hypothesis with Lipschitz factor `L < 1`.
- Explicit `BoundaryModel` hypothesis with Lipschitz constant `K`.
- Quantitative drift envelope:
  `K * dist(x₀, f x₀) * L^n`.
- Main research obligations:
  - geometric world-step bound;
  - geometric boundary/self-model drift bound;
  - quantitative persistence predicate;
  - envelope tends to zero;
  - actual tracking drift tends to zero.
- Counterexamples:
  - expanding dynamics admit no factor below one;
  - contractive half-dynamics with inverse observation violate boundary regularity
    and show increasing observed drift.
- Hostile controls remove contractivity and boundary Lipschitz continuity.

Issue #7 closes only after the 9-theorem research build, axiom audit, 2/2
mutation controls, root 124-theorem workflow, and post-merge verification all
pass.

## Deliberately withheld

- Whole-system correctness.
- Runtime refinement of Lean models to Python/Rust executors.
- Cryptographic authenticity from hash equality alone.
- Independent reproduction claims not backed by an independent run.
- Production authority.
