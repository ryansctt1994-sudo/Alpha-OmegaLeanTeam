/-!
# Weaver recovery and replacement semantics

An unclosed request is recovered fail-closed: its original request ID is marked
consumed and its outcome becomes indeterminate. That original record is not
eligible for automatic redispatch.

A replacement request is a different request. It is admissible only when an
explicit authorization is bound to the original request and operation, names a
different request ID, and carries either a reconciliation result or an explicit
duplicate-effect waiver.

Cryptographic verification, durable storage refinement, and physical exactly-once
effects are outside this model.
-/

namespace AlphaOmega.RecoveryReplacement

inductive Outcome where
  | pending
  | pass
  | reject
  | indeterminate
deriving Repr, DecidableEq

structure RequestRecord where
  requestId : String
  operationKey : String
  consumed : Bool
  outcome : Outcome
  authority : Nat
deriving Repr, DecidableEq

def recoverUnclosed (r : RequestRecord) : RequestRecord :=
  { r with consumed := true, outcome := .indeterminate }

def AutoRedispatchAllowed (r : RequestRecord) : Prop :=
  r.consumed = false ∧ r.outcome = .pending

theorem recover_unclosed_consumes_id (r : RequestRecord) :
    (recoverUnclosed r).consumed = true := by
  rfl

theorem recover_unclosed_is_indeterminate (r : RequestRecord) :
    (recoverUnclosed r).outcome = .indeterminate := by
  rfl

theorem recover_unclosed_preserves_request_id (r : RequestRecord) :
    (recoverUnclosed r).requestId = r.requestId := by
  rfl

theorem recover_unclosed_preserves_operation_key (r : RequestRecord) :
    (recoverUnclosed r).operationKey = r.operationKey := by
  rfl

theorem recovered_never_auto_redispatches (r : RequestRecord) :
    ¬ AutoRedispatchAllowed (recoverUnclosed r) := by
  simp [AutoRedispatchAllowed, recoverUnclosed]

inductive ReplacementBasis where
  | reconciled
  | duplicateEffectWaiver
deriving Repr, DecidableEq

structure ReplacementAuthorization where
  originalRequestId : String
  replacementRequestId : String
  operationKey : String
  authorized : Bool
  basis : Option ReplacementBasis
deriving Repr, DecidableEq

def ReplacementAllowed
    (original : RequestRecord)
    (auth : ReplacementAuthorization) : Prop :=
  original.consumed = true ∧
  original.outcome = .indeterminate ∧
  auth.authorized = true ∧
  auth.originalRequestId = original.requestId ∧
  auth.operationKey = original.operationKey ∧
  auth.replacementRequestId ≠ original.requestId ∧
  ∃ basis, auth.basis = some basis

theorem replacement_requires_consumed_original
    {original : RequestRecord}
    {auth : ReplacementAuthorization}
    (h : ReplacementAllowed original auth) :
    original.consumed = true := by
  rcases h with ⟨hc, _, _, _, _, _, _⟩
  exact hc

theorem replacement_requires_indeterminate_original
    {original : RequestRecord}
    {auth : ReplacementAuthorization}
    (h : ReplacementAllowed original auth) :
    original.outcome = .indeterminate := by
  rcases h with ⟨_, ho, _, _, _, _, _⟩
  exact ho

theorem replacement_requires_authorization
    {original : RequestRecord}
    {auth : ReplacementAuthorization}
    (h : ReplacementAllowed original auth) :
    auth.authorized = true := by
  rcases h with ⟨_, _, ha, _, _, _, _⟩
  exact ha

theorem replacement_requires_binding
    {original : RequestRecord}
    {auth : ReplacementAuthorization}
    (h : ReplacementAllowed original auth) :
    auth.originalRequestId = original.requestId ∧
    auth.operationKey = original.operationKey := by
  rcases h with ⟨_, _, _, hid, hop, _, _⟩
  exact ⟨hid, hop⟩

theorem replacement_requires_distinct_id
    {original : RequestRecord}
    {auth : ReplacementAuthorization}
    (h : ReplacementAllowed original auth) :
    auth.replacementRequestId ≠ original.requestId := by
  rcases h with ⟨_, _, _, _, _, hneq, _⟩
  exact hneq

theorem replacement_requires_resolution_basis
    {original : RequestRecord}
    {auth : ReplacementAuthorization}
    (h : ReplacementAllowed original auth) :
    ∃ basis, auth.basis = some basis := by
  rcases h with ⟨_, _, _, _, _, _, hbasis⟩
  exact hbasis

def authorityOnly
    (original : RequestRecord)
    (replacementRequestId : String) : ReplacementAuthorization :=
  { originalRequestId := original.requestId
    replacementRequestId := replacementRequestId
    operationKey := original.operationKey
    authorized := true
    basis := none }

theorem authority_only_not_sufficient
    (original : RequestRecord)
    (replacementRequestId : String) :
    ¬ ReplacementAllowed original (authorityOnly original replacementRequestId) := by
  intro h
  rcases h with ⟨_, _, _, _, _, _, ⟨basis, hbasis⟩⟩
  simp [authorityOnly] at hbasis

theorem replacement_keeps_original_nonredispatchable
    {original : RequestRecord}
    {auth : ReplacementAuthorization}
    (h : ReplacementAllowed original auth) :
    ¬ AutoRedispatchAllowed original := by
  have hc := replacement_requires_consumed_original h
  simp [AutoRedispatchAllowed, hc]

end AlphaOmega.RecoveryReplacement
