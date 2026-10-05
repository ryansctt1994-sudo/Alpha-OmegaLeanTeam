# Provenance and claim status

This repository is a consolidation layer. Source provenance is preserved and
claim strength is capped by what the checked Lean artifacts actually establish.

## Imported theorem corpora

### IntrospectionTwin core

Source repository: `ryansctt1994-sudo/introspection-twin`  
Source commit: `fcc63c085497a26bf1468294a3df53fdd6a56c9f`

Copied source files:

- `IntrospectionTwin.lean`
- `IntrospectionTwin/Witness.lean`
- `IntrospectionTwin/Receipt.lean`
- `IntrospectionTwin/Gate.lean`
- `IntrospectionTwin/Admit.lean`
- `IntrospectionTwin/Twin/Observation.lean`
- `IntrospectionTwin/Twin/Bounds.lean`
- `IntrospectionTwin/Twin/State.lean`

These files contain 31 theorem declarations. The intentionally poisoned
`Bypass/KernelBypass.lean`, `Test/NativeDecide.lean`, and hostile harness
files are not part of the canonical library import. Their adversarial findings
remain source-project validation evidence, not production theorem modules.

The source repository reports a Lean 4.22.0 clean build and no `sorry` in the
library. At consolidation time GitHub exposed no workflow runs directly bound
to commit `fcc63c0`, so this repository's own clean CI is the qualification
gate for the imported copy.

### Weaver Lattice Core

Source repository: `ryansctt1994-sudo/Weaver_Os`  
Source PR: #66  
Source head: `b162a7cea43959214bd9e928ea6c9965976cdcc2`

Copied source files:

- `LatticeCore.lean`
- `LatticeCore/Deflation.lean`
- `LatticeCore/Models.lean`
- `LatticeCore/Counterexamples.lean`

These files contain 16 theorem declarations covering explicit order laws,
deflationarity, monotonicity, idempotence, meet restriction, permission
attenuation, assurance minimum, information accumulation, and counterexamples.

The source head had successful GitHub workflow runs for both **Verification
evidence** and **Formal foundations**. The latter performed a clean stock Lean
4.22.0 build and theorem axiom audit.

## New AlphaOmega formalizations

The `AlphaOmega/` modules are new formalizations created for this consolidation.
They intentionally prove narrow statements:

- explicit countermodels for capability ≠ authority;
- evidence ≠ authority;
- witness ≠ evidence;
- signature ≠ truth;
- evidence/check/witness transitions preserve authority in the modeled state;
- evidence growth does not automatically raise the authority coordinate;
- authority caps never raise authority;
- unclosed recovery intent normalizes to indeterminate, not pass;
- recovery normalization is idempotent and preserves authority;
- rejection and failed checks preserve modeled protected state and budget.

These are mathematical properties of the definitions in this repository. They
do not establish runtime refinement, production safety, or external authority.

## Reviewed but not imported into the root Lean 4.22.0 corpus

### Math_Build1994

Current source includes:

`MathBuild.sqrt2_irrational_real : Irrational (Real.sqrt 2)`

implemented by reusing Mathlib's maintained `irrational_sqrt_two`. It remains
excluded from the root Lean 4.22.0 corpus, but v0.4 now reproduces it inside the
separate `mathlib-track/` trust boundary with exact Lean, Mathlib, source,
axiom-audit, and mutation gates.

### lean-workers-union

Source repository: `ryansctt1994-sudo/lean-workers-union`  
Repaired source commit: `e537c7104cf4601fe26eca2531baea9be07faf22`

The earlier `transition_keeps_identity` theorem was reflexive. The source repo
has now been repaired with an explicit pre/post transition constructor and
relation, plus proofs of complete identity, member-id, and credit preservation.
Lean 4.22.0 is pinned there, its theorem axiom inventory is checked, and an
identity-rewrite mutation is required to fail.

Alpha-Omega's `AlphaOmega/UnionTransition.lean` is a separately checked
canonical model with the same preservation intent. No runtime refinement claim
is inferred from agreement between the two source models.

### AutoProof

AutoProof is a theorem-proving workspace and Lean front end, not itself a pinned
Lean theorem library in its current repository state.

### LogOS

LogOS contains Agda/formal-method material, but it is not a Lean corpus and its
own README explicitly withholds whole-system formal-verification claims.

### AGI-to-ASI-TRANSITION-PROOF-LAYER

This repository is Python/narrative material, not a Lean project. Claims about
consciousness, quantum processing, or ASI readiness are not imported as formal
theorems.

## Canonical proof gate

A theorem enters the canonical corpus only when all of the following hold:

1. the pinned Lean build succeeds;
2. the source contains no `sorry`, `admit`, or new `axiom` declarations;
3. the axiom inventory contains only approved Lean foundations used by the
   imported theorem set: `propext`, `Quot.sound`, and `Classical.choice`;
4. the theorem is described no more strongly than its formal statement;
5. provenance names the source commit when code was imported.

A green build raises evidence for this source tree. It does not grant runtime or
production authority.


## v0.2 canonical formalizations

### Union transition preservation

Motivating source: `ryansctt1994-sudo/lean-workers-union`.

The source repository's prior reflexive theorem was replaced upstream at
`e537c7104cf4601fe26eca2531baea9be07faf22`. In parallel,
`AlphaOmega/UnionTransition.lean` provides the canonical transition function
and pre/post transition relation. Its preservation theorems relate the
constructed post-state to the actual pre-state.

Both source trees are kernel checked. Agreement between them is still not a
runtime-refinement proof for an external union implementation.

### Weaver recovery/replacement semantics

Motivating source: Weaver OS recovery specification, PR #66 source head
`b162a7cea43959214bd9e928ea6c9965976cdcc2`.

