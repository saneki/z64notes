Stored Song
===========

`u16` at `0x801C6A7C`:
- Writes `0xFF` at: `0x80158130`
- Writes `0xFF` at: `0x80151FA8`
- Writes song at: `0x80154B1C`
  - Function: `0x801541D4`
  - Gets from instruction at: `0x80154A6C`
  - Reads byte at `(*(u8*)((0x803E6B20 +0x14908) +0x1F00))[1]`
    - Offset:  `(0x14908 + 0x1F00) = 0x16808‬`
    - Pointer: `(0x803E6B20 + 0x14908 + 0x1F00) = 0x803FD328`
    - Deref:   `0x801FD43A`
      - This seems to be a song/ocarina related structure.

If you change the stored song mid-song animation, it won't do whatever the song does.

Thus it probably checks the stored song again after the animation is over, to determine what happens.

Read breakpoint after song:
- `0x801579C8`
  - Function for both: `0x8015680C(z2_game_t *game)`
  - This function seems to be called per-frame.
- `0x80157DE8` (if is `0xFF` here, does not do song effect?)
  - This second usage may be specifically for songs with prompts?
  - Seems to be `if` statements in the following order:
    - `0x06`
    - `0x0C`
    - `0x0D` (Song of Double Time)
    - ...

Note: Song note count seems to be: `*(s16*)0x801C6A74`
- Counts from 1 to 8, then cycles back to 1.
- Write breakpoint: `0x80154A50`
  - Another referenced address in this block: `0x801CFC98`.
    - Seems to be a structure relating to the song notes.

## Structure At `0x801FD43A`

Function `0x8019CEC4` seems to copy stuff into this structure:
- `0x8019CEEC`: copies `[4]` from result of function call to: `0x8019B02C`
  - Current note being played during playback.
- `0x8019CF04`: copies `[5]` from: `*(u8*)0x801D6FE0`

Stored song byte is written to by: `0x8019CEA4`
- Uses result from call to function: `0x8019AFE8`
- In most cases this function takes: `(*(u8*)0x801D8528) - 1`

This byte at `0x801D8528` is written to by: `0x8019BE54`
- Function: `0x8019BC44`

Function: `0x8019BC44`
- Branch at `0x8019BCCC`: branches if no input to process
- Branch at `0x8019BCD4`: hit once before note, once after note
  - If no branch, processes once per note

Read breakpoint on stored song:
- `0x80154A58`
- `0x80154A6C`
  - Around here is actually where it stores the stored song byte at `0x801C6A7C`, which is mentioned above.

## Some Tracing

Loads song ctxt struct from pointer: `*(void**)(0x803EB428 +0x1F00)`.

Copies stored song byte at: `0x80154A64`
- Stores in `*(u16*)(0x803EB428 +0x12028)`
- Result: `0x803FD450`

Copies at `0x80154B38`:
- Stores in `*(u16*)(0x803EB428 +0x1202E)`

Copies at `0x80154B4C`:
- Re-stores in `*(u16*)(0x803EB428 +0x12028)`
