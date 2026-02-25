---
name: signoff-flow
description: Use when user mentions signoff, sign-off, approval workflow, initiative approval, BMAD workflow, or wants to manage product initiatives through approval stages (PRD, UX, Architecture, Epics, Readiness). Automatically installs required tools and guides users through complete signoff workflow.
---

# Signoff Flow Workflow

Guide initiatives through a structured approval process using GitHub PRs as gates and Jira tickets for visibility.

## CRITICAL: Auto-Install Behavior

**When a required tool is missing, EXECUTE the installation command directly. Do NOT just show the command to the user.**

This skill is designed for non-technical users who should not need to copy/paste commands.

## CRITICAL: Confirmation Required for External Actions

**ALWAYS ask for user confirmation BEFORE executing these actions:**

| Action | Requires Confirmation | Example Confirmation Message |
|--------|----------------------|------------------------------|
| Commit & Push | ✅ YES | "I'm about to commit and push these changes to GitHub. Proceed?" |
| Create Pull Request | ✅ YES | "I'm about to create a PR titled '[BMAD][FEAT-123] PRD' with reviewers @user1, @user2. Proceed?" |
| Create Jira Tickets | ✅ YES | "I'm about to create 3 Jira tickets in project PROJ: [list tickets]. Proceed?" |
| Install tools | ❌ NO | Execute automatically |
| Clone repo | ❌ NO | Execute automatically |
| Create local files | ❌ NO | Execute automatically |

**Wait for explicit user confirmation (e.g., "yes", "proceed", "go ahead") before executing confirmed actions.**

## Pre-flight Check (ALWAYS RUN FIRST)

When user wants to use signoff flow, execute these checks and auto-install as needed:

### Step 1: Check and Install Homebrew (macOS)

```bash
which brew
```

**If brew is NOT found and OS is macOS:**

Tell the user: "I need to install Homebrew first. This requires your password and may take a few minutes."

Then provide the command for them to run (Homebrew requires interactive installation):
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Wait for confirmation before continuing.

### Step 2: Check and Install Git

```bash
which git
```

**If git is NOT found:**
- macOS: EXECUTE `xcode-select --install` (requires user interaction)
- Tell user to wait for installation to complete

### Step 3: Check and Install GitHub CLI

```bash
which gh
```

**If gh is NOT found, AUTOMATICALLY EXECUTE:**

macOS:
```bash
brew install gh
```

Windows:
```bash
winget install --id GitHub.cli -e
```

**DO NOT just show the command. EXECUTE IT.**

After installation, verify:
```bash
gh --version
```

### Step 4: Check GitHub Authentication

```bash
gh auth status
```

**If NOT authenticated:**

Tell the user: "I need to connect to your GitHub account. This will open a browser window."

Then EXECUTE:
```bash
gh auth login --web
```

This is interactive and requires user action in the browser.

### Step 5: Check and Install Atlassian CLI (for Jira)

```bash
which acli
```

**If acli is NOT found, AUTOMATICALLY EXECUTE:**

```bash
brew tap atlassian/homebrew-acli && brew install acli
```

**DO NOT just show the command. EXECUTE IT.**

After installation, verify:
```bash
acli --version
```

### Step 6: Check Jira Authentication

```bash
acli jira auth status
```

**If NOT authenticated:**

⚠️ **This step requires manual user action** because the command needs interaction after browser auth.

Tell the user:

```
I need you to connect to your Jira account. This is a one-time setup.

Please run this command in your terminal:

    acli jira auth login --web

This will:
1. Open your browser for Atlassian login
2. After you authorize, come back to the terminal
3. Press ENTER to complete the authentication

Let me know when you're done!
```

**DO NOT execute this command directly** - it will hang waiting for user input.

Wait for user to confirm they completed authentication, then verify:
```bash
acli jira auth status
```

### Step 7: Check Project

Look for `_bmad-output/governance/governance.yaml` in the current directory.

If not found, help user find or clone a project.

## Summary of Auto-Install Behavior

