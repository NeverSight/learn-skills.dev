---
name: plan-builder
description: Write implementation plans with appropriate templates based on complexity. Use when planning features or changes. Provides minimal, standard, and full templates for different scope levels.
allowed-tools: Read Write Edit
disable-model-invocation: true
---

# Plan Builder

Write implementation plans using the appropriate template based on complexity.

## Template Selection

| Complexity | When to Use | Template |
|------------|-------------|----------|
| **Minimal** | Simple bugs, small improvements, clear single-file changes | `references/minimal.md` |
| **Standard** | Most features, complex bugs, team collaboration | `references/standard.md` |
| **Comprehensive** | Major features, architectural changes, multi-phase work | `references/comprehensive.md` |

## Selection Criteria

### Use Minimal When
- Fix is obvious and localized
- Single file or 2-3 related files
- No architectural decisions needed
- Clear acceptance criteria from description

### Use Standard When (Default)
- Multiple components affected
- Requires research or external docs
- Team needs context for review
- Has dependencies or risks

### Use Comprehensive When
- New system or major feature
- Multiple phases of work
- Architectural decisions required
- Cross-cutting concerns (security, performance)
- Involves multiple teams or stakeholders

## Plan Output

Write plans to: `docs/plans/[YYYYMMDDHHMMSS]_<title>.md`

Include in every plan:
- Research findings with file paths (e.g., `src/models/user.rb:42`)
- External documentation URLs
- Related issues/PRs if known
- **Acceptance Criteria** from user input (populated from blueprint Step 2)

## Conditional Sections

### UI Features
Include "Design System Reference" section when feature involves:
- Pages, components, forms, buttons, modals
- Visual design elements

### DevOps Features
Include "Infrastructure Context" section when feature involves:
- Terraform/OpenTofu, Ansible, cloud resources
- Docker, CI/CD, infrastructure

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Use comprehensive for simple bugs | Match template to actual complexity |
| Skip Acceptance Criteria | Always include testable criteria |
| Leave placeholder text | Fill all sections or remove them |
| Over-plan obvious changes | Minimal template exists for a reason |
