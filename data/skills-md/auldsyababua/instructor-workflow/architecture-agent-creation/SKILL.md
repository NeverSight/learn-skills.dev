---
name: architecture-agent-creation
description: Create specialized infrastructure agent definitions for platform/service management (Grafana, Prometheus, Traefik, ERPNext, etc.). Use when the user requests creation of an agent for a specific technology platform or infrastructure component. This skill produces complete agent prompts with integrated research, SOPs, tool references, and handoff protocols following the Linear-First Agentic Workflow framework.
---

# Architecture Agent Creation

## Overview

Create complete, production-ready agent definitions for infrastructure and platform management agents (Grafana, Prometheus, Traefik, ERPNext, n8n, Jupyter, etc.). Each agent definition includes:

1. **Agent prompt file** (`.claude/agents/<agent-name>.md`) with YAML frontmatter
2. **Reference documentation** (3 docs covering best practices, API/CLI reference, troubleshooting)
3. **Integration specifications** (handoff protocols, Linear workflow position, delegation triggers)
4. **Tool requirements** (MCP tools, CLI installation, credentials)

This skill is designed for the **Linear-First Agentic Workflow framework** where Traycer delegates to specialized agents following a 7-Phase TDD workflow.

## When to Use This Skill

Use this skill when:
- User requests "create an agent for [technology]" (e.g., "create a Grafana agent")
- Need to add infrastructure agent to agentic workflow (Prometheus, n8n, Jupyter, Traefik)
- Building agent for specific platform/service (ERPNext, Qdrant, vLLM, OpenWebUI)
- Expanding agent coverage for homelab/infrastructure automation

**Trigger patterns**:
- "Make me an agent for Grafana"
- "Create a Prometheus monitoring agent"
- "I need an agent to manage Traefik reverse proxy"
- "Build an ERPNext integration agent"

**NOT for**:
- Workflow coordination agents (Planning, Action, QA, Tracking) - use `agent-builder` skill instead
- General-purpose coding tasks
- One-off automation scripts

## Core Capabilities

### 1. Agent Definition Research

Research the target technology platform to understand:
- **Purpose & architecture** - What the technology does, how it works
- **Tool ecosystem** - CLI tools, APIs, configuration methods
- **Integration patterns** - How to connect with other services
- **Common workflows** - Typical operational tasks and procedures
- **Best practices** - Security, performance, reliability patterns
- **Real-world examples** - Working commands with expected output

**Tools Used**: WebFetch, WebSearch, official documentation, community resources

**Output**: Comprehensive research brief covering all aspects needed for agent creation

### 2. Agent Prompt Generation

Create complete agent prompt with sections:
- **Agent Identity** - Name, domain, primary responsibility, delegation triggers
- **Core Capabilities** - 3-4 major capability categories with tools and patterns
- **Technology Stack** - Version numbers, tools, dependencies, documentation sources
- **Standard Operating Procedures** - Step-by-step workflows for common tasks
- **Best Practices** - DO/DON'T lists for proper usage
- **Workflow Position** - Where agent fits in 7-Phase TDD workflow
- **Integration Points** - Handoff sources and targets
- **Security Considerations** - Secrets management, access control, vulnerabilities
- **Handoff Protocol** - Incoming/outgoing handoff formats
- **Tool Inventory** - MCP tools, CLI tools, file operations
- **Error Handling** - Common failures, retry strategy, escalation criteria
- **Quality Checklist** - Pre-completion verification items
- **Example Workflows** - 2-3 complete scenarios with commands and output
- **Tool Installation** - Installation commands for all required tools

**Tools Used**: Write tool to create agent prompt file

**Output**: Complete agent prompt file at `.claude/agents/<agent-name>.md`

### 3. Reference Documentation Creation

Generate 3 reference documents in `docs/agents/<agent-name>/ref-docs/`:

**1. Best Practices Guide** (600-800 words):
- Configuration management patterns
- Performance optimization techniques
- Reliability and HA patterns
- Security hardening steps
- Monitoring and observability
- Common pitfalls to avoid

**2. API/CLI Reference** (600-800 words):
- Essential CLI commands with examples
- API endpoints with curl commands and expected responses
- Configuration file formats with YAML/JSON examples
- Data schemas for key resources
- Authentication methods

