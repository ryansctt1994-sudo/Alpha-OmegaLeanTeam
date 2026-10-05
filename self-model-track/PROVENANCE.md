# Self-Model Persistence Track Provenance

Status: isolated research track for Alpha-Omega v0.5.

## Source search

Before formalizing this track, the connected GitHub repositories were searched
for prior Lean sources matching:

- `PersistentSelfModel`
- `BoundaryGeometry`
- `QuantitativePersistence`
- `IdentityThroughChange`
- contractive tracking
- boundary continuity

No pinned prior Lean source implementing those named objects was recovered from
the indexed repositories. The v0.5 theorem source is therefore a new
formalization of the continuity sketch rather than an imported theorem corpus.

## Trust boundary

This directory is a separate Lean/Lake research boundary.

Pinned environment:

- Lean: `leanprover/lean4:v4.31.0-rc1`
- Lean Linux release SHA-256:
  `055f1780f20f9774bbe270d5d4cf7561fb26ee6734c0917ba6cfb867e33cb99e`
- Mathlib:
  `d568c8c09630de097a046763c17b9ea99f95f950`

It does not change the root Lean 4.22.0 governance corpus and does not change
the v0.4 one-theorem `mathlib-track/`.

## Mathematical interpretation

The model is discrete-time and general over pseudometric spaces.

- `ContractiveDynamics` supplies an update function with an explicit
  Lipschitz factor strictly below one.
- `BoundaryModel` supplies an observation/model map with an explicit
  Lipschitz constant.
- `trackingDrift` is the metric distance between successive observed
  self-model states.
- `driftBound` is the geometric envelope
  `K * dist(x₀, f x₀) * L^n`.
- `QuantitativePersistence` means the observed drift is bounded by a supplied
  sequence; it is not a claim about psychological identity.

The main theorems prove that the geometric envelope bounds tracking drift and
that both the envelope and the actual drift tend to zero.

## Counterexamples

The track includes two explicit failure modes:

1. `expandingWorld x = 2x` admits no global Lipschitz factor below one.
2. `halfWorld x = x/2` is contractive, but the inverse observation
   `x ↦ x⁻¹` is not 1-Lipschitz and its observed drift grows on the first two
   steps from the chosen initial state.

These counterexamples are mathematical witnesses that the hypotheses should not
be read as decorative prose.

## Claim ceiling

This research theorem does not establish:

- consciousness;
- personhood;
- subjective continuity;
- persistence of a deployed AI system;
- correctness of any learned representation;
- runtime refinement;
- operational authority.

It proves metric statements about explicitly defined mathematical dynamics.
