Fairy
=====

Read breakpoint on current health when fairy picked up (from 2 to 3 hearts, so max `0x30`):
- `0x80115974`
  - Sets to `0xA0`, a weird value when max is `0x30`?
- `0x80115990`
  - Sets to `0x30`, what we want in this case.

Function: `0x80115908`
- Args:
  - `A0`: `0x803E6B20` (`z64_game_t *`)
  - `A1`: `0x80` (???)
- Return (1), from inside Zora Cape:
  - Return: `0x80407D38`
  - Return Function: `0x80407B84`
    - Part of scene-related data/heap?
- Return (2), warped in from South Clock Town:
  - Return: `0x8040CCE8`
    - The return addresses are different! Probably inside Fairy actor allocation.

### Fairy Actor Spawn (Zora Cape)

Function: `0x800BAC60` (documented by DB as `actor_spawn`):
- Args when fairy spawned after breaking pot:
  - `A0`: `0x803E87C0` (???, very close to "loaded actor list", `0x803E6B20 +0x1CA0`)
  - `A1`: `0x803E6B20` (`z64_game_t *`)
  - `A2`: `0x10`       (???)
  - `A3`: `0xC5A88000` (or `-5392.0`, loaded into `F12`)
    - Tweaking this value made the fairy spawn in the wall?
  - Stack:
    - `f32 0x0050 (SP)`: `0x42580000` (or `54.0`, loaded into `F4`)
      - Z position of fairy! However, fairy very quickly "glides" to Link's Z position.
      - This happens when you jump in the water as well.
    - `f32 0x0054 (SP)`: `0x44F3E000` (or `1951.0`, loaded into `F6`)
      - Tweaking this value changed the direction the fairy went after spawning?
    - `u16 0x005A (SP)`: `0x0000`     (loaded into `T6`)
    - `u16 0x005E (SP)`: `0x0000`     (loaded into `T7`)
    - `u16 0x0062 (SP)`: `0x0000`     (loaded into `T8`)
    - `u32 0x0064 (SP)`: `0x00004902` (loaded into `T9`)
- Calls other `actor_spawn` function documented by DB: `0x800BAE14`.

### Spawning a Fairy

Spawning a fairy once works as intended, returning the pointer to the Actor memory struct.

When attempting to spawn a fairy twice, it returns the same pointer but does not actually "spawn" it.
- Thus, this only "spawns" an actor if not already in memory?
- Maybe we will need to use the initial one and reset its state.

#### Actor Struct Comparison

Fairy `Actor` struct before being "used":

```
00000000  00 10 07 00 02 00 00 30 C5 A8 80 00 42 58 00 00  .......0Å¨€.BX..
00000010  44 F3 E0 00 00 00 00 00 00 00 00 00 00 02 00 03  Dóà.............
00000020  03 FF 00 00 C5 A8 80 00 42 58 00 00 44 F3 E0 00  .ÿ..Å¨€.BX..Dóà.
00000030  00 00 00 00 00 00 00 00 FF 00 00 00 C5 A8 80 00  ........ÿ...Å¨€.
00000040  42 58 00 00 44 F3 E0 00 00 00 00 00 00 00 00 00  BX..Dóà.........
00000050  00 00 00 00 00 00 00 00 3C 03 12 6F 3C 03 12 6F  ........<..o<..o
00000060  3C 03 12 6F 00 00 00 00 00 00 00 00 00 00 00 00  <..o............
00000070  00 00 00 00 00 00 00 00 C1 A0 00 00 00 00 00 00  ........Á ......
00000080  00 00 00 00 00 32 00 00 00 00 00 00 00 00 00 00  .....2..........
00000090  00 00 00 00 7F 7F FF FF 00 00 00 00 00 00 00 00  ......ÿÿ........
000000A0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
000000B0  00 0A 00 0A 00 00 FF 08 00 00 00 00 00 00 00 00  ......ÿ.........
000000C0  00 00 00 00 00 00 00 00 00 00 00 00 41 70 00 00  ............Ap..
000000D0  FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ÿ...............
000000E0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
000000F0  00 00 00 00 00 00 00 00 00 00 00 00 44 7A 00 00  ............Dz..
00000100  43 AF 00 00 44 2F 00 00 C5 A8 80 00 42 58 00 00  C¯..D/..Å¨€.BX..
00000110  44 F3 E0 00 00 00 00 00 00 00 00 00 00 00 00 FF  Dóà............ÿ
00000120  00 00 00 00 00 00 00 00 80 45 42 10 00 00 00 00  ........€EB.....
00000130  00 00 00 00 80 40 71 EC 80 40 A2 88 80 40 A4 08  ....€@qì€@¢ˆ€@¤.
00000140  80 1A F1 D0                                      €.ñÐ
```

