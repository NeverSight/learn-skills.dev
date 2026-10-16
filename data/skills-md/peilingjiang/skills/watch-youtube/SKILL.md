---
name: watch-youtube
description: Learn from YouTube videos by extracting transcripts and presenting structured knowledge. Use when users share YouTube URLs or ask about video tutorials.
license: MIT
compatibility: Requires Python 3.8+ and pip packages (youtube-transcript-api, requests, beautifulsoup4)
allowed-tools: Bash(python:*) Read Write Edit Glob
---

# Watch YouTube

Extract knowledge from YouTube videos and present it in the conversation.

## Quick Reference

| User Intent                       | Action                               |
| --------------------------------- | ------------------------------------ |
| Shares YouTube URL(s)             | Extract and present knowledge        |
| "search/find videos about X"      | Search → show results → user picks   |
| "watch videos about X"            | Search → watch top results           |
| "save as skill" / "remember this" | Save extracted knowledge as SKILL.md |

---

## Step 1: Get Video(s)

### Option A: User Provides URL(s)

Extract transcript from each URL:

```bash
python {{SKILL_DIR}}/scripts/transcript.py "VIDEO_URL"
```

### Option B: User Wants to Search

```bash
python {{SKILL_DIR}}/scripts/search.py "QUERY" --max-results 5
```

Then either:

- **"watch videos about X"** → Auto-select top 3 (or top 1 if "a video")
- **"search/find videos about X"** → Show list, let user choose

After selection, extract transcripts for chosen video(s).

---

## Step 2: Extract Knowledge

Analyze the transcript(s) and extract the knowledge (either to use for the next steps or present to the user based on the context):

1. **Summary** - What the video teaches (2-3 sentences)
2. **Key Steps** - Actionable instructions with commands/code
3. **Important Concepts** - Core ideas explained clearly
4. **Warnings** - Common pitfalls mentioned
5. **Tips** - Pro recommendations from the video

For multiple videos: combine insights, deduplicate overlapping concepts, note differing perspectives.

---

## Step 3: Save as Skill (Only When Requested)

**Default behavior: Use knowledge for the ongoing tasks, do not save files.**

Only save when user explicitly asks with phrases like:

- "save this as a skill"
- "remember this for later"
- "make it a skill"

### To Save:

1. Read the extraction prompt: [references/extract-knowledge.md](references/extract-knowledge.md)

2. Read the appropriate template:
   - Single video: [assets/templates/skill-single.md](assets/templates/skill-single.md)
   - Multiple videos: [assets/templates/skill-series.md](assets/templates/skill-series.md)

3. Ask where to save:
   - **Project** (default): `.claude/skills/{skill-name}/SKILL.md`
   - **Personal**: `~/.claude/skills/{skill-name}/SKILL.md`

4. Save and confirm with skill name and how to invoke it (`/skill-name`)

5. Remind the user that the skill can only be loaded when Claude Code is reloaded

---

## Error Handling

| Error                     | Solution                  |
| ------------------------- | ------------------------- |
| "No transcript available" | Suggest alternative video |
| "Video not found"         | Ask user to verify URL    |
| "Module not found"        | Run setup command below   |

### First-Time Setup

```bash
pip install -r {{SKILL_DIR}}/scripts/requirements.txt
```
