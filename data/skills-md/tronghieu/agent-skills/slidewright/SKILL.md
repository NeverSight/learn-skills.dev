---
name: slidewright
description: >-
  Build interactive presentation websites — slide decks projected to a room, controlled
  by one presenter. Use this skill WHENEVER the user wants to create, build, or design a
  presentation, slide deck, talk, or "bài thuyết trình / slide / trình chiếu", and also
  when they ask to add/edit slides, restyle a deck, scaffold a new presentation project,
  reuse their presentation setup in another repo, control slides from a phone (remote,
  QR code, "điều khiển slide bằng điện thoại"), or export slides to PDF — even if they
  don't say the word "slide" but clearly need projected talk visuals (e.g. "I'm giving a
  talk next week and need visuals", "dựng deck cho buổi chia sẻ", "làm mấy trang chiếu
  cho hội thảo"). Supports two tracks: a zero-build single HTML file, or a Vite + React
  project. Do NOT use it for printable documents, normal web apps, or dashboards meant
  for individual users to interact with.
---

# Interactive presentation builder

Build slide decks that run as a website and are **projected to a room**. The deck is the
visual half of a talk; the presenter does the talking. Two ways to build, one shared
design language.

## First, the mental model (read before writing any code)

There is **one operator** (the presenter) on **one machine**. Slides go on a big screen;
the audience only **looks** — they never click, type, or interact. Everything below
follows from this. Four failure modes to avoid:

- **Text too small.** Slides are read from across a room, not on a laptop. Never use
  web-reading sizes (`text-sm`, `16px`) or fixed Tailwind text classes (`text-4xl`).
  Always use fluid `clamp()` so text scales with the screen. Honour the typography floor
  (body ≈ 30–36px, never below 28px on a 1080p canvas). See `references/design-system.md`.
- **Content hugging an edge.** Padding is a two-layer contract. Slide content must stay
  inside the viewport safe area, and content inside a card, panel, callout, bordered box,
  or other visible container must stay inset from that container's own edge. A parent
  slide's padding does not protect a nested container; `gap` and child margins are not a
  substitute for the container's own padding. Both scaffolds provide safe-area padding
  and a `.slide-surface` inset helper. Even `fullBleed` slides keep text content inset.
- **Building an app.** No input fields, no "Submit", no login, no data collection — there
  is no backend and nowhere for data to go. Interaction is only the presenter clicking to
  reveal/advance content. If a component asks "where does this data go?", it's wrong.
- **Wrong voice for the audience.** A board report is not a lesson and a pitch is not a
  status update. The deck type sets the structure and the voice. Decide it first — see
  `references/deck-types.md`.

The presenter may hold a **phone remote** (scan a QR code from the terminal, then tap
Next/Prev). It is the same single operator on a second device, not audience interaction.

`references/design-system.md` is the heart of this skill — the typography floor, two-layer
padding contract, content overflow, layout recipes, motion, and palette. Read it whenever
you design or restyle slide content.

## Workflow

1. **Understand and clarify the talk.**
   - **Content:** If the presentation content is vague or unclear, ask questions to clarify the topic, audience, speaker (name/role), and key message before building. For Vietnamese content, the default voice is plain, honest, direct — no marketing hype.
   - **Deck type:** Decide what the deck is for before writing: report upward, decision request, pitch, training, talk, or internal update. Infer it from the request and tell the user your choice in one line; ask only when two types fit equally. Then read `references/deck-types.md` and follow that type's arc, voice, and prohibitions.
   - **Style:** Ask the user for their preferred visual style and suggest these 5 modern options:
     1. *Minimalist Bauhaus*: High contrast, geometric typography, generous whitespace.
     2. *Dark Mode Cinematic*: Deep slate/black backgrounds, dramatic contrast, glowing accents.
     3. *Editorial / Magazine*: Sophisticated font pairings (serif + sans), structured grid layouts.
     4. *Glassmorphism*: Soft background gradients with blurred, translucent content panels.
     5. *Neo-Brutalism*: Bold typography, raw borders, hard shadows, high energy.
2. **Pick a track** (below). If unsure, ask once; otherwise default to plain HTML for
   small/quick decks and React for substantial, maintained talks.
3. **Scaffold** with the matching script — don't hand-assemble the boilerplate.
4. **Build slides** in the arc and voice of the deck type, following
   `references/design-system.md`: one idea per slide, few
   words, real visuals, projection-legible type, presenter-only interaction, and the
   two-layer padding contract for both viewport and content containers. Respect the
   density limits — never exceed 5 bullets, ~60 words, or 5×4 table cells per slide.
   If content doesn't fit at the typography floor, split into more slides — never shrink
   past the floor and never produce a slide that scrolls vertically.
