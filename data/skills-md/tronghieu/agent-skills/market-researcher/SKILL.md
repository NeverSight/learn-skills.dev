---
name: market-researcher
description: >
  Conduct rigorous, citation-backed desk market research: quick go/no-go market
  scans, market sizing (TAM/SAM/SOM), competitor analysis, customer demand
  signals, and trend/macro (PESTEL) analysis. Use this skill whenever the user
  wants to research, size, validate, or enter a market — "is there a market
  for…", "how big is the market for…", "who are the competitors of…", "should I
  build/launch/sell…", "validate this business idea", "market research for…",
  "market entry" — in any language and for any country's market (e.g.
  "nghiên cứu thị trường", "étude de marché", "市場調査", "análisis de
  mercado"), even when the user never says the words "market research". Also
  use it when
  another skill or workflow (strategy-board, design-thinking, a product brief)
  needs external market facts delivered into its fact base or research folder.
---

# Market Researcher

A desk-research engine for market questions. It takes a raw question like
"should we build X?" or "how big is the market for Y in Brazil?" and returns a
research report in which **every factual claim traces to a registered source**
— the discipline the typical AI market analysis lacks, and the reason this
skill exists. A confident fabricated market size looks exactly like a real one;
the citation machinery below is what makes the difference detectable.

The skill runs desk research only: web sources, public data, documents the
user provides. It designs around that limit honestly — what it learns about
customers are *demand signals and hypotheses*, never validated insights (see
non-negotiable 5).

## Non-negotiables

These five rules outrank everything else in this skill:

1. **Every claim is traceable.** Every number and every factual assertion in a
   deliverable either carries a source tag `[S#]` that resolves to a row in
   `sources.md`, or is an explicit derived estimate showing its formula and
   cited inputs, or is labelled `(assumption A#)`. Nothing rides on authority
   of tone. If you catch yourself writing "the market is growing rapidly"
   without a tag, stop and either find the source or cut the sentence.
2. **Current facts come from the web, not from memory.** Market sizes, prices,
   competitor products, funding, regulations — research them fresh. Training
   data is stale and, worse, statistically plausible. If web access is
   unavailable, say so and stop; do not degrade into an uncited essay.
3. **Triangulate; never silently average.** Size markets with more than one
   method when the decision warrants it. When two credible sources or methods
   disagree by more than ~2x, report the conflict and diagnose it (different
   market definitions, years, currencies, revenue-vs-GMV) rather than blending
   it away.
4. **A verification pass runs before delivery.** A skeptic re-checks key
   claims against their sources, re-does estimate arithmetic, and flags stale
   data. Findings it cannot resolve ship *in the report* as caveats, not
   silently dropped.
5. **Desk research yields signals, not validated customer insight.** Personas
   and needs produced here are hypotheses to be tested by real primary
   research (interviews, tests) that the user or a calling skill owns. Label
   them as such and always end customer sections with "open questions for
   primary research".

## Prerequisite

Web search and web fetch. Check availability before promising anything; if
missing, tell the user what you need and stop rather than answering from
training data (non-negotiable 2).

### Tool economy

Desk research is reading, not browsing. Use the cheapest tool that gets the
text, in this order:

1. **Built-in web search** (WebSearch or equivalent) to find sources.
2. **Built-in fetch** (WebFetch or equivalent) to read them — it returns the
   page text, which is all a citation needs.
3. **Browser automation** (agent-browser, Chrome/Playwright tools) only as a
   last resort for a specific page that fetch genuinely cannot read
   (JS-only rendering, interaction-gated content) *and* that no alternative
   source covers. Never screenshot pages to "read" them.

This ordering is a cost rule, not a style preference: a browser session burns
tokens on screenshots and DOM snapshots at a rate that can exceed the entire
rest of the lane, and it produces nothing a citation needs that fetched text
doesn't. If another skill's guidance says to prefer browser tools, it does
not apply inside this skill's research lanes. Pass this rule to every lane
subagent you spawn.

One harness quirk: some environments guard the Write tool against
report-shaped filenames (`report.md`, `summary.md`, `findings-*.md`). If a
required output file is blocked, write it via a shell heredoc instead — the
filenames are part of this skill's contract and must not be renamed to
appease the guard.

## Two modes

