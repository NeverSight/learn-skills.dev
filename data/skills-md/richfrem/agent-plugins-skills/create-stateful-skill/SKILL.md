---
name: create-stateful-skill
description: Interactive initialization script that generates an advanced Agent Skill utilizing L4 State Management, Lifecycle Artifacts, Tone Configuration, and Chained Commands. Use when authoring complex, persistent workflows.
disable-model-invocation: false
tier: 1
allowed-tools: Bash, Read, Write
---
# Stateful Skill Scaffold Generator

## Overview
You are tasked with generating a new **Stateful Agent Skill**. 
While standard skills (via `create-skill`) execute isolated tasks, stateful skills possess deeper systemic awareness: they manage artifact lifecycles over time, configure multi-dimensional tone, propagate epistemic confidence hierarchies, and link to other skills via Chained Commands.

These patterns were extracted from the L4 Anthropic Customer Support and Legal ecosystems.

## Execution Steps

### 1. Requirements & L4 Pattern Discovery
Use a guided discovery interview. First, get the standard metadata (Skill Name, Description).
Then, progressively ask the user which L4 State/Lifecycle templates they need injected:

**Q1. Epistemic Trust (Tiered Authority)**
Does the agent need a Tiered Source Authority model to propagate a Confidence Score (High/Med/Low) into its outputs based on the evidentiary hierarchy?

**Q2. Artifact Lifecycle Management**
Does this skill create or maintain persistent outputs (e.g., KB articles, tickets)? If so, we will inject the Artifact Lifecycle State Machine (Draft → Published → Needs Update) and a Scheduled Maintenance Cadence.

**Q3. Multi-Dimensional Tone Configuration**
Does this skill draft external communications? If so, we will inject the Tone Configuration matrix (Situation Type × Audience Segment = Tone Label).

**Q4. Escalation & Quality Gates**
Does this skill require an Escalation Trigger Taxonomy (Stop, Alert, Explain, Recommend) or a Business Impact Quantification Protocol before proceeding?

**Q5. Workflow Navigation (Chained Commands)**
What commands logically follow this output? We will inject an "Offer Next Steps" block to chain this node to other skills.

### Phase 1.5: Recap & Confirm
**Do NOT immediately scaffold after the interview.**
You must pause and explicitly list out:
- The decided Skill Name and Description
- Which of the 5 L4 State/Lifecycle templates you plan to inject
Ask the user: "Does this look right? (yes / adjust)"

### 2. Scaffold the Infrastructure (Preventing Context Bloat)
Execute the deterministic `scaffold.py` script to generate the physical directories:
```bash
python3 ./scripts/scaffold.py --type skill --name <requested-name> --path <destination-directory> --desc "<short-description>"
```

### 3. Generate Lean Pattern References (Lazy-Loading)
**CRITICAL: Do NOT bloat the generated skill with massive definitions of these patterns.** 
Instead of writing out the entire theory of Escalation Taxonomies or Lifecycle State Machines in every new skill, you must practice **Progressive Disclosure**:
- For each selected L4 pattern in Step 1, create a LEAN file in `references/` (e.g., `references/tone-matrix.md`). Load its specific definition file from the catalog `~~l4-pattern-catalog` (see CONNECTORS.md) to learn how to scaffold it.
- This file should ONLY contain the domain-specific tables (the actual matrix values for this specific skill).
- Do not explain *how* the pattern works; the central `pattern-catalog.md` already defines the mechanics. Just provide the blank or filled templates for this specific workflow.

### 4. Finalize the `SKILL.md` (Pointers Only)
Write the final `SKILL.md`. Ensure it:
1. Keeps the primary instructions concise (<300 lines).
2. Uses Markdown links (e.g., `[See Escalation Rules](references/escalation-taxonomy.md)`) so the LLM only loads the context when needed.
3. Includes the **Chained Commands** (Offer Next Steps) block at the bottom.
4. Includes the mandatory **Source Transparency Declaration**.


## Next Actions
- Offer to run `audit-plugin` to validate the generated artifacts.
