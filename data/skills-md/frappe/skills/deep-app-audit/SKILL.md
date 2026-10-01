---
name: deep-app-audit
description: Deep audit of a Frappe app for security, correctness, and customization defects. Runs every security scope and every quality rule in a separate agent, verifies each candidate in a fresh context, and compiles one report. User-invoked only - run /deep-app-audit [app path] [options].
disable-model-invocation: true
---

# Deep app audit

This skill audits one Frappe app checkout on three tracks and writes one report:

| Track | Prompts | Id prefix |
|---|---|---|
| Security | the scopes in the area directories of `security/` | `S-A` to `S-L` |
| Security | the posture checks in `security/checks/` | `S-P` |
| Correctness | the rules in `quality/B-correctness/` | `Q-B` |
| Customization | the rules in `quality/A-customization/` | `Q-A` |
| Customization | the checks in `quality/checks/` | `Q-K` |

The id of a prompt is its track prefix and its file id: `security/A-authorization/A02-*.md` is
`S-A02`. `quality/mechanisms/` is background for the quality rules, not a set of prompts.

Both tracks work the same way. `security/_conventions.md` and `quality/_conventions.md` have the
same sections, and each one is the contract for its track: the method, the finding bar, the
severity ladder, the verification steps, and the finding format. The task prompts in `prompts/`
are the same for both tracks, and they point each agent to the conventions of its track.

## How a run works

A run has two parts:

| Part | Who does it | Steps |
|---|---|---|
| Setup: the arguments, the target, the inventory, semgrep, the test site | you, the coordinator | 1 to 4 |
| Tasks: the scans, the checks, the verifications, the report | `scripts/run_audit.py` | 5 |

Setup needs judgement: a bench is different on each machine, and an app has its own actors. So
you do it. The tasks need no judgement to schedule, so a script schedules them. The script starts
each task as a new process of an agent CLI, so each task has a fresh context. A verifier that saw
the scan is not independent, and one context cannot hold 160 scans.

The script does not depend on one model or one harness. `agents.json` maps each task kind to a
command, and a command can be any CLI that takes a prompt and can read files, run commands, and
write a file. The scan and the verify tasks can use different models.

The script:

- runs the tasks in parallel, with one set of test users for each worker
- queues the verifiers of a scan when the scan file lands, most severe first, within the caps
- checks the format of each result file, and runs the task again when the file is missing or
  wrong
- runs the site reset command after each task, and stops when the site stops answering
- writes `run.json` (the state of each task) and `summary.json` (the counts), and starts the
  report when the tasks are complete

Every task writes its result to a file in the run directory. A task whose result file is valid is
complete, so a stopped run continues where it stopped when you start the script again.

Do not audit the app yourself, and do not start task agents yourself.

## 1. Read the arguments

The argument is the app checkout to audit, then options in plain words. With no path, use the
current directory.

| Option | Example | Default |
|---|---|---|
| `only`: id prefixes to run | `S-A`, `Q-B05` | everything |
| `skip`: id prefixes to leave out | `S-L`, `S-P05` | nothing |
| `no checks`: run no whole-surface check | | checks run |
| `no site`: read the source only | | create a site |
| `site`: reuse an existing disposable site | `myapp-audit.localhost` | create one |
| `db root password`: for `bench new-site` | | none |
| `bench`: the bench directory | | found above the checkout |
| `output`: the run directory | | `<target>/../<app>-deep-audit/` |
| `semgrep rules`: a local clone of `frappe/semgrep-rules` | `~/src/semgrep-rules` | clone into the run directory |
| `no semgrep`: do not run the semgrep rules | | semgrep runs |
| `drop site`: drop the created site at the end | | keep it for triage |
| `agents`: the agent commands file | `~/audit-agents.json` | `<run dir>/agents.json` |
| `jobs`: agents that run at the same time | `4` | `16` |
| `max candidates`: verification cap for each scan | `15` | `15` |
| `max verifications`: verification cap for the run | `600` | `600` |
| `timeout`: hours before the run stops | `12` | `8` |

