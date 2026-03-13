---
name: create-sub-agent
description: Interactive initialization script that generates a compliant Sub-Agent configuration. Use when you need to create a nested contextual boundary with specific tools or persistent memory.
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---
# Sub-Agent Scaffold Generator

You are tasked with generating a new Sub-Agent context boundary using our deterministic backend scaffolding pipeline.

## Execution Steps:

1. **Gather Requirements:**
   Before proceeding, you MUST read:
   - `plugins reference/agent-scaffolders/references/hitl-interaction-design.md`
   - `plugins reference/agent-scaffolders/references/pattern-decision-matrix.md`
   
   Use these guides to ask the user for:
   - The name of the sub-agent.
   - The core purpose (to form the `description` and system prompt).
   - The escalation risk: does this agent need an Escalation Trigger Taxonomy explicitly defined in its prompt?
   - The trust posture: warn the user that all sub-agent return boundaries MUST end in a Source Transparency Declaration (Sources Checked/Unavailable).
   - Where the agent should be placed (`.claude/skills/` or within a plugin's `/agents/` folder).

2. **Scaffold the Sub-Agent:**
   You must execute the hidden deterministic `scaffold.py` script.
   
   Run the following bash command:
   ```bash
   python3 ./scripts/scaffold.py --type sub-agent --name <requested-name> --path <destination-directory> --desc "<core-purpose>"
   ```

3. **Confirmation:**
   Print a success message and advise the user on how to spawn the sub-agent (usually via the System `Task` tool).


## Next Actions
- Offer to run `audit-plugin` to validate the generated artifacts.
