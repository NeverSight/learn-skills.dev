---
name: evolve-team
description: >
  Evolve an existing team composition by refining its structure in-place or
  creating a specialized variant. Covers assessing the current team against
  template and coordination patterns, gathering evolution requirements,
  choosing scope (adjust members, change coordination pattern, split/merge
  teams), applying changes to the team file and CONFIG block, updating
  version metadata, and synchronizing the registry and cross-references.
  Use when a team's member roster is outdated, coordination pattern no
  longer fits, user feedback reveals workflow gaps, a specialized variant
  is needed alongside the original, or agents have been added or removed
  from the library affecting team composition.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: general
  complexity: intermediate
  language: multi
  tags: meta, team, evolution, coordination, maintenance
---

# Evolve an Existing Team

Improve, restructure, or create a specialized variant of a team that was originally authored with `create-team`. This procedure covers the maintenance side of the team lifecycle: assessing gaps against the template and coordination patterns, applying targeted improvements to composition and workflow, bumping versions, and keeping the registry and cross-references in sync.

## When to Use

- A team's member roster is outdated after agents were added, removed, or evolved
- User feedback reveals workflow bottlenecks, unclear handoffs, or missing perspectives
- The coordination pattern no longer fits the team's actual workflow (e.g., hub-and-spoke should be parallel)
- A specialized variant is needed alongside the original (e.g., `r-package-review` and `r-package-review-security-focused`)
- Team members' responsibilities overlap and need sharper boundaries
- The CONFIG block is out of sync with the prose description or the members list
- A team needs to be split into two smaller teams or two teams need to be merged

## Inputs

- **Required**: Path to the existing team file to evolve (e.g., `teams/r-package-review.md`)
- **Required**: Evolution trigger (feedback, new agents, coordination mismatch, scope overlap, performance issues, agent evolution)
- **Optional**: Target version bump magnitude (patch, minor, major)
- **Optional**: Whether to create a specialized variant instead of refining in-place (default: refine in-place)

## Procedure

### Step 1: Assess the Current Team

Read the existing team file and evaluate each section against the team template (`teams/_template.md`):

| Section | What to Check | Common Issues |
|---------|--------------|---------------|
| Frontmatter | All required fields (`name`, `description`, `lead`, `version`, `author`, `coordination`, `members[]`) | Missing `tags`, stale `version`, wrong `coordination` |
| Purpose | Clear multi-agent justification (at least two distinct specialties) | Could be handled by a single agent |
| Team Composition | Table matches frontmatter members, no overlapping responsibilities | Stale table, duplicated focus areas |
| Coordination Pattern | Matches actual workflow, ASCII diagram present | Wrong pattern for the workflow |
| Task Decomposition | Phased breakdown with concrete tasks per member | Vague tasks, missing phases |
| CONFIG Block | Valid YAML between markers, matches frontmatter and prose | Out of sync, missing `blocked_by`, invalid YAML |
| Usage Scenarios | 2-3 realistic activation prompts | Placeholder text |
| Limitations | 3-5 honest constraints | Missing or too generic |
| See Also | Valid links to member agents, related teams, guides | Stale links |

```bash
# Read the team file
cat teams/<team-name>.md

# Verify all member agents still exist
grep "id:" teams/<team-name>.md | while read line; do
  agent=$(echo "$line" | grep -oP '(?<=id: )[\w-]+')
  grep "id: $agent" agents/_registry.yml || echo "MISSING: $agent"
done

# Check if the team is referenced by any guide
grep -r "<team-name>" guides/*.md
```

**Expected:** A list of specific gaps, weaknesses, or improvement opportunities organized by section.

**On failure:** If the team file does not exist or has no frontmatter, this skill does not apply — use `create-team` instead to author it from scratch.

### Step 2: Gather Evolution Requirements

Identify and categorize what triggered the evolution:

| Trigger | Example | Typical Scope |
|---------|---------|---------------|
| User feedback | "Reviews take too long, agents duplicate effort" | Sharpen responsibilities or change pattern |
| New agent available | `api-security-analyst` agent was created | Add member |
| Agent evolved | `code-reviewer` gained new skills | Update member responsibilities |
| Agent removed | `deprecated-agent` was retired | Remove member, reassign tasks |
| Coordination mismatch | Sequential team has independent subtasks | Change to parallel |
| Scope expansion | Team needs to cover deployment, not just review | Add member or create variant |
| Team too large | 6+ members causing coordination overhead | Split into two teams |
| Team too small | Single member does most of the work | Merge with another team or add members |

Document the specific changes needed before editing:

```
- Frontmatter: add new member `api-security-analyst` with role "API Security Reviewer"
- Team Composition: add row to composition table
- Task Decomposition: add API security review tasks to execution phase
- CONFIG block: add member and tasks entries
- See Also: add link to new agent file
```

**Expected:** A concrete list of changes, each mapped to a specific section of the team file.

**On failure:** If the changes are unclear, consult the user for clarification before proceeding. Vague evolution goals produce vague improvements.

### Step 3: Choose Evolution Scope