"Only security" is `only: S-`. "Only correctness" is `only: Q-B`. "Only quality" is `only: Q-`.

## 2. Confirm the target

Confirm that the path holds a Frappe app: one package in it holds `hooks.py`. If it does not,
stop and tell the user.

Tell the user in two or three lines what will run: the app, the tracks, whether a test site is
created, the agent CLI and the models, and the approximate agent count. A full run is about 160
scan and check agents, plus one agent for each candidate. It can be several hundred agents. Do
not ask for confirmation when the user gave the path and the options. The command is the opt-in.

The test site needs write access to a bench. When the checkout is not in a bench, or the bench
looks like production, use `no site` and say so.

## 3. Prepare the run

Do this yourself. Change no file inside the app checkout.

1. Resolve the checkout to an absolute path. Record the app package name (the directory that
   holds `hooks.py`) and the short commit hash from `git -C <target> rev-parse --short HEAD`.
2. Find the bench, read-only. A bench directory holds `sites/`, `apps/`, and `Procfile`. An
   installed app is usually at `<bench>/apps/<app>`. Record the Frappe version from
   `apps/frappe/frappe/__init__.py`, and the apps that the target requires (`required_apps` in
   `hooks.py`, `pyproject.toml`) or imports, with the path of each on the bench.
3. Create the run directory. When it already holds `setup.json`, this is a resumed run: read it,
   and skip to the first step that is not complete.
4. Build the entry-point inventory:

   ```
   python <skill dir>/scripts/build_inventory.py <run dir>/inventory.json --root <target>
   ```

   The script is read-only. It needs no bench, no site, and no database. It also loads the
   DocTypes of `frappe` and of the apps that the target requires, when they are next to the
   checkout in `<bench>/apps`. For each such app in another directory, add
   `--doctypes-from <path>`. When it fails, record the error. The audit continues without the
   inventory.
5. Run the Frappe semgrep rules, unless the user gave `no semgrep`. The rules are the source of
   the `semgrep` field of the quality rules, so run them once here, not in each scan.
   1. Get semgrep. When `semgrep` is on `PATH`, use it. Else, when `uv` is on `PATH`, run
      `uv tool install semgrep`, and call semgrep as `uv tool run semgrep`, because the uv tool
      directory is not always on `PATH`. Do not install uv or pip packages in another way.
   2. Get the rules. With the `semgrep rules` option, use that clone as it is. Else, when
      `<run dir>/semgrep-rules` does not exist, clone it:
      `git clone --depth 1 https://github.com/frappe/semgrep-rules <run dir>/semgrep-rules`.
      A clone in the run directory keeps the rules of one run fixed, also when the run resumes.
      Record the short commit hash of the clone.
   3. Scan the checkout, and give each match its bare rule id. Semgrep prefixes the rule id
      with the path of the rules directory, so remove everything up to the last `.`:

      ```
      <semgrep> scan --config <rules>/rules --json --metrics=off --quiet --output <run dir>/semgrep-raw.json <target>
      jq --arg t "<target>/" '[.results[] | {rule: (.check_id | split(".") | last),
        file: (.path | ltrimstr($t)), line: .start.line, message: .extra.message}]' \
        <run dir>/semgrep-raw.json > <run dir>/semgrep.json
      ```

   When one of these steps fails, record the error. The audit continues without semgrep.
6. List the prompts. Include every `*.md` file in the directories from the table above. Exclude
   files whose name starts with `_`. Apply `only` and `skip` to the ids, and leave out the checks
   with `no checks`.
7. Write `<run dir>/setup.json`. `notes` is optional: facts about the app that every agent needs,
   such as a product name that is different from the DocType name.

   ```json
   {
     "target": "/abs/path/to/app", "app": "myapp", "commit": "abc1234",
     "bench": "/abs/path/to/bench", "frameworkVersion": "16.0.0-dev",
     "dependencies": [{"app": "erpnext", "path": "/abs/path/to/bench/apps/erpnext"}],
     "inventory": "/abs/run/dir/inventory.json", "inventoryError": null,
     "semgrep": "/abs/run/dir/semgrep.json", "semgrepRules": "/abs/run/dir/semgrep-rules",
     "semgrepRulesCommit": "def5678", "semgrepError": null,
     "scans": ["S-A01", "Q-B05"], "checks": ["S-P01", "Q-K01"],
     "notes": "In the UI, the DocType Sales Invoice is called Bill."
   }
   ```
