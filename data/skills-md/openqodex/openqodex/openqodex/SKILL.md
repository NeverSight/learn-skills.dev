---
name: openqodex
description: Code review for the current change, before it is pushed. One command runs the security, secret, dependency and lint scanners that fit the changed files, a separate reviewer that checks every scanner finding and is given every changed line, and prints the report. Use before every git push, when asked for a code review, a security scan, or to review changes, a diff or a pull request, and when a push was blocked or warned by OpenQodex.
---

# OpenQodex: review the change before it is pushed

OpenQodex reviews a change in one command. It takes a frozen copy of the change, runs the deterministic scanners that fit the changed files (gitleaks, semgrep, bandit, hadolint, shellcheck, actionlint, osv-scanner and others), keeps what they report on changed lines, and starts its own reviewer: a separate Claude Code or Codex process that reads only that copy. The reviewer checks every scanner finding, is given every changed line and answers in a fixed shape; OpenQodex checks the answer with scripts and prints one report. No key and no account are needed beyond the developer's Claude Code or Codex login. The code goes to the model that login uses. The reviewer can also search the web and open web pages unless `reviewer_web: off` is set in `~/.openqodex/config.yaml`. Two scanners go online, and neither sends code: semgrep downloads its rule packs from the Semgrep registry on each run, and when the change touches a dependency file, osv-scanner sends the names and versions of the dependencies to osv.dev. `--offline` skips both scanners.

## When to run

- Before any `git push`.
- When the developer asks you to review their changes.
- When a push was blocked or warned by the OpenQodex hook.
- After fixing findings, to check the change again.

## Who reviews

OpenQodex starts its own reviewer process for every review, with no memory of this session. You do not start a subagent for it and you do not review the change yourself: run the command and show what it prints.

If `review` says "Full review unavailable" and prints a way to review with the agent you are in, follow it: run the command it names and do what the brief it prints says.

## Procedure

When the file `~/.openqodex/bin/openqodex` exists, run it in place of `npx -y openqodex@<version>` in every command of this skill: it is the copy `openqodex init` installed.

1. From the repository, run:

   ```
   npx -y openqodex@0.8.1 review
   ```

   It reviews the change: the commits not yet pushed plus everything uncommitted, untracked files included. To review the whole repository instead, run:

   ```
   npx -y openqodex@0.8.1 review --all
   ```

2. Wait for it. A review takes one to three minutes. Many agents stop a command after two minutes, so give it up to ten minutes, or run it in the background and wait until it exits. While the reviewer works, it prints a progress line every 15 seconds on stderr. Do not start it a second time while one runs.

3. Show the developer the report it printed, exactly as printed. Do not reword it, shorten it or add findings of your own. The same report is saved as `report.md`; its path is on the last progress line.

4. Act on the exit code:
   - 0: the review is complete and nothing blocks the push.
   - 1: the review is complete and its verdict is `blocked`. Do not push. Show the developer the findings; push only if they say so after seeing them.
   - 2: there is no complete review. The output says what is missing (for example "Full review unavailable" when no reviewer could start, or "Review incomplete" with the reasons). Tell the developer exactly that. Never present the scanner output as a review.

## Reviewing a branch or a pull request

When the developer asks you to review a branch or a pull request that is not their current work, name it:

```
npx -y openqodex@0.8.1 review feature/login
npx -y openqodex@0.8.1 review '#42'
```

Quote `#42`: in a shell `#` starts a comment. A pull request link works too. OpenQodex fetches the target, checks it out in a temporary folder and reviews what it added since it left its base. This is someone else's code: never run its tests, scripts, builds or services, and never edit it.

## Rules

- Never edit code during the review. Review first, show the report, then fix only what the developer asks you to fix.
- Never run `openqodex trust` without asking the developer first. It approves a custom scanner, which is a command that runs on their machine.
- Never set `OPENQODEX_SKIP`. It is the developer's switch, not yours.
- When the verdict is `blocked`, do not push unless the developer says so after seeing the findings.
- When OpenQodex prints "OpenQodex had a problem. Nothing has been sent." with `1 create a GitHub issue` and `2 ignore`, tell the developer in one line what went wrong and give them the two choices. Never choose 1 yourself. If they say 1, run `npx -y openqodex@0.8.1 report --send-last` from the same folder. Anything else means 2: do nothing.

## Reading the report

- The report is in `.openqodex/reviews/<time>-<id>/` in the repository: `report.md` to read, `report.json` and `report.sarif` for tools. `.openqodex/latest.json` points at the newest review. The reports never show in `git status`: `.openqodex/.gitignore` keeps them out. The two other files in that folder, `config.yaml` and `custom-instructions.md`, are the team's and are meant to be committed.
- The verdict is `passed` (with or without warnings) or `blocked`. It is `blocked` only when the repository's config (`.openqodex/config.yaml`, or `.openqodex.yaml` at the root) sets `block_on_severity` and a finding is at or above it. With no config, OpenQodex warns and never blocks.
- A complete review means every stage ran, every scanner finding was checked and every changed line was put in front of the reviewer; anything not covered is named in the report. It does not mean nothing was missed: no review finds everything.
- The coverage list says, for each scanner, whether it ran. A scanner that did not run has a one-line reason:
  - `no matching files`: nothing in the change is the kind of file it reads.
  - `installing`: it is being downloaded for the first time; it is included from the next run. Say so to the developer rather than waiting.
  - `not installed`: it could not be installed here; the reason says why.
  - `needs Ruby 2.7+` or `needs Go`: brakeman and rubocop need Ruby, golangci-lint needs Go. OpenQodex does not install language runtimes. If the developer wants those scanners, they install Ruby or Go the usual way for their system (for example `brew install ruby go` on a Mac) and run the review again.
  - `untrusted`: a custom scanner from the repo's config that the developer has not approved. Tell the developer; approving it is their decision (`npx -y openqodex@0.8.1 trust`).
  - `failed`: the scanner ran and broke; the reason has its error. A scanner problem never changes the exit code.

## Inside a sandbox

Some agents run commands in a sandbox that cannot reach the network or write outside the project. There the first run cannot download the scanners, and the reviewer may not reach its model. Tell the developer to run this once in their own terminal, outside the agent:

```
npx -y openqodex@0.8.1 doctor --install
```

It downloads every scanner that fits the machine into `~/.openqodex/tools/`. If the review still says "Full review unavailable" inside the sandbox, the developer runs `npx -y openqodex@0.8.1 review` in their own terminal.

## More

`npx -y openqodex@0.8.1 guide` prints this guide. `npx -y openqodex@0.8.1 guide <topic>` prints a page of the docs, offline: `quickstart`, `config`, `scanners`, `custom-scanners`, `security`, `agents`, `cli`.
