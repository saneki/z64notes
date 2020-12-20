Deku Colors
===========

## Spin Sparkles

Uses similar effect behavior as FD sparkles.
- Colors are located in `PlayerActor` file at offset: `0x2FEA8`

## Dust Cloud

```
4F6500:4F6CF0 UNKNOWN
...
6EAF20:720000 OVL KS:   01 player_actor
```

Actor info at table entry: `0x801AE4A0`
```
00DE9FB0 00DEA7A0 80977210 80977A00
804F6500 80977910 01000000
```
- Labeled in MM spreadsheet as: `Effect_Ss_Dust`

Writes dust cloud SetPrimColor at: `0x804F692C`
- SetEnvColor at: `0x804F6978`

Writing Env/Prim colors to effect buffer thing: `0x804F660C`
- Stores in effect buffer struct (size `0x60`) at offsets:
  - Env?:  `0x40, 0x42, 0x44`
  - Prim?: `0x48, 0x4A, 0x4C`
  - Uses `s16` or `u16`.
- Loads from stack buffer struct at offsets:
  - Env?:  `0x24, 0x25, 0x26`
  - Prim?: `0x28, 0x29, 0x2A`
  - Uses `u8`.
- Stack buffer struct color data written to at: `0x800B0D80`.
  - Loading from: `0x8071ADC0`
  - File offset: `0x2FEA0`
  - These color values are directly before the sparkle effect colors in `player_actor`.

~~Writing colors to effect buffer thing: `0x804F6090`~~
- ~~Function: `0x804F5FC4`~~

## Flower Petals

Drawing flower petals while in flight:
- Left flower:  `DA380003 80249A68, DE000000 06008C50`
- Right flower: `DA380003 802499E8, DE000000 06008C50`

Relevant segment: `DB060018 805DCF30`
- Object `0x154`: `5DCF30:5E8960 OB 0154    True 011A5000:011B0A30`

### DList `06008C50`

DList at `06008C50` calls two other DLists:
```
DE000000 06008BA0
DE000000 06008AB8
DF000000 00000000
```

Writes call to this DList at: `0x801273D8`

### DList `06008BA0`

Draws yellow center of flower.

```
D7000002 FFFFFFFF
E7000000 00000000
FC12FE04 3FFE77F8
FA0000FF FFBEA0FF
FB000000 00C8FFFF
E200001C C8112078
E7000000 00000000
E3001001 00000000
FD100000 06008C68
F5100000 070D0340
E6000000 00000000
F3000000 070FF200
E7000000 00000000
F5100800 000D0340
F2000000 0003C03C
D9000000 00230005
01009012 06007D80
06000204 00040600
06080A04 000C0804
06040E0C 0004100E
06021004 00040A06
DF000000 00000000
```

### DList `06008AB8`

Draws flower petals.

```
D7000002 FFFFFFFF
E7000000 00000000
FC127E60 FFFFF3F8
E200001C C8112078
E7000000 00000000
E3001001 00000000
FD100000 06008E68
F5100000 070D0340
E6000000 00000000
F3000000 070FF200
E7000000 00000000
F5100800 000D0340
F2000000 0003C03C
FA000080 FFFFFFFF
D9000000 00230005
01020040 06007E10
06000204 00000602
06080206 00040A00
06080C02 000E0806
06101214 00161812
061A1C1E 00101612
0616101A 001E161A
06202224 00222628
062A2C2E 00222824
062E2428 002E282A
06303234 00323634
06363238 00323A38
0636383C 00343E30
DF000000 00000000
```

#### Color Combiner

`FC127E60FFFFF3F8` = `(1, 15, 4, 7, 7, 7, 7, 1, 3, 15, 0, 7, 7, 7, 7, 0)`
- Cycle 1 Color: `(1, 15, 4, 7)`
- Cycle 1 Alpha: `(7, 7,  7, 1)`
- Cycle 2 Color: `(3, 15, 0, 7)`
- Cycle 2 Alpha: `(7, 7,  7, 0)`

Cycles:
- Cycle 1:
  - Color: `(Texel0 - 0) * Shade + 0`
  - Alpha: `(0 - 0) * 0 + Texel0`
  - `MODULATERGBDECALA_PRIM`
- Cycle 2:
  - Color: `(Primitive - 0) * Combine + 0`
  - Alpha: `(0 - 0) * 0 + Combine`

`FC 12 7E 60, FF FF F3 F8`

`FC 12 7E 00, F1 FF F3 F8` => `FC127E00F1FFF3F8`
