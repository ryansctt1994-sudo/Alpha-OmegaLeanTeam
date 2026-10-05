# v0.6 AO-HISTORY Runtime Forward-Simulation Contract

Status: **FROZEN FOR PROOF IMPLEMENTATION ON MERGE**  
Tracking issue: #18

This document freezes the statement to be attempted in v0.6. It intentionally
contains **no Lean correspondence proof and no Python correspondence harness**.
Those artifacts must be built only after this contract is merged.

The target claim is a **forward simulation on a named concrete transition
subset**. It is not Abadi–Lamport refinement, backward simulation, or a whole
Python correctness proof.

---

## 1. Immutable source boundary

### 1.1 Abstract system M

Repository: `ryansctt1994-sudo/Alpha-OmegaLeanTeam`

Canonical v0.5 base:
`8ac7478c92d95b891bdff4d1c002dbfed5d43b85`

Normative abstract artifacts on that base:

- `HISTORY_CONTRACT_v1.md`
  - blob SHA: `2be9388acc0b4f66ba9d791fdbb4a66a63adc94e`
- `AlphaOmega/History.lean`
  - blob SHA: `ff88532b1315dbc76ab36f130e533a62e9ef9529`

The abstract protected state is:

```text
M = AlphaOmega.History.History
  = { entries : List Entry, head : Digest }
```

The abstract append operation is `appendEntry`; admissibility is
`Admissible hash h e`; rejection is `reject h e = h`.

### 1.2 Concrete runtime R

Repository: `ryansctt1994-sudo/Weaver_Os`  
Pinned commit:
`ee725f7cf923d86d915900fc93ef2e3f6e5eef1c`

Normative concrete artifacts:

- `triadic_controls/ledger.py`
  - blob SHA: `a967376fd3b1c2170e5ee7b2659e15d851db884b`
- `tools/verify_triad_ledger.py`
  - blob SHA: `e20322297af3c19e7ad3c5c1c32da3717cfea757`
- `schemas/triad_event.schema.json`
  - blob SHA: `93ce0918131167cb492592d5696d3e9fa4faf49f`
- `tests/test_triad_multiblock.py`
  - blob SHA: `17b5caff6187d6346c1cc8071fe2f796df5f62d4`

Named concrete functions in scope:

- `TriadLedger.load_events`
- `TriadLedger.append_event`
- `verify_chain`
- `validate_event_integrity`
- `compute_event_hash`
- strict `verify_bytes`

No other Weaver subsystem is implicitly included.

---

## 2. Claim class

The v0.6 proof target is:

```text
R --cstep--> R'
    implies
ForwardMatch(cstep, alpha(R), alpha(R'))
```

for the transition labels enumerated in section 6 and only for states in the
domain defined in section 3.

`ForwardMatch` has exactly three allowed shapes:

1. **APPEND**
   - one legal AO-HISTORY append step;
2. **REJECT**
   - protected abstract history is unchanged;
3. **STUTTER**
   - protected abstract history is unchanged.

This is a labeled forward simulation. It does **not** establish:

- that every abstract step is realizable;
- that every Python step has an abstract counterpart;
- a total abstraction over arbitrary Python objects/files;
- trace refinement in the Abadi–Lamport sense;
- liveness;
- crash refinement;
- concurrency refinement.

---

## 3. Concrete state domain

The proof-level concrete state is a persisted ledger snapshot, not the
surrounding application:

```text
RuntimeState R :=
  rawLedgerBytes : bytes
  events         : list[Python event object]
```

Path names, process identity, file descriptors, clocks, permissions, and
external policy objects are not fields of the protected refinement state.

### 3.1 R_ok

`R_ok` is the reachable fragment on which `alpha` is defined.

A state belongs to `R_ok` when:

1. `rawLedgerBytes` decodes through the pinned ledger loading contract to
   exactly `events`; and
2. the pinned `verify_chain(events)` returns successfully.

The empty/missing-ledger case is represented by:

```text
events = []
head   = "genesis"
```

because `TriadLedger.load_events` accepts the absent ledger as the empty
chain.

The strict signed verifier `verify_bytes` defines a narrower executable
validation surface, called `R_strict`, used by the later replay harness.
`R_strict` is not the domain of `alpha`; this avoids silently making
signature or trusted-key verification part of the simulation theorem.

### 3.2 Rejected attempts

A rejected append attempt is represented as an attempted transition whose
persisted protected ledger snapshot is unchanged:

```text
R' = R
```

under assumptions A–F.

An invalid pre-existing file for which `load_events` / `verify_chain`
fails is **outside R_ok**. The v0.6 theorem does not manufacture an abstract
history for corrupt arbitrary bytes.

---

## 4. Abstraction function alpha

Signature:

```text
alpha : R_ok -> AlphaOmega.History.History
```

For `R.events = [e0, ..., en]`:

```text
alpha(R).entries = map abstractEntry R.events

alpha(R).head =
  "genesis"                      if R.events = []
  R.events[-1]["event_hash"]     otherwise
```

### 4.1 Event field mapping

