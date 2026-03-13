---
name: laravel-progressive-learning
description: |
  Maintain a per-repo guideline that tracks mistakes, corrections, and
  what works for Laravel/PHP work. Activates EVERY session, unconditionally.
  Read the guideline before doing anything. Write to it continuously as you
  work — not just at session boundaries. Log your own mistakes, not just user
  corrections. The guideline lives in the repo at `.ai/guidelines/`.
author: ivanfuhr
version: 1.0.0
date: 2026-02-08
---

# laravel-progressive-learning Guideline (Laravel/PHP)

You maintain a per-repo markdown guideline that tracks mistakes, corrections,
and patterns that work or don't. You read it before doing anything and update it
continuously as you work — whenever you learn something worth recording.

**This guideline is always active. Every session. No trigger required.**

## Session Start: Read Your Guideline

First thing, every session — read `.ai/guidelines/learning.md` before doing
anything else. Internalize what's there and apply it silently. Don't announce
that you read it. Just apply what you know.

If no guideline exists yet, create one at `.ai/guidelines/learning.md`:

```markdown
# laravel-progressive-learning Guideline (Laravel/PHP)

## Corrections
| Date | Source | What Went Wrong | What To Do Instead |
|------|--------|----------------|-------------------|

## User Preferences
- (accumulate here as you learn them)

## Patterns That Work
- (approaches that succeeded)

## Patterns That Don't Work
- (approaches that failed and why)

## Domain Notes
- (project/domain context that matters)

## Laravel/PHP Notes
- (framework-specific rules, conventions, or gotchas)
```

Adapt the sections to fit the repo's domain. Design something you can usefully
consume.

## Continuous Updates

Update the guideline as you work, not just at session start and end. Write to
it whenever you learn something worth recording:

- **You hit an error and figure out why.** Log it immediately. Don't wait.
- **The user corrects you.** Log what you did and what they wanted instead.
- **You catch your own mistake.** Log it. Your mistakes count the same as
  user corrections — maybe more, because you're the one who knows what went
  wrong internally.
- **You try something and it fails.** Log the approach and why it didn't work
  so you don't repeat it.
- **You try something and it works well.** Log the pattern.
- **You re-read the guideline mid-task** because you're about to do something
  you've gotten wrong before. Good. Do this.

The guideline is a living document. Treat it like working memory that persists
across sessions, not a journal you write in once.

## What to Log

Log anything that would change your behavior if you read it next session:

- **Your own mistakes**: wrong assumptions, bad approaches, misread code,
  failed commands, incorrect fixes you had to redo.
- **User corrections**: anything the user told you to do differently.
- **Tool/environment surprises**: things about this repo, its tooling, or its
  patterns that you didn't expect.
- **Preferences**: how the user likes things done — style, structure, process.
- **What worked**: approaches that succeeded, especially non-obvious ones.

Be specific. "Made an error" is useless. "Assumed the API returns a list but
it returns a paginated object with `.items`" is actionable.

## Laravel/PHP Reminders

- Prefer Eloquent models and relationships over raw queries.
- Use Form Request classes for validation, not inline rules.
- Use Laravel helpers like `str()` and `collect()` instead of native functions.
- Avoid `DB::` unless necessary; prefer `Model::query()` and transactions.
- Use `vendor/bin/sail` for all Artisan/Composer/PHP/Node commands.

## Guideline Maintenance

Every 5-10 sessions, or when the file exceeds ~150 lines, consolidate:

- Merge redundant entries into a single rule.
- Promote repeated corrections to User Preferences.
- Remove entries that are now captured as top-level rules.
- Archive resolved or outdated notes.
- Keep total length under 200 lines of high-signal content.

A 50-line guideline of hard-won rules beats a 500-line log of raw entries.

## Example

**Early in a session** — you misread a function signature and pass args in the
wrong order. You catch it yourself. Log it:

```markdown
| 2026-02-06 | self | Passed (name, id) to createUser but signature is (id, name) | Check function signatures before calling, this codebase doesn't follow conventional arg ordering |
```

**Mid-session** — user corrects your import style. Log it:

```markdown
| 2026-02-06 | user | Used relative imports | This repo uses absolute imports from `src/` — always |
```

**Later** — you re-read the guideline before editing another file and use
absolute imports without being told. That's the loop working.

----------------

IMPORTANT: Instead of creating a logs file, create a Boost guideline in
`.ai/guidelines/` (see https://laravel.com/docs/12.x/boost#adding-custom-ai-guidelines)
and then run `php artisan boost:update --ansi`.
