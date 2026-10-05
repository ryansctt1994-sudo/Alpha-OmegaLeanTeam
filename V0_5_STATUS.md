# Alpha-Omega v0.5 canonical status

Implementation commit:
`5b7e43fafc2cdd823071c46ffd407256129bdb11`

## Trust boundaries

| Boundary | Lean | Theorems | Mutations | Status |
| --- | --- | ---: | ---: | --- |
| Root governance kernel | 4.22.0 | 124 | 11/11 killed | PASS |
| Isolated Mathlib track | 4.31.0-rc1 | 1 | 2/2 killed | PASS |
| Self-model research track | 4.31.0-rc1 | 9 | 2/2 killed | PASS |

The theorem counts are intentionally **not combined**. Each row is a separate
verification/trust boundary.

## v0.5 result

For contractive dynamics with Lipschitz factor `L < 1` and a boundary/model
map with Lipschitz constant `K`, the research track proves:

```text
trackingDrift(n) ≤ K * dist(x₀, f x₀) * L^n
```

It also proves the right-hand side tends to zero and that actual tracking drift
tends to zero.

## Counterexamples

- Expanding dynamics show contractivity cannot simply be omitted.
- Contractive half-dynamics with inverse observation show boundary regularity
  matters.

## Claim ceiling

The v0.5 theorem is a metric-dynamics result. It does not establish
consciousness, personhood, subjective identity, deployed-system persistence,
runtime refinement, or operational authority.