**3. Troubleshooting Guide** (600-800 words):
- Diagnostic procedures with commands
- Common errors with symptoms and resolutions
- Performance issue diagnosis
- Integration problem solving
- Health check procedures

**Tools Used**: Write tool to create reference docs

**Output**: 3 reference markdown files with concrete, actionable examples

### 4. Integration Specification

Define how agent integrates into agentic workflow:

**Delegation Triggers**: Keywords/patterns that trigger agent from Traycer
**Handoff Sources**: Which agents delegate TO this agent
**Handoff Targets**: Which agents this agent delegates TO
**Linear Workflow Position**: Which phases (Research/Spec/QA/Action/Tracking) agent operates in
**Linear Integration**: MCP tool usage with project filtering examples

**Tools Used**: None (integrated into agent prompt)

**Output**: Integration notes section in agent prompt

## Standard Operating Procedures

### SOP-1: Create Infrastructure Agent from Scratch

**Trigger**: User requests "create an agent for [technology]"

**Steps**:

1. **Gather Requirements**
   ```bash
   # Confirm technology details with user
   # - Technology name and version
   # - Primary use case (what will agent manage?)
   # - Integration points (which other agents will it work with?)
   ```

2. **Research Phase** (15-20 minutes)
   - Use WebFetch/WebSearch to gather:
     - Official documentation (architecture, API reference, CLI tools)
     - Best practices from production deployments
     - Common workflows and operational patterns
     - Security considerations and hardening steps
     - Real command examples with expected output
   - Create research brief in `docs/.scratch/<issue-id>/research-brief.md`

3. **Generate Agent Prompt** (10-15 minutes)
   - Use template from `references/agent-prompt-template.md`
   - Fill ALL sections with researched content (no placeholders)
   - Include concrete examples, working commands, expected output
   - Specify exact version numbers for tools
   - Define retry strategy with timings (2s, 4s, 8s backoff)
   - Add Linear MCP integration with project filtering code
   - Write to `.claude/agents/<agent-name>.md`

4. **Create Reference Documentation** (15-20 minutes)
   - Generate 3 reference docs using templates:
     - `<agent-name>-best-practices.md` - Configuration, performance, security patterns
     - `<agent-name>-api-reference.md` - CLI commands, API endpoints, schemas
     - `<agent-name>-troubleshooting.md` - Diagnostics, common errors, resolutions
   - Write to `docs/agents/<agent-name>/ref-docs/`

5. **Add Integration Specifications** (5 minutes)
   - Define delegation triggers (keywords that invoke agent)
   - Specify handoff sources/targets (which agents communicate)
   - Document Linear workflow position (which TDD phases)
   - List tool requirements (MCP servers, CLI tools, credentials)

6. **Validation Check**
   - [ ] Agent prompt 1,200-1,500 words with ALL sections filled
   - [ ] No placeholders like `[command]` or `[description]`
   - [ ] Each SOP has step-by-step commands (not abstract descriptions)
   - [ ] API examples include full curl commands and expected responses
   - [ ] Security section covers secrets, access control, vulnerabilities
   - [ ] Retry strategy specifies exact backoff timings
   - [ ] Linear MCP integration includes project filtering code
   - [ ] 7-Phase workflow position is clear
   - [ ] Reference docs have concrete examples (not theoretical)
   - [ ] Tool installation has actual commands for all tools

**Output**: Complete agent definition ready for use

**Handoff**: Report completion to Traycer with agent file paths

### SOP-2: Update Existing Infrastructure Agent

**Trigger**: User requests "update [agent] to add [capability]"

**Steps**:

1. **Read Existing Agent Prompt**
   ```bash
   # Read current agent file
   Read .claude/agents/<agent-name>.md
   ```

2. **Research New Capability**
   - Use WebFetch/WebSearch to research new feature
   - Gather commands, API endpoints, examples
   - Identify integration changes needed

3. **Update Agent Prompt**
   - Add new capability to "Core Capabilities" section
   - Update relevant SOP or add new SOP
   - Add to "Tool Inventory" if new tools needed
   - Update "Example Workflows" if applicable

4. **Update Reference Docs (if needed)**
   - Add new API endpoints to API reference
   - Add new best practices
   - Add troubleshooting for new errors

