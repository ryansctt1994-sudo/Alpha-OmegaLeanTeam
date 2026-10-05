import Std

/-!
# AO-HISTORY-v1 structural history model

This module proves append-only extension, previous-digest linkage, broken
ancestry rejection, and protected-history invariance on rejection.

The digest function is a parameter. The byte-level SHA-256/canonical-JSON
contract is frozen separately in HISTORY_CONTRACT_v1.md; cryptographic
collision resistance and Python-runtime refinement are outside these proofs.
-/

namespace AlphaOmega.History

abbrev Digest := String

def genesisDigest : Digest := "genesis"

structure DigestInput where
  index : Nat
  timestamp : String
  eventType : String
  actor : String
  publicKey : String
  payloadCanonical : String
  prevDigest : Digest
  policyVersion : String
deriving Repr, DecidableEq

structure Entry where
  input : DigestInput
  eventDigest : Digest
  signature : Option String
deriving Repr, DecidableEq

structure History where
  entries : List Entry
  head : Digest
deriving Repr, DecidableEq

def empty : History :=
  { entries := [], head := genesisDigest }

def HashValid (hash : DigestInput → Digest) (e : Entry) : Prop :=
  e.eventDigest = hash e.input

def LinkValid (h : History) (e : Entry) : Prop :=
  e.input.prevDigest = h.head

def IndexValid (h : History) (e : Entry) : Prop :=
  e.input.index = h.entries.length

def Admissible (hash : DigestInput → Digest) (h : History) (e : Entry) : Prop :=
  HashValid hash e ∧ LinkValid h e ∧ IndexValid h e

def appendEntry (h : History) (e : Entry) : History :=
  { entries := h.entries ++ [e], head := e.eventDigest }

def EntriesPrefix (old new : History) : Prop :=
  ∃ suffix, new.entries = old.entries ++ suffix

inductive ValidExtension (hash : DigestInput → Digest) : History → History → Prop where
  | refl (h : History) : ValidExtension hash h h
  | step
      {origin current : History}
      (hprev : ValidExtension hash origin current)
      (e : Entry)
      (hadm : Admissible hash current e) :
      ValidExtension hash origin (appendEntry current e)

theorem append_entry_length (h : History) (e : Entry) :
    (appendEntry h e).entries.length = h.entries.length + 1 := by
  simp [appendEntry]

theorem append_entries_prefix (h : History) (e : Entry) :
    EntriesPrefix h (appendEntry h e) := by
  exact ⟨[e], rfl⟩

theorem valid_extension_prefix
    {hash : DigestInput → Digest}
    {old new : History}
    (h : ValidExtension hash old new) :
    EntriesPrefix old new := by
  induction h with
  | refl =>
      exact ⟨[], by simp⟩
  | step hprev e hadm ih =>
      rcases ih with ⟨suffix, hsuffix⟩
      refine ⟨suffix ++ [e], ?_⟩
      simp [appendEntry, hsuffix, List.append_assoc]

theorem valid_extension_length
    {hash : DigestInput → Digest}
    {old new : History}
    (h : ValidExtension hash old new) :
    old.entries.length ≤ new.entries.length := by
  rcases valid_extension_prefix h with ⟨suffix, hsuffix⟩
  rw [hsuffix, List.length_append]
  omega

theorem admissible_hash_matches
    {hash : DigestInput → Digest}
    {h : History}
    {e : Entry}
    (hadm : Admissible hash h e) :
    e.eventDigest = hash e.input := by
  exact hadm.1

theorem admissible_prev_matches_head
    {hash : DigestInput → Digest}
    {h : History}
    {e : Entry}
    (hadm : Admissible hash h e) :
    e.input.prevDigest = h.head := by
  exact hadm.2.1

theorem admissible_index_matches_length
    {hash : DigestInput → Digest}
    {h : History}
    {e : Entry}
    (hadm : Admissible hash h e) :
    e.input.index = h.entries.length := by
  exact hadm.2.2

theorem broken_ancestry_rejected
    {hash : DigestInput → Digest}
    {h : History}
    {e : Entry}
    (hbroken : e.input.prevDigest ≠ h.head) :
    ¬ Admissible hash h e := by
  intro hadm
  exact hbroken (admissible_prev_matches_head hadm)

theorem hash_mismatch_rejected
    {hash : DigestInput → Digest}
    {h : History}
    {e : Entry}
    (hbad : e.eventDigest ≠ hash e.input) :
    ¬ Admissible hash h e := by
  intro hadm
  exact hbad (admissible_hash_matches hadm)

theorem wrong_index_rejected
    {hash : DigestInput → Digest}
    {h : History}
    {e : Entry}
    (hbad : e.input.index ≠ h.entries.length) :
    ¬ Admissible hash h e := by
  intro hadm
  exact hbad (admissible_index_matches_length hadm)

def reject (h : History) (_e : Entry) : History :=
  h

theorem rejection_preserves_history (h : History) (e : Entry) :
    reject h e = h := by
  rfl

theorem rejection_preserves_head (h : History) (e : Entry) :
    (reject h e).head = h.head := by
  rfl

theorem rejection_preserves_entries (h : History) (e : Entry) :
    (reject h e).entries = h.entries := by
  rfl

end AlphaOmega.History
