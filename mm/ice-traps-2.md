Ice Traps
=========

## Midair Damage

Link damage function in `player_actor`:
- Vanilla: `0x80750FA8`
- Offset:  `0x6088`

When attacked by Ice Keese, uses `A2 = 3` for argument.

## Player Function Pointer

Player actor uses a function pointer for the current state of the player (action?).

Function pointer field: `*(void**)(link +0x748)`
- Absolute: `0x804004F8`

This pointer is updated in function `0x8074E924`, using argument in `A2`.
- It can be called from multiple places.

### Function `0x80771B60`:

This is the function used for handling player state while in ice.

On land it runs for multiple frames, in water it only runs once so something is overwriting it.

What this function does when not branching (usual behaviour until timer field == 6):
- Sets `*(s8*)(link +0xAE7) += 1`, which is a timer-related field.
- Sets `*(u32*)(link +0xA70) |= 0x4000`, labeled as `Z2_ACTION_STATE2_FROZEN`.

After 1 frame, function pointer is updated with `0x8076DD58`.
- Return: `0x80758F24`
  - Function: `0x80758DC0`
  - Function called once when entering water.
    - Return: `0x8075934C`
    - Branches at: `0x807592A0`
      - Branch is hit per-frame when in water?
      - Checks state flags: If `flag1 & 0x0FFFFFFF` is greater than 0.
      - Basically optimized checking if `Z2_ACTION_STATE1_SWIM` is set.
    - Before this, branches at `0x8075910C` if on land, does not reach other branch.
      - Gets hit multiple times per frame? Sometimes branches and sometimes not?
      - Branches if: `*(f32**)(link +0xA68)[11] >= *(f32*)(link +0x8C)`
        - Compares player `water_surface_distance` field to float value in table.
        - Link points to some table of floats: `*(f32**)(link +0xA68) == (f32*)0x80779080`
          - This pointer changes depending on Link's form.
          - For Zora the value at `[11]` is: `56.0`
- This code seems to be hit whenever Link enters water in swimming state.

Branches taken to reach `0x80759344`:
- If-loop for a bunch of hardcoded function addresses, checking if function pointer is one of them.
- If not, call function which sets function pointer for swimming?

### Function `0x8076DD58`

NOP-ing out function calls:
- `0x8074BB0C`: No longer draws Link's arm animations.
- `0x80764A44`: Link sinks but remains in swimming animation/state.

Function `0x80764A44` is likely used to handle Link's buoyancy.

Zora seems to sink after a few frames even with buoyancy.
- Seems to be updating function pointer for Zora, see: `0x807515A8`
  - Returns: `0x80771C0C`, inside function for handling frozen state.
- Updates function pointer to `0x807716AC`
  - This function seems to be called for other forms when voiding, may need to check if Zora form and swim flag set?

### Other Notes

Updates function pointer to `0x8076DD58`.
- Returns: `0x80758F24`
  - Same function call we saw earlier for entering water.
  - Returns: `0x8075934C`

- If `Z2_ACTION_STATE1_SWIM` is not set, update state.
- Else
  - If `*(s8*)(link +0x145) < 5`, And (check function against hardcoded addresses)

```c
if ((state & SWIM_STATE) == 0 || )
```

## Sound Effects When Entering Water

Function `0x8074B41C` - Seems like a function to emit player sound effects (grunts, etc), probably factors in form?

Calls to `0x800B8E58` which relate to player in water:
- `0x80758D88` - Splashing sound when entering water, Id: `0x2889`
  - Function: `0x80758D60`
  - Same function: At `0x80758D78`, calls function `0x80754BC0` to spawn actor for splash effect.
- `0x80758B24` - Mini-spash sound when entering water, Id: `0x863`

Function `0x80758D60`:
- Offset: `0xDE40`
- Causes splash visual & sound effects when entering water.
- Called at: `0x80758F80`, in function: `0x80758DC0` (function called when entering water)
  - If SWIM flag is not set, or...
  - Compares Link's water-dist field, branches over if not "in water."

## Visual Effect

`0x807643EC` - Checks if frozen flag is set, if so draws ice?
- When ice splinters, seems to be drawing in actor code, but Spectrum does not recognize the actor?

### Cracking-Ice Actor & Relevant Table

What seems to be actor details (found at `0x801AE778`, actor RAM was `0x8051E660`):
```
00DF1A70 00DF1E70 8097ECD0 8097F0D0
8051E660 8097F070 01000000
```

This actor table seems to be at: `[0x801AE4A0, 0x801AE8E4)`
- Contains: VROM start, VROM end, VRAM start, VRAM end, RAM pointer, VRAM init, flags?

## Landing Frozen In Water (Non-Zora)

When landing into water when in frozen state (with "frozen" function pointer), updates function pointer upon landing.
- Does so from function call at: `0x80758F1C`
- As documented previously, this is in part due to branch at `0x807592A0`. This branch is not even reached if frozen Zora.
  - It *does* get hit if non-frozen Zora.
  - So why isn't frozen Zora reaching this branch?
  - This entire function (`0x80758FDC`) is no longer hit once in voiding state.
    - The function is called at: `0x80762ABC`
  - Doesn't get called because "time stop" player flag is set when voiding!
