Spider House Door Crash
=======================

- Commit: `fef4d39`
- Object data table: `0x8072A8F0`

### Example Object Data Table

Example table for object data when leaving a room.

Before:
```
00960000 8074AD90
013F0000 8074C540
00900000 8074CD80
02280000 8074CF70
```

After (facing door, no crash):
```
00900000 8074AD90
02280000 8074AF80
013F0000 8074C7E0
00000000 00000000
```

After (facing outward, crash):
```
013F0000 8074AD90
00900000 8074B5D0
02280000 8074B7C0
00000000 00000000
```

Actors seem to only be drawn if the game thinks they could be visible.
- This impacts the order of object data in the buffer.

## Assigning Pointers for Game DLists

See: `0x80173DF0`

```c
u32 index  = gfx->frame_cnt_1 & 1;
u32 offset = index * 0x19B30;
// Or:     = (((index * 129) * 3) * 17) * 16;
// Or:     = ((((((index << 7) + index) << 2) - index) << 4) + index) << 4;
u8 *base   = 0x80209EA0 + offset; // Store in S1
u8 *opa    = base + 0x6508; // Should be either: 0x80209EA0, 0x80229ED8
```
