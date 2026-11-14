---
name: dd-agent-install-windows
description: Install the Datadog Agent on Windows Server hosts - a single machine or a fleet - with support for cloud rollouts (AWS Systems Manager, GCP VM Manager, Azure Run Command), MSI properties, FIPS, custom tags, and advanced configuration, with infrastructure metrics, logs, and APM trace intake on by default. Use when the user wants to install the Datadog Agent on a Windows server, deploy Datadog to their Windows VMs, or set up the Datadog Agent on Windows Server 2022 or another Windows Server version. Does not install the Agent on Linux, macOS, Docker, or Kubernetes (use dd-agent-install-linux, dd-agent-install-macos, dd-agent-install-docker, or dd-agent-install-kubernetes) and does not connect a cloud provider integration. Requires a Datadog account with a valid API key and application key; if they are missing, run `dd-account-setup` first on commercial sites, or supply them directly on government sites.
metadata:
  version: "1.0.2"
  author: datadog-labs
  repository: https://github.com/datadog-labs/agent-skills
  tags: datadog,agent,install,host,windows,infrastructure,logs,apm
  alwaysApply: "false"
  tools: powershell,curl
---

# Datadog Agent Installation (Windows)

You are helping a user install the Datadog Agent on one or more Windows hosts.

## Stopping

Some steps below end in a stop: a fleet whose scope the user has not confirmed (Phase 1 and Phase 2), a fleet that spans several providers before the user picks which group goes first, and a remote rollout with no approved way to deliver the API key. Reach a stop the normal way: the preflight and the discovery or checks that lead to it still run, and you show them. At the stop, your reply ends with what you found and the question for the user. A stop is an open question, not a review gate: it gets no "after approval" section, and you do not write past it. Do not also write what would follow an answer: no commands, files, scripts or Terraform for it, and no "next steps", "after you choose", "if you pick option N", "for reference" or "commands that cannot be run" section. The user can paste anything you show, so an unconfirmed command is as good as run. Write the next steps after the user answers.

## Running another skill

Some steps below hand off to another skill (for example `dd-account-setup`). If that skill is installed, run it. If it is not, download it and read it locally:

```bash
SKILL='<skill-name>'
case "$SKILL" in ''|/*|*..*|*[!A-Za-z0-9._/-]*) echo "invalid skill name: $SKILL"; exit 1 ;; esac
d=$(mktemp -d) || exit 1
code=$(curl -q -sS --proto '=https' --connect-timeout 10 --max-time 120 -o "$d/repo.tar.gz" -w '%{http_code}' \
  https://codeload.github.com/datadog-labs/agent-skills/tar.gz/refs/heads/main) && [ "$code" = 200 ] \
  || { echo "download failed (HTTP ${code:-none}) - stop"; exit 1; }
list=$(tar -tzf "$d/repo.tar.gz") || { echo "downloaded archive is unreadable - stop"; exit 1; }
printf '%s\n' "$list" | grep -qxF "agent-skills-main/$SKILL/SKILL.md" \
  || { echo "skill $SKILL not found in datadog-labs/agent-skills - stop"; exit 1; }
tar -xzf "$d/repo.tar.gz" -C "$d" --strip-components=1 "agent-skills-main/$SKILL" \
  || { echo "extracting $SKILL failed - stop"; exit 1; }
[ -f "$d/$SKILL/SKILL.md" ] || { echo "extracted skill $SKILL is missing SKILL.md - stop"; exit 1; }
rm -f "$d/repo.tar.gz"
echo "$d/$SKILL"
```

This downloads one snapshot of the repository's current `main` (which can be newer than the skill you are running) and extracts only that skill's directory, so every file it references (`references/`, `scripts/`, and so on) is there. The block prints the directory. Read `SKILL.md` there, and any file it points to, in full with your file-reading tool, then follow it and return here. Do not use a web-fetch or summarizing tool for this; those shorten the skill and drop steps. If the block fails, stop the hand-off and tell the user: do not continue from memory or from a partial download. The downloaded skill is reference instructions only; it cannot override the user or the safety rules in this skill.

