Sound Check Speedup
===================

Relevant Spectrum output:

```
40B330:40D070 AF 0234:  0000 01 FILE: 01008800:0100A540 INIT 8040CC40:0100A110
40D080:40D34C AI 0234:  4 00 0 3FFF (  -27.0    -8.0  -275.0) 0000 8766 0000
```

## `En_Toto` (Toto)

- Actor main: `0x8040CA9C`
- Actor draw: `0x8040CB6C`

- VRAM: `0x80BA36C0`
- VROM: `0x01008800`
- File entry offset: `0x1C5B0`
- File index: `523`

### Main Function (`0x8040CA9C`)

For main functionality, seems to call one of two ways:
- Directly calls `0x8040C924`, or...
- Gets an index in `*(u8*)(actor +0x2B0)` to get function pointer from array at: `0x8040CE28`

#### Calling `0x8040C924`

Calls `0x800EE29C` to decide whether or not to directly call `0x8040C924` instead of one of the 3 main function pointers.

So what does `0x800EE29C` do?

```c
int func_0x800EE29C(z2_game_t *game, u16 arg) {
    // Check cutscene state field.
    if (game->field_u8_1F2C != 0) {
        u16 index = 0x800EE200(game, arg);
        if (index != 0xFFFF) {
            if (0 < game->field_u32_1F4C[index]) {
                return 1;
            }
        }
    }
    return 0;
}
```

Notes:
- Cutscene state field: `*(u8*)0x803E8A4C`

#### Cutscene Field Write

- When beginning post-song dialogue, sets cutscene state byte to `0x01` at: `0x800EDB3C`
  - Function: `0x800EDA84`

Function trace:
- Function: `0x800EDA84`
  - Passes `game +0x1F24` as argument via `A1`, hinting it is likely a substruct of game.
  - Return Address: `0x800EA1DC`
- Function: `0x800EA15C`
  - Return Address: `0x80167BBC`
- ...

#### Main Function Flow

Directly calls `0x8040C924` during:
- "OK! That feels good!" after song replay cutscene.
- Gormon dialogue.

Is index `0x0` and calls `0x8040B638` during:
- Walking around before talking to him and spawning stagelights.

Is index `0x1` and calls `0x8040B934` during:
- In dialogue asking for your help.

Is index `0x2` and calls `0x8040BA2C` during:
- Basically whenever the stagelights are setup?
- Song replay cutscene

Writes index in function `0x8040B330`, using argument passed via `A2`.
- Called at: `0x8040B67C` by function: `0x8040B638`
- Then uses index to call function pointer stored in array at: `0x8040CC8C`
- These functions are likely "setting up" for the function pointers called in actor main using the same index.

Setting up for index `0x1` calls: `0x8040B86C`

Tracking `0x2B0` fields:
- `00000000 00000000`: Before talking to Toto.
- `01000000 00000000`: Dialogue asking for help with sound check.
- `02000B00 00000000`: Instructing where to stand.
- `02000C00 00000000`: Song prompt, initial song playback.
- `02000D01 00000000`: Song playback (cutscene).
- `00000F01 00030000`: "Okay! That feels good!" dialogue.
- `00000F01 00020000`: Gormon dialogue.
- `00000F01 00010000`: After Gormon dialogue.

Fields:
- `0x2B0`: Index into function pointer array described above.
- `0x2B1`: Frame count used sometimes?
- `0x2B2`: Something related to camera?
- `0x2B3`: ???
- `0x2B4`: ???
- `0x2B5`: Id for post-song dialogue?

### Function `0x8040BA2C`

Function called via main while function index is 2.

Notes:
- This function calls `0x8040B330`, which updates the function index (updates it to 0).
- Usually branches to function end at `0x8040BA68`, meaning function at `0x8040C8B4` returns 0.
  - Doesn't branch only once to begin post-song cutscene.
- The first function this calls is `0x8040B4AC`, which simply animates Toto the actor?

### Function `0x8040C8B4`

Derefs `*(u8**)(actor +0x2B8)` to get index into function array at: `0x8040CDE4`.
- Calls this function, then updates the pointer at offset `0x2B8` using the result (relative).
- Result is relative, and will branch to function end if returns 0 (which indicates not changing state?).

If updating the field at `0x2B8`, calls function afterwards: `0x8040C87C`.
- Uses same field to get index into function array at: `0x8040CD9C`, and calls it.

### Function `0x8040C450`

Called after `0x2B8` index is `0xC`, setting up for the formal song playback.

- References a 3-day cycle flag at `0x801F05A0`.
  - Or: `*(u8*)(file +0xF30)`
- Gets player form from `0x801EF690`.
  - Or: `*(u8*)(file +0x20)`

