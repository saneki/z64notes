Ice Physics
===========

Updates `z64_link.common.pos1` when sliding at:
- `0x800FF50C`
- This is actually likely to be a `copy_xyzf` function.
- Args:
  - `A0`: `0x803FFDB8` (dest struct)
  - `A1`: `0x803FFDD4` (source struct)
- Return: `0x8076345C`

The data at `0x803FFDD4` is written to at:
- `0x800B69EC`
- Seems to use a different field in `z64_link_t`, which is the delta to the struct at `+0x24`.
  - Adds these values to x, y, z respectively.
  - `+0xA4,0xA8,0xAC`
- Args:
  - `A0`: `0x803FFDB0`
- Return: `0x807621FC`

---

`0x803FFE30` seems to be set to special value when on icy surface.
- This is apparently the `floor_poly` field of an actor, so this makes sense.
- For example, `0x807256E0`.
- Setting this value at: `0x800C1098`

---

Word value that might correspond: `*(uint16_t *)(0x803FFDB0 +0xB72)`
- Address: `0x80400922`
- Writes at: `0x80761338`
- Uses return value from call to: `0x800C9BDC`

Function: `0x800C9BDC`
- Very small function that calls `0x800C9BB8`
- Args:
  - A0: `0x803E7350`
  - A1: `0x80723E20`
  - A2: `0x32`

Function: `0x800C9BB8`
- Very small function that calls `0x800C9694`
- Args:
  - A0: `0x803E7350`
  - A1: `0x80723E20`
  - A2: `0x32`
  - A3: `0x01`

Function: `0x800C9694`
- With the arguments above, gets the word value from `0x80720F04`

### Sound Effects

Breaking on function: `0x801A5CFC`

- Call 1:
  - Args: `(0x80F, 0x803FFE9C, 4, 0x801FD264)`
  - Return: `0x8019F690`
  - Seems to be sound effect of walking on ice floor.
- Call 2:
  - Args: Same as Call 1
  - Return: `0x8019F76C`
- Call 3:
  - Args: `(0xDF, 0x803FFE9C, 4, 0x801FD264)`
  - Return: `0x8019F7C8`
  - Return Function: `0x8019F780`
  - This is it! Is called for multiple frames until sliding ends.
- Call 4:
  - Same as Call 3
- Call 5:
  - Same as Call 3
- Call 6:
  - Same as Call 3

Function: `0x8019F780`
- Return: `0x80761DD4`
- Return Function: `0x80761C14`
- Checks against 2 floats.
  - `*(float *)(0x803FFDB0 +0xAD0) == 0.0 && *(float *)(0x803FFDB0 +0x70) != 0.0`

Function: `0x80761C14`
- Branches that happen when sliding:
  - `0x1C34`: No branch
  - `0x1C44`: No branch
  - `0x1C5C`: No branch
  - `0x1C7C`: Branch
  - `0x1C90`: Branch
  - `0x1CD8`: Branch
  - `0x1D1C`: Branch
  - `0x1D98`: No branch
  - `0x1DB4`: No branch
  - Calls `0x8019F780`
- Branches that happen when not sliding:
  - `0x1C34`: No branch
  - `0x1C44`: Branch
    - Checks: `*(uint32_t *)0x8077FF98 != 5`
    - This value seems to always be `5` when on ice.
    - Stored at: `0x80760FAC`

## Ice Enemy Sound Effects

Plays two sound effects per frame:
- `0x801A5CFC(0x2032, 0x80417F6C, 4, 0x801DB4B0)`
  - Return: `0x8019F1F8`
- `0x801A5CFC(0x31A4, 0x80420B5C, 4, 0x801DB4B0)`
  - Return: `0x8019F1F8`
