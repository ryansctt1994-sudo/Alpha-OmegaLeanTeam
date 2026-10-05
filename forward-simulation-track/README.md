# AO-HISTORY named-step forward simulation candidate

This is an isolated Lean **4.22.0** trust boundary for issue #20. The root
governance inventory remains **124**, with its own build, audit, and 11 mutants.
This track adds **12 new theorem declarations**; the byte-identical vendored
13-theorem History module is a dependency, not 13 new results.

## Exact scope

The frozen contract is `../V0_6_FORWARD_SIMULATION_CONTRACT.md`, merged at
`e7fb0be1713ce6cba94166e2234ebb8d16025081`. It is unchanged.

`ForwardSimulation.lean` gives typed events, `RuntimeState`, `R_ok`, the exact
`abstractEntry` field mapping, `alpha`, the seven labels, a concrete step
relation, one theorem per label, and an aggregate forward-simulation theorem.
It also proves legal abstract extension for accepted append.

The relation assumes the named concrete guards and byte/event effects. It does
not assume `ForwardMatch`, abstract admissibility, or abstraction equality.
Those are derived. The decoder, concrete digest, serialization, and integrity
admission and strict-verifier outcome are explicit encoding parameters.
Successful strict verification and strict rejection require opposite observed
outcomes in the typed step relation. These observations are checked against
the real verifier during replay; Lean does not prove signature policy.
Digest assumption D is restricted
to admitted candidates. A/C/E delimit the deterministic uninterrupted
single-writer interval; B freezes source semantics; F excludes environment
identity from protected transition authority.

The connection between this encoding and Python has source inspection and
bounded executable evidence. There is no universal Lean semantics of Python,
proof of JSON parsing, or proof that every possible Python execution has the
encoded effects. In particular, rejection/read-only byte preservation is an
encoded premise tested against real operations, not an independently proved
Python memory theorem.

## Replay and trust boundary

`vendor/Weaver_Os` contains byte-identical sources from
`Weaver_Os@ee725f7cf923d86d915900fc93ef2e3f6e5eef1c`.
The 10 frozen blobs, manifest, root contract copies, and real callable code
objects are checked before execution. Replay calls the real `append_event`,
`load_events`, `compute_event_hash`, and `tools.verify_triad_ledger.verify_bytes`.

There are **43 transitions**, covering all seven labels at ledger depths
0/1/3/8. Integrity rejections include bad hash, present bad signature, and bad
schema. Strict rejection includes empty bytes, wrong head, and untrusted key.
Unicode and nested payloads exercise the canonical payload mapping.

Every transition emits exact UTF-8 raw snapshots, their SHA-256 values, loaded
events, and both abstract states. Generated `Replay.lean` kernel-checks:

- the finite fixture decoder and chain-valid endpoints;
- Python-produced abstraction values against Lean `alpha`;
- concrete guards, append-only bytes, and loaded-event effects;
- a `CStep` witness and application of the general theorem.

Fixture digest tables contain hashes computed by the pinned Python source.
They instantiate assumption D for the corpus; Lean does not compute or prove
SHA-256. Finite decoder tables similarly certify the recorded correspondence,
not arbitrary byte parsing. Certificates use ordinary `decide`, not native
proof shortcuts. All 86 named fixture step/replay theorems are axiom-audited.

`fixture-pins.json` freezes the generated certificate, snapshots, and mutation
results. CI regenerates them and checks byte identity. Source hashes in
`generated/validation.json` bind the current harness and proof implementation.

## Boundary witnesses

**EX-1:** the real append is interrupted by an injected I/O failure at its
second write, after flushing JSON but before newline. The primitive loader
accepts that complete JSON; the strict verifier rejects framing. This snapshot
can remain inside `R_ok`, but the attempted step is outside assumption C.
It is not a demonstrated OS process kill, power-loss test, or durability test.

**EX-2:** real unsigned append and primitive load succeed; strict verification
rejects the unsigned event. Signature policy is not imported into abstract
append admission.

## Mutation gates

MU-1..MU-5 run modified runtime behavior in isolated processes **after the
original inputs pass source checks**. The replay must detect missing prior
hash/index/integrity guards, writes on reject, and prefix rewrite. They are
behavioral failures, not only changed-source-hash failures.

MU-6 substitutes an external abstract head. MU-7 substitutes a fake callable
and fails callable binding. MU-8 independently changes the frozen contract
and runtime source and fails before replay: **8 families / 9 probes**.

Five additional Lean mutants remove prior/index/digest guards, prepend an
entry, or replace the abstract head. Existing correspondence proofs must fail.
All mutant subprocesses require their intended diagnostic, not just an
arbitrary nonzero exit. The 38 original multiblock verifier tests also run.

## Reproduce

With the SHA-256-pinned Lean 4.22.0 archive from the isolated CI workflow:

```bash
cd forward-simulation-track
python3 -m pip install -r requirements.txt
python3 validate.py
```

Root governance validation runs separately from the repository root:

```bash
lake build
python3 tools/check_v02_mutations.py
lake env lean -DwarningAsError=true Audit.lean
```

CI retains the certificates, snapshots, source-bound summary, and logs as
`ao-history-forward-simulation-evidence`. Passing this track does not imply
passing the root, Mathlib, or self-model workflows.

## Claim ceiling

Candidate implementation pending head-bound CI and review. Issue #20 remains
open until all frozen promotion conditions are assessed. The permitted claim
sentence and mandatory exclusions remain exactly section 12 of the contract.

No crash persistence, concurrency, parser correctness, cryptographic strength,
trusted-key authenticity, backward simulation, liveness, whole-runtime
verification, independent W1 reproduction, or operational authority is claimed.
