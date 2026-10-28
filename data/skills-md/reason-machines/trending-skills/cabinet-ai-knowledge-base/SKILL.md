---
name: cabinet-ai-knowledge-base
description: AI-first knowledge base and startup OS with file-based storage, AI agents, scheduled jobs, and embedded apps
triggers:
  - set up cabinet knowledge base
  - add an AI agent to cabinet
  - configure scheduled jobs in cabinet
  - create a cabinet workspace
  - how do I use cabinet
  - build AI team with cabinet
  - self-hosted AI knowledge base
  - cabinet agent templates
---

# Cabinet AI Knowledge Base

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Cabinet is an AI-first startup OS and knowledge base where everything lives as markdown files on disk. No database, no vendor lock-in — self-hosted with AI agents that have memory, scheduled jobs, embedded HTML apps, git-backed history, and a full web terminal.

---

## Installation

### Quick Start (recommended)

```bash
npx create-cabinet@latest
cd cabinet
npm run dev:all
```

Open [http://localhost:3000](http://localhost:3000) — the onboarding wizard builds your AI team in 5 questions.

### Manual Clone

```bash
git clone https://github.com/hilash/cabinet.git
cd cabinet
npm install
cp .env.example .env.local
npm run dev:all
```

### Prerequisites

- Node.js 20+
- Claude Code CLI: `npm install -g @anthropic-ai/claude-code`
- macOS or Linux (Windows via WSL)

---

## Environment Configuration

```bash
# .env.local
KB_PASSWORD=your_optional_password   # Leave empty for no auth
DOMAIN=localhost                     # Or your custom domain
```

---

## Key Commands

```bash
npm run dev          # Next.js dev server on port 3000
npm run dev:daemon   # WebSocket + job scheduler on port 3001
npm run dev:all      # Both servers together (use this for development)
npm run build        # Production build
npm run start        # Production mode (both servers)
```

---

## Architecture

```
cabinet/
  src/
    app/api/         → Next.js API routes
    components/      → React components (sidebar, editor, agents, jobs, terminal)
    stores/          → Zustand state management
    lib/             → Storage, markdown, git, agents, jobs
  server/
    cabinet-daemon.ts → WebSocket + job scheduler + agent executor
  data/
    .agents/.library/ → 20 pre-built agent templates
    getting-started/  → Default KB pages
```

**Tech stack:** Next.js 16, TypeScript, Tailwind CSS, shadcn/ui, Tiptap, Zustand, xterm.js, node-cron

---

## Project Structure (data directory)

Cabinet stores everything as markdown files under `data/`:

```
data/
  getting-started/
    index.md
  my-project/
    index.md
    research.md
    index.html        ← Embedded HTML app (auto-rendered as iframe)
  .agents/
    .library/
      ceo.md
      product-manager.md
      researcher.md
    active/
      my-ceo/
        index.md      ← Agent definition
        memory.md     ← Agent memory (auto-updated)
```

---

## Agent Definition Format

Agents are defined as markdown files with YAML frontmatter:

```markdown
---
name: Research Scout
role: researcher
schedule: "0 */6 * * *"   # Cron: every 6 hours
skills:
  - web-search
  - summarization
  - reddit-scout
goals:
  - Monitor competitor activity
  - Surface trending topics in AI tooling
  - File weekly summary reports
---

# Research Scout

You are a research agent for [Company Name]. Your job is to...

## Memory

<!-- Agent memory is auto-appended here by the daemon -->
```

---

## Creating a Custom Agent

### Via the UI

1. Navigate to the Agents panel in the sidebar
2. Click "New Agent" and select a template or start blank
3. Fill in role, goals, and schedule
4. Cabinet creates `data/.agents/active/<agent-name>/index.md`

### Programmatically

```typescript
// src/lib/agents.ts pattern — create an agent file directly
import fs from 'fs/promises'
import path from 'path'

const agentDir = path.join(process.cwd(), 'data', '.agents', 'active', 'my-agent')

await fs.mkdir(agentDir, { recursive: true })

await fs.writeFile(
  path.join(agentDir, 'index.md'),
  `---
name: My Custom Agent
role: analyst
schedule: "0 9 * * 1"
goals:
  - Analyze weekly metrics
  - Post summary to #reports channel
---

# My Custom Agent

You are a data analyst agent. Every Monday at 9am you will...
`
)
```

---

## Scheduled Jobs (Cron)

Agents use standard cron syntax in their frontmatter `schedule` field:

```yaml
# Common schedule patterns
schedule: "0 */6 * * *"    # Every 6 hours
schedule: "0 9 * * 1"      # Every Monday at 9am
schedule: "0 8 * * *"      # Every day at 8am
schedule: "*/30 * * * *"   # Every 30 minutes
schedule: "0 0 * * 0"      # Weekly on Sunday midnight
```

The Cabinet daemon (`server/cabinet-daemon.ts`) reads agent files and registers jobs via `node-cron`. Jobs run agent prompts through Claude Code and write results back to the agent's memory file.

---

## Embedded HTML Apps

Drop an `index.html` in any folder under `data/` — Cabinet automatically renders it as an embedded iframe with a full-screen toggle:

```
data/
  my-dashboard/
    index.html    ← Cabinet renders this as an embedded app
    data.json
    style.css
```

Example `data/my-dashboard/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Metrics Dashboard</title>
  <style>
    body { font-family: sans-serif; padding: 20px; background: #1a1a1a; color: #eee; }
    .metric { font-size: 2rem; font-weight: bold; color: #55c938; }
  </style>
</head>
<body>
  <h1>Weekly Metrics</h1>
  <div class="metric" id="count">Loading...</div>
  <script>
    fetch('./data.json')
      .then(r => r.json())
      .then(d => document.getElementById('count').textContent = d.value)
  </script>
</body>
</html>
```

No build step required. Version controlled via git automatically.

---

## Git-Backed History

Every save auto-commits. Cabinet wraps git operations in `src/lib/git.ts`:

```typescript
// Auto-commit on every page save (Cabinet handles this internally)
// To access history via the UI:
// 1. Open any page
// 2. Click the history icon in the toolbar
// 3. Browse diffs and restore any version

// To inspect from the shell:
cd data
git log --oneline
git diff HEAD~1 HEAD -- my-project/research.md
git checkout HEAD~5 -- my-project/research.md  # Restore older version
```

---

## Markdown Page Format

Cabinet pages are standard markdown files with optional frontmatter:

```markdown
---
title: Competitor Analysis
tags: [research, competitors, q2-2026]
created: 2026-04-07
agent: research-scout
---

# Competitor Analysis

## Summary

...

## Last Updated by Agent

<!-- Agent appends updates here -->
```

---

## API Routes

Cabinet exposes Next.js API routes under `src/app/api/`:

```typescript
// Read a page
GET /api/pages?path=my-project/research

// Save a page
POST /api/pages
Body: { path: "my-project/research", content: "# Research\n..." }

// List directory
GET /api/files?dir=my-project

// Run an agent manually
POST /api/agents/run
Body: { agentId: "research-scout" }

// Get agent status
GET /api/agents/status?id=research-scout

// Search all pages
GET /api/search?q=competitor+analysis
```

### Example: Calling the API from TypeScript

```typescript
// Read a knowledge base page
const response = await fetch('/api/pages?path=my-project/research')
const { content, path } = await response.json()

// Save a page
await fetch('/api/pages', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    path: 'my-project/research',
    content: '# Research\n\nUpdated content...'
  })
})

// Trigger an agent run
await fetch('/api/agents/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ agentId: 'research-scout' })
})
```

---

## Zustand State Management

Cabinet uses Zustand stores in `src/stores/`. Key patterns:

```typescript
// Access the page store in a component
import { usePageStore } from '@/stores/pageStore'

function MyComponent() {
  const { currentPage, savePage, pages } = usePageStore()

  const handleSave = async (content: string) => {
    await savePage({ path: currentPage.path, content })
  }

  return <div>{currentPage?.title}</div>
}

// Access agent store
import { useAgentStore } from '@/stores/agentStore'

function AgentPanel() {
  const { agents, runAgent, agentStatus } = useAgentStore()

  return (
    <ul>
      {agents.map(agent => (
        <li key={agent.id}>
          {agent.name} — {agentStatus[agent.id]}
          <button onClick={() => runAgent(agent.id)}>Run</button>
        </li>
      ))}
    </ul>
  )
}
```

---

## Pre-Built Agent Templates

Located in `data/.agents/.library/`. Available roles:

| Department | Agents |
|---|---|
| Leadership | CEO, COO, CFO, CTO |
| Product | Product Manager, UX Designer |
| Marketing | Content Marketer, SEO Specialist, Social Media, Growth Marketer, Copywriter |
| Engineering | Editor, QA Agent, DevOps Engineer |
| Sales & Support | Sales Agent, Customer Success |
| Analytics | Data Analyst |
| Operations | People Ops, Legal Advisor, Researcher |

To activate a template:

```bash
# Copy a template to active agents
cp data/.agents/.library/researcher.md data/.agents/active/my-researcher/index.md
# Then edit goals and schedule in the copied file
```

---

## Adding a New Agent Template

```markdown
<!-- data/.agents/.library/custom-scout.md -->
---
name: Custom Scout
role: researcher
schedule: "0 8 * * *"
skills:
  - web-search
  - summarization
goals:
  - Monitor industry news daily
  - Summarize top 5 findings
  - Append to data/research/daily-digest.md
---

# Custom Scout

You are a research agent. Each morning you will search for recent developments
in [TOPIC] and append a dated summary to the daily digest.

## Instructions

1. Search for "[TOPIC] news" from the last 24 hours
2. Select the 5 most relevant items
3. Write a 2-3 sentence summary per item
4. Append to `data/research/daily-digest.md` with today's date as a heading

## Memory

<!-- Populated automatically -->
```

---

## Common Patterns

### Pattern 1: Knowledge Base with Agent Automation

```
data/
  company/
    overview.md          ← Human-maintained
    competitors/
      analysis.md        ← Agent-updated weekly
      index.html         ← Auto-generated dashboard
  agents/
    competitor-scout/
      index.md           ← Runs every Monday
      memory.md          ← Tracks what it found last week
```

### Pattern 2: Research Pipeline

```
1. Researcher agent scouts Reddit/HN every 6h → writes to data/inbox/
2. Analyst agent summarizes inbox daily → writes to data/research/weekly.md
3. CEO agent reads weekly.md every Monday → writes strategic notes
```

### Pattern 3: Using the Web Terminal

The web terminal (xterm.js + node-pty) gives full shell access inside the browser:

- Press `Ctrl+\`` or click the terminal icon in the sidebar
- Run Claude Code directly: `claude "analyze the data in research/competitors.md"`
- Full shell: edit files, run scripts, commit to git

---

## Troubleshooting

### Daemon not starting

```bash
# Check if port 3001 is in use
lsof -i :3001
# Kill if needed
kill -9 $(lsof -t -i:3001)
# Restart
npm run dev:all
```

### Claude Code not found

```bash
npm install -g @anthropic-ai/claude-code
# Verify
claude --version
```

### Agent jobs not running

```bash
# Check daemon logs
npm run dev:daemon
# Verify cron syntax at https://crontab.guru
# Check agent frontmatter has valid schedule field
```

### Git history not working

```bash
cd data
git status
# If not initialized:
git init
git add .
git commit -m "initial"
```

### Port conflicts

```bash
# Next.js uses 3000, daemon uses 3001
# Override in package.json scripts or set PORT env var
PORT=3002 npm run dev
```

### Embedded HTML app not rendering

- File must be named exactly `index.html`
- Must be inside a folder under `data/`
- Check browser console for CSP/iframe errors
- Try accessing directly: `http://localhost:3000/apps/my-folder`

---

## Self-Hosting in Production

```bash
npm run build
npm run start   # Runs both Next.js and daemon in production mode

# With PM2
pm2 start npm --name "cabinet" -- run start
pm2 save
pm2 startup
```

```nginx
# Nginx reverse proxy
server {
  listen 80;
  server_name yourdomain.com;

  location / {
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
  }

  location /ws {
    proxy_pass http://localhost:3001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
  }
}
```

---

## Resources

- **Website:** [runcabinet.com](https://runcabinet.com)
- **Discord:** [discord.gg/rxd8BYnN](https://discord.gg/rxd8BYnN)
- **Cloud Waitlist:** [runcabinet.com/waitlist](https://runcabinet.com/waitlist)
- **GitHub:** [github.com/hilash/cabinet](https://github.com/hilash/cabinet)
- **Author:** [@HilaShmuel](https://x.com/HilaShmuel)
- **Changelog:** `CHANGELOG.md` in the repo root
