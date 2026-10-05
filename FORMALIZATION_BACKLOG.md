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

## Active v0.4 — issue #6

- Isolated sibling Lake package under `mathlib-track/`.
- Lean pin: `v4.31.0-rc1`.
- Mathlib pin: `d568c8c09630de097a046763c17b9ea99f95f950`.
- Upstream theorem source pinned to
  `Math_Build1994@41d2c9ae8a362a79de4f95733adf0fd8b53a151c`.
- The isolated track contains exactly one theorem declaration:
  `MathBuild.sqrt2_irrational_real`.
- Separate workflow owns Mathlib verification; the root Lean 4.22.0 canonical
  workflow and 124-theorem inventory are unchanged.
- Two hostile controls must fail: unresolved proof and changed Mathlib pin.

Issue #6 closes only after the isolated workflow passes on PR and post-merge
main while the canonical root workflow remains independently green.

## Next

- #7 — quantitative self-model persistence research track.

## Deliberately withheld

- Whole-system correctness.
- Runtime refinement of Lean models to Python/Rust executors.
- Cryptographic authenticity from hash equality alone.
- Independent reproduction claims not backed by an independent run.
- Production authority.
