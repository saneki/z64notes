Song Textbox Skip
=================

Messagebox context: `0x803E6B20 +0x14908`
- Absolute: `0x803FB428`
- Main data starts at `0x1F00`: `0x803FD328`

## Stored Song Id Function

Function to get stored song Id to write to RDRAM: `0x8019AFE8`
- Caller function: `0x8019CE6C`

```c
// Function: 0x8019AFE8
u8 get_next_stored_song_id() {
    u8 value = *(u8*)0x801D8528;
    if (value != 0) {
        return (value - 1) & 0xFF;
    }

    if (*(u32*)0x801D6FEC != 0) {
        return 0xFE;
    } else {
        return 0xFF;
    }
}
```

### Byte at `0x801D8528`

Setting this byte while idling with Ocarina triggers a song's playback.
Writes stored song value (+1?) at: `0x8019BE54`.


After reading stored song (`0x3`, Elegy) at `0x801FD43A`, reads value from:
- `0x8019CF80`
- `0x80154A58`
  - Writes value to: `*(s16*)(0x803E6B20 +0x12028)`
- `0x80154A6C`
  - Uses in conditionals.
- `0x80154B2C`
  - Writes value to: `*(s16*)(0x803E6B20 +0x1202E)`
- `0x80154B48`
  - Writes value to: `*(s16*)(0x803E6B20 +0x12028)`
- [song textbox spawns]

## Playback Boolean

Byte is `1` when doing song playback: `0x801FD43F`
- Writes value at: `*(u8*)0x8019CF04`
- Retrieves value from: `*(u8*)0x801D6FE0`

Locking this value to `0` prevents the *visible* song playback to some extent.
- Song playbox textbox still spawns (but empty?).
- Audio playback is unaffected.
- Visual effect is unaffected.
- Still presents message box from after song.

Where is `0x801D6FE0` written from?
- Writes `1` at: `0x8019C500`

Calls function `0x8019C398`
- Called by: `0x80155248`
- Function is only called once (while initializing playback?)
- Arguments:
  - `A0` = `4`
  - `A1` = `1`
- Branches:
  - `0xC3B8 -> 0xC3D8`: Branches
  - `0xC3DC`: No branch
  - `0xC430 -> 0xC46C`: Branches
  - `0xC470 -> 0xC4F8`: Branches
  - `0xC500`

## Very Large Ocarina Processing Function?

Function: `0x801541D4`
- Does initial check of `*(u32*)(0x803E6B20 +0x14908 +0x1F10) != 0`

This field at `+0x1F10` is likely the ocarina action state Id?

