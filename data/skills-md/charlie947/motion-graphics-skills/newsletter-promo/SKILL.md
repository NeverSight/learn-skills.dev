---
name: newsletter-promo
description: Turn a newsletter edition into a 12-20 second promo clip for LinkedIn, Instagram or X that drives people to read and subscribe. Hook question, three proof frames from the edition, then the newsletter name and where to read it. Use when someone says "promo for my newsletter", "trailer for this edition", "get people to my Substack", "teaser video" or "promote this issue".
---

# Newsletter promo, built in code

A promo does one job: make someone want the full edition. Show the best bits, never the whole thing.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them.

## Step 1: Ask for four things, then wait

1. **The edition link** or the full text. Read it before anything else.
2. **The hook.** The one question or promise the edition answers. If none is given, propose three from the edition's own lines and wait for a pick.
3. **Three proof frames.** Real images, charts or clips from the edition. Attached files only.
4. **The ending card,** word for word: newsletter name, where to read it, and an optional subscriber count with its source.

## Step 2: Structure (15 seconds)

| Time | Frame |
|---|---|
| 0-3s | The hook, big. A question works better than a statement. |
| 3-11s | Three proof frames, about 2.5s each, each with a 3-5 word label. |
| 11-15s | Newsletter name, "Read it free at [URL]", held still. |

## Step 3: Build brief (paste into Claude Code)

```
Build one self-contained HTML file called index.html: a 15-second promo at [WIDTH] x [HEIGHT] for my newsletter edition, using only the files I attached.

Hook (0-3s): "[HOOK]" in bold condensed type, [TEXT] on [BG], key words in [ACCENT].
Proof (3-11s): my three attached images in this order, each held about 2.5 seconds with a slow push-in and this label: [LABEL 1], [LABEL 2], [LABEL 3].
End card (11-15s): "[NEWSLETTER NAME]" and "Read it free at [URL]". Hold still, readable on a phone.

Banned: typewriter text, glow, bouncing, gradients on text, any claim or number not in my brief.

Build rules: every frame from the time alone, window.seek(seconds), wait for seek when the URL has ?render. Capture one frame per shot and check every label is readable at phone size.
```

## Step 4: Export and post

Export 1080 x 1350 for LinkedIn and 1080 x 1920 for Stories and Reels. Put the edition link in the first line of the caption, not only the comments.
