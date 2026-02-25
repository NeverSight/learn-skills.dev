---
name: repurpose-video
description: Repurpose a completed YouTube video into newsletter issues, social media posts, and other content formats. This is a thin orchestrator — it sequences writing:copywriting invocations with different platform references.
---

# Repurpose Video

## Overview

This orchestrator takes a completed video's content and transforms it into multi-platform content. It sequences `writing:copywriting` invocations with platform-specific references to produce newsletter issues, Twitter threads, LinkedIn posts, and Substack Notes -- all maintaining consistent voice through the writing skill's built-in voice handling.

**Core Principle**: This is a thin orchestrator. All content generation is delegated to `writing:copywriting` with the appropriate platform reference. This skill manages the workflow sequence and platform-specific decisions only.

## When to Use

Use this skill when:
- A video has been completed and you want to distribute its content across platforms
- The user asks to repurpose a video into other content formats
- You need to create a newsletter issue, social media posts, or other content from a video
- You want to maximize the reach of a single video's content

## Prerequisites

A completed video with at least one of the following available in the episode directory (`./youtube/episode/[episode_number]_[topic_short_name]/`):
- `research.md` -- research findings
- `plan.md` -- video plan with title, hook, and outline
- `transcript.md` -- video transcript
- Key points or notes provided by the user

The more source material available, the better the repurposed content will be. A transcript is the richest source, but a plan + research combination also works well.

## Repurposing Workflow

Execute all steps below in order.

### Step 1: Load Source Material

Read all available source files from the episode directory:
- `./youtube/episode/[episode_number]_[topic_short_name]/research.md`
- `./youtube/episode/[episode_number]_[topic_short_name]/plan.md`
- `./youtube/episode/[episode_number]_[topic_short_name]/transcript.md`

If the user provides additional notes or key points, incorporate those as well.

### Step 2: Extract Key Content

Synthesize the source material into a content brief:
- **Core thesis**: The main argument or insight from the video
- **Key takeaways**: 3-5 actionable insights or lessons
- **Supporting points**: Examples, data, or stories used in the video
- **Unique angle**: What makes this perspective different from existing content
- **Call to action**: What the viewer/reader should do next

This content brief will be provided as context to each downstream `writing:copywriting` invocation.

### Step 3: Newsletter Issue

**MANDATORY**: Invoke `writing:copywriting` with `references/newsletter.md` to draft a newsletter issue.

Provide the content brief and specify:
- Transform the video's content into a written newsletter format
- Adapt the structure for reading (not watching)
- Include the key takeaways in a scannable format
- Link back to the YouTube video

The `writing:copywriting` skill will automatically invoke `writing:voice` for voice consistency.

### Step 4: Twitter Thread

**MANDATORY**: Invoke `writing:copywriting` with `references/twitter.md` to draft a Twitter thread.

Provide the content brief and specify:
- Distill the video into a compelling thread (5-10 tweets)
- Lead with the most attention-grabbing insight
- Each tweet should stand alone but build on the narrative
- Include a link to the video in the final tweet

### Step 5: LinkedIn Post

**MANDATORY**: Invoke `writing:copywriting` with `references/linkedin.md` to draft a LinkedIn post.

Provide the content brief and specify:
- Adapt the video's professional insights for LinkedIn's audience
- Use a hook-based opening that stops the scroll
- Include actionable takeaways
- End with engagement prompt and video link

### Step 6: Substack Note

**MANDATORY**: Invoke `writing:copywriting` with `references/substack-notes.md` to draft a Substack Note.

Provide the content brief and specify:
- Create a concise, conversational note
- Highlight one key insight or takeaway
- Drive traffic to the full newsletter issue or video

### Step 7: Present and Save

1. Present all repurposed content to the user for review:
   - Newsletter issue
   - Twitter thread
   - LinkedIn post
   - Substack Note

2. After user approval (with any requested edits), save all content to the episode directory:
   - `./youtube/episode/[episode_number]_[topic_short_name]/repurposed.md`

The repurposed content file should contain all platform versions with clear section headers.

## Output Format

The saved `repurposed.md` file should follow this structure:

```markdown
# [Episode_Number]: [Topic] - Repurposed Content

## Source
- Video: [Title]
- Episode: [Number]
- Core Thesis: [One sentence]

## Newsletter Issue
[Full newsletter content]

## Twitter Thread
[Numbered tweets]

## LinkedIn Post
[Full LinkedIn post]

## Substack Note
[Full Substack Note]
```

## Quality Checklist

Verify completion before finalizing:
- [ ] Source material loaded (research, plan, transcript, or notes)
- [ ] Content brief extracted with core thesis, takeaways, and unique angle
- [ ] `writing:copywriting` invoked with `references/newsletter.md` -- newsletter drafted
- [ ] `writing:copywriting` invoked with `references/twitter.md` -- Twitter thread drafted
- [ ] `writing:copywriting` invoked with `references/linkedin.md` -- LinkedIn post drafted
- [ ] `writing:copywriting` invoked with `references/substack-notes.md` -- Substack Note drafted
- [ ] Voice consistency maintained across all platforms (handled by writing skill)
- [ ] Each platform's content adapts the message to its audience and format
- [ ] Video link included in all platform content
- [ ] All content presented to user for review
- [ ] Final content saved to `repurposed.md` in episode directory

## Common Pitfalls to Avoid

1. **Copy-pasting across platforms**: Each platform needs content adapted to its format and audience -- do not reuse the same text
2. **Skipping the content brief**: Jumping straight to writing without extracting key points leads to unfocused content
3. **Missing voice consistency**: Always let `writing:copywriting` handle voice through its built-in `writing:voice` invocation
4. **Forgetting video links**: Every platform piece should drive traffic back to the video
5. **Over-repurposing**: Not every video insight fits every platform -- let the writing skill adapt appropriately
