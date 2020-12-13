`Obj_Ghaka`
===========

## Pull Speed

Spectrum output:

```
40C420:40CBE0 AF 01FB:  0000 01 FILE: 00FA1560:00FA1D20 INIT 8040CB00:00FA1C40
40CBF0:40CD5C AI 01FB:  6 00 0 00FF (    0.0     6.0   259.0) 0000 0000 0000
```

When pulling, writes position value `*(f32*)(actor +0x2C)` at: `0x8040C844`
- Setting field using `F10`, which is `F4 + F8`
  - `F4` is probably spawn coordinate value, so `F8` is likely distance of pull thus far.
  - `F8` is converted from `T7`, which is a `s16`: `*(s16*)(actor +0x168)`
    - Address of `s16` field: `0x8040CD58`
    - Goes from `0` (before pull) to `64` (pull completed)

Write breakpoint on `0x8040CD58`: breaks on `0x800FEF6C`
- Function: `0x800FEF2C`
- Return: `0x8040C814`
- Call: `func_0x800FEF2C((actor +0x168), 0x64, 1)`
  - This `1` is the amount to increase per frame, increasing it speeds up the pull.
