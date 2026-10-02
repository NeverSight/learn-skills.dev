---
name: pr-and-issue-discipline
description: Use when opening a pull request, writing or changing its body or title, or writing an issue.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# PR and Issue Discipline

> Show the change, do not describe it: a fenced block is the text form of a picture, so the reader skims it and gets the change; the fewest words after, under a hard size budget, in the shape that fits the change; anything written for a tool or another agent sits in one collapsed section at the bottom.

These rules apply to any session that opens or updates a PR or writes an issue. "The author" below is whoever prepared the change, human or agent, alone or in a multi-agent session. What happens after the PR exists (draft flips, review rounds, the merge) is the `/pr-landing-discipline` skill's moment; someone else's thread (an issue reply, a review of their PR) is the `/reply-and-review-discipline` skill's.

## When to Apply

- Opening a pull request, or writing or changing its body or title
- Writing a bug report or issue
- Re-reading the body before the PR is offered to its reader

Open every PR as a DRAFT; from there the `/pr-landing-discipline` skill owns it: the draft flips, the babysit loop, who merges, and the gates before landing.

## PR Bodies: Show the Change, Shaped to It

Show the change rather than describe it. A PR body is text, so its picture is a fenced block: real captured output wherever behavior is observable, a diagram, table, or the contract's own shape where nothing runs. The reader skims the blocks and gets the change without reading a paragraph. Shape the body to the change; never force every PR through one template.

**Two parts.** Part one is for a human skimming: the change shown (the opening block, in one of the shapes below), then the fewest words. Part two, at the BOTTOM, is a single collapsible section, collapsed by default, for anything written for another agent or tool rather than the human reader:

```markdown
<details>
<summary>Technical details</summary>

...

</details>
```

- **Into part two:** reviewer guidance for bot reviewers such as Copilot, mechanism detail beyond `## How`, the recorded-not-built and accepted-deviation lists, gate detail beyond the `## Proof` totals, file-by-file notes, line counts that fit the stated purpose.
- **The test is the reader, not the item type.** Part one holds whatever the human needs to know or decide about this change; part two holds everything else. The list above is the default sorting, decided case by case. A review finding that changed what the change does, or left something undone, is part one even though it came from a round.
- **Nothing in part one depends on part two.** A PR whose detail fits in part one has no part two.
- **The summary line is a heading.** The Readability rules below govern it: "Technical details" names content.

**Size budget.** Part one has a hard cap, counted before publishing. The bullet counts are defaults: a change whose mechanism needs eight bullets gets eight. Part two has no length cap, only the format rules below. An agent that believes this change cannot fit the cap asks the user before publishing over it, with the count and the lines it would keep. The user decides, never the agent alone.

| Region | Budget |
| --- | --- |
| Part one prose (words outside fenced blocks) | 150 words, hard cap |
| `## How` | 3 to 6 bullets by default, one sentence each, about 15 words. Or one small diagram or table |
| `## Proof` | 2 to 4 bullets by default, latest totals only |
| `Technical details` | No length cap. One fact per line, one sentence each |

**Readability is an accessibility requirement.** Readers include people with dyslexia, and a wall of prose costs them the PR. The standard is the one the `/docs-discipline` skill states for any page: a mix of devices the reader can skim, with the detail in short paragraphs where they choose to read.

These rules bind PR bodies and the `/reply-and-review-discipline` skill's replies alike (it points here rather than restating them):

- **Pick the device from the content.** Paragraphs, bullets, tables, and fenced blocks mix. Each appears because it shows this content faster, never because the last section had one.
- **A bullet is for a list.** Parallel items, steps, options, findings. A line of reasoning stays prose. Turning every sentence into a bullet hides which ones are the same kind of thing.
- **Short paragraphs are fine.** One idea per paragraph, one to three sentences, under 70 words. Short sentences, about 20 words, one idea each.
- **No semicolon chains.** A semicolon joining clauses means two sentences were forced into one. Split them.
- **Bold lead-ins on bullets.** The bold words name the point so a skim reads the lead-ins alone.
- **No nesting past one level.** A list inside a list is content asking for a table or a subsection.
- **Headings name the content** ("What changed", "What the report shows"), never the reader's level: "In plain words", "Simple version", and "Non-technical summary" read as talking down.
- **The blocks carry the change, the words only what no block can.** The defaults above are what most changes need. Go past them when this change needs it, never because a round added something.
- **`/unslop` runs last**, where installed, over the prose that remains: the AI tells go before the body is offered.

