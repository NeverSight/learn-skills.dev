---
name: work-automation-kit
description: "Install planning/PM workflows: specs, ticket breakdown, tracker docs, triage."
disable-model-invocation: true
---

Install workflow skills and scaffold tracker labels, domain context, and ADR layout. Prompt loop: explore -> present -> confirm -> write.

## Install

Install once: `grilling`, `domain-modeling`, `triage`, `diagnosing-bugs`, `prototype`, `to-questionnaire`, `to-spec`, `to-tickets`, `handoff`, `writing-for-agents`, `visual-plan`, `visual-recap`, `plan-arbiter`, `agent-watchdog`, `read-the-damn-docs`, `efficient-frontier`.

```bash
for skill in grilling domain-modeling triage diagnosing-bugs prototype \
  to-questionnaire to-spec to-tickets handoff writing-for-agents visual-plan \
  visual-recap plan-arbiter agent-watchdog read-the-damn-docs efficient-frontier
do
  bunx skills@latest add "malinskibeniamin/skills/$skill" --agent claude-code -y
done
```

Jira optionally adds `setup-atlassian-workflow` via `acli`.

## Project context

Read [REFERENCE.md](REFERENCE.md), then:

1. Inspect remotes, agent rules, `docs/agents/`, context/ADRs, whether triage is installed, and monorepo signals.
2. Recommend tracker first; ask only if choice branches.
3. With triage installed, ask whether to keep default five canonical role labels (yes recommended); only collect overrides if the user says no. Otherwise skip labels.
4. Default non-monorepos to single-context without asking. Offer multi-context only for a monorepo, then confirm layout.
5. Confirm draft docs before writing; reuse `templates/`.
6. Choose one instruction file: edit `CLAUDE.md` first when it exists, otherwise `AGENTS.md`; if neither exists, ask which to create. Write approved:
   - `docs/agents/issue-tracker.md`, including `## Wayfinding operations` when `/wayfinder` exists;
   - `docs/agents/triage-labels.md` only with triage;
   - `docs/agents/domain.md`;
   - selected file's `## Agent skills` block with `### Issue tracker`, summary/link, and conditional label/domain pointers.
7. Verify `### Issue tracker` and its link after writing, plus labels, Wayfinding operations, and context layout.
