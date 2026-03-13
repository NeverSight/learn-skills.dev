---
name: development-workflow
description: Spec-driven development lifecycle — EARS requirements, technical design docs, implementation tracking, and contribution guidelines. Use when planning features, defining requirements, or managing project lifecycle.
license: Complete terms in LICENSE.txt
---

# Development Workflow

Structured approach to software development ensuring requirements are clearly defined, designs are meticulously planned, and implementations are thoroughly documented with proper contribution practices.

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

**Project Planning & Requirements:**
- Starting new features or phases of work
- Defining requirements using structured notation
- Creating technical designs and architecture documents
- Managing implementation plans from concept to completion
- Ensuring thorough documentation before coding
- Understanding project structure and existing patterns

**Repository Contributions:**
- Creating issues, commits, or pull requests in a repository
- Needing to follow repository guidelines before making contributions
- Creating PRs, pushing code, or following contribution workflows
- Following project-specific contribution guidelines

**Quality Assurance:**
- Ensuring code review standards are met
- Validating tests and requirements before implementation
- Managing project decisions and trade-offs documentation
- Tracking progress and blockers

## Part 1: Spec-Driven Development

### Core Artifacts

Maintain these artifacts throughout the project lifecycle:

| Artifact | Purpose | Location |
|----------|---------|----------|
| `requirements.md` | User stories and acceptance criteria in EARS notation | Project root or `/docs/requirements/` |
| `design.md` | Technical architecture, sequence diagrams, implementation considerations | Project root or `/docs/design/` |
| `tasks.md` | Detailed, trackable implementation plan | Project root or `/docs/planning/` |

### EARS Notation for Requirements

**EARS = Easy Approach to Requirements Syntax**

#### Basic EARS Patterns

**1. Universal Requirements**
Apply to all entities without condition
- "The system **shall** validate all user input."
- "Each user **shall** have a unique email address."

**2. State-Driven Requirements**
Apply only in specific system states
- "When the user is authenticated, the system **shall** display the dashboard."
- "If the payment fails, the system **shall** retry up to 3 times."

**3. Event-Driven Requirements**
Triggered by specific events
- "When the user clicks 'Submit', the system **shall** validate the form."
- "Upon receiving a new message, the chat application **shall** update the conversation view."

**4. Optional-Feature Requirements**
Describing optional or conditional features
- "The system **may** provide offline access if supported."
- "The user **may** choose to receive email notifications."

**5. Unwanted Behavior**
Specifying what should not happen
- "The system **shall not** store passwords in plain text."
- "The application **shall not** allow simultaneous sessions from different locations unless configured."

#### Complete EARS Example

```markdown
# User Authentication Requirements

## Universal Requirements
- U-001: The system **shall** require users to provide an email address and password for login.
- U-002: The system **shall** validate email addresses using RFC 5322 format.

## Event-Driven Requirements
- E-001: **When** the user clicks "Forgot Password", the system **shall** send a password reset link to the registered email.
- E-002: **Upon** successful authentication, the system **shall** generate a session token valid for 24 hours.

## State-Driven Requirements
- S-001: **If** the user has enabled two-factor authentication, the system **shall** prompt for the verification code.
- S-002: **When** the account is locked due to too many failed attempts, the system **shall** unlock it after 30 minutes.

## Unwanted Behavior
- N-001: The system **shall not** reveal whether an email address is registered during password reset.
- N-002: The system **shall not** allow the same account to be used from more than 3 IP addresses simultaneously.

## Optional Features
- O-001: The system **may** support social login providers (Google, Facebook, GitHub).
```

### Technical Design Documentation

```markdown
# Design: [Feature Name]

## Overview
High-level description of what this feature does and why it's needed.

## Architecture
### System Diagram
```
User → Frontend → API Gateway → Service → Database
                              ↓
                         Cache Layer
```

### Component Structure
```
src/
├── components/
│   └── FeatureName/
│       ├── FeatureComponent.tsx
│       ├── SubComponent.tsx
│       └── styles.css
├── services/
│   └── featureService.ts
├── api/
│   └── featureApi.ts
└── types/
    └── feature.types.ts