For example, while playing Elegy, it goes in order of:
- `0x20`: Ocarina resting state.
- `0x0C`: Song playback.
- `0x30`: Finish song playback with song name in message box.
- `0x3C`: Show Elegy result prompt (can't use in this area).

When transitioning from `0x20` to `0x0C`, writes value `0x0C` at: `0x8015124C`
- Value is in `T7`, retrieved from (not guaranteed): `*(u32*)(0x803FB590 +0x1D84)`
  - `0x803FD314`

Apparently this value is actually some difference involving the values of a specific table of structs.
- Struct table at: `0x801C6B98`
- See: `0x80158908`

The pointer into this table is retrieved from: `*(void**)(0x803E6B20 +0x1698C)`
- Absolute value: `0x803FD4AC`
- This points to the start of the table, `0x801C6B98`.
- It then iterates through the table until it finds a specific value in the first `s16` of the struct.
  - Basically whatever is in `A3`.

Gets difference of: `cur[i + 1].field_4 - cur[i].field_4`

Stores at:
- `*(u32*)(0x803E6B20 +0x14A70 +0x1D80)`
- `*(u32*)(0x803E6B20 +0x14A70 +0x1D84)`

When standing with Ocarina, key is `0x1B5A`.

## Messagebox Function

Function `0x80150D08` is called whenever messagebox changes state when using ocarina.

This includes when Link pulls out the Ocarina, which involves messagebox state for some reason.

Message box Ids:
- `0x1B5A`: Pulling out ocarina.
- `0x1B5B`: Song playback.
  - Return: `0x80151964`
- `0x1B75`: Show song completed message for Elegy.
  - Return: `0x80151964`
- `0x1B95`: Show "Your notes echoed far..." message.
  - Return: `0x801518DC`
    - Return Function: `0x801518B0`
  - Return: `0x801554F4`
    - This calls the wrapper function with the hardcoded `0x1B95` Id.

To show the "bad Elegy" message, checks if `*(s16*)(0x803E6B20 +0xA4)` is not a bunch of hardcoded Ids.
- Absolute: `0x803E6BC4`
- This is a bunch of hardcoded checks for specific scene Ids that Elegy can be used in!
  - See: `0x80155464`

Elegy of Emptiness processing likely begins at `0x801553FC`.
- The question is, how did the code jump here?
- Probably jumping using table earlier in function.
  - Likely jumping at `0x801543A4`, using jump table at `0x801DF3CC`.
  - In this case, using offset of `0x5C`, and thus an index of `0x17`.
  - Is loading index from `*(u8*)(0x803FB428 +0x1F22)`
    - Or: `*(u8*)(0x803E6B20 +0x14908 +0x1F22)`
    - Absolute: `0x803FD34A`

- Writes `0x12` to field at: `0x80154CD4`
- Writes `0x16` to field at: `0x80155350`
- Writes `0x17` to field at: `0x801553A0`
  - Code jumps to: `0x80155378`

Experiment with writing `0x17` instead of `0x12`:
- Takes a "bad branch" at `0x80155444`.
- To resolve this, make sure: `*(u16*)(0x803FB428 +0x202C) == 0x32`

Notes:
- Function `0x801518B0`: Seems to be a wrapper-like function for `0x80150D08`?

When playing Elegy, jump indexes change as follows:
- 0x0D
- 0x0E
- 0x05
- 0x12
- [a few frames pass]
- 0x06
- 0x13
- 0x14
- [song playback]
- 0x15
- 0x05
- 0x06
- 0x16
- [shows "You played the Elegy of Emptiness" for a few frames]
- 0x17
- 0x18
- 0x43
- 0x01
- 0x02
- 0x03
- 0x04
- 0x06
- 0x42
- [shows "Your notes echoed far..." message]
- 0x43
- 0x00

When playing Sonata:
- Does the same, but after first `0x43`, sets to `0x00` and stops.

## Test Implementation:

- `0x80154CD0`: Set next index to `0x18` instead of `0x12`.
- `0x80154CF0`: Lower frame countdown value to `0x2` instead of `0xA`.
- `0x80155444`: NOP out check for `*(u16*)(game->msgbox_ctxt +0x202C) == 0x32`

However, when attempting this, sound effects remain semi-muted until pulling out the Ocarina again.
- When setting to `0x17` instead of `0x18`, this side effect does not occur!
- After some investigation, this is likely because when handling `0x17`, a function is called which restores the volume of sound effects.
  - Specifically: `0x8019C300(0)`

Notes:
- The code that sets index `0x12` is actually when processing index `0xD`.
  - Code range: `[0x801549AC, 0x80154E60)`

## Song Effect Byte

When Elegy succeeds, writes: `*(u16*)(0x803E6B20 +0x14908 +0x202A) = 3`
- Absolute: `*(u16*)0x803FD452 = 3`

This byte is next read at:
- `0x8076FBF4`
  - This function specifically checks for Elegy (`3`) at `0x8076FE80`.
  - Elegy-specific code begins at `0x8076FE88`
  - Call to function `0x8074EBF0` seems to be what spawns statue and overwrite song effect?
    - `0x8074EBF0(game, link, 0x80772F0C, 0)`
    - `A2` (`0x80772F0C` in this case) points to a function.
- `0x8042CA94` (`Obj_Wturn`, or "Stone Tower Temple Inverter", see Spectrum output below)
- `0x80157C28`

Relevant Spectrum output:

```
42CA40:42CF40 AF 0027:  0000 01 FILE: 00D21B40:00D22040 INIT 8042CEB0:00D21FB0
42CF50:42D09C AI 0027:  7 00 0 0014 (    8.0   -70.0  1165.0) 0000 C000 0000
```

## Function `0x80772F0C`

This is the upper-most function for performing the statue spawn for Elegy.
It mostly just seems to lock input and count frames up to `0x5B`, and on frame `0x0A` calls another function which does the actual statue spawn: `0x80765AD0`

This function also seems to handle the effects which happen while spawning the Statue:
- Surrounding area darkens.
- HUD disappears and isn't usable.
- Certain events don't happen until it's over.
  - Standing on Stone Tower buttons don't cause platform mini-cutscene.

### Camera

The camera is caused by field: `*(s16*)(camera +0x140)`.

This value is written to by tiny function: `0x800DE308`
- It seems to mainly be called at: `0x801695E8`, using the value in `A1`.
- Function: `0x80169590`

Function `0x80169590`:
- Probable signature: `0x80169590(z2_game_t *game, u32 camera_index, s16 camera_value)`
- New camera field value is passed via `A2`, camera index is likely `A1`.

When setting value `1` for camera index `0`, is called by: `0x800F1EFC`
- Function: `0x800F1D84`
- Uses fields:
  - Gets game pointer from: `*(void**)(0x801BD8B0 +0x10)`
  - Gets camera index from: `*(s16*)(0x801BD8B0 +0x14)`
  - Uses hardcoded field value of `1`, so whatever is calling this is probably important.
- This function is being called by `0x80406E60`, code for actor `0x160` ("Camera Refocuser").

The Elegy statue function is likely spawning the Camera Refocuser actor using function `0x800BAC60`.

Relevant Spectrum output:

```
406B90:4070B0 AF 0160:  0000 01 FILE: 00EB5F70:00EB6490 INIT 80407000:00EB63E0
4070C0:40728C AI 0160:  7 00 0 0024 (  140.2  -560.0  3162.1) 0000 0000 0000
```

## Spawning

The statue spawning function at `0x80765AD0` is capable of spawning two actor types:
- At `0x80765B68`: Spawns actor type `0x21`, the Elegy statue itself.
  - This only gets called if the specific statue does not already exist. If it does, the statue fades out and moves before fading back in.
- At `0x80765BE4`: Spawns actor type `0x160`, the "Camera Refocuser" actor.
  - This also handles the HUD changes, and visual effect during the statue spawn/move.

Checks for existing statue actor: `(void**)(0x803E6B20 +0x1EF4)[form_index]`

Fade in likely has something to do with Elegy statue actor field bytes at `0x190` and `0x191`.

### Fields

Decrements counter at offset `0x192`, from `0xFF`: `0x8042CD8C`
- Actor file offset: `0x25C`
- Calls: `0x800FEF2C((s16*)(actor +0x192), 0xFF, 8)`
- This decrements value by 8, returns `1` if reached `0`?
- This same function call is also used to grow the value!

Before moving statue, first decrements counter at offset `0x191` at: `0x8042CCB0`
- This is set to its initial value of `0x14` in the player function at: `0x80765B28`

Relevant Spectrum output:

```
42CB30:42CFF0 AF 0021:  0000 01 FILE: 00D1D3C0:00D1D880 INIT 8042CF30:00D1D7C0
42D000:42D194 AI 0021:  7 00 0 0001 (  150.2  -560.0  2980.4) 0000 8DBF 0000
```

## Camera Refocuser

Functions:
- Actor main: `0x8043199C`
- Actor draw: `0x804319C0`

Actor main calls function pointer at offset `actor +0x1C8`, which seems to always be: `0x804317DC`
- This pointer is written by init at: `0x804316C8`

```
4316A0:431BC0 AF 0160:  0000 01 FILE: 00EB5F70:00EB6490 INIT 80431B10:00EB63E0
431BD0:431D9C AI 0160:  7 00 0 0012 (  129.0  -560.0  3096.1) 0000 0000 0000
```

## Elegy Speedup Patch Notes

`0x80765B1C`: Update pre-despawn frame count value from `0x14` to `0x1`.
`Eff_Change +0x2A4`: Remove call to `0x800FD2B4`, which darkens the scene.
`0x80431970`: Remove call to `0x800F1D84`, which modifies the camera.
- Relative to actor file (`Eff_Change`): `0x2D0`
`En_Torch2 +0x25C`: Increase fade speed of statue from `0x8` to `0x20`.

Actor VRAM/VROM values:
- `En_Torch2` (Elegy Statue):
  - VRAM: `0x808A31B0`
  - VROM: `0x00D1D3C0`
  - File offset of entry: `0x1A910`
  - File index: `65`
- `Eff_Change`:
  - VRAM: `0x80A4C490`
  - VROM: `0x00EB5F70`
  - File offset of entry: `0x1B8E0`
  - File index: `318`
