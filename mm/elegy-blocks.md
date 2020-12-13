Elegy Blocks
============

Camera field at offset `0x142` is modified while playing the cutscene:
- Written to `0x3B` at: `0x800DFA84`, while forcing camera to block movement.
  - Function: `0x800DF8EC`
- Written to `0x48` at the same place, while panning camera back to player.

Function trace while writing `0x3B`:
- Function: `0x800DF8EC`
  - Return: `0x800DFBB8`
- Function: `0x800DFB14`
  - Return: `0x800F1F80`
- Function: `0x800F1D84`
  - Return: `0x800F1C84`
- Function: `0x800F1C68`
  - Return: `0x8042DFE4`

Relevant Spectrum output:

```
42DC80:42EAB0 AF 0245:  0000 09 FILE: 01028960:01029790 INIT 8042E900:010295E0
```

Actor `0x245` is `Bg_F40_Block`, or "Stone Tower Temple Shifting Block".

-----

Function call: `0x800F1C68(*(s8*)(actor +0x38), actor)`

Notes:
- Field at `*(s16*)(camera[1] +0x1C)` seems to be used to count down frames for camera panning animation.
- The initial value is written at `0x800DC8D8`.

```c
f32 value = *(f32*)(camera +0x4);
u16 result = (u16)sqrt(value - 200.0);
```

### Bleh

The uppermost function `0x800F1C68` is also called while writing `0x48`:
- Function: `0x800F1C68`
  - Return: `0x800F1AA8`
- Function: `0x800F1A7C`
  - Return: `0x801690B0`
- Function: `0x80168F64`
  - Return: `0x801737A8`
- Function: `0x8017377C`
  - Return: `0x80174524`
- ...

When writing pointer of actor to camera before cutscene:
- `0x8042DFDC`: Calls `0x800F1C68`


### Camera State Notes

The Stone Tower block actor calls `0x800F1C68` with value `0xF`, part of the actor struct at offset `0x38`.
In a function call to `0x800F1D84`, this value gets written to `0x801BD8B0`.
After further checking, the value at this address gets updated to `0x7E` when camera is panning back to the player.
- This value is written to by the same function mentioned (`0x800F1D84`), see trace [1].

Function trace [1]:
- Function: `0x800F1D84`
  - Return Address: `0x800F1C84`
- Function: `0x800F1C68`
  - Return Address: `0x800F1AA8`
  - This function call passes hardcoded value `0x7E` via `A0`.
  - Note: Only does so if `0x800F1BE4(0x7E) != 0`
- Function: `0x800F1A7C`
  - Return Address: `0x801690B0`
- Function: `0x80168F64`
  - Return Address: `0x801737A8`
- Function: `0x8017377C`
  - Calls function `0x80168F64` via variable.
  - Specifically calls function at `0x803E6B20 +0x4`, which is apparently the "gamestate update" function.

## Active Cameras

### Function `0x801694DC`

- Checks `0x803E6B20 +0x800`, which is active cameras array, until it finds a NULL entry and returns counter?
- Actually sets up the next available camera for use, while preserving state of previous cameras?
- Maybe the 4 cameras are meant to be a "stack"?
- Possible name/signature: `z2_ActivateNextCamera(z2_game_t *game)`

Function chain (when panning camera to player):
- Function: `0x801694DC` (`z2_ActivateNextCamera`)
  - Return Address: `0x800F1E5C`
- Function: `0x800F1D84`
  - Return Address: `0x800F1C84`
- Function: `0x800F1C68`
  - Return Address: `0x800F1AA8`
- Function: `0x800F1A7C`
  - Return Address: `0x801690B0`
  - This is the same function with the hardcoded `0x7E` values.

### Function `0x80169600`

Inferred signature: `z2_DeactivateCamera(z2_game_t *game, s16 index)`

## Camera Deactivation

When deactivating camera (set pointer to `0`) to prepare for panning, the following call chain occurs:

- Function: `0x80169600`
  - Return Address: `0x800F1A40`