```

## Data Models

### entities/Feature.ts
```typescript
interface FeatureEntity {
  id: string;
  name: string;
  status: 'active' | 'inactive';
  createdAt: Date;
  // ... other fields
}
```

### API Contracts

#### POST /api/features
```typescript
interface CreateFeatureRequest {
  name: string;
  /* ... other fields */
}

interface CreateFeatureResponse {
  id: string;
  status: 'created';
}
```

## Error Handling
| Error Code | HTTP Status | Description |
|-----------|-------------|-------------|
| FEATURE_001 | 409 | Feature name already exists |
| FEATURE_002 | 400 | Invalid feature data |

## Sequence Diagram
```
User → Frontend: Click "Create Feature"
Frontend → API: POST /api/features
API → Validator: Validate data
Validator → API: Valid / Invalid
API → Database: Insert feature
Database → API: Created
API → Frontend: Return feature ID
Frontend → User: Show success message
```

## Security Considerations
- Authentication required for all mutations
- Input validation on all endpoints
- Rate limiting on create operations
- Audit logging for all changes

## Performance Considerations
- Caching strategy for read operations
- Database indexing requirements
- CDN for static assets

## Implementation Phases
1. Phase 1: Core CRUD operations
2. Phase 2: Validation and error handling
3. Phase 3: Caching layer
4. Phase 4: Testing and documentation
```

### Implementation Task Tracking

```markdown
# Tasks: [Feature Name] Implementation

## Phase 1: Foundation
- [ ] Setup project structure and dependencies
- [ ] Create base data models
- [ ] Configure database schema
- [ ] Setup API endpoints scaffolding

## Phase 2: Core Functionality
- [ ] Implement feature creation endpoint
- [ ] Implement feature retrieval endpoint
- [ ] Implement feature update endpoint
- [ ] Implement feature deletion endpoint

## Phase 3: Frontend Integration
- [ ] Build main component
- [ ] Integrate with API
- [ ] Add loading and error states
- [ ] Implement user feedback messages

## Phase 4: Testing
- [ ] Unit tests for service layer
- [ ] Integration tests for API
- [ ] Component tests for UI
- [ ] End-to-end tests with Playwright

## Phase 5: Deployment
- [ ] Create migration scripts
- [ ] Setup CI/CD pipeline
- [ ] Deploy to staging environment
- [ ] Conduct QA review
- [ ] Deploy to production

## Phase 6: Documentation
- [ ] Update API documentation
- [ ] Write user documentation
- [ ] Update changelog
```

---

## Part 2: Repository Contribution Guidelines

### Pre-Contribution Checklist

Before creating any PR or making changes:

```markdown
## Pre-Submission Checklist

### Repository Understanding
- [ ] Read README.md for project overview
- [ ] Read CONTRIBUTING.md for contribution rules
- [ ] Reviewed issue and PR templates
- [ ] Checked for existing related issues or PRs

### Environment Setup
- [ ] forked repository (if required)
- [ ] cloned repository locally
- [ ] setup development environment
- [ ] installed all dependencies

### Development Standards
- [ ] Understand coding style conventions
- [ ] Familiar with branching strategy
- [ ] Aware of commit message conventions
- [ ] Know testing requirements
```

### Issue Creation Workflow

#### When to Create Issues
- New feature requests
- Bug reports
- Documentation gaps
- Security vulnerabilities
- Performance concerns

#### Issue Template

```markdown
## Issue: [Brief Title]

### Type: [Feature Request / Bug Report / Question / Documentation]

### Priority: [Low / Medium / High / Critical]

### Description
[Detailed description of the issue or feature request]

### Reproduction Steps (for bugs)
1. [First step]
2. [Second step]
3. [Third step]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happened]

### Environment
- OS: [e.g., Windows 10, macOS 12.5]
- Browser: [e.g., Chrome 120, Firefox 115]
- Version: [If applicable]

### Additional Context
[Any other information that might be helpful]
- Screenshots
- Error messages
- Logs
```

