---
name: evolve-skill
description: >
  Evolve an existing skill by refining its content in-place or creating an
  advanced variant. Covers assessing the current skill, gathering evolution
  requirements, choosing scope (refinement vs. variant), applying changes,
  updating version metadata, and synchronizing the registry and cross-references.
  Use when a skill's procedure steps are outdated, user feedback reveals gaps,
  a skill needs a complexity upgrade, an advanced variant is needed alongside
  the original, or related skills are added and cross-references are stale.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.1"
  domain: general
  complexity: intermediate
  language: multi
  tags: meta, skill, agentskills, maintenance, evolution, versioning
---

# Evolve an Existing Skill

Improve, extend, or create an advanced variant of a skill that was originally authored with `create-skill`. This procedure covers the maintenance side of the skill lifecycle: assessing gaps, applying targeted improvements, bumping versions, and keeping the registry and cross-references in sync.

## When to Use

- A skill's procedure steps are outdated or incomplete after tooling changes
- User feedback reveals missing pitfalls, unclear steps, or weak validation
- A skill needs to grow from basic to intermediate (or intermediate to advanced)
- An advanced variant is needed alongside the original (e.g., `create-r-package` and `create-r-package-advanced`)
- Related skills were added or removed and cross-references are stale

## Inputs

- **Required**: Path to the existing SKILL.md to evolve
- **Required**: Evolution trigger (feedback, tooling change, complexity upgrade, new related skills, discovered pitfalls)
- **Optional**: Target complexity level if changing (basic, intermediate, advanced)
- **Optional**: Whether to create an advanced variant instead of refining in-place (default: refine in-place)

## Procedure

### Step 1: Assess the Current Skill

Read the existing SKILL.md and evaluate each section against the quality checklist:

| Section | What to Check | Common Issues |
|---------|--------------|---------------|
| Frontmatter | All required fields present, `description` < 1024 chars | Missing `tags`, stale `version` |
| When to Use | 3-5 concrete trigger conditions | Vague or overlapping triggers |
| Inputs | Required vs optional clearly separated | Missing defaults for optional inputs |
| Procedure | Each step has code + Expected + On failure | Missing On failure blocks, pseudocode instead of real commands |
| Validation | Each item is binary pass/fail | Subjective criteria ("code is clean") |
| Common Pitfalls | 3-6 with cause and avoidance | Too generic ("be careful") |
| Related Skills | 2-5 valid skill references | Stale references to renamed/removed skills |

```bash
# Read the skill
cat skills/<skill-name>/SKILL.md

# Check frontmatter parses
head -20 skills/<skill-name>/SKILL.md

# Verify related skills still exist
grep -oP '`[\w-]+`' skills/<skill-name>/SKILL.md | sort -u
```

**Expected:** A list of specific gaps, weaknesses, or improvement opportunities.

**On failure:** If the SKILL.md doesn't exist or has no frontmatter, this skill doesn't apply — use `create-skill` instead to author it from scratch.

### Step 2: Gather Evolution Requirements

Identify and categorize what triggered the evolution:

| Trigger | Example | Typical Scope |
|---------|---------|---------------|
| User feedback | "Step 3 is unclear" | Refinement |
| Tooling change | New API version, deprecated command | Refinement |
| Discovered pitfall | Common failure not documented | Refinement |
| Complexity upgrade | Skill is too shallow for real use | Refinement or variant |
| New related skills | Adjacent skill was added | Refinement (cross-refs) |
| Advanced use case | Power users need deeper coverage | Variant |

Document the specific changes needed before editing. List each change with its target section.

**Expected:** A concrete list of changes (e.g., "Add On failure to Step 4", "Add new Step 6 for edge case X", "Update Related Skills to include `new-skill`").

**On failure:** If the changes are unclear, consult the user for clarification before proceeding. Vague evolution goals produce vague improvements.

### Step 3: Choose Evolution Scope

Use this decision matrix to determine whether to refine in-place or create a variant:

| Criteria | Refinement (in-place) | Advanced Variant (new skill) |
|----------|----------------------|------------------------------|
| Skill ID | Unchanged | New ID: `<skill>-advanced` |
| File path | Same SKILL.md | New directory |
| Version bump | Patch or minor | Starts at 1.0 |
| Complexity | May increase | Higher than original |
| Registry | No new entry | New entry added |
| Symlinks | No change | New symlinks needed |
| Original skill | Modified directly | Left intact, gains cross-reference |

**Refinement**: Choose when improving quality, fixing gaps, or adding modest new content. The skill keeps its identity.

**Variant**: Choose when the evolved version would double the length, change the target audience, or require substantially different inputs. The original stays as-is for simpler use cases.

**Expected:** A clear decision — refinement or variant — with rationale.

**On failure:** If unsure, default to refinement. You can always extract a variant later; it's harder to merge one back.

### Step 4: Apply Content Changes

#### For Refinements

Edit the existing SKILL.md directly:

```bash
# Open for editing
# Add/revise procedure steps
# Strengthen Expected/On failure pairs
# Add tables or examples
# Update When to Use triggers
# Revise Inputs if scope changed
```

Follow these editing rules:
- Preserve all existing sections — add content, don't remove sections
- Keep step numbering sequential after insertions
- Every new or modified step must have both Expected and On failure
- New pitfalls go at the end of the Common Pitfalls section
- New related skills go at the end of the Related Skills section

#### For Variants

```bash
# Create the variant directory
mkdir -p skills/<skill-name>-advanced/

# Copy the original as a starting point
cp skills/<skill-name>/SKILL.md skills/<skill-name>-advanced/SKILL.md

# Edit the variant:
# - Change `name` to `<skill-name>-advanced`
# - Update `description` to reflect the advanced scope
# - Raise `complexity` (e.g., intermediate → advanced)
# - Reset `version` to "1.0"
# - Add/expand procedure steps for the advanced use case
# - Reference the original in Related Skills as a prerequisite
```

