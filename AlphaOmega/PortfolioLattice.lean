import AlphaOmega.EvidenceAuthority
import LatticeCore.Deflation

/-!
# Portfolio lattice integration

This module connects the typed Evidence × Authority state directly to the
generic LatticeCore meet/restriction machinery.

Promotion is proof-carrying: minimum evidence, a verified witness, green checks,
and a separate authority grant are all required before the authority coordinate
may increase. Governed promotion is then capped through LatticeCore.restrict.

These are source-model statements only. They do not grant operational authority
or prove runtime refinement.
-/

namespace AlphaOmega.PortfolioLattice

abbrev Level := AlphaOmega.EvidenceAuthority.Level

def Le : Level → Level → Prop :=
  AlphaOmega.EvidenceAuthority.Le

def meet : Level → Level → Level :=
  AlphaOmega.EvidenceAuthority.meet

def levelMeetOrder : LatticeCore.MeetOrder Level where
  le := Le
  refl := AlphaOmega.EvidenceAuthority.le_refl
  trans := AlphaOmega.EvidenceAuthority.le_trans
  antisymm := by
    intro x y hxy hyx
    cases x with
    | mk xe xa =>
      cases y with
      | mk ye ya =>
        change xe ≤ ye ∧ xa ≤ ya at hxy
        change ye ≤ xe ∧ ya ≤ xa at hyx
        have he : xe = ye := Nat.le_antisymm hxy.1 hyx.1
        have ha : xa = ya := Nat.le_antisymm hxy.2 hyx.2
        cases he
        cases ha
        rfl
  meet := meet
  meet_le_left := AlphaOmega.EvidenceAuthority.meet_le_left
  meet_le_right := AlphaOmega.EvidenceAuthority.meet_le_right
  le_meet := AlphaOmega.EvidenceAuthority.le_meet

structure Constraints where
  evidenceCap : Nat
  authorityCap : Nat
deriving Repr, DecidableEq

def asLevel (c : Constraints) : Level :=
  { evidence := c.evidenceCap, authority := c.authorityCap }

def ConstraintsLe (a b : Constraints) : Prop :=
  a.evidenceCap ≤ b.evidenceCap ∧ a.authorityCap ≤ b.authorityCap

def portfolioCap (c : Constraints) (s : Level) : Level :=
  LatticeCore.restrict levelMeetOrder (asLevel c) s

theorem portfolioCap_deflationary (c : Constraints) :
    LatticeCore.Deflationary levelMeetOrder.toOrder (portfolioCap c) :=
  LatticeCore.restrict_deflationary levelMeetOrder (asLevel c)

theorem portfolioCap_monotone (c : Constraints) :
    LatticeCore.Monotone levelMeetOrder.toOrder (portfolioCap c) :=
  LatticeCore.restrict_monotone levelMeetOrder (asLevel c)

theorem portfolioCap_idempotent (c : Constraints) :
    LatticeCore.Idempotent (portfolioCap c) :=
  LatticeCore.restrict_idempotent levelMeetOrder (asLevel c)

theorem portfolioCap_monotone_in_constraints
    {c₁ c₂ : Constraints}
    (h : ConstraintsLe c₁ c₂)
    (s : Level) :
    Le (portfolioCap c₁ s) (portfolioCap c₂ s) := by
  change levelMeetOrder.toOrder.le
    (levelMeetOrder.meet s (asLevel c₁))
    (levelMeetOrder.meet s (asLevel c₂))
  apply levelMeetOrder.le_meet
  · exact levelMeetOrder.meet_le_left _ _
  · have hc : levelMeetOrder.toOrder.le (asLevel c₁) (asLevel c₂) := by
      exact h
    exact levelMeetOrder.trans (levelMeetOrder.meet_le_right _ _) hc

def demote (ceiling : Level) (s : Level) : Level :=
  LatticeCore.restrict levelMeetOrder ceiling s

theorem demotion_deflationary (ceiling : Level) :
    LatticeCore.Deflationary levelMeetOrder.toOrder (demote ceiling) :=
  LatticeCore.restrict_deflationary levelMeetOrder ceiling

theorem demotion_monotone (ceiling : Level) :
    LatticeCore.Monotone levelMeetOrder.toOrder (demote ceiling) :=
  LatticeCore.restrict_monotone levelMeetOrder ceiling