Fairy `Actor` struct after being "used":

```
00000000  00 10 07 00 02 00 00 70 C5 A8 80 00 42 58 00 00  .......pÅ¨€.BX..
00000010  44 F3 E0 00 00 00 00 00 00 00 00 00 00 02 00 03  Dóà.............
00000020  03 FF 00 00 C5 AA 1A 71 40 C6 66 36 44 F9 93 9A  .ÿ..Åª.q@Æf6Dù“š
00000030  00 00 68 91 00 00 00 00 FF 00 00 00 C5 A8 80 00  ..h‘....ÿ...Å¨€.
00000040  42 58 00 00 44 F3 E0 00 00 00 00 00 00 00 00 00  BX..Dóà.........
00000050  00 00 00 00 00 00 00 00 38 A7 C0 77 38 A7 C0 77  ........8§Àw8§Àw
00000060  38 A7 C0 77 C0 4A 59 9A BF 4C CC CD C0 3C 78 00  8§ÀwÀJYš¿LÌÍÀ<x.
00000070  3F A9 4F 8F 00 00 00 00 C1 A0 00 00 00 00 00 00  ?©O.....Á ......
00000080  00 00 00 00 00 32 00 00 00 00 00 00 00 00 00 00  .....2..........
00000090  00 00 69 6A 43 DA 8A BB 41 9E B3 0D 40 D3 33 64  ..ijCÚŠ»Až³.@Ó3d
000000A0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
000000B0  00 0A 00 0A 00 00 FF 08 00 00 00 00 00 00 B3 C5  ......ÿ.......³Å
000000C0  00 00 00 00 00 00 00 00 00 00 00 00 41 70 00 00  ............Ap..
000000D0  FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ÿ...............
000000E0  00 00 00 00 00 00 00 00 00 00 00 00 41 63 8C 00  ............AcŒ.
000000F0  C1 1D 9A 00 43 2C 8B 30 43 40 42 98 44 7A 00 00  Á.š.C,‹0C@B˜Dz..
00000100  43 AF 00 00 44 2F 00 00 C5 A9 F4 80 40 EC CC 9C  C¯..D/..Å©ô€@ìÌœ
00000110  44 FA 20 F4 00 00 00 00 00 00 00 00 00 00 00 FF  Dú ô...........ÿ
00000120  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000130  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000140  80 1A F1 D0                                      €.ñÐ
```

When attempting to spawn a second fairy in the same scene, the struct gets somewhat reset:

```
00000000  00 10 07 00 02 00 00 30 C3 41 C1 0C 00 00 00 00  .......0ÃAÁ.....
00000010  43 8E E6 08 00 00 00 00 00 00 00 00 00 02 00 03  CŽæ.............
00000020  03 FF 00 00 C3 41 C1 0C 00 00 00 00 43 8E E6 08  .ÿ..ÃAÁ.....CŽæ.
00000030  00 00 00 00 00 00 00 00 FF 00 00 00 C3 41 C1 0C  ........ÿ...ÃAÁ.
00000040  00 00 00 00 43 8E E6 08 00 00 00 00 00 00 00 00  ....CŽæ.........
00000050  00 00 00 00 00 00 00 00 3C 03 12 6F 3C 03 12 6F  ........<..o<..o
00000060  3C 03 12 6F 00 00 00 00 00 00 00 00 00 00 00 00  <..o............
00000070  00 00 00 00 00 00 00 00 C1 A0 00 00 00 00 00 00  ........Á ......
00000080  00 00 00 00 00 32 00 00 00 00 00 00 00 00 00 00  .....2..........
00000090  00 00 00 00 7F 7F FF FF 00 00 00 00 00 00 00 00  ......ÿÿ........
000000A0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
000000B0  00 0A 00 0A 00 00 FF 08 00 00 00 00 00 00 00 00  ......ÿ.........
000000C0  00 00 00 00 00 00 00 00 00 00 00 00 41 70 00 00  ............Ap..
000000D0  FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ÿ...............
000000E0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
000000F0  00 00 00 00 00 00 00 00 00 00 00 00 44 7A 00 00  ............Dz..
00000100  43 AF 00 00 44 2F 00 00 C3 41 C1 0C 00 00 00 00  C¯..D/..ÃAÁ.....
00000110  43 8E E6 08 00 00 00 00 00 00 00 00 00 00 00 FF  CŽæ............ÿ
00000120  00 00 00 00 00 00 00 00 80 44 29 10 00 00 00 00  ........€D).....
00000130  00 00 00 00 80 40 71 EC 00 00 00 00 00 00 00 00  ....€@qì........
00000140  80 1A F1 D0                                      €.ñÐ
```

