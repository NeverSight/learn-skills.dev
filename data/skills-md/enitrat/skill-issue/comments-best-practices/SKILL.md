---
name: comments-best-practices
description:
  Guide for deciding when to keep, write, rewrite, or delete code comments and JSDoc. Use when
  writing new comments, reviewing comments in a PR, or cleaning up commentary in existing code.
  Trigger for "should I comment this", "review these comments", "is this comment necessary", "clean
  up comments", "write jsdoc", "document this function".
---

# Comments Are Deodorant

Kevlin Henney: "Comments are deodorant for stinky code." A comment that exists to make confusing
code bearable is not documentation — it's a mask over a defect. The defect is still there. Robert C.
Martin goes further: "Comments are, at best, a necessary evil... every comment represents a failure
to express ourselves in code." Don't comment bad code — rewrite it.

A comment is untyped, unexecuted, unenforced prose sitting next to code that keeps changing. Nothing
about it stays true unless something forces it to. That's the whole risk profile: every comment you
write is a claim that will silently rot the first time the code around it changes and nobody
remembers to update the sentence.

## The litmus test

Three independent sources — Ousterhout ("comments should describe things that aren't obvious from
the code"), the Linux kernel style guide ("say what the code does, not how"), and Martin's
"redundant comment" smell — converge on one test. Read the comment. Read the code. **If the comment
adds zero information the code doesn't already give you, delete it.** This is not a judgment call to
agonize over; it's mechanical. `i++; // increment i` fails it. So does `// loop over items` above a
for-loop. So does a paragraph explaining what a well-named function obviously does.

A comment only earns its place past this test if it does one of two things (refactoring.guru's
carve-out, the sharpest boundary found across all sources):

1. Explains **why** this approach was chosen over the obvious alternative — rationale the code
   cannot carry no matter how well it's named.
2. Explains a genuinely complex algorithm **after every simplification has already been tried and
   failed** — not as a substitute for trying.

If a comment doesn't clear one of those two bars, it's deodorant. Cut it, and if the surrounding
code is what made the comment feel necessary, fix the code instead: extract a variable, extract a
method, rename, add an assertion for the implicit rule the comment was trying to state in prose. The
comment text is often the method name you're missing — "`# creating report` / `# sending report`"
above two blocks is a signal to extract `createReport()` / `sendReport()`, not to keep the comments.

## Delete on sight — named anti-patterns

Recognize these by name; each is a specific, well-documented failure mode, not a style nit. When you
find one, remove it — don't ask permission, don't soften it into a shorter version of itself:

| Anti-pattern             | What it looks like                                                                                                                                                                                         |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Parrot / redundant**   | Restates exactly what the next line does. The most common offender by volume.                                                                                                                              |
| **Mumbling**             | Vague, unclear, written to satisfy a rule rather than to inform. Worse than no comment.                                                                                                                    |
| **Misleading**           | No longer true. Actively dangerous — a reader trusts it and gets burned.                                                                                                                                   |
| **Rotting**              | Was true once; the code around it changed and nobody updated the sentence. Same danger as misleading — assume any unenforced claim about behavior has already rotted until you verify it against the code. |
| **Journal / changelog**  | "Previously we...", "renamed from...", dated changelog entries. Git already owns history.                                                                                                                  |
| **Mandated / noise**     | Exists only because a rule says every function/getter needs one. Adds nothing.                                                                                                                             |
| **Position markers**     | `////////////////` banners. Rarely earn their visual weight.                                                                                                                                               |
| **Closing-brace**        | `} // end if`. The real signal is that the function is too long to read without one.                                                                                                                       |
| **Attribution/byline**   | "Added by John" — `git blame` does this better and never goes stale.                                                                                                                                       |
| **Commented-out code**   | Dead code kept "just in case." Delete it — version control remembers, the file shouldn't.                                                                                                                  |
| **Nonlocal reference**   | Describes something far away in the system; invalidated by a change the reader can't see.                                                                                                                  |
| **Stale doc/issue link** | Dead ticket refs, `§section` pointers into docs that move or get archived.                                                                                                                                 |

## Keep or rewrite — comments that clear the bar

Keep, and if verbose, tighten to one or two present-tense sentences placed directly beside the
decision they protect (distance breeds drift):

- **Intent / rationale** — why this approach over the obvious alternative.
- **Non-obvious constraints** — API quirks, spec bugs, ordering requirements, race conditions,
  precision/timezone caveats.
- **Business rules** invisible in the code path.
- **Workarounds**, with enough context to know when it's safe to remove.
- **Safety/security rationale** — why something is deliberately omitted or guarded.
- **Performance tradeoffs** a future maintainer could plausibly and reasonably break.
- **Warnings of consequence** — "must run before X", "not thread-safe", "takes 3 hours".
- **Legal/license headers** and **codegen banners** — different category, see "Never touch" below.

If a comment carries real intent but leans on **cryptic private shorthand** (internal rule codes
like `R1`/`R2`, doc-section refs like `§W.6`), rewrite it to restate the actual reasoning inline so
it survives without the external doc — don't just delete it because it's terse.

## JSDoc / TSDoc

The compiler already owns types — Effective TypeScript's rule: "nothing stays in sync unless it's
forced to." A type annotation is forced to stay correct by the type checker; a `@param {number}` tag
is not, and _will_ eventually lie about a signature that changed. Google's TypeScript style guide
draws the same line structurally: `/** */` is API documentation for the consumer, parsed by tooling;
`//` is implementation commentary for the next human reader. Keep them doing different jobs.

JSDoc is a **consumer contract**: it tells someone calling the symbol _what it is_ and _how to use
it_. It is not a place for design narrative, self-justification, project history, or a walkthrough
of the implementation. A consumer never needs to know why v1 is "deliberately narrow" or what got
"removed" — that's inward-facing yapping; delete it.

**Do:**

- Document an exported symbol **only when its name and types don't already convey how to call it.**
  A public boundary does not auto-earn a doc. An added doc that restates the signature is mandated
  noise — don't write it, and delete it where it exists.
- When a doc IS warranted, write **one line**: what the thing is / how a consumer uses it — never
  its internal steps. "Adapts an Executable into a bearer-gated, budget-bounded Vercel cron handler"
  — not a four-clause tour of the auth → budget → status → boot-failure pipeline.
- Use `@param name description` / `@returns description` — description only, never the type.
- Use structured tags where they add real signal: `@remarks`, `@example`, `@deprecated` (with a
  migration path), `@throws`, `@see`/`{@link}`, `@internal`/`@beta`, `@typeParam`.

**Don't:**

- **Never repeat a type in JSDoc.** `@param {number} value` duplicates what the signature already
  guarantees and rots the moment the signature changes without the tag being touched. Write
  `@param value the value to clamp`, not `@param {number} value`. If you find a `{type}` in a
  `@param`/`@returns` tag, strip just the braces and keep the description.
- **Don't re-encode a keyword the language already states** — no `@private` on a `private` member,
  no `@enum` on an `enum`. The keyword is enforced; the tag isn't, so it's the one that goes stale.
- **Don't push a fact into a comment that a type could carry instead.** `// does not modify nums` →
  type the parameter `readonly number[]`. A variable named for what it obviously is
  (`ageNum: number`) doesn't also need a comment restating its type.
- **Don't add JSDoc to trivial internal helpers** whose name and types already say everything.
- **Don't let `@param`/`@returns` restate the obvious** — no `@returns the result`.

## Bias hard toward deletion — worked examples

The default outcome of reviewing a comment is **deletion**. Keeping is the exception you have to
justify, and the justification bar is high. When in doubt, cut. These worked examples set the
calibration — match this severity, not a gentler version of it.

**Internal design rationale is not a keep-worthy "why".** The litmus test keeps rationale the code
can't carry — but that means an _external_ constraint that would bite a maintainer (a third-party
API quirk, a spec bug, an indexing footgun), **not** a story about how you designed this module.
"Deliberately narrow", "the single policy knob", "removed from v1", "a deliberate cliff, not a hooks
layer", "TESTING SEAM: …" all describe your own design process. Delete them. Git and design docs own
that history; the code does not.

