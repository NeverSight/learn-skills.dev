---
name: plan-video
description: Orchestrate foundation skills to create a complete YouTube video plan. This is a thin orchestrator — it sequences skill invocations and manages the user selection workflow, but delegates all content generation to foundation skills.
---

# Plan Video

## Overview

This orchestrator sequences foundation skills to produce a complete video plan: researched titles, thumbnail concepts, hook strategies, and a content outline. It manages the user selection workflow between steps but delegates all content generation to specialized skills.

**Core Principle**: This is a thin orchestrator. Never generate titles, thumbnails, hooks, or outlines manually. Always delegate to the appropriate foundation skill.

## YouTube-Specific Context

### Episode Directory Convention

All episode files live under `./youtube/episode/[episode_number]_[topic_short_name]/`.

- **Research file**: `research.md` in the episode directory
- **Plan file**: `plan.md` in the episode directory
- **Thumbnails**: saved to the episode directory during finalization

### Channel Information

If a local channel context file exists (e.g., `./youtube/channel.md` or similar), load it at the start of the workflow to provide channel-specific context to downstream skills.

## YouTube MCP Tools Available

When `content-strategy:research` is invoked from this orchestrator, the YouTube Analytics MCP tools are available for data gathering. These tools provide access to:

- `search_videos` -- find videos by keyword, channel, or criteria
- `get_video_details` -- video stats, views, likes, comments, publish date
- `get_channel_details` -- channel metadata, subscriber count, video count
- `get_video_comments` -- comment text and sentiment data
- `get_video_transcript` -- full video transcript
- `get_related_videos` -- videos related to a specific video
- `get_trending_videos` -- currently trending videos
- `get_video_enhanced_transcript` -- enhanced transcript with timestamps

