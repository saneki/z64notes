`En_Zog`
========

## Push Speed

```
420FF0:423B00 AF 0224:  0000 01 FILE: 00FF8480:00FFAF80 INIT 80423540:00FFA9D0
423B10:423E3C AI 0224:  4 00 0 080F (-1604.0   -11.5  4671.0) 0000 3BFF 0000
```

Writes actor X/Z speed to `0` at: `0x80422B68`
- Actor field: `*(f32*)(actor +0x70)`

Writes actor X/Z speed in `player_actor` code: `0x80765450`
- Function: `0x807653AC`
- Seems to be a function that is called only when in water, and checks if anything is grabbed to push it using Link's linear velocity.

```c
f32 cos = cosS_to_F(actor->rot2.y);
f32 velocity = link->linear_velocity;
return cos * velocity * 0.5;
```
