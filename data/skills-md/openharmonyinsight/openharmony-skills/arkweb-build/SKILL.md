---
name: arkweb-build
description: This skill should be used when the user asks to "编译 ArkWeb", "build ArkWeb", "执行 ArkWeb 编译", "验证 ArkWeb 构建", "排查 ArkWeb build.log", "分析 ArkWeb 编译失败", or mentions build_arkweb.sh, src/out/<product>/build.log, ArkWeb native or browser build targets, or incremental ArkWeb build verification. Handles command selection, incremental build execution, success verification, and build.log-first failure diagnosis for ArkWeb projects.
version: 0.1.3
author: ringking0
---

# ArkWeb Build Skill

This skill supports building ArkWeb projects through `build_arkweb.sh`, verifying the result, and diagnosing failures from `src/out/<product>/build.log`.

Requires a Linux build host with GNU coreutils and `/proc` available.

## When to use this skill

Use it when the user wants to:

- run an ArkWeb build
- choose the right ArkWeb build target
- verify whether a build actually succeeded
- diagnose a failed ArkWeb build from logs
- continue an incremental ArkWeb build without cleaning the tree

## Project root rules

ArkWeb wrapper roots usually look like `arkweb_*` directories in the current workspace and contain:

- `build_arkweb.sh`
- `src/arkweb/build/build.sh`

Build commands must run from the wrapper root, not from `src/`.

Use this helper to find the root from anywhere inside the tree:

```bash
find_arkweb_root() {
  local dir="${1:-$PWD}"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/build_arkweb.sh" && -f "$dir/src/arkweb/build/build.sh" ]]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  echo "ArkWeb root not found" >&2
  return 1
}
```

For git status and diff, use the real worktree under `src/`:

```bash
git -C "$(find_arkweb_root)/src" status --short
```

Note: `src` and `src/arkweb` are different git repositories. The `arkweb` repo lives under `src/`, but change diagnosis must inspect the two repos separately.

## Configuration precedence

If the caller already provides workflow or build configuration, do not replace it with defaults:

- `context.automation.buildCommands`
- `context.automation.verifyCommands`
- `context.automation.buildTarget`
- `context.automation.buildOutputDir`
- `context.automation.buildTimeoutMinutes`

Only fall back to the default commands below when that configuration is incomplete.

## Default build behavior

Default to incremental builds. Do not clean the tree unless the user explicitly asks for a clean build.

Never do these automatically:

- `git clean`
- `git reset --hard`
- `rm -rf src/out`
- `gn clean`
- `ninja -t clean`
- re-syncing dependencies just to "get a clean environment"

Before starting a build, always check whether the current product has been built before. Use the presence of `src/out/<product>/build.log` as the primary signal:

```bash
if [[ -f <arkweb-root>/src/out/rk3568_64/build.log ]]; then
  echo "Incremental build path"
else
  echo "First build path"
fi
```

If `build.log` does not exist yet, treat it as a first build unless the caller provides stronger evidence otherwise. The first build is usually much slower and should be called out explicitly before running it:

- expected duration: about 2 to 3 hours
- do not mislabel this as a normal incremental build
- avoid prematurely judging the build as hung just because it stays in setup or prebuild stages for a long time

Primary default command:

```bash
cd <arkweb-root>
./build_arkweb.sh rk3568_64 -t w -A
```

The most common variations are listed in [references/build-commands.md](references/build-commands.md).

## Repair responsibility and change boundaries

When the build fails, do not stop at extracting and reporting the error. The default expectation is to continue through root-cause analysis, make an allowed fix, and rerun the build to verify the result.

Allowed fixes:

- modify source files, `BUILD.gn` / `.gni`, ArkWeb-owned build scripts, or project configuration inside the current ArkWeb tree
- restore missing Git LFS assets for the current project, or rerun build commands inside the current project
- adjust the build target, resume strategy, or parallelism, then verify with another build

Explicitly forbidden changes:

- do not modify toolchains, SDK archives, install scripts, or other prebuilt payloads under `<arkweb-root>/src/ohos_sdk/`
- do not modify server files outside the current ArkWeb project directory, including other checkouts, global environment files, system directories, or unrelated files under the user home directory

