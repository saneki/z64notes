World Colors
============

## `En_Water_Effect`

Actor Id: `0x170`

```
413C40:416600 AF 0170:  0000 06 FILE: 00EC2280:00EC4C40 INIT 80416430:00EC4A70
```

Writes `SetPrimColor` at: `0x80414B0C`

## `Obj_Syokudai` (Torch Stand)

Actor Id: `0x39`

```
4201B0:420F90 AF 0039:  0000 06 FILE: 00D36210:00D36FE0 INIT 80420E40:00D36EA0
```

- Writes `SetPrimColor(0xFFFF00FF)` at: `0x80420D44`
  - Used for "main fire" color.
- Writes `SetEnvColor(0xFF000000)` at: `0x80420D60`
  - Used for "inner fire" color.

Note: Even if you NOP out the draw function where these display list instructions are written, the
flare from the torch flame is still drawn.

It might be drawn on `poly_opa` instead of `poly_xlu`.

## Goron Roll

...

## Unknown

Function at `0x800B0B10` used to write `SetPrimColor` and `SetEnvColor` instructions.
- Called from: `0x80532FC0`