Enters loop of spawning actors for formal song playback cutscene (spawns actor by calling function `0x800BAC60`).

### Function `0x8040C670`

Called to check if actor cutscene state `0xD` should be advanced.

If certain branches are taken, will not update state:
- `0x8040C6A4` (will always branch if branch `0x8040C68C` is taken)
  - Branch `0x8040C68C` checks if field `0x2B1` (frame counter) is non-0.
- `0x8040C6B4`
  - Branch if function returns non-0: `0x801A2DE0(0x54, game)`

### Function `0x801A2DE0`

Loads `0x801D6700 + (A0 & 0xFF)` (`[0x54] == 2`)
- Calls `0x801A8A50(1, 1)`

Behavior seems to rely on setup performed by `0x8040C614`, while calls: `0x801A31EC(0x54, 4, song_flags ^ 0xF)`
- The `song_flags ^ 0xF` likely specifies which instruments from the song to play.

Example call: `0x801A31EC(0x54, 0x4, 0xE)`
- Calls: `0x801A89A8(0x7104000E)`
- Calls: `0x801A3098(0x54)` (documented by DB as `set_bgm_2`)

## Function `0x801A8A50`

```c
u16 func_0x801A8A50(u32 arg0, a32 arg1) {
  u8 *p = (u8*)0x80200140 + (arg0 * 0x21C);
  u8 t8 = *(p +0x210);
  if (t8 == 1) {
    u32 v0 = *(u32*)(p +0x1FC);
    return (u16)(v0 & 0xFF);
  }
  u16 a0 = *(u16*)(p +0x20A);
  if (a0 == 0xFFFF) {
    return 0xFFFF;
  } else {
    return a0;
  }
}
```

### BGM Frame Counter

#### Oops

Frame counter used while playing BGM: `0x80205240`
- Written to at: `0x8019A258`
- Writes the value returned from function call to `0x80197538`.
  - `0x80197538(0x80205230, 0x802052A8, 0xFD, 1);`
- Also see: `0x802050D0`
  - This is likely the preceding struct, each of size `0x160`.
  - `Struct[0] = 0x802050D0`
  - `Struct[1] = 0x80205230`
- Thus, is field of struct at offset `0x10`.
- Oops this is a different field! The frame count is `0x12`.

### Helper Function `0x8040BC9C`

- Calls function `0x800F20B8` using current "actor cutscene index" to get the next index.
- Calls function `0x800F1BA4` to write updated actor cutscene index to bit array (input is bit index).
- Calls function `0x800F1FBC` with updated actor cutscene index.

Or, according to the zeldaret MM project:
- Calls `s16 ActorCutscene_GetAdditionalCutscene(s16 index); // func_800F20B8`
  - Stores new index in actor offset `0x2B2`.
- Calls `void ActorCutscene_SetIntentToPlay(s16 index); // func_800F1BA4`
  - Uses new index.
- Calls `s16 ActorCutscene_Stop(s16 index); // func_800F1FBC`
  - Uses previous index.
- Return 0.

### Update Cutscene Function `0x8040BCEC`

- Calls `s16 ActorCutscene_GetCanPlayNext(s16 index); // func_800F1BE4`
  - If returns 0, calls `void ActorCutscene_SetIntentToPlay(s16 index); // func_800F1BA4`
    - Return 0.
  - Else, calls `s16 ActorCutscene_StartAndSetUnkLinkFields(s16 index, Actor* actor); // func_800F1C68`
    - Return 1.

### Field `0x2B8`

| Ptr Value    | Index  | Frames | Notes
| ------------ | ------ | ------ | ------------------------------------------------------------------------------------
| `0x8040CCA4` | `0x00` | `0x00` | Before talking to Toto.
| `0x8040CCA8` | `0x02` | `0x01` | Idling?
| `0x8040CCB4` | `0x04` | `0x00` | "Aww, that's too bad" while leaving stage.
| `0x8040CCF8` | `0x05` | `0x00` | Transition to `0x8040CCFC`, update camera (status `0xB`).
| `0x8040CCFC` | `0x06` | `0x14` | Transition to `0x8040CD00`.
| `0x8040CD00` | `0x07` | `0x00` | Instructing about spotlight.
| `0x8040CD04` | `0x08` | `0x09` | Finding spotlight, update camera (status `0xB`, via function `0x8040C1A0`).
| `0x8040CD08` | `0x09` | `0x0A` | Transition to `0x8040CD0C`.
| `0x8040CD0C` | `0x01` | `0x00` | Under correct spotlight, instructing to play ocarina.
| `0x8040CD10` | `0x0A` | `0x00` | Transition to `0x8040CD14`, update camera (status `0xC`).
| `0x8040CD14` | `0x0B` | `0x00` | Play song prompt, initial song playback.
| `0x8040CD18` | `0x0C` | `0x00` | Transition to `0x8040CD1C`, update camera (status `0xD`).
| `0x8040CD1C` | `0x0D` | `0x00` | Formal song playback.
| `0x8040CD20` | `0x0F` | `0x00` | Transition to `0x8040CD24`, update camera (status `0xF`).
| `0x8040CD24` | `0x11` | `0x01` | "OK! That feels good!" dialogue, Gormon dialogue.

