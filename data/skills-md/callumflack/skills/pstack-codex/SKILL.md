---
name: pstack-codex
description: "Codex compatibility layer for pstack. Must be used alongside any pstack-provided skill in Codex, including Poteto Mode, setup-pstack, architect, arena, how, why, interrogate, reflect, swarm, and pstack playbooks or principles. Translates Cursor Task, agent-type, model, and concurrency instructions into Codex collaboration-agent calls. Do not use in Cursor."
---

# Pstack for Codex

Use the selected pstack skill and this adapter together. Pstack owns the workflow; this skill owns only the Codex execution translation. State once in commentary that both are active so the user can see the adapter was selected.

Do not edit pstack, reinterpret its playbook, or read Cursor model slugs as Codex model slugs. Leave `~/.cursor/rules/pstack-models.mdc` to Cursor.

## Thread-scoped Poteto mode

Codex does not implement pstack's `mode: true` metadata. Install the compatibility hook once:

```sh
python3 ~/.agents/skills/pstack-codex/scripts/poteto-session-mode.py install
```

The installer adds one `UserPromptSubmit` hook without replacing unrelated hooks. After installation, `/poteto-mode` or an explicit `$poteto-mode` skill invocation activates Poteto for that Codex thread. Later prompts in the same thread reload Poteto and this adapter. Other threads remain unchanged. `/poteto-mode off` deactivates it only for the current thread.

The hook names the stable personal-plugin route at `~/plugins/pstack/skills/poteto-mode/SKILL.md`. Read Poteto from that route. Do not fall back to the removed flat-registry path at `~/.agents/skills/poteto-mode/SKILL.md`.

The hook stores `active` or `inactive` by Codex session ID. Keep the inactive state. Earlier injected context remains in the transcript, so deleting state cannot reliably opt out.

## Model routing

Use the current Codex collaboration tool's declared model and reasoning-effort values. Verify a configured model before every spawn. If it is unavailable, omit the model override and inherit the parent; never invent or translate an unconfirmed slug.

| Pstack role | Codex model | Reasoning effort |
| --- | --- | --- |
| feature, refactoring | `gpt-6.1-sol` | `high` |
| bug-fix, perf-issue, hillclimb | `gpt-6.1-sol` | `high` |
| hardest tasks | `gpt-6.1-sol` | `xhigh` |
| judgment, architecture review | `gpt-6-astra` | `high` |
| prose, how explainer, why synthesizer | `gpt-6.1-sol` | `high` |
| how explorer, why investigators, swarm workers | `gpt-6-luna` | `high` |
| reflect tooling | `gpt-6.1-sol` | `high` |
| reflect judgment, divergent, synthesizer | `gpt-6-astra` | `high` |

Use the hardest-tasks row for subtle concurrency or cross-cutting implementation. Reserve `max` for a difficult unresolved problem or an explicitly exhaustive review.

For how critics, arena runners, architect runners, interrogate reviewers, and other pstack panels, preserve the requested logical panel length using this ordered pool. Cycle through it when more seats are requested:

1. `gpt-6.1-sol` at `high`
2. `gpt-6-astra` at `high`
3. `gpt-6-luna` at `high`

Respect the collaboration tool's live concurrency limit. If the panel is larger than the available child slots, run rolling waves without shrinking the panel. For an arena cross-judge, prefer an available model from the pool that differs from the parent and the winning candidate's model.

## Tool translation

- Cursor `Task` call -> Codex `spawn_agent`.
- `subagent_type: poteto-agent` -> a `worker` told to read the installed `poteto-mode` skill completely before working.
- `subagent_type: generalPurpose` -> `explorer` for read-only codebase discovery, `worker` for owned implementation, otherwise `default`.
- `run_in_background: true` -> spawn the independent agents together; Codex agents already run asynchronously.
- `readonly: true` -> use an `explorer` when the task is codebase exploration; otherwise put the read-only boundary explicitly in the prompt.
- Cursor `environment: cloud|local` -> use Codex's available local agent environment. If the workflow genuinely requires a Cursor cloud agent, report that boundary instead of pretending it ran.
- Explicit model override -> set both `model` and `reasoning_effort`, and use `fork_turns: none` or a bounded positive turn count rather than full-history inheritance.

Workers share the filesystem. Give every worker explicit ownership, say that other agents may be editing concurrently, and isolate competing writes in separate worktrees or output directories as the pstack workflow requires.

## Precedence

The user's request and repository instructions remain authoritative. Keep pstack's workflow, panel membership, review separation, and verification gates intact; adapt only the Cursor-specific execution mechanics that Codex cannot perform literally.