| | **Quick Scan** (default) | **Deep Dive** (opt-in) |
|---|---|---|
| Question | "Is this worth a closer look?" | "What exactly are we walking into?" |
| Duration | One session | Multi-session, resumable |
| Sizing | One method + sanity check, wide honest ranges | ≥2 methods, triangulated |
| Competitors | 5–10 identified, one-line profiles | Top 3–5 profiled in depth |
| Customers | Headline demand signals | Full signal mining + hypothesis personas |
| Macro | 2–3 kill-factors / tailwinds only | Structured PESTEL + trends |
| Output | Go/no-go brief (~4–8 pages) | Modular report |

Default to Quick Scan and say so — "I'll run a quick scan first; we can deep-
dive into any lane that looks decisive." Go straight to Deep Dive only when
the user asks for depth or a calling skill specifies it. Deep Dive is modular:
the user picks lanes (sizing / competitors / demand / macro); don't run all
four ritualistically if only one matters to the decision.

Keep Quick Scan actually quick: a hard working budget of **~15 registered
sources per lane** — enough to bound the answer, not to settle it. Write the
budget into every lane subagent's prompt and stop a lane when its marginal
source stops changing the lane's answer; "one more source" past that point
is Deep Dive work the user didn't order. Depth beyond the budget belongs in
Deep Dive, where the user has opted into the cost. Tell the user at intake
what they're buying ("a quick scan takes a while and reads a few dozen
sources; a deep dive is a multi-session effort") so "quick" doesn't
over-promise.

## Workflow

### 0. Intake

Establish, in one short exchange (not an interview):

- **The decision behind the question.** "Research the pet food market" hides
  "should I quit my job to start a pet food brand?" — the decision determines
  depth, lanes, and what "so what" means. Ask if not obvious.
- **Market definition draft**: product/service category, customer type
  (B2B/B2C), geography, any segment constraints. A market size without a
  market definition is noise.
- **Mode** (default Quick Scan) and, for Deep Dive, which lanes.
- **Output location**: standalone → `./research/market/<topic-slug>/`;
  called from another skill's workspace → the path it provides (see
  "Composition contract").

Confirm the frame back in 3–5 lines, then start. Don't re-elicit what the
conversation already contains.

### 1. Initialize the research workspace

```bash
bash /mnt/skills/user/market-researcher/scripts/init-research.sh <output-dir> "<topic>" <mode>
```

This scaffolds the directory, `sources.md` (the source registry), `state.md`
(progress tracking for resume), and `report.md` skeleton. When running inside
this repo use `skills/market-researcher/scripts/init-research.sh`.

### 2. Run research lanes

Four lanes, each with its own reference file — read the reference before
running the lane:

| Lane | Reference | Quick Scan version |
|---|---|---|
| Market & sizing | `references/market-sizing.md` | One method, ranges |
| Competitors | `references/competitor-analysis.md` | Scan of 5–10 |
| Demand signals | `references/demand-signals.md` | Headline signals |
| Trends & macro | `references/trends-macro.md` | Kill-factors only |

**Parallelize when you can.** If subagents are available, run lanes as
parallel agents; give each agent its lane's reference file, the market
definition, the mode, and the citation rules (point it at
`references/citation-schema.md`). Each lane writes `findings-<lane>.md` in the
workspace and registers every source it uses in `sources.md` with the next
free `[S#]` id. If subagents are not available, run lanes sequentially
yourself — the discipline is identical, only the wall-clock differs.

Lane outputs are evidence files, not prose essays: claims tagged, quotes
linked, estimates showing their arithmetic.

### 3. Synthesize

Read all lane findings and write the report body (structures in
`references/report-templates.md`). Synthesis rules:

- **"So what?" for every section.** Findings that don't bear on the decision
  get cut, no matter how interesting.
- **Rigor lives in the evidence files; the report reads like a good
  consultant wrote it.** Citation tags stay, but the machinery talk (lane
  names, ID-block bookkeeping, process narration) does not belong in the
  report body — move it to state.md. Prefer the crisp formulation: "priced
  against a $150k assistant, $30/mo is cheap [S12]" beats a paragraph of
  hedged setup. A report that is rigorous but tiring to read loses to a
  well-written uncited one in practice, and that is a failure of this skill's
  purpose, not a style preference.
- The verdict is a **recommendation with confidence and reasoning**, not a
  hedge. "Go, with medium confidence, because A and B; the thing that would
  change this is C."
