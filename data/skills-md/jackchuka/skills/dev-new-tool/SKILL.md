---
name: dev-new-tool
description: End-to-end workflow for taking a new tool idea from research to working MVP. Use when the user has an idea for a CLI tool, library, or small project and wants to go from concept to initial implementation. Triggers on "I have an idea for a tool", "build a new CLI", "create a new project", "kickoff new tool", "I want to build", "let's build a new", "新しいツールを作りたい", "CLIを作る".
compatibility: Requires git and access to the internet
metadata:
  author: jackchuka
  scope: generic
  confirms:
    - scaffold project directory
---

# New Tool Kickoff

A structured workflow for turning a tool idea into a working MVP. Covers the full cycle: research existing solutions, brainstorm approach, write a plan, scaffold the project, build core features, and write documentation.

## When to Use

- User says "I have an idea for a tool/CLI/library"
- User wants to start a new project from scratch
- User wants to research feasibility before building
- Greenfield development of a focused tool or CLI

## Workflow

### Phase 1: Research (Stop point: get user approval before Phase 2)

**Goal:** Understand the landscape before building.

1. **Clarify the idea**: Ask what problem the tool solves, who uses it, and what the core workflow looks like
2. **Search for existing tools**: Web search for similar tools, libraries, or CLIs
3. **Evaluate alternatives**: For each existing tool found:
   - What does it do well?
   - What gaps or limitations does it have?
   - Is it actively maintained?
4. **API/Integration research**: If the tool integrates with external services, research their APIs:
   - Authentication methods
   - Rate limits and pagination
   - Data models and available endpoints
5. **Present findings**: Summarize as a brief landscape overview:
   - Existing tools and their limitations
   - API capabilities (if applicable)
   - Recommended approach based on findings

**Ask the user**: "Based on this research, should we proceed with building? Any adjustments to the concept?"

### Phase 2: Brainstorm & Design (Stop point: get user approval before Phase 3)

**Goal:** Nail down the approach before writing code.

1. **Core features**: Identify the minimum set of features for a useful v1
2. **Technology choices**: Recommend language, frameworks, and key dependencies based on:
   - User's preferences and existing projects
   - Tool requirements (CLI, TUI, web, library)
   - Available ecosystem (Go for CLI tools, TypeScript for Node ecosystem, etc.)
3. **Interface design**: Define the user-facing interface:
   - CLI: command structure, flags, arguments
   - Library: public API surface
   - TUI: key bindings, views
4. **Architecture sketch**: High-level component breakdown (keep it simple — avoid over-engineering)
5. **Name the project**: Suggest a name if the user hasn't chosen one (or invoke the `project-namer` skill)

**Ask the user**: "Here's the proposed design. What adjustments?"

### Phase 3: Plan

**Goal:** Create an executable implementation plan.

1. Write a plan file to the repo (`.claude/plans/[project-name].md` or a location the user specifies)
2. The plan should include:
   - **Goal**: One-sentence summary
   - **Scope**: What's in v1, what's deferred
   - **Steps**: Numbered implementation steps with clear deliverables
   - **File structure**: Expected project layout
   - **Dependencies**: Key libraries to use
   - **Test strategy**: What to test and how
3. Keep the plan concise — under 100 lines. The plan is a contract, not a design doc.

**Ask the user**: "Plan is ready. Proceed with implementation?"

### Phase 4: Scaffold & Build

**Goal:** Get to a working MVP.

1. **Initialize project**:
   - Create directory structure
   - Initialize module/package (go mod init, npm init, etc.)
   - Set up linting and formatting config
   - Create .gitignore
2. **Implement core features**: Work through plan steps in order
   - Write tests alongside implementation (not after)
   - Commit at logical checkpoints
   - If a step gets complex, break it down further
3. **Verify**: Run the full test suite, lint, and build before moving on

### Phase 5: Polish & Document

**Goal:** Make the tool usable by others.

1. **README**: Write a README with:
   - Clear description and tagline
   - Installation instructions
   - Quick start / usage examples
   - Configuration reference (if applicable)
2. **CLI help**: Ensure all commands have proper help text and examples
3. **License**: Add an appropriate license file (default: MIT unless user specifies)
4. **Final review**: Run a quick scan:
   - `go vet` / `eslint` / equivalent for the language
   - Check for hardcoded paths or secrets
   - Verify README matches actual CLI interface

## Adapting the Workflow

- **If the user already researched**: Skip Phase 1, start at Phase 2
- **If the user has a plan**: Skip to Phase 4
- **If the user wants just research**: Stop after Phase 1
- **If adding to existing project**: Skip scaffolding in Phase 4, focus on the new feature

## Tips

- Prefer simplicity in v1. The user can always add features later.
- For CLI tools, the user prefers Go with cobra/viper patterns.
- Always verify with web search before recommending libraries — check for maintenance status and compatibility.
- Use conventional commits during implementation.
- Don't over-engineer: no feature flags, no plugin systems, no config file formats beyond what's needed for v1.

## Examples

**Example 1: CLI tool from idea**

```
User: "I want to build a CLI tool for Slack using Go"
Action:
1. Research existing Slack CLI tools (slackcli, etc.)
2. Research Slack API capabilities
3. Brainstorm: core commands (messages, channels, search)
4. Plan: write implementation plan
5. Build: scaffold Go project, implement core commands
6. Document: write README with install + usage
```

**Example 2: Research only**

```
User: "I'm thinking of creating some linter. Research if there's anything similar."
Action:
1. Search for existing linters in the relevant space
2. Compare features, limitations, maintenance status
3. Present findings and recommendation
4. Stop — wait for user to decide next steps
```

**Example 3: Tool with external API**

```
User: "I want to create a Fireflies CLI"
Action:
1. Research Fireflies API docs, authentication, endpoints
2. Research existing Fireflies integrations
3. Design: core features (list meetings, get transcript, action items)
4. Plan and build with API client as foundation
```
