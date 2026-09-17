---
name: catalyst-job-scheduling
description: "Catalyst Job Scheduling — job pools, immediate/background jobs, and crons (Periodic, OneTime, Calendar, CronExpression) executing Job functions, Webhooks, Circuits, AppSail. Trigger on 'job scheduling', 'job pool', 'jobpool_id', 'submit a job', 'immediate job', 'cron job', 'scheduled function', 'submitJob', 'createCron', 'retry_interval', 'time_of_execution', or errors 'not a job function', 'job_name must contain only alphanumeric'. Replaces deprecated Cron."
metadata:
  version: "2.0.0"
---

# Catalyst Job Scheduling

Job Scheduling runs background work in three pieces: **job pools** (capacity containers), **jobs** (one execution each, submitted immediately via API/SDK/MCP), and **crons** (schedulers that submit jobs on a timetable). Every fact in this skill and its references is runtime-verified against a live Catalyst project (Aug 2026) unless marked otherwise.

## Prerequisites

Before any operation, load `references/job-scheduling-basics.md` — it covers the five setup rules that cause most failures: job pool must exist first (no default), targets must be JOB-type functions, all time values in seconds, `job_name` limits, and function-vs-pool memory constraints.

## How It Works

1. **Identify the target type**: Job function (most common), Webhook (any HTTP URL), Circuit, or AppSail. Create/verify a matching-type job pool (Function pools size by `memory` MB; the others by concurrent `number` 1–10).
2. **One-off work → submit an immediate job** (MCP `CatalystbyZoho_Create_Immediate_Job` or SDK `jobScheduling().job().submitJob()`). Recurring or delayed work → create a cron (`CatalystbyZoho_Create_Cron_Job` or SDK `cron().createCron()`) choosing Periodic / OneTime / Calendar / CronExpression. Load `references/job-scheduling-basics.md` for exact payloads for both paths.
3. **Write the Job function handler** `(jobRequest, context)`: initialize the SDK with `catalyst.initialize(context, { scope: 'admin' })`, read inputs via `jobRequest.getAllJobParams()` (all values arrive as strings), and ALWAYS end with `context.closeWithSuccess()` or `closeWithFailure()` — failure is what triggers the retry chain.
4. **For retries, dynamic scheduling, webhook targets, or monitoring**, load `references/job-scheduling-advanced.md` — retry semantics (new job records linked by `parent_job_id`), firing behaviors (Periodic crons fire immediately on create AND update; past-dated OneTime fires instantly; OneTime auto-disables after firing), and observability traps (success/failure counters stay 0; dynamic crons are hidden from list APIs).
5. **Verify by job records, not counters**: `CatalystbyZoho_Get_Job_By_Id` shows `job_status` (`PENDING → RUNNING → SUCCESS | FAILURE`), `execution_time`, `dispatch_delay`, `response_code`. Do not trust cron `success_count`/`failure_count` — they stay 0.

## Security Checklist

- **Never log `jobRequest.getJobDetails()` or `getJobMetaDetails()` wholesale** — at runtime their `headers` contain live credentials (`X-ZC-PROJECT-SECRET-KEY`, `X-ZC-Admin-Cred-Token`). Extract only the fields you need.
- Webhook-target jobs to your own project's function URLs carry those same credential headers; treat webhook receiver logs as sensitive.
- Job functions run with admin privileges — validate/whitelist anything you accept via `params` before using it in queries.
- **Never store secrets in job `headers`/`params`** — `Get_Job_By_Id` / `Get_Cron_Job_By_Id` / `List_All_Crons` return them in plaintext. Never paste a raw cron/job dump into chat, issues, or logs.

## Hallucination Guards

- The SDK enum `CRON_TYPE.CALENDER` ("Calender") is misspelled and **rejected by the server**. Use the string `'Calendar'`.
- `retry_interval` is NOT milliseconds. Seconds, 60–86400. `15 * 60 * 1000` is rejected.
- Immediate jobs and scheduled jobs share the same 15-minute timeout; `context.getMaxExecutionTimeMs()` returns the STRING `"900000"` (`parseInt` before math), while `getRemainingExecutionTimeMs()` returns a number.

## Triggers

- "job scheduling", "job pool", "jobpool", `jobpool_id`, "create a job pool"
- "submit a job", "immediate job", "background job", "run this function as a job", `submitJob`, `Create_Immediate_Job`
- "cron", "cron job", "scheduled function", "schedule a function", "recurring job", `createCron`, `Create_Cron_Job`, `cron_expression`, `time_of_execution`, "Periodic", "OneTime cron", "Calendar cron"
- "retry a job", `number_of_retries`, `retry_interval`, `parent_job_id`, "dunning", "billing schedule", "trial expiry job"
- `pauseCron`, `resumeCron`, `runCron`, `deleteCron`, "pause a cron", "trigger a cron manually", `Submit_Cron_Job`
- Errors: "The given function is not a job function", "job_name must contain only alphanumeric and underscore", "job_name should be within 1-20 char length", "retry interval should be within 60s", "Delete all associated Pre-defined Crons before deleting Job Pool", "memory allocated for the Job Function is higher"
- "webhook job", "call a URL on schedule", `notify_url`

## References

| File | Load when the query is about… |
|------|-------------------------------|
| `references/job-scheduling-basics.md` | Core concepts, job pools, immediate jobs, all 4 cron types, MCP tool workflows, Node SDK calls, Job function handler template, CLI setup |
| `references/job-scheduling-advanced.md` | Retry semantics, dynamic (in-code) cron creation, firing/timing behaviors, webhook-target jobs, notify_url, monitoring/observability, security guardrails, pool capacity rules |
