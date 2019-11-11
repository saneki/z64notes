Majora's Mask Randomizer - DPAD
===============================

Starting notes:

- OoT randomizer's DPAD implementation is largely in [`dpad.c`][ootr_dpad.c].
- Graphics functions can be found in [glankk's N64 development tools][glankk_n64] repo in
  [`gfxdis.c`][n64_gfxdis.c].

## DPAD Functionality

The DPAD functionality uses the following in-game functions:

- `z64_playsfx` (to play a sound effect)
- `z64_UpdateEquipment` (to update equipment)
- `z64_usebutton` (to use an item)

It also requires knowing the address of the global state structure, called `z64_file` in this case.
For example, `z64_file.iron_boots` is used to check whether or not the iron boots have been obtained.

## DPAD Display

### Sprite Functions

The DPAD display uses the following sprite functions:

- `sprite_load`
- `sprite_draw`

These functions *might* be specific to OoT (depending on the `z64_disp_buf_t` and `sprite_t` types)
and thus may need to be re-coded for MM.

They are defined in [`gfx.c`][ootr_gfx.c].

### N64 Display Functions

It also heavily relies on various display functions from [`gfxdis.c`][n64_gfxdis.c], such as
`gSPDisplayList` and `gDPSetCombineMode`.

### Overlay Display Buffer

When drawing, a display buffer is used and is retrieved like this:

```c
z64_disp_buf_t *db = &(z64_ctxt.gfx->overlay);
```

May need to find and dissect the MM version of `z64_ctxt` to figure out the struct.

## Other Ideas

The way OoT Randomizer implements its assembly/c code (among other things) is really messy?

Might want to abstract a lot of this assembly, C, build scripts, etc into a separate repository.
Some of it could be useful outside of a randomizer context (like playing the original OoT with the
DPAD addition). And then allow other repos to include their own assembly/c code also?

It might also be a good idea to make the assembly/compilation modular somehow. So that randomizer
builds could include multiple pre-compiled patches(?) instead of an all-or-nothing approach.

## Debugging

Deathbasket's notes: https://wiki.cloudmodding.com/mm/Notes/Deathbasket

More RAM notes:
- https://cloudmodding.com/zelda/mm
- https://www.zeldacodes.org/addresses/mm-u (VC version?)

Dump region to get `z64_file_t` structure:
- `0x801EF670` to `0x80506BA0`

Bomber's code: 32451

### OoT Copy-From-VROM

Function: `0x80000DF0`
Example: `copy_from_vrom(0x80206BE0, 0xE021F0, 0x14E0)`

When setting a write breakpoint on dest, hits: `0x8000118C`
- Dest pointer in `S0`.
- Length `0x14E0` in `T6`.

### Bremen Mask

Set write breakpoint: `0x801EF6FF`

When writing Bremen mask to inventory, hits: `0x801142DC`

This is probably inside the function `0x80112E80`, documented by Deathbasket, which puts an item into the inventory.

The call is made at `0x807657E4`.

### Global Context & Graphics Buffer

Global context seems to be: `0x803E6B20`
Following, graphics buffer: `0x801F9CB8`
Overlay display buffer is `+0x2A8`: `0x801F9F60` (seems more likely to be `0x801F9F50` though?)

`Gfx` type as defined in [`gbi.h`][n64_gbi.h_Gfx]:

```c
typedef struct
{
  _Alignas(8)
  uint32_t        hi;
  uint32_t        lo;
} Gfx;
```

[ootr_dpad.c]:https://github.com/TestRunnerSRL/OoT-Randomizer/blob/master/ASM/c/dpad.c
[glankk_n64]:https://github.com/glankk/n64
[ootr_gfx.c]:https://github.com/TestRunnerSRL/OoT-Randomizer/blob/master/ASM/c/gfx.c
[n64_gbi.h_Gfx]:https://github.com/glankk/n64/blob/588d1ff03a9e79f36a17bbbdc2a3a8537251a118/include/n64/gbi.h#L2543
[n64_gfxdis.c]:https://github.com/glankk/n64/blob/master/src/gfxdis/gfxdis.c
