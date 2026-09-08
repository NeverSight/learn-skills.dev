---
name: search-first
description: Use before writing custom code or a research workflow when a maintained library, tool, skill, or proven pattern may already exist. Start with local reuse and targeted evidence; broaden to external research for new dependencies, new mechanisms, or uncertain external facts.
license: MIT
---

# /search-first — Research Before You Code

Systematizes the "search for existing solutions before implementing" workflow.

## Trigger

Use this skill when:
- Starting a new feature that likely has existing solutions
- Adding a dependency or integration
- The user asks "add X functionality" and you're about to write code
- Before creating a new utility, helper, or abstraction

## Workflow

```
┌─────────────────────────────────────────────┐
│  0. NEED + LOCAL REUSE GATE                 │
│     Inspect approved local implementations  │
│     and results before external searching    │
├─────────────────────────────────────────────┤
│  1. RESEARCH DECISION                       │
│     Decide whether reuse, targeted lookup,   │
│     or broader research is actually needed   │
├─────────────────────────────────────────────┤
│  2. TARGETED SEARCH (only when warranted)   │
│     ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│     │ Registry │ │  Tools / │ │  GitHub / │  │
│     │  / docs  │ │  skills  │ │  evidence │  │
│     └──────────┘ └──────────┘ └──────────┘  │
├─────────────────────────────────────────────┤
│  3. EVALUATE                                │
│     Score candidates (functionality, maint, │
│     community, docs, license, deps)         │
├─────────────────────────────────────────────┤
│  4. DECIDE                                  │
│     ┌─────────┐  ┌──────────┐  ┌─────────┐  │
│     │  Adopt  │  │  Extend  │  │  Build   │  │
│     │ as-is   │  │  /Wrap   │  │  Custom  │  │
│     └─────────┘  └──────────┘  └─────────┘  │
├─────────────────────────────────────────────┤
│  5. IMPLEMENT                               │
│     Reuse approved solution or write the    │
│     smallest justified custom code           │
└─────────────────────────────────────────────┘
```

## Decision Matrix

| Signal | Action |
|--------|--------|
| Approved local implementation or result | **Reuse or repair** — no broad fresh search required |
| Specific local gap or uncertainty | **Targeted lookup** — search only for that issue |
| New dependency, new mechanism, or uncertain external fact | **Research** — compare evidence before deciding |
| Exact match, well-maintained, MIT/Apache | **Adopt** — use directly when available or within authorized implementation scope |
| Partial match, good foundation | **Extend** — add a thin wrapper within authorized implementation scope |
| Multiple weak matches | **Compose** — combine 2-3 small packages |
| Nothing suitable found | **Build** — write custom, but informed by research |

## Research Gate

Start with the repository and approved local catalog. Inspect existing modules,
tests, lockfiles, configured tools or skills, prior results, and known patterns
before searching externally. If an approved implementation or result already
meets the need, reuse it. For a known defect or result gap, repair or fill it
and use a targeted lookup only when a specific external fact or compatibility
question remains; do not force a broad external search or launch the full
researcher workflow for every fix.

Broader research is warranted when selecting a new dependency, introducing a
new mechanism or architecture, or relying on external facts that may be
uncertain or changed. Delegate only a bounded, independent search that would
materially improve the decision. For search-only or advisory work, do not turn a
recommendation into an automatic package install, configuration change,
publication, message, or other external mutation. For an implementation request,
ordinary project-scoped dependency installation and configuration are allowed
within the existing task authority and budget; ask before global or system
changes, new external effects, or scope or cost expansion.

## How to Use

### Step 0: Tool Availability Preflight

This is agent guidance, not an executable setup script. Check only the channels
that are relevant to the task and project in front of you.

| Channel | Check | If missing |
|---------|-------|------------|
| Repository search | `rg --files` and targeted `rg` queries | State that only visible files were inspected |
| Package registry | `npm --version`, `python -m pip --version`, or project package manager | Use web/docs search and avoid claiming registry coverage |
| GitHub CLI | `gh auth status` | Use public web or local git history only |
| MCP/docs tools | Available tool list or local MCP config | Fall back to official docs/web search |
| Skill catalog | Inspect the active harness's available skills or configured skill root | Say no local skill catalog was available |

### Academic Literature Path

When the task needs research grounding, method positioning, related work,
citation support, or top-venue precedent, use `$research-evidence` instead of
ad hoc web search. Prefer CVPR, ICCV, ECCV, ICLR, NeurIPS/NIPS, and ICML for
CV/ML work; include CoRL, ICRA, IROS, AAAI, IJCAI, T-ITS, and RA-L only when
the user topic justifies autonomous-driving, robotics, or collaborative
perception coverage.

