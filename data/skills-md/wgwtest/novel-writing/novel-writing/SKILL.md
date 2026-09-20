---
name: novel-writing
description: Use when planning, drafting, revising, or reviewing fiction where character anchoring, viewpoint drift, implausible knowledge or decisions, unnatural dialogue, scene or chapter continuity, style fidelity, or grounded physical and institutional causality matter.
---

# Novel Writing

## Overview

Use this skill for fiction work that needs narrative craft, not just sentence-level cleanup. It is designed for three stages: planning a scene, chapter, arc, or whole story; drafting or continuing prose; and reviewing finished fiction for concrete problems.

## When to Use

Use this skill when the user asks to:

- plan a chapter, scene, arc, volume, whole-story outline, story synopsis, canon document, or reveal sequence
- continue or rewrite fiction prose
- check whether a chapter is structurally sound
- review whether characters are introduced clearly
- preserve an author's original voice while revising
- test whether a scene obeys real-world limits such as visibility, procedure, age, or capability

Do not use this skill for:

- poetry-only requests
- screenplay formatting work
- pure copyediting where narrative judgment is not needed
- non-fiction writing

## Stage Selection

First decide which stage the task belongs to.

### 1. Planning

Use when the user is deciding what a scene, chapter, arc, volume, or whole story should do before prose is written.

Read:

- `references/planning.md` for scene- or chapter-level planning
- `references/story-outline-and-causal-summary.md` for an arc, volume, or whole-story outline, a story synopsis, or a standalone canon/theory document
- `references/cognition-layers-and-language.md` when knowledge, motive, or disclosure drives decisions
- `references/scene-causality-and-agency.md` for conflict, responsibility, action order, or chapter interfaces
- `references/dialogue-and-behavior.md` when a planned meeting, interview, consultation, investigation, or technical scene could collapse into turn-taking exposition
- `references/scene-and-structure.md` when chapter flow is the main concern
- `references/realism-constraints.md` when the chapter depends on real-world limits

### 2. Drafting or Continuing

Use when the user wants new fiction prose, a rewrite of prose, or a continuation of an existing chapter.

Read:

- `references/character-introductions.md`
- `references/cognition-layers-and-language.md` when decisions or dialogue depend on unequal knowledge, judgment, or motive
- `references/scene-causality-and-agency.md` for conflict, movement, authority, or continuity
- `references/dialogue-and-behavior.md` for sustained dialogue, meetings, interviews, interrogations, domestic confrontations, or laboratory and research scenes
- `references/scene-and-structure.md`
- `references/style-fidelity.md`
- `references/realism-constraints.md` when the scene depends on real-world constraints

### 3. Reviewing

Use when the user wants critique, diagnosis, or revision advice on existing fiction.

Read:

- `references/revision-checklist.md`
- `references/dialogue-and-behavior.md` when dialogue reads like a transcript, characters take orderly turns, or the scene contains motion but little human response
- then load the specific reference files that match the problems you find

## Long-Fiction Context Strategy

When the fiction project is long enough that loading the entire formal draft would be wasteful, use context LOD instead of full-text-first reading.

### Load order

- `L0 Task`: the immediate writing or review job
- `L1 Hard constraints`: outline, timeline, setting, issue records, local project rules
- `L2 Near-field full text`: current chapter, adjacent chapters, and linked manuscript layers when fidelity matters
- `L3 Far-field structure`: chapter cards, timeline slices, and outline slices
- `L4 Cold zone`: unrelated future chapters and distant full text, excluded by default

- If you are directly revising a chapter, read that chapter's full text.
- If dialogue rhythm, psychological detail, ambiguity, flirtation, or body-detail writing matters, read the relevant full text instead of relying on summary material.
- If structure cards conflict with prose, trust the prose and update the cards later.
- If the available structured context is insufficient, expand by targeted full-text reads, not by loading the whole novel.
- Future-chapter prose is excluded by default unless a confirmed continuity dependency requires it.

### Collaboration-state discipline

For persistent chapter state, cross-session recovery, manuscript-layer synchronization, or parallel chapter ownership, use `novel-project-strategy`. Keep this skill focused on narrative work and adjacent-prose continuity.

## Hard Rules

### Reader Knowledge Is Not Author Knowledge

Never assume the reader already knows:

- who a character is
- how people are related
- what a place looks like
- why a behavior matters

If the author knows it but the prose has not shown it, treat it as missing.

### Important Characters Cannot Enter Naked

When an important character first enters the story in an effective way, the prose must give the reader enough to anchor them:

- identity or role
- relationship to the current event or viewpoint
- first impression

If the character is a villain, love interest, rival, or core ally, the prose also needs at least one recognisable trait such as:

- appearance
- clothing
- posture
- voice
- habitual gesture
- other people's reaction

### Scene Information Must Obey Access Limits

Characters may only know what the scene allows them to know.

Always separate:

- what they can see
- what they can hear
- what they can physically reach
- what they can correctly infer

Seeing something is not the same as understanding it. Getting close once is not the same as having time to inspect it.

### Cognition Must Change Choice and Language

Separate information distribution from epistemic status before consequential decisions or dialogue. Track what is shared, specialized, or private; then distinguish observation, report, judgment, intention, and misrecognition.

Use shared understanding to constrain the scene without redundant exposition, specialized understanding to change risk or available methods, and individual cognition to determine what a character chooses, hides, distorts, tests, or says. Classify all of it relative to the current character, time, and audience.

### Viewpoint Does Not Own Every Decision

Separate the experiential center, problem owner, decision owner, domain actor, and execution owner. POV determines what pressure reaches the reader first; it does not automatically grant authority, expertise, or permanent control.

Make consequential scenes legible as perception or misinterpretation, narrowed options, decision, action, consequence, and reassessment. Treat that chain as a diagnostic scaffold, not a mandatory formula or a ban on omniscient and multi-viewpoint fiction.

### Dialogue Must Happen Through Behavior

Sustained dialogue must remain embodied and consequential. A scene is not active merely because characters handle props or instruments. Distinguish functional action, which reveals strategy or changes the next beat, from decorative action and procedural action.

Do not repair transcript-like prose by attaching an emotion label or arbitrary gesture to every line. Action density is not a quality target, and beats must not be distributed evenly. Rapid dialogue may remain untagged when voice and pressure are clear. Add a behavioral beat where information lands, a lie is tested, power shifts, restraint fails, or a decision changes.

Causal and response checks are author-side diagnostics, not a sentence-by-sentence narration template. Let context, dialogue, action, and pauses carry the exchange; direct statements of silence remain valid. Use the distinctions in [Dialogue and Behavior](references/dialogue-and-behavior.md#causal-coherence-is-a-diagnostic-not-narration) rather than routinely explaining whether a remark was answered.

### Every Scene Segment Must Earn Its Place

Every chapter or functional segment should be able to answer:

- What problem is this segment handling?
- Who changes here?
- What moves forward by the end?

If the prose only accumulates content without changing the situation, treat it as structurally weak.

### Protect Style-Bearing Material

Default to preserving the author's:

- dialogue
- inner thoughts
- digressive texture
- observational details
- flirtation or ambiguity
- rhythm-bearing repetition

You may fix wording, punctuation, transcription noise, and paragraph breaks. Do not silently compress concrete material into summary.

### Review Output Must Be Specific

When reviewing fiction, report concrete findings with:

- location
- problem type
- why it fails
- how to revise it

Avoid vague comments such as "a bit stiff" or "could be improved."

### Project Rules Override This Skill

If the fiction project already has local rules, style contracts, or manuscript-layer rules, follow those first. This skill supplies general fiction method, not project-specific law.

## Working Pattern

1. Identify the stage.
2. Identify the minimum context tier needed for the task.
3. Load only the reference files needed for that stage.
4. Load project-local outline, timeline, setting, and issue files before pulling extra prose.
5. Pull near-field full prose when revising language, style, or chapter continuity.
6. Apply the hard rules before proposing prose changes.
7. If reviewing, produce structured findings before any summary.
8. When delivering plain-text manuscript files, run the bundled checker as `python <skill-directory>/scripts/check_manuscript_text.py <file-or-directory>`; review warnings instead of treating them as automatic prose defects.
9. If the task touches sensitive realism constraints and you are unsure, say what must be verified instead of bluffing.

## References

- [Planning](references/planning.md): chapter tasks, optional planning aids, and entry/exit state
- [Story Outline and Causal Summary](references/story-outline-and-causal-summary.md): story-first ordering, causal bridges, knowledge layers, and final-form outline checks
- [Cognition Layers and Language](references/cognition-layers-and-language.md): information source, epistemic status, decisions, and disclosure
- [Scene Causality and Agency](references/scene-causality-and-agency.md): POV pressure, responsibility, action topology, and continuity
- [Dialogue and Behavior](references/dialogue-and-behavior.md): embodied exchange, functional action, transcript prevention, and dialogue-heavy professional scenes
- [Character Introductions](references/character-introductions.md): first-entry rules for characters
- [Scene and Structure](references/scene-and-structure.md): scene progression and chapter shape
- [Style Fidelity](references/style-fidelity.md): preserving authorial texture during revision
- [Realism Constraints](references/realism-constraints.md): institutions, bodies, crowds, spectacle, and access limits
- [Revision Checklist](references/revision-checklist.md): structured review output and manuscript hygiene