### Branching Strategy

```markdown
## Branch Naming Convention

### Feature Branches
`feature/[JIRA-TICKET]/[short-description]`
Examples:
- feature/PROJ-123/user-authentication
- feature/PROJ-456/dark-mode-support

### Bugfix Branches
`bugfix/[JIRA-TICKET]/[issue-description]`
Examples:
- bugfix/PROJ-789/login-redirect-loop
- bugfix/PROJ-321/memory-leak-report

### Hotfix Branches (production issues)
`hotfix/[JIRA-TICKET]/[critical-description]`
Examples:
- hotfix/PROJ-999/security-vulnerability
- hotfix/PROJ-888/database-down

### Release Branches
`release/v[major].[minor]`
Examples:
- release/v1.2.0
- release/v2.0.0

### Branch Protection Rules
- Protect `main` and `develop` branches
- Require pull request reviews (at least 1 approval)
- Require status checks to pass (CI builds, tests)
- Require branches to be up-to-date before merging
```

### Commit Message Standards (Conventional Commits)

```markdown
## Conventional Commit Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type       | Purpose                        | Example                          |
|------------|--------------------------------|----------------------------------|
| `feat`     | New feature                     | `feat(auth): add OAuth2 support`   |
| `fix`      | Bug fix                         | `fix(api): resolve null reference`  |
| `docs`     | Documentation only              | `docs(readme): update setup guide`  |
| `style`    | Formatting/style (no logic)      | `style(ui): fix indentation`       |
| `refactor` | Code refactor (no feature/fix)   | `refactor(svc): extract helpers`  |
| `perf`     | Performance improvement          | `perf(db): add index on email`    |
| `test`     | Add/update tests                | `test(auth): add unit tests`      |
| `build`    | Build system/dependencies        | `build(ci): upgrade Node to v20`  |
| `ci`       | CI/config changes              | `ci(github): add workflow for PRs`|
| `chore`    | Maintenance/misc               | `chore(deps): update packages`    |
| `revert`   | Revert commit                 | `revert: feat(login)`             |

### Breaking Changes
```
feat(api)!: remove deprecated v1 endpoint

BREAKING CHANGE: v1 endpoints are no longer supported. Use v2.
```

### Good Commit Examples
```
feat(auth): add refresh token mechanism
- Implement JWT refresh tokens
- Add storage for access tokens
- Update token validation logic

fix(ui): resolve mobile navigation issue
- Mobile menu was not closing after clicking links
- Added event listener to handle link clicks
- Tested on iOS Safari and Chrome Mobile

docs(readme): update installation instructions
- Clarified Node.js version requirement
- Added troubleshooting section
```

### Bad Commit Examples (Don't use)
```
update 2
fixed bug
wip
changes
final
work in progress
```

### Commit Workflow
```bash
# Stage changes
git add .

# Interactive staging (optional)
git add -i

# Commit with good message
git commit -m "feat(auth): implement OAuth2 login"

# Or use multi-line for body and footer
git commit -m "fix(db): optimize query performance

Added composite index on user_email and created_at
Reduced query time from 500ms to 50ms

Closes issue #123"
```

---

## Part 3: Pull Request Process

### Creating Pull Requests

#### PR Checklist

```markdown
## Pull Request Checklist

### Before Submitting
- [ ] Branch is up-to-date with target branch
- [ ] Code compiles without errors
- [ ] All tests pass locally
- [ ] Linters pass without errors
- [ ] Documentation updated (README, API docs, code comments)
- [ ] Self-review completed

### PR Description
- [ ] Clear title following conventional commits
- [ ] Description explains "why" not just "what"
- [ ] Screenshots for UI changes included
- [ ] Breaking changes documented
- [ ] Related issues referenced (e.g., "Closes #123")
- [ ] Testing instructions provided

### Code Quality
- [ ] Follows project coding standards
- [ ] No commented-out code
- [ ] No console.log statements
- [ ] meaningful variable and function names
- [ ] No sensitive data exposed