8. Get the agent commands. With the `agents` option, use that file. Else, when
   `<run dir>/agents.json` does not exist, copy `<skill dir>/agents.example.json` to it, and set
   each role to the CLI of your own harness when the file has a profile for it. When the file has
   no profile for your harness, or you do not know which CLI you run in, ask the user. The tools
   that a profile allows are the tools that each task agent gets, so do not widen them.

## 4. Start the test site

Skip this step with `no site`. Do it yourself, or give the steps below to one agent. The site
lets verifiers send real requests. Without it, the audit reads the source only.

1. Confirm the bench with `bench --version`, run from the bench directory. When there is no
   bench, continue without a site. Do not install bench or a database server, and do not change
   the configuration of the machine.
2. Get a site. With the `site` option, reuse that site. Confirm first that it is not a
   production site: when it holds real data, stop and continue without a site. Otherwise the
   site name is `<app>-audit.localhost`. When a site with that name exists, reuse it: the audit
   owns that name. Else create it:

   ```
   bench new-site <site> --admin-password audit-admin-pw [--db-root-password <pw>]
   ```

   The command must never stop at a prompt. When it fails, record the error and continue
   without a site. Never create, change, drop, or migrate another site.
3. Install the apps that the target requires, then the target:
   `bench --site <site> install-app <app>`.
4. Create the test users. Each worker of the run gets its own set, so that a task can change its
   users, and the reset after the task cannot disturb another task. Make `jobs` sets, numbered
   from 0. Set `k` has these users, each with the password `audit-user-pw`, `enabled = 1`, and no
   onboarding or password-reset requirement:
   - `milkshake-s<k>-website@example.com`: Website User, no other role
   - `milkshake-s<k>-user@example.com`: plain System User, no other role. When the framework
     derives the user type from the roles, a user with no desk role is a Website User. Then
     create one role `milkshake Desk User` with desk access and no permission, and give it that
     role.
   - `milkshake-s<k>-manager@example.com`: System User and System Manager, to compare with what
     a manager can already do
   - for each role that the app defines (the roles in the permissions of its DocTypes, pages,
     and reports that the framework does not define): two users,
     `milkshake-s<k>-<role slug>-a@example.com` and `-b@example.com`, with that role only. Two
     users of one role let a verifier test access to the records of another user.

   Record the roles that each user has after it is saved. App logic can add a role.
5. Write the reset script, `<run dir>/reset_site.py`, and record its command. The run calls the
   command after each task, with `{slot}` replaced by the set number. The script puts each user of
   that set back to its recorded state: the roles, exactly, `enabled = 1`, the user type, and the
   password. It also sets the Administrator password to `audit-admin-pw` again. It changes
   nothing else, it finishes in seconds, and it does not use `bench console`. For example, run it
   with the Python of the bench from `<bench>/sites`, and call `frappe.init` and
   `frappe.connect` for the site. Run the command once for each set, and confirm that it exits
   with 0.
6. Serve the site in the background: `bench serve --port 8199`, from the bench directory. When
   the site needs a `Host` header, record it.
7. Record the configuration that changes how a control behaves. Read
   `sites/common_site_config.json` and the `site_config.json` of the site. Record at least
   `ignore_csrf`, `developer_mode`, `allow_tests`, `server_script_enabled`,
   `disable_website_cache`, `maintenance_mode`, and every `*_disabled` or `allow_*` key, with its
   value. Mark each key whose value disables or loosens a control as `weakens: true`, with one
   line on the effect. A bench with `ignore_csrf: 1` accepts a cross-site request that
   production rejects, so a 200 from it proves nothing about production.