5. **Validation Check**
   - [ ] New capability fully documented with examples
   - [ ] SOPs updated with step-by-step commands
   - [ ] No conflicts with existing capabilities
   - [ ] All sections still have concrete examples

**Output**: Updated agent definition

**Handoff**: Report changes to Traycer

## Best Practices

**DO**:
- ✅ Research official documentation FIRST before writing agent prompt
- ✅ Include actual commands with expected output (not placeholders)
- ✅ Specify exact version numbers (Grafana 11.x, Prometheus 2.48+)
- ✅ Define retry strategy with specific timings (2s, 4s, 8s backoff)
- ✅ Include Linear MCP project filtering code examples
- ✅ Write 2-3 complete example workflows with full command sequences
- ✅ Provide tool installation commands for all dependencies
- ✅ Cover 4+ common errors with symptoms and resolutions
- ✅ Reference official docs as sources

**DO NOT**:
- ❌ Leave placeholder text like `[command]` or `[description]`
- ❌ Write generic descriptions without concrete examples
- ❌ Skip security considerations section
- ❌ Omit retry strategy or escalation criteria
- ❌ Forget Linear MCP project filtering (causes cross-contamination)
- ❌ Create agent without researching current best practices
- ❌ Use outdated version numbers (check latest stable releases)
- ❌ Copy examples without verifying they work

## Workflow Position in 7-Phase TDD

**This skill operates in**:
- **Phase 1 (Research)**: When Research Agent creates infrastructure agent definition

**Receives handoffs from**:
- **Traycer**: User request to create new infrastructure agent

**Delegates to**:
- None (produces deliverable directly)

**Typical flow**:
1. User → Traycer: "Create a Grafana agent"
2. Traycer → Planning Agent: "Use architecture-agent-creation skill"
3. Planning Agent (this skill):
   - Researches Grafana using WebFetch/WebSearch
   - Generates complete agent prompt with all sections
   - Creates 3 reference docs with examples
   - Validates completeness
4. Planning Agent → Traycer: "Grafana agent created at `.claude/agents/grafana-agent.md`"

## Resources

This skill includes reference materials demonstrating the expected output format:

### references/

**agent-prompt-template.md**: Complete template showing all required sections for an infrastructure agent prompt. Based on the enriched Grafana agent prompt with all corrections baked in. Use this as the blueprint for all new agent definitions.

**research-checklist.md**: Systematic checklist of research areas to cover when creating a new agent. Ensures no critical information is missed during the research phase.

**agent-definition-schema.md**: Formal schema defining all sections, required content types, word counts, and validation criteria for complete agent definitions.

### assets/

*No assets required for this skill - output is markdown text files.*

### scripts/

*No scripts required - skill uses built-in tools (Read, Write, WebFetch, WebSearch).*

## Quality Standards

### Agent Prompt Quality

**Length**: 1,200-1,500 words minimum

