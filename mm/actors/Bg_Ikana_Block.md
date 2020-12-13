`Bg_Ikana_Block`
================

Spectrum output:

```
40D8A0:40DA20 AI 0218:  1 05 0 FFFF ( -300.0   670.0 -1410.0) 0000 0000 0000
4177B0:418480 AF 0218:  0000 01 FILE: 00FE3BE0:00FE48B0 INIT 80418370:00FE47A0
```

Position field at `actor +0x24`, written to at:

- Write breakpoint: `0x800FF080`
  - Function: `0x800FF03C`
  - Return: `0x80418018`
- Return Function: `0x80417FE0`
