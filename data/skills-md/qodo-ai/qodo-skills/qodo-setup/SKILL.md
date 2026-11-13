---
name: qodo-setup
description: Set up Qodo in a coding agent — install the CLI, sign in, and verify tools. Use after plugin installation, on setup requests, or when a Qodo skill finds a missing CLI or login.
owner: Qodo
metadata:
  vendor: qodo
  version: "1.0.14"
  recommended: "true"
  package: "qodo"
  distribution: "skills-sh"
---

# Set up Qodo

## Description

Skill installation is not readiness. References are relative to this SKILL.md.

## Prerequisites

Shell or host-connected QAR MCP; never handle credentials.

## Instructions

### Connected MCP

Inspect QAR schemas; call a harmless read and check isError before structuredContent. A catalog proves neither read nor write access; never test-write. Host/QAR own auth. Report missing tools, MT-AUTH-FORBIDDEN or connection errors; never request API keys. For MCP-only setup, hand back. CLI collection uses the same deployment.

### Runtime

PowerShell: resolve the verified native/Node invocation in [runtime.md](references/runtime.md). POSIX: probe:

```sh
qodo --version
```

Then try `"${QODO_HOME:-$HOME/.qodo}/bin/qodo" --version` if missing. Use that verified installer if missing. Setup covers installation subject to host approvals; plugin installation alone does not.
Keep the executable as `<qodo>`. Require Qodo CLI **2.0.0 or newer** before auth; compatible versions skip update preflight.

### Runtime compatibility recovery

For old/unparseable versions, stop authenticated calls and explain. Before update checks/changes, test only whether QODO_UPDATE_BASE_URL is set; never print/change it. If set, stop for user resolution. All routes preserve origin, exact versions and update holds; never replace an exact version with a channel.
For parsed1.x, normal `qodo update` reaches approved stable2.x only if that origin enables migration. Require a newer compatible same-origin2.x target from the selected route's supported check. If legacy aliases serve1.x, check latest-2 before proposing `qodo update --channel latest-2`. Missing/failed checks stop; never assume activation or unrelated future-major authority.
For unparseable version/no supported updater, use the checksum-pinned installer reference. Preserve supported customer selectors/settings; normal verified installation selects the approved version. Explain the route; reuse covering runtime/installation authority or ask once before changing it. Make one approved attempt, reprobe unadorned version, and stop on denial/failure/incompatibility without another route, skill edits or an auth diagnosis.

### Connect and verify

Run:

```sh
<qodo> read whoami --json --skill qodo-setup --skill-version 1.0.14 --distribution skills-sh
```

Reuse success. Read [authentication.md](references/authentication.md) before login on failure; preserve deployment, never fall back to Cloud. Wait/recheck identity; stop on denial/cancellation. Diagnostic approval is not blanket authority.
Only after identity succeeds run:

```sh
<qodo> tools --refresh --json --skill qodo-setup --skill-version 1.0.14 --distribution skills-sh
```

Require task capability. On failure report signed in but tools unavailable, exact error and that retry; do not log in again. Reuse verified context with host approvals.

## Configuration

Setup does not authorize enterprise installation/maintenance. Disclose packages/maintenance; preserve opt-outs, edits, owners and choices. Never install optional Standards. For QODO_NOTICE/repeated Kiro read approvals read [host-recovery.md](references/host-recovery.md). CLI owns credentials/transport/updates; lifecycle owners update skills.
## Error Handling

Report the error and one next action. Never claim readiness after failure, disable Keychain, copy credentials, change permissions or offer unrestricted approvals.

## 4. Hand off

Confirm Qodo connection/tools and return to the task. Readiness does not guarantee later access.
