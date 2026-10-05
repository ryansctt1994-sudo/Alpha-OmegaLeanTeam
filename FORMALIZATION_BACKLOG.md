# Formalization backlog

This is the next-pass queue. Nothing below is counted as proved merely because
it is listed here.

## High priority

- Strengthen the lean-workers-union transition model so the post-state is an
  explicit function/relation of the pre-state, then prove identity preservation
  across that relation instead of proving reflexivity.
- Formalize the Weaver recovery replacement-request rule: an indeterminate
  original request remains consumed, and a replacement requires an explicit
  reconciliation or duplicate-effect waiver.
- Add a typed evidence/authority lattice whose meet and promotion rules encode
  the portfolio claim ceiling directly.
- Formalize hash-chain extension properties for observation history once a
  digest primitive and serialization contract are fixed.
- Add a separate Mathlib subproject for `MathBuild.sqrt2_irrational_real`
  without changing the root Lean 4.22.0 trust boundary.
- Translate the self-model persistence sketch into a nontrivial theorem over a
  metric/order structure rather than a definitional restatement.

## Deliberately withheld

- Whole-system correctness.
- Runtime refinement of Lean models to Python/Rust executors.
- Cryptographic authenticity from hash equality alone.
- Independent reproduction claims not backed by an independent run.
- Production authority.
