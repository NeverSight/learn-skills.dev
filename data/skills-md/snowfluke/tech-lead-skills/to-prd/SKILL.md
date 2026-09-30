---
name: to-prd
description: Add a feature or change request to a project that is already running. Turns the latest grill-me decision log, or the conversation, into new user stories and acceptance criteria, continuing the US and AC numbering, in docs/business/ in us-ac-formatter's format or in the project's older business docs in their own layout and language. Asks only for what the acceptance criteria need and the input lacks, lists the specs the change touches, and opens a parent GitHub issue that links it all. Use when the user wants a PRD, wants to add a feature mid-project, or asks to turn a discussion into stories. Hands off to to-issues.
---

# To PRD

The mid-project entry to the pipeline. `product-discovery` and `us-ac-formatter`
start a project. This skill adds to one that already runs, in the same format,
so `docs/business/` stays the single source of truth.

## 1. Read the input and the project

- **Input.** Take the latest decision log in `docs/decisions/`, if `grill-me` wrote one for this feature. Otherwise use the conversation.
- **Business docs.** Read `docs/business/user-story.md`, `sprint-breakdown.md`, and the per-sprint files under `acceptance-criteria-breakdown/`. An older project may keep its stories and criteria in other files, for example `docs/USER_STORY.md` and `docs/ACCEPTANCE_CRITERIA.md`. Note the highest US and AC numbers, and how the project groups its work.
- **Glossary.** Read `docs/GLOSSARY.md` if it exists, and use its terms.
- **Specs.** Read the index of `docs/technical-specs/` and of `docs/api-specs/`: `_index.md`, or an older name such as `0.technical-index.md`.
- **Issue conventions.** Read `.github/ISSUE_TEMPLATE/` (including `config.yml`), and list the labels and milestones with `gh label list` and `gh api repos/{owner}/{repo}/milestones`. Step 6 follows them.

If `docs/business/` does not exist, pick the case that fits:

- **Older business docs exist.** They are the source of truth. Continue their US and AC numbering, and write in their layout and language. Ask once whether to migrate them into `docs/business/` instead. Never start a second set next to them.
- **No business docs in any form, but code exists (adopt mode).** Create the skeleton in `us-ac-formatter`'s file targets: `user-story.md`, `sprint-breakdown.md`, and `acceptance-criteria-breakdown/` with the first sprint file. Start at `US-01`. Features that already shipped get no stories.
- **No code yet.** This is a new project. Stop and point the user at `product-discovery`.

## 2. Draft the stories and criteria

- One `US-XX` per actor goal, numbered from the next free number, with persona, action, and business value.
- One `AC-XX.YY` per observable outcome, as a Gherkin scenario.
- Write the prose in the business docs' language. Keep UI labels, messages, and domain terms verbatim; never translate them.

## 3. Ask about the gaps

Ask only what a THEN clause needs and the input does not give: the exact message
or label text, the role that may act, and the empty, error, and loading states.
Ask where the stories belong in the project's grouping of work. Never guess. Use the grouping of the file you write into. If the project groups work another way (priority tiers, milestones), use its grouping. If the business docs have no grouping, add none; the board places the cards later. Do not reconcile other groupings the project keeps elsewhere. If it groups work by sprint and the sprint is new, also ask for its goal title, and add the sprint to `sprint-breakdown.md` in `us-ac-formatter`'s format before step 4 runs the index script.

Ask one question at a time, each with a recommended answer, the way `grill-me`
does. Then show the full draft and get the user's approval.

## 4. Write the business docs

**`docs/business/`.** Read the `us-ac-formatter` skill's `references/layout.md`
and follow its output format and file targets exactly. Merge into the existing
files. Do not rewrite stories or criteria that are already there. Then
regenerate the AC index with that skill's script:

```bash
python3 <us-ac-formatter dir>/scripts/build_ac_index.py --business-dir docs/business --write
```

**Older business docs.** Add the new stories and criteria in the files and
layout they already use: for a table, one new row per story or criterion with
the table's columns. Do not run the index script; it reads only
`docs/business/`.

Hand the changed files to `git-commit`. The parent issue links to them, so the
user pushes before step 6.

## 5. List the spec impact

Name each section in `docs/technical-specs/` and `docs/api-specs/` that the
change touches, and say what must change there in one line each. Do not edit
the specs here. `technical-spec` and `api-spec` own them.

## 6. Open the parent issue

Check the issue convention from step 1 first. If the project does not file
issues for planned work (for example its template says to reference the task ID
in the pull request), open no issue. Save the body as
`docs/decisions/<YYYY-MM-DD>-prd-<slug>.md` instead, and report its path. The
next step is `to-issues` with that file.

Otherwise show the issue to the user, and create it only after they approve:

```bash
gh issue create --title "US-XX <feature name>" --body-file /tmp/prd-<slug>.md <labels and milestone per the project's convention>
# In a project that github-project-init set up, for example:
#   --label type:feature --label sprint:<n> --milestone "Sprint <n>: <goal>"
```

The project's issue conventions from step 1 are the source of truth. If
`github-project-init` set the project up, use its labels and milestones; if one
is missing, show it to the user, and after they agree create it the way that
skill does (Phase 2, sections A and D). If the project has its own labels, use
the closest of those. Add a label or milestone only after the user agrees. The body follows [references/parent-issue.md](references/parent-issue.md).

Report the issue number. The next step is `to-issues` with that number.
