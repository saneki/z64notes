Tracing
=======

Ocarina of Time
---------------

### Frame/State Update Function

Breakpoint: `0x8009CAC8`
- Return: `800A0C00`
- Return Function: `0x800A0BD0`

Function: `0x800A0BD0`
- Still single break/frame
- Return: `0x800A16BC`
- Return Function: `0x800A1688`

Function: `0x800A1688`
- Still single break/frame
- Return: `0x800A19C8`
- Return Function: `0x800A1934`

Function: `0x800A1934`
- Might be top-level frame process loop? Not returning.
- Loop: `[0x800A19C0, 0x800A19D0]`

Using the `BEQZ` bytes, found the equivalent in Majora's Mask:
- Loop: `[0x801749C8, 0x801749D8]`

### Boot Hook

The `boot.asm` file says it hooks in memory at: `0x800A1C54`.

This is a function that seems to be run only once early on for initialization.

Function: `0x800A1C50`
- Args:
  - `A0`: `0`
- Return: `0x8000062C`
- Return Function: `0x800005A0`

### DPAD Draw Hook

In `hacks.asm`, hooks 2 instructions at: `0x8007571C`.

Function: `0x800756F0`
- Args:
  - `A0`: `0x801C84A0`
- Return: `0x8009C06C`

In Rom: `0xB43060` might be a hit? Similar instructions near backwards-branch.
- RAM: `0x8015D000`
- Function: `0x8015B198`
- Return: `0x80151AA4`
- Function seems way bigger, very unlikely.
- Seems to break at the same point as OoT though? Maybe.

Pointers:
- Context: `0x801C84A0`
- Gfx:     `0x8011F290`
- Overlay: `0x8011F538‬`

State of overlay at DPad hook time:
- `0x00002000` `0x8018C958` `0x8018C9B8` `0x8018E958`
- So at this point, `0x60` bytes of display list used.

Majora's Mask
-------------

`z64_file_t` address: `0x801EF670`

### Frame Processing

Main function: `0x801748A0`

Top-level frame process loop is mentioned above.

It calls: `0x80174868`, which calls two other functions:
- `0x801744AC`, this *does not* update the frame.
- `0x801744F8`, this *does* update the frame.

### Magic Meter Size

Read breakpoint: `z64_file_t *` `+0x3F2E`
- Hit: `0x80116A68`
- Function: `0x80116918`
- Return: `0x801201B8`
- Return Function: `0x8011F0E0`?

Function: `0x8011F0E0`
- End: `0x80120F8C`

### Time-Played Frame Counter

#### Read Breakpoint: `z64_file_t *` `+0x4F`

- Hit: `0x80409FB8` (function `0x80409F5C`)
- Hit: `0x8040A194`
- Frame renders

Function: `0x80409F5C`
- May be a good test address for a per-frame thing?
- End: `0x8040A280`
- Return: `0x800B974C`
- Return Function: `0x800B948C`

#### Write Breakpoint

- Hit: `0x8040A1A8`
- Return: `0x800B974C`

Function: `0x800B948C`
- Return: `0x800B9898`

### C-Button

Read Breakpoint: `z64_file_t *` `+0x5D`

During text box:
- Hit: `0x80110FAC`
- Hit: `0x801110DC`
- Hit: `0x8011116C`
- Hit: `0x801113B0`
- Hit: `0x801113F8`
- Hit: `0x801115F8`
- Hit: `0x80111728`
- Hit: `0x80111A14`
- Hit: `0x80111A60`
- Frame renders
- Click
- Hit: `0x801178C4`
- Click
- Hit: `0x801188C4`
- Click
- Hit: `0x80117C40`
- Click
- Hit: `0x801189C0`

### Draw Interface

DB notes this is: `0x801210E0`
Return: `0x80167C80`

### DMA Table

Read Breakpoint on DMA table first byte: `0x80006800`
Breaks on: `0x80000114` on boot.
- At this point, the DMA table looks identical to what's in the rom file (`0x7400`).
- Breaks in the same spot for following table entry bytes.
- Thus, appears to be a segment of boot code (not function) starting at `0x800000CC` which uses
  the table to set up the mapping.
- Seems to happen in a loop from `[0x80000114, 0x80000184]`, reading the table in segments of
  4 bytes.
  - `T1` is pointer to current word.

### Deku Nuts

See: `0x80115AD8`, breaks before item use?
- ~~Function: `0x80115908`~~
- Seems to branch to `0x80115AA8` from somewhere? (`0x80115A30`)
- Real function begin might be `0x80115A14`
  - `A0` = `0x9` (deku nut Id)
  - `A1` = `0xFFFFFFFF` (-1)
  - Might be a "use_deku_nut" or "subtract_deku_nut" function
- Return: `0x8077006C`
- Return Function: `0x8076FFB8`
- `deku_nut_ammo = *(deku_nut_ammo) - 1;`

Function: `0x8076FFB8`
- `A0`: `0x803FFDB0`
- Return: `0x80762F78`

### Form Change

Breaks: `0x80755DB4`

Function: `0x80755D48`
- `A0`: Context
- `A1`: `0x803FFDB0`
- `A2`: Form byte
- Return: `0x80756068` (to human form)
- Return: `0x807560A4` (to deku form)
  - Seems to be getting `A2` (byte value to use) from `0x803FFEFA` (`0x803FFDB0 +0x14A`).
    - Then subtracting that value by `0x4E`.
- Return function?: `0x80755F20`

#### Transformation Masks Byte: `0x803FFEFA`

Breaks in 4 places (in 3 functions):
- `0x8074F068` (set to value before animation)
- `0x8074EC1C` (set to `0`)
- `0x8074EC28` (set to value)
- *animation happens*
- `0x8075F258` (set to `0` after animation)
  - This also sets a bunch of nearby values?

The three functions in order:
- `0x8074EE20`
  - Only called on using mask?
  - Return: `0x8074D748`
  - Return Function: `0x8074D29C`
- `0x8074EBF0`
  - Return: `0x8074EC20`
- `0x8075EF54`
  - Return: `0x8075F148`

