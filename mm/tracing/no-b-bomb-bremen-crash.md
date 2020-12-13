No B-Button Bomb Mask & Bremen Mask Crash
=========================================

Tracing: `0x8074D29C`
- D2C0: No
- D2D0: No
- D2E0: No
- D2F0: No
- D300: No
- D30C: No
- D320: Branch -> 0xD3BC
- D3C4: Branch -> 0xD3F0
- D3F8: No
- D408: Branch -> 0xD564
- D570: Branch -> 0xD598
- D5B8: Branch -> 0xD638
- D63C: Branch -> 0xD69C
- D69C: Branch -> 0xD6B4
- D6B8: Branch -> 0xD6D4
- D6FC: Branch -> 0xD738

### Vanilla Trace with *No B button* & Using Ocarina w/ Bremen Mask

I just realized the first three checks of this function are checking the action state flags.
- Located at: `0x803FFDB0 +0xA6C, +0xA70, +0xA74`

Then it does some checks which are likely related to non-transformation masks.
- Specifically, byte at `0x803FFDB0 +0x153` is some mask Id?
  - `0x803FFF03`
- Actually, other values around this seem to correspond to mask qualities.

- `0xD2C0`: No branch
- `0xD2D0`: No branch
- `0xD2E0`: No branch
  - Calls: `0x801240DC`
- `0xD2F0`: No branch
- `0xD300`: No branch
- `0xD30C`: No branch
  - Calls: `0x8074D19C`
- `0xD320`: Branch -> `0xD3BC`
- `0xD3C4`: Branch -> `0xD3F0`
  - Store byte: `V1` (`0x01`) in `0x803FFDB0 +0x154`
  - In this case, `V1` is the result of call to `0x8074D19C`
  - Setting this value only happens when a non-transformation mask is equipped???
- `0xD3F8`: No branch
- `0xD408`: Branch -> `0xD564`
  - Calls: `0x8074D254`
- `0xD570`: Branch -> `0xD598`
  - Calls: `0x8012364C`
- `0xD5B8`: Branch -> `0xD638`
- `0xD63C`: Branch -> `0xD69C`
- `0xD69C`: Branch -> `0xD6B4`
- `0xD6B8`: Branch -> `0xD6D4`
  - Calls: `0x8074C9B4`
  - Calls: `0x80124110`
- `0xD6FC`: Branch -> `0xD738`
  - Store byte: `0x02` in `0x803FFDB0 +0x146` (remember this from before!?)
  - Calls: `0x8074EE20` (`UseItem` function)

Function: `0x8074D19C`
- `func_0x8074D19C(z64_link_t *link, uint8_t arg1);`
- For `A1`: `(*(uint8_t *)(0x803FFDB0 +0x153) + 0x39)`
  - Takes the byte value (some mask Id?) and adds a constant `0x39`.

Function: `0x8074D154`
- `func_0x8074D154(z64_link_t *link, uint8_t item, uint8_t arg2);`

When calling during a crash setup, this jump at `0xD408` doesn't happen!
- Checks: `*(uint8_t *)(0x803FFDB0 +0x014A) < 2`
- Yep, `z64_UseItem` sets this value, and somehow a crash happens down the line!
- This value seems to be tied to the item Link currently has out (for example, `0x14` for Ocarina).

#### Now *with B button* & Using Ocarina w/ Bremen Mask

Same?

#### Now *with B button* & Using Ocarina w/ *no mask*

- `0xD2C0`: No branch
- `0xD2D0`: No branch
- `0xD2E0`: No branch
- `0xD2F0`: No branch
- `0xD300`: No branch
- `0xD30C`: Branch -> `0xD3F4`
- `0xD3F8`: No branch
- `0xD408`: Branch -> `0xD564`
- `0xD570`: Branch -> `0xD598`
- `0xD5B8`: Branch -> `0xD638`
- `0xD63C`: Branch -> `0xD69C`
- `0xD69C`: Branch -> `0xD6B4`
- `0xD6B8`: Branch -> `0xD6D4`
- `0xD6FC`: Branch -> `0xD738`

### Older trace

With mask on (non-buggy):
- `0xD2C0`: No branch
- `0xD2D0`: No branch
- `0xD2E0`: No branch
- `0xD2F0`: No branch
- `0xD300`: No branch
- `0xD30C`: No branch
- `0xD320`: Branch -> `0xD3BC`
- `0xD3C4`: Branch -> `0xD3F0`
- `0xD3F8`: No branch
- `0xD408`: No branch
- `0xD41C`: No branch
- `0xD428`: No branch
- `0xD438`: Branch -> `0xD448`
- `0xD464`: Branch -> `0xD564`
- `0xD570`: Branch -> `0xD598`
- Hits `0xD5A4`

## Idea Code

```c
#define z64_Func8074D19C_addr 0x8074D19C
typedef uint8_t (*z64_Func8074D19C_proc)(z64_link_t *link, uint8_t mask);
#define z64_Func8074D19C ((z64_Func8074D19C_proc) z64_Func8074D19C_addr)

// Backup
uint8_t c_left = z64_file.c_buttons[0];

z64_file.c_buttons[0] = item;
if (z64_link.mask != 0) {
    uint8_t result = z64_Func8074D19C(&z64_link, z64_link.mask + 0x39);
    if (z64_link.mask != 0x14) {
        z64_link.mask_c = result;
    } else {
        // ...?
    }
}

z64_link.pre_use = 1; // C-left?
z64_UseItem(&z64_ctxt, &z64_link, item);

// Restore
z64_file.c_buttons[0] = c_left;
```
