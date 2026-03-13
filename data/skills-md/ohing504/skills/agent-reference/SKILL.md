---
name: agent-reference
description: "Generate objective reference check reports about the user from real AI collaboration data — session history, git logs, GitHub profile, and memory files. Like a colleague writing a professional reference, but grounded in actual shared work. Use whenever the user asks to evaluate them as a developer, wants a reference letter, work style analysis, introduced by my agents content, interview prep from collaboration history, or blog topics from past discussions. Triggers on: write a reference, analyze my work patterns, what do you think of me, 나에 대한 레퍼런스 써줘, 내 작업 스타일 분석해줘. Not for general code review, architecture docs, cover letters, or codebase-only analysis."
---

# Agent Reference — Introduced by My Agents

You are writing an objective reference check report about a user you've worked with — like a colleague writing a professional reference letter, but grounded in your actual experience as an AI agent.

This is valuable because you have direct evidence from real collaboration: the decisions they made, how they communicated, what they built, how they handled problems. Your report should be honest, specific, and evidence-based — not a flattering endorsement.

## How This Skill Works

There are two phases, each triggered by the user:

| Phase | Command | What happens |
|-------|---------|-------------|
| **Analyze** | "analyze", "write a reference", "analyze my work style" | You analyze your own sessions and produce individual reports |
| **Aggregate** | "aggregate", "combine reports", "create summary" | You combine reports from multiple agents into unified outputs |

Most users will run Phase 1 in each agent they use, then run Phase 2 once to combine everything.

---

## Phase 1: Individual Analysis

You analyze the user's collaboration history and produce two types of reports:

1. **User Profile Report** — who they are as a person/collaborator (consistent across projects)
2. **Project Report(s)** — what they did in each specific project

### Step 1: Collect Data

You have access to rich local data about the user's work. Gather evidence from these sources before writing anything.

#### Data Sources (in order of efficiency)

> **Non-Claude-Code agents**: The paths below are Claude Code-specific. If running in Cursor, Windsurf, Cline, Aider, or other agents, read `references/multi-agent-data-sources.md` for equivalent paths and formats. Git history and memory/rules files are available across all agents.

**1. Auto Memory files** (start here — already-distilled insights):
```
~/.claude/projects/{project-path}/memory/MEMORY.md
```
Each project has a memory file with patterns, preferences, and lessons learned across sessions. These are the most information-dense source — curated summaries of what agents observed over time.

**2. Git history** (structured, searchable):
```bash
git log --oneline --since="6 months ago" -50    # recent activity
git shortlog -sn                                 # contribution volume
git log --format="%s" -100                       # commit message patterns
```
Analyze across all projects the user works on (check `~/.claude/projects/` for project paths). Git history reveals: commit style, code quality, decision patterns, work cadence.

**3. Session conversation logs** (deepest detail):
```
~/.claude/projects/{project-path}/{session-id}.jsonl
```
JSONL files containing full conversation transcripts — user messages, assistant responses, tool calls. Each line is a JSON object with `type` field (`"user"`, `"assistant"`, `"tool_use"`, `"progress"`, etc.). User messages are in objects where `type` is `"user"` with a `message.content` field. Assistant messages have `message.role: "assistant"`.

These files can be large. Sampling strategy:
- Count total sessions per project to gauge volume
- Read recent sessions first (more representative of current style)
- Sample across different projects for breadth
- Look for sessions with high tool call counts (more substantive work)

**4. Session statistics** (quantitative patterns):
```
~/.claude/.session-stats.json
```
Per-session tool usage counts and timestamps. Reveals: which tools the user relies on, session frequency, work patterns over time.

**5. Project-specific state** (if available):
- `.omc/project-memory.json` — structured project knowledge
- `.omc/notepad.md` — working notes
- Project `CLAUDE.md` files — user's instructions to agents

**6. GitHub profile & repository data** (public activity + opt-in private):
```bash
gh auth status                           # check if gh CLI is available
gh repo list --limit 50 --json name,isPrivate,pushedAt,primaryLanguage
```
If `gh` CLI is authenticated, read `references/github-analysis-guide.md` for the full workflow. This includes: contribution calendar (커밋 잔디), per-repo activity, PR patterns, language distribution, and privacy handling for private repos.

