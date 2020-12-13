World of Skulltula
==================

## Planning Ideas

- Fork of MMR nicknamed "World of Skulltula"
- Custom Readme file for GitHub, ex: `SKULLTULA.md`
- Use `strict_yaml` for base file defining Skulltula details, paths, pools, etc.
- Script will compile YAML to JSON for being embedded in Randomizer.
  - Script would also generate Markdown and maybe HTML tables for documentation.
  - Name identifier, scene, time of day, basic or advanced, pool, max # in pool, logic details

General layout of documentation:
- World of Skulltula is a modification of MMR which distributes Skulltula throughout the world.
- While this means that Skulltula have been removed from the spider houses, Skulltula can still spawn in them in unique locations.

### Problems to Solve

In-game problems:
- Ensure Skullwalltulas cleanly despawn as daytime happens, if flagged for night-only.
  - Reference to OoT for how that should look: https://youtu.be/1APMxFyoLp4?t=1100
  - Will probably want to see how this happens in OoT, they likely have a function for it unused in MM which we can call.
- Certain scenes have issues when Skullwalltula object is "injected" into objects list, specifically: Stock Pot Inn, Romani Ranch
- Have path data retrieved from custom source instead of scene commands.
- Allow sword, hookshot, etc to be used in specific scenes if enabled (ex. Stock Pot Inn).
- Figure out how to spawn from bonking a tree, breaking a box or pot?
- If placing in miniboss rooms, need to ensure the fight ends even if Skullwalltula is alive.
- If placing in scenes with archery games, need to ensure it doesn't interfere with mobs spawning.

### Notable Boxes

- Cuccoo shack.

## Reading Actor Variable (Constructor) :: Session 1

```
416400:419940 AF 0050:  0000 01 FILE: 00D52B10:00D56050 INIT 80419480:00D55B90
```

Constructor: `0x80418F14`

- `0x80417434`: Loads `var & 0x3FC`
  - A2 = Chest Flag
  - T7 = Type
- `0x80418FC4`
- `0x80419024`: Loads path value from var: `A1 = ((var & 0xFF00) >> 8) & 0xFF`
  - Calls function `0x8013BEDC`, some sort of path-related function?
  - `func_0x8013BEDC(game, path_var, 0xFF, actor +0x4A0)`

## Reading Pathway Index :: Session 2

```
41FE20:423360 AF 0050:  0000 04 FILE: 00D52B10:00D56050 INIT 80422EA0:00D55B90
```

During init function:
- Loads var at: `0x80422A44`
- Calls: `func_0x8013BEDC(game, path_index, 0xFF, actor +0x4A0)`
- Returns pointer to path table entry in scene data, stores in `0x1E4`.
- Near end of function, checks if `0x1E4` pointer is non-NULL.
  - If so, calls function `0x804213E8`.

- Path index is at `*(u32*)(actor +0x4A0)`.
- Reads at: `0x80421FD4`.
  - Calculates: `A1 = pathbuf + (index * 6)`, passes to function call `0x800FF54C`.
    - Converts X/Y/Z of `[u16]` to `[f32]`, stores in `0x0034,8,C (SP)`
    - Calls function `func_0x80420D74(actor, f32 *node)`
    - Calls function `func_0x80180100(F12=node.z, F14=node.x)`
  - Loads pointer from `0x0044 (SP)`, which is result of function call to `0x80100504`.
  - Calls: `func_0x80100504(skullwalltula->path.nodes)`, actor offset: `0x1E4`.
    - This likely takes segmented address (relative to scene data) of nodes field, and returns RAM address.

References fields of actor:
- `0x144: ?`
- `0x154: f32`
- `0x15C: f32`
- `0x164: void*`: Points further into actor data (part of linked list?)
- `0x168: void*`: Points further into actor data (part of linked list?)
- `0x188: void*`: Function pointer to following function in actor file.
- `0x18C: void*`: Function pointer to function in actor file?
- `0x1E4: void*`: Pointer to path table entry in scene data.
- `0x374: f32[3]`: Some float position.
- `0x414: f32`
- `0x450: f32`
- `0x454: s16`
- `0x456: s16`
- `0x45E: s16`
- `0x4A0: u32`: Path entry index in scene data.

### Investigating Specific Path

