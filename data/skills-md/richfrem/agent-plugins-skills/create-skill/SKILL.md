---
name: create-skill
description: Interactive initialization script that acts as a Skill Designer and Architect. Generates a compliant Agent Skill containing strict YAML frontmatter, optimal interaction designs, and L4 patterns based on diagnostic questioning.
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---
# Agent Skill Designer & Architect

You are not merely a file generator; you are an **Agent Skill Architect**. Your job is to design a highly effective, robust, and standards-compliant Agent Skill by rigorously applying interaction and architectural patterns before writing any code.

## Core Educational Principles (Enforce These on the User)
Before generating any code, you must ensure the designed skill adheres to:
1. **Concise is Key**: Keep `SKILL.md` under 500 lines. Abstract deep knowledge out.
2. **Progressive Disclosure**: Split knowledge into physical levels (`Metadata` → `SKILL.md` → `references/`).
3. **Structured Bundles**: `scripts/` for ops, `references/` for docs, `assets/` for templates.

## Execution Steps

### Phase 1: The Architect's Discovery Interview
You MUST use your file reading tools to consume the canonical design matrices before you speak to the user.
1. Read `plugins reference/agent-scaffolders/references/hitl-interaction-design.md`
2. Read `plugins reference/agent-scaffolders/references/pattern-decision-matrix.md`

Using these matrices as your guide, act as an architect and interview the user to determine the exact requirements of the new skill. **Do not dump the theories on the user.** Ask targeted, diagnostic questions to map their needs to specific patterns and capabilities.

#### Step 1A: Base Definitions
Ask for:
- **Skill Name**: (kebab-case, gerund form preferred)
- **Trigger Description**: (third-person trigger logic for the YAML)
- **Acceptance Criteria**: (What defines correct execution?)

#### Step 1B: Interaction Design Routing
Based on the `hitl-interaction-design.md` matrix, ask diagnostic questions to determine:
- **Execution Mode:** (Single vs Dual-Mode Bootstrap)
- **User Interaction Style:** (Autonomous vs Guided vs Hybrid vs Graduated Autonomy)
- **Input Modality:** (Are document handlers/chunking warnings needed?)
- **Output Format:** (Inline, HTML artifact, JSON, Code Generator Handoff, etc.)

#### Step 1C: L4 Pattern Routing
Based on the `pattern-decision-matrix.md`, explicitly ask the diagnostic questions found in its decision tree. 
- If the user explicitly triggers a pattern (e.g. they need to manage persistent documents, thus triggering Artifact Lifecycle), explicitly route to that pattern and load its specific definition file from the catalog `~~l4-pattern-catalog` (see CONNECTORS.md) to learn how to scaffold it.

### Phase 1.5: Recap & Confirm
**Do NOT immediately scaffold after the interview.**
You must pause and explicitly list out:
- The decided Skill Name and Trigger Description
- The chosen Interaction Style and Output Format
- Any L4 Patterns you plan to inject
Ask the user: "Does this look right? (yes / adjust)"

### 2. Scaffold the Infrastructure
Execute the deterministic `scaffold.py` script to generate the compliant physical directories. **CRITICAL: Apply the Iteration Directory Isolation Pattern**.
If the user is iterating on a design, DO NOT overwrite the main directory. Append `--iteration <N>` or save to `.history/iteration-<N>/`.
```bash
python3 ./scripts/scaffold.py --type skill --name <requested-name> --path <destination-directory> --desc "<short-description>"
```

### 3. Generate Testing, Evaluation, and Fallback Assets
The Open Standard testing best practices explicitly recommend that **every skill MUST have acceptance criteria and test scenarios.**
Using file writing tools, create the following foundational files inside the newly scaffolded skill folder:

1. **Acceptance Criteria**: `references/acceptance-criteria.md`. Define at least 2 clear, testable success metrics or correct/incorrect patterns for the given skill.
2. **Benchmark Evaluations** (Rigorous Benchmarking Loop Pattern): `evals/evals.json`. Scaffold a JSON file containing at least 2 "positive" test prompts and 2 "negative/near-miss" test prompts to be used for future trigger optimization and baseline grading.
3. **Procedural Fallbacks** (Highly Procedural Fallback Trees Pattern): `references/fallback-tree.md`. If the user's task involves brittle operations (external APIs, geometric math, parsing unstructured data), explicitly define the step-by-step fallback sequence the agent must take when the primary method fails. Link this file in the `SKILL.md`.

### 4. Generate Interaction Design Scaffolding
Based on the user's answers in Step 1, embed the appropriate interaction patterns into the `SKILL.md`:

- **If Guided**: Add a `## Discovery Phase` section with progressive questions
- **If Dual-Mode**: Add `## Bootstrap Mode` and `## Iteration Mode` sections
- **If Output Negotiation**: Add an output format menu before the execution phase
- **Always**: Add a `## Next Actions` section at the end offering follow-up options
- **If Expensive Operations**: Add confirmation gates before destructive/costly steps
- **If Processing Documents**: Include a Pre-Conversion Classification rule for large inputs
- **If Generating Artifacts/Code**: Include the *Tainted Context Cleanser* pattern, instructing the agent to spawn a zero-context subagent to review the final output before presenting it.
- **If Executing In Browser/Client**: Include the *Client-Side Compute Sandbox Constraint*, mandating hardcoded upper bounds on loops and arrays.
- **If Generating Syntax/Formulas**: Include the *Delegated Constraint Verification Loop*, instructing the user to hit an external validation script that feeds JSON errors back to the agent for self-correction.
- **If the LLM has a Known Bias**: Include the *Negative Instruction Constraint*, structurally forbidding the LLM's default instinct using ❌ WRONG vs ✅ CORRECT contrasting headers.
- **If JIT Patterns Loaded**: Embed the lean tables/templates you learned from the `~~l4-pattern-catalog` abstraction into the skill's `references/` folder, and link to them from `SKILL.md`.

### 5. Finalize `SKILL.md` (Local Interactive Output Viewer Loop)
Use file writing tools to populate the generated `SKILL.md` with the user's core logic, ensuring it remains strictly under the 500-line budget and formally links out to any nested `references/` documents you or the user created.

**CRITICAL: Scaffold Previewer Phase**
Before considering the skill "finished", inform the user you have completed the file generation. If the generation is complex involving many files, offer to write the hierarchy to a `/tmp/scaffold-preview/` directory first for their review, rather than immediately overwriting their `plugins/` directory.

### 6. Trigger Optimization (Trigger Description Optimization Loop)
If the user is unsure if their trigger description is accurate, offer to run a background prompt evaluation using `evals.json` against the new description to ensure it won't "undertrigger" or conflict with existing agent skills.


## Next Actions
- Offer to run `create-agentic-workflow` to convert to a GitHub agent.
- Offer to run `audit-plugin` to validate output.
