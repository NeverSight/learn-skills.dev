---
name: generate-media
description: Use when generating or editing an image or video with an AI model — ads, mockups, style variations, image-to-video. Calls a provider API (OpenRouter today), saves the file outside the repo, and reports what it actually cost.
user-invocable: true
argument-hint: "[<what to generate>]"
---

# Generate Media

One generation per invocation through a provider API. The file lands in `$HOME/.cache/generate-media/`.

Provider reference — read before the first API call:

- OpenRouter (default): [providers/openrouter.md](providers/openrouter.md)

## Rules

1. **Stop if the provider key is missing.** For OpenRouter that is `OPENROUTER_API_KEY` — check `.env` in the project root, then the environment. Never write a key into a tracked file. If missing, point the user at <https://openrouter.ai/settings/keys> and stop.

2. **Look up model IDs from the API. Never guess them.** IDs change and a wrong one wastes a paid round trip.

3. **Pick the cheapest model that meets the need**, unless the user named one. Exceptions worth saying out loud: `openai/gpt-image-2` for legible text inside an image, a `-pro` tier when the user asked for production quality.

4. **Quote the cost before calling, and only quote a figure you can source.** Video runs 10×–50× an image.
   - Video: use the per-second table in the provider reference. No row there means no published rate — say so and wait.
   - Image: unquotable before the call (`pricing.image_output` is per output token, not per image). Name the model, say the cost lands after the response, and go ahead — a still is normally a few cents.
   - Wait for the user when a sourced figure exceeds ~$0.50, or when a video price is unknown.

   Settle motion on a cheap draft before paying for a real render: `bytedance/seedance-2.0-mini` is ~$0.08 for 6 s at 720p, less at 480p. Price scales with `width × height × duration`, so halving the resolution is the cheapest way to test an idea.

5. **Save to `$OUT_DIR/<slug>.<ext>`, where `OUT_DIR="$HOME/.cache/generate-media"`.** `mkdir -p` it first. Write `$HOME`, never a bare `~` — a quoted tilde does not expand and drops a literal `./~/` directory into the project. Never overwrite — add a numeric suffix. Never leave a result only in the API response. Copy into the project only when the user asks; raw output is 2–3 MB stills and 6 Mbps clips, which should not enter git.

6. **Report the absolute file path and the real cost** from `usage.cost` in the response, never an estimate.

## Check before reporting done

- The file just written is non-empty: `test -s "$OUT"` — a failed base64 decode leaves 0 bytes. Check that one path, not the whole directory; it is shared across every project and holds old results.
- A video is an actual `.mp4`, not a JSON error body: `file "$OUT"`.

## Common mistakes

- **Treating video as synchronous.** `POST /videos` returns `202` with a `polling_url`. Poll ~every 30 s until `completed`, then download.
- **Estimating cost from a pricing field.** Read `usage.cost` from the response.
- **Piping base64 straight into a file.** Decode it: `jq -r '.data[0].b64_json' resp.json | base64 -d > out.png`.
- **Sending a local path as a reference image.** Reference inputs take an HTTP(S) URL or a base64 data URL.
