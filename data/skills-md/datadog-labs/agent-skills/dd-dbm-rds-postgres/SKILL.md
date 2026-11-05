---
name: dd-dbm-rds-postgres
description: Set up Datadog Database Monitoring (DBM) for PostgreSQL on AWS RDS - enable pg_stat_statements on the instance's parameter group, then deploy a managed Agent with CloudFormation, provision one with Terraform, or configure an existing Agent, plus the read-only datadog monitoring user. Use when the user wants to set up Database Monitoring for an RDS Postgres database, monitor query performance on a Postgres RDS instance, enable DBM for Postgres on RDS, or use Terraform to set up DBM for an RDS Postgres database. Does not handle Aurora, RDS Multi-AZ DB clusters, or read replicas (point the user at the source writer or the DBM docs instead), and does not set up DBM for other engines. Requires the Datadog AWS integration for the AWS account that holds the instance; run `dd-aws-integration` first if it is missing.
metadata:
  version: "1.0.0"
  author: datadog-labs
  repository: https://github.com/datadog-labs/agent-skills
  tags: datadog,database-monitoring,dbm,postgres,rds,aws,terraform
  alwaysApply: "false"
  tools: aws,jq
---

# Datadog Database Monitoring for Postgres on RDS

You are helping a user set up Datadog Database Monitoring (DBM) for a PostgreSQL database on AWS RDS.

DBM collects query metrics, samples, and execution plans via a Datadog Agent that connects to the RDS
endpoint as a read-only monitoring user. There are **three ways to run that Agent**, and this skill
supports all three:

- **Managed (CloudFormation)** - Datadog deploys a small Fargate Agent into the account that connects
  to the instance and bootstraps the `datadog` user for you. This is the same approach as the
  in-product "Quick Install". Every step is an **AWS control-plane or Datadog API call**, so it works
  from this shell with no database connection or host access - pick this when the user has no Agent
  that can already reach the database.
- **Terraform-provisioned** - provision a dedicated Fargate or EC2 Agent, or add the DBM cluster check
  to an existing EKS Agent deployment, in the user's Terraform project. Pick this when the user wants
  the Agent and network policy owned by IaC and can run the database bootstrap from a DB-reachable host
  or through SSM. Terraform manages secret containers and IAM, but secret *values* are seeded
  out-of-band so they never enter Terraform state.
- **Existing Agent (manual)** - add a `postgres` check to an Agent the user already runs (host / ECS /
  Kubernetes). Pick this when they already have an Agent with network reachability to the database and
  want to reuse it (no extra Fargate service).

**All three paths require `pg_stat_statements` on the instance** (Phase 2) - including the managed path,
because the managed installer does *not* configure the RDS parameter group. This is a **product
integration (PINT) flow**: it requires an existing Datadog AWS integration.

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
case "$DD_SITE" in datadoghq.com|us3.datadoghq.com|us5.datadoghq.com|datadoghq.eu|ap1.datadoghq.com|ap2.datadoghq.com|uk1.datadoghq.com|ddog-gov.com|us2.ddog-gov.com) ;;
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
arrive through the loader as `$DD_API_KEY` / `$DD_APP_KEY`. Two consequences follow, and both are
deliberate:

- **Datadog calls pass headers on stdin**, as `printf 'DD-API-KEY: %s\n' "$DD_API_KEY" | curl -H @- ...`.
  `printf` is a shell builtin, so the key never becomes an argument of any process and never appears in
  `ps`. Writing `-H "DD-API-KEY: $DD_API_KEY"` instead would put it in curl's argv. (`-H @-` needs
  curl 7.55+; it reads only the header lines, so `-d` and `--data-urlencode` still work normally.)
- **The API key reaches AWS only through a protected temp file.** Where this skill stores it in Secrets
  Manager (the managed and Terraform paths), it is written with `printf` to a `umask 077` temp file and
  passed as `--secret-string file://...`, never on argv and never through `-var` / `TF_VAR_*`, so it
  stays out of Terraform state and plan files (Phase 3C, C1).

Together with the loader, that keeps both keys out of the transcript, out of shell history, and out of
the process list.

**Tools.** `aws` and `jq` are required; `psql` and `terraform` are optional (`psql` for the database
bootstrap on the Terraform and existing-Agent paths, `terraform` for the Terraform path):

