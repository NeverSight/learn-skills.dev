---
name: skill-builder
description: Interactive guide for creating new agent skills from scratch. Use this skill when the user wants to create a skill, write a SKILL.md, package a skill folder, or convert an existing workflow into a reusable skill. Also trigger when the user mentions "create skill", "new skill", "SKILL.md", "teach the agent", or wants to standardize a repeatable process into a skill.
---

# Skill Builder

Step-by-step guide for creating high-quality agent skills based on the open Agent Skills standard.

## What is a skill

A skill is a portable folder containing instructions that teach an AI agent how to handle specific tasks or workflows. Instead of re-explaining preferences, processes, and domain expertise in every session, a skill captures that knowledge once and applies it consistently across interactions and platforms.

A skill contains:
- `SKILL.md` (required): instructions in Markdown with YAML frontmatter
- `scripts/` (optional): executable code (Javascript, Bash, etc.)
- `references/` (optional): documentation loaded as needed
- `assets/` (optional): templates, fonts, icons used in output

### Core design principles

**Progressive disclosure:** skills use a three-level loading system to minimize token usage while maintaining specialized expertise.
- Level 1 (YAML frontmatter): always loaded. Tells the agent when the skill is relevant.
- Level 2 (SKILL.md body): loaded when the agent determines the skill applies. Contains full instructions.
- Level 3 (Linked files): additional resources the agent navigates only as needed.

**Composability:** an agent can load multiple skills simultaneously. Your skill should work well alongside others, not assume it's the only capability available.

**Portability:** skills are an open standard. A well-built skill works across any platform that supports the standard, provided the environment meets any dependencies.

## Creation process

### Step 1: Define use cases

Before writing anything, identify 2-3 concrete use cases. For each one:

```
Use Case: [name]
Trigger: [what the user says or does]
Steps: [sequence of actions]
Result: [what gets produced at the end]
```

Key questions:
1. What should the agent be able to do with this skill?
2. When should it trigger? (phrases, contexts)
3. What's the expected output format?
4. Does it need external tools (MCP servers, APIs) or only built-in capabilities?

Common skill categories:

**Document & asset creation** — generating consistent, high-quality outputs like documents, presentations, code, designs. Key techniques: embedded style guides, template structures, quality checklists.

**Workflow automation** — multi-step processes that benefit from consistent methodology. Key techniques: step-by-step workflows with validation gates, iterative refinement loops.

**MCP enhancement** — workflow guidance layered on top of MCP server tool access. Key techniques: coordinating multiple MCP calls in sequence, embedding domain expertise, error handling for common MCP issues.

### Step 2: Design the folder structure

```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional - executable code
├── references/       # Optional - additional documentation
└── assets/           # Optional - templates, resources
```

Critical rules:
- The file MUST be named exactly `SKILL.md` (case-sensitive). No variations (SKILL.MD, skill.md, etc.)
- The folder uses kebab-case: `my-cool-skill` ✅ | `My Skill` ❌ | `my_skill` ❌
- Do NOT include `README.md` inside the skill folder. All documentation goes in SKILL.md or `references/`
- Do NOT use reserved platform names in the skill name

### Step 3: Write the YAML frontmatter

The frontmatter is how the agent decides whether to load your skill. This is the most important part.

```yaml
---
name: name-in-kebab-case
description: What the skill does and when to use it. Include specific trigger phrases.
---
```

**`name` field** (required):
- Kebab-case only, no spaces or capitals
- Should match the folder name

**`description` field** (required, max 1024 characters):
- MUST include WHAT it does + WHEN to use it
- Include specific phrases users would actually say
- Mention file types if applicable
- No XML tags (< >)
- Lean slightly "pushy" — agents tend to under-trigger, so a description that's assertive about when to activate performs better than one that's conservative

Good description examples:

```yaml
# Good - specific and actionable
description: Analyzes Figma design files and generates developer handoff documentation. Use when the user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

# Good - includes trigger phrases
description: Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when the user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".

# Good - clear value proposition with negative trigger
description: Advanced data analysis for CSV files. Use for statistical modeling, regression, clustering. Do NOT use for simple data exploration (use data-viz skill instead).
```

Bad description examples:

```yaml
# Too vague
description: Helps with projects.

# Missing triggers
description: Creates sophisticated multi-page documentation systems.

# Too technical, no user triggers
description: Implements the Project entity model with hierarchical relationships.
```

**Optional fields:**
- `license`: MIT, Apache-2.0, etc.
- `compatibility`: environment requirements, intended platforms, required system packages (1-500 chars)
- `allowed-tools`: restrict which tools the skill can invoke
- `metadata`: custom key-value pairs

```yaml
metadata:
  author: Your Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
```

**Security restrictions:**
- No XML angle brackets (< >) in frontmatter — frontmatter appears in the agent's system prompt and could inject instructions
- No code execution in YAML (safe YAML parsing is used)

### Step 4: Write the instructions

After the frontmatter, write the instructions in Markdown. Recommended structure:

```markdown
---
name: my-skill
description: [...]
---

# Skill Name

# Instructions

### Step 1: [First step]
Clear explanation of what happens.

Example:
\```bash
node scripts/fetch_data.js --project-id PROJECT_ID
\```
Expected output: [describe what success looks like]

### Step 2: [Next step]
...

## Examples

**Example 1: [common scenario]**
User says: "..."
Actions: ...
Result: ...

## Troubleshooting

**Error: [common message]**
Cause: [why it happens]
Solution: [how to fix]
```

