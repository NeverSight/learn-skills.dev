---
name: update-skill-content
description: >
  Update the content of an existing SKILL.md to improve accuracy,
  completeness, and clarity. Covers version bumping, procedure
  refinement, pitfall expansion, and related skills synchronization. Use
  when a skill's procedures reference outdated tools or APIs, the Common
  Pitfalls section is thin, Related Skills has broken cross-references, or
  after receiving feedback that a skill's procedures are unclear or incomplete.
license: MIT
allowed-tools: Read Write Edit Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.1"
  domain: review
  complexity: intermediate
  language: multi
  tags: review, skills, content, update, maintenance, quality
---

# Update Skill Content

Improve an existing SKILL.md by refining procedure steps, expanding Common Pitfalls with real failure modes, synchronizing the Related Skills section, and bumping the version number. Use this after a skill passes format validation but has content gaps, stale references, or incomplete procedures.

## When to Use

- A skill's procedure steps reference outdated tools, APIs, or version numbers
- Common Pitfalls section is thin (fewer than 3 pitfalls) or missing real failure modes
- Related Skills section has broken cross-references or is missing relevant links
- Procedure steps lack concrete code examples or have vague instructions
- A new skill has been added to the library that should be cross-referenced from existing skills
- After receiving feedback that a skill's procedures are unclear or incomplete

## Inputs

- **Required**: Path to the SKILL.md file to update
- **Optional**: Specific section(s) to focus on (e.g., "procedure", "pitfalls", "related-skills")
- **Optional**: Source of updates (changelog, issue report, user feedback)
- **Optional**: Whether to bump version (default: yes, minor bump)

## Procedure

### Step 1: Read Current Skill and Assess Content Quality

Read the entire SKILL.md and evaluate each section for completeness and accuracy.

Assessment criteria per section:
- **When to Use**: Are triggers concrete and actionable? (3-5 items expected)
- **Inputs**: Are types, defaults, and required/optional clearly separated?
- **Procedure**: Does each step have concrete code, Expected, and On failure?
- **Validation**: Are checklist items objectively testable? (5+ items expected)
- **Common Pitfalls**: Are pitfalls specific with symptoms and fixes? (3-6 expected)
- **Related Skills**: Do referenced skills exist? Are obvious related skills missing?

**Expected:** A clear picture of which sections need improvement, with specific gaps identified.

**On failure:** If the skill cannot be read (path error), verify the path. If the SKILL.md has broken YAML frontmatter, fix frontmatter first using `review-skill-format` before attempting content updates.

### Step 2: Check for Stale References

Scan procedure steps for version-specific references, tool names, URLs, and API patterns that may have changed.

Common staleness indicators:
- Specific version numbers (e.g., `v1.24`, `R 4.3.0`, `Node 18`)
- URLs that may have moved or expired
- CLI flags or command syntax that has changed
- Package names that have been renamed or deprecated
- Configuration file formats that have evolved

```bash
# Check for version-specific references
grep -nE '[vV][0-9]+\.[0-9]+' skills/<skill-name>/SKILL.md

# Check for URLs
grep -nE 'https?://' skills/<skill-name>/SKILL.md
```

**Expected:** A list of potentially stale references with line numbers. Each reference is verified as current or flagged for update.

**On failure:** If too many references to check manually, prioritize: procedure code blocks first (most likely to cause runtime failures), then Common Pitfalls (may reference old workarounds), then informational text.

### Step 3: Update Procedure Steps for Accuracy

For each procedure step identified as needing improvement:

1. Verify code blocks still execute correctly or reflect current best practices
2. Add missing context sentences that explain *why* the step is needed
3. Ensure concrete commands use real paths, real flags, and real output
4. Update Expected blocks to match current tool behavior
5. Update On failure blocks with current error messages and fixes

When updating code blocks, preserve the original structure:
- Keep step numbering consistent
- Maintain the `### Step N: Title` format
- Do not reorder steps unless the original order was incorrect

**Expected:** All procedure steps contain current, executable code. Expected/On failure blocks reflect actual current behavior.

**On failure:** If unsure whether a code block is still correct, add a note: `<!-- TODO: Verify this command against current version -->`. Do not remove working code blocks to replace with untested alternatives.

### Step 4: Expand Common Pitfalls

