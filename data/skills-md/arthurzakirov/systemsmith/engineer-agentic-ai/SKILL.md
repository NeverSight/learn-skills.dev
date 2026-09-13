---
name: engineer-agentic-ai
description: "Translate natural-language requests about modifying an AI coding agent, its skills, MCP tools, MCP servers, prompts, routing, tool descriptions, context loading, memory, portability, or other agentic behavior into the concrete mechanics of the target system. Use when a request is underspecified, phrased in human terms instead of runtime terms, or risks making the wrong change because the agent must reason about how Codex, Claude Code, OpenCode, MCP-based systems, or similar runtimes select skills, choose tools, load instructions, apply configuration, and stay transferable across users and machines."
---

# Engineer Agentic AI

## Overview

Convert fuzzy requests about "my AI" into precise changes to the underlying agent system. Focus on the mechanics that actually determine behavior: trigger metadata, prompt layering, context injection, tool availability, MCP descriptions, resource loading, and evaluation surfaces.

## Reframe The Request

Translate user language into implementation language before proposing edits.

- Identify the target system or closest equivalent: Codex skill, Claude Code instruction file, OpenCode config, agent prompt, tool policy, memory file, plugin, or runtime setting.
- Replace anthropomorphic phrasing such as "make the AI understand" with concrete levers such as "change trigger metadata", "move guidance into a file loaded post-trigger", or "add a deterministic script."
- State which layer the request belongs to: always-loaded metadata, conditionally loaded instructions, on-demand reference material, executable tooling, or UI-only metadata.
- Prefer the smallest layer that can reliably change the behavior.

## Model The Runtime

Reason from how the system actually consumes the artifact.

- Treat the YAML frontmatter as the skill's interface contract for invocation. Treat the markdown body as the implementation that executes after invocation.
- Treat MCP server descriptions and MCP tool descriptions the same way: they are interface text used for tool selection, not a place to explain internals.
- For skill metadata, assume `name` and `description` exist to help the agent decide whether to load the skill. Write them for pattern matching, not for human explanation.
- For MCP tools, assume the description is the primary selection surface exposed before tool execution. Write it to indicate when the tool should be called and what observable outcome it provides.
- For MCP servers, assume the server description helps the agent understand when the server's capability area is relevant at all.
- For the SKILL body, assume it is only read after the skill triggers. Put operating instructions there, not trigger criteria that the loader cannot see.
- For tool implementation code, assume Python, libraries, and internal logic are invisible or irrelevant until after the tool has already been selected.
- For references, assume they are read only when explicitly needed. Move bulky examples, schemas, or variant-specific details there.
- For scripts and assets, assume they improve determinism or reuse rather than explanation.
- For UI metadata such as `agents/openai.yaml`, optimize for the human chooser, not the runtime router.

## Separate Interface From Implementation

Keep a single source of truth for invocation.

- Put "when this skill should load" in the YAML `description`, because that text is available before selection.
- Put "when this MCP tool or server should be used" in its description field, because that text is available before execution.
- Put "what to do after loading" in the markdown body, because that text is only available after selection.
- Put "how the tool works internally" in the implementation code, not in the description.
- Do not try to fix missed invocation by adding more "use this skill when..." prose to the markdown body. If the skill failed to trigger, the body was never available to help.
- Do not try to fix missed tool use by expanding the tool description with library names, architecture, or internal algorithms unless those details are necessary for correct invocation.
- Avoid describing implementation details in the YAML description when the real consumer need is the observable outcome or contract.
- Prefer interface wording similar to a function signature or API contract: what kind of request this handles, what outcome it enables, and what context should route here.
- Prefer body wording similar to an implementation: procedures, constraints, scripts, decision rules, and execution details.

Use the programming analogy directly:

- The YAML description is like the public function signature and docstring used for selection.
- An MCP tool description is like the public signature and contract for choosing that tool.
- The markdown body is like the function body.
- The Python tool implementation is also like the function body.
- References, scripts, and assets are support code and data loaded only when needed.
- A caller choosing a function cares about inputs, outputs, and when to call it, not the internal algorithm.

## Apply The Same Principle To MCP

Use the same retrieval model across skills and tools.

