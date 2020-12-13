Tries reading form (`0x801EF690`) at:
- `0x8075016C`

Assigning C button values:

When swapping left & down C buttons:
- Assigns left at:
  - `0x8075DD94`
    - Function: `0x8075D7DC`
- Assigns bottom at:
  - `0x80751E14`
    - Function: `0x80751504`

Assigning Ocarina to left C button:
- `0x80751BD4`
  - Function: `0x80751504`
  - Return: `0x8075DD94`
  - Return Function: `0x8075D7DC`

Assigning to bottom C button:
- `0x80751E14`
  - Return: `0x8075DD94`
    - Same return address as left C button?

Function `0x8075150C`
- Signature: `func_0x8075150C(z64_ctxt_t *ctxt);`
