---
name: brainstorm-to-issue
description: >
  Turns a completed brainstorming conversation about a problem into a GitHub
  issue using a fixed five-section intent template (Problem, Proposed
  outcome, Affected users and systems, Constraints, Open questions). Trigger
  this when the user says the brainstorm is done and asks to file, create,
  or open an issue for it — not while still exploring the problem.
---

# Brainstorm → GitHub Issue

## Relationship to Superpowers

If Superpowers is installed, this skill and Superpowers' own `brainstorming`
skill are sequential, not competing:

- This skill captures **intent** — a short problem/outcome write-up — and
  runs first, before any implementation planning.
- Superpowers' `brainstorming` produces the full **spec** — the detailed,
  implementation-relevant design — and runs second, once the intent issue
  exists.

Don't let this skill's synthesis expand into spec-writing territory
(alternatives considered, technical constraints, out-of-scope boundaries)
— that's Superpowers' job, seeded from this issue by the
`superpowers-issue-bridge` skill.

## When this applies

The user has been discussing a problem, need, or idea conversationally
(with any AI agent — this isn't specific to a coding session) and now wants
that discussion turned into a tracked GitHub issue. Do not run this while
the problem is still being explored — only once the user signals it's
ready (e.g. "create the issue for this," "file this," "let's turn this
into an issue").

## Preconditions

1. Check for `docs/agents/issue-tracker.md`. If it doesn't exist, tell the
   user to run the `configure-issue-tracker` skill first, and stop — don't
   guess a tracker or repo.
2. Read the tracker config from that file:
   - **GitHub backend:** use the `owner/repo` it records. Confirm `gh`
     is authenticated (`gh auth status`); if not, tell the user to run
     `gh auth login` and stop.
   - **Local markdown backend:** write to `.scratch/<feature>/` instead of
     creating a GitHub issue — skip all `gh` steps below and use a
     slugified title as the filename.
   - **Other/freeform backend:** follow whatever the recorded notes
     describe; ask the user if the notes don't cover this case.
   - If the user explicitly names a different repo/tracker for this one
     run, use that instead of the config — a one-off override doesn't
     require re-running setup.

## Steps

1. Re-read the brainstorming conversation and extract, in the user's own
   words wherever possible:
   - **Title** — a short name for the problem/feature (this becomes the
     issue title, not a `#` heading inside the body).
   - **Problem** — what's wrong today, for whom, and why it matters.
   - **Proposed outcome** — what "better" looks like, stated as an outcome
     not an implementation.
   - **Affected users and systems** — who and what this touches.
   - **Constraints** — any hard limits already mentioned (compliance,
     security, scope boundaries, deadlines).
   - **Open questions** — anything genuinely unresolved. Leave real
     uncertainty in rather than inventing a confident answer.
2. If any section has no real content from the conversation, write
   "None identified" rather than fabricating detail — do not pad sections
   to look complete.
3. Draft the issue body using exactly this template. The title is used
   twice — once as the GitHub issue title itself, and once as the H1 at
   the top of the body, so the content still reads correctly if exported,
   printed, or viewed outside GitHub's issue chrome:

   ```markdown
   # {title}

   ## Problem
   {problem}

   ## Proposed outcome
   {proposed_outcome}

   ## Affected users and systems
   {affected}

   ## Constraints
   {constraints}

   ## Open questions
   {open_questions}
   ```

4. Show the drafted title and body to the user and ask for confirmation
   or edits before creating anything. Do not create the issue silently.
5. Once confirmed, create it:

   ```bash
   gh issue create \
     --repo <owner>/<repo> \
     --title "<title>" \
     --body-file <tmp-file> \
     --label <label from docs/agents/issue-tracker.md, default: intent>
   ```

   (Create the label first with `gh label create <label>` if it doesn't
   exist yet — don't fail silently if the label is missing.)

6. Report the issue URL back to the user. This issue is the entry point
   ("intent issue") for the project/feature going forward — later stages
   (spec, plan, PR) should reference its number. If Superpowers is
   installed, tell the user this issue is now ready to hand off: starting
   Superpowers' `brainstorming` skill referencing this issue number (the
   `superpowers-issue-bridge` skill handles seeding it in) is the natural
   next step.

## What NOT to do

- Don't run this mid-brainstorm — wait for explicit confirmation the
  discussion is done.
- Don't invent content for empty sections.
- Don't create the issue without showing the draft first.
- Don't guess the target repo if it can't be inferred.

---

## Non-Claude-Code version (plain prompt)

For tools without a skills/auto-discovery mechanism, paste this as a
one-off prompt once brainstorming is done:

> Based on our conversation above, draft a GitHub issue using exactly this
> template — an H1 with the title, then Problem, Proposed outcome,
> Affected users and systems, Constraints, Open questions — each section a
> few sentences, using "None identified" for anything we didn't actually
> discuss. Give me the title and body as plain text; don't create anything
> yet, just show me the draft.

Then create it yourself with:

```bash
gh issue create --repo <owner>/<repo> --title "<title>" --body-file draft.md --label intent
```
