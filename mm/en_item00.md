`En_Item00` Actor
=================

## Piece of Heart

Variable: `0x??06`

This field is read:
- In Function: `0x800A640C`
  - At: `0x800A6420`
  - At: `0x800A6458`
  - At: `0x800A65B0`
  - At: `0x800A65E0`
- In Function: `0x800A6B98`
  - At: `0x800A6CDC`
- In Function: `0x800A7128`
  - At: `0x800A714C`
  - This call checks if type is in proper range, which is `[0, 0x1C]`.
  - If so, it uses type (multiplies by 4) to load a function from a table at `0x801DBFF4`.
    - From a second look, this might be a compiled `switch` statement? Each branch is into the same function.
  - It then branches.
    - For Heart Piece (`0x06`) branches to: `0x800A7184`
      - This ends up calling the function: `0x800A75B8`
    - Args:
      - `A0` = `z2_actor_t *`
      - `A1` = `z2_game_t *`

Function: `0x800A75B8(z2_actor_t *actor, z2_game_t *game)`
- Definitely seems like a draw function for Heart Piece.
  - It calls the same pre-draw function we see the skulltula token call (`0x800B8118`)
  - Calls `0x80181A40(z2_gfx_t *gfx)`

Function: `0x8012C2DC(z2_gfx_t *gfx)`
- Writes a display list instruction to make Heart Piece draw properly?
- `0xDE000000 0x801C13A0`
- ... or: `gsSPDisplayList(0x801C13A0)`

## Segments

Writes display list instructions for Heart Piece segment: `0x800B9B9C`
- Function: `0x800B9A04`
  - Return: `0x800BA5B0`
- Writes address at: `0x800B9BBC`
- Instructions: `0xDB060018 <address>`
  - Note: The `0x18` offset is `(6 * 4)`, since this is segment 6 and each pointer is 4 bytes.
  - Address points to Object 1 on the heap (for Heart Piece at least).
    - Address: `0x8055FF40`
  - Reference function: `gsSPSegment(6, address)`
- Loads address from `0x803E6B20 +0x17D98`, thus `&(z2_game) +0x17D98`.
  - `z2_game.obj_ctxt.obj[0].data`

## Get-Item

Function pointer is called during Heart Piece Get-Item function: `0x800EF2AC`
- This calls the function `0x8012C2DC` listed above.

### Objects

Object lists:
- MM: https://wiki.cloudmodding.com/mm/Object_List_(U)
- OoT: https://wiki.cloudmodding.com/oot/Object_Table/NTSC_1.0

In OoT, get-item Heart Piece is in object `0xBD`, or `object_gi_hearts`, shortly after `0xB7` (`object_gi_heart`).

In MM, `object_gi_hearts` is not documented, but from comparison is obviously object `0x96`.

However, when getting a Heart Piece, Spectrum does not show this object in memory and I'm not sure why?

## Actor Rotation

Field used for rotation: `(z2_actor_t +0xBE)`
- Or: `actor.rot_2.y`
- Goes from: `0xC4C0` -> `0xC880` -> `0xCC40`
- Thus seems to increase by `0x3C0` per frame.

## Temp

Skulltula Token Draw: 0x80413C3C (Offset 0x2EC)
VROM: 0xDFFA8C

```
413950:413D70 AF 00E3:  0000 01 FILE: 00DFF7A0:00DFFBC0 INIT 80413C90:00DFFAE0
```