```bash
for t in aws jq; do command -v "$t" >/dev/null 2>&1 && echo "$t: available" || echo "MISSING $t"; done
for t in psql terraform; do command -v "$t" >/dev/null 2>&1 && echo "$t: available" || echo "$t: not installed (optional)"; done
```

**The snippets here are POSIX shell.** Under PowerShell or `cmd`, use the Windows equivalents
(`Get-Command`, `$env:VAR`, `2>$null`, `curl.exe`) - same calls, same order.

## Phase 1: Prerequisites and Discovery

### Confirm the AWS Integration and Resource Collection

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | tr -d '\r' | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
# Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"; : "${DD_APP_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
resp=$(printf 'DD-API-KEY: %s\nDD-APPLICATION-KEY: %s\n' "$DD_API_KEY" "$DD_APP_KEY" \
  | curl -sS -w '\n%{http_code}' -X GET -H @- "https://api.${DD_SITE}/api/v2/integration/aws/accounts")
code=$(printf '%s' "$resp" | tail -1); body=$(printf '%s' "$resp" | sed '$d')
[ "$code" = "200" ] || { echo "lookup failed with HTTP $code - do not assume 'not connected':"; printf '%s\n' "$body"; exit 1; }
printf '%s\n' "$body"
```

The AWS integration is a **conditional** prerequisite: check for it here rather than running
`dd-aws-integration` unconditionally (which would prompt for account/regions and apply Terraform even
when the org is already integrated). Branch on this check **against the account you're operating in**, not just
"any account" - in a multi-account org the response can list other integrated accounts while the one
holding your RDS instance is not integrated, leaving the PINT prerequisite unmet for that resource. Get
the operating account (the RDS instance you'll target lives here) and compare it to the integrated list:

```bash
aws sts get-caller-identity --query Account --output text
```

If that account ID is among the integrated accounts, continue. If it isn't, stop and run the
`dd-aws-integration` skill for this account now, then return here. Resource Collection (`resources_config.extended_collection`) is **not required for
core DBM** - query metrics, samples, and explain plans come from the Agent's database connection. It
only enriches DBM by correlating the instance with its **RDS infrastructure metrics** (CPU, memory,
disk), which is optional. If the user wants that correlation, confirm it's `true` and enable it via
`dd-aws-integration`; otherwise skip it.

### Identify the RDS Instance

This skill targets a **standalone, writable single-instance RDS PostgreSQL** database - `Engine=postgres`,
**not part of a cluster, and not a read replica**.

**Set the target region before discovery.** RDS is regional, so `describe-db-instances` only lists the
CLI's current region - if the instance lives elsewhere the list comes back empty and you can't recover the
region from this output. Ask the user which region the instance is in (shown in the RDS console) and
substitute it for `<REGION>`. Every regional `aws` call from here passes `--region <REGION>` explicitly:
most agent runtimes start a fresh shell per command, so an exported `AWS_REGION` would not reach later
blocks, and the CLI would fall back to the default region (or fail if none is set).

If the user isn't sure which region, find the Postgres instances across all regions first, then set
`<REGION>` to the match and continue. The region list itself needs an explicit region to query: use
`us-east-1` for commercial AWS, or `us-gov-west-1` for GovCloud. The block stops if the region list
can't be read, so an empty result really means no instances:

```bash
DISCOVERY_REGION='us-east-1'   # us-gov-west-1 for GovCloud
REGIONS=$(aws ec2 describe-regions --region "$DISCOVERY_REGION" --query "Regions[].RegionName" --output text) \
  || { echo "Could not list regions from $DISCOVERY_REGION; ask the user for the region instead." >&2; exit 1; }
[ -n "$REGIONS" ] || { echo "Region list is empty; ask the user for the region instead." >&2; exit 1; }
printf '%s\n' "$REGIONS" | tr -s '[:space:]' '\n' | while read -r region; do
  [ -n "$region" ] || continue
  aws rds describe-db-instances --region "$region" \
    --query "DBInstances[?Engine=='postgres'||Engine=='aurora-postgresql'].[DBInstanceIdentifier]" \
    --output text </dev/null | sed "s/^/$region /"
