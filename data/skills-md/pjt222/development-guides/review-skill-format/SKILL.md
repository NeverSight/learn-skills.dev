---
name: review-skill-format
description: >
  Review a SKILL.md file for compliance with the agentskills.io standard.
  Checks YAML frontmatter fields, required sections, line count limits,
  procedure step format, and registry synchronization. Use when a new skill
  needs format validation before merge, an existing skill has been modified and
  requires re-validation, performing a batch audit of all skills in a domain,
  or reviewing a contributor's skill submission in a pull request.
license: MIT
allowed-tools: Read Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.1"
  domain: review
  complexity: intermediate
  language: multi
  tags: review, skills, format, validation, agentskills, quality
---

# Review Skill Format

Validate a SKILL.md file against the agentskills.io open standard. This skill checks YAML frontmatter completeness, required section presence, procedure step format (Expected/On failure blocks), line count limits, and registry synchronization. Use this before merging any new or modified skill.

## When to Use

- A new skill has been authored and needs format validation before merge
- An existing skill has been modified and needs re-validation
- Performing a batch audit of all skills in a domain
- Verifying a skill created by the `create-skill` meta-skill
- Reviewing a contributor's skill submission in a pull request

## Inputs

- **Required**: Path to the SKILL.md file (e.g., `skills/setup-vault/SKILL.md`)
- **Optional**: Strictness level (`lenient` or `strict`, default: `strict`)
- **Optional**: Whether to check registry sync (default: yes)

## Procedure

### Step 1: Verify File Exists and Read Content

Confirm the SKILL.md file exists at the expected path and read its full content.

```bash
# Verify file exists
test -f skills/<skill-name>/SKILL.md && echo "EXISTS" || echo "MISSING"

# Count lines
wc -l < skills/<skill-name>/SKILL.md
```

**Expected:** File exists and content is readable. Line count is displayed.

**On failure:** If the file does not exist, check the path for typos. Verify the skill directory exists with `ls skills/<skill-name>/`. If the directory is missing, the skill has not been created yet — use `create-skill` first.

### Step 2: Check YAML Frontmatter Fields

Parse the YAML frontmatter block (between `---` delimiters) and verify all required and recommended fields are present.

Required fields:
- `name` — matches directory name (kebab-case)
- `description` — under 1024 characters, starts with a verb
- `license` — typically `MIT`
- `allowed-tools` — comma-separated or space-separated tool list

Recommended metadata fields:
- `metadata.author` — author name
- `metadata.version` — semantic version string
- `metadata.domain` — one of the domains listed in `skills/_registry.yml`
- `metadata.complexity` — one of: `basic`, `intermediate`, `advanced`
- `metadata.language` — primary language or `multi`
- `metadata.tags` — comma-separated, 3-6 tags, includes domain name

```bash
# Check required frontmatter fields exist
head -30 skills/<skill-name>/SKILL.md | grep -q '^name:' && echo "name: OK" || echo "name: MISSING"
head -30 skills/<skill-name>/SKILL.md | grep -q '^description:' && echo "description: OK" || echo "description: MISSING"
head -30 skills/<skill-name>/SKILL.md | grep -q '^license:' && echo "license: OK" || echo "license: MISSING"
head -30 skills/<skill-name>/SKILL.md | grep -q '^allowed-tools:' && echo "allowed-tools: OK" || echo "allowed-tools: MISSING"
```

**Expected:** All four required fields present. All six metadata fields present. `name` matches directory name. `description` is under 1024 characters.

**On failure:** Report each missing field as BLOCKING. If `name` does not match directory name, report as BLOCKING with the expected value. If `description` exceeds 1024 characters, report as SUGGEST with current length.

### Step 3: Check Required Sections

Verify all six required sections are present in the skill body (after frontmatter).

Required sections:
1. `## When to Use`
2. `## Inputs`
3. `## Procedure` (with `### Step N:` sub-sections)
4. `## Validation` (may also appear as `## Validation Checklist`)
5. `## Common Pitfalls`
6. `## Related Skills`

```bash
# Check each required section
for section in "## When to Use" "## Inputs" "## Procedure" "## Common Pitfalls" "## Related Skills"; do
  grep -q "$section" skills/<skill-name>/SKILL.md && echo "$section: OK" || echo "$section: MISSING"
done

# Validation section may use either heading
grep -qE "## Validation( Checklist)?" skills/<skill-name>/SKILL.md && echo "Validation: OK" || echo "Validation: MISSING"
```

**Expected:** All six sections present. Procedure section contains at least one `### Step` sub-heading.

