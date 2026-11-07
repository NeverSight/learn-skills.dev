---
name: my-brain-is-full-crew
description: A team of 10 AI agents that manage your Obsidian vault for knowledge, nutrition, and mental wellness using Claude Code
triggers:
  - set up my brain crew obsidian agents
  - install my brain is full crew
  - configure obsidian claude agents vault
  - add AI agents to my obsidian vault
  - set up second brain with claude agents
  - initialize my brain crew vault
  - configure knowledge wellness nutrition agents
  - help me install my brain is full crew
---

# My Brain Is Full — Crew

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

A crew of 10 AI agents embedded in your Obsidian vault that manage knowledge, nutrition, and mental wellness through natural conversation with Claude Code. Built by a PhD researcher for people who are drowning — not just optimizing.

---

## What It Does

The Crew installs 10 specialized agents into your vault's `.claude/` directory. Each agent has its own system prompt, tool restrictions, and model assignment. You talk to Claude Code naturally; it activates the right agent automatically.

| Agent | Role |
|---|---|
| **Architect** | Vault setup, onboarding, folder structure |
| **Scribe** | Captures messy text into clean structured notes |
| **Sorter** | Nightly inbox triage — routes notes to correct folders |
| **Seeker** | Search and synthesis across your entire vault |
| **Connector** | Discovers hidden links between notes |
| **Librarian** | Weekly health checks, dedup, broken link repair |
| **Transcriber** | Turns recordings/transcripts into structured meeting notes |
| **Postman** | Bridges Gmail + Google Calendar with your vault |
| **Food Coach** | Meal ideas, grocery lists, wellness motivation (opt-in) |
| **Wellness Guide** | Active listening, grounding techniques, stress support (opt-in) |

Agents communicate via a shared `Meta/agent-messages.md` message board inside your vault.

---

## Prerequisites

