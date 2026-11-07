---
name: add-agent-playbooks
description: Add Redis Iris Agent Playbooks to an existing agent. Use when approved answers or repeatable procedures live in prompts, document retrieval, or a semantic response cache. Connect or provision a Playbook, publish FAQs and Skills, and verify the first application turn with optional review proposals.
license: MIT
metadata:
  author: redis
  version: "1.0.0"
---

# Add Agent Playbooks

Bring an existing Python agent to one verified Playbook-backed turn, then finish the requested content migration or integration. FAQs supply published answers; Skills supply procedures loaded separately from discovery previews. The application owns response policy, tool permissions, and approval of actions.

## 1. Orient and choose the behavior

Find the model call, tool registration, framework/version, and existing policy or procedure sources. Preserve the graph, business tools, and global response/authorization rules. Infer these decisions from the request and code; ask only about unresolved choices and state defaults used:

| Decision | Result |
|---|---|
| Which repeated tasks need procedures? | One Skill per procedure; skip when none. Move task-specific tool guidance out of prompts. |
| Which questions require approved answers? | One FAQ per approved answer; skip when none. |
| Which audiences use the content? | One audience: no attribute or filter. Several: matching attributes on content and a trusted runtime audience. |
| Should uncovered answers be submitted for review? | Default no. Yes: choose automatic uncovered proposals or an application-owned quality/privacy gate; preserve existing gates. |
| Where does the content live today? | Convert relevant prompt text, docs, or retrieved content into versioned files. Retain authoritative sources. |

Prefer progressive disclosure when the agent can execute tools; use score-based hooks otherwise. Define clarification, escalation, and outage behavior: approved-only answers need an explicit policy for insufficient content.

## 2. Check prerequisites and connect

Follow [provisioning](references/provisioning.md) for the short prerequisite check and new, partial, or existing setup. Reuse usable configuration and published content. Local defaults require a running stack; Cloud and self-managed administration use different paths.

Check framework APIs against the installed version before editing. Use an available docs MCP. For the CLI, run `iris agent-playbooks <command> --help`. Inspect installed package source when documentation does not match the installed API. Report unresolved compatibility questions.

## 3. Publish the first relevant content

Follow [content authoring](references/content.md) for file formats, quality checks, audience attributes, validation, previews, and publication. Begin with one approved FAQ or procedure relevant to the requested task; use both only when needed. Confirm its serving version before wiring the agent. Complete any broader requested migration after the first turn works.

## 4. Integrate with the application

Follow [runtime integration](references/integration.md) for the chosen mode, async variants, and framework placement. Create one configured context object and use it throughout. Build context from the base prompt afresh each turn. Register disclosure tools with both the model and executor.

## 5. Run, inspect, and improve

Follow [first success](references/first-success.md): execute the actual application, inspect the content keys/versions and procedure loads, check a paraphrase and missing-content behavior, fix observed gaps, and rerun. Show the user what worked and how to repeat it. Once replacement reads work, remove obsolete runtime prompt/retriever/cache code and its unused embedding pipeline; run affected application checks on the final integration.

## 6. Hand off and maintain

Use the handoff in [first success](references/first-success.md#handoff) to distinguish observed results from unverified work and leave an exact repeat command. Walk through the [next approved content update](references/content.md#maintain-the-content), naming the content owner/publisher and any remaining deployment configuration.

## Essential constraints and optional paths

- Every `iris` command uses root options `--json --no-input`. The CLI handles administration and content management; the Python SDK runs inside the application.
- Keep runtime `.env` credentials separate from `.env.content` publishing credentials and administrative tokens. Grant the agent `read`, adding `propose` only for submissions. Never print secrets or commit env files.
- Publication selects serving content. A proposal is a review candidate; submitting or accepting one does not implicitly publish it.
- For a semantic response cache, read [cache migration](references/response-cache.md) before replacing its lookup/write path.
- For background proposals from Agent Memory, read [Memory extraction](references/memory-extraction.md) before enabling another submission path.
