---
name: github-repo-product-naming
description: Use this skill when naming or renaming a GitHub repository, product, CLI, plugin, skill pack, framework, app, or public developer project. It reverse-engineers association-based open-source naming patterns and produces product name, repo slug, tagline, About description, topics, rejected names, and README hero copy.
---

# GitHub Repository Product Naming Skill

## Purpose

Name public developer projects so they are memorable, searchable, association-rich, and aligned with the actual product identity.

A good repo name is not just a category. It is a compressed mental model.

Weak:

```text
workstation-setup
engineering-methods
profile-updater-app
automation-tool
my-scripts
```

Stronger:

```text
AgentDesk
SystemSmith
ProofStack
CodexBar
LazyVim
OpenClaw
```

The name should make a visitor think:

```text
“I roughly know what world this belongs to, and I want to inspect it.”
```

## When to use

Use this skill when the user asks about:

- naming a repo
- renaming a repo
- choosing a product name
- choosing a repo slug
- making names more memorable, badass, viral, open-source-native, or marketable
- splitting a repo into multiple public repos
- building a coherent repo ecosystem
- writing GitHub About descriptions
- turning a technical folder name into a product-like project
- avoiding wrong associations
- checking whether a name is already overloaded

Also use this skill automatically inside `github-repo-launch-page` whenever the repo name affects adoption.

## Core principle

Names work through association transfer.

A strong name borrows meaning from things people already know, then twists it toward the new use case.

Examples of association transfer:

```text
OpenAI -> OpenClaw / OpenCode / OpenSpec
LazyGit -> LazyVim -> LazyBrowser / LazyDocs / LazyForms
Codex -> CodexBar
language models + chaining components -> LangChain
mythic messenger -> Hermes Agent
```

The goal is not random cleverness. The goal is to trigger the right mental shortcut.

## Inputs to collect

Before naming, identify:

1. **Thing being named**
   - repo
   - CLI
   - app
   - skill pack
   - framework
   - plugin
   - profile system
   - setup system
   - documentation system

2. **User**
   - developer
   - maintainer
   - data engineer
   - AI-agent builder
   - job seeker
   - creator
   - operator
   - personal productivity user

3. **Job to be done**
   - setup machine
   - write profile
   - build agents
   - review code
   - structure tickets
   - document systems
   - avoid repeated work
   - automate browser workflows
   - package reusable methods

4. **Emotional promise**
   - ready
   - control
   - leverage
   - proof
   - speed
   - craft
   - calm
   - clarity
   - local ownership
   - fewer repeated decisions

5. **Technical identity**
   - code
   - agents
   - systems
   - architecture
   - browser
   - desk/workstation
   - proof/evidence
   - docs
   - workflows
   - skills

6. **Wrong associations to avoid**
   - boats, games, fanfiction, crypto, malware, surveillance, military, dating, gambling, low-quality SEO, unrelated companies, or too-generic consulting language

7. **Ecosystem relationship**
   - standalone project
   - one repo in a suite
   - plugin for existing tool
   - extension of a known pattern
   - personal brand system

## Naming patterns

### 1. Familiar token + twist

Use when the project lives inside a known movement or trend.

Formula:

```text
<known-token><twist>
```

Examples:

```text
OpenClaw
OpenCode
OpenSpec
AgentDesk
CodexBar
```

Good for:

- AI agents
- developer tools
- open-source utilities
- plugins/extensions
- trend-adjacent products

Risk:

- may look derivative if the twist is weak
- may imply affiliation if too close to a trademark or company name

### 2. Ecosystem prefix + adjacent use case

Use when users already understand a naming family.

Formula:

```text
<ecosystem-prefix><new-domain>
```

Examples:

```text
LazyVim
LazyGit
LazyDocker
AgentBrowser
AgentInbox
AgentDesk
```

Good for:

- making annoying workflows easier
- developer utilities
- setup systems
- UI wrappers around known tasks

Risk:

- “Lazy” can imply low rigor if the audience values discipline
- avoid copying active brands too closely

### 3. Technical concept as metaphor

Use when the project’s architecture or mental model is the hook.

Formula:

```text
<technical-concept><mechanism>
```

Examples:

```text
LangChain
VectorStore
SystemSmith
ProofStack
CodeGraph
```

Good for:

- frameworks
- architecture tools
- skill systems
- engineering-method repos
- knowledge systems

Risk:

- too abstract if the subtitle does not clarify the use case

### 4. Surface metaphor

Use when the project places something in a familiar UI/location.

Formula:

```text
<known-thing><surface>
```

Examples:

```text
CodexBar
ClaudeDesk
SlackLens
JiraRadar
GitHubPilot
```

Good for:

- desktop apps
- menu bar apps
- dashboards
- browser extensions
- CLI wrappers
- assistant surfaces

