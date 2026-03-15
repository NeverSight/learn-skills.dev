---
name: ib_trade-osint
description: "OSINT Intelligence Cycle & Prefilter skill. Transforms raw public information into actionable, trade-relevant intelligence by prioritizing recency, source authority, and market impact."
---

# Skill: ib_trade-osint

## Purpose
This skill implements a fully automated, trading-specific Open Source Intelligence (OSINT) cycle. It transforms raw public information into actionable, trade-relevant intelligence by prioritizing recency, source authority, and probable market impact.

## Core Mandates
1. **Recency First:** Prioritize information from the last 24–48 hours. Max window is 14 days.
2. **PRIO-A Dominance:** Official releases, news wires, and primary market-moving sources (PRIO A) must be checked first before moving to lower-priority discovery (PRIO B, C, D).
3. **No Trade Without Catalyst:** Do not recommend trades based on noise. Only high-impact, corroborated catalysts survive the prefilter.
4. **Adversarial Interrogation:** Treat every signal as a hypothesis. Corroborate across independent sources before confirming a "high impact" score.

## 1. The Intelligence Cycle
The cycle consists of six continuous phases:
1. **Planning:** Define the objective (e.g., "Identify AI supply chain shocks in the next 72h").
2. **Collection:** 70% controlled (user-curated) / 30% open discovery.
3. **Processing:** Cleaning, normalization, deduplication, and entity extraction (tickers, sectors, regions).
4. **Evaluation:** Apply the 4x4 Priority x Impact Matrix.
5. **Analysis:** Identify first/second-order causal chains and directional (Bullish/Bearish) implications.
6. **Dissemination:** Produce machine-readable intelligence candidates for the Analysis skill.

## 2. Source Priority Taxonomy
- **PRIO A (Primary):** SEC filings, official press releases, news wires, regulatory/government notices.
- **PRIO B (Market Structure):** Market data, earnings calendars, analyst revisions, options flow.
- **PRIO C (Contextual):** Specialist industry reporting, security research, trade publications.
- **PRIO D (Discovery):** Social chatter, minor blogs, forums (Weak signals only).

## 3. The Prefilter Matrix (4x4)
Score every event to decide if it survives for analysis:

| Priority \ Impact | Low | Medium | High |
|---|---|---|---|
| **PRIO A** | Watchlist Link only | Retain & Map | **Immediate Escalation** |
| **PRIO B** | Context only | Retain | **Immediate Escalation** |
| **PRIO C** | Archive | Context | Corroboration Required |
| **PRIO D** | Ignore | Queue | Alert Only |

## 4. Scoring Logic (Thresholds)
- **Score (0-15+):** Sum of weights (Priority: A=4, B=3, C=2, D=1; Impact: High=4, Med=3, Low=2; Directness: Ticker=3, Sector=2).
- **12+:** High-conviction intelligence candidate.
- **9-11:** Retain for fusion.
- **<9:** Archive or discard.

## 5. Decision Translation
- **Buy/Sell Now:** High-conviction (12+) + Bullish/Bearish direction + Direct Ticker impact.
- **Limit Order:** High-conviction + Directional edge + Volatility/Price dislocation.
- **Watch:** Low-conviction or mixed signals.

## 6. Target Intelligence Schema (JSON/YAML)
Every result must include:
- `ticker`: Affected asset(s).
- `catalyst_score`: Numerical value based on the prefilter.
- `direction`: `bullish`, `bearish`, or `mixed`.
- `impact_horizon`: `0-24h`, `24-72h`, or `7d`.
- `confidence`: `confirmed`, `probable`, or `possible`.
- `source_refs`: List of URLs or source IDs.
