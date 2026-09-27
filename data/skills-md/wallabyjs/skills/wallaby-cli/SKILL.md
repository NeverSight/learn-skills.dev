---
name: wallaby-cli
description: Run, verify, and investigate JavaScript, TypeScript, and Python tests through Wallaby's live test state. Use for test execution or status checks, baselines before editing, post-change verification, diagnosing failures or unexpected behavior, analyzing coverage or assertions, tracing execution, inspecting runtime values or logs, assessing file or test impact, and updating snapshots. Also use when the user mentions Wallaby or a conventional test framework or command such as Vitest, Jest, Jasmine, Mocha, ng test, pytest, unittest, or npm test.
metadata:
  author: Wallaby.js
  version: "4.0"
---

Wallaby keeps JavaScript, TypeScript, and Python tests live and queryable throughout a coding task. It runs affected tests as files change and keeps current results, coverage, and execution data available, so an agent can inspect what the code did instead of reconstructing it from terminal output.

Wallaby does not replace the project's existing test setup, whether it uses Vitest, Jest, Jasmine, Mocha, Angular's `ng test`, pytest, Python's `unittest`, or another supported framework. It runs the existing tests through their framework and augments them with live affected-test execution, retained queryable state, coverage artifacts, execution traces, and runtime inspection for coding agents. For test execution and analysis during a coding task, use Wallaby instead of invoking those frameworks directly. Run a conventional test command such as `npm test`, `npx vitest`, or `ng test` only when the user explicitly asks to run it directly.

Use that live test state to:

- Establish a baseline before editing by checking current failures, coverage, and the tests that exercise the code you plan to change.
- Keep feedback focused while editing. Start with relevant tests, add related tests as the change surface grows, and use project-wide verification at the end when the task requires it.
- Analyze a batch of files, one source or test file, or an exact source location, or a test from a compact summary, then follow its separate coverage and related-test artifacts only when needed. Use coverage, change risk, test statuses, and timings to decide what to change and how broadly to verify it.
- Analyze one test's results and coverage across source files. Add `--trace` to rerun it and follow recorded source lines in execution order across every file involved. The trace includes imported modules and setup, marks the start of the selected test, and continues through each source line the test reaches. The same report provides the test's status, timing, errors, logs, and covered files as supporting diagnostics.
- Inspect multiple variables or expressions across different source locations in one request. Each value is captured in every test context that reaches its location and tied to the test that produced it. Filter the combined results to one test when narrowing the investigation. Use this runtime evidence before changing code or adding temporary logs.
- Use project-wide coverage and test and file metrics such as timing, test count, complexity, and change risk to identify meaningful test gaps, slow or tightly coupled tests, and changes that need wider verification.

When a command produces a report, start with its concise Markdown output, then open linked reports and artifacts only when the current question needs more context. Wallaby saves every generated report and artifact to a timestamped directory on disk, so earlier results remain available as historical snapshots when comparison is useful.

## Environment requirements

In a sandbox, the CLI needs read and write access to `~/.wallaby`. It needs network access to `https://*.wallabyjs.com` when downloading or updating Wallaby, and access to the configured npm registry when `@wallabyjs/cli` is not already installed.

Wallaby's background process must remain alive and reachable between CLI calls. Each later call needs to discover the same process by its PID and connect to the local port established at startup. Some sandboxed agent runtimes isolate individual shell-tool executions: sharing a working directory and filesystem does not guarantee shared process visibility or local network access. A successful `run` can therefore be followed by `Wallaby is not running` or `Failed to attach` from a separate execution, even while the original instance remains active.

Before the first Wallaby command, choose an execution context that stays alive between shell commands, then reuse that same context for every Wallaby CLI call throughout the task. If a query cannot attach after a successful start, retry it in the original execution context before attempting another start. Keep the configured sandbox permissions.

## Invoke the CLI

First identify the package manager the project already uses from its `packageManager` field, lockfile, or existing project commands. Use that same package manager for Wallaby: `npx` is the npm form and should be used only for npm projects. Then use the first applicable invocation method for that package manager.