### Testing
- [ ] New features tested
- [ ] Bug fixes verified
- [ ] Edge cases covered
- [ ] Manual testing completed as described
```

#### PR Template

```markdown
## Description
[Provide a brief description of the changes in this PR]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation
- [ ] Refactoring
- [ ] Performance improvement

## Issue
[Closes #xxx] or [Related to #xxx]

## Changes Made
### Main Changes
- [Describe the main changes implemented]

### Technical Details
[Any technical details reviewers should know]

### Breaking Changes
[Any breaking changes and migration steps]

## Testing
### Manual Testing Steps
1. [Step 1]
2. [Step 2]

### Automated Testing
- [ ] Unit tests added and passing
- [ ] Integration tests added and passing
- [ ] E2E tests added and passing

## Screenshots
[Include before/after screenshots for UI changes]

## Checklist
- [ ] I have read the contributing guidelines
- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code appropriately
- [ ] Changes have no linting errors
- [ ] All tests are passing
- [ ] Changes do not break existing functionality
```

### Code Review Guidelines

#### For Reviewers

```markdown
## Code Review Principles

### Be Constructive
- Focus on improving code, not criticizing it
- Provide specific examples and suggestions
- Ask questions rather than making demands
- Acknowledge good code and smart solutions

### Review Focus Areas

#### Correctness
- [ ] Logic is correct and handles edge cases
- [ ] Error handling is adequate
- [ ] No obvious bugs or race conditions
- [ ] API contracts are maintained

#### Code Quality
- [ ] Code is readable and maintainable
- [ ] Naming follows conventions
- [ ] Complexity is reasonable
- [ ] No code duplication

#### Architecture
- [ ] Follows established patterns
- [ ] Good separation of concerns
- [ ] Proper abstractions used
- [ ] No tight coupling

#### Security
- [ ] No security vulnerabilities
- [ ] Input validation present
- [ ] Authentication/authorization correct
- [ ] No sensitive data exposure

### Review Priority Comments
🔴 **Blocker**: Must be fixed before merge
🟡 **Concern**: Discuss before merge
🟢 **Suggestion**: Nice to have, not blocking
```

---

## Part 4: Documentation Standards

### Documentation Templates

#### Action Documentation
```markdown
### [TYPE] - [ACTION] - [TIMESTAMP]

**Objective**: [Goal being accomplished]

**Context**: [Current state, requirements, reference to prior steps]

**Decision**: [Approach chosen and rationale]

**Execution**: [Steps taken with parameters and commands]

**Output**: [Complete results, logs, metrics]

**Validation**: [Success verification and results]

**Next**: [Continuation plan to next action]
```

#### Decision Record
```markdown
### Decision - [TIMESTAMP]

**Decision**: [What was decided]

**Context**: [Situation and driving data]

**Options**:
- Option 1: [Description] - [Pros/Cons]
- Option 2: [Description] - [Pros/Cons]
- Option 3: [Description] - [Pros/Cons]

**Rationale**: [Why selected option is superior]

**Impact**: [Anticipated consequences]

**Review**: [Reassessment conditions]
```

#### Summary Formats

**Streamlined Action Log (for changelogs):**
`[TYPE][TIMESTAMP] Goal: [X] → Action: [Y] → Result: [Z] → Next: [W]`

**Quick Summary (for updates):**
**What**: [Brief description]
**Why**: [Context/rationale]
**How**: [Approach taken]
**Status**: [Current state]
**Next**: [Upcoming step]

---

## Part 5: Quality Gates

### Definition of Done

```markdown
## Definition of Done (DoD)

### Development
- [ ] Code written and committed
- [ ] Code follows project style guide
- [ ] Code compiles without errors
- [ ] No console errors or warnings
- [ ] Self-review completed

### Testing
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Manual testing completed
- [ ] Edge cases identified and handled
- [ ] Test coverage meets project threshold (>80%)

### Documentation
- [ ] README updated if API changed
- [ ] API documentation updated
- [ ] Code comments added/updated
- [ ] User documentation updated if needed

### Code Review
- [ ] Pull request created
- [ ] At least one approval received
- [ ] All review comments addressed
- [ ] CI/CD pipeline passes
- [ ] Merged to appropriate branch

### Deployment
- [ ] Deployment tested in staging
- [ ] Smoke tests passed
- [ ] Performance validated
- [ ] Monitoring/alerting configured
- [ ] Rollback procedure documented
```

### Quality Checklist

```markdown
## Code Quality Checklist

### Functionality
- [ ] All acceptance criteria met
- [ ] Requirements from design document fulfilled
- [ ] Edge cases handled
- [ ] Error states handled gracefully

### Usability
- [ ] User-friendly error messages
- [ ] Clear feedback for actions
- [ ] Accessible (keyboard, screen reader)
- [ ] Responsive design verified

### Performance
- [ ] Meet performance requirements
- [ ] No memory leaks
- [ ] Efficient algorithms used
- [ ] Appropriate caching

### Security
- [ ] Input validation
- [ ] Output encoding (prevent XSS)
- [ ] Authentication/authorization implemented
- [ ] No sensitive data in logs
- [ ] Dependencies audited and up-to-date

### Maintainability
- [ ] Code is readable
- [ ] Good variable/function names
- [ ] Appropriate abstractions
- [ ] No code duplication
- [ ] Adequate comments

### Testing
- [ ] Unit tests for critical paths
- [ ] Integration tests for API
- [ ] E2E tests for user flows
- [ ] Tests are reliable and not flaky
```

---

## Part 6: Project Lifecycle Management

### Phase-based Development

```markdown
## Development Phases

### Phase 1: Requirements & Planning
- Gather requirements from stakeholders
- Document in EARS notation
- Create technical design
- Identify risks and dependencies
- Estimate effort and timeline

### Phase 2: Development
- Set up feature branches
- Implement core functionality
- Write tests alongside code
- Code review and iteration

### Phase 3: Testing & QA
- Run automated tests
- Perform manual testing
- Conduct QA review
- Fix identified issues
- Performance testing

### Phase 4: Deployment
- Deploy to staging
- Execute smoke tests
- Get stakeholder approval
- Deploy to production
- Monitor for issues

### Phase 5: Post-Release
- Monitor metrics and logs
- Collect user feedback
- Address critical bugs
- Document lessons learned
- Update process improvements
```

## Development Workflow Best Practices

### Before Coding
- [ ] Requirements clearly defined and reviewed
- [ ] Technical design documented
- [ ] Dependencies identified
- [ ] Acceptance criteria established
- [ ] Testing strategy planned

### During Development
- [ ] Small, frequent commits
- [ ] Write tests alongside code
- [ ] Follow coding standards
- [ ] Continuous self-review
- [ ] Request early feedback

### Before Release
- [ ] All tests passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Security review (if needed)
- [ ] Release notes prepared

### After Release
- [ ] Monitor production carefully
- [ ] Be ready to rollback
- [ ] Document issues and fixes
- [ ] Update metrics and dashboards
- [ ] Conduct retrospective

---

## References & Resources

### Documentation
- [EARS Notation Reference](./references/ears-notation-reference.md) — Complete EARS requirement patterns with examples and traceability matrix
- [Design Doc Guide](./references/design-doc-guide.md) — Technical design document writing guide with ADR template

### Scripts
- [Create Spec Scaffold](./scripts/create-spec-scaffold.ps1) — PowerShell script to generate requirements, design, and tasks documents

### Examples
- [Feature Spec Example](./examples/feature-spec-example.md) — Complete spec-driven development example for User Authentication

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [devops-tooling](../devops-tooling/SKILL.md) | Git operations and CI/CD automation for the workflow |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Write specs and design docs within the workflow |
| [breaking-changes-management](../breaking-changes-management/SKILL.md) | Manage versioning during the release lifecycle |
| [code-quality](../code-quality/SKILL.md) | Code review and quality gates in the workflow |

---
