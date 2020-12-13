Jinx
====

## Wrong Guesses

Possible byte: `0x803FFECD`

Write breakpoint:
- Write to `0`: `0x800BA534`
- Write to value: `0x800B9D04`
  - Only does this if `*(uint32_t *)(0x803FFDB0 +0xC8) != 0`