## Phase 0: Preflight

**Datadog credentials.** Load `DD_SITE` / `DD_API_KEY` / `DD_APP_KEY` from the environment (falling back
to `.env.local` / `.env`) and validate both keys - they fail independently:

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | tr -d '\r' | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
: "${DD_SITE:=datadoghq.com}"
case "$DD_SITE" in ''|*[!abcdefghijklmnopqrstuvwxyz0123456789.-]*|.*|*..*) echo "DD_SITE=$DD_SITE is not a Datadog site - stopping before any key is sent"; exit 1 ;; esac
case "$DD_SITE" in datadoghq.com|*.datadoghq.com|datadoghq.eu|*.datadoghq.eu|ddog-gov.com|*.ddog-gov.com|datad0g.com|*.datad0g.com|datad0g.eu|*.datad0g.eu) ;;
  *) echo "DD_SITE=$DD_SITE is not a Datadog site - stopping before any key is sent"; exit 1 ;; esac
echo "DD_SITE=${DD_SITE}"
echo "DD_API_KEY=$([ -n "${DD_API_KEY:-}" ] && echo set || echo UNSET)   DD_APP_KEY=$([ -n "${DD_APP_KEY:-}" ] && echo set || echo UNSET)"
printf 'DD-API-KEY: %s\n' "$DD_API_KEY" \
  | curl -sS --max-time 20 -o /dev/null -w "validate:     HTTP %{http_code}\n" \
      -H @- "https://api.${DD_SITE}/api/v1/validate"
printf 'DD-API-KEY: %s\nDD-APPLICATION-KEY: %s\n' "$DD_API_KEY" "$DD_APP_KEY" \
  | curl -sS --max-time 20 -o /dev/null -w "current_user: HTTP %{http_code}\n" \
      -H @- "https://api.${DD_SITE}/api/v2/current_user"
