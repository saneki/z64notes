HUD Colours
===========

Pointers:
- Context: `0x803E6B20`
- Gfx:     `0x801F9CB8`
- Overlay: `0x801F9F50‬`
  - Buffer: `0x8020E1A8`
  - Buffer: `0x8022E4B8`
- PolyOpa: `0x801F9F60‬`
  - This is used in the main menu instead of Overlay.
  - Buffer: `0x802105A8`
  - Buffer: `0x802308B8`

## Existing Research

Function: `0x8010069C` (`update_heart_colours` according to DB)
- Return: `0x8012153C`

Function: `0x80101844` (`update_beating_heart` according to DB)
- Return: `0x80121470`
- Signature: `update_beating_heart(z64_game_t *game);`
- Notes:
  - Seems to use fields:
    - `*(uint16_t *)(game +0x6F1C)`
    - `*(uint16_t *)(game +0x6F1E)`
    - Address: `0x803FDA3C‬`
  - Seems to store fields:
    - `*(int16_t *)(game +0x252)`
    - `*(int16_t *)(game +0x254)`
    - Address: `0x803E6D72‬`

## Main Menu

Display list `SetPrimColor` instructions:
- `0x8077A688` writes color of rupee.
  - Writes actual value: `0x8077A6EC`
  - Loads colors from `0x8077F814`
- `0x8077AB58` writes color of heart *container* (or pieces) icon.
  - Writes actual value: `0x8077AB70`
  - Gets alpha from: `*(int16_t *)(0x80406B20 +0x44D4)`
- `0x8077AC34` writes color of hearts.
  - Writes actual value: `0x8077AC78`
  - Loads colors from `0x8077F83C`

The main menu root drawing function seems to be `0x8017377C`.
- This actually seems to call a function pointer, not just used for main menu.
- Actual root function might be `0x8077E3B8`

## Display List Tracing

Display list `SetPrimColor` instructions:
- `0x80118DEC` - Writes color of A button icon.
- `0x8010D234` - Writes color of (part of) magic meter border.
  - Writes actual value: `0x8010D270`
  - This function is used for three different values:
    - Writes `0xFFFFFFFF`
    - Writes `0xFFFFFFFF`
    - Writes `0x64FF78FF`
      - This is the B button background color!
    - See below for more info
  - Loading alpha from `0x0036 (sp)`
  - Loading colors from:
    - `0x002A (sp)`
    - `0x002E (sp)`
    - `0x0032 (sp)`
    - These are stored in caller function starting at: `0x801171B0`
    - They are also all hardcoded!
- `0x8010D3E0` - Writes color of C buttons.
  - Function: `0x8010D2D4`
    - Called 3 times, once per C button?
  - Colors from stack:
    - `0x001E (sp)`
    - `0x0022 (sp)`
    - `0x0026 (sp)`
    - `0x002A (sp)` (alpha)
- `0x80103E7C` - Writes color of green triangle on map.
  - Writes actual value: `0x80103E94`
  - Gets alpha from: `*(int16_t *)(0x803F6B20 +0x6C5C)`
    - Address: `0x803FD77C‬`
- `0x801063B8` - Writes color of red triangle on map.
  - Writes actual value: `0x801063D8`
- `0x80103FB0` - Writes color of something related to chests on map.
- `0x8010D008` - Writes color of B button shadow.
  - Is also used for most of the magic meter shadow.
- `0x8010D314` - Writes color of C button shadows.
- `0x80104890` - Writes color of doors on map (small white squares).
  - For actual value, writes at: `0x80104958`
- `0x8011F440` - Writes color of rupee icon.
  - For actual value, writes at: `0x8011F4A8`
  - Seems to get colors from `0x801BFD2C`
