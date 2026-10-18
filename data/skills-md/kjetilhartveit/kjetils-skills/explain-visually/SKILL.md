---
name: explain-visually
description: Use when the user asks for a visual explanation or to 'explain visually'.
---

# Explain Visually

The goal: the reader quickly understands what changes, how it works and why, and can decide, without reading
every line of code. Show rather than tell, concise first, details on demand. One page, ~1,000–1,500 words:
short story steps, and the detail a decision needs in the option rows and toggles.

Say exactly what the facts say, above all in the headline:

- "Migrated" is not "kept" or "working"; "honoured" is not "unchanged". Name exceptions in the same sentence:
  "263 rules migrate; 1 must be switched off".
- A number measured under changed conditions is not "the same": "5.3 s, after switching that rule off".
- What holds for some members doesn't hold for the group: name them ("react-x and react-jsx load as plugins").
- Write for a reader new to the tools: gloss each tool or term the first time it appears, in a few words in
  the same sentence ("tsgolint, Oxc's type-checking helper"), in the story and in option rows alike.

The look comes from the `explainer-kit` skill; each chapter follows its `explain-with-*` skill.

## Use this skill when

- The user asks for a visual explanation, an explainer or "explain this visually".
- Explaining a code change, a proposal, a plan or an architecture decision so the user can make informed decisions.

## 1. Gather/research information/facts into `facts.md`

- If a facts file already exists (e.g. the task gives you one), it is your source of truth: skip to step 2.
- Research the facts/topics using up to 3 concurrent subagents.
  - Output each fact; one line with its source (`file:line`, link, or the command you ran). Don't restate facts in your thinking; write them down once.
  - Get numbers from commands (`grep -c`, `jq`, a timed run), not by counting by hand.
  - Measure on the real repo when it is cheap (a scratch copy or worktree, never the repo itself). Note method and
    versions. Never stretch one measurement into "every" or "all".
  - Budget: stop when every claim you plan to make has a source.
- You, as an orchestrator, combines the research into `facts.md`.
- Note what the user must decide, the effort per option, the risks with their fixes, and what would change the recommendation.

## 2. Plan the page (no separate brief)

Write the plan as the first lines of `notes.md` (≤ 15 lines): the one-sentence answer and its main cost, the 3–5
key numbers (each gets **one** home on the page), the 4–8 terms to gloss, the one real snippet to show (config or
code the reader would change, ≤ 8 lines), and one line per chapter. Chapters:

| Chapter  | Built with                             | Section  | When                                               |
| -------- | -------------------------------------- | -------- | -------------------------------------------------- |
| Overview | this skill (kit overview)              | —        | always                                             |
| Story    | `explain-with-storytelling`            | `story`  | always: 5–7 steps, one evolving graphic            |
| Code     | `explain-with-code-walkthrough`        | `code`   | only when the change _is_ code the reader must see |
| Decision | `explain-with-preview`, options (JSON) | `decide` | when the user has something to decide              |

- At most **3 chapters** after the overview. Fragility, dependencies and complexity go into the decision options'
  rows (keeps / loses / fix first / risks), not into chapters of their own. A separate before/after chapter
  (`explain-with-preview`) only replaces Code when there is no decision.
- **Overview:** a headline that states the answer and its main cost ("lint 44 s → 5.3 s; 1 rule and 3 checks to
  port"), one sentence, one hero (to scale; for
  numbers use the kit's HTML `ev-bars ev-bars--hero`, which stays legible on phones), and one key line with at most
  one "Decide" callout. No grid of info boxes.
- Only add `explain-with-section-clips`, `-slides` or `-video` when the user asks for them.

## 3. Build the chapters yourself

- Read `explainer-kit/assets/FRAGMENT-CONTRACT.md` and the chapter skills you use, all in one turn. The contract
  is the whole API: **never read `kit.css`, `kit.js`, `assemble.py` or `SCRIPTS-AND-TABS.md`** for this page.
- Write the chapters yourself, one file each, in order, each with the Write tool (never a shell heredoc: one
  stray quote fails the whole command and every file has to be written again). Don't start subagents for a page this size.
- Use kit components as they are; no new themes, fonts or components, and no layout CSS of your own.
- Show the real snippet from your plan as the recommended option's `code` in the decision JSON (and the cautious
  option's, if it changes config), not as a chapter of its own.
- References go in the details: file paths in code headers, links in the decision's Sources toggle.

## 4. Assemble, check once, publish

```bash
python <kit>/assets/preview.py decide.json --out frag-decide.html
python <kit>/assets/assemble.py --page --toc --title "Short name" --overview overview.html \
  --section story=frag-story.html --section decide=frag-decide.html --out index.html
python <kit>/assets/check.py index.html
```

- Run these only after every file write has returned, as one chained command.
- Fix the contract errors the assembler reports.
- Run `check.py` once. Fix only the problems it lists, run it once more, then stop. Don't take or study
  screenshots to hunt for other issues and don't write your own browser scripts.
- Read your page text once against `facts.md`: counts, names, no "every/all" the facts don't support.
- Publish the single page as an artifact (unless told to just write the file). Reply in at most 5 lines: the
  answer, the page path, and anything unchecked.
