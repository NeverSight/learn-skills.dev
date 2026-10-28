---
name: dependency-cooldown
description: |
  Configure a minimum release age (cooldown) on package managers so freshly published
  versions are not installed for N days — a cheap, high-leverage defense against
  supply chain attacks (npm shai-hulud, axios typosquats, malicious post-install hooks).
  Use when the user asks to harden a project or their machine against supply chain
  attacks, set a "cooldown" / "bake period" / "min-release-age" / "exclude-newer",
  block too-fresh packages, or apply the recommendations from the Datadog "dependency
  cooldowns" or Matteo Collina gist. Covers npm, pnpm, yarn, uv, and pip.
  Do NOT use for: lockfile pinning, SCA scanning (Snyk/Dependabot), Poetry (no native
  support), or audit tooling.
metadata:
  imankulov.skills-sh-group: Security
  imankulov.skills-sh-order: "10"
  imankulov.claude-display-name: Dependency Cooldown
  imankulov.claude-category: development
  imankulov.claude-keywords: "dependency,cooldown,agent-skills"
---

# Dependency Cooldown

Set a minimum age (default **7 days**) below which a package version cannot be installed.
Most malicious releases are detected and yanked within hours, so a one-week gate filters
out the smash-and-grab incidents at near-zero cost.

## First question: user-level or project-level?

Ask the user (or infer from context) before editing anything:

- **User-level (global)** — Applies to every project the user works on. Best for
  individual developers hardening their own machine. Lives in the user's home directory.
- **Project-level** — Applies only to this repo. Best when the team has committed to
  the policy and wants it enforced via the repo's config files. Lives in the repo.

If both exist, project-level wins for that repo.

## Default value: 7 days

Use 7 days unless the user specifies otherwise. Each package manager uses different
units — the table below lists the **7-day value** for each.

| Manager   | Config key             | Unit     | 7-day value | Min version       |
|-----------|------------------------|----------|-------------|-------------------|
| npm       | `min-release-age`      | days     | `7`         | npm 11.10.0       |
| pnpm      | `minimumReleaseAge`    | minutes  | `10080`     | pnpm 10.16        |
| yarn      | `npmMinimalAgeGate`    | minutes  | `10080`     | yarn 4.10.0       |
| uv        | `exclude-newer`        | duration | `"7 days"`  | uv 0.9.17         |
| pip       | `uploaded-prior-to`    | ISO 8601 | `P7D`       | pip 26.1          |

Before writing config, check the installed version with `<manager> --version`; if it's
below the table's minimum, pause and offer the user an upgrade using the **Upgrade
Recipes** section below.

## Recipes

### npm

npm 11.10.0 is a late-2025 release; older npm rejects the key. If `npm --version`
reports anything earlier, pause and offer the user an upgrade with `npm install -g npm@latest`.

User-level:
```bash
npm config set min-release-age 7 --location=user
```

Verify by reading the file (`grep min-release-age ~/.npmrc`): `npm config get
min-release-age` may return `null` even when the value is set — a known display bug in
npm 11.

Project-level (`.npmrc` at repo root):
```
min-release-age=7
```

npm has no per-package exclusion mechanism. For a one-off bypass, pass the flag at
install time: `npm install foo --min-release-age=0`.

### pnpm

User-level (writes to `~/.config/pnpm/rc`):
```bash
pnpm config set minimumReleaseAge 10080 --location=user
# Verify: pnpm config get minimumReleaseAge
```

Project-level (`pnpm-workspace.yaml` at repo root — required even for non-workspace
repos; `package.json` is not accepted):
```yaml
minimumReleaseAge: 10080
minimumReleaseAgeExclude:
  - '@yourorg/*'
```

Add `minimumReleaseAgeExclude` for internal packages so your own org's releases are not
gated. pnpm 11+ defaults to `1440` (1 day) already — explicitly setting 10080 raises it
to 7 days.

For a one-off bypass: `pnpm install foo --config.minimumReleaseAge=0`.

### yarn (Berry, v4+)

Yarn classic (v1) has no cooldown support — upgrade to Berry, or use one of the other
managers.

User-level (`~/.yarnrc.yml`):
```yaml
npmMinimalAgeGate: 10080
```

Project-level (`.yarnrc.yml` at repo root):
```yaml
npmMinimalAgeGate: 10080
npmPreapprovedPackages:
  - "@yourorg/*"
```

Pass minutes as a **number**, not a string like `"7d"` — there is a known parsing bug
where the suffix is silently ignored, leaving the gate disabled. Confirm with
`yarn config get npmMinimalAgeGate`; it should return `10080`.

### uv

User-level: macOS `~/Library/Application Support/uv/uv.toml`; Linux
`~/.config/uv/uv.toml` (or `$XDG_CONFIG_HOME/uv/uv.toml`).
```toml
exclude-newer = "7 days"
```

Project-level (`pyproject.toml` under `[tool.uv]`):
```toml
[tool.uv]
exclude-newer = "7 days"

[tool.uv.exclude-newer-package]
"yourorg-internal" = "0 days"
```

