---
name: context-bundling
description: Create technical bundles of code, design, and documentation for external review or context sharing. Use when you need to package multiple project files into a single Markdown file while preserving folder hierarchy and providing contextual notes for each file.
version: 1.0.0
---
# Context Bundling Skill 📦

## Overview
This skill centralizes the knowledge and workflows for creating "Context Bundles." These bundles are essential for compiling large amounts of code and design context into a single, portable Markdown file for sharing with other AI agents or for human review.

## 🎯 Primary Directive
**Curate, Consolidate, and Convey.** You do not just "list files"; you architect context. You ensure that any bundle you create is:
1. **Complete:** Contains all required dependencies, documentation, and source code.
2. **Ordered:** Flows logically (Identity/Prompt → Manifest → Design Docs → Source Code).
3. **Annotated:** Every file must include a brief note explaining its purpose in the bundle.

## Core Workflow: Generating a Bundle

The context bundler operates through a simple JSON manifest pattern. 

### 1. Analyze the Intent
Before bundling, determine what the user is trying to accomplish:
- **Code Review**: Include implementation files and overarching logic.
- **Red Team / Security**: Include architecture diagrams and security protocols.
- **Bootstrapping**: Include `README`, `.env.example`, and structural scaffolding.

### 2. Define the Manifest Schema
You must formulate a JSON manifest containing the exact files to be bundled.
```json
{
  "title": "Bundle Title",
  "description": "Short explanation of the bundle's goal.",
  "files": [
    {
      "path": "docs/architecture.md",
      "note": "Primary design document"
    },
    {
      "path": "src/main.py",
      "note": "Core implementation logic"
    }
  ]
}
```

### 3. Generate the Markdown Bundle
Use your native tools (e.g., `cat`, `view_file`, or custom scripts depending on the host agent environment) to read the contents of each file listed in the manifest and compile them into a target `output.md` file.

The final bundle format must follow this structure:

```markdown
# [Bundle Title]
**Description:** [Description]

## Index
1. `docs/architecture.md` - Primary design document
2. `src/main.py` - Core implementation logic

---

## File: `docs/architecture.md`
> Note: Primary design document

\`\`\`markdown
... file contents ...
\`\`\`

---

## File: `src/main.py`
> Note: Core implementation logic

\`\`\`python
... file contents ...
\`\`\`
```

## Conditional Step Inclusion & Error Handling
If a file requested in the manifest does not exist or raises a permissions error:
1. Do **not** abort the entire bundle.
2. In the final `output.md`, insert a placeholder explicitly declaring the failure:
   ```markdown
   ## File: `missing/file.py`
   > 🔴 **NOT INCLUDED**: The file was not found or could not be read.
   ```
3. Proceed bundling the remaining valid files.

## Best Practices & Anti-Patterns
1. **Self-Contained Functionality:** The output file must contain 100% of the context required for a secondary agent to operate without needing to run terminal commands.
2. **Specialized Prompts:** If bundling for an external review (e.g., a "Red Team" security check), suggest including a specialized prompt file as the very first file in the bundle to guide the receiving LLM.

### Common Bundling Mistakes
- **Bloat**: Including `node_modules/` or massive `.json` dumps instead of targeted files.
- **Silent Exclusion**: Filtering out an unreadable file without explicitly declaring it missing (violates transparency).
