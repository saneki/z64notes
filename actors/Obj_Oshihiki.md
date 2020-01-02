Obj_Oshihiki (Pushblock)
========================

Info from CloudModding:

```
Pushblock
Id: 007A
Object: 0003
```

## Push Speed

Spectrum output for actor file:
- Loaded at `0x80414DC0`

```
414DC0:416670 AF 007A:  0000 02 FILE: 00D8A370:00D8BC20 INIT 80416360:00D8B910
```

When push speed is calculated, it uses the `f32` at: `*(f32*)(actor +0x16C)`
- When initializing push, is set by a small function to the constant value `0x40000000`, or `2.0`.
- This same function (and value) is used for pulls as well.
- Function offset: `0x1084‬`
- Function VROM: `0xD8B3F4`