**Encodable contracts go into types and tests, not prose.** If an invariant can be expressed as a
type, a `readonly`, a `never` error channel, or a test assertion, encode it there and delete the
sentence. Prose invariants rot; enforced ones can't. A block like
`INVARIANTS (callers may rely on these): 1. execute never fails …` is not a contract — it's a
contract's shadow. The real contract is the `never` channel and the test that asserts ordering.

**Even a legitimate footgun gets one line.** When a constraint genuinely can't be encoded and would
cause a silent bug if a maintainer "simplified" it, name the hazard in a single line. Do not explain
the full mechanism in the comment — that reasoning, if it's worth keeping at all, lives in a design
doc, not beside the code.

**Never cite outside documentation, and avoid naming other code.** A comment must not link to or
cite external docs — no URLs, ticket refs, ADR numbers, `CONTEXT.md`/`ARCHITECTURE.md §` pointers,
spec section numbers. If such a comment carries real reasoning, restate that reasoning inline so it
survives without the doc; if the citation _is_ the content, delete the comment. Likewise avoid
referring to other functions, symbols, test names, or files by name — they go stale on any
rename/move and turn the comment misleading. Rephrase to describe the local behavior directly. The
only cross-references that may stay are ones that don't rot on an internal rename: a stable external
API (viem types, an on-chain revert name), a stable public endpoint path, or a tooling-maintained
`{@link}` — and even then only when load-bearing.

