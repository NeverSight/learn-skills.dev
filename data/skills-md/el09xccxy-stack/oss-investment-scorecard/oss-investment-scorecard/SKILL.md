---
name: oss-investment-scorecard
description: >
  Evaluate whether an open source project / company is investable by a USD-denominated VC fund in the current AI cycle.
  ALWAYS use this skill when the user asks any of the following:
  - "evaluate [project] for investment"
  - "can we invest in [project]"
  - "score this open source company"
  - "投资评估 [项目]"
  - "这个开源项目值得投吗"
  - "给 [公司] 打分"
  - Any request to assess, rate, or rank an open source startup's investability
  - Any comparison of two or more open source companies from an investment perspective
  The skill produces a structured 5-dimension weighted scorecard (max 10 pts), a pass/recommend/watch verdict, and an IC-ready one-paragraph thesis. It also flags one-vote-veto conditions that cause an immediate Pass regardless of total score.
---

# Open Source Project Investment Scorecard

## Purpose

Produce a rigorous, consistent, reusable investment evaluation for any open source project/company being considered by a USD VC fund — specifically calibrated for the **AI technology acceleration cycle (2023-onwards)**.

Built from: Bessemer Venture Partners Data 3.0 Roadmap, Oxx VC, Basis Set Ventures, Linux Foundation / COSSA, Unusual VC, Matrix VC, and two live case studies (Eigent.AI / CAMEL-AI and Datastrato / Apache Gravitino).

---

## Step 1 — Macro Gate (Non-Scoring Pre-Check)

Before scoring, answer these three binary questions. If any answer is NO, stop and recommend Pass.

1. **Is the sub-sector still in its window-of-opportunity phase?**
   - Yes if: no single open-source project has monopolised the niche yet, OR the target IS that emerging monopolist.
   - No if: a dominant closed-source or open-source player already owns >60% mindshare AND the target has no credible differentiation.

2. **Does open-source mode confer structural advantage here?**
   - Yes if: vendor-neutral governance, community data flywheel, standards control, or ecosystem lock-in applies.
   - No if: the project is essentially a wrapper / prompt-engineering layer with no community moat.

3. **Is the AI-cycle value premium applicable?**
   - Higher than cloud-era because: the project sits on a structural chokepoint in the AI stack — examples include inference throughput optimisation, training data infrastructure, model/experiment lifecycle management, AI-native metadata governance, or hardware abstraction layers where the open-source project becomes the compatibility standard across chips and cloud platforms.
   - If purely a cloud-era Open Core play with no AI-cycle differentiation, note this as a risk factor (not automatic veto).

If all three pass → proceed to the five-dimension scorecard.

---

## Step 2 — Five-Dimension Scorecard

Score each dimension **0–10**. Apply weights. Sum for a weighted total out of 10.

| # | Dimension | Weight |
|---|-----------|--------|
| A | Open-Source Ecosystem & Community Health | 25% |
| B | Team & Globalisation Capability | 20% |
| C | Technical Moat & Market Positioning | 20% |
| D | Commercialisation Path & PMF | 20% |
| E | Capital Exit Path | 15% |

---

### Dimension A — Open-Source Ecosystem & Community Health (25%)

**Core principle: Keyboard Metrics > Mouse Metrics.**
GitHub Stars are the most manipulable vanity metric. Prioritise the following in descending importance:

| Signal | What to Look For | Strong (8-10) | Weak (<5) |
|--------|-----------------|---------------|-----------|
| Dependent Repositories | Projects that depend on this one in production | ≥1,000 | <10 |
| Monthly Active Contributors | Unique devs with commits in last 30 days | ≥50 | <5 |
| External Contributor % | Non-core-team share of commits | ≥40% | <10% |
| PR Merge Latency | Avg days open→merged | ≤7 days | >30 days |
| Issue Close Rate (90d) | % issues resolved | ≥60% | <20% |
| Release Cadence | Regularity of versioned releases | Weekly/bi-weekly | Sporadic |
| ADOPTERS.md / Enterprise Logos | Named production deployments | 5+ named logos | None |
| Governance Tier | ASF TLP > ASF Incubator > CNCF > standalone | ASF TLP | No governance |
| Stars — same-sector Share of Voice | Not absolute; compare to 3 closest rivals | Top-2 in niche | Bottom half |
| Prestigious Backing | GitHub SOS Fund, CNCF Sandbox, LF project | Yes | No |

**Scoring guide:** Average the signals above. An ASF Top-Level Project graduation is worth +1 bonus point (rare, non-manipulable).

**One-Vote Veto for A:** External contributor % <5% (pure self-directed project) → automatic Pass.

---

### Dimension B — Team & Globalisation Capability (20%)

Two sub-components weighted equally: **Engineering Depth** and **GTM/Global Reach**.

