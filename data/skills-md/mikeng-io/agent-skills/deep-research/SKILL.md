---
name: deep-research
description: Generic multi-domain research framework with domain-aware scheduling. Model-agnostic and domain-agnostic - perform comprehensive research on any topic.
location: managed
dependencies:
  - context
  - preflight
  - domain-registry
allowed-tools:
  - ToolSearch
  - mcp__brave-search__brave_web_search
  - mcp__brave-search__brave_news_search
  - mcp__brave-search__brave_local_search
  - mcp__perplexity__search
  - mcp__web-search-prime__webSearchPrime
  - mcp__web-reader__webReader
  - mcp__sequential-thinking__sequentialthinking
  - mcp__context7__query-docs
  - mcp__zread__search_doc
  - mcp__zread__read_file
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_click
  - mcp__playwright__browser_fill_form
  - mcp__playwright__browser_take_screenshot
  - mcp__playwright__browser_evaluate
  - mcp__browser-tools__takeScreenshot
  - mcp__browser-tools__getConsoleLogs
  - mcp__browser-tools__getNetworkLogs
  - Read
  - Task
  - Skill
  - Write
  - Bash(mkdir *)
---

# Deep Research: Multi-Domain Research Framework

Execute this skill to perform comprehensive research on any topic using domain-aware scheduling and parallel information gathering.

## Execution Instructions

When invoked, you will:

0. **Resolve scope and context** — invoke context skill (always), then preflight if confidence is low
1. **Discover available research tools** using ToolSearch
2. **Analyze the research intent** from working_scope to extract:
   - Primary research topic/question
   - Confirmed domains (from working_scope)
   - Research depth and scope indicators
   - Research methodology requirements (web search, crawling, interactive)

---

## Dependency Check

Before executing any step, verify all required skills are present:

```
[skills-root]/context/SKILL.md
[skills-root]/preflight/SKILL.md
[skills-root]/domain-registry/README.md
```

Where `[skills-root]` is the parent of this skill's directory. Resolve with `ls ../` from this skill's location.

If any required file is missing → **stop immediately** and output:

```
⚠ Missing required skills for deep-research:

  {missing-skill}
    Expected: {skills-root}/{missing-skill}/SKILL.md

Install the missing skill(s):
  git clone https://github.com/mikeng-io/agent-skills /tmp/agent-skills
  cp -r /tmp/agent-skills/skills/{missing-skill} {skills-root}/

Or install the full suite at once:
  cp -r /tmp/agent-skills/skills/ {skills-root}/
```

All dependencies present → proceed to Step 0.

---

## Step 0: Scope & Context Resolution

**Context (always required):**

Invoke `Skill("context")` first. It classifies the research topic, detects relevant domains, and assesses confidence:

```yaml
context_report:
  artifact_type: ""  # code | financial | marketing | creative | research | mixed
  domains: []        # matched domain names from domain-registry
  routing: ""        # routing recommendation (informational for research)
  confidence: ""     # high | medium | low
```

**Preflight (conditional — triggered by context confidence):**

Invoke `Skill("preflight")` only if `context_report.confidence == "low"` OR one or more signals remain unresolved:
- The research topic or question is not clearly stated
- Research intent is ambiguous (background vs. deep dive vs. comparison?)
- Domains cannot be inferred from available context

Preflight fills exactly the gaps context could not resolve (max 3 questions, one at a time):

```yaml
scope_clarification:
  artifact: ""       # primary research topic or question
  intent: "research"
  domains: []        # supplements context_report.domains
  constraints: []    # explicit focus areas, excluded areas, depth preferences
  confidence: ""     # high | medium
```

If `context_report.confidence == "high"` → skip preflight entirely.

**Merge into working scope:**
```yaml
working_scope:
  artifact: ""            # primary research topic or question
  domains: []             # from context_report (authoritative), supplemented by preflight
  constraints: []         # depth, focus, exclusion preferences
  context_summary: ""     # combined description for researcher agent prompts
  research_depth: ""      # BRIEF | STANDARD | COMPREHENSIVE (from constraints or defaults)
```

Use `working_scope` throughout this skill. Steps 1+ use it instead of re-extracting from conversation.

