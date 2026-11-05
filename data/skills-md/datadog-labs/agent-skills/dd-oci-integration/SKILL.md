---
name: dd-oci-integration
description: Set up the Datadog Oracle Cloud Infrastructure (OCI) integration with Terraform - verifies ~/.oci/config, then applies Datadog's official oracle-cloud-integration module to create the Datadog service user, group, IAM policies, and API key in the tenancy and register it with Datadog, optionally including log collection. Use when the user has Oracle Cloud resources, wants to monitor an OCI tenancy, wants to connect OCI to Datadog, or asks to set up or repair the OCI integration.
metadata:
  version: "1.0.0"
  author: datadog-labs
  repository: https://github.com/datadog-labs/agent-skills
  tags: datadog,oci,oracle-cloud,integration,terraform,cloud
  alwaysApply: "false"
  tools: terraform
---

# Datadog OCI Integration

You are helping a user set up the Datadog OCI integration using Terraform.

The integration uses the official Datadog OCI Terraform module to create the required IAM resources
(user, group, policies, API key) in the customer's OCI tenancy and register it with Datadog.

This is a hands-on setup: run the commands yourself as part of the conversation rather than handing the
user a list, keep them in the loop, and pause for confirmation before `terraform apply`.

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

**Terraform or OpenTofu.** Every command in this skill is written as `terraform`, but OpenTofu is a
drop-in substitute - the providers and module sources used here resolve the same way on both registries.
Check which binary the user actually has before Phase 1:

```bash
command -v terraform tofu
```

If only `tofu` is on the PATH, read every `terraform <subcommand>` below as `tofu <subcommand>`. If both
are present, ask which one the user wants rather than guessing.

**Datadog credentials.** Load `DD_SITE` / `DD_API_KEY` / `DD_APP_KEY` from the environment (falling back
to `.env.local` / `.env`) and validate both keys - they fail independently:

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
: "${DD_SITE:=datadoghq.com}"
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
| Either key unset | Nothing to validate | On a commercial site, run the **dd-account-setup** skill, then come back. On `ddog-gov.com` or `us2.ddog-gov.com`, ask the user for the keys directly - that skill validates `DD_SITE` against a list that excludes both government sites and will reject them |

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
arrive through the loader as `$DD_API_KEY` / `$DD_APP_KEY`. Two consequences follow, and both are
deliberate:

- **Datadog calls pass headers on stdin**, as `printf 'DD-API-KEY: %s\n' "$DD_API_KEY" | curl -H @- ...`.
  `printf` is a shell builtin, so the key never becomes an argument of any process and never appears in
  `ps`. Writing `-H "DD-API-KEY: $DD_API_KEY"` instead would put it in curl's argv. (`-H @-` needs
  curl 7.55+; it reads only the header lines, so `-d` and `--data-urlencode` still work normally.)
- **Terraform never receives the keys as values at all** for AWS, Azure, and GCP: the Datadog provider
  reads `DD_API_KEY` / `DD_APP_KEY` from the environment, so there are no root variables, no `-var=`
  arguments, and nothing for Terraform to record in state or a saved plan. (OCI is the exception - its
  module needs them as inputs, so there they travel as `TF_VAR_*`.)

Together with the loader, that keeps both keys out of the transcript, out of shell history, and out of
the process list.

**Tools.** `terraform` is required; the `oci` CLI is optional (it validates config and looks up OCIDs):

```bash
command -v terraform || echo "MISSING terraform - https://developer.hashicorp.com/terraform/install"
command -v oci >/dev/null 2>&1 && echo "oci: available" || echo "oci: not installed"
```

**The snippets here are POSIX shell.** Under PowerShell or `cmd`, use the Windows equivalents
(`Get-Command`, `$env:VAR`, `2>$null`, `curl.exe`) - same calls, same order.

## Phase 1: Verify OCI Credentials

Terraform's `oci` provider reads from `~/.oci/config`, so that file must exist and be complete before
`terraform apply` can succeed.

