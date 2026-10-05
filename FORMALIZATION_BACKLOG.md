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

- #7 — quantitative self-model persistence research track. **Completed** in
  v0.5 at `5b7e43fafc2cdd823071c46ffd407256129bdb11`:
  - separate `self-model-track/` trust boundary;
  - general pseudometric spaces and discrete-time dynamics;
  - 9 kernel-checked research theorem declarations;
  - explicit contractivity and boundary-Lipschitz hypotheses;
  - geometric drift bound and asymptotic drift-to-zero theorem;
  - expanding-dynamics and inverse-boundary counterexamples;
  - contractivity-removal and boundary-continuity-removal mutants killed 2/2;
  - root 124-theorem workflow and research workflow both green post-merge.

## Deliberately withheld

- Whole-system correctness.
- Runtime refinement of Lean models to Python/Rust executors.
- Cryptographic authenticity from hash equality alone.
- Independent reproduction claims not backed by an independent run.
- Production authority.


## v0.6 refinement program

- #18 — AO-HISTORY runtime forward-simulation contract freeze. **Completed** at
  `e7fb0be1713ce6cba94166e2234ebb8d16025081`.
  - exact abstract and concrete artifacts pinned;
  - `R_ok`, `alpha`, assumptions A–F, seven transition labels, stutter/reject
    policy, excluded surface, two boundary witnesses, eight mutants, and the
    exact permitted future claim sentence frozen;
  - no correspondence proof was claimed by closing #18.

- #20 — AO-HISTORY named-step forward simulation. **Active**.
  - implement the frozen abstraction and labeled step relation;
  - prove append/reject/stutter correspondence for the seven encoded labels;
  - replay against the real pinned Weaver verifier/runtime;
  - demonstrate EX-1/EX-2;
  - kill MU-1 through MU-7 and fail MU-8 at the source-binding gate;
  - keep the root Lean 4.22.0 / 124-theorem governance boundary independently
    green.

The current claim ceiling remains v0.5 until #20 satisfies the frozen v0.6
promotion gate.
