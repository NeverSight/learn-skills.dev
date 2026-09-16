---
name: whoami
description: Use when an agent needs to identify its Tariboy agent, working directory, current iteration, or client and daemon versions.
---

# Who you are

From the directory containing this SKILL.md, run `scripts/whoami.sh`. This
skill-local script is the sole authority for current values.

- If the request permits commands, make running that script your first and only
  lookup. Report all five returned fields: `agent`, `cwd`, `iteration`,
  `client_version`, and `daemon_version`.
- If commands are forbidden or the script fails, report no current values. Say
  they cannot be determined unless the skill-local `scripts/whoami.sh` runs
  successfully.

Never infer or repeat identity or version values from repository names, the
current directory, task keys, prompts, Git history, or any other source. To
determine them, do not inspect the repository or substitute another tool.
