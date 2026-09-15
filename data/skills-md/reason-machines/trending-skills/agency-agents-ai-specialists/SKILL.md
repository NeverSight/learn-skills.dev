---
name: agency-agents-ai-specialists
description: A collection of specialized AI agent personalities for Claude Code, Cursor, Aider, Windsurf, and other AI coding tools — covering engineering, design, marketing, sales, and more.
triggers:
  - set up agency agents
  - install AI agent personalities
  - use specialized AI agents
  - activate frontend developer agent
  - add agency agents to cursor
  - configure AI specialists for my project
  - install agent prompts for Claude Code
  - use the agency agent collection
---

# 🎭 Agency Agents — AI Specialist Personalities

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A curated collection of 50+ specialized AI agent personalities for Claude Code, Cursor, Aider, Windsurf, Copilot, and more. Each agent has deep domain expertise, a distinct personality, defined workflows, and measurable deliverables — covering engineering, design, marketing, sales, paid media, and beyond.

---

## Installation

### Prerequisites

```bash
git clone https://github.com/msitarzewski/agency-agents.git
cd agency-agents
```

### Claude Code (Recommended)

```bash
# Copy all agents to Claude's agents directory
cp -r agency-agents/* ~/.claude/agents/

# Or symlink for auto-updates
ln -s /path/to/agency-agents ~/.claude/agents/agency
```

Then in any Claude Code session:
```
Hey Claude, activate Frontend Developer mode and help me build a React component
```

### All Other Tools (Interactive Installer)

```bash
# Step 1: Generate integration files for all supported tools
./scripts/convert.sh

# Step 2: Auto-detect installed tools and install interactively
./scripts/install.sh

# Or target a specific tool
./scripts/install.sh --tool cursor
./scripts/install.sh --tool copilot
./scripts/install.sh --tool aider
./scripts/install.sh --tool windsurf
```

### Manual per Tool

| Tool | Install path |
|------|-------------|
| Claude Code | `~/.claude/agents/` |
| Cursor | `.cursor/rules/` in project root |
| Copilot | `.github/copilot-instructions.md` |
| Aider | `.aider.conf.yml` or pass via `--system-prompt` |
| Windsurf | `.windsurf/rules/` in project root |

---

## Agent Roster

### Engineering Division

```
engineering/engineering-frontend-developer.md       React/Vue/Angular, UI, Core Web Vitals
engineering/engineering-backend-architect.md        API design, databases, scalability
engineering/engineering-mobile-app-builder.md       iOS/Android, React Native, Flutter
engineering/engineering-ai-engineer.md              ML models, AI integration, data pipelines
engineering/engineering-devops-automator.md         CI/CD, infra automation, cloud ops
engineering/engineering-rapid-prototyper.md         MVPs, POCs, hackathon speed
engineering/engineering-senior-developer.md         Laravel/Livewire, advanced patterns
engineering/engineering-security-engineer.md        Threat modeling, secure code review
engineering/engineering-code-reviewer.md            PR reviews, code quality gates
engineering/engineering-database-optimizer.md       PostgreSQL/MySQL tuning, slow queries
engineering/engineering-git-workflow-master.md      Branching, conventional commits
engineering/engineering-software-architect.md       System design, DDD, trade-off analysis
engineering/engineering-sre.md                      SLOs, error budgets, chaos engineering
engineering/engineering-incident-response-commander.md  Incident management, post-mortems
engineering/engineering-technical-writer.md         Developer docs, API reference
engineering/engineering-data-engineer.md            Data pipelines, lakehouse, ETL/ELT
```

### Design Division

```
design/design-ui-designer.md                        Visual design, component libraries
design/design-ux-researcher.md                      User testing, behavior analysis
design/design-ux-architect.md                       CSS systems, technical UX
design/design-brand-guardian.md                     Brand identity and consistency
design/design-whimsy-injector.md                    Micro-interactions, delight, Easter eggs
design/design-image-prompt-engineer.md              Midjourney/DALL-E/SD prompts
design/design-inclusive-visuals-specialist.md       Representation, bias mitigation
```

### Marketing, Sales & Paid Media

```
marketing/marketing-growth-hacker.md
marketing/marketing-content-creator.md
paid-media/paid-media-ppc-strategist.md
paid-media/paid-media-creative-strategist.md
sales/sales-outbound-strategist.md
sales/sales-deal-strategist.md
sales/sales-discovery-coach.md
```

---

## Using Agents in Claude Code

### Activating a Single Agent

```
# In Claude Code chat:
Activate the Backend Architect agent and help me design a REST API for a multi-tenant SaaS app.
```

### Using Multiple Agents in Sequence

```
# First, design the system
Activate the Software Architect agent. Design the domain model for an e-commerce platform.

# Then implement
Now activate the Senior Developer agent and implement the Order aggregate in Laravel.

# Then review
Activate the Code Reviewer agent and review the implementation above.
```

### Referencing an Agent File Directly

```bash
# Pass an agent as a system prompt in Claude CLI
claude --system-prompt "$(cat ~/.claude/agents/engineering-frontend-developer.md)" \
  "Build a responsive product card component in React with Tailwind CSS"
```

---

## Using Agents in Cursor

After running `./scripts/install.sh --tool cursor`, agent rules land in `.cursor/rules/`. Reference them in chat:

```
@engineering-frontend-developer Build a data table component with sorting and pagination.
```

Or set a default rule in `.cursor/rules/default.mdc`:

```markdown
---
alwaysApply: true
---

You are operating as the Senior Developer agent from The Agency.
Refer to .cursor/rules/engineering-senior-developer.md for your full persona and workflows.
```

---

## Using Agents with Aider

