---
name: dd-agent-install-macos
description: Install the Datadog Agent on a macOS machine with the macOS installer, with infrastructure metrics, logs, and APM trace intake on by default, plus optional live processes, APM instrumentation, custom tags, and service management. Use when the user wants to install the Datadog Agent on their Mac, set up Datadog on macOS, or monitor a macOS developer or CI machine with Datadog. Does not install the Agent on Linux, Windows, Docker, or Kubernetes (use dd-agent-install-linux, dd-agent-install-windows, dd-agent-install-docker, or dd-agent-install-kubernetes) and does not target managed cloud fleets. Requires a Datadog account with a valid API key and application key; run `dd-account-setup` first if they are missing.
metadata:
  version: "1.0.0"
  author: datadog-labs
  repository: https://github.com/datadog-labs/agent-skills
  tags: datadog,agent,install,host,macos,infrastructure,logs,apm
  alwaysApply: "false"
  tools: curl
---

# Datadog Agent Installation (macOS)

You are helping a user install the Datadog Agent on a macOS machine.

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

**Tools.** `curl` is required:

```bash
command -v curl || echo "MISSING curl"
```

## Phase 1: Discover the Target

Start conversationally. Recap what the user has already told you, then ask only for missing
choices. macOS Agent installs target a specific machine - usually a developer or CI
workstation - not a managed cloud fleet.

Determine:

- The Datadog site and optional environment or global tags.
- Whether a proxy or custom hostname is required.
- Which non-default products beyond the three pillars the user wants: live process collection.

Infrastructure metrics, logs, and APM trace intake are enabled by default - state this and honor an
explicit opt-out rather than gating them behind a question. Two caveats set expectations; they are
not reasons to leave a pillar off:

- The Logs Agent starts collecting, but application log sources still need integration or custom
  log configuration to produce useful logs - enable it and name that follow-up.
- The APM receiver accepts traces but does not instrument applications. Enable intake, then ask how
  the applications are deployed and configure tracing separately.

## Phase 2: Direct Install

Use the macOS installer, not the Linux package installer:

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | tr -d '\r' | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
# Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
export DD_API_KEY
if ! installer=$(curl -fsSL https://install.datadoghq.com/scripts/install_mac_os.sh); then
  echo "Installer download failed - stop here." >&2
elif ! sudo --preserve-env=DD_API_KEY,DD_SITE bash -c "$installer"; then
  echo "Agent install failed - stop here and read the output above." >&2
fi
```

`sudo --preserve-env=DD_API_KEY,DD_SITE` hands the exported values to the installer through the
environment, so the key never appears on `sudo`'s command line (`sudo DD_API_KEY=...` would put it
there). The install script writes the key to its own root-only install file. Stop if either message
prints; do not continue to the logs step. If sudo refuses to preserve the environment (a restricted
sudoers policy), stop and ask the user to run the install themselves rather than putting the key on
the command line.

Infrastructure metrics and the APM trace receiver are on by default. The macOS installer has no logs
flag, so enable the Logs Agent (the third pillar) after install by setting `logs_enabled: true` in
`datadog.yaml` and restarting; drop this step only on a logs opt-out:

```bash
cfg=/opt/datadog-agent/etc/datadog.yaml
sudo sed -i '' -E '/^logs_enabled[[:space:]]*:/d' "$cfg"
printf '\nlogs_enabled: true\n' | sudo tee -a "$cfg" >/dev/null
if [ "$(sudo grep -cE '^logs_enabled[[:space:]]*:' "$cfg")" = 1 ] \
  && sudo grep -qxE 'logs_enabled:[[:space:]]*true' "$cfg"; then
  sudo launchctl kickstart -k system/com.datadoghq.agent
else
  echo "logs_enabled update did not leave exactly one 'logs_enabled: true' line - stop and inspect $cfg." >&2; false
fi
```

This removes every existing top-level `logs_enabled` key (including `logs_enabled : false` forms)
and appends a single `logs_enabled: true`, so the file never ends up with conflicting keys. The
Agent restarts only after the check passes; if the message prints, stop before continuing.

The macOS install script does not take environment, tags, hostname, or proxy as environment
variables. If the user asked for any of those, set them in `/opt/datadog-agent/etc/datadog.yaml`
(`env:`, `tags:`, `hostname:`, and the `proxy:` block respectively) and restart with
`sudo launchctl kickstart -k system/com.datadoghq.agent` rather than dropping the request.

Configure optional live-process settings after installation. Application tracing still requires
tracer installation or another supported instrumentation method.

Paths:

- Configuration: `/opt/datadog-agent/etc/datadog.yaml`
- Integration configs: `/opt/datadog-agent/etc/conf.d/`
- Log: `/opt/datadog-agent/logs/agent.log`

Verify and manage the service:

```bash
datadog-agent status
sudo launchctl print system/com.datadoghq.agent
sudo launchctl kickstart -k system/com.datadoghq.agent
```

Use `sudo launchctl kill SIGTERM system/com.datadoghq.agent` to stop it.

## Phase 3: Configure Selected Products

After the Agent is healthy:

- For application logs, identify the exact files and create the corresponding integration
  configuration. `logs_enabled: true` alone does not select application sources.
- For APM, identify the application language and deployment process, then configure supported
  tracer libraries. Verify traces rather than only the Agent receiver.

Do not enable optional products solely because they are available.

## Phase 4: Verify

Run the status command and confirm:

- The API key is valid.
- The Forwarder reports successful transactions.
- Core checks are running.
- The default-on Logs Agent and Trace Agent (and any explicitly selected Process Agent) are
  healthy.

```bash
datadog-agent status
```

If the host does not appear, check `/opt/datadog-agent/logs/agent.log`.

Confirm the host in `<APP_BASE>/infrastructure`.

## Getting the Most Out of Your Agent

After the host reports, query a recent infrastructure metric with the Datadog metrics API:

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
from the `Hostname` section of `datadog-agent status` (or `datadog-agent hostname`) and query that
host. Do not use `avg:system.cpu.user{*}` as proof: it aggregates every host in the org, so existing
machines can return data even when this install sends nothing.

Useful links:

- Infrastructure: `<APP_BASE>/infrastructure`
- System overview: `<APP_BASE>/dash/integration/1/system---overview`
- Integrations: `<APP_BASE>/integrations`

End by summarizing exactly what was changed, which optional products were configured, and what
remains for application log sources or tracing instrumentation.
