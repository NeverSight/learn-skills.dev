---
name: package-plugin
description: Build the upload archive for a plugin payload in this distribution repository. Use when asked to package the plugin, produce the submission zip, cut a plugin release artifact, or prepare a Codex/OpenAI Plugin Portal upload. Covers host selection, the pre-flight gates, and what to do after the archive exists.
---

# Package a plugin payload

## The archive is host-specific, not portable

There is one archive per host, built from one `plugins/<host>/<plugin>/`
payload. Never treat a built archive as a generic "OpenDesign plugin zip" and
never hand a Codex archive to another host. The payload's own contents are
host conventions:

| Payload member | Why it is host-specific |
| --- | --- |
| `.codex-plugin/plugin.json` | The manifest directory name is Codex's convention. Another host reads a different directory. |
| `open-design.package.json` | Declares `schemaVersion: "open-design-codex-cloud-package/v3"` and `minimumCodexCliVersion`. |
| `skills/<skill>/agents/openai.yaml` | Per-skill interface metadata keyed by host. A different host reads a different filename in `agents/`. |

The repository layout encodes the same rule: `plugins/<host>/<plugin-name>/`,
described under "Host directory convention" in `AGENTS.md`. Codex is the only
validated host in this revision.

The host-neutral parts — `README.md`, `SKILL.md`, `assets/` — are shared
*content*, not a shared *package*. They only become installable once wrapped
in one host's manifest.

## Build it

```bash
node scripts/package-plugin.mjs
```

`--host` defaults to `codex`, the only host with packaging rules. Useful flags:

- `--host <name>` — pick a different host payload.
- `--plugin <name>` — required only when `plugins/<host>/` holds more than one plugin.
- `--out-dir <path>` — archive destination; defaults to `.tmp/plugin-upload` (gitignored).
- `--skip-gates` — skip the validator and package tests. Use only for a throwaway inspection build, never for one you intend to upload.
- `--json` — machine-readable result, including the archive `sha256`.

The archive lands at `.tmp/plugin-upload/<plugin>-plugin-<version>.zip` for
Codex. That filename has no host token because 0.5.2 was submitted to the
Portal under it and submission records should stay continuous; every host
added later gets `<plugin>-<host>-plugin-<version>.zip` instead.

## What the script refuses to do

Each of these is a real failure mode that would otherwise ship a broken or
mislabelled archive, so treat a rejection as a bug in the payload, not as an
obstacle to work around:

- **Unknown host.** A host with no entry in the script's `HOSTS` table is rejected rather than packaged with guessed conventions.
- **Foreign interface file.** A Codex payload carrying `agents/claude.yaml` (or any non-`openai.yaml` interface) is rejected — that is exactly the cross-host leak this split exists to prevent.
- **Wrong package contract.** A payload whose `*.package.json` declares another host's `schemaVersion`.
- **Stale provenance.** `release-manifest.json` `plugin.contentListSha256`, `plugin.version`, or `plugin.path` disagreeing with the payload on disk. This is the common one: someone edited the payload and forgot to regenerate the digest. The error prints the regeneration command.
- **OS junk or symlinks.** `.DS_Store`, `__MACOSX/`, `Thumbs.db`, `desktop.ini`, or any symlink inside the payload.

Unless `--skip-gates` is passed, it also runs `scripts/validate-distribution.mjs`
and `tests/distribution-contract.test.mjs` first, and reports their results.

## Reproducibility

The same reviewed tree always produces the same archive bytes. Entries are
emitted in a fixed C-collation order, `zip -X` drops platform extra fields, and
staged mtimes are normalized to `release-manifest.json`'s `generatedAt` with
`TZ=UTC`. Two consecutive runs must yield the same `sha256`; if they do not,
something is writing into the payload between runs — find it before uploading.

Record the printed `archive sha256` alongside the submission so the uploaded
bytes can be re-derived later.

## Adding a new host

Do not package a host by loosening a check. Add its entry to `HOSTS` in
`scripts/package-plugin.mjs` with all of:

- `manifestPath` — where that host reads the plugin manifest.
- `packageContractSchema` — the `schemaVersion` its package contract must declare.
- `agentInterfaceFile` — the filename it reads inside each skill's `agents/`.

Then create the validated payload at `plugins/<host>/<plugin>/`, extend
`scripts/validate-distribution.mjs` and `tests/distribution-contract.test.mjs`
to cover it, and only then build. `AGENTS.md` requires a validated
host-specific package before a host directory is added at all.

## After the archive exists

The archive is a Portal upload artifact only. It is **not** the normal user
installation route — users install through the Git marketplace
(`codex plugin marketplace add nexu-io/open-design-agent-plugins`), which reads
`plugins/codex/open-design/` from `main` directly and never touches this zip.

The reverse substitution fails too: a GitHub source download ("Download ZIP",
or a repository/PR archive) is not an upload artifact. It nests the manifest
under `<archive>/plugins/<host>/<plugin>/`, and the Portal requires it at the
archive root. If someone reports "Plugin manifest not found", check which file
they uploaded before looking at the payload.

Before submitting, confirm the reviewer-facing records match the version you
just built: `docs/SUBMISSION_TEST_CASES.md`, and the `validation` block in
`release-manifest.json` (entries marked `not-rerun-for-<version>` still refer to
an older candidate and must be re-run against the Portal's own validators).
