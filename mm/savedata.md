Savedata
========

## Load From New Cycle

Function `0x80144E78(z2_game_t *game, z2_camera_t *camera)`:
- Loads `z2_file` data from flash for new 3-day cycle.
- Expected arg values:
  - Game:   `0x803E6B20`
  - Camera: `0x803E6D40`
    - Likely a union struct which has other uses when in file select.
- Function end: `0x80145468`

## Load From Owl Save

Ultimately, loading from an owl save appears to (mostly) be a simple `memcpy` of `0x3CA0` bytes.
- Seems to set a bunch of bytes after the `memcpy` as well.

Load from owl save trace:
- `0x800913F0`, writes 4-byte value to `z2_file`.
  - Function: `0x800912C0` (`bcopy`)
- Return: `0x800FECAC`
  - Function: `0x800FEC90` (`memcpy`)
- Return: `0x8014502C`
  - Call (owl save):  `memcpy(0x801EF670, 0x80506BA0, 0x3CA0)`
  - Call (new cycle): `memcpy(0x801EF670, 0x80506BA0, 0x100C)`
  - Function: `0x80144E78`

How does it check if an owl save or not to determine the `memcpy` size?
- Dereferences: `0x801C6870 + T2`
- `T2` is loaded from `0x0020 (sp)`, used as index into array of 8 `u32` values:
  - 4 values of `0x100C`
  - 4 values of `0x3CA0`
  - These correspond to how the flash data is laid out:
    - Slot 1 New-Day save (+ backup entry)
    - Slot 2 New-Day save (+ backup entry)
    - Slot 1 Owl-Sta save (+ backup entry)
    - Slot 2 Owl-Sta save (+ backup entry)

## Loading Save Data

When loading from a save, the raw flash data is loaded into a buffer at: `0x80506BA0`

### Zero-ing out `0x4000`-size buffer for save data before loading

Write breakpoint: `0x80089668`
- Function: `0x80089630`, which is `bzero`
- Return: `0x80144EAC`
- Return Function: `0x80144E78`

### Writing save data to buffer before loading

#### Owl save

Writes save data to buffer using call at: `0x80144F4C`
- Calls function: `0x80185968`

#### New 3-day cycle

Writes save data to buffer using call at: `0x80144FC0`
- Calls function: `0x80185968`

#### Differentiating

The game needs to know whether or not to load the owl save entry, or the new cycle entry.
To do this, it checks the byte: `*(u8*)(game +0x2446A)`
- Where `game` is usually `0x803E6B20`
- If `byte == 0`, is a new cycle save. Otherwise is an owl save.

#### Functions

Relevant function: `0x80185968(void *dest, uint chunk_offset, uint chunk_count)`
- Copies flash data into RDRAM buffer.
- Uses chunk offset and count, chunks being `0x80` bytes in size.

### Writing save data to buffer for flash

#### SoT: Likely calculating checksum

Break on write breakpoint: `0x801445FC`
- Function: `0x801445E4`
- Return: `0x8014564C`

#### SoT: Copying data

Call at `0x80145664`: `memcpy(0x80716F20, 0x801EF670, 0x100C)`
- Getting dest pointer from `lw a0, 0x0004 (t1)`, with `T1`: `0x803EB1D8`

#### Owl Statues

The code for the owl statues is in the same function and right above the code for SoT saving.

See: `0x80145560` (call to checksum function).

Differences in `memcpy` sizes:
- Owl save: `0x3CA0`
- SoT save: `0x100C`

#### Buffer is not zero-d

Sometimes it appears that extra data is being written for SoT saves, which should only be `0x100C`
bytes.

However, this isn't the case. The intermediary buffer for writing to flash (at `0x80716F20`) is
never zero-d after owl saving. So if you perform an owl save (which writes `0x3CA0` bytes to the
buffer), then choose another save file and perform a SoT save, only `0x100C` bytes will be copied
to the buffer but the data from the owl save will still be there. The chunk of `0x2000` bytes will
then be written to the file entry in flash. However, when loading the data the game will only
memcpy the first `0x100C` bytes to `z2_file`. Thus this area of the flash save data is not actually
used by the game and may be used by hackers.
