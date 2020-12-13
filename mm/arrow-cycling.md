Arrow Cycling
=============

## `En_Arrow` Overlay

Example dump of info in table:

```
00D04460 00D06730 8088A240 8088C510
80508CA0 8088C1C0 00000000 00020200
```

VRAM: `[0x8088A240, 0x8088C510)`
Init: `0x8088C1C0` (offset: `0x1F80`)

## Spawning Arrows

Spawns arrow actors using the function at `0x800BAE14`.
- Return: `0x800BB130`
  - Return Function: `0x800BB0C0`
  - This is just another wrapper function around the actor spawn function.
- Return: `0x8074DD28`
  - Return Function: `0x8074DB88`
  - Called once when bringing out bow/hookshot, and once again when pulling back bow string or preparing hookshot to fire.
- Return: `0x807663B8`
  - Return Function: `0x807662DC`
  - Called via function pointer: `link +0xAC4`
  - This is the function pointer used when bow or hookshot are out and being used.
- Return: `0x8074F704`

- Calls function `0x8074DA4C` to determine which actor variable to use for the spawned arrow.
  - `0x8074DA4C(z2_game_t *game, z2_link_t *link, u32 *unknown, u32 *arrow_var)`
- Gets magic from `*(s8*)0x801EF6A9`, and amount of magic required from arrow at `*(u8*)0x8077A448`.
  - Uses `arrow_var - 3` as index into table.
  - If not enough magic, updates `arrow_var` to 2 (normal).

## Arrow Actor Data

Some fields to note:
- `0x120`: Pointer to Link while in bow (before firing).

## Special Arrow Actors

The effects for fire, ice and light arrows have their own actors:
- `0x7D` = `Arrow_Fire`
- `0x7E` = `Arrow_Ice`
- `0x7F` = `Arrow_Light`

Spectrum output:

```
54BA70:54DD40 AF 000F:  0002 01 FILE: 00D04460:00D06730 INIT 8054D9F0:00D063E0
```

This special actor is also spawned by a call to `0x800BB0C0` by the `En_Arrow` actor.
- Calls at: `0x8054D048`
  - Function which performs call: `0x8054CF50`, actor file offset: `0x14E0`
  - This the main processing function for the `En_Arrow` actor.

## Arrow Main Function

The arrow main function is what spawns the special arrow actor.

It does so if:
- Actor variable is in range `[3, 6)`, as expected.

## Pointers to Pointers

When a special arrow is prepared in the bow, the following pointers are set:
- `link->attached_b` -> `En_Arrow` actor instance.
- `arrow->attached_a` -> `z2_link_t` actor instance.
- `arrow->attached_b` -> special arrow actor instance.
- `special->attached_a` -> `En_Arrow` actor instance.

### Destructing

- Return: `0x800B6974`
  - Return Function: `0x800B6948`
  - This function just checks if `actor->ctor == 0 && actor->dtor != 0` before calling `dtor`.
- Return: `0x800BB548`
  - Return Function: `0x800BB498`
  - Prototype: `0x800BB498(z2_actor_ctxt_t *ctxt, z2_actor_t *actor, z2_game_t *game)`
- Return: `0x800B9554`
  - Return Function: `0x800B948C`
- Return: `0x800B9898`

## "Denied" Sound Effect

A sound effect is played when an arrow is "denied," if you try to use an elemental arrow while an
existing elemental arrow's effect is still visible/active.

Trace sfx function `0x8019F0C8`:
- Return: `0x8074DBD4`
  - Return Function: `0x8074DB88`
- Checks if `*(s16*)0x801F3598 != 0`, and if so plays the sound effect `0x4806`.

Value write breakpoints:
- Clears (writes `0`) at: `0x80115DA8`
  - This is only hit once after special arrow actor is deconstructed (presumably).
- Writes `1` at: `0x80115E8C`
  - Function: `0x8011????(z2_game_t *game, u8 magic_required, u32 zero)`
  - Return: `0x8074DD50`
    - Return Function: `0x8074DB88`
    - Same function that plays sound effect *and* spawns the arrow actor.
    - Thus it probably isn't being called again because we aren't spawning a new arrow actor.
- Writes `2` at: `0x80116484`
- Writes `3` at: `0x801164E0`
- Writes `0` every frame otherwise: `0x80116904`

## Arrow Trail Color

Each arrow type has its own trail color. At first I thought it was due to a field in the `En_Arrow`
actor which differs depending on the type of arrow it is.

Possible values for field `*(u32*)0x1C0`:
- Normal: `0x00000020`
- Fire:   `0x00000800`
- Ice:    `0x00001000`
- Light:  `0x00002000`

However, changing this field does not appear to change the trail color.

## Arrow Draw

Arrow trail color is written to DList at: `0x800AA8F4`
- Gets 4 color bytes starting from: `0x801E54D0 +0x1A2`.
  - Absolute: `0x801E5672`
- Function: `0x800AA700`
  - Return: `0x800AB0BC`
- Function: `0x800AABE0`
  - Return: `0x800AB590`

Copies over some data around `0x800A875C`, for example: from `0x8050AC94` -> `0x801E54D0`.
- That is copying from the `En_Arrow` actor file.

