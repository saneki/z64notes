Pause Context
=============

Pause Code File RDRAM: `0x8074AF20`
Pause Code File VRAM:  `0x808160A0`
Pause context: `0x803FD850`
- Or: `0x803E6B20 +0x16D30`

## Processing A Button

Messagebox Indicator Byte: `0x803FDB09`
- Offset: `0x2B9`
- Written to `0x01` at: `0x80751444`
- Written to `0x00` at: `0x80157D64`

Normally, branch at `0x80751424` is taken, if NOT pressing the A button.

Certain branches to `0x807513EC`:
- However, these branch instructions are only ever hit if hovering over an item.
- They are NOT hit when hovering over an empty slot!
- Branches:
  - `0x807510E8`
  - `0x807510F4`
  - `0x80751104`
  - `0x80751114`
  - `0x80751124`

### Empty Slot Check

The `BEQ` instruction right above them checks for empty slot: `0x807510DC`
- Function: `0x80750B28`
- Function End: `0x80751500`
- Instruction: `BEQ  S1, AT, 0x8075149C`
  - Dest Offset: `0x657C`
  - Dest VRAM: `0x8081C61C`
- `S1` holds the item Id in the selected slot.
- `S1` will be `0x3E7` if slot is empty (`AT` will always be `0x3E7`).

Address `0x807510D4` might be a good place to hook for A-button processing, and if not using
original processing, use this branch to jump near end of function early.
- Offset: `0x61B4`
- VRAM: `0x8081C254`

## Affecting the HUD Context

Value at `0x803FD68C` determines the text on the A button.
- `0xAC0900` for "Decide"

This value gets updated at: `0x80080C38`
- From function call argument `A2`.
- Function: `0x80080C04`
  - Return Addr: `0x801154CC`
  - Return Func: `0x80115428`
    - Return Addr: `0x80115580`
    - Return Func: `0x8011552C`
      - Return Addr: `0x8074D174` (Pause Menu code)
      - This code only hit when switching to "Decide" text.
      - Checks if `*(u16*)(game +0x16BFA)` is `0x06`.
      - Or: `hud_ctxt +0x212`
      - Address: `0x803FD71A`

Loads text "Info" (value `0x15`) at: `0x8074D274`

## HUD C Button Icons Reloading

Loads texture data from `LoadFileFromArchive` function at address: `0x80178DAC`
- Return Addr: `0x80178E6C`
- Return Func: `0x80178E3C`
  - Return Addr: `0x80112BD4`
  - Return Func: `0x80112B40`
    - Return Addr: `0x80752068` (Pause Menu code)

Calling: `func_0x80112B40(z2_game_t *game, u8 button_slot)`.

Gets dest of extracted file from:
- `*(u32*)(game + 0x16B60) + (button_slot * 0x1000)`
- The pointer is at: `hud_ctxt +0x178`

Note: `0x80178E3C` seems to basically be `LoadFileFromArchive`, but translates the VROM addr to
PROM for you.

## A Button Alpha

When in pause menu from an "Item Prompt," A button is always faded (alpha is `0x46`).
- Alpha written to at: `0x8010F0C8`
- Return: `0x801212D0`

Button usability array at: `0x801F3588‬`
- Sets usable at: `0x80751084`
- Sets unusable at: `0x807510B4`
  - Same instruction that sets unusable for "Item Prompt" selection, is only hit once.
  - Check at `0x8075106C`: Don't enable if `*(u32*)(game +0x16818) != 0`
    - Address: `0x803FD338`