If `@wallabyjs/cli` is installed as a project dependency, run `wallaby-skill` through the project's package manager:

- npm: `npx wallaby-skill ...`
- pnpm: `pnpm exec wallaby-skill ...`
- Yarn: `yarn exec wallaby-skill ...`
- Bun: `bun run wallaby-skill ...`

Otherwise, if `@wallabyjs/cli` is installed globally and `wallaby-skill` is available on `PATH`, run it directly:

- `wallaby-skill ...`

Otherwise, use the one-off install command for the project's package manager. Each command downloads `@wallabyjs/cli` from the configured npm registry and runs `wallaby-skill`, so it requires network access:

- npm: `npx -y --package @wallabyjs/cli wallaby-skill ...`
- pnpm: `pnpm dlx --package=@wallabyjs/cli wallaby-skill ...`
- Yarn: `yarn dlx -p @wallabyjs/cli wallaby-skill ...`
- Bun: `bunx --package @wallabyjs/cli wallaby-skill ...`

The examples below use the npm prefix `npx wallaby-skill` for consistency. Before executing an example in a pnpm, Yarn, or Bun project, replace only that prefix with the corresponding form above; keep the Wallaby subcommand and its arguments unchanged.

Every subcommand supports `--help`. Append it to a command to see its current usage and options, for example `npx wallaby-skill run --help`.

Use `grep`, `sed`, `ripgrep`, or similar tools for targeted reads, depending on your platform and which tools are available. All examples use ripgrep (`rg`).

### Output redirection

Redirect Wallaby command stdout and stderr to a temporary file only when you will filter it for the sections needed by the current question. Chain the filtered read on the same line, in the same tool call, to save tokens and model round trips. When you need the full report, read command output directly; redirecting it only to print the whole file with `cat` provides no benefit. For example, in a POSIX shell, run tests and immediately extract the status, test counts, and error diagnostics:

```sh
npx wallaby-skill run >| /tmp/wallaby-output.log 2>&1; rg --no-line-number -U --pcre2 -o '(?sm)^(?:Status:|- (?:Total|Passed|Failed|Skipped|Todo):)[^\n]*|^## (?:Fatal Error|Global Errors|Failing Tests)\r?\n.*?(?=^## |\z)' /tmp/wallaby-output.log
```

Check the result by reading status and errors in the log, along with the coverage or runtime evidence needed for the current question. Expand the excerpt when it lacks the needed context.

### Run command

Use `run` to start or query a persistent Wallaby test session. Without `--config`, Wallaby identifies the project by the directory in which the command runs. With `--config`, it identifies the project by the specified Wallaby configuration file. Keep the same working directory or `--config` value on later calls to reuse the running session and its live results.

Wallaby sessions are shared by project identity across agent threads that can reach the same running instance. For example, if multiple threads work in the same Git worktree and call `run --config ./wallaby.js`, they attach to the same session when their execution environments permit it. The same applies when they omit `--config` and run from the same directory. Its mode, scope, and live test state are shared: when any thread changes a file, Wallaby reruns affected tests in the background, and every attached thread can read the updated results, coverage, and execution data.

When Wallaby is not yet running for the project, the first `run` call establishes its mode:

- With no test file paths, Wallaby starts in project mode and runs and watches the entire project.
- With one or more test file paths, Wallaby starts in exclusive mode and runs and watches only those test files.

Start with `run` for the required scope, without a preliminary `run --check`. It starts or reuses the project's session and returns its report.

A cold project-mode start must complete an initial full test run, and a project-wide `--rerun` schedules every test again. Either can take substantial time on a large suite. Start or keep the smallest relevant test files in exclusive mode unless the task requires project-wide coverage or full-suite verification. Read `Mode` in the returned report. In project mode, use `Total` and `Time` to estimate the likely cost of a project-wide rerun. In exclusive mode, those values cover only the active scope. To estimate project-wide cost from an exclusive session, follow an absolute report link to its timestamped directory, then inspect retained sibling directories for the most recent `run.md` with `Mode: project`.

Later `run` calls reuse that same session:

