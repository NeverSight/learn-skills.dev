---
name: skill-writing-best-practices
description: Guidelines for creating AI agent skills. Use when writing new skills, documenting coding patterns, or reviewing skill files. Triggers when creating or modifying files in the skills/ directory.
---

# Skill Writing Best Practices

Patterns for creating effective AI agent skills that capture coding conventions and best practices. Contains 6 rules covering structure, content, and writing style.

## When to Apply

Reference these guidelines when:

- Creating a new skill from scratch
- Extracting patterns from an existing codebase
- Reviewing or improving existing skills
- Converting documentation into skill format

## Rules Summary

### Structure (HIGH)

#### skill-directory-structure - @rules/skill-directory-structure.md

Every skill has a SKILL.md and a rules/ directory.

```
skills/
└── topic-best-practices/
    ├── SKILL.md              # Main summary with all rules
    └── rules/
        ├── rule-name.md      # Detailed individual rules
        └── another-rule.md
```

#### skill-md-structure - @rules/skill-md-structure.md

SKILL.md has frontmatter, overview, and condensed rule summaries.

```markdown
---
name: topic-best-practices
description: When to use this skill.
---

# Topic Best Practices

Brief intro. Contains N rules across M categories.

## When to Apply

- Situation 1
- Situation 2

## Rules Summary

### Category (IMPACT)

#### rule-name - @rules/rule-name.md

One sentence. Code example.
```

#### rule-file-structure - @rules/rule-file-structure.md

Each rule file has frontmatter, explanation, examples, and takeaways.

```markdown
---
title: Rule Title
impact: HIGH
tags: [relevant, tags]
---

# Rule Title

What to do and why.

## Why

- Benefit 1
- Benefit 2

## Pattern

\`\`\`ruby
# Bad
bad_code

# Good
good_code
\`\`\`

## Rules

1. Takeaway 1
2. Takeaway 2
```

### Content (HIGH)

#### concrete-examples - @rules/concrete-examples.md

Every rule needs code examples. Abstract advice is hard to apply.

```markdown
# Bad: Too abstract
"Keep your code organized."

# Good: Concrete
"Place concerns in `app/models/model_name/` not `app/models/concerns/`."

\`\`\`ruby
# Shows exactly what to do
app/models/card/closeable.rb
\`\`\`
```

#### explain-why - @rules/explain-why.md

Don't just show what. Explain why it matters.

```markdown
## Why

- **Testability**: Sync method can be tested without job infrastructure
- **Flexibility**: Callers choose sync or async based on context
- **Clarity**: The `_later` suffix makes async behavior explicit
```

### Style (MEDIUM)

#### writing-style - @rules/writing-style.md

Write naturally. Avoid AI-isms and excessive formatting.

```markdown
# Bad
---
Here is an overview of the key points:
---

# Good
Group related rules by category. Each rule gets a one-sentence
description and a short code example.
```

## Philosophy

Good skills are:

1. **Concrete** - Every rule has code examples
2. **Reasoned** - Explains why, not just what
3. **Scannable** - Easy to find relevant rules quickly
4. **Honest** - Shows when NOT to use a pattern
5. **Natural** - Written like documentation, not AI output
