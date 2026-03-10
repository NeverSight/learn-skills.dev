---
name: skill-search-optimizer
description: Optimize agent skills for discoverability on ClawdHub/MoltHub. Use when improving search ranking, writing descriptions for semantic search, understanding how the registry indexes skills, testing search visibility, or analyzing why a skill isn't being found.
metadata: {"clawdbot":{"emoji":"🔎","requires":{"anyBins":["npx"]},"os":["linux","darwin","win32"]}}
---

# Skill Search Optimizer

Optimize skills for discoverability on the ClawdHub registry. Covers how search works, how to write descriptions that rank well, content strategies for semantic matching, testing visibility, and competitive positioning.

## When to Use

- A published skill isn't appearing in relevant searches
- Writing a skill description for maximum discoverability
- Understanding how ClawdHub's search indexes and ranks skills
- Comparing your skill's visibility against competitors
- Improving an existing skill's search performance

## How ClawdHub Search Works

### Architecture

ClawdHub uses **vector-based semantic search**, not keyword matching:

```
User query → OpenAI embedding → Vector similarity search → Ranked results
             (text-embedding-*)    (Convex vector index)
```

Key implications:
1. **Meaning matters more than exact keywords** — "container debugging" matches "Docker troubleshooting"
2. **But keywords still help** — the embedding model encodes specific terms with high signal
3. **Description is the primary indexed field** — content may contribute but description is dominant
4. **Short queries match broad descriptions** — "docker" matches skills about containers generally
5. **Specific queries match specific descriptions** — "debug crashed Docker container" favors skills that mention debugging and crashes

### What Gets Indexed

```
PRIMARY:   description field (frontmatter)
SECONDARY: name/slug field
TERTIARY:  skill content (body markdown) — likely summarized or truncated before embedding

The description field is your search ranking. Everything else is secondary.
```

### Search API

```bash
# How search is called internally
# POST https://clawdhub.com/api/cli/search
# Body: { "query": "user search terms", "limit": 10 }
# Returns: ranked list of skills with similarity scores

# CLI search
npx molthub@latest search "your query"
```

## Description Optimization

### The anatomy of a high-ranking description

```yaml
# Pattern:
# [Action verb] + [specific scope]. Use when [trigger 1], [trigger 2], [trigger 3].
# Also covers [related topic].

# Example (strong):
description: >-
  Schedule and manage recurring tasks with cron and systemd timers.
  Use when setting up cron jobs, writing systemd timer units,
  handling timezone-aware scheduling, monitoring failed jobs,
  implementing retry patterns, or debugging why a scheduled task didn't run.

# Why it works:
# - "Schedule and manage recurring tasks" → broad match for scheduling queries
# - "cron and systemd timers" → exact match for specific tool queries
# - "Use when..." triggers → matches natural-language questions
# - "debugging why a scheduled task didn't run" → matches troubleshooting queries
```

### Description formulas

#### Formula 1: Tool-focused skill

```yaml
description: >-
  [Verb] with [tool/technology]. Use when [task 1], [task 2], [task 3].
  Covers [sub-topic 1], [sub-topic 2], and [sub-topic 3].
```

Example:
```yaml
description: >-
  Debug Docker containers and Compose stacks. Use when inspecting
  container logs, diagnosing networking issues, troubleshooting
  build failures, or investigating resource usage. Covers exec,
  health checks, multi-stage builds, and distroless containers.
```

#### Formula 2: Pattern/reference skill

```yaml
description: >-
  [Topic] patterns for [scope]. Use when [task 1], [task 2], [task 3].
  Also covers [related scope].
```

Example:
```yaml
description: >-
  Regex patterns for validation, parsing, and text extraction across
  JavaScript, Python, Go, and grep. Use when writing regex for emails,
  URLs, IPs, dates, or custom formats. Also covers lookahead,
  lookbehind, and search-and-replace for code refactoring.
```

#### Formula 3: Workflow/process skill

```yaml
description: >-
  [Process description] from [start] to [end]. Use when [scenario 1],
  [scenario 2], [scenario 3].
```

Example:
```yaml
description: >-
  CI/CD pipeline configuration from commit to deployment. Use when
  setting up GitHub Actions, creating matrix builds, caching
  dependencies, building Docker images, or managing deployment secrets.
```

### Keyword strategy

Semantic search understands synonyms, but being explicit helps:

```yaml
# Include both the formal term AND common synonyms
description: >-
  SSH tunneling and port forwarding for remote access.
  Use when creating SSH tunnels, setting up port forwards,
  connecting through jump hosts (bastion hosts), managing
  SSH keys, or transferring files with scp and rsync.

# "tunneling" and "port forwarding" are related but distinct queries
# "jump hosts" and "bastion hosts" are synonyms — include both
# "scp and rsync" catches file transfer queries
```

Terms to include:
- **Primary tool names**: `docker`, `git`, `curl`, `make`
- **Action verbs**: `debug`, `test`, `deploy`, `monitor`, `parse`
- **Common synonyms**: `container` / `Docker`, `CI/CD` / `pipeline` / `GitHub Actions`
- **Problem descriptions**: `debugging why X doesn't work`, `troubleshooting Y`

### Description length

```
TOO SHORT (< 50 chars):
  "Make things with Makefiles"
  → Not enough semantic surface for the embedding model

SWEET SPOT (80-200 chars):
  "Write Makefiles for any project type. Use when setting up build
   automation, defining multi-target builds, or using Make for Go,
   Python, Docker, and Node.js. Also covers Just and Task."
  → Rich semantic content, multiple match angles

TOO LONG (> 250 chars):
  [Long paragraph trying to list everything]
  → Gets truncated in search results display
  → Dilutes the embedding with low-signal words
  → Harder to read in listings
```

## Content Optimization

### How body content affects search

The skill body (markdown content after frontmatter) likely contributes to search in two ways:

1. **Skill preview/summary**: The registry may extract or summarize content for display
2. **Secondary embedding signal**: Full content may be embedded separately or appended to description

Optimization strategy:
- **Front-load important terms** in the first paragraph after the title
- **Use headings that match search queries** — "## Encode and Decode" matches better than "## Section 2"
- **Repeat key terms naturally** throughout the document (don't stuff, but don't avoid them either)

```markdown
# GOOD: Heading matches likely search query
## Port Forwarding
## Key Management
## Connection Debugging

# BAD: Generic headings with no search value
## Getting Started
## Advanced Usage
## Miscellaneous
```

### First paragraph optimization

The first paragraph after the title is prime search real estate:

```markdown
# GOOD
# SSH Tunnel

Create and manage SSH tunnels for secure remote access. Covers local,
remote, and dynamic port forwarding, jump hosts, key management,
agent forwarding, and file transfers with scp and rsync.

# BAD
# SSH Tunnel

This skill provides information about SSH.
```

## Testing Search Visibility

### Manual testing

```bash
# Test with the exact queries users would type

# Broad query (should your skill appear?)
npx molthub@latest search "docker"
npx molthub@latest search "testing"
npx molthub@latest search "build automation"

# Specific query (should your skill rank #1?)
npx molthub@latest search "debug docker container"
npx molthub@latest search "write makefile for go project"
npx molthub@latest search "cron job not running"

# Problem-oriented query (does your skill match troubleshooting?)
npx molthub@latest search "container networking not working"
npx molthub@latest search "why is my cron job not executing"

# Synonym query (does your skill match alternative terms?)
npx molthub@latest search "bastion host" # should match ssh-tunnel
npx molthub@latest search "scheduled task" # should match cron-scheduling
```

### Test matrix

Build a test matrix for your skill:

```
SEARCH VISIBILITY MATRIX
Skill: [your-skill-slug]

Query                              | Appears? | Rank | Competitor
─────────────────────────────────────────────────────────────────
[broad term]                       | Y/N      | #__  | [who ranks above]
[specific use case]                | Y/N      | #__  | [who ranks above]
[problem/troubleshooting query]    | Y/N      | #__  | [who ranks above]
[synonym for main topic]           | Y/N      | #__  | [who ranks above]
[related but different topic]      | Y/N      | #__  | [expected?]

TARGET: Appear in top 3 for specific queries, top 10 for broad queries
```

### Iterative improvement

```bash
# 1. Publish initial version
npx molthub@latest publish ./skills/my-skill \
  --slug my-skill --name "My Skill" --version 1.0.0

# 2. Test search visibility
npx molthub@latest search "primary query"
npx molthub@latest search "secondary query"

# 3. If ranking is poor, update the description
# Edit SKILL.md frontmatter

# 4. Publish updated version
npx molthub@latest publish ./skills/my-skill \
  --slug my-skill --name "My Skill" --version 1.0.1 \
  --changelog "Improve description for search visibility"

# 5. Re-test (embeddings update on publish)
npx molthub@latest search "primary query"
```

## Competitive Positioning

### Analyzing competing skills

