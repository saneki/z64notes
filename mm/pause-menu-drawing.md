Pause Menu Drawing
==================

Uses table of segmented-address pointers to draw menu borders/etc: `0x80760580`

Example DList of vanilla game drawing Hookshot on C buttons:

```
E7000000 00000000
FA000000 FFFFFFFF
FC119623 FF2FFFFF
FD180000 80540ED0 // Texture address start = 0x80540ED0
F5180000 07000000
E6000000 00000000
F3000000 073FF080
E7000000 00000000
F5181000 00000000
F2000000 0007C07C
E449C0A8 0043C048
E1000000 00000000 // Texture start = (0, 0)
F1000000 05500550
```

### Icon Item 24 List

- 0 = Skulltula
- 1 = Heart Container?
- 2 = Heart Piece
- 3 = Heart Piece
- 4 = Heart Container?
- 5 = Heart Container?
- 6 = Boss Key
- 7 = Compass
- 8 = Map
- 9 = Skulltula
- 10 = Small Key
- 11 = Magic jar
- 12 = Magic jar (large)

### Stray Fairy Icon

Starts writing around `0x80752A3C`.

```
E7000000 00000000
FC119623 FF2FFFFF
FA000000 FFFFFFF9 // Alpha value flutters.
FD180000 02008998 // Alternates between 0x02008998 (facing side) and 0x0C001B80 (facing front).
F5180000 07000150
E6000000 00000000
F3000000 072FF080
E7000000 00000000
F5181000 00000150
F2000000 0007C05C
E4158290 000D8230 // Dimensions: x=32, y=24
E1000000 04000000 // 04000000 when facing left, 00000000 when facing right.
F1000000 04000400
```

Segment `0x2` = `0x80518AE0` (???)
Segment `0xC` = `0x805FDFD0` (`icon_item_map`)
- Seems to be different if in dungeon vs. out of dungeon.

How does it choose the segmented address?

```c
s16 A = *(s16*)0x8076034C;           // Likely the state for depicting fairy direction.
u16 B = *(u16*)(0x801EF670 +0x48C8); // Likely the dungeon index.
// Get results from table.
u32 result = *(u32*)0x80760360 + (A * 4) + (B * 0x10);
```

Table dump for segmented addresses:

```
02008998 0C001B80
02008998 0C001B80
02009598 0C002780
02009598 0C002780
0200A198 0C003380
0200A198 0C003380
0200AD98 0C003F80
0200AD98 0C003F80
```

#### What is `0x80518AE0` ???

Referenced at: `0x803FD678`, or: `game +0x16B58`, or: `game.hud_ctxt +0x170`.
- Field name seems to be `parameter_static`.

### Skulltula Token Icon

Starts writing around: `0x8011F97C`.

```
E7000000 00000000
FC119623 FF2FFFFF
FA000000 FFFFFFFF
FB000000 000000FF
FD180000 020031E0 // Fmt=RGBA, Siz=32b
F5180000 07000000
E6000000 00000000
F3000000 0723F0AB
E7000000 00000000
F5180C00 00000000
F2000000 0005C05C
E40B0334 000502EC // Dimensions: x=24, y=18
E1000000 00000000
F1000000 04000400
```
