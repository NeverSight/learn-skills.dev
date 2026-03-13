---
name: custom-agent-usage
description: Discover, validate, and invoke .agent.md custom agents. Use when finding agent files in the local Claude or VS Code Insiders directories, checking frontmatter, verifying disable-model-invocation, or determining agentName for runSubagent calls.
license: Complete terms in LICENSE.txt
---

# Custom Agent Usage

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

Activate this skill when:
- Discovering available custom agents from the local Claude or VS Code Insiders agent directories
- Understanding `.agent.md` file structure and frontmatter
- Checking if an agent can be invoked as a subagent
- Learning which `agentName` to use for delegation
- Understanding agent tools and capabilities

## Custom Agent Discovery

Custom agents for this environment are discovered from these directories:
- Claude agents: `C:\Users\LOQ\.claude\agents`
- VS Code Insiders prompts: `C:\Users\LOQ\AppData\Roaming\Code - Insiders\User\prompts`

Notes:
- Filter to `*.agent.md` when discovering subagents.
- The VS Code Insiders prompts directory can also contain `.prompt.md` and `.instructions.md` files that are not subagents.

**To discover agents:**
1. Search for `*.agent.md` files in the configured Claude and VS Code Insiders directories.
2. Read frontmatter of each agent file to understand capabilities.
3. Ignore `.prompt.md` and `.instructions.md` files when the goal is subagent delegation.

## Agent Frontmatter

Key frontmatter fields in `.agent.md`:

| Field | Purpose | Required? |
|--------|-----------|-----------|
| `name` | Display name used in `agentName` parameter | Recommended |
| `description` | What the agent specializes in | Recommended |
| `tools` | Tools available to the agent | Optional |
| `disable-model-invocation` | If false, agent can be invoked as subagent | Required |

## Invocability Check

**CRITICAL**: Only agents with `disable-model-invocation: false` in frontmatter can be invoked as subagents.

Check frontmatter:
```yaml
---
name: "Code Explainer"
description: For analyzing and documenting existing code
disable-model-invocation: false  # Must be false for subagent delegation
tools: [Read, Search]
---
```

## Using Custom Agents

### Step 1: Discover Available Agents

Search the real agent directories and keep only `*.agent.md` files:
```powershell
Get-ChildItem `
  'C:\Users\LOQ\.claude\agents', `
  'C:\Users\LOQ\AppData\Roaming\Code - Insiders\User\prompts' `
  -Filter *.agent.md `
  -File
```

Or use the helper script:
```powershell
node .\scripts\agent-finder.js
```

### Step 2: Check Invocability

Verify `disable-model-invocation: false` is set.

### Step 3: Get Agent Name

Use the `name` field from frontmatter exactly as is.
- If frontmatter has `name` field value, use that value in quotes.
- If name is not specified, use the filename without the `.agent.md` extension.

### Step 4: Delegate Task

```javascript
runSubagent({
  agentName: "Playwright Tester Mode",  // Must match 'name' from frontmatter exactly
  description: "Test checkout flow",
  prompt: "Perform exploratory testing on the checkout flow: product selection -> cart -> payment confirmation. Generate comprehensive Playwright tests covering success scenarios, validation errors, edge cases (empty cart, payment failures), and accessibility."
})
```

## Workflow Example

```javascript
// Step 1: Main agent analyzes task and identifies need for testing
// "I need comprehensive testing for the checkout flow"

// Step 2: Discover custom testing agent
// Found: C:\Users\LOQ\.claude\agents\playwright-tester.agent.md
// disable-model-invocation: false and name: "Playwright Tester Mode"

// Step 3: Delegate to custom agent
runSubagent({
  agentName: "Playwright Tester Mode",
  description: "Test checkout flow",
  prompt: "Perform exploratory testing on the checkout flow: product selection -> cart -> payment confirmation. Generate comprehensive Playwright tests covering success scenarios, validation errors, edge cases (empty cart, payment failures), and accessibility."
})

// Step 4: Review test output and integrate into test suite
```

## Examples & Scripts

- [Agent Discovery Workflow](./examples/agent-discovery-workflow.md) - Examples of finding and using custom agents
- [Agent Finder Script](./scripts/agent-finder.js) - Node.js script to discover and inspect custom agents

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [agent-task-mapping](../agent-task-mapping/SKILL.md) | Map tasks to agents after discovering available agents |
| [subagent-delegation](../subagent-delegation/SKILL.md) | Delegation patterns after validating agent invocability |