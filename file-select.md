File Select Menu
================

## Constructor / Destructor

File:
- RDRAM: `0x8076F160`
- VROM:  `0x00C7E4F0`
- VRAM:  `0x80804010`
- PROM:  `0x00BCE010`
  - PROM is specific to my ROM.

Constructor:
- Offset: `0xFC88`
- RDRAM:  `0x8077EDE8‬`
- VRAM:   `0x80813C98‬`
- VROM:   `0x00C8E178`

Destructor:
- Offset: `0xFC64`
- RDRAM:  `0x8077EDC4`
- VRAM:   `0x80813C74‬`
- VROM:   `0x00C8E154‬`

## Fade Out

At end of File Select drawing function, display list ends with:
- `0xFA000000 0x00000000`
  - Writing fade out color?
- `0xDE000000 0x0E0002E0`
  - Definitely not a RDRAM address, maybe special value according to the ucode?
  - Is also a constant in the code.

Writes display list instruction (color): `0x8077EA24`
- Function: `0x8077E3B8`
  - Seems to be the root draw function for file select.
- Gets alpha byte from: `*(u16*)(0x80406B20 +0x450A) & 0xFF`
  - Address: `0x8040B02A`
