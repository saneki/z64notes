Asm Patch Bug
=============

Seeing patched instructions in memory at `0x800C43C4`, *why*???

Patched instructions:
- Virtual address (from `boot.asm`): `0xB5A904`
- Expected RAM address: `0x801748A4`
- After decompressing the patched ROM, I'm seeing them in their expected place in the file.
  - Example: `0xAAA5C8`
- Difference in how my decompressor treats `DoesNotExist` entries in the file table???

In decompressed patched ROM, seeing original boot instructions:
- `0xB5AAB4` (difference is `0x1B0` from file address in `boot.asm`?)
- This is because the file beforehand with address `0x00AD1000` had `0x1B0` bytes added by the randomizer.

Addresses in the patch file are file offsets, not virtual addresses.
- So, look at the physical begin/end, not virtual
- Maybe create better patcher?

### Three `DoesNotExist` Files

- `00957000 009ECEC0`, diff: `0x95EC0`
- `009ED000 009F4700`, diff: `0x7700‬`
- `00A807A0 00A8B9C0`, diff: `0xB220`

Total: `0xA87E0`
