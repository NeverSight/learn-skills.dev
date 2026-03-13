---
name: cmd-idiot-proof-docs
description: Simplify documentation for clarity and scannability with approval-gated edits
disable-model-invocation: true
---

# Simple Docs for Humans and Agents

Use this command to write or rewrite documentation so it is simple, fast to scan, and easy to execute.

## Primary Goal

- Bias toward simple docs.
- Start with the shortest successful path.
- Preserve original meaning and factual content while reordering for clarity.

## Required Output Order

1. Quickstart (always first)
2. Main workflow
3. Configuration/reference tables (when relevant)
4. Alternative paths (only when they are true user/code path alternatives)
5. Extra details at the end inside `<details><summary>...</summary>...</details>`

## Approval Gate (Required)

- Before editing any file, show a change preview for approval.
- Use this exact preview structure for each file:
  - Additions
  - Removals
  - Changes
- Show the concrete text to be added, removed, or changed.
- Wait for explicit user approval before applying edits.
- Apply only the approved edits.
- If approval is not granted, do not modify files.

## Core Rules

- Optimize for both human readers and agent readers.
- Maximize copy-paste command snippets.
- Prefer short sections and concise language.
- Use Markdown tables when information is structured.
- Use Mermaid diagrams when they improve understanding of flow or architecture.
- Avoid unnecessary sections.
- Avoid "Optional" sections unless they represent an actual alternate path.
- Put superfluous/background material at the end.
- Add "Code Structure" only when repository layout helps task completion.

## Command Block Rules (Strict)

- Do not place comments inside bash code blocks.
- Put labels outside code blocks.

Correct pattern:

Start the server:

```bash
make start_server
```

Run a command:

```bash
make run_command
```

Incorrect pattern (separate steps combined in one unlabeled block):

```bash
make start_server
make run_command
```

## Section Defaults

Use only sections that add value for the specific document. Default section set:

- Quickstart
- Main Workflow
- Configuration
- Code Structure (only if useful)
- Troubleshooting (only for real recurring issues)

## Configuration Table Format

If environment variables or configuration values are required, use this format:

| Name | Purpose | Default |
| --- | --- | --- |
| `APP_ENV` | Runtime environment | `development` |
| `API_URL` | Base URL for API calls | `http://localhost:8000` |

## Details Block Rule

Move long explanations, implementation notes, and low-priority reference material into details blocks:

```markdown
<details>
<summary>Deep dive: request lifecycle</summary>

Detailed explanation here.

</details>
```

## Deliverable

- Return the final output as Markdown (`.md`).
- Keep all important content, but simplify, reorder, and prioritize for quick execution.
