---
name: project-documentation
description: Create non-technical documentation for project features in the docs/ folder. Use when documenting completed features, writing feature documentation, explaining how features work, or when the user asks to document the project or create docs for non-developers.
---

# Project Feature Documentation

You write clear, non-technical documentation for project features that explains what they do, why they exist, and how they work - without diving into code specifics. Documentation is stored in the `docs/` folder as markdown files.

## Purpose

These docs serve two audiences:

1. **Non-developers** - Product managers, designers, stakeholders who need to understand features conceptually
2. **AI agents troubleshooting issues** - Provide context about intended behavior, business rules, and feature relationships when AI has code access but needs to understand what *should* happen

## Target Audience

Write in plain language that non-developers can understand, but include details that help AI agents working in the codebase quickly orient themselves to expected behavior and business logic.

## Feature Index (Recommended)

Create a `docs/README.md` that serves as both a feature inventory and navigation index. List features only after they've been documented.

**Good Example for formatting purposes**

```markdown
# Project Documentation

## Core Features

### [User Authentication](user-authentication.md)
**Related**: User Profile, Session Management
**Summary**: Account creation, login, password reset

### [Payment Processing](payment-processing.md)
**Related**: Order Management, Email Notifications
**Summary**: Stripe integration for payments, refunds, and disputes

### [Dashboard Analytics](dashboard-analytics.md)
**Related**: User Authentication (requires login)
**Summary**: Real-time metrics and reporting

## Secondary Features

### [Email Notifications](email-notifications.md)
**Related**: Most core features
**Summary**: SendGrid integration with queued processing

## Integrations

### [Stripe API](stripe-integration.md)
**Related**: Payment Processing
**Summary**: Payment gateway for transactions and webhooks
```

### Index Best Practices

**Add features to the index only after documenting them**. This keeps the index clean and ensures every listed feature has documentation.

**Include these fields**:
- Feature name - linked to documentation file
- Related features - dependencies and relationships
- Summary - one-line description

## Documentation Structure

Each feature gets its own markdown file in `docs/`. File names should be descriptive and lowercase with hyphens:

```
docs/
├── user-authentication.md
├── payment-processing.md
├── email-notifications.md
└── dashboard-analytics.md
```

## What Qualifies as a "Feature"?

A feature represents any significant user-facing behavior or system capability, including:

- **User-facing functionality** - Actions users can perform (login, submit forms, view reports)
- **Admin workflows** - Backend processes for managing the system (user management, content moderation)
- **Business rules and conditional logic** - Rules that govern behavior (approval workflows, eligibility checks)
- **Permissions and role-based behavior** - What different user types can/cannot do
- **Integrations with third-party services** - External APIs, payment gateways, email services
- **Background processing** - Cron jobs, scheduled tasks, queued operations
- **Automation** - Automatic actions triggered by events (auto-notifications, data sync)
- **Custom data flows** - How information moves through the system
- **Lifecycle behavior** - State transitions and what triggers them

If it affects user experience or system behavior, it's worth documenting.

## Feature Documentation Template

Use this structure for each feature:

```markdown
# [Feature Name]

## What It Does

[1-2 paragraph overview of what this feature accomplishes from the user's perspective]

## Why We Built It

[Explain the problem this solves or the need it fulfills]

## How It Works

[Step-by-step explanation of the feature's behavior and logic, without code details]

### Key Components

- **[Component 1]**: What it does
- **[Component 2]**: What it does
- **[Component 3]**: What it does

### Data Flow

[What information enters the feature, how it's transformed, and what comes out]

## User Experience

[Describe what users see and how they interact with this feature]

## Expected Behavior

### Success Scenarios
- **Scenario 1**: [Input] → [Expected Result]
- **Scenario 2**: [Input] → [Expected Result]

### Error Scenarios
- **When [condition]**: [Expected behavior/message]
- **When [condition]**: [Expected behavior/message]

## Business Rules

[Critical validation rules, constraints, and logic that must always be enforced]

**Examples:**
- Passwords must be 8+ characters with 1 number and 1 special character
- Users cannot delete items that are currently in use
- Refunds are only allowed within 30 days of purchase

## Dependencies

### Required Features/Systems
- [Feature/System]: Why it's needed

### Affected Features
- [Feature]: How this feature impacts it

### External Services
- [Service]: What it's used for

## Common Issues & Edge Cases

[Document known edge cases, gotchas, or areas that commonly cause confusion]

**Examples:**
- When the external API times out, the system should queue and retry
- If a user has multiple sessions, changes in one should reflect in all
- Empty state: what happens when there's no data to display

## Future Considerations

[Optional: Known limitations or planned enhancements]
```

## Writing Guidelines

