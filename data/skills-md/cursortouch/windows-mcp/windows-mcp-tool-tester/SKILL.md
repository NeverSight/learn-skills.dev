---
name: windows-mcp-tool-tester
description: >
  Automated testing skill for Windows-MCP tools. Use this skill whenever the user wants to test,
  validate, benchmark, or evaluate any Windows-MCP tool (App, PowerShell, Screenshot, Snapshot,
  Click, Type, Scroll, Move, Shortcut, Wait, MultiSelect, MultiEdit, Clipboard, Process,
  Notification, FileSystem, Registry, Scrape). Triggers on phrases like "test the Click tool",
  "benchmark Screenshot", "validate FileSystem", "run QA on Registry", "check if PowerShell works",
  "evaluate tool performance", or any mention of testing/validating a Windows-MCP tool.
  Each invocation tests exactly ONE tool.
---

# Windows-MCP Tool Tester

An automated testing skill that generates comprehensive test cases for a single Windows-MCP tool,
executes them, and produces a structured test report with pass/fail results, performance metrics,
and actionable recommendations.

## Core Principles

- **One tool per invocation.** If the user doesn't specify which tool to test, ask them before proceeding.
- **Black-box testing only.** Derive test cases exclusively from the MCP tool description and parameter schema — never read source code. Silence in the schema is a documentation gap, not a testing hint.
- **Auto-generate test cases** from the tool's MCP description and parameter schema. Cover common scenarios, edge cases, parameter combinations, and error handling paths.
- **Measure two dimensions**: correctness (return value matches expectations) and response time (end-to-end, including MCP overhead).
- **Mandatory side-effect verification**: every tool call that may modify system state MUST be independently verified — no exceptions, no sampling.
- **Safe cleanup**: track process PIDs spawned during testing; only kill those specific PIDs during teardown, never kill by process name alone.
- **Safety first**: Windows-MCP has full system access with no sandboxing. Tests involving
  destructive tools (FileSystem delete, Registry set/delete, Process kill, PowerShell) can
  modify or destroy data. Running in a **VM or Windows Sandbox** is strongly recommended.
  Before executing destructive test cases, confirm the user accepts the risk. See `SECURITY.md`.
- **Produce a structured report** at the end (see Step 4).

---

## Step 0: Identify the Target Tool

If the user hasn't specified a tool, present the full list and ask them to pick one:

> App, PowerShell, Screenshot, Snapshot, Click, Type, Scroll, Move, Shortcut, Wait,
> MultiSelect, MultiEdit, Clipboard, Process, Notification, FileSystem, Registry, Scrape

Once a tool is confirmed, proceed to Step 1. Do NOT test multiple tools in one session.

---

## Step 1: Analyze the Tool

Read the tool's MCP description and parameter schema via the MCP server's tool listing. Identify:

1. **All parameters** — name, type, required/optional, default value, allowed values (enums)
2. **All modes** (if the tool is mode-based, e.g., FileSystem has read/write/copy/move/delete/list/search/info)
3. **Return value structure** — what the tool returns on success vs. failure
4. **Side effects** — does it modify system state? (important for test isolation)
5. **Dependencies** — does it require a running app, an open window, existing files, etc.?

Use this analysis to inform test case generation. If the description is ambiguous or silent on a
behavior, note it as a documentation gap and design a test to probe it. The tool's response is
the ground truth.

---

## Step 2: Generate Test Cases

Design test cases that cover the following categories. Not every category applies to every tool —
use judgment based on the tool's nature.

### Category A: Basic Functionality (Required)
Test the tool's primary purpose with standard, well-formed inputs.
- One test per mode/operation type (e.g., for FileSystem: read, write, list, etc.)
- Use realistic parameter values

### Category B: Parameter Variations (Required)
- Test each optional parameter individually to verify it takes effect
- Test enum parameters with every allowed value
- Test boolean parameters in both true and false states
- **For `anyOf` union types**: The schema advertises all listed types as valid, so the tool must handle each correctly.
  - `anyOf: [boolean, string]` (e.g., `drag`, `use_vision`): test boolean `true`/`false` AND string `"true"`/`"false"` — both must produce the same behavior.
  - **Caveat:** MCP transport layers may silently coerce `"true"` (string) to `true` (boolean)
    before the tool sees it. To genuinely probe the string path, also test non-standard truthy
    strings like `"yes"` or `"1"` — if those fail while `"true"` passes, the tool likely only
    receives booleans and the string branch is untested.
  - `anyOf: [<type>, null]` (nullable): test with a valid value AND explicit `null`. An unhandled TypeError on null is a FAIL.
