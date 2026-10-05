/-!
# Authority-preserving evidence transitions

The transition functions below intentionally leave authority unchanged. The
theorems state exactly that design property and nothing about external systems.
-/

namespace AlphaOmega

structure PromotionState where
  evidence : Nat
  authority : Nat
  greenChecks : Nat
  witnesses : Nat
deriving Repr, DecidableEq

def recordEvidence (s : PromotionState) (amount : Nat) : PromotionState :=
  { s with evidence := s.evidence + amount }

def recordGreenCheck (s : PromotionState) : PromotionState :=
  { s with greenChecks := s.greenChecks + 1 }

def recordWitness (s : PromotionState) : PromotionState :=
  { s with witnesses := s.witnesses + 1 }

theorem recordEvidence_preserves_authority (s : PromotionState) (amount : Nat) :
    (recordEvidence s amount).authority = s.authority := by
  rfl

theorem recordGreenCheck_preserves_authority (s : PromotionState) :
    (recordGreenCheck s).authority = s.authority := by
  rfl

theorem recordWitness_preserves_authority (s : PromotionState) :
    (recordWitness s).authority = s.authority := by
  rfl

theorem evidence_growth_without_authority_growth (s : PromotionState) (amount : Nat) :
    (recordEvidence s amount).evidence = s.evidence + amount ∧
    (recordEvidence s amount).authority = s.authority := by
  exact ⟨rfl, rfl⟩

end AlphaOmega