**Important**: Always present the repo list to the user and let them choose which repos to include. Private repos default to the Private level — never expose private repo details without explicit consent.

#### Discovering Projects

Data about the user may be spread across multiple sources. Combine them to build a complete picture.

**1. Session-tracked projects** (have conversation history):
```bash
ls ~/.claude/projects/
```
Directory names encode project paths (e.g., `-Users-ohing-workspace-financial` → `/Users/ohing/workspace/financial`). Count `.jsonl` files in each to see session volume.

**2. Local workspace projects** (may lack session data):
Ask the user where they keep their projects — e.g., `~/workspace`, `~/projects`, `~/code`. Then scan for git repos:
```bash
find ~/workspace -maxdepth 2 -name ".git" -type d 2>/dev/null | sed 's/\/.git$//'
```
This catches projects the user worked on before switching machines, before using AI agents, or with other tools that don't leave session logs. These projects can still be analyzed via git history.

**3. GitHub repos** (remote activity):
If `gh` CLI is available, actively pull the user's repo list and contribution data. See Data Source #6 above and `references/github-analysis-guide.md` for the full workflow. Use the repo list to identify projects not available locally.

#### Present a Selection Interface

After discovering projects from all sources, present a unified list to the user. **Scale the display based on project count:**

**Few projects (≤10 total):** Show all with details
```
Found 8 projects:

Session data:
  [x] financial (72 sessions, 140 commits)
  [x] agentfiles (76 sessions, 205 commits)
  [ ] playground (2 sessions) — exclude by default (low activity)

Local workspace:
  [ ] klming-flutter — git history only (347 commits)

GitHub:
  [x] oss-contrib-repo (public, 12 PRs)
  [ ] old-experiment (public, 3 commits) — exclude by default
```

**Many projects (>10 total):** Group by category, show top projects, summarize the rest
```
Found 34 projects across 3 sources:

Recommended for analysis (high activity):
  [x] financial (72 sessions, 140 commits)
  [x] agentfiles (76 sessions, 205 commits)
  [x] my-saas-app (45 sessions, 312 commits)
  ... and 4 more with significant activity

Skipping by default (low activity): 23 projects
  (say "show all" to see the full list)

Which ones should I include or exclude?
```

**After selection, offer deeper analysis:**
```
Want me to analyze any of these projects more deeply?
If you provide the local path (e.g., ~/workspace/my-app),
I can read git history, session logs, and code structure
for richer project reports.
```

**Analyzing external project paths:**
When the user provides a project path, you can read its data directly:
```bash
git -C ~/workspace/my-app log --oneline -50          # git history
ls ~/.claude/projects/-Users-*-workspace-my-app/      # session logs
cat ~/.claude/projects/-Users-*-workspace-my-app/memory/MEMORY.md  # memory
```
No skill installation is needed in the target project — read access is sufficient.

**Key principles:**
- Default to including session-tracked projects with meaningful activity
- Default to excluding projects with very low activity (<3 sessions, <5 commits)
- Always ask before including non-session-tracked projects — the user may not want everything analyzed
- Let the user add projects from any path — analysis only needs read access, no skill installation required
- For deeper analysis, request the local project path so you can read git logs and session data directly

#### Assign Privacy Levels

After the user selects projects, ask them to assign a privacy level to each. This applies to **all projects** — not just GitHub repos. The same 4-level system from `references/github-analysis-guide.md` applies:

| Level | What appears in reports |
|-------|------------------------|
| **Full** | Project name, tech stack, specific observations, code patterns |
| **Private** | Generic description, tech stack, observations without identifying details |
| **Stats only** | Contribution counts and patterns only |
| **Excluded** | Not mentioned at all |

**Defaults:**
- Open source / public projects → Full
- Private repos, employer projects → **Private** (ask user to confirm)
- Side projects the user owns → Full (unless user says otherwise)

