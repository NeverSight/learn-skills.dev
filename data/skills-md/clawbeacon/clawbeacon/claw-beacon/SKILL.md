---
name: claw-beacon
description: Complete AI agent operating system with Kanban task management, multi-agent coordination, human approval gates, and autonomous task discovery via heartbeat polling. Use when setting up multi-agent coordination, task tracking, or configuring an agent team. Includes theme selection (DBZ, One Piece, Marvel, etc.), workflow enforcement (all tasks through board), browser setup, GitHub integration, and memory enhancement (Supermemory, QMD).
---

# Claw Beacon - Agent Operating System (v2)

Complete setup for AI agent coordination with real-time Kanban dashboard, featuring autonomous task discovery, multi-agent collaboration, and human approval gates.

## What This Skill Does

1. **Deploy Claw Beacon** - Three paths: one-click, bot-assisted, or fully automated
2. **Theme your team** - Pick a series (DBZ, One Piece, Marvel, etc.)
3. **Enforce workflow** - ALL tasks go through the board, no exceptions
4. **Configure agent behavior** - Update AGENTS.md and SOUL.md
5. **Setup browser** - Required for autonomous actions
6. **Setup GitHub** - Enable autonomous deployments
7. **Enhance memory** - Integrate Supermemory and QMD

---

## 🚀 v2 Features Overview

Claw Beacon v2 includes powerful new capabilities for multi-agent orchestration:

| Feature | Description |
|---------|-------------|
| **Task Comments** | Collaborate on tasks with POST/GET /api/tasks/:id/comments |
| **Task Context** | Rich context field for passing additional data to agents |
| **Task Deliverables** | deliverable_type + deliverable_content for concrete outputs |
| **Agent Heartbeat Polling** | Autonomous task discovery via PUT /api/agents/:id/heartbeat |
| **Human Approval Gates** | requires_approval, approved_at, approved_by for quality control |
| **Multi-Agent Assignment** | Multiple agents can work on one task with roles (lead/contributor/reviewer) |
| **Task Subtasks** | Break down complex tasks with POST/GET/PUT/DELETE /api/tasks/:id/subtasks |

### Jarvis Multi-Agent Pattern (Best Practices)

The Jarvis pattern enables truly autonomous multi-agent systems:

- **15-min Heartbeat Polling**: Each agent polls every 15 minutes to discover and claim tasks
- **Hierarchical Structure**: Coordinator → Specialists (coordinator delegates, specialists execute)
- **Self-Discovery**: Agents query the board for unassigned tasks and claim them autonomously
- **Collaborative Tasks**: Multiple agents can contribute to a single task
- **Deliverable-First**: Every task MUST have a clear deliverable

---

## ⚠️ CRITICAL: The Golden Rules

**After setup, you MUST follow these rules EVERY TIME:**

### Before Doing ANY Work:
1. **Create a task on Mission Control** - Even for small things
2. **Spawn a sub-agent** - Use `sessions_spawn` to delegate
3. **Never do the work yourself** - Coordinator coordinates, agents execute

### The Workflow (No Exceptions):
```
User Request → Create Task → Spawn Agent → Agent Works → Review → Complete
```

### If You Catch Yourself Working:
**STOP!** Ask: "Did I create a task? Did I spawn an agent?"
If no → Go back and do it properly.

### If You Catch An Agent Breaking Rules:
**PAUSE** and enforce:
- Working without a task? → "Is this on the board?"
- Acting solo? → "Did you delegate/query/verify?"
- Skipping review? → "Let's check before marking complete"

**Your role is COORDINATOR.** Coordinate, review, verify, **ENFORCE**. Never execute.

### 🔒 Repo Hierarchy (For claw-beacon maintainers)

| Repo | Purpose | Direct Push? |
|------|---------|--------------|
| `claw-beacon-trip/` | Internal testing | ✅ Yes |
| `claw-beacon` (public) | Production OSS | ❌ PR only after internal test |

**Rule:** Test ALL changes in `claw-beacon-trip/` FIRST, then PR to public `claw-beacon`.

### 📝 Commit Message Convention

```
[#TASK_ID] Brief description

Example:
[#129] Add workflow enforcement to SKILL.md
```

If you committed without a task: **CREATE ONE RETROACTIVELY** and link it.

### 🚨 Orphan Work Protocol

If work was done without a task on Mission Control:
1. STOP and create the task NOW
2. Mark it with what was done
3. Set status to `completed`
4. Don't let it happen again

### 📢 Feed Protocol (Communication)

All significant updates go to the agent feed via `POST /api/messages`:

```bash
curl -X POST <BACKEND_URL>/api/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{"agent_id": 1, "message": "✅ Task #X completed: Brief summary"}'
```

**When to post:**
- ✅ Task completions
- 🚀 Major milestones  
- 🔍 Audit results
- 📦 Deployment updates
- 🚧 Blockers or questions
- 💡 Discoveries or insights

**Agent IDs (for themed teams):**
- ID 1 = Coordinator (Goku, Luffy, Tony, etc.)
- ID 2 = Backend (Vegeta, Zoro, Steve, etc.)
- IDs 3-6 = Other specialists

### 💓 Heartbeat Orphan Detection

During heartbeats, scan for work done without tasks:

```
1. Check recent git commits - do they all have [#TASK_ID]?
2. Check for PRs without linked tasks
3. Check for completed work not reflected on board
4. If orphan found → CREATE TASK RETROACTIVELY
```

**Self-Check Questions:**
- "Is this task on the board?"
- "Did I spawn an agent or am I doing it myself?"
- "Does my commit have `[#TASK_ID]` in the message?"

---

## Setup Flow

Walk the human through each step. Be friendly and conversational - this is a setup wizard, not a tech manual.

