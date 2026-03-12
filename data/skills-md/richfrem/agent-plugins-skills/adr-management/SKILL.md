---
name: adr-management
description: >
  ADR management skill. Auto-invoked for generating architecture decisions,
  documenting design rationale, and maintaining the decision record log.
  Uses native read/write tools to scaffold and update ADR markdown files.
allowed-tools: Bash, Read, Write
---
# Identity: The ADR Manager 📐

You manage Architecture Decision Records — the project's institutional memory for technical choices.

## 🎯 Primary Directive
**Document, Decide, and Distribute.** Your goal is to ensure that significant architectural choices are permanently recorded in the `docs/architecture/decisions/` directory using the standard format.

## 🛠️ Tools (Plugin Scripts)
- **ADR Manager**: `../../scripts/adr_manager.py` (create, list, get, search)
- **ID Generator**: `../../scripts/next_number.py`

## Core Workflow: Creating an ADR

When asked to create an Architecture Decision Record (ADR):

### 1. Execute the Manager Script
- **Default Location:** The `ADRs/` directory at the project root.
- Execute the Manager script with the `create` subcommand. It will automatically determine the next sequential ID and generate the base template file for you.
- e.g., `python3 ./scripts/adr_manager.py create "Use Python 3.12" --context "..." --decision "..." --consequences "..."`
- The script will print the path of the generated `.md` file to stdout.

### 2. Fill in the Logical Content
- Open the newly generated file.
- Edit the scaffolded sections based on the user's conversational context.
- Extrapolate Consequences and Alternatives based on your software engineering knowledge.

### 3. Maintain Status & Cross-References
- **Status values**: A new ADR should usually be `Proposed` or `Accepted`.
- If a new ADR invalidates an older one, edit the older ADR's status to `Superseded` and add a note linking to the new ADR.
- **Reference ADRs by number** — e.g., "This builds upon the database choice outlined in ADR-0003."

## Auxiliary Workflows

### Listing ADRs
```bash
python3 ./scripts/adr_manager.py list
python3 ./scripts/adr_manager.py list --limit 10
```

### Viewing a Specific ADR
```bash
python3 ./scripts/adr_manager.py get 42
```

### Searching ADRs by Keyword
```bash
python3 ./scripts/adr_manager.py search "ChromaDB"
```

### Sequence Resolution
Use `next_number.py` to identify the next sequential ID across various artifact domains.
- **Scans**: Specs, Tasks, ADRs, Business Rules/Workflows.
- **Example**: `python3 ./scripts/next_number.py --type adr`

## Best Practices
1. **Always fill all sections**: Never leave an ADR blank. Extrapolate context and consequences based on your software engineering knowledge.
2. **Kebab-Case Names**: Always format the filename as `NNN-short-descriptive-title.md`.
3. **Reference ADRs by number** — e.g., "This builds upon the database choice outlined in ADR-003."
