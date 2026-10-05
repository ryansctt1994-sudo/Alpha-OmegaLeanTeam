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

## Active v0.3 — issue #5

- AO-HISTORY-v1 serialization/digest contract frozen from committed Weaver Triad ledger semantics.
- Structural Lean model added for append-only prefix preservation, ancestry linkage, digest/index admission, broken-ancestry rejection, and rejection-path protected-head invariance.
- Three hostile mutations added: dropped previous-link check, prepend/reorder behavior, and reject-path head mutation.
- Issue #5 closes only after the 124-theorem build, 11/11 mutation suite, and axiom audit pass on PR and post-merge main.

## Next

- #6 — isolated Mathlib theorem subproject.
- #7 — quantitative self-model persistence research track.

## Deliberately withheld

- Whole-system correctness.
- Runtime refinement of Lean models to Python/Rust executors.
- Cryptographic authenticity from hash equality alone.
- Independent reproduction claims not backed by an independent run.
- Production authority.