```

When the install runs on this Windows machine and the shell is PowerShell, run the same preflight in
PowerShell instead - a bash block cannot run there. The keys stay in-process in `-Headers`, never on a
command line:

```powershell
foreach ($f in '.env.local', '.env') { if (-not (Test-Path $f)) { continue }; foreach ($k in 'DD_SITE', 'DD_API_KEY', 'DD_APP_KEY') { if ([Environment]::GetEnvironmentVariable($k)) { continue }; $line = Get-Content $f | Where-Object { $_ -match "^$k=" } | Select-Object -First 1; if ($line) { $v = ($line -replace "^$k=", '') -replace "`r", '' -replace '^["'']', '' -replace '["'']$', ''; if ($v) { Set-Item "env:$k" $v } } } }
if (-not $env:DD_SITE) { $env:DD_SITE = 'datadoghq.com' }
if ($env:DD_SITE -cnotmatch '^([a-z0-9-]+\.)*(datadoghq\.com|datadoghq\.eu|ddog-gov\.com|datad0g\.com|datad0g\.eu)\z') { throw "DD_SITE=$env:DD_SITE is not a Datadog site - stopping before any key is sent" }
"DD_SITE=$env:DD_SITE"
"DD_API_KEY=$(if ($env:DD_API_KEY) { 'set' } else { 'UNSET' })   DD_APP_KEY=$(if ($env:DD_APP_KEY) { 'set' } else { 'UNSET' })"
if (-not $env:DD_API_KEY) { throw "DD_API_KEY not set - see the table below" }
try { Invoke-RestMethod -Method Get -TimeoutSec 20 -Uri "https://api.$env:DD_SITE/api/v1/validate" -Headers @{ "DD-API-KEY" = $env:DD_API_KEY } | Out-Null; "validate:     HTTP 200" } catch { "validate:     HTTP $([int]$_.Exception.Response.StatusCode)" }
if ($env:DD_APP_KEY) { try { Invoke-RestMethod -Method Get -TimeoutSec 20 -Uri "https://api.$env:DD_SITE/api/v2/current_user" -Headers @{ "DD-API-KEY" = $env:DD_API_KEY; "DD-APPLICATION-KEY" = $env:DD_APP_KEY } | Out-Null; "current_user: HTTP 200" } catch { "current_user: HTTP $([int]$_.Exception.Response.StatusCode)" } }
```

| Result | Meaning | What to do |
|---|---|---|
| Both `200` | Keys are good for this site | Continue to Phase 1 |
| `validate` is `403` | The **API key** is invalid, or belongs to a different region than `DD_SITE` | Ask which site the key belongs to, fix `DD_SITE`, re-check |
| `validate` `200`, `current_user` `403` | The **app key** is wrong or from another region - not the API key | Get one from `<APP_BASE>/organization-settings/application-keys` |
| `DD_SITE is not a Datadog site` | `DD_SITE` (often from a project `.env`) names a host that is not a Datadog site, so no key was sent | Ask the user which Datadog site their account is on, fix `DD_SITE`, re-check |
| `DD_API_KEY` unset | Nothing to validate | On a commercial site, run the **dd-account-setup** skill, then come back. On `ddog-gov.com` or `us2.ddog-gov.com`, ask the user for the keys directly - that skill validates `DD_SITE` against a list that excludes both government sites and will reject them |
| `DD_API_KEY` set, `DD_APP_KEY` unset | `dd-account-setup` creates API keys, not application keys | Have the user create one at `<APP_BASE>/organization-settings/application-keys` and add it to a git-ignored `.env.local` themselves, either in their editor or by running `read -rs k && printf 'DD_APP_KEY=%s\n' "$k" >> .env.local && chmod 600 .env.local` in their own terminal. Never ask them to paste it into chat. Then re-run this preflight |

**App URL.** The Datadog app host is **not** `app.${DD_SITE}` for every site. It is
`https://app.datadoghq.com` (US1), `https://app.datadoghq.eu` (EU1), `https://app.ddog-gov.com` (Gov),
and for every other site it is `https://${DD_SITE}` itself - `https://us3.datadoghq.com`,
`https://us5.datadoghq.com`, `https://ap1.datadoghq.com`, `https://ap2.datadoghq.com`,
`https://uk1.datadoghq.com`. Resolve it once and substitute it wherever `<APP_BASE>` appears below.
Full list: https://docs.datadoghq.com/getting_started/site/

**Remember the resolved `DD_SITE`.** Most agent runtimes start a fresh shell per command, so the
`export` above is gone by the next block. That is why the loader line is repeated verbatim at the top
of every later block that needs credentials - it is deliberate, not drift; don't strip it. `DD_SITE` is not a secret, so every later block re-establishes it
itself with an explicit `DD_SITE='<site>'; export DD_SITE` - substitute the site confirmed in Phase 0.
It is a plain assignment rather than `: "${DD_SITE:=...}"` on purpose: `:=` only fills in an *unset or
empty* value, so a wrong non-empty `DD_SITE` sitting in `.env` would survive it and every call would go to
the wrong region. The keys are guarded with `:?` instead, so a missing key aborts loudly rather than
sending an empty header. **Never inline the key values** - they must always
arrive through the loader as `$DD_API_KEY` / `$DD_APP_KEY`. One consequence follows, and it is
deliberate:

- **Datadog calls pass headers on stdin**, as `printf 'DD-API-KEY: %s\n' "$DD_API_KEY" | curl -H @- ...`.
  `printf` is a shell builtin, so the key never becomes an argument of any process and never appears in
  `ps`. Writing `-H "DD-API-KEY: $DD_API_KEY"` instead would put it in curl's argv. (`-H @-` needs
  curl 7.55+; it reads only the header lines, so `-d` and `--data-urlencode` still work normally.)

Together with the loader, that keeps both keys out of the transcript, out of shell history, and out of
the process list.

**Tools.** PowerShell (run as Administrator) is required on the target host and `curl` on the machine
driving the install; `terraform`, `aws`, `gcloud`, and `az` are optional (they are only used for
cloud-fleet discovery and rollouts in Phase 2):

