---
name: research
description: >-
  Deep multi-source research with confidence scoring. Auto-classifies
  complexity. Use for technical investigation, fact-checking. NOT for code
  review or simple Q&A.
argument-hint: "<question or topic> [--depth quick|standard|deep|exhaustive] [--format brief|deep|bib|matrix]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
hooks:
  PreToolUse:
    - matcher: Edit
      hooks:
        - command: 'bash -c "echo BLOCKED: research skill is read-only — no file edits permitted >&2; exit 1"'
---

# Deep Research

General-purpose deep research with multi-source synthesis, confidence scoring, and anti-hallucination verification. Adopts SOTA patterns from OpenAI Deep Research (multi-agent triage pipeline), Google Gemini Deep Research (user-reviewable plans), STORM (perspective-guided conversations), Perplexity (source confidence ratings), and LangChain ODR (supervisor-researcher with reflection).

## Vocabulary

| Term | Definition |
|------|-----------|
| **query** | The user's research question or topic; the unit of investigation |
| **claim** | A discrete assertion to be verified; extracted from sources or user input |
| **source** | A specific origin of information: URL, document, database record, or API response |
| **evidence** | A source-backed datum supporting or contradicting a claim; always has provenance |
| **provenance** | The chain from evidence to source: tool used, URL, access timestamp, excerpt |
| **confidence** | Score 0.0-1.0 per claim; based on evidence strength and cross-validation |
| **cross-validation** | Verifying a claim across 2+ independent sources; the core anti-hallucination mechanism |
| **triangulation** | Confirming a finding using 3+ methodologically diverse sources |
| **contradiction** | When two credible sources assert incompatible claims; must be surfaced explicitly |
| **synthesis** | The final research product: not a summary but a novel integration of evidence with analysis |
| **journal** | The saved markdown record of a research session, stored in `~/.claude/research/` |
| **sweep** | Wave 1: broad parallel search across multiple tools and sources |
| **deep dive** | Wave 2: targeted follow-up on specific leads from the sweep |
| **lead** | A promising source or thread identified during the sweep, warranting deeper investigation |
| **tier** | Complexity classification: Quick (0-2), Standard (3-5), Deep (6-8), Exhaustive (9-10) |
| **finding** | A verified claim with evidence chain, confidence score, and provenance; the atomic unit of output |
| **gap** | An identified area where evidence is insufficient, contradictory, or absent |
| **bias marker** | An explicit flag on a finding indicating potential bias (recency, authority, LLM prior, etc.) |
| **degraded mode** | Operation when research tools are unavailable; confidence ceilings applied |

## Dispatch

| `$ARGUMENTS` | Action |
|---|---|
| Question or topic text (has verb or `?`) | **Investigate** — classify complexity, execute wave pipeline |
| Vague input (<5 words, no verb, no `?`) | **Intake** — ask 2-3 clarifying questions, then classify |
| `check <claim>` or `verify <claim>` | **Fact-check** — verify claim against 3+ search engines |
| `compare <A> vs <B> [vs <C>...]` | **Compare** — structured comparison with decision matrix output |
| `survey <field or topic>` | **Survey** — landscape mapping, annotated bibliography |
| `track <topic>` | **Track** — load prior journal, search for updates since last session |
| `resume [number or keyword]` | **Resume** — resume a saved research session |
| `list [active\|domain\|tier]` | **List** — show journal metadata table |
| `archive` | **Archive** — move journals older than 90 days |
| `delete <N>` | **Delete** — delete journal N with confirmation |
| `export [N]` | **Export** — render HTML dashboard for journal N (default: current) |
| Empty | **Gallery** — show topic examples + "ask me anything" prompt |

### Auto-Detection Heuristic

If no mode keyword matches:

1. Ends with `?` or starts with question word (who/what/when/where/why/how/is/are/can/does/should/will) → **Investigate**
2. Contains `vs`, `versus`, `compared to`, `or` between noun phrases → **Compare**
3. Declarative statement with factual claim, no question syntax → **Fact-check**
4. Broad field name with no specific question → ask: "Investigate a specific question, or survey the entire field?"
5. Ambiguous → ask: "Would you like me to investigate this question, verify this claim, or survey this field?"

### Gallery (Empty Arguments)

