---
name: writing-for-humans
description: "Write, revise, or critique substantial human-facing prose: documentation, PR descriptions, articles, newsletters, explainers, and educational content."
disable-model-invocation: true
---

# Writing for Humans

Make the reader's effort feel well spent. Create the conditions for a human to follow, understand, feel, judge, or act without replacing the author's meaning and voice with generic polish.

For agent-facing instructions such as `AGENTS.md`, `CLAUDE.md`, skills, prompts, rules, or policies, use `writing-for-agents` instead.

## Workflow

1. **Frame the assignment.** Identify whether the task is to create, revise, or critique; determine the genre and requested scope; inspect the artifact, supplied material, and available sources of truth. Separate established fact, author claim, interpretation, and uncertainty. This step is complete when the mode, scope, and authority of the material are explicit.
2. **Set the author contract.** Establish the intended meaning or central promise, stance, voice, relationship with the audience, non-negotiable material, and permitted degree of intervention. In revision, identify the diction, rhythm, specificity, humor, restraint, and productive irregularities that make the writing recognizably the author's. This step is complete when the agent can state what must become clearer and what must remain the author's.
3. **Set the reader contract.** Identify one primary reader, their job, prior knowledge or current model, stakes, available attention, likely friction, reason to continue, and intended exit. Define the exit as what the reader should be able to explain, distinguish, find, evaluate, feel, remember, or do. Keep comprehension, agreement, attention, emotion, recall, and action as separate outcomes. This step is complete when success can be checked without relying on “the reader gets it.”
4. **Load branch guidance.** Read [`references/reader-progression.md`](references/reader-progression.md) for new substantial pieces, structural revisions, or critiques of comprehension, argument, pacing, or narrative; a bounded copyedit that preserves structure may skip it. Read [`references/articles-and-newsletters.md`](references/articles-and-newsletters.md) for articles, essays, newsletters, opinionated educational writing, or edits where authorial voice and reader relationship are central. Read [`references/pr-descriptions.md`](references/pr-descriptions.md) for pull request descriptions. Read [`references/visual-explanations.md`](references/visual-explanations.md) when a visual would materially reduce the effort needed to understand structure, logic, interaction, or change.
   Read and follow [Stop Slop](references/stop-slop/stop-slop.md) when drafting, editing or reviewing prose for AI writing patterns.
5. **Design the path.** Organize the material around the reader's progression rather than the order in which the author discovered it. Give every section a legible job, supply each necessary inference, and place qualifications where they change interpretation. Keep planning scaffolds internal unless the user requests them or they belong in a durable planning artifact. This step is complete when the headings or structural turns reveal a coherent path to the intended exit.
6. **Produce the requested artifact.**
   - For a new piece, write the complete path in the requested form.
   - For a revision, preserve supported facts, intended meaning, useful voice, public contracts, and out-of-scope material unless evidence or the user requires a change.
   - For a critique, identify specific reader problems with evidence and concrete improvement examples; rewrite only when requested.
7. **Inspect truth and experience.** Trace consequential factual claims to their sources or frame them honestly as interpretation, judgment, or lived experience. Check commands, examples, quotations, links, names, and verification claims when applicable. Inspect whether the text supplies the conditions for its promised reader exit, then reread for voice drift and unintended changes of meaning. Keep the evidence level honest: inspecting the text is not observing a reader, and a fresh-agent read is a proxy rather than human validation.
8. **Run a fresh-reader proxy only by request.** When the user explicitly asks for a fresh-reader pass, second-reader validation, Cartographer review, or another agent to inspect reader friction, ambiguity, or gaps, read [`references/fresh-reader-pass.md`](references/fresh-reader-pass.md) and dispatch its bounded fresh-context Cartographer pass. Treat ordinary requests to create, revise, critique, or review writing as self-inspection only. Reconcile the proxy's findings rather than accepting them mechanically, and revise material problems within scope. This step is complete when every applicable acceptance condition holds and any proxy claim is labeled as such.

## Doctrine

- Preserve the author's identity while removing friction around their meaning.
- Prefer a real reader journey over an inventory of everything the author knows.
- Put the fastest useful orientation before completeness; let readers scan, reread, or leave when their job calls for it.
- Use examples first when the reader must implement, reasons first when they must judge, and story when events or consequences genuinely carry the idea.
- Use curiosity, tension, surprise, visuals, and rhetorical flourish only when they improve orientation, understanding, feeling, judgment, or action.

## Acceptance Gate

- The author's intended meaning, stance, and recognizable voice survive the work.
- The primary reader and intended exit are explicit in the design, even when they remain invisible in the prose.
- The structure follows the reader's job, and every necessary passage earns its place.
- Consequential claims are supported, attributed, or clearly framed with the right epistemic status.
- The genre's specific contract is satisfied without forcing one universal template.
- No unresolved blocking ambiguity or gap remains unless it is intentional and disclosed.
- Claims about reader success match the available evidence: text inspection, fresh-reader proxy, or human validation.