`AlphaOmega/RecoveryReplacement.lean` formalizes the narrow rules that an
unclosed request becomes consumed and indeterminate, the original ID is not
automatically redispatchable, and a replacement requires explicit binding,
a distinct request ID, authorization, and a reconciliation or
duplicate-effect-waiver basis.

The model does not prove durable-storage refinement, cryptographic verification,
or physical exactly-once effects.

### Evidence × Authority

`AlphaOmega/EvidenceAuthority.lean` makes evidence and authority separate
ordered coordinates. Evidence accumulation preserves authority; meet/cap
operations cannot silently raise authority.

Natural-number coordinates are an abstract order model only.

### v0.2 sensitivity controls

`tools/check_v02_mutations.py` creates six semantic mutants and requires all
six to fail Lean: identity rewrite, unconsumed recovery, fabricated PASS,
same-ID replacement, missing resolution basis, and evidence-driven authority
growth.


## v0.2+ LatticeCore integration

Canonical commit: `bae0bb53ab33ba8d4bb4d84a85ce5cff30b676b6`

`AlphaOmega/PortfolioLattice.lean` connects the previously separate
Evidence × Authority state to the imported Weaver Lattice Core.

The integration adds 18 theorem declarations covering:

- a `LatticeCore.MeetOrder` instance for `EvidenceAuthority.Level`;
- portfolio caps defined by the generic `LatticeCore.restrict` operator;
- cap deflationarity, monotonicity, and idempotence;
- monotonicity of portfolio caps in their constraint parameters;
- meet-based demotion and preservation of a lower authority tier when that tier
  is supported by both the current state and the demotion ceiling;
- proof-carrying promotion requiring minimum evidence, verified witness, green
  checks, and a separate authority grant;
- governed promotion that composes promotion with the portfolio cap and cannot
  exceed either the evidence or authority ceiling.

The semantic mutation suite now contains eight controls. The two v0.2+ additions
remove the portfolio cap from governed promotion and remove the separate
authority-grant requirement. Both mutants are required to fail Lean.

This does not turn evidence into authority. Authority increase remains an
explicit, separately witnessed premise of the formal promotion relation. The
model does not itself grant operational authority or establish runtime
refinement.


## v0.3 AO-HISTORY-v1

Canonical implementation commit: `396706c7f9ab24bf3cca1505e018664cc093fd53`

The digest/history contract is frozen in `HISTORY_CONTRACT_v1.md`, derived
from Weaver_Os commit `ee725f7cf923d86d915900fc93ef2e3f6e5eef1c`.

Normative source artifacts:
- `triadic_controls/ledger.py` blob `a967376fd3b1c2170e5ee7b2659e15d851db884b`
- `schemas/triad_event.schema.json` blob `93ce0918131167cb492592d5696d3e9fa4faf49f`
- `tools/verify_triad_ledger.py` blob `e20322297af3c19e7ad3c5c1c32da3717cfea757`
- `tests/test_triad_multiblock.py` blob `17b5caff6187d6346c1cc8071fe2f796df5f62d4`

The frozen contract removes `event_hash` and `signature` before hashing,
keeps `prev_hash` inside the digest input, uses compact sorted UTF-8 JSON with
NaN/Infinity forbidden, and specifies SHA-256 lowercase hex plus genesis/index
and previous-hash continuity.

`AlphaOmega/History.lean` adds 13 structural theorems:
- exact-prefix append-only extension;
- history length non-decrease;
- digest, previous-head, and index admission;
- broken-ancestry, hash-mismatch, and wrong-index rejection;
- rejection preserving the full protected history, entries, and head.

The digest function is parametric in Lean. These theorems therefore do not
claim SHA-256 collision resistance, Ed25519 authenticity, byte-level
Python/Lean refinement, durable storage, distributed consensus, or authority.


## v0.4 isolated Mathlib track

Canonical implementation commit:
`58c51f3cfaf02933bd0c26f98655a7a9dd04866e`

Directory: `mathlib-track/`

Upstream source:
- repository: `ryansctt1994-sudo/Math_Build1994`
- commit: `41d2c9ae8a362a79de4f95733adf0fd8b53a151c`
- theorem blob:
  `d0e5e997327619231ed9a7039f6ca4295a7195a7`
- upstream `lean-toolchain` blob:
  `8c7e931aab0179018e3e987d8395daa4466fc3aa`
- upstream `lakefile.lean` blob:
  `14525ef831661111106b26e9ee869140819da87e`

Pinned verification environment:
- Lean: `leanprover/lean4:v4.31.0-rc1`
- Lean Linux release SHA-256:
  `055f1780f20f9774bbe270d5d4cf7561fb26ee6734c0917ba6cfb867e33cb99e`
- Mathlib:
  `d568c8c09630de097a046763c17b9ea99f95f950`

The isolated workflow performs an exact textual pin guard, checksum-verifies the
Lean release archive, runs `lake update`, checks the generated manifest resolves
Mathlib to the required commit, builds the isolated library, audits theorem
axioms, and requires two hostile controls to fail:

1. replacing the theorem proof with an unresolved reference;
2. changing the Mathlib commit pin.

The first PR CI attempt failed because a helper action required a pre-existing
Lake manifest. That failure did not affect the root governance workflow. The
isolated workflow was then made self-contained and passed both on the PR and on
post-merge `main`.

The theorem
`MathBuild.sqrt2_irrational_real : Irrational (Real.sqrt 2)`
reuses Mathlib's maintained `irrational_sqrt_two`. It is kernel-checked proof
reuse in the pinned environment, not an independent derivation of the
mathematics.

The root Lean 4.22.0 corpus remains exactly 124 theorem declarations.
