Frozen
======

Frozen timer: `0x80400898` (`0x803FFDB0 +0xAE8`)

Written to at: `0x8074B384`
- Function: `0x8074B318`
- Return: `0x80771BC4`
- Return Function:`0x80771B60`
  - Return: `0x80762F78`
  - Called from function pointer at: `0x804004F8` (`0x803FFDB0 +0x748`)
  - Function pointer seems to be tied to specific actions.
  - Frozen function pointer: `0x80771B60`
  - Function pointer is set at: `0x8074EA84`
    - Function: `0x8074E924`
    - Return (when freezing): `0x80751084`
      - Return Function: `0x80750FA8`
    - Seems to be checking bytes at:
      - `0x803FFDB0 +0x147` (`0x803FFEF7`)
      - `0x803FFDB0 +0x14A` (`0x803FFEFA`)
      - Might be used in some state transition?

Function: `0x80750FA8`
- Only called once when starting freeze
- Return: `0x80751FAC`
- Normally jumps past freeze code at: `0x80751E80`
  - This actually seems to process all damage, not just freeze damage.
  - The frozen part is determined by the damage effect type, stored in `0x005C (SP)`.

## Tracing Function: `0x80751A90`

When in invincibility frames:
- 0x1AAC: Branch -> 0x1AD4
- 0x1B04: No branch
- 0x1B10: No branch
- 0x1B24: No
- 0x1B34: No
- 0x1B44: Branch -> 0x1BC8
- 0x1BC8: Branch -> 0x1C5C
- 0x1C6C: No
- 0x1C7C: No
- 0x1C88: Branch -> 0x1E04
- 0x1E04: No
- 0x1E0C: No
  - Branches here if in invincibility frame?
  - `V1` seems to contain invincibility frame counter!
  - Getting `V1` from: `0x803FFDB0 +0xD5C`
    - `0x80400B0C‬`
    - First written at: `0x80750E34`
      - Function: `0x80750E28`
      - Return: `0x80751050`
- 0x1E1C: No
- 0x1E28: No
- 0x1E38: No
- 0x1E48: No
- 0x1E58: No
- 0x1E68: Branch -> 0x1E7C
- 0x1E80: Branch -> 0x1FB4

### Crashing on hook when spawning (after Song of Time)

Caused by not returning early from damage process function after freezing Link.
