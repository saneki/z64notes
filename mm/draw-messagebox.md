Draw Messagebox
===============

Function: `0x80156758`
- Calls function `0x80174A40` to get address of DList to branch to for drawing messagebox.

## Blinker Color

Writes blinker color values to DList at:
- Primitive: `0x80147D34`
- Environment: `0x80147D64`
  - Color bytes:
    - Red:   `T5`
    - Green: `T1`
    - Blue:  `T2`

## Color Values and Timer

See: `0x801CFCD8`.

## Bank Cursor

Writes bank cursor color: `0x80148474`
- Uses color values at: `*(s16*)0x801CFD{28, 2C, 30}`
- These alternate, using color values:
  - Color 1: `0x801CFD10`
  - Color 2: `0x801CFD16`
  - Color glow: `0x801CFD22`
  - Uses exact same colors as message prompt icon.

## Text Colors

Writes text (character) color at: `0x80149B74`

Gets yellow color from: `*(s16*)(0x803FB428 +0x20{18, 1A, 1C, 1E})`
- Address is the colors of the current character being drawn.

### Current Character Color

Normal character color from: `0x803FB428 +0x20{C8, CA, CC}`

#### Special Colors

Current character color is written around: `0x8015AD88`
- This seems to be for writing colored characters only.

Uses base pointer in `V1`: `0x801D083C`
- Offset in `T6`.
- `T6 = T9 * S4`
  - When yellow C-button icon color: `T9 = 3`, `S4 = 6`.
  - Struct entries may be 6 bytes in size?

## Button Note Colors

Writes color of "A" button: `0x80153BE8`
- Gets color values from:
  - `*(s16*)(0x801F6B{0C, 0E, 10})`
  - In order of RBG instead of RGB.
  - Default: `#5096FF`
- "C" button colors are the same format at: `0x801F6B18`
  - Default: `#FFFF32`

These values are not always in memory, they are written when necessary.
- Written at: `0x801475A8`
  - Function called at: `0x80151F90`
- This just writes using hardcoded constants.

The shadow color values of the "A" and "C" notes exist alongside the main colors.
- Value: `#0A0A0A`

### Button Note Blinking

Button icons blink when confirming Scarecrow's Song.

Blinking updates note colors, using differences each frame set at:
- A button: `*(s16*)0x801C6A{80, 84, 88}`
- Also "blinks" the shadow color for A & C buttons (blinks differently for A and C too).

#### Delta Values (Differences)

Delta values are written at:
- A button icon (red): `0x801531DC`

For A button icon (red), writes result of: `V0 / T0`
- Relevant instructions:
  - `T6 = *(s16*)0x801C6A90`
  - `T7 = T6 * 6`
    - Full expression: `T7 = ((T6 << 2) - T6) << 1`
  - `SW T7, 0x0040 (sp)`
  - ...
  - `T8 = 0x0040 (sp)`
  - `T9 = 0x801D0340`
  - `A0 = T8 + T9`
  - `T6 = *(s16*)A0`
  - `A1 = *(s16*)0x801F6B12`
  - `V1 = A1 - T6`
  - `V0 = V1`
- Notes:
  - Value stored in `0x0040 (sp)` is `6` (`1 * 6`).

Basically it seems to be taking color values starting at `0x801D0334`, and the value multiplied by
6 is getting the offset into this table?
- Each "entry" is 6 bytes, 3 `s16` color values.
- Order at start: A button 1, A button 2, A shadow 1, A shadow 2, C button 1, etc...

## Song Grid

Writes color of lines at: `0x80152794`.
- Gets color values from: `*(s16*)(0x803FB428 +0x20{34, 36, 38, 3C})`
  - This address is gotten from: `0x803E6B20 +0x14908`
- Default: `0xFF0000B4`
Writes large note color at: `0x80152B58`.
- Uses hardcoded constant.
- Default: `0xFF6400FF`

### Substruct

Likely a "messagebox context".

Probable struct offset:
- Start:  `0x803FB428`
- Offset: `0x14908`
- Size:   `0x20E0`
Post-struct might start at: `0x803FD508`
- Offset: `0x169E8`
- This is the HUD context.

## Pause Menu

### Song Button Notes

- When drawing static (not playing the song on Pause Menu):
  - Draw color for A button icon: `0x8074C2BC`
  - Draw color for C button icon: `0x8074C2E0`
- When drawing playback:
  - Draw color for A button icon: `0x8074C0F4`
  - Draw color for C button icon: `0x8074C124`
- When drawing while playing:
  - Draw color for A button icon: `0x8074C4F4`
  - Draw color for C button icon: `0x8074C524`

### Menu Selector

- Inner circle of menu selector icon: `0x8075CA18`
  - Uses color values: `*(s16*)0x807607{10, 14, 18}`
- Outer circle (background) of menu selector icon: `0x8075CA68`
  - Uses color values: `*(s16*)0x807607{1C, 20, 24}`
  - Values written to starting at: `0x807573{E0, E4}`.

Good place for struct start: `0x807607C8`

- Yellow inner color 1: `(s16*)0x807607D4`
  - Default: `0xFFFF00`
- Yellow inner color 2: `(s16*)0x807607DA`
  - Default: `0xFFFF00`
- Yellow color outer 1: `(s16*)0x807607F8`
  - Default: `0x000000`
- Yellow color outer 2: `(s16*)0x807607FE`
  - Default: `0xFFA000`

- Blue color inner 1: `(s16*)0x807607E0`
  - Default: `0x6496FF`
- Blue color inner 2: `(s16*)0x807607E6`
  - Default: `0x64FFFF`
- Blue color outer 1: `(s16*)0x80760804`
  - Default: `0x000064`
- Blue color outer 2: `(s16*)0x8076080A`
  - Default: `0x0096FF`

Bleh:
- `T3 = *(s16*)0x80760810)`
- `T1 = V1 / T3`
- `T1 = (s16)T1`

### Pause Menu Trace

Function at `0x80163C0C` calls into `kaleido_scope` code.
- Gets pointer at `0x801F6C04`
- Points to function: `0x8075D258`
  - Offset: `0x12338`
  - VRAM: `0x808283D8`

## Shop Cursor

Curiosity Shop cursor color is written at: `0x80410138`

Uses color values at: `*(u32*)(actor +0x22{0, 4, 8, C})`
- These alternate like other color values do.
- Color values written per frame around: `0x8040F6A4`

Spectrum output:

```
40CC20:4114A0 AF 002A:  0000 01 FILE: 00D222B0:00D26B30 INIT 80410B90:00D26220
```

## Menu Instruction Subtitle

Menu subtitle with instructions: "[C Buttons] to Equip"
- Written using called DList: `DE000000 0B000130`
- Not sure what address is using segment `0x0B`.
- Is set near beginning of root DList: `DB06002C 8065AAD0`
  - Gets address from: `*(u32*)(0x803FD850 +0x17C)`
  - Uses a field in the `pause_ctxt` structure.
- References Object `0x11`: `654E80:6730D0 OB 0011    True 0115B000:01179250`
- Thus the DList is at: `8065AC00`

A button color:
- Segment offset: `0x188`
- Default: `0x0064FF`
C buttons color:
- Segment offset: `0x130`
- Default: `0xFF9600`

Writes background color of subtitle section: `0x80758AD8`
- Default color: `0x968C5AFF`.
- Also used for Z and R buttons.