5. **Keep the required chrome:** a visible bottom navigation slider (dot strip) and slide
   number. Both scaffolds include it — don't remove it.
6. **Write speaker notes** in the `<deck-name>-notes.md` file the scaffold creates (never
   on the slides themselves).
7. **Run the verify script** to catch text-too-small and content-too-dense violations:
   ```bash
   bash /mnt/skills/user/slidewright/scripts/verify-slides.sh <path-to-deck>
   ```
   Fix every reported issue before proceeding.
8. **Run the spacing audit before handoff.** Check every slide at 1920×1080 and at one
   smaller viewport. No text or primary content may cross the viewport safe area. For
   every element that draws a visible boundary (`background`, `border`, `outline`,
   `shadow`, rounded surface, or text-overlay panel), verify that its content has
   padding on all four sides. Media and purely decorative edge-to-edge layers are the
   only exceptions; text over them belongs in a nested padded surface.
9. **Tell the user how to present with the phone remote.** Both scaffolds include it.
   The HTML track runs `node <deck>/slidewright-remote.mjs`. The React track runs `npm run dev`.
   The terminal prints a QR code for the phone. See `references/remote-control.md`.
   Keep the deck's `window.slidewright` API and `slidewright:change` event when you edit
   navigation code.
10. **Export to PDF** if asked — see `references/export-pdf.md`.

Put each deck in its own folder. Keep any live-demo app as a separate project, not inside
the deck.

## Choosing a track

| Pick | When | Reference |
| --- | --- | --- |
| **Plain HTML** | Zero setup wanted; runs by opening a file; quick deck; shareable anywhere; no toolchain. Gets unwieldy past ~15–20 rich slides. | `references/html-track.md` |
| **Vite + React** | Many slides, reusable components, state-driven interactions, TypeScript, Framer Motion, maintained/re-run talks. | `references/react-track.md` |

Both produce the same projected experience and obey the same design system; they differ
only in implementation.

## Scaffolding

**Plain HTML** — single self-contained `index.html`, Tailwind via CDN, no build:

```bash
bash scripts/new-html-deck.sh <deck-name> [target-dir] [--title "Deck title"]
```

**Vite + React** — scaffolds with the official Vite tool and installs the **latest**
React, Tailwind, Framer Motion, and Lucide (versions are intentionally not pinned, so
each deck starts on current tooling), then layers the `App → Deck → Slide` architecture:

```bash
bash scripts/new-react-deck.sh <deck-name> [target-dir] [--no-install]
cd <deck-name> && npm run dev
```

Both scaffolds include the phone remote (`slidewright-remote.mjs`, zero dependencies).
For a deck scaffolded before the remote existed:

```bash
bash scripts/add-remote.sh <path-to-deck>
```

After scaffolding, read the matching track reference for how slides are structured and how
to add/reorder them, then build the content.

## Files in this skill

- `references/design-system.md` — projection rules, typography floor, layout recipes,
  motion, palette. The core; consult for any content/design work.
- `references/deck-types.md` — the six deck types and each one's arc, voice, and
  prohibitions. Read it before writing slide content.
- `references/html-track.md` — plain-HTML deck structure, template internals, adding slides.
- `references/react-track.md` — Vite+React architecture, slide ordering, Tailwind wiring.
- `references/export-pdf.md` — PDF export options and speaker-notes convention.
- `references/remote-control.md` — phone remote: running it, the deck API contract,
  security, troubleshooting (wrong IP, firewall, venue Wi-Fi).
- `scripts/new-html-deck.sh` — scaffold a plain-HTML deck.
- `scripts/new-react-deck.sh` — scaffold a Vite + React deck.
- `scripts/add-remote.sh` — add the phone remote to an existing deck.
- `assets/remote/slidewright-remote.mjs` — the phone remote: WebSocket relay, remote
  page, terminal QR code, static server (HTML track) and Vite plugin (React track).
  The scaffolds copy it into each deck; edit this source, not the copies.
- `scripts/export-deck-pdf.py` — export a deck to a content-complete PDF (waits for render
  and reveals hidden content; image-based).
- `scripts/verify-slides.sh` — static analysis of deck files: flags text below the
  typography floor, fixed-px font sizes, excessive bullet counts, and high word density
  per slide. Run after building slides and before handoff.
