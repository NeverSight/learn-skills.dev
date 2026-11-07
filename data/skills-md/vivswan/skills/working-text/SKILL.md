---
name: working-text
description: "Use when writing or reviewing working text: a repository page, a code comment, a description or help text, a PR, an issue, a CI comment, a Notion page, or a diagram that a colleague will scan to get work done, or when a change moves code across the layers an architecture page declares. Not for a paper, an essay, or any text read start to finish."
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Working Text

This skill governs working text: anything a colleague reads to get work done in a repository, on GitHub, in CI output, in Notion, or in a diagram. A README, a comment, a description or help text, a PR or issue, a review reply, a commit body, an agent brief, a Mermaid chart. It does not govern a paper, an essay, or a book, which a reader studies rather than scans.

> Text the reader scans and gets. Every fact is shown by the device that shows it fastest, and a paragraph carries only what no device shows. Every path, symbol, and check it names is real. A probe makes the two mechanical readings exact.

Working text is scanned to act on, not read to learn. This skill owns how it reads, its shape and its facts, wherever it appears. What each artifact must contain stays with its own skill: a PR body or issue with the `/pr-and-issue-discipline` skill, AGENTS.md with the `/code-standards` skill.

Where `/unslop` is installed, it runs last over the prose that remains.

## The specimen

One paragraph of a CI guide, an example from one repository's page on its `merge-gate` check, 73 words carrying three rules and two exceptions:

```markdown
The judgment, whole: every needed result must be `success`, or `skipped` for a job named in `allowed-skips`. Anything else (`failure`, `cancelled`, a skip the list does not name) fails the gate, and the step summary lists every job with its result. The default workflow names `checks` alone, so a scheduled run passes on `ci` and an all-skipped run cannot pass; the release workflow names nothing, since none of its gating jobs may skip.
```

The same facts, shown:

```markdown
The judgment, whole:

| Needed result | Gate |
| --- | --- |
| `success` | passes |
| `skipped`, for a job named in `allowed-skips` | passes |
| anything else: `failure`, `cancelled`, a skip the list does not name | fails; the step summary lists every job with its result |

- **Default workflow:** `allowed-skips` names `checks` alone, so a scheduled run passes on `ci` and an all-skipped run cannot pass.
- **Release workflow:** names nothing, since none of its gating jobs may skip.
```

A reader opened that page and called it a wall of text. The probe agrees and says where:

