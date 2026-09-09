---
name: git-work-recap
description: Recap a person's authored pull-request work over a day or a longer horizon in concise Markdown, optionally enriched with tracker activity. Use when a user asks what they worked on, requests a stand-up update, daily or weekly summary, sprint or month recap, or asks for PR activity from a date or range such as yesterday, last Friday, this week, or the last two weeks. Searches all accessible repositories by default, treats late-night work as part of the previous workday, and uses the most recent prior workday with activity when no date is supplied.
---

# Git Work Recap

Produce a short, evidence-backed Markdown recap of work represented by an author's own pull requests, plus tracker activity when a tracker is reachable. Scale from a single stand-up day to a multi-week horizon.

## Tools

GitHub is the required spine. Prefer the GitHub connector for PR discovery and metadata when one is available. If no connector is available, use the `gh` CLI (`gh pr list --author <user> --search ...`, `gh pr view <n> --json ...`, `gh api ...`). Use local `git` only to resolve repository context or cross-check related commits; never treat local history as the complete PR record.

An issue tracker (Linear or similar) is an optional lane. Use it only when a connector for it is already available in the session — never install, authenticate, or prompt for one. When it is unavailable, omit the tracker section silently rather than reporting its absence.

This skill only reads — never comment on, edit, merge, or transition anything.

## Resolve inputs

1. Resolve the repository scope in this order:
   - Narrow to a single repository when the user names one, by `owner/name`, repository URL, or plain name, or when they clearly mean the current project.
   - **Otherwise search all accessible repositories, including private ones.** This is the default: a recap question is about what the person did, not about the directory the session happens to start in, and the repository they worked in is frequently not the one they are sitting in. A single author-and-date-scoped search across the account is cheap; the expensive step is metadata hydration, which the budget below already controls.
   - Use the current checkout (`git remote get-url origin`, normalized from SSH or HTTPS, falling back to other remotes) to *order and label* results, not to exclude them. Lead with the checkout's repository when it appears in the results.
   - Never ask which repository to use. Account-wide search always has an answer, even if that answer is "no activity."
2. Resolve the author in this order:
   - Use an explicit GitHub username.
   - Otherwise use the authenticated GitHub connector user (or `gh api user`).
   - Ask for the username only when neither is available.
   - **Scope is strictly PRs this author opened.** Filter every query by author first, then apply the window rules below. Do not include PRs the author only reviewed, commented on, or merged on someone else's behalf.
3. Resolve the timezone explicitly. Use the timezone the user names; otherwise resolve the runtime's zone and state the resolved IANA zone in the result. Never leave the zone implicit — a scheduled or remote run may not share the user's local time.

## Resolve the window

Treat a workday as running from `03:00` to `02:59:59` the following morning, so late-night work counts toward the day it belongs to rather than the calendar day it landed on.

- **Explicit date** — honor it, and apply the same `03:00`–`02:59:59` bounds to that date. Also honor natural-language references such as `yesterday`, `Friday`, or `last Friday`.
- **Explicit range** — honor multi-day horizons such as `this week`, `last week`, `the last two weeks`, `since Monday`, `this sprint`, `August`, or an explicit `date..date`. The range starts at `03:00` on its first day and ends at `02:59:59` after its last day, or at the current time when it includes today. Treat any horizon the user names as legitimate; there is no upper bound on an explicitly requested range.
- **No date, Tuesday through Friday** — cover the previous calendar day from `03:00` through `02:59:59` today.
- **No date, Monday** — cover Friday `03:00` through Monday `02:59:59`, including the weekend.
- **Today so far** — when the request is for the current day's stand-up (no explicit past date), also cover today from `03:00` through the current time as a separate, clearly labeled window.

State the exact dates, times, and timezone each window covers.

If the *default* window has no matching activity and no date or range was supplied, search backward by whole workdays for the most recent one with activity — **at most 2 workdays**, and never further. This cap governs only the search for an unrequested day; it never limits a range the user asked for. If nothing is found, report that clearly instead of guessing or scanning wider.

### Long ranges

A range spanning more than about three workdays changes what is useful, not just how much to fetch. Adjust on both axes:

- **Hydrate selectively.** The candidate-then-hydrate budget below still holds, but a month of PRs will exceed what is worth reading in full. Hydrate the substantial items — larger diffs, PRs whose titles do not state an outcome, anything anchoring a theme — and let list-level metadata carry the rest.
- **Summarize by theme, not by day.** Daily bullets stop being readable past a week. Group by outcome or workstream, then by repository, and use dates only where sequence matters.
- **Report shape and rhythm.** Over a long range, aggregate context earns its place: how many PRs landed, what still sits open at the end of the range, which workstreams dominated, and anything started but not finished. Keep this to a few lines — it frames the themes, it does not replace them.

