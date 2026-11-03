# AO-MUT-001 — Fail-Closed Mutation Oracle

Based on `main` commit `01e3291f643b7742464fccbb798310a4513bd67c`.

## Positive control and receipts

After the pinned root `lake build`, `tools/check_v02_mutations.py` compiles each unmodified source at its mutant's exact temporary path using the same `lake env lean -DwarningAsError=true` invocation. If any original fails, the whole campaign is `HARNESS_FAILURE`, and no mutant is executed or counted.

For a mutant to count as `KILLED`, the oracle requires a nonzero exit and a Lean error diagnostic located within the predeclared theorem's source span. Otherwise the result is `SURVIVED` or `INCONCLUSIVE`. The oracle records baseline/mutant source SHA-256, stdout, stderr, exit codes, target theorem, source span and error locations to `mutation-witness-ledger.json`, uploaded by CI even on failure.

Offline tests include an always-green checker, broken baseline, missing import diagnostic, unrelated file error, ambiguous target, and stderr custody.

## New IntrospectionTwin gate target

The new `gate-drops-kernel-accepted` mutant removes the `kernelAccepted` predicate from `IntrospectionTwin.evaluateGate` without modifying `evaluateGate_sound`.

This is a specification-sensitivity control. A killed mutant does **not** prove that `synthesizeWitness` reads genuinely replayed kernel proof evidence or that a real runtime's reader and decision path refine the Lean model. These properties require separate implementation-level witness observation and adversarial replay.

## Boundary of the claim

Even theorem-local compilation errors are only diagnostic witnesses. They can reflect elaboration or proof-script fragility rather than the logical falsity of the mutated property. This release does not assert full corpus mutation coverage or independent runtime refinement.