```text
$ bun docs-probe.mts --shape-only docs/merge-gate.md
docs-probe: 19 finding(s)
  docs/merge-gate.md:10: paragraph of 73 words; the cap is 70. Split it, or turn its facts into bullets, a table, or numbered steps
  docs/merge-gate.md:28: list item of 173 words; the cap is 70. Split it, or turn its facts into bullets, a table, or numbered steps
  docs/merge-gate.md:99: list item of 218 words; the cap is 70. Split it, or turn its facts into bullets, a table, or numbered steps
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

A change of device must show the content faster than the device it replaces, or the device stays. A table earns its place only when the items share two or more fields a reader compares down a column. A one-line-per-item list turned into a name-and-description table gained nothing and goes back.

Monotony is a wall of its own: table after table, or bullet after bullet, down a page reads like a spreadsheet. Treat it as a signal to regroup or merge the content, with any device change still subject to the gain test above. Bullets that stay the fastest carrier for every section stay.

Four rules hold across every device:

- **Every device is a choice.** A table, a bullet list, a link, or a diagram appears because it shows this content faster than prose would. It never appears because the previous section had one. The test is the skim (the two layers, below).
- **One carrier per point.** A diagram followed by a paragraph re-explaining it means the diagram failed, so fix the diagram or drop the paragraph. Never carry the same content as a table and again as prose or a diagram. A diagram's accessible text alternative (alt text, or a one-sentence equivalent for screen readers) is not a second carrier.
- **A bullet is for a list.** Bullets carry items that are a list or a checklist. A line of reasoning stays prose. Turning every sentence into a bullet hides which ones are the same kind of thing.
- **Break a convention when the content reads better without it.** Troubleshooting pages that dropped their tables for the three-line triple read better than the tables did. Say why in the review, not in the page.

## Write for the reader who skims

Every reader of these pages skims, then reads one section closely. Both readers are served by the same rules, and the page holds enough detail to be useful without becoming exhaustive.

**Two layers.** The top layer (headings, figures, diagrams, captured blocks, the shape of tables, first sentences, emphasized text) carries the whole sense of the page on its own. The detail layer (paragraph bodies, table cells) is what a reader opens for more. Every device choice above serves the top layer.

Shape:

- **The most important point opens each section.** A reader who stops after the first sentence leaves with the right fact.
- **Headings tell the story on their own** ("What gates what", "When the version changes"), never the reader's level ("Simple version"). Read in sequence, the headings are the page's outline. They appear only on a page above about 500 words.
- **One idea per paragraph,** 1 to 3 sentences, under 70 words. **Short sentences,** one idea each, about 20 words.
- **No nesting past one level.** A list inside a list is content asking for a different device: a table, a tree, a subsection, whichever shows it.
- **The page reads from beginning to end.** Sections follow the order a reader meets the subject. A fact is introduced before it is used.

Words:

- **Plain, direct, active.** "The build writes the lockfile" rather than "the lockfile is written by the build". One term per thing, kept for the whole page. A name the reader has not met is defined where it first appears, in plain words before the mechanism name ("the check that gates every merge" comes before its job name, `merge-gate`).
- **Example first, then the rule.** The block or the row shows it. The sentence after says what it means.
- **Show the artifact.** Log lines, error text, and tree output are quoted verbatim, never paraphrased.
- **Programmer register.** Precise nouns, the repository's own names, no marketing. `/unslop`, where installed, removes the AI tells that survive.

Facts:

- **One owner per fact.** A fact lives on one page. Other pages link to it in the sentence that needs it (`the [retry page](retries.md#the-limit) owns this limit`) and never restate it. A separate links or navigation section exists only when the page is an index.
- **Every internal link works.** The target exists and the anchor names a heading on it. The probe checks the targets, and the anchors are read.
- **Mark what kind of fact it is.** A confirmed fact stands bare. An assumption, a claim supplied by someone else, a risk, a recommendation, or anything not independently verified is labeled as such where it appears ("a guess, to save a round trip" or "reported by the user, not reproduced").
- **Cut only what the reader does not need.** Implementation detail, repetition, and filler go, while definitions, reasoning, limitations, and next steps stay. A cut is a content change the PR names, and a restructure (below) moves every fact and cuts none.
- **Open with one orienting sentence** saying what the page is and what it is not, then whatever the reader needs first. Never background.

### Prose inside artifacts

Description or help text a human reads inside a code artifact is working text like any other, under the paragraph, device, and heading rules above. The artifacts:

- a GitHub action or workflow `description`
- a package manifest's description
- CLI help text
- issue and PR templates

A skill's frontmatter description is excluded: it is a trigger, owned by the `/craft-skills-and-memories` skill.

The artifact-specific facts:

- **An action description** is a literal block (`|`).
- **Input and output descriptions** are one sentence each.
- **Never `${{` inside an action or workflow description.** GitHub evaluates it when the file loads, and a stray `${{` fails the action as soon as it loads.

## The probe

The probe reports the two readings a reviewer otherwise takes by eye. `scripts/docs-probe.mts` ships with this skill and reads a page's prose units, the paragraphs and list items.

Front matter, headings, fences, tables, comments, and generated regions are not prose. The probe reports:

- a unit over the cap (`--max-words`, default 70), with the line it starts on
- a repository path the prose names that does not exist: a backticked `<dir>/<file>.<ext>`, `./<file>`, `../<file>`, or `<dir>/`, or a relative link target

Replace the angle-bracket placeholders with the repository's own paths.

```bash
bun "<skill-dir>/scripts/docs-probe.mts" README.md docs/*.md               # exit 0: docs-probe: 4 page(s) clean (cap 70 words)
bun "<skill-dir>/scripts/docs-probe.mts" --shape-only <skill pages>          # a recipe page names files of the repository it describes
bun "<skill-dir>/scripts/docs-probe.mts" --base <template-dir> docs/*.md     # pages that name files a template or generator writes into other repositories
```

```text usage=skills/working-text/scripts/docs-probe.mts
usage: docs-probe.mts [--root <dir>] [--base <dir>]... [--max-words <n>] [--shape-only] <page.md>...
  --root        the repository root paths resolve against (default: cwd)
  --base        a directory under the root that paths also resolve against (repeatable)
  --max-words   the cap on a paragraph or list item (default: 70)
  --shape-only  word counts only; skip the check that named paths exist
exits: 0 every page is clean; 1 findings, one per line as page:line: message; 2 usage or an unreadable page
```

The path check leaves alone, on purpose: placeholders (`<skill-dir>/x`), globs, `owner/repo` slugs, absolute paths, and bare file names (`package.json`). It also leaves alone a path whose first segment exists nowhere between the page and the root, nor under a `--base` (a page describing another layout).

A path resolves against the root, the page's directory, every directory between, and each `--base`. So a skill's reference page may name a script under its own `scripts/` folder, and a page describing a template may name a file by the path it will have in the repositories generated from it.

The cap becomes a gate, not a taste, when the repository's check command enforces it: through a published package (the same cap ships as a Vale rule under `vale/`, for repositories that already run Vale) or through the repository's own probe. A skill's script stays an instrument run from the skill directory, never copied into a repository.

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
- A device change with no gain (a one-line list turned into a name-and-description table), device monotony where regrouping or merging the content would have read faster (table after table, bullet after bullet), or content carried twice (a paragraph re-explaining a diagram, a bullet restating an arrow, but not a diagram's alt text or one-sentence screen-reader equivalent).
- A fact restated on a second page where a link to its owner would do.
- An internal link whose target or anchor does not resolve.
- A links or navigation section on a page that is not an index.
- A heading naming the reader's level instead of the content.
- Headings that do not outline the page when read in sequence, or headings on a page under about 500 words.
- A section whose key point sits after the setup, or a list nested inside a list.
- Bullets carrying a line of reasoning that should be prose.
- A page whose top layer (headings, figures, diagrams, captured blocks, the shape of tables, first sentences, emphasized text) does not carry the story on its own.
- An assumption, a supplied claim, a risk, a recommendation, or an unverified reading presented as a confirmed fact.
- A shortened page that dropped a definition, a reason, a limitation, or a next step the reader needed.
- A path, link, symbol, or check the page names that does not exist (the probe for paths and links, `scripts/architecture/check-page.mts` for diagram boxes).
- A reshaped page that lost a fact, added one, or dropped a heading anchor another page links to.
- An architecture page whose module map shows an edge the code does not draw.
- A box naming a symbol its file does not export, or a concept diagram with no `Demonstrated by:` line.
- Prose inside a code artifact, per this skill's "Prose inside artifacts" subsection, that breaks the page rules. An action description that is not a literal block, or that gives an input or output more than one sentence. `${{` inside an action or workflow description.
- Wall-of-text prose anywhere a human skims: docs, reports, PR text (the `/pr-and-issue-discipline` skill owns the PR body's content).

