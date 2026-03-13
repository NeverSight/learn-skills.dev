---
name: appbuilder-connector-setup
description: Set up Adobe App Builder connector projects. Routes users through three paths based on workspace JSON availability (JSON-driven, guided download, or interactive script), with connector-type-to-template mapping. Also handles post-setup tasks like deployment, troubleshooting, and configuration management.
---

# App Builder Connector Setup

Guide users through Adobe App Builder connector setup. Act as the interactive UI for Options 1 and 2 by running non-interactive commands and asking explicit choices. Hand off Option 3 to terminal onboarding.

## Connector Type Mapping

Resolve template names internally. Do not ask users to type template package names.

| Connector Type | Template Name                   |
| -------------- | ------------------------------- |
| Translate      | `@adobe/generator-app-excshell` |

## Connector Type Inference Rule

Infer connector type from the user's first request when explicit.

- If user says `set-up translate connector for me` (or equivalent), set type to `Translate` and do not ask connector-type question.
- If user says only `set-up connector for me` (type not specified), ask connector-type question in Step 1.3.

## Required Order

Follow this order without reordering:

1. Phase 0: Developer Console guidance
2. Phase 0.1: Project exists gate
3. Prerequisites check
4. Authentication preflight
5. Phase 1: Entry question
6. Option 1, 2, or 3

Never request workspace JSON before authentication succeeds.

## AskQuestion Rule

When using `AskQuestion`, wait for the user response and continue from the matching branch in the next turn.

## Phase 0: Developer Console Setup

Instruct user to verify they already created an App Builder project:

1. Go to `https://developer.adobe.com/console`
2. Select organization
3. Create project from template (`App Builder`)
4. Open a workspace (`Stage` or `Production`)

### Phase 0.1: Project Exists Gate

Use `AskQuestion`:

- Prompt: `Have you created an App Builder project already in Adobe Developer Console?`
- Options: `Yes`, `No`

Branch:

- `Yes`: continue to prerequisites.
- `No`: stop flow and ask user to create project first.

## Prerequisites Check

Run:

```bash
node --version
npm --version
aio --version
```

If Node is missing or `<20`, use `AskQuestion` with:

1. Install via nvm (recommended)
2. Install via Homebrew (macOS)
3. Install manually

Handle each branch:

- nvm:

```bash
nvm install 20
nvm use 20
```

- Homebrew:

```bash
brew install node@20
```

- Manual: point to `https://nodejs.org/`, wait for confirmation.

Verify with `node --version` before continuing.

If AIO CLI is missing:

```bash
npm install -g @adobe/aio-cli
aio --version
```

Continue to authentication preflight only after prerequisites pass.

## Authentication Preflight

**CI environment check (required first step):** Before running any auth command, check whether `CI=1` is set:

```bash
echo "CI=${CI}"
```

If `CI=1`, the IMS Auth SDK will block interactive login entirely (no URL, just an error). This happens in Cursor's agent shell. In that case, prefix ALL auth commands with `env CI=` to unset it for that invocation.

Run in foreground and wait for completion:

```bash
# Standard (non-CI shell):
aio auth login --open

# Cursor agent shell (CI=1 is injected automatically):
env CI= aio auth login --open
```

Treat auth output as sensitive; do not echo raw token values.

Interpretation:

- Success: continue.
- Waiting with manual login URL: capture URL and run:

```bash
open "<capturedLoginUrl>"
```

Then keep waiting for the original auth command to exit.

- Failure or timeout: retry once with:

```bash
# Standard:
aio auth login --force --no-open

# Cursor agent shell:
env CI= aio auth login --force --no-open
```

If retry shows login URL, run `open "<capturedLoginUrl>"` and wait.

Environment notes:

- If auth writes outside workspace and fails permission checks (for example `~/.config/aio`), rerun with elevated permissions.
- If `open` fails because of sandbox/GUI limits, rerun `open` with elevated permissions.
- Cursor agent shell always sets `CI=1`, `NO_COLOR=1`, and `TERM=dumb`. Use `env CI=` prefix on all `aio auth` commands when running inside Cursor.

If both login attempts fail, stop setup and hand off:

```bash
npx appbuilder-connector-interactive-onboarding
```

Do not request workspace JSON after auth failure.

## Phase 1: Entry Question

Run only after authentication passes.

