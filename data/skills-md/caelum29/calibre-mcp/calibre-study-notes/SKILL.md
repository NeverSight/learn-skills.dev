---
name: calibre-study-notes
description: >
  Generate active-learning study notes (конспекти) from books in the Calibre
  library, for a HUMAN learner — not an agent skill. Produces a markdown note
  built for retention: questions-first sections, own-words concepts, reader-domain
  examples, self-test with source pointers, Anki export, spaced-review metadata.
  Also runs interactive review (quiz) sessions over existing notes.
  Use for: studying a topic, a theme, or a chapter of a book from the library.
  Single-book agent-skill distillation belongs to `calibre-distill`; multi-book
  topic skills belong to `calibre-distill-topic`. This skill is for notes a
  person will study from.
  Triggers: "конспект", "законспектуй", "зроби конспект", "хочу вивчити",
  "розібрати розділ", "розбери главу", "study notes", "make notes on",
  "learn this chapter", "підготуй матеріал для вивчення", "повтори зі мною",
  "review my notes", "поганяй по конспекту", "quiz me on".
---

# calibre-study-notes

Turn a chapter/topic from the user's Calibre library into a study note a human
can actually learn from — or run a review session over an existing note.

**Audience is the human learner.** Everything follows from that. A perfect
prose summary is a FAILURE here: reading a finished summary bypasses the
generation effect (people retain what they process, not what they read).
The note must force processing: questions before answers, hidden answers,
retrieval prompts, blanks for the reader's own words.

## Modes

| Mode       | What it produces | When |
|------------|------------------|------|
| `generate` | Full study note file (default) | "законспектуй розділ X" |
| `scaffold` | Structure + questions + source pointers only; body left as fill-in blanks for the human | User wants maximum retention / asks to "fill it myself" |
| `review`   | Interactive quiz session in chat over an existing note; no new file | "поганяй мене по...", "review", or a note's `next_review` date has passed |

Depth (orthogonal to mode):
- `quick` — TL;DR + core concepts + 5 self-test questions. No diagrams, no
  cross-library search. Default when the user asks casually or the runtime
  model/budget is constrained.
- `deep` — full template: reader-domain examples, diagrams, `scope: library`
  cross-check, Anki block, misconceptions, full verification. Default when the
  user says "глибоко", "детально", or is preparing for interviews/exams.

If mode/depth are ambiguous, infer from phrasing; do not ask about them
separately — fold into the scoping step below.

## Workflow (generate / scaffold)

### 1. Scope — before touching the book

Establish, from context or by asking (ONE compact question, not an interview):
- **Reader level** in this topic: new / adjacent experience / refreshing.
- **Goal**: interview in N days / deep study / working reference.
- **Scope**: one chapter, several chapters, or a topic across the book.
  A topic across ≥3 books → suggest `calibre-distill-topic` instead.

Skip anything already answerable from the conversation or user context.
Reader level and goal directly set depth, number of examples, and analogy
domain — do not proceed without them.

### 2. Locate and map the source

1. `calibre_search` (mode: meta) → book id, if not given.
2. `calibre_get_content` with `structure: true` → chapter map with cursors.
3. Confirm with the user which chapter(s) match their ask if the mapping
   is not obvious (chapter titles often differ from topic names).

### 3. Targeted retrieval — never "read everything"

1. Read the target chapter(s) via cursor walking (`calibre_get_content`).
2. For each core concept that feels under-covered after the chapter read,
   run `calibre_semantic_search` with `scope: book` to pull clarifying
   passages from elsewhere in the same book.
3. **deep only:** `calibre_semantic_search` with `scope: library` on the 2–3
   central concepts — if other books on the shelf explain them differently,
   capture that in a "Де джерела розходяться" note inside the relevant
   concept section. Do not turn this into a second research project: one
   query per central concept, top hits only.

### 4. Write the note

Follow `references/template.md` exactly for structure. Non-negotiable
invariants (also enforced in step 5):

- **Own words everywhere.** No verbatim passages. Quotes: at most one per
  source, under 15 words, only when the exact phrasing is the point.
- **Compression floor:** note body ≤ 10–15% of the source chapter length.
  Longer means you are writing a displacive retelling, not a study note.
- **One idea = one section** (Zettelkasten atomicity). Each concept section
  answers: what it is (own words) → why it exists / what problem it solves →
  example → typical misconception.
- **Questions come before answers.** Every concept section opens with 2–3
  guiding questions. Answers to self-test questions go inside `<details>`.
