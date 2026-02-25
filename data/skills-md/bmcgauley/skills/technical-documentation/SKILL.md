---
name: technical-documentation
description: Comprehensive technical documentation skill for creating clear, accurate, and user-centered documentation across all formats including API docs, user guides, developer documentation, knowledge bases, and system documentation. This skill should be used when creating, organizing, or maintaining technical documentation that explains complex systems, procedures, or concepts to various technical and non-technical audiences.
---

# Technical Documentation

## Overview

This skill provides frameworks and methodologies for creating technical documentation that is accurate, accessible, and actionable. It covers the full spectrum from API references to end-user guides, emphasizing clarity, completeness, and continuous maintenance.

## Documentation Type Decision Tree

To determine the appropriate documentation approach:

```
What are you documenting?
├── API/CODE
│   ├── REST/GraphQL API → Use "API Documentation"
│   ├── SDK/Library → Use "SDK Documentation"
│   ├── Code Functions → Use "Code Documentation"
│   └── Architecture → Use "System Design Docs"
├── USER-FACING
│   ├── End User Guide → Use "User Documentation"
│   ├── Admin Guide → Use "Administrator Docs"
│   ├── Tutorials → Use "Tutorial Documentation"
│   └── FAQ/KB → Use "Knowledge Base Articles"
├── DEVELOPER-FACING
│   ├── Setup/Install → Use "Getting Started Guides"
│   ├── Contributing → Use "Contribution Guidelines"
│   ├── Architecture → Use "Technical Specifications"
│   └── Troubleshooting → Use "Debug Documentation"
└── PROCESS/OPERATIONS
    ├── Runbooks → Use "Operational Runbooks"
    ├── Deployment → Use "Deployment Guides"
    ├── Incident Response → Use "Incident Playbooks"
    └── Release Notes → Use "Release Documentation"
```

## Core Documentation Principles

### The Four C's of Technical Documentation

1. **Clear** - Unambiguous and easy to understand
2. **Concise** - No unnecessary words or complexity
3. **Correct** - Technically accurate and tested
4. **Complete** - All necessary information included

### Documentation-First Development

Write documentation:
- **Before coding** - Design docs and specifications
- **During coding** - Inline comments and updates
- **After coding** - Final polish and examples
- **Continuously** - Updates with each change

### Audience-Centered Approach

Always consider:
- **Who** is reading this documentation?
- **What** do they need to accomplish?
- **When** will they read it (setup, troubleshooting, learning)?
- **Where** are they in their journey (beginner to expert)?
- **Why** do they need this information?
- **How** will they use it?

## API Documentation

### OpenAPI/Swagger Structure

```yaml
# API Endpoint Documentation Template
endpoint:
  path: /api/v1/resource/{id}
  method: GET|POST|PUT|DELETE
  summary: Brief description (one line)
  description: |
    Detailed explanation of what this endpoint does,
    when to use it, and any important considerations.
  
  parameters:
    - name: id
      in: path|query|header|cookie
      required: true|false
      schema:
        type: string|number|boolean
        format: uuid|email|date
      description: What this parameter does
      example: "123e4567-e89b-12d3-a456-426614174000"
  
  requestBody:
    required: true|false
    content:
      application/json:
        schema:
          type: object
          properties:
            field1:
              type: string
              description: Purpose of this field
        example:
          field1: "value"
  
  responses:
    200:
      description: Successful response
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Resource'
    400:
      description: Bad request - invalid parameters
    401:
      description: Unauthorized - invalid or missing auth
    404:
      description: Not found - resource doesn't exist
    500:
      description: Server error - something went wrong
  
  security:
    - bearerAuth: []
    - apiKey: []
```

### API Documentation Best Practices

#### Request Examples
Provide examples in multiple formats:

```bash
# cURL
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'

# JavaScript/Fetch
const response = await fetch('https://api.example.com/v1/users', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com'
  })
});

# Python/Requests
import requests

response = requests.post(
    'https://api.example.com/v1/users',
    headers={
        'Authorization': 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    json={
        'name': 'John Doe',
        'email': 'john@example.com'
    }
)
```

#### Response Examples
Show both successful and error responses:

