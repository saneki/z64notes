Epona C-buttons Fade
====================

- `hud_ctxt +0x30E`
- `0x803E6B20 +0x169E8 +0x30E`

When mounting Epona, C-buttons alpha value is updated by function: `0x8010F1A8`
- Function is called at: `0x8012123C`
This code begins at `0x80121214`, seems to be dynamically branched to from `0x801211A8`.
Uses function table at `0x801DDC4C`, index is from: `*(u16*)(0x801EF670 +0x3F20) - 1`
- Or: `z2_file.buttons_state.transition_state - 1`

Check for Goron Race scene is around `0x8011287C`, in function: ...

Disables C buttons when mounting Epona at: `0x8011206C`
- This code is only reached for frame when preparing to mount Epona
- One branch which determines this seems to be at `0x80111DB0`, will branch if mounting Epona.
  - Branches if: `*(u8*)(link +0x14B) != 3`
- Branch at 0x80111D30 will branch if not mounting Epona?
  - Branches if: `*(s8*)(0x803E6B20 +0x2887C) < 2`
  - Absolute: `0x803FF39C`
- When mounting Epona, will branch past this check at `0x80111CF8`.
  - Branches if: `(*(u32*)(0x803FFDB0 +0xA6C) & 0x800000) != 0`
  - Thus it is checking for the `Z2_ACTION_STATE1_EPONA` flag.