- **Examples from the reader's domain.** If the reader's stack/domain is
  known (from context or scoping), generate examples and analogies from it —
  not abstract foo/bar. Code examples are written fresh, never copied.
- **Every self-test question carries a source pointer** — chapter + cursor
  (or page) so the human can verify against the book, not against the note.
- **Anki block** at the end: `Q;A` pairs, importable, ≤1 fact per card.
- **Language:** write the note in the user's language (default: Ukrainian),
  keep domain terms in original English.

`scaffold` mode: same template, but concept bodies are replaced with the
guiding questions plus a blank prompt (`_Твоє пояснення:_`) and the source
pointer. Self-test and Anki sections are still generated in full.

### 5. Diagrams — earn their place

A diagram is justified only when the concept has structure that prose conveys
worse: topology, state sequence, distribution, flow, scale comparison.
Definitions, principles, trade-offs = text. Never one-diagram-per-section.

Mermaid rules (portability across Obsidian/GitHub/VS Code renderers):
- Allowed types: `flowchart`, `sequenceDiagram`, `stateDiagram-v2`,
  `classDiagram`, `erDiagram`. Nothing experimental.
- All labels containing non-alphanumeric characters go in double quotes.
- ≤8 nodes per diagram; more → split into overview + detail.
- Accept Mermaid's auto-layout; do not fight it with hacks.

Leave interactivity hooks in the note where a live widget would help:
`> 💡 У review-сесії попроси: "покажи інтерактивно <concept>"`.

### 6. Verify before finalizing

Run every check whose capability is available; skip silently otherwise:
- **Verbatim gate:** if the repo's `scripts/legal-gate.mjs` is reachable via
  shell, run it against the note (`--book <id>`). Fix any overlap findings.
- **Mermaid validation:** if shell is available, extract every ```mermaid
  block and run `npx -y @mermaid-js/mermaid-cli -i <block> -o /dev/null`;
  fix parser errors and re-run until clean.
- **Self-check (always):**
  - every self-test question is answerable from the note OR carries an exact
    source pointer;
  - compression floor holds;
  - no section violates questions-first;
  - Anki cards are atomic;
  - front-matter is complete (see template).

### 7. Save and register

- Write the note to the user's notes location. Ask once per session if
  unknown; remember the answer. Sensible default inside an Obsidian vault:
  `study-notes/<book-slug>/<chapter-or-topic-slug>.md`.
- Front-matter must include `next_review` (first interval: +1 day).
- **Optional, only with user consent and gated writes enabled:** stamp the
  book in Calibre — add tag `studied:<topic-slug>` via `calibre_update_book`.

## Review mode

Trigger: user asks to review, or an existing note's `next_review` has passed
and the user touches that topic.

1. Locate the existing note (filesystem). If none exists — offer to generate.
2. Run the self-test **as a dialog, one question at a time**. Wait for the
   user's answer before showing anything. Give feedback in own words;
   on a wrong/shaky answer, pull the exact source passage via
   `calibre_get_content` with the stored cursor and walk through it.
3. Two misses on the same concept → slow down: re-explain from scratch with
   a fresh analogy from the reader's domain; offer an interactive widget
   if the environment supports inline widgets.
4. End of session: update front-matter — `last_reviewed: <today>`,
   `next_review` per simple ladder: 1d → 7d → 30d → 90d (advance one step on
   a clean session, reset to 1d on a rough one). Append one line to a
   `## Review log` section: date, score (n/m), weak concepts.
5. Never dump all answers at once. The dialog IS the study mechanism.

## Output adaptation (capability-based, not environment-based)

- **Inline interactive widgets available** (claude.ai / Desktop chat):
  use them during review sessions and for structural concepts on request;
  keep mermaid in the file as the portable fallback.
- **Shell available** (Claude Code): run the verification gates in step 6;
  write files natively.
- **No shell:** restrict mermaid to the safe subset above, skip mmdc/legal
  gates, note in the final message that gates were skipped.
- **No file write available:** deliver the note as markdown in the response
  and say where it should be saved.

## Anti-patterns — hard NO

- A polished prose summary with no questions, no blanks, no self-test.
- Retelling the chapter's structure heading-by-heading.
- Verbatim or near-verbatim passages from the book.
- A diagram for every section.
- Answering the review quiz for the user, or showing all answers up front.
- Asking a multi-question intake interview when context already answers it.