Note: This area of code seems to only be in memory when needed.
To test, I set a write breakpoint on `0x8074F000`.
Break: `0x80089668` (seems to zero memory in sizes of `0x20`)
- Apparently this area of memory is being swapped out on pause screen?
- Might be distinguishing between "Main Gameplay" vs "Pause Screen" code?

This means: We will probably need to call some always-there function which maps this code into
memory before calling it.

Return chain: `0x8074EE20` (called only when transforming?)
- Return: `0x8074D748`
  - Function: `0x8074D29C` (called constantly)
- Return: `0x8074DA1C`
  - Function: `0x8074D94C`
- Return: `0x8074F6D4`
  - Function: `0x8074F5FC`
- Return: `0x80750548`
  - Function: `0x807504E8`
- Return: `0x80768474`
  - Function: `0x8076842C`
- Return: `0x80762F78` (jump: `JALR RA, T9`)
  - Function: `0x80762388`
- Return: `0x807637D0`
  - Function: `0x80763548`
- Return: `0x80160BB0` (jump: `JALR RA, T9`)
  - `T9 = *0x801F6B38`
  - This address always seems to point to `0x80763548`.
  - Function: `0x80160B80`

Function `0x8074D29C`:
- Args:
  - `A0`: `(z64_link_t *) 0x803FFDB0`
  - `A1`: `(z64_ctxt_t *) 0x803E6B20`
- Normal control flow: Branches to end of function at `0x8074D680`.
- At some point, `A2` holds the item of mask being used (deku is `0x32`).

### UseItem

Function `0x8074EE20`:
- Args:
  - `A0`: `(z64_ctxt_t *) 0x803E6B20`
  - `A1`: `(z64_link_t *) 0x803FFDB0`
  - `A2`: Item code.
  - `A3`: `2` (unsure if used)
- Seems to be the "Use Item" function.

Function: `0x8074C9B4`
- If usable item?: Gets `*(uint8_t *)(0x80789E2C + item)`

Checking C buttons in `z64_file_t`:
- Breaks: `0x8074D204`
  - Function: `0x8074D19C`
  - Return: `0x8074D31C`

#### Twice-Used Bug

Checking Mask (`0x803FFF03`):
- Breaks: `0x8074F244`
  - Happens even during bug where mask doesn't get equipped (via dpad)
  - Sets it appropriately according to mask?
- Breaks: `0x8074F22C`
  - Sets it to 0.
  - After NOP-ing this, seems to be the "unequip" code.
  - It's calling `UseItem` twice!

First Return: `0x80780188` (our code)
Second Return: `0x8074D3B4`
- Function: `0x8074D29C`
- This seems to be the culprit. NOP-ing this call (at `0x8074D3AC`) seems to fix the issue.

The branch at `0x8074D30C` seems to branch if wearing mask?
- Checks `*(uint8_t *)(0x803FFDB0 +0x153) == 0`

The branch at `0x8074D320` branches with non-buggy mask, but doesn't with buggy mask.
- Seems to branch using result from function call `0x8074D19C`
- We want it to return 0?

### No B-Button Bug

Before calling `0x8074EE20`:
- Sets `A3` to `0x0146 (S0)` (where `S0 = 0x803FFDB0`)
  - Byte is at: `0x803FFEF6‬`
  - This byte seems to be reset after sword swing with mask on?
    - Write break: `0x8074D710` (same function that calls `UseItem`)
    - It's right next to the call in fact.
    - This seems to be because doing normal sword swings is considered using the sword item.
      - The jump slash isn't though?

Tracing branches on sword swing:

`0x8074D5B8` (executes every frame)
- jumps to `0x8074D63C` (executes only on swing)
- jumps to `0x8074D69C`
- which executes until `0x8074D6D8` (and beyond).

The branch delay instruction at `0x8074D5BC` puts item code into `A2` from `V0`:
- `OR A2, V0, R0`

Gets this value from the call to `0x8012364C`.

Function: `0x8012364C`
- Does some checks against:
  - Bytes: `0x801EF670 [+0x3F19, +0x3F1A, +0x3F1B]` depending on C-button?
    - This is likely used for moving items to C-buttons in menu.
    - They are always `0x00` outside of menu, `0xFF` in menu.
  - Short: `0x801EF670 +0x3F22`
- `uint8_t GetItemFromButton(z64_ctxt_t *ctxt, z64_link_t *link, uint8_t button)`

Button checking loop beforehand: `0x8074D5D8`
- Checks `uint16_t [4]` array at `0x8077A438`
- `T8 = 0x801F9A0C` (stack pointer)
  - `T8 = 0x8077FFD4`, which points to a value

Omg I've been looking at the wrong call this whole time, `GetItemFromButton` gets called twice.
- Focus on call at `0x8074D5A4` instead.
- Gets button from call to `0x8074D254`

Function `0x8074D254`:
- `T6 = *(uint16_t)((*0x8077FFD4) + 0xC)`
- ... or `T6 = *(uint16_t *)(0x801F9A0C + 0xC)`
- The value at `0x8077FFD4` changes, but in this case is set to the stack variable `0x801F9A0C`.
- This is set by the function `0x80762388`.
  - Return: `0x807637D0`

C Buttons accessed:
- `0x8074D204`
- `0x8074D370`

Found it! The struct at `0x801F9A0C` gets modified by instructions at: `0x80763740`.
- `T8` points to the dest struct
- `S1` points to the global context struct: `0x803E6B20`
- Seems to just be copying values over???
- Successfully copies `0x4000` over, read breakpoints:
  - `0x80756910`
  - `0x80757628`

#### Manual Tracing of `0x8074D29C` Branches

With mask on (non-buggy):
- `0xD2C0`: No branch
- `0xD2D0`: No branch
- `0xD2E0`: No branch
- `0xD2F0`: No branch
- `0xD300`: No branch
- `0xD30C`: No branch
- `0xD320`: Branch -> `0xD3BC`
- `0xD3C4`: Branch -> `0xD3F0`
- `0xD3F8`: No branch
- `0xD408`: No branch
- `0xD41C`: No branch
- `0xD428`: No branch
- `0xD438`: Branch -> `0xD448`
- `0xD464`: Branch -> `0xD564`
- `0xD570`: Branch -> `0xD598`
- Hits `0xD5A4`

