---
name: apex-skill-forge
description: "Self-replicating meta-skill to forge Cathedral-tier Antigravity agent skills. Triggers: create a skill, forge skill, build agent context"
version: "4.2.0"
archetype: "transformer"
platform: "google-antigravity"
license: "Proprietary - APEX Business Systems Ltd."
---

# APEX Antigravity Skill Forge

**Input**: Vague/broken user request for a new capability.  
**Output**: A strictly formatted, zero-drift `skill.md` file saved directly to the Antigravity agent directory.  
**Success**: Generated file contains YAML frontmatter, contract-first I/O, decision trees, working examples, and a troubleshooting table.  
**Fails When**: Generating prose walls, violating the "Show Over Tell" Iron Law, missing YAML frontmatter, or failing to lock the explicit failure modes.

---

## 🏛️ APEX PROPRIETARY LICENSE

**Copyright © 2026 APEX Business Systems Ltd. All Rights Reserved.**
This software is proprietary and confidential. Internal use only. Public distribution, unauthorized modification, or redistribution is strictly prohibited. 

---

## Decision Tree

**Calculate Ambiguity Level:**
*(missing_verbs×0.25) + (missing_domain×0.30) + (missing_output×0.20) + (vagueness×0.15)*
├─ Ambiguity > 30% → Use "Clarification Protocol"
└─ Ambiguity ≤ 30% → Use "Direct Forge Protocol"

---

## Direct Forge Protocol

**Failures to avoid**:
- ❌ Explaining how the skill works → Violates "Show Over Tell". Code examples only.
- ❌ Writing paragraphs → Violates "Trees Over Prose". Use decision trees exclusively.
- ❌ Outputting a `.txt` file instead of `skill.md` → Breaks Antigravity lazy-loading infrastructure.

**Correct approach**:
1. **Signal Extraction**: Parse nouns, verbs, domain markers, and implied goals.
2. **Contract Synthesis**: Lock Input, Output, Success metrics, and explicit Fails before writing logic.
3. **Archetype Assignment**: Classify as Workflow, Toolkit, Domain, Orchestrator, Transformer, or Guardian.
4. **Forge**: Generate exactly one Markdown code block containing the finalized skill.
5. **Deploy**: Save directly to `[Project-Root]/.agent/skills/[skill-name]/skill.md`.

---

## Clarification Protocol

**Failures to avoid**:
- ❌ Asking more than 2 questions → Violates Lazy-CEO minimal friction protocol.
- ❌ Open-ended inquiries → Increases cognitive load and drift potential.

**Correct approach**:
Prompt user definitively: "Context required to forge skill. 1. What is the precise input data format? 2. What is the explicit failure condition?"

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Agent ignores the generated skill | Missing YAML frontmatter | Ensure `---` encapsulates the name, description, and license at the very top of the file. |
| Context token bloat | Skill exceeds 200 lines | Ruthlessly refactor prose into strict decision trees and bulleted lists. |
| Hallucinated capabilities | Missing Contract Synthesis | Force the agent to re-run Phase 3 and explicitly define the "Fails When" conditions. |
| Unlicensed replication | Missing headers | Ensure APEX Copyright block is present at compilation. |