**Settle the profile before running anything else in this skill.** If the user named a profile, export it
now; every snippet below, every `oci` CLI call, and the module's `config_file_profile` all read the same
value. Skip this and the checks validate `DEFAULT`, which can be a different tenancy and user than the one
being installed - the checks then pass or fail on the wrong identity:

```bash
export OCI_CLI_PROFILE="TEAM"   # <- the profile the user named; omit only if they said DEFAULT
```

Then check the required fields **without dumping the file** - an OCI profile can contain a `pass_phrase`,
and printing the whole profile would put it in the transcript:

```bash
cfg="$HOME/.oci/config"
[ -r "$cfg" ] || { echo "missing or unreadable: $cfg"; exit 1; }
prof="${OCI_CLI_PROFILE:-DEFAULT}"
field() { awk -v p="[$prof]" -v k="$1" '/^\[/{inp=($0==p); next} inp && $0 ~ "^[ \t]*"k"[ \t]*=" {sub(/^[^=]*=[ \t]*/,""); gsub(/[ \t]+$/,""); print; exit}' "$cfg"; }
bad=0
for k in user tenancy region key_file fingerprint; do
  v=$(field "$k")
  [ -n "$v" ] || bad=1
  case "$k" in
    fingerprint) printf '%-12s %s\n' "$k" "$([ -n "$v" ] && echo present || echo MISSING)" ;;
    *)           printf '%-12s %s\n' "$k" "${v:-MISSING}" ;;
  esac
done
[ -n "$(field pass_phrase)" ] && echo "note: this profile has a pass_phrase; it is deliberately not printed"
keyf=$(field key_file); case "$keyf" in "~/"*) keyf="$HOME/${keyf#\~/}" ;; esac
if [ -n "$keyf" ] && [ -r "$keyf" ]; then echo "key_file     readable"
else echo "key_file     NOT readable: ${keyf:-<unset>}"; bad=1; fi
[ "$bad" -eq 0 ] || { echo "profile [$prof] in $cfg is incomplete - fix it before continuing"; exit 1; }
```

Every one of `user`, `tenancy`, `fingerprint`, `key_file`, `region` must be present, and the private key
must be readable. An empty value or `MISSING` means the profile is incomplete - do not continue.

If the file is missing or incomplete, walk the user through setup:

1. Log into the OCI Console and navigate to **Profile** → **My profile** → **API keys** → **Add API key**.
2. Select **Generate API key pair**, download the private key, and save it to `~/.oci/oci_api_key.pem`.
3. Set permissions on the key: `chmod 600 ~/.oci/oci_api_key.pem`
4. Copy the configuration file snippet that OCI displays after adding the key.
5. Save it to `~/.oci/config` and ensure `key_file` points to the downloaded private key path.

If the `oci` CLI is available, the user can also run
`oci setup config --profile "${OCI_CLI_PROFILE:-DEFAULT}"` to generate the config interactively as an
alternative to the manual steps above.

Validate that the credentials actually authenticate:

**If the `oci` CLI is available:**
```bash
oci --profile "${OCI_CLI_PROFILE:-DEFAULT}" iam region-subscription list 2>&1
```
If this succeeds, proceed. If it fails with an authentication error, help the user fix the config
before continuing.

**Otherwise**, skip the explicit validation here. `terraform plan` in Phase 3 will surface any
auth issues with a clear error from the OCI provider - fix the config at that point if it fails.

## Phase 2: Gather Information

The module needs the **tenancy OCID** and the **OCID of the authenticated user**. Both are already in the
profile verified in Phase 1, which is the authoritative source - read them from there:

```bash
cfg="$HOME/.oci/config"; prof="${OCI_CLI_PROFILE:-DEFAULT}"
field() { awk -v p="[$prof]" -v k="$1" '/^\[/{inp=($0==p); next} inp && $0 ~ "^[ \t]*"k"[ \t]*=" {sub(/^[^=]*=[ \t]*/,""); gsub(/[ \t]+$/,""); print; exit}' "$cfg"; }
tenancy=$(field tenancy); user=$(field user)
case "$tenancy" in ocid1.tenancy.*) echo "TENANCY_OCID=$tenancy" ;;
  *) echo "tenancy in $cfg is missing or not an ocid1.tenancy OCID - fix Phase 1 first"; exit 1 ;; esac
case "$user" in ocid1.user.*) echo "USER_OCID=$user" ;;
  *) echo "user in $cfg is missing or not an ocid1.user OCID - fix Phase 1 first"; exit 1 ;; esac
```

