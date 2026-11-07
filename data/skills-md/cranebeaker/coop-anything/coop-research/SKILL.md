---
name: coop-research
description: Find every existing co-op attempt for a game, its newest build, its bug reports, and co-op work on other games with the same engine. Use before writing any code.
---

# Co-op research

- Search with several phrasings and in the fan base's languages; GitHub code, repos, forks and non-default branches; ModDB, Nexus, archive.org, Steam guides, Reddit, the game's Discord.
- Never report "nothing exists" without listing what was searched. Write `searched:` notes.
- For each find: link, author handle, license, last confirmed activity, what it really syncs (players visible, story, enemies, world, items), where bug reports live, newest build verified by hash or version string.
- Bug reports from Discord: follow `playbook/discord-export.md` (Terms of Service first, never handle tokens in chat).
- Add or correct entries in `data/directory.yaml`, run `python tools/build_directory.py`.

Details: `playbook/research.md`, `playbook/engine-families.md`.
