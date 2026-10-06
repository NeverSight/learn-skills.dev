---
name: aizen-init
description: "Bootstrap a team backend project from a GitHub/GitLab repo and the project documents, in 11 strict sequential steps with review checkpoints (v3) - Git Flow (develop + feature branches), an approved plan in .aizen/runs/init/plans/, backend skeleton with /health and /health/ready, multi-stage Dockerfile + compose with all infrastructure, .env/.env.example + one central config, fail-fast infrastructure connections, adapters behind interfaces (logger included), AOP layers, request-id middleware, authentication/authorization, a full README, then a graphify review against the documents before handover. Use when starting/bootstrapping a new backend project for a team (khởi tạo dự án backend, dựng khung backend, init backend, setup docker compose + health check, bắt đầu dự án backend cho team). Not for: a feature, bug fix, pipeline or schema in an existing project (aizen-build)."
---

# aizen-init — bootstrap a team backend project (v3)

Takes a repo URL + project documents and delivers a running backend skeleton: architecture, Docker, infra
connections that must succeed, cross-cutting layers, README — step by step, each step gated and reviewable.

**Read first:** `rules/hard-rules.md`, then `references/core/rules.md` and `references/core/mcp.md` (aizen-core).
Stack, Docker and pipeline knowledge comes from the Aizen packs: `references/backend/stacks/java.md` ·
`references/backend/stacks/python.md` · `references/backend/stacks/typescript-nestjs.md` (with their vendored
Spring Boot / FastAPI guides), `references/infra/platforms/docker.md`, `references/infra/secrets.md`.

`<SKILL_DIR>` = this skill's folder; `<P>` = the project root (the local clone). All agent files go in `<P>/.aizen/runs/init/`.


## Run contract (enforced by the guard)

`<CORE_DIR>` = the aizen-core folder next to this skill. The run is `init`: `uv run "<CORE_DIR>/scripts/core/guard.py" start --skill aizen-init --run init --goal "<project>"` before `check_inputs.py`. At each checkpoint `uv run "<CORE_DIR>/scripts/core/guard.py" ask --run init --question "<what to approve>"`, stop; on the owner's ok `uv run "<CORE_DIR>/scripts/core/guard.py" go --run init --text "<their words>"` and set `Approved: yes`.
- Fill `.aizen/runs/<RUN>/sheet.md` as you go: tick a step only with evidence the guard can check —
  `file:<path>` · `cmd:<the command you ran>` · `out:"<a line it printed>"` · `sha:<commit>` · `url:<source cited in the output>`.
- The Stop hook runs the contract (`manifest.json` → `contract`): open items → you continue with the exact list.
  `uv run "<CORE_DIR>/scripts/core/guard.py" check --run <RUN>` shows it any time. A step that truly does not apply:
  `uv run "<CORE_DIR>/scripts/core/guard.py" waive --run <RUN> --step <id> --reason "…" --evidence <file | real output>`.
- The contract runs `gate.py 11`: every step report, checkpoint approval and artifact.
- Never write `run.json`, the ledger, waivers or evidence yourself, and never say "done" — the guard marks the run
  done and archives it.

## Workflow

Run steps **in order**. Before each step run the gate; it must exit 0:

```bash
uv run "<SKILL_DIR>/scripts/gate.py" --project <P> <step>
```

After each step write `.aizen/runs/init/reports/step-<N>.md` (`assets/report-template.md`) with `Status: done` and the
evidence, update the plan row, commit on the step branch, merge into `develop`. At a **checkpoint** (1, 5, 9, 10)
stop, show the report, and wait for the user's "ok"; then set `Approved: yes`. Done criteria per step:
`references/step-checklist.md`.

**Pre-step — inputs.** Need a GitHub/GitLab repo URL and the detailed project documents. Missing either → ask
for it and stop. Then:
`uv run "<SKILL_DIR>/scripts/check_inputs.py" --project <P> --repo <url> --docs <file|dir|url> [...]`
— creates `.aizen/runs/init/{plans,reports,graphify}`, writes `.aizen/runs/init/inputs.md`, adds the agent entries of
`assets/gitignore-agent.txt` to `<P>/.gitignore`.

