---
name: jira-refine
description: "Turn the transcript of a recorded backlog-refinement session into enriched Jira issues: segment by the ticket keys spoken aloud, fill a fixed template from what was actually said, stage every ticket beside its source excerpt for review, then push descriptions, dependency links, a goal field, and a batch label."
argument-hint: '[transcript path] [--session-date YYYY-MM-DD] | --apply <staging.md> [--dry-run]'
disable-model-invocation: true
---

# jira-refine

A recorded refinement session is an input nobody controlled: people talk over each other, decide half a thing, and move on. The template here is a set of slots that transcript fills or leaves empty, and **an empty slot is written down as empty**. The `- not discussed: <section>` line is the deliverable for a gap, not a hole to paper over. One invented acceptance criterion costs the tech lead their trust in every other line of the file, and that trust is the only reason this skill is worth running.

Two modes, joined by nothing but a file on disk. Stage mode turns a transcript into a `.refine.md` staging file and stops. Apply mode reads that file from disk and pushes what it finds there — not what this conversation remembers writing — so an edit the user made in an editor between the two counts exactly as much as one you made. No ticket reaches the tracker without `status: approved` on its entry.

The skill is user-invoked (`disable-model-invocation: true`) because a misfire writes into a client's tracker: an unwanted push costs somebody's team a conversation, and a missed trigger costs the user one typed word. `scripts/jira-apply.py` is the only file here that knows Jira exists. Everything above it is tracker-agnostic.

Where a step names a shell command, treat it as the intent and use your native shell or file tools.

Resolve once per invocation:

- **MODE** — `apply` when `--apply` is present, else `stage`.
- **TRANSCRIPT** — the transcript path from the arguments. VTT, SRT, and `[HH:MM:SS] Speaker: text` plain text all parse; `segment.py` sniffs which.
- **SESSION_DATE** — `--session-date`, else a `YYYY-MM-DD` found in the transcript's filename, else ask the user. Never the file's mtime: a transcript copied off a share carries the copy's date, and this value lands in the batch label, the frontmatter, and every Provenance block that follows.
- **CONFIG** — the first of `$JIRA_REFINE_CONFIG`, `./jira-refine.toml`, `~/.config/jira-refine/config.toml` that exists and parses. Prove it by parsing, not by testing existence, so a half-edited file falls through to the next rung instead of stopping the run. None of the three → stop and point the user at [`assets/jira-refine.example.toml`](assets/jira-refine.example.toml), which carries every key with its default.
- **STAGING** — in apply mode, the path after `--apply`. In stage mode, `<transcript stem>.refine.md` beside TRANSCRIPT; refuse to overwrite one that already holds any `approved` or `applied` entry, since that file is a reviewed session and regenerating it throws the review away.
- **DRY_RUN** — set by `--dry-run`.

## Stage mode

### Step 1 — Segment

```
jira-refine/scripts/segment.py TRANSCRIPT --config CONFIG --session-date SESSION_DATE > STAGING
```

Exit 1 means no project key was ever heard as a boundary. Show the user the config's `projects` list and ask what prefixes the room actually says out loud and what they sound like — "the plat board", "platform dash ninety one" — then add them under `[spoken_aliases]` and rerun. A missing alias costs a whole segment silently.

Exit 4 means the transcript names no ticket keys at all, typed or spoken. That is a planning session, where tickets are made in the call rather than discussed, and stage mode has nothing to refine. Delete the empty STAGING the redirect created and skip Steps 2 through 4. Read the transcript yourself, draft each new-work moment in the Gaps to file shape Step 3 defines—`file-issue`'s task shape plus the line saying where filing it would land—and show the user those drafts. They are the run's deliverable.

`segment.py` writes the skeleton and nothing else, so the shape line is yours to compose. Rerun the same command with `--json` appended and read `stats` (`boundaries`, `revisited_total`, `mentioned_in_passing`, `median_duration_seconds`) and `preamble.turns`, then print one line like `4 segments, 1 revisited, 1 mentioned in passing, 2 preamble turns; median 1m40s`. That line is the user's correction point: it is where they notice the session they remember had six tickets in it.

**Done when:** STAGING exists and the shape line has been printed, or, on exit 4, no STAGING file remains and every new-work moment in the transcript has a draft the user has seen.

### Step 2 — Fill each entry from its excerpt