With mask on (differences, buggy):
- `0xD320`: No branch (this is first branch taken differently)
- `0xD334`: No branch
- `0xD348`: No branch
- `0xD380`: Branch -> `0xD394`
- `0xD3B4`: Always branch -> `0xD74C`
- Misses `0xD5A4`

Note: Even when hitting the function in buggy mode, `0x4000` (B button) is still set to the
`pad_t` on the stack (`0x801F9A0C + 0xC`). So it is still recognizing correct inputs but not
processing for some reason?

This establishes what was already known about `0x8074D320`?

Replacing jump at `0x8074D314` with `ADDIU V0, R0, 1` seems to fix B button issue? No idea if this
has any side effects.

### Lens of Truth Magic Decrement

Checking magic value:
- Breaks: `0x801166C0`
- Function: `0x80116348`
- Gets existing value and subtracts 1.
- Checks flag byte: `*(uint8_t *)(0x801EF670 +0xF06)` -> `0x801F0576`
- Apparently: Branch at `0x80116394` is taken if Lens of Truth *not* being used.
  - `*(uint16_t *)(0x801EF670 +0x3F28)` -> `0x801F3598‬`
  - This value seems to be set to `7` when lens on, `0` when lens off.
  - Is updated once per frame when off.
    - Breaks (off): `0x80116904`
      - Function: `0x80116348`
      - Same function!
      - This instruction is exactly where `0x80116394` jumps to!
    - Breaks (turning on): `0x80115F24`
      - Function: `0x80115DB4`
      - Return: `0x8074ED68`

### Graphics Context

Pointers:
- Context: `0x803E6B20`
- Gfx:     `0x801F9CB8`
- Overlay: `0x801F9F50‬`

First field of `z64_ctxt_t *` (at `0x803E6B20`) is the graphics context.
- Points to `0x801F9CB8` (stack variable) but is also `0` sometimes.
- Set to `0` at: `0x80168F90`
  - Function: `0x80168F64`
- Restored from `0` at: `0x80168FAC`
  - Same function!
- The first function that gets called after it is restored, is `0x80168DAC`.

Function: `0x80168F64`
- Return: `0x801737A8`
- Return Function: `0x8017377C`

Function: `0x8017377C`
- At time of hitting this function, overlay display buffer pointer has been set and contents are empty.
- Return: `0x80174524`
- Return Function: `0x801744F8`

Function: `0x801744F8`
- Return: `0x80174890`

#### Minimap Alpha

Might be writing minimap alpha at: 0x8011A12C (writes: `0xFA000000 0x00AA64FB` to display list)?
- `0xFA` indicates `G_SETPRIMCOLOR`
- `0x00AA` matches (in OoT): `z64_game.hud_alpha_channels.minimap` when hidden?

This code is only reachable via branch, branches at: `0x80119B20`.
- Still seems to break when the map is enabled though, maybe not.

### Map Purchase

Purchase of Woodfall map affects (offsets of `0x801EF670`):
- 0xEA7: 0x00 => 0x01
- 0xEA8: 0x00 => 0x40
- 0xEAA: 0x20 => 0x28
- 0xEAB: 0x00 => 0x80
- 0xEAF: 0x09 => 0x69
- 0xF1B: 0x01 => 0x03 (???)
- 0xF63: 0x03 => 0x1F (corresponds to clouds hidden on map screen)

### C Buttons Interface

DB notes this is at: `0x80118890`.

Function: `0x80118890`
- Return: `0x80120224`
- From NOP-ing, this actually draws the triangle-pattern and item textures on the C-Buttons, not
  the buttons themselves!
- This does *not* draw the underlying C-Button as faded out when unusable.
- Underlying C & B buttons are drawn by `0x80117100`.
  - Which is called right before this function.

Function: `0x80117100`
- ...

Dump of display list additions after call to `0x8010CFBC` (call at `0x801171E0`):

```
E7 00 00 00 00 00 00 00 FA 00 00 00 00 00 00 64
FD 70 00 00 02 00 0F 60 F5 70 00 00 07 00 00 00
E6 00 00 00 00 00 00 00 F3 00 00 00 07 1F F2 00
E7 00 00 00 00 00 00 00 F5 68 08 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 31 80 C0 00 2A 40 4C
E1 00 00 00 00 00 00 00 F1 00 00 00 04 7E 04 7E
E7 00 00 00 00 00 00 00 FA 00 00 00 64 FF 78 FF
E4 31 00 B8 00 29 C0 44 E1 00 00 00 00 00 00 00
F1 00 00 00 04 7E 04 7E
```

Seems to use:
- Color format: `G_IM_FMT_IA`
- Bit size: `G_IM_SIZ_16b`

```c
uint8_t *structure = (0x803E6B20 + 0x169E8);

// Get left C-button value and alpha
uint8_t c_left = *(uint8_t *)(0x801EF670 + 0x4D);
uint8_t c_left_alpha = *(uint16_t *)(structure + 0x26A) & 0xFF;

// ...

// Get bottom C-button value and alpha
uint8_t c_bottom = *(uint8_t *)(0x801EF670 + 0x4E);
uint8_t c_bottom_alpha = *(uint16_t *)(structure + 0x26C) & 0xFF;

// ...

// Get right C-button value and alpha
uint8_t c_right = *(uint8_t *)(0x801EF670 + 0x4F);
uint8_t c_right_alpha = *(uint16_t *)(structure + 0x26E) & 0xFF;

// ...
```

This shows us where the C-button alpha values are located, relative to the context structure.
- Address of sub-structure: `0x803FD508`
  - C-button alphas: `0x803FD772‬`
    - Write breakpoint:
      - `0x8010F028` - Called after form transformation
      - `0x8010F038` - Called during menu?
      - `0x8010F274` - Called (twice) before form transformation

Function `0x8010F028`:

```c
uint8_t *ctxt = (0x803E6B20);
uint8_t *file = (0x801EF670);

uint8_t *v0 = (ctxt + 0x169E8);
uint8_t t6 = *(uint8_t *)(file + 0x3F18); // [0x3F18, 0x3F1C]?
                                          // 0x801F3588
uint8_t t7 = *(uint8_t *)(file + 0x1015);

if (t6 == 0xFF) {
  // ...
} else if (t7 == 0xFF) {
  // ...
}

// Finish reversing this?...
```

