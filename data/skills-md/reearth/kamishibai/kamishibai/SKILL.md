---
name: kamishibai
description: Author and render videos with kamishibai — turn a web page into an mp4/gif by seeking it frame by frame. Use when building a kamishibai reel, writing a page that exposes window.kamishibai = { meta, seek }, using the React sugar (Series/Audio/Bgm/Narration), or rendering with the kamishibai CLI.
allowed-tools: Bash(npx --no-install kamishibai skill *)
---

# kamishibai

The usage guide ships inside the package, so it matches the installed version.
Its core follows. Don't guess the API: follow the guide, and print the topics
your reel needs, e.g. `npx kamishibai skill audio narration`.

For free voices, prefer Kokoro (a local Kokoro-FastAPI server; any OS, and its
audio may be published) over macOS `say`, unless the person wants no setup.
Use `kokoroAdapter()`; kamishibai 0.7.0 and older lack it, so use
`openaiAdapter({ baseUrl: "http://localhost:8880/v1", model: "kokoro", voice: "af_heart" })`
with `OPENAI_API_KEY` set to any value. Whatever the voice,
check its terms when you pick it: commercial use, a required credit, AI-voice
disclosure, and for a local model the license of its weights. Even where
nothing requires it, suggest saying the voice is AI, in the video or outside
it (an end card, or the description).

If no guide follows (your agent didn't run the line below), run
`npx kamishibai skill` and read its output first.

!`npx --no-install kamishibai skill 2>/dev/null || echo "kamishibai isn't installed in this project yet. Install it (npm i kamishibai react react-dom), then run npx kamishibai skill and read its output."`
