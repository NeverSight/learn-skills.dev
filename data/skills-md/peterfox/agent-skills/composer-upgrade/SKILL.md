---
name: composer-upgrade
description: Guides PHP project upgrades using Composer commands. Use when helping users upgrade PHP packages, understand dependency conflicts, interpret `composer outdated` output, use `composer why-not` to diagnose version constraints, use `composer why` to trace dependencies, use `composer bump` to harden version constraints after upgrading, plan safe upgrade paths, or resolve package version conflicts in composer.json.
---

# Composer Upgrade

## Upgrade Workflow

Follow this sequence when upgrading a PHP project:

1. **Identify what's outdated** → `composer outdated`
2. **Diagnose blockers** → `composer why-not vendor/package version`
3. **Trace dependencies** → `composer why vendor/package`
4. **Update packages** → `composer update vendor/package --with-all-dependencies`
5. **Test**
6. **Harden constraints** → `composer bump` (applications only)

See [references/commands.md](references/commands.md) for full flag reference.
See [references/upgrade-workflow.md](references/upgrade-workflow.md) for detailed strategies.

## Core Commands

### composer outdated

Lists packages with newer versions available.

```bash
composer outdated                    # all packages
composer outdated --direct           # only packages in require/require-dev
composer outdated symfony/*          # filter by pattern
composer outdated --format=json      # machine-readable output
```

**Reading the output:**
- **Red** = semver major bump (breaking changes likely)
- **Yellow** = semver minor/patch (safe upgrade)
- `!` marker = package is not semver-safe (minor/patch but breaking)

Columns: `name | current | latest | description`

### composer why-not

Shows what prevents upgrading a package to a specific version.

```bash
composer why-not vendor/package 2.0
composer why-not php 8.2            # check what blocks a PHP version requirement
composer why-not vendor/package "*" # check what blocks any upgrade
```

Output shows the dependency chain: which packages require conflicting versions.

### composer why

Shows which installed packages depend on a given package.

```bash
composer why vendor/package
composer why-not vendor/package     # inverse: what conflicts with it
```

### composer update

```bash
composer update                                  # update all (risky on large projects)
composer update vendor/package                   # update one package
composer update vendor/package --with-all-dependencies  # also update its deps
composer update --dry-run                        # preview changes without applying
```

## Common Patterns

### "Why can't I update X?"

```bash
composer why-not vendor/package 3.0
```

Read the output to find which package constrains it, then check if that constraining package itself can be updated.

### "What's blocking my PHP version upgrade?"

```bash
composer why-not php 8.2
```

Lists every package that lacks a `php: ^8.2` constraint, sorted by most blocking.

### "Safe incremental upgrade"

Prefer updating direct dependencies one at a time with `--dry-run` first:

```bash
composer update vendor/package --with-all-dependencies --dry-run
composer update vendor/package --with-all-dependencies
```

### Relaxing constraints in composer.json

When `why-not` reveals a constraint in your own `composer.json`, update the version constraint and re-run:

```json
"require": {
    "vendor/package": "^3.0"   // was "^2.0"
}
```

Then: `composer update vendor/package`

### Hardening constraints after upgrading (applications)

After updating packages in an application, run `composer bump` to raise the lower bounds of constraints in `composer.json` to the currently installed versions:

```bash
composer bump                  # harden all constraints
composer bump vendor/package   # harden one package
composer bump --dev-only       # only require-dev (safe for libraries too)
```

Before: `"symfony/console": "^6.0"` → After: `"symfony/console": "^6.4.3"`

This prevents future `composer install` runs from resolving older versions that weren't tested. It does **not** prevent future minor/patch upgrades — the `^` is preserved.

**Enable auto-bump in `composer.json` for applications:**

```json
{
    "config": {
        "bump-after-update": true
    }
}
```

With this set, Composer automatically runs `bump` after every `composer update`. Use `"dev"` or `"no-dev"` to limit which dependency group is bumped.

> **Applications only**: Do not run `composer bump` (without `--dev-only`) on libraries. Narrowing lower bounds of library dependencies causes version conflicts for downstream consumers.