```json
// Success Response (200 OK)
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T09:30:00Z",
  "updated_at": "2024-01-15T09:30:00Z"
}

// Error Response (400 Bad Request)
{
  "error": {
    "code": "INVALID_EMAIL",
    "message": "The email address provided is not valid",
    "field": "email",
    "details": "Email must be a valid email address format"
  }
}
```

### SDK Documentation Pattern

```markdown
## Installation

### npm
\`\`\`bash
npm install @company/sdk
\`\`\`

### yarn
\`\`\`bash
yarn add @company/sdk
\`\`\`

## Quick Start

\`\`\`javascript
import { Client } from '@company/sdk';

// Initialize the client
const client = new Client({
  apiKey: 'YOUR_API_KEY',
  baseUrl: 'https://api.example.com' // Optional
});

// Make your first request
const users = await client.users.list();
console.log(users);
\`\`\`

## Authentication

The SDK supports multiple authentication methods:

### API Key Authentication
\`\`\`javascript
const client = new Client({
  apiKey: 'YOUR_API_KEY'
});
\`\`\`

### OAuth 2.0
\`\`\`javascript
const client = new Client({
  clientId: 'YOUR_CLIENT_ID',
  clientSecret: 'YOUR_CLIENT_SECRET',
  redirectUri: 'http://localhost:3000/callback'
});

// Get authorization URL
const authUrl = client.auth.getAuthorizationUrl();

// Exchange code for token
const token = await client.auth.exchangeCode(code);
\`\`\`
```

## User Documentation

### Structure for User Guides

#### Getting Started Section
```markdown
# Getting Started with [Product Name]

## What You'll Learn
By the end of this guide, you'll be able to:
- [ ] Set up your account
- [ ] Complete your first task
- [ ] Understand core concepts
- [ ] Know where to find help

## Prerequisites
Before you begin, make sure you have:
- An account (sign up at [link])
- Required permissions (see [permissions guide])
- System requirements met (see [requirements])

## Step 1: Initial Setup
[Clear, numbered steps with screenshots]

## Step 2: Your First Task
[Guided walkthrough of common task]

## What's Next?
- Explore [advanced features]
- Read [best practices]
- Join [community]
```

#### Task-Based Documentation
Structure documentation around what users want to do:

```markdown
# How to [Accomplish Task]

## Before You Begin
- Time required: ~X minutes
- Prerequisites: [list]
- Permissions needed: [list]

## Steps

### 1. [First Action]
[Screenshot or diagram]

**To [action]:**
1. Navigate to [location]
2. Click [button/link]
3. Enter [information]

> **Note:** [Important information]

> **Tip:** [Helpful suggestion]

> **Warning:** [Potential issue to avoid]

### 2. [Second Action]
[Continue pattern]

## Troubleshooting

### Problem: [Common Issue]
**Symptoms:** What the user sees
**Cause:** Why it happens
**Solution:** How to fix it

## Related Topics
- [Link to related task]
- [Link to concept explanation]
- [Link to reference]
```

### Progressive Disclosure Pattern

Organize information from simple to complex:

```markdown
## Overview (Everyone reads)
Brief explanation in plain language.

## Basic Usage (Most users read)
Common use cases with examples.

<details>
<summary>Advanced Configuration (Some users read)</summary>

Detailed configuration options and edge cases.

</details>

<details>
<summary>Technical Details (Few users read)</summary>

Implementation details, performance considerations, etc.

</details>
```

## Developer Documentation

### README Template

```markdown
# Project Name

Brief description of what this project does and who it's for.

## Features

- ✨ Feature 1
- 🚀 Feature 2
- 💡 Feature 3

## Installation

### Requirements
- Requirement 1 (version X.X+)
- Requirement 2

### Setup
\`\`\`bash
# Clone the repository
git clone https://github.com/username/project.git

# Navigate to project directory
cd project

# Install dependencies
npm install

# Run the application
npm start
\`\`\`

## Usage

### Basic Example
\`\`\`javascript
import { Module } from 'project';

const instance = new Module();
instance.doSomething();
\`\`\`

### Advanced Example
\`\`\`javascript
// More complex usage
\`\`\`

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| option1 | string | 'default' | What this does |
| option2 | boolean | false | When to use this |

## API Reference

### `methodName(param1, param2)`

Description of what this method does.

**Parameters:**
- `param1` (Type): Description
- `param2` (Type): Description

**Returns:** Type - Description

**Example:**
\`\`\`javascript
const result = methodName('value1', 'value2');
\`\`\`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.
```

