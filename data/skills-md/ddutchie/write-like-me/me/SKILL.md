---
name: me
description: Writes in the user's own voice using their saved style profile. Use for anything the user will send or publish as themselves (emails, Slack, PRs, posts, docs). /me init sets it up.
license: MIT
metadata:
  version: "0.2.0"
---

# me

Write the way the user writes: their words, rhythm and habits, not the default AI voice.

The user's voice lives in a style profile, a markdown file this skill creates and keeps up to date. This file tells you how to set it up, apply it and improve it.

## When this applies

Use the profile for text the user will **send or publish as themselves**, such as emails, Slack or chat messages, PR descriptions, commit messages, issue comments, social posts, blog drafts, docs and cover letters.

Do **not** restyle your own replies to the user. Explanations, plans and status updates stay in your normal voice unless the user asks otherwise.

## Find the profile

Check all three places:

1. `.me/STYLE.md` in the current project. This is a project voice, such as a company's docs style.
2. `~/.me/STYLE.md`, the user's global voice.
3. `STYLE.md` next to this `SKILL.md`, for environments without a persistent home directory, such as claude.ai uploads. Use it only when neither of the others exists.

When both 1 and 2 exist, layer them: the project profile overrides the global one section by section, and anything it leaves out comes from the global one. A file that is empty or has no Samples, Mechanics or Registers section counts as missing.

**Always say which profile you used.** After every draft, add one line naming what you loaded:

```
voice: ~/.me/STYLE.md
voice: .me/STYLE.md over ~/.me/STYLE.md
```

This line is for the user, never part of the text. Keep it out of the draft, commit messages and any file you write; if you wrote the text straight into a file or commit, put the line in your reply instead.

**If no profile exists, say so loudly.** A missing profile usually means another machine, a teammate's checkout or CI. Falling back quietly produces the default voice with nothing to show for it.

- If the user asked for writing directly (`/me <text>`, "write this like me"), don't draft. Say no profile was found, list the paths you checked, and offer `/me init`. Write neutral prose only if they tell you to go ahead.
- If you're drafting on your own (a commit message, a PR description), write plain, neutral prose that follows `references/ai-tells.md`, and **start** your reply with `voice: none found (checked .me/STYLE.md, ~/.me/STYLE.md, skill folder), neutral style used`.

## Commands

Read the first word of the arguments: `$ARGUMENTS`.

| Argument | Do this |
|---|---|
| `init` | Run the setup interview (below) |
| `learn` | Learn from the user's edits (below) |
| `show` | Summarise the profile in 5–8 bullets, then the `voice:` line for what was loaded |
| `edit <change>` | Apply the change to the profile, show the diff and save once the user confirms |
| *(any other text)* | Rewrite that text in the user's voice |
| *(empty)* | If no profile exists, run `init`. Otherwise show the profile path and these commands |

## Writing in the user's voice

1. Load the profile, and read `references/ai-tells.md` once per session.
2. Choose the **register** that fits the destination (Slack, email, PR, post and so on). If the profile has no entry for it, use the nearest one.
3. Write the draft. The **samples** outrank the rules: when they disagree, sound like the samples.
   - **Don't turn the user into a caricature.** Tell habits apart from quirks.
     - **Habits** are what the user does nearly every time in a register, such as lowercase in Slack or no full stop at the end. Apply them always.
     - **Quirks** show up now and then: "…", "!!", CAPS for emphasis, dropped apostrophes, a pet phrase. Budget them by length, not per message. The profile's **Quirks** table gives each one's rate per 1000 words in each register. Expected uses = rate × draft words ÷ 1000. Round down. Below 1, the quirk is optional: use it once only if a spot in the draft calls for it, and leave it out when unsure.
     - Example: "…" at 20 per 1000 words gives a 300-word email about 6 and a 25-word Slack reply 0.5, so at most one and often none. A two-line reply never carries the full quirk load. Short drafts sound like the user through habits, word choice and length.
     - If the profile has no rates (profiles from before v0.2), estimate them from its Samples before drafting.
4. Check the draft against the profile's **Never** list and against `references/ai-tells.md`, then fix every hit.
5. Keep the facts. Change voice, not meaning. Never invent opinions, experiences or commitments the user didn't give you.
6. Deliver the draft with no preamble like "Here's a version in your voice:", then the `voice:` line. When you had to guess at something important, add at most one more line.

For length, match the register. If the user's Slack messages are 12 words long, yours should be too.

## `init`: build the profile

Aim for about five minutes. Ask **one question at a time** and wait for each answer. Take the questions from `references/interview.md`.

1. **Samples first.** Ask for 2–5 things the user actually wrote, such as Slack messages, emails, a PR description or a post. Real samples tell you far more than the answers do. If the user has none, go on with the interview only and mark the profile `confidence: low`.
2. **Interview.** Ask the core questions in `references/interview.md`. Skip any question the samples already answered.
3. **Analyse.** Pull out the concrete patterns: typical sentence length, capitalisation, punctuation (em dashes? Oxford comma? `...`?), contractions, emoji, spelling variant, how the user opens and closes, recurring phrases, how they hedge or push back, and what they never do. Report patterns you observed, not impressions. "Lowercase in Slack, sentence case in email" beats "casual tone".
   - Sort each pattern into a **habit** (in nearly every sample of that register) or a **quirk** (only some of them).
   - For each quirk, count the words in that register's samples and the quirk's uses, and record the rate per 1000 words. List a quirk only if it appears at least twice. If a register has under about 300 words of samples, mark its rates `rough`.
4. **Draft.** Fill in `references/profile-template.md`. Quote short real excerpts under **Samples**.
5. **Confirm.** Show the draft and ask what's wrong. Then write two short test pieces, such as a Slack reply and an email, and ask whether they sound right. Revise until the user is happy.
6. **Save.** Ask whether this is the global voice (`~/.me/STYLE.md`) or a project voice (`.me/STYLE.md`). Create the folder if needed and write the file. If you can't write files (claude.ai), print the full profile in a code block and tell the user to save it as `STYLE.md` inside their copy of this skill folder, then re-upload it.

## `learn`: improve from edits

The best signal is what the user changes in your drafts.

1. Get the pair: your draft, and the version the user actually sent. Look for it in the conversation, or ask the user to paste it.
2. Diff the two. Sort each change into **voice** (wording, rhythm, formality, punctuation, length) or **content** (facts, decisions, scope). Learn only from voice changes.
3. Suggest at most 3 new or changed rules, each quoting the edit it came from. Leave out one-off changes; a rule needs a pattern, or a change the user says is always true.
   - If the user keeps deleting a quirk you added, suggest lowering its rate rather than dropping it.
4. Once the user approves, update the profile and add a dated line to its **Learned from edits** log.

When you notice the user heavily rewrote one of your drafts during normal work, offer `/me learn` in one line. Don't run it without asking.

## Rules for the profile file

- Never change the profile without the user's approval. Show the diff first.
- Keep it under about 300 lines. Merge rules that overlap, and trim old samples before adding new ones.
- The profile is personal. Don't copy it into other projects, commits or shared files unless the user asks.
