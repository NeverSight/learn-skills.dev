---
name: plan-based-skill-builder
description: Builds Cursor skills from plan documents by analyzing workflows, extracting key instructions, and creating structured skill files. Use when creating skills from restart plans, deployment plans, prioritization plans, retest plans, or any structured plan documents.
---

# Plan-Based Skill Builder

## Quick Start

When building a skill from a plan document:

1. Analyze the plan document structure and purpose
2. Extract workflows, checklists, and key instructions
3. Identify trigger scenarios and use cases
4. Create a structured SKILL.md following best practices
5. Generate supporting files if needed (reference.md, examples.md)

## Plan Document Types

### Restart Plans
- Focus on restart procedures, verification steps, health checks
- Extract restart workflows, validation commands, troubleshooting steps
- Create skills for restart operations, system recovery, health monitoring

### Deployment Plans
- Focus on deployment steps, configuration, validation
- Extract deployment workflows, configuration templates, rollback procedures
- Create skills for deployment operations, configuration management

### Prioritization Plans
- Focus on ranking, scoring, decision-making frameworks
- Extract scoring rubrics, ranking algorithms, decision criteria
- Create skills for prioritization, ranking, selection workflows

### Retest Plans
- Focus on testing procedures, validation steps, success criteria
- Extract test workflows, validation commands, acceptance criteria
- Create skills for testing, validation, quality assurance

### Migration Plans
- Focus on migration steps, data transformation, validation
- Extract migration workflows, transformation rules, verification steps
- Create skills for migration operations, data transformation

## Skill Creation Workflow

### Step 1: Analyze Plan Document

Read the plan document and identify:

**Purpose & Scope:**
- What is the main goal of this plan?
- What domain/area does it cover?
- What problems does it solve?

**Key Workflows:**
- What are the main steps or procedures?
- Are there checklists or sequential processes?
- What decision points exist?

**Trigger Scenarios:**
- When would someone need this skill?
- What keywords or situations trigger its use?
- What related tasks would benefit from this?

**Key Instructions:**
- What specific commands or procedures are documented?
- What patterns or templates are provided?
- What validation or verification steps exist?

**Supporting Information:**
- Are there examples or reference materials?
- Are there scripts or utilities mentioned?
- Are there integration points with other systems?

### Step 2: Extract Skill Components

**Name:**
- Use lowercase, hyphens, max 64 chars
- Reflect the plan's purpose (e.g., `restart-operations`, `deployment-workflow`)
- Be specific and descriptive

**Description:**
- Write in third person
- Include WHAT (capabilities) and WHEN (trigger scenarios)
- Include key terms for discovery
- Max 1024 chars

**Instructions:**
- Convert plan steps into actionable instructions
- Preserve workflows and checklists
- Include command examples and code snippets
- Add validation steps and error handling

**Examples:**
- Extract concrete examples from the plan
- Include command-line examples
- Show expected outputs or results

**Integration Points:**
- Identify related skills or systems
- Document dependencies
- Reference related workflows

### Step 3: Structure the Skill

Follow the standard SKILL.md structure:

```markdown
---
name: skill-name
description: [Third-person description with triggers]
---

# Skill Name

## Quick Start
[Essential instructions]

## Workflow
[Step-by-step process]

## Key Components
[Important concepts, commands, patterns]

## Examples
[Concrete examples]

## Integration Points
[Related skills, systems, workflows]

## Troubleshooting
[Common issues and solutions]
```

### Step 4: Create Supporting Files (If Needed)

**reference.md:**
- Detailed API documentation
- Complete command reference
- Advanced configurations

**examples.md:**
- Extended examples
- Use case scenarios
- Edge cases

**scripts/ (if needed):**
- Utility scripts mentioned in plan
- Validation scripts
- Helper tools

## Plan Analysis Patterns

### Restart Plan Pattern

**Common Sections:**
- Restart procedures (stop → wait → start)
- Health checks and verification
- Troubleshooting steps
- Rollback procedures

**Skill Extraction:**
```markdown
## Restart Workflow

1. Stop services: [commands]
2. Wait for cleanup: [duration]
3. Start services: [commands]
4. Verify health: [checks]
5. Validate functionality: [tests]
```

### Deployment Plan Pattern

**Common Sections:**
- Pre-deployment checks
- Deployment steps
- Post-deployment validation
- Rollback procedures

