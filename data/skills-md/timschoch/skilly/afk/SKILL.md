---
name: afk
description: Take a task and run it alone while the user is away, up to staged changes, an open PR or a merged PR. Stops on low confidence, growing blast radius or a block. Use when the user runs /afk with a task or issue.
disable-model-invocation: true
argument-hint: <task|issue-url>
---

# AFK

The user hands over a task and leaves. Settle every question up front, then work alone until the chosen end state or a stop.

## 1. Launch

The user waits on nothing. In the first reply:

1. Print this question before any tool call:

   ```markdown
   1. End with?
      1.1 staged changes
      1.2 open PR
      1.3 merged PR
   ```

2. Spawn a researcher agent in the background. Pick its model per the repo's model rule. Task: read the issue with its comments, the code it names, `GLOSSARY.md` and related ADRs, then return a draft of the brief below.
3. End the turn.

Numbering follows `.claude/rules/workflow-dialog.md`.

## 2. Brief

When the researcher returns, send one message, whether or not question 1 has an answer yet. An open question 1 stays in the message, so the user answers everything in one reply.

- **What I'd do:** at most three bullets. Name the files and areas you plan to touch. This is the scope.
- **Questions:** only what blocks the work or forks the solution. Numbered, one sub-item per option, **recommended** marks your pick. No questions: omit the section.
- Last line: `go?`

Repeat until the user approves. A changed scope or end state needs a new `go?`.

## 3. Go

On approval, print one line and start work:

```
starting now... <animal> _<sound>_ "<joke>"
```

- Pick the animal from this list that fits the task best: 🐒🦍🦧🐕🐩🐺🦊🦝🐈🐈‍⬛🦁🐯🐅🐆🫎🫏🐎🦄🦓🦌🦬🐂🐃🐄🐖🐗🐏🐑🐐🐫🦙🦒🐘🦣🦏🦛🐁🐀🐇🐿️🦫🦔🦇🐻🐨🐼🦥🦦🦨🦘🦡🦃🐓🐥🐧🕊️🦅🦆🦢🦉🦤🦩🦚🦜🐦‍⬛🪿🐦‍🔥🐸🐊🐢🦎🐍🐉🦕🦖🐳🐋🐬🦭🐠🐡🦈🐙🪼🦀🦑🐌🦋🐛🐜🐝🪲🐞🦗🪳🕷️🦂🦟🪰🪱🦠
- Sound: the noise that animal makes, italic.
- Joke: one line, about both the animal and the task.

Example, task "remove the old login auth system": `starting now... 🦖 _Roaar_ "Why did the T-Rex die during the meteor hit? He still had the old login credentials for the underground bunker."`

## 4. Work

Build, test, verify per the repo's rules. Ask nothing between `go` and the end. A question means a stop.

Stop when:

- **Confidence drops.** You doubt the approach works, you found a better approach that needs a major pivot, or you guess at intent the brief did not settle.
- **Blast radius grows.** The change needs a file or area outside the scope, a new public API, a schema change or a new dependency.
- **Blocked.** Missing access, secret or tool, or a decision only the user can make.
- **Red loop.** The same check stays red after 3 fix attempts.

On a stop, leave the work uncommitted and print the report in the `/progress` shape (`.agents/skills/progress/SKILL.md`), the stop reason under **Needs you**.

## 5. End

The end state answer is the user's sign-off in advance. It replaces the approval step of `.claude/rules/workflow-sign-off.md` for this task only.

| End state | Do |
| --- | --- |
| staged changes | Stage the work, stop. |
| open PR | Commit, push, open the PR. Stop at green CI. |
| merged PR | As open PR, then apply `.agents/skills/babysit-pr/SKILL.md` with `--merge`. |

CI failures and review items after the push count toward the stop rules above.

Close with the report in the `/progress` shape: end state reached, links (PR, commits), what was verified and how.