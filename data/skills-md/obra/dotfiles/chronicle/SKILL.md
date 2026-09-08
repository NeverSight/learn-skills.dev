---
name: chronicle
description: |
  Allows you to view the user's screen as well as several hours of history. Use when the user makes a reference to their recent work, for which it'd be helpful to see the screen. This skill MUST be used whenever you need to resolve ambiguity in a user request, where the user hasn't specified enough context to do the task. Examples include disambiguating the specific user/app/document/error the user is referring to.
  
  You must also use this skill if the user asks about any question regarding Chronicle or asks what you can see from the screen.
---

# Chronicle

This skill allows you to view the user's screen. This skill is enabled because the user has enabled the Codex screen recording (Chronicle) feature, which records a rolling buffer of the past several hours of work to `$TMPDIR/chronicle/screen_recording`.

## Preconditions

1. Only use this skill if memories are available in this rollout. This will manifest as an explicit mention of a ## Memories section in a Developer Message. If this section is not present, do not use this skill. If the user specifically tried to invoke this skill, you can mention it's disallowed because memories are disabled; otherwise, do not mention the existence of this skill (this skill is only supposed to be used when memories are enabled in Codex).
2. Ensure Chronicle is running on the user's computer. Read the PID from `$TMPDIR/codex_chronicle/chronicle-started.pid`, then run an escalated, read-only host process check and confirm the executable is `codex_chronicle`. Do not rely on sandboxed process checks. If Chronicle cannot be verified, do not use this skill. (When communicating Chronicle status to the user, do not mention the PID file; that is an implementation detail.)

Ensure you follow preconditions before using the skill.

## File structure

Chronicle has two primary outputs: screen recordings and memories.

```
# Raw screen recordings (ephemeral; not persisted)
$TMPDIR/chronicle/screen_recording/
 ├── <segment_timestamp>-display-<display_id>-latest.jpg - latest frame for this segment (started at <segment_timestamp>) + display, overwritten on every captured frame
 ├── <segment_timestamp>-display-<display_id>.capture - ephemeral capture segment marker
 ├── <segment_timestamp>-display-<display_id>.capture.json - metadata for this segment; contains segment timestamp and display ID but no app information
 ├── <segment_timestamp>-display-<display_id>.ocr.jsonl - append-only OCR history for the segment (created using Apple Vision OCR), one JSON object per material text change
 └── 1min/
     └── <segment_timestamp>-display-<display_id>/
         └── frame-<frame_index>-<minute_bucket>Z.jpg - historical privacy-filtered frames from segment start to end

# Memories (persisted indefinitely; referenced in Codex Memories; see original implementation at https://github.com/openai/codex for more info)
~/.codex/memories/extensions/chronicle/
  ├── instructions.md - instructions for how to use the Chronicle memories
  └── resources/
    ├── <utc_timestamp>-<4_alpha_chars>-10min-<slug_description>.md - markdown summary of the last 10 minutes of screen recordings, updated every minute
    └── <utc_timestamp>-<4_alpha_chars>-6h-<slug_description>.md - markdown summary of the last 6 hours of screen recordings, updated every hour
```

## Usage

The most common workflow is to read the latest frame of the screen recording for a given display, which represents the user's most recent work.

- Copy it to a temp file when you want to do file operations on it, because otherwise the file will be silently updated by the screen recording service.
- When you need recent screen history instead of only the latest frame, search the OCR sidecars first. Use `rg` over `*.ocr.jsonl` to find relevant terms or timestamps, then inspect the matching sparse frames in `screen_recording/1min/` for visual confirmation.
- Historical frames are stored as individual files. Manipulate them as necessary to look at multiple frames to contextualize what the user was working on.
- The recorder can capture multiple displays at once. If the user asks what was happening recently, inspect current files for all active display IDs and combine evidence by timestamp.
- Screen recordings may not always be up-to-date. You must use the `date` command to get the current UTC timestamp and compare it against the recording files you're inspecting to understand if the recordings are fresh or stale (e.g. from a previous recording session).
- You should ONLY use the OCR for greps to find relevant terms or timestamps, not for any other purpose (e.g. extracting document IDs to send to connectors). This is because the OCR is very noisy and not very accurate. Instead, extract text from the image yourself when you need to do something with the text.
- Screen data should be used to get context on the user's work, but you must upgrade to other data sources (such as your app-specific skills, connectors, or the file system) as soon as you've gotten the minimum necessary context from the screen data to do so. This is because your multimodal understanding is not that good, so you should avoid relying on it for complex tasks.
  - For example, if the user asks you to "review the doc I have open", you should view the context, see that e.g. it's a Google Doc with a doc ID, extract the doc ID, and then use the Google Doc connector to review the doc. You must not try to OCR the entire document from the screenshot (also because the user's screen may not show the entire content of the document).