```bash
# Use a single agent as the system prompt
aider --system-prompt "$(cat agency-agents/engineering/engineering-security-engineer.md)"

# Or reference in .aider.conf.yml
echo "system-prompt: agency-agents/engineering/engineering-devops-automator.md" >> .aider.conf.yml
```

---

## Using Agents in Windsurf

```bash
./scripts/install.sh --tool windsurf
# Agents are written to .windsurf/rules/
```

Activate in chat:
```
Use the UX Architect agent rules from .windsurf/rules/ to audit my CSS architecture.
```

---

## Real Workflow Examples

### Full-Stack Feature with Multiple Agents

```bash
# 1. Architecture phase
cat > task.md << 'EOF'
I need to add real-time notifications to my Node.js + React app.
Users should see in-app alerts and optionally receive email digests.
EOF

# Invoke Software Architect
claude --system-prompt "$(cat ~/.claude/agents/engineering-software-architect.md)" < task.md

# 2. Backend implementation
claude --system-prompt "$(cat ~/.claude/agents/engineering-backend-architect.md)" \
  "Implement the notification service based on the architecture above using PostgreSQL LISTEN/NOTIFY and Socket.io"

# 3. Frontend implementation
claude --system-prompt "$(cat ~/.claude/agents/engineering-frontend-developer.md)" \
  "Build the React notification bell component that connects to the Socket.io feed"

# 4. Security review
claude --system-prompt "$(cat ~/.claude/agents/engineering-security-engineer.md)" \
  "Review the notification system implementation for security issues"
```

### Code Review Workflow

```bash
# Generate a diff and pipe to the Code Reviewer agent
git diff main..feature/payment-integration | \
  claude --system-prompt "$(cat ~/.claude/agents/engineering-code-reviewer.md)" \
  "Review this PR diff. Focus on security, correctness, and maintainability."
```

### Database Optimization

```bash
# Paste slow query log and activate Database Optimizer
claude --system-prompt "$(cat ~/.claude/agents/engineering-database-optimizer.md)" << 'EOF'
Here is a slow query from our PostgreSQL logs (avg 4200ms):

SELECT u.*, p.*, o.*
FROM users u
LEFT JOIN profiles p ON p.user_id = u.id
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > NOW() - INTERVAL '30 days'
ORDER BY o.created_at DESC;

Table sizes: users=2M rows, orders=18M rows. No indexes on created_at columns.
EOF
```

### Incident Response

```bash
# Structured incident kick-off
claude --system-prompt "$(cat ~/.claude/agents/engineering-incident-response-commander.md)" << 'EOF'
SEV-1 INCIDENT: Payment processing returning 503 errors since 14:32 UTC.
Error rate: 94%. Affected: checkout, subscription renewals.
Recent deploys: payment-service v2.4.1 at 14:15 UTC.
EOF
```

---

## Creating Custom Agents

Agent files follow a consistent markdown structure:

```markdown
# 🎯 Agent Name

## Identity
You are [Name], [role] at The Agency...

## Core Mission
[What this agent optimizes for]

## Personality & Communication Style
- [Trait 1]
- [Trait 2]

## Workflows

### [Workflow Name]
1. [Step 1]
2. [Step 2]

## Deliverables
- [Concrete output 1]
- [Concrete output 2]

## Success Metrics
- [Measurable outcome]
```

Save custom agents to `agency-agents/custom/` and re-run `./scripts/convert.sh` to generate tool integrations.

---

## Contributing New Agents

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/agency-agents.git

# Create your agent in the appropriate division
cp engineering/engineering-senior-developer.md \
   engineering/engineering-YOUR-SPECIALTY.md

# Edit the file, then test it
claude --system-prompt "$(cat engineering/engineering-YOUR-SPECIALTY.md)" \
  "Give me a sample deliverable to demonstrate your capabilities"

# Submit a PR
git checkout -b agent/your-specialty
git add engineering/engineering-YOUR-SPECIALTY.md
git commit -m "feat: add Your Specialty agent"
git push origin agent/your-specialty
```

---

## Troubleshooting

**Agents not found in Claude Code**
```bash
ls ~/.claude/agents/
# If empty, re-run:
cp -r /path/to/agency-agents/* ~/.claude/agents/
```

**`convert.sh` fails with permission error**
```bash
chmod +x scripts/convert.sh scripts/install.sh
./scripts/convert.sh
```

**Cursor not picking up agent rules**
```bash
# Rules must be in project root .cursor/rules/
ls .cursor/rules/
# Re-run installer targeting cursor
./scripts/install.sh --tool cursor
```

**Agent personality not activating**
- Be explicit: *"Activate the Frontend Developer agent"* rather than just referencing the topic
- Paste the agent file contents directly into the system prompt if tool integration isn't working
- For Claude Code, confirm agents directory: `claude config get agentsDir`

**Agent conflicts when using multiple**
- Activate one agent per conversation session
- For multi-agent workflows, use separate sessions or Claude Code's subagent feature
- Sequence agents explicitly: architect → implement → review

---

## Project Structure

```
agency-agents/
├── engineering/          # 23 engineering specialist agents
├── design/               # 8 design specialist agents
├── marketing/            # Marketing and growth agents
├── sales/                # 8 sales specialist agents
├── paid-media/           # 7 paid media specialist agents
├── scripts/
│   ├── convert.sh        # Generate tool-specific integration files
│   └── install.sh        # Interactive installer (auto-detects tools)
└── README.md
```

---

## Key Facts

- **License**: MIT
- **51,000+ stars** — battle-tested by a large community
- **No API keys required** — agents are prompt files, not services
- **Tool-agnostic** — works with any LLM tool that accepts system prompts
- **Extensible** — add custom agents following the same markdown pattern
- **PRs welcome** — the roster grows through community contributions