**Skill Extraction:**
```markdown
## Deployment Process

### Pre-Deployment
- [ ] Checklist item 1
- [ ] Checklist item 2

### Deployment
1. Step 1: [command]
2. Step 2: [command]

### Post-Deployment
- Verify: [check]
- Validate: [test]
```

### Prioritization Plan Pattern

**Common Sections:**
- Scoring framework
- Ranking algorithm
- Decision criteria
- Action recommendations

**Skill Extraction:**
```markdown
## Scoring Framework

### Factor 1: [Name]
- **5**: [Criteria]
- **4**: [Criteria]
- **3**: [Criteria]

### Ranking Process
1. Score each item
2. Calculate composite
3. Rank by score
4. Categorize by action
```

## Example: Building from Restart Plan

**Input Plan Document:**
```markdown
# System Restart Plan

## Restart Procedure
1. Stop API: `kill -TERM <PID>`
2. Wait 10 seconds
3. Start API: `make start-paper`
4. Verify: `curl :8000/ready`
```

**Generated Skill:**
```markdown
---
name: system-restart
description: Restart trading systems with proper sequencing and health verification. Use when restarting APIs, services, or when system recovery is needed.
---

# System Restart

## Quick Start

Restart sequence:
1. Stop services gracefully
2. Wait for cleanup
3. Start services
4. Verify health

## Restart Workflow

### Step 1: Stop Services
```bash
# Find and stop API
lsof -nP -iTCP:8000 | awk '/LISTEN/ {print $2}' | xargs kill -TERM
```

### Step 2: Wait for Cleanup
```bash
sleep 10  # Allow graceful shutdown
```

### Step 3: Start Services
```bash
make start-paper  # or make live
```

### Step 4: Verify Health
```bash
curl :8000/ready | jq  # Should return 200
curl :8000/metrics | grep '^trader_is_leader'  # Should be 1
```
```

## Best Practices

### 1. Preserve Plan Structure
- Keep workflows intact
- Maintain checklists
- Preserve command sequences

### 2. Enhance with Context
- Add error handling not in plan
- Include troubleshooting steps
- Add validation checks

### 3. Make It Discoverable
- Include trigger keywords in description
- Add related terms
- Reference common use cases

### 4. Keep It Concise
- Extract essential information
- Remove redundant explanations
- Focus on actionable content

### 5. Add Integration Points
- Reference related skills
- Link to documentation
- Connect to related workflows

## Common Extraction Patterns

### Commands → Instructions
```markdown
# Plan:
```bash
make start-paper
```

# Skill:
## Start System
```bash
make start-paper
```
Wait 10 seconds, then verify with `curl :8000/ready`
```

### Checklists → Workflows
```markdown
# Plan:
- [ ] Step 1
- [ ] Step 2

# Skill:
## Deployment Checklist
1. Step 1: [details]
2. Step 2: [details]
```

### Procedures → Step-by-Step
```markdown
# Plan:
1. Do X
2. Then Y
3. Finally Z

# Skill:
## Procedure
### Step 1: Do X
[Details and commands]

### Step 2: Then Y
[Details and commands]

### Step 3: Finally Z
[Details and commands]
```

## Validation Checklist

After creating a skill from a plan, verify:

- [ ] Skill name is lowercase, hyphenated, max 64 chars
- [ ] Description is third-person, includes triggers
- [ ] Description includes WHAT and WHEN
- [ ] Instructions are actionable and clear
- [ ] Workflows preserve plan structure
- [ ] Examples are concrete and useful
- [ ] Integration points are documented
- [ ] SKILL.md is under 500 lines
- [ ] Supporting files are one level deep
- [ ] Commands are tested and accurate

## Related Resources

- Skill creation guide: `create-skill` skill
- Plan documents: `*PLAN*.md` files in root
- Existing skills: `.cursor/skills/` directory
- Agent files: `.cursor/agents/` directory

## Troubleshooting

### Plan Too Vague
- Look for implicit workflows
- Extract common patterns
- Add general guidance

### Plan Too Specific
- Generalize to broader use cases
- Extract reusable patterns
- Add configuration options

### Missing Information
- Infer from context
- Add placeholder sections
- Document assumptions

### Conflicting Information
- Use most recent or authoritative source
- Document conflicts
- Provide alternatives

Always create skills that are discoverable, actionable, and aligned with the plan's intent while following Cursor skill best practices.
