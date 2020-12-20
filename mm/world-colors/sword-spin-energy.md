Sword Spin Energy
=================

Relevant actor files:
```
4D8FD0:4DAF70 AF 0035:  0002 01 FILE: 00D2F5D0:00D31570 INIT 804DAD10:00D31310
```

Relevant objects:
```
52FF40:5C2520 OB 0001    True 0108B000:0111D5E0
```

Writes relevant DList at: `0x804DACD4`
- This is in actor of Id `0x35`: `En_M_Thunder`, Spin Attack & Sword Beam Effects
- Function start: `0x804DA38C`

Sample of graphics instructions this function writes:

```
DB060010 8052FF40
...
DB060018 8052FF40
---
DE000000 801C13A0
DA380003 80247178
DB060020 80247148
FA000080 AAFFFF35
DE000000 04025850 ; SetEnvColor at offset 0xA0: #0000FF80
DE000000 04025970 ; SetEnvColor at offset 0xA0: #0064FF80
FA000080 AAFFFF00
FB000000 0064FF80
DA380003 80247108
DB060024 802470D8
DE000000 040268F0 ; No colors in this DList.
```

- Writes first `SetPrimColor` value: `0x804DA788`
- Writes second `SetPrimColor` value: `0x804DABB0`
- Writes `SetEnvColor` value: `0x804DABC8`

Colors:
- `#AAFFFF` = `hsv(180, 33.3, 100.0)`
- `#0064FF` = `hsv(216, 100.0, 100.0)`
- `#0000FF` = `hsv(240, 100.0, 100.0)`

## Great Spin

```
4D8FD0:4DAF70 AF 0035:  0002 01 FILE: 00D2F5D0:00D31570 INIT 804DAD10:00D31310
```

```
DE000000 801C13A0
DA380003 80247BA8
DB060020 80247B78
FA000080 FFFFAAD4
DE000000 04025DD0 ; SetEnvColor at offset 0xA0: #FF000080
DE000000 04025EF0 ; SetEnvColor at offset 0xA0: #FF640080
FA000080 AAFFFF00
FB000000 0064FF80
DA380003 80247B38
DB060024 80247B08
DE000000 040268F0
```

- Writes first `SetPrimColor` value: `0x804DA684`
- Writes second `SetPrimColor` value: `0x804DABB0`
- Writes `SetEnvColor` value: `0x804DABC8`

Colors:
- `#FFFFAA`
- `#0064FF`
- `#0000FF`

## Fierce Deity Sword Beam

```
4D90D0:4DB070 AF 0035:  0002 01 FILE: 00D2F5D0:00D31570 INIT 804DAE10:00D31310
```

- `0x804DA988`: SetPrimColor `#AAFFFF`
- `0x804DA9A0`: SetEnvColor  `#0064FF`

Prim color seems to correspond to Cyan-Magenta-Yellow:
- `#00AAAA` = Cyan
- `#AA00AA` = Magenta
- `#AAAA00` = Yellow

### Color Combiner

Probably DList: `0x801C13A0`
- `FC127E03 FF0FF3FF`: `(1, 15, 4, 7, 7, 7, 7, 1, 0, 15, 3, 7, 0, 7, 3, 7)`
  - Cycle 1 Color: `(1, 15, 4, 7)`
  - Cycle 1 Alpha: `(7, 7,  7, 1)`
  - Cycle 2 Color: `(0, 15, 3, 7)`
  - Cycle 2 Alpha: `(0, 7,  3, 7)`

- Cycle 1:
  - Color: `(Texel0 - 0) * Shade + 0`
  - Alpha: `(0 - 0) * 0 + Texel0`
  - Names:
    - `MODULATERGBDECALA_PRIM`
    - `MODULATEIDECALA_PRIM`
    - "Multiply texture color and primitive color. Output texture alpha."
- Cycle 2:
  - Color: `(Combine - 0) * Primitive + 0`
  - Alpha: `(Combine - 0) * Shade + 0`

## Fierce Deity Sparkle Effect

```
4D90D0:4DB070 AF 0035:  0002 00 FILE: 00D2F5D0:00D31570 INIT 804DAE10:00D31310
...
6EAF20:720000 OVL KS:   01 player_actor
```

Sparkle effect occurs when Z-targetting.

Writes sparkle colors to "effect buffer?" starting at: `0x804DB1B0`
- Called by: `0x800B063C`
  - Called by: `0x800B1818`
  - Gets `A3` from: `addiu a3, sp, 0x001C`
  - Storing colors on stack via `swl, swr` at: `0x800B17E8`
  - Getting colors from: `0x8071A884` (inner), `0x8071A888` (outer)
  - Default colors: `#64FFFF` and `#006464`
  - File offset: `0x2F964`
- Gets colors from `u8[]`: `0x801F9864 +0x28,9,A`
  - This is on stack.

## Fierce Deity Damage Effect

Writes env color for FD damage effect at: `0x800BF1E8`
- Code looks like a mess similar to shop cursor color, where it *partly* alternates between two colors?
- Not sure if the two colors are static or variable.

## Charging Sword Spin (Attempt 1)

```
414DF0:4161E0 AF 007B:  0000 01 FILE: 00D8BC20:00D8D010 INIT 80416040:00D8CE70
```

- Writes SetPrimColor color value: `0x80415EB8`
  - ???
- Writes blue SetEnvColor color value: `0x80415DAC`
  - These colors don't seem to matter.

Calls DList: `DE000000 04054A90`
- Relevant segment: `DB060010 8056FE60`
- Object 1.
- No colors in it, not even sure if related.

## Charging Sword Spin (Attempt 2)

```
521040:522FE0 AF 0035:  0002 01 FILE: 00D2F5D0:00D31570 INIT 80522D80:00D31310
```

Writes colors around: `0x80522C20`

## Charging Sword Sparks

```
40B510:40C900 AF 007B:  0000 01 FILE: 00D8BC20:00D8D010 INIT 8040C760:00D8CE70
```

Actor table entry:
```
00D8BC20 00D8D010 80918B40 80919F30
8040B510 80919D90 00000000 00000100
```

- `0x8040C49C`: `lui t5, 0xFF00`     => SetEnvColor `#FF0000`
- `0x8040C4C0`: `ori t8, r0, 0xFF00` => SetEnvColor `#0000FF`
