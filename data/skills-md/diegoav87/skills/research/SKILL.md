---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source. Open it with the date it was written and the exact versions it was verified against.
3. Save it where the repo already keeps such notes, or `docs/research/` if it keeps none, with the date in the filename.

When it reports back, give the user the file's path and the answer in a few sentences.

A note is never updated later. Newer findings go in a new dated note.
