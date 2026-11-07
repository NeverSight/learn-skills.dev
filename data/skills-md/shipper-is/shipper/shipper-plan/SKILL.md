---
name: shipper-plan
description: A custom planning skill to create high-fidelity plans using the Shipper framework
---

The goal of this skill is to create a detailed and comprehensive plan for a feature or task based on the user's limited input.

Before anything else, read and follow [./CONFIG.md](./CONFIG.md). It tells you where plans, spikes, bugs, reviews, and modules live in this repository (written below as `<plans>`, `<spikes>`, `<bugs>`, `<reviews>`, and `<modules>`) and which team and personal preferences apply.

## Module references

If the user's request contains a Shipper module reference — a `https://shipper.is/modules/<id>` URL (with or without trailing slash), a `modules/<id>` path on GitHub, or an explicit module id such as `customer-support` — follow the **module flow** below. Otherwise, the standard four-step flow applies unchanged.

### Module flow

1. **Install the module.** Run `shipper modules add <id>` from the repository root (pass `--dir <path>` if the repo is not the current working directory). `shipper modules add` already installs into the configured modules directory, `<modules>/<id>/`. If the `shipper` CLI is not installed, fall back to fetching markdown from `https://raw.githubusercontent.com/shipper-is/shipper/main/modules/<id>/`: start with `MODULE.md`, then fetch each reference file linked with a relative `./FILE.md` path, and write them into `<modules>/<id>/`.
2. **Read the module.** Read every file in `<modules>/<id>/`. The module is the feature spec — it defines behavior, data model, UX, and architecture in stack-neutral terms.
3. **Map to the host repo.** Explore the host codebase to map the module's requirements (data model, UI surfaces, auth assumptions) onto the repo's actual stack and conventions.
4. **Ask integration questions.** Use the tool you have available to ask clarifying questions focused on choices the module leaves open (placement, naming, which optional features to include). Do not re-ask things the module already decides.
5. **Write the plan.** Cite both module files (as the spec) and host repo files (as the integration points). In the Plan Overview, include a line such as: `Built from module \`customer-support\` v1` (use the module's actual `id` and `version` from its frontmatter). State that `<modules>/` should be committed to the repo alongside the plan.

After install, the next step for the user is `/shipper-loop` on the plan (or `/shipper-build` for a single phase) — same as the standard flow.

## Standard flow

This is a READ-ONLY process. You must not make edits, run non-readonly tools, change configs, or commit anything — **except** for the allowed writes listed below.

**Allowed writes:** the plan markdown file in `<plans>/open/`, and module files installed into `<modules>/<id>/` (via `shipper modules add` or the raw-GitHub fallback above). Running `shipper modules add` is explicitly permitted.

The first step is to gather just enough context from the existing codebase to try and better understand what the user is asking for. If the `shipper_search` MCP tool is available, start by searching with a short natural-language description of the request to find related plans, spikes, bugs, and reviews (open and done), then read the most relevant hits with `shipper_get_doc` or your file reader. If the tool is not available, fall back to grep/glob over the artifact directories. Treat hits as leads, not truth — verify against the current code. Use parallel subagents to look at different parts of the codebase or angles at once.

The second step is to use the tool you have available to ask the user clarifying questions about their request. This will help to ensure that the plan is tailored to their specific needs and requirements. The goal is to gain a clear understanding of the user's objectives, push back on anywhere that their request dissents with the existing codebase, and ensure that there is mutual understanding of the outcomes.

The third step is to take another pass to gather any additional context that may be relevant now that the user's objectives are clearer. This should include looking up any existing reusable parts of the codebase and common/shared codebase conventions that we should utilize.

The fourth step is to create a detailed plan (as a markdown file). It is important that the plan contains a considerable amount of detail because it will be passed down to a junior level developer with minimal understanding of the codebase. It is smart to include specific files that need changing, reusable parts of the codebase that need to be utilized, existing conventions that the codebase follows that need to be upheld, and important caveats or things to watch out for that a junior level developer would miss.

New plan files must start with a YAML frontmatter block containing `type: plan` at the very top (before the `#` title).

The plan should include all of that information at the beginning of the plan structured in the following sections:

A: Plan Overview
B: Related Files
C: Existing Code to Utilize
D: Codebase Conventions to Follow
E: Gotchas

Following those sections we need a "Plan" section that includes an in-depth task list with checkboxes that follows the pattern of Phases and Sections. Like this:

----
## Phase 1
- overview of phase 1
- list of outcomes
### Section 1
- overview of section 1
- checklist of items to be completed in this section
### Section 2
- overview of section 2
- checklist of items to be completed in this section
----

Plan quality requirements:
- Cite specific files and essential snippets
- Use full-path markdown links for files
- Keep scope proportional to the task
- May use mermaid diagrams for architecture/flows
- No emojis in the plan

The junior engineer will use this plan as a roadmap to see everything that needs to be completed.

Place the plan in `<plans>/open/` (committed to the repository). If they do not exist yet, also create `open/` and `done/` folders under `<plans>`, `<spikes>`, and `<bugs>`.
