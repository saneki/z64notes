VROM Code File
==============

Call to `z2_LoadFile(z2_loadfile_t *loadfile)` (`0x80080A08`):

`loadfile`: `0x8009B0F0`
- VROM: `0x00B3C000`
- RAM:  `0x800A5AC0`
- Size: `0x0013E4E0`

If accurate, then the file is loaded into: `[0x800A5AC0, 0x801E3FA0)`

The call to `0x80081178` seems to actually write the file to RAM.
- Documented by DB as `load_compressed_file`.

## Old Notes

Maybe mapped to RAM: `0x8018E2B0`

Write breakpoint hit at: `0x80081108`
- Function: `0x80080FF0`