- A skill description and an MCP tool description serve the same class of purpose: they help the agent decide whether to bring a capability into play.
- The main difference is the implementation artifact behind the interface: a skill usually expands into markdown instructions, while an MCP tool expands into executable code.
- Because the routing mechanism is similar, the writing rule is similar: describe when to use it and what result it provides, not how it is built internally.
- If a tool uses FastMCP, a custom transport, helper libraries, caching, or complex orchestration, that is usually implementation detail and belongs in code or internal docs, not the description.
- Server descriptions operate at a broader routing level; tool descriptions operate at a narrower action-selection level. Both should stay contract-oriented.
- When multiple tools overlap, sharpen the descriptions around distinguishing inputs, outputs, and intended use cases instead of exposing internals.

## Do Not Mistake Emphasis For Control

Treat repeated words like "always", "never", "critical", or "super important" as a signal to inspect the control plane.

- Do not try to solve reliability problems by amplifying prompt wording across every skill, instruction file, or tool description.
- Louder wording is not a mechanism. It does not create determinism, reduce context overload, or guarantee enforcement.
- If a user says something must always happen or must never happen, interpret that as a requirement for stronger control, not stronger prose.
- If many instructions compete in the same context window, assume some will be dropped or deprioritized. Fix the mechanism before adding more text.
- Avoid turning the system into a graveyard of all-caps priorities and duplicated warnings. That usually makes routing and execution worse, not better.

## Escalate To Stronger Mechanisms

Choose the lightest mechanism that can actually enforce the requirement.

1. Diagnose why the behavior failed.
2. If the capability was never selected, fix the routing surface: skill description, tool description, server description, or other pre-selection metadata.
3. If the capability was selected but instructions were ignored because the context was crowded or ambiguous, simplify, split, or relocate instructions.
4. If the requirement is truly high-confidence or prohibitive, move from probabilistic instructions to deterministic controls.

Deterministic controls can include:

- event hooks that inject context, run checks, block actions, or trigger tooling
- plugins that intercept runtime events or alter behavior
- tool permissions or approval policies that deny, allow, or gate actions
- wrappers or scripts that always run before or after a critical action
- tests, validators, or linters that catch violations automatically
- scheduled automations or trigger-driven workflows when the behavior should happen without relying on a fresh user prompt

When choosing among these, use the official documentation for the current platform instead of assuming feature parity across systems.

- Claude Code exposes hook events such as session start, prompt submission, and pre/post tool use, which can inject context or block actions depending on the hook type.
- OpenCode exposes plugins with event hooks and tool permissions that can allow, deny, or require approval.
- Codex exposes different surfaces such as skills, plugins, permissions, and automations or triggers depending on product surface; do not assume it has the same hook model as Claude Code.

## Map Extremes To Enforcement

Translate "always" and "never" into enforceable runtime behavior.

- "Always load this context before the agent works" suggests a startup, session, or prompt-submission hook, or another deterministic context-injection surface.
- "Always run this check after edits" suggests a post-edit hook, plugin event, or automated validator.
- "Never run this command" suggests a pre-tool hook, permission rule, or blocking wrapper.
- "Always ask before touching this system" suggests an approval or permission policy.
- "Always do this recurring task" suggests an automation, schedule, or trigger rather than a passive instruction sitting in context.

If no deterministic surface exists on the platform, say so explicitly and then choose the strongest available fallback rather than pretending prompt wording is equivalent.

## Design For Portability

Treat local names, local paths, and local product wording as contamination unless they are intentionally required.

- Build skills, prompts, hooks, plugins, MCP servers, and related artifacts so they can be shared across people, machines, operating systems, and directory layouts.
- Do not hard-code home directories, usernames, desktop paths, repository roots, temp directories, or other machine-specific locations when a portable construction is possible.
- Prefer environment variables, repository-relative paths, configuration variables, or runtime discovery over literal absolute paths.
- If a path depends on local installation or company setup, define the dependency explicitly and construct the path from environment variables at runtime.
- If setup requires a user to export variables in a shell profile or config file, say so directly and name the variable instead of embedding one person's filesystem layout into the artifact.
- If a tool needs a URI, command path, or binary location, make that configurable rather than assuming one install location.

Portable patterns:

- `${HOME}` instead of `/home/arthur` or `/Users/alice`
- `${CODEX_HOME}` or another documented root variable instead of a machine-specific skill directory
- repository-relative paths when the artifact lives inside the repo
- config entries or environment variables for external tools, service endpoints, and credentials

Non-portable patterns:

- `/home/arthur/.codex/...`
- `C:\\Users\\Arthur\\...`
- prose that assumes one specific operating system or shell without saying so
- scripts that only work because the author's machine has a particular binary in a particular place

