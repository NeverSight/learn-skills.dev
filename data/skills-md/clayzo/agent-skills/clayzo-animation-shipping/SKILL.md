---
name: clayzo-animation-shipping
description: Ship an existing Clayzo animation as a web playback artifact or rendered media. Use for renderer selection, React or Next integration, assets and fonts, deployment, export preflight, loop verification, and approval of the exact revision being released.
---

# Clayzo animation shipping

Always read [shipping animations](references/shipping-animations.md).

Before final output, read both [previewing work](references/previewing-work.md) and [self-review](references/self-review.md). If the artifact loops, also read [loop design](references/loop-design.md).

Ship the exact reviewed revision. Confirm renderer coverage, fonts and assets (audio included), playback behavior, sound, deployment paths, and export constraints. Use `clayzo` commands and the stable `createPlayer()` / `PlayerHandle` renderer contract. Playback runtimes never authenticate.
