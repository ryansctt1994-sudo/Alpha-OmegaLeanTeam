import AlphaOmega.History

/-!
An encoding of the seven frozen named steps, not a semantics of all Python.
Decoder, event serializer, integrity admission, and concrete digest are explicit
parameters. Their connection to Python is executable evidence, not a parser or
whole-program proof. A/C/E delimit the uninterrupted single-writer interval;
B pins source semantics; D is `DigestBridge`; F excludes environment authority.
-/
namespace AOForward
open AlphaOmega.History

structure Event where
  index : Nat
  timestamp : String
  event_type : String
  actor : String
  public_key : String
  payloadCanonical : String
  prev_hash : String
  policy_version : String
  event_hash : String
  signature : Option String
deriving Repr, DecidableEq

def abstractEntry (e : Event) : Entry :=
  { input := {
      index := e.index
      timestamp := e.timestamp
      eventType := e.event_type
      actor := e.actor
      publicKey := e.public_key
      payloadCanonical := e.payloadCanonical
      prevDigest := e.prev_hash
      policyVersion := e.policy_version }
    eventDigest := e.event_hash
    signature := e.signature }

def concreteHead (events : List Event) : String :=
  match events.getLast? with
  | none => "genesis"
  | some e => e.event_hash

structure RuntimeState where
  rawLedgerBytes : List UInt8
  events : List Event
deriving Repr, DecidableEq

structure Encoding where
  decode : List UInt8 → Option (List Event)
  compute_event_hash : Event → String
  integrity : Event → Bool
  serializeLine : Event → List UInt8
  strictVerify : List UInt8 → Bool

def ChainValid (enc : Encoding) (events : List Event) : Prop :=
  (events.zipIdx.all fun (e, i) =>
    enc.integrity e && decide (e.event_hash = enc.compute_event_hash e) &&
    decide (e.index = i) && decide (e.prev_hash = concreteHead (events.take i))) = true

