Ice Trap Buggy Sound
====================

Using Sfx: `0x31F1`
Function: `0x801A5CFC`

Call chain:
- 0x801A5CFC
- 0x8019F1F0
- 0x800B9DDC (S0 = 0x8043CD60, ...)
- 0x800BA4F8

Spectrum output:
```
43AB90:43CD50 AF 0006:  0000 01 FILE: 00CE1FB0:00CE4170 INIT 8043CAF0:00CE3F10
43CD60:43CF84 AI 0006:  B 00 0 0E8A (  479.0   220.0   495.0) 0000 C000 0000
```

0x31F1 value seen at `*(u16*)actor +0x50`? Unknown actor field?

This value is only written when opening the chest. Is written at: `0x800B901C`
- This is called by actor: `0x8043C30C`
- Actor file offset: `0x177C`

Right before the call, loads constant into `A1`: `addiu a1, r0, 0x31F1`.

Is using the vanilla sound effect `0x31F1` in `En_Box` code, which was the proper sound effect in
OoT. Was not updated for MM.
