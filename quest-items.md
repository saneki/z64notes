Quest Items
===========

Quest items by slots:
- Top: Moon's Tear, Deeds
- Middle: Inn Room Key, Express Mail to Mama
- Bottom: Letter to Kafei, Pendant of Memories

## Room Key Check

Room Key item: `0x2D`

There are at least 2 checks for the Room Key item:
- The inn door in East Clock Town
- The room door in the inn itself

When near the door actor En_Door (in East Clock Town), function gets called per frame: `0x8013296C`
- Call: `func_0x8013296C(0x803E6B20, 0x801F99CC, 0x801F99F8)`
- Return: `0x801330A8`
- Return Function: `0x80133038`
- Loads inventory index from: `*(u8*)0x801C20A5`
- Compares the byte in this inventory slot to hardcoded value `0x2D`, which is Room Key.
- If Room Key not in inventory, also checks for Kafei Letter.
- References table at `0x801C2078`, which seems to have inventory slots.
  - There are multiple entries for specific slots, including the quest item slots.
  - Likely each are used for different purposes.
  - Quest items: `[0x801C20A0, 0x801C20AA)`
  - NOTE: Looking again, this table is used to map: Item Id -> Slot Index

Link mask addr: `0x803FFF03`

```c
// 0x8012403C
u8 get_link_mask(z2_game_t *game) {
    // Game + 0x1CCC is the Link pointer
    z2_link_t *link = game->actor_ctxt.actor_list[2].first;
    return link->mask; // Offset: 0x153
}

void * func_0x8013296C(z2_game_t *game, u8 **ppdata, u8 *a2) {
    // A1 deref-ed points into En_Door Actor File data (not Actor Instance).
    // Specifically: Offset 0xEE4‬ (0x805674C4 - 0x805665E0)
    // Data deref-ed points to 3 bytes:
    // [0] = ???, [1] = Lookup Type, [2] = Move-Ahead Amount
    u8* pdata = *ppdata;
    u8 lookup = pdata[1];
    if (lookup == 0) {
        // Room Key check
        // Used for Inn front door & locked room
        u8 idx = *(u8*)0x801C20A5;
        if (z2_file.inventory[idx] == 0x2D) {
            goto label;
        }
    }
    if (lookup == 1) {
        // Kafei Letter check
        // Likely used for door to Kafei's hideout
        u8 idx = *(u8*)0x801C20A7;
        if (z2_file.inventory[idx] == 0x2F) {
            goto label;
        }
    }
    if (lookup == 2) {
        // Romani Mask check for Milk Bar (only checked at 10 PM or after)
        u8 mask = get_link_mask(game);
        if (mask != 7) {
            return 0;
        }
    } else {
        return pdata;
    }
label:
    // Move ahead data pointer
    u8 offset = pdata[2];
    *ppdata = (pdata + offset);
    return 0;
}
```

## Pause Screen Inventory

Pause Context: `0x803FD850` (`0x803E6B20 +0x16D30`)
- Icon Pointers: `0x803FD9B8`
- There are six, and loaded into DList using `gsSPSegment(segment, base)`.

```
DB 06 00 20 80 56 C7 60 // gsSPSegment(G_MWO_SEGMENT_8, 0x8056C760);
DB 06 00 24 80 60 26 20 // gsSPSegment(G_MWO_SEGMENT_9, 0x80602620);
DB 06 00 28 80 62 72 10 // gsSPSegment(G_MWO_SEGMENT_A, 0x80627210);
DB 06 00 30 80 60 9D 20 // gsSPSegment(G_MWO_SEGMENT_C, 0x80609D20);
DB 06 00 34 80 61 E8 10 // gsSPSegment(G_MWO_SEGMENT_D, 0x8061E810);
DB 06 00 2C 80 62 7C 10 // gsSPSegment(G_MWO_SEGMENT_B, 0x80627C10);
```

### Segment Theory

Theory: I think when encountering DList instructions with "weird" RAM addresses, they might
actually be using these segments.

So `FD180000 08040000` means: `G_SETTIMG`, Segment 8, Offset `0x040000`.

### Inventory Draw Function

