Stray Fairy Draw
================

PolyOpa pointer at during draw function: `0x80210990` -> `0x802109A0`
- Right before that, writes segment 6: `0xDB060018 0x8058C3D0`
- That data is from Object 1

## Investigating Function `0x80134DBC`

### Fourth Arg (`A3`)

Pseudo-code from disassembly:

```c
// Calculate amount of bytes needed for matrix data.
// Multiplies by 0x40 as each vertex is 0x10 bytes: (x, y, z, w).
// Then rounds up to multiple of 0x10 (this is unnecessary but they do it anyways).
unsigned int A3 = 9;
unsigned int T9 = (A3 * 0x40);
// Round value up to a multiple of 0x10
unsigned int T1 = (T9 + 0xF) & 0xFFFFFFF0;

// Allocate space in stack for matrix data
void *T8 = game->common.gfx->poly_opa.d;
*(game->common.gfx->poly_opa.d) = T8 - T1;
```

Thus, the parameter for `A3` is the count of matrix structures to push onto the `poly_opa` stack.

## Stray Fairy Glow Effect

Spectrum output:

```
410810:412070 AF 01B0:  0000 01 FILE: 00F31E90:00F336F0 INIT 80411DB0:00F33430
412080:4122B0 AI 01B0:  7 00 0 FE03 (-2085.6  -111.0   411.4) 0000 0000 0000
```

Writes to `poly_xlu` DList:
- Writes `SetEnvColor` at instructions: `0x8040A674`, `0x8040A6DC`
