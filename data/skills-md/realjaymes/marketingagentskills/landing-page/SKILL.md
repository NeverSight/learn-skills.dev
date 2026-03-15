---
name: landing-page
version: 1.0.0
description: Creates landing page copy using modular section templates. Use when the user wants to "write a homepage," "create landing page copy," "landing page sections," or "homepage template."
---

# Landing Page Assistant

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Generate structured, conversion-focused landing page copy using James Praise's modular section framework.

## When to Use

- User wants to create a new landing page or homepage
- User needs copy for specific landing page sections
- User mentions "landing page template," "homepage copy," or "page sections"

## Instructions

1. **Confirm page type**: Homepage, feature page, or campaign landing page
2. **Gather inputs**: Product name, value proposition, target audience, key features, social proof
3. **Generate section-by-section copy** following the template structure
4. **Include visual/CTA notes** for each section

## Section Structure

Generate copy for each section in order:

### Hero Section
- **Headline**: Action statement explaining unique value proposition
- **Subheadline**: 1-2 sentences explaining product and how it creates value
- **Bullet Points**: 2 specific claims, 2 objection handles, 3 social proof points
- **Social Proof**: Testimonials, logos, ratings, stats
- **Hero CTA**: Action-focused, value-focused, or objection-handling

### Problem to Solution Comparison
- **Before vs After**: Pain points vs solution benefits
- **Old Way vs New Way**: Limitations vs capabilities
- **CTA**: Reinforce action

### Features, Capabilities & Benefits
For each feature (3-6 features):
- **Heading**: Feature name
- **Description**: Capability + Benefit
- **Visual note**: Image suggestion
- **CTA**: Feature-specific action

### Integrations
For each integration (2-4):
- **Heading**: Integration name
- **Description**: Capability + Benefit
- **Visual**: Logo placement

### How It Works
For each step (3-5 steps):
- **Heading**: Step title
- **Description**: What user does/gets
- **Visual note**: Screenshot suggestion

### FAQs
- **Feature FAQs**: 2-3 questions about features
- **Objection FAQs**: 2-3 questions addressing concerns

### Second CTA Section
- **Heading**: Switch/upgrade focused
- **Description**: Value outcome statement
- **Bullet Points**: Objection handles + ease of start
- **CTA**: Clear next action

### Founder's Note (Optional)
- Put yourself in their shoes
- Explain their problem
- Take ownership
- Show the happy ending

## Output Format

```markdown
## [Section Name]

**Headline**: [Copy]

**Subheadline**: [Copy]

**Bullet Points**:
- [Point 1]
- [Point 2]

**CTA**: [Button text]

**Visual Note**: [Suggestion]
```

## Constraints

- Each section must have Headline, Description, and CTA (where applicable)
- Use bullet points for feature/benefit lists
- Bold key phrases and product names
- No generic filler text
- Use placeholders [Product Name] if info missing
- Hyphen rules: Hyphens connect words (well-being); en dashes for ranges (June-August); em dashes for breaks in thought

## Reference

See `references/landing-page-framework.md` for complete section templates and examples.