Attempting to spawn a second fairy, one frame after the first (after second call to `SpawnActor`):
- Looking at this, some function pointers get immediately removed, can check if they are gone.

```
Offset(h) 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

00000000  00 10 07 00 02 00 00 30 44 56 36 C4 42 C8 00 00  .......0DV6ÄBÈ..
00000010  43 0F 68 98 00 00 00 00 00 00 00 00 00 02 00 03  C.h˜............
00000020  03 FF 00 00 44 56 36 C4 42 C8 00 00 43 0F 68 98  .ÿ..DV6ÄBÈ..C.h˜
00000030  00 00 00 00 00 00 00 00 FF 00 00 00 44 56 36 C4  ........ÿ...DV6Ä
00000040  42 C8 00 00 43 0F 68 98 00 00 00 00 00 00 00 00  BÈ..C.h˜........
00000050  00 00 00 00 00 00 00 00 3C 03 12 6F 3C 03 12 6F  ........<..o<..o
00000060  3C 03 12 6F 00 00 00 00 00 00 00 00 00 00 00 00  <..o............
00000070  00 00 00 00 00 00 00 00 C1 A0 00 00 00 00 00 00  ........Á ......
00000080  00 00 00 00 00 32 00 00 00 00 00 00 00 00 00 00  .....2..........
00000090  00 00 00 00 7F 7F FF FF 00 00 00 00 00 00 00 00  ......ÿÿ........
000000A0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
000000B0  00 0A 00 0A 00 00 FF 08 00 00 00 00 00 00 00 00  ......ÿ.........
000000C0  00 00 00 00 00 00 00 00 00 00 00 00 41 70 00 00  ............Ap..
000000D0  FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ÿ...............
000000E0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
000000F0  00 00 00 00 00 00 00 00 00 00 00 00 44 7A 00 00  ............Dz..
00000100  43 AF 00 00 44 2F 00 00 44 56 36 C4 42 C8 00 00  C¯..D/..DV6ÄBÈ..
00000110  43 0F 68 98 00 00 00 00 00 00 00 00 00 00 00 FF  C.h˜...........ÿ
00000120  00 00 00 00 00 00 00 00 80 41 78 90 00 00 00 00  ........€Ax.....
00000130  00 00 00 00 80 40 71 EC 00 00 00 00 00 00 00 00  ....€@qì........
00000140  80 1A F1 D0                                      €.ñÐ
```

Actor's Main Function:
- Return: `0x800B974C`
- Signature: `void (z64_actor_t* actor, z64_game* game);`

## Fairy Animation State

Attempting to reverse via sound effect:

- Fairy actor: `0x8041B5A0`
- Sound effect happens: `0x801A5CFC(0x480B, 0x801DB4A4, 4, 0x801DB4B0)`
  - Return: `0x8019F100`
  - Return Function: `0x8019F0C8`

Call chain:
- Return: `0x8019F100`
  - Function: `0x8019F0C8`
- Return: `0x80115934`
  - Function: `0x80195908`