Draw function: `0x80756DB0`
- Return Address:  `0x80757838`
- Return Function: `0x8075705C`
  - Return Address:  `0x8075D3C8`
  - Return Function: `0x8075D258`
    - Return Address:  `0x80163C7C`
    - Return Function: `0x80163C0C`
    - This likely calls the root draw function for pause menu.

Thus the likely root draw function is: `0x8075D258(z2_game_t *game)`
- Has pointer to `z2_pause_ctxt_t` in `S1` (see: `0x8075D2B4`).

Function call at `0x807509F0` seems to draw individual items for the "Select Item" screen.
- Function: `func_0x80756954(z2_gfx_t *gfx, u32 seg_addr, u16 width, u16 height)`
- Caller uses table at `0x801C1E6C`, to map: Item Id -> Seg Addr
- A0 = `0x801F9CB8` (`0x801EF670 +0xA648‬`)

#### `F3DEX2` Instructions

Dump of DList instructions for drawing the Hookshot icon:

```
// These 4 instructions are from a different instance (probably not Hookshot).
// They also happen before the function call.
E7 00 00 00 00 00 00 00 // gsDPPipeSync();
FC 11 96 23 FF 2F FF FF // gsDPSetCombineLERP(...);
FA 00 00 00 FF FF FF FF // gsDPSetPrimColor(0, 0, 0xFF, 0xFF, 0xFF, 0xFF);
01 00 40 08 80 24 98 98 // gsSPVertex(0x80249898, 4, 0); // Loads 4 vertices from RDRAM

// Instructions that happen during function.
FD 18 00 00 08 00 F0 00 // gsDPSetTextureImage(..., 0x0800F000);
F5 18 00 00 07 00 00 00 // gsDPSetTile(...);
E6 00 00 00 00 00 00 00 // gsDPLoadSync();
F3 00 00 00 07 3F F0 80 // gsDPLoadBlock(...);
E7 00 00 00 00 00 00 00 // gsDPPipeSync();
F5 18 10 00 00 00 00 00 // gsDPSetTile(...);
F2 00 00 00 00 07 C0 7C // gsDPSetTileSize(0, 0, 0, 0x7C, 0x7C);
07 00 04 06 00 00 06 02 // gsSPQuadrangle(0, 4, 6, 2);
```

Example dump of vertices for location of Room Key icon (from `0x80249B58`):
- For vertex structure, see bottom of: http://n64devkit.square7.ch/n64man/gsp/gSPVertex.htm
- From a glance, x and y might be relative to center of screen?
- Top left:     (0x40, 0x1A)
- Bottom right: (0x60, -0x6)

```
0040001A 00000000 00000000 FFFFFFFF
0060001A 00000000 04000000 FFFFFFFF
0040FFFA 00000000 00000400 FFFFFFFF
0060FFFA 00000000 04000400 FFFFFFFF
```

Spectrum output for drawing Room Key in inventory:

```
80212138: FA000000 FFFFFFFF // G_SETPRIMCOLOR
80212140: 01004008 80229848 // G_VTX
80212148: FD180000 0802D000 // G_SETTIMG G_IM_FMT_RGBA G_IM_SIZ_32b 0001
80212150: F5180000 07000000 // G_SETTILE G_TX_LOADTILE G_IM_FMT_RGBA G_IM_SIZ_32b line 0 PAL 0
80212158: E6000000 00000000 // G_RDPLOADSYNC
80212160: F3000000 073FF080 // G_LOADBLOCK G_TX_LOADTILE ST (0.00,0.00) TEXELS 0400 DXT 0.0625 1/DXT 16
80212168: E7000000 00000000 // G_RDPPIPESYNC
80212170: F5181000 00000000 // G_SETTILE G_TX_RENDERTILE G_IM_FMT_RGBA G_IM_SIZ_32b line 8 PAL 0
80212178: F2000000 0007C07C // G_SETTILESIZE G_TX_RENDERTILE ST (0.00,0.00), (31.00,31.00)
80212180: 07000406 00000602 // G_LINE3D
```

## PrimColor

Seems to write an `FA` command (SetPrimColor) per item slot at: `0x8075077C`.
- Getting alpha from: `*(u16*)(0x803FD850 +0x224)`