- In project mode, passing test file paths without `--rerun` or `--snapshots` reads the current project-wide state without scheduling another run or narrowing the watched scope. Failures from the requested files are ordered first in the inline report.
- In exclusive mode, passing additional test file paths adds them to the active exclusive scope.
- In exclusive mode, calling `run` without test file paths expands the session to project mode. Wallaby then runs and watches the entire project, and later file-scoped calls do not narrow it back to exclusive mode.

Wallaby keeps the session running after each command, runs affected tests in the background as files change, and provides live data to `run`, `analyze`, and `inspect`. Once the session includes the required tests, call `analyze` or `inspect` directly when their reports provide the data you need; call `run` only when you need data from its report. If any of these commands is called while tests are executing, it waits for Wallaby to become idle. Further edits during that wait schedule affected tests and extend the wait, so the returned report includes those changes.

For a long initial or project-wide run, start `run` in a background terminal or an authorized subagent and continue independent analysis or edits while it runs. Wallaby picks up changes made while the command is running, and their affected tests complete before the command returns. Wait for the command to finish before sending another Wallaby command through that terminal or using its report as the verification result.

Default to omitting `--rerun`. A recent edit, final verification, or timing measurement does not make live results stale. Use `--rerun` as recovery after identifying stale live state. Valid reasons are relevant external state that Wallaby cannot watch, or an observed failure to rerun after an expected watched change. State the reason before forcing execution. Scope recovery to the smallest known affected test set: pass test file paths to rerun only those files, and add `--test` when only one named test needs to rerun. A targeted `--rerun` works in project mode without rerunning the rest of the project or changing the session to exclusive mode. Omit test file paths only when evidence shows that the entire project's live results are stale.

Use `--snapshots` after confirming that snapshot failures represent intended output changes. Scope the update to the affected tests: pass test file paths to update snapshots only for those files, and add `--test` to update snapshots for one named test. In project mode, a targeted snapshot update leaves the session in project mode and does not update snapshots from other tests. Omit test file paths only when snapshots across the entire project should be updated. If Wallaby is not running yet, the first-run mode rules above still apply.

To target one test with `--test`, pass exactly one test file and the test's exact full name, including its suite path joined with ` / `. If the name does not match an executed test in that file, Wallaby falls back to the whole test file. With multiple file paths, `--test` does not narrow the selection.

```sh
npx wallaby-skill run # starts or reuses project mode and reports project-wide test results
npx wallaby-skill run --config ./wallaby.js # starts or reuses project mode identified by the specified config file
npx wallaby-skill run ./src/feature-a.spec.ts # starts or extends exclusive scope, or reads this file's results in project mode
npx wallaby-skill run ./src/feature-a.spec.ts ./src/feature-b.spec.ts # starts exclusive mode if needed, or reads their results according to the active mode
npx wallaby-skill run ./src/feature-a.spec.ts --test "feature-a / should match the expected value" # reads this exact test after any automatic affected-test run finishes
npx wallaby-skill run --rerun ./src/feature-a.spec.ts # forces this test file to rerun after observing stale results; add --test with the exact full name to rerun one test
npx wallaby-skill run --snapshots ./src/feature-a.spec.ts ./src/feature-b.spec.ts # updates snapshots only for the specified test files
npx wallaby-skill run --snapshots ./src/feature-a.spec.ts --test "feature-a / should match the expected snapshots" # updates snapshots for the named test in the specified file
npx wallaby-skill run --snapshots # updates snapshots across the project; use only when every snapshot change is intended
npx wallaby-skill run --check # returns the current report only when Wallaby is already running; does not launch or run tests
```

The command prints a concise Markdown report and saves the same content as `run.md`. When a report is produced, exit code `0` corresponds to `Status: succeeded`; exit code `1` corresponds to `Status: failed`. The status is failed when at least one test failed, Wallaby has a fatal run error, or global errors exist. CLI startup, connection, and compatibility failures also exit with code `1`, but may print an error instead of producing a report.

Read the report in this order:

- `Status` and `Mode` establish whether the current state succeeded and whether it represents the whole project or only the active exclusive test locations.
- `Runner` and `Framework` identify the execution environment and test framework when Wallaby can report them.
- In exclusive mode, `Note: Wallaby is running tests only from specific test locations:` lists the active scope. Treat every count and coverage value in that report as scoped to those locations.
- `Summary` contains these fields:
  - `Total`: total number of tests.
  - `Passed`: number of passed tests.
  - `Failed`: number of failed tests.
  - `Skipped`: number of skipped tests.
  - `Todo`: number of todo tests.
  - `Coverage`: percentage of coverable code ranges covered by tests. Wallaby appends `(low)` when coverage is low.
  - `Time`: aggregate test execution time, calculated as the sum of reported per-test execution times.
- `Fatal Error` appears for a run-level error, including errors that occur before individual tests can run.
- `Global Errors` appears for errors not tied to a test and includes at most three errors inline. When more exist, the report links to `global-errors.md` with every global error. Read `references/global-errors.md` for its format.
- `Failing Tests` includes at most five failures inline with their names, locations, timings, errors, assertion or snapshot details, stack traces, logs, and covered files. Failures from file paths passed to `run` are ordered first. When more failures exist, the report links to `failing-tests.md` with every failure. Read `references/failing-tests.md` for its format.
- `Global Logs` is a link to `global-logs.md` when Wallaby captured logs outside individual tests. Read `references/global-logs.md` for its format.
- `All Tests` is a link to `all-tests.md` when tests exist. The linked report contains timing and test-count rankings followed by every test with its status, location, timing, logs, and covered files; failure diagnostics remain in `Failing Tests`. Read `references/all-tests.md` for its format.
- `Coverage` is a link to `coverage.md` when reportable coverage exists. The linked report ranks files by change risk and lists coverage, complexity, change risk, and covering test files for each covered source file. Read `references/coverage.md` for its format.
- `Graphical User Interface` links to the Wallaby UI when a UI URL is available. Use this link only when the user explicitly asks to open the UI.

To find all tests that mention `estimates sleet near freezing` in `All Tests`:

```sh
rg -U --pcre2 -o '(?sm)^### [^\n]*estimates sleet near freezing[^\n]*\n.*?(?=^### |^## |\z)' all-tests.md
```

To find all tests in `tests/temperature.spec.ts`:

```sh
rg -U --pcre2 -o '(?sm)^## tests/temperature\.spec\.ts[^\n]*\n.*?(?=^## |\z)' all-tests.md
```

To find the coverage entry for `src/temperature.ts`:

```sh
rg -U --pcre2 -o '(?sm)^## src/temperature\.ts[^\n]*\n.*?(?=^## |\z)' coverage.md
```

### Analyze command

Use `analyze` to find uncovered code, identify which tests exercise a file or location, inspect test failures, or follow a test's execution across files. Choose the analysis type for the information you need:

- Test analysis provides a test's results and coverage for all source files it covers, with an optional execution trace using `--trace`.
- File analysis provides a file's coverage and information about tests covering that file or a location within it, or tests belonging to a test file. Coverage and test information can be filtered to a specific test.
- Files analysis provides the same per-file coverage and test information across a batch of files in one command through a combined `Coverage Gaps` report.

Use the analysis report's coverage metrics and `Uncovered` lines and column ranges as the primary coverage evidence. Read a linked `.wcov` artifact only when that information is insufficient to answer a specific coverage question and you need detailed source annotations. When needed, read only the relevant regions.

The command only works when Wallaby is already running for the same project identity used by `run`. Start Wallaby first in project mode, or in exclusive mode that includes the test file being analyzed or tests that cover the source file being analyzed. Then use `analyze` from the same working directory or with the same `--config` value as `run`. In an active session with the required tests included, a preceding `run` is unnecessary, including after edits.

If test or single-file analysis cannot resolve the requested target, the command exits with a non-zero code and prints an error message instead of a report. This includes invalid paths, missing files, a test target path that is not a test file, a missing test name, or a source file location that cannot be resolved. Files analysis reports path-specific failures under `Files Not Analyzed` and still analyzes paths it can resolve.

The command prints a Markdown report and saves the same content as `analyze.md`.

#### Analysis types