Risk:

- can become too literal if the surface is not central

### 5. Craft / forge / smith metaphor

Use when the repo is about engineering judgment, methods, systems, or transformation.

Formula:

```text
<object><craft-word>
```

Craft words:

```text
Smith
Forge
Craft
Foundry
Workbench
Kit
Stack
OS
Lab
```

Examples:

```text
SystemSmith
ProofForge
SignalCraft
AgentFoundry
MethodKit
```

Good for:

- reusable engineering methods
- agentic AI practices
- architecture frameworks
- code/design review systems
- public methodology repos

Risk:

- `Forge`, `Craft`, and `Foundry` are often overused
- check collisions and wrong associations

### 6. Proof / signal / evidence family

Use when the repo turns private evidence into public positioning.

Examples:

```text
ProofStack
SignalCraft
ProofKit
StoryProof
CareerSignal
```

Good for:

- career positioning
- LinkedIn/resume systems
- portfolio/story generators
- credibility artifacts
- public-safe achievement transformation

Risk:

- too vague if it does not mention career, resume, or public profile in subtitle

### 7. Agent + environment/surface

Use when the repo prepares places where humans and agents work.

Examples:

```text
AgentDesk
AgentBrowser
AgentInbox
AgentShell
AgentOS
AgentBridge
```

Good for:

- workstation setup
- browser automation
- WSL2/macOS/CLI setup
- MCP/tooling environments
- agent-human workspaces

Risk:

- too broad if the repo is only a narrow script collection

### 8. Negative manifesto

Use carefully. It can be memorable, but usually works better as a tagline than a repo name.

Examples:

```text
never-do-work-twice
dont-repeat-yourself
zero-to-one
```

Good for:

- manifestos
- essays
- slogans
- top README lines

Risk:

- too long
- harder as a namespace
- defined by avoided pain rather than desired identity

Often convert it into:

```text
Name: SystemSmith
Tagline: Never solve the same engineering problem twice.
```

## Scoring rubric

Score candidates from 1-5.

### Association fit

Does it trigger the right world?

```text
1 = random or wrong domain
3 = somewhat related
5 = immediately points to the right ecosystem
```

### Specificity

Does it express the actual project rather than a generic category?

```text
1 = vague category
3 = usable but broad
5 = compressed mental model
```

### Memorability

Would someone remember and repeat it?

```text
1 = forgettable
3 = decent
5 = short, distinctive, sticky
```

### Wrong-association risk

Does it trigger unrelated meanings?

```text
1 = strong wrong association
3 = manageable ambiguity
5 = clean association
```

Important: high score here means low risk.

### Ecosystem fit

Does it fit the user’s other repo names?

```text
1 = disconnected
3 = acceptable
5 = coherent naming family
```

### Slug quality

Is it good as a GitHub repo slug, package, CLI, URL, and folder?

```text
1 = long/ugly/confusing
3 = workable
5 = short, lowercase, command-friendly
```

### Expansion potential

Can it hold future scope without becoming misleading?

```text
1 = too narrow or too grandiose
3 = enough room
5 = can become a suite/category
```

Total possible score: 35.

Only recommend names that score at least 26 unless the user explicitly wants a weird or experimental name.

## Wrong-association test

Before recommending a name, test it manually.

Ask:

1. What does this word already mean?
2. What would Google autocomplete likely show?
3. What would GitHub search likely show?
4. Does it sound like a game, fanfiction tool, crypto coin, malware, military tool, adult product, or unrelated company?
5. Does it imply affiliation with a company or product the user does not own?
6. Does the subtitle fix the ambiguity, or is the ambiguity too strong?
7. Would a technical recruiter, open-source maintainer, or engineer understand the intended domain within 5 seconds?

Reject names where the wrong association is stronger than the intended association.

Example:

```text
ShipCraft
```

Problem:

- “ship” strongly triggers boats, ships, games, maritime history, and model-building.
- It may be intended as “ship software,” but the compound makes the maritime reading too strong.

Verdict:

```text
Reject for software engineering methods unless the project is actually about shipping/logistics/maritime.
```

## Collision checks

Check or ask the user to check:

- GitHub repositories
- package registries relevant to the project: npm, PyPI, crates.io, Homebrew, Docker Hub
- domain availability if a website matters
- search engine top results
- trademark risk for commercial use
- social handles if public branding matters

Collision does not automatically reject a name. Reject when:

- top results are unrelated but dominant
- an active project in the same category already owns the name
- the name implies false affiliation
- the slug is unavailable in the user’s GitHub namespace
- the wrong association is hard to override

## Output format

Produce:

```md
## Naming Diagnosis

Current name:
Problem:
Desired association:
Associations to avoid:

## Best Recommendation

Product name:
Repo slug:
Tagline:
GitHub About description:
README hero:
Topics:

## Why This Works

- Association:
- Specificity:
- Memorability:
- Ecosystem fit:
- Wrong-association risk:

## Candidate Table

| Candidate | Score | Association | Risk | Verdict |
|---|---:|---|---|---|

## Rejected Names

- Name — reason rejected.

## Final Copy

# <ProductName>

> <Tagline>

<Positioning paragraph>
```

## Tone rules

Use concrete judgment. Do not present 20 names as equally good.

Prefer:

- one strongest recommendation
- 3-6 serious alternatives
- explicit rejection reasons
- a clear final decision

Avoid:

- generic name storms
- names that merely describe the folder
- hype words without product identity
- names whose ambiguity has to be explained away
- names that imply company affiliation

## Arthur-specific naming system

For Arthur Zakirov’s public repo ecosystem, prefer a coherent product family:

```text
ProofStack   -> career proof and public-safe positioning
AgentDesk    -> machine and AI-agent workstation setup
SystemSmith  -> engineering methods for code, agents, and architecture
```

### ProofStack

Use for:

- career positioning
- resume/LinkedIn/profile systems
- private evidence to public artifact workflows
- portfolio/blog/story generation
- recruiter/interview material
- proof-before-claim writing systems

Canonical copy:

```md
# ProofStack

> Turn private work evidence into public-safe career signal.

ProofStack helps convert raw achievements into credible resumes, LinkedIn sections, portfolio stories, articles, and interview material without leaking private details or overclaiming.
```

About description:

```text
Turn private work evidence into public-safe resumes, LinkedIn sections, portfolio stories, and interview material.
```

Topics:

```text
career-positioning
resume
linkedin
portfolio
technical-writing
proof-of-work
agent-skills
codex
claude-code
public-profile
```

### AgentDesk

Use for:

- workstation setup
- WSL2/macOS/Windows setup
- monitor/browser/Bitwarden/OpenClaw/Codex/Claude setup
- local machine as agent-ready workspace
- human + AI developer environment setup

Canonical copy:

```md
# AgentDesk

> Make any machine ready for human + AI work.

AgentDesk is a setup system for WSL2, macOS, browsers, monitors, Codex, Claude Code, OpenClaw, and other tools that turn a fresh machine into a productive agent-ready workstation.
```

About description:

```text
Setup system for turning WSL2, macOS, browsers, and developer tools into an agent-ready workstation.
```

Topics:

```text
workstation-setup
wsl2
macos
developer-productivity
ai-agents
codex
claude-code
openclaw
browser-automation
agent-workstation
```

### SystemSmith

Use for:

- software engineering methods
- code review and self-review
- security hygiene
- technical messaging
- living artifacts and documentation
- information architecture
- agentic AI engineering
- system architecture
- reusable engineering judgment

Canonical copy:

```md
# SystemSmith

> Engineering methods for code, agents, and architecture.

SystemSmith turns recurring engineering judgment into reusable agent skills: how to scope tickets, review your own work, write durable docs, avoid leaking secrets, structure technical messages, reason about agentic systems, and build cleaner software/information architectures.
```

About description:

```text
Engineering methods for code, agents, docs, security, reviews, and system architecture.
```

Topics:

```text
software-engineering
system-design
agentic-ai
ai-agents
agent-skills
code-review
technical-writing
security
information-architecture
developer-productivity
codex
claude-code
```

## Name-to-boundary mapping for Arthur’s current split

Use this boundary unless the repository evidence says otherwise:

```text
ProofStack:
- resume
- LinkedIn
- bio
- public career positioning
- article/story frameworks
- portfolio proof
- proof-safe achievement packets

AgentDesk:
- hardware
- OS setup
- WSL2
- macOS
- browsers
- monitors
- Bitwarden local profile
- OpenClaw/Codex/Claude setup
- machine-specific config

SystemSmith:
- SWE method
- self-review
- security
- messaging framework
- living artifacts
- format markdown
- engineer agentic AI
- system/information architecture
```

If a skill overlaps:

- If it installs/configures a machine or tool, put it in `AgentDesk`.
- If it expresses career signal or public profile value, put it in `ProofStack`.
- If it teaches engineering judgment, architecture, documentation, review, communication, or agent design, put it in `SystemSmith`.

## Naming checklist

Before final answer:

- Current name assessed.
- Desired association stated.
- Wrong associations listed.
- At least 6 candidates considered.
- Rejected names include reasons.
- Final name has tagline and literal subtitle.
- Repo slug is lowercase and CLI-friendly.
- GitHub About description is provided.
- Topics are provided.
- README hero copy is provided.
- Ecosystem fit is explained.