Use this decision matrix to determine whether to refine in-place or create a variant:

| Criteria | Refinement (in-place) | Specialized Variant (new team) |
|----------|----------------------|-------------------------------|
| Team ID | Unchanged | New ID: `<team>-<specialty>` |
| File path | Same `.md` file | New file in `teams/` |
| Version bump | Patch or minor | Starts at 1.0.0 |
| Coordination | May change | May differ from original |
| Registry | Update existing entry | New entry added |
| Original team | Modified directly | Left intact, gains See Also cross-reference |

**Refinement**: Choose when adjusting members, sharpening responsibilities, fixing the CONFIG block, or changing the coordination pattern. The team keeps its identity.

**Variant**: Choose when the evolved version would serve a substantially different use case, require a different coordination pattern, or target a different audience. The original stays as-is for its existing use case.

Additional scope decisions:

| Situation | Action |
|-----------|--------|
| Team has 6+ members and is slow | Split into two focused teams |
| Two teams of 2 cover adjacent domains | Merge into one team of 3-4 |
| Team's coordination pattern is wrong | Refinement — change pattern in-place |
| Team needs entirely different lead | Refinement if lead exists; create agent first if not |

**Expected:** A clear decision — refinement, variant, split, or merge — with rationale.

**On failure:** If unsure, default to refinement. Splitting or merging teams has higher blast radius and should be confirmed with the user.

### Step 4: Apply Changes to the Team File

#### For Refinements

Edit the existing team file directly. Maintain consistency across all sections that reference team composition:

1. **Frontmatter `members[]`**: Add, remove, or update member entries (each with `id`, `role`, `responsibilities`)
2. **Team Composition table**: Must match frontmatter members exactly
3. **Coordination Pattern**: Update prose and ASCII diagram if the pattern changes
4. **Task Decomposition**: Revise phases and per-member tasks to reflect new composition
5. **CONFIG block**: Update `members` and `tasks` lists to match (see Step 5)
6. **Usage Scenarios**: Revise if the team's activation triggers changed
7. **Limitations**: Update to reflect new constraints or remove resolved ones
8. **See Also**: Update agent links and add references to new related teams or guides

Follow these editing rules:
- Preserve all existing sections — add content, do not remove sections
- When adding a member, add them to ALL of: frontmatter, composition table, task decomposition, and CONFIG block
- When removing a member, remove from ALL of those locations and reassign their tasks
- Verify each member agent exists: `grep "id: agent-name" agents/_registry.yml`
- Keep the lead in the members list — the lead is always a member

#### For Variants

```bash
# Copy the original as a starting point
cp teams/<team-name>.md teams/<team-name>-<specialty>.md

# Edit the variant:
# - Change `name` to `<team-name>-<specialty>`
# - Update `description` to reflect the specialized scope
# - Adjust `coordination` pattern if needed
# - Reset `version` to "1.0.0"
# - Modify members, tasks, and CONFIG block for the specialized use case
# - Reference the original in See Also as a general-purpose alternative
```

**Expected:** The team file (refined or new variant) passes the assessment checklist from Step 1, with all sections internally consistent.

**On failure:** If an edit breaks internal consistency (e.g., CONFIG block lists a member not in frontmatter), compare the frontmatter `members[]` against the Team Composition table, Task Decomposition, and CONFIG block to find the mismatch.

### Step 5: Update the CONFIG Block

The CONFIG block between `<!-- CONFIG:START -->` and `<!-- CONFIG:END -->` must stay in sync with the prose sections. After any member or task change:

1. Verify every `agent` in CONFIG `members` matches a member in the frontmatter
2. Verify every `assignee` in CONFIG `tasks` matches a member agent id
3. Update `blocked_by` dependencies if task ordering changed
4. Ensure the synthesis/final task references all prerequisite tasks

```yaml
team:
  name: <team-name>
  lead: <lead-agent>
  coordination: <pattern>
  members:
    - agent: <agent-id>
      role: <role-title>
      subagent_type: <agent-id>
  tasks:
    - name: <task-name>
      assignee: <agent-id>
      description: <one-line>
    - name: synthesize-results
      assignee: <lead-agent>
      description: Collect and synthesize all member outputs
      blocked_by: [<prior-task-names>]
```

**Expected:** CONFIG YAML is valid, all agents and tasks are consistent with the rest of the file, and `blocked_by` forms a valid DAG.

**On failure:** Parse the CONFIG block YAML separately to find syntax errors. Cross-check every `assignee` against the `members` list.

### Step 6: Update Version and Metadata

Bump the `version` field in frontmatter following semantic versioning:

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Wording fix, See Also update | Patch: 1.0.0 → 1.0.1 | Fixed stale agent link |
| New member added, tasks revised | Minor: 1.0.0 → 1.1.0 | Added security-analyst member |
| Coordination pattern changed, team restructured | Major: 1.0.0 → 2.0.0 | Changed from hub-and-spoke to parallel |

Also update:
- `updated` date to the current date
- `tags` if the team's domain coverage changed
- `description` if the team's purpose is materially different
- `coordination` if the pattern changed