Do **not** try to derive these from `oci iam region-subscription list` or `oci iam user list`: a
`RegionSubscription` carries no tenancy id, and `user list` returns an arbitrary first user in the
tenancy rather than the authenticated one, so both quietly produce the wrong value.

Confirm the two OCIDs with the user before continuing. If they want a different tenancy or user than the
profile's, have them say so explicitly, or find the values in the OCI Console:

- **Tenancy OCID**: **Administration** → **Tenancy Details**.
- **User OCID**: **Profile** → **My profile** → the OCID is shown under the user's name.

The home region is read from the same profile, so it needs no separate input.

Also ask if they want to enable **log collection** (default: yes). Unlike the AWS, Azure, and GCP
integrations, OCI log forwarding is part of this same module - `logs_enabled = true` provisions it.

## Phase 3: Generate and Apply Terraform

### Check what already exists - local Terraform first, then Datadog

Do this **before** generating or applying anything, and in this order. Local state first, because it
decides whether an existing integration is something you can update or something you must not touch:

```bash
find . -maxdepth 1 -type f \( -name '*.tf' -o -name 'terraform.tfstate' \) -print
# A project is "present" if it has configuration - .terraform/ may simply not exist yet on a fresh clone
# with a remote backend, and terraform.tfstate does not exist at all when state is remote.
if [ -n "$(find . -maxdepth 1 -type f \( -name '*.tf' -o -name '*.tf.json' \) -print -quit)" ]; then
  terraform init -input=false >/dev/null || { echo "terraform init failed - resolve that before concluding anything about existing state"; exit 1; }
  out=$(terraform state list 2>&1); rc=$?
  if [ "$rc" -ne 0 ]; then
    case $out in
      *'No state file'*|*'no state'*|*'Backend initialization required'*)
        echo "project is initialized but has no state yet - treat as a clean install" ;;
      *)
        printf '%s\n' "$out"
        echo "could not read state (backend or credentials problem) - do NOT treat this as 'nothing exists'"; exit 1 ;;
    esac
  elif [ -z "$out" ]; then
    echo "state is empty - treat as a clean install"
  else
    printf '%s\n' "$out" | grep -F 'module.datadog_oci' || echo "state exists but holds no module.datadog_oci resource"
  fi
else
  echo "no Terraform configuration here yet - clean install"
fi
```

Match the **exact** resource address `module.datadog_oci`, not a loose `grep -i datadog`: unrelated Datadog
resources, or cloud IAM left behind by a partial apply, would otherwise read as a managed integration.

Then ask Datadog what it already has:

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
# Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"; : "${DD_APP_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
resp=$(printf 'DD-API-KEY: %s\nDD-APPLICATION-KEY: %s\n' "$DD_API_KEY" "$DD_APP_KEY" \
  | curl -sS -w '\n%{http_code}' -X GET -H @- "https://api.${DD_SITE}/api/v2/integration/oci/tenancies")