Use the evidence result to decide `Adopt`, `Extend`, `Compose`, or `Build` only
when the Research Gate calls for external evidence.
Do not claim literature coverage when the research-evidence tool or source
channel was unavailable.

### Quick Mode (inline)

Before writing a utility or adding functionality, mentally run through:

0. Is there an approved implementation or result locally? → Inspect relevant
   modules, tests, configs, and outputs first; reuse or repair it.
1. Is there a specific gap or uncertainty? → Run a targeted lookup only if it
   would change the decision.
2. Is a new dependency or mechanism, or an uncertain external fact involved? →
   Research the relevant registries, docs, or evidence.
3. Is there an MCP or connected tool for this? → Inspect the active tool list and
   relevant configuration when research is warranted.
4. Is there a skill for this? → Inspect the active harness's skill catalog.
5. Is there a GitHub implementation/template? → Search maintained OSS when the
   Research Gate calls for it before writing net-new code.

### Full Mode (agent)

For non-trivial functionality that passes the Research Gate, launch the
researcher agent only when a bounded, independent search would materially help.
Do not launch the full researcher workflow for routine fixes, result fills, or
known local reuse.

```
Agent(subagent_type="general-purpose", prompt="
  Research existing tools for: [DESCRIPTION]
  Language/framework: [LANG]
  Constraints: [ANY]

  Search: relevant package registries, connected tools, agent skills/catalog,
  GitHub, official docs, or academic evidence
  Return: A bounded comparison with recommendation and evidence gaps
")
```

Use the current agent or subagent tool exposed by the active harness. If no
delegation tool is available, run the same bounded search channels directly.

## Search Shortcuts by Category

### Development Tooling
- Linting → `eslint`, `ruff`, `textlint`, `markdownlint`
- Formatting → `prettier`, `black`, `gofmt`
- Testing → `jest`, `pytest`, `go test`
- Pre-commit → `husky`, `lint-staged`, `pre-commit`

### AI/LLM Integration
- Provider SDKs → official documentation or the configured documentation tool
- Prompt management → Check MCP servers
- Document processing → `unstructured`, `pdfplumber`, `mammoth`

### Data & APIs
- HTTP clients → `httpx` (Python), `ky`/`undici` (Node)
- Validation → `zod` (TS), `pydantic` (Python)
- Database → Check for MCP servers first

### Content & Publishing
- Markdown processing → `remark`, `unified`, `markdown-it`
- Image optimization → `sharp`, `imagemin`

## Integration Points

### With planner agent
The planner should invoke researcher before Phase 1 (Architecture Review) when
the Research Gate calls for external research:
- Researcher identifies available tools
- Planner incorporates them into the implementation plan
- Avoids "reinventing the wheel" in the plan

### With architect agent
The architect should consult researcher, when warranted, for:
- Technology stack decisions
- Integration pattern discovery
- Existing reference architectures

### With iterative-retrieval skill
When broader research is warranted, combine for progressive discovery:
- Cycle 1: Broad search (npm, PyPI, MCP)
- Cycle 2: Evaluate top candidates in detail
- Cycle 3: Test compatibility with project constraints

## Examples

### Example 1: "Add dead link checking"
```
Need: Check markdown files for broken links
Search: npm "markdown dead link checker"
Found: textlint-rule-no-dead-link (score: 9/10)
Action: ADOPT — recommend textlint-rule-no-dead-link; install it within an
authorized project implementation
Result: Zero custom code, battle-tested solution
```

### Example 2: "Add HTTP client wrapper"
```
Need: Resilient HTTP client with retries and timeout handling
Search: npm "http client retry", PyPI "httpx retry"
Found: got (Node) with retry plugin, httpx (Python) with built-in retry
Action: ADOPT — recommend got/httpx directly with retry config; apply it within
an authorized project implementation
Result: Zero custom code, production-proven libraries
```

### Example 3: "Add config file linter"
```
Need: Validate project config files against a schema
Search: npm "config linter schema", "json schema validator cli"
Found: ajv-cli (score: 8/10)
Action: ADOPT + EXTEND — recommend ajv-cli; use it within an authorized project
implementation, then write a project-specific schema
Result: 1 package + 1 schema file, no custom validation logic
```

## Anti-Patterns

- **Jumping to code**: Writing a utility without checking if one exists
- **Ignoring MCP**: Not checking if an MCP server already provides the capability
- **Silent skipping**: Reporting "nothing found" when a search channel was unavailable
- **Over-customizing**: Wrapping a library so heavily it loses its benefits
- **Dependency bloat**: Installing a massive package for one small feature
- **Forced discovery**: Running broad external search or the full researcher for a
  routine local fix or result fill
- **Unbounded delegation**: Sending vague research tasks without an independent,
  decision-relevant deliverable
- **Unauthorized mutation**: Installing, configuring, publishing, or sending
  anything merely because a recommendation was made
