---
name: build-taste
description: Open a temporary canvas to collect a project's visual references, then turn its images, sites, and notes into a persistent taste skill. Use when someone wants to start, build, or refresh their design taste for a coding project.
---

# Build Taste

Use this skill in the project whose interface the person is building. The canvas runs on their machine for this session and writes only a `taste` skill folder inside that project. They do not need an existing taste file or a hosted account.

1. Resolve the project root. Use the current project unless the person names another. Choose `--agent agents` for Codex, Cursor, and agents that read `.agents/skills/`; choose `--agent claude` for Claude Code. When both are present, use the folder their current coding agent reads.
2. Start `node <this-skill-folder>/scripts/canvas-server.mjs --project <absolute-project-root> --agent <agents|claude>` as a long-running process. It prints a `TASTE_CANVAS_URL`. Open that URL in the person's browser if your tools allow it; otherwise give them the URL. Keep the process running while they paste images, drop screenshots, add site links and notes, write what they like about each reference, and group the ones that belong together. The canvas saves changes to the project as they go.
3. Wait for the person to click **Finish and build taste**. The process prints `TASTE_BOARD_READY` and exits. If the page is closed without Finish, the process prints `TASTE_CANVAS_CLOSED` after 20 quiet minutes and exits; the board is saved, so read it the same way, or ask whether they want to keep going. The board stays open in their browser and keeps saving into the project (a quiet copy of the server takes over, closes itself after 20 idle minutes, and is replaced on the next run); anything changed after Finish is read next time. If they stop early, their saved board remains in the project; resume the canvas next time.
4. Read `board/BOARD.md` in the created taste folder. Open each new image it lists (a site's own preview picture is listed with it), visit site links when available, and treat the person's notes, “why” lines and group names as the strongest evidence. Things in one group were put together on purpose: ask what they share before what each one is. Read the existing `SKILL.md` before editing it. Add grounded, actionable patterns and measurements to its Taste, Visual system, Type, Layout, Motion, or Copy sections. Record each processed reference under From the board. Preserve existing rules, corrections, and dated taste log entries. Do not invent preferences from a single ambiguous example.
5. Tell the person what you learned and where `SKILL.md` and their references now live. On later runs, the canvas loads the existing board; saving it never overwrites the agent's `SKILL.md`.

The local canvas script needs Node.js 20 or newer. It has no package dependencies. It binds only to `127.0.0.1`, uses a one-session URL token, and never sends the person's files to a Tasteboard server.