- Test with default values (omit optional params) vs. explicit values

### Category C: Edge Cases (Required)
- Empty strings, zero values, negative numbers where applicable
- Boundary values (e.g., very long text for Type, timeout=0 for PowerShell)
- Unicode / special characters in string parameters
- Very large or very small numeric inputs

### Category D: Error Handling (Required)
- Missing required parameters
- Invalid parameter types or out-of-range values
- Referencing nonexistent resources (files, windows, processes, registry keys)
- Operations that should fail gracefully (e.g., deleting a non-existent file)

### Category E: Parameter Interaction (When Applicable)
- Combinations of parameters that might interact (e.g., Click with both `loc` and `label`)
- Mutually exclusive parameters
- Mode-specific parameter requirements
- **Cross-mode parameter applicability**: For mode-based tools, pass parameters meant for one
  mode while calling another (e.g., `window_loc` in `launch` mode). Silently ignoring them is
  a documentation gap worth reporting.

### Category F: Idempotency & State (When Applicable)
- For tools marked `idempotentHint: true`: call twice with same args, verify same result
- For destructive tools: verify cleanup or rollback is possible
- For stateful tools: verify state changes are reflected correctly

### Test Case Format

For each test case, define:

```
ID:          TC-{ToolName}-{Number}
Category:    A/B/C/D/E/F
Description: What this test verifies
Parameters:  The exact parameters to pass
Expected:    What a correct result looks like (success/failure, key content in response)
Setup:       Any prerequisite actions (create a file, open an app, etc.)
Teardown:    Any cleanup actions after the test
```

Present the test plan to the user for confirmation before executing.
Aim for **10-20 test cases** depending on tool complexity.

Include an **estimated execution time**: approximately **30-45 seconds** per test case
(includes timing calls, tool execution, verification). App launches add 5-10s extra.
Present as a range, e.g., "Estimated execution time: 8-12 minutes (15 test cases)".

---

## Step 3: Execute Tests

### Pre-Test Step 1: Gather Environment Info

Before running test cases, collect the test environment details for the report. Use these
PowerShell commands for reliable results:

```powershell
# OS version
(Get-CimInstance Win32_OperatingSystem).Caption + " " + (Get-CimInstance Win32_OperatingSystem).Version

# Display resolution (physical pixels)
Get-CimInstance Win32_VideoController | Select-Object CurrentHorizontalResolution, CurrentVerticalResolution

# Display count
(Get-CimInstance Win32_PnPEntity | Where-Object { $_.PNPClass -eq 'Monitor' -and $_.Status -eq 'OK' }).Count

# DPI scale factor (96 = 100%, 120 = 125%, 144 = 150%, 192 = 200%)
Get-ItemProperty 'HKCU:\Control Panel\Desktop\WindowMetrics' -Name AppliedDPI -ErrorAction SilentlyContinue | Select-Object -ExpandProperty AppliedDPI
```

Also call Screenshot once — its `Screenshot Original Size` cross-checks the DPI value,
and its output includes `Active Desktop` and `All Desktops`.

### Pre-Test Step 2: Prepare Environment

For **input tools** (Type, Click, Scroll, Move, Shortcut, MultiSelect, MultiEdit), prepare the
environment before executing any test cases:

1. **IME (Input Method) state**: Check the Tray Input Indicator in the Snapshot output. If it
   shows a non-English input mode (e.g., "Chinese Mode", "Japanese Mode"), switch to English
   mode first using the `Shortcut` tool (typically `shift` to toggle). **This is critical for
   Type tool tests** — an active IME will intercept keystrokes and produce incorrect characters.
   Record the original IME state and restore it after testing.

2. **Label availability check**: Call Snapshot on the test target window and verify whether the
   element you intend to use with `label` parameter is actually listed in the Interactive Elements.
   Common pitfalls:
   - Modern Windows 11 Notepad's text editing area is **not** exposed as an interactive element
     in the UI tree — use `loc` coordinates instead.
   - Some complex controls (e.g., rich text editors, canvas-based UIs) may not enumerate child
     elements.
   If a planned `label`-based test has no valid label target, adapt the test to use `loc`, or
   pick a different element that does have a label (e.g., a search box, address bar).

