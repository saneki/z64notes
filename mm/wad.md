Zelda 64 WADs
=============

D-Pad Support
-------------

### Ocarina of Time

`gzinject` uses the following `.gzi` patch file for OoT Randomizer:

```
# oot randomizer
0000 00000000 00000001
# use 8MB memory
0304 00002EB0 60000000
# allocate 32MB for rom
0304 0005BF44 3C807200
# Apply Dpad remappings
0302 0016BAF4 00000400
0302 0016BAF8 00000200
0302 0016BAFC 00000100
```

This selects the `00000001.app` content file for modification. For OoT, this file is not compressed.

Each of the values it overwrites are `0x00000020`, probably a button flag indicating the L-button.

It specifically ignores the D-Pad up button to preserve usage of the L-button for map toggle.

### Majora's Mask

In Majora's Mask, the `00000001.app` file *is* compressed (with LZ77).

The following snippet is an example of re-packing a WAD using a patch file, then re-extracting it
to get the decompressed app file.

```sh
gzinject -a pack -w Patched.wad -p decomp.gzi
gzinject -a extract -w Patched.wad
```

... where `decomp.gzi` consists of a patch file to decompress the app file:

```
# Select content1.app
0000 00000000 00000001
# Decompress selected
0100 00000000 00000000
```

Knowing how OoT does its patching, in the app file for MM there are two addresses which may
correlate to the button codes (which are right next to each other):

- `0x00148512` (from testing, this is likely it)
- `0x0014856A`

When unmodified, each of these addresses point to four `0x00000020` values.

Possible `.gzi` patch for Majora's Mask:

```
# Majora's Mask (U)
# Select content1.app
0000 00000000 00000001
# Decompress selected
0100 00000000 00000000
# Write D-Pad remappings
0304 00148512 00000800
0304 00148516 00000400
0304 0014851A 00000200
0304 0014851E 00000100
# Recompress selected
0200 00000000 00000000
```
