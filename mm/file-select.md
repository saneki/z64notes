File Select
===========

Vanilla File Select base address: `0x8076F160`

File Select file VRAM: `[0x80804010, 0x80814EB0)`
File Select context VRAM: `0x80813DF0`
- Offset:                 `0xFDE0`
- Vanilla RDRAM:          `0x8077EF40`

## File Info Structure

Struct at field `0x8040AF14` (`0x803E6B20 +0x243F4`):
```c
struct {
    // Each field has array of 4: File 1 SoT, File 2 SoT, File 1 Owl, File 2 Owl
    char zelda3[6][4];
    s16 unknown[4];
    char name[8][4];
    s16 max_health[4];
    s16 cur_health[4];
    u32 flags[4];
    u8 double_defense[4]; // 0 = None, 0x14 = Double Defense
    u16 time[4];
    s16 day[4];
    u8 type[4]; // 0 = SoT, Else = Owl
    s16 rupees[4];
    u8 wallets[4];
    u8 masks[4];
    u8 heart_pieces; // [0, 3]
}
```

## Drawing File Select

### Button Glow for Selection

- `0x8077CB58`: Writes prim color to DList.
  - Gets alpha value from: `*(s16*)(0x803E6B20 +0x244F0)`
  - Seems like color values are at: `+0x244EA, +0x244EC, +0x244EE, +0x244F0`

### Secondary Button Index (Yes / Quit)

- Index: `*(s16*)(0x803E6B20 +0x24482)`
  - Yes = 0, Quit = 1
- Index into 2-entry array: `value = *(s16*)(0x8077F7A0 + (index << 2));`
  - Yes = `0x3AC`, Quit = `0x3B0`
  - Further code:
    - `addr = *(u32*)(0x803E6B20 +0x243E4) + (value << 4);`
    - `*(s16*)(addr +2) + 4`
  - Pointer value: `(0x803E6B20 +0x243E4) == 0x8040AF04`: `0x80246258`
    - This address contains a large vertex buffer.
    - Likely using 4 vertices to define button rectangle to draw, at offsets `0x3AC0` and `0x3B00`.
      - `0x80246258 +0x3AC0 == 0x80249D18`
      - Offset `0x3B80` seems to be glowing button effect for selected button.
- Animation frame when selecting file: `0x803E6B20 +0x2448C`.
  - Used as index into function array: `0x8077F8CC[index]`
  - First few functions:
    - `0x8077D5B0`
    - `0x8077D7B8`
    - `0x8077D8B0`
    - `0x8077D990`

- `0x80778824`: Giant function which writes button vertices?
  - To find vertex buffer: `S3 << 4`
  - Seems to loop through large vertex buffer (`0x80246258`) by `0x40` bytes at a time.

- Stores pointer to vertices in `T9`, see: `0x8077A218`
- When selecting file, sets secondary button index to 0 at: `0x8077D7A0`

Idea for patching:
- When checking button index for specific file, check if `index > 1`.
  - If false, do default behavior.
  - If true, go to custom code which points to custom vertex buffer.
- Use owl icon spot for displaying crash recovery icon.

### Drawing Secondary Buttons DList

`0x8077C864`: Writes segmented address of texture?
- `segaddr = (u32*)0x8077F8B4[(*(s16*)((0x803E6B20 +0x244F6 + (i * 2)))]`
  - `0x803E6B20 +0x244F6 == 0x8040B016`
  - `0x8077F8B4` is array of 4 segaddrs of button textures: Copy, Erase, Yes, Quit

Draw "Yes" button:
```
E7000000 00000000
F5702000 00000000
F2000000 000FC03C
07080C0E 00080E0A
E7000000 00000000
FA000000 6496FFC8
FD700000 010207B0
F5700000 07000000
E6000000 00000000
F3000000 073FF080
```

Draw "Quit" button:
```
E7000000 00000000
F5702000 00000000
F2000000 000FC03C
07000406 00000602
FA000000 6496FFC8
FD700000 01027FB0
F5700000 07000000
E6000000 00000000
F3000000 073FF080
```

### Owl Panel

Branches:
- `0x8077BD4C`: If always branches, will not draw texture for background panels (main or owl save info).
- `0x8077BE14`: If always branches, will not draw texture for background panel (owl save info).

Logic for drawing owl panel:
- `T2 < 5`

## Owl Save - Read Buffer Before Flash Write

Read Trace:
- Break: `0x800913A4`
  - Return: `0x800FECAC`
- Function: `0x800FEC90` (`memcpy`)
  - Return: `0x80147300`

This call is copying the data back into `0x801EF670`.

### Writing Owl Save to Flash

`0x80185B1C`: `DMA_RamToFlash(void *buf, u32 block, u32 block_cnt)`
- Block size is `0x80`.

`0x80185D40`: `WriteFlash(struct thing *arg)`

