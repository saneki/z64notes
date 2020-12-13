Garo Hints
==========

Garo & Spawner variables table (CVS format):

```
Spawner Variable, Garo Variable, Location
0x2041, 0x0, Ikana Valley Bottom #1
0x20C0, 0x1, Ikana Valley Bottom #2 (Near Dock)
0x2145, 0x2, Ikana Valley Top #1 (Near Cave)
0x21C2, 0x3, Ikana Valley Top #2 (Near Ikana Castle)
0x2243, 0x4, Ikana Valley Top #3 (Near Owl)
0x22C4, 0x5, Ikana Valley Top #4 (Near Stone Tower)
0x2349, 0x6, Ikana Castle #1 (Right of Entrance)
0x23CA, 0x7, Ikana Castle #2 (Left of Entrance)
0x244B, 0x8, Ikana Castle #3 (Entrance)
0x24CC, 0x9, Ikana Castle #4 (Roof)
```

Mapping of Garo variable to message Id:
- `0x0`:  `0x139A`
- `0x1`:  `0x139B`
- `0x2`:  `0x139D`, or `0x13A1` with storms (cave flag).
- `0x3`:  `0x139E`, or `0x13A2` with storms (cave flag).
- `0x4`:  `0x139F`, or `0x13A3` with storms (cave flag).
- `0x5`:  `0x13A0`, or `0x13A4` with storms (cave flag).
- `0x6`:  `0x13A5`
- `0x7`:  `0x13A6`
- `0x8`:  `0x13A7`
- `0x9`:  `0x13A8`
- `0xA+`: `0x139C`, probably fallback for invalid index.
- Has Elegy: `0x139C`