code=$(printf '%s' "$resp" | tail -1); body=$(printf '%s' "$resp" | sed '$d')
[ "$code" = "200" ] || { echo "lookup failed with HTTP $code - do not assume 'not connected':"; printf '%s\n' "$body"; exit 1; }
printf '%s\n' "$body"
```

Now reconcile the two answers before doing anything:

- **Not in Datadog, nothing in local state** - a clean install. Continue.
- **In Datadog *and* present in local state** - this is the update/repair case, not a duplicate.
  Continue into the Terraform below as a change to the existing resources, and let the plan show
  what it will alter.
- **In Datadog but *absent* from local state** (the tenancy OCID from Phase 2 is already registered) - stop. Applying would either create a
  duplicate or fight with whatever manages it. Say so plainly and offer the options: manage it wherever it is already managed, or delete the
  integration in Datadog first. **Do not offer `terraform import` here** - this skill deploys a module, and a module has no single importable address, so there is no safe one-line import for it.
  Only continue if the user picks one and confirms.
- **Present in local state but *absent* from Datadog** - a partial or rolled-back install. The cloud-side
  resources may exist while the registration does not. Do not start from scratch: run the plan and let it
  show what is missing, and expect it to re-create only the registration.

### Check for Existing Terraform

```bash
find . -maxdepth 1 -type f \( -name '*.tf' -o -name 'terraform.tfstate' \) -print
```

If existing `.tf` files are found, check for existing `datadog` or `oci` providers and reuse them.

### Generate Terraform

The integration uses the official Datadog OCI Terraform module, pinned to a release tag. Terraform's
lock file does not lock remote module revisions, so an unpinned Git source re-resolves the default
branch on every fresh `init` - and this module creates IAM users, policies, API keys and Vault
resources, so an upstream change would silently alter what an unchanged config provisions:

```hcl
variable "datadog_api_key" {
  description = "Datadog API key"
  type        = string
  sensitive   = true
}

variable "datadog_app_key" {
  description = "Datadog application key"
  type        = string
  sensitive   = true
}

module "datadog_oci" {
  source = "github.com/DataDog/oracle-cloud-integration//datadog-terraform-onboarding?ref=datadog-integration-v1.1.17"

  datadog_api_key = var.datadog_api_key
  datadog_app_key = var.datadog_app_key
  datadog_site    = "<DD_SITE>"

  tenancy_ocid      = "<TENANCY_OCID>"
  current_user_ocid = "<USER_OCID>"

  # Must match the profile verified in Phase 1. The module builds its own providers and otherwise reads
  # DEFAULT, which can be a different identity than the one you just validated.
  config_file_profile = "<OCI_CLI_PROFILE>"