Spectrum output for `En_Arrow` actor file:

```
508CA0:50AF70 AF 000F:  0002 02 FILE: 00D04460:00D06730 INIT 8050AC20:00D063E0
```

### Draw Data Copy Trace

Trace:
- Function: `0x800A8720`
  - Return: `0x800AFAF8`
  - Called by function pointer.
- Function: `0x800AF960`
  - Return: `0x80508DA4`
  - Actor file code for `En_Arrow`.
- Function: `0x80508CA0`
  - Constructor function for `En_Arrow`.
  - Thus, it is copying color data (and more?) somewhere during constructor only.

The `En_Arrow` constructor makes 4 calls to `0x80508CA0` depending on the actor variable:
- One for `var < 3`  (Normal Arrow)
- One for `var == 3` (Fire Arrow)
- One for `var == 4` (Ice Arrow)
- One for `var == 5` (Light Arrow)

## Magic Consumption

When switching from normal arrows -> elemental arrows, game code automatically consumes magic at:
- Address: `0x801164AC`
  - Function: `0x80116348`
- Return: `0x80121B28`

Uses field at `*(s16*)(0x801EF670 +0x3F32)`.
- Absolute: `0x801F35A2`

The function uses an address table `0x801EDB78` for branching into itself.
- Uses index: `*(s16*)(0x801EF670 +0x3F28) - 1`
  - Absolute: `0x801F3598`
  - Consumes magic if this field is `2`, and thus the index is `1`.
  - This is the same field used to check if arrow effect is still active!

### Visible Consumption Ideas

- Update arrow actor to set magic consume state to 4 instead of 1.
- Check if arrow leaving (not attached to link, has velocity), if so set flag.
- Next frame, if flag is set: update magic consume state to 2.

## Arrow Draw (Old Notes)

Instructions called during normal arrow draw:

(Segment `0x04` = `0x8059A540`)

```
DE000000 801C13A0
DA380003 80228508
DE000000 04013FF0 // Calls: 0x805AE530
```

This DList, however, doesn't seem to affect the arrow trail color:

```
E7000000 00000000 E3001001 00000000
D7000002 FFFFFFFF FD100000 040128D0
F5100000 0701C040 E6000000 00000000
F3000000 077FF200 E7000000 00000000
F5100800 0001C040 F2000000 0003C1FC
FC127E03 FFFFFDF8 E200001C C8112078
D9F3FFFF 00000000 D9FFFFFF 00030400
FA000000 FFFFFFFF 01012024 04013CD0
06000204 00000602 06080600 00080A06
060C0402 000C0E04 06101214 00101612
060C100E 000C1610 0608120A 00081412
06181A1C 00181E1A 0618201E 00182220
E7000000 00000000 FD100000 040138D0
F5100000 07050150 E6000000 00000000
F3000000 071FF100 E7000000 00000000
F5101000 00050150 F2000000 0007C03C
FC127E03 FFFFF3F8 E200001C C8113078
D9FFFBFF 00000000 01008010 04013DF0
06000204 00000406 06080A0C 00080E0A
E7000000 00000000 D7000002 07D009C4
FD100000 0400CA30 F5100000 07054551
E6000000 00000000 F3000000 073FF100
E7000000 00000000 F5101000 00054551
F2000000 0007C07C FC127E03 FFFFFDF8
E200001C C8112078 D9FFFFFF 000C0400
FA000000 FFFFFFFF 01003006 04013E70
05000204 00000000 0101502A 04013EA0
06000204 0006080A 060C0A08 000E1012
06141618 001A1C0C 060A1A06 001E2022
05242628 00000000 DF000000 00000000
```

With green trail (but still does not draw trail):

```
DE000000 801C13A0
DA380003 80248978
DE000000 04014370 // Calls: 0x805AE8B0
```

```
E7000000 00000000 E3001001 00000000
D7000002 07D009C4 FD100000 0400CA30
F5100000 07054551 E6000000 00000000
F3000000 073FF100 E7000000 00000000
F5101000 00054551 F2000000 0007C07C
FC127E03 FFFFFDF8 E200001C C8112078
D9FFFFFF 000F0400 FA000000 FFFFFFFF
01003006 040141D0 05000204 00000000
01009012 04014200 06000204 0006080A
050C0E10 00000000 E7000000 00000000
D7000002 FFFFFFFF FD100000 040138D0
F5100000 07050150 E6000000 00000000
F3000000 071FF100 E7000000 00000000
F5101000 00050150 F2000000 0007C03C
FC127E03 FFFFF3F8 E200001C C8113078
D9F3FBFF 00000000 FA000000 FFFFFFFF
01004008 04014290 06000204 00000602
01004008 040142D0 06000204 00000602
E7000000 00000000 FD100000 040128D0
F5100000 0701C040 E6000000 00000000
F3000000 077FF200 E7000000 00000000
F5100800 0001C040 F2000000 0003C1FC
FC127E03 FFFFFDF8 E200001C C8112078
D9FFFFFF 00000400 0100600C 04014310
06000204 00000602 06080A00 000A0600
06040A08 0004020A DF000000 00000000
```
