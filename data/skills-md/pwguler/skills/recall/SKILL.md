---
name: recall
description: Rebuild where recent work stands, from past sessions of the agent, the live repository, and the history of the project. Give back a short brief. Run it before you start or continue work, with or without a topic.
disable-model-invocation: true
---

Before work starts or continues, rebuild where it stands, and give back a short brief. Read only what the topic needs, then stop.

Fast path: when the message of the user already holds the state, use it and skip the session search. The state is paths, the branch, and the change in progress.

1. Fix the scope, and say it back in one line. The window is the last 7 days, unless the user names another. Add the topic when one is named. The project is this working directory. Read the sessions of another project only when the user asks. "All" stays all. Never reduce it to the latest few without saying so.
2. Find the transcripts of the past sessions of this project, as [transcripts.md](references/transcripts.md) says for your agent. Sort them by modification time (`ls -t`). Leave out the current session and the transcripts of subagent runs. When your agent keeps no transcripts that you can read, say so, and work from the repository and its history.
3. Search before you read. Grep each transcript for the topic, then read only the lines that match. Read the summaries that the agent already wrote before the turns. When the matching lines total more than about 2,000, split the transcripts across subagents. Each subagent returns one block for each session. The block gives the topic, the user's goal, decisions, open threads, the user's corrections, and artifacts. Artifacts are branches, PRs, commits, and tickets. Tag each block with its session id.
4. When the topic names a feature, file, area, or bug, also run the history path of the `research` skill. Ask what the current state is, what was tried and did not work, and what users still report.
5. Check every branch, PR, commit, and ticket that the search found against the live state, with `git` and `gh`. Read what an agent did from its session entries: the commands that it ran, and the errors that it hit. Never infer it.
6. Write the brief in four sections. **Where it stands** has five bullets at most. **Threads** has one line for each thread. Each line starts with exactly one tag: `[in flight <branch>]`, `[open PR #N]`, `[merged #N]`, `[reverted #N]`, `[done, uncommitted]`, or `[planned]`. **Problems** has five items at most: the problems that recur. Include complaints that users still make, and any fix that landed and was reverted later. **Next move** is one concrete action.

Rules:

- Stay on the topic. A thread next to it goes in only when it blocks this one. When the brief is longer than one screen, cut detail before you cut threads.
- Cite every finding: a session by its id, and the history by its source (commit, PR, or ticket).
- Recall only reads. It changes no file, branch, or ticket.
- Redact secrets found in a session. Replace a token, key, password, or connection string with a placeholder.
