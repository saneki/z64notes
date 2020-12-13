Boat Cruise Speedup
===================

Flags:
- Woodfall clear: `0x801F057C`
- Koume saved:    `*(u8*)0x801F0574 == 8`
- Has done archery once: `*(u8*)(0x801EF670 + 0x1010) & 1 == 1`

## Koume

Relevant Spectrum output:

```
423360:424AA0 AF 0214:  0000 01 FILE: 00FDB1B0:00FDC8F0 INIT 80424820:00FDC670
424AB0:424E58 AI 0214:  4 FF 0 080F ( -284.9    72.6   195.2) 020D 9D3C E890
```

Gets main function pointer from actor offset `0x144`.

Checks minigame counter 2 (`0x801F35AC`) which is # of times Koume has been hit.
- See:       `0x80423CC8`
- Function:  `0x80423CB0`
- Called at: `0x80423DC0`
- Caller:    `0x80423D94`
- Afterwards, checks `*(u8*)(file +0x1010) & 1 != 0`, unsure what this is.

## Archery Boat

Relevant Spectrum output:

```
42C320:42D1F0 AF 00A7:  0000 01 FILE: 00DC6850:00DC7720 INIT 8042D130:00DC7660
42D200:42D390 AI 00A7:  1 FF 0 0001 ( -461.7   -15.0   446.0) 0000 9055 0000
```

- VRAM: `0x80953A90`
- VROM: `0x00DC6850`
- File entry offset: `0x1AE90`
- File index: `153`

- Actor main: `0x8042D074`
- Actor draw: `0x8042D098`

Gets main function pointer from actor offset `0x15C`.
- During archery: `0x8042C82C`
- Ending archery 1: `0x8042CB30`
  - Written at: `0x8042C97C`
- Ending archery 2: `0x8042C81C`
  - Written at: `0x8042CBAC`

Function to move boat (advance along path): `0x8042C47C`

NOP-ing out branch will end the game early, as well as stop the boat while fading out.
- Checks: `*(u16*)(actor +0x160) & 2 != 0`

## Boat Speed

During normal tour, updates positions at: `0x8042DD28`
- Gets positions from: `(f32*)(actor +0x170)`

The values at `+0x170` copy from: `0x801D15B0`
- This actually seems to be setting the values to 0.
- The real values are set by the function: `0x8013B350`

The function call to `0x8013AF00` is likely updating these values, used to advance the boat along a path.

Relevant Spectrum output:

```
42DB00:42E9D0 AF 00A7:  0000 01 FILE: 00DC6850:00DC7720 INIT 8042E910:00DC7660
42E9E0:42EB70 AI 00A7:  1 FF 0 0001 (  811.5   -15.0   307.4) 0000 35CB 0000
```

### Function 0x8013B350

- Function: `0x8013B350`
  - Return Address: `0x8013B790`
- Function: `0x8013B6B0`
  - Return Address: `0x8042DDA4`
- Function: `0x8042DC5C`

### Field 0x160

Bitflag:
- `0000 0001` = Active?
- `0000 0010` = Path complete.
- `0000 1000` = Resting state?
- `0001 0000` = Latter half of cruise (not embarking at palace).

### Field 0x164

Points into scene data: `0x806BFF1C`
- Scene: `0x806BF840`
- Offset: `0x6DC`

Relevant scene header: `0D000000 020006D4`
- `0x0D` is Pathways!

Path entry pointed to: `2A07FFFF 02000444`
- `0x2A`: number of points
- `0x02000444`: location of first point
