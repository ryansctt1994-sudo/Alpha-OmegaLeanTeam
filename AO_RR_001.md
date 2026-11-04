# AO-RR-001 — Reader Refinement / Witness Fabrication

**Scope:** adversarial experiment only. No production Lean theorem statements or
proofs are modified on this branch. The experiment deliberately modifies one
line of `IntrospectionTwin/Witness.lean` **inside the disposable CI job**,
rebuilds, probes the admission path, and restores the original file.

## Precommitted prediction

1. Unmodified Lean reader refuses admission for a declaration confirmed absent
   from `getEnv`, with the full root build and axiom audit passing.
2. Changing only the missing-declaration branch of `synthesizeWitness` from
   `⟨false, false, 0, []⟩` to `⟨true, true, 0, []⟩` will leave the
   complete theorem corpus and axiom audit green, **while the actual
   `admit` entry point admits the absent declaration**.
3. A separate **counterfactual type sketch** with
   `evidence : observedAccepted = true` accepts `true` and rejects a
   term of type `ReplayCertificate false` by type checking.

## Evidence conditions

- Pin Lean 4.22.0 in the existing canonical workflow.
- Clean and build the corpus and run `Audit.lean` for BOTH baseline and mutant.
- Use the same temporary probe source path and same Lean command in both.
- Independent check: the declaration does not exist in the live Lean
  environment, not merely in the reader's self-reported `kernelAccepted`.
- A passing experiment requires baseline admission false, mutant admission
  true, the unchanged theorem corpus building, and positive/negative
  type-prototype compilations as specified.
- Preserve command exit codes, stdout/stderr logs and hashes as an
  always-uploaded CI artifact.
- Restore the original source even after an error.

## Claim ceiling

A surviving reader mutation proves the **inadequacy of the present theorem
suite as a guard against a compromised witness reader**. It does not prove that
the current unmodified reader is dishonest, nor that any fielded deployment
has accepted a fabricated witness.

The counterfactual proof-carrying type experiment is only a type-checking
demonstration: a proof of `observedAccepted = true` is not evidence that an
independent kernel actually accepted a declaration. Code that chooses
`observedAccepted := true` can manufacture `rfl`; and metaprogramming
and unsafe kernel bypass remain outside the model. Genuine remediation
requires that a trustworthy verification boundary own witness issuance,
bind the certificate to the theorem's source/environment, and protect the
handoff to the effect-authority gate. A syntactically stronger field alone
cannot establish runtime refinement.

## Dependency

Stacked over draft PR #24 (AO-MUT-001). Neither branch is merged to `main`
by this experiment.
