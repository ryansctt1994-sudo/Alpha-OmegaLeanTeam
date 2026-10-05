import Lake
open Lake DSL

package «alpha-omega-self-model-track» where
  -- Isolated research track for quantitative self-model persistence.
  -- It is not part of the root Lean 4.22.0 governance kernel.

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d568c8c09630de097a046763c17b9ea99f95f950"

@[default_target]
lean_lib SelfModelTrack where
  -- Isolated library root: SelfModelTrack/
