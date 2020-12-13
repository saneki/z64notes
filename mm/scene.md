Scenes
======

## Entrance Value (in `z2_file_t`)

Updates entrance value (`0x801EF670`) at: `0x80167058`
- Function: `0x80166B30`
- Retrieves new value from: `(uint32_t)(*(uint16_t *)(0x803FEB20 +0x87A))`
  - Address: `0x803FF39A`
  - Calculates base from: `A0 + 0x18000`, where `A0 = 0x803E6B20` (`z2_game_t`)
  - So basically, gets new value from `0x803E6B20 +0x1887A`
- This function is called once per frame.
- Branches:
  - `0x80166FC0`: hit per frame of fade in & out of scene transition
  - `0x80166FD8`: hit once before scene change, once after scene change
  - `0x80167008`: hit once before scene change
  - `0x80167028`: hit once before scene change

Function `0x80166068`:
- Some sort of function used in scene initialization?
- Called twice during scene transition:
  - Called after fade out of old, before fade in to new:
    - Return: `0x8016631C`
    - Function: `0x8016613C`
      - Return: `0x80173A98`
      - Function: `0x80173A50`
  - Called after fade in to new finished:
    - Return: `0x801670D0`

## Scene Value (in `z2_game_t`)

As discussed above, is located at `0x803E6B20 +0x1887A`, which is `0x803FF39A`.

Note: All heap addresses assume heap is modified to end at `0x80750000` instead of `0x80780000`.

- Set to scene value at: `0x8072296C`
  - Function: `0x80722934`
  - Return: `0x80722CBC`
- Cleared at: `0x80089680`

The value is set right as the scene transition animation happens, and it is cleared mid-transition
after the screen fades out.

## Load Room

Load room function: `0x8012E96C`
- Return: `0x8012E954`

## Weather Effects Actor

Mountain Village: `0x6402`, `278.0,  2000.0,  300.0`
Path to Snowhead: `0x6402`, `735.0, -1141.0, -1632.0`

## Actor Spawning

When scene starting, spawns actors using function: `0x800BAE14`
- Return: `0x800BB484`
- Return Function: `0x800BB2D0`
  - Return: `0x800B92E0` (called once?)
  - Return: `0x800B9438` (called multiple)
    - Function: `0x800B9334`

Function: `0x800BB2D0`
- `z2_actor_t* func_0x800BB2D0(z2_actor_ctxt_t *actor_ctxt, void *in_room_struct, z2_game_t *game);`
- Arg `A1` increments by `0x10` per call to this function? Pointer into list in room struct?

Function: `0x800B9334`
- Hit once per frame
- Check at `0x800B937C` for if loading new scene?
  - If `*(int16_t *)(0x803FEB20 +0x846) > 0` then loading new scene and load in actors?