Review the Common Pitfalls section and expand if gaps exist.

Quality criteria for pitfalls:
- Each pitfall has a **bold name** followed by a specific description
- The description includes the *symptom* (what goes wrong) and the *fix* (how to avoid or recover)
- Pitfalls are drawn from real failure modes, not hypothetical concerns
- 3-6 pitfalls is the target range

Sources for new pitfalls:
- Procedure steps with complex On failure blocks (these are likely pitfalls)
- Related skills that warn about the same tools or patterns
- Common issues reported by users of the procedure

**Expected:** 3-6 pitfalls, each with a specific symptom and fix. No generic pitfalls like "be careful" or "test thoroughly".

**On failure:** If only 1-2 pitfalls can be identified, that is acceptable for basic-complexity skills. For intermediate and advanced skills, fewer than 3 pitfalls suggests the author has not fully explored failure modes — flag this for future expansion.

### Step 5: Synchronize Related Skills Section

Verify all cross-references in the Related Skills section are valid and add any missing links.

1. For each referenced skill, verify it exists:
   ```bash
   # Check if referenced skill exists
   test -d skills/referenced-skill-name && echo "EXISTS" || echo "NOT FOUND"
   ```
2. Search for skills that reference this skill (they should be cross-linked):
   ```bash
   # Find skills that reference this skill
   grep -rl "skill-name" skills/*/SKILL.md
   ```
3. Check for obvious related skills based on domain and tags
4. Use the format: `- \`skill-id\` — one-line description of the relationship`

**Expected:** All referenced skills exist on disk. Bidirectional cross-references are in place. No orphaned links.

**On failure:** If a referenced skill does not exist, either remove the reference or note it as a planned future skill with a comment. If many skills reference this one but are not listed in Related Skills, add the most relevant 2-3.

### Step 6: Bump Version in Frontmatter

Update the `metadata.version` field following semantic versioning:
- **Patch bump** (1.0 to 1.1): Typo fixes, minor clarifications, URL updates
- **Minor bump** (1.0 to 2.0): New procedure steps, significant content additions, structural changes
- **Note**: Skills use simplified two-part versioning (major.minor)

Also update any date fields if present in the frontmatter.

**Expected:** Version is bumped appropriately. The change magnitude matches the update scope.

**On failure:** If the current version cannot be parsed, set it to `"1.1"` and add a comment noting the version history gap.

## Validation

- [ ] All procedure steps contain current, executable code or concrete instructions
- [ ] No stale version references, URLs, or deprecated tool names remain
- [ ] Every procedure step has **Expected:** and **On failure:** blocks
- [ ] Common Pitfalls section has 3-6 specific pitfalls with symptoms and fixes
- [ ] All Related Skills cross-references point to existing skills
- [ ] Bidirectional cross-references are in place for closely related skills
- [ ] Version in frontmatter has been bumped appropriately
- [ ] Line count remains under 500 after updates
- [ ] SKILL.md still passes `review-skill-format` validation after changes

## Common Pitfalls

- **Updating code without testing**: Changing a command in a procedure step without verifying it works is worse than leaving the old command. When uncertain, add a verification comment rather than an untested replacement.
- **Over-expanding pitfalls**: Adding 10+ pitfalls dilutes the section. Keep the 3-6 most impactful pitfalls; move edge cases to a `references/` file if needed.
- **Breaking cross-references during updates**: When renaming a skill or changing its domain, grep the entire skills library for references to the old name. Use `grep -rl "old-name" skills/` to find all occurrences.
- **Forgetting to bump version**: Every content update, no matter how small, should bump the version. This allows consumers to detect when a skill has changed.
- **Scope creep into refactoring**: Content updates improve *what* the skill says. If you find yourself restructuring sections or extracting to `references/`, switch to the `refactor-skill-structure` skill instead.

## Related Skills

- `review-skill-format` — Run format validation before content updates to ensure the base structure is sound
- `refactor-skill-structure` — When content updates push the skill over 500 lines, refactor structure to make room
- `evolve-skill` — For deeper changes that go beyond content updates (e.g., creating an advanced variant)
- `create-skill` — Reference the canonical format spec when adding new sections or procedure steps
- `repair-broken-references` — Use for bulk cross-reference repair across the entire skills library
