/-!
# Nontrivial union transition preservation

This module replaces the old reflexive identity statement with an explicit
pre-state -> post-state transition model. The transition relation constructs a
new state with a potentially different role, heartbeat, and lease while keeping
the member identity and credit fixed.

These theorems are source-model statements only. They do not establish that an
external union runtime refines this relation.
-/

namespace AlphaOmega.UnionTransition

structure MemberIdentity where
  memberId : String
  repo : String
  publicKey : String
  capabilities : List String
deriving Repr, DecidableEq

inductive Role where
  | orchestrator
  | worker
  | relay
  | observer
deriving Repr, DecidableEq

inductive ValidRoleTransition : Role -> Role -> Prop where
  | orchestrator_to_worker :
      ValidRoleTransition .orchestrator .worker
  | worker_to_relay :
      ValidRoleTransition .worker .relay
  | relay_to_orchestrator :
      ValidRoleTransition .relay .orchestrator
  | worker_to_orchestrator :
      ValidRoleTransition .worker .orchestrator
  | orchestrator_to_observer :
      ValidRoleTransition .orchestrator .observer

structure MemberState where
  identity : MemberIdentity
  role : Role
  credit : Nat
  heartbeat : Nat
  lease : Option String
  live : Bool
deriving Repr, DecidableEq

def applyRoleTransition
    (before : MemberState)
    (nextRole : Role)
    (nextHeartbeat : Nat)
    (nextLease : Option String) : MemberState :=
  { before with
    role := nextRole
    heartbeat := nextHeartbeat
    lease := nextLease }

inductive Transition : MemberState -> MemberState -> Prop where
  | roleChange
      (before : MemberState)
      (nextRole : Role)
      (nextHeartbeat : Nat)
      (nextLease : Option String)
      (valid : ValidRoleTransition before.role nextRole) :
      Transition before (applyRoleTransition before nextRole nextHeartbeat nextLease)

theorem apply_preserves_identity
    (before : MemberState)
    (nextRole : Role)
    (nextHeartbeat : Nat)
    (nextLease : Option String) :
    (applyRoleTransition before nextRole nextHeartbeat nextLease).identity = before.identity := by
  rfl

theorem apply_preserves_member_id
    (before : MemberState)
    (nextRole : Role)
    (nextHeartbeat : Nat)
    (nextLease : Option String) :
    (applyRoleTransition before nextRole nextHeartbeat nextLease).identity.memberId =
      before.identity.memberId := by
  rfl

theorem apply_preserves_credit
    (before : MemberState)
    (nextRole : Role)
    (nextHeartbeat : Nat)
    (nextLease : Option String) :
    (applyRoleTransition before nextRole nextHeartbeat nextLease).credit = before.credit := by
  rfl

theorem legal_transition_preserves_identity
    {before after : MemberState}
    (h : Transition before after) :
    after.identity = before.identity := by
  cases h
  rfl

theorem legal_transition_preserves_member_id
    {before after : MemberState}
    (h : Transition before after) :
    after.identity.memberId = before.identity.memberId := by
  rw [legal_transition_preserves_identity h]

theorem legal_transition_preserves_credit
    {before after : MemberState}
    (h : Transition before after) :
    after.credit = before.credit := by
  cases h
  rfl

end AlphaOmega.UnionTransition
