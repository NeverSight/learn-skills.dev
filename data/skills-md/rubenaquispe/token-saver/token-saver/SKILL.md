---
name: token-saver
description: "Token optimization dashboard with two sections - (1) Workspace file compression for ALL .md files in context, (2) AI model audit that detects current models and suggests cheaper alternatives. Shows \"possible savings\" until optimizations are applied. Triggers on \"optimize tokens\", \"reduce AI costs\", \"model audit\", \"save money on AI\"."
---

# Token Saver

> **💡 Did you know?** Every time you send a prompt, your workspace files (SOUL.md, USER.md, MEMORY.md, AGENTS.md, and more) are sent along with it — every single time. These files count toward your context window, slowing down responses and costing you real money on every message. Token Saver compresses these files using AI-efficient notation that preserves all your data while making everything lighter, faster, and cheaper.

**Cut your AI costs by 40-90% with one command.**

## What You Get

```
/optimize
```

A clean dashboard showing:

**🗜️ File Compression** — Scans ALL your .md workspace files and shows exactly how much you can save by compressing them to AI-efficient notation. MEMORY.md alone typically saves 90%+.

**🤖 Model Audit** — Detects which AI models you're using (main chat, cron jobs, subagents) and recommends cheaper alternatives with specific dollar savings.

**📊 Combined Savings** — Total weekly/monthly/annual savings estimate across both optimizations.

## Commands

| Command | What it does |
|---|---|
| `/optimize` | Dashboard with all savings options |
| `/optimize tokens` | Compress workspace files (auto-backup) |
| `/optimize models` | Detailed model cost comparison |
| `/optimize revert` | Restore files from backups |

## ✨ Persistent Mode (Auto-Enabled)

When you run `/optimize tokens`, the skill also enables **Persistent Mode** — a one-liner instruction added to AGENTS.md that tells your AI to keep writing in compressed notation going forward. This means:

- **One-and-done optimization** — files stay lean as your AI adds new content
- **No re-optimization needed** — AI maintains the compressed format automatically  
- **Easy to turn off** — `/optimize revert` removes persistent mode and restores all files

Without persistent mode, workspace files would gradually grow back to verbose format as your AI writes new entries.

## Safety

- **Auto-backup** before any file change
- **"Possible savings"** shown until you actually apply
- **One-command revert** — `/optimize revert` restores everything + turns off persistent mode
- Only compresses files where real savings exist

## How It Works

AI models understand compressed notation perfectly:

**Before (500+ tokens):**
> When Ruben greets me in the morning with phrases like "good morning" or "what's on today", I should proactively review our task list, mention pending items, and check for urgent issues...

**After (30 tokens):**
> `MORNING: greeting → review(todos+pending+urgent)`

Same meaning. 90% fewer tokens. Real dollar savings.

## Scripts

- `scripts/optimizer.js` — Main dashboard and command handler
- `scripts/analyzer.js` — Token counting, model detection, cost calculations
- `scripts/compressor.js` — AI-notation compression engine