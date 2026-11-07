---
name: snap-analyzer
description: >
  Scans an existing application codebase and produces a snap-analysis.json file that
  captures everything needed to package the app as a snap: language/runtime, build system,
  entry points, system resource requirements, snap plugin recommendation, interface list,
  hook requirements, confinement type, and layout needs. Does NOT write snapcraft.yaml —
  its output is consumed by the snapcraft-author skill. WHEN: analyze snap requirements,
  snap analysis, scan for snap interfaces, identify snap plugs, snap project analysis,
  pre-packaging scan, snap dependency discovery, snap confinement analysis, snap interface
  mapping, prepare snap packaging.
license: "Apache-2.0"
metadata:
  author: "Canonical"
  version: "1.4.0"
  summary: "Scans a codebase and writes snap-analysis.json — a structured packaging specification consumed by snapcraft-author, including target_arch for cross-arch builds."
  tags:
    - snap
    - snapcraft
    - analysis
    - canonical
    - linux
---

# Snap Analyzer

Scans the current project directory and writes a `snap-analysis.json` — a complete
packaging specification that the `snapcraft-author` skill consumes to generate
`snapcraft.yaml`, lifecycle hooks, and a packaging guide.

> **Where the file goes:** write it to a project-scoped path under `/tmp`, not the
> project root — it is a transient hand-off artifact, not a project deliverable, so it
> never pollutes the repo or gets committed by accident. The canonical path is:
>
> ```
> /tmp/snap-analysis-<dirname>.json     where <dirname> = basename of the project dir
> ```
>
> Compute it once and reuse it verbatim (the `snapcraft-author` skill reads the same path):
>
> ```bash
> ANALYSIS_FILE="/tmp/snap-analysis-$(basename "$PWD").json"
> ```

---

## Step 1: Codebase Analysis

Read `references/analysis-checklist.md` and work through every section systematically.
Inspect actual files — `Makefile`, `go.mod`, `package.json`, `*.service`, `CMakeLists.txt`,
source imports, README — before drawing conclusions. Do not ask the user for information
that can be read from the repository.

Record findings for:

- **Language / runtime** — Go, Python, Node.js, C/C++, Rust, Java, shell, etc.
- **Build system** — make, cmake, meson, cargo, go build, npm/yarn, setuptools, etc.
- **Entry points** — binary names, wrapper scripts, systemd units
- **App type** — command, service, desktop GUI, or several. Decide it from upstream's main
  usage (README examples, `--help`, man pages, bundled unit files), not from what the README
  calls the app: an app run with user-chosen arguments in the foreground is a command app,
  and a service app needs a real signal (bundled unit or init script, documented service
  mode, fixed startup config, or start-on-boot docs). See `references/analysis-checklist.md`
  §4a, and record the usage in `notes[]`
- **System resources accessed** — network sockets, filesystem paths, devices, D-Bus,
  audio, display server, secrets, hardware, etc.
- **Hardcoded paths** — `/etc/<name>`, `/var/lib/<name>`, `/run/<name>`, etc.
- **Version** — from `go.mod`, `package.json`, `CMakeLists.txt`, `setup.py`, a `VERSION`
  file, or the most recent git tag
