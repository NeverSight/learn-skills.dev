---
name: set-up-wso2-open-banking
description: WSO2 Open Banking Accelerator setup guide on Identity Server, optionally with API Manager and Streaming Integrator. Covers zip extraction, updates, MySQL config, certificate exchange, and startup.
---

# Setting up WSO2 Open Banking

Set up **WSO2 Open Banking Accelerator** on:

- **WSO2 Identity Server (IS)**
- **WSO2 API Manager (APIM)** (required for OB3, optional for OB4)
- Optional **WSO2 Streaming Integrator (SI)** (OB3 data publishing only)

Rules:

- Collect all inputs first.
- Run steps in order.
- Stop on first failed check/command.
- Use skip logic for optional components.
- Use idempotent checks before destructive actions.

## Guardrails

- Confirm before destructive actions (scripts, keystores/truststores, overwriting configs).
- Do not ask the user to paste secrets.
- Change only the files listed in this workflow.
- Run commands one by one (do not combine all commands into one script).

## Execution contract

1. Do not execute any command until all required non-secret inputs are collected.
2. During input collection, ask one question at a time.
3. For secret values, require environment variables only (never ask to paste raw secrets).
4. When a pre-check fails, stop immediately and report the exact failed check.
5. For optional components (APIM/SI), skip all related steps explicitly and log the skip reason.
6. Always print resolved paths before running commands there.

## Input contract (collect first)

If missing, use defaults.

- `OB_VERSION`: `OB3` or `OB4` (default: `OB4`)

### Version-specific inputs

- If `OB_VERSION=OB3`, use [OB3 inputs](./resources/v3/user-inputs.md).
- If `OB_VERSION=OB4`, use [OB4 inputs](./resources/v4/user-inputs.md).

### Host inputs

- `IS_HOST`: default `https://localhost:9446`
- `APIM_HOST`: default `https://localhost:9443` (required only when APIM is selected)
- `SI_HOST`: default `https://localhost:9444` (required only when SI is selected)

### Database host inputs

- `DB_HOST`: default `localhost`
- `DB_PORT`: default `3306`

### Workspace input

- `WORK_DIR`: absolute path used to create the setup directory (default: `$pwd`)

## Primary workflow (do not reorder)

### 1. Prerequisites

- Run preflight checks:

```bash
java -version
command -v mysql
command -v curl
command -v keytool
command -v unzip
```

- Stop if any required tools are missing.

### 2. Install accelerators into base products

- Create `<WORK_DIR>/wso2-open-banking-accelerator` and `cd` into it.

- Resolve and record canonical paths after extraction:
  - `<IS_HOME>`
  - `<APIM_HOME>` (if `IS+APIM`)
  - `<SI_HOME>` (if OB3 data publishing requested)
  - `<OB_IAM_ACCELERATOR_HOME>` inside `<IS_HOME>`
  - `<OB_AM_ACCELERATOR_HOME>` inside `<APIM_HOME>` (if `IS+APIM`)
  - `<OB_SI_ACCELERATOR_HOME>` inside `<SI_HOME>` (if OB3 data publishing)

- A zip source is a URL if it starts with `https://`; otherwise treat it as a local path. Download only for URLs.

- Extract base product zips into the current directory.

- Unzip accelerators into corresponding base product directories.

- Path resolution rule:
  - `<IS_HOME>`: extracted dir name starts with `wso2is-` and contains `bin`.
  - `<APIM_HOME>`: extracted dir name starts with `wso2am-` and contains `bin`.
  - `<SI_HOME>`: extracted dir name starts with `wso2si-` and contains `bin`.
  - `<OB_IAM_ACCELERATOR_HOME>`: dir under `<IS_HOME>` containing `repository/conf/configure.properties`.
  - `<OB_AM_ACCELERATOR_HOME>`: dir under `<APIM_HOME>` containing `repository/conf/configure.properties`.
  - `<OB_SI_ACCELERATOR_HOME>`: dir under `<SI_HOME>` containing `repository/conf/configure.properties`.

- Verify path existence before continuing:
  - `<IS_HOME>/bin`
  - `<OB_IAM_ACCELERATOR_HOME>/bin`
  - `<APIM_HOME>/bin` and `<OB_AM_ACCELERATOR_HOME>/bin` only if `IS+APIM`

- Version-specific branch:
  - If `OB3`, run [set up IS connector](./resources/v3/set-up-is-connector.md).
  - If OB3 data publishing requested, run [set up data publishing](./resources/v3/set-up-data-publishing.md).

### 3. Update base products and accelerators

- Select relevant update binary by OS:
  - macOS: `wso2update_darwin`
  - Linux: `wso2update_linux`
  - Windows: `wso2update_windows.exe`

- Verify the OS-specific update tool exists in each directory below.
  - `<IS_HOME>/bin`
  - `<OB_IAM_ACCELERATOR_HOME>/bin`
  - `<APIM_HOME>/bin` (if `IS+APIM`)
  - `<OB_AM_ACCELERATOR_HOME>/bin` (if `IS+APIM`)
  - `<SI_HOME>/bin` (if OB3 data publishing)
  - `<OB_SI_ACCELERATOR_HOME>/bin` (if OB3 data publishing)

