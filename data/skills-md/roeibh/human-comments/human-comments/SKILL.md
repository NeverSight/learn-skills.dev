---
name: human-comments
description: Write code comments the way a senior engineer would — almost none, and the few that survive are short human fragments, not sentences. The code documents itself; a comment is a last resort for what the code genuinely cannot say. Use this WHENEVER writing or editing code in any language, and especially when the user complains that comments are too verbose, too long, noisy, "AI-sounding", essay-like, or that they add lines to a diff or PR. Triggers on "fewer comments", "shorter comments", "stop over-commenting", "these read like AI wrote them", "make comments concise", "the code should self-document", or any time you are about to add a comment to code.
---

# Human-like comments

The default is **no comment**. Good code documents itself through names, types, and structure. A comment is what you write when — and only when — the code genuinely cannot carry the information itself. Treat every comment as a small failure you have to justify.

AI over-comments compulsively: it narrates each step, restates the code in prose, and turns a one-word gotcha into a three-sentence paragraph written for a stranger. A senior engineer does the opposite — they delete, rename, and only when truly stuck leave a terse fragment for the next person.

## Before writing a comment, try to delete the need for it

In order, these usually beat a comment:

1. **The code already says it.** `// increment the counter` above `counter++` → delete. If a reader can see it, don't narrate it.
2. **A better name says it.** Rename the variable, function, or constant; extract a named boolean or helper. `if (u.age >= 18 && u.verified)` → `if (isEligibleVoter)` kills the comment that would have explained it. Prefer this over commenting.
3. **A type says it.** An enum, a union, a branded type, or a non-null signature often removes the comment entirely.
4. **It's design rationale, not a code fact.** Long "why we chose this approach" reasoning belongs in the commit message, PR description, or an ADR — not wedged inline. Inline, leave at most a one-line pointer.

Only if none of these apply does a comment earn its place.

## If a comment must survive, make it short and human

- **One line. A fragment, not a sentence.** How a dev jots a note to a teammate, not how a manual is written. No preamble, no full grammar if a phrase does it. `// off-by-one: API is 1-indexed` — not "We subtract one here because the external API uses 1-based indexing whereas our array is 0-based."
- **Only the surprising part.** The reader can see *what* the code does. Tell them the one thing they can't see and would get wrong: the gotcha, the reason, the constraint, the footgun.
- **If it needs a second sentence, stop.** That's a signal the code should be clearer, or the explanation belongs in a PR/ADR. Cut it down or move it out.
- **Match the file.** Mirror the surrounding density and tone. If neighbors have no comments, don't be the one who adds a paragraph.
- **Keep existing markers and house style.** An established convention is not AI noise: preserve `TODO:`/`FIXME:`/`HACK:`/`NOTE:` tags, tool markers like `ponytail:`, ADR markers, and numbered-step sequences. Trim the prose around a marker, never the marker itself.
- **Above the code, not trailing** — except a short clarifier on a single value.

## The AI tells to strip

If a comment has any of these, it reads as AI-written. Fix or delete:

- Full, grammatically complete sentences explaining the *mechanism* ("We iterate over each item, check whether it is already in the set, and if not add it, so that...").
- Restating the signature in a docstring ("Build the config object for the request" above `buildRequestConfig(): RequestConfig`).
- Narrating history or edits: "added", "changed", "now handles", "updated to", "previously".
- Hedging and over-explaining: spelling out every branch, every guarantee, every edge case the code already handles visibly.
- Decorative banners and section headers (`// ===== Helpers =====`).
- Commented-out code — delete it; that's what git is for.
- A guard comment restating the guard (`// skip if empty` above `if (!items.length) return`).

## What actually earns a comment

Short list. If it isn't roughly one of these, you probably don't need it:

- A non-obvious **why** or gotcha the code can't show (`// provider webhook can beat its own DB commit`).
- A **workaround** with its cause, ideally a link (`// works around nodejs/node#1234`).
- A **warning / footgun** (`// order matters: auth must run before rate-limit`).
- A **cross-file coupling** the reader would miss (`// keep in sync with schema.prisma`).
- A pointer to deeper context — keep what makes it navigable (`// see docs/adr/0003-….md`, a URL, or an issue #), not just a bare id.
- A public/exported **API docstring** where the codebase clearly expects them — and even then, only the non-obvious, never a re-type of the signature. Keep it to 1–2 lines, leading with the non-obvious; if it needs more, that belongs in a doc. Private helpers almost never need one.

## Examples

**Restate the code → delete**
```ts
// Loop over users and send each an email      ← delete
for (const user of users) sendEmail(user);
```

**Better name, no comment**
```ts
// bad: comment props up an unclear name
const d = Date.now() - start; // elapsed time in ms
// good: name carries it
const elapsedMs = Date.now() - start;
```

**Essay docstring → one-line fragment (or nothing)**
```ts
// before (AI): four lines of mechanism
/**
 * Merge the paginated responses into one list. Each page is fetched independently, so the same
 * record can appear on two pages when items shift between requests; this dedupes by id and keeps
 * the newest version, so the returned list never contains a duplicate or a stale row.
 */
// after (human): just the surprising why
// pages can overlap when rows shift mid-fetch, so dedupe by id (newest wins)
```

**Multi-clause why → fragment**
```ts
// before: We add a 250ms delay because the provider's webhook sometimes arrives before their
//         database has committed, causing a race condition.
// after:
// provider webhook can beat its own DB commit
await sleep(250);
```

**Edit narration → the fact, or nothing**
```ts
// before: Changed from 10s to 30s to fix API timeouts
// after:
// upstream p99 ~22s
const TIMEOUT_MS = 30_000;
```

The through-line: first make the code say it. If it can't, one short human fragment about the one thing the reader would otherwise get wrong. Everything else, delete.