### Architecture Documentation

```markdown
# System Architecture

## Overview

[High-level architecture diagram]

Brief description of the system and its purpose.

## Components

### Component 1: [Name]
**Purpose:** What this component does
**Technology:** Languages, frameworks used
**Dependencies:** What it depends on
**Interface:** How it communicates

### Component 2: [Name]
[Continue pattern]

## Data Flow

1. **Step 1:** User initiates action
2. **Step 2:** Request processed by [component]
3. **Step 3:** Data retrieved from [source]
4. **Step 4:** Response returned to user

[Sequence diagram showing flow]

## Design Decisions

### Decision: [Technology/Pattern Choice]
**Context:** The situation that required a decision
**Options Considered:**
1. Option A - Pros/Cons
2. Option B - Pros/Cons

**Decision:** What was chosen and why
**Consequences:** Impact of this decision

## Security Considerations

- Authentication: How users are verified
- Authorization: How permissions are managed
- Data Protection: How sensitive data is handled
- Audit Logging: What is logged and where

## Performance Considerations

- Caching Strategy: What, where, TTL
- Load Balancing: Method and configuration
- Scaling Approach: Horizontal vs Vertical
- Bottlenecks: Known issues and mitigation

## Deployment

### Environments
- Development: Configuration and purpose
- Staging: Configuration and purpose
- Production: Configuration and purpose

### Infrastructure
- Hosting: Where and how
- CI/CD: Pipeline and process
- Monitoring: Tools and metrics
- Backup: Strategy and frequency
```

## Knowledge Base Articles

### Problem-Solution Format

```markdown
# Error: [Specific Error Message]

## Symptoms
What the user experiences when this error occurs.

## Cause
Technical explanation of why this happens.

## Solution

### Quick Fix
Immediate steps to resolve the issue:
1. Step one
2. Step two
3. Step three

### Permanent Solution
Long-term fix to prevent recurrence:
1. Configuration change
2. System update
3. Process improvement

## Prevention
How to avoid this issue in the future.

## Related Articles
- [Link to similar issue]
- [Link to underlying concept]
```

### FAQ Format

```markdown
# Frequently Asked Questions

## General Questions

### Q: What is [Product/Feature]?
**A:** Clear, concise answer in 2-3 sentences.

### Q: How much does it cost?
**A:** Pricing information with link to full pricing page.

## Technical Questions

### Q: What are the system requirements?
**A:** 
- **Minimum:** List minimum requirements
- **Recommended:** List recommended specs
- **Optimal:** List best performance specs

### Q: Is my data secure?
**A:** Security explanation with specifics about:
- Encryption methods
- Compliance certifications
- Data handling policies

## Troubleshooting

### Q: Why isn't [feature] working?
**A:** Common causes and solutions:
1. **Cause 1:** Solution
2. **Cause 2:** Solution
3. **Still having issues?** [Contact support link]
```

## Documentation Formats and Tools

### Markdown Best Practices

```markdown
# Use Semantic Headers
Don't skip header levels. Use h1 → h2 → h3 in order.

## Format Code Properly
Inline code: `const variable = "value"`
Code blocks with language hints:
\`\`\`javascript
// This enables syntax highlighting
const example = true;
\`\`\`

## Create Clear Tables
| Column 1 | Column 2 | Column 3 |
|:---------|:--------:|---------:|
| Left     | Center   | Right    |
| Aligned  | Aligned  | Aligned  |

## Use Emphasis Wisely
- **Bold** for important terms first mention
- *Italic* for emphasis or introducing terms
- `code` for commands, file names, values
- > Blockquotes for important notes

## Link Meaningfully
Good: [View the API documentation](link)
Bad: [Click here](link) for documentation

## Include Visual Aids
![Alt text for accessibility](image.png)
*Figure 1: Caption explaining the image*
```

### Documentation Site Structure

```
docs/
├── getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   └── first-steps.md
├── guides/
│   ├── beginner/
│   ├── intermediate/
│   └── advanced/
├── reference/
│   ├── api/
│   ├── cli/
│   ├── configuration/
│   └── glossary.md
├── tutorials/
│   ├── tutorial-1.md
│   └── tutorial-2.md
├── troubleshooting/
│   ├── common-issues.md
│   └── error-codes.md
└── contributing/
    ├── code-of-conduct.md
    ├── development-setup.md
    └── pull-requests.md
```