**Template check, once per session, at plan time.** Before the first PR or issue of the session, while still planning, resolve the choice once and reuse it for every PR and issue in that session:

1. Look for templates in the target repository, case-insensitively and at any extension (`.md`, `.txt`, none): `pull_request_template*` and `PULL_REQUEST_TEMPLATE*` at the repository root, in `.github/`, and in `docs/`, plus `.github/PULL_REQUEST_TEMPLATE/` and `.github/ISSUE_TEMPLATE/`.
2. None found: the shapes below apply directly. Do not ask.
3. Any found: ask the user once, in these words, "Use this repository's templates, or this skill's shapes?" Name the repository, say whether it is theirs or someone else's, and list the templates found by filename. A user who installed this skill often prefers its shapes, and a third party's maintainers usually expect their own, so ask rather than assume either way.
4. Carry the answer for the rest of the session, for every PR and every issue in it. Answer "the skill's shapes": use the shapes below throughout. Answer "the repository's templates": use the template whose purpose matches each artifact, without asking again; where the repository ships no template for that artifact (issue templates but no PR template, or the reverse), the shapes below fill the gap.

Whichever is chosen, the repository's `CONTRIBUTING` guidance still applies: honor its rules on title conventions, required sections, and linked issues inside the body you write.

### Additive feature

Its detail fits in part one, so it has no part two.

````markdown
## What this adds

```text
$ bun run shards --changed
manifest build/image-sets.json v3: 5 contexts, files and dependencies validated against the checkout
changed: api -> dependency closure {base, api} -> shards: [base, base+api]
```

## How

- **Validates the manifest** against the checkout before anything else runs.
- **Closes each changed context** over its declared dependencies.
- **Emits the GitHub Actions matrix** from the closure, one shard per entry.

## Proof

- **Tests:** manifest validation and shard-resolution cases pass (2 new).
- **Gate:** `bun run check` green.
````

### Existing behavior change or bug fix

Open with `Before` / `After` as real captured output; the comparison is the visualization. When nothing observable changes (a pure refactor), open with `## What this changes` and the same `## How` and `## Proof`.

````markdown
## Before

```text
$ bun run check
scripts/sweep.mts: probe timed out after 120s; agent marked dead (it was mid-build)
```

## After

```text
$ bun run check
scripts/sweep.mts: probe extended 120s -> 300s while the build lock is held; agent alive
```

## How

```text
before: probe start -> fixed 120s -> timeout -> agent marked dead (mid-build)
after:  probe start -> 120s up -> build lock held? -> extend to 300s -> live verdict
```

## Proof

- **Tests:** 34 green (2 new).
- **Gate:** `bun run check` green.

<details>
<summary>Technical details</summary>

- **Reviewer note (Copilot):** the 300s ceiling is a constant in `scripts/sweep.mts`, not a flag.
- **Refused: `--probe-ceiling`.** No second caller exists.
- **Proof detail:** one new test pins the extension while the lock is held, the other the plain 120s verdict without it.
- **Files:** `scripts/sweep.mts` (the probe), `tests/sweep-script.test.ts` (the two cases).

BEGIN_COMMIT_OVERRIDE
fix(sweep)!: extend the probe while the build lock is held

BREAKING CHANGE: `--probe-timeout` is removed; the probe extends itself while the build lock is held.
The probe's dead verdict can arrive up to 300s after start instead of at 120s; callers that raced it must re-read.
END_COMMIT_OVERRIDE

</details>
````

The block closing the details section is the commit-override rule below at work: this specimen's merge carries two breaks, so one `BREAKING CHANGE` footer lists them on two lines.

### Contract or documentation PR

Use `## What this specifies` when the PR defines a contract rather than executable behavior. Nothing runs, so show the contract itself (its schema, table, or layout) in a block, not in prose.

````markdown
## What this specifies

```text
SKILL.md                    disable-model-invocation: true
agents/openai.yaml          policy.allow_implicit_invocation: false   <- must pair with the line above

agents/openai.yaml          .codex-plugin/plugin.json
interface.display_name      == interface.displayName
interface.short_description == interface.shortDescription   (25-64 chars)
interface.brand_color       == interface.brandColor
```

## How

- **The smoke test reads the three files** per skill on every build.
- **Any drift between the mirrored fields** fails the build with the field named.
- **The invocation pair is checked together,** so one flag without the other fails.

## Proof

- **Smoke test:** the mirrored-block and invocation-pairing cases pass.
- **Gate:** `bun run check` green.

<details>
<summary>Technical details</summary>

- **Accepted deviation:** `longDescription` is not mirrored, since the codex manifest carries the long form alone.

