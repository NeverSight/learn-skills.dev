---
name: cofounder-ssh-key-rotation
description: >
  This skill should be used when the user asks to "rotate SSH keys", "regenerate SSH keys",
  "replace SSH keys", "renew SSH keys", or when the agent needs SSH access to a deployed VM
  for troubleshooting (logs, debugging, database access) but discovers the expected SSH key
  file is missing from the local disk (e.g. `~/.ssh/<repo-name>` does not exist). Also use
  when the user mentions "lost SSH key", "SSH key not found", "can't SSH into server",
  "permission denied SSH", "moved to a new computer", or "cloned repo on another machine".
---

# SSH Key Rotation

Rotates the SSH key for all VMs of a deployed environment. After rotation, only the new key grants access -- the old key is permanently revoked from every VM.

## When to Use

1. **Explicit request**: The user asks to rotate, regenerate, or replace SSH keys.
2. **Missing local key**: The agent needs to SSH into a VM (for logs, debugging, database access, etc.) but the expected key file does not exist on disk.

### Detecting a missing key

Before any SSH operation, the agent resolves the key path:

```bash
REPO_NAME=$(gh repo view --json name -q .name)

# Preview environment
SSH_KEY=~/.ssh/$REPO_NAME

# Other environments (e.g., production)
SSH_KEY=~/.ssh/$REPO_NAME-production
```

If the file does not exist (`test -f "$SSH_KEY"` fails), the key is missing and rotation is needed.

## Warnings (Always Communicate Before Proceeding)

Before starting rotation, **always** warn the user:

1. **Downtime**: Rotation stops each VM, resets its SSH key, and restarts it. All VMs in the environment will experience downtime during the process (accessories first, then workers, then web -- to minimize user-facing downtime).
2. **Old key revoked**: The old SSH key is permanently erased from all VMs' `authorized_keys` files. Anyone using the old key will lose access immediately.
3. **All environments are independent**: Each environment (preview, production, etc.) has its own SSH key. Rotation only affects the specified environment.

Ask for explicit confirmation before proceeding.

## Rotation Procedure

### Step 1: Determine the environment

Identify which environment needs rotation:

- If the user specifies an environment, use it.
- If the agent discovered a missing key during a troubleshooting attempt, use the environment that was being targeted.
- If ambiguous, ask the user.

### Step 2: Generate a new SSH key locally

Delete the old key file (if it exists) and generate a fresh one using the standard naming convention:

```bash
REPO_NAME=$(gh repo view --json name -q .name)

# Preview environment
rm -f ~/.ssh/$REPO_NAME ~/.ssh/$REPO_NAME.pub
ssh-keygen -t ed25519 -f ~/.ssh/$REPO_NAME -N "" -C "$REPO_NAME-deploy"
chmod 600 ~/.ssh/$REPO_NAME

# Other environments (e.g., production)
rm -f ~/.ssh/$REPO_NAME-production ~/.ssh/$REPO_NAME-production.pub
ssh-keygen -t ed25519 -f ~/.ssh/$REPO_NAME-production -N "" -C "$REPO_NAME-deploy-production"
chmod 600 ~/.ssh/$REPO_NAME-production
```

### Step 3: Update the GitHub secret

Upload the new private key to the corresponding GitHub secret:

```bash
# Preview
gh secret set SSH_PRIVATE_KEY < ~/.ssh/$REPO_NAME

# Production (or other environment -- suffix matches env_name uppercased)
gh secret set SSH_PRIVATE_KEY_PRODUCTION < ~/.ssh/$REPO_NAME-production
```

### Step 4: Create and run the rotation caller workflow

Create a caller workflow that invokes the reusable rotation workflow. This follows the same pattern as teardown workflows:

