---
name: dt-setup-oneagent
description: Reference knowledge for installing, uninstalling, or creating-and-installing Dynatrace OneAgent across VM/server, Kubernetes (Operator + DynaKube), AWS Lambda (layer + env vars, plus optional fresh function provisioning), Windows hosts, remote Linux hosts / EC2 instances over SSH, and Azure VMs / VM Scale Sets. Returns documented endpoints, env vars, token scopes, and copy-paste-ready commands. Returns the exact commands to run rather than executing them. Use when the user asks to install or uninstall OneAgent, or asks "how do I…", "what URL/scope/var do I need for…", or "explain the OneAgent deployment for X".
license: Apache-2.0
---

# Deploy Dynatrace OneAgent — knowledge reference

This skill is **reference-only**. It contains the documented endpoints, environment variables, token scopes, and commands that an operator (or another agent) needs to install OneAgent manually across the supported targets. It executes nothing.

> This skill gives you the commands; it does not run them. Follow the procedure for the target you need, substituting the environment URL and token as documented below.

## Hard rules for any agent consuming this skill

- **Operate only on resources the user explicitly named.** Never create a placeholder/test Lambda, IAM role, K8s namespace, secret, S3 bucket, EC2 instance, or any other fixture on your own initiative — not to "demonstrate", not "while we're at it", not preemptively. If the named resource doesn't exist and the user hasn't asked for it to be created, stop and ask. Side resources (additional Secrets Manager entries, monitoring, helper stacks) must not be provisioned silently — surface them as confirmation questions with the exact definition first.
- **Explicit user-driven create modes are fine.** When the user passes `--create` (or explicitly says "yes, create it" after being asked), provisioning exactly the resources documented for that mode is the right thing to do — see *Create a new function and install OneAgent* in [references/aws-lambda.md](references/aws-lambda.md) for the documented set. Don't second-guess the function name the user typed: do **not** pattern-match on names like "test", "demo", "scratch", "tmp" and refuse, warn, or insist on an alternative. The input is authoritative; the rule above is about *silent* or *unsolicited* creation, not user-requested creation.
- **Never persist the API token.** The token's only job is to (a) authenticate the OneAgent artifact download / layer-ARN lookup and (b) get handed to the target system (Lambda env var or Secrets Manager, Linux installer, DynaKube secret) as part of the install. Do not cache it to local files, write it to scratch scripts, leave it in shell history, copy it into PR descriptions, or store it anywhere outside the target system that strictly needs it. Treat each run as fresh: supply via env var or 0600 file, use, discard.
- **Never echo or log the API token.** When you have to reference it in a command, write `$DT_API_TOKEN` or an elided prefix (`dt0s16.…`, `dt0c01.…`). Don't paste the literal value into prose.
- **Never assume the env URL, and confirm the tenant before installing.** Targeting the wrong environment fails *silently*: the install succeeds and the host or function simply reports to a tenant nobody is watching. An environment URL the user stated explicitly always wins over anything derived from a tool default or a previous run — never let a cached or discovered value override it. State the tenant you are about to use and let the user correct you. Tenant IDs (`abc12345`) and labs vs. prod determine the correct host.
- **Writes that take a collection replace it — read, merge, then write.** Several APIs here accept a whole collection and overwrite whatever was there: `aws lambda update-function-configuration` does this for **both** `--environment` and `--layers`, so sending only the Dynatrace values silently deletes the function's own variables and any other layers. Always read current state, merge your additions into it, and write the union back. Take a rollback snapshot before the first write. This applies wherever you are about to replace a set rather than add to one.
- **Deriving the env URL from dtctl.** `dtctl config current-context` returns only the *context name* (e.g. `my-env`), not a URL. The URL comes from `dtctl config describe-context <ctx>`. Do **not** pipe that straight into `jq`: some dtctl versions ignore `-o json` and print a human table (`Environment:  https://…`) while still exiting 0, so jq dies on a parse error and takes any `set -e -o pipefail` script down with it. Check the output really is JSON first, and fall back to scraping the `Environment:` line:

```bash
CTX="$(dtctl config current-context 2>/dev/null || true)"
OUT="$(dtctl config describe-context "$CTX" -o json 2>/dev/null || true)"
if printf '%s' "$OUT" | jq -e . >/dev/null 2>&1; then
  DT_ENV_URL="$(printf '%s' "$OUT" | jq -r '.environment // .url // empty')"
else
  DT_ENV_URL="$(printf '%s' "$OUT" | awk 'tolower($1) ~ /^(environment|url):$/ {print $2; exit}')"
fi
```

