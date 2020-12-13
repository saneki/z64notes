Matrix Stack
============

## Possibly Relevant Info

- https://wiki.cloudmodding.com/oot/Rendering

This page describes a matrix stack being located by using the display buffer struct's final field ("append end address").

## OoT and `GetMatrixStackTop`

Address from OoTR:

```c
#define z64_GetMatrixStackTop_addr 0x800AA78C
```

This function simply returns: `*(void**)0x80121204`
- Example value at that address is: `0x802105E0`

OoT pointers:
- Context: `0x801C84A0`
- Gfx:     `0x8011F290`
- Overlay: `0x8011F538`
- PolyOpa: `0x8011F548`
- PolyXlu: `0x8011F558`

Call chain:
- `0x800AA78C` (`z64_GetMatrixStackTop`)
  - Return: `0x800AA7B4`
  - In Link's tree house, this gets called twice per frame.
- `0x800AA79C`
  - NOTE: Following notes were an actor on the heap but I didn't realize.
    - Return: `0x801E50C8`
    - A little further after returning, reads and updates field at `z2_gfx_t +0x2D0`.
      - See: `0x801E510C`
      - This field is: `z64_gfx.poly_xlu.p`
      - It writes an instruction starting with: `0xDA380003`.
  - Return: `0x8009C38C`
    - Function: `0x8009C0A8`
    - This function writes a bunch of display list `0xDB060000` instructions.
  - Return: `0x8009C398`
  - In this function, calls `0x800ABA10`, which seems to be a `MtxF` copy function?
  - Possible match in MM at VROM: `0xB3C000 +0xDC21C‬`, or: `0xC1821C‬`
    - In RAM: `0x800A5AC0 +0xDC21C`, or `0x80181CDC`
    - Seems like it! When checking which functions call it, a specific address is seen often: `0x801FBE04`
- `0x801E4D20`

## Majora's Mask

Pointers:
- Context: `0x803E6B20`
- Gfx:     `0x801F9CB8`
- Overlay: `0x801F9F50‬`
- PolyOpa: `0x801F9F60‬`
- PolyXlu: `0x801F9F70‬`

### Actor Context

The `z2_actor_ctxt_t` has a `MtxF` in it, might be used for this?
- Offset: `0x120`
- Address: `0x803E6B20 + 0x1CA0 + 0x120`
  - `0x803E88E0`
