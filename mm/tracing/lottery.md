Lottery
=======

## Current Guess

Writes current guess to: `*(uint32_t *)(0x801EF670 +0xEF0)`
- Address: `0x801F0560`
- Format: `0x00000DDD`, where `D` are 4-bit digits.
  - 1 is `0x1`, 2 is `0x2`, and so on.

Writes at:
- `0x8012F2C4`
  - Seems to be copying from global context/game struct:
    - `*(uint16_t *)(0x803E6B20 +0x695C)`
    - `*(uint16_t *)(0x803E6B20 +0x695E)`
    - `*(uint16_t *)(0x803E6B20 +0x6960)`
    - Address: `0x803ED47C`
    - Probably getting inputs from "Enter your number" dialogue box?