theorem demotion_idempotent (ceiling : Level) :
    LatticeCore.Idempotent (demote ceiling) :=
  LatticeCore.restrict_idempotent levelMeetOrder ceiling

def SupportsAuthorityTier (s : Level) (tier : Nat) : Prop :=
  tier ≤ s.authority

theorem demotion_preserves_shared_lower_tier
    (s ceiling : Level)
    (tier : Nat)
    (hs : SupportsAuthorityTier s tier)
    (hc : SupportsAuthorityTier ceiling tier) :
    SupportsAuthorityTier (demote ceiling s) tier := by
  change tier ≤ Nat.min s.authority ceiling.authority
  exact Nat.le_min.mpr ⟨hs, hc⟩

structure PromotionRequest where
  targetAuthority : Nat
  minimumEvidence : Nat
  witnessVerified : Bool
  checksGreen : Bool
  authorityGranted : Bool
deriving Repr, DecidableEq

def PromotionAuthorized (s : Level) (p : PromotionRequest) : Prop :=
  p.minimumEvidence ≤ s.evidence ∧
  s.authority ≤ p.targetAuthority ∧
  p.witnessVerified = true ∧
  p.checksGreen = true ∧
  p.authorityGranted = true

def promote
    (s : Level)
    (p : PromotionRequest)
    (_h : PromotionAuthorized s p) : Level :=
  { s with authority := p.targetAuthority }

theorem promotion_preserves_evidence
    (s : Level)
    (p : PromotionRequest)
    (h : PromotionAuthorized s p) :
    (promote s p h).evidence = s.evidence := by
  rfl

theorem promotion_never_decreases_authority
    (s : Level)
    (p : PromotionRequest)
    (h : PromotionAuthorized s p) :
    s.authority ≤ (promote s p h).authority := by
  change s.authority ≤ p.targetAuthority
  exact h.2.1

theorem promotion_requires_minimum_evidence
    {s : Level}
    {p : PromotionRequest}
    (h : PromotionAuthorized s p) :
    p.minimumEvidence ≤ s.evidence := by
  exact h.1

theorem promotion_requires_verified_witness
    {s : Level}
    {p : PromotionRequest}
    (h : PromotionAuthorized s p) :
    p.witnessVerified = true := by
  exact h.2.2.1

theorem promotion_requires_green_checks
    {s : Level}
    {p : PromotionRequest}
    (h : PromotionAuthorized s p) :
    p.checksGreen = true := by
  exact h.2.2.2.1

theorem promotion_requires_authority_grant
    {s : Level}
    {p : PromotionRequest}
    (h : PromotionAuthorized s p) :
    p.authorityGranted = true := by
  exact h.2.2.2.2

theorem no_grant_blocks_promotion
    (s : Level)
    (p : PromotionRequest)
    (hgrant : p.authorityGranted = false) :
    ¬ PromotionAuthorized s p := by
  intro h
  have hg := promotion_requires_authority_grant h
  rw [hgrant] at hg
  contradiction

def governedPromote
    (c : Constraints)
    (s : Level)
    (p : PromotionRequest)
    (h : PromotionAuthorized s p) : Level :=
  portfolioCap c (promote s p h)

theorem governed_promotion_is_capped
    (c : Constraints)
    (s : Level)
    (p : PromotionRequest)
    (h : PromotionAuthorized s p) :
    Le (governedPromote c s p h) (promote s p h) := by
  exact portfolioCap_deflationary c (promote s p h)

theorem governed_promotion_respects_evidence_cap
    (c : Constraints)
    (s : Level)
    (p : PromotionRequest)
    (h : PromotionAuthorized s p) :
    (governedPromote c s p h).evidence ≤ c.evidenceCap := by
  change Nat.min s.evidence c.evidenceCap ≤ c.evidenceCap
  exact Nat.min_le_right _ _

theorem governed_promotion_respects_authority_cap
    (c : Constraints)
    (s : Level)
    (p : PromotionRequest)
    (h : PromotionAuthorized s p) :
    (governedPromote c s p h).authority ≤ c.authorityCap := by
  change Nat.min p.targetAuthority c.authorityCap ≤ c.authorityCap
  exact Nat.min_le_right _ _

end AlphaOmega.PortfolioLattice
