---
name: short-drama-skill-finder
description: Recommend AI short drama, micro drama and manju (漫剧) skills from a hand-checked list of 90+ projects, matched to the user's stage (novel adaptation, episode outlines and hooks, script writing, review, storyboards, character consistency, video prompts, production), video model (Seedance/即梦, Kling/可灵, MiniMax, Wan, Veo, Sora, ComfyUI) and agent (Claude Code, Codex, OpenClaw/龙虾, Qwen, Doubao, WorkBuddy). Use when someone asks which skill or tool to use for an AI short drama or 短剧/漫剧, or how to install one. 帮你从人工核对过的短剧、漫剧 skill 清单里挑合适的：小说改编、集纲钩子、剧本、审稿、分镜、角色一致性、视频提示词、出片。
---

# Short drama skill finder

Pick skills for an AI short drama project from the Awesome Short Drama Skills list (https://shortdramaskills.com). Every entry in the list was checked by hand and tagged by type, production stage, video model and supported agents.

## 1. Get the data

Fetch `https://shortdramaskills.com/data.json`. If that fails, read the same list from `https://raw.githubusercontent.com/UnderleveledBuilder/awesome-short-drama-skills/main/README.md` (English: `README.en.md`), which has the same entries without the structured fields.

`data.json` has `updated`, `taxonomy` (labels for `types`, `stages` and `models` in `zh` and `en`) and `items`. Each item has:

| Field | Meaning |
|---|---|
| `repo`, `github` | GitHub repo |
| `desc`, `overview`, `note` | Summary, longer overview and editor's note, each with `zh` and `en` (`note` may be null) |
| `page` | Detail page on the site, `zh` and `en` |
| `type` | `pipeline` all-in-one, `writing`, `visual`, `source`, `craft`, `companion`, `platform` (a full app, not a skill) |
| `stages` | `market` `adaptation` `character` `structure` `drafting` `revision` `storyboard` `prompt` `production` |
| `models` | Video models it targets, such as `seedance` `kling` `minimax` `wan` `veo` `sora` `comfyui` |
| `agents` | Agents the author says it supports; empty means not stated (most SKILL.md skills work in any agent that loads skills) |
| `format` | `skill` (standard SKILL.md) or prompt files |
| `install` | Install command when there is one, such as `npx skills add owner/repo` |
| `language` | Main output language |
| `featured`, `checked`, `stars`, `pushed_at`, `license`, `archived` | Editor's pick, date checked, GitHub stars, last push, license, archived flag |

## 2. Understand the need

Work out, asking at most one short question if it is unclear:
- the stage or stages they need help with (map their words to `stages`; "改编/小说转剧本" is `adaptation`, "钩子/付费卡点/集纲" is `structure`, "分镜" is `storyboard`, "提示词" is `prompt`, "出片/剪辑/配音" is `production`);
- the video model, if any;
- the agent they use;
- whether they want one all-in-one pipeline or a few focused skills;
- output language and any license constraint (for commercial use).

## 3. Choose

- Drop `archived` items, and `platform` items unless the user wants a full app.
- Keep items whose `stages` and `models` match. Prefer, in order: `featured`, a matching agent in `agents`, `format` = `skill`, recent `pushed_at`, a license that fits. Use `stars` only to break ties.
- Recommend 3 to 5 items. For a full workflow, suggest one `pipeline` item, or one focused skill per stage.

## 4. Answer

Answer in the user's language, using the `zh` or `en` fields to match. For each pick give:
- name, linked to `github`;
- one sentence on why it fits, from `desc`, `overview` or `note`;
- the `install` command, or "see the repo README" when there is none;
- supported agents, license and last update;
- the `page` link for details.

Then:
- say the list was last updated on `updated`;
- for script skills, point to the side-by-side tests at https://shortdramaskills.com/evals/;
- remind the user that skills can ship scripts, so read a skill's SKILL.md before installing it. Do not run install commands without the user's go-ahead.

If nothing in the list fits, say so plainly instead of stretching a match.
