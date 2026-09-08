---
name: agentuse
description: AgentUse CLI and agent workflow guide. Use when the user mentions "agentuse", ".agentuse", "agentuse skills", "run an agent", "list agents", "agent sessions", "agentuse serve", creating or managing AgentUse agents, or wants to inspect/run/schedule AgentUse workflows. Always load the current builtin core instructions from the installed CLI before non-trivial AgentUse work.
hidden: true
---

# AgentUse

This is a discovery stub, not the usage guide. The CLI serves builtin skill
content matched to the installed version, so load that before non-trivial work:

```bash
agentuse skills get core [--full]   # start here
```

Before creating, editing, reviewing, or debugging any `.agentuse` file, load
both authoring guides:

```bash
agentuse skills get core --full
agentuse skills get creator --full
```

`core` routes to the specialized builtin skills:

```bash
agentuse skills get runner          # run, list, sessions, serve, schedules
agentuse skills get creator         # author and improve .agentuse files
agentuse skills get onboarding      # guided first agent from terminal or Web UI
agentuse skills installed           # inspect project/user skills
```

For first-run setup, prefer the explicit cross-environment entrypoint:

```bash
agentuse setup                      # choose Browser or Terminal interactively
agentuse setup --web                # guided Web UI; prints the URL if no browser is available
agentuse setup --terminal           # guided terminal flow
agentuse setup --terminal --yes     # create the default managed project, my-agents
```

`agentuse setup` does not treat the shell's current directory as a project. Its
managed projects live beside the user config under `projects/`, unless an
existing project has already been configured.

Keep this stub small and stable; the authoritative instructions live in the CLI.
