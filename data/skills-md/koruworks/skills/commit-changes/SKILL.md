---
name: commit-changes
description: Write a high-level commit summary of the current work — what changed and why the decisions were taken — show it for approval, then commit on approval without pushing. Use when the user asks to summarise, write up, or commit a batch of work, or says "commit this" / "write a commit message". Its length is proportional to the change — a one-line fix gets a sentence or two, a multi-file batch gets the full sectioned body. The summary is also read downstream by people and LLMs generating changelogs, release notes, marketing copy and user-guide updates, so it is written for that second audience as well as for git. Never commits a binary file without asking first.
---

# Commit summary

A commit message is read three times: by the next person doing `git log`, by
whoever writes the changelog, and by an LLM asked to turn a release into
marketing copy or a user-guide section. Write once, for all three.

## The shape

1. **Verify before you describe.** Run the project's formatter and the tests
   proportionate to the change, using the project's own commands. The summary
   states test status as fact, so it has to be one; explicitly name any
   checks that were not run.
2. **Read the actual diff** — `git status --short`, `git diff --stat`, and the
   hunks for anything you did not write yourself this session. Do not
   summarise from memory of the conversation; the tree is the truth. Check the
   staged set for binaries while you are here — see *Binaries need approval*.
3. **Size it to the diff** (see *Proportion* below), then **draft the
   summary** to the structure — using only the parts the change has earned.
4. **Show it to the user and stop.** Do not commit yet. (A skill that runs
   unattended — such as execute-plan — may pre-approve this step; it says so.)
5. **On approval, commit. Never push.** Push only if asked in that same
   breath.

## Proportion

The message is as long as the change, not as long as the template. Every
reader below pays for padding: the person skimming `git log` has to scroll
past it, and the changelog LLM will dutifully inflate a one-line fix into a
feature announcement if the body reads like one.

- **A small fix** — one hunk, one file, one visible effect — gets a subject
  and one to three sentences: what was wrong, what changed, and the *why* if
  it is not obvious from the diff. No headings.
- **A medium change** — several files, one feature or one bug with a decision
  in it — gets the opening paragraph plus whichever of the sections below have
  real content. Usually that is *Decisions* and *Verification*; a bug found
  along the way earns its paragraph, an absent one earns no heading.
- **A large batch** — many files, several features, or a merge — gets the full
  structure. This is the case the template below was written for.

The rule for any section is the same: it appears when it has a fact to carry
and disappears when it does not. A heading with one sentence under it is a
sign the change was smaller than the template. Do not write "Trade-offs:
none" — leave it out.

The audiences do not change the length, only what must survive the cut:

- **`git log`** needs the subject to say what changed for a user, at every
  size.
- **The changelog** needs one sentence it can lift whole. In a small fix that
  is the first sentence of the body, so write it in user terms even when the
  fix is a typo in a list.
- **The next engineer** needs the *why* whenever the diff does not say it. A
  two-line fix whose reason is not obvious still gets its reason; a
  twenty-file refactor whose reason is obvious does not get a *Decisions*
  section pretending otherwise.

Verification is the one part that is never cut for size, only shortened: a
small fix says in a clause what was run and what was not.

## Structure

The full shape, for a large batch. Smaller changes take the subject, the
opening, and only the sections that have content — see *Proportion*.

```
<subject: what a user can now do, or what changed for them — one line>

<opening: the problem it solves, in two or three sentences. What was wrong
before, and what the change is. This paragraph is the one a changelog or a
marketing blurb can lift whole, so write it in user terms, not module terms.>

<Themed sections with headings.> Group by what the reader cares about, not by
module or file. "The menu", "The tab strip", "Typography" beat
"src/menu" and "lib/render".

<Decisions worth keeping.> For each: what was chosen, what the alternative
was, and why it lost. A decision recorded without its alternative is an
assertion; with it, it is an argument the next person can re-open honestly.

<Bugs found along the way.> Especially pre-existing ones. Say plainly whether
a user would have felt it — that is what decides if it earns a changelog line.

<Trade-offs and costs.> What got worse, what a behaviour change costs someone
who relied on the old one.

<Closing: verification.> What was tested, what was confirmed by running the
app, and — separately and explicitly — **what was not**.
```

