---
name: create-team
description: >
  Create a new team composition file following the agent-almanac
  team template and registry conventions. Covers team purpose definition,
  member selection, coordination pattern choice, task decomposition
  design, machine-readable configuration block, registry integration,
  and README automation. Use when defining a multi-agent workflow,
  composing agents for a complex review process, or creating a
  coordinated group for recurring collaborative tasks.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: general
  complexity: intermediate
  language: multi
  tags: meta, team, creation, composition, coordination
---

# Create a New Team

Define a multi-agent team composition that coordinates two or more agents to accomplish tasks requiring multiple perspectives, specialties, or phases. The resulting team file integrates with the teams registry and can be activated in Claude Code by name.

## When to Use

- A task requires multiple perspectives that a single agent cannot provide (e.g., code review plus security audit plus architecture review)
- You need a recurring collaborative workflow with consistent role assignments and handoff patterns
- An existing agent composition is being used repeatedly and should be formalized
- A complex process naturally decomposes into phases or specialties handled by different agents
- You want to define a coordinated group for sprint-based, pipeline-based, or parallel work

## Inputs

- **Required**: Team name (lowercase kebab-case, e.g., `data-pipeline-review`)
- **Required**: Team purpose (one paragraph describing what problem requires multiple agents)
- **Required**: Lead agent (must exist in `agents/_registry.yml`)
- **Optional**: Coordination pattern (default: hub-and-spoke). One of: `hub-and-spoke`, `sequential`, `parallel`, `timeboxed`, `adaptive`
- **Optional**: Number of members (default: 3-4; recommended range: 2-5)
- **Optional**: Source material (existing workflow, runbook, or ad-hoc team composition to formalize)

## Procedure

### Step 1: Define Team Purpose

Articulate what problem requires multiple agents working together. A valid team purpose must answer:

1. **What outcome** does this team deliver? (e.g., a comprehensive review report, a deployed application, a sprint increment)
2. **Why can't a single agent do this?** Identify at least two distinct specialties or perspectives required.
3. **When should this team be activated?** Define the trigger conditions.

Write the purpose as one paragraph that a human or agent can read to decide whether to activate this team.

**Expected:** A clear paragraph explaining the team's value proposition, with at least two distinct specialties identified.

**On failure:** If you cannot identify two distinct specialties, the task likely does not need a team. Use a single agent with multiple skills instead.

### Step 2: Select Lead Agent

The lead agent orchestrates the team. Choose an agent from `agents/_registry.yml` that:

- Has domain expertise relevant to the team's primary output
- Can decompose incoming requests into subtasks for other members
- Can synthesize results from multiple reviewers into a coherent deliverable

```bash
# List all available agents
grep "^  - id:" agents/_registry.yml
```

The lead must also appear as a member in the team composition (the lead is always a member).

**Expected:** One agent selected as lead, confirmed to exist in the agents registry.

**On failure:** If no existing agent fits the lead role, create one first using the `create-agent` skill (or `agents/_template.md` manually). Do not create a team with a lead that does not exist as an agent definition.

### Step 3: Select Member Agents

Choose 2-5 members (including the lead) with clear, non-overlapping responsibilities. For each member, define:

- **id**: Agent name from the agents registry
- **role**: A short title (e.g., "Quality Reviewer", "Security Auditor", "Architecture Reviewer")
- **responsibilities**: One sentence describing what this member does that no other member does

```bash
# Verify each candidate agent exists
grep "id: agent-name-here" agents/_registry.yml
```

Validate non-overlap: no two members should have the same primary responsibility. If responsibilities overlap, either merge the roles or sharpen the boundaries.

**Expected:** 2-5 members selected, each with a unique role and clear responsibilities, all confirmed in the agents registry.

**On failure:** If a needed agent does not exist, create it first. If responsibilities overlap between two members, rewrite them to clarify boundaries or remove one member.

### Step 4: Choose Coordination Pattern

Select the pattern that best fits the team's workflow. The five patterns and their use cases:

