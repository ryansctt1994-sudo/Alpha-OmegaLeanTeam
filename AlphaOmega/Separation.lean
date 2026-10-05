/-!
# Separation countermodels

These theorems formalize non-implication by exhibiting explicit worlds where the
antecedent is present and the claimed consequence is absent. They do not claim
anything stronger about arbitrary implementations.
-/

namespace AlphaOmega

structure ClaimWorld where
  capability : Bool
  evidence : Bool
  witness : Bool
  signed : Bool
  authority : Bool
  truth : Bool
deriving Repr, DecidableEq

def capabilityWithoutAuthority : ClaimWorld :=
  ⟨true, false, false, false, false, false⟩

def evidenceWithoutAuthority : ClaimWorld :=
  ⟨false, true, false, false, false, false⟩

def witnessWithoutEvidence : ClaimWorld :=
  ⟨false, false, true, false, false, false⟩

def signatureWithoutTruth : ClaimWorld :=
  ⟨false, false, false, true, false, false⟩

def signedEvidenceWithoutAuthority : ClaimWorld :=
  ⟨false, true, false, true, false, false⟩

theorem capability_not_sufficient_for_authority :
    ∃ w : ClaimWorld, w.capability = true ∧ w.authority = false := by
  exact ⟨capabilityWithoutAuthority, rfl, rfl⟩

theorem evidence_not_sufficient_for_authority :
    ∃ w : ClaimWorld, w.evidence = true ∧ w.authority = false := by
  exact ⟨evidenceWithoutAuthority, rfl, rfl⟩

theorem witness_not_sufficient_for_evidence :
    ∃ w : ClaimWorld, w.witness = true ∧ w.evidence = false := by
  exact ⟨witnessWithoutEvidence, rfl, rfl⟩

theorem signature_not_sufficient_for_truth :
    ∃ w : ClaimWorld, w.signed = true ∧ w.truth = false := by
  exact ⟨signatureWithoutTruth, rfl, rfl⟩

theorem signed_evidence_not_sufficient_for_authority :
    ∃ w : ClaimWorld, w.signed = true ∧ w.evidence = true ∧ w.authority = false := by
  exact ⟨signedEvidenceWithoutAuthority, rfl, rfl, rfl⟩

end AlphaOmega
