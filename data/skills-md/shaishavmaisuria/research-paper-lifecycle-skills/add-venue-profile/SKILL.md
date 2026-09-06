---
name: add-venue-profile
description: Creates a new venue-profile YAML for venues/conferences/ from a conference CFP URL, validates it against venues/schema.yml, and preps the contribution PR. Use when the user wants to add a venue, contribute or refresh a venue profile, encode a conference's submission requirements (deadlines, page limits, blind level, template invocation, rebuttal format, submission system) as machine-readable YAML, copy a profile forward to a new year, or validate a profile before opening a pull request. Covers scaffolding the file, extracting facts from the live CFP, the DBLP/Semantic Scholar/Crossref alias table, the mandatory verified provenance block, schema validation, and PR-readiness checks.
---

# Add Venue Profile

Turn a conference's Call for Papers into a merge-ready venue profile — the
community-contribution loop that grows the `venues/` data moat. Output is one
new file, `venues/conferences/<venue>-<year>.yml`, that passes validation and
arrives with provenance, plus a prepared (never auto-opened) pull request.
Every other venue-aware skill (`preflight-check`, `tailor-to-venue`,
`write-rebuttal`, `prepare-camera-ready`) runs on these profiles, so a wrong
fact here becomes someone else's desk reject. Accuracy beats completeness.

## When to use

- "Add VENUE to the repo" / "contribute a venue profile" / "my conference
  isn't in venues/".
- A new CFP cycle opened and last year's profile must be copied forward.
- A drafted profile needs validation or PR prep before submission upstream.

## Inputs

- The venue's live CFP or author-instructions URL (ask for it if the user
  only names the venue — never build a profile from memory).
- `venues/schema.yml` — read it first; it defines every field and the
  mandatory `verified:` provenance block.
- An existing family file in `venues/families/` (pick via the table in
  [references/profile-walkthrough.md](references/profile-walkthrough.md)).
- `CONTACT_EMAIL` env var for the polite fetch User-Agent (script prompts
  if unset).

## Process

1. **Scope one venue, one year.** Read `venues/schema.yml`. If
   `venues/conferences/` already has this venue:
   - same year → switch to refreshing that file (re-verify every fact live);
   - older year → copy forward into a NEW file. Never edit last year's file
     into this year's; profiles are year-versioned on purpose, and every
     copied fact must be re-verified against the live CFP.

2. **Scaffold the skeleton.** Pick the family from the walkthrough table,
   then run from the repo root:

   ```
   python3 skills/add-venue-profile/scripts/init_profile.py <venue>-<year> \
       --family <family> --cfp-url "<url>"
   ```

   This writes a schema-shaped skeleton with TODO markers and a
   `needs-verification` provenance block. It refuses to overwrite existing
   profiles and rejects unknown families (listing the valid ones).

3. **Fetch the live CFP.** Run:

   ```
   python3 skills/add-venue-profile/scripts/fetch_cfp.py "<cfp-url>"
   ```

   One page per invocation (rate-limited, cached under `.cache/`, gitignored).
   Fetch only the follow-up pages you need — per-track pages, the deadline
   table, camera-ready instructions — one call each, never a site crawl.
   Exit 3 means the CFP is a PDF: read the saved file directly. A
   "very little text extracted" warning means a JavaScript-rendered page: ask
   the user to paste the text and keep `confidence: needs-verification`.
   Confirm the page's year matches the requested year before extracting —
   stale CFPs survive at near-identical URLs.

4. **Fill every field** following
   [references/profile-walkthrough.md](references/profile-walkthrough.md)
   (field-by-field rules, the family table, the trap list). Non-negotiables:
   - Numbers and dates only from fetched text. Missing fact = `null` plus an
     explanatory note — never inferred, never recalled from training data.
   - Page limits must record what is EXCLUDED, with the CFP's sentence
     quoted verbatim in the track `notes`.
   - Deadlines carry the CFP's stated timezone — AoE is common, not
     universal.
   - `llm_policy` and `dual_submission` are verbatim quotes, never
     paraphrased.