**Required Sections** (all must be present):
- Agent Identity (name, domain, responsibility, triggers)
- Core Capabilities (3-4 categories with tools and patterns)
- Technology Stack (versions, tools, dependencies, docs)
- Standard Operating Procedures (3+ SOPs with commands)
- Best Practices (DO/DON'T lists)
- Workflow Position (7-Phase TDD integration)
- Integration Points (handoff sources/targets)
- Security Considerations (secrets, access control, vulnerabilities)
- Handoff Protocol (incoming/outgoing formats)
- Tool Inventory (MCP tools, CLI tools, file ops)
- Error Handling (common failures, retry strategy, escalation)
- Quality Checklist (pre-completion verification)
- Example Workflows (2-3 complete scenarios)
- Tool Installation (commands for all tools)

**Content Standards**:
- No placeholders - all sections filled with concrete content
- Real commands with expected output (not generic descriptions)
- Specific version numbers (not "latest")
- Actual error messages with resolutions
- Working code examples (curl commands, YAML configs)

### Reference Documentation Quality

**Length**: 600-800 words per document (3 docs total: 1,800-2,400 words)

**Content Standards**:
- Concrete examples (not theoretical concepts)
- Real commands that can be copied and executed
- Expected output shown for all commands
- Error messages with exact text and resolutions
- Version-specific details where relevant

## Example Output Structure

```markdown
.claude/agents/grafana-agent.md         # Main agent prompt (1,200-1,500 words)
docs/agents/grafana-agent/
└── ref-docs/
    ├── grafana-best-practices.md       # Best practices (600-800 words)
    ├── grafana-api-reference.md        # API/CLI reference (600-800 words)
    └── grafana-troubleshooting.md      # Troubleshooting (600-800 words)
```

## Integration with Agentic Workflow

**Trigger Keywords** (from Traycer):
- "create an agent for [technology]"
- "make me a [technology] agent"
- "build an agent to manage [technology]"
- "need an agent for [platform]"

**Linear Workflow**:
- Used by Planning Agent when infrastructure agent needed
- Not typically invoked by other specialized agents
- Creates deliverables (agent files) but doesn't update Linear directly

**Handoff Protocol**:
- Receives: User request from Traycer (conversational)
- Produces: Agent prompt + reference docs (file artifacts)
- Reports: Completion to Traycer with file paths

## Common Pitfalls

**Pitfall 1: Placeholder Content**
- **Symptom**: Agent prompt contains `[command]`, `[description]`, `[TODO]`
- **Impact**: Agent is unusable - lacks actionable guidance
- **Solution**: Research thoroughly BEFORE writing, fill ALL sections with concrete examples

**Pitfall 2: Generic Descriptions**
- **Symptom**: SOPs say "run appropriate commands" instead of showing actual commands
- **Impact**: Agent doesn't know what to do
- **Solution**: Include full curl commands, config files, expected output

**Pitfall 3: Outdated Version Info**
- **Symptom**: References Grafana 9.x when current is 11.x
- **Impact**: Syntax errors, deprecated APIs, broken examples
- **Solution**: Check official docs for latest stable version FIRST

**Pitfall 4: Missing Linear MCP Filtering**
- **Symptom**: Agent uses `list_issues()` without project filter
- **Impact**: Sees ALL issues from ALL teams (cross-contamination)
- **Solution**: Always include project filtering code example in agent prompt

**Pitfall 5: Vague Retry Strategy**
- **Symptom**: "Retry on network errors" without timing details
- **Impact**: Agent retries indefinitely or escalates prematurely
- **Solution**: Specify exact backoff timings (2s, 4s, 8s) and escalation triggers

**Pitfall 6: No Security Section**
- **Symptom**: Agent prompt lacks secrets management guidance
- **Impact**: Hardcoded secrets in configs, security vulnerabilities
- **Solution**: Always include secrets, access control, and vulnerability sections

## Validation Checklist

Before marking agent complete, verify:

- [ ] Agent prompt is 1,200-1,500 words with ALL sections filled
- [ ] Each of 3 reference docs is 600-800 words with concrete examples
- [ ] SOPs have step-by-step commands (not placeholders like `[command]`)
- [ ] API examples include full curl commands and expected JSON responses
- [ ] Security section covers secrets, access control, common vulnerabilities
- [ ] Retry strategy specifies exact backoff timings and escalation triggers
- [ ] Linear integration includes MCP tool names and project filtering code
- [ ] 7-Phase workflow position is clear with specific handoff agents
- [ ] Quality checklist includes security scan requirement
- [ ] Example workflows show complete command sequences with output
- [ ] Tool installation section has actual commands for all tools
- [ ] Error handling covers 4+ common failures with resolutions
- [ ] Technology stack specifies exact version numbers (not "latest")
- [ ] Reference docs saved in correct directory structure
- [ ] All file paths use repo-relative paths (no user-specific absolute paths)

## Technical Notes

**Tool Requirements**:
- **WebFetch** - Required for fetching official documentation
- **WebSearch** - Required for finding community best practices
- **Read** - For reading existing agent files during updates
- **Write** - For creating agent prompt and reference docs
- **Glob** - For finding existing agent files

**No MCP servers required** - This skill uses built-in Claude Code tools only.

**Output Format**: All files are GitHub-flavored Markdown with YAML frontmatter (for agent prompts).

**File Naming Convention**:
- Agent prompt: `<technology>-agent.md` (lowercase with hyphens)
- Reference docs: `<technology>-<topic>.md` (e.g., `grafana-best-practices.md`)

**Target Audience**: The agent prompts are written for Claude instances (not humans), so use imperative/infinitive form ("Create dashboard", "Test connection") rather than second person ("You should create").
