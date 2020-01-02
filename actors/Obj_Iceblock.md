Obj_Iceblock
============

- Actor Id: `0x143`
- Actor File VRAM: `0x80A13090`

## Push Speed

Spectrum output:
- File: 0x80423940

```
40D3A0:40D658 AI 0143:  1 02 0 0000 ( 1485.0  -360.0  2325.0) 0000 0000 0000
...
423940:427DD0 AF 0143:  0000 01 FILE: 00E8CC00:00E91090 INIT 804276E0:00E909A0
```

Field at `actor +0x148`:
- Function `0x80425CCC`: sets to 0
- `0x800B7314`: adds value to field
  - Function: `0x800B72F8(z2_actor_t *actor, f32 amount, s16 field_0x150)`
  - Return: `0x80734ED0` (note: for this address, heap ends at `0x80750000`)

Function `0x80425CCC` modifies `actor +0x148`.

### Other Field

Field at `actor +0x24` (position data):
- Written to at `0x800FF080`
  - Function: `0x800FF03C`
  - Return: `0x80426798`
  - Return Function: `0x80426700`
    - Offset: `0x2DC0`
- Seems to use fields `actor +0x264, actor +0x268`
- Function also references:
  - `0x80427928` -> `0x44088889` (`546.13336`) (???)
  - `0x8042792C` -> `0x40333333` (`2.8`) (maximum velocity)
  - `0x80427930` -> `0x3F99999A` (`1.2`) (initial velocity)

However, the maximum velocity is clamped by the constant loaded at `0x8042674C`:
- `lui at, 0x4060` -> `0x40600000`, or `3.5`

## Velocity Notes

From some re-examination:
- Function call to `0x800FED84`: this function is `sinS_to_F` according to DB's notes.
- This is likely using `sin` for a "speed up, then slow down" for the push/pull velocity.
- `F6` is the initial velocity.
- `F18` is the additive velocity that gets multiplied by the result of `sin`.
- `F12` is a clamp on the resulting (final) value.

```c
float F12 = 3.5      // Clamp (maximum resulting value)
float F6 = 1.2;      // Initial
float F18 = 2.8;     // Additive
float F0 = sin(x);
float F4 = F0 * F18; // Multiply additive velocity by sin result
float F2 = F4 + F6;  // Add result to initial velocity
if (F12 < F2) {      // Clamp to roof value
    F0 = F12;
} else {
    F0 = F2;
}
```
