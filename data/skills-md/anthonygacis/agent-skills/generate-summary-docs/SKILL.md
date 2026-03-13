---
name: generate-summary-docs
description: Generate structured, digestible documentation summaries organized in markdown format. Creates comprehensive summaries covering key points, special syntax, topics, and how things work. Use when the user asks to summarize, explain, document, digest, or break down complex information about code, libraries, infrastructure, APIs, or technical topics.
---

# Generate Summary Documentation

Generate well-organized, digestible documentation summaries in markdown format. This skill helps you create structured documentation that makes complex topics easy to understand.

## Documentation Structure

All documentation is stored in a `.summary/` directory with this structure:

```
.summary/
├── README.md                    # Main table of contents
├── topic-name/                  # Topic-specific folder
│   ├── overview.md              # High-level summary
│   ├── key-concepts.md          # Core concepts explained
│   ├── syntax-reference.md      # Special syntax and patterns
│   ├── how-it-works.md          # Implementation details
│   └── examples.md              # Practical examples
└── another-topic/
    └── ...
```

## Documentation Workflow

### Step 1: Analyze the Content

Before generating documentation:
1. Identify the main topic and subtopics
2. Determine what type of content you're documenting (library, API, infrastructure, codebase)
3. Gather relevant information from code, files, or user input

### Step 2: Create Directory Structure

1. Check if `.summary/` exists at the workspace root
2. Create a topic-specific subdirectory with a clear, kebab-case name
3. Plan the file split based on content volume

### Step 3: Generate Documentation Files

Create markdown files for each section of the topic. Each file should be focused and digestible (aim for 100-300 lines per file).

#### Required Sections

**overview.md** - High-level summary
```markdown
# [Topic Name] - Overview

## Summary
Brief 2-3 paragraph summary of what this is and why it matters.

## Key Points
- Point 1: Important aspect
- Point 2: Critical feature
- Point 3: Notable characteristic

## Quick Links
- [Key Concepts](key-concepts.md)
- [Syntax Reference](syntax-reference.md)
- [How It Works](how-it-works.md)
```

**key-concepts.md** - Core concepts explained
```markdown
# [Topic Name] - Key Concepts

## Concept 1: [Name]
Brief explanation of the concept.

### Details
- Detailed point 1
- Detailed point 2

### When to Use
Practical guidance on when this concept applies.

---

## Concept 2: [Name]
...
```

**syntax-reference.md** - Special syntax and patterns (if applicable)
```markdown
# [Topic Name] - Syntax Reference

## Basic Syntax

### Pattern 1
\`\`\`language
code example
\`\`\`

**Explanation**: What this does and when to use it.

### Pattern 2
...

## Special Cases
Document any edge cases or special syntax variations.
```

**how-it-works.md** - Implementation details and internals
```markdown
# [Topic Name] - How It Works

## Architecture
Explain the overall architecture or flow.

## Step-by-Step Process
1. **Step 1**: What happens first
2. **Step 2**: What happens next
3. **Step 3**: Final result

## Under the Hood
Technical details about implementation.

## Gotchas and Considerations
- Gotcha 1: What to watch out for
- Gotcha 2: Common mistake to avoid
```

**examples.md** - Practical examples
```markdown
# [Topic Name] - Examples

## Example 1: [Use Case]
**Scenario**: Describe the use case

\`\`\`language
code example
\`\`\`

**Explanation**: What this example demonstrates.

---

## Example 2: [Use Case]
...
```

#### Optional Sections

Create additional files as needed:
- `advanced-usage.md` - Advanced patterns and techniques
- `troubleshooting.md` - Common issues and solutions
- `comparison.md` - Comparisons with alternatives
- `migration.md` - Migration guides
- `best-practices.md` - Recommended patterns

### Step 4: Update Main README

After creating topic documentation, update `.summary/README.md`:

```markdown
# Documentation Summary

This directory contains structured, digestible documentation summaries.

## Topics

### [Topic Name 1](topic-name-1/)
Brief one-line description of this topic.

**Contents:**
- [Overview](topic-name-1/overview.md) - High-level summary
- [Key Concepts](topic-name-1/key-concepts.md) - Core concepts
- [Syntax Reference](topic-name-1/syntax-reference.md) - Special syntax
- [How It Works](topic-name-1/how-it-works.md) - Implementation details
- [Examples](topic-name-1/examples.md) - Practical examples

---

### [Topic Name 2](topic-name-2/)
Brief one-line description of this topic.

**Contents:**
...
```

## File Organization Guidelines

### When to Split Files

