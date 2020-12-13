Permanent Owl Save
==================

## Owl Statue

Relevant Spectrum output for Owl Statue actor (post-SoT):

```
4346D0:434ED0 AF 0223:  0000 01 FILE: 00FF7C80:00FF8480 INIT 80434DC0:00FF8370
434EE0:435090 AI 0223:  7 00 0 0004 ( -540.0   100.0 -1099.0) 0000 C000 0000
```

- Actor instance size: `0x1B0`
- Actor main function: `0x8043499C`
- Actor draw function: `0x80434B00`

When starting Owl dialogue, main function sets byte at `0x1A8` to `1`.
- When ending dialogue, sets to `0`.

Calls `0x800B84D0(z2_actor_t *actor, z2_game_t *game)`, if returns non-0 sets byte to `1` for dialogue.

Calls function `0x800B867C` to check if dialogue is ending?

Function `0x800B84D0`:
- Check `(actor->flags & 0x0100) != 0`, if so unset flag and initiate dialogue.

Checks for yes/no answer at `*(u8*)(game +0x16929)`, a byte in the messsage box context (offset `0x12021`).
