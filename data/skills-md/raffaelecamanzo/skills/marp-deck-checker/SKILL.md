---
name: marp-deck-checker
description: Visual QA on the rendered PDF of a MARP deck. Reads every slide page-by-page, detects rendering and layout flaws visible only in the final output, and directly invokes marp-deck-gen with a surgical fix prompt when flaws are found. No report file is written.
---

# Marp Deck Consistency Checker

## Purpose

Perform visual QA on the rendered PDF of the deck. Detect layout and rendering flaws that only appear in the final output. When flaws are found, directly invoke `marp-deck-gen` with a targeted fix prompt — no report file is written.

---

## Inputs

| Input | Source |
|-------|--------|
| `output/<slugified-title>_<date>.pdf` | Most recently modified PDF in `output/` (auto-located) |
| `slides/deck.md` | Read to map page numbers to slide titles |
| `.marp/references/deck-template.md` | Used to judge what constitutes a flaw |

---

## Output

- **PASS**: inline message only, no file written
- **FLAWS FOUND**: invoke `marp-deck-gen` via Skill tool with a structured fix prompt; no file written

---

## Workflow

### Step 1 — Locate PDF

- List `output/` and select the most recently modified `.pdf` file.
- If no PDF exists: run `task pdf`, then re-check.
- If `task pdf` fails: stop and report the error.

---

### Step 2 — Read PDF

- Read the PDF using the Read tool (max 20 pages per call).
- For decks with more than 20 slides, make multiple Read calls with appropriate page ranges.
- Also read `slides/deck.md` to build a map of `page number → slide title`.

---

### Step 3 — Analyze each page

For each page, evaluate it against the flaw taxonomy below. Exempt slides:
- Frontpage, section dividers, and closing slides are **exempt** from F2–F12.
- They are still subject to **F1** (content overflow) and **F10** (title clipped at top).

#### Flaw taxonomy

| ID | Name | Description |
|----|------|-------------|
| F1 | Content overflow at bottom | Text or elements cut off at the bottom edge of the slide |
| F2 | Content misplaced on page | Content appears in the wrong region (e.g., body text in header area) |
| F3 | Content compressed | Content squeezed into a portion of the slide with blank space elsewhere |
| F4 | Vertical imbalance | Visible gap between title and body content (empty elements or excess spacing) |
| F5 | Diagram/image too small | Labels or details illegible at normal zoom |
| F6 | Text overlapping image | Text renders on top of or obscured by an image or diagram |
| F7 | Blank or near-blank slide | Content slide with almost no visible content |
| F8 | Missing slide title | Content slide with no title visible |
| F9 | Two-column imbalance | One column nearly empty, the other overloaded |
| F10 | Title clipped at top | Slide title visually cut off at the top edge |
| F11 | Process-flow content below card row | In process-flow layouts, content appears below the card row instead of inside it |
| F12 | Compact modifier needed but absent | Slide is clearly too dense but lacks the `compact` class modifier |

---

### Step 4 — Compile findings

- Build a list of all flaws found, keyed by page number and slide title.
- If no flaws are found: report **PASS** inline and stop.

---

### Step 5 — Invoke `marp-deck-gen`

If flaws are found, invoke `marp-deck-gen` using the Skill tool with the improvement prompt below.

After invoking `marp-deck-gen`, tell the user:
> "Re-run `task pdf` and then re-invoke the checker to confirm the fixes."

---

## Improvement prompt format

Pass the following as the prompt to `marp-deck-gen`:

```
VISUAL RENDERING FIX REQUEST
Fix only layout/structure of the listed slides. Do not change content.

Slide <N> — "<title>"
  Flaws: <flaw ID>: <short description of what was observed>
  Fix guidance: <concrete instruction from the table below>

[repeat for each affected slide]
```

---

## Fix guidance table

| Flaw | Concrete fix guidance |
|------|-----------------------|
| F1 — overflow (no `compact`) | Add `compact` modifier to the slide class |
| F1 — overflow (`compact` already present) | Rephrase and shorten body text to reduce volume while preserving meaning. Remove the least important bullet(s) as a last resort. |
| F2 — misplaced content | Review HTML container structure; ensure content is inside the correct layout column or section |
| F3 — compressed content | Remove unnecessary `<div>` wrappers or explicit height constraints that cage the content |
| F4 — vertical imbalance | Remove empty `<p>`, `<br>`, or spacer elements between title and body |
| F5 — image too small | Switch slide class to `image-wide` or `image-tall` based on the diagram's aspect ratio; increase diagram size if feasible |
| F6 — text overlapping image | Separate image and text into distinct layout columns; use `visual-split` or two-column class |
| F7 — blank slide | Verify asset paths (`../.marp/assets/<name>.png`) and that content is not hidden inside a broken HTML block |
| F8 — missing title | Add a `###` heading as the slide title; verify it appears before content blocks |
| F9 — two-column imbalance | Redistribute bullets evenly between columns, or collapse to single-column if one side is nearly empty |
| F10 — title clipped | Reduce title font size via inline style, or shorten the title text |
| F11 — process-flow below card row | Move stray content inside the card container; check that closing `</div>` tags are correct |
| F12 — compact absent | Add `compact` modifier to the slide class |

---

## Constraints on the deck-gen invocation

- Do **not** change slides not listed in the fix prompt.
- Fix layout and structure first (class tokens, HTML containers, modifiers).
- **Exception — overflow that cannot be resolved structurally:** if a slide already has `compact` and content still overflows (F1/F12), rephrase and shorten body text to reduce volume while preserving meaning. Remove the least important bullet(s) as a last resort. This is the only case where content may be changed.
- Re-read `.marp/references/deck-template.md` before applying fixes.

---

## Non-goals

- Do not write any report file.
- Do not rewrite content on slides not listed as flawed.
- Do not invent new slides or reorganize slide order.
- Do not make aesthetic changes not caused by a detected flaw.