In the above code, `0x801EF670 +0x3F18` points to 4 bytes, each of which is either `0x00` or `0xFF`,
indicating the enabled-ness of the B and C buttons.

Sidenote: After looking around that address (`0x801F3588`) for a bit, byte `0x801F3593` might
actually be an input-lock flag (`value == 0x32` if C buttons are usable?).
- `0x00` when on black-screen before transition/cutscene, Song-of-Soaring select screen
- `0x01` when changing areas, cutscenes, learning/playing ocarina songs
  - In cutscenes, mostly `0x01` but also `0x00` and `0x02` for a bit.
- `0x02` when using Ocarina, telescope, soaring
- `0x05` when in NPC dialogue
- `0x07` when on pause menu
- `0x0C` when in mini-game (C buttons are hidden)
  - Includes Epona
- `0x10` when at give-a-C-button-item prompt
- `0x32` when able to use B/C buttons?

Write breakpoint on these:
- `0x80112E34` - Zero-ing them out
- `0x8075D748` - Writing `0xFF` to all of them
- `0x8075F8BC` - Writing individual values to each
  - Uses bytes at `0x807628D8`.
  - This code might be specific to Deku Game grotto?
- `0x80111C44` - ...
- `0x80110B38` - Write `0xFF` to all?
- `0x801109B0` - Going underwater? Actually called for every frame in water.
  - Check at `0x80110894` *specifically* checks for Zora Mask item to enable.
  - This means `A2` is the item code.
  - Call to `0x801242DC` might be interesting.

Function: `0x80110038`
- Args:
  - `A0`: `0x803E6B20`
- End: `0x80111CAC`
- Doesn't seem to return anything?
- Writes to:
  - `uint8_t[4] *(0x801EF670 +0x3F18)`
  - `uint16_t   *(0x801EF670 +0x3F22)`
    - `0x80111C98`
  - Other places:
    - `T9`: `0x80110518`
    - `T7`: `0x80110CE8`
    - `T8`: `0x80110EEC`

Function: `0x801242DC`
- Args:
  - `A0`: `0x803E6B20`
  - `A1`: `0x801EF67[1,2,3]`
  - `A2`: `0x9`
  - `A3`: `0x1`

### Draw C Button Items

On call, display list pointer changes:
- From: `0x8022EBF0`
- To: `0x8022ED58`

```
E7 00 00 00 00 00 00 00 FA 00 00 00 FF FF FF FF
FC 11 96 23 FF 2F FF FF FD 18 00 00 80 53 EE D0
F5 18 00 00 07 00 00 00 E6 00 00 00 00 00 00 00
F3 00 00 00 07 3F F0 80 E7 00 00 00 00 00 00 00
F5 18 10 00 00 00 00 00 F2 00 00 00 00 07 C0 7C
E4 3E C0 A8 00 38 C0 48 E1 00 00 00 00 00 00 00
F1 00 00 00 05 50 05 50 E7 00 00 00 00 00 00 00
FC 30 96 61 55 2E FF 7F E7 00 00 00 00 00 00 00
FA 00 00 00 FF FF FF FF FC 11 96 23 FF 2F FF FF
FD 18 00 00 80 53 FE D0 F5 18 00 00 07 00 00 00
E6 00 00 00 00 00 00 00 F3 00 00 00 07 3F F0 80
E7 00 00 00 00 00 00 00 F5 18 10 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 44 40 E8 00 3E 40 88
E1 00 00 00 00 00 00 00 F1 00 00 00 05 50 05 50
E7 00 00 00 00 00 00 00 FC 30 96 61 55 2E FF 7F
E7 00 00 00 00 00 00 00 FA 00 00 00 FF FF FF FF
FC 11 96 23 FF 2F FF FF FD 18 00 00 80 54 0E D0
F5 18 00 00 07 00 00 00 E6 00 00 00 00 00 00 00
F3 00 00 00 07 3F F0 80 E7 00 00 00 00 00 00 00
F5 18 10 00 00 00 00 00 F2 00 00 00 00 07 C0 7C
E4 49 C0 A8 00 43 C0 48 E1 00 00 00 00 00 00 00
F1 00 00 00 05 50 05 50 E7 00 00 00 00 00 00 00
FC 30 96 61 55 2E FF 7F
```

Uses these texture memory addresses, specifically reserved for C-buttons:
- `0x8053EED0`
- `0x8053FED0`
- `0x80540ED0`

Write breakpoint for `0x8053EED0`:
- `0x800810A8`
  - Function: `0x80080FF0`

When switching out an item, the data at these addresses will be modified for the new item.

Function: `0x80080FF0`
- Return: `0x800811F4`
  - Function: `0x80081178`
- Return: `0x80178D9C`
  - Function: `0x80178D7C`
- Return: `0x80178E2C`
  - Function: `0x80178DAC`
- Return: `0x80178E6C`
  - Function: `0x80178DAC` (recursive call)
- Return: `0x80178E6C`
  - Function: `0x80178E3C`
- Return: `0x80112BD4`
  - Function: `0x80112B40`
- Return: `0x807563A8`
  - This is pause menu code.
  - Only gets called when setting the *left c button* specifically.

This call to `0x80112B40` happens for all three C buttons:
- `0x807563A4` for left C button (as mentioned above)
- `0x8075647C` for bottom C button
- `0x80756554` for right C button

Sidenote: During call to this function, `A2` points to `0x803FD850`.
- In memory, this seems to have a magic number: `0x56494557` (`VIEW`)
- This is likely a sub-structure or some data in `z64_ctxt_t`.

Function: `0x80112B40`
- Args:
  - `A0`: `0x803FD850`
  - `A1`: C-button index?

Function: `0x80178E3C`
- Args:
  - `A0`: `0xA36C10` (virtual ROM address?)
    - This value actually has its own file entry in the table.
  - `A1`: Item code
  - `A2`: `0x803FD850` (likely arg passed by parent function)
  - `A3`: `0x1000` (dest length?)