- If missing, stop and tell the user their WSO2 subscription is likely missing. Ask them to contact [WSO2 Online Support System](https://support.wso2.com/) to download the product or skip updates.

- Verify the required environment variables for the update tool are set. Stop if missing:
```bash
test -n "$OB_AGENT_UPDATE_TOOL_USERNAME"
test -n "$OB_AGENT_UPDATE_TOOL_PASSWORD"
```

- Run the update tool in each directory:

```bash
./<WSO2UPDATE_BINARY> --username "$OB_AGENT_UPDATE_TOOL_USERNAME" --password "$OB_AGENT_UPDATE_TOOL_PASSWORD"
```

### 4. Configure MySQL database

- Verify MySQL >= 8.0 available, stop if not.

- Verify DB credentials are provided via environment variables. Stop if missing:
```bash
test -n "$OB_AGENT_DATABASE_USERNAME"
test -n "$OB_AGENT_DATABASE_PASSWORD"
```

- Verify DB credentials by connecting to the DB. Stop if invalid.

MySQL check example:

```bash
MYSQL_PWD="$OB_AGENT_DATABASE_PASSWORD" mysql -h "$DB_HOST" -P "$DB_PORT" -u "$OB_AGENT_DATABASE_USERNAME" -e "SELECT 1;"
```

- Download compatible JDBC driver (MySQL 8 example):

```bash
curl -L "https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/9.6.0/mysql-connector-j-9.6.0.jar" -o mysql-connector-j-9.6.0.jar
```

- Place the JDBC driver JAR:
  - IS: copy the driver JAR into `<IS_HOME>/repository/components/lib`
  - APIM: copy the driver JAR into `<APIM_HOME>/repository/components/lib`
  - SI: copy the driver JAR into `<SI_HOME>/lib` (if OB3 data publishing requires DB connectivity there)

- Set and verify `DB_USER` and `DB_PASS` in `<OB_IAM_ACCELERATOR_HOME>/repository/conf/configure.properties` match the environment variables. Do not print the values, report only `MATCH` or `MISMATCH` per property. Stop on any `MISMATCH`:
  ```bash
  grep -q "^DB_USER=$OB_AGENT_DATABASE_USERNAME$" repository/conf/configure.properties && echo "DB_USER: MATCH" || echo "DB_USER: MISMATCH"
  ```
>Note: Use `Select-String` on Windows.

- Update the following in `<OB_IAM_ACCELERATOR_HOME>/repository/conf/configure.properties`:
  - DB connection properties
  - Change DB name pattern from current value to `<DATE_PREFIX>_*`
  - Hostnames for IS/APIM/SI
  - `IS_PRODUCT=wso2is-<IS_VERSION>`
  - `PRODUCT_CONF_PATH=repository/resources/wso2is-<IS_VERSION>-deployment.toml`

`<DATE_PREFIX>` uses today's date in `YYYYMMDD`.

- Run IAM Accelerator scripts:

```bash
cd <OB_IAM_ACCELERATOR_HOME>/bin
./merge.sh
./configure.sh
```

- If `IS+APIM`, repeat equivalent configuration + scripts in:
  - `<OB_AM_ACCELERATOR_HOME>/repository/conf/configure.properties`
  - `<OB_AM_ACCELERATOR_HOME>/bin` (`merge.sh`, `configure.sh`)

- If OB3 data publishing is requested, repeat equivalent configuration + scripts in:
  - `<OB_SI_ACCELERATOR_HOME>/repository/conf/configure.properties`
  - `<OB_SI_ACCELERATOR_HOME>/bin` (`merge.sh`, `configure.sh`)

- Create event-notification tables (OB4 only):
  - Check if target tables already exist; skip if present.
  - Run `mysql.sql` from `<IS_HOME>/dbscripts/financial-services/event-notifications` against the consent DB.
  - Default consent DB name: `<DATE_PREFIX>_*consentdb`

### 5. Exchange Certificates

- Follow the [exchange certificates guide](./resources/exchange-certificates.md).

### 6. Start servers and verify basic health

Start order:

1. IS: run the OS-specific startup script in `<IS_HOME>/bin`

```bash
./wso2server.(sh|bat) start
```

2. APIM (optional): run the OS-specific startup script in `<APIM_HOME>/bin`

```bash
./api-manager.(sh|bat) start
```

3. SI (optional): run the OS-specific startup script in `<SI_HOME>/bin`

```bash
./server.(sh|bat) start
```

Verification checklist:

- IS, APIM, and SI hosts and ports are reachable
- No critical errors in selected components logs:
  - `<IS_HOME>/repository/logs/wso2carbon.log`
  - `<APIM_HOME>/repository/logs/wso2carbon.log` (if APIM selected)
  - `<SI_HOME>/wso2/server/logs/carbon.log` (if SI selected)

## Completion criteria (must satisfy all applicable)

- All selected components start successfully.
- Health/port checks pass for selected components only.
- No startup-blocking or critical errors in logs after 30 seconds (e.g., ERROR|FATAL).
- Accelerator configs and DB scripts are applied for selected components.
- Certificate exchange is complete for selected components.

## Failure handling

- On any failed command:
  1. Stop immediately.
  2. Report the exact command, exit code, and path.
  3. Do not continue until user confirms remediation.