8. Prove that the site works:
   - `curl -sS -o /dev/null -w '%{http_code}' <base url>/api/method/ping` returns 200
   - a login as `milkshake-s0-user@example.com` through `/api/method/login` returns 200 and sets
     a cookie
   - `bench --site <site> list-apps` shows the app

   When a check fails, continue without a site. A site that half works is worse than no site,
   because verifiers read its errors as evidence.
9. Write `<run dir>/site.json`. `slots` holds one list of users for each set, in set order.
   `notes` holds what every agent must know about the site: for example, that it starts with no
   records.

   ```json
   {
     "ready": true, "site": "myapp-audit.localhost", "baseUrl": "http://localhost:8199",
     "hostHeader": "myapp-audit.localhost",
     "bench": "/abs/path/to/bench", "created": true, "apps": ["frappe", "myapp"],
     "adminPassword": "audit-admin-pw",
     "slots": [[{"email": "milkshake-s0-user@example.com", "password": "audit-user-pw", "actor": "plain System User", "roles": ["milkshake Desk User"]}]],
     "resetCommand": "cd /abs/path/to/bench/sites && ../env/bin/python /abs/run/dir/reset_site.py {slot}",
     "notes": "The site starts with no records.",
     "config": [{"key": "ignore_csrf", "value": "1", "weakens": true, "effect": "CSRF is not checked"}]
   }
   ```

   Without a site, write `{"ready": false, "reason": "..."}`.

## 5. Run the tasks

Start the script from the skill directory, detached from your harness, and send its output to
`<run dir>/run.log`:

```
mkdir -p <run dir>/tmp && [ -e <run dir>/tmp/last-check ] || touch <run dir>/tmp/last-check
setsid nohup python <skill dir>/scripts/run_audit.py <run dir> --agents <agents file> \
  --jobs <jobs> --timeout <timeout> \
  --max-candidates <max candidates> --max-verifications <max verifications> \
  [--only <prefix> ...] [--skip <prefix> ...] >> <run dir>/run.log 2>&1 < /dev/null &
```

Do not run the script as a background command of your harness. A harness often stops a
background command after a fixed time, for example 2 hours, and a run takes longer. The script
has its own time limit, `--timeout`. At that limit, it stops its agents and exits.

Start it once with `--dry-run` first. The dry run starts no agent. It shows the task list, the
command of each task kind, and one full prompt of each kind. Read one prompt, and confirm that
the site, the users, and the paths are correct.

When your harness cannot start a detached process, or does not let you start agent processes,
give the user the command, and stop. They run it, and ask you for the rest of the steps
when it is complete.

While the script runs, do not start agents. The script prints one line for each task that ends.
`<run dir>/run.json` has the state of each task, and `<run dir>/logs/<task>.log` has the output of
each agent. When the script stops before the end, start it again with the same arguments. It
continues with the tasks that have no valid result.

### Tell the user the progress

A run takes hours. Without updates, the user cannot tell a slow run from a stopped run. So check
the progress every 10 to 15 minutes, until the script exits. Use a timer or a wake-up from your
harness. The harness does not tell you when a detached script exits, so each wake-up must start
the next one. When your harness has neither, tell the user how to watch the run themselves
(`tail -f <run dir>/run.log`) and wait for the script to exit.

Each check runs this, from the run directory:

```
kill -0 "$(cat run.pid)" 2>/dev/null && echo "script: running" || echo "script: exited"
grep -E '^(ok|FAIL) ' run.log | tail -n 1
grep -vE '^(ok|FAIL) ' run.log | tail -n 5
jq -r '"complete: \([.tasks[] | select(.ok)] | length), failed: \(.failed | length), verifications left in the cap: \(.verificationsLeft), site down: \(.siteDown), timed out: \(.timedOut)"' run.json
jq -r '"now: \(now | strflocaltime("%F %T")), updated: \(.updated), last progress: \(.lastProgress), deadline: \(.deadline)", (.running | to_entries[] | "attempt running since \(.value): \(.key)")' run.json
find verdicts -name '*.json' -newer tmp/last-check -print0 | xargs -0r jq -r \
  'select(.verdict == "confirmed") | "\(.severity) \(input_filename | split("/")[1]): \(.finding.title)"'
touch tmp/last-check
```