Use `AskQuestion`:

- Prompt: `Do you have the workspace config JSON downloaded from Adobe Developer Console?`
- Options:

1. `Yes, I'll share the file path`
2. `No — how do I download it?`
3. `No — I want to set it up interactively`

Branch:

- Option 1 -> Option 1 (JSON Path)
- Option 2 -> Option 2 (Download Guide)
- Option 3 -> Option 3 (Interactive Script)

## Option 1: JSON Path (Agent-Driven)

### Step 1.1: Request JSON

Ask for either:

- JSON file path (example: `~/Downloads/MyProject-393012-Stage.json`)
- JSON content pasted in chat or shared by `@` reference

### Step 1.2: Read and Confirm JSON

Read JSON and extract:

- `project.org.name`
- `project.name`
- `project.workspace.name`

Confirm with `AskQuestion`:

- Prompt: `Configuring for Organization: [org], Project: [project], Workspace: [workspace]. Proceed with this workspace config?`
- Options:

1. `Yes, continue`
2. `No, I'll provide a different JSON`

Branch:

- `Yes`: continue.
- `No`: return to Step 1.1.

Do not rerun auth unless user reports auth errors.

### Step 1.3: Select Connector Type

If connector type is already explicit in user request (for example `translate`), skip this step and use that type.
Otherwise use `AskQuestion`:

- Prompt: `What type of connector are you building?`
- Options: `Translate`

Resolve template from mapping table internally.

### Step 1.4: Choose Target Directory

Set target directory automatically to `./<project-name-lowercase>`, announce it, then ensure it exists:

```bash
mkdir -p <targetDir>
```

### Step 1.5: Pre-seed Workspace Config (Required)

Run before `aio app init`:

```bash
aio app use <jsonPath> --merge --no-input
```

Run in `working_directory: "<targetDir>"`.

### Step 1.6: Scaffold

Run:

```bash
aio app init <targetDir> --template <templateName> --yes --import <jsonPath>
```

If the runner supports non-blocking execution, poll until command exit. After completion, verify `<targetDir>/app.config.yaml` exists.

### Step 1.7: Install Dependencies

Run in `<targetDir>`:

```bash
npm install
```

If install fails, suggest `npm cache clean --force` and retry.

### Step 1.8: Complete

Report completion and provide next commands without auto-running:

```bash
cd <targetDir>
aio app dev
aio app run
aio app deploy
```

## Option 2: Download Guide

Provide download steps:

1. Open `https://developer.adobe.com/console`
2. Select organization
3. Open project
4. Open workspace in left sidebar
5. Click `Download All`
6. Share JSON path or JSON contents

When JSON arrives, continue with Option 1 from Step 1.2.

## Option 3: Interactive Script

Hand off and stop:

```bash
npx appbuilder-connector-interactive-onboarding
```

Tell user to return for deployment, troubleshooting, or post-setup help.

## Post-Setup Command Guidance

Default to guidance-first. Do not auto-run long-lived commands (`aio app dev`, `aio app run`) unless user explicitly asks.

Common commands:

```bash
aio app dev
aio app run
aio app deploy
aio app undeploy
aio app logs
```

## Configuration Management

View current selections:

```bash
aio console org selected
aio console project selected
aio console workspace selected
```

Switch workspace:

```bash
aio console workspace list --json
aio console workspace select <workspaceId>
aio console workspace dl /tmp/workspace-config.json
aio app use /tmp/workspace-config.json --merge --no-input
```

Switch project:

```bash
aio console project list --json
aio console project select <projectId>
```

Switch organization:

```bash
aio console org list --json
aio console org select <orgId>
```

Clear and re-authenticate:

```bash
aio auth logout
aio auth login
```

If login fails, force refresh:

```bash
aio auth logout
aio auth login --force
```

## References

- [App Builder Guide](references/app-builder-guide.md)
- [Troubleshooting](references/troubleshooting.md)
- [Project Structure](references/project-structure.md)
- [Official Documentation](https://developer.adobe.com/app-builder/docs/intro_and_overview/)
- [Adobe Developer Console](https://developer.adobe.com/console)
- [I/O Runtime Documentation](https://developer.adobe.com/runtime/docs/)
- [AIO CLI Reference](https://developer.adobe.com/app-builder/docs/resources/cli/)