**Expected:** Frontmatter `version` and `updated` reflect the magnitude and date of changes. New variants start at `"1.0.0"`.

**On failure:** If you forget to bump the version, the next evolution will have no way to distinguish the current state from the previous one. Always bump before committing.

### Step 7: Update Registry and Cross-References

#### For Refinements

Update the existing entry in `teams/_registry.yml` to match the revised frontmatter:

```bash
# Find the team's registry entry
grep -A 10 "id: <team-name>" teams/_registry.yml
```

Update `description`, `lead`, `members`, and `coordination` fields to match the team file. No count change is needed.

#### For Variants

Add the new team to `teams/_registry.yml`:

```yaml
- id: <team-name>-<specialty>
  path: <team-name>-<specialty>.md
  lead: <lead-agent>
  members: [agent-1, agent-2, agent-3]
  coordination: <pattern>
  description: One-line description of the specialized variant
```

Then:
1. Increment `total_teams` at the top of the registry
2. Add See Also cross-reference in the original team pointing to the variant
3. Add See Also cross-reference in the variant pointing to the original

Run the README automation:

```bash
npm run update-readmes
```

**Expected:** Registry entry matches the team file frontmatter. `npm run update-readmes` exits 0. For variants, `total_teams` equals the actual number of team entries.

**On failure:** If the registry count is wrong, count entries with `grep -c "^  - id:" teams/_registry.yml` and correct the count. If README automation fails, verify `package.json` exists and `js-yaml` is installed.

### Step 8: Validate the Evolved Team

Run the full validation checklist:

- [ ] Team file exists at the expected path
- [ ] YAML frontmatter parses without errors
- [ ] `version` was bumped (refinement) or set to "1.0.0" (variant)
- [ ] `updated` date reflects today
- [ ] All required sections present: Purpose, Team Composition, Coordination Pattern, Task Decomposition, Configuration, Usage Scenarios, Limitations, See Also
- [ ] Frontmatter `members[]` matches Team Composition table
- [ ] CONFIG block members match frontmatter members
- [ ] CONFIG block tasks have valid assignees and `blocked_by` references
- [ ] All member agent IDs exist in `agents/_registry.yml`
- [ ] Lead agent appears in the members list
- [ ] No two members share the same primary responsibility
- [ ] Registry entry exists and matches frontmatter
- [ ] For variants: `total_teams` count matches actual count on disk
- [ ] Cross-references are bidirectional (original ↔ variant)
- [ ] `git diff` shows no accidental deletions from the original content

```bash
# Verify frontmatter
head -25 teams/<team-name>.md

# Verify all member agents exist
for agent in agent-a agent-b agent-c; do
  grep "id: $agent" agents/_registry.yml
done

# Count teams on disk vs registry
ls teams/*.md | grep -v template | wc -l
grep total_teams teams/_registry.yml

# Review all changes
git diff
```

**Expected:** All checklist items pass. The evolved team is ready to commit.

**On failure:** Address each failing item individually. The most common post-evolution issues are CONFIG block drift (members or tasks not matching the prose) and a forgotten `updated` date.

## Validation

- [ ] Team file exists and has valid YAML frontmatter
- [ ] `version` field reflects the changes made
- [ ] `updated` date is current
- [ ] All sections present and internally consistent
- [ ] Frontmatter `members[]`, Team Composition table, and CONFIG block are in sync
- [ ] All member agent IDs exist in `agents/_registry.yml`
- [ ] Lead agent is in the members list
- [ ] CONFIG block YAML is valid and parseable
- [ ] Registry entry matches the team file
- [ ] For variants: new entry in `teams/_registry.yml` with correct path
- [ ] For variants: `total_teams` count updated
- [ ] Cross-references are valid (no broken links in See Also)
- [ ] `git diff` confirms no accidental content removal

## Common Pitfalls

- **CONFIG block drift**: The CONFIG block, frontmatter, and prose sections must all agree on members and tasks. Updating one without the others is the most common team evolution error. After every change, cross-check all three.
- **Forgetting to bump version**: Without version bumps, there is no way to track what changed or when. Always update `version` and `updated` in frontmatter before committing.
- **Orphaned member references**: When removing a member, their tasks in the Task Decomposition and CONFIG block must be reassigned or removed. Leaving orphaned assignees causes activation failures.
- **Wrong coordination pattern after evolution**: Adding parallel-capable members to a sequential team, or making a hub-and-spoke team where agents need each other's output. Re-evaluate the pattern decision from `create-team` Step 4 after any structural change.
- **Team too large after adding members**: Teams with more than 5 members become hard to coordinate. If evolution pushes the team past 5, consider splitting into two focused teams instead.
- **Stale See Also after variant creation**: When creating a variant, both the original and the variant need to reference each other. One-directional references leave the graph incomplete.

## Related Skills

- `create-team` — foundation for authoring new teams; evolve-team assumes this was followed originally
- `evolve-skill` — the parallel procedure for evolving SKILL.md files
- `evolve-agent` — the parallel procedure for evolving agent definitions
- `commit-changes` — commit the evolved team with a descriptive message