**On failure:** Report each missing section as BLOCKING. A skill without all six sections is non-compliant with the agentskills.io standard. Provide the section template from the `create-skill` meta-skill.

### Step 4: Check Procedure Step Format

Verify each procedure step follows the required pattern: numbered step title, context, code block(s), and **Expected:**/**On failure:** blocks.

For each `### Step N:` sub-section, check:
1. The step has a descriptive title (not just "Step N")
2. At least one code block or concrete instruction exists
3. An `**Expected:**` block is present
4. An `**On failure:**` block is present

**Expected:** Every procedure step has both **Expected:** and **On failure:** blocks. Steps contain concrete code or instructions, not vague descriptions.

**On failure:** Report each step missing Expected/On failure as BLOCKING. If steps contain only vague instructions ("configure the system appropriately"), report as SUGGEST with a note to add concrete commands.

### Step 5: Verify Line Count

Check that the SKILL.md is within the 500-line limit.

```bash
lines=$(wc -l < skills/<skill-name>/SKILL.md)
[ "$lines" -le 500 ] && echo "OK ($lines lines)" || echo "OVER LIMIT ($lines lines > 500)"
```

**Expected:** Line count is 500 or fewer.

**On failure:** If over 500 lines, report as BLOCKING. Recommend using the `refactor-skill-structure` skill to extract code blocks >15 lines to `references/EXAMPLES.md`. Typical reduction: 20-40% by extracting extended examples.

### Step 6: Check Registry Synchronization

Verify the skill is listed in `skills/_registry.yml` under the correct domain with matching metadata.

Check:
1. Skill `id` exists under the correct domain section
2. `path` matches `<skill-name>/SKILL.md`
3. `complexity` matches frontmatter
4. `description` is present (may be abbreviated)
5. `total_skills` count at the top of the registry matches actual skill count

```bash
# Check if skill is in registry
grep -q "id: <skill-name>" skills/_registry.yml && echo "Registry: FOUND" || echo "Registry: NOT FOUND"

# Check path
grep -A1 "id: <skill-name>" skills/_registry.yml | grep -q "path: <skill-name>/SKILL.md" && echo "Path: OK" || echo "Path: MISMATCH"
```

**Expected:** Skill is listed in the registry under the correct domain with matching path and metadata. Total count is accurate.

**On failure:** If not found in registry, report as BLOCKING. Provide the registry entry template:
```yaml
- id: skill-name
  path: skill-name/SKILL.md
  complexity: intermediate
  language: multi
  description: One-line description
```

## Validation

- [ ] SKILL.md file exists at the expected path
- [ ] YAML frontmatter parses without errors
- [ ] All four required frontmatter fields present (`name`, `description`, `license`, `allowed-tools`)
- [ ] All six metadata fields present (`author`, `version`, `domain`, `complexity`, `language`, `tags`)
- [ ] `name` field matches directory name
- [ ] `description` is under 1024 characters
- [ ] All six required sections present (When to Use, Inputs, Procedure, Validation, Common Pitfalls, Related Skills)
- [ ] Every procedure step has **Expected:** and **On failure:** blocks
- [ ] Line count is 500 or fewer
- [ ] Skill is listed in `_registry.yml` with correct domain, path, and metadata
- [ ] `total_skills` count in registry is accurate

## Common Pitfalls

- **Checking frontmatter with regex only**: YAML parsing can be subtle. A `description: >` multiline block looks different from `description: "inline"`. Check both patterns when searching for fields.
- **Missing the Validation section variant**: Some skills use `## Validation Checklist` instead of `## Validation`. Both are acceptable; check for either heading.
- **Forgetting registry total count**: After adding a skill to the registry, the `total_skills` number at the top must also be incremented. This is a common miss in PRs.
- **Name vs. title confusion**: The `name` field must be kebab-case matching the directory name. The `# Title` heading is human-readable and can differ (e.g., name: `review-skill-format`, title: `# Review Skill Format`).
- **Lenient mode skipping blockers**: Even in lenient mode, missing required sections and frontmatter fields should still be flagged. Lenient mode only relaxes style and metadata recommendations.

## Related Skills

- `create-skill` — The canonical format specification; use as the authoritative reference for what a valid SKILL.md looks like
- `update-skill-content` — After format validation passes, use this to improve content quality
- `refactor-skill-structure` — When a skill fails the line count check, use this to extract and reorganize
- `review-pull-request` — When reviewing a PR that adds or modifies skills, combine PR review with format validation
