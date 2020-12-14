Goron Roll Effect
=================

## Main DList Instructions

Writes `SetEnvColor(0x9B0000XX)` in `player_actor`: `0x80764094`.
- `XX` is alpha which is set dynamically.

### First `G_DL` Instruction

Immediately afterwards, calls a separate DList in Object `0x14C`.
- Uses segmented base for Object `0x14C`.
- Note: The `G_DL` command to call the DList uses segmented addressing into Object `0x14C`.
  - Instructions: `DE000000 060127B0` (offset `0x127B0`)
- Specific `SetPrimColor` instruction is at offset: `0x127C8`.

### The `G_MOVEWORD` Instruction

Calls a `G_MOVEWORD` with buffer: `0x80249FD8`
- Instructions: `DB060020 80249FD8` (using `0x20` indicates `G_MW_FOG`)
- This instruction is written to at: `0x80130B0C`
  - Function: `0x80130A94`
  - The function seems to both write the `G_MOVEWORD` instruction to the main DList...
  - ... and also build the instructions in the buffer it points to.

This function specifically builds 3 instructions:
- `G_SETPRIMCOLOR` to set the primary color (uses values in pointer in argument `A2`).
- `G_SETENVCOLOR` to set the env color (uses values in pointer in argument `A3`).
- `G_ENDDL` to end the DList.

In this case, `A2` and `A3` point into Object `0x14C`:
- `A2`: `0x80608EF0`
  - This seems to point to a small "color table" used when generating DLists for Goron roll.
- `A3`: `0x80608EFC`
- Object `0x14C`: `[0x805F4890, 0x8060C320)`

Callback chain for this function:
- Return: `0x80130CFC`
  - Return Function: `0x80130C5C`
- Return: `0x80131730`
  - Return Function: `0x80131690`
- Return: `0x801317E4`
  - Return Function: `0x801317C0`
- Return: `0x807640C8`
  - This is the function call!

### Second `G_DL` Instruction

Then calls another `G_DL`:
- Instructions: `DE000000 060134D0` (offset `0x134D0`)
- This draws the red tip of the energy effect? Or nothing?

#### Raw DList

```
D7000002 FFFFFFFF E7000000 00000000
FC272E60 3514E37F FA000080 FF0000FF
DE000000 08000000 E200001C C8104A50
E3001001 00000000 FD900000 06013660
F5900000 07018460 E6000000 00000000
F3000000 073FF200 E7000000 00000000
F5800800 00F18460 F2000000 000FC0FC
FD900000 06013E60 F5900100 07018060
E6000000 00000000 F3000000 073FF200
E7000000 00000000 F5800900 01F18060
F2000000 010FC0FC D9000000 00210005
01020040 06013140 06000204 00000608
060A0C0E 00101214 06101618 000A1A1C
061E0C20 00221224 0626282A 0008062C
06262E30 00220232 062A282C 001E1634
06361A38 00362E3A 06302E36 00363830
063C2826 003A2E26 062C063E 002C283C
06320200 00000832 06141222 00223214
06341610 00101434 060E0C1E 001E340E
06381A0A 000A0E38 01019032 06013340
D9000000 00210405 06000204 0006080A
060A0406 000C0E10 0610060C 00121416
06160C12 00181A1C 061C1218 001E2022
0622181E 00242628 06281E24 0024022A
06002C2E 002E302A DF000000 00000000
```

## Goron Roll Effect Color Table (Red)

Offset into object `0x14C`: `0x14660`

This is used to draw specifically the "red tip" of the effect.
- Alternates between 2 sets of colors per frame.

```c
struct {
  u8 primColor1[5]; // #FF0000FF, 0x80
  u8 primColor2[5]; // #FF9B00FF, 0x80
  u8 unknown_A[2];  // Unused?
  u8 envColor1[4];  // #640000FF
  u8 envColor2[4];  // #C80000FF
};
```

## Color Combiner Notes

Default color values as HSV:

```
Prim:  #FF9B00 = hsv(36, 100.0, 100.0)
Env:   #9B0000 = hsv(0, 100.0, 60.8)

Prim1: #FF0000 = hsv(0, 100.0, 100.0)
Env1:  #640000 = hsv(0, 100.0, 39.2)

Prim2: #FF9B00 = hsv(36, 100.0, 100.0)
Env2:  #C80000 = hsv(0, 100.0, 78.4)
```

Notes:
- Prim colors always have max Saturation & Value.
- Env colors always have max Saturation, hue locks to multiple of 120?

`#4CD24C`: Combines better with env `#24C024` than env `#246424`.
- `#4CD24C` = `hsv(120, 63.8, 82.4)` (Prim)
- `#246424` = `hsv(120. 64.0, 39.2)` (Env, generated)
- `#24C024` = `hsv(120, 81.3, 75.3)` (Env, draws better)
- `#45C045` = `hsv(120, 64.0, 75.3)` (Env, draws better)
- `#3CA63C` = `hsv(120, 64.0, 65.0)` (Env, better dark colors)

## Punch Color

Writes env color for punch at: `0x80127500`
- Default color: `#FF0000`
- Immediately after, writes `G_DL` instruction to call DList: `0x06011AB8`
- Relevant `G_MOVEWORD`: `DB060018 805C4890`, which points to Goron object (`0x14C`)
  - In this DList, writes Prim color: `FA000080 FFC832FF`
  - Default color: `#FFC832`

Relationship between `#FF9B00` and `#FFC832`:
- `#FF9B00` = `hsv(36, 100.0, 100.0)`
- `#FFC832` = `hsv(44, 80.4, 100.0)`
- Mostly the same except for `5/4` saturation ratio?

Punch is still partly red.
- ~~Related to function call at `0x800B9AA0`?~~
- Writes env color at: `0x80122E50`.