**Expected:** The SKILL.md (refined or new variant) passes the assessment checklist from Step 1.

**On failure:** If a step edit breaks the document structure, use `git diff` to review changes and revert partial edits with `git checkout -- <file>`.

### Step 5: Update Version and Metadata

Bump the `version` field in frontmatter following semver conventions:

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Typo fix, wording clarification | Patch: 1.0 → 1.1 | Fixed unclear sentence in Step 3 |
| New step, new pitfall, new table | Minor: 1.0 → 2.0 | Added Step 7 for edge case handling |
| Restructured procedure, changed inputs | Major: 1.0 → 2.0 | Reorganized from 5 to 8 steps |

Also update:
- `complexity` if the scope expanded (e.g., basic → intermediate)
- `tags` if the coverage area changed
- `description` if the skill's scope is materially different

**Expected:** Frontmatter `version` reflects the magnitude of changes. New variants start at `"1.0"`.

**On failure:** If you forget to bump the version, the next evolution will have no way to distinguish the current state from the previous one. Always bump before committing.

### Step 6: Update Registry and Cross-References

#### For Refinements

No registry changes are needed (path unchanged). Update cross-references only if Related Skills changed in other skills:

```bash
# Check if any skill references the evolved skill
grep -r "<skill-name>" skills/*/SKILL.md
```

#### For Variants

Add the new skill to `skills/_registry.yml`:

```yaml
- id: <skill-name>-advanced
  path: <skill-name>-advanced/SKILL.md
  complexity: advanced
  language: multi
  description: One-line description of the advanced variant
```

Then:
1. Increment `total_skills` at the top of the registry
2. Add Related Skills cross-reference in the original skill pointing to the variant
3. Add Related Skills cross-reference in the variant pointing to the original
4. Create symlinks for slash command discovery:

```bash
# Project-level
ln -s ../../skills/<skill-name>-advanced .claude/skills/<skill-name>-advanced

# Global
ln -s /mnt/d/dev/p/agent-almanac/skills/<skill-name>-advanced ~/.claude/skills/<skill-name>-advanced
```

**Expected:** Registry `total_skills` matches `find skills -name SKILL.md | wc -l`. Cross-references are bidirectional.

**On failure:** If the registry count is wrong, run `find skills -name SKILL.md | wc -l` to get the true count and correct the registry. For broken symlinks, use `readlink -f` to debug resolution.

### Step 7: Validate the Evolved Skill

Run the full validation checklist:

- [ ] SKILL.md exists at the expected path
- [ ] YAML frontmatter parses without errors
- [ ] `version` was bumped (refinement) or set to "1.0" (variant)
- [ ] All sections present: When to Use, Inputs, Procedure, Validation, Common Pitfalls, Related Skills
- [ ] Every procedure step has Expected and On failure blocks
- [ ] Related Skills reference valid, existing skill names
- [ ] Registry entry exists with correct path (variants only)
- [ ] `total_skills` count matches actual skill count on disk
- [ ] Symlinks resolve correctly (variants only)
- [ ] `git diff` shows no accidental deletions from the original content

```bash
# Verify frontmatter
head -20 skills/<skill-name>/SKILL.md

# Count skills on disk vs registry
find skills -name SKILL.md | wc -l
grep total_skills skills/_registry.yml

# Check symlinks (for variants)
ls -la .claude/skills/<skill-name>-advanced
readlink -f .claude/skills/<skill-name>-advanced/SKILL.md

# Review all changes
git diff
```

**Expected:** All checklist items pass. The evolved skill is ready to commit.

**On failure:** Address each failing item individually. The most common post-evolution issue is a stale `total_skills` count — always verify it last.

## Validation

- [ ] SKILL.md exists and has valid YAML frontmatter
- [ ] `version` field reflects the changes made
- [ ] All procedure steps have Expected and On failure blocks
- [ ] Related Skills references are valid (no broken cross-references)
- [ ] Registry `total_skills` matches actual count on disk
- [ ] For variants: new entry in `_registry.yml` with correct path
- [ ] For variants: symlinks created at `.claude/skills/` and `~/.claude/skills/`
- [ ] `git diff` confirms no accidental content removal

## Common Pitfalls

- **Forgetting to bump version**: Without version bumps, there's no way to track what changed or when. Always update `version` in frontmatter before committing.
- **Accidental content deletion**: When restructuring steps, it's easy to drop an On failure block or a table row. Always review `git diff` before committing.
- **Stale cross-references**: When creating a variant, both the original and the variant need to reference each other. One-directional references leave the graph incomplete.
- **Registry count drift**: After creating a variant, the `total_skills` count must be incremented. Forgetting this causes validation failures in other skills that check the registry.
- **Scope creep during refinement**: A refinement that doubles the skill's length should probably be a variant instead. If you're adding more than 3 new procedure steps, reconsider the scope decision from Step 3.
- **Avoid `git mv` on NTFS-mounted paths (WSL)**: On `/mnt/` paths, `git mv` for directories can create broken permissions (`d?????????`). Use `mkdir -p` + copy files + `git rm` the old path instead. See the [environment guide](../../guides/setting-up-your-environment.md) troubleshooting section.

## Related Skills

- `create-skill` — foundation for authoring new skills; evolve-skill assumes this was followed originally
- `commit-changes` — commit the evolved skill with a descriptive message
- `configure-git-repository` — version-controlled skill changes
- `security-audit-codebase` — review evolved skills for accidentally included secrets
