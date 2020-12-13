Bg_Dblue_Movebg
===============

Great Bay Temple turn-thingies.
Actor Id: `0x174`

## Rotation

Spectrum output (file and instance):

```
411730:4138B0 AF 0174:  0000 05 FILE: 00E935F0:00E95760 INIT 8041353C:00E953FC
...
42EEA0:42F210 AI 0174:  1 08 0 1331 (  210.0  -215.0  1487.0) 0000 26C1 0000
```

When rotated by Link, updates rotation at: `0x80412568`.
- Seems to use a `f32` as a multiplier at `0x8041368C`.
- Function: `0x804124A8`
  - Return: `0x80412ED8`
  - Return Function: `0x80412EC0`
    - Return: `0x800B974C`

Calls function `0x804124A8` from pointer stored at `actor +0x15C`.

## Timer

Uses a timer field to determine how long the rotation cutscene lasts.
- Amount to increase counter by frame: `*(u16*)(actor +0x188)`
- Timer count: `*(u16*)(actor +0x18A)`

Timer is written to by non-actor function: `0x800FEF2C(u16 *counter, u16 max, s16 increment)`
- Return: `0x80412504`
- This is the same function that writes the rotation as mentioned above, slightly beforehand.

Changing the 3 constants can control the push/pull speed without messing up the animation:
- `0x804124C4` - interval maximum value
  - Offset: `File +0xD94`, `Function +0x1C`
  - VROM: `0xE94384`
- `0x804124CC` - interval increment value
  - Offset: `File +0xD9C`, `Function +0x24`
- `0x804124E0` - interval maximum value + 1
  - Offset: `File +0xDB0`, `Function +0x38`

## One-Way Faucet

The one-way faucet uses a different function for rotation: 0x804120F4
- It uses the same function & fields as the other function to manage the timer.
