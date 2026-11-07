---
name: smart-delegate
description: >
  Quality-first delegation that routes independent work to suitable agents or models without
  assuming a particular provider. Use for multi-file exploration, reviews, research, parallel
  work, or when the user asks to delegate or use agents.
allowed-tools: Bash(python3 *load-config.py*)
---

# Smart Delegate

Delegate focused work when doing so improves quality, speed, or context isolation. Quality comes
first: pick the least expensive model that can reliably complete the task, and prefer the more
capable one when uncertain. A weak answer from a cheaper model costs more in rework than the
stronger model would have.

This skill recommends which model suits an assignment. When the selected profile has an
`invocation`, follow it as the delegation mechanism (for example a CLI such as `codex` or
`opencode`). Otherwise use the host environment's own delegation tools. Run slow invocations in the
background with a time limit.

## Active configuration

Every time this skill is invoked, the active configuration is loaded by
`scripts/load-config.py` and injected below with YAML comments removed. Use only this injected
text. Do not read the configuration files yourself, and do not ask the user to paste them.

!`python3 "${CLAUDE_SKILL_DIR}/scripts/load-config.py"`

The script uses the first file found and does not merge: `.smart-delegate/config.yaml` in the
current project, then `~/.config/smart-delegate/config.yaml`, then the bundled
[config.yaml](config.yaml) defaults (four tiers: Fast, Focused, Deep, Strongest, each listing
preferred model names). If nothing is injected above, route using the models available in the
environment.

When you delegate, pass the selected profile's `invocation` text verbatim in the assignment, along
with its `description` when it helps the delegate. Do this on every delegation, not only the first.
For enabled `review` and `qa` stages, pass their `description` and `invocation` the same way.

A configuration may contain an ordered `models` list and optional `review` and `qa` stages:

```yaml
models:
  - title: Focused worker
    model: Sonnet
    priority: 10
    description: |
      Use for bounded implementation and investigation.
      Synthesize evidence into a concise result.
    invocation: |
      Invoke the configured worker with the assignment on stdin.
      Preserve the worker's structured result.

review:
  enabled: true
  description: |
    Review completed changes for correctness and regressions.
    Include maintainability findings supported by evidence.
  invocation: |
    Invoke the configured reviewer with the completed diff.
    Request prioritized findings with file references.

qa:
  enabled: true
  description: |
    Exercise changed behavior.
    Verify every acceptance criterion independently.
  invocation: |
    Run the configured QA tool against the changed behavior.
    Preserve commands, results, and failure evidence.
```

This is the only configuration file used by both Smart Delegate and Coordinator. The file, every
section, and every parameter are optional. Supported parameters are:

- `models`: list of available routing profiles. When absent or empty, select from models and tools
  available in the environment.
- `models[].title`: human-readable profile label; it does not need to match a provider model ID.
- `models[].model`: optional model name or ID, or a list of them in preference order (for example
  `[Sonnet, Terra]`). Use the first one available in the environment, passing it as the model
  parameter of the host's delegation tool when that tool accepts one, or injecting it into
  `invocation`. When absent or none is available, use the host's default model for the profile; if
  that is also unsuitable, fall back to the next suitable profile.
- `models[].description`: guidance describing which tasks suit the profile. When absent, infer
  suitability from the other fields and current environment.
- `models[].priority`: numeric preference among equally suitable profiles; lower numbers are
  preferred. Entries without it retain file order after entries with an explicit priority.
- `models[].invocation`: free-form instructions for invoking the profile through an agent, model,
  CLI, API, or other tool. Inject it into the assignment and follow it when the profile is selected.
- `review`: post-change review stage. Its presence enables automatic review unless disabled.
- `review.enabled`: boolean; `false` disables review and any other value or omission enables it.
- `review.description`: free-form review scope and selection guidance.
- `review.invocation`: free-form instructions for invoking a reviewer or review tool.
- `qa`: post-change quality-assurance stage. Its presence enables automatic QA unless disabled.
- `qa.enabled`: boolean; `false` disables QA and any other value or omission enables it.
- `qa.description`: free-form QA scope, acceptance criteria, and selection guidance.
- `qa.invocation`: free-form instructions for invoking a QA agent, test runner, or other tool.

Every `description` and `invocation` accepts a single-line YAML string or a multiline block scalar.
Use `|` to preserve line breaks exactly. Use `>` to fold wrapped lines into spaces. Preserve the
parsed text when injecting it into assignments; do not flatten, truncate, or split instructions.

Keep simple invocations inline. When invocation requires several commands, branching, retries,
substantial quoting, or reusable logic, put that behavior in a script instead of embedding it in
YAML. The `invocation` value should explain to the agent:

- the script path and required runtime;
- how to pass the assignment and any other inputs;
- expected stdout, artifacts, and exit-code meaning;
- prerequisites and safe failure behavior.

Prefer paths relative to the configuration file or project and state which base is used. The agent
must inspect the script's usage help or relevant source before its first execution, must not guess
missing arguments, and must preserve the user's authorization boundaries when running it.

Ignore empty model entries and unknown parameters that cannot inform routing. For an enabled review
or QA stage without `invocation`, select an appropriate configured profile and available delegation
mechanism. Pass enabled stages to Coordinator; Smart Delegate selects and invokes their workers.

Treat descriptions as selection guidance, not keyword rules. If no invocation is provided, use the
environment's normal delegation mechanism with the selected model. Never invent an unavailable
model or tool. If a configured invocation cannot be used, select the next suitable profile or use
the environment's normal delegation mechanism.

## Decide when to delegate

Delegate when at least one of these applies:

- Two or more independent tasks can run in parallel.
- Exploration requires reading several files or sources and returning a synthesis.
- A focused review benefits from an isolated context.
- The task has clear inputs and outputs and does not need user interaction.

Work inline when delegation overhead exceeds the likely benefit, the result is needed before any
other work can proceed, or the task requires user dialogue.

When several independent tasks exist, launch them together when the environment supports it. Give
each delegate a bounded assignment and ask for conclusions or artifacts rather than raw context.

## Route work

Compare the task against any configured profile information. Consider ambiguity, breadth, required
judgment, risk, and the cost of a weak answer. Choose the lowest-cost profile that is clearly
capable. If uncertain between candidates, choose the more capable one even when its priority is
lower.

Typical routing signals:

- Lookups, exploration, and transformations need little judgment (Fast).
- Bounded implementation, diagnosis, review, and synthesis with clear instructions (Focused).
- Architecture, ambiguity, security, and tradeoffs need deeper judgment (Deep).
- Costly-to-reverse or highest-stakes decisions justify the strongest tier (Strongest).

Configuration expresses user preferences but does not override availability, safety constraints,
or explicit instructions in the current request.
