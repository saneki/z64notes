## Ice voiding Zora

Void flag: `*(u32*)(0x801EF670 +0x3CB0)`
- Absolute address: `0x801F3320`

This void flag is written to 1 at function `0x80169EFC`, called at: `0x80771780`.

Checks Link field: `*(s8*)(link +0xAE7)`
- Absolute address: `0x80400897`
- This field is relevant to freezing.
- If `value > 0`, will call function `0x80169EFC` to set the void flag.

Before voiding, this Link field is written to 1 at: `0x80771C20`
- To reach this code, checks if: `*(u8*)(link +0x14B) == 2`
- This is checking if the form is Zora.

## Freezeable

Maybe freeze function: `0x8074B318`
- Called at: `0x80771BBC`
  - Function: `0x80771B60`
  - Called once per frame while frozen, so what calls this?
- Called at: `0x80762F70`
  - Called via function pointer at `link +0x748` (see: `0x804004F8`).
  - So question is: what writes this pointer to "frozen" function?

Writes this function pointer in function: `0x8074E924`
- Uses variable in `0x0030 (SP)`, from `A2`.

This function is called to write "frozen" function at: `0x8075107C`.
- Function: `0x80750FA8`, likely the function for processing damage.

Code path taken for `0x80771B60` while in water:
- `0x1B80` - No branch
- `0x1B88` - No branch (branch here if freeze?)
- Reaches end.

### In Water

In water, runs `0x80771B60` for one frame before overwriting with: `0x8076DD58`
- Calls function to write this at: `0x80758F1C`

# Garo

Garo actor Id: `0x113`

Spawned dynamically by actor `0x112`, at: `0x80412AEC`

Relevant Spectrum output:
```
4128E0:413280 AF 0112:  0000 04 FILE: 00E1FBF0:00E20590 INIT 80413190:00E204A0
```
