# Alpha-Omega v0.2 candidate status

Target: nontrivial transition preservation + fail-closed recovery/replacement
semantics + typed Evidence × Authority foundation.

## Candidate theorem delta

| Area | New theorem declarations |
| --- | ---: |
| Union transition semantics | 6 |
| Recovery/replacement semantics | 13 |
| Evidence × Authority | 8 |
| **Total new** | **27** |
| v0.1 baseline | 66 |
| **v0.2 candidate total** | **93** |

## Required gates

- Lean 4.22.0 pinned build.
- Exactly 93 theorem declarations under the guarded roots.
- No source `sorry`, `admit`, or new `axiom`.
- Six targeted semantic mutations killed.
- Explicit `Audit.lean` axiom inventory.
- Only approved Lean foundations: `propext`, `Quot.sound`,
  `Classical.choice`.

## Claim ceiling

Passing these gates qualifies the Lean source-model statements only. It does not
establish external runtime refinement, durable storage correctness, cryptographic
authenticity, independent reproduction, or operational authority.
