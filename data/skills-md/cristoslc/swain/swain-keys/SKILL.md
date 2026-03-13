---
name: swain-keys
description: "Per-project SSH key provisioning for git signing and authentication. Generates ed25519 keys, configures git signing, registers on GitHub, and sets up SSH host aliases to bypass global agents (e.g., 1Password)."
user-invocable: true
allowed-tools: Bash, Read, Edit, Glob
metadata:
  short-description: SSH key provisioning for projects
  version: 1.0.0
  author: cristos
  license: MIT
  source: swain
---

# swain-keys

Per-project SSH key provisioning for git signing and authentication.

## When invoked

Locate and run the provisioning script at `skills/swain-keys/scripts/swain-keys.sh`:

```bash
SCRIPT="$(find . .claude .agents -path '*/swain-keys/scripts/swain-keys.sh' -print -quit 2>/dev/null)"
```

If the path search fails, glob for `**/swain-keys/scripts/swain-keys.sh`.

## Workflows

### Default (no arguments or "set up keys")

Run `--status` first to show current state:

```bash
bash "$SCRIPT" --status
```

If keys are not fully provisioned, ask the user if they'd like to proceed with provisioning.

### Provision ("provision keys", "configure signing", "set up SSH")

Run the full provisioning flow:

```bash
bash "$SCRIPT" --provision
```

The script will:
1. Derive a project name from the git remote or directory
2. Generate `~/.ssh/<project>_signing` (ed25519, no passphrase) if not exists
3. Create `~/.ssh/allowed_signers_<project>` with the configured git email
4. Add the public key to GitHub via `gh ssh-key add` for both authentication and signing
5. Create `~/.ssh/config.d/<project>.conf` with a host alias that bypasses global SSH agents
6. Update the git remote URL to use the project-specific host alias
7. Set local git config for commit and tag signing
8. Verify SSH connectivity and signing capability

### Status ("key status", "check keys")

```bash
bash "$SCRIPT" --status
```

### Verify ("verify keys", "test signing")

```bash
bash "$SCRIPT" --verify
```

## Handling scope refresh

If `gh ssh-key add` fails due to insufficient scopes, the script will print an action-needed message. When this happens:

1. Tell the user they need to authorize additional GitHub scopes
2. Show them the command: `gh auth refresh -s admin:public_key,admin:ssh_signing_key`
3. This will open a browser for OAuth — it requires human interaction
4. After they confirm, re-run `--provision` (idempotent, will skip completed steps)

## Integration with swain-init

When called from swain-init, run `--provision` directly without the status-first flow. swain-init handles the "would you like to?" prompt.

## Session bookmark

After provisioning, update the session bookmark:

```bash
BOOKMARK="$(find . .claude .agents -path '*/swain-session/scripts/swain-bookmark.sh' -print -quit 2>/dev/null)"
bash "$BOOKMARK" "Provisioned SSH keys for <project> — signing and auth configured"
```

## Error handling

- If not in a git repo: fail with clear message
- If `gh` CLI unavailable: skip GitHub registration steps, warn user to add keys manually
- If git email not configured: fail early with instructions
- All steps are idempotent — safe to re-run after fixing issues
