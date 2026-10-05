/-!
# Claim ceilings

Evidence and authority are independent coordinates. Raising the evidence
coordinate does not raise authority. Capping authority can only preserve or
lower it.
-/

namespace AlphaOmega

structure ClaimCeiling where
  evidence : Nat
  authority : Nat
deriving Repr, DecidableEq

def addEvidence (c : ClaimCeiling) (newEvidence : Nat) : ClaimCeiling :=
  { c with evidence := Nat.max c.evidence newEvidence }

def capAuthority (c : ClaimCeiling) (cap : Nat) : ClaimCeiling :=
  { c with authority := Nat.min c.authority cap }

theorem addEvidence_preserves_authority (c : ClaimCeiling) (newEvidence : Nat) :
    (addEvidence c newEvidence).authority = c.authority := by
  rfl

theorem capAuthority_never_raises (c : ClaimCeiling) (cap : Nat) :
    (capAuthority c cap).authority ≤ c.authority := by
  exact Nat.min_le_left _ _

end AlphaOmega
