---
name: stata-ai-skill
version: v1.3
description: Run, configure, reset, or reconfigure Stata through the native Stata AI Skill background service at http://127.0.0.1:19522. Use when the user asks to run Stata commands, regressions, summarize data, t tests, hypothesis tests, do-files, .do scripts, .dta datasets, econometrics workflows, switch the configured Stata installation, redo Skill setup, clear Stata AI Skill configuration, or search Stata articles and cookbook-style resources with lianxh. No VS Code, Node.js, or Python runtime is required on the user side.
---

# Stata AI Skill

Requires Apple Silicon macOS or Windows, the native `stata-ai-skill`
executable, and a locally installed/licensed Stata. Intel Mac is not
supported. If automatic Stata discovery fails, use the agent-guided two-stage
`aiskill setup` fallback on the same localhost service port.

This native service is extracted from
[ZihaoVistonWang/stata-all-in-one](https://github.com/ZihaoVistonWang/stata-all-in-one)
and preserves the AI Skill HTTP workflow without requiring VS Code at runtime.

Use the native localhost service at `http://127.0.0.1:19522` to run Stata.
Do not import internal modules. The stable interface is HTTP.

## Locate The Executable

Agents must resolve the executable from this skill directory before using PATH
or build outputs. Do not require the user to know Cargo's `target/release`
directory.

Expected packaged layout:

```text
stata-ai-skill/
  SKILL.md
  bin/
    macos/
      stata-ai-skill            (legacy fallback)
    macos-arm64/
      stata-ai-skill            (Apple Silicon)
    windows/
      stata-ai-skill.exe          (x64)
    windows-arm64/
      stata-ai-skill.exe          (ARM64)
  scripts/
    discover_stata_windows.bat
  stata/
    aiskill/
      aiskill.ado
      aiskill.sthlp
      aiskill.pkg
      stata.toc
```

Resolution order:

1. If `STATA_AI_SKILL_BIN` is set, use that exact executable path.
2. macOS Apple Silicon: use `<this-skill-directory>/bin/macos-arm64/stata-ai-skill`.
3. macOS Intel (`x86_64`): stop and tell the user this skill does not support Intel Mac.
4. macOS Apple Silicon fallback: use `<this-skill-directory>/bin/macos/stata-ai-skill`.
5. Windows x64: use `<this-skill-directory>\bin\windows\stata-ai-skill.exe`.
6. Windows ARM64: use `<this-skill-directory>\bin\windows-arm64\stata-ai-skill.exe`.
7. Fallback only if packaged binary is missing on a supported platform: use `stata-ai-skill` from PATH.

To detect macOS architecture:

```bash
case "$(uname -m)" in
  arm64) exe="./bin/macos-arm64/stata-ai-skill" ;;
  x86_64)
    echo "Stata AI Skill does not support Intel Mac."
    exit 1
    ;;
  *) exe="./bin/macos/stata-ai-skill" ;;
esac
```

To detect Windows architecture from PowerShell:

```powershell
if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") {
    $exe = ".\bin\windows-arm64\stata-ai-skill.exe"
} else {
    $exe = ".\bin\windows\stata-ai-skill.exe"
}
```

For development builds, refresh the packaged executable with:

```bash
cargo run -p xtask -- dist
```

When writing commands below, replace `stata-ai-skill` with the resolved
executable path. Examples:

```bash
# macOS, from the skill directory
./bin/macos-arm64/stata-ai-skill serve
```

```powershell
# Windows, from the skill directory
.\bin\windows\stata-ai-skill.exe serve
```

## Agent Workflow

### Reset And Reconfigure

Interpret requests such as "reconfigure this Skill", "reset the Stata Skill",
"重新配置该技能", "重置 Stata 配置", "换一个 Stata", or "start setup
over" as an explicit request to delete the persisted Stata AI Skill
configuration and run setup again. The request itself authorizes this reset;
do not ask for another confirmation.

If the service is online, reset it in place:

```bash
curl -s -X POST http://127.0.0.1:19522/configure/reset
```

This removes the persisted config file and returns `restartRequired: true`.
Wait for the service to stop, then restart it with the resolved executable and
no `--stata-path` argument. Stopping the process safely closes the embedded
Stata session and clears install/setup tokens and phases. It does not uninstall
Stata, delete ado packages, or alter the Stata license.

If the service is offline, use the resolved executable and then start it:

```bash
stata-ai-skill config reset
stata-ai-skill serve
```

After restarting, read `/status` and follow the ordinary setup flow below. A
detected candidate must be shown to the user for explicit
selection even when there is only one; no candidate enters the manual two-stage
flow. If reset returns HTTP 409 because Stata is busy, wait for the current
execution to finish and retry once. Do not use `aiskill setup, force` as a
substitute because it leaves the old persisted selection in place.

1. Check whether the service is running:

```bash
curl -s --connect-timeout 2 http://127.0.0.1:19522/status 2>/dev/null || echo "OFFLINE"
```

2. If offline, start the native executable:

```bash
stata-ai-skill serve
```

Use the resolved executable path from "Locate The Executable"; the bare command
above is only shorthand. Run the service as a long-lived background process so
the agent can continue issuing HTTP requests. On macOS/zsh:

```bash
nohup ./bin/macos-arm64/stata-ai-skill serve > /tmp/stata-ai-skill.log 2>&1 &
```

If startup fails because the port is already in use, first recheck `/status`.
If another Stata AI Skill service is already responding, reuse it. Otherwise
choose another port and persist it:

```bash
./bin/macos-arm64/stata-ai-skill config set --port 19523
nohup ./bin/macos-arm64/stata-ai-skill serve > /tmp/stata-ai-skill.log 2>&1 &
curl -s http://127.0.0.1:19523/status
```

3. Read `setup.phase` before attempting execution. The setup states and required
agent actions are:

| `setup.phase` | Agent action |
|---|---|
| `selection_required` | Ask the user to choose a detected Stata installation, then call `/configure` |
| `manual_setup_required` | Immediately create an install session and give the user the generated `installation.do` command |
| `awaiting_install_result` | Wait for the user to run the first copied command; poll `/status` every two seconds in windows no longer than one minute |
| `awaiting_aiskill_setup` | Give the user the second command, `aiskill setup` |
| `configuring` | Continue polling until `ready` or `configuration_failed` |
| `install_failed` | Offer retry or skip; do not show `aiskill setup` |
| `configuration_failed` | Report `setup.lastResult`, license diagnostics, and offer retry |
| `ready` | Call `/execute` |

### Confirm An Automatically Detected Installation

`detectedCandidates` is sorted by newest Stata version, then MP, SE, BE, and
IC. Even when there is only one candidate, do not select it silently. Use the
host agent's best structured question tool to show the recommended candidate,
other candidates, and a manual-setup choice. If no structured question tool is
available, ask in chat and wait for an explicit reply.

If the user chooses manual setup, treat that selection as the complete choice:
call `POST /setup/install-session` immediately and show its returned command.
Do not ask a second question about installing `aiskill`.

After confirmation, configure and initialize through the already running
service; no restart is needed:

```bash
curl -s -X POST http://127.0.0.1:19522/configure \
  -H "Content-Type: application/json" \
  -d '{"stataPath":"/Applications/StataNow/StataMP.app"}'
```

Use the selected candidate's `path` exactly. A successful response returns the
updated status with `sessionActive: true` and `setup.phase: "ready"`.

### Manual Two-Stage `aiskill setup`

Use this when automatic discovery finds no candidates or the user explicitly
chooses manual setup. That choice already starts the manual workflow; do not
ask for a second installation confirmation. Immediately create an installation
session:

```bash
curl -s -X POST http://127.0.0.1:19522/setup/install-session
```

Copy or display the returned `command` exactly. It contains the absolute path
of the generated script, for example:

```stata
do "D:/path/to/the/system/temp/directory/installation.do"
```

Tell the user to run this command in the specific GUI Stata installation they
want the Skill to use. The command runs `net install` inside that Stata process,
so Stata itself selects the correct PERSONAL/PLUS ado directory for that user;
the agent and background service must not guess or write the ado path directly.

The 19522 service remains alive in `awaiting_install_result` and receives the
script's success or failure callback at `GET /installed`. Poll JSON `/status`
in the background; do not issue the second command until the phase becomes
`awaiting_aiskill_setup`. Then ask the user to run this in the same separately
opened GUI Stata:

```stata
aiskill setup
```

Never run `aiskill setup` through `/execute`. It obtains a one-time token from
`GET /status?format=stata`, reports the GUI Stata platform, version, edition,
machine type, and `c(sysdir_stata)` to `GET /setup`, and returns immediately.
Continue polling JSON `/status` until `ready` or `configuration_failed`.

Setup/install tokens are single-use and expire after ten minutes. Ordinary
JSON `/status` polling does not rotate or invalidate the Stata setup token.

4. If `/status` returns `sessionActive: true` and `setup.phase: "ready"`, call
`/execute`.

`/status` includes diagnostic fields agents should use for troubleshooting:

- `config.port`
- `config.stataPath`
- `config.configFile`
- `config.logDir`
- `config.tempDir`
- `config.graphDir`
- `capabilities.cwd`
- `capabilities.timeoutMaxSeconds`

If `/status` returns `needsLicense: true` or `missing: "stata_license"`, Stata
was found but the license file was not found. Tell the user:

"Stata is installed, but the service cannot find the Stata license file
`stata.lic` / `STATA.lic`. Please open Stata once to confirm it is licensed, or
check that the license file exists in the Stata installation folder."

Common license locations:

- macOS: `/Applications/StataNow/stata.lic`
- Windows: `C:\Program Files\Stata18\STATA.lic`

## Execute

### Read Command Help First

Before using a specific Stata command, first run `help <command>` through
`/execute` and read its documentation. Confirm the command syntax, options, and
version-specific behavior before composing the final analysis command. For
example, run `help regress` before using `regress`.

If Stata reports that the help file or command is unavailable, do not guess its
syntax. Report the missing command and request approval before installing any
community-contributed package.

### Run Existing Do-Files Directly

When the user provides an existing `.do` file, pass its path in the `file`
field. Prefer this over copying the file, reading it with Python or shell
commands, or sending its contents through `code`.

- Use `file` for an existing `.do` file and `code` for inline Stata commands.
- Use an absolute `file` path whenever possible. Paths containing spaces are
  supported; JSON-encode the path normally and do not copy it to `/tmp`.
- Set `cwd` to the do-file's project directory when it uses relative paths for
  datasets, included do-files, logs, or generated output.
- The file must be accessible to the local Stata AI Skill service process.
- Do not send both `file` and `code`; if both are present, `file` takes
  precedence.

#### macOS And Linux

Use `curl` from bash or zsh:

```bash
curl -s -X POST http://127.0.0.1:19522/execute \
  -H "Content-Type: application/json" \
  -d '{"file":"/Users/me/project/analysis.do","cwd":"/Users/me/project","timeout":120}'
```

#### Windows Command Prompt

Windows supports both Command Prompt (`cmd.exe`) and PowerShell; PowerShell is
not required. From Command Prompt, escape the JSON double quotes:

```cmd
curl.exe -s -X POST http://127.0.0.1:19522/execute -H "Content-Type: application/json" -d "{\"file\":\"C:\\Users\\me\\project\\analysis.do\",\"cwd\":\"C:\\Users\\me\\project\",\"timeout\":120}"
```

#### Windows PowerShell

Write the request JSON, not the do-file, to a temporary UTF-8 file without a
BOM, then send it with `curl.exe`:

```powershell
$body = '{"file":"C:\\Users\\me\\project\\analysis.do","cwd":"C:\\Users\\me\\project","timeout":120}'
[System.IO.File]::WriteAllText("$env:TEMP\stata_body.json", $body, [System.Text.UTF8Encoding]::new($false))
curl.exe -s -X POST http://127.0.0.1:19522/execute `
  -H "Content-Type: application/json" `
  --data-binary "@$env:TEMP\stata_body.json"
```

In all three cases, the service executes the do-file directly and applies `cwd`
before the `do` command.

For additional PowerShell quoting, UTF-8 BOM, and multiline JSON guidance, read
[`references/windows-powershell-http.md`](references/windows-powershell-http.md)
when the active shell is Windows PowerShell.

Response:

```json
{
  "success": true,
  "returnCode": 0,
  "output": "4",
  "error": "",
  "graphs": []
}
```

For long commands, set `timeout` in seconds:

```bash
curl -s -X POST http://127.0.0.1:19522/execute \
  -H "Content-Type: application/json" \
  -d '{"code":"bootstrap r(mean), reps(1000): summarize price", "timeout": 300}'
```

For workflows that use relative paths, set `cwd`. The service prepends a Stata
`cd` command before running inline code or a do-file:

```bash
curl -s -X POST http://127.0.0.1:19522/execute \
  -H "Content-Type: application/json" \
  -d '{"cwd":"/Users/me/project","code":"use data/auto.dta, clear\nsummarize"}'
```

### Timeout Recovery

A timeout returns HTTP 408 and sends a Stata break signal. If the response says
`Stata is still stopping`, `/status.busy` deliberately remains `true`; do not
send another execution until it becomes `false`. Send `/break` again if needed,
or call `/shutdown` and restart the service if Stata never finishes stopping.

### Graph Export

The standalone service enables Stata graph capture with `quietly _gr_list on`
after session initialization. It recognizes `graph export` at its original
position, including leading `.`, `quietly`/`qui`, `capture`/`cap`, and
`noisily`/`noi` prefixes. It preserves `replace` and `name(...)`; bitmap
`width(...)` and `height(...)` control the Rust-rendered output dimensions.

Explicit SVG exports are executed safely and returned in the response
`graphs` array:

```json
[{ "name": "Graph", "svg": "/absolute/path/to/foo.svg", "png": null }]
```

PNG/JPG/JPEG exports are supported without asking Stata to write those formats
directly. At the same point in the user's code, the service exports SVG first,
then converts it with bundled Rust libraries, keeps the SVG path, and writes
the requested bitmap path. For PNG requests, the `png` field contains the
generated PNG path. For JPG/JPEG
requests, `png` remains `null` and the graph object includes `file` and
`format` fields for the generated bitmap. Other unsafe bitmap formats such as
TIF and TIFF are still rewritten to SVG and reported in `output`.

If user code does not contain an explicit `graph export`, successful executions
keep the automatic `_gr_list` SVG export behavior and return generated SVG
paths under `graphs`.

## Lianxh Search

When the user asks for Stata cookbook examples, command tutorials, or Lianxh
articles, read and follow
[`references/lianxh-search.md`](references/lianxh-search.md). It contains the
installation-consent boundary, three-query limit, search syntax, and timeout
recovery workflow.

## Break And Shutdown

Interrupt the current Stata execution:

```bash
curl -s -X POST http://127.0.0.1:19522/break
```

Close the background service:

```bash
curl -s -X POST http://127.0.0.1:19522/shutdown
```

## Files

The service uses system directories only. It does not create `.stata-all-in-one/`
in the current repository or working directory. Temporary `.do` files are unique
and deleted after execution. Graphs are first exported as SVG and returned as
absolute paths in `graphs`; explicit PNG/JPG/JPEG requests are converted from
that SVG without requiring a system image converter.
