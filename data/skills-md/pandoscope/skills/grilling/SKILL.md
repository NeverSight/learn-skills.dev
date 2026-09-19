---
name: grilling
description: >
  Grill the user about a plan, decision, or idea via scored
  multiple-choice questions. Use when the user wants to stress-test
  their thinking or uses any 'grill' trigger phrase.
metadata.derived-from: https://github.com/mattpocock/skills/blob/e9fcdf95b402d360f90f1db8d776d5dd450f9234/skills/productivity/grilling/SKILL.md
metadata.derivation-note: Adds scored multiple-choice format rendered from session JSON to an interactive page or text fallback, ruling + rejection-reason recording to a decision store, artifact embedding of alternatives. Detached from upstream — no sync.
---

# Grilling

Interview user until shared understanding. Walk every branch of decision tree, dependencies one by one. ONE question at a time — wait for answer before next. *Facts* findable in environment: look up, never ask. *Decisions* are user's — put each to user, wait. Do not act until user confirms.

Naming: question `S«s»Q«q»`, answer `S«s»Q«q»A«n»`.

## Steps

1. `resolve-store.sh path` — locates store harness already cloned. Resolve, never clone. Exits non-zero naming its own fix when store is unnamed, unresolved or absent; unnamed → say so out loud and record nothing (silent skip is indistinguishable from successful record). Store URL lives in environment only — never hardcoded, never echoed into artifacts.
2. `resolve-store.sh unmerged` — any records → refuse to open session until principal merges previous one, per [recording.md](recording.md).
3. `resolve-store.sh preferences` — emits active set as JSON array for session's `preferences`: copied, never retyped. Inject that set ONLY, never decision history.
4. Author every decision point as session JSON — whole session so far, answers included. Contract: `render/decision-context.ts` beside this file; semantics: [format.md](format.md). NEVER hand-format a question; renderer appends free-text slot itself.
5. Render both user-facing forms — validation failure names offending field; fix JSON, re-run:

   ```bash
   node --experimental-strip-types <skill-dir>/render/render.ts <session.json> --out <dir>
   ```

6. Publish `session.html` as artifact, redeploying same URL as session grows; unavailable → print `session.md` into chat verbatim — never as file attachment, never as timed dialog (dialogs close while user still typing).
7. Answers arrive as page's copied JSON pasted into chat, or as chat replies: answer id ("S1Q2A1" or "1"), correction via "N, but actually because …" — shorthand "N, BAB …". No live page-to-agent channel yet (pandoscope/skills#139). What answers mean: [reading.md](reading.md). Follow-ups: append new questions plus answers received, re-render; user may revisit earlier answers.
8. Session end: record every ruling to store, embed rejection reasons in session's target artifact, per [recording.md](recording.md).
9. `check.sh <session.json>` — re-validates session, verifies citations are verbatim store lines, fails while records stay unmerged, prints residue to verify by hand.

## Question rules

- Slot 1 carries prediction: preference-driven when active rules match (named in `matches`), else cold pick. Diverging recommendation sits at slot 2, if-clause arguing when it beats slot 1.
- Wildcard ONLY when genuinely plausible unexplored branch exists.
- If-clause = when option beats recommendation. Add "why not recommended" only when it differs from negated if-clause.
- Near-ties MUST be marked; never fabricate weaknesses for close calls, and never score them as misses.
- Correction ("N, but actually because …", shorthand "N, BAB …") accepts option, overrides its stated reason — highest-signal event; flag in record.
- Drill down with ONE follow-up (2-3 ranked guesses + free text) only when free-text answer leaves rejection reasons unstated. Guesses count as predictions.

## Non-goals

No automatic preference-rule acceptance — human in loop always. No embedding/RAG tooling. No upstream sync.
