Chest
=====

Initialization uses actor variable to set certain fields:
- Sets chest type (4 leading bits) to byte at field `0x1F1`.
- Sets chest item thing to `u32` at field `0x21C`.
  - If this is `0x76`, is ice trap.

`0x8012F1BC`: `IncrementSkullTokenCount(u32 type)`

`0x80112E80`: `GiveItem(z2_game_t *game, u8 item)`
- If `item >= 0x8B`: `result = (u16*)(0x801BF8B4)[item]`, `T3 = (u8*)(0x801C2078)[result]`

When getting Skulltula Token, uses get-item entry stored at 0x800B35F0 to determine which.

Ice Trap calls "Damage" function to freeze:
- RDRAM: `0x807702AC`
- `*(s16*)(link +0x384) == 0x52 || == 0x76`
  - Absolute: `0x80400134`
  - Ice trap sets this value to `0x76`.
  - While near chest, this value will be `0xFF8A` (`0 - 0x76`).
- `0x8043BFA0` calls function `0x800B8B84` to set this field in Link actor.
  - This is also using value from chest actor at `0x21C`, so we need to control this field.

Relevant Spectrum output:

```
43AB90:43CD50 AF 0006:  0000 01 FILE: 00CE1FB0:00CE4170 INIT 8043CAF0:00CE3F10
43CD60:43CF84 AI 0006:  B 00 0 0E8A (  479.0   220.0   495.0) 0000 C000 0000
```

Patched function: Offset `0x10F8`
