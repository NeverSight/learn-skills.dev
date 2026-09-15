---
name: github-profile-authority-page
description: Use this skill when creating or redesigning a GitHub profile README and pinned-project strategy so the profile communicates credibility, project taste, current focus, writing, and practical authority without sounding arrogant or exposing private employer work.
---

# GitHub Profile Authority Page Skill

## Purpose

Turn a GitHub profile into a developer landing page.

A strong profile page should answer:

1. Who is this person?
2. What kind of problems do they solve?
3. What should I look at first?
4. Why are they credible?
5. What are they working on now?
6. Where can I read more or contact them?

The goal is not to list everything. The goal is to curate the strongest evidence.

## When to use

Use this skill when the user asks to:

- redesign a GitHub profile README
- make a GitHub profile look more credible, memorable, or professional
- choose pinned repositories
- present projects, articles, accomplishments, or public work
- align GitHub with LinkedIn, portfolio, blog, resume, or job search positioning
- synthesize a “Start Here” section from many projects
- avoid sounding arrogant while still communicating authority

## First: inspect the profile surface

Inspect:

- `USERNAME/USERNAME` repository
- profile `README.md`
- pinned repositories
- public repos and their descriptions
- profile bio, website, location, organizations, social links
- blog/portfolio links
- recent public activity
- README badges, stats cards, and images
- article list or RSS-generated blog section, if present
- whether the profile exposes private employer work, personal addresses, secrets, or misleading claims

If GitHub metadata cannot be read automatically, output a manual checklist.

## Profile strategy

A profile README has a different job than a repo README.

A repo README sells one project.
A profile README sells a coherent pattern across projects.

The profile should not be a dumping ground for every repo. It should show a narrow, credible wedge.

## Naming and ecosystem dependency

When selecting pinned repos or rewriting the profile, inspect repo names.

Use `github-repo-product-naming` if pinned projects have weak names, unclear boundaries, or inconsistent ecosystem positioning.

A strong profile benefits from a coherent naming system. For example:

```text
ProofStack   -> public-safe career proof
AgentDesk    -> agent-ready workstation setup
SystemSmith  -> engineering methods for code, agents, and architecture
```

This is stronger than pinning generic repo names such as:

```text
proofstack
agentdesk
systemsmith
```

The profile should present the product names, while subtitles explain the literal use case.

## Reverse-engineered profile patterns

Strong technical profiles often use these blocks:

### 1. Identity wedge in the first screen

Common formula:

```md
# Hi, I'm <Name>

📍 <location or remote context> | <current role/wedge> | <credible anchor>

I build <category of things> for <audience/problem>. Right now I’m focused on <current focus>.
```

Good:

```md
# Hi, I'm Arthur

Junior Data Engineer building practical cloud/data workflows and agentic automation tools.

I use Python, AWS, Databricks, and browser automation to turn recurring high-friction workflows into small, reusable systems.
```

Weak:

```md
# Hi there 👋

I'm passionate about technology and always learning new things.
```

### 2. “Start Here” before long lists

Use `## Start Here` to point visitors to 3-6 best items.

Each item should be one line:

```md
- **[Project](link)** — concrete outcome or reason to inspect it.
```

Better:

```md
- **[SystemSmith](link)** — reusable engineering methods for code, agents, docs, security, reviews, and architecture.
```

Worse:

```md
- **[engineering-methods](link)** — my cool engineering docs.
```

### 3. Categorized project portfolio

After “Start Here”, group projects by theme.

Example categories:

- Agentic AI & Browser Automation
- Data Engineering & Cloud Workflows
- Developer Productivity
- Personal Operations Systems
- ML / Research Implementations
- Writing & Case Studies

Avoid one endless list.

### 4. Evidence ladder

Use the strongest public-safe proof available.

Possible proof types:

- current role, if public
- shipped public repos
- articles/case studies
- open-source contributions
- thesis/research projects
- competitions
- demos
- metrics from public projects
- talks/media
- certifications, if relevant