Present research examples spanning domains:

| # | Domain | Example | Likely Tier |
|---|--------|---------|-------------|
| 1 | Technology | "What are the current best practices for LLM agent architectures?" | Deep |
| 2 | Academic | "What is the state of evidence on intermittent fasting for longevity?" | Standard |
| 3 | Market | "How does the competitive landscape for vector databases compare?" | Deep |
| 4 | Fact-check | "Is it true that 90% of startups fail within the first year?" | Standard |
| 5 | Architecture | "When should you choose event sourcing over CRUD?" | Standard |
| 6 | Trends | "What emerging programming languages gained traction in 2025-2026?" | Standard |

> Pick a number, paste your own question, or type `guide me`.

### Skill Awareness

Before starting research, check if another skill is a better fit:

| Signal | Redirect |
|--------|----------|
| Code review, PR review, diff analysis | Suggest `/honest-review` |
| Strategic decision with adversaries, game theory | Suggest `/wargame` |
| Multi-perspective expert debate | Suggest `/host-panel` |
| Prompt optimization, model-specific prompting | Suggest `/prompt-engineer` |

If the user confirms they want general research, proceed.

## Complexity Classification

Score the query on 5 dimensions (0-2 each, total 0-10):

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Scope breadth** | Single fact/definition | Multi-faceted, 2-3 domains | Cross-disciplinary, 4+ domains |
| **Source difficulty** | Top search results suffice | Specialized databases or multiple source types | Paywalled, fragmented, or conflicting sources |
| **Temporal sensitivity** | Stable/historical | Evolving field (months matter) | Fast-moving (days/weeks matter), active controversy |
| **Verification complexity** | Easily verifiable (official docs) | 2-3 independent sources needed | Contested claims, expert disagreement, no consensus |
| **Synthesis demand** | Answer is a fact or list | Compare/contrast viewpoints | Novel integration of conflicting threads |

| Total | Tier | Strategy |
|-------|------|----------|
| 0-2 | **Quick** | Inline, 1-2 searches, fire-and-forget |
| 3-5 | **Standard** | Subagent wave, 3-5 parallel searchers, report delivered |
| 6-8 | **Deep** | Agent team (TeamCreate), 3-5 teammates, interactive session |
| 9-10 | **Exhaustive** | Agent team, 4-6 teammates + nested subagent waves, interactive |

Present the scoring to the user. User can override tier with `--depth <tier>`.

## Wave Pipeline

All non-Quick research follows this 5-wave pipeline. Quick merges Waves 0+1+4 inline.

### Wave 0: Triage (always inline, never parallelized)

1. Run `!uv run python skills/research/scripts/research-scanner.py "$ARGUMENTS"` for deterministic pre-scan
2. Decompose query into 2-5 sub-questions
3. Score complexity on the 5-dimension rubric
4. Check tool availability — probe key MCP tools; set degraded mode flags and confidence ceilings per `references/source-selection.md`
5. Select tools per domain signals — read `references/source-selection.md`
6. Check for existing journals — if `track` or `resume`, load prior state
7. **Present triage to user** — show: complexity score, sub-questions, planned strategy, estimated tier. User may override.

### Wave 1: Broad Sweep (parallel)

Scale by tier:

**Quick (inline):** 1-2 tool calls sequentially. No subagents.

**Standard (subagent wave):** Dispatch 3-5 parallel subagents via Task tool:
```
Subagent A → brave-search + duckduckgo-search for sub-question 1
Subagent B → exa + g-search for sub-question 2
Subagent C → context7 / deepwiki / arxiv / semantic-scholar for technical specifics
Subagent D → wikipedia / wikidata for factual grounding
[Subagent E → PubMed / openalex if academic domain detected]
```

**Deep (agent team):** TeamCreate `"research-{slug}"`:
```
Lead: triage (Wave 0), orchestrate, judge reconcile (Wave 3), synthesize (Wave 4)
  |-- web-researcher:       brave-search, duckduckgo-search, exa, g-search
  |-- tech-researcher:      context7, deepwiki, arxiv, semantic-scholar, package-version
  |-- content-extractor:    fetcher, trafilatura, docling, wikipedia, wayback
  |-- [academic-researcher: arxiv, semantic-scholar, openalex, crossref, PubMed]
  |-- [adversarial-reviewer: devil's advocate — counter-search all emerging findings]
```
Spawn academic-researcher if domain signals include academic/scientific. Spawn adversarial-reviewer for Exhaustive tier or if verification complexity >= 2.

