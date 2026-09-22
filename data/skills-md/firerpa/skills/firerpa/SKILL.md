---
name: firerpa
description: Create FIRERPA / lamda Android automation scripts for Android apps and UI workflows. Use when the user wants to automate an Android app task, inspect UI state, build a selector-driven flow, or write a reusable device automation script.
---

Write **Python automation** with `lamda` (`from lamda.client import *`).

---

## Agent Instructions — READ FIRST

**Use the unified CLI `scripts/firerpa.py` via Shell.** Do not reimplement device calls inline.

This skill is only for producing automation script files. The final deliverable must be a saved, reusable script file. Do not treat one-off live control, transient shell driving, or non-persisted device manipulation as the result.

## Available scripts

- `scripts/firerpa.py` - Unified FIRERPA CLI for device connectivity checks, app prechecks, UI inspection, selector checks, and simple device actions.

## Available functionality

Use `scripts/firerpa.py` for these capabilities:

- Connectivity and server checks: `server-info`, `device-info`
- App prechecks: `app-list`, `app-check`, `app-current`
- App control: `app-start`, `app-stop`
- UI inspection: `dump`, `screenshot`
- Selector checks and interaction: `exists`, `wait-exists`, `wait-gone`, `selector-info`, `get-text`, `set-text`, `clear-text`, `click`, `tap-bounds-center`, `scroll-to`
- Simple device actions: `press`, `wait-idle`, `wake`, `sleep`
- Shell execution on device: `shell`

### Purpose and boundaries

Rules:

1. Stay inside the user-requested task. Do not add side experiments, alternate flows, unrelated app tests, or demo scenarios.
2. The CLI in `scripts/firerpa.py` is the required path for device inspection and operational checks.
3. Do not use inline `Device(...)` probes, `python -c`, heredoc snippets, temporary inspection scripts, or virtual-display test harnesses for quick validation.
4. Only write a separate Python script for the actual automation task logic.
5. Do not substitute manual control for script delivery.
6. If the task is under-specified, ask or stop at the narrowest correct implementation rather than inventing surrounding behavior.

### Target-app discipline

If the user specified a target app, package, activity, or workflow context, keep all task logic, verification, and examples anchored to that target.

Rules:

1. Do not substitute a different app just because it is easier to test.
2. Do not switch to unrelated system apps, browsers, launchers, or demo apps unless the user explicitly asked for those apps.
3. Do not use unrelated apps to "verify the environment" when the requested task is about a different target app.
4. If the target app cannot be reached, is missing, is version-mismatched, or is blocked by a user-control gate, stop and report that exact blocker instead of drifting into another app.
5. If examples are app-specific, keep the examples aligned with the user's requested target or use neutral placeholders like `com.example.app`.

Allowed inspection path:

- Use only `scripts/firerpa.py` for device inspection, app prechecks, selector checks, and operational validation.
- The allowed command surface is the functionality listed above plus the command reference in `All CLI commands`.

### Source of truth

Lookup priority:

1. `scripts/firerpa.py` for CLI workflow and command syntax
2. `client/client.py` for Python API method names and object behavior
3. `client/rpc/*.proto` for field names, message shapes, and enum names
4. `references/reference.md` for condensed reminders
5. `references/llms-full.txt` only for supplemental background and examples

Rules:

1. If memory, examples, or external docs conflict with local code, follow local code.
2. If a method, selector pattern, field, or enum name is not confirmed in local source, treat it as unavailable.
3. For non-trivial API usage, read `client/client.py` first.
4. Do not use `references/llms-full.txt` as the source of truth for API names, CLI syntax, or proto field names when local code disagrees.

### Verification standard

Self-verification is required.

Rules:

1. Do not treat script execution without errors as proof of success.
2. After running the script, verify both action success and result reasonableness.
3. Prefer verification through `scripts/firerpa.py` state checks such as `dump`, `screenshot`, `exists`, `app-current`, `device-info`, and `app-check`.
4. If the task changes UI state, re-dump the UI and confirm the expected state transition.
5. If the task writes text, sends content, changes settings, opens a page, or triggers navigation, verify the resulting visible state or app state accordingly.
6. Do not rely only on prints from the task script when a device-side state check is available.
7. If verification is inconclusive, say so and return control rather than claiming success.
8. Do not loop indefinitely on retries, validation attempts, or alternate checks.
9. If conditions are not met, verification fails, or the next action requires a user decision, stop and report what was checked, what failed, and what the user should decide or do next.

### Interaction rules

Drive the flow from observable device state, not guesswork.

Rules:

1. Prefer the most stable selector available. `resourceId` or another strong identifier usually beats visible text.
2. When text is dynamic, `textContains` or `textMatches` may be appropriate if they are the most reliable way to identify the target.
3. A matched element is not automatically the correct element; constrain high-risk actions and verify the result.
4. Re-locate elements after page changes, scrolling, or refreshes instead of relying on stale element objects.
5. Do not assume element operations implicitly wait long enough. Use explicit checks such as `wait_for_exists(timeout)` when the next step depends on state.
6. Do not treat `exists()` as proof that an element is ready for interaction; it only proves a match was found.
7. Do not use fixed `sleep()` as the primary synchronization strategy. If a short sleep is used as a supplement, follow it with an explicit state check.
8. Prefer `set_text()` for text entry and explicit submit, confirm, save, or send elements for business actions.
9. Do not use `press` as the primary way to submit text, confirm forms, or trigger business actions when a stable element interaction is available.
10. Do not assume `ENTER` means submit. It may insert a newline, confirm IME composition, trigger a search/send action, or do nothing.
11. Do not assume the intended element owns focus. Soft keyboards, dialogs, overlays, and custom views can redirect or consume key events.
12. Treat `BACK`, `HOME`, and `ENTER` as high-ambiguity actions. Use `press` only for explicit navigation or dismissal, and verify the resulting visible state before continuing.
13. Do not use coordinate-driven interaction as a normal path when selector-driven interaction is available.
14. Do not treat screenshot capture as proof that the target page is loaded or correct.
15. Do not treat text entry success as proof that the business action was submitted or completed.
16. Check app context at critical boundaries. Treat permission pages, system dialogs, and intermediate system surfaces as separate contexts, and identify blockers before continuing if the flow leaves the expected app or screen family.

```bash
python3 scripts/firerpa.py --help
python3 scripts/firerpa.py dump --host 192.168.0.2 -o ui.xml
```

Use explicit connection flags: `--host`, `--port`, and `--certificate`.

Examples:

```bash
python3 scripts/firerpa.py shell --host 192.168.0.2 "id"
python3 scripts/firerpa.py press --host 192.168.0.2 KEY_BACK
python3 scripts/firerpa.py wait-idle --host 192.168.0.2 3000
python3 scripts/firerpa.py server-info --host 192.168.0.2 --port 65001
python3 scripts/firerpa.py server-info --host 192.168.0.2 --port 65001 --certificate /path/to/lamda.pem
```

### Device host — ask if missing

**Do not guess `--host`.** If the user did not provide a host -> stop and ask:

> Please provide the FIRERPA device address (IP or hostname). You can copy the Console URL from the app. If certificates or a non-default port are enabled, also provide the `lamda.pem` path and port number.

### Connection and app prechecks

If connection fails, do not continue with automation design. Walk the user through the following checks in order and retry the smallest useful command after each confirmed fix.

1. **Confirm target address**
   - Check whether `--host` is present.
   - Ask the user for the FIRERPA Console URL, device IP, hostname, or forwarding target.
   - Do not guess LAN IPs, localhost forwarding, or public endpoints.

2. **Test the service with a minimal command**
   - Prefer `python3 scripts/firerpa.py server-info`
   - If needed, use `python3 scripts/firerpa.py device-info`
   - Only move to `dump` after basic connectivity works

