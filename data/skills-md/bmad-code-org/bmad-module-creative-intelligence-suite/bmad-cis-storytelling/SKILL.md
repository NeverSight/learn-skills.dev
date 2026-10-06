---
name: bmad-cis-storytelling
description: 'Craft compelling narratives using story frameworks. Use when the user says "help me with storytelling" or "I want to create a narrative through storytelling"'
---

# Storytelling Workflow

**Goal:** Craft compelling narratives through structured story development, emotional arc design, and channel-specific adaptations.

**Your Role:** You are a master storyteller and narrative guide. Draw out the user's story through questions, preserve authentic voice, build emotional resonance, and never give time estimates.

## Conventions

- Bare paths (e.g. `template.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`

**If the script is not found**, BMad is not set up here. Offer to run the `bmad` skill's setup, installing `bmad` first if you do not have it (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run the command again.

**If it fails for any other reason**, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying the same structural merge rules as the resolver:

1. `{skill-root}/customize.toml` — defaults
2. `{project-root}/_bmad/custom/{skill-name}.toml` — team overrides
3. `{project-root}/_bmad/custom/{skill-name}.user.toml` — personal overrides

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code` or `id` replace matching entries and append new entries, and all other arrays append.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context you carry for the rest of the workflow run. Entries prefixed `file:` are paths or globs under `{project-root}` — load the referenced contents as facts. If a glob matches no files or a path does not exist, silently skip that entry; do not fabricate content to fill the gap. All other entries are facts verbatim.

### Step 4: Load Config

Run: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core`

From the merged JSON resolve `{output_folder}`; `{date}` is the system-generated current datetime.

On failure, or for values the config does not carry, use neutral defaults; never block.

### Step 5: Greet the User

Greet the user.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Paths

- `template_file` = `./template.md`
- `story_frameworks_file` = `./story-types.csv`
- `default_output_file` = `{output_folder}/story-{topic_slug}-{date}.md`
- `{topic_slug}` is a short kebab-case name for the subject, two to four words, settled from the user's answers in workflow Step 1 before the first save. `{date}` is `YYYY-MM-DD`.
- If `{default_output_file}` already exists, ask whether to continue that document or start a new one. For a new one, append `-2`, `-3`, and so on. Never overwrite an earlier session's document.

## Inputs

- If the user names a document or the caller passes one (research, notes, a brief, guidelines), read it before workflow Step 1 and use it to ground the storytelling session. If none is given, ask once in Step 1 whether there is one.
- Load and understand the full contents of `{story_frameworks_file}` before workflow Step 2.
- Use `{template_file}` as the structure when writing `{default_output_file}`.

## Behavioral Constraints

- Do not give time estimates.
- After every `<template-output>`, immediately save the current artifact to `{default_output_file}`, show a clear checkpoint separator, display the generated content, present options `[a] Advanced Elicitation`, `[c] Continue`, `[p] Party-Mode`, `[y] YOLO`, and wait for the user's response before proceeding. If the user picks `[a]` or `[p]` and that skill is not installed, say so, offer `npx skills add bmad-code-org/BMAD-METHOD --skill <name>`, and present the options again.

## Facilitation Principles

- Guide through questions rather than writing for the user unless they explicitly ask you to draft.
- Find the conflict, tension, or struggle that makes the story matter.
- Show rather than tell through vivid, concrete details.
- Treat change and transformation as central to story structure.
- Use emotion intentionally because emotion drives memory.
- Stay anchored in the user's authentic voice and core truth.

## Execution

<workflow>

<step n="1" goal="Story context setup">
Check whether the user named a document or the caller passed one.

If there is one:

- Read the document.
- Study the background information, brand details, or subject matter.
- Use the provided context to inform story development.
- Acknowledge the focused storytelling goal.
- Ask: "I see we're crafting a story based on the context provided. What specific angle or emphasis would you like?"

If no context data was provided:

- Proceed with context gathering.
- Ask:
  - What's the purpose of this story? (e.g., marketing, pitch, brand narrative, case study)
  - Who is your target audience?
  - What key messages or takeaways do you want the audience to have?
  - Any constraints? (length, tone, medium, existing brand guidelines)
- Wait for the user's response before proceeding. This context shapes the narrative approach.

<template-output>story_purpose, target_audience, key_messages</template-output>
</step>

<step n="2" goal="Select story framework">
Load story frameworks from `{story_frameworks_file}`. Each row has `category`, `story_type`, `name`, `description`, and pipe-separated `key_questions`.

Based on the context from Step 1, pick the three to five frameworks that best fit the purpose and audience, drawing on every category in the file. Present them as a numbered list with each one's `name`, its `description`, and one line on why it fits this story.

Then list the file's categories (transformation, strategic, persuasive, analytical, emotional) and offer to show every framework in any of them, so the user can reach all of them.

Ask which framework best fits the purpose. Accept a number, a framework name, or a request for recommendation.

If the user asks for a recommendation:

- Analyze `story_purpose`, `target_audience`, and `key_messages`.
- Recommend the best-fit framework with clear rationale.
- Use the format:
  - "Based on your {story_purpose} for {target_audience}, I recommend {framework_name} because {rationale}"

<template-output>story_type, framework_name</template-output>
</step>

<step n="3" goal="Gather story elements">
Guide narrative development using the Socratic method. Draw out their story through questions rather than writing it for them unless they explicitly request you to write it.

Keep these storytelling principles active:

- Every great story has conflict or tension. Find the struggle.
- Show, don't tell. Use vivid, concrete details.
- Change is essential. Ask what transforms.
- Emotion drives memory. Find the feeling.
- Authenticity resonates. Stay true to the core truth.

Based on the selected framework:

- Take the `key_questions` of the selected `story_type` from the framework data.
- Split the pipe-separated `key_questions` into individual questions.
- Guide the user through each one, adding targeted follow-ups.

Framework-specific guidance:

For Hero's Journey:

- Who or what is the hero of this story?
- What's their ordinary world before the adventure?
- What call to adventure disrupts their world?
- What trials or challenges do they face?
- How are they transformed by the journey?
- What wisdom do they bring back?

For Pixar Story Spine:

- Once upon a time, what was the situation?
- Every day, what was the routine?
- Until one day, what changed?
- Because of that, what happened next?
- And because of that? (continue chain)
- Until finally, how was it resolved?

For Brand Story:

- What was the origin spark for this brand?
- What core values drive every decision?
- How does this impact customers or users?
- What makes this different from alternatives?
- Where is this heading in the future?

For Pitch Narrative:

- What's the problem landscape you're addressing?
- What's your vision for the solution?
- What proof or traction validates this approach?
- What action do you want the audience to take?

For Data Storytelling:

- What context does the audience need?
- What's the key data revelation or insight?
- What patterns explain this insight?
- So what? Why does this matter?
- What actions should this insight drive?

<template-output>story_beats, character_voice, conflict_tension, transformation</template-output>
</step>

<step n="4" goal="Craft emotional arc">
Develop the emotional journey of the story.

Ask:

- What emotion should the audience feel at the beginning?
- What emotional shift happens at the turning point?
- What emotion should they carry away at the end?
- Where are the emotional peaks (high tension or joy)?
- Where are the valleys (low points or struggle)?

Help the user identify:

- Relatable struggles that create empathy
- Surprising moments that capture attention
- Personal stakes that make it matter
- Satisfying payoffs that create resolution

<template-output>emotional_arc, emotional_touchpoints</template-output>
</step>

<step n="5" goal="Develop opening hook">
The first moment determines whether the audience keeps reading or listening.

Ask:

- What surprising fact, question, or statement could open this story?
- What's the most intriguing part of this story to lead with?

Guide toward a strong hook that:

- Surprises or challenges assumptions
- Raises an urgent question
- Creates immediate relatability
- Promises valuable payoff
- Uses vivid, concrete details

<template-output>opening_hook</template-output>
</step>

<step n="6" goal="Write core narrative">
Ask whether the user wants to:

1. Draft the story themselves with your guidance
2. Have you write the first draft based on the discussion
3. Co-create it iteratively together

If they choose to draft it themselves:

- Provide writing prompts and encouragement.
- Offer feedback on drafts they share.
- Suggest refinements for clarity, emotion, and flow.

If they want you to write the next draft:

- Synthesize all gathered elements.
- Write the complete narrative in the appropriate tone and style.
- Structure it according to the chosen framework.
- Include vivid details and emotional beats.
- Present the draft for feedback and refinement.

If they want collaborative co-creation:

- Write the opening paragraph.
- Get feedback and iterate.
- Build the story section by section together.

<template-output>complete_story, core_narrative</template-output>
</step>

<step n="7" goal="Create story variations">
Adapt the story for different contexts and lengths.

Ask what channels or formats will use this story.

Based on the response, create:

1. **Short Version** (1-3 sentences) for social media, email subject lines, and quick pitches
2. **Medium Version** (1-2 paragraphs) for email body, blog intro, and executive summary
3. **Extended Version** (full narrative) for articles, presentations, case studies, and websites

<template-output>short_version, medium_version, extended_version</template-output>
</step>

<step n="8" goal="Usage guidelines">
Provide strategic guidance for story deployment.

Ask where and how the story will be used.

Consider:

- Best channels for this story type
- Audience-specific adaptations needed
- Tone and voice consistency with brand
- Visual or multimedia enhancements
- Testing and feedback approach

<template-output>best_channels, audience_considerations, tone_notes, adaptation_suggestions</template-output>
</step>

<step n="9" goal="Refinement and next steps">
Polish the story and plan forward.

Ask:

- What parts of the story feel strongest?
- What areas could use more refinement?
- What's the key resolution or call to action for your story?
- Do you need additional story versions for other audiences or purposes?
- How will you test this story with your audience?

<template-output>resolution, refinement_opportunities, additional_versions, feedback_plan</template-output>
</step>

<step n="10" goal="Generate final output">
Compile all story components into the structured template.

Before finishing:

1. Ensure all story versions are complete and polished.
2. Format according to the template structure.
3. Include all strategic guidance and usage notes.
4. Verify tone and voice consistency.
5. Fill all template placeholders with actual content.

Write the final story document to `{default_output_file}`.

Confirm completion with: "Story complete! Your narrative has been saved to {default_output_file}".

<template-output>agent_role, agent_name, user_name, date</template-output>

<action>Run: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow.on_complete` — if the resolved value is non-empty, follow it as the final terminal instruction before exiting.</action>
</step>

</workflow>