**Exhaustive:** Deep team + each teammate runs nested subagent waves internally.

Each subagent/teammate returns structured findings:
```json
{
  "sub_question": "...",
  "findings": [{"claim": "...", "source_url": "...", "source_tool": "...", "excerpt": "...", "confidence_raw": 0.6}],
  "leads": ["url1", "url2"],
  "gaps": ["could not find data on X"]
}
```

### Wave 1.5: Perspective Expansion (Deep/Exhaustive only)

STORM-style perspective-guided conversation. Spawn 2-4 perspective subagents:

| Perspective | Focus | Question Style |
|-------------|-------|---------------|
| **Skeptic** | What could be wrong? What's missing? | "What evidence would disprove this?" |
| **Domain Expert** | Technical depth, nuance, edge cases | "What do practitioners actually encounter?" |
| **Practitioner** | Real-world applicability, trade-offs | "What matters when you actually build this?" |
| **Theorist** | First principles, abstractions, frameworks | "What underlying model explains this?" |

Each perspective agent reviews Wave 1 findings and generates 2-3 additional sub-questions from their viewpoint. These sub-questions feed into Wave 2.

### Wave 2: Deep Dive (parallel, targeted)

1. Rank leads from Wave 1 by potential value (citation frequency, source authority, relevance)
2. Dispatch deep-read subagents — use fetcher/trafilatura/docling to extract full content from top leads
3. Follow citation chains — if a source cites another, fetch the original
4. Fill gaps — for each gap identified in Wave 1, dispatch targeted searches
5. Use thinking MCPs:
   - `cascade-thinking` for multi-perspective analysis of complex findings
   - `structured-thinking` for tracking evidence chains and contradictions
   - `think-strategies` for complex question decomposition (Standard+ only)

### Wave 3: Cross-Validation (parallel)

The anti-hallucination wave. Read `references/confidence-rubric.md` and `references/self-verification.md`.

For every claim surviving Waves 1-2:

1. **Independence check** — are supporting sources truly independent? Sources citing each other are NOT independent.
2. **Counter-search** — explicitly search for evidence AGAINST each major claim using a different search engine
3. **Freshness check** — verify sources are current (flag if >1 year old for time-sensitive topics)
4. **Contradiction scan** — read `references/contradiction-protocol.md`, identify and classify disagreements
5. **Confidence scoring** — assign 0.0-1.0 per `references/confidence-rubric.md`
6. **Bias sweep** — check each finding against 10 bias categories (7 core + 3 LLM-specific) per `references/bias-detection.md`

**Self-Verification (3+ findings survive):** Spawn devil's advocate subagent per `references/self-verification.md`:
> For each finding, attempt to disprove it. Search for counterarguments. Check if evidence is outdated. Verify claims actually follow from cited evidence. Flag LLM confabulations.

Adjust confidence: Survives +0.05, Weakened -0.10, Disproven set to 0.0.
Adjustments are subject to hard caps — single-source claims remain capped at 0.60 even after survival adjustment.

### Wave 4: Synthesis (always inline, lead only)

Produce the final research product. Read `references/output-formats.md` for templates.

The synthesis is NOT a summary. It must:

1. **Answer directly** — answer the user's question clearly
2. **Map evidence** — all verified findings with confidence and citations
3. **Surface contradictions** — where sources disagree, with analysis of why
4. **Show confidence landscape** — what is known confidently, what is uncertain, what is unknown
5. **Audit biases** — biases detected during research
6. **Identify gaps** — what evidence is missing, what further research would help
7. **Distill takeaways** — 3-7 numbered key findings
8. **Cite sources** — full bibliography with provenance

**Output format** adapts to mode:
- Investigate → Research Brief (Standard) or Deep Report (Deep/Exhaustive)
- Fact-check → Quick Answer with verdict + evidence
- Compare → Decision Matrix
- Survey → Annotated Bibliography
- User can override with `--format brief|deep|bib|matrix`

## Confidence Scoring

