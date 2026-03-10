---
name: refactor-skill-structure
description: >
  Refactor an over-long or poorly structured SKILL.md by extracting
  examples to references/EXAMPLES.md, splitting compound procedures,
  and reorganizing sections for progressive disclosure. Use when a skill
  exceeds the 500-line CI limit, when code blocks dominate the skill body,
  when a procedure step contains multiple unrelated operations, or after a
  content update pushed the skill over the line limit.
license: MIT
allowed-tools: Read Write Edit Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.1"
  domain: review
  complexity: advanced
  language: multi
  tags: review, skills, refactoring, structure, progressive-disclosure
---

# Refactor Skill Structure

Refactor a SKILL.md that has exceeded the 500-line limit or developed structural problems. This skill extracts extended code examples to `references/EXAMPLES.md`, splits compound procedures into focused sub-procedures, adds cross-references for progressive disclosure, and verifies the skill remains complete and valid after restructuring.

## When to Use

- A skill exceeds the 500-line limit enforced by CI
- A single procedure step contains multiple unrelated operations that should be separate steps
- Code blocks longer than 15 lines dominate the SKILL.md and could be extracted
- The skill has accumulated ad-hoc sections that break the standard six-section structure
- After a content update pushed the skill over the line limit
- A skill review flagged structural issues that go beyond content quality

## Inputs

- **Required**: Path to the SKILL.md file to refactor
- **Optional**: Target line count (default: aim for 80% of the 500-line limit, i.e., ~400 lines)
- **Optional**: Whether to create `references/EXAMPLES.md` (default: yes, if extractable content exists)
- **Optional**: Whether to split into multiple skills (default: no, prefer extraction first)

## Procedure

### Step 1: Measure Current Line Count and Identify Bloat Sources

Read the skill and create a section-by-section line budget to identify where the bloat is.

```bash
# Total line count
wc -l < skills/<skill-name>/SKILL.md

# Line count per section (approximate)
grep -n "^## \|^### " skills/<skill-name>/SKILL.md
```

Classify bloat sources:
- **Extractable**: Code blocks >15 lines, full configuration examples, multi-variant examples
- **Splittable**: Compound procedure steps doing 2+ unrelated operations
- **Trimable**: Redundant explanations, overly verbose context sentences
- **Structural**: Ad-hoc sections not in the standard six-section structure

**Expected:** A line budget showing which sections are over-sized and which bloat category applies to each. The largest sections are the primary refactoring targets.

**On failure:** If the skill is under 500 lines and no structural issues are apparent, this skill may not be needed. Verify the refactoring request is justified before proceeding.

### Step 2: Extract Code Blocks to references/EXAMPLES.md

Move code blocks longer than 15 lines to a `references/EXAMPLES.md` file, leaving brief inline snippets (3-10 lines) in the main SKILL.md.

1. Create the references directory:
   ```bash
   mkdir -p skills/<skill-name>/references/
   ```

2. For each extractable code block:
   - Copy the full code block to `references/EXAMPLES.md` under a descriptive heading
   - Replace the code block in SKILL.md with a brief 3-5 line snippet
   - Add a cross-reference: `See [EXAMPLES.md](references/EXAMPLES.md#heading) for the complete configuration.`

3. Structure `references/EXAMPLES.md` with clear headings:
   ```markdown
   # Examples

   ## Example 1: Full Configuration

   Complete configuration file for [context]:

   \```yaml
   # ... full config here ...
   \```

   ## Example 2: Multi-Variant Setup

   ### Variant A: Development
   \```yaml
   # ... dev config ...
   \```

   ### Variant B: Production
   \```yaml
   # ... prod config ...
   \```
   ```

**Expected:** All code blocks >15 lines are extracted. The main SKILL.md retains brief inline snippets for readability. Cross-references link to the extracted content. `references/EXAMPLES.md` is well-organized with descriptive headings.

**On failure:** If extracting code blocks does not reduce the line count sufficiently (still over 500), proceed to Step 3 for procedure splitting. If the skill has very few code blocks (e.g., a natural-language skill), focus on Steps 3 and 4 instead.

### Step 3: Split Compound Procedures into Focused Steps

Identify procedure steps that perform multiple unrelated operations and split them.

Signs of a compound step:
- The step title contains "and" (e.g., "Configure Database and Set Up Caching")
- The step has multiple Expected/On failure blocks (or should have)
- The step is longer than 30 lines
- The step could be skipped or done in a different order from its sub-parts

For each compound step:
1. Identify the distinct operations within the step
2. Create a new `### Step N:` for each operation
3. Renumber subsequent steps
4. Ensure each new step has its own Expected and On failure blocks
5. Add transition context between new steps

**Expected:** Each procedure step does one thing. No step exceeds 30 lines. Step count may increase but each step is independently verifiable.

**On failure:** If splitting a step creates steps that are too granular (e.g., 20+ total steps), consider grouping related micro-steps under a single step with numbered sub-steps instead. The sweet spot is 5-12 procedure steps.

### Step 4: Add Cross-References from SKILL.md to Extracted Content

Ensure the main SKILL.md maintains readability and discoverability after extraction.

For each extraction:
1. The inline snippet in SKILL.md should be self-sufficient for the common case
2. The cross-reference should explain what additional content is available
3. Use relative paths: `[EXAMPLES.md](references/EXAMPLES.md#section-anchor)`

