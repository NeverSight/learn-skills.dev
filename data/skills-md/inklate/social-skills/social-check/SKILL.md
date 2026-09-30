---
name: social-check
description: >
  Validate a social post draft against the target platform's real constraints
  and conventions before it goes out, covering LinkedIn, X, Instagram,
  Facebook, Threads, Bluesky, and Mastodon. Use when the user says "check this
  post", asks "will this work on Instagram", says "validate this draft", or
  asks "is this too long for X". It checks length against hard limits and
  visible-truncation points, link placement norms, hashtag count and position,
  media expectations including aspect ratios and alt text, first-comment
  strategy, engagement-bait patterns, formatting that renders oddly, and
  accessibility. It reads social-context.md so voice-level checks and house
  rules match the user's brand voice and platform setup. Every check returns
  pass, warn, or fix — and every fix comes with the corrected text inline,
  ready to paste.
license: MIT
metadata:
  version: 0.1.0
  category: Check
  topics:
    - checking
    - linkedin
    - x
    - instagram
  examplePrompt: "Check if this draft works on LinkedIn and Instagram"
---

Run a draft through each target platform's real constraints and hand back a pass/warn/fix verdict per check, with the fixed text supplied inline. A bundled linter does the mechanical counting; you supply the judgment.

## Context

Read `social-context.md` at the project root (also check `.agents/social-context.md`) for the `## Voice` rules, `## Platforms`, and the `## Never` list. Hashtag, emoji, and link conventions may not be spelled out there — if they aren't, use the inline fallback below. If it's missing, offer to run the `social-context` skill first, but don't block — ask 2–3 quick inline questions and proceed:

- Which platform(s) is this draft for?
- Does the post have media, and does it have alt text?
- Any house rules on hashtags, emoji, or links?

## Workflow

1. **Establish targets.** Confirm which platform(s) the draft is bound for. Evaluate one draft per platform separately — a draft can pass X and fail LinkedIn, and averaging verdicts helps nobody.

2. **Run the linter for the mechanical checks.** It computes platform-accurate character counts (X bills URLs at 23 and emoji at 2; Mastodon bills URLs at 23), the truncation point, link count and placement, hashtag count/placement/casing, engagement-bait phrasing, and formatting gotchas — deterministically, so you never eyeball a character count:

   ```bash
   bun scripts/lint-post.mjs --platform x --file draft.txt      # one platform
   bun scripts/lint-post.mjs --all --file draft.txt             # every platform
   echo "$DRAFT" | bun scripts/lint-post.mjs --platform linkedin
   ```

   It prints JSON — `{ counts, checks: [{ check, verdict, detail }], summary }` — with each `verdict` as `pass`, `warn`, or `fix`, and exits non-zero when any check is a `fix`. `node` works in place of `bun`. Run it with `--help` for options, or `--list` for supported platforms. If neither runtime is available, count by hand against [references/platform-limits.md](references/platform-limits.md).

3. **Read the reasoning when a flag needs it.** Load [references/platform-limits.md](references/platform-limits.md) for the full constraint table, the per-platform link and hashtag norms, the media/aspect rules, and the verdict-discipline definitions. Don't restate limits from memory — that reference (and the JSON the linter reads) is the source of truth.

4. **Add the judgment the linter can't.** The script flags mechanics; these are yours:
   - **Hook.** Does the first visible line carry a complete, compelling idea before the truncation point the linter reported? "So I've been thinking about someth…" is a `fix` — supply a rewritten opening inline.
   - **Media & alt text.** If media is described, check the aspect ratio against the placement's rule in [references/platform-limits.md](references/platform-limits.md) (Media & accessibility), and confirm the alt text actually describes the image — "image" or keyword stuffing is a `fix`.
   - **First-comment strategy.** If a link belongs in the first comment (or the draft says "link in comments"), draft that comment — one line of context plus the link.
   - **Engagement bait.** When the linter flags bait, replace it with an ask that requests genuine input, not a reflex.
   - **Voice.** Check the draft against every rule in the Voice section of `social-context.md`.

5. **Assemble the verdict.** Merge the linter's mechanical verdicts with your judgment calls into one table per platform: `pass` / `warn` / `fix`, a one-clause reason, and for every `fix` the corrected text inline. If a check doesn't apply (no media, no links), say `n/a` rather than dropping the row. If anything was `fix`, finish with a fully corrected version of the whole post for that platform.

## Quality bar

Check against the real numbers in [references/platform-limits.md](references/platform-limits.md), not a vague memory of "roughly 280". Verdict discipline:

- `pass` — meets the constraint; nothing more to say.
- `warn` — will publish but underperform or annoy; give a one-clause reason and a suggested improvement.
- `fix` — don't post as-is; supply the corrected text inline. A `fix` without corrected text is an unfinished check.

Run every check for every target platform. A silently skipped check reads as a pass.

## Deliverable

Per target platform: a verdict table (check | verdict | note), each `fix` row followed by the corrected text inline, and — if anything was `fix` — a complete corrected draft for that platform, plus the drafted first comment if the strategy calls for one. The user copies the corrected draft and posts it wherever and whenever they choose — hand it back and stop.
