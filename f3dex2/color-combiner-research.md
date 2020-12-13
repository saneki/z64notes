Color Combiner Research
=======================

## Stray Fairy Get-Item Model

### Interior Combine Modes

Full arguments:

(2, 3, 14, 1, 1, 7, 6, 1, 3, 5, 0, 5, 7, 7, 7, 0)
(2, 3, 14, 1), (1, 7, 6, 1), (3, 5, 0, 5), (7, 7, 7, 0)

- Cycle 1
  - color0: `(TEXEL1 - PRIMITIVE) * PRIM_LOD_FRAC + TEXEL0`
  - alpha0: `(TEXEL0 - 0) * PRIM_LOD_FRAC + TEXEL0`
- Cycle 2
  - color1: `(PRIMITIVE - ENVIRONMENT) * TEXEL0_ALPHA + ENVIRONMENT`
  - alpha1: `(0 - 0) * 0 + COMBINED`
