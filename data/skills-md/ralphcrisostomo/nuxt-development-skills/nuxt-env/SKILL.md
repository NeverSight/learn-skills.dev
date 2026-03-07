---
name: nuxt-env
description: "Use when setting up SOPS + age encryption for environment variables. Checks dependencies, creates config, copies scripts, and adds package.json commands. Triggers on: setup sops, setup env encryption, add age encryption, env:pull, env:push."
model: sonnet
user-invocable: true
---

# nuxt-env

Set up SOPS + age encryption for environment variables in a Nuxt project.

## When to Use

- Setting up encrypted environment variable management for a project
- Adding SOPS + age encryption workflow
- User mentions `env:pull`, `env:push`, `env:encrypt`, `env:decrypt`
- Onboarding a project to the encrypted env bundle workflow

## Pre-flight: System Dependencies

Check and install system dependencies in order:

### 1. sops + age

```bash
which sops && which age-keygen
```

If either is missing:

```bash
brew install sops age
```

### 2. npm dependencies

Check if `chalk` is in the target project's `devDependencies`. If missing:

```bash
bun add -d chalk
```

### 3. Age keypair

Check if the age key file exists:

```bash
test -f ~/.config/sops/age/keys.txt
```

If missing, generate one:

```bash
mkdir -p ~/.config/sops/age
age-keygen -o ~/.config/sops/age/keys.txt
```

Display the public key to the user (they will need it for `.sops.yaml`):

```bash
age-keygen -y ~/.config/sops/age/keys.txt
```

**Tell the user to save this public key** -- it goes into `.sops.yaml` and must be shared with teammates.

## Setup Steps

Run these steps in the target project root.

### 1. Create directories

```bash
mkdir -p secrets .tmp
```

### 2. Add .gitignore entries

Append to the project root `.gitignore` if not already present:

```
.tmp/
```

Ensure `secrets/` has proper git tracking -- encrypted files ARE tracked, plain JSON is NOT. Add `secrets/.gitignore` with:

```
# Ignore decrypted plain JSON bundles
*.json
# But track encrypted sops files
!*.sops.json
!.gitignore
!.gitkeep
```

Create `secrets/.gitkeep` if the directory is empty.

### 3. Create `.sops.yaml`

**Skip if `.sops.yaml` already exists.** Otherwise create at project root:

```yaml
# Replace the placeholder recipients below with real age public keys (age1...)
# for your developer team and CI before encrypting secrets.
creation_rules:
    - path_regex: ^(.+[\\/])?secrets[\\/].*\.sops\.json$
      age: >-
          AGE_PUBLIC_KEY_HERE
```

Prompt the user to replace `AGE_PUBLIC_KEY_HERE` with the public key displayed in pre-flight step 3. If the public key was just generated, offer to substitute it automatically.

### 4. Copy scripts

Copy these files from this skill's `scripts/` directory to the target project's `scripts/` directory:

| Source (skill)              | Target (project)            |
| --------------------------- | --------------------------- |
| `scripts/sops-bundle.ts`   | `scripts/sops-bundle.ts`    |
| `scripts/env-variables.ts` | `scripts/env-variables.ts`  |
| `scripts/libs/load-env.ts` | `scripts/libs/load-env.ts`  |

Create `scripts/libs/` if it doesn't exist. **Skip any file that already exists** in the target -- warn the user instead.

### 5. Add package.json scripts

Read the target project's `package.json`. Add the following scripts, **skipping any that already exist**:

```json
{
    "env:export": "bun scripts/env-variables.ts --export-json --out .tmp/env-bundle.json",
    "env:apply": "bun scripts/env-variables.ts --import-json --in .tmp/env-bundle.json",
    "env:apply:dry": "bun scripts/env-variables.ts --import-json --in .tmp/env-bundle.json --dry-run",
    "env:decrypt": "bun scripts/sops-bundle.ts decrypt",
    "env:encrypt": "bun scripts/sops-bundle.ts encrypt",
    "env:pull": "bun run env:decrypt && bun run env:apply",
    "env:push": "bun run env:export && bun run env:encrypt"
}
```

## Post-setup Verification

After all steps, verify:

1. `which sops && which age-keygen` -- both installed
2. `ls scripts/sops-bundle.ts scripts/env-variables.ts scripts/libs/load-env.ts` -- all scripts exist
3. `package.json` has all `env:*` scripts
4. `.sops.yaml` exists with correct structure
5. `secrets/.gitignore` exists with correct rules
6. `.tmp/` is in `.gitignore`

Print a summary of what was created/skipped.

## Usage After Setup

| Command            | What it does                                         |
| ------------------ | ---------------------------------------------------- |
| `bun run env:push` | Export .env files to JSON bundle, then SOPS-encrypt   |
| `bun run env:pull` | SOPS-decrypt the bundle, then write .env files        |
| `bun run env:encrypt` | Encrypt `.tmp/env-bundle.json` to `secrets/env-bundle.sops.json` |
| `bun run env:decrypt` | Decrypt `secrets/env-bundle.sops.json` to `.tmp/env-bundle.json` |
| `bun run env:export`  | Export .env files to `.tmp/env-bundle.json`         |
| `bun run env:apply`   | Write `.tmp/env-bundle.json` back to .env files     |
