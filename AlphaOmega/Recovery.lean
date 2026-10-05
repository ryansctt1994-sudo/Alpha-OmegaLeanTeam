/-!
# Fail-closed recovery normalization

An unclosed intent normalizes to an indeterminate outcome, never to execution
success. Re-normalization is idempotent and authority is preserved.
-/

namespace AlphaOmega

inductive RecoveryDisposition where
  | intent
  | indeterminate
  | pass
  | reject
deriving Repr, DecidableEq

def normalizeRecovery : RecoveryDisposition → RecoveryDisposition
  | .intent => .indeterminate
  | d => d

theorem normalizeRecovery_idempotent (d : RecoveryDisposition) :
    normalizeRecovery (normalizeRecovery d) = normalizeRecovery d := by
  cases d <;> rfl

theorem intent_normalizes_to_indeterminate :
    normalizeRecovery .intent = .indeterminate := by
  rfl

theorem intent_does_not_normalize_to_pass :
    normalizeRecovery .intent ≠ .pass := by
  decide

structure RecoveryRecord where
  disposition : RecoveryDisposition
  authority : Nat
deriving Repr, DecidableEq

def normalizeRecord (r : RecoveryRecord) : RecoveryRecord :=
  { r with disposition := normalizeRecovery r.disposition }

theorem normalizeRecord_preserves_authority (r : RecoveryRecord) :
    (normalizeRecord r).authority = r.authority := by
  rfl

end AlphaOmega
