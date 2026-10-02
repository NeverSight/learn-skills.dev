---
name: docs-discipline
description: Use when writing or reviewing a page of a repository's documentation (a README, a guide, a reference or architecture page, a docs site), or when a change moves code across the layers an architecture page declares.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Docs Discipline

> A page the reader skims and gets. Every fact is shown by the device that shows it fastest, and a paragraph carries only what no device shows. Every path, symbol, and check it names is real. A probe makes the two mechanical readings exact.

Repository documentation is read by a programmer in a hurry and by agents, and this skill owns its shape and its facts. PR bodies and issues belong to the `/pr-and-issue-discipline` skill, AGENTS.md to the `/code-standards` skill.

Where `/unslop` is installed, it runs last over the prose that remains.

## The specimen

One paragraph of a fleet guide ([all-green.md at 7cb9aa3f](https://github.com/Vivswan/repo-platform/blob/7cb9aa3f/docs/all-green.md)), 71 words carrying three rules and two exceptions:

```markdown
The judgment, whole: every needed result must be `success`, or `skipped` for a job named in `allowed-skips`. Anything else (`failure`, `cancelled`, a skip the list does not name) fails the gate, and the step summary lists every job with its result. The managed skeleton names `checks` alone, so a schedule night passes on `ci` and an all-skipped run cannot pass; repo-platform's own ci.yml names nothing, since none of its gating jobs may skip.
```

The same facts, shown:

```markdown
The judgment, whole:

| Needed result | Gate |
| --- | --- |
| `success` | passes |
| `skipped`, for a job named in `allowed-skips` | passes |
| anything else: `failure`, `cancelled`, a skip the list does not name | fails; the step summary lists every job with its result |

- **Managed skeleton:** `allowed-skips` names `checks` alone, so a schedule night passes on `ci` and an all-skipped run cannot pass.
- **repo-platform's own ci.yml:** names nothing, since none of its gating jobs may skip.
```

The owner opened that page and called it a wall of text. The probe agrees and says where:

```text
$ bun docs-probe.mts --shape-only docs/all-green.md
docs-probe: 19 finding(s)
  docs/all-green.md:10: paragraph of 73 words; the cap is 70. Split it, or turn its facts into bullets, a table, or numbered steps
  docs/all-green.md:28: list item of 173 words; the cap is 70. Split it, or turn its facts into bullets, a table, or numbered steps
  docs/all-green.md:99: list item of 218 words; the cap is 70. Split it, or turn its facts into bullets, a table, or numbered steps
```

## Pick the device from the content

There is no mandated carrier. Ask what the reader must see, then use the device that shows it in one glance.

These are devices that carried real pages well, with the content each fits. A page that needs a different one uses it.

| The reader must see | A device that showed it | Why it won |
| --- | --- | --- |
| which value wins, and where inheritance stops | an ASCII tree with the winner on each leaf | a table cannot show the branch |
| what a command does | its real captured output, then the fewest words | the output is the fact; prose about it is a copy |
| what to do about a symptom | three lines: what you see, what it means, what to do | a symptom needs the quoted error and a causal chain, which a table cell truncates |
| a break between versions | a table with an old form, a new form, and a column for what the old form does now | the fourth column is the observable symptom, not the rule |
| two states side by side | a status matrix, resolved by one prose line saying what left means and what right means | the matrix holds the states, the sentence holds the reading |
| how code is arranged | a mermaid diagram whose boxes name real files and exports, closed by a link to the test that demonstrates it | a box a checker can verify does not rot |
| a sequence | an arrow flow, or numbered steps with one fenced block per step that runs something | the order is the content |
| how a change reads | a before block and an after block | the comparison is the visualization |
| plain facts | bullets, each opened by a bold lead-in that names the fact | the reader scans the lead-ins and stops where it matters |

Four rules hold across every device:

- **Every device is a choice.** A table, a bullet list, a link, or a diagram appears because it shows this content faster than prose would. It never appears because the previous section had one. The test is the skim. A reader who takes in only the headings, the first sentences, the tables, the diagrams, the captured blocks, and the emphasized text gets the whole story.
- **One carrier per point.** A diagram followed by a paragraph re-explaining it means the diagram failed. Fix the diagram or drop the paragraph.
- **A bullet is for a list.** Bullets carry items that are a list or a checklist. A line of reasoning stays prose. Turning every sentence into a bullet hides which ones are the same kind of thing.
- **Break a convention when the content reads better without it.** Troubleshooting pages that dropped their tables for the three-line triple read better than the tables did. Say why in the review, not in the page.

## Write for the reader who skims

Every reader of these pages skims, then reads one section closely. Both readers are served by the same rules, and the page holds enough detail to be useful without becoming exhaustive.

Shape:

- **The most important point opens each section.** A reader who stops after the first sentence leaves with the right fact.
- **Headings tell the story on their own** ("What gates what", "When the pin moves"), never the reader's level ("Simple version"). Read in sequence, the headings are the page's outline. They appear only on a page above about 500 words.
- **One idea per paragraph,** 1 to 3 sentences, under 70 words. **Short sentences,** one idea each, about 20 words.
- **No nesting past one level.** A list inside a list is content asking for a different device: a table, a tree, a subsection, whichever shows it.
- **The page reads from beginning to end.** Sections follow the order a reader meets the subject. A fact is introduced before it is used.

Words:

- **Plain, direct, active.** "The sync moves the pin" rather than "the pin is moved by the sync". One term per thing, kept for the whole page. A name the reader has not met is defined where it first appears, in plain words before the mechanism name ("the check that judges every job" comes before `all-green`).
- **Example first, then the rule.** The block or the row shows it. The sentence after says what it means.
- **Show the artifact.** Log lines, error text, and tree output are quoted verbatim, never paraphrased.
- **Programmer register.** Precise nouns, the repository's own names, no marketing. `/unslop`, where installed, removes the AI tells that survive.

Facts:

- **One owner per fact.** A fact lives on one page. Other pages link to it in the sentence that needs it (`the [undeclared-policy page](undeclared.md#the-knob) owns this knob`) and never restate it. A separate links or navigation section exists only when the page is an index.
- **Every internal link works.** The target exists and the anchor names a heading on it. The probe checks the targets, and the anchors are read.
- **Mark what kind of fact it is.** A confirmed fact stands bare. An assumption, a claim supplied by someone else, a risk, a recommendation, or anything not independently verified is labeled as such where it appears ("a guess, to save a round trip" or "reported by the user, not reproduced").
- **Cut only what the reader does not need.** Implementation detail, repetition, and filler go, while definitions, reasoning, limitations, and next steps stay. A cut is a content change the PR names, and a restructure (below) moves every fact and cuts none.
- **Open with one orienting sentence** saying what the page is and what it is not, then whatever the reader needs first. Never background.

## The probe

The probe reports the two readings a reviewer otherwise takes by eye. `scripts/docs-probe.mts` ships with this skill and reads a page's prose units, the paragraphs and list items.

Front matter, headings, fences, tables, comments, and generated regions are not prose. The probe reports:

- a unit over the cap (`--max-words`, default 70), with the line it starts on
- a repository path the prose names that does not exist: a backticked `<dir>/<file>.<ext>`, `./<file>`, `../<file>`, or `<dir>/`, or a relative link target

```bash
bun "<skill-dir>/scripts/docs-probe.mts" README.md docs/*.md               # exit 0: docs-probe: 4 page(s) clean (cap 70 words)
bun "<skill-dir>/scripts/docs-probe.mts" --shape-only skills/*/SKILL.md     # a recipe page names files of the repository it describes
```

| Exit | Meaning |
| --- | --- |
| 0 | every page clean |
| 1 | findings, one per line: `page:line: message` |
| 2 | usage, or a page that does not exist |

The path check leaves alone, on purpose: placeholders (`<skill-dir>/x`), globs, `owner/repo` slugs, absolute paths, and bare file names (`package.json`). It also leaves alone a path whose first segment exists nowhere between the page and the root (a page describing another layout).

A path resolves against the root, the page's directory, and every directory between. So a skill's reference page may name a script under its own `scripts/` folder.

Copy the script into the repository's scripts directory and run it in the check command. The cap is then a gate, not a taste.

## Restructuring an existing page

Reshaping prose moves facts. The change must move all of them and only them.

1. Census before: the headings and anchors (`grep -n '^#' <page>`), and the probe's finding count.
2. Reshape. Every fact of the old paragraph lands somewhere on the new page. A fact the old page did not state does not appear.
3. Census after: the same headings and anchors (another page may link to one), and the probe clean.
4. Review the pair with the `/rubber-duck-review` skill where installed, with this standing question. List every fact of the old page absent from the new, and every fact of the new page absent from the old. Both lists empty is the pass.

The PR body shows one paragraph before and after, as the specimen above does, and carries both censuses.

## The architecture page

The page kind with the most to rot has its own recipe in `references/architecture-page.md`. The recipe is one layering declaration, a lint that fails in both directions, a module map rendered from the declaration, and a page test. The page test checks that every diagram box names a file that exists and a symbol it exports.

## Review Criteria

- A paragraph or list item over 70 words (run `docs-probe.mts` rather than counting by eye), or a paragraph over three sentences.
- Prose that describes what a device would show in one glance: a command without its output, a rule the reader must reconstruct from a paragraph, a break whose observable symptom is not stated.
- A device followed by a paragraph re-explaining it, or a bullet under a diagram that restates an arrow.
- A fact restated on a second page where a link to its owner would do.
- An internal link whose target or anchor does not resolve.
- A links or navigation section on a page that is not an index.
- A heading naming the reader's level instead of the content.
- Headings that do not outline the page when read in sequence, or headings on a page under about 500 words.
- A section whose key point sits after the setup, or a list nested inside a list.
- Bullets carrying a line of reasoning that should be prose, or a device used because the last section had one.
- A page whose headings, first sentences, tables, diagrams, captured blocks, and emphasized text do not carry the story on their own.
- An assumption, a supplied claim, a risk, a recommendation, or an unverified reading presented as a confirmed fact.
- A shortened page that dropped a definition, a reason, a limitation, or a next step the reader needed.
- A path, link, symbol, or check the page names that does not exist (the probe for paths and links, `check-architecture-page.mts` for diagram boxes).
- A reshaped page that lost a fact, added one, or dropped a heading anchor another page links to.
- An architecture page whose module map shows an edge the code does not draw.
- A box naming a symbol its file does not export, or a concept diagram with no `Demonstrated by:` line.
- Wall-of-text prose anywhere a human skims: docs, reports, PR text (the `/pr-and-issue-discipline` skill's Readability rules own the PR body).

