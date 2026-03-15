---
name: deep-research
description: >
  Conduct deep, source-grounded research with freshness checks and citations, then synthesize an actionable answer. 
  Use for time-sensitive, niche, or high-stakes topics; when the user asks to “zweryfikuj”, “zrób research”, or when uncertainty is high.
compatibility: > 
  Requires internet access (Cursor browser / web tools or MCP). 
  Optional: MCP memory to store research memos.
allowed-tools: WebSearch(*) MCP(*) Read
metadata:
  mode: progressive-disclosure
  outputs: research-brief, decision-memo, implementation-notes
---

# deep-research

## Activation gate (anti-noise)
Run only if at least one is true:
- User explicitly requests research/verification or provides external links.
- Topic is time-sensitive (prices, laws, tooling versions, security, vendor docs).
- You detect >10% risk of outdated knowledge.
Otherwise: answer normally (no research ritual).

## Research protocol
### 1) Frame
- Restate the question as a falsifiable query.
- Define “freshness window” (e.g., last 3–6 months) unless user asks historical.
- Define acceptance criteria for sources (primary docs preferred).

### 2) Collect sources
- Prefer: official docs, primary specs, reputable engineering blogs, vendor changelogs.
- For each key claim, capture at least one authoritative source.
- If sources disagree: represent both and explain implications.

### 3) Extract & normalize
- Extract only what is needed to answer.
- Keep notes in a compact “evidence table” (claim → source → date).

### 4) Synthesize
Produce one of:
- Research brief (short, decision-oriented)
- Decision memo (trade-offs + recommendation)
- Implementation notes (steps + verification commands)

### 5) Verification hooks (optional)
If the environment allows:
- Provide 1–3 concrete commands/tests to verify claims locally.
- For Cursor, prefer commands that are fast and deterministic.

## Optional: store memo to MCP memory
If the user says “zapisz”:
- Store: question, key findings, chosen decision, links, and date.

## Output contract
- Lead with recommendation.
- Then evidence-backed reasoning (citations).
- End with “how to verify quickly”.

## Failure handling
If web/tools not available:
- Mark claims as UNCERTAIN.
- Provide the shortest verification path (exact query + official doc location).
