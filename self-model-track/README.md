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

This is a standard Banach-style contraction estimate transported through a
Lipschitz observation map, **not a novel mathematical persistence theorem**.
The contribution is a Lean formulation with inspectable hypotheses and
counterexamples. Vanishing successive drift does not, by itself, prove that
the entire orbit has a limit in the space. A separate completeness hypothesis
is needed for the usual fixed-point convergence result. For example, on the
incomplete space `(0,1)` the map `x ↦ (x+1)/2` is a contraction whose iterates
approach `1`, a point outside that space. This example is described here, not
yet formalized as an additional Lean counterexample.

## Counterexamples

- An expanding map shows why contractivity cannot simply be dropped.
- A contractive half-map paired with inverse observation shows why boundary
  regularity matters.

## Boundary

This package is not part of the root 124-theorem Lean 4.22 governance corpus.
It is also separate from the v0.4 one-theorem Mathlib track.
