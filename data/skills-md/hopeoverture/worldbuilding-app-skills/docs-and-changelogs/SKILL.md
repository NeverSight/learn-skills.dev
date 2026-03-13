---
name: docs-and-changelogs
description: Generates comprehensive changelogs from Conventional Commits, maintains CHANGELOG.md files, and scaffolds project documentation like PRD.md or ADR.md. This skill should be used when creating changelogs, generating release notes, maintaining version history, documenting architectural decisions, or scaffolding project requirements documentation. Use for changelog generation, release notes, version documentation, ADR, PRD, or technical documentation.
---

# Documentation and Changelogs

Generate and maintain project documentation including changelogs, architectural decision records, and product requirement documents.

## Overview

To manage project documentation effectively:

1. Generate changelogs from git commit history using Conventional Commits
2. Maintain CHANGELOG.md with semantic versioning
3. Create architectural decision records (ADR) for significant decisions
4. Scaffold product requirement documents (PRD) for new features
5. Automate documentation updates as part of release process

## Changelog Generation

To generate changelogs from Conventional Commits:

1. Parse git commit history for conventional commit messages
2. Categorize commits by type (feat, fix, chore, docs, etc.)
3. Group by version/release using git tags
4. Format according to Keep a Changelog standards
5. Append to existing CHANGELOG.md or create new file

Use `scripts/generate_changelog.py` to automate changelog generation from commit history.

### Conventional Commits Format

Follow this commit message structure:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

**Breaking Changes:**
- Add `BREAKING CHANGE:` in footer or `!` after type
- Example: `feat!: redesign entity schema structure`

## CHANGELOG.md Maintenance

To maintain changelog file:

1. Structure with sections: Unreleased, versioned releases
2. Use semantic versioning (MAJOR.MINOR.PATCH)
3. Group changes by category (Added, Changed, Deprecated, Removed, Fixed, Security)
4. Include links to commits and pull requests
5. Add release dates in ISO format (YYYY-MM-DD)

Consult `references/changelog-format.md` for detailed formatting guidelines and examples.

## Architectural Decision Records (ADR)

To create architectural decision records:

1. Use `scripts/create_adr.py` to scaffold new ADR file
2. Number ADRs sequentially (0001-title.md, 0002-title.md)
3. Include standard sections: Context, Decision, Consequences
4. Document alternatives considered
5. Reference related ADRs

Use `assets/adr-template.md` as starting point for new ADRs.

### ADR Structure

Standard ADR sections:

- **Title**: Short, descriptive name
- **Status**: Proposed, Accepted, Deprecated, Superseded
- **Context**: What problem are we solving?
- **Decision**: What did we decide to do?
- **Consequences**: What are the tradeoffs and impacts?
- **Alternatives Considered**: What other options were evaluated?

## Product Requirement Documents (PRD)

To scaffold product requirement documents:

1. Use `scripts/create_prd.py` to generate PRD template
2. Define problem statement and goals
3. List functional and non-functional requirements
4. Include user stories and acceptance criteria
5. Document technical constraints and dependencies

Reference `assets/prd-template.md` for comprehensive PRD structure.

### PRD Sections

Standard PRD components:

- **Overview**: High-level description
- **Problem Statement**: What problem are we solving?
- **Goals and Non-Goals**: Scope definition
- **User Stories**: Who, what, why format
- **Requirements**: Functional and non-functional
- **Design Considerations**: UI/UX, architecture
- **Success Metrics**: How to measure success
- **Timeline**: Development phases

## Implementation Steps

### Generate Changelog from Commits

To generate changelog:

1. **Collect Commits**
   ```bash
   python scripts/generate_changelog.py --since v1.0.0
   ```

2. **Categorize Changes**
   - Parse commit messages for conventional commit types
   - Extract breaking changes
   - Group by scope if present

3. **Format Output**
   - Generate markdown with appropriate headings
   - Link to commits and PRs
   - Add version header with date

4. **Update CHANGELOG.md**
   - Prepend new version section
   - Maintain existing content
   - Update "Unreleased" section

### Create New ADR

To document architectural decision:

1. **Generate ADR File**
   ```bash
   python scripts/create_adr.py "use postgresql for entity storage"
   ```

2. **Fill Template**
   - Document context and constraints
   - Explain decision rationale
   - List consequences and tradeoffs

3. **Review and Commit**
   - Get team feedback
   - Update status to "Accepted"
   - Link from main architecture docs

### Scaffold New PRD

To create product requirements:

1. **Generate PRD Template**
   ```bash
   python scripts/create_prd.py "timeline visualization feature"
   ```

2. **Complete Sections**
   - Define problem and goals
   - Write user stories
   - List requirements

3. **Review with Stakeholders**
   - Get product team input
   - Validate technical feasibility
   - Refine scope and requirements

## Automation

To automate documentation updates:

### Release Workflow Integration

Add to `.github/workflows/release.yml`:

```yaml
- name: Generate changelog
  run: python scripts/generate_changelog.py --output CHANGELOG.md

- name: Commit changelog
  run: |
    git config user.name github-actions
    git config user.email github-actions@github.com
    git add CHANGELOG.md
    git commit -m "docs: update changelog for ${{ github.ref_name }}"
```

### Pre-commit Hook

Add to `.git/hooks/commit-msg`:

```bash
#!/bin/bash
# Validate conventional commit format
python scripts/validate_commit_msg.py "$1"
```

## Documentation Structure

Organize project documentation:

```
docs/
├── CHANGELOG.md           # Version history
├── ADR/                   # Architectural decisions
│   ├── 0001-use-nextjs.md
│   └── 0002-database-choice.md
├── PRD/                   # Product requirements
│   ├── timeline-feature.md
│   └── entity-relationships.md
└── api/                   # API documentation
    └── endpoints.md
```

## Best Practices

### Changelog

- Write for users, not developers
- Use present tense ("Add" not "Added")
- Link to relevant issues/PRs
- Highlight breaking changes prominently
- Keep entries concise and clear

### ADR

- Write when decision is made, not after
- Document alternatives considered
- Be honest about tradeoffs
- Update status if decision changes
- Link related ADRs

### PRD

- Start with user needs, not solutions
- Include success metrics
- Define scope clearly (goals and non-goals)
- Get stakeholder buy-in early
- Update as requirements evolve

## Version Management

To manage semantic versioning:

1. **MAJOR**: Breaking changes (incompatible API changes)
2. **MINOR**: New features (backward-compatible)
3. **PATCH**: Bug fixes (backward-compatible)

Use `scripts/bump_version.py` to update version across package.json, changelog, and tags.

## Release Notes

To generate release notes:

1. Extract relevant changelog section
2. Add highlights and notable changes
3. Include upgrade instructions if needed
4. Link to full changelog
5. Publish to GitHub releases

Use `scripts/generate_release_notes.py` to create formatted release notes from changelog.

## Troubleshooting

Common issues:

- **Commits Not Categorized**: Ensure commits follow Conventional Commits format
- **Missing Version**: Tag releases in git with semantic version numbers
- **Duplicate Entries**: Check for merge conflicts in CHANGELOG.md
- **Broken Links**: Verify commit SHAs and PR numbers are correct