If the problem can only be bypassed by touching one of those forbidden areas, call that out explicitly as a constraint and switch to an in-project alternative such as:

- rechecking and restoring the current project's Git LFS assets
- fixing dependencies, target wiring, or source errors inside the current project
- lowering parallelism and rerunning the build

## Change-first diagnosis

To localize build failures faster, inspect what the developer changed before widening the search. Most build failures are introduced by the current patch, so starting from `git` usually gives a faster and more accurate path to a minimal fix.

ArkWeb trees often come with default dirty files that should not be treated as developer edits. Start with the bundled filter script:

- `bash <skill-dir>/scripts/show_relevant_changes.sh <arkweb-root>`

Filter rules built into the bundled script:

- ignore the whole `third_party/rust-toolchain/` directory by prefix
- ignore the whole `third_party/rust/chromium_crates_io/` directory by prefix
- in the `src` repo, also ignore these exact default-noise entries:
  `third_party/ohos_ndk/includes/ohos_adapter/screenlock_manager_adapter.h`,
  `third_party/ohos_nweb_hap/hvigor/`,
  `third_party/ohos_nweb_hap/signature/`
- in the `src/arkweb` repo, also ignore this exact default-noise entry:
  `build/search_engines/prepopulated_engines.json`

If more raw git detail is still needed, check these next:

- `git -C <arkweb-root>/src status --short`
- `git -C <arkweb-root>/src diff --stat`
- `git -C <arkweb-root>/src diff --cached --stat`
- `git -C <arkweb-root>/src/arkweb status --short`
- `git -C <arkweb-root>/src/arkweb diff --stat`
- `git -C <arkweb-root>/src/arkweb diff --cached --stat`
- if `build.log` already points to a file, target, or symbol, inspect the matching path with `git diff`

Diagnosis rules:

- correlate the failing file, target, or missing symbol in the log with the current developer changes first
- filter out default dirty entries before deciding which changes are truly relevant to the failure
- if the current patch already explains the failure, do not broaden the search to unrelated directories or targets
- aim for a minimal fix, usually near the changed code or dependency declaration that introduced the failure
- only expand into broader project-level investigation when the current `git` changes do not explain the problem

## Failure stage classification

Before choosing a rerun strategy, classify the failure stage from `build.log`:

- `pre-gn/sdk-lfs`: SDK install, archive extraction, Git LFS pointer, missing package, `gzip`/`tar`/`unzip` errors before GN or Ninja. Fix assets or setup, then rerun the configured build command.
- `gn-generation`: `ERROR at //...`, `Unable to load`, bad `BUILD.gn` or `.gni` evaluation. Fix GN configuration, then rerun GN or the configured build command.
- `ninja-graph-or-target`: `ninja: error: unknown target`, missing `build.ninja`, or Ninja graph loading errors. Fix target selection or generated build graph, then rerun the configured target set.
- `ninja-compile-link`: compiler or linker failures after Ninja starts, such as `FAILED:`, `fatal error:`, `undefined reference`, `multiple definition`, `ld.lld: error`, or `clang++: error`.
- `resource-or-terminated`: explicit `killed` or `OutOfMemory`.
- `resource-or-terminated-suspected`: log tail still looks like Ninja progress, with no `FAILED:`, GN error, or Ninja target error. Treat this as a resource-pressure suspicion and inspect the latest snapshot before changing code.

Single-command quick verification is only for `ninja-compile-link`. After fixing that root cause, first `cd <arkweb-root>/src/out/<product>` and rerun the failed compiler or linker command shown after the first `FAILED:` line when it is available in `build.log`. The command is emitted relative to the Ninja output directory, so running it from the wrapper root or `src/` can fail incorrectly. If that command succeeds, switch back to the correct directory before broader verification: use `<arkweb-root>` for the full `build_arkweb.sh` command, or `<arkweb-root>/src` only when deliberately rerunning the same direct Ninja target set. Before that broader verification, still record a resource snapshot with `scripts/capture_resource_snapshot.sh`. Do not use single-command verification for `pre-gn/sdk-lfs`, `gn-generation`, or `ninja-graph-or-target`.

## Execution rules