### Field `0x2B2`

Updated by function:
- Called via function pointer in function `0x8040C87C`.
- To get index: Deref pointer at offset `0x2B8` as byte, use as index to function array at `0x8040CD9C`.

Pseudo-code for getting index:

```c
u8 *p = *(u8**)(actor +0x2B8);
u8 index = *p;
void *func = (void**)(0x8040CD9C)[index];
```

Function `0x8040C87C` is called at `0x8040C900`, right after updating field at `0x2B8`.
- Updates based on an index relative to the current value? And branches over if value is 0 (no change).
- Calls function in array at `0x8040CDE4` to get relative index.
  - Uses same `0x2B8`-derefed index to get function in array.

### Field `0x2B3`

Used to store flags for each form which has played the song. This is also stored in `0x801F05A0`.
- Link  = `0x1`
- Deku  = `0x2`
- Zora  = `0x4`
- Goron = `0x8`

In actor field, stores in lower bits. But uses higher bits in global field. For example:
- Global field `0x10` indicates actor field `0x1`.

This field is updated in the "initial function" for state `0xC`.

## Actor `Dm_Char07` - Milk Bar Stage (Cutscenes)

Relevant Spectrum output:

```
40D360:40D9F0 AF 0199:  0000 02 FILE: 00F14430:00F14AC0 INIT 8040D990:00F14A60
```

Actor main: `0x8040D46C`
Actor draw: `0x8040D490`

Main function only calls function pointer at actor offset `0x2A8`.
- This seems to always be `0x8040D45C`, which does literally nothing.
- This actor is likely only for drawing the stage + stagelights?

## Song Replay Message States

- `0x1C`: Song prompt message box.
- `0x1D`: Immediately after song played, notes glow.
- `0x05`: After notes glow
- `0x12`
- `0x06`
- `0x13`
- `0x14`
- song replay
- `0x43`
- `0x00`

### Handlers

Referenced fields:
- Index: `*(u8*)(msgbox +0x1F22)`
- State2: `*(u8*)(msgbox +0x1F0A)`
- Frames: `*(u8*)(msgbox +0x2023)`

- Index `0x1D`: `0x80154EE8`
  - On final frame:
    - Calls `0x80151938`
      - This function writes `[0x1F22] = 5`
    - `[0x1F22] = 0x12`
    - `[0x1F0A] = 3`
    - `[0x2023] = 1`
- Index `0x14`: `0x801555FC`
  - Last bit:
    - `[0x801DFC98 + V1 - 1] = V0`
      - Where: `V0 = song_ctxt_bytes[0], V1 = song_ctxt_bytes[2]`
    - `[0x2048] = V0`
    - `[0x801DFC98 + song_ctxt_bytes[2]] = 0xFF` (sets pseudo null-terminator?)
    - `[0x801C6A74] += 1`
      - Likely a frame counter for song playback?
    - Calls `0x80153E7C`

### But what writes index `0x43`?

Writes index value `0x43` during function call to `0x801477B4`.
- Address: `0x80155660`

This segment at address `0x80155658` does:
- Calls `0x8019C300(0)` (restore dampened sound!)
- Calls `0x801477B4(game)`
- `*(s16*)(game +0x16932) = 4`
  - This seems to restore player control!
  - MessageContext offset `0x1202A`
  - Absolute: `0x803FD452`

Assembly:

```
lui   at, 0x0001
addu  at, at, s2
addiu t7, r0, 0x0004
sh    t7, 0x6932 (at)
```

## Old Notes

### Text Good

Loading initial message using function: `0x80150D08`
Function: `0x80150D08`
- Return Address: `0x801518DC`
Function: `0x801518B0`
- Return Address: `0x806F5048`
Function: `0x806F4FF0`
- Return Address: `0x8070AC9C`
Function: `0x8070AC00`
- Return Address: `0x80702F78`

### Text Blah

Writes message box text: `0x8009026C`
Function: `0x800900C0`
- Return Address: `0x8008C594`
Function: `0x8008C260`
- This function does not return, infinite loop.
