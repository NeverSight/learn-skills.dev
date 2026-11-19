---
name: agent-git-override-main-identity
description: "Opt in to bot-attributed commits from this repository's main worktree by changing only this clone's local Git identity."
version: 1.0.0
author: koalyptus
license: MIT
platforms: [linux, macos, windows]
---

# Override Main-Worktree Identity

Use this only when the account owner explicitly wants bot-attributed commits from the current GitHub repository's main worktree. This GitHub-specific workflow uses GitHub noreply identity values; it is not intended for GitLab or other Git hosts. The standard `agent-git-setup` workflow remains unchanged and continues to leave the main-worktree identity alone.

## Important behavior

- The override changes only this clone's `.git/config`; it does not change global Git config or other repositories.
- It is persistent, not session-scoped. Every commit from this repository's main worktree uses the bot identity until the restore skill is run.
- This includes commits the account owner makes from the main worktree while the override is active.
- The script saves the exact prior repo-local `user.name` and `user.email` state in `.git/agent-main-identity.backup.config`. If the values were not set locally, restore removes the temporary local values so the prior global/default identity applies again.
- The script refuses to run from a linked worktree. It uses the bot identity persisted by `agent-git-setup`; it does not ask the account owner to enter the bot name, email, or repository path.

## Workflow

1. Confirm that the account owner intends to enable bot identity persistently for this repository's main worktree and understands that their own commits here will also be bot-attributed until restoration. Skill invocation alone is not consent to change the identity.
2. Confirm `agent-git-setup` has already configured the bot identity for this clone. If not, stop and ask the account owner to run the existing setup workflow first.
3. Set `SKILL_DIR` to this skill's installation directory, resolved from the loaded `SKILL.md` path. Use the helper bundled there, not a `scripts/` path relative to the target repository. Do not ask the account owner for the skill path. Run with the target main worktree as the current directory and explicit target (`.`). On Linux or macOS:

   ```bash
   bash "$SKILL_DIR/scripts/agent-git-override-main-identity.sh" --confirm .
   ```

   On Windows:

   ```powershell
   pwsh "$SKILL_DIR/scripts/agent-git-override-main-identity.ps1" --confirm .
   ```

4. Verify `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` resolve to the configured bot identity. Tell the account owner the override is active and direct them to `agent-git-restore-main-identity` when they want their original identity back.

If the script reports an existing backup, incomplete setup, changed identity, or any other error, stop. Do not delete or rewrite the backup to force activation.