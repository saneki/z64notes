`Obj_Moon_Stone` (Moon's Tear)
==============================

## Spectrum output

### In Observatory

Spectrum output (inside Observatory):

```
40D450:40D9E0 AF 0283:  0000 01 FILE: 0106B490:0106BA20 INIT 8040D950:0106B990
40D9F0:40DB88 AI 0283:  6 01 0 0000 (  154.0   -44.0  -106.0) 0000 8AAA 0000
```

Draw function: `0x8040D850`
- Actor file offset: `0x400`

Main function
- Actor file offset: `0x3C0`

### Using Telescope

Spectrum output (when using telescope into Termina Field):

```
44FDB0:450340 AF 0283:  0000 01 FILE: 0106B490:0106BA20 INIT 804502B0:0106B990
450350:4504E8 AI 0283:  6 00 0 1000 ( 3660.0   254.0  1427.0) 0000 0000 0000
```

### Termina Field

Spectrum output (in Termina Field):

```
44EF30:44F4C0 AF 0283:  0000 01 FILE: 0106B490:0106BA20 INIT 8044F430:0106B990
44F4D0:44F668 AI 0283:  6 00 0 1000 ( 3660.0   254.0  1427.0) 0000 0000 0000
```

Actor overlay entry:

```
0106B490 0106BA20 80C06510 80C06AA0
8044EF30 80C06A10 00000000 00000100
```

ROM offset of `dmadata` entry: `0x1CAA0`
- Relative to start: `0x25A0`
- Table entry index (decimal): `602`

## Draw Function

Note: `0x80400B40` seems to be reserved for Get-Item objects.
- The object data in decompressed ROM is located at `0x0180F600` (PROM offset)
- This corresponds to VROM `0x0194D000`, which is `object_gi_reserve00`.

### opa

Sets up segmented address before calling Get-Item function:

```
DB060018 80400B40
```

Get-Item function writes the following instructions to `poly_opa`:

```
DE000000 801C13A0
DB060024 802297A8
DB060028 80229778
DA380003 80229738
DE000000 06000D78
```

### xlu

Sets up segmented address before calling Get-Item function:

```
DB060030 801C0850
DB060018 80400B40
```

Get-Item function writes the following instructions to `poly_xlu`:

```
DE000000 801C13A0
DB060024 802297A8
DB060028 80229778
DA380003 802296F8
DE000000 06000C80
```

## Investigation

### Object Buffer

Buffer at `0x80400B40`, used for object for current Get-Item, size when using Moon's Tear object:
- Start: `0x80400B40`
- End: `0x804027B0`
- Size: `0x1C70`

### Segment Instructions (`9`, `A`)

Function `0x801309F4` is used to write segment instructions for `0x24` and `0x28`:
- `0x801309F4(z2_game_t *game, u32 offset, void *some_data);`
- Offset is passed to function before it is multiplied by 4.
  - Thus `0x9` for `0x24`, and `0xA` for `0x28`.

For `0x24`: uses `0x80402790`
- Offset into object: `0x1C50`
For `0x28`: uses `0x80402798`
- Offset into object: `0x1C58`

In Moon's Tear Get-Item function, writes these by calling function:
- Calls function: `0x80131758(0x803E6B20, 0x804027A0)`
- Getting second arg value from return value of function call to `0x80100504`.
  - Calls: `0x80100504(0x06001C60)`
  - This is resolving a segment address using the table in RDRAM!
  - It's probably crashing because we aren't setting Segment 6 in that table, just writing it directly to the display list.

### Call Chain

Call chain for `0x801309F4`:
- Return: `0x80131730`
  - Return Function: `0x80131690`
- Return: `0x8013177C`
  - Return Function: `0x80131758`
- Return: `0x800EF6A0`
  - Return Function: `0x800EF65C`
  - This is Get-Item draw function for Moon's Tear.
- Return: `0x800EE354`
  - Return Function: `0x800EE320`
  - This is the function for drawing Get-Item by graphic Id.

### Debugging Function Variable Call

Function: `0x80131690`
- Call at: `0x80131728`

- Gets offset `0x1C60` into object data.
- Derefs `+2` from that offset as a `u16` ...
  - ... which is used into a function pointer array at `0x801C3BD8`.
  - Seems to be an array of `6` functions.