- **Shipped script interpreters** — shebang lines on any helper script that ends up in the
  shipped `apps[]` surface, cross-checked against the build-system-inferred `stage_packages`
  (see the checklist's shebang item)

---

## Step 2: Determine Confinement

**Always default to `strict` confinement.** Classic confinement must only be considered
when the app genuinely cannot operate within the snap interface system even after interfaces
are applied. The primary signal is: **does the app need to exec arbitrary host binaries
that cannot be known at packaging time?**

| App type | Classic potentially needed |
|---|---|
| Text editors / IDEs, shells, debuggers, terminal multiplexers | Yes — spawn arbitrary host programs |
| Compiler/toolchain, build systems, package managers | Yes — arbitrary host paths and tools |
| CI/CD runners | Yes — arbitrary pipelines |
| Image editors, media players, file managers, network tools | No — strict + interfaces is sufficient |

### If classic confinement appears necessary

Before recording `"confinement": "classic"` in the output, **stop and ask the user**
whether they want to proceed with classic confinement. Frame the question with these
caveats:

> ⚠️ **Classic confinement has significant restrictions:**
>
> 1. **Snap Store approval required** — Classic snaps must be manually reviewed and
>    approved by the Snap Store team before they can be distributed. This process takes
>    on average **3–5 business days** and approval is not guaranteed.
>    See: https://documentation.ubuntu.com/snapcraft/latest/how-to/crafting/enable-classic-confinement/#request-classic-confinement-on-the-snap-store
>
> 2. **Not supported on Ubuntu Core** — Classic confinement is incompatible with Ubuntu
>    Core devices (e.g. IoT/embedded targets). If this snap may ever run on Ubuntu Core,
>    classic confinement is not a viable option.
>    See: https://forum.snapcraft.io/t/building-classic-snap-on-ubuntu-core/4243
>
> **Recommendation:** Use `strict` confinement with the appropriate interfaces where
> possible. Would you like to proceed with classic confinement, or continue with strict?

If the user chooses **strict**, record `"confinement": "strict"` and continue with
interface mapping (Step 4) to cover the app's requirements.

If the user explicitly confirms **classic**, record `"confinement": "classic"` and add
both caveats above to `notes`.

Set `grade: stable` for production-ready apps, `devel` for work-in-progress.

---

## Step 3: Select Plugin

Choose the snapcraft plugin that best fits the build:

| Condition | Plugin |
|---|---|
| Go module project (`go.mod` present) | `go` |
| Python project (`setup.py` / `pyproject.toml`) | `python` |
| Node.js project (`package.json`) | `npm` |
| CMake project (`CMakeLists.txt`) | `cmake` |
| Meson project (`meson.build`) | `meson` |
| Rust/Cargo project (`Cargo.toml`) | `rust` |
| Non-standard or multi-stage build | `nil` with explicit `override-build` commands |
| Pre-built binaries / scripts only | `dump` |

If post-build steps are needed on top of a language plugin (e.g. fetching assets,
compiling grammars), note them in `build.override_build_extra` — snapcraft-author will add an
`override-build` that calls `craftctl default` first then appends the extra steps.

---

## Step 4: Map Interfaces

For each system resource identified in Step 1, find the corresponding snap interface.
Consult `references/snap-interfaces-catalog.md`.

For each interface record:
- The interface name
- Which app(s) require it
- Whether it auto-connects (AC) or requires a manual `snap connect` (MC)
- The detection reason (one sentence)

---

## Step 5: Determine Hooks

Consult `references/snap-hooks-reference.md`. Add a hook to the list **only** when the
app has a genuine lifecycle requirement:

- `install` — first-run directory creation, initial config, default values
- `configure` — validate and apply `snap set` changes. **Required whenever the snap has
  any snap option**: snapd rejects every `snap set` on a snap without a `configure` hook
  (`snap "<name>" has no "configure" hook`), even when the app reads the option itself.
- `connect-plug-*` / `disconnect-plug-*` — react to interface connect/disconnect
- `pre-refresh` / `post-refresh` — state migration around updates

**Snap options.** Search the whole repository (including wrapper scripts and sourced
helpers) for `snapctl get`, and note any option your plan seeds with `snapctl set`. Record
each such option once in top-level `config_options[]` (see Step 6). Whenever
`config_options[]` is non-empty:

- list `configure` in `hooks` — the pipeline's contract schema rejects an analysis that doesn't
- list `install` when any option has a non-null `default`, so the install hook can seed it

---

## Step 6: Write snap-analysis.json

Write the file to the project-scoped `/tmp` path (`/tmp/snap-analysis-$(basename "$PWD").json`),
**not** the project root. Use this exact schema:

```json
{
  "schema_version": "1.3",
  "project": {
    "name": "<snap-name>",
    "version": "<version>",
    "summary": "<one-line summary, max 78 chars>",
    "description": "<multi-line description>",
    "license": "<SPDX identifier or null>",
    "grade": "stable | devel"
  },
  "snap": {
    "base": "core24",
    "confinement": "strict | classic",
    "classic_reason": "<explanation or null>"
  },
  "build": {
    "plugin": "<plugin name>",
    "plugin_config": {},
    "build_packages": [],
    "stage_packages": [],
    "override_build_extra": null
  },
  "apps": [
    {
      "name": "<app-name>",
      "command": "<path/to/binary>",
      "daemon": null,
      "plugs": ["<interface-name>"],
      "environment": {}
    }
  ],
  "hooks": ["<hook-name>"],
  "config_options": [
    {
      "key": "<snap option key, e.g. daemon.port>",
      "source": "snapctl",
      "type": "port | enum | integer | boolean | path | string",
      "allowed_values": [],
      "default": "<default value as a string, or null>",
      "restart_required": true
    }
  ],
  "layouts": {
    "<snap-path>": { "bind": "<snap-variable-path>" }
  },
  "interfaces": [
    {
      "name": "<interface-name>",
      "apps": ["<app-name>"],
      "auto_connected": true,
      "reason": "<one sentence>"
    }
  ],
  "notes": ["<any packaging caveat or assumption worth flagging>"],
  "target_arch": null
}
```

**Field rules:**
- `apps[].daemon`: `null` for command apps; `"simple"`, `"forking"`, or `"notify"` for service
  apps. Follow checklist §4a: a command app by default, a service app only for a real
  signal. When both apply, name the command app after the binary and the service app
  `daemon`
- `apps[].command` for a command app: the binary, or a wrapper that ends in
  `exec "$SNAP/<path>/<binary>" "$@"`. Never hardcode a path or flag the user chooses per
  run; describe any wrapper in `notes[]`
- `apps[].plugs`: declare `home` / `removable-media` only on apps that can reach
  user-chosen paths
- `apps[].plugs`: list only interface names, not full plug definitions
- `build.plugin_config`: plugin-specific keys (e.g. `{"go-importpath": "..."}` for the go plugin)
- `layouts`: only include when the app hardcodes paths outside of snap-writable locations
- `hooks`: empty array `[]` when no hooks are needed; must contain `configure` whenever
  `config_options` is non-empty
- `config_options`: one entry per snap option (omit the field, or use `[]`, when there are
  none). `source` is `"snapctl"` when the app or its wrapper reads the option with
  `snapctl get`. `type` drives the validation the `configure` hook generates: use `boolean`
  for on/off flags that accept only `true`/`false`, `enum` with `allowed_values` for a fixed
  set of values, and `string` only for free-form text. `restart_required` is `true` when a
  running daemon reads the option only at startup, so the hook must restart it
- `notes`: include classic-confinement store-review warning if applicable; include any
  assumption that snapcraft-author cannot verify without reading the source
- `target_arch`: `null` means build for the host architecture (the default — leave it `null`
  unless a non-host architecture was explicitly requested). When the caller
  (`snap-builder`'s Phase 0.1a) provides a target architecture, or the user names one
  directly, record it as one of `amd64`/`arm64`/`armhf`/`i386`/`ppc64el`/`s390x`/`riscv64`
- `schema_version`: always `"1.3"`, whichever optional fields are populated

Before reporting, check:
- if `config_options` is non-empty, `hooks` contains `configure`;
- every snap option is read by the upstream code or by the wrapper of a justified service
  app, never invented for a plain command;
- `notes[]` records upstream's main usage, and a service-only snap records why it has no
  command app.

---

## Step 7: Report

After writing the analysis file, summarize in the chat (state the full `/tmp` path so the
user and the `snapcraft-author` skill know where it is):

- **Language / plugin** chosen and why
- **Apps** — each app's type (command or service) and the upstream usage or service
  signal behind it
- **Confinement** chosen and why (especially if classic)
- **Interfaces** listed — which auto-connect and which require `snap connect`
- **Hooks** identified and why
- **Snap options** — each key with its type and default
- **Layouts** required and why
- Any open questions or assumptions recorded in `notes`

Do **not** generate `snapcraft.yaml` or any other snap artifact — that is the
`snapcraft-author` skill's responsibility.

---

## Resources

| File | Purpose |
|---|---|
| `references/analysis-checklist.md` | Systematic checklist for scanning a codebase |
| `references/snap-interfaces-catalog.md` | Maps system resources to snap interface names, AC/MC status |
| `references/snap-hooks-reference.md` | Reference for snap lifecycle hooks |
