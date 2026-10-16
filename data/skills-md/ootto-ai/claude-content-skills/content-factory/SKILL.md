---
name: content-factory
description: >
  The whole setup in one command — run the entire reel factory end to end. Claude takes a proven viral
  format, studies it frame by frame, writes an original hook + script in your voice, builds the finished
  reel (on-screen text, scene per beat, voiceover/music/captions/animations), writes the caption +
  hashtags, and wires the comment→DM lead loop — then repeats it 3× a day. This is the orchestrator that
  runs the other skills in order. Use when the user says "run the content factory", "make me a reel",
  "set up my whole content system", "how do you make these reels", "do the whole thing", "build my
  content machine", or "post for me every day".
user-invokable: true
argument-hint: "[your niche/topic + (optional) a viral reel URL to model + your @handle + a CTA keyword]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Content Factory — the whole setup, one command

**This is exactly how the whole page gets made.** One reel, idea → leads, then 3× a day. The Content
Factory is the *orchestrator*: it runs the other skills in order so you get a finished, on-brand reel
plus the lead loop — not just notes. Point it at a topic (and optionally a viral reel to model) and it
drives the entire pipeline.

> The individual skills each do one job. This one runs **all of them, in sequence**, and hands the
> output of each step to the next.

## The pipeline (what runs, in order)

```
0. CONNECT     onboarding .......... one-time: connect the Apify MCP (teardown) + the Composio MCP→Instagram
                                      (post + DM), and make sure Remotion is available (render). Ask if missing.
1. MEMORY      ai-brain ............. recall your voice + past winners (so it sounds like YOU)
2. FIND+STUDY  Apify ............... tear a proven reel down frame-by-frame + transcript
3. HOOK        viral-hook-writer .... 10 scroll-stopping hooks for the first 1–3s, ranked
4. SCRIPT      reel-scripter ........ tight 30–45s ORIGINAL script — your words, the proven structure
5. BUILD+RENDER reel-builder + Remotion (+ Seedance via Runway) ... the REAL rendered mp4
6. CAPTION     caption-and-hashtags . caption + tiered hashtags + a first comment built for saves
7. POST        Composio ............ actually publishes to your Instagram (after your OK)
8. LEADS       Composio ............ keyword rule LIVE — every comment → public reply + DM, 24/7
9. COMPOUND    ai-brain ............. save what worked back to memory → the next reel starts smarter
```

**This runs for REAL by calling the tools directly — it is a harness, not a description.** The creative
steps (3–6 script/hook/caption) are Claude; the execution steps use the underlying tools, no wrapper:
- **Step 0 CONNECT (once, at onboarding):** connect the **Apify MCP** (reel teardown/scraping) and the
  **Composio MCP → Instagram** (posting + comment/DM), and confirm **Remotion** is installed for rendering.
  If any of these is NOT connected, STOP and ASK the user to connect it (walk them through Apify, then
  Composio/Instagram) — never search for or reuse a key. This onboarding is what the whole loop depends on.
- **Step 2** uses **Apify** to actually tear down the model reel.
- **Step 5** renders the real mp4 with **Remotion** (+ **Seedance via Runway** for acting beats) — see
  [reel-builder](../reel-builder/SKILL.md) for the render harness.
- **Step 7** uses **Composio** to actually publish to the user's Instagram (pause for their OK first).
- **Step 8** uses **Composio** to wire the comment→DM lead loop so it fires live, 24/7.

If a tool isn't connected, do the creative pipeline (script + plan) and tell the user exactly what to
connect — Apify, then Composio/Instagram, plus Remotion — to make it run end to end. Never fake a render or a post.

## When to use
You want the *whole* reel + lead loop, not one piece. Run this as your daily driver. For a single step,
call that skill directly (e.g. just `/viral-hook-writer`).

## What you'll need
- Your **niche/topic** and **audience**.
- Optional but better: a **viral reel URL** in your niche to model the format (Claude studies it in step 2).
- Your **@handle**, your **voice** (a line or two, or via [ai-brain](../ai-brain/SKILL.md)), and a
  **CTA keyword** (e.g. `GUIDE`) for the comment→DM loop.