- `0x8011FFA4` - ???
- `0x80100CF0` - Writes color of hearts foreground.
  - Writes actual value: `0x80100D28`
  - Gets colors from:
    - `*(int16_t *)(0x803FD508 +0x236)`
    - `*(int16_t *)(0x803FD508 +0x23A)`
    - `*(int16_t *)(0x803FD508 +0x23E)`
    - Address: `0x803FD73E‬`
    - Secondary heart RGB values seem to be copied from around: `0x801BE990`
      - See instructions at: `0x80100754`
  - These values are written to around: `0x80100738`
  - Does check for double defense heart count at: `0x80100C14`
    - If double defense, branches at: `0x80100CAC -> 0x80100FE8`
    - Writes non beating DD heart color at: `0x801010A0`
      - Reading colors from:
        - `*(int16_t *)0x801F4F60`
        - `*(int16_t *)0x801F4F62`
        - `*(int16_t *)0x801F4F64`
        - Somewhere in `z64_file_t` ???
        - These values are written to at: `0x801008F4`
          - Function: `0x8010069C`
          - This function is also used to set the normal heart colors to constants.
          - Return: `0x8012153C` (within the `draw_hud` function)
- `0x8012009C` - Writes color of rupee number text (when wallet is full).
  - Writes actual value: `0x801200AC`
  - Default color: `0x78FF00FF`
- `0x801198FC` - Writes color of central clock lines.
- `0x801199EC` - Writes color of outer clock line.
- `0x8011A128` - Writes color of clock diamond (not during Inverted SoT?).
  - Default color: `0x00AA64FB`
  - Seems to get alpha from `RA`: `*(int16_t *)0x801BFB2C`
  - This seems to be the entire clock alpha.
- `0x8011A06C` - Writes color of inverted clock diamond.
  - Writes actual value: `0x8011A08C`
  - See section for details
- `0x8011A1B8` - Writes color of clock "1st", etc.
- `0x8011A0B0` - Writes color of clock emblem pulse?
  - Writes actual value: `0x8011A0C8`
- `0x8011A394` - Writes color of emblem sun.
  - Writes actual value: `0x8011A3AC`
  - Default color: `0xFFFF6EFB`
- `0x8011A730` - Writes color of sun.
  - Writes actual value: `0x8011A748`
  - Default color: `0xFF646EFB`
- `0x8011A880` - Writes color of moon.
  - Writes actual value: `0x8011A898`
  - Default color: `0xFFFF37FB`
- `0x801178F0` - Writes color of left C-button triangle.
  - Writes actual value: `0x80117900`
  - Function: `0x80117100`
  - `0x8011787C` - Loads color constant into `T2` (for left C-button)
  - `0x801179EC` - Loads color constant into `T2` (for bottom, right C-buttons)
    - Bottom of loop which branches back up.
- `0x80117924` - Writes color of bottom C-button triangle.
  - Writes actual value: `0x80117934`
- `0x8011794C` - Writes color of right C-button triangle.
  - Writes actual value: `0x8011795C`
- `0x80117F54` - Writes color of inner number for ammo counter (normal, grey).
  - Writes actual value: `0x80117F50`
  - Function: `0x80117BD0`, seems to only write ammo counter.
- `0x80117F14` - Writes color of inner number for ammo counter (max, green).
  - Writes actual value: `0x80117F24`

### The Inverted Clock Diamond Color

- `0x8011A06C` - Writes color of inverted clock diamond.
  - Writes actual value: `0x8011A08C`
  - Gets: `*(int16_t *)0x801BFBCC` (for red value)
  - These values change due to the flashing color.
  - `0x801BFBCC` is written to at:
    - `0x80119CC0` - when increasing
    - `0x80119FF0` - when at floor (`0x00`) or peak (`0x64`)
    - `0x80119C74` - when decreasing
    - At all of these points, timer value stored in `A1`?
      - Counts from `0xF` to `0x0` for either increasing or decreasing.
      - Thus when `0x0` is either at floor or peak.
      - `A1` seems to be read from: `*(int16_t *)0x801BFBE4`
      - Value next to it seems to indicate increasing or decreasing: `*(int16_t *)0x801BFBE8`

`0x801BFBEC` has three pairs of `int16_t` which are the roof and the floor for each color.
- So it is basically alternating between two color values.
- Reads:
  - Reds:   `0x80119B40`
  - Greens: `0x80119C08`
  - Blues:  `0x80119CD4`