| Score | Basis |
|-------|-------|
| 0.9-1.0 | Official docs + 2 independent sources agree, no contradictions |
| 0.7-0.8 | 2+ independent sources agree, minor qualifications |
| 0.5-0.6 | Single authoritative source, or 2 sources with partial agreement |
| 0.3-0.4 | Single non-authoritative source, or conflicting evidence |
| 0.2-0.3 | Multiple non-authoritative sources with partial agreement, or single source with significant caveats |
| 0.1-0.2 | LLM reasoning only, no external evidence found |
| 0.0 | Actively contradicted by evidence |

**Hard rules:**
- No claim reported at >= 0.7 unless supported by 2+ independent sources
- Single-source claims cap at 0.6 regardless of source authority
- Degraded mode (all research tools unavailable): max confidence 0.4, all findings labeled "unverified"

**Merged confidence** (for claims supported by multiple sources):
`c_merged = 1 - (1-c1)(1-c2)...(1-cN)` capped at 0.99

## Evidence Chain Structure

Every finding carries this structure:

```
FINDING RR-{seq:03d}: [claim statement]
  CONFIDENCE: [0.0-1.0]
  EVIDENCE:
    1. [source_tool] [url] [access_timestamp] — [relevant excerpt, max 100 words]
    2. [source_tool] [url] [access_timestamp] — [relevant excerpt, max 100 words]
  CROSS-VALIDATION: [agrees|contradicts|partial] across [N] independent sources
  BIAS MARKERS: [none | list of detected biases with category]
  GAPS: [none | what additional evidence would strengthen this finding]
```

Use `!uv run python skills/research/scripts/finding-formatter.py --format markdown` to normalize.

## Source Selection

Read `references/source-selection.md` during Wave 0 for the full tool-to-domain mapping. Summary:

| Domain Signal | Primary Tools | Secondary Tools |
|--------------|---------------|-----------------|
| Library/API docs | context7, deepwiki, package-version | brave-search |
| Academic/scientific | arxiv, semantic-scholar, PubMed, openalex | crossref, brave-search |
| Current events/trends | brave-search, exa, duckduckgo-search, g-search | fetcher, trafilatura |
| GitHub repos/OSS | deepwiki, repomix | brave-search |
| General knowledge | wikipedia, wikidata, brave-search | fetcher |
| Historical content | wayback, brave-search | fetcher |
| Fact-checking | 3+ search engines mandatory | wikidata for structured claims |
| PDF/document analysis | docling | trafilatura |

**Multi-engine protocol:** For any claim requiring verification, use minimum 2 different search engines. Different engines have different indices and biases. Agreement across engines increases confidence.

## Bias Detection

Check every finding against 10 bias categories. Read `references/bias-detection.md` for full detection signals and mitigation strategies.

| Bias | Detection Signal | Mitigation |
|------|-----------------|------------|
| **LLM prior** | Matches common training patterns, lacks fresh evidence | Flag; require fresh source confirmation |
| **Recency** | Overweighting recent results, ignoring historical context | Search for historical perspective |
| **Authority** | Uncritically accepting prestigious sources | Cross-validate even authoritative claims |
| **Confirmation** | Queries constructed to confirm initial hypothesis | Use neutral queries; search for counterarguments |
| **Survivorship** | Only finding successful examples | Search for failures/counterexamples |
| **Selection** | Search engine bubble, English-only | Use multiple engines; note coverage limitations |
| **Anchoring** | First source disproportionately shapes interpretation | Document first source separately; seek contrast |

## State Management

- **Journal path:** `~/.claude/research/`
- **Archive path:** `~/.claude/research/archive/`
- **Filename convention:** `{YYYY-MM-DD}-{domain}-{slug}.md`
  - `{domain}`: `tech`, `academic`, `market`, `policy`, `factcheck`, `compare`, `survey`, `track`, `general`
  - `{slug}`: 3-5 word semantic summary, kebab-case
  - Collision: append `-v2`, `-v3`
- **Format:** YAML frontmatter + markdown body + `<!-- STATE -->` blocks

**Save protocol:**
- Quick: save once at end with `status: Complete`
- Standard/Deep/Exhaustive: save after Wave 1 with `status: In Progress`, update after each wave, finalize after synthesis

