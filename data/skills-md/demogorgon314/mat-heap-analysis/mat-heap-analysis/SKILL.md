---
name: mat-heap-analysis
description: Use when the user wants to inspect a Java heap dump with Eclipse MAT through a local CLI, including leak suspects reports, overview reports, OQL queries, histogram analysis, path-to-gc-roots checks, and index inspection.
---

# MAT Heap Analysis

## Overview

Use the bundled launcher that lives next to this skill to analyze `.hprof` and other MAT-supported heap dumps without depending on a separate checked-out repo.

Resolve every `scripts/...` and `references/...` path relative to the directory that contains this `SKILL.md`. Do not assume the current working directory is the skill directory.

Let `skill_dir` be the directory containing this `SKILL.md`. Prefer the self-locating wrapper at `"$skill_dir/scripts/mat"`. If that wrapper cannot be executed directly, fall back to `node "$skill_dir/scripts/mat.cjs"`.

Start with `doctor` if MAT or Java may be misconfigured. Prefer `triage` for first-pass analysis, then use `inspect-object`, `compare`, `run`, and `query` for follow-up analysis.

## Runtime Defaults

- Resolve the launcher from this skill's directory instead of the user repo's current working directory.
- Prefer `"$skill_dir/scripts/mat"` as the entrypoint.
- Fall back to `node "$skill_dir/scripts/mat.cjs"` only if the shell wrapper cannot be executed directly.
- On macOS, `doctor` auto-detects MAT at `/Applications/MemoryAnalyzer.app/Contents/Eclipse` when installed there.
- When `--heap` is present and no allowlist is configured, the CLI automatically trusts the heap's parent directory.
- When MAT cannot write near the source heap, the CLI stages the heap into a writable workspace before running reports and queries.
- High-level analysis commands use isolated workspaces so their intermediate MAT artifacts do not clobber each other.
- Add `--allowed-root` only when the workflow spans multiple directories, such as `compare` or heaps outside the main heap directory.

## Quick Start

Use the bundled launcher resolved from this skill's directory:

`"$skill_dir/scripts/mat"`

Common first commands:

```bash
"$skill_dir/scripts/mat" doctor
"$skill_dir/scripts/mat" triage --heap ./heap.hprof
"$skill_dir/scripts/mat" inspect-object --heap ./heap.hprof --object-id 0xc2300098
"$skill_dir/scripts/mat" compare --heap ./new.hprof --baseline ../baseline/old.hprof --allowed-root ../baseline
"$skill_dir/scripts/mat" show-artifact ./heap_Leak_Suspects.zip
```

## Workflow

1. Derive `skill_dir` from the current `SKILL.md` path and call `"$skill_dir/scripts/mat"` instead of `node scripts/mat.cjs` from the user repo.
2. Run `"$skill_dir/scripts/mat" doctor` if MAT launcher or Java is unknown.
3. Run `"$skill_dir/scripts/mat" catalog --json` or `"$skill_dir/scripts/mat" <command> --help` for capability discovery.
4. For a new heap, prefer `"$skill_dir/scripts/mat" triage --heap ...`.
5. For focused analysis, use:
   - `"$skill_dir/scripts/mat" inspect-object --heap ... --object-id 0x...`
   - `"$skill_dir/scripts/mat" compare --heap ... --baseline ...`
   - `"$skill_dir/scripts/mat" run histogram`
   - `"$skill_dir/scripts/mat" run path2gc --args 0x...`
   - `"$skill_dir/scripts/mat" query --query 'SELECT ...'`
6. Use `"$skill_dir/scripts/mat" show-artifact ...` instead of raw `unzip -p` when you need to inspect MAT HTML or zip output.
7. Prefer `--json` when a later step will parse the result.
8. On failure, use the returned `Hint`, `stderr`, and exit code rather than guessing.

## Installation Expectations

- The skill bundles a ready-to-run Node launcher in `assets/runtime/mat.cjs`.
- Use the sibling launcher in this skill directory, preferably `scripts/mat`.
- Use `scripts/mat.cjs` only as a direct Node fallback when the wrapper cannot be executed.
- The only external prerequisites are `node`, Java, and an Eclipse MAT installation.
- Prefer defaults for single-heap local analysis.
- Configure MAT with `--mat-home` or `MAT_HOME` only when MAT is not installed in the default location.
- Configure `--allowed-root` or `MAT_ALLOWED_ROOTS` only when the analysis spans additional directories.

## References

Read `references/commands.md` for command examples, compare-mode usage, and common recovery patterns.
