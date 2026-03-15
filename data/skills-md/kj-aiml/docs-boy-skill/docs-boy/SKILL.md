---
name: docs-boy
description: |
  Comprehensive project documentation generator and maintainer. Triggers when user asks to create docs, write documentation, update docs, generate changelog, create milestone, audit documentation, setup documentation for new project, or before commits to generate UPDATE-SUMMARY and changelog. Use proactively when significant code changes are made or new features are implemented.
---

# Docs-Boy: Project Documentation Skill

A comprehensive documentation skill that ensures consistent, well-structured project documentation with automated changelog generation and milestone tracking.

## Core Documentation Structure

Every project should have this structure in `/docs`:

```
/docs/
├── 01-System-Design.md        # Architecture overview
├── 02-Design-Patterns.md      # Patterns used in codebase
├── 03-Database-Design.md      # Schema and data models
├── 04-Tech-Stack.md           # Technologies and versions
├── 05-Project-Structure.md    # Directory organization
├── 06-API-Documentation.md    # API endpoints and contracts
├── 07-Setup-Installation.md   # Getting started guide
├── 08-Contribution-Guide.md   # How to contribute
├── 09-Design-System.md        # UI/UX guidelines
├── BRAND-GUIDELINES.md        # Brand identity (optional)
├── UPDATE-SUMMARY.md          # Latest changes summary
├── changelogs/
│   └── version-X.X.X.md       # Version history
└── milestone/
    └── feature-name/          # Active development tracking
```

---

## Workflow

### 1. Understand the Request

Identify what the user needs:
- **Create docs?** → Initialize full structure
- **Update docs?** → Analyze changes, update relevant files
- **Changelog?** → Generate from recent changes
- **Milestone?** → Create tracking plan
- **Pre-commit?** → Update UPDATE-SUMMARY and changelog
- **Audit?** → Check completeness against structure

### 2. Investigate Before Writing

**CRITICAL:** Always read the codebase before generating documentation.

1. **Check project type:**
   - `package.json` → Node.js/JavaScript
   - `requirements.txt` / `pyproject.toml` → Python
   - `Cargo.toml` → Rust
   - `go.mod` → Go

2. **Understand architecture:**
   - Read `README.md` for project overview
   - Check `src/` or `app/` for frontend structure
   - Check `server/`, `api/`, `backend/` for backend
   - Look at `docker-compose.yml`, `Dockerfile` for deployment

3. **Identify technologies:**
   - Check dependencies for frameworks (React, NestJS, etc.)
   - Look at config files (vite.config, tsconfig, etc.)
   - Note database schemas, API patterns

4. **Never invent or assume.** If something is unclear, ask the user.

### 3. Generate Documentation

Use templates from `references/templates.md` as starting points, but customize based on actual codebase findings.

### 4. Verify and Finalize

1. Re-read generated docs for accuracy
2. Ensure all file paths and code examples are correct
3. Check version numbers match `package.json` or equivalent
4. Verify no orphaned or outdated documentation

---

## Commands

| Command | Action |
|---------|--------|
| `docs init` | Initialize full docs structure for new project |
| `docs audit` | Check existing docs against required structure |
| `docs update` | Update docs based on recent code changes |
| `docs changelog` | Generate version changelog from recent changes |
| `docs milestone` | Create/update milestone tracking |
| `docs pre-commit` | Generate UPDATE-SUMMARY and changelog before commit |

---

## Pre-Commit Workflow

Before every commit, this skill should:

1. **Detect Changes:** Analyze staged files and recent modifications
2. **Update UPDATE-SUMMARY.md:** Summarize what changed
3. **Update/Create Changelog:** If version changed, create new changelog entry
4. **Review Milestone:** If working on milestone, update progress

---

## Writing Style Guide

### General Rules

1. **Be Concise:** Short sentences, bullet points
2. **Be Specific:** Include file paths, versions, concrete examples
3. **Use Status Icons:**
   - ✅ Completed/Done
   - ⏳ In Progress
   - ❌ Not Started/Planned
   - 🔨 Under Construction
4. **Include Version Info:** Note which version doc was last updated
5. **Date Format:** Full date (e.g., "February 25, 2026")

### Formatting

- **Headers:** `#` for title, `##` for sections, `###` for subsections
- **Code Blocks:** Always specify language (```typescript, ```bash)
- **Tables:** Use for structured data (versions, APIs, configs)
- **ASCII Diagrams:** Use for architecture visualizations

### Code Examples

Always include:
- File path as comment
- Brief description
- Complete, runnable examples

```typescript
// src/utils/example.ts
// Description of what this does

export function example() {
  // implementation
}
```

---

## Audit Checklist

When auditing documentation, verify:

- [ ] `/docs` directory exists at project root
- [ ] All numbered topics (01-09) exist
- [ ] BRAND-GUIDELINES.md exists (if branding defined)
- [ ] UPDATE-SUMMARY.md exists and is current
- [ ] `/docs/changelogs/` exists with version files
- [ ] `/docs/milestone/` exists for active development
- [ ] All docs follow writing style guide
- [ ] Version numbers are consistent across docs
- [ ] No orphaned or outdated documentation
- [ ] Code examples are accurate and runnable
- [ ] Architecture diagrams are current

---

## Usage Examples

```
User: "Create docs for this project"
→ Investigate codebase → Initialize full /docs structure with templates

User: "Check if my docs are complete"
→ Audit against required structure → Report missing/outdated files

User: "Create changelog for v1.2.0"
→ Analyze git diff → Generate version-1.2.0.md

User: "I'm about to commit these changes"
→ Update UPDATE-SUMMARY.md → Create changelog entry if needed

User: "Create milestone for auth feature"
→ Create /docs/milestone/auth-feature/ with plan.md
```

---

## Reference Files

For detailed templates and examples, see:
- `references/templates.md` - All documentation templates
- `references/changelog-format.md` - Changelog writing guide
- `references/milestone-format.md` - Milestone tracking guide