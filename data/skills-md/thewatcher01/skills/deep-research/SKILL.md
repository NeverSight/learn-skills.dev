---
name: deep-research
description: "Systematic deep research methodology for complex tasks requiring comprehensive web, GitHub, community, and documentation research. Use when: deep dive, comprehensive research, SOTA analysis, technology evaluation, architecture decisions, library comparison, migration planning, complex debugging, best practices audit, prior art search, unfamiliar patterns, competitive analysis, security audit research."
---

# Deep Research Skill

Systematic methodology for autonomous comprehensive research. This skill transforms any task into a research-backed, SOTA-optimized implementation by following a structured protocol.

---

## When This Skill Activates

This skill supplements the always-on `auto-research` instruction with **detailed methodology** for complex research scenarios:

- Architecture decisions (new system, major refactor, technology choice)
- Technology evaluations (comparing libraries, frameworks, approaches)
- Migration planning (version upgrades, library swaps, architectural shifts)
- Complex debugging (unfamiliar errors, subtle issues, environment-specific bugs)
- Best practices audit (security, performance, accessibility, SEO)
- Prior art search (has someone solved this before? how?)

---

## Phase 1 — Scope & Strategy (Before Searching)

### 1.1 Decompose the Task

Break the request into atomic research questions:

```markdown
## Research Questions
- Q1: What is the SOTA approach for [specific problem]?
- Q2: What are the known pitfalls/anti-patterns?
- Q3: What version/compatibility constraints exist?
- Q4: Are there existing implementations to reference?
```

### 1.2 Identify Search Domains

Map each question to the most relevant sources:

| Question Type              | Primary Sources                                    | Secondary Sources                  |
| -------------------------- | -------------------------------------------------- | ---------------------------------- |
| "How to" / Implementation  | Official docs, GitHub examples                     | Community blogs, SO answers        |
| "Best practice" / Pattern  | Framework guides, GitHub discussions, awesome-lists | Conference talks, expert blogs     |
| "Bug / Issue"              | GitHub issues, SO, framework changelogs            | Community forums, Discord          |
| "Compare" / Evaluate       | npm trends, GitHub stars/activity, benchmarks       | Blog comparisons, Reddit threads   |
| "Security" / Vulnerability | CVE databases, security advisories, official docs  | OWASP guides, security blogs       |
| "Architecture" / Design    | ADRs in open-source repos, framework docs          | Martin Fowler, thoughtworks radar  |

### 1.3 Define Search Keywords

Generate **3-5 search query variants** per question using:
- Exact terms: `"TanStack Query v5" suspense streaming`
- Alternations: `nextjs|next.js "app router" caching|cache`
- Error-specific: paste exact error message + framework version

---

## Phase 2 — Parallel Research Execution

### 2.1 Codebase Scan (Always First)

```
1. grep_search / semantic_search for related patterns in workspace
2. Check package.json / lock files for pinned versions
3. Read existing implementations of similar features
4. Check project conventions (AGENTS.md, instructions, README)
```

### 2.2 Web Research (Parallel Batches)

Launch **2-4 parallel `web/fetch` calls** per batch:

**Batch 1 — Official Sources:**
- Framework/library official docs (latest version matching project)
- GitHub repository README, CHANGELOG, migration guide
- Official blog posts / announcements

**Batch 2 — Community Sources:**
- GitHub Issues/Discussions (filter: open + closed, sort by reactions)
- Stack Overflow (tagged questions, sort by votes)
- awesome-* lists for the technology

**Batch 3 — Deep Dive (if needed):**
- Specific GitHub repos implementing the pattern
- npm/registry package comparisons
- Blog posts from recognized experts
- Conference talk summaries

### 2.3 Source Quality Checklist

For each source found, quickly assess:

- [ ] **Date**: Published within last 6 months? (if older, is the info stable/version-independent?)
- [ ] **Version**: Matches project's pinned versions? (reject v4 guides when project uses v5)
- [ ] **Authority**: Official docs > maintainer comments > expert blogs > random posts
- [ ] **Validation**: Can the claim be cross-referenced with at least one other source?
- [ ] **Completeness**: Does it address edge cases, not just happy path?

---

## Phase 3 — Synthesis & Enrichment

### 3.1 Cross-Reference Matrix

For conflicting information, build a decision matrix:

```markdown
| Approach  | Source 1 (docs) | Source 2 (GitHub) | Source 3 (blog) | Verdict     |
| --------- | --------------- | ----------------- | --------------- | ----------- |
| Option A  | ✅ Recommended  | ⚠️ Works but...  | ✅ Preferred    | → Use this  |
| Option B  | ❌ Deprecated   | ✅ Still works    | ❌ Anti-pattern | → Avoid     |
```

### 3.2 Enrichment Checklist

After research, enrich the original request with:

- [ ] **Missing requirements** the user didn't consider (edge cases, error handling, a11y)
- [ ] **SOTA patterns** discovered during research (better alternatives to naive approach)
- [ ] **Anti-patterns** to explicitly avoid (with source citation)
- [ ] **Version-specific gotchas** for the project's stack
- [ ] **Performance implications** of the chosen approach
- [ ] **Security considerations** if applicable
- [ ] **Testing strategy** informed by common failure modes found in issues

### 3.3 Synthesis Output Format

Before implementing, briefly present findings:

```markdown
## Research Findings

**Approach**: [chosen approach with 1-sentence justification]
**Key Sources**: [2-3 most authoritative sources with URLs]
**Enrichments**: [what was added beyond the original request]
**Risks**: [any gotchas or limitations discovered]
```

Keep this short (5-10 lines max). The user wants implementation, not a thesis.

---

## Phase 4 — Implementation Integration

### 4.1 Apply Findings

- Implement using the SOTA approach identified in research
- Add inline comments citing sources for non-obvious decisions: `// Ref: https://... — avoids hydration mismatch`
- Apply discovered anti-pattern avoidance proactively
- Include error handling for edge cases found in issue trackers

### 4.2 Post-Implementation Validation

- Verify implementation matches the approach described in official docs
- Check for version-specific behaviors (breaking changes, deprecated APIs)
- If available, run tests to confirm the approach works

---

## Common Research Templates

### Template: Library/Framework Feature

```
1. Check official docs for [feature] in [version]
2. Search GitHub issues: "[feature] [version]" label:bug|enhancement
3. Check CHANGELOG for breaking changes since [version]
4. Find usage examples in popular repos
```

### Template: Bug Investigation

```
1. Search exact error message in GitHub issues
2. Check if fixed in newer version (CHANGELOG)
3. Search Stack Overflow with error + framework version
4. Check if related to known breaking change
```

### Template: Architecture Decision

```
1. Search ADRs in reference architectures (GitHub)
2. Check official framework recommendations
3. Compare approaches in popular open-source projects
4. Read expert analysis (ThoughtWorks Radar, Martin Fowler, etc.)
5. Check community consensus (Reddit, Discord, Discussions)
```

### Template: Technology Comparison

```
1. npm trends / star history (activity != quality, but stale = risk)
2. Bundle size comparison (bundlephobia)
3. Official docs quality and completeness
4. GitHub issues: response time, community health
5. Migration path from current tool
```

---

## Anti-Patterns to Avoid

- ❌ **Research paralysis** — don't spend 10 min researching a 30-second fix
- ❌ **Source dumping** — don't paste raw research at user; synthesize
- ❌ **Outdated confidence** — don't trust a 2022 guide for a tool on v5 when project uses v8
- ❌ **Single source** — never base architectural decisions on one blog post
- ❌ **Ignoring codebase** — always check existing patterns first; consistency > theoretical best
- ❌ **Over-researching** — 3 quality sources beat 15 mediocre ones