Function: `0x80080950`
- `table_entry * GetFileEntryOfVirtualAddr(uint32_t virt_addr)`
- Uses hardcoded address of `0x8009F8B0`
  - Is a large table of pointers?
  - Oh! This is the DMA file table in memory.

Function: `0x80080954`
- `GetPhysicalAddrOfFile(uint32_t virt_file)`

Function: `0x80178DAC`
- `LoadItemTexture(uint32_t phys_file, uint8_t item, uint8_t *dest, uint32_t length)`
- Args:
  - `A0`: `0x980F60` (physical ROM address?)
  - `A1`: Item code?
  - `A2`: Dest address
  - `A3`: `0x1000` (dest length)

Weird Values:
- Goron Mask: `0x0099C12C`
- Zora Mask:  `0x0099CB7C`
- Virtual address into compressed texture data?
  - Except the file entry for this virtual address is a `DoesNotExist` entry.
  - Oh! This is actually likely the physical address, translated from the previous virtual address value.
  - The weird `0xA?????` was a virtual address, and resolved to `0x9?????` which is the physical address.

File at `0x009959E0` (through `0x009DACB0`):
- Seems to be a table of offsets (relative to itself) which are each `Yaz0` entries.
- I'm guessing each of these is a `Yaz0`-compressed texture.
- The first offset is `0x2FC`, and each offset is 4 bytes in size.
  - Thus, there should be `0xBF` (`191`) compressed chunks.

### Draw B Button Item

Function: `0x80118084`
- Called at: `0x80120214`

Only does this conditionally:
- If: `*(uint8_t *)(0x801EF690) == *(uint8_t *)(0x803FFDB0 + 0x14B)`

On call, display list pointer changes:
- From: `0x8022EBE0`
- To: `0x8022EC48`

#### Item Sprite Display List

When drawing the Kokiri Sword over the B button, this is what is added to the display list:
```
E7 00 00 00 00 00 00 00 FA 00 00 00 FF FF FF FF
FC 11 96 23 FF 2F FF FF FD 18 00 00 80 53 DE D0
F5 18 00 00 07 00 00 00 E6 00 00 00 00 00 00 00
F3 00 00 00 07 3F F0 80 E7 00 00 00 00 00 00 00
F5 18 10 00 00 00 00 00 F2 00 00 00 00 07 C0 7C
E4 31 40 BC 00 29 C0 44 E1 00 00 00 00 00 00 00
F1 00 00 00 04 4C 04 4C
```

This translates to the following opcodes:
```
G_RDPPIPESYNC   : E7 00 00 00 00 00 00 00
G_SETPRIMCOLOR  : FA 00 00 00 FF FF FF FF
G_SETCOMBINE    : FC 11 96 23 FF 2F FF FF
G_SETTIMG       : FD 18 00 00 80 53 DE D0
G_SETTILE       : F5 18 00 00 07 00 00 00
G_RDPLOADSYNC   : E6 00 00 00 00 00 00 00
G_LOADBLOCK     : F3 00 00 00 07 3F F0 80
G_RDPPIPESYNC   : E7 00 00 00 00 00 00 00
G_SETTILE       : F5 18 10 00 00 00 00 00
G_SETTILESIZE   : F2 00 00 00 00 07 C0 7C
G_TEXRECT       : E4 31 40 BC 00 29 C0 44
                  E1 00 00 00 00 00 00 00
                  F1 00 00 00 04 4C 04 4C
```

As functions:

```c
gsDPPipeSync();
gsDPSetPrimColor(0, 0, 0xFF, 0xFF, 0xFF, 0xFF);
// ...
// gsDPSetCombineLERP(a0=1, c0=3, Aa0=1, Ac0=3, a1=1, c1=3, b0=0xF, b1=0xF, Aa1=1, Ac1=3, d0=7, Ab0=7, Ad0=7, d1=7, Ab1=7, Ad1=7); // MICROCODE ORDER
//
// Note: The "A**=0" is not using the actual value 0, but is being used to concat into the constant "G_ACMUX_0". 
// gsDPSetCombineLERP(a0=TEXEL0, c0=PRIMITIVE, Aa0=TEXEL0, Ac0=PRIMITIVE, a1=TEXEL0, c1=PRIMITIVE, b0=K5, b1=K5, Aa1=TEXEL0, Ac1=PRIMITIVE, d0=COMBINED_ALPHA, Ab0=0, Ad0=0, d1=COMBINED_ALPHA, Ab1=0, Ad1=0)
gsDPSetCombineLERP(TEXEL0, K5, PRIMITIVE, COMBINED_ALPHA, TEXEL0, 0, PRIMITIVE, 0, TEXEL0, K5, PRIMITIVE, COMBINED_ALPHA, TEXEL0, 0, PRIMITIVE, 0);

gsDPSetTextureImage(0, 3, 0, 0x8053DED0); // Width value is 0, thus actual width is 1?
// Tile 7?
gsDPSetTile(0, 3, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0); // Siz=3, Tile=7
gsDPLoadSync();
gsDPLoadBlock(7, 0, 0, 0x3FF, 0x80);
gsDPPipeSync();
// Tile 0?
gsDPSetTile(0, 3, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0); // Siz=3, Line=8
gsDPSetTileSize(0, 0, 0, 0x7C, 0x7C);
gsSPTextureRectangle(0x29C, 0x44, 0x314, 0xBC, 0, 0, 0, 0x44C, 0x44C);
```

After dumping `0x1000` bytes from `0x8053DED0` and adding a bitmap header, can confirm it is the
sword texture.
- Size: 32 x 32
- Fmt:  RGBA
- Bits: 32 per texel (8/8/8/8)

### Link Action-Based Flags

There seem to be three action-based state flags at `0x8040081C`:
- Relative to `z64_link_t`: `0x803FFDB0 +0xA6C`