## What makes these summaries useful

- **Lead with the user-facing change**, not the refactor that enabled it. The
  refactor goes lower down, where it explains *how* rather than *what*.
- **Say why, not just what.** `git diff` already says what. The reasoning is
  the only part that cannot be recovered from the tree.
- **Name the alternative that lost.** "A second menu beside the first, not one
  nested inside it, because nesting would have meant teaching three functions
  about depth" tells the next person why not to 'simplify' it back.
- **Record surprises.** A platform quirk, an API that did not behave as
  documented, a constant that turned out to be load-bearing. That is the
  content nobody can rederive.
- **Flag what is unverified, in its own sentence.** A downstream LLM will
  happily announce a feature ships. If something is only unit-tested, or was
  never seen running, say so where it cannot be skimmed past.
- **Keep it concise per point, not few points.** Dense is fine; padding is
  not. Every line should carry a fact a reader could not guess — and if the
  change has only three such facts, the message is three sentences long.

## Honesty rules

These matter more than usual, because a summary is amplified downstream.

- Never describe a behaviour that is not in the diff.
- Never claim a test or a manual check that was not run.
- If a change is behind a flag, say which flag and what its default is.
- If something is platform-specific, say so — a changelog that promises Linux
  users a Windows-only feature is a support ticket.
- Prefer "not visually confirmed" over silence. Silence reads as confirmed.

## Binaries need approval

**Never commit a binary file without asking the user first.** Not a video,
not an audio file, not an archive, not a compiled artifact, not a font, not a
large image. Ask, name the file and its size, and wait.

The reason is that git history is permanent. A blob committed once is carried
by every clone forever, even after a later commit deletes the file — the
working tree looks clean while `.git` keeps paying. Getting it back out means
rewriting history, which is cheap on a private branch and disruptive once it
has been merged and pulled. There is no quiet way to undo this later, which is
why the gate sits before the commit rather than after it.

Check the staged set before every commit, not the working tree — a binary
shows as `-` in both numstat columns:

```sh
git diff --cached --numstat | awk '$1=="-" && $2=="-" {print $3}'
```

If that prints anything, stop and ask. Say what each file is, how big it is,
and why the change seems to want it. Two answers are usually better than
committing:

- **Host it instead.** Media, sample recordings and downloadable payloads
  belong on an asset host or object storage, with the repo keeping only the
  URL, a checksum (e.g. SHA-256) and a fetch step.
- **Generate it instead.** If a build step can produce the file, commit the
  step and ignore the output.

This is an approval gate, not a ban — some binaries genuinely belong in the
tree, such as a handful of brand assets. The user decides which; the point is
that they get to decide, while the decision is still cheap to reverse.

## Committing

- Fold the docs into the same commit. Docs are part of the change, so a
  summary that mentions a decision should have its decision record beside it,
  if the project keeps them.
- **Amend or new commit** is a judgement, and worth stating rather than
  assuming: amend while the existing commit is still the same unit of work,
  start a new one when the batch is a distinct step. Say which you chose and
  why, so the user can redirect.
- End the message with whatever co-author or sign-off trailer your own
  environment or the project requires — never one copied from another agent's
  session.
- Write the message from a file or a heredoc, never a chain of `-m` flags —
  the structure above does not survive them. On Windows PowerShell prefer
  writing the body to a file and `git commit -F path`.
- **Do not push.** Not as a follow-up, not as a convenience.

## Watch out for

- **Untracked junk.** Check `git status` for stray files before `git add -A`;
  exclude them rather than committing them. Path-exclude pathspecs can fail on
  odd filenames — verify with `git status` after staging, not before.
  `git add -A` is also how binaries get in by accident: run the numstat check
  above afterwards.
- **Reformatting you did not intend.** A formatter may touch files unrelated
  to the change if the tree was not clean to begin with. Mention it rather
  than letting it look deliberate.
- **A stale build.** If the user has been testing while you worked, their
  screenshots may predate the change being described. Worth a sentence when
  their feedback and the code disagree.