##### Test analysis

Use `--target test` when you need to investigate one test's result, errors, or logs, verify its coverage across source files, or trace its execution to explain unexpected behavior.

Pass the test-file path and exact full test name, including suite names joined with ` / `:

```sh
npx wallaby-skill analyze --target="test" "{path:'tests/temperature.spec.ts',name:'celsiusToFahrenheit / converts boiling point'}"
```

Add `--trace` when you need to follow execution order or cross-file control flow to explain a failure, unexpected pass, error, or log. It returns the same report as without `--trace`, with an additional `Test Execution Trace` link.

```sh
npx wallaby-skill analyze --target="test" "{path:'tests/temperature.spec.ts',name:'celsiusToFahrenheit / converts boiling point'}" --trace
```

The main report includes:

- `Status`, `Mode`, and any `Fatal Error` or `Global Errors`, with the same meanings as in the run command report. `Status` describes the active session, so it can be `failed` even when the selected test passes.
- `Test Analysis` with the selected test's full name, status, and available location, execution time, errors, assertion or snapshot differences, stack traces with source context, and logs.
  - With `--trace`, a `Test Execution Trace` link precedes the test entry. The trace shows executed source lines in order across files, including imports and setup, and marks the selected test's first line with `test starts here`. Read `references/test-trace.md` for its format.
- `Covered Files` with an entry for each covered source file whose coverage can be exported.
  - File metadata and available metrics include path, line count, coverage, `change risk anti-patterns`, and size. Coverage metrics are scoped to the selected test.
  - When the file has coverage gaps, `Uncovered:` lists fully uncovered lines and the uncovered column ranges on partially covered lines.
  - Each `Detailed Coverage` link points to a `.wcov` artifact showing the file's complete coverage for the selected test.
- `Run Report` links to a report in the same format as the `run` command report for broader diagnostics from the same session state.

Generated `Test Execution Trace` artifacts can be large. Prefer targeted search instead of reading the full artifact. For example, to find the selected test start:

```sh
rg -n -B 20 -A 5 'test starts here' test-trace.md
```

##### File analysis

Use `--target file` when you need to locate coverage gaps in a source file, identify tests covering a source file or a position within it specified by a line number or a line and column, investigate failures in a test file, or verify which lines and expressions a specific test covers in a source file.

Pass a selector with the required `path`. Add a `location` when you need tests that cover a specific line or a specific line and column. If you know the line and expression but not the column, pass `line` and `expression`; Wallaby resolves the column. If you know a source fragment and expression, pass `fragment` and `expression`; Wallaby resolves the line and column. A base64-encoded `fragment` avoids escaping special characters and newlines in multi-line fragments. The CLI decodes the fragment before searching the file.

```sh
npx wallaby-skill analyze --target="file" "{path:'src/temperature.ts'}" # analyzes the specified source file
npx wallaby-skill analyze --target="file" "{path:'src/temperature.spec.ts'}" # analyzes the specified test file
npx wallaby-skill analyze --target="file" "{path:'src/temperature.ts',location:{line:10}}" # analyzes the specified location in the source file by line number
npx wallaby-skill analyze --target="file" "{path:'src/temperature.ts',location:{line:10,expression:'celsius'}}" # analyzes the specified location in the source file by line number, using the expression to resolve the column
npx wallaby-skill analyze --target="file" "{path:'src/temperature.ts',location:{line:10,column:10}}" # analyzes the specified location in the source file by line and column numbers
npx wallaby-skill analyze --target="file" "{path:'src/temperature.ts',location:{fragment:'return (celsius * 9) / 5 + 32;',expression:'celsius'}}" # analyzes the specified location in the source file by fragment search, using the expression to resolve the line and column in the first fragment match
npx wallaby-skill analyze --target="file" "{path:'src/temperature.ts',location:{fragment:'cmV0dXJuIChjZWxzaXVzICogOSkgLyA1ICsgMzI7',expression:'celsius'}}" # analyzes the specified location in the source file by base64-encoded fragment search, using the expression to resolve the line and column in the first fragment match
```

