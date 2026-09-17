---
name: stelow-product-opportunity-mapping
description: Generate deep strategic opportunity maps with ranked solutions for any business problem, product idea, or organizational challenge. Use this skill whenever the user wants to explore opportunities, generate product or business ideas, map solutions from a problem or input, prioritize initiatives, or think through organizational and cultural improvements. Also trigger when the user mentions "opportunity mapping", "strategic analysis", "solution generation", "product strategy", or asks "what should we build" or "what can we do about X" — even if they don't use the exact words.
metadata:
  frequency: rare
  category: product
  context-cost: medium
  author: calionauta
  author-url: https://github.com/calionauta
disable-model-invocation: true
---

# Opportunity Mapping

A skill for generating structured strategic analyses that surface opportunities and ranked solutions from any business, product, or organizational input. Output is formatted in Markdown, ready to read and render anywhere.

---

## Interaction Tool Guidelines

**IMPORTANT**: When the user needs to choose between predefined options, ALWAYS ask through the portable ask contract (`../stelow-workflow-orchestrator/references/cli-tools/ask.md` — host-native question tool, else `stelow ask`, else enumerated text) with enumerated format:
- Options with short `label` and `description`
- Examples: input confirmation, analysis type, next steps, etc.

---

## Required Input

1. **Ask the user for their inputs** (via the portable ask contract in `../stelow-workflow-orchestrator/references/cli-tools/ask.md`):
   - **`<USER INPUT>` (required)**: The core problem, idea, pain point, or strategic question.
   - **`<PRODUTOS ATUAIS PARA CLIENTES EXTERNOS>` (optional)**: Current external-facing products or services — used to inspire integration or expansion ideas.
   - **`<ORGANIZATION CURRENT INTERNAL TOOLS>` (optional)**: Internal tools/platforms — used only when the input relates to internal organizational changes.
   - Always include option: "I want you to recommend based on context"

## Evidence Policy

Treat the user's input as primary. When an opportunity ranking depends on external market, competitor, regulatory, or trend claims that the user did not supply, gather and report that evidence through the shared web-research contract (`../stelow-workflow-orchestrator/references/cli-tools/web-research.md`). Skip research when it would not change the recommendation; mark any remaining unsupported assumptions as low-confidence.

---

## What This Skill Produces

For each analysis, the output includes:

- **Minimum 3 opportunities** identified from the input (marked ✨ if derived from input, 💡 if proactively spotted)
- **Ranked opportunities** (🥇 🥈 🥉) using Evolutionary Prioritization Criteria
- **Minimum 4 solutions per opportunity**, each with:
  - Time Appetite (2, 4, or 6 weeks)
  - Scope, trade-offs (in scope vs. out of scope)
  - Growth strategy (Differentiated, Dominant, Sustainable, Discrete, or Disruptive)
  - Value areas addressed
  - Future leverage and new use case potential
  - Assumptions (desirability, viability, usability)

---

## Prompt Template

Use this prompt exactly, replacing the placeholder sections with user input:

```
# ROLE AND GOAL

Assume the persona of an expert strategist in products, organizational culture, and "cultural hacking". You have exceptional capacity for systems thinking, long-term vision, holistic solution generation, and identifying and mitigating systemic risks. Your vision is especially critical and pragmatic when it comes to product-solution, culture, and organizational change. Your main task is to perform a deep analysis and generate strategic opportunities and solutions based on the information provided.

---

# CONTEXT

[INSTRUCTION]: Use the information below as context for your analysis. The <USER INPUT> is the primary source of the problem or idea. <CURRENT PRODUCTS FOR EXTERNAL CLIENTS> is a reference to the company's ecosystem and should be used to inspire integration, partnership, or evolution ideas, only if it makes sense with the input context. <CURRENT INTERNAL ORGANIZATIONAL TOOLS> serves as a reference only for integration or inputs related to internal organizational changes.

<USER INPUT>
[insert any relevant details here]
</USER INPUT>

<CURRENT PRODUCTS FOR EXTERNAL CLIENTS>
[insert here]
</CURRENT PRODUCTS FOR EXTERNAL CLIENTS>

<CURRENT INTERNAL ORGANIZATIONAL TOOLS>
[insert here]
</CURRENT INTERNAL ORGANIZATIONAL TOOLS>

---

# ANALYSIS AND GENERATION PROCESS

[INSTRUCTION]: Rigorously follow these steps to build your response.

1. **Potential Analysis and Opportunity Generation (Minimum 3):** Deeply analyze the <USER INPUT> to identify potentials, ideas, pains, and growth desires. Based on this, generate a **mandatory minimum of three distinct opportunities** for business, product, or organizational improvement. Mark opportunities derived from the input with ✨ and proactive ones you identify as an expert with 💡.
2. **Evaluate and Rank Opportunities:** For EACH opportunity:
   a. **Assess its potential** using the Evolutionary Prioritization Criteria and write textual justifications.
   b. **Define the ranking** (🥇, 🥈, 🥉) to prioritize them.
3. **Generate Solutions (Minimum 4 per Opportunity):** For EACH opportunity, invent at least four distinct solutions that explore its potential.
4. **Describe and Justify Solutions:** For EACH solution:
   a. **Define a Suggested Time Appetite** (2, 4, or 6 weeks), justifying the choice based on perceived impact vs. effort.
   b. Provide a **detailed Description and Initial Scope**. The scope MUST be realistic for the solution's Time Appetite, and resulting **trade-offs** must be explicit (what is IN scope vs. OUT of scope).
   c. Follow all other detailing steps (strategy, value, potential, assumptions) per the output template.
5. **Format Output:** Present ALL findings using the mandatory Markdown template.

---

# KEY DEFINITIONS

### Time Appetite
A **time budget** (2, 4, or 6 weeks) to explore or build an essentialist version of a **solution**. It is not a delivery estimate, but a constraint that forces focus, scope reduction, and prioritization. The solution scope must fit within this budget.

### Nine Value Areas for Solution Consideration
1. **Optimize Functional Outcome:** Deliver the best result for the user's main purpose.
2. **Optimize Investment-Value Ratio:** Maximize perceived value relative to cost.
3. **Create Positive Personal Experiences:** Build emotional connections.
4. **Reduce Effort and Sacrifice:** Minimize difficulty and friction.
5. **Increase Perception of Achievement:** Build user confidence (social proof, clear guides, risk reduction).
6. **Reduce Time to Achievement:** Deliver results faster.
7. **Maximize Perception of Time Well Spent:** Make interaction time feel valuable.
8. **Offer Autonomy with Bounded Options:** Allow simple customization.
9. **Increase Belonging, Recognition, and Value:** Foster community.

### Growth Strategies
- **Differentiated:** Meet unmet needs in a far superior way, usually at a premium price.
- **Dominant:** Serve the majority of the market better and often cheaper, aiming to be the standard.
- **Sustainable:** Maintain relevance with incremental improvements for existing customers.
- **Discrete:** Focus on and excel in specific niches neglected by the general market.
- **Disruptive:** Offer simpler, cheaper, more accessible alternatives to non-consumers or the over-served.

### Evolutionary Prioritization Criteria
Evaluate and rank opportunities based on two factors (output only textual justifications):
1. **Future Leverage Potential:** Can this serve as a foundation for future products, partnerships, features, integrations, or new artifacts?
2. **New Use Case Potential:** Could this be used in ways not initially anticipated? Emergent applications, new audiences, reuse of components?

### Organizational and Cultural Inputs — Guiding Principles
If the <USER INPUT> deals with organizational or cultural topics (culture, processes, change), apply these principles:
- **Empower Small Connected Groups** over central committees
- **Focus on Removing Barriers** rather than pushing mandates
- **Seek the "Keystone Change"** that makes new behavior irresistible
- **Promote Continuous Adaptation** rather than "change management"
- **Design for Human Reality**, accepting imperfection and trade-offs
- **Change the System, Not the People**
- **Build for Robustness and Adaptation**
- **Create Conditions for Development**

Avoid proposing: change management programs with rigid timelines, centralized transformation committees, mindset-change workshops without systemic change, or utopian solutions that ignore complexity.

---

# OUTPUT FORMAT RULES

[CRITICAL INSTRUCTION]: Your output MUST be Markdown, rendered directly (no wrapping code block). Follow these rules strictly:

1. **Format:** Use exclusively Markdown syntax.
2. **Hierarchy:** `#` for title, `##` for Opportunity, `###` for Solution.
3. **Lists:** `-` for first level, two-space indent per deeper level.
4. **Style:** `**text**` for bold, `*text*` for italic.
5. **Icons:** Use 🥇, 🥈, 🥉, ✨, 💡 in context.
6. **Minimum Opportunities:** Output MUST contain at least 3 opportunity sections.
7. **Justifications:** All justifications must be concise and follow the template format.

### Mandatory Output Template (Markdown)

[FIRST, GENERATE THIS PART]

## 🧭 Index of Opportunities and Solutions