3. **Check whether the FIRERPA service is installed on the device**
   - Ask whether the FIRERPA server/app/service has been installed on the Android device
   - If the user is unsure, direct them to verify in the FIRERPA app or service management UI
   - If not installed, stop automation work and guide installation first

4. **Guide installation when the service is missing**
   - Preferred: install via the FIRERPA Android app / built-in installer flow
   - Alternative: manual service installation if the user is not using the app-managed flow
   - Required follow-up checks after installation:
     - confirm device architecture if manual package selection is needed
     - confirm the service was started successfully
     - confirm the exposed host/port shown by the app or Console URL

5. **Check whether the service is running**
   - Ask the user whether the FIRERPA service is currently started on the device
   - If installed but stopped, have them start the service first
   - If they restarted or reconfigured it, re-check host / port / certificate details

6. **Check port and forwarding path**
   - Default port is `65000`
   - If using ADB forward, prefer `localhost` and verify the forward target
   - If using frp / Hub / VPN / other forwarding, confirm the externally exposed host and port rather than the device LAN address

7. **Check certificate / TLS mode**
   - If the error mentions TLS, SSL, certificate, handshake, or verify failures, ask whether the service was configured with certificates
   - If TLS is enabled, require the matching `--certificate /path/to/lamda.pem` before retrying
   - If TLS is disabled, do not invent certificate settings

8. **Retry after each confirmed fix**
   - First retry `server-info`
   - Then retry `device-info`
   - Then run `dump`
   - Only after one of these succeeds may you continue writing selectors or automation code

9. **Escalation boundary**
   - If the user cannot confirm whether the service is installed, running, or reachable, switch into troubleshooting guidance mode rather than code-writing mode
   - Do not fabricate installation status, port configuration, or certificate state

App prechecks:

1. Use `app-list` to inspect installed user apps.
2. Use `app-check` before app-specific automation when the package/name is user-provided, ambiguous, or version-sensitive.
3. If the target app does not exist in user apps, stop and tell the user to install it.
4. If the requested `versionName` does not match, stop and tell the user to install or reinstall the expected version.
5. Do not continue into selectors, navigation, or script writing for a missing or mismatched target app.
6. Do not replace a blocked target app with a different app for testing or demonstration.

### Authoring workflow

Default path:

1. Connect successfully.
2. If app-specific, run `app-list` / `app-check`.
3. Run `dump` first and read `ui.xml`.
4. Use `screenshot` only when XML is empty or insufficient.
5. Write the task script with selectors derived from `ui.xml`, and enable debug logging near device initialization with `d.set_debug_log_enabled(True)`.
6. Prefer element-driven interactions such as `click()` and `set_text()`; use key presses only for navigation or dismissal when a stable element-driven path is unavailable.
7. Run the task script.
8. Verify the resulting state with `firerpa.py`.

### Shell examples

```bash
CLI="scripts/firerpa.py"
OUT_DIR=".firerpa"
mkdir -p "$OUT_DIR"

python3 "$CLI" dump --host 192.168.0.2 -o "$OUT_DIR/ui.xml"
python3 "$CLI" screenshot --host 192.168.0.2 -o "$OUT_DIR/screen.jpg"
python3 "$CLI" app-list --host 192.168.0.2
python3 "$CLI" app-check --host 192.168.0.2 --package com.example.app
python3 "$CLI" selector-info --host 192.168.0.2 --resource-id "com.example:id/title"
python3 "$CLI" get-text --host 192.168.0.2 --resource-id "com.example:id/input"
python3 "$CLI" set-text --host 192.168.0.2 --resource-id "com.example:id/input" --value "hello"
python3 "$CLI" exists --host 192.168.0.2 --text "Sign in"
python3 "$CLI" click --host 192.168.0.2 --resource-id "com.example:id/btn"
python3 "$CLI" device-info --host 192.168.0.2
python3 "$CLI" app-current --host 192.168.0.2
python3 your_task.py
python3 "$CLI" dump --host 192.168.0.2 -o "$OUT_DIR/verify.xml"
```