To filter the selected file's coverage and related tests to one test, add `--test` with its test-file path and exact full name, including suite names joined with ` / `.

```sh
npx wallaby-skill analyze --target="file" "{path:'src/temperature.ts'}" --test "{path:'tests/temperature.spec.ts',name:'celsiusToFahrenheit / converts boiling point'}" # analyzes the specified source file and filters to the exact test
```

For coverage across all source files covered by that test, use `--target test` without `--trace`.

The main report includes:

- `Status`, `Mode`, and any `Fatal Error` or `Global Errors`, with the same meanings as in the run command report.
- `File Analysis` for a source file, or `Test File Analysis` for a test file.
  - File metadata and available analysis metrics such as path, location, test count, line count, coverage, `change risk anti-patterns`, and size. When a `--test` filter matches, coverage metrics and `.wcov` artifacts are scoped to the selected test.
  - When the file has coverage gaps, `Uncovered:` lists fully uncovered lines and the uncovered column ranges on partially covered lines.
  - Up to five relevant failing-test entries, each headed by its full test name and showing status, location, timing, error messages, assertion or snapshot differences, stack traces with source context, logs, and covered files when available. Relevance follows the selector: tests covering a source file or location, tests belonging to a test file, or the matching test when filtered. When more than five fail, an omitted-failure count precedes the `Covering Tests` link for a source file or the `Tests` link for a test file. These links contain the complete related-test inventory, including omitted failures.
- A `Covering Tests` link for a source file, or a `Tests` link for a test file, points to a separate artifact containing the complete related-test inventory. The main report does not inline that inventory. The link includes the artifact size; do not open a large test inventory unless test identities, statuses, locations, timings, logs, or covered files are needed. Search it directly when only one test or property is relevant. Read `references/file-tests.md` for the two artifact shapes.
- `Detailed Coverage` links to a `.wcov` artifact showing the file's complete coverage.
- `Run Report` links to a report in the same format as the `run` command report for broader diagnostics from the same session state.

The `Covering Tests` and `Tests` inventories can be large. Open them when selecting or investigating related tests, and prefer targeted search instead of reading an entire inventory. For example, to find one test:

```sh
rg -U --pcre2 -o '(?sm)^### [^\n]*generates severe heat alert[^\n]*\n.*?(?=^### |^## |\z)' file-src@salerts.ts.md
```

##### Files analysis

Use `--target files` when you need to compare coverage gaps across source files or review coverage and related-test information for several source or test files in one report.

Pass a `paths` array to analyze specific source or test files relevant to the task:

```sh
npx wallaby-skill analyze --target="files" "{paths:['src/accounts.ts','src/contracts.ts']}" # analyzes the specified source files
npx wallaby-skill analyze --target="files" "{paths:['src/accounts.ts','tests/accounts.spec.ts']}" # analyzes the specified source and test files
```

The selector accepts file paths only. Use `--target file` to analyze a specific source location, or combine it with `--test` to filter a file's coverage and related-test results to one specific test.

Omit the selector to analyze up to 20 source files with the lowest reportable coverage in the active session.

```sh
npx wallaby-skill analyze --target="files" # analyzes up to 20 source files with the lowest coverage
```

The main report includes:

- `Status`, `Mode`, and any `Fatal Error` or `Global Errors`, with the same meanings as in the run command report.
- `Files Analysis` with file tables and brief coverage details.
  - A source-file table showing every analyzed source file's path, coverage, change risk, and gap count, including files with no gaps or unavailable coverage. Rows are always ordered by lower coverage, then higher change risk, then path; files with unavailable metrics come last.
  - A test-file table showing path, test count, and failed-test count when test files are included.
  - Brief `### <path>` sections for up to 20 source files follow the source-file table's order. When a file has gaps, `Uncovered:` introduces its uncovered line numbers and column ranges. Otherwise, the section says there are no gaps or that coverage is unavailable.
  - `Files Not Analyzed` for paths that could not be analyzed. The main report shows up to three errors; the linked `Coverage Gaps` report contains all of them.