### Best practices for instructions

**Be specific and actionable:**
```markdown
# ✅ Good
Run `bun run scripts/validate.ts --input {filename}` to check data format.
If validation fails, common issues include:
- Missing required fields (add them to the CSV)
- Invalid date formats (use YYYY-MM-DD)

# ❌ Bad
Validate the data before proceeding.
```

**Include error handling** with concrete resolution steps. For MCP-dependent skills, include connection verification, authentication checks, and fallback instructions.

**Use progressive disclosure:** keep SKILL.md focused on core instructions (ideally <500 lines). Move detailed documentation to `references/` and link to it. For large reference files (>300 lines), include a table of contents.

**Explain the why:** instead of rigid MUSTs, explain the reasoning behind each instruction. Current LLMs are smart and respond better to understanding rationale than to authoritarian commands. If you find yourself writing ALWAYS or NEVER in all caps, reframe and explain the reasoning so the model understands why.

**Use imperative form:** "Run the script" instead of "The script should be run".

**Define output formats explicitly:**
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Include examples with input/output pairs:**
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

**For critical validations, bundle scripts:** code is deterministic; language interpretation isn't. If a check can be automated, write a script in `scripts/` rather than relying on the agent to interpret instructions correctly every time.

### Step 5: Testing

Three testing areas:

**1. Triggering tests** — does the skill load at the right times?
- ✅ Triggers on obvious tasks
- ✅ Triggers on paraphrased requests
- ❌ Does NOT trigger on unrelated topics

Quick debugging: ask the agent "When would you use the [skill name] skill?" — it will quote the description back and you can adjust based on what's missing.

**2. Functional tests** — does the skill produce correct outputs?
- Valid outputs generated
- API/MCP calls succeed
- Error handling works
- Edge cases covered

**3. Performance comparison** — does the skill improve results vs baseline?
- Measure back-and-forth messages needed
- Measure failed API calls requiring retry
- Measure tokens consumed
- Compare with-skill vs without-skill

Recommended approach: iterate on a single challenging task until the agent succeeds, then extract the winning approach into the skill. This provides faster signal than broad testing. Once you have a working foundation, expand to multiple test cases for coverage.

### Step 6: Iterate

**Under-triggering signals:**
- Skill doesn't load when it should
- Users manually enabling it
- Solution: add more keywords, trigger phrases, and nuance to the description

**Over-triggering signals:**
- Skill loads for irrelevant queries
- Users disabling it
- Solution: add negative triggers, narrow the scope, be more specific

**Execution issues:**
- Inconsistent results across sessions
- API call failures
- Users needing to correct the agent
- Solution: improve instructions, add error handling, look for steps that should be scripted

## Common patterns

### Pattern 1: Sequential workflow orchestration
For multi-step processes in a specific order. Explicit step ordering, dependencies between steps, validation at each stage, rollback instructions for failures.

```markdown
### Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company

### Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification

### Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)
```

### Pattern 2: Multi-MCP coordination
For workflows spanning multiple services (e.g., Figma → Drive → Linear → Slack). Clear phase separation, data passing between MCPs, validation before advancing, centralized error handling.

### Pattern 3: Iterative refinement
For when output quality improves with iteration. Initial draft → quality check via validation script → refinement loop → finalization. Include explicit quality criteria and know when to stop.

### Pattern 4: Context-aware tool selection
For when the same outcome is achieved with different tools depending on context. Clear decision tree (e.g., large files → cloud storage, collaborative docs → Notion, code → GitHub), fallback options, transparency about choices.

### Pattern 5: Domain-specific intelligence
For when the skill adds specialized knowledge beyond tool access. Domain expertise embedded in logic, compliance/validation before action, comprehensive audit trail, clear governance rules.

## Distribution

**Individual installation:**
1. Zip the skill folder
2. Upload via the platform's skill settings
3. Or place in the platform's skills directory

**Organization deployment:**
- Platform admins can deploy skills workspace-wide
- Enables automatic updates and centralized management

**Public distribution:**
1. Host on GitHub with a clear README at repo level (NOT inside the skill folder)
2. Include example usage and screenshots
3. If paired with an MCP server, document both together and explain the combined value
4. Provide a quick-start installation guide

**Positioning tip:** focus on outcomes, not features. "Set up complete project workspaces in seconds instead of 30 minutes of manual setup" beats "A folder containing YAML frontmatter and Markdown instructions."

## Final checklist

Before starting:
- [ ] 2-3 concrete use cases identified
- [ ] Required tools identified (built-in, MCP, or API)
- [ ] Folder structure planned

During development:
- [ ] Folder named in kebab-case
- [ ] `SKILL.md` file exists (exact case-sensitive spelling)
- [ ] YAML frontmatter has `---` delimiters
- [ ] `name` field: kebab-case, no spaces, no capitals
- [ ] `description` includes WHAT and WHEN
- [ ] No XML tags (< >) in frontmatter
- [ ] Instructions are clear and actionable
- [ ] Error handling included
- [ ] Examples provided
- [ ] References clearly linked

Before upload:
- [ ] Tested triggering on obvious tasks
- [ ] Tested triggering on paraphrased requests
- [ ] Verified doesn't trigger on unrelated topics
- [ ] Functional tests pass
- [ ] Tool/MCP integration works (if applicable)

After upload:
- [ ] Tested in real conversations
- [ ] Monitored for under/over-triggering
- [ ] Collected user feedback
- [ ] Iterated on description and instructions