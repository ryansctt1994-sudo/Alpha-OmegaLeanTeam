# Formalization backlog

Nothing is counted as proved merely because it is listed here. Canonical work is
tracked by GitHub issues using **statement → assumptions → required artifact →
falsification test → promotion condition**.

## Completed in v0.2

- #2 — nontrivial union transition preservation. **Completed** in canonical
  Alpha-Omega and repaired upstream in `lean-workers-union`.
- #3 — Weaver recovery and replacement semantics. **Completed** at the
  source-model claim ceiling.

## Active v0.2+ — issue #4

Typed Evidence × Authority foundation is already proved. The remaining
LatticeCore integration is split into explicit sub-obligations:

1. **LatticeCore instance**
   - instantiate `LatticeCore.MeetOrder` for `EvidenceAuthority.Level`;
   - reuse `restrict` as the canonical portfolio ceiling operator;
   - prove cap deflationarity, monotonicity, and idempotence through the generic
     LatticeCore theorems.

2. **Portfolio constraints**
   - type evidence and authority ceilings separately;
   - prove portfolio caps are monotone in weaker/stronger constraint parameters;
   - prove a lower authority tier remains supported when it is below both the
     current authority and the demotion ceiling.

3. **Explicit promotion**
   - define a proof-carrying promotion request requiring minimum evidence,
     verified witness, green checks, and a separate authority grant;
   - prove each gate is necessary;
   - prove promotion preserves evidence and cannot decrease authority.

4. **Governed promotion**
   - compose explicit promotion with the portfolio cap;
   - prove even an authorized promotion cannot exceed the evidence or authority
     ceiling.

5. **Falsification**
   - mutate governed promotion to bypass the cap;
   - mutate the promotion authorization predicate to drop the authority grant;
   - both mutants must fail the canonical verification gate.

Issue #4 closes only when all five sub-obligations are kernel checked, audited,
mutation-sensitive, and merged.

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
