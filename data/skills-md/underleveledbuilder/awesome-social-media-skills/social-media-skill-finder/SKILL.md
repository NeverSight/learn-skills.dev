---
name: social-media-skill-finder
description: Recommend social media skills and MCP tools from a hand-checked, security-scanned list, matched to the job (writing posts and threads, covers and short video, scheduling and publishing, trends and analytics, replies and DMs, positioning and growth), the platform (Xiaohongshu/小红书/RedNote, Douyin/抖音, WeChat Official Accounts/公众号, Bilibili, Weibo, Zhihu, X/Twitter, YouTube, TikTok, Instagram, LinkedIn, Threads, Reddit) and the agent (Claude Code, Codex, OpenClaw/龙虾, Qwen, Doubao, WorkBuddy). Use when someone asks which skill or tool to use for social media or 自媒体 work, or how to install one. 帮你从人工核对、做过安全检查的自媒体 skill 清单里挑合适的：写笔记和推文、封面和短视频、发布、热点和数据、互动、账号定位。
---

# Social media skill finder

Pick skills for social media work from the Awesome Social Media Skills list (https://github.com/UnderleveledBuilder/awesome-social-media-skills). Every entry was checked by hand, scanned by a script for risky files and commands, and tagged by job, platform, format and supported agents.

## 1. Get the data

Fetch `https://raw.githubusercontent.com/UnderleveledBuilder/awesome-social-media-skills/main/catalog.json`. If that fails, read `README.md` (English: `README.en.md`) from the same place; it has the same entries without the structured fields.

`catalog.json` has `updated`, `groups`, `facets` (the `platforms` labels), `formats` and `entries`. Each entry has:

| Field | Meaning |
|---|---|
| `repo`, `url`, `name` | GitHub repo |
| `group` | `pipeline` all-in-one, `writing` (including pre-publish compliance checks), `visual` (layout, covers, images and video), `publish`, `research`, `strategy`, `mcp` (MCP server or CLI tool, not a skill), `apps` (full app). Comment replies and DMs are handled by some `pipeline` and `publish` entries |
| `platforms` | Platforms it targets, such as `xiaohongshu` `douyin` `wechat` `channels` `bilibili` `weibo` `zhihu` `x` `youtube` `tiktok` `instagram` `linkedin` `threads` `reddit`; `general` means any platform |
| `format` | `skill` (standard SKILL.md), `prompts`, `mcp`, `app` |
| `agents` | Agents the author says it supports; empty means not stated (most SKILL.md skills work in any agent that loads skills) |
| `desc`, `desc_en`, `note`, `note_en` | Summary and editor's note in Chinese and English |
| `install` | Install command when there is one, such as `npx skills add owner/repo` |
| `lang` | Main language of the skill's own text |
| `featured`, `checked`, `stars`, `pushed_at`, `license`, `skills` | Editor's pick, date checked, GitHub stars, last push, license, number of skills in the repo |

## 2. Understand the need

Work out, asking at most one short question if it is unclear:
- the platform or platforms;
- the job: writing, visuals, publishing, research, engagement or strategy;
- whether they want the agent to post for them (needs an MCP or automation tool that logs in as them) or only to draft;
- the agent they use, output language, and any license constraint.

## 3. Choose

- Drop entries whose `pushed_at` is over a year old unless nothing else fits.
- Keep entries whose `platforms` match (or `general`) and whose `group` fits the job. Prefer, in order: `featured`, a matching agent in `agents`, `format` = `skill`, recent `pushed_at`, a license that fits. Use `stars` only to break ties.
- Recommend 3 to 5 entries. For posting, pair a writing skill with a `publish` skill or an `mcp` tool.

## 4. Answer

Answer in the user's language, using `desc`/`note` for Chinese and `desc_en`/`note_en` for English. For each pick give:
- name, linked to `url`;
- one sentence on why it fits;
- the `install` command, or "see the repo README" when there is none;
- supported agents, license and last update.

Then:
- say the list was last updated on `updated`;
- for anything that logs in or posts for the user, say plainly that it uses their account and that platforms limit automation, so they should read how it stores the session and keep the final publish click themselves;
- remind the user that skills can ship scripts, so read a skill's SKILL.md before installing it. Do not run install commands without the user's go-ahead.

If nothing in the list fits, say so plainly instead of stretching a match.
