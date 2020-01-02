Item Textures VROM
==================

Loads item textures from archive file at VROM address `0xA36C10`.

## Differing Formats

After `0x61`, the file format of the image data changes.

For example, loading index `0x64` from VROM file `0xA36C10`:
- Buffer Start: `0x805EEE50`
- Buffer End:   `0x805EF750`
- Length:       `0x900`

Assuming length of `0x900` is RGBA8 (32-bits per pixel): `(0x900 / 4) = 576 pixels`
- `576 == 24^2`, so likely a 24x24 texture.
