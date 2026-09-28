---
name: fountain-onboarding
description: Set up Fountain. Trigger on first use, when asked, when preferences are empty, or when a skill is missing something.
---

## Overview

This skill ensures that the user can effectively use Fountain API and skills.

It makes sure that:

- Fountain API is reachable.
- Fountain skills are installed.
- Project preferences are recorded.
- Relevant software is installed.
- Any other blockers are resolved.

You MUST go through each outstanding item, even if the task does not require some of the above.
This way, you do not need to ask the user again later.

## Input

- None.

## Output

- Updated preferences.
- A scheduled run of skill **fountain-daily-growth**.
- A summary in the chat: what changed, what is still missing, and who must act on it.
- A next step: return to the task that triggered this skill, or offer a first run of skill **fountain-clip-finder**.

## Housekeeping

You MUST read HOUSEKEEPING.md if you haven't already.

## Process

1. Ensure you are in a fully capable agent environment, such as Claude Code or Codex.
   Otherwise, suggest that the user uses such an environment to take full advantage of Fountain.
2. Ensure you have access to Fountain API by fetching the user's projects.
   An empty array is fine, as long as the status is 200.
   If you don't have access, install the plugin from https://github.com/fountain-fm/fountain-skills
3. Ensure you have access to Fountain skills: **fountain-clip-finder**, **fountain-clip-producer**,
   **fountain-daily-growth**, and **fountain-reports**.
   If you don't have access, install the plugin from https://github.com/fountain-fm/fountain-skills
4. Ensure that the user has at least one project.
   Otherwise, link to https://fountain.fm/studio/onboarding?kind=PODCAST
5. Ensure that the project has at least one podcast.
   Otherwise, link to https://fountain.fm/studio/{project_id}/onboarding?kind=PODCAST
6. If there are no connected social channels, suggest connecting YouTube, X, or Instagram via the Social API.
7. Ensure the project preferences specify the source of clip material, automation (auto-render, etc.),
   email addresses to send the reports to, and any other relevant details.
8. When running locally, ensure all relevant software is installed: Python 3.11 or above, yt-dlp,
   ffmpeg + ffprobe (the most complete version that includes libass, drawtext, fontconfig and whisper,
   e.g. Homebrew `ffmpeg-full`), OpenCV 4.8 or later, ImageMagick, and a whisper.cpp model file
   (`ggml-base.en.bin` in `~/.cache/whisper`).
   If something is missing, attempt to install it yourself.
   If you cannot install it, make it easy for the user to install it themselves, even if they are non-technical.
9. Research the look of the show: its artwork, its website, and its existing clips.
   Write out brand guidelines from that research.
   Choose the caption style (using skill **fountain-clip-producer**), color, and font.
   Record the guidelines, and the logo URLs if available.
   Don't include logos in the clip settings unless existing clips have them.
   Present a mockup of what the clip will look like.
   Offer to customize the style on the clip styling page.
10. Set up automatic daily growth using skill **fountain-daily-growth**.
    Record its time and the machine that runs it under Automation.

## Additional notes

Record each preference with the Project API as soon as you or the user choose it.
Any preference that the agent asks to confirm MUST already be recorded in project preferences.
Therefore, if the user leaves the chat, the choices made so far are still recorded.

Onboarding must not feel overwhelming:

- Record the Fountain defaults below.
  Then present them for the user to confirm, and offer customization as an option.
  Do not present all options unless the user chooses to customize.
- Do not provide unnecessary information.
- When appropriate, make a decision yourself but offer customization.

Fountain defaults:

- Each report delivered as email, under Reporting.
- `performance` and `review-posts-simple` as two separate reports, under Reporting.
- Auto-render on, under Automation.
- 3 clips per day, under Automation.

When no user is present, e.g. in a scheduled run, do only the steps that need no answer from the user.
Report what is still missing, so that the user can complete it in the next chat.

When this skill is triggered as part of a specific task, explain to the user why they need to go through this skill.