3. **Warm-up call**: Execute 1-2 throwaway tool calls (not counted in test results) to warm up
   the MCP connection, window focus, and UI tree cache. First calls are typically slower due to
   cold start effects — excluding them gives more representative performance numbers.

### Test Execution

Run each test case sequentially. For each test:

> **Label freshness rule:** Snapshot labels are a point-in-time snapshot. If any action between
> tests could change the UI state, call Snapshot again before using `label` parameters.

> **State reset between tests:** Each test case should start from a known, clean state. For
> input tools sharing a test window (e.g., Notepad), define a standard reset procedure and
> execute it in Setup:
> - **Type tests**: Shortcut (Ctrl+A) → Shortcut (Delete) to clear the text area
> - **Click/Move tests**: Move cursor to a neutral position away from interactive elements
> - **Scroll tests**: Reset scroll position to top (Ctrl+Home)
>
> If a test's Setup includes `clear=true` in the tool call itself, you may skip the manual
> reset — but verify in the teardown that the state is clean for the next test.

1. **Setup** — perform any prerequisite actions (e.g., create a temp file for FileSystem read tests).
   When spawning processes, **record their PIDs** for teardown (see Test Isolation Guidelines).
2. **Record start time** — call PowerShell to capture a precise timestamp in milliseconds **before** calling the tool:
   ```powershell
   [long](([System.DateTime]::UtcNow - [System.DateTime]::UnixEpoch).TotalMilliseconds)
   ```
   Save the returned integer as `$t_start`.
3. **Call the MCP tool** with the specified parameters
4. **Record end time** — immediately after the tool returns, call PowerShell again with the same command. Save as `$t_end`.
5. **Compute elapsed time** — `elapsed_ms = $t_end - $t_start`. Note: this includes MCP
   overhead from the timestamp calls themselves (~3-5s each). Use for relative comparison
   between test cases only. **When testing the PowerShell tool itself**, timing is
   self-referential — record times as `N/A (self-referential)` and rely on the PowerShell
   tool's own `timeout` behavior and status codes for performance assessment instead.
6. **Capture the response** — store the full return value and measure `response_size`:
   - **Text-only tools**: character count of the returned string.
   - **Mixed-content tools** (Screenshot, Snapshot): character count of the **text portion only**,
     note `+image` in the report. Do not attempt to measure image byte size.
7. **Evaluate correctness** — compare the response against expected behavior:
   - Does the response indicate success/failure as expected?
   - Does the response content match expected patterns?
   - For error cases: does the error message make sense and provide useful information?
8. **Verify side effects (MANDATORY)** — independently verify EVERY mutating tool call. Never
   rely solely on the tool's return value. Never skip or sample.
   **Rule: verification MUST NOT use the same tool under test.** Use a different tool
   (preferably PowerShell) to cross-check. Verification methods:
   - **Move/Click**: call Screenshot or Snapshot to verify the expected UI change occurred.
   - **Type**: use Shortcut (Ctrl+A → Ctrl+C) then PowerShell `Get-Clipboard` to capture
     exact text for comparison.
   - **Drag (Move with drag=True)**: call Snapshot to verify the target window actually moved.
   - **App (launch/resize)**: call PowerShell (`Get-Process`) to verify process exists, and
     Screenshot/Snapshot to verify window position/size.
   - **FileSystem**: verify with PowerShell (`Test-Path`, `Get-Content`, `Get-ChildItem`)
     — never with the FileSystem tool itself.
   - **Registry**: verify with PowerShell (`Get-ItemProperty`, `reg query`)
     — never with the Registry tool itself.
   - **Clipboard (set)**: verify with PowerShell (`Get-Clipboard`)
     — never with the Clipboard tool itself.
   - **Process (kill)**: verify with PowerShell (`Get-Process -Id $pid`)
     — never with the Process tool itself.
   - **Shortcut**: call Screenshot to verify the shortcut's expected effect occurred.
   - For read-only tools (Screenshot, Snapshot, Scrape, Process list), this step is not needed.
   - If verification fails but the tool reported success, mark the test as **FAIL** and note
     "tool reported success but side effect not confirmed" in the root cause analysis.
9. **Teardown** — clean up any side effects (delete temp files, close apps, etc.)

> **IMPORTANT:** Never estimate response times. Always use the PowerShell measurement above.
> If unavailable, record `N/A` and explain why.

