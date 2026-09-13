---
name: bitwarden-personal-profile
description: Load, validate, and use a user's private personal profile from Bitwarden CLI for form filling, PDF completion, applications, and identity/contact/employment/housing reuse. Use when an agent needs stable personal data backed by Bitwarden, language-aware profile values, a bundled schema for personal facts, or a safe workflow that materializes real profile values outside Git.
---

# Bitwarden Personal Profile

## Contract

Use this skill to access stable personal facts from Bitwarden without committing private values.

- The schema and fake example are bundled in this skill.
- Real profile values must live outside the repository.
- Prefer `$ADC_PERSONAL_PROFILE_PATH`; otherwise use `~/.config/AgentDesk/personal-profile.yaml`.
- Never write real profile values into this skill folder, a public repo, logs, screenshots, or final answers unless the user explicitly asks for those values.

## Workflow

1. Locate the private profile.
   - Use `$ADC_PERSONAL_PROFILE_PATH` when set.
   - Otherwise use `~/.config/AgentDesk/personal-profile.yaml`.
   - If the file is missing and the user uses Bitwarden Secrets Manager, run `scripts/bitwarden_to_profile.py`.
   - If Bitwarden is unavailable, run `scripts/init-private-profile.sh` and ask the user to fill the generated local file.

2. Validate before use.
   - Run `scripts/validate_profile.py "$ADC_PERSONAL_PROFILE_PATH"` or the default path.
   - Stop if validation fails.

3. Match the output language to the target form.
   - Read `references/language-policy.md`.
   - For English forms, prefer `en` values.
   - For German forms, prefer `de` values.
   - Keep proper nouns and official names unchanged unless the profile explicitly provides a translation.

4. Load only the fields needed for the task.
   - Use `scripts/load_profile.py --json` for normalized JSON.
   - Do not paste the whole profile into conversation when only a few fields are needed.

## Commands

Initialize a private local profile from the fake example:

```bash
skills/bitwarden-personal-profile/scripts/init-private-profile.sh
```

Create a Bitwarden Secrets Manager import JSON from a local private profile:

```bash
skills/bitwarden-personal-profile/scripts/profile_to_bitwarden_import.py \
  "$HOME/.config/AgentDesk/personal-profile.yaml" \
  --project-name "AgentDesk" \
  --output "$HOME/.config/AgentDesk/bitwarden-personal-profile-import.json"
```

Create or update the secret directly with `bws` when the project already exists:

```bash
skills/bitwarden-personal-profile/scripts/profile_to_bws_secret.py \
  "$HOME/.config/AgentDesk/personal-profile.yaml" \
  --project-id "$BWS_PERSONAL_PROFILE_PROJECT_ID"
```

Materialize from Bitwarden Secrets Manager export JSON, a `bws` secret id, or a project scan:

```bash
skills/bitwarden-personal-profile/scripts/bitwarden_to_profile.py \
  --from-bws-project-id "$BWS_PERSONAL_PROFILE_PROJECT_ID" \
  --output "$HOME/.config/AgentDesk/personal-profile.yaml"
```

Validate:

```bash
skills/bitwarden-personal-profile/scripts/validate_profile.py "$HOME/.config/AgentDesk/personal-profile.yaml"
```

Load normalized JSON:

```bash
skills/bitwarden-personal-profile/scripts/load_profile.py --json
```

## Bitwarden Notes

Use Bitwarden Secrets Manager as the private source of truth. Store the profile YAML as a single secret value with key `ADC_PERSONAL_PROFILE_YAML`.

Before using direct CLI operations, the Bitwarden Secrets Manager CLI must be installed and authenticated:

```bash
export BWS_ACCESS_TOKEN="..."
```

The materialized file is local private state. It is not a Git artifact.

## Resources

- `references/personal-profile.schema.json`: committed schema.
- `references/personal-profile.example.yaml`: committed fake example.
- `references/language-policy.md`: language selection rules.
- `references/bitwarden-secrets-manager-schema.md`: Bitwarden Secrets Manager mapping.
- `scripts/init-private-profile.sh`: create local private profile path from the fake example.
- `scripts/profile_to_bitwarden_import.py`: convert personal profile YAML into Bitwarden import JSON.
- `scripts/profile_to_bws_secret.py`: create or update the profile secret through `bws`.
- `scripts/bitwarden_to_profile.py`: materialize a profile from Bitwarden import/export JSON or `bws`.
- `scripts/materialize_profile.py`: legacy Password Manager secure-note fallback.
- `scripts/validate_profile.py`: validate structure and language maps.
- `scripts/load_profile.py`: load the private profile for other skills.
