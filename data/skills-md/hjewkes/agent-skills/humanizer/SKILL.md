---
name: humanizer
description: Use when writing or editing text intended for other humans — READMEs, emails, Slack messages, commit messages, documentation, PR descriptions. Cleans AI-generated text patterns and applies context-appropriate tone.
---

# Humanizer

Clean AI-generated text by normalizing characters, flagging overused phrases, and following context-appropriate writing guidelines.

## Workflow

1. **Identify context** — determine what you're writing: README, email, Slack message, commit message, or general documentation
2. **Load the guide** — read the appropriate reference file (see table below)
3. **Write following the guide** — apply tone, structure, and length guidelines as you draft
4. **Run the script** — pipe final text through `humanize` for mechanical cleanup and phrase flagging
5. **Review flags** — rewrite any flagged phrases naturally; don't just delete them, replace with plain language

## Context Guides

| Context | Reference | Key principle |
|---------|-----------|---------------|
| README | [references/readme-guide.md](references/readme-guide.md) | Direct and factual, show the command first |
| Email | [references/email-guide.md](references/email-guide.md) | State the ask in the first sentence |
| Slack | [references/slack-guide.md](references/slack-guide.md) | Terse — 1-2 sentences max |
| Commit | [references/commit-guide.md](references/commit-guide.md) | Imperative mood, explain why not what |
| General | Apply common sense from all guides | Prefer clarity over formality |

## CLI Reference

| Command | Description |
|---------|-------------|
| `echo "text" \| humanize` | Clean text via stdin |
| `humanize file.md` | Clean text from file |
| `humanize --report file.md` | Verbose output with replacement counts |
| `humanize --help` | Show usage |

**Exit codes:** 0 = clean, 1 = error, 2 = phrase flags found (text still cleaned)

## What the Script Fixes Automatically

- Em dashes → space-hyphen-space
- Smart quotes → straight quotes
- Unicode ellipsis → three periods
- Non-breaking/invisible spaces → regular spaces
- Invisible Unicode watermark characters → removed
- Bullet characters → ASCII hyphens

## What Gets Flagged (Not Auto-Fixed)

The script flags phrases that need human judgment to rewrite:
- **Red-flag words:** delve, tapestry, seamless, robust, comprehensive, etc.
- **Hedging filler:** "it's important to note", "it's worth noting"
- **Cliche openers/closers:** "I hope this finds you well", "feel free to reach out"
- **Overused transitions:** furthermore, moreover, additionally

Full pattern list: [references/phrases.txt](references/phrases.txt)
