Mods Files
==========

## Function `0x801449A4`

File: `update-chests`
Prototype: `void * 0x801449A4(u32 index)`

- Multiples `A0` (`index`) by 8 to get offset into `gi-table` for the specified entry.
- Calls function `0x801DC46C` to get PROM address of the `gi-table` file.
- Adds PROM address with `gi-table` offset and stores in `A0`.
- Loads address `0x800B35F0` for something (place to store loaded `gi-table` entry?).
- Subtracts `A0` by 8 (basically decrementing `index` used by 1).
- Calls `0x801DC434(u32 prom_addr, void *dest, 8)` and returns.
  - This is basically a wrapper function for a `bcopy`.
  - Thus, `0x800B35F0` is the global buffer being used to store the current `gi-table` entry data.

## Crash Investigation (Heart Piece)

Crash happens right after call to function `0x801449A4`, when `player_actor` calls function `0x800B3488`.
- Crash happens at beginning of function, address: `0x800B3494`
- Tries to deref `A0`, which is only the first byte of `gi-table` entry loaded previously.
- It turns out the function this is relying on is actually in `fix-item-checks`.

## Crash Investigation (Skulltula Token)

Crash happens during function call at: `0x80412EE8`
- Calls function: `0x801DC6DC`

Skulltula Token actor file:

```
412DF0:413210 AF 00E3:  0000 01 FILE: 00DFF7A0:00DFFBC0 INIT 80413130:00DFFAE0
```

### Nevermind this is wrong

Crash happens right after call to function `0x801449AC`, during function call to `0x801518B0`.
- Happens at: `0x801DC738`

In function `0x801518B0`, happens during function call at `0x801518D4`.
- Calls function: `0x80150D08`
- This is the `load_message` function as documented by DB.

In function `0x80150D08`, happens during function call at `0x8015126C`.
- Calls function: `0x80080C90`
- The called function is the `z2_ReadFile` function.

## Clock Town Heart Piece

Actor variable with `standing-hearts` applied: `0x8B`

## Green Rupee

- Seems to be graphic Id `0x50`.
- Get-Item function is `0x800EFAB8`.

### Wrong???

- Calls function `0x801DC46C` to get the offset of the `dmadata` entry for the `gi-table` file.
  - Offset is relative to `dmadata` start address.
  - Uses `gi-table` file index stored at `0x8014496C`.
