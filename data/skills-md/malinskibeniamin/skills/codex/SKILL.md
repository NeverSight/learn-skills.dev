---
name: codex
description: Delegate to GPT-5.6 through the Codex CLI. Use for clear-spec implementation, independent review, computer use, investigation, data analysis, or token-heavy mechanical work.
---

**Host gate:** Claude-hosted only. In native Codex, work inline unless the user explicitly requests delegation/parallel agents. Never start recursive `codex exec`; preserve selected model/reasoning and Codex config.

Capability-check once: `codex exec -m gpt-5.6-sol "reply OK"`. If unavailable, use the strongest available GPT and label it; absent CLI skips the lane.

## Route

| Variant | Use |
|---|---|
| Sol, `xhigh` (`max` only eval-backed/explicit) | code, UI, review, planning, computer use |
| Terra | eval-gated, balanced tool loops |
| Luna | eval-gated, low-risk high-volume loops |

Read `config/model-routing.json`; never infer quality from name/price. [REFERENCE.md](REFERENCE.md) owns provider gates and CLI mechanics.

## Prompt contract

Codex lacks this conversation. Name repo/branch, objective, scope/exclusions, criteria, skill rules/exemplar, verification, evidence, stop. Send only local context/diff; exclude secrets. **Steering payload:** inline matched path rules and one `exemplars/` file.

## Modes

- **Implement:** `codex exec -m gpt-5.6-sol -c 'model_reasoning_effort="xhigh"'`; concurrent writes use isolated worktrees.
- **Review:** different model family when permitted; otherwise labeled clean-context Sol, `-s read-only`, P0-P3 evidence.
- **Adversarial:** Claude-hosted and authorized only; one lane, never verdict.
- **Computer use:** name app/URL, states, evidence.
- **Investigate/analyze:** read-only compact report.

## Workflow

1. Pass host/authorization gate.
2. Select quality-qualified config route.
3. Write self-contained contract.
4. Run with timeout/reference background pattern.
5. Verify citations, commands, and high-risk conclusions before integrating.

Architecture, synthesis, product, safety, and final judgment stay with the coordinator. Sol may own user-facing output and meets the same visual evidence gate.
