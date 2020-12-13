Get-Item
========

## Drawing

Draw function for when getting item: `0x800EE320(z2_game_t *game, s16 graphic)`.

Struct Table: `0x801BB170`
- Each entry is size `0x24`, first field is callback function for drawing the Get-Item model.
- Table ends at `0x801BC208`.
- Contains `0x76` entries.

### Heart Piece

Heart Piece (`graphic_id_minus_1 = 0x13`) calls: `0x800EF2AC`