## Version Control for Documentation

### Versioning Strategy

```markdown
# Documentation Versions

## Version Numbering
- v1.0.0 - Major version (breaking changes)
- v1.1.0 - Minor version (new features)
- v1.1.1 - Patch version (bug fixes)

## Version Banner
> **Note:** You are viewing documentation for v2.0.
> For v1.x documentation, see [here](link).

## Deprecation Notices
> **Deprecated:** This feature will be removed in v3.0.
> Use [alternative feature] instead.
> Migration guide: [link]

## Changelog Integration
### Version 2.1.0 (2024-01-15)
#### Added
- New feature documentation
- Additional examples

#### Changed
- Updated API endpoint descriptions
- Improved error messages

#### Fixed
- Corrected typos in examples
- Fixed broken links

#### Removed
- Deprecated v1 endpoints
```

## Quality Checklist

### Pre-Publication Review

#### Content Quality
- [ ] Technically accurate and tested
- [ ] Complete (no TODO or TBD remaining)
- [ ] Clear and concise writing
- [ ] Appropriate for target audience
- [ ] Examples work as written
- [ ] Screenshots current and annotated

#### Structure and Organization
- [ ] Logical flow and organization
- [ ] Consistent formatting
- [ ] Proper header hierarchy
- [ ] Table of contents for long docs
- [ ] Cross-references working
- [ ] Navigation clear

#### Language and Style
- [ ] Active voice predominant
- [ ] Present tense for current state
- [ ] Consistent terminology
- [ ] No jargon without explanation
- [ ] Spell-checked
- [ ] Grammar-checked

#### Technical Elements
- [ ] Code examples syntax-highlighted
- [ ] Commands copy-pasteable
- [ ] API endpoints accurate
- [ ] Version numbers correct
- [ ] Links validated
- [ ] Images optimized

#### Accessibility
- [ ] Alt text for images
- [ ] Descriptive link text
- [ ] Color not sole indicator
- [ ] Keyboard navigation works
- [ ] Screen reader friendly
- [ ] Mobile responsive

### Documentation Maintenance

#### Regular Updates
- **Weekly:** Fix reported issues
- **Monthly:** Review analytics, update FAQs
- **Quarterly:** Audit for accuracy
- **Annually:** Major reorganization

#### Feedback Integration
1. Monitor support tickets for doc gaps
2. Track documentation analytics
3. Conduct user surveys
4. Run documentation usability tests
5. Implement feedback systematically

## Style Guide

### Writing Style

#### Voice and Tone
- **Active:** "Configure the server" not "The server should be configured"
- **Direct:** "You must" not "It is required that you"
- **Friendly:** Professional but approachable
- **Inclusive:** Avoid assumptions about expertise

#### Word Choice
- Use simple words when possible
- Define technical terms on first use
- Be consistent with terminology
- Avoid colloquialisms and idioms
- Spell out acronyms initially

#### Sentence Structure
- Keep sentences under 25 words
- One idea per sentence
- Use bullet points for lists
- Break up long paragraphs
- Start with the most important information

### Formatting Conventions

#### Capitalization
- Sentence case for headers
- Title case for product names
- lowercase for commands and code
- UPPERCASE for environment variables

#### Punctuation
- Oxford comma in lists
- No period in headers
- Colon before code blocks
- Semicolon sparingly

#### Special Elements
- **Note:** Additional helpful information
- **Tip:** Best practice or shortcut
- **Important:** Critical information
- **Warning:** Potential problems
- **Danger:** Data loss or security risk

## Resources

### Scripts
- `scripts/doc_validator.py` - Validates documentation structure and links
- `scripts/api_doc_generator.py` - Generates API docs from code comments
- `scripts/changelog_builder.py` - Creates changelog from git commits

### References
- `references/style_guide.md` - Complete documentation style guide
- `references/template_library.md` - Documentation templates for all types
- `references/markdown_cheatsheet.md` - Quick reference for markdown syntax
- `references/diagramming_guide.md` - How to create effective technical diagrams

### Assets
- `assets/templates/api_reference.md` - API documentation template
- `assets/templates/user_guide.md` - User guide template
- `assets/templates/readme.md` - README template
- `assets/templates/troubleshooting.md` - Troubleshooting guide template