## Gather evidence

For the resolved author and window, collect the union of that author's PRs that were:

- created in the window;
- updated in the window; or
- merged in the window.

Deduplicate by PR number. Include a PR opened in the window even if it merged later, and include a PR opened earlier if it was updated or merged in the window.

Attribute by actor, not by object. A PR belonging to the author is not evidence that the author did something in the window — someone else's merge, review, or bot push does not count as their work. Prefer event-level evidence (commits, pushes, PR events, review submissions) over a bare `updatedAt` timestamp, and never attribute a generic update timestamp to the author unless the data supports it.

This matters most for merges. A PR the author opened earlier and someone else merged inside the window is the merger's action, not the author's: report it as carry-over that landed, name who merged it, and do not present it as work the author did that day. When `mergedBy` matches the author, the merge is theirs and needs no attribution note.

Fetch metadata efficiently. First identify candidate PRs from list/search summaries, then hydrate **only the candidates for the resolved window** with full metadata — do not eagerly fetch full metadata across the whole backward search range. For each hydrated PR read the title, body, timestamps, and status; read file/line statistics and changed filenames or patch **only when the description is insufficient** to state the outcome. Do not infer substantive work from the title alone.

Because search summaries may omit or normalize dates, verify candidate timestamps against full PR metadata before including a PR in the window.

### Tracker lane (optional)

When a tracker connector is available, collect issues the author created, completed, moved, assigned, or commented on within the same window, as the authenticated user.

Query on more than assignment. An assignee filter misses issues the author filed and handed to someone else, which is exactly the work that leaves no PR trace. Query at least issues assigned to the author and issues created by the author, then filter both to the window using event-level fields — `createdAt`, `startedAt`, `completedAt`, state transitions, comment timestamps — rather than a bare `updatedAt`. Apply the same attribution rule as for PRs.

**Report only what the PRs do not already say.** Most tracker items map one-to-one onto a PR that closes them; listing both sides restates the same work twice. When an issue corresponds to a PR already in the recap, fold it in as an identifier on that bullet instead of giving it its own line. Give tracker items their own bullets when they carry information no PR does — issues filed, triaged, reprioritized, commented on, or moved without code landing. Record issue identifiers and direct links either way.

## Synthesize

Group closely related PRs into a single theme only when they are clearly parts of the same outcome. Otherwise use one bullet per PR. Group by repository when the run spans more than one. Over a long range this inverts: theme grouping becomes the default and a bare per-PR list the exception.

For each item:

- lead with the user-facing or engineering outcome;
- mention the main implementation scope in one compact sentence;
- link the PR number;
- mention carry-over timing only when relevant, such as "opened Friday, merged Saturday."

Avoid repeating PR descriptions, commit-by-commit narration, raw file lists, decorative prose, and unsupported claims. Mention PR counts or aggregate change statistics only when they add useful context.

## Output

Match the output shape to the request.

**Single window, GitHub only** — return the lean form:

```markdown
# Work summary — Friday, 31 July 2026 (Europe/Lisbon)

- **Outcome or theme** — What changed and why it matters. [PR #123](https://github.com/owner/repo/pull/123)

**Overall:** One sentence covering the main themes and relevant PR timing.
```

**Multiple windows, multiple sources, or a range longer than about three workdays** — lead with a 3–6 bullet executive summary, then compact sections. Over a long range, replace the per-window sections with one section per theme or workstream, and let the summary carry the rhythm of the period:

```markdown
# Work recap — Europe/Lisbon

**Summary**
- 3–6 bullets, distinguishing the previous workday from today so far.

## Previous workday — Friday 31 July 03:00 to Saturday 1 August 02:59
- **Outcome or theme** — What changed and why it matters. [PR #123](https://github.com/owner/repo/pull/123)

## Today so far — Monday 3 August 03:00 to 09:15
- **Outcome or theme** — What changed and why it matters. [PR #124](https://github.com/owner/repo/pull/124)

## Blockers and ambiguity
- Anything unresolved, unattributable, or missing evidence.
```

Place tracker items in the relevant window section. Items that duplicate a PR become an identifier on that PR's bullet; items with no PR of their own get their own bullets, labeled as tracker activity. Omit the blockers section when there is nothing to report.

State plainly when a window has no supported activity rather than inventing work or borrowing items from the other window. If nothing matches at all, return the resolved repository, author, timezone, and window plus a plain statement that no authored activity was found.