- Function: `0x800F17FC`
  - Return Address: `0x800F1B18`
- Function: `0x800F1A7C`
  - Return Address: `0x801690B0`

So the camera deactivation is done by the game state itself, rather than an actor.

## Example Implementation

`0x800F1AA0`: `NOP` out function call which eventually activates 2nd camera for `0x7E` camera panning?
`0x80169A38`: `NOP` out function call which copies position values from one camera to current?
- Function: `0x801699D4`

### Function `0x801699D4`

Inferred signature: `z2_CopyCameraFields(z2_game_t *game, u8 dest_index, u8 src_index)`

Function trace during Stone Tower block animation:
- Function: `0x801699D4`
  - Return Address: `0x800F18CC`
- Function: `0x800F17FC`
  - Return Address: `0x800F1B18`
- Function: `0x800F1A7C`
  - Return Address: `0x801690B0`

### Function `0x800F1A7C`

The function call to `0x800F17FC` seems to restore control to the original camera. `NOP`-ing it out causes the camera to hang when it should switch over.
- Only calls this function if `*(s16*)(0x801BD8B0 +4) != 0xFFFF`

### Function `0x800F17FC`

Only calls function `0x801699D4` if specific return value has a field which is `2`.

```c
u8 *v0 = 0x800F14F8();
if (*(v0 +0xA) == 2) {
    // ...
    0x801699D4();
    // ...
}
```

### Function `0x800F14F8`

`0x800F14F8(s16 value)`
- When panning camera back, uses `A0` value of `0x7E`.

Seems to be "actor cutscene" structs, see: https://wiki.cloudmodding.com/mm/Scenes_and_Rooms#Actor_Cutscenes

```c
func_0x800F14F8(s16 value) {
    if (value < 0x78) {
        // Points into scene data, containing some camera info structs?
        u32 *p = (u32 *)0x801F4DF0;
        return *p + (value * 0x10);
    } else {
        // If in range [0x78, 0x7F], then use one of 8 global camera info structs?
        value -= 0x78;
        return 0x801BD830 + (value * 0x10);
    }
}
```

Data at `0x801BD830` seems to be an array of 8 structures size `0x10` each.
- Each struct seems like its own array of 8 16-bit values.

### Function `0x800F1BE4`

I think this function is meant to get the value of a bit in a bit array at `0x801F4E10`.
- The bitfield has an index (index of byte), and a shift field (index of bit into byte).
- And then simply returns 0 if not set, or 1 if set.

```c
s16 func_0x800F1BE4(s16 value) {
    if (value == 0x7F) {
        if (*(s16*)0x801BD8B0 == -1) {
            return 0x7F;
        } else {
            return 0;
        }
    } else if (value < 0) {
        return -1;
    } else {
        // The input value is a bitfield consisting of an index and a 3-bit shift field used in a mask.
        s16 index = value >> 3;
        u8 *byte = *(u8*)(0x801F4E10 + index);
        u8 shift = value & 7;
        u32 result = (1 << shift) & byte;
        if (result == 0) {
            return 0;
        } else {
            return 1;
        }
    }
}
```

## Block Speed

Copies position values from offset `0x24` to `0x3C` at: `0x80433864`
- Copies vector values using function `0x800FF50C`.

When traveling "slowly", new position values (offset `0x24`) written to at: `0x801004B0`

Trace:
- Function: `0x80100448`
  - Return Address: `0x80432F14`

Seems to get speed at offset 0x70.
- Slow: 20.0 (hardcoded value `0x41A00000` in function at `0x804334D8`)
- Fast: 40.0 (hardcoded value `0x42200000` in function at `0x804336F8`)

Relevant Spectrum output:

```
432C30:433A60 AF 0245:  0000 09 FILE: 01028960:01029790 INIT 804338B0:010295E0
```

Actor: `0x245`
- File VRAM: `0x80BC3980`
- File VROM: `0x01028960`
- File table offset: `0x1C6C0`
- File index: `540`