- `0x8040081C`
  - Flags
    - `0x20000000` - Ocarina / transforming?
      - `0x20010040` - When talking to NPCs.
    - `0x10000000` - Ocarina / transforming?
    - `0x04000000` - Taking damage
    - `0x01000000` - Zora weapon is drawn, "Put Away" may display
    - `0x00800000` - On Epona
    - `0x00400000` - Using shield
    - `0x00200000` - Both Zora fins are in air
    - `0x00100000` - Aiming Zora fins
    - `0x00040000` - In air
    - `0x00020000` - Z-target view
    - `0x00008000` - Z-target on
    - `0x00002000` - Hanging from ledge.
    - `0x00001000` - Charging spin attack (no magic?)
    - `0x00000080` - Dead
    - `0x00000004` - Climbing ledge
- `0x80400820`
  - Flags
    - `0x08000000` - Ocarina?
    - `0x00400000` - Stationary on Epona (shows "Down" button)
    - `0x00200000` - Related to Z-target?
    - `0x00100000` - Tatl is out
    - `0x00080000` - Backflip, sidehop
    - `0x00020000` - Spin attack
    - `0x00002000` - Related to Z-target?
    - `0x00001000` - Stationary while climbing
    - `0x00000040` - Transforming?
      - Climbing
      - Hanging from ledge
      - Deku spinning
      - Goron ball
      - On Epona.
    - `0x00000020` - Running (and goron punch? might just be "moving")
    - `0x00000008` - Sometimes is set while running?
  - Notes:
    - In Goron ball-form: `0x00000060`
      - `0x00000068` while moving in ball-form with momentum
- `0x80400824`
  - Flags
    - `0x08000000` - Rolling
    - `0x02000000` - Attack (sword swing, zora punch, etc)
    - `0x00080000` - Goron spike-roll
    - `0x00020000` - Transforming (latter-half)?
    - `0x00000008` - Post-attack
    - `0x00000002` - Jump attack beginning

### Minimap Again

Probably writing Minimap display list instructions at: `0x80103270`
- Function: `0x801031D0`
- Return: `0x8010672C`
- Function only gets hit if minimap is enabled!

Jumps over call to function at: `0x801066A0`
- `T8 = *(void **)0x801F3F60`
  - ... which resolves to `0x803824D0`?
- Branches if: `*(uint16_t *)(0x803824D0 +0x0B52) != 0`
  - Address after math: `0x80383022`
  - Setting the `u16` at this address to 0 will enable the map, non-0 will disable.
- Not sure if any of this is clock-town specific.

TODO: Check where this value is written from, and figure out a hook to do variable-dependent
disabling of the L-button minimap toggle.

### Emulator Testing

Nemu64 actually draws D-Pad icon! However, errors:
- `Error: LoadBlock or LoadTile simulation without tmem failed`

### Our Draw Code (Debugging)

C-buttons function: `0x80118890`

Pointers (copy-paste from above):
- Context: `0x803E6B20`
- Gfx:     `0x801F9CB8`
- Overlay: `0x801F9F50‬`

- From: `0x8022EA60`
- To: `0x8022EC18`

- From: `0x8022EA58`
- To: `0x8022EC10`

Dump of display list when drawing 5 textures:

```
06 00 00 00 80 78 0B 10 E7 00 00 00 00 00 00 00
FA 00 00 00 FF FF FF FF FC 11 96 23 FF 2F FF FF
FD 70 00 1F 80 78 0B 78 F5 70 10 00 07 00 00 00
E6 00 00 00 00 00 00 00 F4 00 00 00 07 07 C0 7C
E7 00 00 00 00 00 00 00 F5 70 10 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 47 C1 40 00 43 C1 00
B4 00 00 00 00 00 00 00 B3 00 00 00 08 00 08 00
FD 18 00 1F 80 7A 00 00 F5 18 10 00 07 00 00 00
E6 00 00 00 00 00 00 00 F4 00 00 00 07 07 C0 7C
E7 00 00 00 00 00 00 00 F5 18 10 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 48 01 00 00 44 00 C0
B4 00 00 00 00 00 00 00 B3 00 00 00 08 00 08 00
FD 18 00 1F 80 7A 10 00 F5 18 10 00 07 00 00 00
E6 00 00 00 00 00 00 00 F4 00 00 00 07 07 C0 7C
E7 00 00 00 00 00 00 00 F5 18 10 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 4B 81 40 00 47 81 00
B4 00 00 00 00 00 00 00 B3 00 00 00 08 00 08 00
FD 18 00 1F 80 7A 20 00 F5 18 10 00 07 00 00 00
E6 00 00 00 00 00 00 00 F4 00 00 00 07 07 C0 7C
E7 00 00 00 00 00 00 00 F5 18 10 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 48 01 74 00 44 01 34
B4 00 00 00 00 00 00 00 B3 00 00 00 08 00 08 00
FD 18 00 1F 80 7A 30 00 F5 18 10 00 07 00 00 00
E6 00 00 00 00 00 00 00 F4 00 00 00 07 07 C0 7C
E7 00 00 00 00 00 00 00 F5 18 10 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 43 C1 40 00 3F C1 00
B4 00 00 00 00 00 00 00 B3 00 00 00 08 00 08 00
E7 00 00 00 00 00 00 00
```

#### OOTR's Draw Code (Broken)

When building the patched ROM without the randomizer itself, the D-Pad doesn't draw correctly???
- Draws black boxes instead.
- Is the randomizer python code fixing this after-the-fact???

Function that reads dpad sprite struct: `0x804049C0`
- Return: `0x80402F70`
- Return Function: `0x80402BC4`
  - Return from that: `0x80401FC4` (this is dpad draw assembly payload)

OoT addresses:
- Context: `0x801C84A0`
- Gfx:     `0x8011F290`
- Overlay: `0x8011F538`

Display list:
- From: `0x8018C9B8`
- To: `0x8018CA80`

Dump:
```
06 00 00 00 80 40 65 A0 E7 00 00 00 00 00 00 00
FC 11 96 23 FF 2F FF FF FA 00 00 00 FF FF FF FF
FD 70 00 1F 80 40 9B E0 F5 70 10 00 07 00 00 00
E6 00 00 00 00 00 00 00 F4 00 00 00 07 07 C0 7C
E7 00 00 00 00 00 00 00 F5 70 10 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 47 C1 40 00 43 C1 00
B4 00 00 00 00 00 00 00 B3 00 00 00 08 00 08 00
FD 18 00 1F 80 54 B9 C0 F5 18 10 00 07 00 00 00
E6 00 00 00 00 00 00 00 F4 00 00 00 07 07 C0 7C
E7 00 00 00 00 00 00 00 F5 18 10 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 47 41 64 00 44 41 34
B4 00 00 00 00 00 00 00 B3 00 00 00 0A AA 0A AA
E7 00 00 00 00 00 00 00
```

