import Lake
open Lake DSL

package «alpha-omega-mathlib-track» where
  -- Isolated Mathlib theorem track. This package is not part of the root
  -- Lean 4.22.0 governance kernel.

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d568c8c09630de097a046763c17b9ea99f95f950"

@[default_target]
lean_lib MathBuild where
  -- Isolated library root: MathBuild/
