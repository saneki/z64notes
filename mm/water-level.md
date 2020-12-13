Water Level
===========

In Great Bay Coast, getting water height (?) from: `0x806BB3B4`
- Getting this pointer from: `*(void**)0x801F99DC` (note: this is arbitrary stack address)
- Scene data is: `0x806B1FD0`, so likely in scene data.
- This controls the collision of water, but not the texture/polygons.

Drawing water:
- Writes segaddr 3 used to draw: `0x803FF20C`, or: `*(void**)(room_ctxt.rooms[0].file +0xC)`
  - So this points to room-related data.
  - Writes at: `0x8012D8C8`
- Writes the `G_DL` at: `0x8012DEB8`
  - Function start: `0x8012D750`
  - Seems like it's iterating list of offsets into room data, and writing as `G_DL` instructions?
  - Builds data similar to linked-list on stack, and iterates using "next" pointer of each entry.
- `0x8012D9B8`: Calling function to resolve segaddr, ex: `0x03000A6C`
  - Gets this segaddr from: `*(void**)(room_ctxt.rooms[0].mesh_hdr +0x4)`
  - So likely drawing meshes?
  - May be building linked-list in stack, to organize meshes by "Z" index, for determining which should draw before others.
    - Would make sense due to ease of "inserting" of linked-lists.