### DO:
- **Use plain language** - avoid jargon and technical terms
- **Focus on behavior** - what happens, not how it's coded
- **Explain the "why"** - business logic and decision rationale
- **Use concrete examples** - specific scenarios with expected outcomes
- **Describe user flows** - "When a user does X, the system does Y"
- **Document edge cases** - what happens in unusual or error situations
- **Be specific about rules** - validation logic, business constraints, required conditions
- **Mention integrations** - what external services or systems are involved
- **List dependencies** - what this relies on and what relies on this
- **Document expected errors** - what error messages should appear when

### DON'T:
- **Reference code** - no function names, classes, or file paths
- **Include implementation details** - no database schemas, API endpoints, technical architecture
- **Use developer jargon** - no "middleware", "ORM", "serialization"
- **Make assumptions** - explain acronyms and domain terms
- **Be vague** - avoid "handles various cases" without explaining them

### Critical for AI Troubleshooting:
- **Document the "happy path"** - what should happen when everything works
- **Document error paths** - what should happen when things go wrong
- **Clarify business rules** - constraints that must ALWAYS be enforced
- **Note feature boundaries** - where one feature ends and another begins
- **Explain non-obvious logic** - anything that might seem like a bug but is intentional
- **Describe implicit behavior** - automatic assignments, default values, hidden triggers
- **Document configuration-dependent behavior** - what changes based on settings or user attributes

## When Code Isn't Enough

Some features have behavior that isn't obvious from reading code alone:

- **Historical context** - Why certain decisions were made
- **Business rules** - Logic based on stakeholder requirements
- **Implicit assumptions** - Default behaviors not explicitly coded
- **Edge case handling** - Decisions about unusual scenarios
- **Configuration-driven behavior** - Different behavior in different contexts

**When you encounter unclear behavior while documenting:**

1. **Note what's unclear** - Document the question you need answered
2. **Ask the user/SME** - Request clarification from someone who knows the business context
3. **Document the answer** - Add the clarified behavior to the documentation
4. **Be explicit** - Make the implicit behavior explicit in the docs

Example questions to ask SMEs:
- "When a user has multiple roles, which permissions take precedence?"
- "What should happen when the external API is down during checkout?"
- "Why do we auto-assign users to Team A instead of Team B?"
- "What's the business reason for the 30-day limit on refunds?"

## Example Documentation

**Good example:**

```markdown
# User Authentication

## What It Does

Allows users to create accounts and securely log in to access their personalized dashboard. Users can also reset their password if they forget it.

## Why We Built It

We needed a secure way to identify users and protect their personal data. Each user has unique settings and history that should only be accessible to them.

## How It Works

### Registration
When someone signs up, they provide an email address and create a password. The system checks that the email isn't already in use and that the password meets security requirements (at least 8 characters, one number, one special character). We send a verification email to confirm they own the email address.

### Login Process
Users enter their email and password. The system verifies these credentials match what's stored. If correct, they get access to their account. After 3 failed attempts, the account is temporarily locked for 15 minutes to prevent unauthorized access attempts.

### Password Reset
If a user forgets their password, they can request a reset link via email. The link is valid for 1 hour. Clicking it allows them to set a new password.

### Data Flow
Email + Password → Validation → Password Security Check → Store Account → Send Verification Email → User Clicks Link → Account Activated

## User Experience

- Registration form with email and password fields
- Validation messages appear in real-time (e.g., "Password too short")
- Verification email arrives within 1-2 minutes
- Login page with "Forgot Password?" link
- Error messages are helpful but don't reveal whether an email exists in the system

## Expected Behavior

### Success Scenarios
- **Valid registration**: User receives verification email within 2 minutes, can click link and access account
- **Valid login**: User enters correct credentials, immediately redirected to dashboard
- **Password reset request**: User receives reset link within 2 minutes, link works for 1 hour

### Error Scenarios
- **Duplicate email**: Show "An account with this email already exists" message
- **Weak password**: Show specific requirements not met (e.g., "Password must include a number")
- **Failed login (1-2 attempts)**: Show "Invalid email or password" message
- **Failed login (3 attempts)**: Show "Account locked for 15 minutes due to too many failed attempts"
- **Expired reset link**: Show "This reset link has expired. Please request a new one."
- **Unverified account login**: Show "Please verify your email before logging in" with option to resend

## Business Rules

- Email addresses must be unique across all accounts (case-insensitive: test@example.com = Test@Example.com)
- Passwords must be at least 8 characters with 1 number and 1 special character (!@#$%^&*)
- Passwords expire after 90 days and users must create a new one
- New password cannot match previous 3 passwords
- Verification emails expire after 24 hours
- Users can't register with disposable email services (list maintained separately)
- Account lockout after 3 failed attempts lasts exactly 15 minutes
- Password reset links expire after 1 hour
- Only one active reset link per account - requesting new one invalidates previous

## Dependencies

### Required Features/Systems
- **Email delivery service**: For verification and password reset emails. If service is down, registration/reset will fail gracefully with "Unable to send email, please try again later"
- **Session management**: Required to maintain logged-in state

### Affected Features
- **User profile**: Cannot be accessed without authentication
- **Dashboard**: Requires active session
- **Settings**: Changes require password re-confirmation

### External Services
- **Email service**: SendGrid for transactional emails
- **Disposable email checker**: API to validate email domains

## Common Issues & Edge Cases

**Multiple tabs/sessions**: If user logs out in one tab, all other tabs should immediately reflect logged-out state. Currently handled via session token validation on each request.

**Email service downtime**: System will retry sending 3 times over 10 minutes. If all fail, user sees error message but account is created - they can request verification resend from login page.

**Case sensitivity**: Email addresses are stored lowercase and compared case-insensitively. "Test@Example.com" and "test@example.com" are treated as same user.

**Timing attacks**: Login error messages deliberately don't distinguish between "email not found" and "wrong password" to prevent account enumeration.

**Clock skew**: Reset links use server time, not user device time, to prevent timezone issues.

## Future Considerations

- Add two-factor authentication option
- Support social login (Google, GitHub)
- Add "Remember me" option for extended sessions
```