def R_ok (enc : Encoding) :=
  { r : RuntimeState // enc.decode r.rawLedgerBytes = some r.events ∧ ChainValid enc r.events }

def alpha {enc : Encoding} (r : R_ok enc) : History :=
  { entries := r.val.events.map abstractEntry, head := concreteHead r.val.events }

def DigestBridge (enc : Encoding) (H : DigestInput → Digest) : Prop :=
  ∀ (r : R_ok enc) (e : Event),
    e.index = r.val.events.length →
    e.prev_hash = concreteHead r.val.events →
    enc.integrity e = true →
    e.event_hash = enc.compute_event_hash e →
    enc.compute_event_hash e = H (abstractEntry e).input

inductive Label where
  | C_LOAD_OK | C_VERIFY_OK | C_APPEND_OK
  | C_APPEND_REJECT_INDEX | C_APPEND_REJECT_PREV
  | C_APPEND_REJECT_INTEGRITY | C_STRICT_VERIFY_REJECT
deriving Repr, DecidableEq

/- Concrete premises reflect guards and persistence effects, never alpha equality
or ForwardMatch. Both endpoints must be in R_ok. Read-only/reject byte identity
is an encoded effect under A/C/E, tested against the real runtime by replay. -/
inductive CStep (enc : Encoding) : Label → R_ok enc → R_ok enc → Prop where
  | load (r r' : R_ok enc) (unchanged : r'.val = r.val) :
      CStep enc .C_LOAD_OK r r'
  | verify (r r' : R_ok enc)
      (accepted : enc.strictVerify r.val.rawLedgerBytes = true)
      (unchanged : r'.val = r.val) :
      CStep enc .C_VERIFY_OK r r'
  | append (r r' : R_ok enc) (e : Event)
      (index : e.index = r.val.events.length)
      (prev : e.prev_hash = concreteHead r.val.events)
      (integrity : enc.integrity e = true)
      (digest : e.event_hash = enc.compute_event_hash e)
      (events : r'.val.events = r.val.events ++ [e])
      (bytes : r'.val.rawLedgerBytes = r.val.rawLedgerBytes ++ enc.serializeLine e) :
      CStep enc .C_APPEND_OK r r'
  | rejectIndex (r r' : R_ok enc) (e : Event)
      (bad : e.index ≠ r.val.events.length) (unchanged : r'.val = r.val) :
      CStep enc .C_APPEND_REJECT_INDEX r r'
  | rejectPrev (r r' : R_ok enc) (e : Event)
      (index : e.index = r.val.events.length)
      (bad : e.prev_hash ≠ concreteHead r.val.events) (unchanged : r'.val = r.val) :
      CStep enc .C_APPEND_REJECT_PREV r r'
  | rejectIntegrity (r r' : R_ok enc) (e : Event)
      (index : e.index = r.val.events.length)
      (prev : e.prev_hash = concreteHead r.val.events)
      (bad : ¬ (enc.integrity e = true ∧ e.event_hash = enc.compute_event_hash e))
      (unchanged : r'.val = r.val) : CStep enc .C_APPEND_REJECT_INTEGRITY r r'
  | strictReject (r r' : R_ok enc)
      (rejected : enc.strictVerify r.val.rawLedgerBytes = false)
      (unchanged : r'.val = r.val) :
      CStep enc .C_STRICT_VERIFY_REJECT r r'

def ForwardMatch (H : DigestInput → Digest) (label : Label) (before after : History) : Prop :=
  match label with
  | .C_APPEND_OK => ∃ e, Admissible H before e ∧ after = appendEntry before e
  | _ => after = before

theorem alpha_preserved {enc : Encoding} {r r' : R_ok enc}
    (unchanged : r'.val = r.val) : alpha r' = alpha r := by
  simp only [alpha, unchanged]

theorem alpha_append {enc : Encoding} {r r' : R_ok enc} {e : Event}
    (events : r'.val.events = r.val.events ++ [e]) :
    alpha r' = appendEntry (alpha r) (abstractEntry e) := by
  simp [alpha, events, appendEntry, concreteHead, abstractEntry]

theorem append_admissible {enc : Encoding} {H : DigestInput → Digest}
    (bridge : DigestBridge enc H) (r : R_ok enc) (e : Event)
    (index : e.index = r.val.events.length)
    (prev : e.prev_hash = concreteHead r.val.events)
    (integrity : enc.integrity e = true)
    (digest : e.event_hash = enc.compute_event_hash e) :
    Admissible H (alpha r) (abstractEntry e) := by
  refine ⟨?_, ?_, ?_⟩
  · exact digest.trans (bridge r e index prev integrity digest)
  · exact prev
  · simpa [IndexValid, alpha, abstractEntry] using index

theorem named_step_forward_simulation {enc : Encoding} {H : DigestInput → Digest}
    (bridge : DigestBridge enc H) {label : Label} {r r' : R_ok enc}
    (step : CStep enc label r r') : ForwardMatch H label (alpha r) (alpha r') := by
  cases step with
  | load _ _ unchanged => exact alpha_preserved unchanged
  | verify _ _ _accepted unchanged => exact alpha_preserved unchanged
  | append r r' e index prev integrity digest events _bytes =>
      exact ⟨abstractEntry e, append_admissible bridge r e index prev integrity digest, alpha_append events⟩
  | rejectIndex _ _ _ _ unchanged => exact alpha_preserved unchanged
  | rejectPrev _ _ _ _ _ unchanged => exact alpha_preserved unchanged
  | rejectIntegrity _ _ _ _ _ _ unchanged => exact alpha_preserved unchanged
  | strictReject _ _ _rejected unchanged => exact alpha_preserved unchanged

theorem C_LOAD_OK {enc : Encoding} {H : DigestInput → Digest}
    (bridge : DigestBridge enc H) {r r' : R_ok enc} (s : CStep enc .C_LOAD_OK r r') :
    ForwardMatch H .C_LOAD_OK (alpha r) (alpha r') := named_step_forward_simulation bridge s
theorem C_VERIFY_OK {enc : Encoding} {H : DigestInput → Digest}
    (bridge : DigestBridge enc H) {r r' : R_ok enc} (s : CStep enc .C_VERIFY_OK r r') :
    ForwardMatch H .C_VERIFY_OK (alpha r) (alpha r') := named_step_forward_simulation bridge s
theorem C_APPEND_OK {enc : Encoding} {H : DigestInput → Digest}
    (bridge : DigestBridge enc H) {r r' : R_ok enc} (s : CStep enc .C_APPEND_OK r r') :
    ForwardMatch H .C_APPEND_OK (alpha r) (alpha r') := named_step_forward_simulation bridge s
theorem C_APPEND_REJECT_INDEX {enc : Encoding} {H : DigestInput → Digest}
    (bridge : DigestBridge enc H) {r r' : R_ok enc} (s : CStep enc .C_APPEND_REJECT_INDEX r r') :
    ForwardMatch H .C_APPEND_REJECT_INDEX (alpha r) (alpha r') := named_step_forward_simulation bridge s
theorem C_APPEND_REJECT_PREV {enc : Encoding} {H : DigestInput → Digest}
    (bridge : DigestBridge enc H) {r r' : R_ok enc} (s : CStep enc .C_APPEND_REJECT_PREV r r') :
    ForwardMatch H .C_APPEND_REJECT_PREV (alpha r) (alpha r') := named_step_forward_simulation bridge s
theorem C_APPEND_REJECT_INTEGRITY {enc : Encoding} {H : DigestInput → Digest}
    (bridge : DigestBridge enc H) {r r' : R_ok enc} (s : CStep enc .C_APPEND_REJECT_INTEGRITY r r') :
    ForwardMatch H .C_APPEND_REJECT_INTEGRITY (alpha r) (alpha r') := named_step_forward_simulation bridge s
theorem C_STRICT_VERIFY_REJECT {enc : Encoding} {H : DigestInput → Digest}
    (bridge : DigestBridge enc H) {r r' : R_ok enc} (s : CStep enc .C_STRICT_VERIFY_REJECT r r') :
    ForwardMatch H .C_STRICT_VERIFY_REJECT (alpha r) (alpha r') := named_step_forward_simulation bridge s

theorem append_valid_extension {enc : Encoding} {H : DigestInput → Digest}
    (bridge : DigestBridge enc H) {r r' : R_ok enc} (s : CStep enc .C_APPEND_OK r r') :
    ValidExtension H (alpha r) (alpha r') := by
  rcases C_APPEND_OK bridge s with ⟨e, hadm, heq⟩
  rw [heq]
  exact .step (.refl _) e hadm

end AOForward