5. **Build the alias table** (`dblp_key`, `s2_venue`, `crossref_container`)
   using the single-lookup API patterns in the walkthrough. Aliases make the
   profile searchable by `find-papers`/`select-venue`; a `null` with a
   "searched, not found" comment beats a guess.

6. **Complete the `verified:` block honestly** — today's date, every URL
   facts came from (annotate which facts each page supplied), and a
   `confidence` the evidence actually supports. `verified-live` only if all
   critical facts came off live pages today.

7. **Validate.** Run from the repo root:

   ```
   python3 skills/add-venue-profile/scripts/validate_profile.py \
       venues/conferences/<venue>-<year>.yml --strict
   ```

   Fix every ERROR. Resolve each WARN or carry a one-line justification into
   the PR body. The script is offline and stdlib-only (uses PyYAML when
   present); CI runs the equivalent `tools/validate_venues.py`, so a clean
   strict pass here predicts a green check.

8. **Prep the PR** following
   [references/pr-checklist.md](references/pr-checklist.md): a branch named
   `venue/<venue>-<year>`, a single-file diff, the PR body template with
   provenance and warning justifications. Show the user the final diff and
   the exact `gh pr create` command — and only run it if the user explicitly
   asks. Never open, push, or submit anything unprompted.

9. **Close with the freshness notice:** *"Profile built from <cfp_url> on
   <date>. CFPs change mid-cycle — re-verify deadlines and page limits
   against the live page before relying on this profile, and expect reviewers
   to spot-check it."*

## Output

- `venues/conferences/<venue>-<year>.yml` — schema-conformant, provenance
  included, strict-validation clean (or warnings justified).
- A prepared branch + commit and a ready-to-send PR description.
- An inline summary card: deadlines (with timezone), per-track limits and
  exclusions, blind level, template invocation, submission system, rebuttal
  format — ending with the re-verify notice.

## Guardrails

- Never fabricate a deadline, page limit, policy, or alias. `null` + note
  beats a guess; a fabricated fact in `venues/` poisons every downstream
  skill.
- Quote LLM-use and dual-submission policies verbatim — paraphrase can
  invert compliance meaning.
- GET-only fetching; one page per script invocation; no bulk crawling. Never
  log in to or register with any submission system.
- Fetched CFP text stays in `.cache/` (gitignored) — never commit it. The
  profile holds facts and short verbatim regulatory quotes only.
- Never open the PR, push, or submit anything on the user's behalf without
  an explicit instruction; preparing is the skill's job, sending is the
  user's.
- Re-verify against the live CFP anything the user is about to rely on, and
  say so in the final answer.

## Source verification

This skill creates venue rule data, so source verification is mandatory:

- Build the profile on demand for the venue and year the user chose. Never
  reuse a remembered or prior-year value without re-checking it.
- Search for and open the live CFP or author-instructions page. Search results,
  snippets, and deadline aggregators are leads only; confirm facts on an
  official venue source before recording them.
- Double-check desk-reject-class facts when possible: deadline, page limit and
  exclusions, blind level, template, and submission system. If sources conflict,
  surface the conflict instead of choosing silently.
- Record a clickable source URL and date for every critical fact in the
  `verified:` provenance block. Use `needs-verification` for anything missing a
  source; an unsourced fact cannot be treated as final.

## Bundled files

- [references/profile-walkthrough.md](references/profile-walkthrough.md) —
  family table, field-by-field extraction rules, verified alias-lookup API
  patterns, the trap list.
- [references/pr-checklist.md](references/pr-checklist.md) — validation
  gates, branch/commit conventions, PR body template, what CI checks.
- `scripts/init_profile.py` — offline scaffolder for a schema-shaped skeleton.
- `scripts/fetch_cfp.py` — polite single-page CFP fetcher (run it; never
  reimplement fetching by hand).
- `scripts/validate_profile.py` — offline schema validator; `--strict` is
  the pre-PR gate.