Read [`references/ticket-template.md`](references/ticket-template.md) once, then work entry by entry. The rules that decide what gets written are these, and they apply on every run:

Every non-empty line under Acceptance criteria, Dependencies, Goal, and Labels ends in `(raw: "four to ten verbatim words" HH:MM:SS)`. The snippet is authoritative and quoted exactly from the excerpt: `check-staging.py` fails the line unless those words appear in that entry's Source excerpt, whitespace aside. Use `L<n>` in place of the timestamp only for a plain-text transcript that carries no clock.

**NEVER invent acceptance criteria.** Write a criterion only where someone stated a condition, a number, a behavior, or a case, or where the excerpt admits no other reading. A criterion that follows logically from what was said is still not something anyone said. A section the room never reached stays empty and takes a `- not discussed: <section>` line under Open questions instead — one per empty content section, always, and never alongside content in the same section.

**Describe outcomes, not implementation.** Where the room only discussed implementation — a table, a queue, a library — write the outcome that implementation serves, and quote the implementation itself under Open questions where a reader can see it was the room's idea rather than a decision this file made.

A Dependency is a key from the entry's `mentions:` list or an explicit blocked-by statement, and nothing else. A key someone said while discussing something else is a mention, not a blocker; each dependency becomes a real Jira issue link, so a wrong one costs somebody a conversation. A Goal goes in only where a product owner named one — inferring it from the acceptance criteria is exactly the failure this step guards against. Provenance is script-filled and is not edited by hand; its values are checked against the frontmatter.

A `### Labels` section exists only on a `schema: 2` file, which `segment.py` writes when CONFIG declares `[label_families]`. A label is stated, like a Goal: write `- <label> (raw: "…" HH:MM:SS)` only where a speaker said one of that label's configured phrases, and quote a snippet that holds the phrase, since `validate` checks it against that label's list. Keep each family within its `max`. A family the room never named keeps the `- not discussed: labels/<family>` line the skeleton wrote; delete that line when you add a label from its family. A Labels line carries the room's words and nothing else: a ticket's subject, its epic, and its acceptance criteria are never a source for one, because a wrong label files the ticket under somebody else's capability.

**Done when:** every entry has every section its `schema:` calls for (eight on schema 1, nine on schema 2), every anchored snippet appears verbatim in that entry's own excerpt, every empty content section carries its `not discussed` line, and every label family has either a stated label or its `labels/<family>` line.

### Step 3 — Summary

Under Spike candidates, keep the `long` and `revisited` flags `segment.py` already wrote and add `circular` where the same question reopened without landing, quoting two anchors that show it. Those first two are arithmetic; `circular` is a reading, which is why it is yours. Leave Mentioned in passing exactly as the script wrote it.

Under Gaps to file, draft each "we need a ticket for X" moment in `file-issue`'s task shape — `# title`, `**Parent:**`, `**Blocked by:**`, `## What and Why`, `## Acceptance Criteria`, `## Non-Goals` — and follow it with an honest line about where filing it would land. `file-issue` writes to GitHub through `gh` and has no Jira path today, so on a Jira backlog the draft **is** the deliverable: say so, and say that filing it means the user carrying it into Jira themselves. Once `file-issue` can write where these tickets live, that line becomes a fenced `/file-issue --fast <draft>` for the user to run. A command that would file a client's ticket into the wrong tracker is worse than no command.

**Never create it here**, and never route it through `jira-apply.py create`. A gap ticket drafted from a passing mention in a transcript has not been interviewed, and `file-issue` exists to do that interviewing.

**Done when:** all four Summary subsections exist, and every gap carries a draft plus an accurate statement of where filing it would land.

### Step 4 — Validate and stop

```
jira-refine/scripts/check-staging.py validate STAGING
```

A non-zero exit is a hard stop. Each stderr line names one broken rule from [`references/staging-format.md`](references/staging-format.md); fix the file and rerun until it exits 0.

Then report STAGING's path, the count per status, and this, plainly: nothing has been pushed anywhere. The user flips each entry's `status: staged` to `approved` or `skipped` in an editor, then runs `/jira-refine --apply STAGING`.

**Stage mode never calls `jira-apply.py`.** It holds no credentials, opens no connection, and cannot write to a tracker even if asked.

**Done when:** `validate` exits 0 and the user has been told the file is theirs to review.

