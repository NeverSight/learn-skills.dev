---
name: writing-skills
description: Use when creating, reviewing, or improving an agent skill; turning a repeatable workflow into a skill; investigating missed or unwanted skill loading; or changing a skill's SKILL.md, references, or helper scripts in ways that affect use. Not for installing or applying an existing skill, explaining the format, or mechanical edits that preserve meaning and behavior.
---

# Writing Skills

A skill should help an agent make a better decision or produce a better result on a recurring task. Make it easy to select, useful when loaded alone, and no more demanding than the problem it addresses.

**Loading this skill does not require a new skill, rewrite, test framework, subagent, or approval ceremony.** For a review-only request, report findings and proposals without editing. Scale authoring and checks to the change.

## 1. Establish the Need and Scope

Read the current skill, relevant supporting files and project instructions, and nearby skill metadata before choosing a solution. Open neighboring bodies when ownership or boundaries need clarification, not as a full library sweep. When available, inspect actual missed loads, wrong outputs, or repeated user corrections. Do not invent a failure because a baseline happens to succeed.

Decide:

- **What improves?** Name the recurring task, intended result, observed gap or explicit requirement, and important exceptions.
- **Where does it belong?** Improve an existing skill when it already owns the trigger. Keep project-only rules in project instructions, session progress out of skills, and deterministic checks in existing automation when suitable. A separate skill needs a distinct selectable task, not just more detail within another workflow.
- **What is authorized?** Separate an audit, a proposed design, and implementation. Ask only about unresolved choices that would materially change scope or behavior; do not reopen settled decisions.

For uncertain structure or portability choices, open [authoring patterns and format notes](references/anthropic-best-practices.md). It distinguishes the open format from product-specific behavior; it is not a second mandatory checklist.

## 2. Design the Trigger Before the Body

Agents normally select from the name and description before seeing the body. A boundary mentioned only in the body cannot prevent the initial wrong selection.

- Use a short, specific name. Match the folder name to frontmatter `name`; use lowercase letters, digits, and single hyphens, without a leading or trailing hyphen.
- Start the description with `Use when...`. Name observable tasks, symptoms, and user intent, including implicit requests when they belong. Avoid a summary of the internal workflow or an exhaustive keyword list.
- Add exclusions for plausible neighboring tasks, not obviously unrelated ones. An explicit request to create or audit a skill can be small; task size alone should not suppress it.
- Define realistic prompts that should load it and near-misses that should not. Include wording that does not name the skill, and relevant user languages. Check selection using metadata alone, separately from application with the body loaded.

If loading is wrong, determine whether the runtime registered the skill and exposed current metadata before broadening the description. Installer discovery, metadata classification, an actual load, and useful execution are different evidence.

## 3. Write the Smallest Useful Guidance

State purpose and scope first, then the decisions or steps that change the result. Include needed inputs, meaningful exceptions, how to handle unavailable evidence/tools, and observable completion criteria. Use concrete examples only where they clarify a real choice; do not explain basics the agent already knows.

- Keep essential guidance in `SKILL.md`. Put focused detail in `references/` and runnable helpers in `scripts/`. Every supporting file needs a reachable entry point with **when to open/run it and why**, preferably beside the relevant decision rather than only in a closing file list.
- Use relative Markdown links for reading and explicit commands for execution. Resolve resources from the loaded skill's directory, not the project's current directory or a hard-coded installation path. Optional details need not be read every time, but a required branch must make its required reference clear.
- Keep one owner for each rule; references expand the body, not contradict it. Keep main references directly reachable from `SKILL.md` and give long guides a contents list or split them by decision.
- Preserve user constraints and instruction priority. A skill cannot authorize deletion, installation, delegation, publication, or policy overrides. Other skills may help when available, but should not be an unconditional dependency unless the skill explicitly targets that environment.
- Prefer a positive recipe or output shape. Use firm boundaries for real risks, not manufactured urgency or obedience rituals. When recurring bypasses need clearer discipline guidance, read [discipline wording](references/discipline-wording.md).

A diagram is optional. When branching is genuinely clearer visually, use the small [Graphviz example](references/graphviz-conventions.dot). For SVG preview, run `node <skill-dir>/scripts/render-graphs.mjs <target-skill-dir>`; it requires Node.js and Graphviz `dot`, expects one graph per top-level `dot` fence (up to three leading spaces, not inside a list or blockquote), writes numbered SVGs to the target's `diagrams/`, and refuses existing output files. Use `--output-dir <new-directory>` to choose another destination. Unsupported indented/quoted fences fail explicitly instead of silently skipping diagrams. It renders diagrams separately; it does not combine independent graphs. Render only trusted DOT inputs; this helper does not sandbox Graphviz or sanitize SVG for publication.

## 4. Verify Selection, Usefulness, and the Package

Choose checks that could expose the changed behavior, using the project's existing practices. Do not add a framework or a fixed test campaign merely because this skill loaded.

1. **Selection:** compare positive and near-miss prompts against metadata. When automatic-loading evidence matters, use a safe scoped request in the target runtime without naming the skill and inspect the actual load/read event. Fresh sessions avoid old metadata; repeated runs or additional models are useful when variability or deployment scope warrants them.
2. **Application:** give a reader or fresh evaluator the body, relevant facts, and access to resources. Ask for a concrete decision or artifact, not a recital. Define expected outcomes independently of the wording being tested. Compare with no skill or the previous revision when practical; keep evaluator context and tools comparable. A successful baseline is evidence too.
3. **Package:** validate frontmatter against the current format/target installer, confirm discovery, follow relative links from a standalone copied folder, and exercise changed scripts with representative success and failure inputs. Check dependencies, output locations, nonzero failure status, and preservation of existing data. Update README, moved-path references, and attribution notices when affected.

Open [testing skills](references/testing-skills.md) when designing behavior comparisons or diagnosing a failed evaluation. For testing always-loaded instructions that select skills, use the [instruction-file experiment](references/instruction-files-testing.md), not as a default instruction to browse every installed skill.

Keep raw results and session progress outside live guidance. Report the revision checked, checks run, concrete misses or regressions, and skipped checks. A read-through is not a behavior test; a simulation or installer listing is not proof of automatic loading, cross-model reliability, or real-world safety. Stop when agreed outcomes have adequate evidence or a named evidence/authorization gap blocks further checking—not when a skill seems “bulletproof.”

## Evaluating This Skill

Maintainers can use [evaluation scenarios](references/evaluation-scenarios.md) to check this skill's own selection, useful application, and reference navigation. These are reusable cases, not completed results or steps for every authoring task.

Adapted supporting material retains a [bundled license notice](references/license-notice.md); consult it for provenance or redistribution, not as authoring guidance.
