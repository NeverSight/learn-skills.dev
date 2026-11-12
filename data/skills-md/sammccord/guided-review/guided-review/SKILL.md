---
name: guided-review
description: Audit a pull request, a stack of pull requests, or a branch, pick the changes that need human judgment, and open them as ordered, annotated tours of small stops grouped into tracks in the Hunk diff viewer, one tour per stack layer. Use for "guided review", "tour this PR", "review tour", "walk me through this PR", or a PR link, branch name, or shared tour JSON file with a request to review it in hunk. Posts to GitHub only the stops the reviewer chooses with Post finding to PR and the comments the reviewer writes with Comment on PR.
---

# Guided review

The reviewer's time is the scarce resource. Do the exhaustive reading yourself, then hand the human a tour of the places where their judgment is required. Each stop is small: a few lines and one point. Related stops form a track, so the reviewer sees how the significant changes connect. A tour that stops at every hunk has failed.

## Inputs

- **Target.** A PR URL, a PR number, or a branch name, plus an optional base ref. Or one or more tour JSON files someone shared, one per stack layer; see [Shared tours](#shared-tours).
- **Stop budget.** Optional. The user may name a number ("12 stops", "stops=30") or a depth: `quick` is about 8, `standard` about 20, `deep` about 40. Default `standard`. The budget counts stops, not findings. Fill it with findings first, then with `inspect` stops in order of significance. Fall short only when the diff runs out of significant changes, and say so in the report. Never pad with nits or Mechanical files to reach it.
- **Summary.** Optional, off by default. The user turns it on with "summary", "share summary", "summary=on", or "summary=<path>". When on, step 10 writes a shareable markdown summary of each tour after the review concludes; see [Shareable summary](#shareable-summary). The default path is the review's `tourPath` with `.json` replaced by `.md`. A given `<path>` is a file for a single review, or a directory for a stack, which gets one `<slug>.md` per layer.

`<skill>` below means the directory containing this file.

Requires `git`, `python3`, `hunk` 0.22 or newer, and `gh` authenticated for the PR's host (`gh auth status --hostname <host>`). GitHub Enterprise works because nothing goes through `hunk gh`.

## 1. Prepare the worktree

Run from inside a clone of the repository under review. If the user is elsewhere, find the clone or `gh repo clone` it first.

```bash
<skill>/scripts/prepare.py <pr-url | pr-number | branch> [base-ref]
```

It checks whether the PR is a layer of a GitHub stack (the stacked-PR chain the `gh stack` extension manages), fetches every open layer, and prints JSON:

- `stack` is the whole stack, bottom layer first, or `null`. `stackLookup` says `found`, `none`, `not-a-pr`, or why the lookup was `unavailable`.
- `reviews` has one entry per open layer, bottom first, or a single entry when there is no stack. Each entry has its own `worktree`, `tourPath`, `base`, `head`, `title`, `url`, `description`, `stat`, `commits`, `stack`, and `cleanup`.

Each review gets branch `review/<slug>` in a worktree under `.git/guided-review/`. The user's checkout is untouched. Read code from the review's worktree, not the user's checkout. Every diff in this skill is `git diff <base>...<head>` for one review. In a stack, a layer's `base` is the lower-layer commit it was built on, so each diff holds only that layer's work. With `needsRebase` that commit is older than the lower layer's current head.

### Stacks

When `reviews` has more than one entry, run steps 2 to 7 once per review and write one tour per layer. Step 9 waits on every layer's tour at once. Never merge layers into one tour.

- Go bottom to top. A layer may rely on the layers below it, so read their tours or diffs for context, but judge only the layer's own diff.
- A problem introduced in a lower layer belongs in that layer's tour, even when you notice it while reading a higher one. Link nothing across tours; mention the other layer by PR number instead.
- Ask whether the split itself is sound: a layer that does not build or does not make sense without the layer above is a finding for the lower layer's tour.
- If your host can run parallel subagents, give each layer its own reviewer with its review entry and the stack, then check that their findings land in the right layer.
- The stop budget applies to each layer separately. Size it to the layer: a two-file layer may need only a few stops.
- Merged layers get no tour. They appear in the stack list for context.
- `needsRebase: true` means the layer below has commits this layer was not built on. The diff still shows only this layer's work, but nothing proves it still applies or builds on the current lower layer. Say so in that layer's `scope.unchecked`, and add a `risk` stop when the lower layer's new commits touch code this layer uses.

### Shared tours

When the target is a tour file, pass every shared file at once:

```bash
<skill>/scripts/prepare.py <tour.json>...
```

It checks out each tour's own `base` and `head`, fetching them from the remote and the PR in its `url` when missing, and copies the tour to the review's `tourPath`. `stackLookup` is `tour`, and `stack` comes from the tour. Use `tourPath` from here on, never the shared file.

Skip steps 2 to 6. The tour is the review. Do not rewrite its stops, verdict, or scope. Run step 7; if an anchor fails, the file does not match its commits, so report the failures and stop. Then continue from step 8. Before answering in step 9, read the code around the stop in the worktree; you did not write the audit. In step 10, the verdict is the tour author's; say where you disagree.

## 2. State the intent

Write two or three sentences on what the change is trying to do, from the description, the commit messages, and linked tickets you can reach. In a stacked PR the ticket describes the whole stack; judge only what `base...head` delivers. Every later judgment is measured against this. A finding that ignores the intent is a bad finding.

## 3. Map the diff

Run `git diff --stat <base>...<head>` and sort every changed file into one bucket:

- **Core.** Behavior changes: logic, control flow, data handling.
- **Contract.** Public API, schema, migration, config, permissions, dependency versions.
- **Tests.** Added, changed, or deleted tests.
- **Mechanical.** Renames, moves, formatting, generated code, lockfiles.

Mechanical files get a sampled check that they are what they claim (a "pure rename" with a changed line is not mechanical). Core and Contract files get the full audit. Deleted tests count as Contract.

## 4. Audit

Read every Core and Contract hunk in full context, plus the callers and callees it touches. Apply the lenses in [references/lenses.md](references/lenses.md).

If your host can run parallel subagents, give each one a slice (by lens or by subsystem) with the intent statement, base, head, and worktree path, and ask for findings with `file:line` evidence. Otherwise run the lenses yourself in sequence. A slice that fails to report is noted as unchecked, not silently dropped.

Run things when you can: the tests for the touched packages, the type checker, a quick repro of a suspected bug. A fact you ran beats a fact you inferred, and the tour says which is which.

## 5. Choose the stops

A stop either carries a finding or points at a significant change a human should inspect with their own eyes. Use one `kind` per stop:

- **blocker.** A bug or regression you traced to a concrete failing path. Show the path. The reviewer's decision is whether it blocks the merge and whether your proposed fix is right.
- **risk.** Code whose safety rests on a fact you could not prove (a caller's behavior, production data, an external system, concurrency).
- **question.** A design, product, or intent call: the code works, but whether it is the right thing is the reviewer's decision.
- **inspect.** A significant change with no defect found that still deserves human eyes: rewritten core logic, a contract or schema change, deleted behavior, a new abstraction's callers. The ask says what to confirm.
- **context.** A definition the reviewer must see before the stops that use it. At most one per track, as its first stop.

Prefer more, smaller stops over fewer large ones. One stop makes one point about a few lines, ideally under 10 and never over 20 (`tour check` warns past 20). A finding that touches three places is three stops: where the value is produced, where it is transformed, where it is consumed. A test that asserts the behavior in question is its own stop. Each stop carries its own short body and ask. Split until each stop's body fits in a few sentences, then stop splitting.

Size the tour to the stop budget from the inputs. A tour with no stops is valid: zero blockers and zero risks is a legitimate result. Say so in the verdict instead of inflating nits or padding with context.

Leave out style preferences, naming, "I would have done it differently", hypothetical inputs no caller can produce, and anything a linter or the test suite already enforces. List a file in `skipped` only when it is a Core or Contract file with real changes and no stop. One line on why. At most 15 entries, the riskiest first; count the rest in `scope.checked`. Do not list tests or Mechanical files.

Group the stops into tracks. A track is one thread the reviewer should hold in their head at once: a causal chain (a new abstraction and each caller migrated onto it), a single concern that spans files (every place the rate limiter is committed or rolled back), or one subsystem. A stop belongs to exactly one track. Usually 2 to 6 tracks. A small tour may use one track, a tour with no stops has no tracks, and a track with one stop is fine when the point really stands alone.

The track `summary` is where relationships live, as bullets like the stop bodies. Say how its stops connect and what the reviewer should conclude after reading them together, such as "the runner commits on every path except the swap handler; stops 4 to 6 show the three paths". Name dependencies on other tracks ("assumes the Release contract from track 1").

Link related stops. Give a stop an `id` (lowercase, digits, hyphens) and write `[[id]]` in another stop's `body` or `ask`, or in a track `summary`, wherever the reader needs the other location to judge this one: the producer a consumer depends on, the test that pins a behavior, the earlier abstraction a later caller misuses, the same pattern in another track. Links cross tracks freely; tracks group, links relate. The reviewer sees each link as `#7 title`, can follow it, and can come back. Link where the relationship changes a judgment, not between every pair of neighbors.

Order tracks so each one only depends on tracks before it: the core abstraction first, then its consequences, then independent concerns. Within a track, order stops the way a reader follows the data or the call chain. Put the track holding the most severe blocker as early as those dependencies allow.

## 6. Write the tour

Write the tour to `tourPath` from step 1. It sits beside the worktree, not inside it. The schema is the `Tour`, `Track`, and `Stop` types in [`core/src/schema.ts`](core/src/schema.ts). Read them before writing.

- `base` and `head` are the SHAs from step 1.
- `url` is the review entry's `url` from step 1. It is needed for **Post finding to PR** and **Comment on PR**.
- `stack` is the review entry's `stack` from step 1, copied as is. Omit it when it is `null`.
- Anchor each stop on lines of the reviewed diff. Use `side: "new"` with new-file line numbers, or `side: "old"` for code that was deleted. `endLine` covers a short range that stays inside one `@@` range of `git diff <base>...<head>`. Adjacent changed lines can belong to different `@@` ranges.
- Write `body`, the tour `summary`, and track summaries as short bullet points, one fact per line, each line starting with `- `. No paragraphs. Aim for 2 to 5 bullets of under 15 words each. Drop filler and restated code.
- `body` covers what changed, why it matters, and the evidence: callers, the trace, the test you ran, or what you could not verify. For example:
  ```
  - Defers RollbackOnErr after Enforce; never calls Commit.
  - Broadcast error after network submit refunds the count. Unlike [[send-commit]].
  - Traced; mocked test passes. No live broadcast run.
  ```
- `ask` is one concrete decision, phrased so the reviewer can answer it after reading the stop. "Is a 30s timeout acceptable for EU traffic?" is a good ask. "Please review" is not. Stops split from one finding ask narrower questions, such as what to confirm at this spot.
- `verdict` is your recommendation: `approve`, `request-changes`, or `discuss`.
- `scope.checked` and `scope.unchecked` say what you verified and what you did not. Be specific ("ran `pkg/policy` tests: pass", "did not exercise the migration against production-sized data"). A check that failed and passed on a rerun with a workaround goes in `checked` with both results; the unresolved cause goes in `unchecked`.

## 7. Check the tour

From the worktree:

```bash
hunk --extension <skill> tour check <tour.json>
```

It validates the schema and confirms every anchor falls inside a hunk of `base...head`. Fix every reported stop and rerun until it prints `ok`. Then clear every warning: split oversized stops and rewrite paragraphs as bullets.

## 8. Open it

```bash
<skill>/scripts/open-tour.sh <worktree> <tour.json>
```

Run it once per review. For a stack, open the layers bottom first; each gets its own terminal tab labelled `review pr-<n>`.

Reopening an unchanged tour resumes its saved decisions. Use `open-tour.sh --fresh <worktree> <tour.json>` for a new review of the same tour. Changed tour contents, refs, repository, or PR/layer start an isolated review automatically. Never copy or replay notes, questions, or answers from an earlier tour or another stack layer into Hunk unless the reviewer explicitly asks to import that history. Legacy mailboxes are retained on disk, not automatically imported.

Hunk needs a real terminal. Inside a Neovim terminal the script opens a Neovim tab. Inside herdr, tmux, or zellij it opens a tab or window there, with a pane fallback for older zellij versions. Inside kitty, WezTerm, Ghostty, Alacritty, Konsole, GNOME Terminal, or foot it opens a tab or window in that terminal. Otherwise it uses iTerm2 when running there or Terminal.app on macOS, and x-terminal-emulator on Linux with a graphical display. If no launcher applies, it prints the command for the user to run. Pass `--print` first to skip launching. It always prints a final `Tour command:` line.

In hunk, the Tour pane on the right lists the tracks, each with its summary and its stops. `>` and `<` step through stops in tour order. `)` and `(` jump to the next or previous track. The current stop expands with its body, its ask, and its links in both directions. Its **Post finding to PR** button asks you to turn that stop into a PR comment. `L` follows a link and `B` goes back. A stacked tour also lists every layer of the stack under the verdict and marks the one under review. The whole diff stays visible, grouped by directory so each folder appears once. `{` and `}` jump between annotated hunks in file order; use `>` and `<` for tour order. `a` toggles the inline notes, and `c` adds a note, which comes to you as a question. `V` marks the current stop agree, disagree, or unsure. `Q` asks you a question. `C` comments on the PR in the reviewer's own words.

The current stop shows three buttons with their keys: **Ask agent** (`Q`), **Comment on PR** (`C`), and **Post finding to PR**. The agent's ask line reads **To confirm:**. A **Finish review** button (`F`) sits in the pane header. `V` has no button. Marks are optional.

## 9. Answer the reviewer

Hunk shows a "Waiting for the agent" placeholder under each unanswered request and a spinner in the Tour pane, and removes the placeholder once answered.

The reviewer talks to you from Hunk while the tour is open. Six things become requests. Every note is a question. A reply under one of your answers is a follow-up. `Q` sends a question. `V` sends a decision on a stop: `agree`, `disagree`, or `unsure`, plus an optional comment. **Post finding to PR** sends a `comment` request for that stop. **Comment on PR** and `C` send a `reviewer-comment` request with the reviewer's own text. Run from the worktree, with every open tour of a stack at once:

```bash
hunk --extension <skill> tour wait <tour.json>... [--timeout <seconds>] [--away <minutes>]
```

It blocks until something needs you, then prints one JSON line. Its `next` field says what to run. The default timeout is 90 seconds. Keep `--timeout` below your shell tool's limit. `--away` defaults to 30 minutes without reviewer activity. Navigation, commands, notes, and requests reset the clock, as do your answers. The most recently active open tour sets the clock for a stack.

- `pending`. `items` lists the requests, each with its `tour`, `id`, `kind`, and the `stop` it was made at. The content is `text`, `decision` and `comment`, or `body` for a `comment` or `reviewer-comment` request. Answer each one, then run `wait` again immediately.
  ```bash
  hunk --extension <skill> tour answer <tour.json> <id> --text '<answer>'
  ```
  The answer appears in Hunk as a reply under the reviewer's note, or as a note at the line or stop the request names. The first line becomes the note's summary, so keep it short. For a `decision`, say whether you agree and why. An `agree` with no comment never reaches you.
- A `comment` request carries the stop's `title`, `ask`, and `anchor` in `stop`, plus its full `body`. Reword it slightly as actionable feedback for the author: what to change and why. Keep the facts and evidence. Turn the reviewer-facing ask into a request or question to the author. Drop `[[id]]` tour links. Keep it short. `tour answer` posts it as a line comment on the PR at the stop, then confirms in Hunk with the GitHub link.
- A `reviewer-comment` request carries the reviewer's words in `body`. Pass `body` to `--text` exactly as given. Do not reword, shorten, or add to it. `tour answer` posts it as a line comment on the PR at the stop, then confirms in Hunk with the GitHub link.
- `idle`. The reviewer is still around or has not started yet. Run `wait` again. Never end your turn on `idle`, however many arrive in a row.
- `away`. No reviewer activity arrived for `--away` minutes. Stop waiting and tell the user the review looks paused. Tell them saying "resume" restarts the wait loop.
- `finished` or `closed`. The reviewer pressed `F`, chose **Finish review** in the Extensions menu, or quit Hunk. The payload has `decisions`, the latest decision per stop, `transcript`, every request with its status and your answer, and `approval`, eligibility and hard blockers for each tour. Go to step 10.

Keep the wait loop running until `finished`, `closed`, or `away`. Answer from what you read in step 4, and say when you do not know. `answer` posts once per request. A request that was already answered is reported as `already-answered`, so rerunning after an interruption is safe.

## 10. Report

For a stack, start with the stack number and one line per layer (PR, verdict, stop count), then give the full report below for each layer, bottom first.

Reply with the verdict and the intent statement. List the tracks, each with a one-line summary and its stops, one line each as number, `kind`, title, and `path:line`. If you used fewer stops than the budget, say why. Include the unchecked scope, the `Tour command:` line (`open-tour.sh --print` gives it without opening a terminal), and each review's `cleanup` command from step 1, copied as is. It removes the worktree, the review branch, any fetched PR ref, and the Q&A files beside the tour.

When step 9 ended with `finished` or `closed`, add a review draft after the report. The reviewer does not have to decide every stop. Silence on a stop means agreement with your verdict and that stop's framing. Build the draft from the transcript. Use questions and notes, decision comments, `disagree` and `unsure` decisions, and comments posted to the PR, whether yours or the reviewer's. Lead with anything that pushes back on your verdict. If the transcript is empty, say in one line that the reviewer agreed with your verdict. Then propose the overall verdict and comments the reviewer could post to the author. The draft is text in your reply. Post nothing else to GitHub except the explicitly confirmed approval below.

After the draft, check `approval` for each tour. If `eligible` is false, the verdict is not `approve` or a stop's latest decision is `disagree`. Briefly say why and do not ask to approve it. When eligible, you decide from the transcript. An empty transcript is agreement. Otherwise read each note, question, decision comment, `unsure` decision, and posted PR comment. Any unresolved concern means do not ask. A request the review ended before you answered also means do not ask unless your draft resolves it. Posted PR comments do not by themselves block approval. Judge whether they ask for changes before merge. Eligibility alone is not permission. If any qualms remain, do not ask or approve.

Only when eligible and free of qualms, end your reply by explicitly asking: “Approve PR #N at head <sha>?” Wait for an explicit yes in the agent chat. Only then run:

```bash
hunk --extension <skill> tour approve <tour.json> --body '<short summary>'
```

Never approve without that yes. For a stack, get confirmation for each layer's PR and head, then run one approval per confirmed layer tour. The CLI rechecks the verdict, any stop whose latest decision is disagree, and the current PR head. It refuses any blocker. It records approval in `approved.json` and avoids reposting an approval at the same head.

### Shareable summary

Only when the Summary input is on and step 9 ended with `finished` or `closed`. Skip it on `away`; the review has not concluded. Write it after the review draft and before asking to approve, then rewrite its Outcome line if an approval is posted.

Build it from the tour JSON and the `finished` or `closed` payload, nothing else. One file per tour. It must read well on its own, pasted into a PR comment, a ticket, or chat, by someone who never opened Hunk:

```markdown
# Guided review: <title>

<url> · `<base short sha>...<head short sha>` · Verdict: **<verdict>**
Outcome: <approved at <sha> | not approved: <one-line reason> | review ended without a decision>

## Intent
<the intent statement from step 2>

## Summary
<the tour summary bullets>

## Stack
<one line per layer: PR, title, marker on the reviewed layer; omit when there is no stack>

## Tracks
### 1. <track title>
<track summary bullets>

| # | Kind | Stop | Location | Reviewer |
|---|------|------|----------|----------|
| 1 | blocker | <title> | `path:line` | disagree: <comment> |

<details><summary>#1 <title></summary>

<body bullets>

**Ask:** <ask>
</details>

## Reviewer discussion
<each transcript item in order: the stop it was made at, the reviewer's text, your answer; posted PR comments with their GitHub links>

## Scope
**Checked:** <scope.checked bullets>
**Unchecked:** <scope.unchecked bullets>
**Skipped:** <skipped entries with reasons>
```

- Number stops in tour order across tracks, the same numbers Hunk shows. Rewrite `[[id]]` links as `#<n> <title>`.
- The Reviewer column holds the latest decision and its comment. Leave it empty where the reviewer made none; silence means agreement, so do not write "agree".
- Omit an empty section, except Scope. A tour with no stops says so in one line under Tracks.
- Include no secrets, tokens, or local paths. The worktree and `cleanup` command stay out of the file.
- Write the file with your file tool, then report its absolute path in the reply. It is not part of `cleanup`, so it survives the worktree's removal. Post it nowhere; sharing is the reviewer's call.
