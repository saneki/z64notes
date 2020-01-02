Camera
======

Human: `44.0`
- Return: `0x800CB72C`
- Function: `0x800CB700`
  - Return: `0x800DEB34`

Read breakpoint on where the result is stored on stack:
- `0x800C3DC8`
  - Moving data from `S3` to `S2`:
    - `S2`: `0x801F99D0`
    - `S3`: `0x801F9AB8`
  - This moved value is then immediately read again at `0x800C3DE4`

## Context & Link Pointers

Cloudmodding notes (for OoT) that camera structs have a Context pointer followed by a Link pointer:
- https://wiki.cloudmodding.com/oot/Cameras

We can find this in (at least) 3 places in the MM global context:
- `0x803E6DCC`
- `0x803E6F44`
- `0x803E7234`

If there pointers are still located at relative offset `+0x7C`, that would mean camera structs are at:
- `0x803E6D50`
- `0x803E6EC8`
- `0x803E71B8‬`

Update: From more research, these are the camera structs:
- `0x803E6D40`
- `0x803E6EB8‬`
- `0x803E7030`
- `0x803E71A8`

Looking at `0x803E6DCC` again:
- If the `Camera S` property is still at `+0x142` like OoT, that would be `+0xC6` relative to the
  Context and Link pointers.
- Thus: `0x803E6E92‬`, and `Camera M` at `0x803E6E94`.
- Breaking on read/write for `0x803E6E94`:
  - Read: `0x800DDF44`
  - Read: `0x8008F214`

I think I've found them (`S`, `M` fields for each camera struct):
- Seem to still be at offset `0x142` in MM as well.
- `0x803E6E80` (link camera)
- `0x803E6FF8` (cutscene camera)
- `0x803E7170‬`
- `0x803E72E8` (other link camera?)

OoT camera structs seem to be `0x16C` in size.
MM camera structs seem to be `0x178` in size.

- Write breakpoint for `0x803E72EB`:
  - `0x8008F228`

## Camera State (Index)

The state value is used for indexing into a table at `0x801B986C`.
- For example, see: `0x800DE360`
- Unlike OoT, each entry is `0xC` in size, instead of `0x8`.
- Seems to have `0x5B` entries, thus the table is `0x444` in size.

## Camera Flags

Offset: `0x14C`
Address: `0x803E6E8C`

Sets `0x200` for swimming at: `0x800DE50C`

## Camera States

- `0x01` Normal
- `0x02` Slightly closer to floor
- `0x03` Camera freezes but follows Link
- `0x04` ??? Seems to restore camera back to `0x01`
- `0x05` Top down glitchy
- `0x06` Camera freezes, no UI, safe
- `0x07` Camera freezes, no UI, safe
- `0x08` Crash?
- `0x09` Crash
- `0x0A` Camera freezes, no UI, safe
  - Used in cutscenes.
- `0x0B` Somewhat zoomed-out top-down? Safe
- `0x0C` Somewhat top-down, restored when using hookshot?
- `0x0D` Like `0x01`?
- `0x0E`
  - Madame Aroma's room
- `0x0F`
  - Milk Bar on stage
- `0x10` Unholy pink
- `0x11` Very slight zoom-in, safe
  - Sewers
  - Grottos
- `0x12` Right above/behind Link, does not change direction
- `0x13` Used for playing Ocarina (not on Link camera)
- `0x14` Similar to `0x13`???
- `0x15` Overhead zoom-in, crashes on change?
- `0x16` Camera freezes, no UI, safe
- `0x17` Camera aligns closer to floor and freezes, crashes on change
- `0x18` Same as `0x17`?
- `0x19` Sweeps around Link
- `0x1A` Crashes
- `0x1B` Little animation from intro, safe?
- `0x1C` Crashes
- `0x1D` Fixed angle but follows Link, safe?
- `0x1E` Somewhat zoomed-out.
- `0x1F`
  - Entering/exiting Dancers/GuruGuru room
- `0x20` Unholy moon
- `0x21` Camera freezes, no UI, safe
- `0x22` Camera freezes, no UI, safe
- `0x23` Bad
- `0x25`
  - Town Shooting Gallery
  - Mayor's Office
- `0x2C`
  - First Day spawn cutscene
  - Transitioning areas
- `0x2D`
  - After entering Stock Pot Inn
- `0x32`
  - Astral Observatory upper staircase
- `0x3A`
  - During Honey & Darling game
- `0x3D`
  - Astral Observatory staircase
  - Milk Bar roof
  - South Clock town on corner chest platform
- `0x3E`
  - Astral Observatory telescope
- `0x3F` Used in Treasure Chest Shop, Astral Observatory, lower to the ground
  - Astral Observatory upper staircase
  - Astral Observatory upper platform
- `0x42` Weird.
- `0x43` Slightly raised.
  - In tall grass in Termina Field.
- `0x44` Slightly raised.
- `0x45` Slightly raised and zoomed out.
- `0x46` Same as `0x01`?
- `0x47` Same as `0x01`?
- `0x48` The world's worst dance party.
- `0x49` Slightly top down, can't aim.
- `0x4A`
  - Astral Observatory upper level
- `0x4B` Slightly lower to the ground
  - Honey & Darling
- `0x50` Camera freezes, zooms-out and follows Link
- `0x51`
  - Stock Pot Inn
  - Town Shooting Gallery when on steps
- `0x53` Slightly raised, safe?
- `0x54` Same as `0x01`?
- `0x55` Constant zoom-in?
- `0x56` Weird zoom before reseting to `0x01`.
- `0x57` Slightly zoomed in.
- `0x58` Same as `0x01`?
- `0x59` Camera repositions then remains fixed.
- `0x5A` Slight zoom/raise.
- `0x5B` Crash, likely past the final entry.
