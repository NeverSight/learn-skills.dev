---
name: project-triage
description: Detect Frappe project type, installed apps, version, and tooling. Use as the first step when working on any Frappe/ERPNext codebase to understand the project structure before making changes.
---

# Frappe Project Triage

Quickly analyze a Frappe project to determine its type, installed apps, version, and available tooling.

## When to use

- First step when opening a new Frappe project
- Before making any code changes to understand the codebase
- When debugging to determine which apps/versions are involved
- To identify the development environment (Bench vs Frappe Manager)

## Inputs required

- Project root path (where `apps/`, `sites/`, or app code lives)
- Access to run shell commands (for version checks)

## Procedure

### 0) Identify project structure

Check for these patterns:

| Pattern | Project Type |
|---------|--------------|
| `apps/` + `sites/` directories | Bench installation |
| `docker-compose.yml` with frappe | Frappe Manager site |
| `pyproject.toml` or `setup.py` with frappe | Standalone app |
| `doctype/` directory | Inside an app module |

### 1) Detect installed apps

```bash
# Inside Bench/FM shell
bench --site <site> list-apps

# Or check apps directory
ls apps/
```

### 2) Check Frappe version

```bash
# Inside Bench/FM shell
bench version

# Or check from Python
bench --site <site> console
>>> frappe.__version__
```

### 3) Identify tooling

| File/Directory | Tooling |
|----------------|---------|
| `Procfile` | Standard bench |
| `docker-compose.yml` | Docker/FM |
| `cypress/` | UI testing available |
| `.github/workflows/` | CI configured |
| `package.json` with `@frappe/*` | JS build tooling |

### 4) Check development mode

```bash
# Check site config
bench --site <site> console
>>> frappe.conf.developer_mode
```

## Verification

- [ ] Project type identified (bench/FM/standalone app)
- [ ] Installed apps listed
- [ ] Frappe version known
- [ ] Development mode status confirmed
- [ ] Available tooling documented

## Failure modes / debugging

- **No site found**: May be inside an app directory, navigate to bench root
- **bench command not found**: Not in bench environment, use `fm shell` or activate venv
- **Permission errors**: Check if running as correct user

## Escalation

If project structure is unclear:
1. Look for `hooks.py` to identify app root
2. Look for `sites/common_site_config.json` for bench root
3. Check git remote for app repository identification

## Output format

After triage, document:
```
Project Type: [bench|frappe-manager|standalone-app]
Frappe Version: X.Y.Z
Installed Apps: [list]
Developer Mode: [yes|no]
Tooling: [list]
Site Name: <site>
```

Use this output to route to the appropriate skill:
- DocType work → `doctype-development`
- API work → `api-development`
- Testing → `testing`
- Enterprise patterns → `enterprise-patterns`

## Guardrails

- **Never modify code** before completing triage - understand the project first
- **Check for custom apps** that may override standard behavior
- **Verify site exists** before running site-specific commands
- **Check developer_mode** before making schema changes (required for DocType modifications)
- **Note Node.js version** - frontend builds require compatible Node (typically 18+ for v15)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Running `bench migrate` without site | Affects wrong/default site | Always use `--site sitename` |
| Assuming ERPNext is installed | Import errors, missing DocTypes | Check `list-apps` output first |
| Missing FM shell context | bench commands not found | Use `fm shell sitename` first |
| Wrong directory level | Commands fail silently | Navigate to bench root (where `apps/` exists) |
| Ignoring custom app overrides | Unexpected behavior | Check hooks.py for overrides |
| Not checking Python version | Syntax/compatibility errors | Verify Python >= 3.10 for v15+ |