Split content into multiple files when:
- A single file would exceed 300 lines
- The topic has distinct subtopics that deserve separate focus
- Different audience levels (beginner vs advanced)

**Example: Large library documentation**
```
library-name/
├── overview.md
├── getting-started.md       # Split from overview
├── core-concepts.md
├── api-authentication.md    # Split from syntax
├── api-endpoints.md         # Split from syntax
├── data-models.md          # Split from how-it-works
├── error-handling.md       # Split from how-it-works
└── examples/               # Subdirectory for many examples
    ├── basic-usage.md
    ├── advanced-patterns.md
    └── real-world-scenarios.md
```

### Naming Conventions

- **Folders**: Use kebab-case, descriptive names (e.g., `terraform-modules`, `api-gateway`)
- **Files**: Use kebab-case, clear purpose (e.g., `getting-started.md`, `api-reference.md`)
- **Headers**: Use sentence case in markdown headings

### Cross-Referencing

Use relative links to connect related documentation:

```markdown
For more details on authentication, see [API Authentication](api-authentication.md).

Related topics:
- [Error Handling](error-handling.md)
- [Data Models](data-models.md)
```

## Content Writing Guidelines

### 1. Use Clear, Concise Language

Write for human understanding:
- ✅ "This function validates user input before processing"
- ❌ "This function implements a validation paradigm that encompasses..."

### 2. Structure with Headers

Use hierarchical headers for easy scanning:
```markdown
# Main Topic

## Major Section

### Subsection

#### Detail Point
```

### 3. Include Code Examples

Always show practical examples with explanations:

```markdown
### Example: User Authentication

\`\`\`python
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if authenticate_user(username, password):
        return jsonify({'token': generate_token(username)})
    return jsonify({'error': 'Invalid credentials'}), 401
\`\`\`

**Key Points:**
- The `authenticate_user()` function validates credentials
- Successful login returns a JWT token
- Failed attempts return 401 status code
```

### 4. Highlight Important Information

Use blockquotes for important notes:

```markdown
> **Important**: Always validate user input before processing to prevent security vulnerabilities.

> **Note**: This feature requires version 2.0 or higher.
```

### 5. Use Lists Effectively

- Use bullet points for unordered information
- Use numbered lists for sequential steps
- Keep list items parallel in structure

### 6. Add Visual Breaks

Use horizontal rules to separate major sections:

```markdown
## Section 1
Content...

---

## Section 2
Content...
```

## Update Strategy

When updating existing documentation:

1. **Read existing files first** - Check what's already documented
2. **Identify gaps** - What's missing or outdated?
3. **Update incrementally** - Don't regenerate everything; update specific files
4. **Maintain consistency** - Match existing style and structure
5. **Update the main README** - Ensure table of contents is current

## Special Considerations

### For Infrastructure Documentation

When documenting infrastructure:
- Include architecture diagrams (mermaid or references)
- Document dependencies and prerequisites
- Explain resource relationships
- Include deployment procedures

### For API Documentation

When documenting APIs:
- List all endpoints with methods
- Show request/response examples
- Document authentication requirements
- Include error codes and meanings

### For Library/Framework Documentation

When documenting libraries:
- Show installation steps
- Provide quick start guide
- Document all public APIs
- Include configuration options

### For Codebase Documentation

When documenting codebases:
- Explain directory structure
- Document architectural patterns
- Show data flow
- List key modules and their purposes

## Complete Example

Here's a complete example for documenting a fictional API:

**User Request**: "Summarize our payment processing API"

**Your Response**:

1. Create directory structure:
```
.summary/
└── payment-api/
    ├── overview.md
    ├── authentication.md
    ├── endpoints.md
    ├── data-models.md
    ├── error-handling.md
    └── examples.md
```

2. Generate each file with appropriate content
3. Update `.summary/README.md` with the new topic
4. Verify all cross-references work

## Quality Checklist

Before completing the documentation:

- [ ] All required sections are present
- [ ] Files are appropriately sized (100-300 lines)
- [ ] Code examples are included and explained
- [ ] Cross-references use correct relative paths
- [ ] Main README.md is updated
- [ ] Consistent formatting throughout
- [ ] Topic folder name is clear and descriptive
- [ ] No duplicate information across files

## Tips for Success

1. **Start with overview.md** - This helps organize your thoughts
2. **Write for the reader** - Assume they're learning this for the first time
3. **Use examples liberally** - Concrete examples beat abstract explanations
4. **Keep it current** - Documentation should reflect the actual implementation
5. **Make it scannable** - Use headers, lists, and code blocks effectively

---

When the user asks you to summarize or document something, follow this workflow to create organized, digestible documentation in the `.summary/` directory.