```yaml
# .github/workflows/rotate-ssh-key-preview.yml
name: Rotate SSH Key Preview
on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  rotate:
    uses: locaweb/locaweb-cloud-provision/.github/workflows/rotate-ssh-key.yml@v1
    with:
      env_name: "preview"
    secrets:
      CLOUDSTACK_API_KEY: ${{ secrets.CLOUDSTACK_API_KEY }}
      CLOUDSTACK_SECRET_KEY: ${{ secrets.CLOUDSTACK_SECRET_KEY }}
      SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
```

For other environments, adjust `env_name` and the `SSH_PRIVATE_KEY` secret reference:

```yaml
# .github/workflows/rotate-ssh-key-production.yml
name: Rotate SSH Key Production
on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  rotate:
    uses: locaweb/locaweb-cloud-provision/.github/workflows/rotate-ssh-key.yml@v1
    with:
      env_name: "production"
    secrets:
      CLOUDSTACK_API_KEY: ${{ secrets.CLOUDSTACK_API_KEY }}
      CLOUDSTACK_SECRET_KEY: ${{ secrets.CLOUDSTACK_SECRET_KEY }}
      SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY_PRODUCTION }}
```

Commit and push the workflow file, then trigger it:

```bash
git add .github/workflows/rotate-ssh-key-preview.yml
git commit -m "Add SSH key rotation workflow for preview"
git push

# Trigger the workflow
gh workflow run rotate-ssh-key-preview.yml
```

### Step 5: Monitor the rotation

```bash
# Watch the run
gh run list --workflow=rotate-ssh-key-preview.yml --limit=5
gh run watch <run-id>
```

Give the user a direct link to follow in the GitHub UI:

```bash
gh run list --limit=1 --json databaseId,url -q '.[0].url'
```

If the workflow fails, read the logs:

```bash
gh run view <run-id> --log-failed
```

### Step 6: Verify SSH access

After the workflow completes successfully, verify that the new key works:

```bash
REPO_NAME=$(gh repo view --json name -q .name)

# Get the web IP from the latest deploy run
rm -rf $HOME/tmp/provision-output
gh run list --workflow=deploy-preview.yml --status=success --limit=1
gh run download <run-id> --name provision-output --dir $HOME/tmp/provision-output
cat $HOME/tmp/provision-output/provision-output.json

# Test SSH with the new key
ssh -i ~/.ssh/$REPO_NAME -o ConnectTimeout=10 root@<web_ip> "echo 'SSH rotation successful'"
```

### Step 7: Resume the original task

If rotation was triggered because the agent needed SSH access for troubleshooting, resume the original operation (checking logs, debugging, database access, etc.) using the new key.

## Workflow Inputs

The reusable rotation workflow (`rotate-ssh-key.yml@v1`) accepts:

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `env_name` | string | `"preview"` | Environment name (must match the deployed environment) |

Required secrets:

| Secret | Description |
|--------|-------------|
| `CLOUDSTACK_API_KEY` | CloudStack API key |
| `CLOUDSTACK_SECRET_KEY` | CloudStack secret key |
| `SSH_PRIVATE_KEY` | The **new** SSH private key (already updated in Step 3) |

## What the Rotation Does (Server-Side)

1. Verifies the SSH keypair and network exist in CloudStack (safety check)
2. Deletes the old keypair from CloudStack and registers the new public key under the same name
3. For each VM (accessories first, workers next, web last):
   - Stops the VM
   - Resets its SSH key via CloudStack API
   - Starts the VM
   - Connects via SSH with the new key and overwrites `authorized_keys` with only the new key
4. Prints a summary of results

## Key File Naming Convention

| Environment | Local key path | GitHub secret |
|---|---|---|
| preview (default) | `~/.ssh/<repo-name>` | `SSH_PRIVATE_KEY` |
| production | `~/.ssh/<repo-name>-production` | `SSH_PRIVATE_KEY_PRODUCTION` |
| other `<env_name>` | `~/.ssh/<repo-name>-<env_name>` | `SSH_PRIVATE_KEY_<ENV_NAME>` (uppercased) |