  logs_enabled = <LOGS_ENABLED>
}
```

The module handles all resource provisioning:
- Creates a Datadog service user and group in OCI
- Creates IAM policies granting Datadog read access to metrics, logs, and resources
- Generates an API key for authentication
- Registers the tenancy with Datadog via the API

**Optional advanced variables** (only include if the user needs them):

| Variable | Description |
|---|---|
| `config_file_profile` | OCI CLI profile the module's providers use. Defaults to `DEFAULT`; set it to match the profile verified in Phase 1 |
| `user_email` | Email address where OCI notifies the user about the created service user |
| `resource_compartment_ocid` | Compartment for Datadog resources. If null, a compartment named `Datadog` is created in the tenancy |
| `existing_user_id` | Use an existing OCI user instead of creating one |
| `existing_group_id` | Use an existing OCI group instead of creating one |
| `domain_id` | Identity domain OCID (for identity-domain tenancies) |
| `subnet_ocids` | Subnets for log collection, one OCID per line |
| `defined_tags` | Defined tags for created resources, `namespace.key:value` one per line. Leave blank unless the tenancy has mandatory tag defaults |
| `logs_only` | Create the integration with metric and resource collection disabled but available |
| `events_collection_enabled` | Collect OCI Events Service events. Defaults to `false` |
| `enable_regional_vaults` | (verified present in the module on `master`, 2026-08-13) Create a Vault/Key/Secret per subscribed region so each region's forwarder reads its API key locally. Defaults to `false`; existing installs must opt in explicitly |

### Apply Terraform

1. Replace all `<PLACEHOLDER>` values - `<DD_SITE>` from Phase 0, `<TENANCY_OCID>` and `<USER_OCID>`
   from Phase 2, `<OCI_CLI_PROFILE>` as the profile settled at the top of Phase 1, and `<LOGS_ENABLED>`
   as `true` or `false`.
2. Run `terraform init` to download the module.
3. Plan, and **save the plan to a file**. Both keys reach Terraform as `TF_VAR_*` environment
   variables, never as `-var=` arguments, which would put them in Terraform's command line:

   ```bash
   for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
   DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
   # Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
   : "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"; : "${DD_APP_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
   export TF_VAR_datadog_api_key="$DD_API_KEY" TF_VAR_datadog_app_key="$DD_APP_KEY"
   umask 077          # tighten permissions on the plan file regardless
   terraform plan -out=tfplan
   ```

   Show the plan output to the user and wait for explicit confirmation.
4. Apply **that saved plan**, only after the user confirms it. Applying the file is what makes the
   approval meaningful: `terraform apply` with no plan file computes a brand-new plan, and `-auto-approve`
   would execute it without anyone seeing it, so anything changed since the plan would go in unreviewed:

   ```bash
   for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
   DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
   # Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
   : "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"; : "${DD_APP_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
   export TF_VAR_datadog_api_key="$DD_API_KEY" TF_VAR_datadog_app_key="$DD_APP_KEY"
   # EXIT cleans up; the signal handlers must also terminate, or a Ctrl-C would delete tfplan and
   # then fall through into a retry of a file that no longer exists.
   trap 'rm -f tfplan' EXIT
   trap 'rm -f tfplan; exit 130' HUP INT TERM
   attempt=1
   while :; do
     out=$(terraform apply tfplan 2>&1); rc=$?
     printf '%s\n' "$out"
     [ "$rc" -eq 0 ] && { echo "apply complete"; break; }
     case $out in
       *'no such host'*|*'dial tcp'*)
         if [ "$attempt" -ge 3 ]; then echo "still failing after $attempt attempts - stopping"; exit 1; fi
         echo "transient OCI endpoint lookup failure - retry $attempt of 3 in 10s"
         attempt=$((attempt + 1)); sleep 10 ;;
       *'stale'*|*'Saved plan is stale'*)
         echo "the saved plan is stale (state moved under it) - re-run the plan step and apply the NEW file"; exit 1 ;;
       *)
         echo "apply failed for a non-transient reason - do NOT retry and do NOT report success"; exit 1 ;;
     esac
   done
   ```

   The `trap` removes the plan file on every exit path, including Ctrl-C while the user is deciding. The
   `if`/`else` around the apply matters because a cleanup command as the block's last line would make a
   failed apply exit 0, and the agent would go on to "verify" a deployment that never happened. (It is an
   `if` rather than `status=$?` on purpose: `status` is a read-only variable in zsh.)

   **OCI is the exception to how the other three skills handle keys.** They pass nothing to Terraform at all -
   the Datadog provider reads the environment - so their plan files contain no secrets. This module takes
   `datadog_api_key` **and** `datadog_app_key` as ordinary module inputs, so **both** keys are recorded in the
   saved plan, and the **API key** additionally lands in state (the module provisions a Vault secret from
   it; the app key is only used for provider headers, which are not persisted), and neither can be `ephemeral` because the module feeds them to resources.
   Consequences to state out loud before planning: `tfplan` is a cleartext secret while it exists, `umask 077`
   only limits other local users, and a remote state backend does not protect it. Add `tfplan` to
   `.gitignore` and never commit it. The traps above delete it on every exit path including Ctrl-C during
   approval - but if the agent's session is killed outright, delete it by hand.

### Handling Transient OCI DNS Errors

OCI's identity endpoint intermittently fails with errors like:
`dial tcp: lookup identity.<region>.oci.oraclecloud.com: no such host`

This is a known transient OCI issue - it does **not** mean the environment lacks OCI access.
If `terraform plan` or `terraform apply` fails with this error, automatically retry the command
up to 3 times with a 10-second pause between attempts. Do not tell the user their environment
is misconfigured or that they lack OCI access based on this error alone.

## Phase 4: Verify Setup

After `terraform apply` completes, verify the tenancy is registered:

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
# Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"; : "${DD_APP_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
resp=$(printf 'DD-API-KEY: %s\nDD-APPLICATION-KEY: %s\n' "$DD_API_KEY" "$DD_APP_KEY" \
  | curl -sS -w '\n%{http_code}' -X GET -H @- "https://api.${DD_SITE}/api/v2/integration/oci/tenancies")
code=$(printf '%s' "$resp" | tail -1); body=$(printf '%s' "$resp" | sed '$d')
[ "$code" = "200" ] || { echo "lookup failed with HTTP $code - do not assume 'not connected':"; printf '%s\n' "$body"; exit 1; }
printf '%s\n' "$body"
```