Swamp Skulltula in shallow water.
- Path entry index: `0xA`
- Path entry: `08FFFFFF 02000280`

Path data:
```
0078 FFEC FE98
0078 FFEC FCF4
FF87 FFEC FCF4
FF88 FFEC FC05
0078 FFEC FC03
0078 FFEC FCD5
FF87 FFEC FCD6
FF88 FFEC FE98
```

## Function `0x8013BEDC`

Signature: `0x8013BEDC(GlobalContext *ctxt, u8 path, u8 unk, u32 *result)`

Returns pointer into scene data, specifically pathway data (command `0x0D`)?
- Pathway data organized as arrays of nodes, followed by a table of entries, each pointing to an array of nodes using a segmented address (scene base address).

- Loads time of day: `T6 = *(u16*)(0x801EF670 +0xC)`
- Loads day index:   `T2 = *(u32*)(0x801EF670 +0x18)`

## Actor Spawning

`0x800BAE70`: Calls function `0x8012F608` to get object array index for actor?
- `A0` points to object context.

Object context: `0x803E6B20 +0x17D88 == 0x803FE8A8`

`0x8012F2E0`: Function which loads special object data onto object heap.
`0x8012F73C`: Loads normal object data onto object heap with negative object Id.
- Code at `0x8012F5C8` changes this back to positive?
- Called from at `0x8012FD2C`, which iterates through `[s16]` of object Ids and loads each object.

## Expanding Object Heap

### How is First Object Allocated?

Function `0x8012F2E0` used for loading special objects.

Gets dest address from: `0x0010 (T7)`
- `T7 = arg0 + (*(u8*)(arg0 +8) * 0x44)`
- Or, `T7` points to next unused object entry (size `0x44`).

So when no objects loaded, what writes dest address for initial object?
- Object context itself has a object-heap-start pointer.

This heap-start pointer is written to at: `0x8012F4A8`.
- Uses return value from function: `0x80172AC8`.
- Calls: `func_0x80172AC8(GlobalContext +0x74, ObjectCtxt *obj)`
  - First arg likely substruct with heap-related values.

Function grows the heap backwards for allocating object data:
```c
func_0x80172AC8(const u8 *heapInfo, u32 amount) {
  heapInfo.cur = (((heapInfo.cur & 0xFFF0) - amount) & 0xFFF0)
}
```

Uses `A3` for amount, which is determined earlier in function `0x8012F3D0`, by scene Id of all things??

```c
if (scene == 0x6C || scene == 0x6D || scene == 0x6E || scene == 0x6F) {
  size = 0x17E800;
} else if (scene == 0x15) {
  size = 0x18B000;
} else if (scene == 0x2D) {
  size = 0x16F800;
} else {
  size = 0x159000;
}
```

#### Tracing via Write

This just leads to thread which performs file read:

Writes first byte at `0x800810A8`, puts address in `S0` (which is from `A1` argument).
- Function: `0x80080FF0`
- Returns to: `0x800811F4`
  - Function: `0x80081178`: `Yaz0_LoadAndDecompressFile`
- Returns to: `0x80080B50`
  - Function: `0x80080A08`
    - Gets `A1` from: `0x0004 (A0)`
- Returns to: `0x80080BCC`
  - Function: `0x80080B84`
- Returns to: `0x80089420`
  - Not a function, likely thread entry for loading files.

### Special Actor Allocation?

`0x80087488`: Heap allocation pointer in `A0` for special actor file?
- Address in `A0`: `(V1 + V0) - A1`
  - `A1` is likely size of heap data to allocate.
  - `V1` seems to be pointer to previous heap entry, `V0` seems to be difference to apply to `V1`.

- Function: `0x80087408`
  - Calls with `A0 = 0x801F5100`.
  - Aligns `A1` to `0x10`-byte boundary?
  - Calls function `0x800871DC` which returns pointer to heap?
  - Stores pointer to next node in header, see: `0x80087494`.
    - This value gets re-written at `0x800873BC`
  - Returns to: `0x80102CA0`
    - Function: `0x80102C88`
  - Returns to: `0x800BAD84`
    - Function: `0x800BACD4`
  - Returns to: `0x800BAE4C`

## Disabling Buttons

Disables B-Button for sword when entering scene: `0x80110F54`
Disables C-button for Hookshot when entering scene: `0x801119D0`

