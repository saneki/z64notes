Fisherman Game Speedup
======================

Relevant Spectrum output:

```
426DB0:428770 AF 0292:  0000 01 FILE: 010788A0:0107A260 INIT 80428490:01079F80
428780:428A84 AI 0292:  4 00 0 0005 ( -631.0   118.0  -711.0) 0000 BE22 0000
```

- VRAM: `0x80C13930`
- VROM: `0x010788A0`
- File entry offset: `0x1CB90`
- File index: `617`

- Actor main: `0x80428288`
- Actor draw: `0x8042839C`

Calls function pointer at offset `0x1D4`.
- During minigame: `0x804276B0`.
- As game ends and he says "All right...That's it!": `0x804274C4`
- After message box: `0x80427978`

As game ends, updates function pointer at: `0x804274B8`
- Function: `0x804274B0`
- Called by: `0x80427948`
- Caller function: `0x804276B0`

Will only reach the above code if: `*(u32*)0x801F3470 == 0 && *(u32*)0x801F3474 == 0`
- Field at `0x801F3474` is some timer that counts down during game, ending at 0.

## Timer Counter

Stores new value as: `0x003C (SP) - 0x00D4 (SP)`

```
// For this timer, value at pointer == 4
// Thus: 0x801EF670 + (4 * 8) == 0x801EF690
T1 = 0x801EF670 + (*(s16*)0x801BF970 * 8);
0x00D4 (SP) = *(u32*)(T1 + 0x3E8C); // 0x801F351C (wrong?)
0x003C (SP) = *(u32*)(T1 + 0x3E1C); // 0x801F34AC
```

Writes `0x00D4 (SP)` at: `0x8011D738`
- This is actual lower bytes of a `s64` integer stored in `0x00D0 (SP)`, the result of function call to `0x800888A8`.

```
s64 x = ...;
// This may likely be getting time in milliseconds?
0x00D0 (SP) = ((x / 3000) / 10000)
```

### Special Note

Timer is checked again after game, and must be 0 to give you the reward! See: `0x804220D8`
- Offset: `0x2D8`

Relevant Spectrum output:
```
421E00:4237C0 AF 0292:  0000 01 FILE: 010788A0:0107A260 INIT 804234E0:01079F80
4237D0:423AD4 AI 0292:  4 00 0 0005 ( -631.0   118.0  -711.0) 0000 C146 0000
```

## Torch Count

Tracks torch count in two places:
- `0x801BF897`
- `0x801F35AA`, or `*(u16*)(file +0x3F3A)`

## Boat Speedup

Relevant Spectrum output:

```
434B80:435310 AF 022C:  0000 01 FILE: 010000B0:01000840 INIT 80435290:010007C0
435320:435488 AI 022C:  1 00 0 047F (-2392.0    -0.8   494.0) FFAD 4721 002D
```

- VRAM: `0x80B9AF50`
- VROM: `0x010000B0`
- File entry offset: `0x1C530`
- File index: `515`

Boat actor variable: `0x047F`
Writes speed of boat while moving at `0x80434FA8`.
Uses field as multiplier: `*(s8*)(actor +0x15D)`

Using byte fields:
- `0x15C`: Boat progress?
- `0x15E`: Boat resting progress number?
- `0x15F`: ???

### Boat Positions

Resting:           (`0xC5158000`, `0x43F70000`)
After moving:      (`0xC508E610`, `0x43E52C29`)
Begin hookshot:    (-318, -318),  or (`0xC39EF9D1`, `0xC39EF9D1`)
Close to platform: (-180, -344),  or (`0xC333F951`, `0xC3AC150D`)
End hookshot:      (-824, -1532), or (`0xC44E343B`, `0xC4BF88CF`)

Median close to platform: (-571, -925)

#### Math Checking

Distance (Begin, Median): 657.6
- 64,009 + 368,449 == 432,458
Distance (Median, End):   657.6
- 64,009 + 368,449 == 432,458
