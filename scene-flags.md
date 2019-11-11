Scene Flags
===========

```c
// 0x800B5BF4
void set_generic_flag(z64_game_t *game, signed char flag);
// 0x800B5C90
void set_chest_flag(z64_game_t *game, uint8_t flag);
// 0x800B5D30
void set_temp_clear_flag(z64_game_t *game, uint8_t flag);
// 0x80169D40
void store_scene_flags(z64_game_t *game);

///
/// Termina Field
///

// When approaching Tatl tree cutscene near entrance to Southern Swamp
set_generic_flag(0x803E6B20, 4);
// Chests
set_chest_flag(0x803E6B20, 0); // Underwater chest
set_chest_flag(0x803E6B20, 2); // Chest on tree stump
```
