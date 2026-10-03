---
name: arena
description: "Compatibility entry for agi-mode Arena: generate independent candidates, compare them, select a base and verify a synthesis. Use for /arena, 'arena this', or an explicit request for competing designs."
disable-model-invocation: true
---

# Arena

The maintained workflow now lives in **agi-mode**. Read and execute [Arena](../agi-mode/playbooks/arena.md), which owns framing, runner selection, isolated candidates, anonymous judging, selection, grafting and verification.

Preserve the caller's task, candidate count, runner preferences and scope. Calling Arena does not start an improvement loop; if already inside Hillclimb, return candidates and evidence to its existing record.

Resolve the sibling path or the registered installation of `agi-mode`. This compatibility entry requires that skill; if unavailable, report the missing dependency rather than inventing candidates or judging results.
