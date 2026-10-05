/-!
# Protected-state invariance

Rejection and failed checks may update diagnostic state, but these transition
functions do not mutate protected state or spend authority-bearing budget.
-/

namespace AlphaOmega

structure KernelState where
  protectedState : Nat
  budget : Nat
  rejected : Bool
  failedChecks : Nat
deriving Repr, DecidableEq

def reject (s : KernelState) : KernelState :=
  { s with rejected := true }

def failedCheck (s : KernelState) : KernelState :=
  { s with failedChecks := s.failedChecks + 1 }

theorem reject_preserves_protected_state (s : KernelState) :
    (reject s).protectedState = s.protectedState := by
  rfl

theorem reject_preserves_budget (s : KernelState) :
    (reject s).budget = s.budget := by
  rfl

theorem failedCheck_preserves_protected_state (s : KernelState) :
    (failedCheck s).protectedState = s.protectedState := by
  rfl

theorem failedCheck_preserves_budget (s : KernelState) :
    (failedCheck s).budget = s.budget := by
  rfl

end AlphaOmega