### Correctness Evaluation Criteria

| Result    | Meaning                                                                                       |
|-----------|-----------------------------------------------------------------------------------------------|
| PASS      | Response matches expected behavior exactly                                                    |
| SOFT PASS | Response is acceptable but slightly different from ideal (e.g., extra whitespace, ordering)    |
| FAIL      | Response doesn't match expected behavior — includes cases where the tool rejects schema-valid input. Never look up source code to explain away a failure. |
| ERROR     | Tool threw an unexpected exception or timed out                                               |
| SKIP      | Test couldn't run due to missing prerequisites (document why)                                 |

### When to SKIP vs. Adapt

If a planned test case cannot execute as designed (e.g., the target element has no `label` in the
UI tree, or a required window state cannot be achieved), decide:

- **SKIP** if the prerequisite is truly missing and no workaround exists. Document the reason.
- **Adapt** if you can achieve the same test intent with a different approach (e.g., use `loc`
  instead of `label`, use a different target app). Update the test case description and note the
  adaptation in the report. Adapting is preferred over skipping when the test intent is still
  achievable.

### Performance Tracking

For each test case, record **response time (ms)** via PowerShell timestamps and
**response size** (character count of the raw response text).

> **Warm-up effect:** The first 1-2 tool calls in a session are typically slower due to MCP
> connection warm-up, UI tree cache initialization, and window focus acquisition. If warm-up
> calls were performed in Pre-Test, note this in the report. If not, flag the first test case's
> timing as potentially inflated and exclude it from aggregate statistics (average, median, P95)
> or mark it separately.

---

## Step 4: Generate the Test Report

**Localization:** If the user specified a language, write the entire report in that language
(headings, tables, commentary, recommendations). Keep test case IDs (e.g., TC-Move-01) in
English. The template below is a structural reference — translate all prose while preserving
the markdown structure.

````markdown
# Windows-MCP Tool Test Report: {ToolName}

**Date:** {timestamp}
**Tool:** {ToolName}
**Total Test Cases:** {N}
**PASS:** {P} | **SOFT PASS:** {SP} | **FAIL:** {F} | **ERROR:** {E} | **SKIP:** {S}
**Overall Pass Rate:** {(P+SP)/N * 100}%

---

## 1. Test Environment

{Record the environment to aid reproducibility. Data gathered in Pre-Test step.}

