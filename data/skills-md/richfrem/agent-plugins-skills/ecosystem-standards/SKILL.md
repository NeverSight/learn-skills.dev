---
name: ecosystem-standards
description: Provides active execution protocols to rigorously audit how code, directory structures, and agent actions comply with the authoritative ecosystem specs. Trigger when validating new skills, plugins, or workflows.
disable-model-invocation: false
allowed-tools: Bash, Read, Write
dependencies: ["skill:ecosystem-authoritative-sources"]
---
# Ecosystem Standards Review Protocol

This skill details how to perform an audit on new or existing capabilities (Skills, Plugins, Workflows, Sub-Agents, and Hooks) against authoritative ecosystem specifications to ensure they are created, installed, and structured correctly.

## Instructions
When invoked to review a codebase component or a planned extension:

1.  **Identify the Component Type**: Determine if the subject is a Plugin boundary, an Agent Skill, an Antigravity Workflow/Rule, a Sub-Agent, or a Hook.
2.  **Recall the Specs**: Before reviewing, read the relevant specification file found in the `ecosystem-authoritative-sources` skill library.
    *   *Path:* `../../references/*.md`
3.  **Perform Rigorous Audit**:
    *   **Structure**: Does the directory schema match the standard (`.claude-plugin/plugin.json`, `my-skill/SKILL.md`)? Are all supporting files strictly organized into the official optional directories (`scripts/`, `references/`, `assets/`) rather than cluttering the skill root?
    *   **Manifest Schema**: Does `plugin.json` follow the authoritative schema? Check:
        - `name` is kebab-case (lowercase, hyphens, no spaces)
        - `version` uses semver (e.g., `0.1.0`, not `1.0`)
        - `author` is an object `{"name": "..."}`, NOT a string
        - No `author.url` field (not in spec)
        - No `commands_dir` or `skills_dir` fields (auto-discovered)
        - `skills`, `agents`, `hooks`, `commands`, `scripts`, `dependencies` arrays are documentation-only (ignored by runtime, OK to keep for human readability)
        - See `references/plugins.md` in `ecosystem-authoritative-sources` for the full schema
    *   **Naming**: Verify the skill name uses the **gerund form** (`verb + -ing`, e.g., `analyzing-spreadsheets`). Reject generic nouns. Ensure the `name` is 1-64 lowercase alphanumeric chars/hyphens only, contains NO consecutive hyphens (`--`), and EXACTLY matches the parent directory name.
    *   **Content**: Does the YAML frontmatter adhere precisely to rules (`description` 1-1024 chars, `compatibility` max 500 chars, `metadata` strictly string-to-string keys/values)? Provide the recommendation to run `skills-ref validate ./my-skill` to definitively catch parse errors.
    *   **Description Viewpoint**: Ensure the `description` is written strictly in the **third person** ("Extracts text", not "I extract text") and isn't overly vague.
    *   **Progressive Disclosure**: For Skills, is the `SKILL.md` file appropriately constrained (< 500 lines) with extraneous detail pushed to one-level deep reference files? **Reject deeply nested reference chains**.
    *   **Reference Paths**: Verify that all file references are strictly relative to the skill's root (e.g., `scripts/extract.py`), avoiding absolute paths outside the plugin boundaries.
    *   **Reference Readability**: Do reference files >100 lines contain a Table of Contents for partial-read navigation?
    *   **Script Quality**: Verify python utility scripts do **not** punt errors back to the LLM (e.g., failing silently), but instead handle exceptions safely or emit clear `stderr` messages. Ensure they don't use undocumented "magic numbers" (voodoo constants).
    *   **Multi-CLI Support**: When integrating agent CLI plugins, support exists for `claude-cli`, `gemini-cli`, and `copilot-cli`. Plugins must reflect the native CLI syntax in their system files.
    *   **Anti-Patterns**: Check for hardcoded credentials and Windows style paths (`\`).
    *   **Connector Abstraction**: If the plugin uses MCP tools, does it include a `CONNECTORS.md` using the `~~category` abstraction pattern instead of hardcoding specific tool names? This is required for portability. Ensure all native tool calls use the fully qualified `ServerName:tool_name` format.
    *   **Interaction Design Quality**: For skills with user interaction, verify they use appropriate patterns:
        - Discovery phases use progressive questioning (broad → specific), not question walls
        - Decision points offer numbered option menus (3-7 items max)
        - Expensive operations have confirmation gates
        - Multi-step workflows include inline copyable **checklists**.
        - Skills end with next-action menus, not dead ends
        - Workflows taking long documents gracefully degrade using Document Format Agnosticism.
    *   **Execution Safety (Plan-Validate-Execute)**: Do destructive or massive workflows mandate an intermediate verifiable plan file (e.g., `changes.json`) before execution?
    *   **Dual-Mode Architecture**: If the skill both creates new artifacts AND improves existing ones, verify it implements the Bootstrap + Iteration dual-mode pattern with separate sections and trigger phrases.
    *   **Output Templates**: If the skill generates reports or artifacts, verify it either defines an output template or negotiates the format with the user.
    *   **Escalation and Safety**: Workflows with external risk must explicitly implement Graduated Autonomy Routing and Escalation Trigger Taxonomies rather than blanket-stopping on all issues.
    *   **Source Transparency**: Data synthesis output MUST conclude with explicit `Sources Checked` and `Sources Unavailable` blocks.
4.  **Produce Feedback**: Provide explicit, granular feedback outlining exactly which ecosystem constraints were violated and concrete suggestions for fixing them. Ensure your feedback is actionable.
