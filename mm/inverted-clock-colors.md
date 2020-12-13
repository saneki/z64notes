Inverted Clock Colors
=====================

- Structure: `0x801BFBCC`

```c
typedef struct s_hval {
    u16 value;
    u16 unused;
} hval;

struct inverted_clock_color_state {
    // Current main colors
    hval main_red;     /* 0x0000, 0x801BFBCC */
    hval main_grn;     /* 0x0004, 0x801BFBD0 */
    hval main_blu;     /* 0x0008, 0x801BFBD4 */

    // Current tint colors
    hval tint_red;     /* 0x000C, 0x801BFBD8 */
    hval tint_grn;     /* 0x0010, 0x801BFBDC */
    hval tint_blu;     /* 0x0014, 0x801BFBE0 */

    hval trans_timer;  /* 0x0018, 0x801BFBE4 */
    hval direction;    /* 0x001C, 0x801BFBE8: 0 if timer decreasing, 1 if increasing. */
    u16  red1;         /* 0x0020, 0x801BFBEC */
    u16  red2;         /* 0x0022, 0x801BFBEE */
    u16  grn1;         /* 0x0024, 0x801BFBF0 */
    u16  grn2;         /* 0x0026, 0x801BFBF2 */
    u16  blu1;         /* 0x0028, 0x801BFBF4 */
    u16  blu2;         /* 0x002A, 0x801BFBF6 */
    u16  tint_red1;    /* 0x002C, 0x801BFBF8 */
    u16  tint_red2;    /* 0x002E, 0x801BFBFA */
    u16  tint_grn1;    /* 0x0030, 0x801BFBFC */
    u16  tint_grn2;    /* 0x0032, 0x801BFBFE */
    u16  tint_blu1;    /* 0x0034, 0x801BFC00 */
    u16  tint_blu2;    /* 0x0036, 0x801BFC02 */
    u16;               /* 0x0038, 0x801BFC04 */
    u16;               /* 0x003A, 0x801BFC08 */
    u16;               /* 0x003C, 0x801BFC0C */
    u16;               /* 0x003E, 0x801BFC10 */
};
```

Blue issue: Weird "array" values at `0x801BFBD8`:
- Example: `[0x4, 0x4, 0x22]`, might suggest a higher opacity for blue value.

The third value (at `*(u16*)0x801BFBE0`) is written to at: `0x8011A0D0`.
- Writes from A2, which can be set from multiple places.
- Most likely at around `0x80119FA0`:

Note: Only happens during the following branch path:
- Obtains values at `0x80119F18` (beginning of blue logic?)
- `0x80119F38` (takes branch, `if (A2 < A0)`)

```c
if (A2 < A0) {
    // Add division result
    // See: 0x80119F40
    u32 T9 = V1 / A1;
    s16 A2 = (s16)(A2 + (s16)T9);
} else {
    // Subtract division result
    // See: 0x80119F88
    u32 T7 = V1 / A1;
    s16 A2 = (s16)(A2 - (s16)T7);
}
```

These code paths only differ in whether or not the division result is added or subtracted from `A2`.