---

## URL normalization

Dynatrace's "new platform" URLs and the classic OneAgent installer endpoints differ. Before constructing installer URLs, convert:

| Input (Dynatrace UI / docs)            | Use for installer endpoints           |
|----------------------------------------|---------------------------------------|
| `https://<id>.apps.dynatrace.com`      | `https://<id>.live.dynatrace.com`     |
| `https://<id>.<region>.apps.dynatracelabs.com` | `https://<id>.<region>.dynatracelabs.com` |
| Anything else                          | unchanged                             |

The tenant ID is the first dot-separated segment (`<id>`).

---

## Token types and the Authorization header

Two token families are in play, and **the `Authorization` scheme is chosen by the token's prefix, not by which endpoint you call**:

| Token | Prefix | Header |
|---|---|---|
| Platform token | `dt0s16.` | `Authorization: Bearer <token>` |
| Access token (classic API token) | `dt0c01.` | `Authorization: Api-Token <token>` |
| PaaS token | `dt0s01.` | `Authorization: Bearer <token>` |
| OAuth client secret | `dt0s02.` / `dt0s03.` | ❌ not directly usable — must be exchanged for a bearer token first |

**Platform tokens are the forward-looking default.** Dynatrace is deprecating access tokens: new tenants can no longer create them, and Classic API endpoints are being updated to accept platform tokens. Do **not** assume a token starts with `dt0c01.`. The reference implementation of this rule is dtwiz's `AuthHeader()` (`pkg/installer/installer.go`): `dt0c01.*` → `Api-Token`, everything else → `Bearer`.

One path hands the token to a component that has historically required a PaaS/access token — if it rejects a platform token, use a `dt0c01.` access token there:

- **Kubernetes** — the Dynatrace Operator authenticates using the `dynakube` secret.

VM, remote VM/EC2, Windows and Lambda call the Deployment API directly and work with either family.

## Token scopes by target

For a **platform token** (`dt0s16.`), the OneAgent-relevant scopes live under **Fleet management**: `fleet-management:oneagents:download`, `fleet-management:oneagent.connection-info:read`, `fleet-management:oneagent.tokens:read`, `fleet-management:cluster-id:read`; Kubernetes additionally wants `fleet-management:activegates:download` and `fleet-management:activegate.tokens:create`. Generating the token via the Dynatrace **QuickStart** app provisions a working set.

For a **classic access token** (`dt0c01.`):

| Target          | Required token scopes |
|-----------------|------------------------|
| VM / Windows    | `InstallerDownload` (PaaS) |
| Kubernetes      | `InstallerDownload`, `settings.read`, `settings.write`, `activeGateTokenManagement.create` — the Dynatrace UI's "Kubernetes: Dynatrace Operator" template sets all four. |
| Azure VM / VMSS | `InstallerDownload` (PaaS). Azure side: the caller's `az` identity needs `Contributor` or any role granting `Microsoft.Compute/.../extensions/write` on the resource. |
| AWS Lambda (runtime token) | A **connection auth token** consumed by the OneAgent layer at runtime. Distinct from the installer token. Create from the Dynatrace UI under *Access tokens* with `entities.read`, or use the Hub → AWS Lambda template. |

Tokens are never username-scoped — they belong to the tenant.

---

## Targets

Each target has its own reference. They share the rules, URL normalization and token guidance above — read those first, then the one you need.

Managed Kubernetes distributions are covered inside the Kubernetes reference rather than separately: the install is identical and only the node type differs, so the deltas belong next to the procedure they modify.

| Target | Reference |
|---|---|
| VM / server (Linux, macOS) | below — the base case every other target builds on |
| Remote VM / EC2 over SSH | → [references/remote-vm-ec2.md](references/remote-vm-ec2.md) |
| Windows host (WSL or native) | → [references/windows.md](references/windows.md) |
| Kubernetes (Operator + DynaKube) — incl. **EKS**, Fargate and Bottlerocket limits | → [references/kubernetes.md](references/kubernetes.md) |
| AWS Lambda (layer + env vars) | → [references/aws-lambda.md](references/aws-lambda.md) |
| Azure VM / VM Scale Set (VM extension) | → [references/azure-vm.md](references/azure-vm.md) |

### By platform

The table above is organised by install mechanism, because that is what decides the procedure. If you are arriving from a particular cloud instead:

| Platform | What you are deploying to | Go to |
|---|---|---|
| **AWS** | EC2 instance | [remote-vm-ec2.md](references/remote-vm-ec2.md) |
| | EKS — EC2 nodes | [kubernetes.md](references/kubernetes.md) |
| | EKS — Fargate or Bottlerocket nodes | [kubernetes.md § AWS EKS specifics](references/kubernetes.md) — full-stack unavailable, `applicationMonitoring` only |
| | Lambda function | [aws-lambda.md](references/aws-lambda.md) |
| **Azure** | VM or VM Scale Set | [azure-vm.md](references/azure-vm.md) |
| | AKS | [kubernetes.md](references/kubernetes.md) — **not** the VM extension, even though node pools are VMSSes |
| **Google Cloud** | GKE (standard) | [kubernetes.md](references/kubernetes.md) |
| | GKE Autopilot | [kubernetes.md](references/kubernetes.md) for the operator path — full-stack is unavailable, as on Bottlerocket. Autopilot-specific tuning is not covered |
| | Compute Engine VM | [remote-vm-ec2.md](references/remote-vm-ec2.md) — the SSH procedure is not AWS-specific |
| **On-prem / anywhere else** | Linux or macOS you are logged into | below |
| | Linux you reach over SSH | [remote-vm-ec2.md](references/remote-vm-ec2.md) |
| | Windows | [windows.md](references/windows.md) |
| | Kubernetes, or OpenShift via the standard operator | [kubernetes.md](references/kubernetes.md) — the classic OpenShift node-config-operator route is not covered |

## VM / server (Linux, macOS)

**Endpoint** (substitute `${DT_ENV_URL_NORMALIZED}` and `${ARCH}` where `ARCH` ∈ `x86 | arm | ppc64le | s390`):

```
GET ${DT_ENV_URL_NORMALIZED}/api/v1/deployment/installer/agent/unix/default/latest?arch=${ARCH}&flavor=default
Header: Authorization: Api-Token ${DT_API_TOKEN}   # dt0c01.… access token
        Authorization: Bearer ${DT_API_TOKEN}      # dt0s16.… platform token
```

**Install command:**

Set the scheme to match your token — `Api-Token` for `dt0c01.…`, `Bearer` for `dt0s16.…`:

```bash
DT_AUTH="Api-Token ${DT_API_TOKEN}"   # platform token: DT_AUTH="Bearer ${DT_API_TOKEN}"

wget -O Dynatrace-OneAgent-Linux.sh \
  --header="Authorization: ${DT_AUTH}" \
  "${DT_ENV_URL_NORMALIZED}/api/v1/deployment/installer/agent/unix/default/latest?arch=${ARCH}&flavor=default"

sudo /bin/sh Dynatrace-OneAgent-Linux.sh \
  --set-monitoring-mode=fullstack \
  --set-app-log-content-access=true \
  [--set-host-group=<name>] \
  [--set-network-zone=<zone>]
```

**Restart caveat:** OneAgent cannot inject into already-running processes. After install, restart the workloads you want monitored.

**Uninstall:**

```bash
sudo /opt/dynatrace/oneagent/agent/uninstall.sh
```

Removes the systemd unit, `/opt/dynatrace`, and the `/etc/ld.so.preload` line that injects the agent.

---

## When you should not use this skill

- The user wants the install performed for them rather than explained. → This skill still applies: follow the target's procedure and run the commands, confirming the tenant first.
- The user is asking why an install failed and wants an explanation. → This skill is appropriate.
- The user wants a target this skill doesn't cover (Azure Functions / App Service / Container Apps, classic OpenShift node-config-operator, GKE Autopilot specifics, ECS Fargate). → Refer to <https://docs.dynatrace.com>; this skill covers VM/server, remote VM/EC2 over SSH, Windows, Kubernetes and AWS Lambda.

## References

- OneAgent Linux install: <https://docs.dynatrace.com/docs/ingest-from/dynatrace-oneagent/installation-and-operation/linux>
- OneAgent Windows install: <https://docs.dynatrace.com/docs/ingest-from/dynatrace-oneagent/installation-and-operation/windows>
- Kubernetes (Operator + DynaKube): <https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s/deployment/full-stack-observability>
- Dynatrace Operator releases: <https://github.com/Dynatrace/dynatrace-operator/releases>
- AWS Lambda (Hub): <https://www.dynatrace.com/hub/detail/amazon-web-services-aws-lambda/>
