---
name: fal-audio
description: "Generate AI audio using Fal.ai audio models. Use when you need to: (1) convert text to natural speech, (2) create podcast-style audio content, or (3) clone voices from audio samples."
version: 1.0.0
skillId: skp-rp9vuflwd7rbpz69qpes5b7q
workflowId: c-jpzyxwna765lcz547405kpa8
installationId: skpi-f2vbjqtn7q295d2ttuqve6uz
category: file-generation
---

# Fal Audio

Generate AI audio using Fal.ai audio models. Use when you need to: (1) convert text to natural speech, (2) create podcast-style audio content, or (3) clone voices from audio samples.

## Input

Provide input as JSON:

```json
{
  "text_content": "The text content to convert to speech. Can be a script, article, or any text you want to vocalize.",
  "audio_type": "Type of audio to generate: 'speech' for simple text-to-speech, 'podcast' for conversational style, or 'clone' for voice cloning",
  "voice_style": "Voice characteristics or style preferences (e.g., 'professional male', 'warm female', 'energetic narrator')",
  "reference_audio": "<file-reference>"
}
```

## Execution (Pattern A: File Generation)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-f2vbjqtn7q295d2ttuqve6uz --input '{
  "text_content": "Hello, welcome to our podcast.",
  "audio_type": "speech",
  "voice_style": "professional male"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-jpzyxwna765lcz547405kpa8"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Download and Show Result

```bash
# Get files from this run
FILES=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.files[]')

# Download and open each file
echo "$FILES" | jq -c '.' | while read -r file; do
  FILE_ID=$(echo "$file" | jq -r '.fileId')
  FILE_NAME=$(echo "$file" | jq -r '.name')
  if [ -n "$FILE_ID" ] && [ "$FILE_ID" != "null" ]; then
    refly file download "$FILE_ID" -o "$HOME/Desktop/${FILE_NAME}"
    open "$HOME/Desktop/${FILE_NAME}"
  fi
done
```

## Expected Output

- **Type**: Audio
- **Format**: .mp3/.wav audio file
- **Location**: `~/Desktop/`
- **Action**: Opens automatically to show user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
