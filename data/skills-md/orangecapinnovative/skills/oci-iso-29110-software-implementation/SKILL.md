---
name: oci-iso-29110-software-implementation
description: "Generate ISO/IEC 29110-5-1-2:2025 (VSE Generic Basic Profile) work-product documents as .docx files for a software project. Use when asked to create or regenerate any of the seven ISO 29110 implementation documents: Software Design, Software Components, Implementation Environment, Maintenance Document, Operation Guidelines, Project Repository, or Repository Backup."
---

# OCI — ISO 29110 Software Implementation Documents

Generate the seven ISO/IEC 29110 work-product documents as `.docx` files by reading the project codebase and prompting the user only for information that cannot be derived from code.

## How It Works

1. The user asks to generate one of the seven ISO 29110 documents (see table below).
2. Load the shared rules file **first**: `iso29110-docx-rules.md` — it defines the shared context file, codebase cache protocol, and all `.docx` rendering rules that apply to every document type.
3. Load the skill file for the requested document type and follow its steps.
4. Run the generated Node.js script with `node` to produce the `.docx` file.

## Document Skills

| Document | When to use | Skill file |
|---|---|---|
| Software Design (SD) | "Generate the software design document" | `iso29110-software-design.md` |
| Software Components (SC) | "Generate the software components document" | `iso29110-software-components.md` |
| Implementation Environment (IE) | "Generate the implementation environment document" | `iso29110-implementation-environment.md` |
| Maintenance Document (MD) | "Generate the maintenance document" | `iso29110-maintenance-document.md` |
| Operation Guidelines (OM) | "Generate the operation guidelines / operations manual" | `iso29110-operation-guidelines.md` |
| Project Repository (RP) | "Generate the project repository document" | `iso29110-project-repository.md` |
| Repository Backup (RPB) | "Generate the repository backup document" | `iso29110-repository-backup.md` |

## Shared Infrastructure (read before any document skill)

- **`iso29110-docx-rules.md`** — must be loaded first; defines:
  - Part A: Shared context file (`.iso29110-context.json`) — avoids re-asking the same project questions across sessions.
  - Part B: Codebase cache (`.iso29110-codebase-cache.json`) — avoids re-reading the codebase across sessions.
  - Part C: Rendering rules — correct `.docx`-js patterns for fonts, tables, images, headings, and code blocks.

## Usage

```
User: "Generate the Software Design document for my project."
→ Load iso29110-docx-rules.md, then iso29110-software-design.md, and follow the steps.

User: "Create the maintenance document."
→ Load iso29110-docx-rules.md, then iso29110-maintenance-document.md, and follow the steps.
```

## Output

Each skill generates a Node.js script using the `docx` npm package and runs it to produce:

```
{ProjectName}_{DocumentType}_V1.0.docx
```

in the user's current working directory.

## Notes

- The `docx` package must be available: `npm install docx` if not already present.
- Context and cache files (`.iso29110-context.json`, `.iso29110-codebase-cache.json`) are written to the working directory. Add them to `.gitignore` if you do not want them committed.
- Author, reviewer, and approver fields are left blank in the generated document for the team to fill in.