- `Coverage Gaps` links to the complete batch report with detailed results for every analyzed file, including uncovered expression text and links to `Covering Tests` or `Tests` and `Detailed Coverage`. Read `references/coverage-gaps.md` for details.
- `Run Report` links to a report in the same format as the `run` command report for broader diagnostics from the same session state.

To list every file-section heading with its line number in `Coverage Gaps`:

```sh
rg -n '^## ' coverage-gaps.md
```

To locate the heading for `src/accounts.ts` and its line number in the report:

```sh
rg -n -Fx '## src/accounts.ts' coverage-gaps.md
```

To print the complete section for `src/accounts.ts`, starting at its heading and stopping before the next file section:

```sh
rg -U --pcre2 -o '(?sm)^## src/accounts\.ts\n.*?(?=^## |\z)' coverage-gaps.md
```

#### Detailed coverage

A `.wcov` artifact contains the complete source file annotated with source line numbers and coverage states: `full`, `partial`, or `none`. It preserves the source file's line count and line positions: line N in the artifact corresponds to line N in the source file, so you can locate coverage information directly by source line number. Partially covered lines also identify uncovered expression ranges when available. Use it to inspect which lines and expressions were executed or missed in their source context. Test analysis and file analysis with a matched `--test` filter show coverage for the selected test; otherwise, coverage reflects the active session. Read [references/wcov.md](references/wcov.md) for the format.

The artifact can be large. Prefer targeted searches instead of reading it in full. For example, to find partially covered lines:

```sh
rg -n 'coverage: partial' file-src@salerts.ts.wcov
```

To find fully uncovered lines:

```sh
rg -n 'coverage: none' file-src@salerts.ts.wcov
```

To show source line 146 of `src/alerts.ts` with its coverage annotation:

```sh
sed -n '146p' file-src@salerts.ts.wcov
```

To find a source expression with its coverage annotation and surrounding lines:

```sh
rg -n -C 3 -F 'alerts.push({' file-src@salerts.ts.wcov
```

### Inspect command

Use `inspect` directly when a failure or unexpected behavior depends on runtime state that static source, coverage, errors, and existing logs do not explain. Inspect variables and expressions at exact source locations to follow state changes, check the inputs and conditions behind a branch, or see why an assertion receives a particular value. Use this runtime evidence instead of adding and later removing temporary `console.log` statements.

The command only works when Wallaby is already running for the same project identity used by `run`. Start Wallaby first in project mode, or in exclusive mode that includes tests reaching the inspected locations. Then use `inspect` from the same working directory or with the same `--config` value as `run`. In an active session with the required tests included, a preceding `run` is unnecessary, including after edits.

Each inspection captures the expression's value in every test execution context that reaches its source location and identifies the test that produced each value. Pass multiple inspections across different files and locations in one request to investigate related runtime state together. Use `--test` to narrow the main report to values from matching tests while retaining a link to the complete unfiltered results.

For every resolved inspection in the request, Wallaby adds temporary runtime instrumentation, then executes the combined affected test set to collect all requested values. The command waits for those tests to finish before returning a consistent report. `--test` filters the reported values; it does not limit which affected tests execute.

After collecting the values, use `inspect --clear` without inspection targets to remove them. A clear-only request schedules no tests and completes immediately when the session is idle. When `--clear` is combined with new inspection targets, Wallaby clears the previous values first, then adds the new instrumentation and executes its affected tests as usual.

Pass each inspection target as a separate argument containing a file path, a source location, and an expression. The source location can be a code fragment, a line number, or a line and column. For example, to inspect the value of the `alerts` variable in `src/alerts.ts`:

```sh
npx wallaby-skill inspect "{path:'src/alerts.ts',location:{fragment:'const alerts: WeatherAlert[] = [];'},expression:'alerts'}" "{path:'src/alerts.ts',location:{line:134},expression:'alerts'}"
```

With fragment-based locations, the fragment acts as both file-search criteria and the containing snippet used to locate the expression inside the file. Fragment-based locations are often a better fit for coding agents because no line-number calculation is required.

A base64-encoded `fragment` avoids escaping special characters and newlines in multi-line fragments. The CLI decodes the fragment before searching the file:

```sh
npx wallaby-skill inspect "{path:'src/alerts.ts',location:{fragment:'Ly8gdW5pcXVlIGNvZGUgZnJhZ21lbnQKY29uc3QgYWxlcnRzOiBXZWF0aGVyQWxlcnRbXSA9IFtdOw=='},expression:'alerts'}"
```

If the line number is known, use it instead of a fragment:

```sh
npx wallaby-skill inspect "{path:'src/alerts.ts',location:{line:134},expression:'alerts'}"
```

If several occurrences of the expression are near the same line, add a column number to pick the closest match:

```sh
npx wallaby-skill inspect "{path:'src/alerts.ts',location:{line:134,column:10},expression:'alerts'}"
```

To show only values produced by tests with a matching name in the main report, pass `--test` with the full or partial test name:

```sh
npx wallaby-skill inspect "{path:'src/alerts.ts',location:{line:134},expression:'alerts'}" --test "alerts output / combined conditions"
```

To clear all previously captured runtime values, pass `--clear`:

```sh
npx wallaby-skill inspect "{path:'src/alerts.ts',location:{line:134},expression:'alerts'}" --clear # clears all captured runtime values and adds new inspection
npx wallaby-skill inspect --clear # clears all captured runtime values
```

When `--clear` is used without inspection targets, the command prints `Cleared all captured runtime values.` instead of a Markdown report.

Otherwise, the command prints a Markdown report and saves the same content as `inspect.md`. A non-zero exit code usually means the report contains failing tests or errors, though it may also mean the CLI or Wallaby itself failed:

- `Status`, `Mode`, and any `Fatal Error` or `Global Errors`, with the same meanings as in the run command report.
- `Runtime Values` shows captured values inline with the source file, line, expression, formatted value, and test that produced each value. If requested inspections could not be captured, it also shows warnings with the path, expression, location, and reason. If additional values are omitted, it links to the full runtime-values report. Read `references/runtime-values.md` when you need the full runtime-values report format.
- When `--test` is used, the main report filters runtime values by test name and links to the full unfiltered report when other values are available. Uncaptured-inspection warnings are still shown because they describe requested inspection locations, not captured values from a specific test.
- `Run Report` links to a report in the same format as the `run` command report for broader diagnostics from the same session state.

To find all captured values for `src/alerts.ts` in `Runtime Values`:

```sh
rg -U --pcre2 -o '(?sm)^## src/alerts\.ts[^\n]*\n.*?(?=^## |\z)' runtime-values.md
```

To find all runtime values produced by tests whose names mention `combined conditions`:

```sh
rg -U --pcre2 -o '(?sm)^## [^\n]*\n.*?^- name: .*combined conditions.*\n.*?(?=^## |\z)' runtime-values.md
```

### Stop command

After the first `run`, Wallaby remains active in the background, watches project files, and keeps its live test state available to later commands. Do not stop it between ordinary `run`, `analyze`, and `inspect` calls. When automatic shutdown is available, Wallaby stops when the detected agent process ends. It also stops after a period without CLI activity: 20 minutes when an agent process was detected, or 5 minutes when no supported agent process could be matched.

Use `stop` explicitly when the running process must be replaced or released:

- Before installing, updating, or removing Node modules, stop Wallaby, make the dependency change, then start it again with `run`. Wallaby does not watch changes inside `node_modules`, so the existing process cannot reliably use updated dependencies.
- Stop the existing session before restarting with a different Wallaby configuration or runtime environment.
- Stop immediately when the user asks, when a clean restart is needed, or when the running process must release its resources before automatic shutdown.

`stop` uses the same project identity as `run`, regardless of whether the session is in project or exclusive mode. Invoke it from the same working directory or with the same `--config` value as `run`. When switching configurations, stop the old session using its existing project identity before starting the new one.

```sh
npx wallaby-skill stop # stops the session identified by the current working directory
npx wallaby-skill stop --config ./wallaby.js # stops the session identified by this Wallaby configuration file
```

### Update command

When `run` reports a Wallaby Core compatibility error, update Core, then retry the same `run` command:

```sh
npx wallaby-skill update
```
