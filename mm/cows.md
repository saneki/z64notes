Cows
====

## Epona's Song and the Milk Messagebox

Debugging in: Termina Field grotto (near Southern Swamp entrance).

Cow actor file:

```
415040:416530 AF 00F3:  0000 04 FILE: 00E0F010:00E10500 INIT 804163A0:00E10370
```

Overlay pointer thing: `0x804163A0`

### Tracing from Message Function

Breaking on `show_message` at `0x801518B0`:
- Return: `0x80755048`
  - Return Function: `0x80754FF0`
- Return: `0x8076AC9C`
  - Called from function pointer.
    - Function from: `*(z2_link +0xD58)`
      - Absolute: `0x80400B08`
  - Return Function: `0x8076AC00`
- Return: `0x80762F78`
  - Called from function pointer.
    - Function from: `*(z2_link +0x748)`
      - Absolute: `0x804004F8`
  - Return Function: `0x80762388`
  - Large function.

Function pointer `z2_link +0xD58`:
- Written to at: `0x8074F99C`
  - Function: `0x8074F97C(z2_game_t *game, z2_link_t *link, void *func, u32 unknown)`
  - Return: `0x8074F9F8`
    - Return Function: `0x8074F9E8`
      - This seems to be used when setting NPC messageboxes.
  - Return: `0x80778B10`
    - Function: `0x807788F0`
    - Branches to this code if `*(u8*)(link +0x147) != 2`
      - Absolute: `0x803FFEF7`
    - This function itself is not called per frame.

### Debugging Distance from Link (X, Z positions)

Field: `*(f32*)(actor +0x98)`

Breaks on: `0x80415E74`
- Function: `0x80415D5C`
- Return: `0x80416248`
  - Return Function: `0x80416170`
  - This is the main function!
  - Specifically from the function pointer call at the end.
  - Gets from actor field: `*(void**)(actor +0x274)`

This checks if the "distance from Link" field is less than `150.0`, and if so does extra things.

## Tracing From Empty Bottle Check

Note: Uses cow actor pointer: `0x80416540`

Checks for empty bottle: `0x80114EB0`
- Return: `0x80415A58`
  - Function: `0x80415A18`
  - Called as function pointer from `*(void**)(actor +0x274)`.
    - Absolute: `0x804167B4`
  - This is an `En_Cow` function!
  - If not full: `0x8041597C`
  - If full: `0x80415858`

Sets function pointer to `0x80415A18` at function: `0x80415AA8`
- Checks if `*(u16*)(actor +0x116) == 0x32C8`
- Absolute: `0x80416656`

Writes `0x80415AA8` to function pointer after Epona's Song at: `0x80415C14`.
- Function: `0x80415B50`
- Return: `0x80416038`
  - This is the actor's main function, calling the function pointer.

### Checks before function pointer

This performs the following checks/branches before changing the function pointer to give milk:
- Checks if `*(u16*)(game +0x16932) != 4`
  - Absolute: `0x803FD452‬`
- Checks if `*(u32*)(0x801BDAA4) != 0`
  - The value at this address is set to `1` for a short time after playing Epona's Song.
- Then checks `(*(u16*)(actor +0x26E) & 4) == 0`
- Then loads X/Z distance from Link, which is `*(f32*)(actor +0x98)` ...
  - ... and checks if less than `150.0`, similar to the other code which checked for distance.

Along with setting the function pointer to give milk, it also sets the global flag at `0x801BDAA4` back to `0`, to prevent other cows from also attempting to give milk.

### What writes the `0x80415B50` function pointer?

In scenes with cows, it always seems to load twice as many as are visible.
- Only the visible cows seem to use the function pointer `0x80415B50`.

It is set in the construct function at: `0x80415318`.
- However, only sets this if actor variable is `0` or `2`.

#### Old Notes / Ignore

Function call to `0x800B3BA4`:
- `func_0x800B3BA4(actor +0xBC, 0.0, 0x800B3FC0, 72.0)`

## Early Ranch Addresses

```
426840:427D30 AF 00F3:  0000 06 FILE: 00E0F010:00E10500 INIT 80427BA0:00E10370
```

Can-give-milk function: `0x80427350`