Cross-reference patterns:
- After a brief code snippet: `See [EXAMPLES.md](references/EXAMPLES.md#full-configuration) for the complete configuration with all options.`
- For multi-variant examples: `See [EXAMPLES.md](references/EXAMPLES.md#variants) for development, staging, and production variants.`
- For extended troubleshooting: `See [EXAMPLES.md](references/EXAMPLES.md#troubleshooting) for additional error scenarios.`

**Expected:** Every extraction has a corresponding cross-reference. A reader can follow the main SKILL.md for the common case and drill into references for details.

**On failure:** If cross-references make the text flow awkward, consolidate multiple references into a single note at the end of the procedure step: `For extended examples including [X], [Y], and [Z], see [EXAMPLES.md](references/EXAMPLES.md).`

### Step 5: Verify Line Count After Refactoring

Re-measure the SKILL.md line count after all changes.

```bash
# Check main SKILL.md
lines=$(wc -l < skills/<skill-name>/SKILL.md)
[ "$lines" -le 500 ] && echo "SKILL.md: OK ($lines lines)" || echo "SKILL.md: STILL OVER ($lines lines)"

# Check references file if created
if [ -f skills/<skill-name>/references/EXAMPLES.md ]; then
  ref_lines=$(wc -l < skills/<skill-name>/references/EXAMPLES.md)
  echo "EXAMPLES.md: $ref_lines lines"
fi

# Total content
echo "Total content: $((lines + ${ref_lines:-0})) lines"
```

**Expected:** SKILL.md is under 500 lines. Ideally under 400 lines to leave room for future growth. The `references/EXAMPLES.md` has no line limit.

**On failure:** If still over 500 lines after extraction and splitting, consider whether the skill should be decomposed into two separate skills. A skill covering too much ground is a sign of scope creep. Use `create-skill` to author the second skill and update Related Skills cross-references in both.

### Step 6: Validate All Sections Still Present

After refactoring, verify the skill still has all required sections and the frontmatter is intact.

Run the `review-skill-format` checklist:
1. YAML frontmatter parses correctly
2. All six required sections present (When to Use, Inputs, Procedure, Validation, Common Pitfalls, Related Skills)
3. Every procedure step has Expected and On failure blocks
4. No orphaned cross-references (all links resolve)

```bash
# Quick section check
for section in "## When to Use" "## Inputs" "## Procedure" "## Common Pitfalls" "## Related Skills"; do
  grep -q "$section" skills/<skill-name>/SKILL.md && echo "$section: OK" || echo "$section: MISSING"
done
grep -qE "## Validation( Checklist)?" skills/<skill-name>/SKILL.md && echo "Validation: OK" || echo "Validation: MISSING"
```

**Expected:** All sections present. No content was accidentally deleted during extraction. Cross-references in SKILL.md resolve to actual headings in EXAMPLES.md.

**On failure:** If a section was accidentally removed, restore it from git history: `git diff skills/<skill-name>/SKILL.md` to see what changed. If cross-references are broken, verify the heading anchors in EXAMPLES.md match the links in SKILL.md (GitHub-flavored markdown anchor rules: lowercase, hyphens for spaces, strip punctuation).

## Validation

- [ ] SKILL.md line count is 500 or fewer
- [ ] All code blocks in SKILL.md are 15 lines or fewer
- [ ] Extracted content is in `references/EXAMPLES.md` with descriptive headings
- [ ] Every extraction has a cross-reference in the main SKILL.md
- [ ] No compound procedure steps remain (each step does one thing)
- [ ] All six required sections are present after refactoring
- [ ] Every procedure step has **Expected:** and **On failure:** blocks
- [ ] YAML frontmatter is intact and parseable
- [ ] Cross-reference links resolve to actual headings in EXAMPLES.md
- [ ] `review-skill-format` validation passes on the refactored skill

## Common Pitfalls

- **Extracting too aggressively**: Moving all code to references makes the main SKILL.md unreadable. Keep 3-10 line snippets inline for the common case. Only extract blocks that are >15 lines or show multiple variants.
- **Broken anchor links**: GitHub-flavored markdown anchors are case-sensitive in some renderers. Use lowercase headings in EXAMPLES.md and match exactly in cross-references. Test with `grep -c "heading-text" references/EXAMPLES.md`.
- **Losing Expected/On failure during splits**: When splitting compound steps, ensure each new step gets its own Expected and On failure blocks. It is easy to leave one step without these blocks after a split.
- **Creating too many tiny steps**: Splitting should produce 5-12 procedure steps. If you end up with 15+, you have split too aggressively. Merge related micro-steps back into logical groups.
- **Forgetting to update references/EXAMPLES.md headings**: If you rename a section in EXAMPLES.md, all cross-reference anchors in SKILL.md must be updated. Grep for the old anchor name to catch all references.

## Related Skills

- `review-skill-format` — Run format validation after refactoring to confirm the skill is still compliant
- `update-skill-content` — Content updates are often the trigger for structural refactoring when they push a skill over the line limit
- `create-skill` — Reference the canonical structure when deciding how to organize extracted content
- `evolve-skill` — When a skill needs to be split into two separate skills, use evolution to create the derivative
