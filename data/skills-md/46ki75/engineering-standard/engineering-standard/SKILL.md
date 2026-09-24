---
name: engineering-standard
description: Apply shared engineering standards when implementing, reviewing, or documenting software. Covers evidence-based verification, iterative delivery of large changes, project contribution rules, development tooling, formatting, Rust conventions, and Git/GitHub workflows.
---

## Engineering principles

- Add comments when they preserve information that would be costly to rediscover, such as rationale, constraints, invariants, or externally verified behavior; do not restate the code.
- Prefer direct, deterministic computation, execution, and verification over inference. Use calculators, tests, diagnostics, type checkers, linters, LSP diagnostics, direct execution, measurements, or other reproducible checks when applicable.
- Verify a problem before attempting to fix it, and verify the fix afterward using the same or an equivalent check whenever possible.
- When reproducing a bug, encode the reproduction as an automated test whenever practical. Confirm that the test fails before the fix, retain it as a regression test, and confirm that it passes afterward.
- When direct verification is not possible, rely on authoritative primary sources such as official documentation, specifications, and RFCs. Use secondary sources only for discovery or context, and verify their claims against primary sources whenever available.
- When iterative subagent review is requested, use a fresh reviewer each round. Verify findings before acting, fix confirmed defects, and add regression tests where practical. Explain rejected findings with evidence. Repeat until no actionable findings remain or the agreed review budget is exhausted; report unresolved findings and verification limits.
- Scale upfront planning to reversibility. For large or uncertain changes, settle decisions that are costly to reverse, such as public interfaces, data formats, migration and rollback paths, and invariants, and keep the rest of the plan high-level.
- For such changes, first extend the repository's existing validation to cover behavior that must be preserved and the intended invariants, record a baseline, including any pre-existing failures, and state what the checks do not cover. Proceed in small steps that each end without new failures, updating checks in the same step only for intended behavior changes. Revise the plan at checkpoints based on what you learn.

## Natural-language content

- Keep responses and other writing concise, and use American English.
- Draft long-form natural-language content in the existing source file or, when none exists, a temporary file. Publish or submit only the reviewed version, directly from the file when supported.
- After creating or updating documentation, instructions, prompts, or other prose, review the affected document or message as a whole before finalizing it. Identify and fix unnecessary repetition and inconsistencies, including conflicts with documents it links to or depends on. Confirm that retained repetition serves a purpose. Address organization before sentence-level wording, and preserve necessary context and technical meaning.

## Project rules

Project- and directory-specific rules take precedence over this skill's defaults. Before editing, humans and agents must read and follow the project's contribution guide, when present, and applicable local instructions. Respect existing guides under other names or locations.

- `README.md`: Link to the contribution guide and explicitly instruct contributors to read it before making changes.
- `CONTRIBUTING.md`: Define shared project-specific contribution rules for humans and agents. Link to detailed references and tool configurations as needed.
- `AGENTS.md`: Link to the contribution guide and explicitly require agents to read it before making changes. Keep agent-only instructions here.

## Tooling and workflow

- Prefer [mise](references/mise/README.md) for development-tool management and task execution. Pin exact tool releases, including patch versions; keep Rust native in `rust-toolchain.toml`. Declare shared tasks in root `mise.toml`, document commands as `mise run <task>`, and use ecosystem package managers for project dependencies. Keep each tool version and workflow definition authoritative in one place.
- Use the repository's existing validation commands. When adopting mise, expose `lint`, `fmt`, `fmt-check`, and a project-wide `check`; use [Lefthook](references/lefthook/README.md) for Git hooks and file-scoped validation. Format affected, covered files and verify the same scope; report failures and unexpected empty selections. Follow the [formatting reference](references/formatting/README.md) for formatter and editor integration.
- Use the [Git](references/git/README.md) and [GitHub](references/github/README.md) defaults.

## Language standards

- For Rust code and project configuration, follow the [Rust reference](references/rust/README.md): workspace inheritance and a shared edition, verified MSRV, baseline lints, locked validation, nextest with doctests, hermetic tests, and typed errors.
