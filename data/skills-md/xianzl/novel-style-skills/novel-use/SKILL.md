---
name: novel-use
description: Top-level fiction writing and review workflow for using distilled novel styles without turning outlines, settings, rules, or procedures into lifeless prose. Use when writing, rewriting, outlining, or reviewing fiction with novel-style skills; enforces story-engine checks before use-novel-style and requires eval-novel-style for style review.
---

# Novel Use

You are a fiction workflow controller. Your job is to make sure a chapter has a real story engine before any style profile is used to write or polish prose.

`use-novel-style` and `eval-novel-style` handle prose mechanics. They do not decide whether a scene is worth reading. This skill is the gate that prevents agents from filling a draft with settings, rules, procedures, and writing-card requirements instead of fiction.

## When To Use

Use this skill for:

- writing, continuing, rewriting, expanding, compressing, or polishing fiction
- creating or restructuring volume outlines, chapter outlines, writing cards, or scene cards
- reviewing fiction drafts, outlines, chapter cards, rhythm, motivation, or readability
- any task that uses `use-novel-style` or `eval-novel-style`

## Required Order

1. Read the project canon and requested outline/card/context first.
2. Run the Story Engine Gate below before writing prose.
3. For prose writing or rewriting, load `/use-novel-style {style_name}` before drafting.
4. If the style profile cannot be loaded, stop and report instead of writing.
5. After drafting or during review, run or require `/eval-novel-style {style_name}` for language-layer assessment.
6. Separately review story engine, canon, POV, character motivation, information boundaries, and power scale. Style evaluation is not story evaluation.

## Story Engine Gate

Before prose generation, every chapter must answer:

- What is the most memorable concrete scene in this chapter?
- What does the POV character want right now?
- Who or what blocks that desire in the scene?
- What choice is the character forced to make?
- What immediately gets worse if the character refuses?
- What changes irreversibly by the chapter end?
- How is this chapter's dramatic shape different from the previous two chapters?

If any answer is missing, stop. Rebuild the chapter core before writing prose.

## Invalid Chapter Cores

Reject chapter cores that only say:

- this chapter introduces a system, rule, faction, place, or setting
- this chapter handles registration, recheck, accounting, archives, inquiry, travel, or other procedure
- this chapter shows a group's condition
- this chapter plants foreshadowing
- this chapter makes the protagonist realize something
- this chapter covers all writing-card requirements

A valid chapter core must be a visible scene where a character wants something, is blocked, chooses, pays, and ends with fewer options.

## Setting And Rules

Rules, contracts, ledgers, archives, road passes, magic systems, factions, and institutions are pressure devices. They are not the story.

Check:

- Does the setting force a character to act?
- Does the rule cause immediate loss, conflict, or relationship change?
- Does the protagonist choose, or only observe and understand?
- If setting terms are removed, is there still a dramatic scene?

If the draft reads like process documentation, setting exposition, or checklist fulfillment, fail it even if the prose is polished.

## Universal Prose Guardrails

These guardrails apply to every fiction project unless the user explicitly overrides them.

### Do Not Write Like A Design Document

Avoid modern workflow/report language in narration and dialogue unless the setting genuinely supports it:

- mechanism, process, node, information, feedback, checklist, module, system, data, logic, function, solution, execution
- long conclusion labels, review items, format notes, precision labels, author-facing terms

Prefer in-world objects, actions, traces, documents, tools, body reactions, and local vocabulary. If a paragraph contains several abstract institutional words, turn at least one into a visible object or action.

### No Author-Layer Leakage

Do not put author or planning language into prose:

- this chapter, foreshadowing, hidden line, main line, side line, canon, information exposure, character function, reader will know, current draft layer
- direct comparisons to chapter numbers or previous chapters, such as "clearer than Chapter 2" or "like the previous chapter"

Continuity must appear through objects, memory, scars, dialogue, documents, repeated gestures, or current scene consequences.

### POV And Information Permissions

Stay inside the current POV's eyes, body, memory, and reasonable inference.