**Engineering Depth signals:**
- Founders are Apache/CNCF/Linux Foundation committers or PMC members in the relevant stack
- Verifiable open-source contribution history (not just the company repo)
- Top-tier academic papers with reproducible benchmarks (NeurIPS / ICML / ICLR / VLDB)
- Prior experience at foundational data/AI infrastructure companies (Cloudera, Databricks, Hortonworks, Confluent, Anyscale equivalent)

**GTM / Global Reach signals:**
- English-first documentation and GitHub presence (Day 1)
- International (non-founding-country) contributors ≥20% of community
- US paying customers or US-based enterprise pilots
- Founder network includes: top VC relationships, Fortune 500 engineering leaders, or prior role as LF/ASF committee chair
- Cayman/Singapore holding structure already in place (or clear plan)

**Scoring guide:**
- 9-10: World-class engineers who are also natural community builders with proven US enterprise access
- 7-8: Strong engineering + partial GTM (needs one key hire)
- 5-6: Strong engineering, weak GTM — flag as "Series A condition"
- <5: Academic team with no commercial execution evidence

**One-Vote Veto for B:** Zero verifiable open-source contribution history outside the company's own repo → automatic Pass.

---

### Dimension C — Technical Moat & Market Positioning (20%)

**Technology Layer Assessment (use highest applicable):**

| Level | Description | VC Signal |
|-------|-------------|-----------|
| L1 | New algorithm / architecture (e.g., DeepGCNs, PagedAttention) | Strongest moat |
| L2 | Significant engineering innovation on known approach | Strong moat |
| L3 | Differentiated system integration / toolchain | Moderate moat |
| L4 | Prompt engineering / fine-tuning only | Pass — no moat |

**Market Positioning:**
- Is this project on track to be the **de facto standard** in its niche?
  - Evidence: independent benchmarks, neutral analyst reports, competitor integrations pointing TO this project
- Does vendor-neutrality create structural lock-in? (Apache governance = enterprise procurement preference)
- Is the sub-sector one of the high-value AI-cycle niches?
  - AI Toolchain (RAG, eval, data synthesis) ✅
  - Edge AI / on-device inference ✅
  - Vertical Models with proprietary data ✅
  - AI-native metadata / data governance ✅
  - General-purpose LLM (competing with OpenAI/Google) ⚠️ very high bar

**Narrative Consistency Check:**
Count how many times the company's core value proposition has changed in public materials. ≥2 pivots in <24 months = -1 point penalty.

**One-Vote Veto for C:** Core product is L4 (Prompt Engineering / fine-tuning wrapper) with no underlying algorithmic differentiation → automatic Pass.

---

### Dimension D — Commercialisation Path & PMF (20%)

**Revenue Quality Hierarchy (highest = best for VC):**

| Rank | Type | VC Multiple | Note |
|------|------|------------|------|
| 1 | Product ARR / Subscription | 8-15x | Best — scales without headcount |
| 2 | Usage-based / API billing | 6-10x | Good — correlates with value delivered |
| 3 | Infrastructure embedding / OEM licensing | Strategic premium | Your engine embedded inside cloud or hardware vendor stacks (e.g., vLLM inside AWS, NVIDIA); licensing or rev-share model; valued on strategic control, not pure ARR multiple |
| 4 | Proprietary data & model asset monetisation | High ceiling, emerging multiple | Selling curated training datasets, benchmark suites, or evaluation infrastructure to AI labs and enterprises; structurally valued in AI cycle but comp set is thin |
| 5 | Professional Services | 1-3x | ⚠️ Not scalable — PS revenue caps out with team size; triggers mandatory product ARR conversion condition in term sheet |
| 6 | Grants / non-dilutive only | 0x | ⚠️ Not VC-grade revenue |

**Key metrics to gather and evaluate:**

| Metric | Healthy Signal | Risk Signal |
|--------|---------------|-------------|
| ARR / revenue (last 12m) | Growing ≥50% YoY | Flat or declining |
| Largest customer concentration | No single customer >30% | One customer >50% |
| Customer geography | US-paying customers present | 100% non-US |
| Gross margin | ≥70% (product), ≥50% (PS) | <40% |
| Inbound % of pipeline | ≥50% inbound (community-driven) | 100% outbound |
| Revenue type | Product ARR dominant | PS dominant |
| Runway | ≥18 months post-raise | <12 months |

**PS Revenue Special Rule:**
PS revenue is not a veto, but it triggers a mandatory condition: in the term sheet, require conversion to ≥$Xk product ARR within 18 months. The threshold X = 50% of current PS ARR.

**Scoring guide:**
- 9-10: Product ARR ≥$1M with US enterprise customers, ≥50% inbound, no single customer >30%
- 7-8: Early product ARR + strong PMF signals (Uber/Apple-calibre logos paying, even if small)
- 5-6: PS revenue with credible enterprise logos OR product revenue <$500K
- <5: No paid customers, or 100% grant-funded, or single customer >70%

