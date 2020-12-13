Keeta to Mountain Village Crash
===============================

Notes:
- Only happens on PJ64 for version 2+, when using recompiler but *not* interpreter?
- Simply having a breakpoint active (read/write/execute) during the Keeta cutscene will prevent the crash?
- Reloading state from directly after Keeta cutscene will prevent the crash.
  - ... but reloading state from textbox before cutscene won't.
- Does not crash if Snow Head temple is cleared (flag at `0x801F0589`).

## Breakpoint Investigation

Narrowing down where the issue is using breakpoints:
- Does not crash if a breakpoint is enabled during:
  - "May I take leave, sir?" textbox to end of cutscene.
  - "Yes, sir!" textbox to end of cutscene.
  - After bones collapse to end of cutscene.
