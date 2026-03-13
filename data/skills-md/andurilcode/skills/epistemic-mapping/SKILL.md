---
name: epistemic-mapping
description: Apply epistemic mapping whenever the user is starting an analysis, entering unknown territory, or needs to understand the limits of their own knowledge before acting. Triggers on phrases like "what do we know?", "what are we missing?", "what would change our minds?", "what are our assumptions?", "where are the blind spots?", "we don't know what we don't know", "what should we validate first?", "what's the riskiest assumption?", or at the start of any complex investigation, design, or decision. Also trigger before other analysis frameworks when the knowledge landscape hasn't been mapped — running diagnosis without knowing what you don't know is a common failure mode. Map your knowledge before you reason with it.
---

# Epistemic Mapping

**Core principle**: Before reasoning about a problem, map the quality and completeness of what you actually know. Unknown unknowns are more dangerous than known unknowns. Confusing belief for knowledge is more dangerous than both.

This is distinct from Cognitive Bias Detection (which audits *how* you reason) — epistemic mapping audits *what* you know and don't know.

---

## The Knowledge Quadrants

Adapted from the Johari Window / Rumsfeld quadrant:

```
                    YOU KNOW IT        YOU DON'T KNOW IT
                 ┌──────────────────┬──────────────────────┐
  IT'S TRUE      │  Known Knowns    │  Unknown Knowns      │
  (reality)      │  (foundation)    │  (blind spots)       │
                 ├──────────────────┼──────────────────────┤
  IT'S NOT TRUE  │  Known Unknowns  │  Unknown Unknowns    │
  (gaps)         │  (open questions)│  (surprises)         │
                 └──────────────────┴──────────────────────┘
```

### Known Knowns
Facts you hold and that are actually true. The foundation for reasoning.

**Risk**: Mistaking beliefs for facts. Something can be a Known Known to you and still be wrong. Ask: *"How do I know this? What's the evidence?"*

### Known Unknowns
Gaps you're aware of. Open questions. Things you've identified as needing research or validation.

**Opportunity**: These are actionable — you know what to go find out.

### Unknown Knowns
Things that are true but you don't realize you know them — or don't realize they're relevant. Also: things the team collectively knows but individuals don't.

**Risk**: Reinventing the wheel. Failing to consult the right person. Missing relevant context that exists in the organization or in prior work.

**Fix**: Wider consultation, explicit knowledge-sharing before analysis.

### Unknown Unknowns
Things you don't know and don't know you don't know. The most dangerous category.

**You can't enumerate them** — but you can reduce them by:
- Bringing in outside perspectives
- Examining your assumptions explicitly
- Looking at prior failures in analogous situations
- Asking "what would surprise me here?"

---

## The DIKW Stack

Knowledge quality isn't binary. Place claims on the stack:

| Level | Description | Example |
|-------|-------------|---------|
| **Wisdom** | Knowing what to do with knowledge | "Given X, we should prioritize Y" |
| **Knowledge** | Synthesized understanding | "Our pipeline degrades under concurrent load" |
| **Information** | Interpreted data | "Latency increases 3× with 5+ parallel agents" |
| **Data** | Raw observations | "Latency: 340ms, 420ms, 890ms, 1200ms, 980ms" |
| **Belief** | Held without clear basis | "The bottleneck is probably the DB" |

Most analyses mix levels without labeling them. Epistemic mapping surfaces where you're reasoning from data vs. belief.

---

## The Pre-Analysis Questions

Before starting any significant investigation or decision:

**1. What do we know with high confidence?**
List facts backed by direct evidence, measurement, or reliable external sources. Be strict — "everyone thinks" is not high confidence.

**2. What do we believe but haven't validated?**
Assumptions held as truths. Prior experiences being applied to the current context. Intuitions.

**3. What are our open questions?**
Known unknowns — gaps we're aware of. Rank by importance: which of these, if answered, would most change our approach?

**4. Where might we have blind spots?**
Who is not in the room? Whose perspective are we missing? What analogous situations have surprised people in the past?

**5. What would change our minds?**
Pre-commit to this before analysis. What evidence, if observed, would lead to a different conclusion? If nothing could change your mind — that's a belief, not a reasoned position.

**6. What's the most dangerous assumption?**
The assumption that, if wrong, most undermines the current plan or analysis.

---

## Output Format

### 🗺️ Knowledge Map

**Known Knowns** (high-confidence facts)
- [Fact 1] — Source: [how we know]
- [Fact 2] — Source: [how we know]

**Working Beliefs** (assumed true, not validated)
- [Belief 1] — Risk if wrong: [High / Medium / Low]
- [Belief 2] — Risk if wrong: [High / Medium / Low]

**Known Unknowns** (open questions, ranked)
1. [Most important gap] — Why it matters: [impact on decision/analysis]
2. [Second gap] — Why it matters: ...

**Suspected Blind Spots**
- [Area where we might not know what we don't know]
- Outside perspectives we haven't consulted
- Historical analogues we haven't examined

### ⚠️ Most Dangerous Assumption
- **Assumption**: [The belief most critical to the current approach]
- **If wrong**: [What breaks]
- **How to validate**: [Cheapest/fastest way to check]
- **Cost of being wrong late**: [What it costs if this surfaces after commitment]

### 🔄 Mind-Change Conditions
Pre-committed conditions that would cause re-evaluation:
- *"If we observe X, we will revise our view on Y"*
- *"If [key assumption] is false, we will [specific response]"*

### 📋 Investigation Priority
Rank the Known Unknowns by: (Importance × Feasibility to answer)
| Question | Importance | Feasibility | Priority |
|----------|-----------|-------------|---------|
| [Q1] | High | High | 1 — answer now |
| [Q2] | High | Low | 2 — reduce uncertainty incrementally |
| [Q3] | Low | High | 3 — answer opportunistically |

---

## Epistemic Hygiene Rules

- **Label your claims**: Is this data, information, knowledge, or belief? Say which.
- **Source your facts**: "We know X" without a source is a belief wearing a fact's clothes.
- **Pre-commit to falsifiability**: If you can't say what would change your mind, you're not reasoning — you're rationalizing.
- **Name the room**: Who's not here? Whose knowledge are we missing?
- **Distinguish absence of evidence from evidence of absence**: "We haven't seen this fail" ≠ "This won't fail."

---

## Thinking Triggers

- *"Are we treating this belief as a fact?"*
- *"Who has relevant knowledge that we haven't consulted?"*
- *"What would a skeptic say we're missing?"*
- *"What happened last time someone approached a similar problem without knowing X?"*
- *"If this analysis is wrong, what's the most likely reason?"*
- *"What question, if answered, would most change our approach right now?"*
