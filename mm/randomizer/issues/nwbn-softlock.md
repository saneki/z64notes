New Wave Bossa Nova - Softlock
==============================

## Relevant Actor

Relevant actor: `En_Mk` (Marine Scientist)

Actor file:

```
4162A0:4174D0 AF 00AE:  0000 01 FILE: 00DCC0A0:00DCD2D0 INIT 80417200:00DCD000
```

Actor file start in RDRAM:      `0x804162A0‬`
- Relevant function (`+0xA48`): `0x80416CE8`

## Giving Item

See player fields:
- `*(s16*)(link +0x384)`: item Id to give?
- `*(s16*)(link +0x386)`: ???
- `*(u32*)(link +0x388)`: Relevant actor instance pointer?

Or absolute addresses (relative to `0x803FFDB0`):
- `*(s16*)0x80400134`
- `*(s16*)0x80400136`
- `*(u32*)0x80400138`

Function which writes to these fields: `0x800B8A1C`

### Investigation

Issue arises from one or more frames processing buttons as if in normal gameplay, between bringing out instrument and processing the player fields at `+0x384,6,8`.

- Modifications to player flag field 1 when bringing out instrument:
  - Loop 1:
    - `0x8074FD5C`: `flag & 0xBFFFFFFF == 0x30000000`
    - `0x80123E30`: `flag & 0xBFF07FFF == 0x30000000`
    - `0x80762EB8`: `flag & 0xFFBFEFEF == 0x30000000`
    - Goto Loop 1
  - Next frame.
- Modifications when between stages:
  - `0x8074EB48`: `flag & 0x4BFFFFBF == 0`
    - Function: `0x8074E924`
  - Loop 1:
    - `0x8074FD5C`: `flag & 0xBFFFFFFF == 0`
    - `0x80123E30`: `flag & 0xBFF07FFF == 0`
    - `0x80762EB8`: `flag & 0xFFBFEFEF == 0`
    - Goto Loop 1 (2 times)
    - After first loop, writes relevant get-item fields.
  - `0x8074EB04`: `flag & 0xFFBFFFFF == 0`
  - `0x8074EB48`: `flag & 0x4BFFFFBF == 0`
- Post:
  - `0x8075A7FC`: `flag |= 0x20000C00`
    - Function: `0x8075A6CC`
  - `0x8074FD5C`: `flag & 0xBFFFFFFF == 0x20000C00`
  - `0x80123E30`: `flag & 0xBFF07FFF == 0x20000C00`
  - `0x80762EB8`: `flag & 0xFFBFEFEF == 0x20000C00`
  - `0x8074EB48`: `flag & 0x4BFFFFBF == 0x00000C00`
  - `0x80755148`: `flag |= 0x20000400`
    - Function: `0x80755108`
  - Loop 1:
    - Advance frame.
    - `0x8074FD5C`: `flag & 0xBFFFFFFF == 0x20000C00`
    - `0x80123E30`: `flag & 0xBFF07FFF == 0x20000C00`
    - `0x80762EB8`: `flag & 0xFFBFEFEF == 0x20000C00`
    - Goto Loop 1

## Relevant MMR Mod Disasm

```
; =========================================================
; File: 0x00DCC0A0, Address: 0x00DCCCA0, Offset: 0x00000C00
; Name: En_Mk :: Marine Scientist
; =========================================================
.headersize (0x809592E0 - 0x00DCC0A0)
; Replaces:
;   jal     0x80112E80
.org 0x80959EE0
    nop

; =========================================================
; File: 0x00DCC0A0, Address: 0x00DCCAE8, Offset: 0x00000A48
; Name: En_Mk :: Marine Scientist
; =========================================================
.headersize (0x809592E0 - 0x00DCC0A0)
; Replaces:
;   addiu   sp, sp, -0x0020
;   sw      s0, 0x0018(sp)
;   or      s0, a0, r0
;   sw      ra, 0x001C(sp)
;   sw      a1, 0x0024(sp)
;   jal     0x80136CD0
;   addiu   a0, s0, 0x0190
;   lw      t6, 0x0024(sp)
;   lbu     t7, 0x1F2C(t6)
;   bnel    t7, r0, 0x80959DC0
;   lb      a0, 0x0038(s0)
;   lb      t8, 0x0038(s0)
;   addiu   at, r0, -0x0001
;   lui     t9, 0x801F
;   bnel    t8, at, 0x80959DC0
;   lb      a0, 0x0038(s0)
;   lbu     t9, 0x057C(t9)
;   lui     t8, 0x8096
.org 0x80959D28
    addiu   sp, sp, -0x0020
    sw      ra, 0x001C(sp)
    lui     at, 0x41A0
    lui     a3, 0x42C8
    sw      at, 0x0010(sp)
    lb      t9, 0x0038(s0)
    lb      t8, 0x0277(s0)
    bne     t9, t8, 0x80959D54
    nop
    jal     0x800B8BD0
    addiu   a2, r0, 0x0075
label_0x80959D54:
    lui     t9, 0x8096
    addiu   t9, t9, -0x61E8
    sw      t9, 0x0280(s0)
    lw      ra, 0x001C(sp)
    addiu   sp, sp, 0x0020
    jr      ra
    nop

; =========================================================
; File: 0x00DCC0A0, Address: 0x00DCD1CC, Offset: 0x0000112C
; Name: En_Mk :: Marine Scientist
; =========================================================
.headersize (0x809592E0 - 0x00DCC0A0)
; Replaces:
;   .dw 0x45000A8C ; bc1f    0x8095CE40
;   .dw 0x46000A9C
.org 0x8095A40C
    .dw 0x45000A74 ; bc1f    0x8095CDE0
    .dw 0x46000A78
```