- **The verdict's confidence must own its structural evidence limits.** Two
  recurring ones: (a) if the data spine — market size, outlet counts, the
  facts the verdict stands on — traces to a single vendor's report series,
  that is a ceiling on confidence, stated in the verdict itself, not a line
  in a caveat list; (b) if the strongest evidence describes an *adjacent*
  segment rather than the user's actual target (e.g. plenty of data on
  merchants who already pay for software, almost none on the no-software
  merchants the user wants to win), say so where the verdict is stated — the
  reader must know which population the conclusion actually rests on.
- Contradictions between lanes are findings, not embarrassments — surface
  them. (Large market but no willingness-to-pay signals is a classic and
  important combination.)
- End with **open questions for primary research** — what desk research
  could not establish and how to test it.

### 4. Verification pass

Before delivery, run a skeptic pass — a separate subagent if available,
otherwise yourself in an explicitly adversarial sitting:

- Take the report's ~10 most decision-relevant claims. For each, open the
  cited source and check it actually says what the report says (numbers,
  units, year, market definition).
- Recompute every derived estimate from its stated inputs — including the
  time axis: a CAGR for 2026–2031 applied to a 2024 base is a silent error;
  reconcile the years or state the mismatch.
- Flag sources older than 2 years presented as current, and single-source
  claims that carry heavy decision weight.
- Check source *portfolio* health, not just individual sources: (a) does one
  publisher — especially a profiled competitor — supply the data spine? (b) is
  one Low-confidence source reused across several different strategic claims?
  (c) do any pain/WTP quotes come from competitor-affiliated sites? Each hit
  becomes a named caveat.
- Anything unresolved becomes a visible caveat in the report; nothing is
  quietly deleted or quietly kept.

Record the pass (what was checked, what was fixed, what remains open) at the
bottom of `state.md`.

### 5. Deliver

Present to the user, in the conversation language: the verdict and confidence,
the three-to-five facts that drive it, the biggest caveat from verification,
and the open questions. Keep it under a screen; the report file holds the
rest. Offer the natural next steps: deep-dive a lane, hand the open questions
to primary research, or re-run the scan later (markets move).

## Source and citation discipline

The full schema lives in `references/citation-schema.md` — read it before
writing any findings file. The one-paragraph version: `sources.md` is a
registry where each source gets an id `[S#]`, URL, publisher, publication
date, date accessed, and a confidence grade (high/medium/low by source type
and corroboration). Claims cite `[S#]`; derived estimates show formula and
cited inputs inline; assumptions get `A#` ids and live in an assumptions table
in the report. An untagged factual sentence is a bug.

## Composition contract (for calling skills)

Other skills (strategy-board, design-thinking, product briefs) can use this
skill as their research engine. The contract:

**Input** — the caller provides: research question + decision context, market
definition (or asks this skill to draft one), mode and lanes, and a target
directory inside the caller's workspace (e.g. strategy-board's fact-base
sources dir, design-thinking's `research/`).

**Output** — this skill writes into that directory: `sources.md` (or appends
to an existing one, continuing its `[S#]` numbering — never renumber existing
sources), `findings-*.md`, and `report.md`. All claims follow the citation
schema, so the caller's artifacts can cite `[S#]` directly without knowing how
the research was done.

**Boundary** — this skill answers market questions. For deep research on
non-market topics, or when the caller needs primary research with real
customers, say so explicitly instead of stretching.

## Resuming across sessions (Deep Dive)

`state.md` tracks: mode, lanes chosen, lanes completed, verification status,
and a short log line per session. When invoked and the output directory
already exists, read `state.md` first and tell the user where things stand
("sizing and competitors done; demand signals lane pending") before doing
anything. Never redo a completed lane silently — ask if the user wants it
refreshed (sources may be stale if much time has passed; say when the lane
was last run).

## References

| File | Read when |
|---|---|
| `references/citation-schema.md` | Always, before writing any findings |
| `references/market-sizing.md` | Running the sizing lane |
| `references/competitor-analysis.md` | Running the competitor lane |
| `references/demand-signals.md` | Running the demand lane |
| `references/trends-macro.md` | Running the macro lane |
| `references/report-templates.md` | Synthesizing the report |

## Presenting results

Lead with the verdict and its confidence. Then the driving facts, each with
its `[S#]`. Then the biggest caveat. Then open questions. Write for an
executive who will read the full report only if this summary earns it. Match
the user's language, whatever it is (a question asked in Spanish gets a
Spanish summary and report; source quotes may stay in their original
language).