In scene without these disabled: Branches at: `0x80110E08`
- Function starts at: `0x80110038`
- Branches: `??? -> 0A58 -> 0B14 -> 0B18 -> 0B84 -> 0BCC -> ... -> 0C70 -> 0D44 -> ... -> 0D64 -> 0DB0 -> ... -> 0DD0 -> 0DF8 -> 0E08`

East Clock Town:
- Branches: `0x005C -> 0x0160`
- Branches: `0x0168 -> 0x01BC`
- Branches: `0x01C4 -> 0x0218`
- Branches: `0x0220 -> 0x0468`
- Branches: `0x0470 -> 0x04C4`
- Branches: `0x04C8 -> 0x05D8`
- Branches: `0x05DC -> 0x0698`
- Branches: `0x0698 -> 0x0728`
- Branches: `0x0744 -> 0x0A4C`
- Branches: `0x0A58 -> 0x0B14`
- Branches: `0x0B18 -> 0x0B64`
- Branches: `0x0B84 -> 0x0BCC`
- Branches: `0x0BD0 -> 0x0BE4`
- Does not branch: `0x0BE8 -> 0x0E10`
  - Diverges here, Inn does branch.
  - Branches if: `*(u8*)(0x803E6B20 +0x169E8 +0x30F) != 0`
  - Byte at `0x30F` of HUD context, `restriction_flags[1]`
    - Absolute: `0x803FD816`
  - Setting `restriction_flags[1] = 0` allows sword.
  - Setting `restriction_flags[11] = 0` allows hookshot, now.
  - Setting `restriction_flags[5] = 3` disallows Song of Double Time.

Restriction flag for sword is written at: `0x80112A34`
- Function: `0x801129E8(GlobalContext *ctxt)`
- Relevant address: `0x801BF6C0`

Loads `V1 = *(u8*)(ctxt +0xA5)`, scene index casted to `u8`.
- Seems to iterate through `u32` array at `0x801BF6C0`.
- Each value includes scene Id (as `u8`) and bitfield for indicating restriction flags?

## Crates

```
416470:416620 AI 00E5:  1 03 0 800A ( -876.0     0.0  -270.0) 0000 4000 0000
416630:4167E0 AI 00E5:  1 03 0 801B ( -750.0     0.0  -876.0) 0000 8000 0000
```

Notes:
- Crates spawning Gold Skulltula seem fairly straightforward:
  - `Crate 0x800A => Skullwalltula 0xFF29 => (Path = 0xFF, Flag = 0xA,  Type = 0x1)`
  - `Crate 0x801B => Skullwalltula 0xFF6D => (Path = 0xFF, Flag = 0x1B, Type = 0x1)`
- Crate variable `0x7F3F` seems to indicate empty crate.

## Trees

Testing in Romani Ranch early Day 1.

```
42E510:42F890 AF 0041:  0000 0B FILE: 00D3DDF0:00D3F160 INIT 8042F5F0:00D3EED0
```

OoT documentation lists `init_rot.z` being used alongside actor variable to specify Skullwalltula in tree actor (`En_Wood02`).
On `En_Wood02` init, will copy `init_rot.z` value to `*(s16*)actor +0x148`.

Function `0x8042ED68` handles spawning item from tree after rolling into.

## Actor Spawning For Current Room

### Special Actors

Loads special actors? Such as actors with Id `0x0000` and `0x0010`.
Calls function: `0x800BAE14`
- Returns to: `0x800BB484`
  - Function: `0x800BB2D0`
- Returns to: `0x800B92E0`
  - Function: `0x800B9170`
- Returns to: `0x8016AAA4`

Loads other special actors? (Id `0x015A`):
Calls function: `0x800BAE14`
- Returns to: `0x800BACC4`
  - Function: `0x800BAC60`
- Returns to: `0x8016AB5C`

### Other actors

Loads other actors:
Calls function: `0x800BAE14`
- Returns to: `0x800BB484`
  - Function: `0x800BB2D0`
- Returns to: `0x800B9438`
  - Seems like it calls function in a loop.
  - Function: `0x800B9334`
- Returns to: `0x800B97F0`
  - Function: `0x800B9780`
- Returns to: `0x80167BA0`
  - Seems to call function once per frame.

If actors already loaded, branches at `0x800B937C`.
- This block will only run once to spawn actors for room load?
