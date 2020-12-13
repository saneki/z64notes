Writes action state 2 flag `0x00000060` at: `0x80769118`
- Function: `0x807690F4`
  - Likely the Link callback used when in flying-backwards state (`link +0x748`, or `0x804004F8`).

## Link Callback Function

This is set by function `0x8074E924`, the function is sent via argument in `A2`.

The return address into function which calls this function to set callback to `0x807690F4`:
- Return: `0x8075125C`
- Return Function: `0x80750FA8`

Branching path:
- Does not branch at: `0x80751020`
- Does not branch at: `0x80751030`
- Does not branch at: `0x80751060`
- Branches at: `0x80751068` -> `0x807510E0`
  - Branches if argument passed via `A2 != 3`.
- Branches at: `0x807510E4` -> `0x80751158`
  - Branches if argument passed via `A2 != 4`.
- Branches at: `0x8075117C` -> `0x80751214`
  - Branches if `(link->action_state1 << 4) >= 0`
  - Basically will branch if 5th most-significant bit is not set?
    - This is likely the "swim" bit.

When getting knocked down by the bell via bomb, this function is called once with:
- `A0 = 0x803E6B20`
- `A1 = 0x803FFDB0`
- `A2 = 1`
- `A3 = 0x409D70A4`

Return address: `0x80751C54`
- Return Function: `0x80751A90`
- This function is updated every frame.
- To reach path of calling knockdown function:

Branching path:
- Branches at: `0x80751AAC` -> `0x80751AD4`
- Does not branch at: `0x80751B10`
- Does not branch at: `0x80751B24`
- Does not branch at: `0x80751B34`
- Branches at: `0x80751B44` -> `0x80751BC8`
- Does not branch at: `0x80751BC8` (normally on other frames it does branch here)
  - Branches if `*(u8*)(link +0xB75) == 0`
    - Absolute: `0x80400925`
- Does not branch at: `0x80751BDC`
- Does not branch at: `0x80751BF8`

Sets `link +0xB75` value at: `0x800B8D3C`
- Function: `0x800B8D10`
- Return: `0x800B8D88`
  - Return Function: `0x800B8D50`
  - This function calls `0x800B8D10` to write constant `3` to the Link field.
- Return: `0x800B8DC4`
  - Return Function: `0x800B8D98`
- Return: `0x8042A6D0`
  - This is the bell actor!
  - Return Function: `0x8042A618`

### Branching Path for Bell

Spectrum output for actor `Obj_Bell`, Id: `0x014E`

```
42A380:42AE60 AF 014E:  0000 01 FILE: 00E9F060:00E9FB40 INIT 8042ACE0:00E9F9C0
42AE70:42B098 AI 014E:  6 00 0 0000 (  633.0   284.0  -966.0) 0000 0CCC 0000
```

Branching path to reach call at `0x8042A6C8`:
- Does not branch at: `0x8042A638`
  - Branches if `(*(u8*)(actor +0x16E) & 2) == 0`
  - This seems to branch if bombs are nearby, but not arrows. So only affects some actors?
  - Field for current actor in memory: `0x8042AFDE`
  - This bit is set at: `0x800E67C4` (`OR`-d by 2).
    - Function: `0x800E6760`
  - Apparently it is also part of a struct (field at `0x12`).
- Does not branch at: `0x8042A678`
- Does not branch at: `0x8042A688`
- Does not branch at: `0x8042A6A0`

Tracing of Function `0x800E6760`:
- Return: `0x800E711C`
  - Return Function: `0x800E7060`
  - Called via function pointer.
- Return: `0x800E7444`
  - Return Function: `0x800E7308`
- Return: `0x80167B6C`
  - Return Function: `0x80167814`
- Return: `0x80167EFC`
  - Return Function: `0x80167DE4`
- Return: `0x80168FA4`
  - Return Function: `0x80168F64`
  - Called via function pointer.
- Return: `0x801737A8`
  - Return Function: `0x8017377C`
- Return: `0x80174524`
  - Return Function: `0x801744F8`
- Return: `0x80174890`
  - Return Function: `0x80174868`
- Return: `0x801749D0`
  - Return Function: `0x801748A0`
  - Likely main function.
- Return: `0x80089420`
  - This is before main function.

Function at `0x800E7060`:
- One example of call points into Link's actor data and bell's actor data:
  - `(0x803E6B20, 0x803FF3A4, 0x804002C8, 0x8042AFCC)`
    - `A1` is `game +0x18884`.
    - `A2` points into Link, `A3` points into bell.
  - However, the function `0x800E6760` does not end up being reached.

But how is it obtaining these pointers into actor data?

Data around `0x803FF3A4` seems to contain at least 2 "lists" (arrays of seemingly predefined size)
which points at these structs for currently loaded actors.

These arrays seem to be populated by actors calling the function `0x800E2928`.
- `0x800E2928(z2_game_t *game, z2_game_18884_t *ctxt, void *actor_inner_data)`
