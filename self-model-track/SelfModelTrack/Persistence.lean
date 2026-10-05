import Mathlib

/-!
# Quantitative self-model persistence

This module gives a discrete-time, general-pseudometric formulation of
persistence. It is intentionally mathematical rather than psychological.

A world update is contractive with factor L < 1. A boundary/model map is
K-Lipschitz. The observed drift between successive self-model states is then
bounded by a geometric envelope:

  K * dist(x₀, f x₀) * L^n.

The bound tends to zero. Two counterexamples show why the contractivity and
boundary-Lipschitz hypotheses are not decorative.
-/

namespace SelfModelTrack

open Filter

noncomputable section

variable {S M : Type*} [PseudoMetricSpace S] [PseudoMetricSpace M]

structure ContractiveDynamics (S : Type*) [PseudoMetricSpace S] where
  step : S → S
  factor : NNReal
  lipschitz : LipschitzWith factor step
  factor_lt_one : factor < 1

structure BoundaryModel (S M : Type*)
    [PseudoMetricSpace S] [PseudoMetricSpace M] where
  observe : S → M
  constant : NNReal
  lipschitz : LipschitzWith constant observe

def worldAt (d : ContractiveDynamics S) (x₀ : S) (n : ℕ) : S :=
  d.step^[n] x₀

def selfModelAt
    (d : ContractiveDynamics S)
    (b : BoundaryModel S M)
    (x₀ : S)
    (n : ℕ) : M :=
  b.observe (worldAt d x₀ n)

def rawObservedDrift
    {A B : Type*}
    [PseudoMetricSpace A]
    [PseudoMetricSpace B]
    (step : A → A)
    (observe : A → B)
    (x₀ : A)
    (n : ℕ) : ℝ :=
  dist (observe (step^[n] x₀)) (observe (step^[n + 1] x₀))

def trackingDrift
    (d : ContractiveDynamics S)
    (b : BoundaryModel S M)
    (x₀ : S)
    (n : ℕ) : ℝ :=
  rawObservedDrift d.step b.observe x₀ n

def driftBound
    (d : ContractiveDynamics S)
    (b : BoundaryModel S M)
    (x₀ : S)
    (n : ℕ) : ℝ :=
  (b.constant : ℝ) * (dist x₀ (d.step x₀) * (d.factor : ℝ) ^ n)

def QuantitativePersistence
    (d : ContractiveDynamics S)
    (b : BoundaryModel S M)
    (x₀ : S)
    (ε : ℕ → ℝ) : Prop :=
  ∀ n, trackingDrift d b x₀ n ≤ ε n

theorem world_step_geometric
    (d : ContractiveDynamics S)
    (x₀ : S)
    (n : ℕ) :
    dist (worldAt d x₀ n) (worldAt d x₀ (n + 1)) ≤
      dist x₀ (d.step x₀) * (d.factor : ℝ) ^ n := by
  simpa [worldAt] using d.lipschitz.dist_iterate_succ_le_geometric x₀ n

theorem boundary_drift_geometric
    (d : ContractiveDynamics S)
    (b : BoundaryModel S M)
    (x₀ : S)
    (n : ℕ) :
    trackingDrift d b x₀ n ≤ driftBound d b x₀ n := by
  calc
    trackingDrift d b x₀ n
        = dist (b.observe (worldAt d x₀ n))
            (b.observe (worldAt d x₀ (n + 1))) := by
              rfl
    _ ≤ (b.constant : ℝ) *
          dist (worldAt d x₀ n) (worldAt d x₀ (n + 1)) := by
          exact b.lipschitz.dist_le_mul _ _
    _ ≤ (b.constant : ℝ) *
          (dist x₀ (d.step x₀) * (d.factor : ℝ) ^ n) := by
          exact mul_le_mul_of_nonneg_left (world_step_geometric d x₀ n)
            b.constant.coe_nonneg
    _ = driftBound d b x₀ n := by
          rfl

