---
name: hap-help
description: Explain Hapstack setup, hap-mode routing, skills, playbooks, principles,
  prerequisites, and host-specific invocation. Use for hap-help or questions about
  using Hapstack.
license: MIT
---

# Hapstack help

Read the [package README](https://github.com/hapwi/hapstack/blob/main/README.md) and [runtime contract](../hap-mode/references/runtime.md). Answer the user's specific question with the relevant installed file; read it before describing its rules. Do not run a workflow merely because you are explaining it.

- Setup and model/budget preferences: [setup-hapstack](../setup-hapstack/SKILL.md) and its configuration reference.
- Task routing: [hap-mode](../hap-mode/SKILL.md). Patch-to-score and shipping route to patcher and ship, overriding generic playbook triggers.
- Understanding: how, why, teach, recall, ketchup, in-your-own-words.
- Design and review: architect, arena, swarm, interrogate, blast-radius.
- Verification: tdd, benchmark-checklist, create-verification-skill, maintain-verification-skill, control-ui, control-cli.
- Writing and code cleanup: unslop, bro, technical-writing, deslop, no-comments.
- Long work and learning: figure-it-out, show-me-your-work, reflect, correct, automate-me, make-bot-ui, and the orchestration/autonomy playbooks.
- Every skill and principle: [catalogue](https://github.com/hapwi/hapstack/blob/main/CATALOG.md). Detailed guidance: [guide](https://github.com/hapwi/hapstack/blob/main/docs/guide/README.md).

In Codex native plugins use `$hapstack:hap-mode` and `$hapstack:setup-hapstack`; linked standalone skills use `$hap-mode` and `$setup-hapstack`. Other hosts use their documented slash or plugin-qualified form. T3 consumes provider-discovered skills and supplies its existing MCP tools; Hapstack itself ships no MCP server. Host discovery and persistent custom modes vary. If a picker omits a skill, verify the actual installation path or explicitly point the agent to its file.

No configuration is required: current-model roles, on-request delegation, existing tooling, and project-defined versioning are defaults. Setup changes those preferences without activating jobs or granting external-write authority. There is no fixed Grok/Claude requirement. Deslop and host control adapters are bundled; private built-ins are not prerequisites.

For an unavailable browser, delegation, scheduler, history source, forge, or score service, report the specific limitation and a supported next step. Never advertise unperformed discovery, a nonexistent tool, or an unverified 100/100. Link the relevant public file under the repository from plugin.json, not a private cache path.