- Return: `0x80407D38` (in Link's actor structure?)
  - Only gets hit once, when collecting fairy.
  - Function: `0x80407B84`
    - This also only seems to get called once, when collecting fairy.

Function: `0x80407B84`
- Args:
  - A0: `0x8040CA40` (`z64_actor_t *` points to fairy actor)
  - A1: `0x803E6B20` (`z64_game_t *`)
- Seems to process a fairy interaction?

Animation counter: `*(uint16_t *)((z64_actor_t *)actor +0x25A)`
- Writes at: `0x8040A2C0`
  - Function: `0x8040A288`
  - Return: `0x800B974C`

## Calling Fairy Process Too Early

Seems to only hit `0x80407D04` if *close to* interacting with fairy.

...

Seems to branch early at `0x80407CA8`.
- Hits this as the fairy spawns after transitioning to a new area.
- Is checking `(*(uint16_t *)((z64_actor_t *fairy) +0x262) & 0x4000) == 0`
  - If so, branches to near end of function.
  - If we `OR` with `0x4000`, can maybe trigger fairy early?

...

Immediately after transitioning areas.

Seems to be function call at `0x80406654`, return value is used

`A0` and `A1` both point to `z64_xyzf_t` structs, with floats for `x`, `y` and `z`.
But `A2` is a bit weird? On loading into new transition, it is `0x42C80000`.
- Also: `100.0`

After the transition, the value uses `0x41200000` as well.
- Also: `10.0`

### `0x80407B84` Branches

On first frame of fairy spawning when entering an area, without interaction:
- `0x7BCC`: Branch
- `0x7C2C`: No branch
- `0x7C5C`: Branch
- `0x7C98`: No branch
- `0x7CA8`: Branch (to near function end)

When spawning a fairy that is instantly collected:
- `0x7BCC`: Branch
- `0x7C2C`: No branch
- `0x7C5C`: Branch
- `0x7C98`: Branch
  - Differs here!

Check at `0x80407C98`:
- Checks result of function call to `0x801233E4`
- Branches if result is `0`

Function: `0x801233E4`
- Args:
  - `A0`: `0x803E6B20` (`z64_game_t *`)

```c
bool func_0x801233E4(z64_game_t *game) {
    // This might be the issue?
    if (!func_0x80123358())
        return false;

    // This part doesn't seem to be the issue
    void* A1 = *(void **)((&z64_game) +0x1CCC); // 0x803E87EC‬, points to 0x803FFDB0 (Link struct)
    uint8_t byte = *(uint8_t *)(A1 +0xAA5);     // 0x80400855‬
    return (byte ^ 5) < 1;                      // Might be wrong here
}
```

Function: `0x80123358`
- Seems to be a general "can interact with things" function???
- Args:
  - `A0`: `0x803E6B20` (`z64_game_t *`)
  - `A1`: `0x803FFDB0` (`z64_link_t *`)

```c
bool func_0x80123358(z64_game_t *game, z64_link_t *link) {
    // Checks action state flag 1
    if ((*(uint32_t *)(link + 0xA6C) & 0x20000280) != 0)
        return false;

    // Checks byte at: link+0x394
    if (*(uint8_t *)(link +0x394) != 0)
        return false;

    // Checks if bits are set in byte: game+0x18875
    if ((*(uint8_t *)(game +0x18875) ^ 0x14) != 0)
        return false;

    // Checks byte at: game+0x18B4A
    if (*(uint8_t *)(game +0x18B4A) != 0)
        return false;

    // Check action state flag 1 again
    if ((*(uint32_t *)(link + 0xA6C) & 1) != 0)
        return false;

    // Check action state flag 3
    if ((*(uint32_t *)(link +0xA74) & 0x80) != 0)
        return false;

    // Check byte at: game+0x1F08
    return *(uint8_t *)(z64_game +0x1F08) != 0;
}
```

### Owl Statue Warp Crash

Spawning a fairy after using owl warp is crashing, because the code containing the ProcessFairy function `0x80407B84` has moved!

It jumps to this from a function pointer variable.

Return: `0x8040A2A8`
- Function: `0x8040A288`
Return: `0x800B974C`

The `ProcessFairy` function is just the `Main` function of the fairy actor in memory, duh!
