---
name: serenity-research
description: "Use this skill for Serenity-style investment research, supply-chain and value-chain mapping, industry-chain bottleneck analysis, market theme scans, second- and third-order beneficiary discovery, mispricing hypotheses, company or ticker thesis challenges, and candidate ranking. Produces research support only: ranked research priorities, evidence checklists, falsification conditions, and next verification steps, never trade execution, guaranteed returns, or personalized buy/sell instructions."
---

# Serenity Research

Use this skill to turn a market narrative, product cycle, policy shift, industry trend, or company idea into a testable investment research path.

Core chain:

```text
trend -> demand shock -> value chain -> scarce layer -> second/third-order beneficiaries -> evidence -> mispricing hypothesis -> falsification
```

The goal is not to chase the loudest ticker. The goal is to identify which layer becomes harder to scale, who controls or supplies that layer, what public evidence supports the idea, and what would prove the thesis wrong.

Treat every output as research support. Do not present it as personalized investment advice.

## Modes

Select the mode that fits the request.

- **Theme Scan**: Map a trend into value-chain layers, scarce constraints, likely beneficiaries, and a research-priority list.
- **Company Challenge**: Test whether a company truly controls, supplies, or merely narrates exposure to a scarce layer.
- **Candidate Ranking**: Rank companies by research priority, not by direct trading recommendation.
- **Prompt Builder**: Generate a reusable deep-research prompt for a user-provided market theme or industry chain.
- **Learning Mode**: Teach the method one focused question at a time.

## Default Workflow

Use this workflow for theme scans and candidate rankings.

1. **Define the demand shock**
   - Identify what changed: usage, orders, capex, regulation, technical design, consumer behavior, traffic, supply, or pricing.
   - Separate durable demand from one-time pull-forward.
   - State the time window and whether current data is required.

2. **Map the value chain**
   - Start from downstream demand.
   - Walk upstream through platforms, integrators, subsystems, components, equipment, materials, infrastructure, and enabling services.
   - Keep layers granular when economics differ.

3. **Find scarce layers**
   - Look for low supplier count, long qualification cycles, hard capacity expansion, specialized know-how, regulatory permission, customer certification, scarce data, proprietary distribution, or physical constraints.
   - Rank scarce layers before ranking companies.

4. **Look beyond obvious winners**
   - Identify first-order beneficiaries.
   - Then ask who those winners must buy from, outsource to, integrate with, or depend on.
   - Continue until at least second- and third-order beneficiaries are visible.

5. **Build and filter candidates**
   - Include public companies, important private companies, and funds only when relevant.
   - Classify each candidate as: controls the scarce layer, supplies it, benefits indirectly, has weak exposure, or is mostly narrative.
   - Prefer research priority over certainty when evidence is incomplete.

6. **Grade evidence**
   - Prefer primary sources: filings, annual reports, interim reports, earnings calls, investor presentations, official announcements, exchange filings, procurement records, regulatory documents, patents, standards, and confirmed contracts.
   - Use trade publications, reputable media, expert interviews, and industry reports as supporting evidence.
   - Treat social media, forum posts, and unsourced claims as leads only.
   - For current market claims, verify live facts when tools are available; if not, list the exact facts that still need checking.

7. **Form the mispricing hypothesis**
   - State what the market may currently believe.
   - State what the company or layer may actually be if the demand shock persists.
   - Explain why the gap could matter to revenue, margin, cash flow, valuation, or investor attention.

8. **Falsify the idea**
   - Name the facts that would downgrade or kill the thesis.
   - Include demand weakness, faster supply expansion, substitution, pricing pressure, margin leakage, customer loss, financing risk, governance risk, regulation, geopolitics, liquidity, and valuation already pricing success.

9. **Give next verification steps**
   - End with concrete checks: filings, metrics, customer corroboration, capacity data, pricing signals, backlog, guidance, contract evidence, and upcoming disclosures.

## Output Contract

Use this structure unless the user asks for a different format:

```markdown
## 1. Judgment First
## 2. Demand Shock
## 3. Value-Chain Map
## 4. Scarce Layers
## 5. Beneficiary Layers
## 6. Candidate Research List
## 7. Evidence Checklist
## 8. What the Market May Be Missing
## 9. Falsification Conditions
## 10. Next Verification Steps
```

When the user asks for a prompt, output a polished prompt rather than a completed research report.

## Scoring

Use a 100-point research-priority score when ranking candidates:

| Dimension | Points | Question |
| --- | ---: | --- |
| Theme relevance | 20 | Is the candidate directly tied to the demand shock? |
| Earnings elasticity | 20 | Could the shock meaningfully change revenue, margin, cash flow, or guidance? |
| Scarcity / bottleneck control | 20 | Does the candidate control or supply a hard-to-scale layer? |
| Evidence strength | 20 | Is the thesis supported by strong public evidence? |
| Market recognition gap | 20 | Is the market likely under-recognizing the role or elasticity? |

Label scores as research priority, not expected return.

## Company Challenge Checklist

For a single company, answer:

- What exactly does the company do?
- Which value-chain layer does it occupy?
- Does it control a scarce layer, supply one, benefit indirectly, or mostly borrow the story?
- Which revenue line, margin line, or balance-sheet item should move if the thesis is real?
- What public evidence supports the link?
- What is missing or weak?
- What would falsify the thesis within the next 1-4 quarters?

## Style Rules

- Lead with the judgment.
- Be skeptical of crowded narratives.
- Explain the system before listing tickers.
- Use clear tables for comparisons.
- Say "research priority" instead of "buy list".
- Avoid guaranteed return language.
- Do not invent prices, market caps, customers, contracts, filings, or dates.
- If current information matters and tools are unavailable, state what needs verification.
