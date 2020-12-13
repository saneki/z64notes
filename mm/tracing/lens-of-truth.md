Lens of Truth
=============

## Display Lists

Looking at display list at: `0x8022E4B8`
- When Lens of Truth is equipped, new instructions starting at `0x8022E538`.
- Writes to the display list here: `0x800BA23C`
  - Function: `0x800B9EF4`
  - Breakpoint isn't hit when Lens is not equipped!

Function: `0x800B9EF4`
- Not hit unless Lens is equipped.
- Return: `0x800BA67C`
- Return Function: `0x800BA42C`

Function: `0x800BA42C`
- Branch occurs at: `0x800BA668`
  - Only calls `0x800B9EF4` if: `T4 != 0`

`T4` increments by 20 per frame, when Lens is first equipped:
- `0x14`
- `0x28`
- `0x3C`
- `0x50`
- `0x64`

When un-equipping, decrements by 10 per frame:
- `0x5A`
- `0x50`
- `0x46`
- `0x3C`
- `0x32`
- `0x28`
- `0x1E`
- `0x14`
- `0x0A`

This makes sense as it zooms in about twice as fast as it zooms out.

`T4` is obtained from: `*(uint8_t *)(0x803E6B20 +0x1CA4)`
- Address: `0x803E87C4‬`

Also around there:
- Byte at `0x803E87C3`: `0x01` if Lens equipped, `0x00` if not equipped.
- When equipped, written to at: `0x8074ED7C`
  - Function: `0x8074ED50`
- When un-equipped, written to at: `0x800B910C`
  - Function: `0x800B90F4`

Function: `0x8074ED50`
- Before writing `0x01`, checks: `0x803E6B20 +0x1CA3`
  - If `0x00`, sets to `0x01` (equips).
  - Else, calls `0x800B90F4` to do unequip.
