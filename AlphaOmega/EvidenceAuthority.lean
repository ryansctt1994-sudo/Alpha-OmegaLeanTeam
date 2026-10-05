/-!
# Typed Evidence x Authority lattice skeleton

Evidence and authority are separate coordinates. The product order below makes
that separation explicit. Meet takes the weaker coordinate in each dimension;
adding evidence leaves authority unchanged; capping authority never raises it.

Natural numbers are an abstract order model, not a claim that real-world
assurance has an intrinsic numeric scale.
-/

namespace AlphaOmega.EvidenceAuthority

structure Level where
  evidence : Nat
  authority : Nat
deriving Repr, DecidableEq

def Le (a b : Level) : Prop :=
  a.evidence ≤ b.evidence ∧ a.authority ≤ b.authority

def meet (a b : Level) : Level :=
  { evidence := Nat.min a.evidence b.evidence
    authority := Nat.min a.authority b.authority }

theorem le_refl (a : Level) : Le a a := by
  exact ⟨Nat.le_refl _, Nat.le_refl _⟩

theorem le_trans {a b c : Level} (hab : Le a b) (hbc : Le b c) : Le a c := by
  exact ⟨Nat.le_trans hab.1 hbc.1, Nat.le_trans hab.2 hbc.2⟩

theorem meet_le_left (a b : Level) : Le (meet a b) a := by
  exact ⟨Nat.min_le_left _ _, Nat.min_le_left _ _⟩

theorem meet_le_right (a b : Level) : Le (meet a b) b := by
  exact ⟨Nat.min_le_right _ _, Nat.min_le_right _ _⟩

theorem le_meet {x a b : Level} (hxa : Le x a) (hxb : Le x b) :
    Le x (meet a b) := by
  exact ⟨Nat.le_min.mpr ⟨hxa.1, hxb.1⟩, Nat.le_min.mpr ⟨hxa.2, hxb.2⟩⟩

def addEvidence (s : Level) (newEvidence : Nat) : Level :=
  { s with evidence := Nat.max s.evidence newEvidence }

theorem addEvidence_preserves_authority (s : Level) (newEvidence : Nat) :
    (addEvidence s newEvidence).authority = s.authority := by
  rfl

theorem addEvidence_never_decreases_evidence (s : Level) (newEvidence : Nat) :
    s.evidence ≤ (addEvidence s newEvidence).evidence := by
  exact Nat.le_max_left _ _

def capAuthority (s : Level) (cap : Nat) : Level :=
  { s with authority := Nat.min s.authority cap }

theorem capAuthority_never_raises (s : Level) (cap : Nat) :
    (capAuthority s cap).authority ≤ s.authority := by
  exact Nat.min_le_left _ _

end AlphaOmega.EvidenceAuthority