- This data seems to be written during boot, decompressed from maybe virtual file address `0xA684D0`.
  - Seems to be part of the first chunk decompressed:
    - `A0`: `0x8009BA10`
    - `A1`: `0x800A5AC0`
    - Yaz0 length is: `0x13E4E0`
    - Return: `0x800811F4`

### Caller of `0x8010D234`

Function: `0x8010CFBC`
- Return: `0x80116A20`
  - Writes: `0xFFFFFFFF`
- Return: `0x80116AA8`
  - Writes: `0xFFFFFFFF`
- Return: `0x801171E8`
  - Writes: `0x64FF78FF`
  - This is the call we're interested in.

#### Old Ignore Me

Function: `0x8010CD98`
- Return: `0x8011A17C`
- Return: `0x8011A208`
- Return: `0x8011F554`
- Oops, this is the wrong function!

## Draw HUD Function

Function: `0x8011F0E0` (`draw_hud`)
- Return: `0x80167F68`
- Notes:
  - Large function that calls other interface functions.
  - Seems to draw the entire HUD.

From my own research, `0x801170B8` seems to be the upper-level function that draws the beating heart.
Function `0x8012C654` seems to draw the black outline for the rupee icon.
Function `0x8010A54C` seems to draw the map.
Function `0x801518B0` seems to draw clock??
Function `0x80119030` draws clock and textboxes.

### Drawing Magic

Function: `0x80116918`

From looking at display list buffer: might be happening around: `0x8011698C`?
- Function: `0x80116918`
- Reads infinite magic flag at: `0x80116E18`
  - This should decide if color is green or blue? Also blinking outline.
  - Infinite magic bit check branches at `0x80116E28`
  - Getting some value from: `0x803FD508 +0x272`
    - Address: `0x803FD77A`
    - This is the magic bar alpha!

### Drawing Map

Function: `0x8010A54C`
- Signature: `draw_map(z64_game_t *game);`

Function: `0x80106644`
- Signature: `draw_map_2(z64_game_t *game, int16_t a1, int16_t a2, int16_t a3);`
  - `A1`: `*(int16_t *)0x801BF550`
  - `A2`: `*(int16_t *)0x801BF554`
  - `A3`: `*(int16_t *)0x801BF558`

Draws display list instructions: `0x80103270`

`0x80109908` - Some function to put map colors in struct pointer?

`0x8010A0A4`: Might be a "do you have a compass" function?
- If returns `0`, jumps to code to draw compass things on map.

`0x8012EE34`: Draws symbols on map (triangles, treasures, etc)

### Drawing Hearts

With 4 total hearts, draws 3rd heart at display list buffer `+0xF0`.
- Address `0x8022E5A8` in my tests (`0x8022E4B8‬ +0xF0`).
- Each (non-beating) heart seems to be drawn by F3DEX2 instructions: `E4`, `E1`, `F1`
- Written to at: `0x801015B0`
  - Function: `0x80100B8C`
  - Return: `0x8011F404`

### Drawing Ammo Count Icon

When drawing, breaks on reading ammo amount:
- `0x80117CD4`
- `0x80117E6C`

From looking at the Display List, this may be due to a lingering `SetEnvColor` that's *supposed* to
be cleared by the magic meter being drawn, but obviously isn't if you don't have magic.
- Writes `SetEnvColor` with `#005000`: `FB 00 00 00` `00 50 00 FF`
  - Writes this at: `0x8011F510`

### Drawing Timer

Testing during Treasure Chest game.

Might be related to function: `0x8010D7D0`
- Seems to draw texture of individual timer char texture (number or colon)
- Return: `0x8011E344`

Timer digits: `0x801BFCE8`
- `0x000A` indicates colon `:`
- Being written around: `0x8011D640`

Check at `0x8011D5E4` jumps past code which draws timer.
- Will not draw timer if: `*(int16_t *)(0x801BF970) == 0x63`

Check at `0x8011D5EC`: Checks byte at `0x801EF670 +0x3DD4`
- Address: `0x801F3434`
- Seems like `0x801EF670 +0x3DD0` is an array of timer state bytes.
  - `[0x4]` - Treasure Chest Game
  - `[0x5]` - Drowning
  - `[0x13]` - Clock tower skull kid
  - `[0x14]` - Honey & Darling