| DON'T (delete or collapse)                                                                                                                                                                                                                                      | DO (what survives)                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `/** Resolves incentive phases into a drip schedule, converting phase days to seconds. */` above `buildDripSchedule(phases): DripSchedule`                                                                                                                      | _(nothing — the name and return type already say it)_                                                                      |
| A 17-line header explaining what a subgraph is, the total-order cursor mechanics, and that responses are validated                                                                                                                                              | `/** Compound (blockNumber, id) cursor — a plain blockNumber_gt cursor silently drops rows in multi-checkpoint blocks. */` |
| `/** Build a Vercel cron handler …: fail-closed bearer auth, an optional liveness ping, the run bounded by the budget, then the graded report mapped to a status (failed → 500, else 200). A boot failure crosses the wire as the canonical aborted report. */` | `/** Adapts an Executable into a bearer-gated, budget-bounded Vercel cron handler. */`                                     |
| `INVARIANTS (callers may rely on these): 1. execute never fails … 2. one report per item …`                                                                                                                                                                     | _(nothing — encode in the `never` channel + a test)_                                                                       |
| A module header narrating "deliberately narrow", "the single policy knob", "removed from v1: recover, numeric concurrency, …"                                                                                                                                   | _(nothing — delete the whole block)_                                                                                       |

**Already at the floor — keep as-is.** These clear the bar because they name an external constraint
in one line and can't be encoded:

- `/** node's crypto.randomInt requires the range span to stay below 2^48. */`
- `// EdDSA signs with no digest; ECDSA/RSA need sha256 — without normalizePem a flattened key fails BAD_END_LINE.`

## Never touch these

Load-bearing directive comments are not prose — leave them exactly as-is, they are read by tooling,
not just humans:

- `eslint-disable`, `oxlint-disable`, `biome-ignore`, `prettier-ignore`
- `@ts-expect-error`, `@ts-ignore`, `@ts-check`
- `"use client"` / `"use server"` pragmas
- Codegen banners (`DO NOT EDIT`, `generated`) and license headers

## Reviewing existing comments

Walk every comment in the file or diff and classify it against the litmus test and the anti-pattern
table above — no comment gets a pass by default. For each one: does it clear one of the two bars? If
not, name which anti-pattern it is and delete it (fixing the underlying code if that's what made it
feel necessary). If it clears the bar but is verbose or cryptic, rewrite it in place. Done means
every comment in scope has been classified and every deletion actually removed from the file — not
summarized as "mostly fine."

---

_Sources: Ousterhout, "A Philosophy of Software Design" (comment red flags, interface vs.
implementation comments); Martin, "Clean Code" ch. 4 (good/bad comment taxonomy); Linux kernel
coding-style.rst §8 (comments); Kevlin Henney ("Comments are deodorant for stinky code");
refactoring.guru "Comments" smell; Google TypeScript Style Guide; Effective TypeScript, Item 30
("Don't Repeat Type Information in Documentation"); Google engineering practices (review-comment
promotion, TODO ownership)._
