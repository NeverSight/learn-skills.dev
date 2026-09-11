---
name: shunk031-github-cgd-identity
description: Use this skill for all GitHub write operations in creative-graphic-design organization repositories (such as design-generators), including git commits and pushes, PR creation and updates, issue and PR comments, labels, milestones, and user-requested merges. Perform them as the creative-graphic-design-dev machine user. Use it both when the user explicitly requests the bot or dev account and whenever beginning write work in a creative-graphic-design organization repository without an explicit request; never use it in repositories of any other organization or host.
---

> [!NOTE]
> After reading this `SKILL.md`, say: `🎨 I read shunk031-github-cgd-identity.`

# CGD Dev Identity

## Overview

Perform git and gh write operations for creative-graphic-design organization repositories as the `creative-graphic-design-dev` machine user (user ID 176740601), not a personal account. A bot-authored PR lets a human account formally review and approve it. Because GitHub does not permit users to approve their own PRs, creating a PR with a personal account would prevent the review flow from working.

## Setup

Before starting write operations, perform the following checks in the working shell and worktree. Run them as a starting procedure rather than investigating only after a failure.

1. For repository writes, confirm that `git remote get-url origin` points to `github.com/creative-graphic-design`.

   If it does not, this skill does not apply; use normal git identity and authentication. New-machine `setup-gh-cgd` bootstrap is exempt.

2. Ensure that GitHub CLI has the bot account in its system credential store. On a new machine, run the interactive setup command once and authenticate in the browser as `creative-graphic-design-dev`:

   ```bash
   setup-gh-cgd
   ```

   Do not use `gh auth switch` during agent work. It changes the active account for the whole host and can race with concurrent sessions.

3. Retrieve the stored bot token by account name and pass it only to each write command that uses gh or git credentials:

   ```bash
   GH_TOKEN="$(gh auth token --hostname github.com --user creative-graphic-design-dev)" gh pr create ...
   GH_TOKEN="$(gh auth token --hostname github.com --user creative-graphic-design-dev)" git push
   ```

   Do not export the token into a persistent shell and do not print it. The per-command prefix keeps account selection explicit and avoids changing GitHub CLI's global active account.

4. Verify the GitHub identity and push permission for the organization repository. `gh api user` only confirms the logged-in account and cannot verify access to organization resources:

   ```bash
   GH_TOKEN="$(gh auth token --hostname github.com --user creative-graphic-design-dev)" gh api user --jq .login
   GH_TOKEN="$(gh auth token --hostname github.com --user creative-graphic-design-dev)" gh api repos/creative-graphic-design/<repo> --jq .permissions.push
   ```

   Do not start write operations unless the first command returns `creative-graphic-design-dev` and the second returns `true`.

5. Set the commit author to the bot for each commit command:

   ```bash
   git -c user.name=creative-graphic-design-dev \
       -c user.email=176740601+creative-graphic-design-dev@users.noreply.github.com \
       commit ...
   ```

   Do not use `git config user.name/email` in a linked worktree: it writes to the shared `.git/config` and changes the author for the main checkout and concurrent worktrees as well.

6. Push over HTTPS because SSH does not use the proxy in this environment. Set an explicit push URL:

   ```bash
   git remote set-url --push origin https://github.com/creative-graphic-design/<repo>
   ```

`GH_TOKEN` applies to both gh and the git credential helper in the same command environment. The credential helper returns the token with the username `x-access-token`.

## Scope

- This skill applies only to creative-graphic-design organization repositories on github.com. Do not use the stored bot credential or the bot commit identity for other hosts, organizations, or personal repositories; use normal authentication and the normal git identity there.
- Attribute every coding-agent write to a creative-graphic-design organization repository to the bot. This includes commits, pushes, PR creation and updates, PR replies, issue comments, labels, milestones, and user-requested merges.
- If any Setup verification fails, abandon the bot identity entirely: do not apply it partially, such as setting the bot commit author while the credential check failed or pushing through another account. Stop and report instead.
- The human (`shunk031`) retains only PR approval in the GitHub UI and the decision to merge. Do not approve PRs as the bot.

## Troubleshooting

- If `gh auth token --user creative-graphic-design-dev` fails or the stored credential is rejected, remove that account with `gh auth logout --hostname github.com --user creative-graphic-design-dev`, then rerun `setup-gh-cgd`. This changes local authentication state and must be done interactively by the user.
- If the identity check succeeds but repository permission is `false`, grant `creative-graphic-design-dev` access to the target repository before retrying. Reauthentication is unnecessary when only repository membership changes.