**Bad example:**

```markdown
# Authentication

Uses JWT tokens with bcrypt hashing. The AuthController handles login() and register() methods. Password validation uses regex pattern /^(?=.*[0-9])(?=.*[!@#$%^&*])/.

Database schema includes users table with email, password_hash, and created_at columns.
```
*This is too technical - focuses on implementation rather than what/why/how from a user perspective.*

## Workflow: Documenting a New Feature

When a feature is complete:

1. **Identify the feature scope** - What constitutes this "feature" from a user perspective?
2. **Create the doc file** - Use a clear, descriptive name in `docs/`
3. **Start with "What"** - Describe what the feature does in simple terms
4. **Explain "Why"** - What problem does it solve?
5. **Detail "How"** - Walk through the behavior and logic
6. **Document expected behavior** - Both success and error scenarios with specific examples
7. **List business rules** - All validation and constraints that must be enforced
8. **Map dependencies** - What this needs and what needs this
9. **Capture edge cases** - Unusual scenarios and how they're handled
10. **Add to index** - Add entry to `docs/README.md` with summary and relationships
11. **Review for clarity** - Would a non-developer understand this? Would an AI agent know what's expected?

## Workflow: Documenting an Existing Project

When documenting a complete project without existing docs:

1. **Identify all features** - Survey the project or use your knowledge of features
2. **Prioritize features** - Start with core functionality, then supporting features
3. **Document each feature** - Follow the template above
4. **Add to index** - Add each feature to `docs/README.md` after documenting it (see Feature Index section above for template)
5. **Link related features** - Cross-reference where features interact in each doc

## Tips for Quality Documentation

### Be Concrete
- ❌ "The system handles various error cases"
- ✅ "If the email service is down, the system queues the message and retries every 5 minutes for up to 2 hours"

### Use Scenarios
- ❌ "Supports bulk operations"
- ✅ "Users can select multiple items and delete them all at once. If any item is locked or in use, the system shows which ones couldn't be deleted and why"

### Explain Decisions
- ❌ "Passwords must be 8+ characters"
- ✅ "Passwords must be 8+ characters to balance security with usability - short enough to remember but long enough to resist common attacks"

### Describe Edge Cases
- ❌ "Handles payment processing"
- ✅ "During payment processing, if the payment gateway times out, the system waits 30 seconds then checks the payment status directly. This prevents duplicate charges"

## Maintaining Documentation

- **Update when behavior changes** - Not when code changes, but when user-facing behavior or business logic changes
- **Keep it current** - Remove or clearly mark deprecated features
- **Version significant changes** - Note when major functionality was added or modified
- **Review periodically** - Ensure docs still accurately reflect the product

## Summary Checklist

Before finalizing feature documentation:

### Core Content
- [ ] Explains what the feature does from a user perspective
- [ ] Clarifies why this feature exists (problem/need)
- [ ] Describes how it works without code references
- [ ] Includes data flow overview

### Expected Behavior (Critical for AI troubleshooting)
- [ ] Documents success scenarios with specific inputs and outputs
- [ ] Documents error scenarios with expected error messages
- [ ] Covers edge cases and unusual situations
- [ ] Clarifies what should happen when dependencies fail

### Business Rules (Critical for AI troubleshooting)
- [ ] Lists all validation rules with specific examples
- [ ] Documents constraints that must ALWAYS be enforced
- [ ] Explains non-obvious logic that might seem like bugs

### Integration & Dependencies
- [ ] Lists required features/systems with explanations
- [ ] Lists features affected by this one
- [ ] Documents external services and their purpose
- [ ] Notes what happens when dependencies are unavailable

### Common Issues
- [ ] Documents known edge cases
- [ ] Explains gotchas or confusing behavior
- [ ] Covers common failure modes

### Quality
- [ ] Uses plain language a non-developer would understand
- [ ] Provides concrete examples, not abstractions
- [ ] Would help AI agent quickly understand expected behavior
- [ ] File is saved in `docs/` with a clear name
