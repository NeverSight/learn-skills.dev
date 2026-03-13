---
name: skill-reviewer-and-enhancer
description: This skill should be used when reviewing, auditing, or improving existing Claude Code skills to ensure they follow Anthropic best practices, have proper structure, use current domain-specific patterns, and include all necessary resources. It analyzes skill quality, identifies gaps, suggests improvements, and can automatically enhance skills with updated best practices. Trigger terms include review skill, audit skill, improve skill, enhance skill, update skill, check skill quality, skill best practices, fix skill, optimize skill, validate skill structure.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Skill Reviewer and Enhancer

Review, audit, and enhance existing Claude Code skills to ensure they follow Anthropic best practices and current domain-specific patterns.

## Overview

To improve skill quality and ensure adherence to official standards, this skill performs comprehensive analysis of existing skills, identifies structural issues, verifies domain-specific best practices, and automatically applies improvements.

## When to Use This Skill

Apply this skill when:
- Reviewing an existing skill for quality and compliance
- Auditing skills before deployment to production
- Updating skills to follow latest Anthropic guidelines
- Ensuring skills use current framework/library patterns
- Identifying missing resources or incomplete implementations
- Enhancing skill descriptions for better discoverability
- Fixing structural or formatting issues
- Modernizing outdated skill instructions

## Step 1: Locate and Read the Skill

To begin the review process:

1. Ask user for the skill path or name if not provided
2. Verify the skill directory exists
3. Read the SKILL.md file completely
4. Note the skill's category and purpose

```bash
# Find skill
ls skills/[category]/[skill-name]/SKILL.md

# Read skill
Read: skills/[category]/[skill-name]/SKILL.md
```

## Step 2: Analyze Skill Structure

To verify proper skill structure, check for:

### Frontmatter Validation

**Required Fields:**
- `name`: Must be present, hyphen-case, no angle brackets
- `description`: Must be present, third-person voice, includes trigger terms, under 1024 characters

**Optional Fields:**
- `allowed-tools`: Present for read-only/analysis skills

**Validation Script:**
```bash
python scripts/analyze_skill_structure.py --skill skills/[category]/[skill-name]
```

### Name Convention Check

Verify name follows hyphen-case:
- [OK] Correct: `skill-reviewer-and-enhancer`, `nextjs-fullstack-scaffold`
- [WRONG] Incorrect: `SkillReviewer`, `skill_reviewer`, `skillReviewer`

Check for invalid patterns:
- Starts or ends with hyphen
- Contains consecutive hyphens (`--`)
- Contains uppercase letters
- Contains underscores or other special characters

### Description Quality Check

Verify description:
- **Voice**: Uses third-person ("This skill should be used when...")
- **Content**: Explains WHAT it does and WHEN to use it
- **Trigger Terms**: Includes specific keywords users would search for
- **Length**: Under 1024 characters
- **Format**: No angle brackets, proper grammar

## Step 3: Review Instruction Style

To verify proper instruction format, scan the SKILL.md body for:

### Imperative Form Check

Instructions should use imperative/infinitive form:
- [OK] Correct: "To create a form, use the generator script"
- [OK] Correct: "Generate schemas using the Zod validator"
- [WRONG] Incorrect: "You should create forms using the generator"
- [WRONG] Incorrect: "You can generate schemas with Zod"

Use Grep to find second-person usage:
```bash
Grep: pattern="\\b[Yy]ou\\b" path="skills/[category]/[skill-name]/SKILL.md" output_mode="content"
```

Flag any instances for correction.

### Section Structure Check

Verify logical organization:
- Overview/Introduction
- When to Use (optional but recommended)
- Prerequisites (if applicable)
- Step-by-step implementation
- Resource references (scripts, references, assets)
- Best practices
- Troubleshooting (optional)

## Step 4: Verify Domain-Specific Best Practices

To ensure the skill follows current best practices for its domain, consult the appropriate reference:

### Development Skills
For Next.js, React, TypeScript, database skills, check:
- Uses latest framework versions (Next.js 15/16, React 19)
- Follows Server Components patterns
- Uses App Router (not Pages Router)
- Implements proper TypeScript types
- Uses modern tooling (Vite, Vitest, ESM)

Consult `references/nextjs-best-practices.md` for detailed checks.