```c
struct DMA_FlashWriteData {
    u32 type;
    u32 result;
    void *buf;
    u32 block;
    u32 block_cnt;
};

// 0x80185B1C.
void DMA_RamToFlash(void *buf, u32 block, u32 block_cnt);

// Calls DMA_RamToFlash and some other things?
void func_0x80185C24(void *buf, u32 block, u32 block_cnt);

// Calls function 0x80185C24 using values in the struct.
// Decomp calls this: SysFlashrom_ThreadEntry
void func_0x80185D40(struct DMA_FlashWriteData *data);

// Writes values to struct in global memory, then calls function to send message: 0x800957B0(0x801FCE58)
void func_0x80185DDC(void *buf, u32 block, u32 block_cnt);

struct something {
    u32 unk_0x00;
    void *buffer;
    u32 unk_0x08;
    u16 unk_0x0C;
    u16 unk_0x0E;
    u32 block;
    u32 block_cnt;
};

// Writes block and block_cnt to dest structure, and constant 1 to field at offset 0xC.
void func_0x80147008(struct something *dest, u32 block, u32 block_cnt);
```

Two calls are made to function `0x80185DDC` when saving at an owl statue, with the following arguments:
- `(0x80746F20, 0x100, 0x80)`: Call at `0x80147168`
  - Function: `0x80147150`
    - Called at: `0x801585A4`
  - Gets args from: `buf = 0x0004(A0), block = 0x0010(A0), block_cnt = 0x0014(A0)`
  - Writes block and block_cnt fields from:
    - `block     = 0x801C6840 + (*(u32*)(0x801EF670 +0x3CA0) * 8)`
    - `block_cnt = 0x801C6850 + (*(u32*)(0x801EF670 +0x3CA0) * 8)`
- `(0x80746F20, 0x180, 0x80)`: Call at `0x801471E4`
  - Function: `0x80147198`

Function `0x80147314`:
- Clear owl save flag from RDRAM file data.
- Clears `ZELDA3` from RDRAM file data to mark as invalid.
- Recalculates the checksum and writes to RDRAM file data.
- Copies RDRAM file data to buffer for writing to flash later.
- Calls 2 functions for writing to flash (owl save slots), main and backup.
- Restores `ZELDA3` in RDRAM file data.

Notes:
- `0x80746F20` is exactly 0x4000 bytes before player/kaleidoscope: `0x8074AF20`
- This is pointed to at: `0x803EB1DC == 0x803E6B20 +0x46BC`

When loading owl save slots, the game invalidates them by calling `0x80185DDC`:
- Called at: `0x80185F6C`
  - Function: `0x80185F64`
- Called at: `0x80146ED0`
  - Function: `0x80146EBC`
- Called at: `0x801473A8`, `0x801473C0`
  - Function: `0x80147314`
  - Need to hook these calls and make them conditional? Or just make this entire function conditional.
  - Note: After first call, game processes a bit before the second call. The game is likely requesting a separate thread do the work of writing to flash, and this thread blocks until it is complete.
    - Call to function `0x80185F04` is what resumes the game until next flash.
- Called at: `0x80145454`

## Writing Song of Time To Flash

Calls function to write to flash: `0x80185DDC`
- Called at: `0x80147038`
  - Function: `0x80147020`
- Called at: `0x801584A0`
  - Function: `0x8015680C`
  - Uses struct at: `0x803EB1D8`, or: `0x803E6B20 +0x46B8`

## Owl Spawn

Uses owl index for determining where to spawn.
- Breaks on read at: `0x80145370`
- `value = *(u16*)(0x801C6A58 + (z2_file.owl_load * 2))`
- ... which is then stored in the current scene field of savefile.
- Need to override this behavior if loading from a crash-recovery file.
- This behavior only happens if owl save field is non-0: `z2_file.owl_save != 0`.

### Grotto Exit

Loading grotto exit from: `*(u16*)(0x803FEB20 +0x87A)`
- `0x803FEB20 == 0x803E6B20 +0x18000`
- This final offset: `0x1887A`
- Absolute value: `0x803FF39A`

This field is copied from: `*(u16*)(0x801EF670 +0x3D24)` when leaving a grotto.
- Absolute: `0x801F3394`

## Bird Theft (Takkuri)

```
43C2C0:43F480 AF 0291:  0000 01 FILE: 010756F0:010788A0 INIT 8043F0F0:01078520
43F490:43FE20 AI 0291:  5 00 28 0000 (-3093.4  -202.1  4051.0) 13C8 0448 0000
```

- VROM: `[0x010756F0, 0x010788A0)`
- VRAM: `[0x80C10770, 0x80C13930)`

### Removing Major Items

Removes major items from inventory:
- `0x8043C764`: Removes first empty bottle from inventory?
- `0x8043C808`: Removes GFS from inventory?
- `0x8043C854`: Removes sword from inventory.

These happen in function `0x8043C65C`, which is only called when Takkuri is stealing a major item.
- Called at: `0x8043D72C`

Seems to have a 50% chance to call the function to remove a major item.

Pseudocode:
```
f32 val = RNG_0();
if (val < 0.5) {
    // Call function to remove major item.
}
```

Float array at `0x8043F200` for RNG chances.

### Removing Minor Items

Removes rupees and ammo from inventory:
- `0x8043CE50`: Subtracts rupees from count.