| Item                     | Value                                                    |
|--------------------------|----------------------------------------------------------|
| OS Version               | {e.g., Windows 11 Pro 10.0.26200}                       |
| Display Resolution       | {e.g., 2560x1440}                                       |
| Screenshot Original Size | {e.g., 3840x2160 — this is resolution x scale factor}   |
| Display Count            | {e.g., 1}                                                |
| Active Virtual Desktop   | {e.g., Desktop 1}                                        |
| MCP Transport            | {e.g., SSE via http://localhost:8088/sse}                |
| Scale Factor             | {e.g., 150% (AppliedDPI=144)}                           |

---

## 2. Executive Summary

{2-3 sentences summarizing the overall health of the tool. Highlight critical failures if any.
Note any patterns — e.g., "all error-handling tests failed" or "basic functionality is solid
but Unicode support is incomplete." Also assess these dimensions when relevant:}

- **Error message quality**: descriptive and actionable, or cryptic?
- **Input validation**: does the tool validate params before executing, or fail deep with confusing errors?
- **Consistency**: do repeated calls with same params return consistent results?
- **Graceful degradation**: when prerequisites are missing, does the tool explain what's needed?

---

## 3. Failed & Error Test Cases

{For each non-passing test case, provide:}

### TC-{ID}: {Description}
- **Category:** {category}
- **Parameters:** `{params}`
- **Expected:** {what should have happened}
- **Actual:** {what actually happened}
- **Side-Effect Verification:** {what the independent verification revealed, if applicable}
- **Root Cause Analysis:** {your best assessment of why it failed}
- **Suggested Fix:** {actionable recommendation for the developer}

{If all tests passed, write: "All test cases passed. No issues to report."}

---

## 4. Performance Analysis

> **Note:** All times are end-to-end measurements including MCP transport overhead
> (serialization, network round-trip, SSE/stdio latency). They do NOT represent pure tool
> execution time. Use these numbers for **relative comparison** and outlier detection — not
> as absolute benchmarks. For pure execution time, check server-side logs with
> `WINDOWS_MCP_PROFILE_SNAPSHOT=1`.

### Response Time

| Test Case | Time (ms) | Assessment |
|-----------|-----------|------------|
| TC-XXX-01 | 6500      | Normal     |
| TC-XXX-02 | 15200     | Slow       |
| ...       | ...       | ...        |

**Average:** {avg} ms | **Median:** {median} ms | **P95:** {p95} ms | **Max:** {max} ms

**Assessment thresholds (end-to-end including MCP overhead):**
- Fast: < 5000ms
- Normal: 5000ms – 10000ms
- Slow: 10000ms – 20000ms
- Very Slow: > 20000ms

{Commentary on any outliers or concerning patterns. When a test case is significantly slower
than peers, note possible causes: app launch wait, UI tree traversal, screenshot capture, etc.}

### Response Size

| Test Case | Response Size (chars) |
|-----------|-----------------------|
| TC-XXX-01 | 245                   |
| ...       | ...                   |

{Note any unexpectedly large or empty responses.}

---

## 5. Environmental Interference & Notes

{List any environmental factors that affected test execution but are not bugs in the tool itself.
These factors help future testers reproduce results and avoid false failures.}

| # | Factor | Impact | Mitigation |
|---|--------|--------|------------|
| 1 | {e.g., IME in Chinese mode} | {e.g., TC-Type-01 typed wrong characters} | {e.g., Switched IME to English before retesting} |
| ... | ... | ... | ... |

**Common environmental factors:**
- **IME state**: Active non-English input methods intercept keystrokes (affects Type, Shortcut)
- **Notification popups**: System or app notifications may steal focus mid-test
- **Background app focus changes**: Chat apps, update dialogs may overlay the test window
- **Screen lock / screensaver**: Can interrupt long-running test sessions
- **Clipboard managers**: Third-party clipboard tools may interfere with Clipboard tests

{If no environmental interference occurred, write: "No environmental interference observed."}

---

## 6. Documentation & Schema Gaps

{List any discrepancies between the tool's MCP parameter schema / description and its actual
behavior or environmental interactions. These are not necessarily bugs — they are places where
the documentation or schema could be improved to set correct expectations for callers.}

| #   | Gap Type                          | Description | Recommendation |
|-----|-----------------------------------|-------------|----------------|
| 1   | {schema / description / behavior} | {desc}      | {rec}          |
| ... | ...                               | ...         | ...            |

**Gap Types:**
- **schema**: parameter schema (types, required/optional, allowed values) does not match actual behavior
- **description**: tool description is silent or ambiguous about a behavior that testing revealed
- **behavior**: tool behaves inconsistently with what the schema + description together imply

{If no gaps were found, write: "No documentation or schema gaps identified."}

---

## 7. All Test Cases

| ID         | Category   | Description | Result | Time (ms) | Response Size |
|------------|------------|-------------|--------|-----------|---------------|
| TC-XXX-01  | A - Basic  | {desc}      | PASS   | 6500      | 245           |
| TC-XXX-02  | B - Params | {desc}      | FAIL   | 8200      | 310           |
| ...        | ...        | ...         | ...    | ...       | ...           |
````

---

## Test Isolation Guidelines

To avoid polluting the system or interfering with user state:

- **FileSystem tests**: Use a dedicated temp directory (e.g., `%TEMP%\wmcp-test-{timestamp}\`).
  Clean up after all tests complete.
- **Registry tests**: Use a dedicated test key under `HKCU:\Software\WMCP-Test-{timestamp}`.
  Delete the entire key after testing.
- **Process tests**: Only list processes (don't kill user processes). If testing kill, spawn a
  sacrificial process first (e.g., `notepad.exe`) and record its PID.
- **App tests**: Use lightweight apps (Notepad, Calculator). **Record PIDs** of all processes
  spawned during testing (use `(Start-Process notepad -PassThru).Id` or query process list
  before/after launch). In teardown, only kill processes by PID — NEVER by name (e.g.,
  `Stop-Process -Id $pid`, not `Stop-Process -Name notepad`), because the user may have their
  own instances of the same application running.
  - **Modern tabbed apps caveat:** Windows 11 Notepad/Terminal may reuse a single process for
    multiple tabs. Diff the process list before/after each launch to detect new PIDs. Only kill
    PIDs that did not exist before testing began.
- **Clipboard tests**: Save and restore the original clipboard content.
- **Input tools (Click, Type, Scroll, Move, Shortcut)**: Open a dedicated test window
  (e.g., Notepad) to receive input. Don't interact with user's active work.
  See also Pre-Test Step 2 for IME state handling — switch to English input mode before testing
  and restore the original state in final teardown.
- **Read-only tools (Screenshot, Snapshot, Scrape)**: Safe to run freely.
- **Notification tests**: User-visible (sends Windows toasts). Avoid repeated or unnecessary
  notifications. Prefer a single clearly labeled test notification per test case.
- **PowerShell tests**: Use read-only commands where possible.

---

## Tool-Specific Testing Guidance

Hints per tool. Always read the actual schema to discover additional scenarios beyond these.

### App
- Modes: launch, resize, switch. Test each mode.
- Launch: test with known apps (notepad, calc), unknown app names
- Resize: test with valid window_loc/window_size, without an active app
- Switch: test switching to a running app, to a non-existent app

### PowerShell
- Simple commands: `echo "hello"`, `Get-Date`, `Get-Process | Select-Object -First 3`
- Timeout behavior: set a very short timeout with a long-running command
- Encoding: commands with Unicode output
- Error output: commands that write to stderr
- Exit codes: commands that fail (e.g., `Get-Item nonexistent`)

### Screenshot
- Default parameters (no args)
- With annotation enabled/disabled
- With reference lines
- With specific display index
- Verify return includes image data

### Snapshot
- Various flag combinations: use_vision, use_dom, use_annotation, use_ui_tree
- All flags off vs. all flags on
- With/without reference lines

### Click
- By coordinates (loc) vs. by label
- Different button types: left, right, middle
- clicks=0 (hover), clicks=1 (single), clicks=2 (double)
- Invalid coordinates (negative, off-screen)
- Invalid label (non-existent element ID)

### Type
- Normal text, Unicode text, special characters
- With and without clear=true
- With and without press_enter=true
- Different caret_position values: start, idle, end
- By coordinates vs. by label
- **IME sensitivity**: Test with IME active to verify behavior (expect failure if tool uses
  keystroke simulation rather than Unicode input). This is a high-value edge case because
  many Windows machines have non-English IMEs installed.
- **Emoji / surrogate pair characters**: Test with characters outside the Basic Multilingual
  Plane (e.g., 🌍, 😀) to verify supplementary plane Unicode support.
- **Empty string**: Test `text=""` — this is a common edge case that may crash if the
  implementation indexes into the string without a length check.

### Scroll
- Vertical up/down, horizontal left/right
- Different wheel_times values (1, 5, 10)
- By coordinates vs. by label

### Move
- Simple move to coordinates
- Drag mode (drag=true)
- By coordinates vs. by label

### Shortcut
- Common shortcuts: ctrl+c, ctrl+v, ctrl+a, alt+tab
- Windows key shortcuts: win+r, win+d
- Multi-key combinations
- Invalid key names

### Wait
- Short duration (1 second)
- Zero duration
- Verify actual elapsed time roughly matches requested duration

### MultiSelect
- Select multiple items by coordinates
- Select by labels
- With and without press_ctrl
- Empty list of items

### MultiEdit
- Edit multiple fields by coordinates
- Edit by labels
- Mixed valid and invalid targets

### Clipboard
- get mode when clipboard has text
- get mode when clipboard is empty
- set mode with normal text
- set mode with Unicode text
- Roundtrip: set then get, verify content matches

### Process
- list mode with default sort
- list mode with different sort_by values (memory, cpu, name)
- list mode with name filter
- list mode with different limit values
- kill mode with a sacrificial process (spawn notepad, then kill it)

### Notification
- Valid notification with title, message, app_id
- Empty title or message
- Special characters in title/message

### FileSystem
- Full mode coverage: read, write, copy, move, delete, list, search, info
- Read: existing file, non-existent file, offset/limit, different encodings
- Write: new file, overwrite, append
- List: with and without pattern, recursive, show_hidden
- Delete: file, empty dir, non-empty dir with recursive

### Registry
- Full mode coverage: get, set, delete, list
- Set and get roundtrip
- Different value types (String, DWord, QWord)
- Non-existent key/value
- Use test-only registry path

### Scrape
- With a URL (lightweight page)
- With and without query parameter
- With use_dom enabled (requires open browser)
- Invalid URL