### Testing Skills
For testing-related skills, check:
- Uses modern test runners (Vitest, not Jest)
- Uses Testing Library patterns
- Implements accessibility testing
- Follows AAA pattern (Arrange, Act, Assert)
- Uses proper mocking strategies

Consult `references/testing-best-practices.md` for detailed checks.

### UI Component Skills
For UI and component skills, check:
- Uses shadcn/ui patterns correctly
- Implements accessibility (ARIA, semantic HTML)
- Follows Tailwind CSS conventions
- Uses proper composition patterns
- Implements dark mode support

Consult `references/ui-best-practices.md` for detailed checks.

### Database Skills
For database and ORM skills, check:
- Uses Prisma 5+ patterns
- Implements proper connection pooling
- Uses prepared statements/parameterized queries
- Implements RLS for Supabase
- Uses proper migration patterns

Consult `references/database-best-practices.md` for detailed checks.

### Security Skills
For security-related skills, check:
- Follows OWASP guidelines
- Implements proper authentication patterns
- Uses secure session management
- Implements CSRF protection
- Uses Content Security Policy
- Validates and sanitizes inputs

Consult `references/security-best-practices.md` for detailed checks.

## Step 5: Check Resource References

To verify bundled resources are properly referenced:

### Scripts Directory
Check if skill references scripts and whether they exist:
```bash
Grep: pattern="scripts/" path="skills/[category]/[skill-name]/SKILL.md" output_mode="content"
Glob: pattern="skills/[category]/[skill-name]/scripts/*"
```

Verify:
- Scripts mentioned in SKILL.md exist in scripts/ directory
- Scripts have proper documentation
- Scripts are executable (Python/Bash)
- Usage examples are provided

### References Directory
Check if skill references documentation:
```bash
Grep: pattern="references/" path="skills/[category]/[skill-name]/SKILL.md" output_mode="content"
Glob: pattern="skills/[category]/[skill-name]/references/*"
```

Verify:
- References mentioned exist
- Large documents (>5k words) use grep patterns for selective loading
- References are up-to-date with current practices

### Assets Directory
Check if skill references templates or output files:
```bash
Grep: pattern="assets/" path="skills/[category]/[skill-name]/SKILL.md" output_mode="content"
Glob: pattern="skills/[category]/[skill-name]/assets/*"
```

Verify:
- Assets mentioned exist
- Templates are properly formatted
- File names are descriptive

## Step 6: Generate Improvement Report

To create a comprehensive review report, use the template from `assets/review-report-template.md`:

```markdown
# Skill Review Report: [Skill Name]

**Skill Path:** skills/[category]/[skill-name]
**Review Date:** [Date]
**Reviewer:** Claude Code (skill-reviewer-and-enhancer)

## Overall Assessment

**Grade:** [A/B/C/D/F]
**Status:** [Production Ready / Needs Minor Fixes / Needs Major Revision]

## Structural Compliance

### Frontmatter
- [x] Name present and valid
- [x] Description present and well-formatted
- [ ] allowed-tools specified (if applicable)

### Naming Convention
- [x] Uses hyphen-case
- [ ] Issue: Contains uppercase/invalid characters

### Description Quality
- [x] Third-person voice
- [x] Includes trigger terms
- [x] Under 1024 characters
- [ ] Issue: Missing WHEN to use explanation

## Instruction Style

### Imperative Form
- [x] Uses verb-first instructions
- [ ] Issue: Found 5 instances of "you should" (lines: 45, 67, 89, 102, 134)

**Recommended Changes:**
```
Line 45: "You should use the script" → "Use the script"
Line 67: "You can generate forms" → "Generate forms" or "To generate forms"
```

## Domain-Specific Best Practices

### [Domain] Patterns
- [x] Uses current framework version
- [x] Follows recommended patterns
- [ ] Issue: References deprecated API (NextAuth v3, should use v5)
- [ ] Issue: Uses Pages Router patterns (should use App Router)

**Recommended Updates:**
[Specific suggestions for domain improvements]

## Resource Completeness

### Scripts
- [ ] Script `generate_form.py` mentioned but not found
- [x] Script `validate_schema.py` exists and documented

### References
- [x] All references exist
- [ ] `api-patterns.md` is outdated (2022 patterns)

### Assets
- [x] All assets exist and properly formatted

## Suggested Improvements

### Critical (Must Fix)
1. **Fix second-person usage**: Replace 5 instances with imperative form
2. **Add missing script**: Create `generate_form.py` or remove reference
3. **Update deprecated API**: Replace NextAuth v3 with v5 patterns

### Recommended (Should Fix)
1. **Enhance description**: Add more trigger terms related to [domain]
2. **Update reference**: Modernize `api-patterns.md` with 2025 patterns
3. **Add troubleshooting**: Include common error scenarios

### Optional (Nice to Have)
1. **Add examples**: Include more code examples for common use cases
2. **Expand prerequisites**: Document required dependencies
3. **Add related skills**: Link to complementary skills

## Modernization Opportunities

1. **Framework Updates**: Update from Next.js 14 to Next.js 15/16
2. **Tooling Updates**: Replace Jest with Vitest
3. **Pattern Updates**: Use Server Actions instead of API routes
4. **Type Safety**: Add more TypeScript examples

## Automated Fixes Available

The following fixes can be applied automatically:
- [ ] Convert "you" to imperative form (5 instances)
- [ ] Update frontmatter format
- [ ] Fix hyphenation in name
- [ ] Add missing allowed-tools field

**Apply automated fixes?** (Yes/No)
```