```bash
# Find skills in your category
npx molthub@latest search "your topic"

# For each competing skill:
# 1. Install it
npx molthub@latest install competitor-skill

# 2. Read the description
head -10 skills/competitor-skill/SKILL.md

# 3. Compare:
#    - Does their description cover queries yours doesn't?
#    - Are they using terms you should add?
#    - What's their content depth vs. yours?
```

### Differentiation strategies

```
STRATEGY 1: Broader scope
  Competitor covers Docker. You cover Docker + Podman + containerd.
  Your description mentions all three → matches more queries.

STRATEGY 2: Deeper specificity
  Competitor covers "git commands". You cover "git workflows" with
  specific scenarios like bisect, worktree, and reflog recovery.
  Your description matches specific troubleshooting queries.

STRATEGY 3: Problem-oriented framing
  Competitor: "Docker container management"
  You: "Debug Docker containers — logs, networking, crashes, resource issues"
  Problem-oriented descriptions match how people actually search.

STRATEGY 4: Cross-tool coverage
  Competitor covers Make only. You cover Make + Just + Task.
  Your description mentions all three → broader match surface.
```

### Filling gaps vs. competing head-on

```
MARKET ANALYSIS:

1. Search for your intended topic
2. Count results:
   0 results → Blue ocean. Any reasonable skill will rank #1.
   1-2 results → Low competition. A better skill wins easily.
   3+ results → Competitive. Need clear differentiation.

For competitive categories, check the existing skills' quality:
- Are their descriptions optimized? (Many aren't)
- Are their examples working? (Test a few)
- Do they cover the full scope? (Often they're narrow)

A well-written skill with an optimized description will outrank
a mediocre skill even in a competitive category.
```

## Registry Dynamics

### Search behavior patterns

```
COMMON SEARCH PATTERNS:

1. Tool name: "docker", "git", "terraform"
   → Match with explicit tool name in description

2. Task description: "deploy to production", "parse CSV"
   → Match with action verbs and task phrases

3. Problem statement: "container not starting", "cron job failed"
   → Match with troubleshooting language in description

4. Comparison: "jest vs vitest", "make vs just"
   → Match by mentioning multiple tools in description

5. How-to: "how to set up CI/CD", "how to forward ports"
   → Match with "Use when setting up..." pattern
```

### Timing and freshness

```
- New skills get indexed immediately on publish
- Updated skills get re-indexed on version bump
- No known freshness bias (older skills don't rank lower)
- The registry is young — early publishers have first-mover advantage
- Slug ownership is permanent — claim good slugs early
```

## Optimization Checklist

```
PRE-PUBLISH SEARCH OPTIMIZATION:

[ ] Description follows the [Action] + [Scope] + [Use when] pattern
[ ] Description is 80-200 characters
[ ] Primary tool/topic names are in the description explicitly
[ ] Common synonyms are included (jump host / bastion host)
[ ] Troubleshooting/problem language is included
[ ] Action verbs match how users search (debug, test, deploy, parse)
[ ] First paragraph after title reinforces key terms
[ ] Section headings use searchable phrases, not generic labels
[ ] Slug is descriptive and matches the primary search term
[ ] No competing skill has a clearly better description for the same queries

POST-PUBLISH VERIFICATION:

[ ] Skill appears in top 3 for its primary specific query
[ ] Skill appears in top 10 for its broad category query
[ ] Skill appears for at least one synonym/alternative query
[ ] Skill appears for at least one problem-oriented query
```

## Tips

- The description field is worth more than the entire rest of the skill for search ranking. Spend 30% of your optimization effort on those 1-2 sentences.
- "Use when..." phrases in descriptions are powerful because they match how users naturally frame searches: "I need something for when X happens."
- Include both the specific tool name AND the general category. "Docker containers" matches both "docker" queries and "container" queries. Just "Docker" misses people searching for "container debugging."
- Problem-oriented language ("debugging why X fails", "troubleshooting Y") matches a huge category of searches that purely descriptive skills miss entirely.
- Test with at least 5 different search queries before publishing. If your skill doesn't appear for its own primary topic, the description needs work.
- Slug names contribute to search matching. `container-debug` is better than `cd-tool` because the slug itself contains searchable terms.
- Don't optimize for queries your skill can't actually answer. Ranking for a query and then disappointing the user is worse than not ranking at all — it leads to reports and uninstalls.
- The registry is young. First-mover advantage is real — claim descriptive slugs and publish quality content now while competition is low.
- Re-publish with a version bump after optimizing your description. The embedding is regenerated on each publish, so description changes take effect immediately.