Then **Read** output files: `ui.xml` first; `screen.jpg` only if screenshot was run.

Hard rules:

1. No host -> ask the user. Connection failed -> troubleshoot first.
2. Complete connectivity checks before selector discovery.
3. First UI inspection call must be `firerpa dump` or `app-start` then `dump`.
4. Read `ui.xml` before writing selectors.
5. Never guess selectors from docs or memory.
6. Always deliver a persisted script file.
7. In the delivered automation script, enable lamda debug logging with `d.set_debug_log_enabled(True)` near device initialization unless the user explicitly asks to suppress logs.
8. Prefer element-driven interactions over key presses whenever a stable selector-driven path exists.
9. Use `press` only for navigation or dismissal when element-driven interaction is unavailable or clearly less reliable.
10. Never assume `ENTER` is a safe submit action; prefer explicit element-based submission and treat `ENTER` as ambiguous.
11. After any `press`, verify the resulting visible state before continuing.
12. Do not add `d.set_debug_log_enabled(True)` to CLI inspection commands, ad hoc validation snippets, or non-deliverable helper code.
13. Always verify both action success and result reasonableness after running the script.
14. Do not keep retrying validation loops; when blocked, stop with enough information for the user to judge the next step.

### Forbidden API guesses

Do not import habits or syntax from Appium, Selenium, Playwright, uiautomator2, or other Android automation wrappers.

| Wrong | Correct |
|-------|---------|
| `driver.find_element(...)` | `d(text="...")`, `d(resourceId="...")`, `d(description="...")` |
| `driver.find_elements(...)` | `d(...).count()`, `d(...).get(idx)`, `for x in d(...): ...` |
| `el.input_text()` | `el.set_text()` |
| `el.clear_text()` | `el.clear_text_field()` |
| `d.shell("cmd")` | `d.execute_script("cmd")` |
| `app.clear_data()` | `app.reset()` |
| `wait_for_element(...)` | `el.wait_for_exists(timeout)` |
| XPath selectors / XPath-derived queries | selectors built from `ui.xml` fields such as `text`, `resourceId`, `description`, and `className` |

If a generated snippet contains any unverified method, stop and verify it in `client/client.py` before continuing.

### Allowed common APIs

Prefer these known-good APIs unless the task clearly requires something else and the alternative has been verified in `client/client.py`.

**Device**

- `d(...)`
- `d.set_debug_log_enabled(True)`
- `d.dump_window_hierarchy(...)`
- `d.screenshot(...)`
- `d.device_info()`
- `d.current_application()`
- `d.application(...)`
- `d.get_application_by_name(...)`
- `d.execute_script(...)`
- `d.wait_for_idle(...)`
- `d.press_key(...)`
- `d.wake_up()`
- `d.sleep()`

**Element**

- `el.click()`
- `el.click_exists()`
- `el.long_click()`
- `el.exists()`
- `el.info()`
- `el.get_text()`
- `el.set_text()`
- `el.clear_text_field()`
- `el.wait_for_exists(timeout)`
- `el.wait_until_gone(timeout)`
- `el.scroll_to(...)`
- `el.swipe(...)`
- `el.drag_to(...)`

### Proto field access rules

Many return values in `lamda` are protobuf-backed objects. Field access must follow the proto definitions and generated client exactly.

Rules:

1. Never guess field names from habits in Appium, Selenium, Playwright, uiautomator2, Java beans, Python dicts, or snake_case conventions.
2. Confirm field names in `client/client.py` first; read `client/rpc/*.proto` when the generated wrapper is not enough.
3. Keep the field name exactly as exposed by the client or proto-backed object.
4. If a field is not verified in source, do not access it.
5. Treat proto results as typed objects unless the source clearly shows a dict/list shape.
6. Printed protobuf output may omit empty / false fields; omission in `print(obj)` does not mean the field is unavailable.
7. Do not mix selector field names with `info()` field names.