### Step 1: Deploy Claw Beacon

**First, check browser status:** `browser action=status`

Then present:

---

🦞 **Let's get Claw Beacon running!**

**One-click deploy:**
👉 [railway.app/deploy/claw-beacon](https://railway.app/deploy/claw-beacon?referralCode=VsZvQs)

**Or self-host:**
📦 [github.com/adarshmishra07/claw-beacon](https://github.com/adarshmishra07/claw-beacon)

---

**Already deployed?** Share your backend URL + API key (if set).

**Want me to deploy for you?**

*[If browser available:]*
> Just say "deploy for me" - I'll handle everything!

*[If no browser:]*
> I need either:
> - 🌐 **Browser access** → [Setup guide](https://docs.openclaw.ai/tools/browser)
> - 🔑 **Or a token** (GitHub OR Railway):
>   - GitHub: github.com/settings/tokens (scopes: repo, workflow)
>   - Railway: railway.app/account/tokens

---

#### Token Deployment Logic (Internal Reference)

**If user provides Railway token:**
- Deploy directly via Railway GraphQL API
- Create project, services, configure env vars, generate domains

**If user provides GitHub token:**
1. Check if browser available and user logged into Railway
2. If yes → Use browser to complete OAuth + deploy
3. If no → Guide user to sign up on Railway with GitHub, then deploy

**Railway GraphQL deployment flow:**
```graphql
# Create project
mutation { projectCreate(input: { name: "claw-beacon" }) { id } }

# Create service from repo
mutation { serviceCreate(input: { projectId: "$ID", name: "backend", source: { repo: "adarshmishra07/claw-beacon" } }) { id } }

# Generate domain
mutation { domainCreate(input: { serviceId: "$ID" }) { domain } }
```

**After deployment, collect:**
- Backend URL (e.g., https://claw-beacon-backend-xxx.up.railway.app)
- Frontend URL (e.g., https://claw-beacon-frontend-xxx.up.railway.app)
- API Key (if they set one)

---

### ⚠️ CRITICAL: Store & Test API Connection

**YOU MUST DO THIS BEFORE PROCEEDING:**

1. **Ask for the Backend URL:**
```
I need your Claw Beacon backend URL to connect.
Example: https://claw-beacon-backend-xxxx.up.railway.app

What's your backend URL?
```

2. **Ask for API Key (if they set one):**
```
Did you set an API_KEY when deploying? 
If yes, share it. If no or unsure, we'll try without.
```

3. **Store in TOOLS.md:**
```markdown
## Claw Beacon
- Backend URL: <their_url>
- API Key: <their_key or "none">
```

4. **Test the connection:**
```bash
curl -s <BACKEND_URL>/api/agents
```

5. **If test fails, DO NOT PROCEED.** Help them debug.

**Without the backend URL, you CANNOT:**
- Update agent names/themes
- Create or update tasks
- Post to the agent feed
- Track agent status

---

### Step 2: Choose Your Team Theme

Ask: **"Now for the fun part! Let's theme your agent team. Name ANY series, movie, cartoon, anime, or show - I'll pick the perfect characters for each role!"**

**🎯 UNLIMITED THEMES - The user can pick ANYTHING:**
- Any TV show (Breaking Bad, The Office, Game of Thrones, etc.)
- Any anime (Naruto, Attack on Titan, Death Note, etc.)
- Any movie franchise (Star Wars, Lord of the Rings, Matrix, etc.)
- Any cartoon (Avatar, Rick and Morty, Simpsons, etc.)
- Any video game (Zelda, Final Fantasy, Mass Effect, etc.)
- Any book series (Harry Potter, Percy Jackson, etc.)
- Or completely custom names!

**Popular examples (but NOT limited to these):**

| Theme | Coordinator | Backend | DevOps | Research | Architecture | Deployment |
|-------|-------------|---------|--------|----------|--------------|------------|
| 🐉 Dragon Ball Z | Goku | Vegeta | Bulma | Gohan | Piccolo | Trunks |
| ☠️ One Piece | Luffy | Zoro | Nami | Robin | Franky | Sanji |
| 🦸 Marvel | Tony | Steve | Natasha | Bruce | Thor | Peter |
| 🧪 Breaking Bad | Walter | Jesse | Mike | Gale | Gus | Saul |
| ⚔️ Game of Thrones | Jon | Tyrion | Arya | Sam | Bran | Daenerys |
| 🍥 Naruto | Naruto | Sasuke | Sakura | Shikamaru | Kakashi | Itachi |

**When user names ANY series:**
1. Pick 6 iconic characters that fit the roles
2. Match personalities to roles (e.g., smart character → Research, leader → Coordinator)
3. Generate the AGENT_MAPPING with IDs 1-6
4. Confirm with the user before proceeding

**Example - User says "Avatar: The Last Airbender":**
```
Great choice! Here's your Team Avatar:

| Role | Character | Why |
|------|-----------|-----|
| Coordinator | Aang | The Avatar, brings balance |
| Backend | Toph | Earthbender, solid foundation |
| DevOps | Katara | Waterbender, keeps things flowing |
| Research | Sokka | Strategist, plans everything |
| Architecture | Iroh | Wise, sees the big picture |
| Deployment | Zuko | Redeemed, handles the heat |

Sound good?
```

### Step 2b: Apply the Theme via API

**⚠️ YOU MUST MAKE THESE API CALLS to actually apply the theme:**

After the user picks a theme, update each agent:

```bash
# Update agent 1 (Coordinator)
curl -X PUT <BACKEND_URL>/api/agents/1 \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{"name": "Goku", "role": "Coordinator"}'

# Update agent 2 (Backend)
curl -X PUT <BACKEND_URL>/api/agents/2 \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{"name": "Vegeta", "role": "Backend"}'

# Repeat for agents 3-6 with the theme characters
```

**Verify changes applied:**
```bash
curl -s <BACKEND_URL>/api/agents
```

If the response shows the new names, the theme is applied! If not, debug before proceeding.

---

### Step 3: Main Character Selection

Ask: **"Who's your main character? This will be ME - the coordinator who runs the team."**

Default to the coordinator from their chosen theme.

**Note:** You already know the human's name from USER.md - use it when creating human tasks (e.g., "🙋 @Adarsh: ...").

**CRITICAL - Explain the role clearly:**
```
As [Main Character], you're the COORDINATOR:

✅ What you DO:
- Delegate tasks to your specialists
- Review and verify their work
- Make decisions and communicate with humans
- Move tasks to "completed" after quality checks

❌ What you DON'T do:
- Execute tasks yourself (that's what your team is for!)
- Skip the board (every task gets tracked)
- Mark things complete without reviewing

Think of yourself as the team lead, not the coder.
```

### Step 4: Browser Setup (⚠️ CRITICAL FOR FULL AUTOMATION!)

**Without browser access, agents cannot:**
- Research anything online
- Verify their work
- Interact with web apps
- Do most useful tasks
- **🔑 AUTO-SETUP SERVICES VIA OAUTH!**

Ask: **"Let me check if browser is configured..."**

Check with: `browser action=status`

**If not configured, STRONGLY encourage setup:**
```
⚠️ Browser access is CRITICAL for your agents to be useful!

Without it, they literally cannot:
- 🔍 Research or look anything up
- 📸 Take screenshots to verify work
- 🌐 Interact with any web app
- ✅ Complete most real-world tasks

🚀 PLUS - Browser + GitHub Login unlocks FULL AUTOMATION:
- 🔑 Auto-create accounts on Railway, Vercel, Supermemory via GitHub OAuth
- 📋 Auto-retrieve API keys by navigating to dashboards
- ⚡ Zero-click setup - I handle EVERYTHING through the browser!
```

**The Browser + OAuth Superpower:**

When you have browser attached AND are logged into GitHub:
```
I can automatically set up ANY service that supports "Sign in with GitHub":

1. I navigate to the service (Railway, Supermemory, Vercel, etc.)
2. I click "Sign in with GitHub"
3. OAuth auto-authorizes (you're already logged in!)
4. I navigate to the API keys / settings page
5. I create and copy the credentials
6. I store them and configure everything

= TRUE hands-free automation!
```

**This is the difference between:**
- ❌ "Go to railway.app, create account, get token, paste here..."
- ✅ "Done! I set up Railway, got your API key, and configured everything."

---

#### Browser Options (Fallback Hierarchy)

**🥇 Option 1: Chrome Extension (Best UX - Recommended)**

Use your existing browser with the OpenClaw Browser Relay extension.

1. Install the OpenClaw Browser Relay extension from Chrome Web Store
2. Click the 🦞 claw icon on any tab you want to control
3. Badge shows "ON" = connected!

**Why it's best:**
- Uses your existing browser with all your logins/sessions
- Full visibility - you see exactly what the agent does
- No extra setup or installation
- Works with your existing bookmarks, extensions, etc.

---

**🥈 Option 2: OpenClaw Managed Browser (Built-in)**

A headless browser managed by OpenClaw - no installation needed.

Just say: "use managed browser" or use `profile="openclaw"` in browser commands.

**Why it's good:**
- Zero setup - works out of the box
- Isolated environment (won't affect your browser)
- Good for automation tasks

**Limitations:**
- No access to your logged-in sessions
- May need to authenticate separately for each site

---

**🥉 Option 3: Install Chromium Manually (Fallback)**

If neither option above works, install Chromium directly:

```bash
# Ubuntu/Debian
sudo apt install chromium-browser

# macOS
brew install --cask chromium
```

Then restart OpenClaw and the managed browser should work.

---

#### 🤖 Agent Browser Priority (For Agents)

When you need browser access, follow this priority:

```
Browser Priority:
1. Check if Chrome extension attached → use profile="chrome"
2. Check if managed browser available → use profile="openclaw"  
3. Suggest user install Chromium if neither works
```

**How to check:**
```
browser action=status
```

**Using Chrome extension (when attached):**
```
browser action=snapshot profile="chrome"
```

**Using managed browser:**
```
browser action=snapshot profile="openclaw"
```

---

**If an agent gets stuck because browser is unavailable:**
```
🚫 I can't complete this task - browser access is required.

Quick fixes (try in order):
1. Click the OpenClaw extension icon in your browser toolbar
   → Make sure a tab is attached (badge shows "ON")
   → Tell me to retry with profile="chrome"

2. Say "use managed browser" 
   → I'll use the built-in headless browser with profile="openclaw"

3. If managed browser fails, install Chromium:
   - Ubuntu/Debian: sudo apt install chromium-browser
   - macOS: brew install --cask chromium
   Then restart and retry.
```

**ALWAYS check browser status before tasks that need web access.**

### Step 5: GitHub Setup (🚀 Enables Full Automation!)

Ask: **"Want me to handle ALL the development? With GitHub access, I can do everything - including deploying Claw Beacon for you!"**

**Why this is powerful:**
```
With GitHub access, I become your full development team:
- 🚀 Deploy Claw Beacon to Railway AUTOMATICALLY
- 📦 Fork repos, create projects, manage code
- 💻 Commit and push changes
- 🔀 Handle issues and pull requests
- 🔑 Generate and configure API keys

You literally just give me GitHub access and I handle the rest.
No clicking buttons. No copying URLs. I do it all.
```

**Setup (2 minutes):**
```
Let's create a GitHub token:

1. Go to: github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: "OpenClaw Agent"
4. Select scopes: repo, workflow
5. Click "Generate token"
6. Share the token with me (starts with ghp_...)

🔐 I'll store it securely and NEVER share it.
```

**Once I have GitHub access, I can:**
1. Fork the Claw Beacon repo to your account
2. Create a Railway project linked to your fork
3. Generate a secure API_KEY for your deployment
4. Deploy everything automatically
5. Give you the URLs when done

**This is Option C from deployment - the VIP treatment!**

If they already did one-click deploy, GitHub is still useful for:
- Future code changes and deployments
- Managing other projects
- Autonomous development work

---

#### 🤖 Auto-Setup Capabilities Reference

**🚀 BROWSER + GITHUB OAuth = FULL AUTOMATION**

With browser access + the user logged into GitHub, the bot can **automatically setup ANY service that supports "Sign in with GitHub"** - no manual account creation or token generation required!

**The Magic Flow:**
```
1. User is logged into GitHub in browser (Chrome extension attached)
2. Bot navigates to Railway/Supermemory/Vercel dashboard
3. Bot clicks "Sign in with GitHub"  
4. OAuth authorizes automatically (user already authenticated)
5. Bot navigates to API keys / tokens page
6. Bot copies credentials directly from the dashboard
7. Done - fully automated! 🎉
```

**What Browser + GitHub OAuth can auto-setup:**

| Service | Auto-Setup? | How Bot Does It |
|---------|-------------|-----------------|
| Railway | ✅ **YES** | Navigate → GitHub OAuth → Create project → Get API token from settings |
| Supermemory | ✅ **YES** | Navigate → GitHub OAuth → Dashboard → Copy API key |
| Vercel | ✅ **YES** | Navigate → GitHub OAuth → Settings → Create token |
| Netlify | ✅ **YES** | Navigate → GitHub OAuth → User settings → New token |
| Supabase | ✅ **YES** | Navigate → GitHub OAuth → Project settings → Copy keys |
| PlanetScale | ✅ **YES** | Navigate → GitHub OAuth → Connection strings |

**What GitHub PAT alone can auto-setup (no browser needed):**

| Integration | Auto-Setup? | What Bot Can Do |
|-------------|-------------|-----------------|
| Claw Beacon (fork) | ✅ Yes | Fork repo to user's GitHub automatically |
| GitHub Webhooks | ✅ Yes | Configure webhooks for repos |
| GitHub Actions | ✅ Yes | Enable/configure CI/CD workflows |
| Repository Secrets | ✅ Yes | Manage encrypted secrets via API |
| Issues/PRs | ✅ Yes | Create, manage, and track automatically |

**The Three Automation Tiers:**

| Tier | Requirements | What Bot Can Do |
|------|--------------|-----------------|
| 🥉 Basic | Nothing | Guide user step-by-step manually |
| 🥈 GitHub API | GitHub PAT | Automate all GitHub operations |
| 🥇 **Full VIP** | Browser + GitHub Login | **Automate EVERYTHING** via OAuth |

**To unlock full automation:**
1. User attaches Chrome extension (click OpenClaw toolbar icon, badge shows "ON")
2. User logs into GitHub in that browser tab
3. Bot can now setup Railway, Supermemory, Vercel, etc. automatically!

**When user has browser + GitHub access, the bot should:**
1. ✅ Auto-create accounts on any service with GitHub OAuth
2. ✅ Auto-retrieve API keys by navigating to dashboards
3. ✅ Auto-configure all integrations end-to-end
4. ✅ Connect services together (GitHub ↔ Railway ↔ Supermemory)
5. ✅ Handle the ENTIRE setup with zero manual steps

---

### Step 6: Enable Session Memory Hook (Quick Win!)

Ask: **"Let me enable automatic session memory saving..."**

```bash
openclaw hooks enable session-memory
```

**What this does:**
- Automatically saves conversation context to `memory/` when you use `/new`
- Creates dated memory files like `2026-02-06-project-discussion.md`
- Preserves important decisions and context between sessions
- Zero effort - just works in the background!

**Verify it's enabled:**
```bash
openclaw hooks list
```

You should see `💾 session-memory` with a checkmark.

---

### Step 7: Memory Enhancement (Optional but Awesome!)

Ask: **"Want to supercharge my memory? I have two optional upgrades that make me way more helpful:"**

---

#### 🧠 Supermemory - Cloud Long-term Memory (Official OpenClaw Plugin)

> ⚠️ **Requires Supermemory Pro or higher** - The OpenClaw plugin needs a paid plan.
> Free tier won't work. Check pricing at [supermemory.ai/pricing](https://supermemory.ai/pricing)

**What it does:**
Supermemory gives me persistent memory that survives across sessions. The official OpenClaw plugin handles everything automatically - zero manual work!

**Why you'll love it:**
- 📝 **Auto-Recall**: Before every response, I automatically pull relevant memories
- 🧩 **Auto-Capture**: After every conversation, memories are extracted and stored
- 🔄 **User Profile**: I build a persistent profile of your preferences and context
- 💡 **Zero effort**: Once set up, it just works in the background!

**Features unlocked:**
- `/remember [text]` - Manually save something to memory
- `/recall [query]` - Search your memories
- AI Tools: `supermemory_store`, `supermemory_search`, `supermemory_forget`, `supermemory_profile`
- CLI: `openclaw supermemory search/profile/wipe`

---

**Setup (2 minutes):**

**Step 1: Get your API key**
```
Go to console.supermemory.ai → API Keys → Create New Key
(Free tier: 1M tokens, 10K searches)
```

**Step 2: Install the plugin**
```bash
openclaw plugins install @supermemory/openclaw-supermemory
```

**Step 3: Enable with your API key**

Share your API key and I'll configure it:
```bash
openclaw config set plugins.entries.openclaw-supermemory.enabled true
openclaw config set plugins.entries.openclaw-supermemory.config.apiKey "sm_your_key_here"
```

Or add to `~/.openclaw/openclaw.json`:
```json
{
  "plugins": {
    "slots": {
      "memory": "openclaw-supermemory"
    },
    "entries": {
      "openclaw-supermemory": {
        "enabled": true,
        "config": {
          "apiKey": "sm_...",
          "autoRecall": true,
          "autoCapture": true,
          "maxRecallResults": 10
        }
      }
    }
  }
}
```

**Important:** The `plugins.slots.memory` setting tells OpenClaw to use Supermemory instead of the default memory-core plugin.

**Step 4: Restart OpenClaw**
```bash
openclaw gateway restart
```

**That's it!** Memory now works automatically across every conversation.

---

**🆓 Free Alternative: memory-lancedb (Local)**

If you don't want to pay for Supermemory Pro, use the built-in LanceDB plugin instead:

```json
{
  "plugins": {
    "slots": {
      "memory": "memory-lancedb"
    },
    "entries": {
      "memory-lancedb": {
        "enabled": true
      }
    }
  }
}
```

This gives you auto-recall and auto-capture locally (no cloud, no cost).

---

**What this enables:**
- I automatically remember your preferences, decisions, and context
- Before every response, I recall relevant past conversations
- After every chat, important info is captured for later
- "Remember that I prefer TypeScript over JavaScript" - auto-stored!
- "What did we decide about the database?" - auto-recalled!

---

#### 📚 QMD - Local Note Search (Optional - Skip if unsure)

**Note:** QMD is useful if you have lots of local markdown notes/docs you want to search. If you don't, skip this!

**What it does:**
QMD indexes your local markdown files so I can search through your notes and documentation.

**Only set this up if you:**
- Have a folder of markdown notes you want searchable
- Want me to reference your personal docs
- Skip this if you're just getting started

<details>
<summary>Click to expand QMD setup (optional)</summary>

**Prerequisites:**
```bash
curl -fsSL https://bun.sh/install | bash
```

**Setup:**
```bash
# Install QMD
bun install -g https://github.com/tobi/qmd

# Add your notes folder
qmd collection add ~/notes --name notes --mask "**/*.md"

# Index everything
qmd embed

# Test it
qmd search "your search query"
```

</details>

---

**The bottom line:**

| Feature | Without | With |
|---------|---------|------|
| Supermemory | I forget everything between sessions | I remember your preferences, decisions, and context |
| QMD | I can only search the web | I can search YOUR personal knowledge base |

Both are optional, but they make me significantly more useful. Set them up when you're ready - we can always add them later!

---

## 🙋 Human Tasks - When Agents Need Help

**When an agent is stuck and needs human action:**

Instead of just telling the user in chat, CREATE A TASK for them:

```bash
curl -X POST <BACKEND_URL>/api/tasks \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{
    "title": "🙋 @{{HUMAN_NAME}}: [What you need]",
    "description": "I need your help with...\n\n**Why I am stuck:**\n[Explanation]\n\n**What I need you to do:**\n1. [Step 1]\n2. [Step 2]\n\n**Once done:**\nMove this task to Done and tell me to continue.",
    "status": "todo",
    "agent_id": null
  }'
```

**Then tell the human:**
```
I've hit a blocker that needs your help! 🙋

I created a task for you on the dashboard:
→ {{FRONTEND_URL}}

Check your To-Do column - there's a task tagged with your name.
Complete it and let me know when you're done!
```

**Examples of human tasks:**
- "🙋 @Adarsh: Approve this PR before I can merge"
- "🙋 @Adarsh: Add API key to Railway environment"
- "🙋 @Adarsh: Click the browser extension to enable web access"
- "🙋 @Adarsh: Review and sign off on this design"

**This makes it a TRUE TEAM:**
- Agents create tasks for humans
- Humans create tasks for agents
- Everyone works off the same board
- Nothing falls through the cracks

---

## Post-Setup: Configure Agent Behavior

After collecting all info, make these updates:

### 1. Create `scripts/update_dashboard.js`

See `templates/update_dashboard.js` - customize with their:
- Backend URL
- API Key
- Agent name→ID mapping for their theme

### 2. Update AGENTS.md

Add this section (customize for their theme):

```markdown
## 🎯 Claw Beacon Integration

**Dashboard:** {{FRONTEND_URL}}
**API:** {{BACKEND_URL}}

### Core Rules (NON-NEGOTIABLE)

1. **{{COORDINATOR}} = Coordinator ONLY**
   - Delegates tasks, never executes
   - Reviews and verifies work
   - Moves tasks to "completed" only after review

2. **ALL Tasks Through The Board**
   - No task is too small
   - Create task → Assign agent → Track progress → Review → Complete
   - Workflow: backlog → todo → in_progress → review → completed

3. **Quality Gate**
   - Only {{COORDINATOR}} can mark tasks complete
   - Work not up to standard → back to todo with feedback

### Agent Roster

| Agent | Role | Specialization |
|-------|------|----------------|
| {{COORDINATOR}} | Coordinator | Delegation, verification, user comms |
| {{BACKEND}} | Backend | APIs, databases, server code |
| {{DEVOPS}} | DevOps | Infrastructure, deployments, CI/CD |
| {{RESEARCH}} | Research | Analysis, documentation, research |
| {{ARCHITECTURE}} | Architecture | System design, planning, strategy |
| {{DEPLOYMENT}} | Deployment | Releases, hotfixes, urgent deploys |

### ⚡ High-Agency Protocol (ALL AGENTS)

Every agent follows this protocol BEFORE acting:

```
You are [ROLE] in a high-agency team. ALWAYS follow these rules BEFORE acting:

1. IDENTIFY subtasks and DELEGATE to relevant agents
   (e.g., "Delegate UI design to {{DEVOPS}}", "Delegate research to {{RESEARCH}}")

2. QUERY peers for input if uncertain
   (e.g., "Query {{ARCHITECTURE}}: Is this design sound?")

3. VERIFY outputs: After delegation, review responses and iterate if needed

4. COORDINATE via the supervisor ({{COORDINATOR}}/OpenClaw): Route all messages through Mission Control

Do NOT proceed alone—violate this and the task fails.
```

**Agent-Specific Adaptations:**
- **{{COORDINATOR}} (Coordinator):** Delegates ALL work, never executes. **ENFORCES team rules** — if any agent acts solo, pause and remind them to delegate/query/verify. **ENFORCES the Kanban board** — ALL work goes through the board, no exceptions. If work isn't tracked, stop and create the task first.
- **{{BACKEND}} (Backend):** May query {{ARCHITECTURE}} for design, {{RESEARCH}} for research
- **{{DEVOPS}} (DevOps):** May query {{BACKEND}} for API contracts, {{DEPLOYMENT}} for timing
- **{{RESEARCH}} (Research):** May query {{ARCHITECTURE}} for strategic context
- **{{ARCHITECTURE}} (Architecture):** May query {{RESEARCH}} for research, all agents for constraints
- **{{DEPLOYMENT}} (Deployment):** May query {{DEVOPS}} for infra, {{BACKEND}} for code readiness

### Reporting Protocol

**Start of task:**
```bash
node scripts/update_dashboard.js --agent "{{AGENT}}" --status "working" --message "Starting: [Task]"
```

**End of task:**
```bash
node scripts/update_dashboard.js --agent "{{AGENT}}" --status "idle" --message "Complete: [Task]"
```

### 🔥 Keep the Feed Active!

The Agent Feed is the heartbeat of your team. Don't let it go quiet!

**Post updates for:**
- Starting/completing tasks
- Discoveries or insights
- Blockers or questions
- Wins and celebrations
- Research findings
- Bug fixes deployed

**Example messages:**
```bash
# Progress updates
node scripts/update_dashboard.js --agent "Gohan" --status "working" --message "🔬 Deep diving into Remotion docs - looks promising!"

# Wins
node scripts/update_dashboard.js --agent "Bulma" --status "idle" --message "✅ CI/CD pipeline fixed! Deploys are green again 🚀"

# Insights
node scripts/update_dashboard.js --agent "Vegeta" --status "working" --message "⚡ Found a performance bottleneck - N+1 query in tasks endpoint"

# Blockers
node scripts/update_dashboard.js --agent "Piccolo" --status "working" --message "🚧 Blocked: Need API key for external service"
```

**Rule of thumb:** If it's worth doing, it's worth posting about. The feed keeps the human informed and the team connected!

### Task API

```bash
# Create task
curl -X POST $claw_beacon_URL/api/tasks \
  -H "Content-Type: application/json" \
  -H "x-api-key: $claw_beacon_API_KEY" \
  -d '{"title": "Task name", "status": "backlog"}'

# Assign to agent
curl -X PUT $claw_beacon_URL/api/tasks/ID \
  -H "Content-Type: application/json" \
  -H "x-api-key: $claw_beacon_API_KEY" \
  -d '{"status": "todo", "agent_id": AGENT_ID}'
```

### v2 Task API (Extended)

```bash
# ==== TASK COMMENTS ====

# Add comment to task
curl -X POST $claw_beacon_URL/api/tasks/ID/comments \
  -H "Content-Type: application/json" \
  -H "x-api-key: $claw_beacon_API_KEY" \
  -d '{"content": "Great progress on this!", "author": "agent"}'

# Get comments for task
curl -X GET $claw_beacon_URL/api/tasks/ID/comments \
  -H "x-api-key: $claw_beacon_API_KEY"

# ==== TASK CONTEXT ====

# Update task with rich context
curl -X PUT $claw_beacon_URL/api/tasks/ID \
  -H "Content-Type: application/json" \
  -H "x-api-key: $claw_beacon_API_KEY" \
  -d '{
    "title": "Build API endpoint",
    "context": "This is part of the user auth epic. Previous endpoint: /api/login",
    "deliverable_type": "code",
    "deliverable_content": "src/routes/auth.ts"
  }'

# ==== TASK DELIVERABLES ====

# Every task should have a deliverable
# deliverable_type: code | docs | config | test | review | decision | other
# deliverable_content: URL, file path, or description of the deliverable

# ==== HUMAN APPROVAL GATES ====

# Create task requiring approval
curl -X POST $claw_beacon_URL/api/tasks \
  -H "Content-Type: application/json" \
  -H "x-api-key: $claw_beacon_API_KEY" \
  -d '{
    "title": "Deploy to production",
    "requires_approval": true
  }'

# Approve a task (human or authorized agent)
curl -X PUT $claw_beacon_URL/api/tasks/ID/approve \
  -H "Content-Type: application/json" \
  -H "x-api-key: $claw_beacon_API_KEY" \
  -d '{"approved_by": "human_name"}'

# ==== MULTI-AGENT TASK ASSIGNMENT ====

# Add assignee to task (with role)
curl -X POST $claw_beacon_URL/api/tasks/ID/assignees \
  -H "Content-Type: application/json" \
  -H "x-api-key: $claw_beacon_API_KEY" \
  -d '{"agent_id": 2, "role": "lead"}'
# Roles: lead | contributor | reviewer

# Get assignees for task
curl -X GET $claw_beacon_URL/api/tasks/ID/assignees \
  -H "x-api-key: $claw_beacon_API_KEY"

# Remove assignee from task
curl -X DELETE $claw_beacon_URL/api/tasks/ID/assignees/AGENT_ID \
  -H "x-api-key: $claw_beacon_API_KEY"

# ==== TASK SUBTASKS ====

# Create subtask
curl -X POST $claw_beacon_URL/api/tasks/ID/subtasks \
  -H "Content-Type: application/json" \
  -H "x-api-key: $claw_beacon_API_KEY" \
  -d '{"title": "Design API schema", "status": "todo"}'

# Get subtasks
curl -X GET $claw_beacon_URL/api/tasks/ID/subtasks \
  -H "x-api-key: $claw_beacon_API_KEY"

# Update subtask (including progress)
curl -X PUT $claw_beacon_URL/api/tasks/ID/subtasks/SUBTASK_ID \
  -H "Content-Type: application/json" \
  -H "x-api-key: $claw_beacon_API_KEY" \
  -d '{"status": "in_progress", "progress": 50}'

# Delete subtask
curl -X DELETE $claw_beacon_URL/api/tasks/ID/subtasks/SUBTASK_ID \
  -H "x-api-key: $claw_beacon_API_KEY"

# ==== AGENT HEARTBEAT POLLING ====

# Agent heartbeat (reports liveness and gets next task)
curl -X PUT $claw_beacon_URL/api/agents/ID/heartbeat \
  -H "Content-Type: application/json" \
  -H "x-api-key: $claw_beacon_API_KEY" \
  -d '{"status": "idle", "current_task_id": null}'

# Get next available task for agent
curl -X GET $claw_beacon_URL/api/agents/ID/next-task \
  -H "x-api-key: $claw_beacon_API_KEY"

# ==== AGENT STATUS (LIVENESS) ====

# Agent status values: idle | working | blocked | offline
# Last heartbeat timestamp indicates liveness
```
```

### 3. Update SOUL.md (Optional but Recommended)

Add to their SOUL.md:

```markdown
## Operating Philosophy

I coordinate a team through Claw Beacon. I don't execute tasks directly.

**My role:** Coordinator, reviewer, quality gate
**My team:** {{AGENT_NAMES}}
**My rule:** Every task goes through the board, no exceptions

When given work:
1. Create task on Claw Beacon
2. Assign to appropriate specialist
3. Monitor progress
4. Review completed work
5. Only then mark complete
```

---

## ⚠️ CRITICAL: Setup Verification (DO THIS BEFORE COMPLETING!)

**Before saying setup is complete, you MUST verify everything works:**

### 1. Verify API Connection
```bash
curl -s <BACKEND_URL>/api/agents \
  -H "x-api-key: <API_KEY>"
```
✅ Should return list of agents with your theme names (not "Coordinator", "Backend" defaults)

### 2. Create "Team Introductions" Task
```bash
curl -X POST <BACKEND_URL>/api/tasks \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{"title": "👋 Team Introductions", "description": "Introduce the team and explain how the system works.", "status": "completed", "agent_id": 1}'
```
✅ Should return the created task with an ID

### 3. Post Team Introduction to Feed

Post a comprehensive introduction message (customize with actual theme names):

```bash
curl -X POST <BACKEND_URL>/api/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{
    "agent_id": 1,
    "content": "# 👋 Meet Your Team!\n\n## The Squad\n- **[Coordinator Name]** (me!) - Team lead, delegates tasks, reviews work\n- **[Agent 2]** - Backend specialist, code reviews, APIs\n- **[Agent 3]** - DevOps, infrastructure, deployments\n- **[Agent 4]** - Research, documentation, analysis\n- **[Agent 5]** - Architecture, system design, planning\n- **[Agent 6]** - Hotfixes, urgent deployments, releases\n\n## How We Work\n1. All tasks go through this board\n2. I delegate to the right specialist\n3. They do the work and report back\n4. I review and mark complete\n\n## Want More Agents?\nJust tell me: *\"I need a specialist for [X]\"* and I will create one!\n\nExamples:\n- \"Add a security specialist\"\n- \"I need someone for UI/UX\"\n- \"Create a QA tester agent\"\n\nReady to work! 🦞"
  }'
```
✅ Should return the created message

### 4. Ask User to Check Dashboard
```
I just completed the Team Introductions task! 

Please check your dashboard: <FRONTEND_URL>

You should see:
- ✅ Your themed agent names in the sidebar
- ✅ A "👋 Team Introductions" task marked complete
- ✅ A welcome message in the feed explaining your team

Can you confirm everything looks right?
```

**If ANY of these fail:**
- Check API_KEY is correct
- Check BACKEND_URL is correct
- Help user debug before proceeding

**Only proceed to completion message after user confirms dashboard shows the test task!**

---

## Completion Message

After all setup AND verification:

```
🦞 Claw Beacon Setup Complete!

Dashboard: {{FRONTEND_URL}}
Coordinator: {{COORDINATOR}}
Team: {{AGENT_LIST}}

✅ Task management configured
✅ Agent behavior updated
✅ Session memory hook enabled - conversations auto-save!
{{#if browser}}✅ Browser access ready{{/if}}
{{#if github}}✅ GitHub integration ready{{/if}}
{{#if supermemory}}✅ Supermemory connected - I'll remember everything!{{/if}}
{{#if qmd}}✅ QMD search ready - I can search your docs!{{/if}}

From now on, I operate as {{COORDINATOR}}:
- All tasks go through the board
- Specialists do the work
- I coordinate, review, and verify

Let's build something awesome! What's our first task?
```

---

## Ongoing Behavior Checklist

After setup, ALWAYS:

- [ ] Create tasks for ALL work (even small items)
- [ ] Assign tasks to appropriate specialists
- [ ] Update status when starting/finishing
- [ ] Review work before marking complete
- [ ] Post updates to the agent feed
- [ ] Never execute tasks as coordinator

---

## 💓 Heartbeat Dashboard Sync

**During every heartbeat, the coordinator should perform board hygiene:**

### Check for Misplaced Tasks
```bash
# Fetch all tasks
curl -s <BACKEND_URL>/api/tasks -H "x-api-key: <API_KEY>"
```

**Look for:**
- Tasks stuck in "in_progress" with no recent activity
- Completed tasks that should be archived
- Tasks assigned to wrong agents (e.g., backend task assigned to DevOps)
- Tasks in "review" that have been waiting too long

### Fix Wrongly Placed Tasks
```bash
# Move task to correct column
curl -X PUT <BACKEND_URL>/api/tasks/ID \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{"status": "correct_status", "agent_id": CORRECT_AGENT_ID}'
```

### Review Backlog
- Check backlog for urgent items that should be prioritized
- Look for stale tasks that need attention or removal
- Identify tasks that can be batched together

### General Board Hygiene
- Ensure all active work has a task
- Verify agent statuses match their assigned tasks
- Clean up duplicate or abandoned tasks
- Post to feed if any significant changes made

**Frequency:** Every heartbeat (typically every 30 min)
**Goal:** Keep the board accurate, current, and actionable

---

## 💓 Agent Heartbeat Polling (v2)

**For autonomous agents using the Jarvis pattern:**

Each agent should poll every 15 minutes to:
1. Report their liveness via `PUT /api/agents/:id/heartbeat`
2. Get the next available task via `GET /api/agents/:id/next-task`
3. Self-assign and begin work if tasks are available

```bash
# Agent heartbeat
curl -X PUT <BACKEND_URL>/api/agents/AGENT_ID/heartbeat \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{"status": "working", "current_task_id": 123}'

# Agent gets next task (self-discovery)
curl -X GET <BACKEND_URL>/api/agents/AGENT_ID/next-task \
  -H "x-api-key: <API_KEY>"
```

**Agent status values:**
- `idle` - Waiting for work
- `working` - Currently executing a task
- `blocked` - Waiting on dependency or human
- `offline` - Not responding

**Liveness indicator:** `last_heartbeat` timestamp on agent record. If >15 min old, agent may be stuck.

---

## 🤖 Jarvis Multi-Agent Pattern (v2 Best Practices)

The Jarvis pattern enables fully autonomous multi-agent coordination where agents self-discover and claim tasks.

### Core Principles

1. **15-Minute Heartbeat Polling**
   - Each agent polls every 15 minutes via `PUT /api/agents/:id/heartbeat`
   - Heartbeat reports agent status (idle/working/blocked)
   - Response includes `next_task` if one is assigned or available

2. **Hierarchical Agent Structure**
   ```
   Coordinator (Goku)
       ↓ delegates
   Specialists (Vegeta, Bulma, Gohan, Piccolo, Trunks)
       ↓ execute
   Report back to coordinator
   ```

3. **Self-Discovery & Task Claiming**
   - Agents query `GET /api/agents/:id/next-task` to find work
   - Unassigned tasks in "backlog" or "todo" are fair game
   - Agent claims task by updating `agent_id` and status

4. **Multi-Agent Collaboration**
   - Multiple agents can work on ONE task via `/api/tasks/:id/assignees`
   - Roles define responsibility: lead | contributor | reviewer
   - Use subtasks to parallelize work

5. **Deliverable-First Thinking**
   - EVERY task must have a deliverable
   - Set `deliverable_type` and `deliverable_content` on creation
   - No task is complete until deliverable is produced

### Agent Heartbeat Loop

```javascript
// Pseudocode for autonomous agent
async function heartbeatLoop(agentId, intervalMs = 15 * 60 * 1000) {
  while (true) {
    // 1. Report heartbeat
    const heartbeat = await fetch(`/api/agents/${agentId}/heartbeat`, {
      method: 'PUT',
      headers: { 'x-api-key': API_KEY },
      body: JSON.stringify({ status: 'idle' })
    });
    
    // 2. Check for assigned task or claim new one
    const response = await fetch(`/api/agents/${agentId}/next-task`, {
      headers: { 'x-api-key': API_KEY }
    });
    const { task } = await response.json();
    
    if (task) {
      // 3. Execute task
      await executeTask(task);
      
      // 4. Update task status
      await fetch(`/api/tasks/${task.id}`, {
        method: 'PUT',
        headers: { 'x-api-key': API_KEY },
        body: JSON.stringify({ 
          status: 'completed',
          deliverable_content: '...' 
        })
      });
    }
    
    // 5. Wait before next poll
    await sleep(intervalMs);
  }
}
```

### Task Assignment Best Practices

| Scenario | Approach |
|----------|----------|
| Single specialist | Assign via `agent_id` on task |
| Lead + contributors | Use `/api/tasks/:id/assignees` with roles |
| Parallel work | Create subtasks, assign different agents |
| Review required | Add reviewer role, set `requires_approval: true` |

### Human Approval Gates

For critical tasks that require human sign-off:

```bash
# Create task requiring approval
curl -X POST $URL/api/tasks \
  -d '{"title": "Deploy v2.0", "requires_approval": true}'

# Human approves
curl -X PUT $URL/api/tasks/ID/approve \
  -d '{"approved_by": "Adarsh"}'

# Agent checks before proceeding
curl -X GET $URL/api/tasks/ID  # Check approved_at != null
```

---

## Files

- `SKILL.md` - This file
- `templates/update_dashboard.js` - Status update script
- `references/themes.md` - Full theme character lists