**One-Vote Veto for D:** Revenue entirely unverified (LoI/MOU only, no signed contracts) AND current valuation >2× sector median → automatic Pass.

---

### Dimension E — Capital Exit Path (15%)

**Exit Path Matrix:**

| Path | Probability Triggers | Typical Valuation Driver |
|------|---------------------|--------------------------|
| Strategic M&A | Project = de facto standard OR team = acqui-hire grade | Strategic control premium (often >ARR multiple) |
| IPO | ARR ≥$50M, growth ≥30%/yr, category leadership | ARR × 8-15x |
| Secondary (VC→PE) | Stable growth + clear path, not IPO-ready | DCF + option value |
| Follow-on rounds | Good progress, not yet exit-ready | Mark-up on next round |

**Strategic M&A value checklist — score higher if:**
- Project is the "Tabular to Databricks" analogue in its niche (infrastructure standard creator)
- Acquirer has clear "must have or competitor gets it" urgency
- Apache / CNCF governance means acquirer gets community credibility, not just code
- Named enterprise customers are logos the acquirer wants in their annual report

**Comparable exit anchors to use:**

| Comparable | Exit | Key Logic |
|-----------|------|-----------|
| Tabular → Databricks | ~$2B | Creator of Iceberg standard → catalog control |
| Red Hat → IBM | $34B | Enterprise Linux standard → platform lock-in |
| GitHub → Microsoft | $7.5B | Developer workflow monopoly |
| HashiCorp → IBM | $6.4B | Infra toolchain standard |
| Databricks | $43B (private) | Data + AI platform standard |

**Scoring guide:**
- 9-10: Clear "must acquire" logic for 2+ named potential buyers; comparable exits >$1B
- 7-8: Credible M&A story with 1-2 named buyers; or strong IPO path visible at Series B/C
- 5-6: Acqui-hire probable; or M&A possible but buyer urgency low
- <5: No credible exit path; project likely to be forked rather than acquired

---

## Step 3 — Compute Weighted Total

```
Total = (A × 0.25) + (B × 0.20) + (C × 0.20) + (D × 0.20) + (E × 0.15)
```

**Decision thresholds:**

| Score | Decision | Action |
|-------|----------|--------|
| 8.5 – 10.0 | 🟢 Strongly Recommend | Fast-track IC; move to term sheet |
| 7.0 – 8.4 | 🟡 Recommend with Conditions | Proceed with milestone-linked terms |
| 5.5 – 6.9 | 🟠 Watch / Track | Add to pipeline; re-evaluate in 6 months |
| < 5.5 | 🔴 Pass | Decline; note reason for future reference |

**One-Vote Vetoes (any = automatic Pass, overrides total score):**
1. External contributor % <5%
2. Zero verifiable engineering contribution history outside company repo
3. Core product is L4 (Prompt Engineering only)
4. Narrative pivot ≥3 times in <24 months
5. Revenue entirely LoI/MOU only + valuation >2× sector median
6. No English documentation AND zero international contributors — applies to any single-country project claiming global ambition

---

## Step 4 — Required Output Format

Always produce output in this order:

### 1. Macro Gate Result
One sentence per question. State whether the project passes the gate.

### 2. Scorecard Table

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| A. Open-Source Ecosystem | 25% | X/10 | X.XX |
| B. Team & Globalisation | 20% | X/10 | X.XX |
| C. Technical Moat | 20% | X/10 | X.XX |
| D. Commercialisation & PMF | 20% | X/10 | X.XX |
| E. Exit Path | 15% | X/10 | X.XX |
| **Total** | 100% | — | **X.XX/10** |

### 3. Verdict Line
`🟢/🟡/🟠/🔴 [Decision] — [One sentence rationale]`

### 4. Dimension Narrative
For each dimension: 2-4 sentences covering the key evidence, the strongest signal, and the main risk. Be direct — do not soften risks.

### 5. One-Vote Veto Check
Explicitly confirm whether any veto condition is triggered.

### 6. IC Thesis (one paragraph, ≤100 words)
Suitable for verbal delivery in an Investment Committee. Structure: ① why now ② why this project ③ exit path conviction.

### 7. DD Priority List
Top 3-5 open questions that, if answered positively, would raise the score by ≥0.5 points. Ranked by importance.

### 8. Watch Triggers (if verdict is Watch/Track)
Specific, measurable milestones that, if hit, would upgrade to Recommend.

---

## Calibration Reference: Scored Examples

See `references/scored-examples.md` for:
- **vLLM/Inferact: Total 8.9/10 → Strongly Recommend. Category-defining inference standard; 2,000+ contributors; a16z + Lightspeed validation. Strong open-source (7.5) and team (6.5) undercut by PMF (4.5) and three narrative pivots.
- **Hugging Face: Total 8.5/10 → Strongly Recommend. $130M ARR, 10,000+ enterprise customers, Google/Amazon/NVIDIA as investors and distribution partners.

These two cases define the calibration anchors for the scoring scale.
