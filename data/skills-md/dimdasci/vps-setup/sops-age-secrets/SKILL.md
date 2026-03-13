---
name: sops-age-secrets
description: |
  SOPS and age encryption for secrets management in git repositories. Use when:
  (1) Setting up encrypted secrets in a project (initial .sops.yaml configuration)
  (2) Encrypting/decrypting YAML, JSON, ENV, or INI files with age keys
  (3) Managing age keys (generation, distribution, rotation)
  (4) Configuring path-based encryption rules for different environments
  (5) Integrating SOPS decryption in CI/CD pipelines (GitHub Actions, GitLab CI)
  (6) Troubleshooting SOPS decryption failures or key issues
  (7) Selective encryption with encrypted_regex patterns
---

# SOPS + age Secrets Management

Encrypt secrets in git with SOPS using age keys. Values are encrypted with AES256-GCM; keys are simple X25519 keypairs.

## Quick Reference

| Task | Command |
|------|---------|
| Generate age key | `age-keygen -o keys.txt` |
| Extract public key | `age-keygen -y keys.txt` |
| Encrypt file | `sops encrypt file.yaml > file.enc.yaml` |
| Decrypt file | `sops decrypt file.enc.yaml` |
| Edit encrypted file | `sops edit file.enc.yaml` |
| Update recipients | `sops updatekeys -y file.enc.yaml` |
| Rotate data key | `sops rotate -i file.enc.yaml` |

## Initial Setup

### 1. Generate Keys

```bash
# Create key directory
mkdir -p ~/.config/sops/age

# Generate keypair
age-keygen -o ~/.config/sops/age/keys.txt
# Output: public key: age1abc123...
```

### 2. Create .sops.yaml

At repository root:
```yaml
creation_rules:
  - age: age1yourpublickeyhere...
```

### 3. Encrypt First File

```bash
sops encrypt config/secrets.yaml > config/secrets.enc.yaml
rm config/secrets.yaml
git add config/secrets.enc.yaml .sops.yaml
```

## Core Workflows

### Encrypt New File
```bash
# Create plaintext file
cat > secrets.yaml << 'EOF'
database:
  password: secret123
api_key: abc-xyz
EOF

# Encrypt (uses .sops.yaml rules)
sops encrypt secrets.yaml > secrets.enc.yaml
rm secrets.yaml
```

### Edit Encrypted File
```bash
# Opens decrypted in $EDITOR, re-encrypts on save
sops edit secrets.enc.yaml
```

### Decrypt for Use
```bash
# To stdout
sops decrypt secrets.enc.yaml

# To file
sops decrypt secrets.enc.yaml > secrets.yaml

# Extract single value
sops decrypt --extract '["database"]["password"]' secrets.enc.yaml
```

### Pass to Process (No File)
```bash
# As environment variables
sops exec-env secrets.enc.yaml './deploy.sh'

# As temporary file
sops exec-file secrets.enc.yaml 'source {}'
```

## Multi-Environment Configuration

```yaml
# .sops.yaml
creation_rules:
  # Production - admin + CI only
  - path_regex: ^config/secrets/prod\..*
    age: >-
      age1admin...,
      age1cicd...

  # Staging/Dev - broader access
  - path_regex: ^config/secrets/.*
    age: >-
      age1admin...,
      age1cicd...,
      age1dev...
```

## Selective Encryption

Only encrypt sensitive keys (keeps file readable):
```yaml
creation_rules:
  - age: age1...
    encrypted_regex: ^(password|secret|token|key|api_key|private)$
```

Result:
```yaml
database:
  host: localhost           # plaintext
  password: ENC[AES256_GCM,data:...,type:str]  # encrypted
```

## CI/CD Integration

### GitHub Actions
```yaml
- name: Decrypt secrets
  env:
    SOPS_AGE_KEY: ${{ secrets.SOPS_AGE_KEY }}
  run: sops decrypt config/secrets.enc.yaml > secrets.yaml
```

Store `AGE-SECRET-KEY-1...` in repository secrets as `SOPS_AGE_KEY`.

### Environment Variables
```bash
# Key file location
export SOPS_AGE_KEY_FILE=/path/to/keys.txt

# Key value directly (CI/CD)
export SOPS_AGE_KEY="AGE-SECRET-KEY-1..."
```

## Key Management

### Add New Recipient
1. Update `.sops.yaml` with new public key
2. Re-encrypt existing files:
   ```bash
   sops updatekeys -y file.enc.yaml
   ```

### Remove Recipient
1. Remove from `.sops.yaml`
2. Re-encrypt and rotate:
   ```bash
   sops updatekeys -y file.enc.yaml
   sops rotate -i file.enc.yaml
   ```

### Key Locations

| Platform | Default Path |
|----------|--------------|
| Linux | `~/.config/sops/age/keys.txt` |
| macOS | `~/Library/Application Support/sops/age/keys.txt` |

## Reference Files

| File | When to Read |
|------|--------------|
| [age-keys.md](references/age-keys.md) | Key generation, storage, distribution patterns |
| [sops-config.md](references/sops-config.md) | .sops.yaml syntax, path rules, key groups |
| [cli-reference.md](references/cli-reference.md) | Full command reference, all flags |
| [ci-cd-patterns.md](references/ci-cd-patterns.md) | GitHub Actions, GitLab CI, Docker integration |
| [troubleshooting.md](references/troubleshooting.md) | Common errors and solutions |

## Common Issues

| Problem | Solution |
|---------|----------|
| "could not decrypt data key" | Wrong key - check `SOPS_AGE_KEY_FILE` or key location |
| "no matching keys found" | File uses Shamir key groups - need multiple keys |
| `.sops.yaml` not found | Run from repo root or ensure file is in parent directory |
| path_regex not matching | Use regex syntax (`.*\.yaml$`), not glob (`*.yaml`) |

## Security Notes

- **Never commit private keys** - Add `keys.txt`, `*.agekey` to `.gitignore`
- **Use dedicated CI keys** - Easier to rotate, limit scope
- **Rotate data keys** - Run `sops rotate` periodically
- **Limit recipients** - Production files should have minimal access

## Official Documentation

| Topic | URL |
|-------|-----|
| SOPS | https://getsops.io/docs/ |
| SOPS GitHub | https://github.com/getsops/sops |
| age | https://github.com/FiloSottile/age |