| Pattern | When to Use | Example Teams |
|---------|-------------|---------------|
| **hub-and-spoke** | Lead distributes tasks, collects results, synthesizes. Best for review and audit workflows. | r-package-review, gxp-compliance-validation, ml-data-science-review |
| **sequential** | Each agent builds on the previous agent's output. Best for pipelines and staged workflows. | fullstack-web-dev, tending |
| **parallel** | All agents work simultaneously on independent subtasks. Best when subtasks have no dependencies. | devops-platform-engineering |
| **timeboxed** | Work organized into fixed-length iterations. Best for ongoing project work with a backlog. | scrum-team |
| **adaptive** | Team self-organizes based on the task. Best for unknown or highly variable tasks. | opaque-team |

**Decision guide:**
- If the lead must see all results before producing output: **hub-and-spoke**
- If agent B needs agent A's output to start: **sequential**
- If all agents can work without seeing each other's output: **parallel**
- If work spans multiple iterations with planning ceremonies: **timeboxed**
- If you cannot predict the task structure in advance: **adaptive**

**Expected:** One coordination pattern selected with a clear rationale for the choice.

**On failure:** If unsure, default to hub-and-spoke. It is the most common pattern and works for most review and analysis workflows.

### Step 5: Design Task Decomposition

Define how a typical incoming request gets split across team members. Structure this as phases:

1. **Setup phase**: What the lead does to analyze the request and create tasks
2. **Execution phase**: What each member works on (in parallel, in sequence, or per-sprint depending on coordination pattern)
3. **Synthesis phase**: How results are collected and the final deliverable is produced

For each member, list 3-5 concrete tasks they would perform on a typical request. These tasks appear in both the "Task Decomposition" prose section and the CONFIG block's `tasks` list.

**Expected:** A phase-structured decomposition with concrete tasks per member, matching the chosen coordination pattern.

**On failure:** If tasks are too vague (e.g., "reviews things"), make them specific (e.g., "reviews code style against tidyverse style guide, checks test coverage, evaluates error message quality").

### Step 6: Write the Team File

Copy the template and fill in all sections:

```bash
cp teams/_template.md teams/<team-name>.md
```

Fill in the following sections in order:

1. **YAML frontmatter**: `name`, `description`, `lead`, `version` ("1.0.0"), `author`, `created`, `updated`, `tags`, `coordination`, `members[]` (each with id, role, responsibilities)
2. **Title**: `# Team Name` (human-readable, title case)
3. **Introduction**: One paragraph summary
4. **Purpose**: Why this team exists, what specialties it combines
5. **Team Composition**: Table with Member, Agent, Role, Focus Areas columns
6. **Coordination Pattern**: Prose description plus ASCII diagram of the flow
7. **Task Decomposition**: Phased breakdown with concrete tasks per member
8. **Configuration**: Machine-readable CONFIG block (see Step 7)
9. **Usage Scenarios**: 2-3 concrete scenarios with example user prompts
10. **Limitations**: 3-5 known constraints
11. **See Also**: Links to member agent files and related skills/teams

**Expected:** A complete team file with all sections filled in, no placeholder text remaining from the template.

**On failure:** Compare against an existing team file (e.g., `teams/r-package-review.md`) to verify structure. Search for template placeholder strings like "your-team-name" or "another-agent" to find unfilled sections.

### Step 7: Write the CONFIG Block

The CONFIG block between `<!-- CONFIG:START -->` and `<!-- CONFIG:END -->` markers provides machine-readable YAML for tooling. Structure it as follows:

    <!-- CONFIG:START -->
    ```yaml
    team:
      name: <team-name>
      lead: <lead-agent-id>
      coordination: <pattern>
      members:
        - agent: <agent-id>
          role: <role-title>
          subagent_type: <agent-id>  # Claude Code subagent type for spawning
        # ... repeat for each member
      tasks:
        - name: <task-name>
          assignee: <agent-id>
          description: <one-line description>
        # ... repeat for each task
        - name: synthesize-report  # final task if hub-and-spoke
          assignee: <lead-agent-id>
          description: <synthesis description>
          blocked_by: [<prior-task-names>]  # for dependency ordering
    ```
    <!-- CONFIG:END -->

The `subagent_type` field maps to Claude Code agent types. For agents defined in `.claude/agents/`, use the agent id as the subagent_type. Use `blocked_by` to express task dependencies (e.g., synthesis is blocked by all review tasks).

**Expected:** CONFIG block is valid YAML, all agents match those in the frontmatter members list, and task dependencies form a valid DAG (no cycles).

