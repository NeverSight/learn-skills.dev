---
name: diataxis-organize-docs
description: Reorganize documentation into the Diataxis framework structure. Splits existing docs into tutorials, how-to guides, reference, and explanation sections.
allowed-tools: Read, Write
---

# Diataxis Documentation Organization

Reorganize documentation by classifying content into the four Diataxis quadrants and creating a structured documentation hierarchy.

## The Four Quadrants

| Quadrant | Orientation | Purpose | User Need |
|----------|-------------|---------|-----------|
| **Tutorial** | Learning | Teach through doing | "I want to learn" |
| **How-to** | Task | Solve specific problems | "I want to accomplish X" |
| **Reference** | Information | Describe the machinery | "I need facts about Y" |
| **Explanation** | Understanding | Clarify concepts | "I want to understand why" |

## Step 1: Analyze Existing Documentation

Scan the documentation directory and classify each file or section:

```
For each document/section, determine:
- Does it walk through steps to learn? → Tutorial
- Does it solve a specific problem? → How-to
- Does it describe APIs/configs/specs? → Reference  
- Does it explain concepts/rationale? → Explanation
```

## Step 2: Create Directory Structure

Organize docs into this hierarchy:

```
docs/
├── tutorials/           # Learning-oriented
│   ├── getting-started/
│   └── {topic}/
├── how-to/              # Task-oriented
│   ├── {task-category}/
│   └── troubleshooting/
├── reference/           # Information-oriented
│   ├── api/
│   ├── configuration/
│   └── architecture/
├── explanation/         # Understanding-oriented
│   ├── concepts/
│   ├── decisions/
│   └── background/
└── index.md             # Navigation hub
```

## Step 3: Classification Criteria

### Tutorials (Learning)

**Characteristics:**
- Step-by-step instructions for beginners
- Builds toward a working example
- Focuses on "what the user does"
- Has a concrete end goal

**Example titles:**
- "Your First Application"
- "Getting Started with X"
- "Building a Sample Project"

**DO NOT include:**
- Exhaustive options or configurations
- Theoretical explanations
- Edge cases

### How-to Guides (Tasks)

**Characteristics:**
- Assumes basic knowledge
- Addresses a specific problem
- Provides actionable steps
- May have multiple valid approaches

**Example titles:**
- "How to Deploy to Production"
- "Migrating from v1 to v2"
- "Configuring Authentication"

**DO NOT include:**
- Teaching fundamentals
- Complete API documentation
- Philosophical discussions

### Reference (Information)

**Characteristics:**
- Accurate and complete
- Consistent structure
- Describes what IS (not how to use)
- Dry, factual tone

**Example content:**
- API endpoints and parameters
- Configuration options
- CLI commands and flags
- Data schemas

**DO NOT include:**
- Explanations of why
- Step-by-step tutorials
- Opinions or recommendations

### Explanation (Understanding)

**Characteristics:**
- Discusses context and background
- Explains design decisions
- Connects concepts together
- Can be discursive

**Example titles:**
- "Understanding the Event Loop"
- "Why We Chose X over Y"
- "Architecture Overview"

**DO NOT include:**
- How-to instructions
- Reference specifications
- Beginner tutorials

## Step 4: Split Mixed Documents

When a document contains multiple types:

1. **Identify boundaries** - Mark where content shifts purpose
2. **Extract sections** - Move each type to its proper location
3. **Add cross-references** - Link related content across quadrants
4. **Preserve context** - Ensure each piece stands alone

### Example Split

**Before (mixed document):**
```markdown
# Authentication

Authentication uses JWT tokens. (explanation)

## Quick Start
1. Install the package... (tutorial)

## API Reference
- `authenticate(user, pass)` - Returns token (reference)

## Troubleshooting
### Token Expired
If you see error X, do Y... (how-to)
```

**After (split):**
```
tutorials/authentication-quickstart.md
how-to/troubleshooting/token-expired.md
reference/api/authentication.md
explanation/concepts/authentication.md
```

## Step 5: Create Navigation Index

Build a documentation hub that helps users find content by their need:

```markdown
# Documentation

## Learning
New here? Start with our tutorials:
- [Getting Started](tutorials/getting-started.md)
- [Your First App](tutorials/first-app.md)

## Guides
Solve specific problems:
- [Deployment](how-to/deployment/)
- [Troubleshooting](how-to/troubleshooting/)

## Reference
Technical specifications:
- [API Reference](reference/api/)
- [Configuration](reference/configuration/)

## Understanding
Deep dives and background:
- [Architecture](explanation/architecture.md)
- [Design Decisions](explanation/decisions/)
```

## Quality Checklist

After reorganization, verify:

- [ ] Each document serves ONE purpose
- [ ] Tutorials have clear learning outcomes
- [ ] How-to guides solve specific problems
- [ ] Reference is complete and accurate
- [ ] Explanations provide genuine insight
- [ ] Cross-references connect related content
- [ ] Navigation makes user intent clear
- [ ] No orphaned or duplicated content

## Anti-Patterns to Fix

| Problem | Solution |
|---------|----------|
| Tutorial with exhaustive options | Move options to reference, link to it |
| How-to explaining fundamentals | Extract to tutorial, assume knowledge |
| Reference with usage examples | Move examples to how-to |
| Explanation with code snippets | Keep only conceptual snippets |
| One giant README | Split into proper quadrants |

## Output Format

After analysis, report:

```markdown
## Documentation Audit

### Current State
- Total documents: X
- Mixed documents: Y
- Missing quadrants: [list]

### Classification Results
| Document | Current Type | Recommended Type | Action |
|----------|--------------|------------------|--------|
| ... | ... | ... | Split/Move/Keep |

### Proposed Structure
[Directory tree with file placements]

### Cross-References Needed
- [doc A] should link to [doc B]
- ...
```