done
```

List the candidates in the target region with their engine, cluster, and replica-source so you can spot
and rule out the deployments it can't handle:

```bash
aws rds describe-db-instances --region <REGION> \
  --query "DBInstances[?Engine=='postgres'||Engine=='aurora-postgresql'].{ID:DBInstanceIdentifier,Engine:Engine,Cluster:DBClusterIdentifier,Replica:ReadReplicaSourceDBInstanceIdentifier,Endpoint:Endpoint.Address,Port:Endpoint.Port,Version:EngineVersion,ParamGroup:DBParameterGroups[0].DBParameterGroupName,SG:VpcSecurityGroups[0].VpcSecurityGroupId,VPC:DBSubnetGroup.VpcId}" \
  --output json
```

Rule out two kinds of instance before continuing:

- **Clustered** (`Cluster` set, or `Engine=aurora-postgresql`). Both Aurora *and* RDS Multi-AZ DB clusters
  (which report `Engine=postgres` but are still clustered) are configured through a **DB cluster parameter
  group** (`modify-db-cluster` / `*-db-cluster-parameter-group`), not the per-instance group this skill
  changes via `modify-db-instance` - and they have separate writer/reader endpoints and different reboot
  semantics. So Phase 2 onward doesn't apply and `pg_stat_statements` wouldn't be enabled correctly.
  (Cluster support is a separate flow.)
- **A read replica** (`Replica` / `ReadReplicaSourceDBInstanceIdentifier` set). Replicas are read-only, so
  the write setup on either path (`CREATE ROLE` / `CREATE EXTENSION` / the explain function) fails against
  them. Point the user at the **source writer** (the `Replica` value) and run the setup there instead.

If either applies, stop and tell the user **where to go instead** rather than leaving them at a dead end:

- **Read replica** (`Replica` set) - run this skill against the **source writer** (the `Replica` value),
  which is the instance identifier of the primary.
- **Aurora / RDS Multi-AZ DB cluster, including Aurora Serverless v2** (`Cluster` set or
  `Engine=aurora-postgresql`) - this per-instance flow can't configure a cluster (different
  parameter-group model, separate writer/reader endpoints). Point the user at Datadog's DBM Postgres
  setup docs (`https://docs.datadoghq.com/database_monitoring/setup_postgres/`); cluster support is a
  separate flow that isn't available here yet. Aurora Serverless v2 without customer-VPC placement in
  particular is not the topology the managed CloudFormation template expects, so the managed path won't
  fit even if the user forces it.

Continue only for a standalone `Engine=postgres` instance with both `Cluster` and `Replica` empty.

From the chosen instance collect the **endpoint**, **port** (default `5432`), **region**, **DB instance
identifier**, **Postgres major version**, **VPC ID**, and **VPC security group ID**, plus the
**currently-attached parameter group**. `<MAJOR_VERSION>` is the major number only (e.g. `15` from
`15.4`) - take the first dot-separated component of `EngineVersion`, or the family
`postgres<MAJOR_VERSION>` will be invalid.

If a field is missing from the output, or the caller lacks `rds:DescribeDBInstances`, ask the user for it
(all are visible in the RDS console). You also need to authenticate as the master user once, to create
the monitoring user - a password, or the **RDS-managed master secret** if the instance uses one (A1 for
the managed path, B3 for the Terraform or existing-Agent path).

> **Managed or Terraform Fargate path - do not reuse the RDS DB subnet group's subnets** for the Agent. Those
> subnets are commonly isolated (no NAT gateway, no VPC endpoints), so the task can't pull its images
> or reach Secrets Manager / Datadog and dies before connecting to Postgres. The Agent needs
> **ECS-capable subnets** with an outbound path (NAT, or ECR + Secrets Manager + Datadog VPC endpoints)
> *and* routing to the RDS instance.

### Choose the install path

The right default depends on whether the user already runs a reachable Agent, wants Terraform ownership,
and has a DB-reachable place to run the bootstrap SQL.

**Default to the managed path (Phase 3A)** when the user has no Datadog Agent that can already reach this
RDS instance and no requirement that Terraform own the Agent. It's the closest equivalent to the in-product Quick Install: every step is an AWS
control-plane or Datadog API call, so it runs from this shell with no database connection or host access,
and the API key is injected from Secrets Manager (A4) rather than stored in plaintext.

