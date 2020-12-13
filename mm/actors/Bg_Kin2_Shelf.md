Bg_Kin2_Shelf
=============

Id:     `0x0211`
Object: `0x01F5`

## Push & Pull Speed

Spectrum output:

```
410FF0:411D80 AF 0211:  0000 04 FILE: 00FD4CB0:00FD5A40 INIT 80411BF0:00FD58B0
411D90:411EF8 AI 0211:  1 02 0 0000 ( -780.0   180.0 -1383.0) 0000 0000 0000
411F10:412078 AI 0211:  1 02 0 0000 ( -750.0   180.0 -1383.0) 0000 0000 0000
412090:4121F8 AI 0211:  1 02 0 0000 ( -810.0   180.0 -1383.0) 0000 0000 0000
412210:412378 AI 0211:  1 02 0 0001 ( -975.0   180.0  -843.0) 0000 4000 0000
```

Writing position value when pushed/pulled: `0x80411918`
- Calls `sinS_to_F` beforehand, input is `s16` in `0x0036 (sp)`.

Seems to always branch at `0x804117D0` to `0x804118B0`.
- Right beforehand, sets `F0`: `LWC1 F0, 0x0160 (S0)` where `S0` is actor data.

Uses value at `*(f32*)(s0 +0x160)` as fraction of current animation?
- Sets to `0.0` at: `0x804116E4`
- Writes value at: `0x804117BC`

Setting `F20`:
- When pushing: hits branch at `0x804118CC` and thus `0x804118D0`
- When pulling: hits `0x804118E4`

### Found It

Function: `0x804116F0`
- Has branch for "smaller shelves" and "larger shelves"
  - Code is seemingly similar to that of the GBT faucets.
  - `0x80411728` - Smaller shelves
    - Uses constants in file at `0x80411C54`, `0x80411C58`
  - `0x8041176C` - Larger shelves
    - Uses constants in file at `0x80411C5C`, `0x80411C60`