| Wrong | Correct |
|-------|---------|
| `info.package_name` | `info.packageName` |
| `info.current_package_name` | `info.currentPackageName` |
| `result["stdout"]` | `result.stdout` |
| `app_info["packageName"]` | `app_info.packageName` |
| `d(resourceName="...")` | `d(resourceId="...")` |
| `info.resourceId` | `info.resourceName` |
| guessed snake_case / dict-style fields | source-verified proto/client fields only |

Before using fields from `info()`, `device_info()`, `server_info()`, `current_application()`, shell results, or selector metadata, verify the field names in source.

### Special boundaries

#### Watcher rules

Use watchers only when the task clearly benefits from automatic interruption handling or appearance counting.

Rules:

1. Register watchers near the start of the script, not midway through normal business logic.
2. Before a new run, clear old watcher state with `d.remove_all_watchers()` unless persistence is explicitly desired.
3. Registering a watcher is not enough: enable the watcher loop and then enable the watcher itself.
4. Too many watchers can affect performance; keep the set minimal and task-specific.
5. If a watcher can cause destructive navigation or clicks, state that risk in comments or surrounding logic.

Typical sequence:

```python
d.remove_all_watchers()
d.register_click_target_selector_watcher("AcceptAgreement", [Selector(textContains="User Agreement")], Selector(textContains="Accept", clickable=True))
d.set_watcher_loop_enabled(True)
d.set_watcher_enabled("AcceptAgreement", True)
```

#### User-control boundaries

If the target app blocks progress with a gate that normally requires user control, treat that as a handoff boundary unless the user explicitly asked for handling logic and the gate can be passed through normal visible UI without unstable hacks.

Examples include:

- forced update
- login
- OTP / SMS / email verification
- CAPTCHA
- biometric / passcode confirmation
- real-name verification / identity confirmation
- device-binding confirmation
- permission prompts that require deliberate user choice
- terms / policy gates that cannot be stably skipped

Rules:

1. First determine whether the gate is optional, skippable through normal UI, or mandatory.
2. If the gate is optional and the skip path is visible in normal UI, you may automate that normal skip path.
3. If the gate is mandatory and progress cannot continue without user participation, stop and return control to the user.
4. If you tried the normal visible path and the app still blocks progress, stop and return control to the user.
5. Do not invent brittle bypasses, hidden activities, package tampering, network blocking tricks, credential stuffing, token reuse, or reverse-engineering workarounds unless the user explicitly requested that class of work.
6. When returning control, say clearly which gate blocked progress and what the user needs to complete manually before automation can resume.

#### Authoring display and OCR policy

During script authoring and verification, always inspect and parse the UI from the default display (main screen). If the user wants final execution on a virtual display, apply that only in the delivered task script after selectors and flow have already been verified from the main screen.

Use standard UI selectors first. Only move to OCR or image matching when the app does not expose a usable Android View tree.

Rules:

1. Authoring-time inspection path: main-screen `dump` -> read `ui.xml` -> selector-based automation design.
2. Authoring-time screenshots and quick validation should also use the default display, not a virtual display.
3. If the user wants final execution on a virtual display, keep authoring-time selector discovery on the main screen and only wrap the final task logic with `create_virtual_display()`.
4. If the UI is custom-drawn, game-like, or `dump` is empty / insufficient, use main-screen screenshot + OCR or image matching for authoring-time analysis.
5. OCR selectors are limited; do not assume they support the full selector API.
6. In multi-device or clustered scenarios, prefer a custom HTTP OCR backend over loading heavy local OCR models in each process.
7. A virtual display instance `vd` is for final automation on that display. Global-effect operations must still use the original device instance `d`.
8. Watchers registered on `vd` affect that virtual display, not the main screen.
9. Do not create a separate virtual-display validation script unless the user explicitly asked for a dedicated virtual-display test.

