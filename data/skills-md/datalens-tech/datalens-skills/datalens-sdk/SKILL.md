---
name: datalens-sdk
description: >-
  Use this skill for any Yandex DataLens automation task through the Python package
  `datalens-sdk`. Trigger on: DataLens, datalens, даталенс, chart, чарт, график, dashboard,
  дашборд, dataset, датасет, connection, подключение, workbook, воркбук, collection, коллекция,
  wizard chart, QL chart, editor chart, BI automation, автоматизация DataLens, "create a
  dashboard", "построй дашборд", "создай чарт", "export dataset", or "clone dashboard"; entity
  ids such as dataset_id, chart_id, dashboard_id, or workbook_id; and requests to create, update,
  inspect, import, export, copy, or diagnose DataLens objects with code. NOT for: business
  questions about metric values; viewing or screenshotting the DataLens web UI; embedding or
  iframes; raw SQL/YQL analysis that does not manage DataLens entities; raw HTTP API calls;
  standalone HTML pages or reports, except publishing or managing them through this SDK.
license: Apache-2.0
metadata:
  domain: datalens
---

# DataLens SDK

Operate Yandex DataLens through the official Python SDK — never hand-built HTTP requests.

Before continuing, locate and read the available skill whose name or namespaced basename is
`datalens`. It supplies the shared installation and object-model context that applies alongside
these SDK instructions. If it is absent, report an incomplete public DataLens skill installation
and stop. After reading it, return here for SDK setup and execution.

**The instructions for this skill are stored inside the installed `datalens-sdk` package**, and are
extended there by whatever DataLens installation the environment targets. The SDK is a 0.x alpha
where minor releases rename classes and methods, so instructions that shipped separately would
describe an API the user does not have. Load them from the package before doing anything else.

If the user is only asking what the SDK is or whether it fits their task, answer that much from
this file and stop. Do not run bootstrap or install a package merely to read its documentation.

## Bootstrap, then load the instructions

Before the first SDK operation in a session, resolve this wrapper skill's directory to an absolute
path and run its bootstrap script **from the user's project directory**:

```bash
bash "/absolute/path/to/datalens-sdk/scripts/bootstrap.sh"
```

The script resolves a uv- or Poetry-managed project before considering `./.venv`, because those
tools commonly own a same-named environment. It creates `./.venv` only for an unmanaged project.
It verifies that every selected `bin/python` identifies itself as belonging to that environment,
so a stale symlink can never install into system Python. It may contact the configured Python
package index and install `datalens-sdk` into the selected environment.

The script deliberately does not encode an SDK version or a Python compatibility range. Plain
environments query through the selected interpreter's pip configuration; uv and Poetry projects
resolve through their native project sources. Candidate selection intersects the SDK metadata with
`PROJECT_REQUIRES_PYTHON` and a numeric `.python-version` pin when present. Compatibility and
freshness checks never upgrade pip or install the SDK or its dependencies. If a candidate can
create a venv, bootstrap uses a disposable venv seeded by that exact interpreter for fresh-project
probes and carries its pip source policy into the probe. Verified project environments are queried
directly.

Parse the `KEY=VALUE` lines after the `---BOOTSTRAP---` marker:

- `STATUS=ready` — use the absolute interpreter from `PYTHON` for every subsequent Python call.
- `STATUS=decision_required` — do not load the package skill or perform SDK work yet:
  - `REASON=sdk_install_required` — a uv/Poetry project needs `datalens-sdk` installed through its
    manager. The dependency may already be declared but missing from an unsynced environment, or
    it may need to be added. This also covers an importable SDK that the manager's synchronization
    would remove or replace. Explain that the manager will select the exact version from the
    project's sources, lock, and Python constraints; reconciliation can upgrade or downgrade the
    currently importable SDK. The project manifest and lock may change when a dependency must be
    added, and uv may update a stale lock to match the manifest during reconciliation. A Poetry
    install can also install other missing locked dependencies but does not remove untracked
    packages; a uv sync is exact and can remove unmanaged packages. No `SDK_VERSION` or
    `AVAILABLE_SDK_VERSION` is expected before this consent. If they approve, run the exact command
    below, then parse its result again:

    ```bash
    bash "/absolute/path/to/datalens-sdk/scripts/bootstrap.sh" --install-sdk
    ```

    Never substitute `pip install` inside a managed project.
  - `REASON=sdk_update_available` — tell the user the installed `SDK_VERSION` and newer compatible
    `AVAILABLE_SDK_VERSION`, give a clickable `CHANGELOG_URL`, and explicitly ask whether to keep
    the installed version or upgrade. Match the user's language. If they keep it, continue with the
    reported `PYTHON`. If they upgrade, run the exact command below with the reported available
    version, then parse its bootstrap result again:

    ```bash
    bash "/absolute/path/to/datalens-sdk/scripts/bootstrap.sh" \
      --upgrade-sdk "$AVAILABLE_SDK_VERSION"
    ```

    If that run reports a different available version, ask again; consent to one version is not
    consent to another. Never substitute a direct pip command.
  - `REASON=sdk_upgrade_target_unavailable` — the approved version is no longer the compatible
    release offered by the index, and bootstrap will not downgrade or guess. Ask whether to keep
    the installed version or retry the original check later.
  - `REASON=sdk_version_check_failed` with `SDK=installed` — explain that the installed SDK works
    but its freshness or manager ownership could not be verified. Ask whether to continue with the
    reported `SDK_VERSION` or retry the original bootstrap command. Do not silently continue or
    describe it as current. This reason never applies to `SDK=missing`.
  - `REASON=sdk_upgrade_failed` with `SDK=installed` — explain that the upgrade failed but the
    reported `SDK_VERSION` remains usable. Ask whether to continue with it or stop; retry the exact
    upgrade command only if the user requests it.
