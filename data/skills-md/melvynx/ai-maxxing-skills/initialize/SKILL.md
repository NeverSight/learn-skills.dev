---
name: initialize
description: Install the base skills every agent should have, globally and in one command - /initialize itself (so it can be rerun), skill-manager, /show-me, /grill-me, /wait-what, /connect-tool and /use-style, all from this kit - plus the settings that stop Claude Code and Codex from asking before each action, the cc / cx shortcuts, the usage band above the prompt in the Claude desktop app and the terminal status bar (context, cost, 5-hour and weekly limits), then asks the user which visual style they like and makes it the default for every file the agent creates. Use when the user types /initialize, sets up a new computer, says "installe les skills de base" or before setup-brain.
---

Give every agent on this computer the base skills, in every folder. Do it yourself and talk to the user in their language, short, no jargon (never say "symlink" or "npx" to them).

If you got this skill from a link instead of a local folder, install nothing else from the repo: the one command below downloads what it needs.

1. Check Node: if `npx --version` fails, run the `setup-node` skill first (from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/setup-node/SKILL.md` when it is not installed).
2. Run the one command, in the background when your tool allows it (2 to 5 minutes):
   ```bash
   curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/initialize/scripts/initialize.sh -o /tmp/initialize.sh && bash /tmp/initialize.sh
   ```
   (Downloaded first, then run: a previous `/initialize` blocks piping a download straight into `bash`.)
   Everything comes from this kit, except Bun (it runs the status bar), installed from its official site `bun.sh` when missing. It installs, for Claude Code and Codex:
   - the skills: `/initialize` itself (so the user can run it again to update everything), `skill-manager` (installs, updates or removes a skill from a name or a link, and creates or fixes their own skills), `/show-me` (explains anything with a small diagram or visual), `/grill-me` (sharpens an idea with questions before building), `/wait-what` (re-explains the last message in plain words when the user is lost), `/connect-tool` (connects any tool like Notion or Stripe) and `/use-style` (gives pages, apps and documents a named visual style like Vercel, Stripe or Linear);
   - the settings: Claude Code and Codex stop asking before each action, while Claude Code still refuses `rm -rf`, `sudo`, piping a download into the terminal and reading `.env` files (their other settings are kept);
   - the shortcuts in the terminal: `cc` opens Claude Code without questions, `ccc` continues the last conversation, `cx` opens Codex, `cxc` resumes the last Codex one;
   - the usage band above the prompt, in the Claude desktop app and in the terminal: context used, cost of the conversation, and the 5-hour and weekly limits with their pace and reset time. It is a Claude Code mod in `~/.claude/mods/aiblueprint` (the folder AIBlueprint uses, so a student who has both never sees it twice), turned on through `CLAUDE_CODE_PLUGIN_DIRS` in `~/.claude/settings.json`; the ⚙ button on the band hides or shows each part;
   - the status bar under the Claude Code prompt in the terminal: folder, git branch, model, cost, context and limits. It runs with Bun from `~/.claude/scripts/statusline`; a rerun updates it and keeps its settings, and a status bar the user set up themselves is kept (`kept your own status bar`).
   The band and the status bar show only in a new session (in the desktop app, start a new session or reopen the app).

   **If you may not change the permission settings yourself** (your rules forbid turning on bypass permissions or the Codex full access), do not stop and do not look for a workaround: run `NO_BYPASS=1 bash /tmp/initialize.sh` instead. It installs everything except those two settings. Then tell the user to turn them on themselves:
   - Claude desktop app: **Settings → Claude Code**, turn on **Allow bypass permissions mode**, then pick **Bypass permissions** in the mode menu next to the message box.
   - Codex: pick **Full access** in the permissions menu under the message box.

   On Windows without bash, run the `npx skills add` line of [scripts/initialize.sh](scripts/initialize.sh) in PowerShell, add the same keys to `~/.claude/settings.json` and `~/.codex/config.toml` by hand, and put the shortcuts in the PowerShell profile (`notepad $PROFILE`) as `function cc { claude --dangerously-skip-permissions $args }`, `function ccc { claude --dangerously-skip-permissions -c $args }`, `function cx { codex $args }`, `function cxc { codex resume --last $args }`. The band and the status bar are only installed by the bash script: tell the user they will not have them.
3. Every skill lands once in `~/.agents/skills/` (the single source, Codex reads it there), and `~/.claude/skills/` only links to it. The script ends with an `ok` or `MISS` line per skill: fix a `FAIL` or `MISS` by rerunning its line and reading the error, never by copying files by hand into `~/.claude/skills`. An `old=` line lists developer skills an older `/initialize` installed (apex, arena, app-icon...): they are not part of the kit anymore. Ask once whether to remove them; on yes run `bash ~/.agents/skills/skill-manager/scripts/skills.sh remove <names>` (they are kept in `~/.cache/removed-skills`, so it can be undone). Never remove them without asking: they may be the user's own.
4. **Style.** Open the style gallery so the user sees every style side by side: `~/.agents/skills/use-style/examples/gallery.html` (`open` on Mac, `xdg-open` on Linux, `start` on Windows). Ask one question: which style speaks to them most, the one they would like for their pages, apps and documents. Give the names with their one-line description from the gallery, and say they can click a card to see it full size. When they hesitate, recommend `vercel`. When `~/.agents/AGENTS.md` already has a `## Style` section, show its style and ask only whether to keep it.
5. **Global rule.** Write their choice in the global rules, `~/.agents/AGENTS.md` (create it when missing; `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` link to it once `setup-brain` ran). When it already has a `## Style` section, replace that section up to the next `## ` heading and keep every other line; otherwise add it at the end, after one blank line:
   ```markdown
   ## Style

   When you create a file the user will look at (a page, an app screen, a dashboard, an HTML report, a document, a visual), use the `use-style` skill with the `<chosen style>` style, unless the user asks for another one or the project already has its own design.
   ```
   When `~/.claude/CLAUDE.md` is a separate file (not a link to `~/.agents/AGENTS.md`), write the same section there too.
6. Tell the user in 3 lines what is installed (and that `cc`, the usage band and the status bar show up in a new terminal window / new Claude Code session, in the desktop app too), that a new session shows `/show-me`, `/grill-me`, `/wait-what`, `/connect-tool`, `/use-style`, `/skill-manager` and `/initialize`, which style is now their default (they can change it any time by asking), and that typing `/initialize` again later updates the skills, the status bar and the usage band.