2. **Create a research plan** with domain-aware effort allocation:
   - Primary domains get 70% of research effort
   - Secondary domains get 30% of research effort
   - Generate 5-10 search queries per domain
   - Identify sites that may require browser automation
   - Plan crawling strategy for complex sources

3. **Execute parallel research** using multiple domain-focused agents:
   - Spawn domain researchers in parallel
   - Use web search for general information
   - Use browser automation for interactive sites, paywalls, or dynamic content
   - Use `agent-browser` skill for complex web interactions (multi-step flows, form submission, navigation) — install only, no MCP config needed
   - Fall back to `mcp__playwright__*` tools if agent-browser is not installed (requires Playwright MCP configured)
   - Fall back to `Bash` with `curl`/`wget` for simpler static requests
   - Collect and validate findings from each source

4. **Synthesize findings** across domains:
   - Identify patterns and consensus
   - Surface contradictions and debates
   - Generate evidence-based recommendations

5. **Validate output format** against schema

6. **Generate and save report** to `.outputs/research/`

---

## Step 0: Discover Available Research Tools

Before beginning research, discover all available MCP tools and skills that can be used for information gathering.

### Tool Discovery Process

Use ToolSearch to find available research tools:

```yaml
# Search for web search tools
ToolSearch: "web search"
  → Returns: brave-search (independent index + news + local), web-search-prime, etc.

# Search for AI-synthesized search (Perplexity)
ToolSearch: "perplexity"
  → Returns: mcp__perplexity__search (AI-grounded answers with citations)
  → If found: use for synthesis-heavy queries or to cross-validate web findings

# Search for browser automation tools (agent-browser preferred, playwright as fallback)
ToolSearch: "browser automation"
  → Returns: agent-browser skill, playwright navigation, screenshot, interaction tools

# Search for content extraction tools
ToolSearch: "web reader content"
  → Returns: web-reader, content extraction tools

# Search for documentation query tools
ToolSearch: "documentation query"
  → Returns: context7, zread tools

# Search for DeepWiki codebase intelligence (optional)
ToolSearch: "devin"
  → Returns: mcp__devin__read_wiki_structure, mcp__devin__read_wiki_contents, mcp__devin__ask_question
  → If found: DeepWiki available — use for codebase-grounded research
  → If not found: fall back to local Glob/Grep/Read
```

### Build Tool Inventory

Create an inventory of available tools for the research session:

```yaml
tool_inventory:
  web_search:
    - mcp__brave-search__brave_web_search      # Brave Search MCP — independent index, no Google bias
    - mcp__brave-search__brave_news_search     # Brave news search — recent/breaking content
    - mcp__brave-search__brave_local_search    # Brave local search — geo-specific results
    - mcp__perplexity__search                  # Perplexity MCP — AI-synthesized answers with citations
    - mcp__web-search-prime__webSearchPrime    # WebSearch Prime — fallback general search

  web_reading:
    - mcp__web-reader__webReader

  browser_automation_primary:
    - agent-browser    # Preferred: skill-based, install only — no MCP config needed

  browser_automation_fallback:
    - mcp__playwright__browser_navigate     # Fallback: requires Playwright MCP configured
    - mcp__playwright__browser_snapshot
    - mcp__playwright__browser_click
    - mcp__playwright__browser_fill_form
    - mcp__playwright__browser_evaluate
    - mcp__browser-tools__takeScreenshot    # Visual capture supplement
    - mcp__browser-tools__getConsoleLogs

  documentation:
    - mcp__context7__query-docs
    - mcp__zread__search_doc

  codebase_intelligence:
    - mcp__devin__ask_question          # DeepWiki: AI-grounded Q&A about indexed GitHub repos
    - mcp__devin__read_wiki_structure   # DeepWiki: list documentation topics for a repo
    - mcp__devin__read_wiki_contents    # DeepWiki: read specific topic documentation
    # Optional — requires Devin API key. Falls back to Glob/Grep/Read if unavailable.
    # See: deepwiki/SKILL.md for setup and usage patterns.
```

### Tool Selection Strategy

Choose tools based on research requirements:

**Standard Web Research:**
- Use `web-search` tools for general queries; prefer Brave Search for independent index coverage
- Use Perplexity (`mcp__perplexity__search`) for synthesis-heavy questions or cross-validation — it returns AI-synthesized answers with citations, useful for "what is the current consensus on X"
- Use `web-reader` for content extraction from specific URLs
- Multi-search strategy: run Brave Web + Perplexity in parallel, then cross-reference results to surface contradictions
- Fallback gracefully if tools unavailable

**Dynamic/Interactive Content:**
- Use `agent-browser` skill (preferred — install only, no MCP config required):
  - Invoke via: `Skill("agent-browser")`
  - Handles: JavaScript-heavy sites, interactive forms, dynamic content, paywalls
- If `agent-browser` not installed → fall back to `mcp__playwright__*` (requires Playwright MCP configured)
- If neither available → fall back to `Bash` with `curl`/`wget` for simpler static requests

**Complex Interactions:**
- Use `agent-browser` skill first for:
  - Multi-step workflows (login → navigate → extract)
  - Complex form filling
  - Sites requiring human-like interaction
  - Screenshot capture with analysis
- If `agent-browser` not installed, use `mcp__playwright__*` tools (requires MCP config)
- If neither available, use `Bash` with `curl`/`wget`

### Tool Availability Handling

**If preferred tools unavailable:**
1. Log missing tools
2. Use available alternatives in fallback order
3. Adjust research strategy accordingly
4. Note limitations in final report

**Fallback chain:**
```
agent-browser → mcp__playwright__* → mcp__browser-tools → web-reader → Bash curl/wget
```

---

## Step 1: Intent Analysis & Domain Detection

Analyze the conversation to extract research intent and infer domains.

```yaml
research_intent:
  primary_topic: ""           # Main research question/topic
  explicit_domains: []        # Domains directly mentioned
  inferred_domains: []        # Domains inferred from context
  research_depth: BRIEF | STANDARD | COMPREHENSIVE
  scope_indicators: []        # Keywords suggesting scope (e.g., "overview", "deep dive")
```

### Domain Detection Strategy

**Primary Domains (70% effort allocation):**
Extract from explicit mentions in conversation:
- Topics directly stated by user
- Subject areas named in research questions
- Fields explicitly referenced

**Secondary Domains (30% effort allocation):**
Infer from contextual cues:
- Language patterns (technical vs. business vs. creative)
- Concerns expressed (performance, security, UX)
- Artifacts referenced (code, designs, documents)