Never include private employer metrics, internal code, private customer data, or confidential project details.

### 5. Current focus

Use a short section:

```md
## Current Focus

- Building agentic automation tools for browser-heavy workflows.
- Improving data/cloud engineering workflows with small CLIs and repeatable pipelines.
- Writing case studies about turning messy work into reusable systems.
```

### 6. Writing section

If the user has articles, add them. For technical credibility, writing often explains project judgment better than repo count.

```md
## Writing

- **[How I cleared 100 tickets in 2 days](link)** — workflow design, automation, and operational leverage.
- **[Article title](link)** — one-line reason to read.
```

### 7. Contact section

Use a compact link row or badges:

```md
## Connect

[Website](...) · [LinkedIn](...) · [Blog](...) · [Email](mailto:...)
```

Do not expose a private home address or personal phone number.

## Recommended profile README structure

Use this default.

```md
# Hi, I'm <Name>

<One-line role/wedge.>

<2-3 sentence positioning paragraph: what you build, for whom, with what stack, and why.>

<p align="left">
  <a href="...">Website</a> ·
  <a href="...">LinkedIn</a> ·
  <a href="...">Blog</a>
</p>

## Start Here

- **[Project 1](...)** — outcome-oriented one-liner.
- **[Project 2](...)** — outcome-oriented one-liner.
- **[Article / case study](...)** — why it matters.

## Current Focus

- ...
- ...
- ...

## Projects

### Agentic AI & Automation

- **[Repo](...)** — what it does and why it matters.

### Data Engineering & Cloud

- **[Repo](...)** — what it does and why it matters.

### Developer Productivity

- **[Repo](...)** — what it does and why it matters.

## Writing

- **[Article](...)** — one-line takeaway.

## Background

- <Public-safe credibility anchor>
- <Relevant education/thesis/competition/open-source contribution>
- <Tools/stack, if useful>

## Connect

...
```

## Pinned repository strategy

GitHub allows up to six pinned items. Use all six only if each is strong.

Recommended mix:

1. best current flagship project
2. best project that shows professional stack
3. best automation/devtool project
4. best writing/portfolio repo or website
5. best older research/thesis/ML repo if still relevant
6. one experimental repo only if it supports the current narrative

Do not pin:

- empty repos
- abandoned toy apps unless labeled as learning archives
- private-looking repo names
- repos with no README
- repos whose About descriptions are vague
- many near-duplicates

Pinned repositories should match the `Start Here` section.

## Project one-liner formulas

Use one of these.

### Outcome formula

```text
<Repo> — helps <audience> achieve <outcome> by <mechanism>.
```

### Problem-to-solution formula

```text
<Repo> — turns <messy recurring problem> into <repeatable workflow/system>.
```

### Case-study formula

```text
<Repo> — case study in <skill>, showing <specific technical judgment>.
```

### Learning archive formula

```text
<Repo> — implementation of <paper/system> to understand <concept>; archived as a learning project.
```

## GitHub profile metadata checklist

### Profile README visibility

The profile README appears when:

- a public repository exists with the same name as the GitHub username
- that repo contains a non-empty root `README.md`

### Profile pins

Choose up to six repositories/gists.

### Profile bio

Recommended length: one sentence.

Formula:

```text
<Data/cloud/AI engineer> building <specific kind of tools> for <specific kind of workflows>.
```

Example:

```text
Junior Data Engineer building practical automation systems for data, cloud, and agentic workflows.
```

### Website

Use the strongest single URL:

- portfolio
- blog
- current flagship project
- Link-in-bio page only if no better option exists

### Repository descriptions

Every pinned repo needs an About description. Use outcome-oriented copy, not “contains code for…”.

### Topics

Every pinned repo should have relevant topics.

## Deterministic audit checks

### First-screen checks

- First 7 lines include name.
- First 10 lines include role/wedge.
- First 15 lines explain what kind of problems the person solves.
- At least one public link exists near the top.
- No generic “I am passionate about technology” wording remains.

