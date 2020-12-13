Temp Notes
==========

### C Buttons / Deku Nut Usage

```c
// Something: 0x80760240
// See: 0x80751E14
// c_button_slot = *(0x803FD850 + 0x272);

// See: 0x80115AD8, breaks before item use?
// ~~Function: 0x80115908~~
// - Seems to branch to 0x80115AA8 from somewhere? (0x80115A30)
// - Real function begin might be 0x80115A14
//  - `A0` = `0x9` (deku nut Id)
//  - `A1` = `0xFFFFFFFF` (-1)
//  - Might be a "use_deku_nut" or "subtract_deku_nut" function
// Return: 0x8077006C
// deku_nut_ammo = *(deku_nut_ammo) - 1;
```

### File Notes

```c
// 0x0F41 : 0x00 before Clock Town scrub summoned, 0x04 afterwards
// 0x8AB6 Bank init flag?

// Get stray fairy in laundry pool:
// 0xCDB: 0x00 => 0x06
// 0xF00: 0x00 => 0x80
// 0xF13: 0x0000 => 0xC007

// After first great fairy encounter:
// 0x0038: 0x00 => 0x01
// 0x0040: 0x00 => 0x01
// 0x0058: 0xFD => 0x09 ("Shoot" on B button for Deku? If 0 no longer says shoot)
// 0x0526: 0x00 => 0x04
// 0x0537: 0x00 => 0x01
// ...
// 0x3F27: 0x00 => 0x00
// 0x3F2E: 0x0000 => 0x0030

// Value of 0x3F2E seems to be the pixel length of the outer bar, only used for visual.

// Finding all bombers (some of these may be day/time based):
// 0x0013: 0x00 => 0x01
// 0x0F03: 0x00 => 0x1F (probably 5-bit flag for each)
// 0x0F2F: 0x00 => 0x02
// 0x0F41: 0x14 => 0x24
// 0x0FE6: 0x05 0x05 0x02 0x03 0x04 0x01 (34251 is the code)
```