Generating:
- `06` instead of `DE`
- `B4` instead of `E1`
- `B3` instead of `F1`

Got it working with Majora's Mask by simply patching the instructions in memory to generate the
correct opcodes.

OMG I'M BUILDING FOR F3DEX INSTEAD OF F3DEX2 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

##### OOTR's Draw Code (Working)

ROM name: `OoTR_248216_CII0XZTZXA.z64`

DPad texture: `0x8040ADD0`
DPad sprite: `0x804067C0`
- Read breakpoint: `0x80404C28`
  - Function: `0x80404B9C`
  - Return: `0x80402F30`
  - Return Function: `0x80402BC0`
    - Return: `0x80401FC4` (dpad hook payload)

Display list:
- From: `0x8018C9B8`
- To: `0x8018CA80`

Display list dump:
```
DE 00 00 00 80 40 67 98 E7 00 00 00 00 00 00 00
FC 11 96 23 FF 2F FF FF FA 00 00 00 FF FF FF FF
FD 70 00 1F 80 40 AD D0 F5 70 10 00 07 00 00 00
E6 00 00 00 00 00 00 00 F4 00 00 00 07 07 C0 7C
E7 00 00 00 00 00 00 00 F5 70 10 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 47 C1 40 00 43 C1 00
E1 00 00 00 00 00 00 00 F1 00 00 00 08 00 08 00
FD 18 00 1F 80 54 B9 C0 F5 18 10 00 07 00 00 00
E6 00 00 00 00 00 00 00 F4 00 00 00 07 07 C0 7C
E7 00 00 00 00 00 00 00 F5 18 10 00 00 00 00 00
F2 00 00 00 00 07 C0 7C E4 47 41 64 00 44 41 34
E1 00 00 00 00 00 00 00 F1 00 00 00 0A AA 0A AA
E7 00 00 00 00 00 00 00
```

Seems correct?

Does it have something to do with my `n64` dependency or environment???

### Button Usable Bug

Bug due to calls in code to `0x80110038`, to check if an item should be usable.
C-button alpha going from `0x46` -> `0x20` when it should go from `0x46` -> `0xFF`.

Breakpoint on: `0x803FD776`
- Hit: `0x8010F098`
  - Return: `0x801212D0`

Return address for `0x80110038`:
- `0x8075F8E8`
- `0x8011298C`
- `0x80780AC0`

I think our call to `0x80110038` is reset-ing the alpha transition value at `0x801F3594`:
- `0x801213A4` tries to write `2`
- .. but then `0x8010EF90` writes `1` again
  - Function: `0x8010EE74`
  - Yep! Calls this function at *the very end* of the function at `0x80110038`.

#### On Original Game

Break on alpha of right C button: `0x803FD77A`
- Breaks: `0x8010F098`, writes `0x20` (from `A1`)
- Breaks: Same place, writes `0x40` (from `A1`)
- Breaks: Same place, writes `0x60` (from `A1`)
- ... same until `0xFF`.

It seems like our call to `0x80110038` might accidentally be breaking this "transition" of alpha
`0x20` to `0xFF`.

How does it know to increase by `0x20` per time?

- `0x801212B0`: Checks if greater than `0xFF`, and uses `0xFF` as max value if so.
- `0x80121278`: Gets the amount to set (in multiples of `0x20`) from `*(uint16_t *)(0x801EF670 +0x3F24)`
  - Absolute address: `0x801F3594`

### Bow Game Button Bug

Might be similar to the button display bug before.

Write breakpoint on right C button alpha: `0x803FD776`
- Link standing next to guy.
- Originally: `0xFF`
- Hit: `0x80102FA4`, write `0xDF`
- Hit: `0x80102FA4`, write `0x9F`
- Hit: `0x80102FA4`, write `0x5F`
- Hit: `0x80102FA4`, write `0x1F`
- Hit: `0x80102FA4`, write `0x00`

In the buggy patch, none of these breakpoints get hit at all until later.
- Link standing on steps to begin game.
- Hit: `0x80102FA4`, write `0xDF`
- Hit: `0x8010F088`, write `0x46`

### Health Jitter

Checks health value around `0x800D062C`.
- Checks if `<= 0x10`, which means 1 heart or less, which is when jitter occurs.

### Flag at `0x801F3586`

Type: `uint16_t`

Unaffected by pause menu? Might only be used outside of pause menu.

This likely indicates which area/scene Link is in.

Values:
- Area Transition: `0xFFFF`
- Boat Cruise Hut: `0x0013`
- Southern Swamp: `0x0C01`

### Magic Flag

Something keeps setting magic flag byte (`0x801EF753`) to `0x01` when changed to `0x00` manually.

Breaks on:
- `0x80121B0C`

Logic of resetting the flag:
- If `*(uint32_t *)(0x803FFDB0 +0xA6C) & 0x200 == 0`, continue?
  - If this is unset everything freezes, except UI animations?
- If `*(uint8_t *)(0x801EF670 +0x40) != 0`, continue.
  - After experimentation, this seems to be the main thing that controls the magic flag being reset.
  - If this value is `0x00`, the C-buttons UI bug doesn't occur when Deku flying.
- If `*(uint8_t *)(0x801EF670 +0x38) == 0`, reset to `0x01`.

### Memory Mapping

What writes to `0x801EF670`?
- `0x80144640`
  - Function: `0x80144628`
  - Uses hardcoded address, doesn't seem to be related to mapping.

Very first call to `0x80080C90` (`ReadFile`):
- Args:
  - `A0`: `0x8077F6F0`
  - `A1`: `0x00C7A4E0`
  - `A2`: `0x00000910`
