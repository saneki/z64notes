Goron Race D-Pad Frame
======================

Branches for function `0x8074D29C`:
- `0xD2C0 -> 0xD74C`: No branch (to function end)
- `0xD2D0 -> 0xD74C`: No branch (to function end)
- `0xD2E0 -> 0xD74C`: No branch (to function end)
- `0xD2F0 -> 0xD74C`: No branch (to function end)
- `0xD300 -> 0xD3F8`: Branches
- `0xD3F8 -> 0xD564`: No branch
- `0xD408 -> 0xD564`: Branches
- `0xD570 -> 0xD598`: No branch
- `0xD57C -> 0xD59C`: Branches
- `0xD5B8 -> 0xD638`: No branch
  - Calls `0x8012364C` before this branch, to return which item is being used via C-buttons.
- `0xD60C -> 0xD748`: Branches (to function end)
  - If we try to use a C-button this frame, it doesn't jump.

Trying C-button:
- `0xD5B8 -> 0xD638`: Branches
- `0xD63C -> 0xD69C`: Branches
- `0xD69C -> 0xD6B4`: Branches
- `0xD6B8 -> 0xD6D4`: Branches
- `0xD6FC -> 0xD738`: Branches
- Calls `0x8074EE20` to use item?
- This means there must be some code in function `0x8012364C` to check if C buttons can be used at all?

Trying C-button (later):
- `0xD60C -> 0xD748`: No branch
- `0xD628 -> 0xD74C`: Branches (to function end)

Something sets bytes to `0x801F3588` to `0xFF` if C-buttons cannot be used at all.
- Writes C-down to `0xFF` at: `0x801128BC`
  - Function: `0x80111CB4`

Function our code calls to get C-button usability: `0x80110038`
- Is normally called at: `0x80112984`, which is this function!

This function at `0x80111CB4` does certain checks which updates the C-button usability:
- Disables C buttons if entrance Id is `0x8E10` (???)
- Disables C buttons if entrance Id is `0xD010` (Goron Race)
- Updates C buttons if: `*(u8*)(0x801EF670 +0xF00) & 1 != 0`
  - ... and some other stuff?
