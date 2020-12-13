`Dm_Hina` (Boss Remains)
========================

Spectrum output:

```
427840:428280 AF 0140:  0000 01 FILE: 00E88F80:00E899C0 INIT 804281E0:00E89920
428290:428414 AI 0140:  7 00 0 0000 (  350.0     0.0   350.0) 0000 0000 0000
```

Actor overlay entry:

```
00E88F80 00E899C0 80A1F410 80A1FE50
80427840 80A1FDB0 00000000 00000100
```

ROM offset of `dmadata` entry: `0x1B6C0`
- Relative to start: `0x11C0`
- Table entry index (decimal): `284`

Object `0x1CC`:
- Start: `0x01A2F000`
- End:   `0x01A3BB90`
- Size:  `0xCB90`

## Draw Function

Draw function: `0x80428080`
- Actor file offset: `0x840`
- VRAM: `0x80A1FC50`

Function calls:
- `0x804280D0` - Calls `0x8018029C`
  - If you `NOP` this call, nothing draws at all.
- `0x8042810C` - Calls `0x8018103C`
  - If you `NOP` this call, the item does not rotate and faces specific direction.
- `0x80428140` - Calls `0x8018039C`
  - If you `NOP` this call, the item appears bigger (scales the matrix values?).
- `0x804281C0` - Calls `0x80427DDC`
  - This is a function from the actor file.
  - Nothing noticeable happens if `NOP`-ed.

### Sample DList Instructions

Sample of DList instructions written by function (to `poly_opa`):

```
DB060018 8069DA80 // gsSPSegment(6, 0x8069DA80);
DE000000 801C13A0 // gsSPDisplayList(0x801C13A0);
DA380003 802487A8 // gsSPMatrix(0x802487A8, G_MTX_LOAD);
DE000000 06000690 // gsSPDisplayList(SEGADDR(6, 0x690));
E7000000 00000000 // gsDPPipeSync();
F8000000 120F1400 // gsDPSetFogColor(0x12, 0x0F, 0x14, 0x00);
DB080000 1900E800 // gsMoveWd(G_MW_FOG, G_MWO_FOG, 0x1900E800);
```

Notes:
- `0x8069DA80` points to object `0x1CC` as expected.
- Calls separate DList in this object at offset `0x690`.
- All of these instructions are written by the call to `0x800EE320` which does the Get-Item draw.

The Get-Item called for Odolwa Remains: `0x800EFD44`
- Near the end, calls function `0x801660B8`, which calls `0x8012BD8C`.
- The function `0x8012BD8C` is what writes the fog color stuff.

### Heart Piece Comparison

Heart Piece Get-Item draw function: `0x800EF2AC`
- Get-Item draw table entry: `0x801BB41C`

Sample of DList instructions written by function (to `poly_xlu`):
- Writes instructions to `poly_xlu`, but uses matrix stack of `poly_opa`.

```
DE000000 801C13A0
DA380003 80249A08
DE000000 06001290
DE000000 06001590
```

A notable difference is that the Boss Remains GI draw function is setting up the segmented address,
as opposed to assuming it was set up by the caller.
- When `NOP`-ing out the instructions which set up the segmented address, it no longer crashes and
  displays correctly!

### Retrieving the Object Address

How is the function retrieving the object address to write it as a segmented address?

- Calls function: `0x8012F608((game +0x17D88), 0x1CC)`
  - Prototype: `u8 (z2_obj_ctxt_t *ctxt, ushort object_id)`
  - Return value is cast to a `u8`, so likely returns such.
  - Returns an index into the object table in the object context struct.
- Multiplies result by `0x44` and adds to `game +0x17D98`.
- Dereferences to get object data pointer.

```c
u8 result = 0x8012F708((game +0x17D88), 0x1CC);
u32 object_addr = *(u32*)(game +0x17D98 + (result * 0x44));
```
