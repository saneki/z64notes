Freestanding Model Hover + Messages
===================================

Spectrum commands used for testing:
- `sp 41 1` to spawn in Astral Observatory.
- `sp 60` to spawn in Fisherman Hut.

Code which uses actor field `0xC4`:
- Moon's Tear: `0x800B9AB4`
- Seahorse:    `0x800B9AB4`

Actor field `0xC4` gets multiplied by field `0x5C`? (`scale.y`)
- Moon's Tear scale: `0x3E99999A => 0.3`
- Seahorse scale:    `0x3BD4FDF3 => 0.0065`

## Messages

Moon's Tear message: `0x5E3`
Seahorse message:    `0x1074`
