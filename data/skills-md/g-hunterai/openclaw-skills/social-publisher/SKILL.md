---
name: social-publisher
description: In-house social publishing pipeline. Slideshow rendering, multi-platform posting, content queue, analytics tracking. Replaces Genviral.
---

Use this skill to run a local social publishing pipeline in Bash + FFmpeg.

## Quick start

1. Configure environment variables documented in `docs/setup.md`.
2. Add queue items with `scripts/publisher.sh queue add --file <json>` or import Genviral data with `scripts/import-genviral.sh --file <json>`.
3. Render slideshow outputs with `scripts/publisher.sh render slideshow --id <id>`.
4. Review preview outputs with `scripts/publisher.sh render preview --id <id>`.
5. Publish with `scripts/publisher.sh post send --id <id>`.
6. Check analytics with `scripts/publisher.sh analytics summary`.

## Notes

- `queue/queue.json` is the source of truth for content state.
- `PUBLISHER_PAUSED=true` blocks posting commands.
- Use `--yes` to bypass confirmation prompts for destructive actions.
## Pitfalls
- Document failure modes as you encounter them
