Message Table
=============

VROM:   `0xC5D0D8`
PROM:   `0xBACBF8` (decompressed)
Offset: `0x1210D8`
RDRAM:  `0x801C6B98`, `0x801CFB00`

Function: `0x801588D0`
- Gets message table pointer from `*(u8**)(game +0x1698C)`.
  - Offset `0x12084` in `MessageContext`.

Reads message data using ReadFile function `0x80080C90`.
- Uses hardcoded VROM address `0x00AD1000` for VROM file start, see: `0x801516C4`.

Two separate message data files:
- `0x00AD1000` - Primary game message data.
- `0x00B3B000` - Credits message data.

Check at `0x80150F68` if message Id is less-than `0x4E20`:
- If so, use primary file `0x00AD1000`.
- Otherwise, use credits file `0x00B3B000`.

`*(u8*)(game +0x16F20) == 0`
