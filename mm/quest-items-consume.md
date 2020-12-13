Quest Items Consume
===================

## Ocean Title Deed

Spectrum output (Ikana Business Scrub):

```
43CCA0:440E50 AF 0274:  0000 01 FILE: 01051B70:01055D20 INIT 80440390:01055260
```

When giving the Ocean Title Deed to the scrub which consumes it:
- First calls item removal function `0x801149A0(0x2C, 5)`
  - Return: `0x8043D0DC` (offset `0x43C`).
  - Return Function: `0x8043D07C` (offset `0x3DC`).

Function at `0x8043D07C`:
- ...

## Moon's Tear Check

Spectrum output:

```
437FD0:43B430 AF 01BD:  0000 01 FILE: 00F40150:00F435B0 INIT 8043AB44:00F42CC4
43B440:43B7B8 AI 01BD:  4 00 0 07E2 ( -692.0    20.5  -348.0) 0000 5171 0000
```

Town Business Scrub is actually a different actor: `En_Sellnuts` (Id `0x01BD`).

It gives the item in the function: `0x80438DEC` (offset `0xE1C`).

### Function Pointers

Stores function pointer at offset `0x2D8`.

- Awaiting an item at prompt screen: `0x80438B24`
- Checking an incorrect item: `0x804382D8`
  - Set at: `0x80438BCC`
- Checking a correct item: `0x80438CB8`
  - Set at: `0x80438BA8`
  - Apparently checks against constant `0x2A` instead of `0x28`??
- Giving reward: `0x80438DEC`

## Inventory Clear (Song of Time)

Clears quest items using item removal function starting at: 0x80144390

## Checking Item to Receive

A function in `player_actor` checks when Link is receiving an item.
- Checks `*(s16*)(link +0x384)` for the get-item index.
- `0x803FFDB0 +0x384 == 0x80400134`
- Function used to set this value: `0x800B8A1C(z2_actor_t *actor, z2_game_t *game, s16 gi, f32 unknown)`

## Post Boxes

```
43E120:43EFE0 AF 01F2:  0000 02 FILE: 00F90B30:00F919F0 INIT 8043ED88:00F91798
43EFF0:43F210 AI 01F2:  6 00 0 0000 (  176.0   100.0  -945.0) 0000 C000 0000
43F220:43F440 AI 01F2:  6 00 0 0004 ( -616.0     0.0   321.0) 0000 4000 0000
```

Calls function to remove item (Letter to Kafei): `0x8010BC28(z2_actor_t *actor, z2_game_t *game, void **a2, void *a3)`
- Callchain:
  - Called via function pointer from: `0x8010C054`
    - Return Function: `0x8010BF58`
  - Return: `0x8043E76C`
    - Return Function: `0x8043E744`

This same function (`0x8010BC28`) is used to remove:
- Pendant when giving it to Anju.
- Letter to Kafei when giving it to a mailbox.
- Letter to Mama when giving it to the Postman.
- Letter to Mama when giving it to Madame Aroma.

## Toilet Hand

Spectrum output:

```
4179F0:418880 AF 027D:  0000 01 FILE: 01062260:010630F0 INIT 80418638:01062EA8
418890:418AEC AI 027D:  4 00 0 0000 (  107.0     4.0   -90.0) 0000 CEF4 0000
```

Calls remove function at: `0x80417B78` (offset `0x188`).
- Function: `0x80417B44`
- This is actually 1 of 6 different calls to remove item in this function, one for each acceptable item type.
  - 4 deeds, 2 letters.