theorem quantitative_persistence
    (d : ContractiveDynamics S)
    (b : BoundaryModel S M)
    (x₀ : S) :
    QuantitativePersistence d b x₀ (driftBound d b x₀) := by
  intro n
  exact boundary_drift_geometric d b x₀ n

theorem drift_bound_tendsto_zero
    (d : ContractiveDynamics S)
    (b : BoundaryModel S M)
    (x₀ : S) :
    Tendsto (fun n : ℕ => driftBound d b x₀ n) atTop (𝓝 0) := by
  have hfactor : (d.factor : ℝ) < 1 := by
    exact_mod_cast d.factor_lt_one
  have hpow :
      Tendsto (fun n : ℕ => (d.factor : ℝ) ^ n) atTop (𝓝 0) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one d.factor.coe_nonneg hfactor
  have hmul :
      Tendsto
        (fun n : ℕ =>
          (b.constant : ℝ) *
            (dist x₀ (d.step x₀) * (d.factor : ℝ) ^ n))
        atTop
        (𝓝 ((b.constant : ℝ) * (dist x₀ (d.step x₀) * 0))) :=
    tendsto_const_nhds.mul (tendsto_const_nhds.mul hpow)
  simpa [driftBound] using hmul

theorem tracking_drift_tendsto_zero
    (d : ContractiveDynamics S)
    (b : BoundaryModel S M)
    (x₀ : S) :
    Tendsto (fun n : ℕ => trackingDrift d b x₀ n) atTop (𝓝 0) := by
  exact squeeze_zero
    (fun _ => dist_nonneg)
    (fun n => boundary_drift_geometric d b x₀ n)
    (drift_bound_tendsto_zero d b x₀)

section Counterexamples

def expandingWorld (x : ℝ) : ℝ :=
  2 * x

theorem expanding_world_not_contractive :
    ¬ ∃ L : NNReal, L < 1 ∧ LipschitzWith L expandingWorld := by
  rintro ⟨L, hL, hLip⟩
  have h := hLip.dist_le_mul (1 : ℝ) (0 : ℝ)
  have hL' : (L : ℝ) < 1 := by
    exact_mod_cast hL
  norm_num [expandingWorld, Real.dist_eq] at h
  linarith

def halfWorld (x : ℝ) : ℝ :=
  (1 / 2 : ℝ) * x

theorem half_world_lipschitz :
    LipschitzWith (1 / 2 : NNReal) halfWorld := by
  apply LipschitzWith.of_dist_le_mul
  intro x y
  rw [Real.dist_eq, Real.dist_eq]
  change |(1 / 2 : ℝ) * x - (1 / 2 : ℝ) * y| ≤
    (1 / 2 : ℝ) * |x - y|
  rw [show (1 / 2 : ℝ) * x - (1 / 2 : ℝ) * y =
      (1 / 2 : ℝ) * (x - y) by ring]
  rw [abs_mul]
  norm_num

def halfDynamics : ContractiveDynamics ℝ where
  step := halfWorld
  factor := (1 / 2 : NNReal)
  lipschitz := half_world_lipschitz
  factor_lt_one := by norm_num

def inverseBoundary (x : ℝ) : ℝ :=
  x⁻¹

theorem inverse_boundary_not_one_lipschitz :
    ¬ LipschitzWith 1 inverseBoundary := by
  intro h
  have h12 := h.dist_le_mul (1 : ℝ) (1 / 2 : ℝ)
  norm_num [inverseBoundary, Real.dist_eq] at h12

theorem inverse_boundary_drift_grows :
    rawObservedDrift halfWorld inverseBoundary (1 : ℝ) 1 >
      rawObservedDrift halfWorld inverseBoundary (1 : ℝ) 0 := by
  norm_num [rawObservedDrift, halfWorld, inverseBoundary,
    Function.iterate_succ_apply, Real.dist_eq]

end Counterexamples

end SelfModelTrack