0. **Git.** `git init`, `git remote add origin <url>`, `git fetch`. Remote already has code → stop, list what
   is there, ask: continue on it or abort. Create `main` (if absent) and `develop`; every later step works on
   `feature/init-<N>-<slug>` from `develop` and merges back with `--no-ff`. Conventional Commits. Never push
   without asking for that push.
1. **Read docs → plan. CHECKPOINT.** Extract stack, conventions, architecture, infrastructure, auth model, tools.
   Anything the docs leave open → list it as a question; never pick for the user. Write the plan from
   `assets/plan-template.md`; show it; revise and re-ask until "ok".
   1.1 Save it as `.aizen/runs/init/plans/plan.md` — one task row per step 2–10 (owner, depends on, done criteria,
   status) so dev agents can pick tasks.
2. **Skeleton + health.** Folder layout per `references/architecture-patterns.md`; `GET /health` (liveness,
   no I/O) works locally.
3. **Docker.** Multi-stage `Dockerfile` (dev + prod targets, non-root) and `docker-compose.yml` with the app +
   every planned infra service, each with a `healthcheck`, app `depends_on: condition: service_healthy`.
   Evidence: `docker compose up -d` → `/health` returns 200.
4. **Env + config.** `.env.example` (every variable, safe sample values, one comment each) and `.env` (git-ignored);
   one central config module that reads and validates env once — a missing/invalid variable stops startup with
   its name.
5. **Infra connections. CHECKPOINT.** Connect to each infra service at startup; a failed connection → log it and
   exit non-zero (fail fast, no lazy retry forever). `GET /health/ready` checks each dependency and reports each
   one. Evidence: compose up → ready shows all `up`; stop one service → app fails to start, with the log.
6. **Adapters.** Every external tool (logger, DB/cache/queue clients, mail, storage…) behind an interface /
   abstract class owned by the app; one implementation each, wired in one composition root. Business code imports
   only the interface.
7. **AOP + request-id + auth.** Request-id middleware (reuse incoming `X-Request-Id` or generate, echo in the
   response, carry through the request context, logger adds it by default); AOP layers: request logging, central
   error handling, input validation, timing. Authentication + authorization per the plan (asked default: JWT
   access/refresh + RBAC). Minimal tests: health, missing-env refuses to start, auth guard.
8. **README.** Fill `references/readme-template.md`: structure, resources, every env variable, config, how to run,
   endpoints, troubleshooting. Each variable in `.env.example` appears in README.
9. **Graphify review. CHECKPOINT.** Build the code graph with the `graphify` skill, move its output to
   `.aizen/runs/init/graphify/`, compare against the plan and docs per `references/graphify-review.md`. Fix gaps (on a
   step branch), re-run, report.
10. **Final review. CHECKPOINT.** `gate.py --project <P> 11` exits 0; fresh `docker compose down -v && up` →
    ready all `up`; tests pass; `git status` clean on `develop`. Hand over (Output below) and wait.

## Rules

- Strict order; skip a step only on the user's explicit permission → report `Status: skipped`,
  `Skip-approved-by: user — <their words>`. `rules/hard-rules.md` has the rest.
- Code: the shortest clear code that runs the project. No feature code beyond the skeleton.

## Output (step 10 handover)

```text
Repo: <url> · branch develop @ <sha> · pushed: yes/no
Stack: <…> · Infra: <postgres, redis, …>
Run: cp .env.example .env && docker compose up -d → http://localhost:<port>/health/ready
Steps: 0–10 done (skipped: none) · tests: <n> passed · graphify: <k> gaps found, <k> fixed
Open questions / follow-ups: <…>
Reports: .aizen/runs/init/reports/ · Plan: .aizen/runs/init/plans/plan.md · Graph: .aizen/runs/init/graphify/
```

## Knowledge (load only what the step needs)

| Need | Read |
|---|---|
| done criteria + evidence per step | `references/step-checklist.md` |
| layers, adapters, AOP, request-id, fail-fast startup | `references/architecture-patterns.md` |
| README sections | `references/readme-template.md` |
| graphify run + what to check | `references/graphify-review.md` |
| plan / report / .gitignore templates | `assets/plan-template.md`, `assets/report-template.md`, `assets/gitignore-agent.txt` |
