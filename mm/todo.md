To-Do
=====

Custom code for Majora's Mask:
- [ ] Implement DPad support for Majora's Mask Randomizer
  - [ ] Find addresses for important memory structures/functions:
    - [x] `z64_file_t` struct.
	- [x] `z64_ctxt_t` struct.
	- [ ] "Use-Item" function.
	- [ ] "Equip-Mask" function, if different.
	- [ ] Location to hook per-frame code.
	- [ ] "Static Item" graphics map address.
- [ ] Try loading OoT/MM with Ghidra loader: [`N64LoaderWV`][N64LoaderWV].

Misc
----

MIPS64 toolkit:
- [ ] Figure out how to properly build MIPS64 `gcc` & friends.
- [ ] Make a repository of `PKGBUILD` files for them that work.
- [ ] Add a `Vagrantfile` for setting up a VM and installing them.
- [ ] In addition, maybe add `PKGBUILD` for [`n64`][glankk-n64] as well.

Rust Packages
-------------

Rust library/toolkit for modifying Zelda64 ROMs (`z64tools-rs`):
- [ ] Separate [`cargo-n64`][cargo-n64] code into `n64rom-rs` package.
- [ ] Pull request for adding keywords for [`yaz0-rs`][yaz0-rs]:
  - Keywords: `n64`, `nintendo64`
- [ ] Using the above, create `z64tools-rs` package.
  - Ideally support: ROM (de)compression, parsing DMATable, etc.

[cargo-n64]: https://github.com/rust-console/cargo-n64
[glankk-n64]: https://github.com/glankk/n64
[N64LoaderWV]: https://github.com/zeroKilo/N64LoaderWV
[yaz0-rs]: https://github.com/gcnhax/yaz0-rs