The last two commands show only the findings that were confirmed after the previous check, so no
finding is told twice, also after a restart.

Tell the user in two or three lines:

- the counts: complete, queued, running, and failed tasks
- each new confirmed finding, one line each, with the severity and the id. Say that a person must
  still confirm it.
- a problem: a failed task, a failed reset, or a site that stopped answering

Read only these outputs. Do not open the scan and verdict files, and do not judge a finding: the
report task does that.

Each check must also confirm that the run makes progress:

- **The script exited.** The last line of `run.log` is `=== exit <code>`. When it is not there,
  the script crashed or was stopped. Tell the user the last lines of `run.log`, and start the
  script again with the same arguments.
- **The script does not answer.** The script updates `run.json` every minute. When `updated` is
  more than 5 minutes old, the script is stuck. Stop it with `kill "$(cat run.pid)"`, which also
  stops its agents, and start it again.
- **No task ends.** The script stops an agent at the `timeout` of its agent profile, 1 hour in
  `agents.example.json`. `last progress` is the end of the last agent attempt, or the start of
  the script. So when `last progress`, or an attempt in `running`, is older than that timeout
  plus 15 minutes, the run is stuck. Stop it and start it again, as above.
  When the same stop occurs two times, stop the run, and tell the user.

A restart continues with the tasks that have no valid result. It does not repeat complete tasks.

The script stops when the test site stops answering, because a verifier reads the errors of a
dead site as evidence. Start the site again, confirm it with step 4.8, and start the script
again.

The script exits with 0 when every task is complete. With 1, `run.json` lists the failed tasks.
The report still ran, and names them.

When `run.json` has `"timedOut": true`, the run reached its time limit, and the report did not
run. Tell the user how many tasks are complete, and ask whether to continue. To continue, start
the script again with the same arguments. Each start has a full `--timeout`.

With `drop site`, and only for a site that this run created: stop `bench serve`, and run
`bench drop-site <site> --force`.

## 6. Tell the user

Read `<run dir>/summary.json` and the header and summary table of `<run dir>/report.md`. Tell the
user:

- the path of the report and of the run directory
- the confirmed candidate count for each track and severity, and the refuted and uncertain
  counts, from `summary.json`. The report folds candidates by root cause, so it has fewer
  findings. Read the header of the report for the distinct count.
- the titles of the Critical and High findings, one line each, from the summary table of the
  report
- the test site name, when the run kept one, so that the user can reproduce a finding
- anything the run dropped: a failed task, a candidate that a cap left unverified, a check that
  was `not applicable`, a semgrep step that failed

Do not copy the report into the reply. Do not propose fixes.

When the report task fails, the run directory still holds every result. Tell the user, and offer
to start the script again. It runs only the report.

## Prompts

The task prompts are templates in `prompts/`. The script fills them from `setup.json` and
`site.json`, and saves each filled prompt in `<run dir>/prompts/<task>.md`.

| Template | Used for |
|---|---|
| `context.md` | the start of every prompt: paths, bench, inventory, semgrep, site, users, rules |
| `scan.md` | one scope or rule, which writes `scans/<id>.json` |
| `verify.md` | one candidate, which writes `verdicts/<id>/<n>.json` |
| `check.md` | one whole-surface check, which writes `checks/<id>.json` |
| `report.md` | the report, which writes `report.md` |

`{{name}}` is a value. `{{#if name}}...{{else}}...{{/if}}` keeps one part when the value is set.
The script stops at the start when a template names a value that it does not know. When you
change the result format in a template, change the check in `validate()` in `run_audit.py` too.

## Warning

The output is agent output. A person must confirm each finding before anyone acts on it. Expect
false positives and gaps. A clean report does not prove that the app is secure or correct.