- `STATUS=blocked` — relay `REASON` and the relevant non-secret fields. Do not improvise another
  install command. When `AVAILABLE_PYTHON` is present, an existing incompatible `./.venv` was
  preserved and the user must decide how to handle it. For `venv_invalid`, do not use or repair the
  interpreter path automatically. For `managed_environment_unavailable` or
  `managed_environment_invalid`, preserve the uv/Poetry project and ask the user to repair or
  select its managed environment; never create a parallel `.venv`. For
  `managed_python_incompatible`, ask the user to change the manager-selected Python rather than
  installing into a different environment. For `configured_python_unavailable`, ask the user to
  install or change the numeric versions in `CONFIGURED_PYTHON`; for
  `configured_python_incompatible`, explain that the configured interpreter does not satisfy the
  intersection of `PROJECT_REQUIRES_PYTHON` and `REQUIRES_PYTHON`. For
  `project_python_constraint_invalid` or `project_metadata_unreadable`, ask the user to repair
  `pyproject.toml`. For `sdk_install_failed`, report that the managed environment was preserved and
  ask whether to retry or inspect the manager error outside the bootstrap protocol.

For any unrecognized `decision_required` reason, stop and show the parsed fields instead of
guessing. A decision applies only to this session; do not write an opt-out marker.

If the marker or `STATUS` is absent, stop and show the raw output. Do not infer success from the
process exit code. In particular, do not treat pip's generic "No matching distribution" message as
proof that the package does not exist, do not upgrade the project's pip merely to improve the
diagnostic, and never install into system Python.

Once bootstrap reports `ready`, or the user explicitly chooses a working installed version after
`decision_required`, run this with the exact reported `PYTHON`:

```bash
"$PYTHON" -c "
import datalens_sdk
for p in datalens_sdk.agent_skill_paths():
    print(p)
"
```

It prints one absolute path per line: the base instructions first, then any **installation
overlays** available in this environment. Extra lines are normal — they are additional detail for
particular DataLens installations, and not all of them necessarily apply here.

**Keep those absolute paths.** Each directory carries its own bundled scripts, examples, and
`references/` tree, referenced relative to it, and expects to be invoked by absolute path. Never
`cd` into one; the user's project directory stays the working directory throughout.

Read `SKILL.md` from the **first** path now and **follow it as if written here** — it is
authoritative and overrides anything you believe about this SDK, including anything in this file.
It owns installation detection: it decides which of the remaining paths apply and tells you when to
read them, so do not read an overlay before it says so. Where an overlay contradicts the base, the
overlay wins. Read the references they route you to on demand, not all of them.

Do not write SDK code, install anything, answer an SDK question, or commit to an approach before
you have read it. A plausible guess at this API is worse than one extra command.

Anything that writes files writes to the user's project directory or a temp dir; the package
directory may be read-only or root-owned.

## Scope

| Task | Where it belongs |
|------|------------------|
| Anything driving DataLens entities from Python | here — load the package instructions above |
| Standalone HTML pages and reports rendered by DataLens | `datalens-html-pages` |
| Publishing or managing an HTML page through the Python SDK | here, through the operations the package instructions document; if there are none, report that and offer an SDK upgrade or MCP/HTTP. Load `datalens-html-pages` for the publication procedure and the final link |
| The DataLens web UI, screenshots, embedding, metric interpretation | neither — say it is out of scope and stop |