- [Claude Code](https://claude.ai/code) with Pro, Max, or Team subscription
- [Obsidian](https://obsidian.md) (free)
- `git` and `bash` available in your terminal

---

## Installation

### 1. Create or open your Obsidian vault

```bash
# Create a new vault directory (or use an existing one)
mkdir ~/my-vault
```

Open Obsidian → Create New Vault → point it at `~/my-vault`.

### 2. Clone the repo inside your vault

```bash
cd ~/my-vault
git clone https://github.com/gnekt/My-Brain-Is-Full-Crew.git
```

### 3. Run the installer

```bash
cd My-Brain-Is-Full-Crew
bash scripts/launchme.sh
```

The installer:
- Asks 2–3 questions (language preference, which agents to enable)
- Copies agents into `../.claude/agents/` (for Claude Code CLI)
- Copies skills into `../.claude/skills/` (for Claude Code Desktop / Cowork)
- Both formats installed automatically — no choice needed

### 4. Initialize your vault

Open Claude Code **inside your vault folder** (not inside the repo subfolder):

```bash
cd ~/my-vault
claude  # or open Claude Code Desktop pointed at this folder
```

Then say:

```
Initialize my vault
```

The Architect runs a friendly onboarding conversation covering:
1. Your name, language, role
2. Which agents to activate
3. Health agents setup (opt-in)
4. Gmail / Google Calendar integrations

---

## Vault Structure

The Crew creates a hybrid PARA + Zettelkasten layout:

```
your-vault/
├── 00-Inbox/          # Capture zone — everything lands here first
├── 01-Projects/       # Active projects with deadlines
├── 02-Areas/          # Ongoing responsibilities (including Health/)
├── 03-Resources/      # Reference material, guides
├── 04-Archive/        # Completed or historical content
├── 05-People/         # Personal CRM
├── 06-Meetings/       # Timestamped meeting notes
├── 07-Daily/          # Daily notes and journals
├── MOC/               # Maps of Content — thematic indexes
├── Templates/         # Obsidian note templates
├── Meta/
│   ├── agent-messages.md   # Shared agent message board
│   ├── user-profile.md     # Your onboarding profile
│   └── vault-health/       # Librarian reports
└── .claude/
    ├── agents/        # Claude Code CLI subagents
    └── skills/        # Claude Code Desktop skills
```

---

## Daily Usage — Natural Language Commands

The interface is conversation. No GUI, no drag-and-drop.

### Knowledge Management

```
# Capture a note
"Save this: meeting with Marco about Q3 budget, he wants the report by Friday"

# Triage inbox
"Triage my inbox"
"Empty my inbox"

# Search
"Find everything I wrote about transformer architectures"
"What do my notes say about the Pomodoro technique?"

# Connect ideas
"Find connections between my notes on sleep and cognitive performance"
"What links to my note on [[Deep Work]]?"

# Vault health
"Run a vault health check"
"Find duplicate notes"
"Fix broken links"
```

### Meetings & Transcription

```
# Process a recording
"Process my meeting recording from this morning"
"Transcribe this: [paste transcript text]"

# Meeting prep
"Prepare me for my 3pm meeting with the research team"
```

### Email & Calendar (Postman)

```
"Check my emails for deadlines this week"
"What meetings do I have tomorrow?"
"Summarize unread emails related to Project Phoenix"
```

### Food Coach (opt-in)

```
"Suggest a high-protein meal I can make in 20 minutes"
"Generate a grocery list for the week"
"I haven't been eating well — give me something easy and nutritious"
```

### Wellness Guide (opt-in)

```
"I'm feeling overwhelmed right now"
"Walk me through a grounding exercise"
"I need to talk through something stressful"
```

---

## Agent Communication Pattern

Agents leave messages for each other on the shared board at `Meta/agent-messages.md`:

```markdown
<!-- Example entries in Meta/agent-messages.md -->

## Pending Messages

### FROM: Transcriber → TO: Sorter
**Date**: 2026-03-21
**Subject**: New meeting note needs filing
**File**: 06-Meetings/2026-03-21-research-sync.md
**Action**: Route to 01-Projects/Thesis/ and extract tasks to inbox

---

### FROM: Food Coach → TO: Wellness Guide
**Date**: 2026-03-21
**Subject**: Stress-eating pattern detected
**Context**: User mentioned eating poorly due to deadline stress 3x this week
**Action**: Check in on stress levels next session
```

When an agent runs, it checks this board and acts on messages addressed to it.

---

## Configuration Files

### User Profile (generated by Architect during onboarding)

```markdown
<!-- Meta/user-profile.md -->
# User Profile

## Identity
- Name: Alex
- Language: English
- Role: PhD Researcher — Cognitive Science
- Timezone: Europe/Rome

## Active Agents
- [x] Architect
- [x] Scribe
- [x] Sorter
- [x] Seeker
- [x] Connector
- [x] Librarian
- [x] Transcriber
- [x] Postman
- [x] Food Coach (opt-in)
- [ ] Wellness Guide (opt-in — not activated)

## Food Coach Settings
- Dietary restrictions: vegetarian, lactose intolerant
- Health goals: increase protein, reduce processed food
- Cooking time preference: max 30 minutes

## Integrations
- Gmail: connected
- Google Calendar: connected
```

### Agent Directory Structure

```bash
.claude/
├── agents/
│   ├── architect.md
│   ├── scribe.md
│   ├── sorter.md
│   ├── seeker.md
│   ├── connector.md
│   ├── librarian.md
│   ├── transcriber.md
│   ├── postman.md
│   ├── food-coach.md
│   └── wellness-guide.md
└── skills/
    ├── architect.md
    ├── scribe.md
    └── ...
```

---

## Reinstalling or Updating

```bash
cd ~/my-vault/My-Brain-Is-Full-Crew

# Pull latest changes
git pull origin main

# Re-run installer (safe to run multiple times)
bash scripts/launchme.sh
```

The installer is idempotent — re-running updates agent files without wiping your vault content.

---

## Enabling / Disabling Opt-In Agents

To enable the Food Coach or Wellness Guide after onboarding:

```
"Enable the Food Coach agent"
"Activate the Wellness Guide"
"Disable the Food Coach"
```

The Architect will update `Meta/user-profile.md` and confirm.

To manually edit, open `Meta/user-profile.md` and change the checkbox:

```markdown
- [x] Food Coach (opt-in)    ← enabled
- [ ] Wellness Guide (opt-in) ← disabled
```

---

## Multilingual Support

The Crew responds in whatever language you use. Switch mid-conversation:

```
"Salva questo: riunione con Marco sul budget Q3"
"Cherche tout ce que j'ai écrit sur la mémoire de travail"
"作業記憶に関するメモを全部見せて"
```

Agents match your language automatically. No configuration needed.

---

## Troubleshooting

### Agents not activating

```bash
# Confirm you're running Claude Code from inside your vault (not the repo subfolder)
cd ~/my-vault
claude

# Confirm agents are installed
ls .claude/agents/
ls .claude/skills/
```

### Re-run onboarding

```
"Re-run vault initialization"
"Reset my user profile"
```

### Vault structure missing

```
"Rebuild vault folder structure"
"Create missing vault folders"
```

### Agent messages not being processed

Check `Meta/agent-messages.md` exists. If missing:

```
"Initialize the agent message board"
```

### Gmail / Calendar integration issues

The Postman agent uses Claude Code's built-in tool access. Ensure Claude Code has browser/OAuth permissions granted for your Google account during onboarding. Re-trigger with:

```
"Reconnect Gmail integration"
"Re-authenticate Google Calendar"
```

---

## Important Disclaimers

- **Health agents are not medical professionals.** Food Coach and Wellness Guide produce AI-generated output — not medical advice, not therapy. Always consult real professionals. Both are opt-in.
- **No warranty.** Back up your vault before use. Provided "as is."
- **Personal use only.** You are responsible for GDPR/CCPA compliance if processing third-party data (e.g., emails containing others' personal information).
- By using the software you agree to the [Terms of Use](https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/TERMS_OF_USE.md). The Architect will ask you to accept during onboarding.

---

## Key Files Reference

| File | Purpose |
|---|---|
| `scripts/launchme.sh` | Main installer — run this |
| `Meta/user-profile.md` | Your preferences and active agents |
| `Meta/agent-messages.md` | Inter-agent communication board |
| `Meta/vault-health/` | Librarian weekly reports |
| `.claude/agents/` | Subagent definitions (CLI) |
| `.claude/skills/` | Skill definitions (Desktop) |
| `docs/getting-started.md` | Beginner step-by-step guide |
| `docs/DISCLAIMERS.md` | Full disclaimer text |