- Do not name a newly appearing character unless the POV already knows the name or the scene supplies it through introduction, callout, label, roster, contract, public rumor, or self-introduction.
- Do not let characters say information they cannot know.
- Do not let narration explain hidden causes, future reveals, or offscreen truth unless current evidence supports it.
- Do not introduce characters as ability labels. Show what they do under pressure first.

### Dialogue Must Not Become Q&A

Avoid three or more rounds of direct question-answer exposition.

Use:

- action as answer
- silence, hesitation, or refusal
- a third person interrupting
- a character answering the thing they care about instead of the literal question
- objects changing hands, being withheld, stamped, closed, broken, or moved

Every dialogue passage should contain nonverbal pressure. Characters should not take turns reading the setting aloud.

### Character Voice Separation

Before writing dialogue, identify relationship and power distance. Characters cannot all be clever, restrained, calculating, and fluent in the same abstract vocabulary.

Check:

- What does this character notice first?
- What words belong to their work, class, age, education, fear, and relationship?
- What do they avoid saying directly?
- What action would they use instead of an explanation?

If multiple characters could swap lines without loss, revise.

### Word And Sentence Density

Do not create texture by repeating abstract key words such as rule, cost, evidence, qualification, debt, system, truth, fate, or price.

If one word has carried the emotion once, the next occurrence should become:

- a concrete object
- a body reaction
- a changed document or tool
- a silence
- a new action

Avoid repeated explanatory negation:

- not X but Y
- not because X but because Y
- does not mean Y
- cannot Y

If two nearby sentences use the same negating structure, replace the next one with action or image.

### Endings Must Not Explain The Point

Chapter endings should leave pressure, not explain meaning. Avoid closing with a thesis statement about what the scene means.

Prefer:

- a document not returned
- a door not opened
- a name written in the wrong place
- a tool left cracked
- a person choosing not to answer
- a resource running out
- a visible consequence that points to the next scene

### Word Count Is Not A Goal

If the scene chain is complete, stop. Do not add extra questions, repeated confirmations, sensory padding, or setting explanation to hit a word count. Expand only with new obstacle, new action, new misread, new choice, or new consequence.

### Power / World Scale

For genre fiction with powers, magic, cultivation, technology, or institutional force, conflict must match the character's current capability.

If a powerful character does not solve the problem directly, the reason must be visible in-world:

- exposure risk
- collateral damage
- trace evidence
- resource cost
- harm to allies
- legal, magical, social, or tactical consequence
- turning a local problem into a larger one

Do not write a high-capability character as helpless in a low-scale obstacle unless the limiting consequence is concrete.

## Writing With Style

When writing prose:

- Use `/use-novel-style {style_name}` only after the Story Engine Gate passes.
- Transfer prose mechanics only: narrative distance, syntax, rhythm, diction, dialogue, and emotion handling.
- Do not copy source names, settings, characters, protected concepts, or signature scenes.
- If the style profile conflicts with project canon or character voice, canon and character voice win.

## Reviewing With Style

When reviewing prose:

- Start with story engine: desire, resistance, choice, cost, irreversible change, next-chapter pull.
- Then check canon, POV, information permissions, character voice, and power scale.
- Then check the Universal Prose Guardrails: author-layer leakage, Q&A exposition, design-document language, same-voice dialogue, repeated abstraction, explanatory endings, and word-count padding.
- Then run or require `/eval-novel-style {style_name}` for style drift and AI-flavor assessment.

A draft can pass `eval-novel-style` and still fail as fiction.

## Review Output Order

Report findings in this order:

1. story engine pass/fail
2. whether the chapter core is functional instead of dramatic
3. visible desire, resistance, choice, cost, irreversible change
4. whether setting/rules/procedure became the main content
5. canon, POV, information boundaries, character voice, power scale
6. style fit and AI flavor from `eval-novel-style`

Do not spend the whole review on wording, forbidden terms, or POV leaks while missing that the chapter has no reason to be read.
