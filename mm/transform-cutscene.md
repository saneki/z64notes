Transform Cutscene
==================

Loads `pad_pressed` (`game +0x20`) at:
- `0x80772A80` (player actor code)
  - Function: `0x80772884`
  - Checks for flag `0xC00F`, which is: `a || b || c_buttons`
  - This is it.
- `0x8010A5B4`
- `0x80168FE4` (copy function?)
