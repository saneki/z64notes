Bomb Lady Speedup
=================

Relevant Spectrum output:

```
// Sakon
40B9A0:410240 AF 0237:  0000 01 FILE: 0100F810:010140B0 INIT 8040F980:010137F0
410250:4106AC AI 0237:  4 00 0 83FF (  383.0   240.0 -2494.0) 0000 C000 0000
// Bomb Shop lady
428390:42A240 AF 0236:  0000 01 FILE: 0100D960:0100F810 INIT 80429EF0:0100F4C0
42A250:42A690 AI 0236:  4 00 0 02FF ( -423.6   200.0 -2576.8) 0000 0031 0000
```

- VRAM: `0x80BAA6D0`
- VROM: `0x0100F810`
- File entry offset: `0x1C5E0`
- File index: `526`

- Actor main: `0x8040F3D8`
- Actor draw: `0x8040F808`

- When starting cutscene, at: `0x8040D6FC`
  - Calls `ActorCutscene_Start(0x12, 0x80410250)`
- After "Ouch! Watch out!", at: `0x8040E5D0`
  - Calls `ActorCutscene_Stop(0x12)`, index is from: `*(s16*)(actor +0x456)`
  - Calls `ActorCutscene_SetIntentToPlay(0x13)`, index is from: `*(s16*)(actor +0x458)`
  - Calls `ActorCutscene_Start(0x13)`, at: `0x8040E524`
- After "Stop! Thief!!!":
  - Calls `ActorCutscene_Stop(0x13)`, at: `0x8040E73C`
- After saving luggage and Sakon runs off, talking to bomb lady:
  - Calls `ActorCutscene_Start(0x7C, 0x803FFDB0)`, at: `0x8074F8AC`
  - This is likely just for starting the dialogue?

Sakon `u32` state field at offset `0x450`
- `0x01` - Loitering before cutscene
- `0x02` - Running towards bomb lady
- `0x03` - Dropping bag
- `0x05` - Running with bag
- `0x06` - Running without bag

Sakon has a function pointer called by main at offset `0x148`.
While running away, this function is always `0x8040E650`.

When Sakon is gone, code at `0x8040E834` sets a flag in `z2_file`.
- Uses field `*(u16*)(actor +0x1E6) & 8 == 8` to determine if luggage is saved.
- Calls function `0x801A89A8` to fade out chase BGM.
- Updates field: `*(u16*)(actor +0x1E6) |= 4`
- Calls function `0x8040BB5C(0x803E6B20, 0xD670)` to zoom-out and begin "cutscene" with bomb lady.

This code only gets hit if `*(s32*)(actor +0x1F8) == 0xFFFFFF9D`, or `-0x63`.
- This is likely used to define which "path" Sakon is taking in the scene?
- Setting this to `0xFFFFFF9D` during the chase will cause it to cleanly end and despawn Sakon!

## Movement

Code at `0x8040E8A0` updates Sakon's movement, calls function: `0x800B6A88`.

Isn't updating Sakon's movement when ending sequence for two reasons:
1. This function call to `0x800B6A88` only happens if branch to set flags, finish sequence, etc doesn't get taken. The code is actually right under it, after a branch.
2. These fields at `0x64`, `0x68` and `0x6C` are directly influenced by fields at `0x70`, `0x74` and `0x78`. These also get set when sequence finishes.

The `xz_velocity` field at `0x70` get written to by function call right beforehand, function `0x800FFDF8`:
- `0x800FFDF8(actor +0x70, 4.0, 0.2, 0.5)`

This velocity field gets set to 0 at `0x8040E864`.