</details>
````

For every form:

- Blocks show, prose tells. Where behavior is observable, the opening block is an actual command and its actual output, complete enough to stand alone; never manufacture output or add it only to satisfy a format. Where nothing runs, the block is a diagram, a table, or the contract shape itself.
- `## How` is 3 to 6 bullets by default, more when the mechanism has more moving parts. One small diagram or table may replace them where it explains the mechanism faster. Each bullet is one sentence of about 15 words with a bold lead-in.
- One carrier per point: a diagram followed by a bullet re-explaining it means the diagram failed. Never a `## How` paragraph per review round.
- `## Proof` is 2 to 4 bullets by default, naming focused behavioral tests or stable checks, with the latest totals where numbers exist. Never one line per review round ("round 3: 20 passed", "round 4: 83 passed"): a new run overwrites the old number. Do not turn it into transient CI, approval, or review status.
- Write programmer to programmer: what changed, how the flow changed, in the reader's technical vocabulary, under the Readability rules above.
- The diff carries the detail. Part one never narrates the implementation process, reduction history, transient status, future work, or the entire diff. It carries line counts only when they contradict the stated purpose, and then the `/pr-landing-discipline` skill's line accounting says when and the reason comes with them.
- Reviewer guidance goes in part two or nowhere. Review round counts go nowhere. A scope caveat follows the reader test: part one when the reader must act on it or would be misled without it, part two otherwise.

**Technical details is a fact list with no length cap.** Written for a bot reviewer or the next agent, read by a human who opened it on purpose. As long as the facts require, and shaped so every line can be skipped on its own:

- **One fact per line, one sentence per line.** A line that needs a second sentence is two facts.
- **Guard and refusal lists use one pattern:** `**Refused: \`--flag\`.** one-clause reason`.
- **Files take one line,** grouped with braces: `scripts/{sweep.mts,probe.mts}`, `tests/sweep-script.test.ts`.
- **No round numbers, no process narrative.** "Copilot round four" and "codex round two" name the session, not the change. The fact stays; the round it came from goes.
- **Nothing part one already says.** A details section that restates `## How` doubled the body for no reader.

**Redact captured output before publishing, and publish no PII anywhere**: strip secrets, tokens, and credentials. Redaction is not paraphrase: the command and the output structure stay verbatim. This is the single definition; the skills that gate on it point here.