### Curation checks

- `## Start Here` appears before long project lists.
- `Start Here` has 3-6 items.
- Each Start Here item has a link and outcome-oriented one-liner.
- Project sections are grouped by theme.
- No section has more than 8 items without a reason.

### Naming checks

- Pinned repo names are product-like or intentionally descriptive.
- Weak names are flagged for `github-repo-product-naming`.
- Product names and subtitles are used consistently.
- The profile’s project ecosystem has a visible pattern.
- Start Here does not expose confusing internal folder names when better product names exist.

### Credibility checks

- At least one public-safe credibility anchor exists.
- Writing/articles are included if available.
- Current focus is explicit.
- Claims are supported by public work or user-provided facts.
- Employer work is not described in confidential detail.
- No fake metrics, stars, awards, affiliations, or production claims.

### Pinned repo checks

- <= 6 pins.
- Pins match the Start Here narrative.
- Every pinned repo has a README.
- Every pinned repo has a useful About description.
- Every pinned repo has topics.
- Empty or outdated repos are not pinned unless explicitly framed as archives.

### Style checks

- Profile is scannable in under 30 seconds.
- No wall of badges without explanation.
- No excessive GitHub stats cards.
- No animated clutter unless it supports the narrative.
- No home address, phone number, API keys, screenshots with secrets, or employer-confidential data.

## Output format

When applying this skill, produce:

1. **Profile diagnosis**: what the current profile communicates and what is missing.
2. **Positioning choice**: the proposed identity wedge.
3. **Project naming/pinning diagnosis**:
   - weak project names
   - proposed product names
   - pinned-repo strategy
4. **Profile README**: complete replacement or patch.
5. **Pinned repo plan**: up to six pins, ordered, with reasons.
6. **Repo metadata updates**:
   - About description for each pinned repo
   - topics for each pinned repo
   - homepage URL, if any
7. **Writing/articles section**: selected links and one-liners.
8. **Safety redactions**: anything to omit or anonymize.
9. **Deterministic checklist result**.

## Tone rules

Use:

- direct, practical, specific language
- restrained confidence
- concrete outcomes
- “public lab” framing when projects are experimental
- “learning archive” framing for old educational repos
- short one-liners for project lists

Avoid:

- humble-brag walls
- unsupported authority claims
- generic passion statements
- too many emojis
- over-indexing on “AI” without explaining the task
- exposing private employer details
- pretending experiments are production products

## Arthur-specific default profile direction

When working on Arthur Zakirov’s profile, use this as the default narrative unless newer evidence overrides it:

```md
# Hi, I'm Arthur

Junior Data Engineer building practical data/cloud workflows and agentic automation tools.

I work with Python, AWS, Databricks, and automation-heavy developer workflows. My public GitHub is a lab for turning recurring friction — apartment search, profile/resume workflows, research, personal operations, and developer tooling — into small, reusable systems.
```

Suggested section themes:

- Agentic AI & Browser Automation
- Data Engineering & Cloud Workflows
- Developer Productivity
- Personal Operations Systems
- ML / Research Archives
- Writing / Case Studies

Default public-safe line:

```md
This GitHub contains public personal projects and learning work. It does not represent private employer code.
```

Preferred ecosystem names:

```text
ProofStack   -> career proof and public-safe positioning
AgentDesk    -> machine and AI-agent workstation setup
SystemSmith  -> engineering methods for code, agents, and architecture
```

Suggested pinned-repo selection criteria for Arthur:

1. ProofStack or the strongest current career/profile automation repo
2. AgentDesk or the strongest setup/workstation/agent environment repo
3. SystemSmith or the strongest engineering-methods repo
4. writing/blog/portfolio repo
5. one data/cloud engineering repo
6. one older ML/thesis/research repo as proof of depth, if polished

Do not pin empty placeholder repos unless explicitly framed as “coming soon” and supported by a strong README.
