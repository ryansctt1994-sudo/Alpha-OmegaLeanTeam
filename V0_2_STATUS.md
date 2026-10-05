# Alpha-Omega v0.2 canonical status

Canonical commit: `4ca4159afcef1caa0a90a622362d20354a994b4c`

Target delivered: nontrivial transition preservation + fail-closed
recovery/replacement semantics + typed Evidence × Authority foundation.

## Theorem delta

| Area | New theorem declarations |
| --- | ---: |
| Union transition semantics | 6 |
| Recovery/replacement semantics | 13 |
| Evidence × Authority | 8 |
| **Total new** | **27** |
| v0.1 baseline | 66 |
| **v0.2 canonical total** | **93** |

## Passed gates

- Lean 4.22.0 pinned build: **PASS**
- Exactly 93 guarded theorem declarations: **PASS**
- No source `sorry`, `admit`, or new `axiom`: **PASS**
- Six targeted semantic mutations killed: **6/6 PASS**
- Explicit `Audit.lean` axiom inventory: **PASS**
- Approved Lean foundations only: `propext`, `Quot.sound`,
  `Classical.choice`: **PASS**
- Post-merge `main` workflow: **PASS**

## Upstream union repair

`ryansctt1994-sudo/lean-workers-union` was repaired separately and merged at
`e537c7104cf4601fe26eca2531baea9be07faf22`.

Its post-merge Lean 4.22.0 workflow is green and its identity-rewrite negative
control is killed.

## Claim ceiling

These gates qualify the Lean source-model statements only. They do not establish
external runtime refinement, durable storage correctness, cryptographic
authenticity, physical exactly-once effects, independent reproduction, or
operational authority.
