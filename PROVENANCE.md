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

implemented by reusing Mathlib's maintained `irrational_sqrt_two`. The source
project currently pins Lean `v4.31.0-rc1` and a specific Mathlib commit, so it
is tracked as a valid external theorem candidate rather than silently mixing
toolchains into the 4.22.0 root project.

### lean-workers-union

The current `transition_keeps_identity` theorem concludes
`m.identity.member_id = m.identity.member_id`. That is reflexive and does not
establish a nontrivial relation between pre- and post-transition states. It is
therefore not counted as a canonical governance invariant here.

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


## v0.2 candidate formalizations

### Union transition preservation

Motivating source: `ryansctt1994-sudo/lean-workers-union`.

The source repository's prior `transition_keeps_identity` theorem was
reflexive. `AlphaOmega/UnionTransition.lean` introduces an explicit transition
function and pre/post transition relation. Its preservation theorems therefore
relate the constructed post-state to the actual pre-state.

This is a corrected formal model in Alpha-Omega; it is not yet a refinement
proof for an external union runtime.

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