## Instructions

Run this prompt (or invoke `/content-factory`). Claude will move through the pipeline, pausing for your
go-ahead at the steps that matter (the format pick, and before posting).

```
You are my content factory. Run the whole pipeline end to end and produce a finished, on-brand reel
plus the lead loop. Work in this order, showing me each step's output before moving on:

CONTEXT
- Niche/topic: [what it's about]
- Audience: [who it's for]
- Model this viral reel (optional): [URL]   ← if none, suggest 3 proven formats in my niche, I'll pick
- My @handle: [@you]   ·   My voice: [a line, or "use ai-brain"]   ·   CTA keyword: [e.g. GUIDE]

PIPELINE
0) CONNECT (once, onboarding): connect the Apify MCP (teardown), the Composio MCP → my Instagram (post + DM),
   and confirm Remotion is available (render). IF ANY IS NOT CONNECTED, STOP AND ASK ME TO CONNECT IT — walk me
   through Apify, then Composio/Instagram — and wait; never search for or reuse a key. Only continue once connected.
0.5) ai-brain: recall my voice + past winners (if connected).
1) FIND+STUDY: use Apify to tear down the model URL (or your suggested pick) → hook, beats, pacing, visuals.
2) viral-hook-writer: 10 hooks, ranked; I'll pick one (or you pick the strongest).
3) reel-scripter: a 30–45s ORIGINAL script in MY voice on that structure (never a copy).
4) reel-builder + Remotion (+ Seedance via Runway): actually RENDER the reel → a real mp4 with the on-screen
   comment-CTA card. Show me the beat table + the rendered reel.
5) caption-and-hashtags: caption + tiered hashtags + first comment, with my CTA keyword.
6) POST: pause for my OK, then Composio actually publishes to my IG. If I say wait, just stage it.
7) Composio + comment-responder: wire the CTA keyword LIVE so every comment → public reply + DM, 24/7.
8) ai-brain: save the winning hook/format back to memory.

If a tool isn't connected, do steps 1–5 as the creative pipeline and tell me exactly what to connect
(Apify, then Instagram via Composio, plus Remotion) to make it run end to end — never fake the render or the post.

RULES
- Model the FORMAT, never the words — original script in my voice (copies get buried by IG Originality).
- The hook carries 80%: front-load it, payoff in the first ~1.5s, works on mute.
- Every line gets a visual; no static "text on a card" for a demo line.
- The public comment reply NEVER contains a link — the link goes in the DM only.
- Be honest: the CTA must deliver exactly what it promises.
```

## The daily loop (3× a day)
Run the factory three times a day, rotating the angle so the feed stays varied:
- **Result/proof** ("Claude made this — N views"), **how-to** (the steps), **contrarian** ("you're doing X wrong").
- Stagger morning / midday / evening. Feed every winner back into [ai-brain](../ai-brain/SKILL.md) so the
  next batch starts from what already worked for *you*.

## Memory makes it yours
Generic in → generic out. Connect [ai-brain](../ai-brain/SKILL.md) (Obsidian vault) first so every step pulls
from **your** proven hooks, voice, and swipe file — that's the difference between "AI content" and content
that sounds like you. Full setup: [ootto.ai/blog →](https://www.ootto.ai/blog)

## Honesty (non-negotiable)
- **Original only.** Model the technique; write your own words. Re-uploads/copies get reach-suppressed.
- **The CTA must be real.** If the reel says "comment GUIDE and I'll send it," the DM must actually send it
  (that's what [comment-responder](../comment-responder/SKILL.md) is for).
- **No links in public replies** — resource goes in the DM.

---

The manual version of the [Ootto](https://www.ootto.ai) content autopilot. These skills are do-it-yourself;
Ootto runs the whole thing for you. **[See it in 3 minutes →](https://www.ootto.ai)**