| Tool | Check Command | Install Command (EXECUTE, don't suggest) |
|------|---------------|------------------------------------------|
| Homebrew | `which brew` | Interactive - guide user |
| Git | `which git` | `xcode-select --install` (interactive) |
| gh CLI | `which gh` | `brew install gh` |
| Atlassian CLI | `which acli` | `brew tap atlassian/homebrew-acli && brew install acli` |

| Auth | Check Command | Auth Command | Notes |
|------|---------------|--------------|-------|
| GitHub | `gh auth status` | `gh auth login --web` | EXECUTE - works automatically |
| Jira | `acli jira auth status` | `acli jira auth login --web` | ⚠️ USER MUST RUN MANUALLY - requires Enter after browser auth |

## Important Instructions for Claude

1. **EXECUTE installation commands directly** - Users are non-technical and should not copy/paste
2. **Wait for each installation to complete** before proceeding to the next check
3. **Only show commands to user** when they require interactive input (passwords, browser auth)
4. **Verify installation** after each install by running the tool with `--version`
5. **Be patient** - installations can take 1-2 minutes
6. **ALWAYS ASK FOR CONFIRMATION** before commit/push, creating PRs, or creating Jira tickets

## Workflow Steps (After Prerequisites Met)

### Finding a Project

If no governance found in current directory:

```bash
# List user's GitHub orgs
gh api user/orgs -q '.[].login'

# List recent repos
gh repo list --limit 10
```

Ask user which project they want to work on.

### Cloning a Project

When user specifies a project (e.g., "HALO/my-project"):

```bash
mkdir -p ~/signoff-projects
gh repo clone OWNER/REPO ~/signoff-projects/REPO
cd ~/signoff-projects/REPO
```

### Setting Up Governance

If `_bmad-output/governance/governance.yaml` doesn't exist, ask for:
- BA lead GitHub username(s)
- Design lead GitHub username(s)
- Dev lead GitHub username(s)
- Jira project key

Then CREATE the file:

```yaml
version: 1
groups:
  ba:
    leads:
      github_users: ["username1"]
  design:
    leads:
      github_users: ["username2"]
  dev:
    leads:
      github_users: ["username3"]

jira:
  project_key: "PROJECT"
  issue_types:
    signoff_request: "Task"

signoff_rules:
  prd:
    required_groups: [ba, design, dev]
  ux:
    required_groups: [ba, design]
  architecture:
    required_groups: [dev]
  epics_stories:
    required_groups: [ba, dev]
  readiness:
    required_groups: [ba, design, dev]
```

### Creating an Initiative

Ask for:
- Initiative key (e.g., FEAT-123)
- Title

Create directory structure:
```
_bmad-output/initiatives/<key>/
├── state.yaml
├── timeline.md
└── artifacts/
```

### Advancing Through Stages (WITH CONFIRMATIONS)

For each stage (prd → ux → architecture → epics_stories → readiness):

#### Step 1: Create artifact stub (NO confirmation needed)
Create the artifact file locally.

#### Step 2: Create branch (NO confirmation needed)
```bash
git checkout -b bmad/<key>/<artifact>
```

#### Step 3: Commit and Push (⚠️ CONFIRMATION REQUIRED)

**BEFORE executing, show the user:**
```
I'm about to commit and push these changes to GitHub:

📁 Files to commit:
- _bmad-output/initiatives/<key>/artifacts/<ARTIFACT>.md
- _bmad-output/initiatives/<key>/state.yaml

📝 Commit message: "[BMAD][<key>] Add <artifact> artifact"

🔄 This will push to branch: bmad/<key>/<artifact>

Do you want me to proceed? (yes/no)
```

**Wait for user confirmation before executing:**
```bash
git add .
git commit -m "[BMAD][<key>] Add <artifact> artifact"
git push -u origin bmad/<key>/<artifact>
```

#### Step 4: Create Pull Request (⚠️ CONFIRMATION REQUIRED)

**BEFORE executing, show the user:**
```
I'm about to create a Pull Request on GitHub:

📋 Title: [BMAD][<key>] <Artifact>
📝 Description: BMAD signoff request for <artifact> phase
👥 Reviewers: @user1, @user2, @user3 (from governance config)
🔀 Branch: bmad/<key>/<artifact> → main

Do you want me to proceed? (yes/no)
```

**Wait for user confirmation before executing:**
```bash
gh pr create --title "[BMAD][<key>] <Artifact>" --body "BMAD signoff request..." 
gh pr edit --add-reviewer user1,user2,user3
```

#### Step 5: Create Jira Tickets (⚠️ CONFIRMATION REQUIRED)

**BEFORE executing, show the user:**
```
I'm about to create Jira tickets for signoff:

🎫 Project: <JIRA_PROJECT_KEY>
📝 Tickets to create:
  1. "[BMAD][<key>][<artifact>] Signoff required — BA"
  2. "[BMAD][<key>][<artifact>] Signoff required — DESIGN"  
  3. "[BMAD][<key>][<artifact>] Signoff required — DEV"

Do you want me to proceed? (yes/no)
```

**Wait for user confirmation before executing:**
```bash
acli jira workitem create --project "KEY" --type "Task" --summary "[BMAD][<key>][<artifact>] Signoff - BA"
acli jira workitem create --project "KEY" --type "Task" --summary "[BMAD][<key>][<artifact>] Signoff - DESIGN"
acli jira workitem create --project "KEY" --type "Task" --summary "[BMAD][<key>][<artifact>] Signoff - DEV"
```

## Example Conversation (Correct Behavior with Confirmations)

```
User: I want to advance the PRD for initiative FEAT-100

Agent: I've created the PRD artifact locally. Now I need to push it to GitHub.

       I'm about to commit and push these changes:
       
       📁 Files: _bmad-output/initiatives/FEAT-100/artifacts/PRD.md
       📝 Commit: "[BMAD][FEAT-100] Add PRD artifact"
       🔀 Branch: bmad/FEAT-100/prd
       
       Do you want me to proceed?

User: yes

Agent: ✅ Changes committed and pushed.
       
       Now I'll create a Pull Request.
       
       📋 Title: [BMAD][FEAT-100] PRD
       👥 Reviewers: @alice (BA), @bob (Design), @charlie (Dev)
       
       Do you want me to proceed?

User: yes

Agent: ✅ PR #42 created: https://github.com/org/repo/pull/42
       
       Finally, I'll create Jira tickets for tracking.
       
       🎫 Tickets to create in PROJECT:
         1. "[BMAD][FEAT-100][prd] Signoff required — BA"
         2. "[BMAD][FEAT-100][prd] Signoff required — DESIGN"
         3. "[BMAD][FEAT-100][prd] Signoff required — DEV"
       
       Do you want me to proceed?

User: yes

Agent: ✅ Created tickets: PROJECT-101, PROJECT-102, PROJECT-103
       
       All done! The PRD is now pending signoff.
```

## WRONG Behavior (Do NOT do this)

```
User: I want to advance the PRD

Agent: [Creates files, commits, pushes, creates PR, creates tickets all at once]
       
       ✅ Done! Created PR and 3 Jira tickets.
```

**THIS IS WRONG.** The agent should ask for confirmation before each external action.
