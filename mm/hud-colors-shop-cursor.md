HUD Colors Shop Cursor
======================

## Bomb Shop

```
40B330:40FAF0 AF 0135:  0000 01 FILE: 00E765A0:00E7AD60 INIT 8040F3B0:00E7A620
```

Writes shop cursor color: `0x8040E684`
- Offset: `0x3354`
- Function: `0x8040DA68`
- Gets color & alpha values from `u32` array at: `actor +0x30C`
Writes these color values at: `0x8040DB10`

```c
// actorBlinkDelta1:       *(f32*)(file +0x42FC)
// actorBlinkDelta2:       *(f32*)(file +0x4300)
// actor->shopCursorRed:   *(f32*)(actor +0x30C)
// actor->shopCursorGreen: *(f32*)(actor +0x310)
// actor->shopCursorBlue:  *(f32*)(actor +0x314)
// actor->shopCursorAlpha: *(f32*)(actor +0x318)
// actor->shopCursorBlink: *(f32*)(actor +0x31C)
// actor->shopCursorDir:    *(u8*)(actor +0x320)
void UpdateShopCursorColor(Actor *actor) {
    f32 blink = actor->shopCursorBlink;
    if (actor->shopCursorDir) {
        blink -= actorBlinkDelta2;
        if (blink <= 0.0) {
            blink = 0.0;
            actor->shopCursorDir = 0;
        }
    } else {
        blink += actorBlinkDelta1;
        if (1.0 <= blink) {
            blink = 1.0;
            actor->shopCursorDir = 1;
        }
    }
    u32 zero = (u32)0.0;
    u32 amount = (u32)(blink * 80.0);
    actor->shopCursorBlink = blink;
    actor->shopCursorRed   = (0 - zero) & 0xFF; // Always 0.
    actor->shopCursorBlue  = 0xFF - zero; // Always 0xFF.
    actor->shopCursorAlpha = 0xFF - zero; // Always 0xFF.
    actor->shopCursorGreen = (80 - amount) & 0xFF;
}
```

## Curiosity Shop

Actor file:
```
40B330:40F8F0 AF 01C4:  0000 01 FILE: 00F46EF0:00F4B4B0 INIT 8040F2C0:00F4AE80
```

Relevant Function: `0x8040C4BC`

## Trading Post

Shop keeper actor (Trading Post):
```
40CC20:4114A0 AF 002A:  0000 01 FILE: 00D222B0:00D26B30 INIT 80410B90:00D26220
```

Writes shop cursor color: `0x80410138`
- Offset: `0x3518`
- Gets color & alpha values from `u32` array at: `actor +0x220`
Writes these color values at function: `0x8040F5E4`