**Domain-registry integration:**
Read domain-registry/domains/*.md to supplement inferred domains.
Research domains include: technical, financial, marketing, creative, legal, strategy.
Select all domains matching the research topic signals.

### Domain Inference Examples

```
User: "Research how to implement event sourcing with Kafka"

Explicit domains:
  - Software Architecture
  - Distributed Systems

Inferred domains:
  - Data Engineering (from "event sourcing")
  - Performance (implied by distributed systems context)
```

```
User: "I need to understand the business implications of AI regulation"

Explicit domains:
  - Business
  - Law/Regulation

Inferred domains:
  - Ethics (from "AI regulation")
  - Technology (AI context)
```

### Domain Output Format

```yaml
domain_analysis:
  primary_domains:
    - domain: "{domain name}"
      confidence: HIGH | MEDIUM | LOW
      rationale: "why detected"
      keywords: ["relevant", "terms"]

  secondary_domains:
    - domain: "{domain name}"
      confidence: HIGH | MEDIUM | LOW
      rationale: "why inferred"
      keywords: ["relevant", "terms"]
```

---

## Step 2: Research Planning

Generate a structured research plan with domain-aware effort allocation.

### Research Question Generation

For each domain, generate 5-10 targeted search queries:

```yaml
research_plan:
  domains:
    - domain: "{domain name}"
      effort_allocation: 0.70  # or 0.30 for secondary
      search_queries:
        - "{broad overview query}"
        - "{specific technical query}"
        - "{implementation/practical query}"
        - "{comparison/alternatives query}"
        - "{challenges/limitations query}"
        - "{recent developments query}"
        - "{best practices query}"
        - "{case studies query}"
```

### Query Generation Guidelines

**Query Types:**
1. **Overview**: "What is {topic}?", "{topic} overview"
2. **Technical**: "{topic} implementation", "{topic} how it works"
3. **Practical**: "{topic} best practices", "{topic} tutorial"
4. **Comparative**: "{topic} vs {alternative}", "{topic} alternatives"
5. **Critical**: "{topic} problems", "{topic} limitations"
6. **Current**: "{topic} 2025", "{topic} latest developments"

### Effort Allocation

```yaml
effort_distribution:
  primary_domains: 0.70
  secondary_domains: 0.30

# Per-domain calculation
queries_per_primary_domain: 8-10
queries_per_secondary_domain: 4-6
```

---

## Step 3: Information Gathering

Execute parallel research using domain-focused agents.

### Tool Availability Check

Use the tool inventory from Step 0 to determine research capabilities:

```yaml
# Core tools (expected to be available)
core_tools:
  - web_search                    # Brave Search or WebSearchPrime
  - web_reader                    # For content extraction
  - sequential_thinking           # For logic validation

# Browser automation (for dynamic/interactive content)
browser_tools:
  - agent-browser                 # PRIMARY: skill-based, install only — no MCP config needed
  - playwright_navigate           # FALLBACK: requires Playwright MCP configured
  - playwright_snapshot
  - playwright_click
  - playwright_fill_form
  - playwright_evaluate
  - browser_screenshot            # Visual capture supplement
  - browser_console_logs          # Debug info

# Specialized tools (optional)
specialized_tools:
  - documentation_query           # context7 or zread
  - repository_search             # For code/GitHub research

# Fallback strategy
fallback: "Use available tools, gracefully degrade, note limitations"
```

### Research Methodology Selection

Choose methodology based on source types:

**Codebase-Grounded Research (use DeepWiki if available):**
- Questions about how an existing system works before researching alternatives
- Architecture intent and design decisions behind code you're analyzing
- Cross-component relationships and implicit contracts in a repository
- Use `mcp__devin__ask_question` for synthesis; `mcp__devin__read_wiki_contents` for specific topics
- Falls back to Glob/Grep/Read if DeepWiki not configured

**Static Content (use web_search + web_reader):**
- News articles
- Blog posts
- Academic papers (PDFs)
- Documentation sites
- Wikipedia-style content

**Dynamic Content (use browser_automation):**
- JavaScript-heavy sites (SPAs)
- Infinite scroll pages
- Content loaded on interaction
- Sites with lazy loading

**Interactive Content (use browser_automation via mcp__playwright__*):**
- Sites requiring login (with authorization)
- Multi-step workflows
- Form submissions
- Search interfaces
- Filtered/paginated results

**Paywalled/Gated Content:**
- Use browser automation if access authorized
- Note limitations if access unavailable
- Look for alternative sources

### Domain Researcher Template

Spawn a researcher for each domain using the Task tool:

```
Capability: high

You are a {DOMAIN} RESEARCHER. Your role is to gather comprehensive information about {topic} from a {DOMAIN} perspective.

## Research Focus
{domain_specific_context}

## Search Queries to Execute
{list_of_queries}

## Your Task
1. Execute each search query using available search tools
2. Read promising sources using appropriate method:
   - Static content: web-reader
   - Dynamic content: browser automation (Playwright)
   - Interactive content: agent-browser skill (fallback: mcp__playwright__* if agent-browser not installed)
3. Extract key findings, evidence, and sources with URLs
4. Assess source credibility (HIGH/MEDIUM/LOW)
5. Identify consensus vs. debate in the field

## Tool Strategy

**For Standard Web Research:**
- Use WebSearch tools for finding sources
- Use web-reader for extracting static content
- Use documentation queries for technical topics

**For Dynamic/Interactive Sites:**
- Use `agent-browser` skill (preferred — install only):
  - Invoke: `Skill("agent-browser")` with instructions for the specific interaction
  - Handles navigation, snapshots, screenshots, JavaScript execution
- If `agent-browser` not installed, fall back to Playwright MCP tools:
  - Navigating: `mcp__playwright__browser_navigate`
  - Capturing state: `mcp__playwright__browser_snapshot`
  - Screenshots: `mcp__playwright__browser_take_screenshot`
  - JavaScript execution: `mcp__playwright__browser_evaluate`

**For Complex Interactions:**
- Use `agent-browser` skill first — no MCP config needed, handles:
  - Multi-step workflows (login → navigate → extract)
  - Complex form filling
  - Human-like interaction
- If `agent-browser` not installed, use `mcp__playwright__*` tools (requires Playwright MCP configured)
- If neither available, use `Bash` with `curl`/`wget` for simpler static requests

**URL Requirements:**
- ALWAYS capture source URLs
- Use actual page URLs (not search result URLs)
- Include direct links for cross-referencing
- Note if URL requires authentication

**Graceful Degradation:**
- If browser tools unavailable, try web-reader
- If web-reader fails, note source as "inaccessible"
- Document tool limitations in findings

## Output Format (JSON)
{
  "agent": "domain-researcher-{domain}",
  "domain": "{domain name}",
  "queries_executed": ["list of queries executed"],
  "findings": [
    {
      "topic": "specific finding",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO",
      "consensus": "STRONG | MODERATE | WEAK | DEBATE",
      "evidence": ["supporting points"],
      "sources": [
        {
          "url": "source URL",
          "title": "source title",
          "credibility": "HIGH | MEDIUM | LOW",
          "type": "academic | industry | blog | documentation | other",
          "date": "publication date if available",
          "key_points": ["extracted insights"]
        }
      ]
    }
  ],
  "contradictions": [
    {
      "topic": "what's debated",
      "viewpoints": ["conflicting perspectives"]
    }
  ],
  "gaps": ["information not found or unclear"]
}
```

### Parallel Execution

Spawn all domain researchers in parallel:

```yaml
execution_strategy:
  mode: parallel
  max_concurrent: 10
  timeout: 300  # seconds per researcher

researchers:
  - "{primary_domain_1}"
  - "{primary_domain_2}"
  - "{secondary_domain_1}"
  - "{secondary_domain_2}"
```

### Browser-Based Research Crawling

For sources requiring browser automation, use this workflow:

#### When to Use Browser Automation

Use browser tools when encountering:
- ❌ web-reader returns incomplete content
- ❌ "JavaScript required" messages
- ❌ Dynamic content not loading
- ❌ Search interfaces requiring interaction
- ❌ Paginated results needing navigation
- ❌ Content behind forms or filters

#### Playwright Research Workflow

**Basic Navigation & Extraction:**
```
1. Navigate to URL
   → mcp__playwright__browser_navigate(url)

2. Capture page state
   → mcp__playwright__browser_snapshot
   → Returns: HTML, visible text, accessibility tree

3. Extract specific content
   → mcp__playwright__browser_evaluate(script)
   → Execute JavaScript to extract data
```

**Interactive Research (Forms, Search, Filters):**
```
1. Navigate to site
   → browser_navigate(url)

2. Fill search/filter forms
   → browser_fill_form(selector, value)

3. Click search/submit buttons
   → browser_click(selector)

4. Wait for results to load
   → browser_evaluate("check if loaded")

5. Extract results
   → browser_snapshot or browser_evaluate
```

**Multi-Page Crawling:**
```
For paginated results:
1. Extract page 1
2. Click "Next" button
3. Extract page 2
4. Repeat until complete or limit reached
5. Aggregate all findings
```

#### Complex Interaction via agent-browser (with Playwright MCP fallback)

For complex multi-step workflows, use `agent-browser` skill (preferred — install only, no MCP config needed). If `agent-browser` is not installed, fall back to `mcp__playwright__*` tools (requires Playwright MCP configured). If neither is available, use `Bash` with `curl`/`wget`.

**Preference order:**
```
agent-browser → mcp__playwright__* → Bash curl/wget
```

**Example agent-browser workflow:**
```
Invoke Skill("agent-browser") with instructions:
- Go to {research_site}
- Search for: {query}
- Extract top results: title, URL, summary, date
- Return as structured JSON
```

**Fallback — Playwright MCP (if agent-browser not installed):**
```
1. mcp__playwright__browser_navigate(url="{research_site}")
2. mcp__playwright__browser_fill_form(selector="input[name=q]", value="{query}")
3. mcp__playwright__browser_click(selector="button[type=submit]")
4. mcp__playwright__browser_snapshot() → extract top results with title, URL, summary, date
5. Return as structured JSON
```

#### URL Capture Requirements

**CRITICAL:** Always capture actual content URLs:

✅ **Correct:**
```json
{
  "url": "https://example.com/article/actual-content",
  "title": "Article Title",
  "method": "playwright-browser-automation"
}
```

❌ **Wrong:**
```json
{
  "url": "https://google.com/search?q=...",
  "title": "Search results",
  "method": "web-search"
}
```

**URL Validation:**
- URL must point to actual content (not search results)
- URL must be clickable/accessible
- URL must be permanent (not session-specific)
- If URL requires auth, note: `"access": "requires-authentication"`

#### Browser Automation Best Practices

**Performance:**
- Use browser automation only when necessary
- Prefer web-reader for static content
- Limit concurrent browser sessions (max 3)
- Set reasonable timeouts (30s per page)

**Ethics & Legal:**
- Respect robots.txt
- Honor rate limiting
- Don't bypass paywalls without authorization
- Note access requirements in findings

**Error Handling:**
- If browser automation fails → try web-reader
- If web-reader fails → note as "inaccessible"
- Log failures in research quality assessment
- Don't block research on single source failure

---

## Step 4: Cross-Domain Exploration

After domain researchers complete, spawn cross-domain analysts:

### Cross-Domain Analyst Template

```
Capability: high

You are a CROSS-DOMAIN ANALYST. Your role is to explore intersections and connections between domains.

## Domains to Analyze
{list_of_domains}

## Domain Findings Summary
{summary_of_findings_from_each_domain}

## Your Task
1. Identify intersections between domains
2. Find where domains agree and disagree
3. Surface insights that emerge only from cross-domain perspective
4. Identify trade-offs and tensions

## Output Format (JSON)
{
  "agent": "cross-domain-analyst",
  "intersections": [
    {
      "domains": ["domain1", "domain2"],
      "connection": "how they relate",
      "agreements": ["where domains align"],
      "tensions": ["where domains conflict"],
      "emergent_insights": ["insights from intersection"]
    }
  ],
  "domain_mapping": {
    "domain1": ["related domains"],
    "domain2": ["related domains"]
  }
}
```

---

## Step 5: Analysis & Synthesis

Analyze findings for quality and generate synthesis.

### Validation Strategy (Three-Layer)

**Layer 1: Source Credibility Assessment**
```yaml
credibility_criteria:
  HIGH:
    - Academic papers with peer review
    - Official documentation
    - Industry standards bodies
    - Recognized experts in field

  MEDIUM:
    - Industry blogs (established companies)
    - Technical tutorials (reputable sources)
    - Conference presentations
    - Books from known publishers

  LOW:
    - Personal blogs without credentials
    - Forum discussions
    - Social media posts
    - Unverified claims
```

**Layer 2: Cross-Reference Validation**
```yaml
validation_method: triangulation

# Finding is validated if:
triangulation_criteria:
  - Mentioned by 3+ independent sources
  - Appears in HIGH credibility sources
  - Consistent across domains
```

**Layer 3: Internal Consistency Check**
```
Use sequential-thinking tool to validate:
- Logical consistency of findings
- Cause-effect relationships
- Assumption validity
```

### Synthesis Generation

Generate synthesis by:

1. **Identify Patterns**: What themes emerge across sources?
2. **Surface Debates**: Where do sources disagree?
3. **Assess Evidence**: Which findings are well-supported?
4. **Map Connections**: How do domains relate?

---

## Step 6: Recommendations & Reporting

Generate structured report with evidence-based recommendations.

### Report Structure

```markdown
# Deep Research Report: {Topic}

**Generated:** {timestamp}
**Research Duration:** {duration}
**Domains Analyzed:** {list of domains}
**Sources Consulted:** {count}
**Validation Status:** {VALIDATED | PARTIAL | PRELIMINARY}

## Executive Summary

{3-5 sentence overview of key findings and recommendations}

---

## Research Intent & Scope

**Primary Research Question:**
{main question/topic}

**Scope:**
- Primary Domains: {list}
- Secondary Domains: {list}
- Research Depth: {BRIEF | STANDARD | COMPREHENSIVE}

---

## Key Findings by Domain

### {Domain 1}

#### {Finding 1}

**Consensus:** {STRONG | MODERATE | WEAK | DEBATE}

**Evidence:**
- {point 1}
- {point 2}

**Sources:**
- [{Title}]({URL}) - {credibility} - {key insight}
- [{Title}]({URL}) - {credibility} - {key insight}

#### {Finding 2}

{repeat pattern}

---

## Cross-Domain Insights

### Intersection: {Domain 1} + {Domain 2}

**Connection:** {how domains relate}

**Agreements:**
- {where domains align}

**Tensions:**
- {where domains conflict}

**Emergent Insights:**
- {insights from intersection}

---

## Synthesis & Patterns

### Key Patterns
{patterns identified across domains}

### Contradictions & Debates
{areas of disagreement with viewpoints}

### Information Gaps
{what could not be found or needs more research}

---

## Recommendations

### Recommendation 1: {Actionable recommendation}

**Rationale:** {evidence-based reasoning}

**Confidence:** {HIGH | MEDIUM | LOW}

**Supporting Evidence:**
- {finding from domain/source}

### Recommendation 2: {Another recommendation}

{repeat pattern}

---

## Research Quality Assessment

**Validation Method:** Triangulation across sources
**Source Credibility Distribution:**
- HIGH: {count} sources
- MEDIUM: {count} sources
- LOW: {count} sources

**Cross-Domain Validation:**
- {percentage}% of findings validated across multiple domains

**Limitations:**
- {constraints or gaps in research}

---

## Sources Bibliography

### {Domain 1} Sources
1. [{Title}]({URL}) - {credibility} - {date}
2. [{Title}]({URL}) - {credibility} - {date}

### {Domain 2} Sources
{repeat pattern}

---

## Appendix: Research Methodology

**Search Strategy:**
- Total queries executed: {count}
- Domains researched: {list}
- Tools used: {list}

**Quality Controls:**
- Source credibility assessment: ✓
- Cross-reference validation: ✓
- Internal consistency check: ✓
```

---

## Step 7: Validate Output Format

Before finalizing the report, validate it against the required format specification to ensure consistency.

### Validation Gate

Spawn an output validator sub-agent using the Task tool:

```
Capability: standard

You are an OUTPUT VALIDATOR for deep-research reports. Your role is to ensure format compliance.

## Files to Validate
- Markdown: {path_to_markdown_file}
- JSON: {path_to_json_file}

## Validation Instructions
Follow the validation procedure defined in: skills/deep-research/validators/output-validator.md

## Schema Location
JSON Schema: skills/deep-research/schemas/research-report-schema.json

## Tasks
1. Load and validate JSON against schema
2. Validate markdown structure and required sections
3. Verify source quality and credibility distribution
4. Cross-check consistency between JSON and markdown
5. Generate validation report

## Output Format
Return validation result as JSON with:
- validation_status: PASS or FAIL
- Specific errors and warnings
- Source quality assessment
- Suggestions for fixes

## Strictness
FAIL on any critical errors:
- Missing required fields
- Invalid enum values
- Type mismatches
- Missing required sections
- Poor source quality (>70% LOW credibility)
- Insufficient sources (<3 total)
```

### Handling Validation Results

**If validation PASSES:**
- Proceed to Step 8 (Save Report)

**If validation FAILS:**
1. Display all errors and warnings to user
2. Provide specific suggestions for each violation
3. DO NOT save report as "latest"
4. Ask user if they want to:
   - Fix the issues and regenerate
   - Override validation (with explicit confirmation)
   - Cancel research

**Example failure output:**
```
❌ Validation FAILED

JSON Errors:
- Missing required field: recommendations
- Invalid research_depth value: 'DEEP' (must be BRIEF, STANDARD, or COMPREHENSIVE)
- executive_summary only 35 characters (minimum: 50)

Markdown Errors:
- Missing required section: ## Research Quality Assessment
- Domain 'Machine Learning' in metadata but no findings section

Source Quality Issues:
- Only 2 sources consulted (minimum: 3)
- 80% of sources are LOW credibility (threshold: 70%)
- Only 1 HIGH credibility source (recommended: at least 30%)

Suggestions:
1. Add at least one recommendation with rationale and evidence
2. Change research_depth to BRIEF, STANDARD, or COMPREHENSIVE
3. Expand executive_summary to at least 50 characters
4. Add ## Research Quality Assessment section
5. Add findings section for Machine Learning or remove from domains
6. Conduct more research - consult at least 3 sources total
7. Include more HIGH credibility sources (academic papers, official docs)

Would you like to regenerate the report with corrections?
```

---

## Step 8: Save Report

## Artifact Output

Save to `.outputs/research/{YYYYMMDD-HHMMSS}-research-{slug}.md` with YAML frontmatter:

```yaml
---
skill: deep-research
timestamp: {ISO-8601}
artifact_type: research
domains: [{domain1}, {domain2}]
context_summary: "{brief description of what was researched}"
session_id: "{unique id}"
---
```

Also save JSON companion: `{timestamp}-research-{slug}.json`

**No symlinks.** To find the latest artifact:
```bash
ls -t .outputs/research/ | head -1
```

**QMD Integration (optional, progressive enhancement):**
```bash
qmd collection add .outputs/research/ --name "deep-research-artifacts" --mask "**/*.md" 2>/dev/null || true
qmd update 2>/dev/null || true
```

**Note:** Only save reports that pass validation.

```
.outputs/research/
├── 20250115-143022-research-event-sourcing-kafka.md
├── 20250115-143022-research-event-sourcing-kafka.json
├── 20250116-091545-research-ai-regulation-business.md
└── 20250116-091545-research-ai-regulation-business.json
```

---

## Step 9: Configuration (Optional)

The system uses these defaults unless overridden:

### Default Configuration

```yaml
# Research execution
research:
  parallel_execution: true
  max_concurrent_researchers: 10
  timeout_seconds: 300