## Generalize Identity And Product Names

Write instructions so they survive changes in model, tool, and human identity.

- Do not anchor reusable skills to one product name just because the user mentioned that product in natural language.
- Translate product-specific user phrasing such as "make Codex do this" or "don't let Claude Code do that" into tool-agnostic role language unless the implementation truly depends on one platform.
- Prefer `you` for the agent and `user` or `I` for the human when writing reusable instructions.
- Avoid human names such as `Arthur` in reusable artifacts. Replace them with `user`, `I`, or another role-based term.
- Avoid agent names such as `Codex`, `Claude Code`, or `Gemini` in reusable instructions unless a platform-specific capability, limitation, or file format makes the distinction necessary.
- If a section is genuinely platform-specific, isolate that specificity in the smallest possible place instead of letting it leak across the whole artifact.

Role mapping:

- `you` = the current AI agent or assistant
- `user` or `I` = the human interacting with the agent
- product names = only when needed to distinguish platform mechanics

This keeps the artifact stable when:

- the same company shares the skill across multiple people
- one person uses multiple machines with different path layouts
- different operating systems are involved
- the same instruction set is reused across Codex, Claude Code, OpenCode, Gemini, or another agent runtime

## Enumerate Provider Equivalents

When a reusable artifact needs to mention a provider-specific file or directory, enumerate equivalents instead of naming only one vendor surface.

- Do not say only `CLAUDE.md`, only `AGENTS.md`, only `.claude/skills/`, or only `.codex-plugin/plugin.json` unless the task is genuinely platform-specific.
- If the concept is cross-provider, name the concept first and then list the relevant concrete paths for Claude Code, Codex, OpenCode, `.agents` or Agent Skills-compatible tools, and any other platform explicitly in scope.
- End the enumeration with a fallback such as `or the equivalent for your agentic AI tool` when the ecosystem may include additional tools.
- Read `references/provider-paths.md` when you need exact current filenames or directories for instruction files, skills, commands, agents, hooks, plugins, or manifests.
- Treat names like skill, command, prompt, slash command, agent, subagent, hook, and plugin as potentially different labels for related mechanics. Translate by function, not by vendor wording alone.

## Write Trigger Metadata For Retrieval

Describe observable request patterns and target artifacts. Avoid restating facts already implied by the environment.

- Name the concrete task, artifact, or mechanism: skills, MCP tools, MCP servers, agent prompts, tool routing, context files, memory, delegation, evaluation harnesses.
- Include the kinds of user requests that should cause invocation: "fix a skill", "make Codex use this correctly", "change how Claude Code loads instructions", "turn this behavior complaint into the right config change."
- For tools, describe the request pattern that should lead to selection and the externally visible action the tool performs.
- Describe the contract from the consumer perspective: what problem this skill takes in and what kind of behavior change or output it produces.
- Avoid "what the skill does internally" phrasing unless it is necessary for retrieval. Internal procedure belongs in the body.
- Avoid "what the tool does internally" phrasing unless it is necessary to distinguish it from another tool.
- Do not waste tokens on phrases like "for AI agents" when the field is only consumed by AI agents anyway.
- Do not describe the skill as if explaining it to a person encountering a catalog entry unless the field is human-facing.
- Prefer wording that helps embedding or pattern matching: nouns, verbs, platforms, artifacts, failure modes.

Bad:
`This skill is needed when an AI agent needs help understanding skills.`

Better:
`Use when editing skill metadata, trigger descriptions, or instruction files for Codex, Claude Code, OpenCode, or similar agent systems, especially when a natural-language request must be converted into the correct runtime mechanism.`

Bad MCP tool description:
`Tool that uses FastMCP, async Python, retries, and custom libraries to fetch data.`

Better MCP tool description:
`Use to fetch the current dataset or record needed to answer a user request when the agent needs live data from this server.`

## Decide What To Change

Choose the implementation target that matches the failure mode.

