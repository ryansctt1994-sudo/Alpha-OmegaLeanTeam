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

## Next

- #5 — tamper-evident history extension.
- #6 — isolated Mathlib theorem subproject.
- #7 — quantitative self-model persistence research track.

## Deliberately withheld

- Whole-system correctness.
- Runtime refinement of Lean models to Python/Rust executors.
- Cryptographic authenticity from hash equality alone.
- Independent reproduction claims not backed by an independent run.
- Production authority.