1. Resolve the wrapper root and execute from there.
2. Prefer workflow-provided commands when present.
3. Run the build in the foreground and wait for the real exit code.
4. Use a long timeout. Default maximum wait: 4 hours.
5. Treat exit code `0` as success. Any non-zero exit, signal termination, or timeout is a failure.
6. On failure, inspect `src/out/<product>/build.log`, then immediately correlate it with recent developer changes from `bash <skill-dir>/scripts/show_relevant_changes.sh <arkweb-root>` so default dirty entries are filtered out first.
7. Before running the build, check whether `src/out/<product>/build.log` exists and tell the caller if this is likely a first build.
8. Record a resource snapshot for the Ninja phase. For `build_arkweb.sh`, capture it immediately before launching the build as the external baseline. For direct Ninja continuation, capture it immediately before the `ninja` command.
9. If the build stops without a compiler or linker error and the process is simply gone, suspect CPU or memory pressure first. Check the latest resource snapshot before drawing other conclusions.
10. In that silent-stop case, suggest lowering parallelism proactively, typically to `-j 32`, and then to `-j 16` if pressure remains high.
11. If `src/out/<product>/args.gn` already exists and the user is clearly continuing the same incremental build, a direct `ninja -C out/<product> <targets>` rerun from `src/` is acceptable. Reuse the same target set as the previous build, not a random single target. Do not switch to direct Ninja just to hide a `build_arkweb.sh` failure.
12. After a build error, the default flow is to complete the full loop of diagnose -> fix -> rebuild -> reverify, not just emit an error summary.
13. For `ninja-compile-link` failures, use the failed command and working directory shown by `scripts/analyze_build_error.sh` as a fast local check after fixing the issue. After that succeeds, record a new resource snapshot, then `cd <arkweb-root>` before rerunning the full configured `build_arkweb.sh` command; use `<arkweb-root>/src` only for an intentional direct Ninja target-set rerun.
14. While fixing the issue, only modify files that are allowed inside the current ArkWeb project. Do not touch `src/ohos_sdk/` and do not modify server files outside the project directory.
15. To converge faster and more accurately, try to explain the failure from the current `git` changes first and keep the repair minimal instead of editing unrelated files.

## Logs and diagnostics

The primary log is:

```text
<arkweb-root>/src/out/<product>/build.log
```

Older logs are usually rotated to timestamped names when a new build starts.

Always inspect the log tail first:

```bash
tail -200 <arkweb-root>/src/out/<product>/build.log
```

If that is not enough, search for:

- `error:`
- `fatal error`
- `undefined reference`
- `multiple definition`
- `ERROR at`
- `No such file`
- `cannot find`
- `killed`
- `OutOfMemory`

Use the bundled scripts:

- `scripts/analyze_build_error.sh` for a structured summary, failure stage classification, first-error context, and failed Ninja command candidate. It accepts either `<product> <arkweb-root>` or `<build.log> <arkweb-root>`.
- `scripts/find_recent_errors.sh` for a quick recent-error scan
- `scripts/inspect_build_state.sh` to inspect available output directories and recent logs
- `scripts/check_lfs_artifacts.sh` to parse the relevant LFS attribute files, check required prebuilts, and detect missing files or LFS pointer files
- `scripts/capture_resource_snapshot.sh` to record CPU and memory headroom before the Ninja phase, so silent build exits can be diagnosed as likely resource pressure. Its first argument is the product name; the ArkWeb root is the third argument in the labeled form or the second argument in the short form.
- `scripts/show_relevant_changes.sh` to filter expected dirty files and show the relevant git changes separately for the `src` repo and the `src/arkweb` repo
  It uses `git status --short -uall`, prints ignored default dirty entries, and supports `--show-all` / `--no-ignore` when the full raw view is needed.

In commands below, `<skill-dir>` means the directory containing this `SKILL.md`.

See:

- [references/build-commands.md](references/build-commands.md)
- [references/common-errors.md](references/common-errors.md)
- [references/log-locations.md](references/log-locations.md)
- [examples/example-workflow.md](examples/example-workflow.md)

## Output expectations

A good build answer should include:

- the exact command used
- the working directory
- the product and target
- the exit status
- the log path checked
- the failure type and location if it failed
- the minimal next fix or next command