## Step 7: Apply Improvements (If Approved)

To apply improvements to the skill, proceed with user approval:

### Automated Fixes

For structural and style issues:

**Fix Second-Person Usage:**
```typescript
// Replace patterns like:
"You should use" → "Use"
"You can generate" → "Generate" or "To generate"
"You need to configure" → "Configure" or "To configure"
"You will see" → "This displays" or "This shows"
"You have to install" → "Install"
```

Use Edit tool to apply changes:
```bash
Edit: file_path="skills/[category]/[skill-name]/SKILL.md"
       old_string="You should use the generator script"
       new_string="Use the generator script"
```

**Fix Frontmatter:**
Add missing fields or correct format:
```yaml
---
name: skill-name-in-hyphen-case
description: Third-person description with trigger terms under 1024 chars.
allowed-tools: Read, Grep, Glob  # For read-only skills
---
```

**Fix Name Convention:**
If name uses wrong format, update both frontmatter and directory:
1. Update name in frontmatter
2. Notify user directory rename needed (cannot be done automatically)

### Domain-Specific Updates

For framework/library updates:

**Update Next.js Patterns:**
- Replace `pages/` with `app/` directory examples
- Replace `getServerSideProps` with Server Components
- Replace API routes with Server Actions (where appropriate)
- Update to Next.js 15/16 syntax

**Update Testing Patterns:**
- Replace Jest with Vitest configuration
- Update Testing Library imports
- Use modern assertion syntax
- Add accessibility testing with axe

**Update Database Patterns:**
- Update Prisma to v5 syntax
- Add proper connection pooling
- Use latest Supabase patterns
- Implement RLS examples

**Update Security Patterns:**
- Use latest OWASP recommendations
- Update CSP directives
- Use modern auth patterns (NextAuth v5, Supabase Auth)
- Add secure header configurations

### Resource Creation

For missing resources:

**Create Missing Scripts:**
Use templates from `assets/script-templates/` to generate placeholder scripts:
```python
#!/usr/bin/env python3
"""
Script for [skill-name]: [purpose]
"""

def main():
    # Implementation here
    pass

if __name__ == "__main__":
    main()
```

**Create Missing References:**
Generate reference documents with appropriate content:
```markdown
# [Topic] Best Practices

## Overview
[Introduction to the topic]

## Patterns
[Common patterns and examples]

## Anti-Patterns
[What to avoid]

## Resources
[External references]
```

**Create Missing Assets:**
Generate template files as needed for the skill's purpose.

## Step 8: Validate Enhanced Skill

To verify improvements, run validation:

```bash
python scripts/quick_validate.py skills/[category]/[skill-name]
```

Confirm:
- Validation passes
- Frontmatter is correct
- Name follows convention
- Description is well-formatted
- Instructions use imperative form
- Resources are referenced correctly
- Domain best practices followed

## Step 9: Generate Enhancement Summary

To document changes made, create a summary:

```markdown
# Skill Enhancement Summary

**Skill:** [name]
**Date:** [date]
**Changes Applied:** [count]

## Structural Fixes
- Fixed second-person usage (5 instances)
- Updated frontmatter format
- Added allowed-tools field

## Domain Updates
- Updated Next.js patterns to v15
- Replaced deprecated APIs
- Added modern code examples

## Resource Updates
- Created missing script: generate_form.py
- Updated reference: api-patterns.md
- Added asset: template.tsx

## Validation
[OK] Skill passes all validation checks
[OK] Ready for production use

## Next Steps
1. Review changes in SKILL.md
2. Test any new scripts
3. Update CATALOG.md if needed
4. Deploy to project or personal directory
```

## Best Practices for Skill Review

### Thoroughness
- Review entire SKILL.md, not just frontmatter
- Check all resource references
- Verify domain-specific patterns
- Test any scripts if possible

### Accuracy
- Consult official documentation for frameworks
- Use latest version numbers
- Verify deprecated APIs
- Check security recommendations

### Improvement Focus
- Prioritize critical structural issues
- Modernize outdated patterns
- Enhance discoverability with better descriptions
- Maintain backward compatibility when possible

### User Communication
- Clearly explain issues found
- Provide specific examples of problems
- Offer actionable recommendations
- Show before/after comparisons

## Common Issues and Fixes

### Issue: Second-Person Usage

**Problem:** Instructions use "you should" or "you can"

**Fix:** Convert to imperative form using Edit tool

### Issue: Outdated Framework Patterns

**Problem:** Skill references old API or deprecated patterns

**Fix:** Update to current version following official documentation

### Issue: Missing Resources

**Problem:** Skill references scripts/references/assets that don't exist

**Fix:** Either create placeholder resources or remove references

### Issue: Poor Description

**Problem:** Description doesn't include trigger terms or explain when to use

**Fix:** Enhance description with specific use cases and keywords

### Issue: Incomplete Instructions

**Problem:** Steps are vague or missing critical details

**Fix:** Add detailed substeps, examples, and edge case handling

## Resource Files

### scripts/analyze_skill_structure.py
Automated analysis tool that parses SKILL.md, validates frontmatter, checks naming conventions, and identifies structural issues.

### scripts/check_domain_patterns.py
Domain-specific pattern validator that checks for current best practices in Next.js, React, testing, databases, security, etc.

### scripts/apply_automated_fixes.py
Batch fix application tool that can automatically correct common issues like second-person usage, frontmatter format, and naming.

### references/nextjs-best-practices.md
Current Next.js patterns including App Router, Server Components, Server Actions, and modern configuration.

### references/testing-best-practices.md
Modern testing patterns with Vitest, React Testing Library, Playwright, and accessibility testing.

### references/ui-best-practices.md
shadcn/ui usage patterns, Tailwind CSS conventions, accessibility guidelines, and component composition.

### references/database-best-practices.md
Prisma ORM patterns, Supabase integration, RLS policies, and database security.

### references/security-best-practices.md
OWASP guidelines, authentication patterns, session management, CSRF protection, and secure headers.

### references/anthropic-skill-standards.md
Official Anthropic skill creation standards including structure, naming, voice, and resource organization.

### assets/review-report-template.md
Structured template for generating comprehensive skill review reports.

### assets/script-templates/
Python and Bash script templates for creating missing skill resources.

### assets/reference-templates/
Markdown templates for creating missing reference documentation.

## Implementation Checklist

When reviewing and enhancing skills:

- [ ] Read complete SKILL.md file
- [ ] Validate frontmatter structure
- [ ] Check naming convention
- [ ] Verify description quality
- [ ] Scan for second-person usage
- [ ] Verify section organization
- [ ] Check domain-specific best practices
- [ ] Verify all resource references
- [ ] Generate improvement report
- [ ] Get user approval for changes
- [ ] Apply automated fixes
- [ ] Apply domain-specific updates
- [ ] Create missing resources
- [ ] Validate enhanced skill
- [ ] Generate enhancement summary
- [ ] Offer to update CATALOG.md

## Integration with Development Workflow

Use this skill as part of:
- **Pre-deployment Review**: Before publishing skills
- **Quality Audit**: Regular skill inventory checks
- **Modernization**: Updating skills with new patterns
- **Onboarding**: Ensuring new skills meet standards
- **Maintenance**: Keeping skills current and accurate

## Continuous Improvement

After enhancing skills:
1. Document patterns found in multiple skills
2. Update reference documents with new best practices
3. Create reusable templates for common fixes
4. Share learnings in team documentation
5. Adjust review criteria based on findings
6. Schedule regular skill audits
