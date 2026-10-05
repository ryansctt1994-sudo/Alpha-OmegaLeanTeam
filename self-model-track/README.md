# Quantitative Self-Model Persistence Research Track

This is an isolated Mathlib-backed research package for issue #7.

## Choice of model

- **General pseudometric spaces**, not only Euclidean space.
- **Discrete time**, not differential dynamics.
- Contractivity and boundary continuity are explicit hypotheses.
- Persistence is metric drift control, not a phenomenological claim.

## Main bound

For contractive world dynamics with factor `L < 1` and a boundary/model map
with Lipschitz constant `K`, the successive observed drift satisfies:

```text
drift(n) ≤ K * dist(x₀, f x₀) * L^n
```

The geometric bound tends to zero, and the actual tracking drift is proved to
tend to zero by squeezing.

## Counterexamples

- An expanding map shows why contractivity cannot simply be dropped.
- A contractive half-map paired with inverse observation shows why boundary
  regularity matters.

## Boundary

This package is not part of the root 124-theorem Lean 4.22 governance corpus.
It is also separate from the v0.4 one-theorem Mathlib track.