## Apply mode

### Step 1 — Validate from disk

Run `check-staging.py validate STAGING` again, against the file as it now sits on disk. Non-zero is a hard stop: the user edited it since Step 4, and a file that no longer parses cannot be pushed safely. Then:

```
jira-refine/scripts/check-staging.py entries STAGING --status approved
```

Zero lines → stop with "nothing approved", and name what the other statuses are.

**Done when:** `validate` exits 0 and at least one approved entry exists.

### Step 2 — Preflight

```
jira-refine/scripts/jira-apply.py get <first approved key> --config CONFIG
```

Exit 3 is a configuration, credential, transport, or Python-floor problem. Stop and give the user the message verbatim — it names the missing piece, and paraphrasing it costs them the fix.

Where `fields.goal` is unset in CONFIG and any approved entry carries a Goal, tell the user it will fall back into the description block and report `unmapped`, which is a normal outcome rather than a failure. Offer the discovery command, and say that it prints candidates without ever writing the config:

```
jira-refine/scripts/jira-apply.py fields --name goal --config CONFIG
```

**Done when:** `get` returned an issue, and any unmapped Goal has been named to the user.

### Step 3 — Dry run, always

```
jira-refine/scripts/check-staging.py entries STAGING --status approved \
  | jira-refine/scripts/jira-apply.py update --config CONFIG --dry-run
```

Stderr carries one plan line per entry and a totals line; stdout carries the report JSON. Show the user the plan lines. A non-zero exit here is the report speaking, not a stop: it means some entry planned a `conflict`, `missing-issue`, or unmapped field, and those entries will report the same thing on the real run. Name them in the ask.

Then ask once: push these N entries? The confirmation always runs, and no flag skips it. A no, or DRY_RUN set, ends the run here — the staging file is untouched and nothing has been written.

**Done when:** the plan lines have been shown and the user has answered.

### Step 4 — Apply

Same pipeline without `--dry-run`, writing the report beside the staging file:

```
jira-refine/scripts/check-staging.py entries STAGING --status approved \
  | jira-refine/scripts/jira-apply.py update --config CONFIG --report <STAGING stem>.apply-<YYYYMMDD-HHMMSS>.jsonl
```

**Done when:** every approved entry appears in the report exactly once.

### Step 5 — Reconcile

Walk the report and write each verdict back into STAGING:

| Report line | Entry becomes |
|---|---|
| `conflict` is non-null | `status: conflict`, plus a `conflict: <the reason, verbatim>` line. This row wins wherever both match |
| otherwise `description` is `applied` or `already-present` | `status: applied`, plus an `applied: <timestamp>` line |

Then append a `#### <YYYY-MM-DDTHH:MM:SS>` block under `### Apply log` holding the run's totals and one line per `unmapped` field naming the entry, the field, and the fallback it took. The Apply log is where a per-run note belongs, and it is the only place one fits: an entry's own sections are a fixed grammar, and an extra bullet under Provenance fails `validate` with `Provenance has 4 bullets, expected 3`.

Run `check-staging.py validate STAGING` once more, so a reconcile that broke the grammar surfaces now rather than on the next run.

Close by telling the user which entries conflicted and why, that setting `on_conflict: append` or `on_conflict: replace` on an entry and flipping it back to `status: approved` resolves it on the next run, and that the Gaps to file drafts from stage mode are still waiting to be filed.

**Done when:** every report line has been written back, the Apply log block exists, `validate` exits 0, and the conflicts and the outstanding gaps have both been named.

## Further Reading

- [references/ticket-template.md](references/ticket-template.md) — read at stage Step 2, for what each field holds (seven, plus Labels on a schema-2 file) and what counts as stated
- [references/staging-format.md](references/staging-format.md) — read when `validate` fails, or when editing a staging file by hand
- [references/tracker-contract.md](references/tracker-contract.md) — read when an apply run reports anything other than `applied`, for the entry and report shapes, the exit codes, and all eight idempotency rules
- [scripts/segment.py](scripts/segment.py) — stage Step 1: transcript to staging skeleton
- [scripts/check-staging.py](scripts/check-staging.py) — the gate at stage Step 4 and apply Step 1, and the entry source for apply Steps 3 and 4
- [scripts/jira-apply.py](scripts/jira-apply.py) — apply Steps 2 through 4: the only file here that talks to a tracker
