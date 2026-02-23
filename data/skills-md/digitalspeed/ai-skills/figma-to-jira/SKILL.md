---
name: figma-to-jira
description: Orchestrates Jira ticket creation from Figma designs using Atomic Design principles. Use this when initializing a project or syncing design specs to Jira for development.
author: DigitalSpeed
---

# Figma to Jira

You are an expert Technical Product Manager. Your goal is to translate Figma designs into a lean, interconnected Jira backlog using pre-configured MCP servers.

**IMPORTANT:** All Figma and Jira operations use MCP tools (provided by the `figma` and `jira` MCP servers). You MUST call these tools directly in the main conversation. Do NOT delegate MCP operations to subagents — subagents cannot access MCP tools and will fail. Do NOT use Bash to re-parse MCP tool result files from disk — read and use MCP responses directly in context as they are returned.

## 1. Quick Start

Create a project directory, install the skill, and configure your MCP servers and project defaults:

```bash
mkdir my-project && cd my-project
npx skills add digitalspeed/ai-skills --skill figma-to-jira
```

Set up `.mcp.json` with both MCP servers:

```json
{
  "mcpServers": {
    "figma": {
      "type": "http",
      "url": "https://mcp.figma.com/mcp"
    },
    "jira": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-atlassian@latest"],
      "env": {
        "JIRA_URL": "https://your-instance.atlassian.net",
        "JIRA_USERNAME": "you@digitalspeed.com",
        "JIRA_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

- **Jira** requires an API token. Generate one at: https://id.atlassian.com/manage-profile/security/api-tokens

Set up `CLAUDE.md` with your project defaults:

```markdown
## Project Config
- Figma: https://www.figma.com/design/abc123/My-App?node-id=0-1
- Jira project key: ALPHA
```

Start Claude Code and authenticate the Figma MCP server:

```
claude
> /mcp
```

Select the **figma** server → **Authenticate** → a browser window will open for Figma OAuth. Once authenticated, add the following to your `CLAUDE.md` to pre-approve MCP tools so the skill runs without confirmation prompts:

```markdown
## Allowed Tools
- mcp__figma__*
- mcp__jira__*
```

Add the following to your `CLAUDE.md` to pre-approve all tools the skill uses, so it runs without confirmation prompts:

```markdown
## Allowed Tools
- mcp__figma__*
- mcp__jira__*
- Bash(python3:*)
```

Then invoke the skill:

```
> Use @figma-to-jira
```

## 2. Inputs

Both MCP servers must be connected **before** invocation. If either server is unavailable, stop and direct the user to complete the Quick Start setup above.

The skill requires a Figma file URL and Jira project key. Check the conversation context and `CLAUDE.md` for these values first. Only ask the user interactively if they are not found:

| Input | Example | Required |
|---|---|---|
| **Figma file URL** | `https://www.figma.com/design/abc123/My-App?node-id=0-1` | Yes |
| **Jira project key** | `ALPHA` | Yes |

## 3. The "Organism" Constraint

Follow Atomic Design principles but **do not** create tickets for anything below the **Organism** level.

- Ignore Atoms and Molecules as standalone tickets.
- Group related components into a single Task.
- Create a dedicated Epic for global elements (e.g. "Epic: Global Components") and add a Task for each one (Header, Footer, Navigation, etc.). These are shared across pages and must be tracked.

## 4. Hierarchy & Mapping Logic

Structure the backlog using this mapping:

- **Epic:** One Epic per Figma Page / screen (e.g., "Epic: Contact Us Page").
- **Task:** One Task per major Section or Organism within that page.
- **Sub-task:** A separate Jira issue (issue type: Sub-task) under a Task, covering a distinct functional or technical implementation detail.

**Sub-tasks must be created as actual Jira sub-task issues** using the Jira MCP `create_issue` tool with the sub-task issue type and a parent link to the Task. Do NOT list sub-tasks inline in the Task description — each one must be its own trackable Jira issue.

Keep ticket counts minimal. Prefer high information density within each ticket over a high volume of granular tickets.

