Yaz0 Implementation Notes
=========================

## YazText

Takes entire source array, builds lookup table (one int for each source byte).
- Builds lookup table on init by iterating backwards.
- `last`: Maps: byte value => most recent index
- Builds `Lookup`: `Lookup[index] = prevIndexWithSameByteValue`

### `MatchNext` Loop

Get byte value at position, checks how many bytes previously was this byte value found.
- Follows these values backwards like a linked list, checking for matches up to a maximum number of bytes away?