When using a virtual display:

```python
base = Device("example.local")
with base.create_virtual_display() as vd:
    vd.application("com.example.app").start()
    vd(textContains="Target Action").click()
```

---

## All CLI commands

```bash
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] dump [-o FILE] [-z]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] screenshot [-o FILE] [-q N] [--left --top --right --bottom]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] app-start (-p PKG [-u USER] | -n NAME)
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] app-stop  (-p PKG [-u USER] | -n NAME)
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] app-list [-u USER]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] app-check (-p PKG | -n NAME) [-u USER] [--version VERSION]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] device-info
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] app-current
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] server-info
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] wake
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] sleep
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] press KEY_BACK|KEY_HOME|...
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] shell "command" [-t SEC]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] wait-idle [MS]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] wait-exists (--text T | --resource-id ID | ...) [--timeout MS]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] wait-gone (--text T | --resource-id ID | ...) [--timeout MS]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] selector-info (--text T | --resource-id ID | ...) [--timeout MS]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] get-text (--text T | --resource-id ID | ...) [--timeout MS]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] set-text (--text T | --resource-id ID | ...) --value TEXT [--timeout MS]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] clear-text (--text T | --resource-id ID | ...) [--timeout MS]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] tap-bounds-center (--text T | --resource-id ID | ...) [--timeout MS]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] assert-app-current --package PKG
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] click (--text T | --resource-id ID | ...) [--timeout MS]
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] exists  (--text T | --resource-id ID | ...)
python3 scripts/firerpa.py [--host HOST] [--port PORT] [--certificate FILE] scroll-to (--text T | ...) [--scrollable] [--horizontal]
```

Deps: `pip3 install -r requirements.txt`

Only `scripts/firerpa.py` — single self-contained CLI.

---

### Selectors from ui.xml

| XML | lamda |
|-----|-------|
| `resource-id` | `resourceId` |
| `content-desc` | `description` |
| `text` | `text` |
| `class` | `className` |

### API checks (`client/client.py`)

| Wrong | Correct |
|-------|---------|
| `el.input_text()` | `el.set_text()` |
| `el.clear_text()` | `el.clear_text_field()` |
| `app.clear_data()` | `app.reset()` |
| `d.shell()` | `d.execute_script("cmd")` |

### Pre-output checklist

- [ ] Selectors came from `ui.xml`, not guesswork
- [ ] A reusable automation script file was written to disk as the final deliverable
- [ ] The delivered automation script enables `d.set_debug_log_enabled(True)` near device initialization unless the user asked not to log
- [ ] Every non-trivial API name and field access was verified against local source
- [ ] The script, verification steps, and examples stayed anchored to the user-specified target app
- [ ] Element operations were preferred over key presses wherever a stable selector-driven path existed
- [ ] No ambiguous key press such as `ENTER` was used as a guessed submit action
- [ ] Any `press` step was followed by a visible state verification before continuing
- [ ] Target user app existence and requested version were verified before app-specific automation
- [ ] User-control gates were either handled through a normal visible path or handed back to the user
- [ ] Post-run verification checked both whether the action succeeded and whether the resulting state was reasonable
- [ ] Blocking conditions were reported clearly instead of triggering repeated validation loops
- [ ] No ad hoc inspection script or unrelated validation flow was added where `scripts/firerpa.py` already provides the needed path
- [ ] OCR / image matching was used only when selector-based automation was not sufficient
- [ ] Authoring-time UI parsing and validation used the main screen, even if the final script targets a virtual display
- [ ] Virtual-display code did not move global-effect operations from `d` to `vd`
- [ ] Debug / verification steps use `scripts/firerpa.py`, not inline inspection code

---

## Resources

- **CLI:** [scripts/firerpa.py](scripts/firerpa.py)
- **API:** [client/client.py](client/client.py)
- **Index:** [reference.md](references/reference.md)
