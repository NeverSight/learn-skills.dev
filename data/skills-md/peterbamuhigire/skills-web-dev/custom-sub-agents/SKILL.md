---
name: custom-sub-agents
description: "Guidance for creating and organizing custom sub-agents in local repos, including folder conventions, per-agent structure, and AGENTS.md indexing. Use when asked where to store sub-agents or how to document them."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Custom Sub-Agents Skill

## Overview

This skill defines the standards and workflow for creating, organizing, and documenting custom sub-agents (AI agents, code assistants, or workflow bots) within the BIRDC ERP project. It ensures that all sub-agents are discoverable, maintainable, and compatible with both GitHub Copilot and Claude in VS Code.

## Folder Structure

```
skills/
└── custom-sub-agents/
	 ├── SKILL.md                ← This skill file (standards, checklist)
	 ├── references/
	 │   └── CUSTOM_SUB_AGENTS_GUIDE.md  ← Reference guide
	 └── [agent folders]/        ← One folder per sub-agent
		  ├── agent-name/
		  │   ├── agent.js|php|py|ts  ← Agent implementation
		  │   ├── README.md           ← Agent documentation
		  │   └── ...
```

## Requirements

1. **One Folder per Sub-Agent**
   - Each sub-agent must have its own folder under `skills/custom-sub-agents/`.
   - Folder name: `agent-name` (kebab-case, descriptive).

2. **Documentation**
   - Each agent folder must include a `README.md` describing:
     - Agent purpose and capabilities
     - Usage instructions
     - Configuration (if any)
     - Example prompts or API calls

3. **Entry Point**
   - The main agent file must be named `agent.js`, `agent.php`, `agent.py`, or `agent.ts` as appropriate.
   - The entry file must export or define a function/class named after the agent (PascalCase).

4. **Reference Guide**
   - All sub-agents must be listed in `references/CUSTOM_SUB_AGENTS_GUIDE.md` with a summary and link to their folder.

5. **Compatibility**
   - Agents must be compatible with both GitHub Copilot and Claude (Anthropic) in VS Code.
   - Use only supported APIs and avoid proprietary features unless polyfilled.

6. **Testing**
   - Each agent must include a test or usage example in its README.md.

7. **Versioning**
   - Update this SKILL.md and the reference guide when adding, removing, or changing agents.

## Technical Implementation & Benefits

### File Naming Convention

- **GitHub Copilot**: Recognizes and auto-loads markdown files named `agent-name.agent.md`
- **Claude**: Compatible with standard markdown documentation
- **Auto-loading**: Context is automatically included in every conversation

### Context Window Optimization

- **Massive Efficiency Gains**: Tasks that consumed 80k+ tokens now use <4k tokens
- **Sustainable Development**: Enables complex, multi-step workflows without context bloat
- **Scalable Architecture**: Supports large projects with extensive requirements

### Implementation Ease

- **Self-Implementing**: Ask Copilot/Claude to create new sub-agents with desired functionality
- **Rapid Prototyping**: New agents can be created quickly with proper structure
- **Iterative Development**: Easy to enhance and modify existing agents

### Skills Integration

- **Enhanced Capabilities**: Combine sub-agents with specialized skills for domain expertise
- **Modular Architecture**: Mix and match agents and skills for specific workflows
- **Best Practice Patterns**: Leverage proven skill frameworks within agent implementations

### Use Case Optimization

- **Big Functional Prompts**: Most beneficial for complex feature development
- **Zero-to-POC Workflows**: Excellent for proof-of-concept and prototyping
- **Simple Fixes**: Consider single LLM for basic "fix that error" scenarios
- **Context-Aware Decisions**: Choose sub-agents when context conservation matters

## Codebase Analysis & Planning

### When to Use Sub-Agents vs Single LLM

**Ask the AI Agent to analyze your codebase:**

```
"Analyze my codebase and recommend where sub-agents would be most beneficial.
Consider: code complexity, domain areas, repetitive tasks, integration points,
and context window requirements. Tell me what agents I need, where they should
live, and how they should interact."
```

### Analysis Criteria

**Create Sub-Agents For:**

1. **Complex Domain Areas**
   - Multi-step workflows (authentication, payments, inventory)
   - Business logic with many edge cases
   - Integration with external APIs/services

2. **Repetitive Development Tasks**
   - Code generation patterns (CRUD operations, API endpoints)
   - Testing strategies for specific components
   - Documentation generation for modules

3. **Context-Intensive Work**
   - Large codebases requiring sustained context
   - Multi-file refactoring operations
   - Complex architectural decisions

4. **Specialized Expertise Areas**
   - Security implementations
   - Performance optimization
   - Database schema design
   - UI/UX pattern implementation

**Use Single LLM For:**

- Simple bug fixes and error resolution
- Code reviews of individual files
- Quick refactoring of small functions
- Basic code explanations

### Planning Your Sub-Agent Architecture

**Step 1: Codebase Analysis Prompt**

```
Analyze this codebase structure and identify:
- Key functional areas that could benefit from specialized agents
- Integration points that require consistent handling
- Repetitive patterns that could be automated
- Complex workflows that consume significant context
- Areas where domain expertise would improve outcomes
```

**Step 2: Agent Definition**
For each identified area, define:

- **Purpose**: What does this agent do?
- **Scope**: What files/code does it handle?
- **Inputs**: What information does it need?
- **Outputs**: What does it produce?
- **Interactions**: How does it work with other agents?

**Step 3: Implementation Planning**

- **File Structure**: Where will the agent live?
- **Dependencies**: What tools/utilities does it need?
- **Testing**: How will you validate the agent?
- **Documentation**: How will users discover and use it?

### Example Analysis Output

**Recommended Sub-Agents:**

1. **Database Migration Agent** (`database-migrations.agent.md`)
   - Handles schema changes, data migrations, rollback strategies
   - Location: `skills/custom-sub-agents/database-migrations/`

2. **API Development Agent** (`api-development.agent.md`)
   - Generates REST endpoints, validates requests, handles errors
   - Location: `skills/custom-sub-agents/api-development/`

3. **UI Component Agent** (`ui-components.agent.md`)
   - Creates reusable components, handles styling, ensures consistency
   - Location: `skills/custom-sub-agents/ui-components/`

### Integration Points

**Cross-Agent Communication:**

- Define clear interfaces between agents
- Establish data sharing protocols
- Create shared utilities and helpers
- Document agent dependencies and workflows

**Context Management:**

- Identify shared context requirements
- Plan for context handoffs between agents
- Optimize for minimal context overlap
- Design for resumable workflows

## VS Code Integration & Enforcement Checklist

- [ ] Register agent folder in `references/CUSTOM_SUB_AGENTS_GUIDE.md`
- [ ] Ensure agent entry file and README.md exist
- [ ] Confirm agent is discoverable by Copilot/Claude (test in VS Code)
- [ ] Add usage example in README.md
- [ ] **Enable sub-agent support in VS Code settings:**
  - Add the following to your `.vscode/settings.json`:

    ```json
    {
      "chat.customAgentInSubagent.enabled": true
    }
    ```

  - This setting is required for both GitHub Copilot and Claude to use custom sub-agents in the latest VS Code Insiders build.

## Example Agent Folder

```
skills/custom-sub-agents/
└── smart-approver/
	 ├── agent.js
	 ├── README.md
```

## See Also

- [references/CUSTOM_SUB_AGENTS_GUIDE.md](references/CUSTOM_SUB_AGENTS_GUIDE.md)

## Last Updated

30 January 2026