Ask whether the user already runs a **Datadog Agent that can reach this RDS endpoint** (a host/EC2, ECS,
or Kubernetes Agent in the same VPC or with network access), and whether they want the Agent owned by
Terraform:

- **No existing reachable Agent, and no requirement that Terraform own it** → **Phase 3A (Managed)** - the recommended default.
- **Yes, reuse it, and Terraform need not own it** → **Phase 3B (Existing Agent)** - avoids standing up a second Agent.
- **Terraform must own the Agent** (whether or not one exists today) → start at **Phase 3C (Terraform-provisioned Agent)**. C1 creates
  the empty secret containers, then sends the flow through B2/B3 for out-of-state secret seeding and SQL
  before returning to C2/C3. This path needs a DB-reachable host, SSM-managed instance, or direct client
  for B3; if none exists, either relax the Terraform-ownership requirement and use 3A, or stop and ask the
  user for a DB-reachable bootstrap path (SSM, host, or client) - do not silently drop to CloudFormation.

The Terraform generator at `<APP_BASE>/databases/setup` is a useful starting point for Agent
infrastructure and networking, but it is **not a complete DBM bootstrap**: the generated module assumes
the `datadog` role and per-database objects already exist, does not configure `pg_stat_statements`, and
may place database/API-key values in `terraform.tfvars`, state, and runtime definitions. Never apply that
bundle unchanged. Phase 3C gives the hardening contract it must meet before it can be used by this flow.

**Caveat for AI agents under a safety/command-approval policy:** the managed path still `curl`s a template
and install script from S3, runs `curl -L "$DBMInstallScriptUrl" | bash` inside the stack, and deploys
with `CAPABILITY_IAM`. Some safety classifiers refuse that remote-code + broad-IAM pattern outright. Don't
fight the classifier: fetch and review the artifacts (Phase 3A), and if the deploy is still blocked, hand
the exact `cloudformation deploy` to the user to run, or use 3B/3C when the database bootstrap is
reachable. That's a harness limitation, not a reason to steer users off the managed path.

## Phase 2: Enable pg_stat_statements (parameter group) - all paths

**Run every `aws` command from here on against the instance's region**, so secrets, security-group
rules, parameter changes, and the reboot don't target your default region. Each command below passes
`--region <REGION>` itself; keep it on any command you add, since a region exported in an earlier block
does not survive into the next shell.

DBM needs `pg_stat_statements` in `shared_preload_libraries` - a **static** parameter. Inspect the
currently-attached group and its `shared_preload_libraries`:

```bash
aws rds describe-db-parameters --region <REGION> --db-parameter-group-name <CURRENT_PARAM_GROUP> \
  --query "Parameters[?ParameterName=='shared_preload_libraries'].ParameterValue" --output text
```

Compute the target value by **appending** `pg_stat_statements` to the existing list when absent - e.g.
`pgaudit` becomes `pgaudit,pg_stat_statements`. **Never replace the whole list**, or you disable
existing libraries like `pgaudit`, `auto_explain`, or `pg_cron`. Call the result
`<SHARED_PRELOAD_LIBRARIES>`.

DBM needs `track_activity_query_size` to be **at least** 4096, but don't lower an instance that already
captures more query text. Read the current value:

```bash
aws rds describe-db-parameters --region <REGION> --db-parameter-group-name <CURRENT_PARAM_GROUP> \
  --query "Parameters[?ParameterName=='track_activity_query_size'].ParameterValue" --output text
```

Use the larger of that value and `4096` as `<TRACK_ACTIVITY_QUERY_SIZE>` (an empty or unset result means
the family default, which is below 4096, so use `4096`).

These values are what the group is **configured** with, not necessarily what the instance has loaded.
A previous run may have changed the group and stopped before the reboot, so also check whether the
instance still has parameter changes waiting for a reboot:

```bash
aws rds describe-db-instances --region <REGION> --db-instance-identifier <DB_INSTANCE_IDENTIFIER> \
  --query "DBInstances[0].DBParameterGroups[0].[DBParameterGroupName,ParameterApplyStatus]" --output text
```

If the attached group isn't the one you just read, use it as `<CURRENT_PARAM_GROUP>`, re-run the two
reads above against it, and recompute both target values before deciding anything.

