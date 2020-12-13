Scopecoin
=========

Function to add rupees to rupee counter: `0x801159EC`
- Rupee counter is: `*(s16*)0x801F0688`, or: `*(s16*)0x801EF670 +0x1018`

When getting the two red rupees from pillar:
- `0x80113EE8`, calls function with amount from: `*(s16*)0x801BF998 +(0x87 * 2)`
  - Absolute: `0x801BFAA6`
- This seems like processing get-item for item Id `0x87` (red rupee).

Spawns red rupee `En_Item00` at: `0x800A79F0`