Confirm the response includes the tenancy OCID. Then check for metrics:

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
# Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"; : "${DD_APP_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
sleep 10
resp=$(printf 'DD-API-KEY: %s\nDD-APPLICATION-KEY: %s\n' "$DD_API_KEY" "$DD_APP_KEY" \
  | curl -sS -w '\n%{http_code}' -G -H @- "https://api.${DD_SITE}/api/v1/query" \
  --data-urlencode "from=$(($(date +%s) - 900))" \
  --data-urlencode "to=$(date +%s)" \
  --data-urlencode "query=avg:oci.computeagent.cpu_utilization{*}")
code=$(printf '%s' "$resp" | tail -1); body=$(printf '%s' "$resp" | sed '$d')
[ "$code" = "200" ] || { echo "metric query failed with HTTP $code - that is NOT 'metrics still propagating':"; printf '%s\n' "$body"; exit 1; }
printf '%s\n' "$body"
```

If metrics are flowing, congratulate the user. If not, let them know OCI metrics typically appear
within 5-10 minutes.

Provide links:
- **OCI Integration tile**: `<APP_BASE>/integrations/oracle-cloud-infrastructure`
- **Metrics Explorer**: `<APP_BASE>/metric/explorer?exp_metric=oci.computeagent.cpu_utilization`
- **Infrastructure Map**: `<APP_BASE>/infrastructure/map`
- **Logs Explorer** (if `logs_enabled`): `<APP_BASE>/logs`

## Important Notes

- The user must have IAM permissions to create users, groups, policies, and API keys in their OCI tenancy.
  For an identity-domain tenancy that means administrator rights on the target domain, since the module
  creates the service user and group there.
- **The module requires Terraform `>= 1.5.0`** (its `providers.tf` declares `required_version = ">= 1.5.0"`).
  An older CLI fails during `terraform init`, so check `terraform version` before Phase 3. Every OpenTofu
  release satisfies this constraint - its versions start at 1.6 - so `tofu version` needs no separate check.
- **`existing_user_id` and `existing_group_id` are an inseparable pair.** The module has a precondition that
  fails when exactly one is set: pass both to reuse an existing user and group, or neither to have it create
  them.
- Only parent tenancies can be integrated - child tenancies inherit from the parent.
- The Terraform module source is `github.com/DataDog/oracle-cloud-integration` - this is the official Datadog module.
- For Terraform-managed integrations, deletion must be done via `terraform destroy`, not the Datadog UI.
- **This module puts secret material in Terraform state.** It creates an OCI API key for the Datadog
  service user and passes the Datadog API key into the resources it provisions, and `sensitive = true`
  redacts values from CLI output without removing them from state
  ([HashiCorp docs](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)).
  **The module offers no way around this:** its only credential inputs are the raw `datadog_api_key` and
  `datadog_app_key` variables - there is no input that accepts a pre-existing Vault secret OCID - and it
  provisions the Vault, Key, and Secret itself. So there are exactly two honest options, and the user must
  pick one before you plan: (a) accept it - and then **configure the encrypted remote backend first**,
  because Terraform's default is a plaintext `terraform.tfstate` in the working directory and moving state
  afterwards leaves the plaintext copy behind - or (b) stop here and use the OCI integration tile in the
  Datadog UI instead, which never puts the key in state at all. Do not imply a third option, and do not
  start a plan under option (a) until the backend is in place and verified.
- The Datadog API and app keys reach Terraform through `TF_VAR_*` at plan/apply time. Don't write them
  into a committed `.tfvars` file or any other persistent file. Note the module still places the API key
  in the plan and the state - see the state disclosure below; that is why the backend decision comes first.
- Never run `terraform apply` without showing the plan to the user first.