If `ParameterApplyStatus` is `pending-reboot`, the configured values are not active yet, so the
no-reboot shortcut below does not apply. The pending change may be unrelated to DBM, so still compare
the configured values with the requirements. If both already match (`pg_stat_statements` is in
`shared_preload_libraries` and `track_activity_query_size` is at least 4096), skip the parameter changes
and go to the **Reboot** step at the end of this phase, with the same explicit confirmation. Otherwise
continue with the **Otherwise** branch below to apply the missing settings, then reboot. The shortcut
applies only when the status is `in-sync`.

**If `pg_stat_statements` is already in `shared_preload_libraries`, `track_activity_query_size` is
already ≥ 4096, *and* the status above is `in-sync`** (common on PG15+ default groups), the required parameters are already satisfied - DBM
collects untruncated query metrics with no parameter change and no reboot. The only settings left are
optional tuning: `pg_stat_statements.track=all` (capture nested statements) and `track_io_timing=1` (I/O
timing in explain plans) - both **dynamic** (`ApplyMethod=immediate`). How to apply them depends on the
current group:

- **On a custom group** - set the two params in place with `modify-db-parameter-group`
  (`ApplyMethod=immediate`); they take effect with **no reboot**. If the group is shared with other
  instances, the shared-group caveat below applies (the change reaches them too), so confirm first.
- **On a `default.*` group** - defaults can't be modified, so enabling these still means creating a
  custom group and **rebooting to attach it** (attaching flips its static params to `pending-reboot`
  even though the values already match). Ask the user whether that fidelity is worth a reboot; if not,
  skip the rest of Phase 2 and go to your chosen install path (Phase 3A, 3B, or 3C).

**Otherwise** - `pg_stat_statements` isn't loaded, or `track_activity_query_size` is below 4096 (the
default 1024 truncates query samples and explain-plan inputs) - a parameter change and reboot are
genuinely required, not optional. Continue and branch on the current group:

**If the instance is on a `default.postgresN` group** (defaults cannot be modified), create a custom
group in the same family - named per-instance so it doesn't collide with other instances or families,
and reused if a prior run created it - and attach it:

```bash
PARAM_GROUP="datadog-dbm-<DB_INSTANCE_IDENTIFIER>-pg<MAJOR_VERSION>"

if ! CREATE_ERR=$(aws rds create-db-parameter-group --region <REGION> \
  --db-parameter-group-name "$PARAM_GROUP" \
  --db-parameter-group-family postgres<MAJOR_VERSION> \
  --description "Datadog DBM settings" 2>&1 >/dev/null); then
  case "$CREATE_ERR" in
    *DBParameterGroupAlreadyExists*) echo "Reusing existing parameter group $PARAM_GROUP" ;;
    *) echo "$CREATE_ERR" >&2; exit 1 ;;
  esac
fi

aws rds modify-db-parameter-group --region <REGION> \
  --db-parameter-group-name "$PARAM_GROUP" \
  --parameters '[
    {"ParameterName":"shared_preload_libraries","ParameterValue":"<SHARED_PRELOAD_LIBRARIES>","ApplyMethod":"pending-reboot"},
    {"ParameterName":"track_activity_query_size","ParameterValue":"<TRACK_ACTIVITY_QUERY_SIZE>","ApplyMethod":"pending-reboot"},
    {"ParameterName":"pg_stat_statements.track","ParameterValue":"all","ApplyMethod":"immediate"},
    {"ParameterName":"track_io_timing","ParameterValue":"1","ApplyMethod":"immediate"}
  ]' >/dev/null || exit 1

SPL=$(aws rds describe-db-parameters --region <REGION> --db-parameter-group-name "$PARAM_GROUP" \
  --query "Parameters[?ParameterName=='shared_preload_libraries'].ParameterValue" --output text) || exit 1
TAQS=$(aws rds describe-db-parameters --region <REGION> --db-parameter-group-name "$PARAM_GROUP" \
  --query "Parameters[?ParameterName=='track_activity_query_size'].ParameterValue" --output text) || exit 1
case ",$(printf '%s' "$SPL" | tr -d ' ')," in
  *,pg_stat_statements,*) ;;
  *) echo "shared_preload_libraries on $PARAM_GROUP is '$SPL'; pg_stat_statements is missing." >&2; exit 1 ;;
esac
case "$TAQS" in
  ''|*[!0-9]*) echo "track_activity_query_size on $PARAM_GROUP is '$TAQS', not a number." >&2; exit 1 ;;
esac
[ "$TAQS" -ge 4096 ] || { echo "track_activity_query_size on $PARAM_GROUP is $TAQS, below 4096." >&2; exit 1; }

PENDING=$(aws rds describe-db-instances --region <REGION> --db-instance-identifier <DB_INSTANCE_IDENTIFIER> \
  --query "DBInstances[0].PendingModifiedValues" --output json) || exit 1
printf '%s' "$PENDING" | jq -e 'length == 0' >/dev/null \
  || { echo "Pending modifications are queued and --apply-immediately would apply them now:" >&2; printf '%s\n' "$PENDING" >&2; exit 1; }

aws rds modify-db-instance --region <REGION> \
  --db-instance-identifier <DB_INSTANCE_IDENTIFIER> \
  --db-parameter-group-name "$PARAM_GROUP" \
  --apply-immediately >/dev/null || exit 1

aws rds wait db-instance-available --region <REGION> --db-instance-identifier <DB_INSTANCE_IDENTIFIER> || exit 1
```

