---
name: periphery-scan
description: Runs a Periphery scan for unused Swift code in a project where Periphery is already set up. Use when a user asks to run Periphery, scan for unused or dead Swift code, or find and remove unused code with Periphery. To install, sign in to or configure Periphery, use periphery-scan-setup instead.
---

# Periphery Scan

## Overview

Run `periphery scan` with the `agent-prompt` output format, which lists each result with removal guidance written for agents. Assume Periphery is installed and signed in, and that the project's `.periphery.yml` holds its options. Don't check any of that up front: scan straight away, and look into the setup only if the scan fails.

## Steps

### 1. Scan

From the project root, the directory that holds `.periphery.yml` (or `Package.swift`):

```sh
periphery scan --format agent-prompt > <output file>
```

In a Bazel project (`MODULE.bazel` or `WORKSPACE` at the root), run its `rules_periphery` scan target instead, usually `//:scan_auto`: `bazel run //:scan_auto -- --format agent-prompt > <output file>`.

- Save the output to a file outside the project, such as in a temporary directory, so you can read it without scanning again.
- Scanning builds the project, which can take many minutes. Tell the user, and run it with a long timeout or in the background.
- Don't add other options unless the user asked for them. The config file holds the project's choices, and options passed on the command line override them.

### 2. Report, then remove if asked

A non-zero exit with results in the output file isn't a failure: `strict: true` in `.periphery.yml` makes the scan exit non-zero when it finds anything, printing `Found N issues.`

If the output starts `No unused code detected.`, tell the user. If it also has a "Trial Mode" notice, the trial hid every result: tell the user how many issues are hidden. Either way, stop there.

Otherwise, the output is a removal task: results, a `## Summary` section and removal guidance. Give the user a brief summary first:
- the number of results, broken down by kind. Each result starts with its kind in brackets, either as a numbered step or as an entry in a "Remove together" or "Change together" step. Lines under a result that don't start with a kind are details of it, not separate results. Count them, rather than tallying by eye: `grep -oE '^([0-9]+\. |   - )\[[^]]+\]' <output file> | sed -E 's/^([0-9]+\. |   - )//' | sort | uniq -c`
- the removable unused code estimate from `## Summary`, quoted. A trial gets two lines, for the trial results and the full results; quote both.
- if there's a "Trial Mode" notice: what share of the files the results cover, and how many issues are hidden

Then:
- If the user asked only to scan or find unused code, offer to remove the results. Don't start until they agree.
- If they asked to remove unused code, carry on.

Before removing, suggest a clean working tree or a new branch, since removal touches many files. Then follow the removal task and guidance in the output. If removing code leaves a file empty, delete the file and remove its references from the Xcode project, or the build fails. When you're done, tell the user what you removed and offer to scan again: removing code can leave other code unused.

### 3. If the scan fails

Tell the user what failed, quoting the key error line. Then:

| Error | Cause | Fix |
|---|---|---|
| `periphery: command not found`, or `--format` doesn't accept `agent-prompt` | Not installed, or an outdated or open-source release | Hand over to periphery-scan-setup |
| `No account credential found` | Not signed in | Signing in opens a browser, so ask the user to run it themselves, then scan again: `! periphery auth login` in Claude Code, or for Bazel `! bazel run @periphery_bin//:periphery -- auth login`. Never ask for an access token's value. |
| `Failed to identify project`, or a project, scheme or target that can't be found | No `.periphery.yml`, or it's out of date | Hand over to periphery-scan-setup |
| No `rules_periphery` scan target (Bazel) | Not set up | Hand over to periphery-scan-setup |
| Anything else | | Read https://periphery.pro/docs/troubleshooting. Propose any change to the project, build settings or `.periphery.yml`, and wait for the user to confirm it. |

To hand over, tell the user what's missing and use the periphery-scan-setup skill. If it isn't installed, they can add it with `npx skills add periphery-pro/skills --skill periphery-scan-setup`, or set up Periphery by following https://periphery.pro/docs/running-a-scan.

If you can't resolve it, offer to open an issue at https://github.com/periphery-pro/issues, following periphery-scan-setup's failure step. The tracker is public, so the issue must be anonymous: replace every project, scheme, target, module, file, type, user, path and company name with placeholders, include no source code, and post only after the user approves the full text.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Checking the install, sign-in or config before scanning | Scan first; investigate only on failure |
| Writing or editing `.periphery.yml` to get a scan working | Hand over to periphery-scan-setup |
| Adding `--schemes`, `--retain-public` or other options on the command line | Let the config file supply them |
| Removing code when the user only asked for a scan | Summarize, then offer removal |
| Revalidating each result before removing it | The output says to treat results as authoritative; follow it |