# Effort allocation
effort_distribution:
  primary_domains: 0.70
  secondary_domains: 0.30

# Queries per domain
queries_per_domain:
  primary: 8-10
  secondary: 4-6

# Output
output_directory: ".outputs/research/"
output_format: "markdown"
include_json: true
```

### Configuration Override Order

1. Built-in defaults
2. Environment variables
3. Config files in `.outputs/research/config.yaml`
4. Command-line arguments

### Environment Variables

```bash
# Execution
export DEEP_RESEARCH_PARALLEL="true"
export DEEP_RESEARCH_MAX_CONCURRENT="10"
export DEEP_RESEARCH_TIMEOUT="300"

# Effort allocation
export DEEP_RESEARCH_PRIMARY_RATIO="0.70"
export DEEP_RESEARCH_SECONDARY_RATIO="0.30"

# Output
export DEEP_RESEARCH_OUTPUT_DIR=".outputs/research/"
export DEEP_RESEARCH_OUTPUT_FORMAT="markdown"
```

---

## Notes

- **Model-agnostic**: Uses capability levels ("highest", "high", "standard") not specific model names
- **Domain-agnostic**: Works for any domain detected from conversation
- **Conversation-driven**: Extracts research intent and domains from what was discussed
- **Tool-agnostic**: Gracefully handles unavailable tools with fallbacks
- **Evidence-based**: All findings tied to sources with credibility assessment
- **Cross-domain**: Identifies insights that emerge from domain intersections
- **Multi-Model**: For cross-model research synthesis, see `deep-council`
- **Domain-Aware**: Research agents adapt to domain context via domain-registry
- **Context Routing**: If the research scope is complex or multi-domain, invoke the `context` skill first to classify artifact type and determine optimal routing (parallel-workflow vs debate-protocol vs deep-council)
- **Severity vs Consensus**: `severity` (CRITICAL/HIGH/MEDIUM/LOW/INFO) reflects the finding's importance; `consensus` (STRONG/MODERATE/WEAK/DEBATE) reflects source agreement strength — both are recorded per finding