The YouTube Researcher agent (defined in this plugin's `agents/youtube-researcher.md`) can also be used for structured data gathering tasks.

## When to Use

Use this skill when:
- Research has been completed and you need to create a video plan
- The user asks to plan a new video
- You need title, thumbnail, hook, and outline options for a video
- You want to produce a production-ready plan with multiple options for user selection

## Prerequisites

**MANDATORY**: Research for the video must be completed first. Either:
1. Research file exists at `./youtube/episode/[episode_number]_[topic_short_name]/research.md`, OR
2. Invoke `content-strategy:research` to conduct research first (YouTube MCP tools are available)

## Planning Workflow

Execute all steps below in order. Track progress systematically.

### Step 0: Load Research

Read the research file for this episode:
- Location: `./youtube/episode/[episode_number]_[topic_short_name]/research.md`

If research does not exist, invoke `content-strategy:research` first. The YouTube MCP tools are available from this orchestrator context, enabling the research skill to gather YouTube-specific data.

The video plan **MUST** incorporate research findings at each step.

### Step 1: Create Plan File

Create a new plan file at: `./youtube/episode/[episode_number]_[topic_short_name]/plan.md`

If a plan file already exists, read it to understand what has been done so far and continue from there.

Initialize the plan file with this template:

```markdown
# [Episode_Number]: [Topic] - Video Plan

## Research Summary
[Summary of research insights]

## Titles
[3 title options with rationale and star ratings]

## Thumbnails
[2 thumbnail concepts per title with rationale and star ratings]

## Hooks
[3 hook options for selected title+thumbnail with rationale and star ratings]

## High-Level Content Outline
[Section structure with key points]

## Final Plan
[Selected title, 3 AB test thumbnails, selected hook, outline]
```

Update this document as you progress through the planning steps.

### Step 2: Generate Title Options

1. **MANDATORY**: Invoke `content-strategy:title` to generate 3 optimized titles.
   - The skill will automatically load `references/youtube-title-formulas.md` for proven title patterns.
   - Provide the research summary as context.

2. Document all title options in the plan file including:
   - Title text
   - Rationale for why it is predicted to perform well and how it aligns with research insights
   - Star rating from 1-3 stars indicating your recommendation

**NOTE**: You MUST complete title generation before proceeding to thumbnails, as thumbnails need to complement the titles.

### Step 3: Generate Thumbnail Concepts

1. **MANDATORY**: Invoke `visual-design:thumbnail` to generate 2 thumbnail concepts for each title. These should be concept descriptions only, not actual images yet.
   - The skill will automatically load `references/thumbnail-formulas.md` for proven thumbnail patterns.
   - Provide each title as context so thumbnails complement them.

2. Document all thumbnail concepts in the plan file including:
   - Title pairing
   - Concept description
   - Rationale for why it is predicted to perform well, how it aligns with research, and how it complements the title
   - Star rating for top 3 thumbnail concepts

### Step 4: Present Recommendation and Get User Selection

1. Present all title/thumbnail combinations to the user, along with your top 3 recommended title + thumbnail pairings.

2. Ask the user to select their one preferred title + thumbnail pairing to proceed with.

3. Update both the title and thumbnail sections in the plan file to indicate the user's selection with a (User Selection) marker next to the selected options.

**CRITICAL**: Present ALL options so the user can make an informed decision. Do not simply select one option and tell the user to use it.

### Step 5: Generate Hook Strategy

1. **MANDATORY**: Invoke `content-strategy:hook` to generate 3 retention-optimized hooks, only for the user's selected title + thumbnail pairing.
   - The skill will automatically load `references/youtube-hooks.md` for proven hook patterns.
   - Provide the selected title + thumbnail concept as context.

2. Document all hook strategies in the plan file including:
   - Hook strategy description (including the actual hook script)
   - Rationale for why it is predicted to perform well, how it aligns with research, and how it complements the title + thumbnail
   - Star rating for each hook

3. Present all hook options to the user and ask the user to select their preferred hook strategy.

4. Update the hook section in the plan file to indicate the user's selection.

The plan should now contain a user-selected title, thumbnail, and hook combination.

### Step 6: High-Level Content Outline

1. **MANDATORY**: Invoke `writing:copywriting` to create a high-level content outline.
   - The skill will automatically load `references/youtube-script.md` for proven script structure patterns.
   - Provide the selected title, thumbnail concept, and hook as context.

2. Create and document the strategic roadmap:
   - Break video into sections (Hook, Intro, Main Content, Outro)
   - List key points and estimated durations
   - Identify critical demonstrations/examples
   - Note transitions

3. Keep the outline **VERY HIGH-LEVEL**. Structure and key points only, no detailed scripts. Do not assume specific content that should be covered -- leave that to the content creator. Focus on what is important to cover from the viewer's perspective.

### Step 7: Finalize Plan with AB Testing Thumbnails

Now that the user has selected their preferred title, thumbnail, and hook, finalize the plan.

1. **MANDATORY**: Invoke `visual-design:thumbnail` to generate 3 thumbnail options for AB testing. These should be actual images generated with `art:nanobanana`, not just concepts. The first thumbnail should be based on the user's selected thumbnail concept. The other 2 should test different visual styles of the first thumbnail.

2. Update the final plan section in the plan file with the complete final selections:

```markdown
## Final Plan
- **Title**: [Selected title]
- **Thumbnails**:
   - ![Thumbnail A](/path/to/thumbnail_a.png)
      Thumbnail A Description
   - ![Thumbnail B](/path/to/thumbnail_b.png)
      Thumbnail B Description
   - ![Thumbnail C](/path/to/thumbnail_c.png)
      Thumbnail C Description
- **Hook**: [Selected hook strategy]
- **Rationale**: [Why this combination works]
```

A final selection should **ALWAYS** have 3 thumbnails to test.

## Execution Guidelines

### Always Invoke Foundation Skills

**NEVER** generate titles, thumbnails, hooks, or outlines manually. Always invoke:
- `content-strategy:title` for title generation
- `visual-design:thumbnail` for thumbnail concepts and images
- `content-strategy:hook` for hook strategies
- `writing:copywriting` for content outline

### Provide Multiple Options

**CRITICAL**: Always include ALL options so the user can make an informed decision. Do not simply select one option and tell the user to use it.

### Ensure Complementarity

Verify that title/thumbnail/hook work together:
- Thumbnail complements title visually
- Hook extends curiosity (does not repeat title)
- All elements align with the unique value proposition

### Back Recommendations with Research

When recommending combinations:
- Reference content gaps from research
- Cite competitor insights
- Explain how the combination addresses the opportunity

## Quality Checklist

Verify completion before finalizing plan:
- [ ] Research file loaded and reviewed
- [ ] `content-strategy:title` invoked -- 3 title options generated
- [ ] `visual-design:thumbnail` invoked -- 2 thumbnail concepts per title
- [ ] User selected title + thumbnail pairing
- [ ] `content-strategy:hook` invoked -- 3 hook strategies generated
- [ ] User selected hook strategy
- [ ] `writing:copywriting` invoked -- high-level content outline created
- [ ] `visual-design:thumbnail` invoked -- 3 AB testing thumbnails generated
- [ ] Plan file complete with all sections populated
- [ ] Recommendations marked by star rating
- [ ] Title/thumbnail/hook complementarity verified
- [ ] Recommendations backed by research insights

## Common Pitfalls to Avoid

1. **Skipping Skill Invocation**: Generating titles/thumbnails/hooks manually -- must invoke foundation skills
2. **Single Option**: Only providing one recommendation -- provide all options to the user along with your recommendations
3. **Missing Research**: Starting without research -- load research or invoke research skill first
4. **Ignoring Complementarity**: Title/thumbnail/hook don't work together -- verify alignment
5. **No Rationale**: Recommendations without explanation -- back with research insights
6. **Too-Detailed Outline**: Writing a full script instead of high-level structure -- keep it strategic

## Example Execution

**Scenario**: User requests plan for video about "Building AI agents with memory" (research already complete)

1. Load research -- Read `./youtube/episode/18_ai_agents_with_memory/research.md`, extract key insights
2. Create plan file at `./youtube/episode/18_ai_agents_with_memory/plan.md`
3. Invoke `content-strategy:title` -- 3 title options focused on practical implementation
4. Invoke `visual-design:thumbnail` -- 2 concepts per title (6 total)
5. Present all options, user selects title + thumbnail pairing
6. Invoke `content-strategy:hook` -- 3 hook strategies for selected pairing
7. User selects hook
8. Invoke `writing:copywriting` -- high-level content outline
9. Invoke `visual-design:thumbnail` -- 3 AB testing thumbnails for final plan
10. Update plan file with complete final selections

**Result**: Production-ready plan with multiple options for user selection, all backed by research and generated using proven patterns from foundation skills.
