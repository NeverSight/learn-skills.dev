---
name: openspec-setup
description: Set up OpenSpec in a project - check the CLI, initialize the openspec/ directory, and create the starter VERIFY.md and GLOSSARY.md. Use when the user wants to start using OpenSpec in a project, or when openspec/VERIFY.md or openspec/GLOSSARY.md is missing.
license: MIT
compatibility: Requires Node.js and npm.
metadata:
  author: openspec
  version: "1.0"
---

Set up OpenSpec in the current project. This workflow is **idempotent**: run it again at any time. It does only the steps that are still missing and never overwrites an existing file.

**CLI compatibility**: On Windows, use `openspec.cmd` in place of `openspec` if PowerShell execution policy blocks the `.ps1` shim.

**Input**: No argument is needed. The user can say what to set up (for example "only the glossary").

**Steps**

1. **Check the OpenSpec CLI**
   ```bash
   openspec --version
   ```
   - If the command fails, tell the user that the CLI is not installed. Ask for confirmation, then run:
     ```bash
     npm install -g @fission-ai/openspec@latest
     ```
   - If the user declines, STOP and explain that the other workflows need the CLI.

2. **Check the project directory**

   Look for `openspec/` in the project root.

   - **If it does not exist**: Ask the user for confirmation, then run:
     ```bash
     openspec init --no-animation --tools none
     ```
     - `--tools none` is required. It creates `openspec/` only. It does NOT write the official skills, so it does not overwrite this fork's skills.
     - If the user wants OpenSpec artifacts in a specific language, add `--language <language>`.
   - **If it exists**: Say "OpenSpec is already initialized" and go to step 3. Do NOT run `openspec init` again.

3. **Check the extension files**

   Check each file separately:
   - `openspec/VERIFY.md`
   - `openspec/GLOSSARY.md`

   If both exist, say so and go to step 5.

   For each missing file, create it from the matching template in step 4 **after the user confirms**. If a file exists, do NOT read it for replacement and do NOT change it.

4. **Create the files from the templates**

   **`openspec/GLOSSARY.md`**
   ````markdown
   # Glossary

   ## core

   - **ExampleTerm** — Definition of example domain term. Aliases: alias1, alias2.
   ````
   Write the file as shown. Tell the user to replace the example entry with real project terms, or to let `openspec-grill` record terms during design discussions.

   **`openspec/VERIFY.md`**
   ````markdown
   # Verification

   ## <project-or-module-name>

   ```bash
   # Add project-specific lint, typecheck, or test commands (e.g. npm test / cargo test)
   npm test
   ```
   ````
   Before you write this file, look for the project's real verification commands in common files (for example `package.json` scripts, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Makefile`). If you find commands:
   - Show them to the user as a proposal. Fill in the module heading and the command block only after the user confirms.
   - Use only commands that exist in those files. Do NOT guess commands.

   If you find nothing, write the template as shown and tell the user to edit it.

   Keep the file structure (headings and fenced command blocks) unchanged.

5. **Show the result**

**Output**

Summarize each step as one of: done, already present, skipped (user declined). For example:

```
## OpenSpec Setup

- CLI: openspec 1.x.x (already installed)
- Project: openspec/ initialized
- GLOSSARY.md: created
- VERIFY.md: already present

Next: run `openspec-explore` or `openspec-grill` to think through an idea, or `openspec-propose` to start a change.
```

**Guardrails**
- Never overwrite or modify an existing `openspec/VERIFY.md` or `openspec/GLOSSARY.md`.
- Never run `openspec init` when `openspec/` already exists.
- Always pass `--tools none` to `openspec init`. A tool selection would overwrite this fork's skills with the official versions.
- Ask for confirmation before you install the CLI, run `openspec init`, or write a file.
- Never run the commands that you find or write in `VERIFY.md`. Verification runs in `openspec-verify-change`.
- Create only the files named in this workflow. Do NOT create changes, specs, or other files.
- Do NOT run git commands.
