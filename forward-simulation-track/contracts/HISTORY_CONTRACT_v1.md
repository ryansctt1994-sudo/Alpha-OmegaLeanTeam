# AO-HISTORY-v1 — Frozen Digest and History Contract

Status: **FROZEN FOR v0.3 FORMALIZATION**

This contract is derived from the committed Triad ledger implementation in
`ryansctt1994-sudo/Weaver_Os` at source commit:

`ee725f7cf923d86d915900fc93ef2e3f6e5eef1c`

Normative source artifacts at that commit:

- `triadic_controls/ledger.py`
  - blob SHA: `a967376fd3b1c2170e5ee7b2659e15d851db884b`
- `schemas/triad_event.schema.json`
  - blob SHA: `93ce0918131167cb492592d5696d3e9fa4faf49f`
- `tools/verify_triad_ledger.py`
  - blob SHA: `e20322297af3c19e7ad3c5c1c32da3717cfea757`
- `tests/test_triad_multiblock.py`
  - blob SHA: `17b5caff6187d6346c1cc8071fe2f796df5f62d4`

The Lean theorems in `AlphaOmega/History.lean` formalize structural history
properties relative to this frozen contract. They do **not** prove the Python
implementation refines the Lean model byte-for-byte.

## 1. Event fields

A persisted event contains:

- `index : Nat`
- `timestamp : String`
- `event_type : String`
- `actor : String`
- `public_key : String`
- `payload : JSON object`
- `prev_hash : String`
- `event_hash : lowercase SHA-256 hex string`
- optional `signature : String`
- `policy_version : String`

The event schema rejects additional top-level fields.

## 2. Digest input

The digest input is the event object after removing:

- `event_hash`
- `signature`

Everything else, including `prev_hash`, remains in the digest input.

This matters: ancestry linkage is itself committed by the event digest.

## 3. Canonical digest serialization

The digest input is serialized exactly as the Triad ledger's
`canonical_json` function:

- UTF-8 encoding;
- Unicode is emitted directly (`ensure_ascii=False`);
- NaN and Infinity are forbidden (`allow_nan=False`);
- object keys are sorted lexicographically (`sort_keys=True`);
- insignificant whitespace is removed with separators `(",", ":")`.

This is the normative AO-HISTORY-v1 digest serialization rule. No claim is
made here that this is byte-for-byte RFC 8785 canonical JSON.

## 4. Digest function

`event_hash = SHA256(canonical_digest_bytes)`

The persisted digest representation is lowercase hexadecimal.

The Lean model treats the digest function parametrically. This preserves the
structural proof boundary: the theorems do not assume collision resistance or
model SHA-256 internals.

## 5. Chain linkage

- Empty history head: literal `"genesis"`.
- Event 0 must have `index = 0` and `prev_hash = "genesis"`.
- Event `i > 0` must have:
  - `index = i`;
  - `prev_hash = event_hash(event[i-1])`.
- A candidate event is admissible only when:
  - its claimed digest matches the frozen digest function;
  - its `prev_hash` equals the current history head;
  - its index equals the current history length.

## 6. Append-only extension

A valid extension may only append entries to the existing history.

It may not:

- reorder prior entries;
- rewrite prior entries;
- delete prior entries;
- prepend a new entry ahead of the existing prefix.

The existing history must remain an exact prefix of the extended history.

This matches the earlier Weaver `ChroniclePrefixInvariant` proof obligation.

## 7. File framing and strict verifier boundary

The pinned strict verifier additionally requires:

- nonempty signed JSONL ledger;
- final newline;
- no CR bytes;
- no blank lines;
- duplicate JSON object keys rejected;
- NaN/Infinity rejected;
- all events signed;
- event public key fingerprint equals the trusted key fingerprint;
- final event hash equals the externally expected head;
- optional exact ledger-file SHA-256 pin.

Those properties are implementation/verifier obligations. The first v0.3 Lean
history model proves structural chain properties, not Ed25519 authenticity or
JSON parser behavior.

## 8. Rejection path

A rejected candidate does not enter the protected history.

Therefore rejection must preserve:

- the complete protected history;
- the existing entry sequence;
- the current chain head.

A separate rejection/evidence log may exist outside this protected history, but
it is not modeled as a successful history extension.

## 9. Claim ceiling

AO-HISTORY-v1 establishes the contract needed to state and prove append-only and
ancestry properties.

It does **not** establish:

- SHA-256 collision resistance;
- signature authenticity;
- trusted-key correctness;
- runtime/Lean refinement;
- distributed consensus;
- storage durability;
- resistance to a fully compromised signing authority;
- operational authority.

Digest linkage is integrity structure, not truth or authority.