The block stops on any failure except the expected `DBParameterGroupAlreadyExists` from a previous run,
and it attaches the group only after confirming that its required values are set.

`--apply-immediately` also applies every other modification already queued on the instance (for
example an instance-class change), which can cause an outage before the reboot confirmation below. The
block therefore stops if `PendingModifiedValues` is not empty. Show the user the queued changes and
proceed only with their explicit approval to apply them now, or wait until they are applied or cleared.

The group swap is asynchronous and briefly leaves the instance in `modifying`; the reboot later in
this phase requires the `available` state, so wait for it to settle here before prompting for it.

Pass `--parameters` as **JSON, not shorthand**, on purpose: `shared_preload_libraries` can hold a
comma-separated list (e.g. `pgaudit,pg_stat_statements`), and the CLI's `Key=Value,...` shorthand would
read that comma as a field separator and fail. Don't convert it back to shorthand.

The Terraform equivalent is an `aws_db_parameter_group "datadog_dbm"` (family `postgres<MAJOR_VERSION>`,
with a per-instance `name` like the CLI's `$PARAM_GROUP` to avoid collisions) carrying the four
`parameter` blocks above - `shared_preload_libraries` and `track_activity_query_size` both use
`apply_method = "pending-reboot"` (both need a restart); the other two are `immediate` - and
`parameter_group_name` set on the `aws_db_instance` *only if the instance is managed in the same
Terraform*; otherwise create the group in Terraform and attach with the `aws rds modify-db-instance`
call above.

**If the instance is already on a custom group**, first confirm it isn't shared with other instances.
Modifying it in place changes these parameters for **every** instance attached to it on their next
reboot:

```bash
aws rds describe-db-instances --region <REGION> \
  --query "DBInstances[?DBParameterGroups[0].DBParameterGroupName=='<CURRENT_PARAM_GROUP>'].DBInstanceIdentifier" \
  --output text
```

If that lists only the target instance, modify *that* group in place; do **not** create or swap groups,
or you drop its existing settings on reboot. If it lists **other** instances, stop and ask the user:
either they accept that the DBM parameters will apply to all of them, or clone the group for this
instance only (create `datadog-dbm-<DB_INSTANCE_IDENTIFIER>-pg<MAJOR_VERSION>` as in the `default.*`
branch above, seeded from this group's parameters, then attach it with the same `PendingModifiedValues`
check). Don't silently reconfigure
instances the user didn't choose to onboard.

```bash
aws rds modify-db-parameter-group --region <REGION> \
  --db-parameter-group-name <CURRENT_PARAM_GROUP> \
  --parameters '[
    {"ParameterName":"shared_preload_libraries","ParameterValue":"<SHARED_PRELOAD_LIBRARIES>","ApplyMethod":"pending-reboot"},
    {"ParameterName":"track_activity_query_size","ParameterValue":"<TRACK_ACTIVITY_QUERY_SIZE>","ApplyMethod":"pending-reboot"},
    {"ParameterName":"pg_stat_statements.track","ParameterValue":"all","ApplyMethod":"immediate"},
    {"ParameterName":"track_io_timing","ParameterValue":"1","ApplyMethod":"immediate"}
  ]'
```

(If the user manages that custom group in Terraform, add these parameters to its existing
`aws_db_parameter_group` resource, leaving their other parameters intact.)

**Reboot** so the static parameters load. The reboot briefly drops connections - **tell the user and
get explicit confirmation before running it**, and offer a maintenance window for production
instances. Only after they confirm:

```bash
aws rds reboot-db-instance --region <REGION> --db-instance-identifier <DB_INSTANCE_IDENTIFIER> || exit 1
aws rds wait db-instance-available --region <REGION> --db-instance-identifier <DB_INSTANCE_IDENTIFIER> || exit 1
STATUS=$(aws rds describe-db-instances --region <REGION> --db-instance-identifier <DB_INSTANCE_IDENTIFIER> \
  --query "DBInstances[0].DBParameterGroups[0].ParameterApplyStatus" --output text)
echo "ParameterApplyStatus: $STATUS"
[ "$STATUS" = "in-sync" ] || { echo "Parameters are not applied yet; wait and re-check before continuing." >&2; exit 1; }
```

## Phase 3A: Managed Agent (CloudFormation) - "Quick Install" equivalent

Follow **`references/managed-cloudformation.md`** (A1 RDS admin secret, A2 network access, A3 managed ECS
cluster, A4 per-instance DBM Agent service). Read it now, then go to **Phase 4**.

## Phase 3B: Self-managed database bootstrap and existing Agent

Follow **`references/existing-agent.md`** (B1 network access, B2 password secret, B3 monitoring user and
grants, B4 existing Agent check). The existing-Agent path runs all of B1-B4; the Terraform path runs only
B2 and B3 when C1 sends it there. Then go to **Phase 4**.

## Phase 3C: Terraform-provisioned Agent

Follow **`references/terraform.md`** (C1 secret and check-config contract, C2 runtime-specific Terraform,
C3 plan, approve, and apply). C1 sends the flow through B2/B3 in `references/existing-agent.md` before
returning to C2. Then go to **Phase 4**.

## Phase 4: Verify and Report - all paths

Confirm DBM data is flowing - verify a **DBM-specific** metric, not just a base connection. The
location-independent check is the Datadog-API query (prefer it):

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | tr -d '\r' | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
# Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"; : "${DD_APP_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
printf 'DD-API-KEY: %s\nDD-APPLICATION-KEY: %s\n' "$DD_API_KEY" "$DD_APP_KEY" |
curl -H @- -s -G "https://api.${DD_SITE}/api/v1/query" \
  --data-urlencode "from=$(($(date +%s) - 900))" \
  --data-urlencode "to=$(date +%s)" \
  --data-urlencode "query=avg:postgresql.queries.count{dbinstanceidentifier:<DB_INSTANCE_IDENTIFIER>}"
```

A non-empty `series` for `postgresql.queries.count` confirms **DBM query metrics** are flowing (the
Agent is reading `pg_stat_statements`) - not just that the base check connected. Also confirm on the
Databases page that **query samples and explain plans** appear. For the **managed** path, check the ECS
service and the `datadog-managed-dbm` CloudWatch logs if nothing shows. For the **Terraform** path, inspect
the Terraform-owned ECS/EC2/EKS runtime and its logs as described in C3. For the **existing-Agent** path,
`sudo datadog-agent status | grep -A 20 postgres` on the Agent host should show the check healthy with
no `pg_stat_statements` / `pg_stat_activity` errors (via SSM or the user).

### Wrap Up

After verification, make one best-effort completion callback so the Datadog UI can finish this flow.

`DD_WORKFLOW_ID` is the UUID of the Datadog user the credentials belong to, which is how the UI
correlates this callback. Resolve it and post in **one** command: many agent runtimes start a fresh
shell per command, so a variable assigned in an earlier one would be empty here.

**Never print the `current_user` response**: it also carries the user's name, handle, and email. If no
JSON parser is available, skip this callback rather than installing one or blocking setup.

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | tr -d '\r' | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
# Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"; : "${DD_APP_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
dd_headers() { printf 'DD-API-KEY: %s\nDD-APPLICATION-KEY: %s\n' "$DD_API_KEY" "$DD_APP_KEY"; }
DD_WORKFLOW_ID="$(dd_headers | curl -H @- -fsS --connect-timeout 5 --max-time 20 \
  "https://api.${DD_SITE}/api/v2/current_user" | jq -er '.data.id')" \
  && dd_headers | curl -H @- -sS --connect-timeout 5 --max-time 20 -X POST \
  "https://api.${DD_SITE}/api/unstable/integration/aws/workflow/agentic_dbm" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{"data":{"type":"integration_setup_status","id":"'"${DD_WORKFLOW_ID}"'","attributes":{"status":"finished","step":"setup_complete"}}}'
```

Do not retry or block setup if this callback fails.

Congratulate the user and give them a short summary of what was set up:

- The instance (`<DB_INSTANCE_IDENTIFIER>`, region, endpoint) and the install path used (managed
  CloudFormation, Terraform-provisioned, or existing Agent).
- What Phase 2 changed on the parameter group (which group, which parameters, whether a reboot ran), or
  that no change was needed.
- The Secrets Manager secrets created or reused, by name - never their values.
- The result of the `postgresql.queries.count` check above.

Then link (construct as `<APP_BASE>/...`, from the Phase 0 App URL table):

- **Database Monitoring**: `<APP_BASE>/databases` - query metrics, samples, explain plans.
- **Databases list**: `<APP_BASE>/databases/list` - per-database health.
- The instance also appears under the **RDS integration** dashboards for infrastructure metrics.

**Suggested next steps:** monitors for connection saturation, replication lag, and slow queries;
repeat for other instances, or set up DBM for other engines (MySQL, SQL Server).

## Important Notes

- **Three paths, one prerequisite.** The managed path (Phase 3A) deploys a Datadog Fargate Agent and
  bootstraps the `datadog` user in-VPC; the existing-Agent path (3B) reuses an Agent; the Terraform path
  starts in 3C, runs the shared B2/B3 bootstrap, and returns to provision the Agent/networking. **All
  three still need `pg_stat_statements` enabled (Phase 2)** - the managed
  installer does *not* set the RDS parameter group, so this skill adds it.
- **Preserve existing DB config.** Append `pg_stat_statements` to `shared_preload_libraries`, never
  replace it. Modify an existing custom parameter group in place; only create+attach a new group for
  `default.*` groups. `shared_preload_libraries` and `track_activity_query_size` need a reboot.
- **Per-database (Terraform and existing-Agent paths).** `CREATE USER` / `GRANT pg_monitor` are cluster-wide (once); the
  schema, USAGE grants, extension, and `explain_statement` function must be created in *every*
  monitored database. Keep the function's `SET TRANSACTION READ ONLY` guard.
- **Secrets.** Managed path: an RDS *admin* secret (JSON `{username,password}`) the in-VPC installer
  uses to bootstrap the `datadog` user. The installer re-runs on every task launch, so keep this secret
  valid (scope it to the ECS execution role; if you rotate the master password, update the secret too) -
  it is not one-time, and dropping it or setting `SkipInitialize=true` without a `DatadogUserSecret`
  breaks the Agent. To avoid standing master creds, use the self-managed `DatadogUserSecret` +
  `SkipInitialize=true` path from the start instead. Terraform/existing-Agent paths: the `datadog`
  user's password is JSON read via the `aws.secrets` backend on whichever Agent runs the check,
  referenced as `ENC[...;password]`; grant that Agent's role `secretsmanager:GetSecretValue`.
  Terraform owns only empty secret containers and IAM; seed values out-of-band. Never inline a password,
  encode it into a runtime definition, or commit it to Terraform state.
- **Managed/Terraform-Fargate networking.** The Fargate Agent's subnets must be ECS-capable (outbound to ECR /
  Secrets Manager / Datadog via NAT or VPC endpoints) and route to the RDS - not the RDS DB subnet
  group's isolated subnets. Open the RDS security group to the Agent's SG on the **actual DB port**,
  not a hard-coded 5432.
- **Execution model.** This skill runs in the user's shell, which directly reaches only Datadog and
  AWS control-plane APIs. The managed path stays entirely within that boundary. The Terraform and
  existing-Agent paths' `psql` grants and host `conf.d`/`datadog-agent status` run from a DB-reachable
  host - agentless via SSM or by the user, never over SSH and never from the local machine unless it has
  verified network reachability.
- The `datadog` user is **read-only** (`pg_monitor`) and never modifies data.
