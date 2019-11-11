Research
========

DeathBasket's Notes
-------------------

Apparently DeathBasket has even more MM notes than I thought:

- Website: https://sites.google.com/site/deathbasketslair/
  - RAM notes: https://sites.google.com/site/deathbasketslair/zelda/majoras-mask/ram-notes
- CloudModding notes: https://wiki.cloudmodding.com/mm/Notes/Deathbasket
- Pastebin: https://pastebin.com/u/DeathBasket
  - MM Postman Timer: https://pastebin.com/WDhtFM3K
  - MM Dog Race Stuff: https://pastebin.com/wb4TbqEA
- GitHub: https://github.com/az64

Other Notes
-----------

mzxrules' notes: https://github.com/mzxrules/-zelda

Filesystem / `DMATable`
-----------------------

Reference code for the filesystem structures can be found in xdaniel's [ozmav] source: [zelda.c]

Segment Addresses
-----------------

The RSP "maintains an array of 16 addresses" to reference data files. These are stored as
[segment addresses][SegmentAddresses].

In OoT, apparently the latter half refer to files such as:

- `icon_item_static`
- `icon_item_24_static`
- `icon_item_field_static`
- `icon_item_dungeon_static`
- etc.

This is likely applicable to Majora's Mask as well.

Majora's Mask Rom Data
----------------------

Rom data seems to end at around `0x02EDA3E0` for the decompressed MM rom.
- `0x02EE0000` might be a good place to place custom stuff, assuming we can jump this far?

[SegmentAddresses]:https://wiki.cloudmodding.com/oot/Addresses#Segment_Addresses
[ozmav]:https://github.com/xdanieldzd/ozmav
[zelda.c]:https://github.com/xdanieldzd/ozmav/blob/master/zsaten/zelda.c#L360
