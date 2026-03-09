---
name: index
description: Maintain directory organization with index files (_index.md/_index.yaml/_index.json) and consistency prompts (_prompt.md)
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: development
---

# Directory Index System

Maintain directory organization with index files (`_index.md`, `_index.yaml`, `_index.json`) and consistency prompts (`_prompt.md`) to save context and ensure file consistency across projects.

## When to use me

Use this skill when:
- Starting a new project or directory structure
- Onboarding to an existing codebase
- Maintaining consistency across multiple files in a directory
- Documenting directory purpose and contents
- Setting up standards for file creation within directories
- Reducing context switching by providing directory-level guidance
- Creating self-documenting directory structures

## What I do

### 1. Index File Creation & Maintenance
- **Create `_index` files** in directories to document contents and purpose
- **Support multiple formats**: Markdown (default), YAML, or JSON based on project preference
- **Track directory contents**: List files and subdirectories with brief descriptions
- **Document directory purpose**: Explain why the directory exists and its role in the project
- **Provide navigation guidance**: Help users understand how to interact with the directory

### 2. Consistency Prompt Management
- **Create `_prompt.md` files** to guide file creation within directories
- **Establish directory-specific standards** for naming, formatting, and content
- **Provide templates and examples** for common file types in the directory
- **Maintain consistency** across files created by different contributors
- **Update prompts** as directory standards evolve

### 3. Context Preservation
- **Save directory context** to reduce cognitive load when navigating
- **Document relationships** between files in the directory
- **Explain conventions** and patterns used within the directory
- **Provide entry points** for understanding complex directory structures
- **Maintain historical context** about directory evolution and decisions

### 4. Navigation Optimization
- **Help models choose** which directories to explore based on index contents
- **Provide quick overviews** without needing to examine every file
- **Filter irrelevant directories** based on documented purposes
- **Accelerate understanding** of project structure and organization

## Index File Formats

### Default: Markdown (`_index.md`)
```markdown
# Directory: src/components/

## Purpose
Reusable UI components for the application.

## Contents
- **Button/** - Interactive button components
- **Form/** - Form elements and validation components  
- **Layout/** - Page layout and structural components
- **Modal/** - Dialog and overlay components
- **Navigation/** - Menu and navigation components

## Conventions
- Use TypeScript with React
- Follow atomic design principles
- Include Storybook stories
- Export via index.ts barrel files

## Related Directories
- `src/styles/` - Component styling
- `src/hooks/` - Custom React hooks
- `src/utils/` - Utility functions

## Last Updated
2024-03-15 - Added new Modal components
```

### YAML Format (`_index.yaml`)
```yaml
directory: src/components/
purpose: Reusable UI components for the application
contents:
  - name: Button
    description: Interactive button components
    type: directory
  - name: Form
    description: Form elements and validation components
    type: directory
  - name: Layout
    description: Page layout and structural components
    type: directory
conventions:
  - Use TypeScript with React
  - Follow atomic design principles
  - Include Storybook stories
related:
  - src/styles/
  - src/hooks/
  - src/utils/
last_updated: 2024-03-15
```

### JSON Format (`_index.json`)
```json
{
  "directory": "src/components/",
  "purpose": "Reusable UI components for the application",
  "contents": [
    {
      "name": "Button",
      "description": "Interactive button components",
      "type": "directory"
    },
    {
      "name": "Form",
      "description": "Form elements and validation components",
      "type": "directory"
    }
  ],
  "conventions": [
    "Use TypeScript with React",
    "Follow atomic design principles",
    "Include Storybook stories"
  ],
  "related": [
    "src/styles/",
    "src/hooks/",
    "src/utils/"
  ],
  "last_updated": "2024-03-15"
}
```

## Prompt File Format (`_prompt.md`)
```markdown
# File Creation Guidelines: src/components/

## When creating new component files in this directory:

### Naming Convention
- Use PascalCase for component names (e.g., `UserProfile.tsx`)
- Use descriptive names that indicate purpose
- Prefix with directory-specific prefixes if needed

### File Structure
```
ComponentName.tsx    # Main component file
ComponentName.styles.ts  # Component styles (if separate)
ComponentName.stories.tsx  # Storybook stories
ComponentName.test.tsx    # Component tests
index.ts            # Barrel export
```

### Content Requirements
- Include PropTypes or TypeScript interfaces
- Add JSDoc comments for public APIs
- Follow the existing component patterns
- Include accessibility attributes (aria-*)

### Import/Export Patterns
- Use named exports for components
- Export types/interfaces separately
- Use barrel files (index.ts) for directory exports

### Testing Requirements
- Write unit tests with React Testing Library
- Include accessibility tests
- Test all user interactions
- Mock external dependencies appropriately

### Styling Guidelines
- Use CSS-in-JS (Emotion) for styling
- Follow design system tokens
- Ensure responsive design
- Maintain accessibility color contrast

### Examples
See `Button/` and `Form/` directories for reference implementations.
```

## Examples

```bash
# Create index files for current directory
npm run index:create -- --format markdown
npm run index:create -- --format yaml
npm run index:create -- --format json

# Create index files recursively
npm run index:create -- --recursive --format markdown

# Update existing index files
npm run index:update -- --directory src/components/

# Generate prompt file
npm run index:prompt -- --directory src/components/

# Validate index consistency
npm run index:validate -- --directory .

# Convert between formats
npm run index:convert -- --from markdown --to yaml

# Interactive index creation
npm run index:interactive

# Generate directory tree with indexes
npm run index:tree -- --depth 3

# Check for missing indexes
npm run index:check -- --directory .
```

## Output format

```
Directory Index Report
──────────────────────────────
Directory: /project/src/components/

Index Files:
  ✅ _index.md - Present and up to date
  ✅ _prompt.md - Present and current
  ⚠️ Button/_index.md - Missing prompt file
  ❌ Form/_index.md - Stale (last updated 90 days ago)
  ✅ Layout/_index.md - Present and current

Directory Contents:
  - Button/ (5 files, 1 subdirectory)
  - Form/ (8 files, 2 subdirectories)
  - Layout/ (3 files, 0 subdirectories)
  - Modal/ (4 files, 1 subdirectory)
  - Navigation/ (6 files, 0 subdirectories)

Index Coverage:
  - Directories with index: 5/6 (83%)
  - Directories with prompt: 4/6 (67%)
  - Average index age: 15 days
  - Stale indexes (>30 days): 1

Consistency Check:
  ✅ Naming conventions followed
  ✅ File structures consistent
  ⚠️ Some missing test files
  ✅ Documentation present

Recommendations:
  1. Update Form/_index.md (stale)
  2. Add _prompt.md to Button/ directory
  3. Consider adding index to Modal/utils/ subdirectory
  4. Review test coverage for newer components

Next Actions:
  - Run: npm run index:update -- --directory Form/
  - Run: npm run index:prompt -- --directory Button/
  - Run: npm run index:create -- --directory Modal/utils/
```

## Notes

- **Index files should NOT contain detailed contents of subdirectories**, only names and general concepts
- **Markdown is the default format** for readability and ease of editing
- **YAML and JSON** are available for machine-readable indexes
- **Prompt files** should be specific to the directory's purpose and content types
- **Indexes should be updated** when directory structure or purpose changes significantly
- **Balance detail with brevity** - indexes should be helpful but not verbose
- **Consider version controlling** index files alongside code
- **Use indexes as living documentation** that evolves with the project
- **Prompt files help maintain consistency** across teams and over time
- **The system saves context** by documenting directory purpose and relationships