Per-package overrides go in `exclude-newer-package`. Relative durations need uv 0.9.17+;
older uv requires an ISO 8601 timestamp.

For a one-off bypass: `uv add foo --exclude-newer="0 days"` (the same value the
per-package override uses to disable the gate).

### pip

If `pip` isn't on PATH (pyenv shims, virtualenv-only setups), substitute
`python3 -m pip` everywhere — `python3 -m pip --version`,
`python3 -m pip config set …`, and so on.

**pyenv / multi-Python setups**: the user-level `pip.conf` is read by *every* pip on
the machine. Check the version of each interpreter you actually use
(`~/.pyenv/versions/*/bin/python3 -m pip --version`), not just `python3 -m pip`.
A pip that's too old to understand `uploaded-prior-to` will error on every install
until you upgrade it.

User-level: macOS `~/Library/Application Support/pip/pip.conf`; Linux
`~/.config/pip/pip.conf`.
```ini
[install]
uploaded-prior-to = P7D
```

The value is an **ISO 8601 duration** (`P7D` = 7 days), *not* a human-readable string.
Pip rejects `"7 days"` with `Invalid isoformat string` — confirmed on pip 26.1.1. An
absolute datetime (`2026-05-01T00:00:00Z`) also works but freezes the gate in time.

Project-level — pip has no project-config file. If the project pins pip behavior, use
uv for resolution and export to `requirements.txt`, or document the flag in the repo's
CONTRIBUTING file: `pip install --uploaded-prior-to "P7D" -r requirements.txt`.

pip 26.0 only accepts absolute ISO timestamps; ISO 8601 durations require pip 26.1+.

For a one-off bypass on any install: `pip install --isolated foo` (ignores all config
files entirely).

### Poetry

Not supported. Poetry has no native cooldown. If the user insists, point them at
[AikidoSec/safe-chain](https://github.com/AikidoSec/safe-chain) as a wrapper, or
suggest migrating resolution to uv.

## Upgrade Recipes

Use these when a tool's version is below the minimum. Present the recipe and get
confirmation before running it — upgrading a package manager changes the user's
environment.

### npm

```bash
npm install -g npm@latest
```

### pnpm

How to upgrade depends on how pnpm was installed. Check with `which pnpm`:

- **Installed via npm global** (path contains `.nvm` or `node_modules`):
  ```bash
  npm install -g pnpm@latest
  ```
  Note: with nvm, global npm packages are per Node version. If you switch Node versions,
  pnpm won't be there. Use the standalone installer to avoid this:
  ```bash
  curl -fsSL https://get.pnpm.io/install.sh | sh -
  ```

- **Installed via standalone** (path contains `.local/share/pnpm` or similar):
  ```bash
  pnpm self-update
  ```

- **Installed via Homebrew**:
  ```bash
  brew upgrade pnpm
  ```

### pip (pyenv setups)

Upgrade every pyenv pip to 26.1+ before writing the config:

```bash
# Upgrade pip in all pyenv environments
for pip_bin in ~/.pyenv/versions/*/bin/pip; do
  "$pip_bin" install --upgrade pip
done
```

If a too-old pip already has the config written (bootstrap trap), use `--isolated` to
bypass the config for that one invocation:

```bash
pip install --isolated --upgrade pip
```

Then write the config only after all pips are confirmed at 26.1+.

## Workflow

1. Ask user-level or project-level (unless they already said).
2. Detect which managers are in scope:
   - Project: look for `package.json` (+ which lockfile), `pyproject.toml`,
     `requirements*.txt`, `.npmrc`, `.yarnrc.yml`, `pnpm-workspace.yaml`.
   - User: ask which the user actually uses, or apply to all installed ones.
3. Verify each tool's version meets the minimum; if too old, offer to upgrade using the
   Upgrade Recipes section. For pip/pyenv, upgrade all interpreters before writing config
   to avoid the bootstrap trap.
4. Apply the 7-day value from the table. Use the CLI form (`config set`) when the
   manager supports it; otherwise edit the config file directly.
5. For pnpm/yarn project-level, ask if the org has an internal package scope to add to
   the bypass list.
6. Read the value back with `<manager> config get <key>` (or inspect the file for
   managers without that command) to catch silent write failures, then print one line
   per manager confirming what changed and where.

## Sources

- [pnpm: Mitigating supply chain attacks](https://pnpm.io/supply-chain-security)
- [Matteo Collina — Configuring minimum release age across npm, pnpm, and yarn](https://gist.github.com/mcollina/b294a6c39ee700d24073c0e5a4e93104)
- [Datadog Security Labs — The case for dependency cooldowns](https://securitylabs.datadoghq.com/articles/dependency-cooldowns/)
- [uv docs — exclude-newer](https://docs.astral.sh/uv/reference/settings/#exclude-newer)
- [pip docs — uploaded-prior-to](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-uploaded-prior-to)
