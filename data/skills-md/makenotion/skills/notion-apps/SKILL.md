---
name: notion-apps
description: Set up and scaffold Notion Apps with the Notion Apps SDK and `ntn`; use when starting a Notion App project.
---

# Notion Apps

## Confirm alpha access

Before running commands or inspecting an App project, ask the user to confirm that
they are in the Notion Apps alpha. CLI authentication, an enabled CLI experiment, or
a locally working SDK does not confirm alpha access. If the user says no or cannot
confirm, explain that SDK code may build locally but deployment requires alpha access,
and stop the App workflow.

## Set up and scaffold

After alpha access is confirmed, check that the Notion CLI is installed with
`ntn --version`. If it is missing, install it using the command for the user's
platform:

```bash
# macOS and Linux
curl -fsSL https://ntn.dev | bash

# Windows
winget install Notion.ntn
```

Scaffold a fresh App project with dependencies installed and Git initialized:

```bash
ntn apps new --install --git <app-directory>
```

Always pass an explicit destination. Agents cannot use the CLI's interactive
directory prompt. Use `.` when the current directory is empty and is an appropriate
project root; otherwise infer a suitable directory from the user's request or
surrounding context. If no safe destination can be inferred, ask where the project
should go before scaffolding. If the `apps` command is unavailable, enable it with
`ntn experiments enable apps` and retry.

Once the project is instantiated, work from its root and read its `AGENTS.md`
completely. That file contains the App design, implementation, capability, and
deployment guidance for the generated project. Follow it and the installed SDK's
version-specific guidance for the rest of the task.
