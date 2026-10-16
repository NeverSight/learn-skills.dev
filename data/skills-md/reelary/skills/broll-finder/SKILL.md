---
name: broll-finder
description: 'Pull b-roll from the user''s own footage library for a voiceover, interview, podcast or talking-head video. Matches each line of narration to cutaway shots by meaning, 100% local on Mac or Windows. Trigger on "b-roll", "broll", "cutaways", "cover shots", "find b-roll for my voiceover", "illustrate this script with my clips", "inserts for my interview". Not for downloading stock footage or generating AI clips.'
---

# B-roll finder

## Steps

1. Get the narration text (ask for it if missing). Split it into beats of one idea each.
2. For each beat call `reelary_search` with a visual description of what should be on screen, not the spoken words ("aerial city at dusk" for "our city never sleeps"). Use `limit: 5`.
3. Present a table: beat, best clip (path + `mm:ss-mm:ss`), one alternative. Flag beats with no good match.
4. If the user wants a timeline, build it with [rough-cut](../rough-cut/SKILL.md) using the beats as the script; for Premiere/Resolve handoff use [nle-export](../nle-export/SKILL.md).

## Without MCP

`npx -y reelary search "<visual description>" --json` per beat.

## Notes

If the `reelary_*` tools are missing or nothing is indexed, use the [reelary](../reelary/SKILL.md) skill first.
