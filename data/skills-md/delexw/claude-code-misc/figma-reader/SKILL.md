---
name: figma-reader
description: Read Figma designs via Figma MCP server. Auto-detects MCP availability and prompts user only if setup is needed. Use when Figma links or UI design images are found in task context.
agent: general-purpose
model: sonnet
argument-hint: Figma link or design prompt [OUT_DIR] (e.g. "https://www.figma.com/design/..." ./out)
allowed-tools: Read, Bash, Write, Edit, mcp__figma__*
context: fork
---

# Figma Reader

Read Figma design context via the Figma MCP server.

## Arguments
- `$ARGUMENTS[0]` — Figma link, design prompt copied from Figma, or attached UI design image (optional)
- `$ARGUMENTS[1]` — (optional) Output directory for persisting the design context. Defaults to `.implement-assets/figma`

When invoked by the orchestrator (e.g. `implement`), `$ARGUMENTS[1]` is provided. When used standalone, it defaults to `.implement-assets/figma`.

## Execution

1. **Codebase check**: Verify this is a frontend project — follow [references/rules.md](references/rules.md) Codebase Check. If not frontend, skip the entire skill.
2. **Pre-flight check**: Use `ToolSearch` to detect if Figma MCP tools are available — follow [references/rules.md](references/rules.md)
3. If MCP is not available, use `AskUserQuestion` to guide setup or allow skip
4. **Resolve design input**:
   - If `$ARGUMENTS[0]` contains a valid Figma link or prompt → use it directly
   - If `$ARGUMENTS[0]` is an attached UI image → show it for context, then use `AskUserQuestion` to ask the user to select the relevant component in Figma (see [references/rules.md](references/rules.md) Design Input)
   - If `$ARGUMENTS[0]` is empty or not provided → use `AskUserQuestion` to ask user (see [references/rules.md](references/rules.md) Design Input)
5. **Read design**: Use the Figma MCP tools to read the design from the Figma link resolved in step 4
   - Format the output per [references/output-format.md](references/output-format.md)
   - **Save output**: Run `mkdir -p $ARGUMENTS[1]` via Bash, then save the full formatted output to `$ARGUMENTS[1]/output.md` using the Write tool

<tags>
   <mode>think</mode>
   <custom>yes</custom>
</tags>
