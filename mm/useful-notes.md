## Spawn at Entrance

Write bytes:
- `*(u8*)(0x803E6B20 +0x18875) = 0x14`
- `*(s16*)(0x803E6B20 +0x1887A) = index;`

Or:
- `*(u8*)(0x803FF395) = 0x14`
- `*(s16*)(0x803FF39A) = index;`

...

Zone spawn: `0x801EF670 +0x3CB4`
- Absolute: `0x801F3324`
- Offset `0x12` = Room
- Offset `0x18` = Scene

Function `0x80169DCC(z2_game_t *game, u32 spawn_index, u32 scene, u32 room)`:
- Seems to be used to write data to spawn struct in `z2_file`.
