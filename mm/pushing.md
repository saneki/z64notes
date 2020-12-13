Pushing / Pulling Blocks
========================

Action state 2 flag: `0x80400820`

Sets action state 2 at:
- `0x80123DB4`
  - `AND`-ing it by `0xFFFFDFFF`
  - Return: `0x80123E80`
- `0x80762E84`
  - `AND`-ing it by `0xFFDFFFFD`
- `0x80762EBC`
  - `AND`-ing it by `0xFBBEAC92`
- `0x8076C304`
  - `OR`-ing it by `0x0141` (push)
  - Setting `GRABBING` and `MAY_GRAB` bits, probably only happens when grabbing a block.
- `0x8076C45C`
  - `OR`-ing it by `0x0141` (pull)
- `0x8075B774`
  - First sets `PUSH_PULL` bit (changes to `0x0151` for pull).
  - `OR`-ing it by `0x0010`
  - References:
    - Byte at:  `0x803FFEFF` (or `link +0x14F`)
    - Table at: `0x80779644`

Function: `0x8075B6C4`
- Initiate block push?
- Does trigger if trying to push into "wall."

Function: `0x8075B71C`
- Signature: `init_block_pull(z64_link_t *link, z64_game_t *game);`
- Initiate block pull?
- Does trigger if trying to pull into "wall."

## Function: `0x8074E924`

I think this is just the function that sets some function pointer based on the current action.

See: `0x8074EA84`

Sets `0x803FFDB0 +0x748` to pointers? Specifically from argument `A2`.
- Address: `0x804004F8`

Values:
- `0x8076AC00` for grab?
- `0x8076C22C` for complete?
- `0x80767470` for ???
- `0x8076842C` for near block?
- `0x8076C2E0` for push?
- `0x8076C42C` for pull?

The push (and pull?) functions get called per frame as long as that variable points to them.

After the pulling is complete, this function pointer gets set to something else: `0x8074EA84`
- Function: `0x8074E924`
  - Return: `0x80753EDC`
- Function: `0x80753E84`
  - Return: `0x8075B688`
- Function: `0x8075B5DC`
  - Return: `0x8076C4D4`
- Function: `0x8076C42C`
  - This is the pull function!
  - Thus the call to `0x8075B5DC` eventually sets the next action function.

Function: `0x8075B5DC`
- `A1` seems to be a flag which indicates direction of block being pulled?
  - Seen: `0x0000`, `0x4000`, `0x8000`, `0xC000`

## Tracing Link's Position

Link's position moves when pulling a block: `0x800FF518`
- Function: `0x800FF50C`
  - Return: `0x8076345C`
  - Copying from: `0x803FFDD4`

Position data at `0x803FFDD4`:
- Breaks on write: `0x800B69EC`
  - Function: `0x800B69AC`
  - Return: `0x807621FC`

Function: `0x800B69AC`
- Sets position value from float math:
  - `F0  = *(float *)0x801AECEC`
  - `F4  = *(float *)(0x803FFDB0 +0x64)`
  - `F6  = F4 + F0`
  - `F8  = *(float *)(0x803FFDB0 +0xA4)`
  - `F10 = F6 + F8`
  - `F16 = *(float *)(0x803FFDB0 +0x24)`
  - `F18 = F16 + F10`
- The only value that seems to be non-zero when pushing block is `+0x24`.
- This `+0x24` value is written when pulling at `0x8075B330`
  - Function: `0x8075B1AC`
    - Return: `0x8075B3B8`
  - Function: `0x8075B374`
    - Return: `0x8076C4C8`
  - Function: `0x8076C42C`
    - Found the pull function again!
    - Thus the function call to `0x8075B374` updates Link's position when moving the block.
    - Also, when this function is NOP-ed out, the block is never actually pulled.

Function: `0x8075B374`
- Hardcoded floats:
  - `0x40A00000` (`5.0`)
  - `0x41700000` (`15.0`)
  - `0x41D66667` (`26.8`)
- Also uses float at `0x80779238 +0x38`.
  - From messing around with this, float at `0x80779238 +0x38` seems to affect Link's collision distance?
- From experimenting, these values affect block grabbing more than anything?

### Block Object

Pointer to block object? (Snowhead Temple Puzzle): `0x8059C480`
- Breaks on some position write (`0x8059C430 +0xC`): `0x800C6F04`
  - Function: `0x800C6838`
    - Return: `0x800C7528`
  - Function: `0x800C73E4`
    - Return: `0x800B98B0`
  - Function: `0x800B9780`
    - Return: `0x80167BA0`
  - Function: `0x80167814`
    - Return: `0x80167EFC`

T5 = `0x0018 (0x80655E48)` = `0x80655D58`
T8 = T5 + `0x50` = `0x80655DA8`

### Block Object 2

Also written to at: `0x800C7110`
- This seems like it may be the "Actual" value.
- Later on in the same function as above? (`0x800C6838`)

## Pull Function Trace

While in the actual act of pulling a block:
- C46C: Branch
- C488: Branch
- C4D4: Branch -> C554
- C564: No branch
- C5A4: No branch
- C608: No branch

Initial call:
- C46C: Branch
- C488: No branch
- C49C: Branch
- C4D4: Branch -> C554
- C564: No branch
- C5A4: No branch
- C608: No branch

Function call to `0x807531BC` might trigger block movement?
