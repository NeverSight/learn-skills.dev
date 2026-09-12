---
name: gen-ssh-key
description: 'Generate SSH keys per team standards and return the public key. Ed25519 by default, RSA 4096 as fallback (RSA 2048 is never allowed); private keys are chmod 600 and named after the service. Use this skill whenever the user wants an SSH key, keypair, deploy key, or login key for a service or machine, or mentions ssh-keygen/puttygen — e.g. "generate ssh key", "create an ssh keypair", "make a login key for service xxx", "generate a deploy key" — even if they do not mention team standards. Prefers puttygen (.ppk/.pem/.pub); falls back to ssh-keygen.'
---

# Generate SSH Keys (Team Standard)

Run one script to produce a standards-compliant SSH key; do not hand-roll
ssh-keygen commands. The script bakes in the team rules (key type, naming,
permissions, overwrite guard), so using it is what guarantees compliance.

## Workflow

1. Derive `<name>` from the service or purpose the user mentions
   (e.g. "jumpserver", "gitlab"). Kebab-case; no spaces or slashes.
2. Pick flags from the request:
   - RSA explicitly requested: add `--rsa` (always RSA 4096; the script
     refuses to produce RSA 2048, which the team bans as too weak).
   - Passphrase wanted: write the passphrase to a temporary file, pass
     `--passphrase-file <file>`, and delete the file afterwards. Never put
     a passphrase on the command line.
   - Machine-readable result wanted (or another program consumes it): add
     `--json` (pure JSON on stdout; diagnostics stay on stderr).
   - The user named a destination: add `--out-dir <dir>` (this may be the
     current directory, e.g. `--out-dir .`), and keys go straight there.
     Otherwise, when neither `--out-dir` nor the skill's `.env`
     (`SSH_KEY_OUTPUT_DIR`) is set, keys go to the default `~/.ssh/generated-keys`.
3. Run the script from the skill directory:

   ```bash
   ./scripts/gen-ssh-key.sh <name> [flags]
   ```

4. Report back: give the user the public key content (it is safe to share)
   and the file paths. Never print, quote, or transmit the private key
   contents, and never write the passphrase into results or logs — the JSON
   output intentionally carries only `passphrase_protected: true`.

If the target files already exist the script refuses; ask the user before
retrying with `--force`.

## Examples

```bash
./scripts/gen-ssh-key.sh jumpserver                       # Ed25519 -> jumpserver.{ppk,pem,pub}
./scripts/gen-ssh-key.sh gitlab --rsa                     # RSA 4096
./scripts/gen-ssh-key.sh svc-x --passphrase-file ./pp.txt --json
./scripts/gen-ssh-key.sh jumpserver --out-dir ~/.ssh/generated-keys
./scripts/gen-ssh-key.sh jumpserver --comment "you@example.com"
./scripts/gen-ssh-key.sh jumpserver --dry-run             # show the plan only
./scripts/gen-ssh-key.sh --tool ssh-keygen jumpserver     # skip puttygen
./scripts/gen-ssh-key.sh -h                               # full flag reference
```

## Team rules baked into the script

- Key type: Ed25519 by default; `--rsa` means RSA 4096; RSA 2048 never.
- Tool: puttygen preferred (adds `.ppk` for PuTTY users); ssh-keygen fallback.
- Naming: `<name>.ppk / .pem / .pub` so keys are identifiable by service.
- Comment `-C` defaults to `<name>`; override with `--comment`.
- Private key `chmod 600`; newly created output directories `chmod 700`.
- Overwrite refused by default; `--force` required.

## Configuration

Output directory precedence: `--out-dir` > `SSH_KEY_OUTPUT_DIR` in `.env`
(at the skill root, one level above `scripts/`) > the built-in default
`~/.ssh/generated-keys`. When both `--out-dir` and `.env` are absent, keys go
to that default rather than the current directory (so they never silently land
in the skill directory); pass `--out-dir .` if you do want the current
directory. To change the default persistently, `cp .env.example .env` at the
skill root and point `SSH_KEY_OUTPUT_DIR` elsewhere.

## Artifacts

| File | Purpose |
|------|---------|
| `<name>.ppk` | PuTTY-native key (puttygen path only) |
| `<name>.pem` | OpenSSH private key (chmod 600, keep secret) |
| `<name>.pub` | OpenSSH public key (share this; import / authorized_keys) |

## Exit codes

`0` success; `1` bad argument, target exists, or generation failed; `2` no
usable tool (neither puttygen nor ssh-keygen installed).
