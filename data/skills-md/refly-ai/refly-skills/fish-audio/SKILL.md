---
name: fish-audio
description: "Generate AI audio using Fish Audio models. Use when you need to: (1) convert text to speech in multiple languages, (2) transcribe audio to text, or (3) create high-quality voice narration."
version: 1.0.0
skillId: skp-w8hqbfko0gi1xzyb1h9fttdl
workflowId: c-rlh0hmmpqce8squjmuoxjtj9
installationId: skpi-h7bbbys1kggo41f0b2xz237l
category: file-generation
---

# Fish Audio

Generate AI audio using Fish Audio models. Use when you need to: (1) convert text to speech in multiple languages, (2) transcribe audio to text, or (3) create high-quality voice narration.

## Input

Provide input as JSON:

```json
{
  "input_text": "The text content to convert to speech",
  "voice_style": "Voice style or characteristics for the speech output (e.g., natural, energetic, calm)",
  "audio_file": "<file-reference>"
}
```

## Execution (Pattern A: File Generation)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-h7bbbys1kggo41f0b2xz237l --input '{
  "text": "This is a sample text to convert to speech.",
  "voice_id": "default"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-rlh0hmmpqce8squjmuoxjtj9"
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
