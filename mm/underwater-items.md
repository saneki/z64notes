Underwater Items
================

C-right alpha: `0x803FD776`
C-right enabled: `0x801F358B`

`0x80110998`: Enables bottle while standing underwater as Zora.

Underwater Ocarina:
- `0x08D4`: No
- `0x80DC`: Branches -> `0x0914`
- `0x091C`: Branches -> `0x0970` (differs here)
- `0x0970`: Branches -> `0x097C`
- `0x0980`: Sets C-button to unusable

Underwater Empty Bottle:
- `0x08D4`: No
- `0x80DC`: Branches -> `0x0914`
- `0x091C`: No
- `0x0924`: Branches -> `0x095C`
- `0x0964`: Branches -> `0x0988`
- `0x0988`: Branches -> `0x0994`
- `0x0998`: Sets C-button to usable