- **PII is anything that tells a reader who the author is, how they work, or how their machine is set up.** Two kinds: identity (a name, an employer, a real login, a hostname, a home path, an email), and anything measured or copied from the author's real environment (figures from real logs, real settings or transcripts, an inventory of installed tools), which identifies the author with no name in it.
- **One substitute per kind:** `octocat`, `work-bot`, or `example-user` for a login; `example.com` for an employer, a domain, or a hostname; `example-user@example.com` for a whole email; `/home/user` or `~` for a home path; `/repo/...` for the checkout path; hand-written example values, said to be examples, for anything measured.
- **What follows from the rule, the specimens, and what stays** (fixtures are hand-authored, a CI check posts no real figure; a product file name and the repository's own coordinate and gates are not PII): `references/redaction.md`.

**Release-please reads the body.** In a repository released by release-please, Conventional Commit footers (`BREAKING CHANGE`, `Release-As`) travel in the PR body as a commit-override block, the last element inside the Technical details section. Release-please parses that block in place of the squash message.

- **The marker words appear nowhere else in the body.**
- **One `BREAKING CHANGE` note per commit:** several breaks share one multi-line footer, one per line, or take one nested-commit block each.
- **A bad block is repaired by editing the merged body.**
- The block's shape, why each rule exists, and the repair: `references/release-please.md`.

**Hand the body to `gh` on stdin, never through a guessable file.** A body drafted at `/tmp/<repo>-pr-body.md` was the specimen: two sessions on one machine picked the same name, and the second overwrote the first's. `gh pr create` and `gh pr edit` take `-` as the body file and read stdin, so a quoted heredoc carries the body with nothing to race over or clean up:

```bash
gh pr create --draft --title "<type(scope): subject>" --body-file - <<'EOF'
## What this changes
...
EOF
```

When the sandbox refuses the heredoc (an agent worktree can reject one whose text contains git commands, and captured output often does), stage the body in a directory `mktemp` minted, at the literal path it printed, and remove that directory in the same command that publishes, whatever `gh` returns:

```bash
# 1. Mint the directory; a harness that starts a fresh shell per tool call loses $body_dir, so copy the printed path by hand:
mktemp -d "${TMPDIR:-/tmp}/pr-body-XXXXXX"   # prints e.g. /tmp/pr-body-Kq3mZp
# 2. Write the body to <that path>/body.md with your Write tool.
# 3. Then, in one shell call, publish and remove the directory on every exit, success or failure:
body_dir="/tmp/pr-body-Kq3mZp"
trap 'rm -rf "$body_dir"' EXIT
gh pr create --draft --title "<type(scope): subject>" --body-file "$body_dir/body.md"
```

## Re-read Before the Human Reads

The body is written when the PR opens and read when the PR is offered; the diff moves in between. Two gates keep it readable: one after every review round, one before the offer.

**After every review round: edit in place, never append.** The specimen was a body that grew to 1,800 words because each of twelve rounds added its own `## How` paragraph and its own `## Proof` line. The rule:

1. A fix to something the body already states edits that `## How` or `## Proof` bullet in place. It does not add a second bullet about the same thing.
2. A fact new to the change (a mechanism or proof the body never stated) gets one new line, in the region the reader test sends it to.
3. A count (tests, gates, lines) is overwritten with the latest total. The old number goes.
4. Nothing in the body says which round produced it.
5. Run the size check below before updating the PR body. Over the cap, re-cut first.

**Before the offer** (the flip to ready, the "ready to merge" report), re-read the body against the final diff as a reader who did not watch the session. How hard to look depends on how far the PR moved: a one-commit PR gets a glance at the Proof numbers, a PR that went through eight review rounds gets every claim re-checked. Run the size check first, then the drift list:

```bash
# Part-one prose: words outside fenced blocks and above the <details> tag. Cap: 150.
# Pipe the CANDIDATE body in through a quoted heredoc: the text about to be published, every round and before the first publish.
# `gh pr view "$n" --json body -q .body |` replaces the heredoc only for the final pre-offer read of what is already published.
# Never point awk at a file name, and keep pipefail on: a missing file or a failed gh read must stop the gate, not count as 0.
set -o pipefail
awk '
  /^(```|~~~)/ { match($0, /^(`+|~+)/); d = substr($0, 1, 1)
                 if (!f)                                       { f = 1; c = d; n = RLENGTH; next }   # opening fence: remember its character and length
                 if (d == c && RLENGTH >= n && /^(`+|~+) *$/) { f = 0 }                              # closing fence: same character, at least as long, nothing else
                 next }
  !f && /^<details>/ { exit }                                                                        # part two starts at a real tag, never one inside a fence
  !f' <<'EOF' | awk '{ for (i = 1; i <= NF; i++) if ($i ~ /[[:alnum:]]/) n++ } END { print n + 0; exit (n > 150) }'   # counts tokens with a letter or digit, so `##`, `-`, and `|` are not words; exits 1 over the cap
<the candidate body>
EOF
```

Over the cap means cut, not justify. Move detail down into part two, which has room for it, or drop what the diff already says. If the cut would lose something the reader must know, stop and ask the user with the count and the candidate lines. Publishing over the cap is the user's call. What usually drifts:

- **Every claim still true.** The opening block is still accurate (its After side, or its only side, is what the code does now), the Proof numbers are the final run's, and every file named as current still exists under that name.
- **Scope drift.** Work the review rounds added or removed is in the body, or its absence is deliberate.
- **Sorting.** Part one holds what the reader needs about the change as it is now. Anything that became detail moved down; anything that became important (a review finding that changed the change, a line count that contradicts the purpose) moved up.
- **Title.** Type and subject name what landed, not the opening plan.
- **Size.** Part one is under 150 words, and no semicolon joins two clauses. `## How` and `## Proof` sit at their defaults unless this change needs more.

A body that no longer matches, or no longer fits, is edited before the flip, never after the reader finds it.

## Issues: Same Principle

What breaks, shown first; then the minimum around it, under the Readability rules above.

The session's template answer, resolved at plan time above, covers issues too: fill the chosen issue template's fields and apply this principle inside them, or use the shape below when the answer was the skill's shapes or no template exists.

````markdown
## What breaks

```text
$ npx skills add Vivswan/skills --skill some-skill
installed: SKILL.md, README.md          (metadata.json silently missing)
```

## Repro

1. Add a `metadata.json` inside any skill folder.
2. Install with `npx skills add`.

## Expected vs actual

- **Expected:** every file in the skill folder installed
- **Actual:** `metadata.json` dropped without a warning
````

Include environment only when it matters: a version-specific parser bug names the version; a pure logic bug does not. When an issue includes captured output, the redaction rule above applies unchanged.
