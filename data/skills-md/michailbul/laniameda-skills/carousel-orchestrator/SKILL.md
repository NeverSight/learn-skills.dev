---
name: carousel-orchestrator
description: >
  Orchestrate the end-to-end LinkedIn carousel creation pipeline.

  Use when the user asks to create/generate/iterate on a LinkedIn carousel or branded
  social slides.

  Handles: parse request → brief Codex (carousel-designer) → visual review → iteration
  feedback → deliver final PDF to Telegram.
---

# Carousel Orchestrator

End-to-end pipeline: user request → Codex generation → visual review → iteration → delivery.

## Step 1 — Parse the request

Extract from the user's message:
- **Topic**: what is the carousel about?
- **Key points**: explicit stats, ideas, or frameworks they want included
- **CTA keyword**: what should people comment? (infer if not given)
- **Tone**: default to brutalist-tech unless user says otherwise
- **Platform**: default to LinkedIn (1080×1350) unless specified

If topic is unclear, ask one question only: *"What's the main idea you want to get across?"*

## Step 2 — Set up project directory

```bash
PROJECT=~/work/carousels/$(date +%Y-%m-%d)-<slug>
mkdir -p $PROJECT/src $PROJECT/dist/slides
cp -r ~/.agents/skills/carousel-designer/scripts $PROJECT/
cp -r ~/.agents/skills/carousel-designer/assets $PROJECT/
cd $PROJECT && npm install playwright 2>/dev/null || true
```

## Step 3 — Spawn Codex

Read `references/brief-template.md`, fill it with parsed content, then:

```bash
codex exec --full-auto --workdir $PROJECT \
  "$(cat filled-brief.md)"
```

Wait for `RENDER_COMPLETE` in Codex output. Timeout: 5 minutes.

## Step 4 — Visual review

Load each PNG in `dist/slides/` with the image tool.
Run every check in `references/quality-checklist.md`.

**Decision:**
- All checks pass → go to Step 6
- 1–3 issues → Step 5 (feedback loop)
- Major structural issues → rebuild (back to Step 3 with amended brief)

Max iterations: **3**. After 3 loops, deliver best available and note issues to user.

## Step 5 — Feedback loop

Format feedback as structured diffs — never prose:
```
slide_1.headline: clips right edge — reduce font-size 148px → 120px
slide_3.metric-card: missing shadow-[16px_16px_0_0_#8566AF]
slide_7.closing: no CTA keyword — add "Comment THROUGHPUT and I'll send it"
```

Spawn Codex again with:
```
Fix the following issues in src/slides.html. Do not change slides not mentioned.
Re-run the render script when done. Print RENDER_COMPLETE.

[paste structured feedback]
```

Return to Step 4.

## Step 6 — Deliver

```bash
# Send PDF
message(send, filePath: $PROJECT/dist/carousel.pdf)

# Send cover slide preview
message(send, filePath: $PROJECT/dist/slides/01.png, 
        caption: "Carousel ready. 7 slides. Reply with any tweaks.")
```

## Reference files
- `references/brief-template.md` — fill this before spawning Codex
- `references/quality-checklist.md` — run this on every PNG set

## Platform specs
| Platform      | Size       | Slides | Format |
|---------------|------------|--------|--------|
| LinkedIn      | 1080×1350  | 5–10   | PDF document carousel |
| Instagram sq  | 1080×1080  | 5–10   | Images |
| Instagram story | 1080×1920 | 3–7  | Images |

*(Instagram templates: not yet built — request when needed)*