**On failure:** Validate YAML syntax. Verify that every `assignee` in the tasks list matches an `agent` in the members list. Check that `blocked_by` references only task names defined earlier in the list.

### Step 8: Add to Registry

Edit `teams/_registry.yml` to add the new team:

```yaml
- id: <team-name>
  path: <team-name>.md
  lead: <lead-agent-id>
  members: [<agent-id-1>, <agent-id-2>, ...]
  coordination: <pattern>
  description: <one-line description matching frontmatter>
```

Update the `total_teams` count at the top of the registry (currently 8; it becomes 9 after adding one team).

```bash
# Verify the entry was added
grep "id: <team-name>" teams/_registry.yml
```

**Expected:** New entry appears in the registry, `total_teams` count is incremented by one.

**On failure:** If the team name already exists in the registry, choose a different name or update the existing entry. Verify the YAML indentation matches existing entries.

### Step 9: Run README Automation

Regenerate README files from the updated registry:

```bash
npm run update-readmes
```

This updates the dynamic sections in `teams/README.md` and any other files with `<!-- AUTO:START -->` / `<!-- AUTO:END -->` markers that reference team data.

**Expected:** Command exits 0, `teams/README.md` now lists the new team.

**On failure:** Run `npm run check-readmes` to see which files are out of sync. If the script fails, verify `package.json` exists in the repository root and `js-yaml` is installed (`npm install`).

### Step 10: Verify Team Activation

Test that the team can be activated in Claude Code:

```
User: Use the <team-name> team to <typical task description>
```

Claude Code should:
1. Find the team file at `teams/<team-name>.md`
2. Identify the lead and members
3. Follow the coordination pattern described in the file

**Expected:** Claude Code recognizes the team name, identifies the correct lead and members, and follows the coordination pattern.

**On failure:** Verify the team file is at `teams/<team-name>.md` (not in a subdirectory). Check that all member agents exist in `.claude/agents/` (which symlinks to `agents/`). Confirm the team is listed in `teams/_registry.yml`.

## Validation

- [ ] Team file exists at `teams/<team-name>.md`
- [ ] YAML frontmatter parses without errors
- [ ] All required frontmatter fields present: `name`, `description`, `lead`, `version`, `author`, `coordination`, `members[]`
- [ ] Each member in frontmatter has `id`, `role`, and `responsibilities`
- [ ] All sections present: Purpose, Team Composition, Coordination Pattern, Task Decomposition, Configuration, Usage Scenarios, Limitations, See Also
- [ ] CONFIG block exists between `<!-- CONFIG:START -->` and `<!-- CONFIG:END -->` markers
- [ ] CONFIG block YAML is valid and parseable
- [ ] All member agent ids exist in `agents/_registry.yml`
- [ ] Lead agent appears in the members list
- [ ] No two members share the same primary responsibility
- [ ] Team is listed in `teams/_registry.yml` with correct path, lead, members, and coordination
- [ ] `total_teams` count in registry is incremented
- [ ] `npm run update-readmes` completes without errors

## Common Pitfalls

- **Too many members**: Teams with more than 5 members become hard to coordinate. The overhead of distributing tasks and synthesizing results outweighs the benefit of additional perspectives. Split into two teams or reduce to the essential specialties.
- **Overlapping responsibilities**: If two members both "review code quality," their findings will conflict and the lead wastes time deduplicating. Each member must have a clearly distinct focus area.
- **Wrong coordination pattern**: Using hub-and-spoke when agents need each other's output (should be sequential), or using sequential when agents can work independently (should be parallel). Review the decision guide in Step 4.
- **Missing CONFIG block**: The CONFIG block is not optional prose decoration. Tooling reads it to auto-create teams with `TeamCreate`. Without it, the team file is only human-readable and cannot be programmatically activated.
- **Lead agent not in members list**: The lead must also appear as a member with their own role and responsibilities. A lead who only "coordinates" without doing substantive work wastes a slot. Give the lead a concrete review or synthesis responsibility.

## Related Skills

- `create-skill` - follows the same meta-pattern for creating SKILL.md files
- `create-agent` - create agent definitions that serve as team members
- `commit-changes` - commit the new team file and registry updates