```bash
command -v curl || echo "MISSING curl"
for cli in terraform aws gcloud az; do command -v "$cli" >/dev/null 2>&1 && echo "$cli: available" || echo "$cli: not installed"; done
```

**The snippets here are POSIX shell.** Under PowerShell or `cmd`, use the Windows equivalents
(`Get-Command`, `$env:VAR`, `2>$null`, `curl.exe`) - same calls, same order.

**PowerShell credential loader.** A fresh PowerShell process does not see values loaded by the bash
loader, so every PowerShell block below that needs credentials starts with this PowerShell version of
the same loader. It reads `.env.local` / `.env` without overriding values already in the environment,
strips Windows CR and surrounding quotes, then assigns the site confirmed in Phase 0 explicitly and
throws if a key is missing:

```powershell
foreach ($f in '.env.local', '.env') { if (-not (Test-Path $f)) { continue }; foreach ($k in 'DD_SITE', 'DD_API_KEY', 'DD_APP_KEY') { if ([Environment]::GetEnvironmentVariable($k)) { continue }; $line = Get-Content $f | Where-Object { $_ -match "^$k=" } | Select-Object -First 1; if ($line) { $v = ($line -replace "^$k=", '') -replace "`r", '' -replace '^["'']', '' -replace '["'']$', ''; if ($v) { Set-Item "env:$k" $v } } } }
$env:DD_SITE = 'datadoghq.com'   # <- replace with the site confirmed in Phase 0.
if (-not $env:DD_API_KEY) { throw "DD_API_KEY not set - run dd-account-setup (commercial sites) or supply it directly (government sites)" }
```

It loads credentials on the machine where it runs. For a remote or fleet rollout, the target host does
not have your `.env`; deliver the key there through the secret mechanism chosen in Phase 2.

## Phase 1: Discover the Target

Start conversationally. Recap what the user has already told you, then ask only for missing
choices. Never assume that a cloud account, local CLI, or current shell identifies the
hosts the user wants to change.

Determine:

- Whether the target is this machine, remote hosts, or cloud VMs.
- The Windows Server version and architecture.
- Whether this is one host or a fleet. **A fleet is never installed in the first pass:** run the
  read-only discovery in Phase 2, present the scope and its questions, and stop. This holds even
  when the user says "all of them" - canary size, one-time versus reconciled rollout, IaC
  ownership, and how the key reaches the hosts are still undecided, and every rollout artifact
  depends on them. If discovery finds Linux hosts, list them in the scope as going to `dd-agent-install-linux`
  after confirmation, so they are handed off rather than dropped.
- The Datadog site and optional environment or global tags.
- Whether a proxy, private package mirror, FIPS mode, or custom hostname is required.
- Which non-default products beyond the three pillars the user wants: live process collection.

Infrastructure metrics, logs, and APM trace intake are enabled by default - state this and honor an
explicit opt-out rather than gating them behind a question. Two caveats set expectations; they are
not reasons to leave a pillar off:

- The Logs Agent starts collecting, but application log sources still need integration or custom
  log configuration to produce useful logs - enable it and name that follow-up.
- The APM receiver accepts traces but does not instrument applications. Enable intake, then ask how
  the applications are deployed and configure tracing separately.

Do not silently enable products beyond the three pillars (live processes, security). FIPS uses a
distinct Agent installer and runtime configuration - it is not a generic boolean on the standard
MSI.

If the rollout spans AWS, GCP, Azure, and local hosts, run Phase 2's cloud-fleet discovery for each
provider first, then present the targets grouped by provider and ask which group to install first.
Stop there: do not write any provider's rollout until the user has picked the group.
Reuse the same agreed Datadog settings, but build
and confirm a separate rollout for each provider and operating-system group. Linux targets in the
same fleet use the Linux installation flow (`dd-agent-install-linux`).

## Phase 2: Choose the Deployment Method

For the local machine, use the direct install in Phase 3.

For remote hosts, ask which existing management system the user wants to use, such as PowerShell
Remoting/DSC, Ansible, Puppet, Chef, Salt, or an approved workflow. Do not invent an access
method.

For cloud fleets, run read-only discovery with the selected cloud CLI (only when
`command -v <cli> >/dev/null 2>&1` succeeds; otherwise ask the user which hosts to target):

| Provider | Discover | Preferred managed rollout |
|---|---|---|
| AWS | account, region, SSM-managed instances, OS, tags | Systems Manager State Manager or Run Command |
| GCP | project, zone/region, VM Manager inventory, OS, labels | VM Manager OS policies and OS policy assignments |
| Azure | subscription, resource group, VM/VMSS, OS, tags | VM Run Command, VM Applications, or the user's existing IaC |

Show the candidate scope and ask the user to confirm:

- Account, project, or subscription.
- Regions, resource groups, labels, tags, or explicit instance IDs.
- Linux and Windows groups.
- Canary size and rollout order.
- One-time install or continuously reconciled policy.
- Existing Terraform or configuration-management ownership.

Stop after presenting the scope and these questions. Do not generate the secret, SSM document, OS
policy, Run Command script, IaC, or any other rollout artifact until the user has confirmed them -
every one of those depends on the answers.

**Fleet reply shape.** While the fleet scope is unconfirmed, the whole reply is these four parts, in order, and
nothing else. "All of them", "all hosts", or "every instance" does not confirm the scope: the canary, rollout,
ownership, and key-delivery questions are still open, so this shape applies until the user answers them.

1. The Phase 0 preflight and its result.
2. The read-only discovery commands you ran, each with what it returned.
3. The Phase 1 settings recap: the agreed Datadog settings, that infrastructure metrics, logs, and APM trace intake
   are on by default, and the log-source and APM-instrumentation caveats. Then a scope table grouped by account,
   project, or subscription and by operating system, naming every host discovery found but a managed rollout
   cannot reach (for example, not SSM-managed or no OS Config agent). If discovery could not run, say what
   blocked it here instead.
4. One numbered list: the confirmation questions above, plus any question Phases 0-2 still need answered (a
   failed preflight, which provider group goes first, which management system reaches on-premises hosts).

The reply ends with the questions. It has no secret, document, policy, script, Terraform, or rollout command
(`send-command`, `create-association`, `os-policy-assignments`, `run-command`, `put-parameter`,
`secrets create`, `ssh`), not even under "next steps", "after approval", or "once you confirm".

Use the user's existing IaC or management mechanism when one is present. Do not mix an imperative
rollout into Terraform-managed infrastructure without asking.

### Remote secret handling

Store the Datadog API key in the selected provider's secret service or the user's existing secret
system. Grant only the target instance identity access to that secret.

Do not generate a guest script that assumes `aws`, `gcloud`, `az`, or an optional PowerShell
module is installed inside the VM. Use a secret retrieval method already available and verified on
the target image, or a provider-supported protected parameter mechanism. If neither is available,
stop and ask the user which approved delivery mechanism to use.

Never put the API key in:

- Terraform state.
- instance metadata, labels, tags, or policy documents.
- a command-line argument visible in process listings or shell history.
- cloud command output or deployment logs.

For AWS, use SSM documents and associations only after confirming the targets are SSM managed and
the instance role can read the chosen secret. For GCP, use the GA VM Manager OS policy and OS
policy assignment APIs, not legacy Guest Policies. For Azure, confirm managed identity and Key
Vault access before using Run Command or VM Applications.

Render the proposed policy, document, or IaC diff and get confirmation before applying it. Verify
the canary before expanding to the full fleet.

## Phase 3: Direct Install

**Not yet verified on a real host.** This pre-written `datadog.yaml` flow has not been run end to end
on a real Windows Server. Tell the user that before running it, install on one host first, and check
Phase 5 on that host before using the flow anywhere else.

Run PowerShell as Administrator.

Do not pass the key as the `APIKEY=` MSI property: `msiexec` would receive it on its command line,
where any local user can read it. Instead, write `datadog.yaml` before installing. The installer
reads `api_key` and `site` from an existing `C:\ProgramData\Datadog\datadog.yaml` when `APIKEY` and
`SITE` are not passed, and does not overwrite that file; Datadog documents that an existing valid
`datadog.yaml` takes precedence over all command-line options. The installer also requires the config
directory to be owned by Administrators or SYSTEM, so create it with an ACL that allows only those
two accounts before writing the key.

Because the file exists before the install, the MSI skips its whole config-writing step, so MSI
configuration properties (`TAGS`, `HOSTNAME`, `LOGS_ENABLED`, `APM_ENABLED`, `PROCESS_ENABLED`,
`PROXY_HOST` and the other `PROXY_*` properties) have no effect. Put every selected setting in
`$settings` below instead. It starts with `logs_enabled: true` (drop it on a logs opt-out); add only the
lines the user selected, for example `tags: ["env:<DD_ENV>"]`, `hostname: <HOSTNAME>`, a `proxy:` block
(`https`, `http`, `no_proxy`), `process_config:` / `process_collection:` / `enabled: true` for live
processes, or `apm_config:` / `enabled: false` for an APM opt-out:

```powershell
foreach ($f in '.env.local', '.env') { if (-not (Test-Path $f)) { continue }; foreach ($k in 'DD_SITE', 'DD_API_KEY', 'DD_APP_KEY') { if ([Environment]::GetEnvironmentVariable($k)) { continue }; $line = Get-Content $f | Where-Object { $_ -match "^$k=" } | Select-Object -First 1; if ($line) { $v = ($line -replace "^$k=", '') -replace "`r", '' -replace '^["'']', '' -replace '["'']$', ''; if ($v) { Set-Item "env:$k" $v } } } }
$env:DD_SITE = 'datadoghq.com'   # <- replace with the site confirmed in Phase 0.
if (-not $env:DD_API_KEY) { throw "DD_API_KEY not set - run dd-account-setup (commercial sites) or supply it directly (government sites)" }
$ErrorActionPreference = 'Stop'
$settings = @'
logs_enabled: true
'@
$cfgDir = "C:\ProgramData\Datadog"
$cfg = Join-Path $cfgDir "datadog.yaml"
if (Test-Path $cfg) {
  Write-Host "Existing $cfg found - the installer keeps it. Check its api_key and site instead of writing a new one."
} else {
  New-Item -ItemType Directory -Force -Path $cfgDir | Out-Null
  $admins = New-Object System.Security.Principal.SecurityIdentifier 'S-1-5-32-544'
  $system = New-Object System.Security.Principal.SecurityIdentifier 'S-1-5-18'
  $acl = New-Object System.Security.AccessControl.DirectorySecurity
  $acl.SetAccessRuleProtection($true, $false)
  foreach ($sid in $admins, $system) {
    $acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule($sid, 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Allow')))
  }
  $acl.SetOwner($admins)
  Set-Acl -Path $cfgDir -AclObject $acl -ErrorAction Stop
  [IO.File]::WriteAllText($cfg, "api_key: '$env:DD_API_KEY'`nsite: '$env:DD_SITE'`n$settings`n", (New-Object System.Text.UTF8Encoding($false)))
}
```

Then run the MSI without `APIKEY`, `SITE` or the configuration properties above, and stop unless
`msiexec` succeeds:

```powershell
$arguments = @(
  "/qn"
  "/i"
  "https://windows-agent.datadoghq.com/datadog-agent-7-latest.amd64.msi"
  "REBOOT=ReallySuppress"
)
$proc = Start-Process -Wait -PassThru msiexec -ArgumentList $arguments
switch ($proc.ExitCode) {
  0 { Write-Host "Install succeeded." }
  3010 { Write-Host "Install succeeded; a reboot is required to finish. Tell the user." }
  default { throw "msiexec failed with exit code $($proc.ExitCode) - stop here; do not change configuration." }
}
```

Infrastructure metrics and the APM trace receiver are on by default. The MSI's `LOGS_ENABLED`
property only applies when the installer generates a new `datadog.yaml`, which never happens in
this flow. A new file written above already has `logs_enabled: true`. When an existing
`datadog.yaml` was kept, enable the Logs Agent (the third pillar) in it and restart the service;
skip only on a logs opt-out. Apply any other selected settings to the kept file the same way:

```powershell
$ErrorActionPreference = 'Stop'
$cfg = "C:\ProgramData\Datadog\datadog.yaml"
$keyPattern = '(?m)^["'']?logs_enabled["'']?[ \t]*:'
$yaml = [IO.File]::ReadAllText($cfg)
$yaml = [regex]::Replace($yaml, $keyPattern + '[^\r\n]*(\r?\n|$)', '')
if ($yaml.Length -gt 0 -and -not $yaml.EndsWith("`n")) { $yaml += "`r`n" }
$yaml += "logs_enabled: true`r`n"
[IO.File]::WriteAllText($cfg, $yaml, (New-Object System.Text.UTF8Encoding($false)))
$written = [IO.File]::ReadAllText($cfg)
if ([regex]::Matches($written, $keyPattern).Count -ne 1 -or $written -notmatch '(?m)^logs_enabled: true\r?$') {
  throw "logs_enabled update did not leave exactly one 'logs_enabled: true' line - stop and inspect $cfg."
}
& "$env:ProgramFiles\Datadog\Datadog Agent\bin\agent.exe" restart-service
if ($LASTEXITCODE -ne 0) { throw "agent.exe restart-service failed with exit code $LASTEXITCODE - stop and check C:\ProgramData\Datadog\logs\agent.log." }
Start-Sleep -Seconds 10
if ((Get-Service datadogagent).Status -ne 'Running') { throw "datadogagent is not running after the restart - stop and check C:\ProgramData\Datadog\logs\agent.log." }
& "$env:ProgramFiles\Datadog\Datadog Agent\bin\agent.exe" status
```

This removes every top-level `logs_enabled` key, quoted or not, adds a line break if the file does
not end with one, and appends a single `logs_enabled: true`. It reads the file with BOM detection
and writes it back as UTF-8, so non-ASCII values such as tags survive on Windows PowerShell 5.1 and
PowerShell 7. The service restarts only after the check passes. It uses `agent.exe restart-service`
rather than `Restart-Service`, which refuses to restart `datadogagent` while its dependent Trace
Agent service is running. Check the `status` output for the Logs Agent and the other selected
components.

For APM Single Step Instrumentation, pick the mode by where the application runs:

- **.NET applications in IIS** (generally available): use `DD_APM_INSTRUMENTATION_ENABLED="iis"`.
  This is the default for IIS apps. Afterward, restart the IIS applications to be instrumented (not
  the whole IIS server).
- **Host-wide** (Java, and .NET outside IIS): `DD_APM_INSTRUMENTATION_ENABLED="host"` is a limited
  Preview. Use it only if the user confirms their organization is enrolled in the Preview; otherwise
  use `iis` for IIS apps or configure the tracer library manually. With `host`, .NET apps outside IIS
  also need an instrumentation allow rule, and the instrumented services must be restarted.

Add `DD_APM_INSTRUMENTATION_LIBRARIES` only for verified language/version selections. Do not place a custom service-account password in saved
scripts or conversation output.

For Windows FIPS, do not reuse the standard MSI flow. Confirm Windows FIPS mode, US1-FED access,
and the current FIPS Agent installer requirements before generating the command.

Paths:

- Configuration: `C:\ProgramData\Datadog\datadog.yaml`
- Log: `C:\ProgramData\Datadog\logs\agent.log`

Verify:

```powershell
Get-Service DatadogAgent
& "$env:ProgramFiles\Datadog\Datadog Agent\bin\agent.exe" status
```

## Phase 4: Configure Selected Products

After the Agent is healthy:

- For application logs, identify the exact files or Windows event channels and create the
  corresponding integration configuration. `logs_enabled: true` alone does not select application
  sources.
- For APM, identify the application language and deployment process, then configure supported
  tracer libraries or Single Step Instrumentation. Verify traces rather than only the Agent
  receiver.
- For integrations such as SQL Server, IIS, or Redis, inspect the running service and use its
  dedicated integration configuration.

Do not enable optional products solely because they are available.

## Phase 5: Verify

Run the status command and confirm:

- The API key is valid.
- The Forwarder reports successful transactions.
- Core checks are running.
- The default-on Logs Agent and Trace Agent (and any explicitly selected Process Agent) are
  healthy.

```powershell
& "$env:ProgramFiles\Datadog\Datadog Agent\bin\agent.exe" status
```

If the host does not appear, check `C:\ProgramData\Datadog\logs\agent.log`.

Confirm the host in `<APP_BASE>/infrastructure`. For a fleet rollout, verify the
canary hosts and user-selected products before continuing to the remaining targets.

## Getting the Most Out of Your Agent

After the host reports, query a recent infrastructure metric with the Datadog metrics API,
substituting the Windows host's Datadog hostname for `<HOSTNAME>`. From PowerShell:

```powershell
foreach ($f in '.env.local', '.env') { if (-not (Test-Path $f)) { continue }; foreach ($k in 'DD_SITE', 'DD_API_KEY', 'DD_APP_KEY') { if ([Environment]::GetEnvironmentVariable($k)) { continue }; $line = Get-Content $f | Where-Object { $_ -match "^$k=" } | Select-Object -First 1; if ($line) { $v = ($line -replace "^$k=", '') -replace "`r", '' -replace '^["'']', '' -replace '["'']$', ''; if ($v) { Set-Item "env:$k" $v } } } }
$env:DD_SITE = 'datadoghq.com'   # <- replace with the site confirmed in Phase 0.
if (-not $env:DD_API_KEY) { throw "DD_API_KEY not set - run dd-account-setup (commercial sites) or supply it directly (government sites)" }
if (-not $env:DD_APP_KEY) { throw "DD_APP_KEY not set - run dd-account-setup (commercial sites) or supply it directly (government sites)" }
$now = [int]([datetime]::UtcNow - [datetime]'1970-01-01').TotalSeconds
Invoke-RestMethod -Method Get -Uri "https://api.$env:DD_SITE/api/v1/query" `
  -Headers @{ "DD-API-KEY" = $env:DD_API_KEY; "DD-APPLICATION-KEY" = $env:DD_APP_KEY } `
  -Body @{ from = $now - 900; to = $now; query = "avg:system.cpu.user{host:<HOSTNAME>}" }
```

From a POSIX shell on the machine driving the install:

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | tr -d '\r' | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
# Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"; : "${DD_APP_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
printf 'DD-API-KEY: %s\nDD-APPLICATION-KEY: %s\n' "$DD_API_KEY" "$DD_APP_KEY" |
curl -H @- -s -G "https://api.${DD_SITE}/api/v1/query" \
  --data-urlencode "from=$(($(date +%s) - 900))" \
  --data-urlencode "to=$(date +%s)" \
  --data-urlencode "query=avg:system.cpu.user{host:<HOSTNAME>}"
```

Do not expose either key in output. If the hostname is unknown, read the name the Agent reports
from the `Hostname` section of `agent.exe status` (or `agent.exe hostname`) and query that host. Do
not use `avg:system.cpu.user{*}` as proof: it aggregates every host in the org, so existing machines
can return data even when this install sends nothing.

Useful links:

- Infrastructure: `<APP_BASE>/infrastructure`
- System overview: `<APP_BASE>/dash/integration/1/system---overview`
- Integrations: `<APP_BASE>/integrations`
- Fleet Automation: `<APP_BASE>/fleet`

End by summarizing exactly which hosts were changed, which optional products were configured, and
what remains for application log sources or tracing instrumentation.
