---
name: create-skill
description: How to create new skills following the agentskills.io specification
---

# Creating New Skills

This skill explains how to create new skills that follow the [agentskills.io](https://agentskills.io/specification) specification.

---

## 🤖 Automatic Skill Identification (For Agent)

**During any work, I should actively monitor for these signals:**

- [ ] **Repetition**: I'm explaining the same process for the 3rd time
- [ ] **Complexity**: Workflow involves >5 sequential steps
- [ ] **Project-specific**: Process is unique to this codebase (not generic programming)
- [ ] **Pattern discovery**: Similar logic appears in 3+ different files
- [ ] **Manual toil**: Repetitive task that could be documented/automated

**Action**: If **2 or more** are true → **PROPOSE creating a skill** to the user

---

## When to Create a Skill

Create a new skill when you have:
- **Repeatable workflows** that are used frequently
- **Domain-specific expertise** that needs to be documented
- **Multi-step processes** that require consistent execution
- **Best practices** for a specific area of the codebase

Examples:
- ✅ Email notification process
- ✅ Reporting and analytics workflow
- ✅ Authentication patterns
- ❌ One-time fixes (document in docs/ instead)
- ❌ Temporary workarounds

---

## Directory Structure

### Basic Skill (most common)
```
.agent/skills/
└── skill-name/
    └── SKILL.md          # Required
```

### Complex Skill (with additional resources)
```
.agent/skills/
└── skill-name/
    ├── SKILL.md          # Required
    ├── scripts/          # Helper scripts
    │   └── helper.sh
    ├── references/       # Reference documentation
    │   └── REFERENCE.md
    └── assets/           # Templates, diagrams, data files
        └── template.json
```

---

## Naming Rules

Skill names must follow these rules:

- **1-64 characters**
- **Lowercase only** (a-z)
- **Use hyphens** (-) to separate words
- **No consecutive hyphens** (--)
- **Cannot start or end with hyphen**
- **Must match directory name**

### ✅ Valid Names
```
name: api-testing
name: user-authentication
name: email-notifications
name: create-skill
```

### ❌ Invalid Names
```
name: API-Testing        # No uppercase
name: api_testing        # No underscores
name: -api-testing       # Cannot start with hyphen
name: api--testing       # No consecutive hyphens
```

---

## SKILL.md Template

```markdown
---
name: skill-name
description: A clear, specific description of what this skill does and when to use it. Include keywords that help identify when this skill is relevant.
---

# Skill Title

Brief introduction explaining the purpose of this skill.

---

## Section 1: Overview

Explain the core concept or workflow.

---

## Section 2: Step-by-Step Guide

Provide detailed instructions with code examples.

### Subsection Example
```language
// Code example
```

---

## Common Pitfalls

List common mistakes and how to avoid them.

---

## Examples

Provide real-world examples of using this skill.
```

---

## Frontmatter Fields

### Required Fields

#### `name`
- Must match the directory name
- Follow naming rules above

```yaml
name: database-migrations
```

#### `description`
- 1-1024 characters
- Describe **what** the skill does
- Describe **when** to use it
- Include specific **keywords** for discoverability

```yaml
description: How to create and run database migrations using Prisma. Use when adding new tables, modifying schemas, or updating database structure in development and production.
```

### Optional Fields

#### `license`
```yaml
license: MIT
```

#### `compatibility`
Use if skill has specific requirements:
```yaml
compatibility: Requires Prisma, PostgreSQL, and Node.js 18+
```

#### `metadata`
Key-value pairs for additional info:
```yaml
metadata:
  author: project-team
  version: "1.0"
  last-updated: "2026-01-17"
```

---

## Writing Good Descriptions

### ✅ Good Descriptions
```yaml
description: How to deploy changes to production using PM2 and GitHub auto-deploy. Use when pushing code updates, database migrations, or configuration changes to the Hetzner server.
```

**Why:** Specific, mentions tools, explains when to use it.

```yaml
description: Guidelines for creating React components following the component-first architecture. Use when building new UI elements or refactoring inline code into reusable components.
```

**Why:** Clear purpose, mentions architectural pattern, explains context.

### ❌ Bad Descriptions
```yaml
description: Helps with deployment
```

**Why:** Too vague, no context, missing keywords.

```yaml
description: This skill is for components
```

**Why:** Doesn't explain what aspect or when to use it.

---

## Optional Directories

### `scripts/`
Use for helper scripts that:
- Automate repetitive tasks
- Validate configurations
- Transform data

**Example:**
```bash
scripts/
├── validate-schema.sh
└── generate-migration.js
```

Scripts should:
- Be self-contained or document dependencies
- Include helpful error messages
- Handle edge cases gracefully

### `references/`
Use for detailed technical documentation:
- API specifications
- Form templates
- Domain-specific guides

**Example:**
```
references/
├── REFERENCE.md      # Detailed API reference
├── FORMS.md          # Form templates
└── best-practices.md # Extended guidelines
```

### `assets/`
Use for supporting files:
- Configuration templates
- Diagrams and images
- Lookup tables or schemas

**Example:**
```
assets/
├── api-flow.png
├── config-template.json
└── migration-template.sql
```

---

## Checklist for New Skills

Before creating a skill, verify:

- [ ] The workflow is used more than once
- [ ] The skill has a clear, specific purpose
- [ ] The name follows naming rules
- [ ] Description includes what, when, and keywords
- [ ] Directory name matches skill name
- [ ] SKILL.md has proper frontmatter
- [ ] Content is organized with headers
- [ ] Examples are provided
- [ ] Common pitfalls are documented

---

## Example: Creating "email-notifications" Skill

### 1. Create Directory
```bash
mkdir -p .agent/skills/email-notifications
```

### 2. Create SKILL.md
```markdown
---
name: email-notifications
description: How to send email notifications using the project's email service. Use when implementing user confirmations, admin alerts, or scheduled reports.
---

# Email Notifications

This skill explains how to send emails in the Digital Befaring application.

---

## Email Templates

All templates are in `src/lib/email/templates/`.

### Available Templates
- `customer-confirmation.tsx` - Customer form submission
- `admin-alert.tsx` - Admin notifications
- `technician-assignment.tsx` - Job assignment

---

## Sending an Email

```typescript
import { sendEmail } from '@/lib/email';

await sendEmail({
    to: customer.email,
    subject: 'Skjema mottatt',
    template: 'customer-confirmation',
    data: { customerName: customer.name }
});
```

---

## Testing

Test emails in development using [Ethereal](https://ethereal.email).
```

### 3. Update GEMINI.md (Optional)
If this is a major skill, mention it in the project documentation.

---

## Validation

After creating a skill, verify:

```bash
# Check structure
ls -la .agent/skills/skill-name/

# Verify frontmatter format
head -n 5 .agent/skills/skill-name/SKILL.md

# Test that agent can read it
# (In conversation, reference the skill and see if agent finds it)
```

---

## Maintenance

Keep skills up-to-date:
- Update when workflows change
- Add new examples as patterns emerge
- Remove outdated information
- Version metadata if needed

```yaml
metadata:
  last-updated: "2026-01-17"
  version: "1.1"
```