- If the problem is incorrect invocation, edit the always-visible trigger metadata.
- If the problem is incorrect tool selection, edit the MCP tool or server description before touching implementation code.
- If the problem is good triggering but bad execution after load, edit the post-trigger instructions.
- If the problem is good tool selection but bad execution, edit the Python implementation, tool schema, or runtime logic rather than the description.
- If the user wants something to always happen or never happen, inspect whether a hook, plugin, permission rule, validator, or automation is the correct surface.
- If the system is overloaded with many competing instructions, reduce context pressure before adding stronger wording.
- If the artifact leaks a local path, username, hostname, or product-specific identity into reusable instructions, replace it with an environment variable, relative path, config surface, or role-based term.
- If the artifact mentions only one provider-specific file for a cross-provider concept, rewrite it to enumerate the known equivalents and add an open-ended fallback.
- If the body contains a long "when to use this skill" section, move the actionable trigger criteria into the YAML description and delete or sharply reduce the duplicate body prose.
- If the problem is repeated fragile code generation, add a script.
- If the problem is too much context in the main instructions, move details into references and point to them.
- If the problem is only about how the skill appears in a picker, edit UI metadata instead of runtime metadata.
- If the request spans multiple layers, separate them explicitly instead of blending them into one vague description.

## Produce An Engineering Translation

When responding or editing, explicitly translate the request into the mechanics you will modify.

Use a compact format like:

1. User intent: what outcome the user actually wants.
2. Runtime interpretation: which mechanism controls that behavior.
3. Change surface: which file or config layer to edit.
4. Why this layer: why the other plausible layers are insufficient or redundant.

Example translation:

- User intent: "Make my AI better at knowing when to use this skill."
- Runtime interpretation: improve skill retrieval, not task execution.
- Change surface: `SKILL.md` frontmatter `description`.
- Why this layer: the body is unavailable until after trigger, and UI metadata is not part of runtime routing.

Another translation:

- User intent: "Make the agent choose this MCP tool correctly."
- Runtime interpretation: improve tool selection, not tool internals.
- Change surface: MCP tool `description`.
- Why this layer: the description is what the agent sees before deciding to call the tool; Python implementation details are not the routing surface.

Another translation:

- User intent: "This must always happen after every file edit."
- Runtime interpretation: this is an enforcement requirement, not a wording requirement.
- Change surface: a post-edit hook, plugin event, validator, or other deterministic runtime control supported by the platform.
- Why this layer: repeating "always do this" in instructions remains probabilistic, while an event-based control can run every time by construction.

Another translation:

- User intent: "Make this work for everyone on the team, not just on my machine."
- Runtime interpretation: remove machine-local assumptions from paths, identities, and platform naming.
- Change surface: environment variables, relative path construction, config surfaces, and reusable role-based wording in the relevant files.
- Why this layer: portability failures come from hard-coded local state, not from insufficiently strong prose.

Another translation:

- User intent: "This instruction should refer to CLAUDE.md, AGENTS.md, skills, and plugin manifests correctly across tools."
- Runtime interpretation: map a shared concept onto the current providers' actual filenames and directories.
- Change surface: reusable wording plus exact path enumeration backed by `references/provider-paths.md`.
- Why this layer: the failure is incorrect provider mapping, not missing emphasis or missing implementation detail.

## Guardrails

- Do not preserve user phrasing if it obscures the mechanism.
- Do not invent abstractions when the platform already exposes a direct primitive.
- Do not conflate human-facing descriptions with machine-facing routing text.
- Do not put trigger logic only in places that are loaded after selection.
- Do not treat the markdown body as a fallback trigger surface.
- Do not let YAML become an implementation dump. Keep it at the contract level.
- Prefer a single source of truth for "when to use this skill." For now, keep that source in YAML `description`.
- Do not let MCP tool descriptions become implementation dumps. Keep them at the contract level too.
- Do not answer "make this always happen" by merely adding more "always", "never", or "critical" wording.
- Do not assume more emphatic instructions can substitute for hooks, plugins, permissions, validators, or automations.
- Do not assume one platform's control surfaces exist on another platform without checking the current docs.
- Do not hard-code personal names, home directories, or machine-local absolute paths into reusable artifacts.
- Do not let one product name become the default pronoun for the agent when the instruction should be portable.
- Do not keep user identity as a proper noun when a role term such as `user`, `I`, or `you` is sufficient.
- Do not mention only one provider-specific path when the underlying concept is cross-provider and the artifact is meant to be reusable.
- Do not add redundant wording whose only meaning is already guaranteed by the field's usage context.

## Output Standard

Deliver either:

- a concrete edit to the relevant system files, or
- a short mapping from user phrasing to the exact files and fields that should change.

If the platform is ambiguous, state the assumption and still express the answer in runtime terms rather than human-description terms.