- 🥇 ✨ OPPORTUNITY 1: [Title of Opportunity 1]
  - 🥇 ✨ SOLUTION 1.1: [Title of Solution 1.1]
  - 🥈 ✨ SOLUTION 1.2: [Title of Solution 1.2]
  - 🥉 ✨ SOLUTION 1.3: [Title of Solution 1.3]
  - ✨ SOLUTION 1.4: [Title of Solution 1.4]

- 🥈 💡 OPPORTUNITY 2: [Title of Opportunity 2]
  - 🥇 💡 SOLUTION 2.1: [Title of Solution 2.1]
  - ...

_(Continue for all opportunities)_

[THEN GENERATE THIS PART]

# 🗺️ Strategic Analysis and Solution Generation: [Main desired outcome inferred from input]

## 🥇 ✨ OPPORTUNITY 1: [Opportunity Name]
- **Future Leverage Potential:** *[Justification]*
- **New Use Case Potential:** *[Justification]*

### 🥇 ✨ SOLUTION 1.1: [Solution Name]
- **Suggested Time Appetite:** [2, 4, or 6 weeks] - *Justification based on impact vs. effort.*
- **Description and Initial Scope:** *[Description with explicit trade-offs: what is IN scope vs. OUT of scope]*
- **How It Works:** *[Minimal conceptual explanation of how the solution operates]*
- **Strategy:** [Strategy Name] (*[One-line strategy description]*) - *Detailed justification*
- **Main Value Areas:** *[List 1–3 areas, e.g., Reduces Effort, Increases Belonging]*
- **Future Leverage Potential:** *[Justification specific to this solution]*
- **New Use Case Potential:** *[Justification specific to this solution]*
- **Assumptions:**
  - The user wants [desirability assumption].
  - It is possible to build [technical viability assumption].
  - The solution is easier to use than [usability assumption].

(Repeat for at least 3 more solutions per opportunity)

## 🥈 💡 OPPORTUNITY 2: [Opportunity Name]
...

## 🥉 💡 OPPORTUNITY 3: [Opportunity Name]
...

---

```

## Error Handling

If the user input is too vague, ambiguous, or irrelevant, output:

## ⚠️ Analysis Impaired by Insufficient Input
- **Problem Identified:** The provided input is too vague or ambiguous for a complete strategic analysis.
- **Action Required:** Please provide a new input that more clearly describes:
  - The problem the user or company is facing.
  - The context in which the problem occurs.
  - The desired outcome or goal to be achieved.

## Examples

### Example: where to focus after a flat quarter

**Input:** "Growth stalled. Map where we should look."

**Steps:**
1. Collect required input (segments, pains, evidence); use the Evidence Policy when the ranking depends on external facts.
2. Generate the opportunity space (needs × segments).
3. Rank by evidence strength × strategic fit, not by excitement.

**Output:** Ranked opportunity map with the top 3 bets and why the rest wait.

## Edge Cases

### No evidence, only opinions
- Mark every node low-confidence; prescribe the cheapest evidence per node.
### Everything looks high-value
- Force trade-offs: appetite is fixed, so something must be cut.
### Map goes stale
- Re-run on a cadence; opportunities decay as markets move.

## Entry (mode detection)

When this skill loads, check for the stelow workflow marker:

```bash
if [ -n "$STELOW_WORKFLOW" ] && [ -n "$STELOW_STATE" ]; then
  echo "stelow: workflow mode (state=$STELOW_STATE)"
else
  echo "stelow: standalone mode (no STELOW_WORKFLOW marker)"
fi
```

In **standalone mode** (no marker), run the existing skill body unchanged.
In **workflow mode**, skip to `### Workflow slice` and emit a complete
`## Hand-off (workflow mode)` block at the end. See
`../stelow-workflow-entry/SKILL.md` for the full marker protocol.

## Hand-off (workflow mode)

```
stage          : triage
description    : Initial assessment. Determine if this is a valid request.
status         : <done|partial|blocked>
artifacts      : <paths created or modified>
next-candidate : select
gate           : none
rework-on      : (none)
```

Workflow mode: emit the above Hand-off block verbatim, then stop. The
router skill consumes the next-candidate field and calls
`scripts/stelow advance <next-candidate>` to move state forward.

### Workflow slice

Workflow mode for the **triage** stage. Standalone behavior lives in
the rest of this file (unchanged). Summary:

> Initial assessment. Determine if this is a valid request.

Primary actions (per stages.yaml): `read, write`. Run only the actions that
produce the artifacts promised in `## Hand-off`; skip anything that does
not advance the workflow.
