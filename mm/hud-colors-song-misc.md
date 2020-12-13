HUD Colors Song Misc
====================

## Score Note

Fancy song note color on left of score:
- Default: `#FF6400FF`
- Written at: `0x80152B58`

## Score Lines

Score lines color:
- Default: `#FF0000B4`
- Written at: `0x80152794`

Gets color & alpha bytes from `s16` array at: `0x803FB428 +0x2034,6,8,C`
- Is within messagebox context: `(s16*)(0x803E6B20 +0x14908 +0x2034)`
- Absolute: `0x803FD45C`

These color & alpha values are first written when entering playing-ocarina state, and are written on 4 different frames.
- Writes hardcoded values: `0x80150C34`
- Function: `0x80150A84`
  - This function seems to initialize certain colors from hardcoded values.