For a concrete Python event `e`:

| Concrete field | Abstract field |
| --- | --- |
| `e["index"]` | `Entry.input.index` |
| `e["timestamp"]` | `Entry.input.timestamp` |
| `e["event_type"]` | `Entry.input.eventType` |
| `e["actor"]` | `Entry.input.actor` |
| `e["public_key"]` | `Entry.input.publicKey` |
| `canonical_json(e["payload"]).decode("utf-8")` | `Entry.input.payloadCanonical` |
| `e["prev_hash"]` | `Entry.input.prevDigest` |
| `e["policy_version"]` | `Entry.input.policyVersion` |
| `e["event_hash"]` | `Entry.eventDigest` |
| optional `e["signature"]` | `Entry.signature` |

The abstraction intentionally does not map Python dictionary insertion order,
JSON whitespace, file path, inode, mtime, file descriptor, process identity,
or external expected-head/key pins into `History`.

### 4.2 Digest bridge

The abstract Lean history model keeps its digest function parametric.

For the encoded v0.6 step set, the bridge assumption is:

```text
H(abstractDigestInput(e)) = compute_event_hash(e)
```

for events admitted by the encoded concrete step.

**No SHA-256 collision-resistance theorem is assumed or claimed.**

This is intentionally narrower than treating SHA-256 as a proved
collision-free oracle. Forward step correspondence needs digest agreement, not
a cryptographic collision theorem.

---

## 5. Assumptions A–F

Every v0.6 correspondence theorem and executable replay result must cite these
assumptions by name.

### A — Deterministic single-threaded step

The named concrete operation executes deterministically on the supplied
snapshot/candidate in one thread. No hidden application callback mutates the
ledger during the encoded step.

### B — Frozen canonical event contract

The AO-HISTORY-v1 serialization/digest contract and the pinned Python event
schema/hash-body rules are unchanged from the immutable artifacts in section 1.

### C — No crash or torn append in the encoded interval

For an accepted append, execution is observed from the validated pre-state
through successful completion of both concrete writes:

```python
handle.write(json.dumps(...))
handle.write("\n")
```

No crash, kill, I/O fault, partial write, or torn persistence occurs inside that
interval.

For rejected steps, no write has occurred before the raised validation error.

### D — Digest correspondence

The abstract digest parameter `H` agrees with pinned
`compute_event_hash` on the concrete events encoded by the simulation.

This is an abstraction assumption, not a proof of cryptographic strength.

### E — No concurrent append or file replacement

No second writer, rename/replacement, symlink retarget, or other actor changes
the ledger between the pre-state snapshot/verification and completion of the
encoded step.

### F — Environment identity is outside protected transition authority

Clock/timestamp values, OS process identity, path identity, permissions, and
similar environment metadata may be event data or harness inputs, but are not
sources of abstract transition authority and are not protected-state fields in
`alpha`.

---

## 6. Encoded concrete transition inventory

Only the following labels may be promoted as v0.6 correspondence results.

| Concrete label | Pinned concrete behavior | Abstract match |
| --- | --- | --- |
| `C_LOAD_OK` | `load_events` returns verified events without writing | `M_STUTTER` |
| `C_VERIFY_OK` | strict `verify_bytes` succeeds without writing | `M_STUTTER` |
| `C_APPEND_OK` | `append_event` validates exact next index, exact previous hash, integrity, then appends one JSONL event | `M_APPEND` |
| `C_APPEND_REJECT_INDEX` | wrong next index raises `LedgerChainError` before write | `M_REJECT` |
| `C_APPEND_REJECT_PREV` | wrong `prev_hash` raises `LedgerChainError` before write | `M_REJECT` |
| `C_APPEND_REJECT_INTEGRITY` | schema/hash/present-signature validation fails before write | `M_REJECT` |
| `C_STRICT_VERIFY_REJECT` | strict `verify_bytes` rejects bytes/head/key/framing/signature without writing | `M_REJECT` |

### 6.1 M_APPEND obligation

For `C_APPEND_OK(R, e, R')`, the later proof must establish:

```text
Admissible H (alpha R) (abstractEntry e)

alpha R' =
  appendEntry (alpha R) (abstractEntry e)
```

and therefore a one-step `ValidExtension H (alpha R) (alpha R')`.

### 6.2 M_REJECT obligation

For each encoded rejected append:

```text
alpha R' = alpha R
```

and equivalently:

```text
alpha R' = reject (alpha R) (abstractEntry e)
```

when an abstract candidate entry is defined.

### 6.3 M_STUTTER obligation

For the read-only accepted steps:

```text
alpha R' = alpha R
```

No abstract append is inferred from successful verification alone.

---

## 7. Strict verifier replay requirement

The later executable correspondence harness must invoke the **real pinned
Python verifier**, not a reimplementation of it.

At minimum it must import and execute:

```text
tools.verify_triad_ledger.verify_bytes
```

from the pinned Weaver source or a byte-identical vendored copy whose source
hash is checked before execution.

For accepted replay fixtures:

1. verify the concrete pre-state with the real verifier when the fixture lies in
   `R_strict`;
2. execute the real named concrete operation;
3. verify the concrete post-state with the real verifier when applicable;
4. emit the concrete pre/post snapshot plus the abstraction result consumed by
   the theorem replay/checker.

The harness may calculate `alpha`, but it may not substitute a model of
`verify_bytes` for the real verifier call.

---

## 8. Witnessed excluded steps

The boundary must be demonstrated by executable counterexamples later. Two
targets are frozen now.

### EX-1 — Crash/torn write between JSON and newline

`append_event` performs the event JSON write and newline write separately.
A process interruption after the first write but before the second can leave
bytes outside the strict framing contract.

This step is outside assumption C and is **not** required to correspond to
either abstract append or protected-state rejection.

A future persistence refinement must model this separately.

### EX-2 — Unsigned append accepted by ledger primitive, rejected by strict verifier

The pinned event schema and `append_event` allow an absent signature.
The strict `verify_bytes` verifier rejects unsigned events.

Therefore:

```text
append_event success != strict-verifier acceptance
```

This is a deliberate boundary witness. Signature/trusted-key semantics are not
silently imported into the abstract append relation.

---

## 9. Hostile mutant list

The v0.6 implementation issue must include at least these mutants.

### MU-1 — Previous-hash bypass

Remove or neutralize the concrete `prev_hash == expected_prev_hash` guard.

Expected result: correspondence or executable replay fails.

### MU-2 — Index bypass

Remove or neutralize the concrete exact-next-index guard.

Expected result: correspondence or executable replay fails.

### MU-3 — Integrity bypass

Skip `validate_event_integrity` on accepted append.

Expected result: the append cannot be promoted as `M_APPEND`.

### MU-4 — Reject-path write

Write candidate bytes before or despite a rejected append.

Expected result: protected-state rejection correspondence fails.

### MU-5 — Prefix rewrite/prepend

Replace append-only persistence with rewrite, prepend, reorder, or deletion of
the existing concrete prefix.

Expected result: `alpha R'` cannot equal one abstract append from
`alpha R`.

### MU-6 — Wrong-head abstraction

Define `alpha(R).head` from an external expected-head parameter instead of the
last verified event hash / genesis.

Expected result: append/link correspondence fails on a targeted fixture.

### MU-7 — Fake-verifier harness

Replace the real `verify_bytes` call with a local predicate/model while
leaving the harness result green.

Expected result: source-binding / harness-integrity gate fails.

### MU-8 — Contract drift

Change canonical JSON/hash-body semantics without updating the frozen artifact
pins.

Expected result: source/provenance pin gate fails before theorem replay.

---

## 10. Explicitly excluded surface

The v0.6 claim does not include:

- backward simulation or abstract-step realizability;
- Abadi–Lamport trace refinement;
- liveness or eventual completion;
- crash recovery, torn writes, fsync, power loss, storage durability;
- concurrent writers, distributed replicas, locking, consensus;
- Python parser correctness or a byte-level proof of JSON decoding;
- SHA-256 collision resistance or preimage resistance;
- Ed25519 authenticity;
- trusted-key correctness;
- security against a compromised signer;
- OS/process identity, filesystem permissions, symlink safety;
- correctness of clocks or timestamps;
- whole-application correctness;
- operational or production authority.

The strict verifier may test some excluded properties as executable evidence.
That does not silently move them into the formal simulation theorem.

---

## 11. Promotion gate for the later proof issue

The subsequent v0.6 proof issue may move the claim ceiling only if all of the
following are present and green:

1. exact pinned abstract and concrete artifacts from section 1;
2. a typed implementation of `alpha` matching section 4;
3. a labeled concrete step model restricted to section 6;
4. Lean correspondence theorems for every encoded label;
5. explicit stutter/reject preservation theorems;
6. executable EX-1 and/or EX-2 boundary witness;
7. hostile mutation controls MU-1 through at least MU-7;
8. replay against the real pinned `verify_bytes`;
9. source/fixture binding so the replay cannot silently target different code;
10. independent root governance CI remaining green.

Nothing weaker changes the runtime-refinement claim ceiling.

---

## 12. Permitted claim sentence

If and only if the later proof gate in section 11 passes, the permitted claim is:

> Under assumptions A–F, the named Weaver Triad ledger runtime transitions
> C_LOAD_OK, C_VERIFY_OK, C_APPEND_OK, C_APPEND_REJECT_INDEX,
> C_APPEND_REJECT_PREV, C_APPEND_REJECT_INTEGRITY, and
> C_STRICT_VERIFY_REJECT forward-simulate the named AO-HISTORY-v1 append,
> reject, or stutter transitions through the frozen abstraction alpha.

Immediately after that sentence, the following boundary must remain attached:

> This is a forward simulation on a named transition subset. Crash persistence,
> concurrency, OS behavior, parser correctness, cryptographic strength,
> signature/trusted-key authenticity, backward simulation, liveness, and
> operational authority remain outside the proved boundary.

No shorter or broader phrasing is canonical.
