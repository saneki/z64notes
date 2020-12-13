MM Adult Link Diffs
===================

What the MM Adult Link patch changes:
- Clock Town guard text changes.
- Bytes from: `0xBA5E72`, `0xBA5EBC`

General area changes:
- `0x00BC2AC0` (file VROM: `0x00B3C000`) - `code`
- `0x00C25D30` (file VROM: `0x00CA7F00`) - `player_actor`
- `0x00C4DAC0` (file VROM: `0x00CF5950`) - `En_Horse` (Child Epona - Cutscenes)
- `0x00C51040` (file VROM: `0x00CF5950`) - `En_Horse` (Child Epona - Cutscenes)
- `0x00C52C00` (file VROM: `0x00CF5950`) - `En_Horse` (Child Epona - Cutscenes)
- `0x00C8B770` (file VROM: `0x00D3B220`) - `Arms_Hook` (Hookshot)
- `0x00F482F0` (file VROM: `0x00FF8480`) - `En_Zog` (Mikau)
- `0x00F49CA0` (file VROM: `0x00FF8480`) - `En_Zog` (Mikau)
- `0x00FFFFB0` (file VROM: `0x0108B000`) - `gameplay_keep` (Gameplay Keep)
- `0x01034D40` (file VROM: `0x0108B000`) - `gameplay_keep` (Gameplay Keep)
- `0x010A6EE0` (file VROM: `0x0115B000`) - `object_link_child` (Child Link)
- `0x010FB610` (file VROM: `0x011B1000`) - `object_mask_ki_tan` (Keaton Mask - Field Model)
- `0x010FC260` (file VROM: `0x011B2000`) - `object_mask_rabit` (Bunny Hood - Field Model)
- `0x010FC3C0` (file VROM: `0x011B2000`) - `object_mask_rabit` (Bunny Hood - Field Model)
- `0x010FC500` (file VROM: `0x011B2000`) - `object_mask_rabit` (Bunny Hood - Field Model)
- `0x011175B0` (file VROM: `0x011D6000`) - `object_mask_bu_san` (Mask of Scents - Field Model)
- `0x011F5190` (file VROM: `0x012C8000`) - `object_horse_link_child` (Child Epona)

Physical ranges of changed files:
- `En_Horse` physical ROM range:          (`0x0C45470`, `0x0C53F80`)
- Player model object physical ROM range: (`0x10A6E20`, `0x10C5070`)
- Epona model object physical ROM range:  (`0x11F5190`, `0x1203680`)

Object table VROM: `0x00C58C80`
- PROM: `0x00BA87A0`

Tunic colors in new player object:
- `0xBB74`
- `0xBF84`
- `0xCD7C`
- `0xE944`
- `0xF17C`
- `0xF3C4`
- `0xF70C`
- `0x1044C`
- `0x11BEC`

## `En_Zog` changes

```
425BB0:4286C0 AF 0224:  0000 01 FILE: 00FF8480:00FFAF80 INIT 80428100:00FFA9D0
4286D0:4289FC AI 0224:  4 00 28 080F (-1447.3    -8.0  4686.4) 0000 3BFF 0000
```

Changes offsets:
- `0x350`
- `0x1D08`

Thus the absolute addresses:
- `0x80425F00`
- `0x804278B8`

---

```
425FA0:428AB0 AF 0224:  0000 01 FILE: 00FF8480:00FFAF80 INIT 804284F0:00FFA9D0
428AC0:428DEC AI 0224:  4 00 0 080F (-1604.0   -10.3  4671.0) 0000 3BFF 0000
```

Starts actor cutscene at: `0x80428114`
- When checking if cutscene should start:
  - Note: `*(s16*)(actor +0x31A)` is an `index` into `s16` array at `actor +0x30C`
  - `*(u16*)(actor +0x30A) & 4 != 0`
  - `*(s16*)(actor +0x31A) != -1` (checks `index` field)
  - `(s16*)(actor +0x30C)[index] != -1`
  - `func_800F207C() != 0x7C` (calls `z2_ActorCutscene_GetCurrentIndex`)
  - `func_800F1BE4((s16*)(actor +0x30C)[index]) != 0` (calls `ActorCutscene_GetCanPlayNext`)
- This flag is set at: `0x80426824`
  - Function: `0x804267D4`
- This function called by function at: `0x80426838`
- This function called at: `0x80427D3C`
  - Conditions: `*(u16*)(actor +0x90) & 1 != 0`
  - Apparently this actor field is `bgcheck_flags`?

Sets this flag if: `*(f32*)(actor +0x68) <= 0.0`
- Checks if actor Y velocity is less-than or equal 0?
- Stores `0` in this field at: `0x80427D24`

Normally branches at `0x800B7758`, so it doesn't write the flag at `actor +0x90`.
- This is actually checking if the flag already has `flag & 1`, so we need to branch past this check?
- The previous branch is only one which can branch past, at `0x800B7748`.
- This branches if: `0.0 <= *(f32*)(actor +0x88) - *(f32*)(actor +0x28)`
- Thus: `(actor->floor_height - actor->pos_2.y) >= 0.0`
- Seems to be checking difference between Y value of floor under actor, and actor Y value relative to `0.0`.
  - So basically whenever floor under actor is greater-than or equal to `0.0`?
- In other words this flag is checking if actor is "grounded".

### Field `0x31A`

Is index into array of actor cutscene Ids.
- Written to via function: `0x80426838`.
- This function also writes actor cutscene flags: `*(u16*)(actor +0x30A) |= 4`
- Function called at: `0x80427D3C`

### Field `0x90`

Field `0x90`:
- Writes `0x1020` at: `0x800C4790`
- Writes `0x1028` at: `0x800B79E4`
- Writes `0x1028` at: `0x800B7708`
- Writes `0x10A8` at: `0x800B77B0`
- Writes `0x10AA` at: `0x800B7824`
- Writes `0x10AB` at: `0x800B7874`
  - Happens due to field at offset `0x68` being less than 0 (`-4.0`)?

### Mikau Position with Adult Link

Starting point: `C4C88000 C103C348 4591F800`
- XZ position: (`-1604.0`, `4671.0`)

After moving as far as possible: `C44D636B C1009DC1 4594614E`
- XZ position: (`-821.5534`, `4748.163`)