## 5. Execution Workflow

Execute this skill in three phases. **Stop and wait for user confirmation between each phase.**

### Phase 1: Analyze Figma Structure

Use the Figma MCP tools directly (do not delegate to subagents):

1. Call the Figma MCP `get_file` or equivalent tool with the Figma file URL to list all pages and top-level frames.
2. For each page, call `get_screenshot` on the top-level frame to capture a visual reference.
3. Present the user with a proposed backlog structure:
   - List each page → proposed Epic name. Every page must have an Epic — do not omit any.
   - Under each Epic, list the major sections/organisms → proposed Tasks

**Stop here and ask the user to confirm or adjust the proposed structure before creating any Jira tickets.**

### Phase 2: Create Jira Tickets

Once the user approves the structure, create tickets using the Jira MCP tools directly:

**Before creating any Epic or Task**, search the Jira project for existing issues with the same name (use `search_issues` or equivalent). If a matching issue already exists for that page or section, skip creation and reuse the existing issue key. Never create duplicate tickets.

1. Create each **Epic** (one per confirmed page/screen), after confirming no duplicate exists.
2. Create each **Task** under its parent Epic (one per major section/organism), after confirming no duplicate exists.
3. Create each **Sub-task** as a separate Jira issue (issue type: Sub-task) with a parent link to its Task. Do NOT embed sub-tasks as text in the Task description.
**Attaching screenshots to tickets:** `get_screenshot` returns base64 image data — it cannot be passed directly to Jira. To attach a screenshot to any Epic or Task:
   1. Call `get_screenshot` (use `type: "jpeg"` to avoid MIME type issues).
   2. Use a `python3` Bash command to decode the base64 and write it to a temp file, e.g. `/tmp/figma-<nodeId>.jpg`.
   3. Call `jira_update_issue` with `attachments: "/tmp/figma-<nodeId>.jpg"` to upload the file.
   4. Delete the temp file after upload.

   Example python3 command:
   ```
   python3 -c "import base64; open('/tmp/figma-NODE_ID.jpg','wb').write(base64.b64decode('BASE64_DATA'))"
   ```

4. For **Epics**:
   - Place the direct Figma node URL prominently at the top of the description.
   - Attach a screenshot using the steps above.
   - Use wiki-link referencing to connect related tickets (e.g., `[[ALPHA-12]]` depends on this layout).
   - Do NOT call `get_design_context` for Epics — they are grouping containers, not implementation specs.
5. For **Tasks**: after calling `get_metadata`, always call `get_design_context` on the same node. Attach a screenshot using the steps above. Extract and embed the following into the Task description so a developer or implementation agent can build from the ticket alone, without Figma access:
   - Layout: dimensions, spacing, padding, alignment
   - Typography: font family, size, weight, line height for each text element
   - Colours: fills, borders, and background values (hex or design token name)
   - Component variants and states (hover, active, disabled, empty, error)
   - Responsive or breakpoint behaviour if present
   - Any interaction notes (e.g. scroll behaviour, sticky positioning)

   Format this as a **Design Spec** section in the Task description, below the Figma URL. Keep it factual and structured — do not paraphrase or summarise away concrete values.
6. For **Sub-tasks**, use the following description format:

   ```
   [Figma node URL]

   [What this sub-task implements — concrete, verifiable details.]

   ## Acceptance Criteria
   - [ ] [Criterion 1: observable behaviour or state that can be verified during UAT]
   - [ ] [Criterion 2: ...]
   ```

   Write acceptance criteria as checkboxes that a QA tester can verify without referencing the Figma file. Each criterion should describe a visible outcome, interaction, or content requirement.

### Phase 3: Summary

After all tickets are created, present the user with:

- Total Epics, Tasks, and Sub-tasks created.
- A list of Epic names with their Jira keys.
- A **Flags & Risks** section (if any) listing implementation concerns, placeholder content, or unresolved questions that need attention before or during development. This is for risks only — do not use it to report skipped design elements.