**Resume protocol:**
1. `resume` (no args): find `status: In Progress` journals. One → auto-resume. Multiple → show list.
2. `resume N`: Nth journal from `list` output (reverse chronological).
3. `resume keyword`: search frontmatter `query` and `domain_tags` for match.

Use `!uv run python skills/research/scripts/journal-store.py` for all journal operations.

**State snapshot** (appended after each wave save):
```html
<!-- STATE
wave_completed: 2
findings_count: 12
leads_pending: ["url1", "url2"]
gaps: ["topic X needs more sources"]
contradictions: 1
next_action: "Wave 3: cross-validate top 8 findings"
-->
```

## In-Session Commands (Deep/Exhaustive)

Available during active research sessions:

| Command | Effect |
|---------|--------|
| `drill <finding #>` | Deep dive into a specific finding with more sources |
| `pivot <new angle>` | Redirect research to a new sub-question |
| `counter <finding #>` | Explicitly search for evidence against a finding |
| `export` | Render HTML dashboard |
| `status` | Show current research state without advancing |
| `sources` | List all sources consulted so far |
| `confidence` | Show confidence distribution across findings |
| `gaps` | List identified knowledge gaps |
| `?` | Show command menu |

Read `references/session-commands.md` for full protocols.

## Reference File Index

| File | Content | Read When |
|------|---------|-----------|
| `references/source-selection.md` | Tool-to-domain mapping, multi-engine protocol, degraded mode | Wave 0 (selecting tools) |
| `references/confidence-rubric.md` | Scoring rubric, cross-validation rules, independence checks | Wave 3 (assigning confidence) |
| `references/evidence-chain.md` | Finding template, provenance format, citation standards | Any wave (structuring evidence) |
| `references/bias-detection.md` | 10 bias categories (7 core + 3 LLM-specific), detection signals, mitigation strategies | Wave 3 (bias audit) |
| `references/contradiction-protocol.md` | 4 contradiction types, resolution framework | Wave 3 (contradiction detection) |
| `references/self-verification.md` | Devil's advocate protocol, hallucination detection | Wave 3 (self-verification) |
| `references/output-formats.md` | Templates for all 5 output formats | Wave 4 (formatting output) |
| `references/team-templates.md` | Team archetypes, subagent prompts, perspective agents | Wave 0 (designing team) |
| `references/session-commands.md` | In-session command protocols | When user issues in-session command |
| `references/dashboard-schema.md` | JSON data contract for HTML dashboard | `export` command |

**Loading rule:** Load ONE reference at a time per the "Read When" column. Do not preload.

## Critical Rules

1. **No claim >= 0.7 unless supported by 2+ independent sources** — single-source claims cap at 0.6
2. **Never fabricate citations** — if URL, author, title, or date cannot be verified, use vague attribution ("a study in this tradition") rather than inventing specifics
3. **Always surface contradictions explicitly** — never silently resolve disagreements; present both sides with evidence
4. **Always present triage scoring before executing research** — user must see and can override complexity tier
5. **Save journal after every wave in Deep/Exhaustive mode** — enables resume after interruption
6. **Never skip Wave 3 (cross-validation) for Standard/Deep/Exhaustive tiers** — this is the anti-hallucination mechanism
7. **Multi-engine search is mandatory for fact-checking** — use minimum 2 different search tools (e.g., brave-search + duckduckgo-search)
8. **Apply the Accounting Rule after every parallel dispatch** — N dispatched = N accounted for before proceeding to next wave
9. **Distinguish facts from interpretations in all output** — factual claims carry evidence; interpretive claims are explicitly labeled as analysis
10. **Flag all LLM-prior findings** — claims matching common training data but lacking fresh evidence must be flagged with bias marker
11. **Max confidence 0.4 in degraded mode** — when all research tools are unavailable, report all findings as "unverified — based on training knowledge"
12. **Load ONE reference file at a time** — do not preload all references into context
13. **Track mode must load prior journal before searching** — avoid re-researching what is already known
14. **The synthesis is not a summary** — it must integrate findings into novel analysis, identify patterns across sources, and surface emergent insights not present in any single source
15. **PreToolUse Edit hook is non-negotiable** — the research skill never modifies source files; it only creates/updates journals in `~/.claude/research/`