- Return: `0x8008504C`
- Return Function: `0x8008501C`
  - `0x8008501C(uint32_t virt_start, uint32_t virt_end, uint32_t ram_start, uint32_t ram_end, ???);`
  - Return: `0x8008510C`
  - Return Function: `0x800850C8`
    - `0x800850C8(uint32_t virt_start, uint32_t virt_end, uint32_t ram_start, uint32_t ram_end);`
    - Return: `0x800B38C0`
    - Return Function: `0x800B3880`
      - `0x800B3880(void *addr);`
      - Points to some sort of memory-mapping struct of size `0x30`.

### Treasure Chest Game

When paying for the game, breakpoint hits on `0x800FF450` (`RNG_int_range`).
- `RNG_int_range((uint16_t)20, (uint16_t)80)`
- Return: `0x800BBBD0`
- Nevermind! This function with these parameters is called regularly?

Scene code seems to be calling `RNG_0` (`0x80086FDC`) once per frame (East Clock Town only does this once every few frames?)
- Return: `0x8040F570`
  - Uses `RNG_0` to determine whether or not to increment scene variable?
    - `*(uint8_t *)(0x80410460 +0x2AC)`
- It seems like scenes always call `RNG_set_seed` (`0x80086FD0`) per load.

### D-Pad Items From Day to Night bug

Can use D-Pad items after using Song of Double Time to go day to night, before the night thing occurs.

Quote:
> I encountered a bug tonight during the restream and I have highlighted the clip where the bug happened.
> I used the Song of Double Time 2-3 times in a row but it didn't progress from Night of First Day to Dawn of the Second Day and cost me some time.
> https://www.twitch.tv/videos/505825978

The C-button processing function `0x8074D29C` might be useful with this.
- It does not break when this occurs, whatever is calling it knows not to.
- It might even be useful to move D-Pad processing into this function? Maybe.

Function: `0x8074D29C`
- Return: `0x8074DA1C`
- Return Function: `0x8074D94C`
  - Still not called
  - Return: `0x8074F6D4`
  - Return Function: `0x8074F5FC`
    - Still not called
    - Return: `0x80750548`
    - Return Function: `0x807504E8`
      - Hits! Starting around end of Song of Time cutscene.
      - Return: `0x807675D8`

`0x807504E8` Branch Trace:
- `0x0520`: No branch
- `0x0530`: Branch to near end of function!
  - This means call to `0x8074AF20` is returning non-zero.

Function: `0x8074AF20`
- `bool 0x8074AF20(z64_ctxt_t *ctxt);`

```c
// ctxt: 0x803E6B20
bool func_0x8074AF20(z64_ctxt_t *ctxt) {
  void *addr = (ctxt + 0x18000);                // 0x803FEB20
  uint8_t value = *(uint8_t *)(addr + 0x875);   // 0x803FF395‬
  uint8_t value2 = *(uint8_t *)(addr + 0xB4A);  // 0x803FF66A
  return (value != 0) && (value2 != 0);
}
```

### Deku Bubble Disable Bug

This is a result of attempting to fix the C-button display when Deku hovering with magic.
- Which sets the magic_reset flag to `0` when hovering.

Apparently, when in Deku form and the magic_reset flag is `0`, the Deku B-button is set to `0xFD` (nothing?).
- However, when the magic_reset flag is changed back to `1`, the Deku B-button remains at `0xFD`.
- So we need to manually restore it.

- Read magic restore: `0x801105E0`
- If `0`:
  - Checks Deku B button: `0x801106E8`
  - If `9`:
    - Resets it to `0xFD`: `0x80110714`

This actually seems to be in the `0x80110038` function (which I called `z64_UpdateButtonUsability`).
- Return: `0x8011298C`

Caller functions checks `(*(uint8_t *)(0x803E6B20 +0x1CA5) & 4) == 0` for something.
- Whether or not to branch to call `0x80110038`?

### Pause Menu

Breaking on `0x80080C90` (`z64_LoadFile`) when entering pause menu.

- Args: `(0x8074AF20, 0xC90550, 0x179B0)`
  - Return: `0x8008504C`
  - Return Function: `0x8008501C`
- Args: `(0x8062D500, 0x9F5000, 0x14AF0)`
  - Return: `0x8075DAC8`
- Args: `(0x80641FF0, 0xA13000, 0x8A00)`
  - Return: `0x8075DB00`
- Args: `(0x8064B3F0, 0xA1C000, 0x2E0)`
  - Return: `0x8075DB78`

Exiting pause menu:

- Args: `(0x8058FF40, 0x108B000, 0x925E0)`
  - Return: `0x8012F700`
- Args: `(0x80622520, 0x11A5000, 0xBA30)`
  - Return: `0x8012F700`
- Args: `(0x80640770, 0x1710000, 0x3A70)`
  - Return: `0x8012F700`
- Args: `(0x806441E0, 0x179B000, 0x11C80)`
  - Return: `0x8012F700`
- Args: `(0x80655E60, 0x183F000, 0x15C0)`
  - Return: `0x8012F700`
- ...

Function with `0x8012F700` seems to be loading in via some sort of table.

Function `0x8012F698`:
- Args:
  - `A0`: `0x803FE8A8`
- Return: `0x8075F89C`

Seems to use `0x801C2740` as a base address for virtual address table?

Function: `0x8074AF28`
- Main pause menu function?
  - Only called for 10 or so frames while it sets up
- Return: `0x807579E8`
- Return Function: `0x8075705C`

Function: `0x8075705C`
- This function seems to run once-per-frame while the pause menu is up.
- Return: `0x8075D3C8`
- Return Function: `0x8075D258`

Function: `0x8075D258`
- Seems to start off by writing display list instructions?

#### Crashing It

Going to attempt crashing on menu.
- `0x8075D54C`

Successfully got a working debug menu.
- Code is very "corrupt" (mostly `0xFF`) where payload should be.
- Seems to be stable from `0x807A4000` to `0x807DA800`
  - Large chunk of "corrupt" data ends at `0x80797200`
  - ... however starting at `0x807A0044` some more data? Not much.
  - ... which seems to end at `0x807A3FCC`.
  - ... Woodfall crashes, uses up to `0x807A5E08`?
  - ... Lens of Truth crashes, uses up to `0x807A9E00`?