Present like this:
```
Privacy levels for selected projects:

  financial        [Private] — private repo
  agentfiles       [Full] — public, open source
  klming-flutter   [Private] — private, published app
  klming-fastapi   [Stats only] — private, employer work

Change any? (e.g., "financial to Full", "klming-fastapi to Excluded")
```

### Step 2: Assess Scope

After collecting data, take stock:

- How many projects and sessions do you have data for?
- What types of work are represented (architecture, implementation, debugging, brainstorming)?
- Which data sources were most informative?
- What's your confidence level — Low (<5 sessions), Medium (5-20), or High (20+)?

Be transparent about your data coverage. A report spanning 5 projects and 200+ sessions is fundamentally different from one based on 3 sessions in one project.

### Step 3: Analyze

Read `references/analysis-dimensions.md` for the dimensions to consider: work style, thinking process, communication, philosophy/values, and technical capability.

The dimensions are prompts for reflection, not a checklist. Focus on what you genuinely observed in the data. Skip what you didn't see. Add anything notable that falls outside the predefined categories.

**The cardinal rule: evidence over judgment.** Every observation should be grounded in something specific — a decision, a pattern, a moment. "Good architect" is worthless. "Restructured the entire auth flow after discovering a race condition, choosing a simpler design that eliminated the class of bug" is gold.

**Cross-project patterns are especially valuable.** When the same behavior appears across different projects and time periods, it's a genuine characteristic — not a situational response.

### Common Analysis Pitfalls

**Don't confuse agent actions with user actions.** Session statistics show tool calls the agent made, not actions the user took directly. When citing work patterns, describe what the user *directed* the agent to do — e.g., "consistently asks the agent to explore the codebase before making changes" rather than "used Read 12,433 times." The user's style is revealed by *what they ask for*, not by raw tool counts.

**Don't misjudge project scope from partial data.** A project directory with mostly docs/chore commits may be an umbrella for sub-projects where the real work happens, or it may be a mature service whose development predates the available session history. Check for sub-project directories and git history depth before characterizing a project's maturity level.

**Acknowledge data boundaries.** Your analysis is limited to what's on the current machine. Previous laptops, other AI agents (Claude Desktop, Cursor, etc.), and pre-session-history work are invisible to you. State this explicitly when it affects confidence.

### Step 4: Validate Findings with the User

Present findings in the language of the current session. Before writing reports, present your key findings and ask the user to verify. Session data can be incomplete or misleading — the user knows their own story best.

**Present a summary of what you found:**
```
Here's what I observed from your sessions and git history.
Please correct anything that's wrong or missing:

Work style:
  - You tend to explore the codebase thoroughly before making changes
  - You prefer iterative small commits over large rewrites
  - [anything wrong here?]

Project roles:
  - financial: led architecture decisions, primary contributor
  - agentfiles: rapid prototyping, experimental approach
  - [any project roles I got wrong?]

Notable patterns:
  - Frequently refactored code for readability after getting it working
  - Strong preference for testing before committing
  - [anything I missed or misread?]
```

**Why this matters:**
- Session data only captures what happened on this machine — the user may have done significant work elsewhere
- Agent-observed patterns may miss context (e.g., a "simple" project may have been intentionally minimal)
- The user may want to emphasize or de-emphasize certain aspects of their work style

Incorporate corrections before proceeding to report writing. If the user provides additional context (e.g., "that project was actually a rewrite of a legacy system"), use it to enrich the analysis.

### Step 5: Write Reports

**User Profile Report:**
- Read `references/user-profile-template.md` for the template
- Save as `user-profile.md` inside a `{date}-{agent-name}/` directory
- One per agent, covering the person across all projects

**Project Report(s):**
- Read `references/project-report-template.md` for the template
- Save as `project-{name}.md` inside the same directory
- One per project you have meaningful context on

Write in the language of the current session.

#### Content Sensitivity Guide

Reports may be published on a public portfolio site. **Respect each project's privacy level** and avoid including content that could cause harm when public. Even for "Full" privacy projects, apply these filters:

**Never include (any privacy level):**
- PII: real names of colleagues, email addresses, phone numbers, internal Slack/Discord channels
- Secrets: API keys, tokens, passwords, internal URLs, server addresses, database connection strings
- Security implementation details: RLS function names, auth bypass patterns, SECURITY DEFINER details, error filtering rules — these expand the attack surface of production services

**Avoid for Private/Stats-only projects:**
- Specific business metrics: exact user counts, MAU, revenue, cost figures (use qualitative descriptions like "production-scale service" instead of "3,000+ users, MAU 500+")
- Internal domain model names and entity names that could identify the project
- Infrastructure stack details: specific cloud services, container orchestration, CI/CD runner setup
- Employer internal systems: auth architecture (e.g., "Keycloak SSO"), payment integrations, internal tool names
- Exact migration dates and timelines

**What TO include (focus on the person, not the project):**
- Technical decision-making patterns and reasoning
- Work style, communication style, problem-solving approach
- General technology categories (e.g., "BaaS migration" not "Firebase→Supabase migration on 2025-07-19")
- Quantified achievements using relative terms (e.g., "dramatically reduced server costs" not "90% cost reduction")

### Step 6: Offer the Reports

Present the reports to the user. They may want to:
- Review and provide feedback before finalizing
- Run Phase 1 in other agents to gather more perspectives
- Proceed directly to Phase 2 aggregation
- Skip Phase 2 and proceed directly to `agent-portfolio` for site generation (Phase 2 is optional — a single agent's reports are sufficient for a portfolio)

When the user provides feedback and corrections, update the report and append a **Review History** section at the bottom. This table records what the user pointed out and what was changed. It serves as evidence that the report was human-reviewed, and provides context for corrections (e.g., "data was limited to current laptop — earlier work on a different machine was not reflected"). See the templates for the format. If the user doesn't request changes, omit this section.

**Suggested output directory**: Save reports to a `reports/` directory in the current working directory (typically the portfolio repo) for easy use with `agent-portfolio`:

```
reports/
└── {date}-{agent-name}/
    ├── user-profile.md
    ├── project-{name}.md
    └── ...
```

This makes it straightforward to copy reports into a portfolio repo later.

---

## Phase 2: Aggregation

Combine individual reports from multiple agents into unified outputs. This phase can run in any agent — it works from the report files, not from session memory.

The user should provide all report files generated in Phase 1.

### Process

Read `references/aggregation-guide.md` for the full aggregation workflow, including:
- How to cross-reference and reconcile observations from different agents
- How to weight reports by confidence level
- How to handle contradictions between agents

Read `references/persona-perspectives.md` for:
- Auto-mapping agent roles (CTO, PM, teammate, etc.) based on report content
- Generating multi-perspective references
- FAQ generation for interviewers
- Blog topic extraction
- Resume-ready "introduced by agents" text

### Outputs

| File | Description |
|------|-------------|
| `aggregated-profile.md` | Unified user profile combining all agent perspectives |
| `aggregated-project-[name].md` | Per-project unified report |
| `references-multi-perspective.md` | Multi-perspective reference (each agent as a named persona) |
| `introduced-by-agents.md` | Resume-ready summary text |
| `faq.md` | Interviewer FAQ with answers grounded in report data |
| `blog-topics.md` | Blog topic suggestions extracted from deep discussion sessions |

---

## Important Principles

**Honesty over flattery.** This is a reference check, not a recommendation letter. Report what you observed with accurate proportions — if 90% positive, reflect that ratio. Don't exaggerate weaknesses for balance, and don't omit them for politeness.

**Specificity is credibility.** The value of an agent reference is that it's grounded in real collaboration data. Generic statements undermine that value entirely.

**Your perspective is unique.** Different agents see different facets of a person. A brainstorming agent sees how they think. A code implementation agent sees how they build. Both perspectives are valuable and should lean into their uniqueness rather than trying to be comprehensive.

**Confidence transparency.** Always declare your confidence level and what it's based on. A reader should know whether your observations come from 3 sessions or 300.
