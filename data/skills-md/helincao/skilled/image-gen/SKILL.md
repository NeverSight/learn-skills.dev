---
name: image-gen
description: Generate and iterate image assets with `scripts/image-gen/generate.mjs` from the installed skill directory. Use when asked to create visuals (PNG/JPG/WEBP/GIF), refine prompts, choose aspect ratios, or troubleshoot `.env` / `GEMINI_API_KEY` / CLI execution.
---

# Image Gen

## Inputs

- Prompt intent (subject + style + constraints)
- Output path with extension (`.png`, `.jpg`, `.webp`, `.gif`)
- Optional aspect ratio (see `references/cli.md`)
- Optional iteration goal (what to change from previous output)

## Preconditions

- `.env` must contain `GEMINI_API_KEY`
- Node.js runtime must support built-in `fetch` (Node 18+)

## Steps

1. Gather missing requirements before generating:
   1. Usage context (hero, icon, background, poster, etc.)
   2. Visual constraints (no text, no logo, no watermark, negative space, etc.)
   3. Aspect ratio and output path
2. If prompt quality is unclear, read `references/prompting.md` and construct a cleaner prompt.
3. If CLI flags/aspect options are unclear, read `references/cli.md`.
4. Run generation from project root:
   ```bash
   node "$SKILL_DIR/scripts/image-gen/generate.mjs" "<prompt>" -a <aspect-ratio> -o <output-path>
   ```
   `SKILL_DIR` is the directory containing this `SKILL.md`.
5. Confirm the output file exists and is non-empty.
6. If the user asks for iteration, keep output path versioned (for example `hero-v2.png`) unless overwrite is requested.

## Troubleshooting

- **`.env` not found**: put `.env` in your current directory or any parent directory (repo root is fine).
- **`GEMINI_API_KEY` missing**: set `GEMINI_API_KEY=...` in `.env` (never paste secrets into issues, logs, or docs).
- **`fetch` is not defined**: run with Node.js 18+ (the CLI relies on built-in `fetch`).
- **API request failed**: include the HTTP status + error body in the report; likely an invalid key, quota/rate limit, or model/API change.
- **Output path errors**: ensure the destination directory exists (the CLI doesn’t create directories).

## Output

- Generated image file at requested path
- Command used (prompt + flags) so the result is reproducible
- Optional iteration suggestions if user requests refinement
