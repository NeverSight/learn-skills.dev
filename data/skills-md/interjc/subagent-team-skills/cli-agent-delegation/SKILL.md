---
name: cli-agent-delegation
description: Outsource well-specified bulk coding work to another vendor's agent through its CLI, a plugin, ACP or an MCP server. Covers OpenAI Codex CLI (codex exec, or OpenAI's Codex plugin for Claude Code), Google Antigravity (agy, with or without the agy-staff plugin) and OpenCode through its Agent Client Protocol server (opencode acp), with fallback ladders, plus onboarding other agents through ACP and its Registry (Grok Build, Cursor, Pi; Gemini CLI is deprecated, use agy). Asks the user which external teams to use and re-checks their capabilities on request. Use this when handing translations, mechanical refactors, test or snapshot backfills, doc syncs or a second-opinion review to an external agent; when running codex, agy or opencode headless; when choosing between them or falling back from one to another; when the user asks which external agents are available or wants to add, drop or verify one; when a liaison dispatches, waits on, resumes or accepts their jobs; or when a dispatch plugin is missing or broken.
license: MIT with Commons Clause v1.0 (see LICENSE)
compatibility: Built for Claude Code (primary) and Codex (secondary) as the host; other hosts are unverified. Needs a shell. The helper scripts need Node.js 18+ (24 recommended); external agents need their own CLIs and accounts (Codex CLI, agy, OpenCode). Run scripts/doctor.mjs first.
metadata:
  version: "0.3.4"
---

# CLI Agent Delegation

Outsourced staff are other vendors' agents run headless. They are cheap or strong, they never get tired of bulk work, and a different model family catches different mistakes. But they cannot ask questions, they do not share your context, and each job carries a fixed start-up cost. This skill is the outsourcing arm of `subagent-team`, where external agents form the fourth layer and each job is tracked by a low-tier in-house *liaison* subagent. Without that skill, still apply the gate below.

This page holds the decisions that apply to every team: gate, team choice, brief, channel ladder, acceptance. Each team's mechanics live in `references/`; read only the page for the team you are about to use.

| You are about to... | Read |
|---|---|
| run Codex CLI, or use OpenAI's Codex plugin | [references/codex.md](references/codex.md) |
| run agy, or use the agy-staff plugin | [references/agy.md](references/agy.md) |
| run OpenCode through ACP | [references/opencode-acp.md](references/opencode-acp.md) |
| add or check any other ACP agent (Grok Build, Cursor, Registry agents) | [references/acp-agents.md](references/acp-agents.md) |
| add a non-ACP CLI or an MCP-fronted agent | [references/other-agents.md](references/other-agents.md) |
| hand a job to a liaison, wait on it, or adapt to a host | [references/liaison-and-hosts.md](references/liaison-and-hosts.md) |
| send a read-only second opinion, especially on sensitive code | [references/read-only-reviews.md](references/read-only-reviews.md) |
| answer "which teams may take work?" or re-verify a team | [references/roster-and-verification.md](references/roster-and-verification.md) |
| judge timings, token costs and past lessons | [references/field-data.md](references/field-data.md) |

## 1. Start

Script paths are relative to this skill's directory. Run `node scripts/doctor.mjs` once per session: it reports the Node version, Codex CLI (and its default effort), agy and agy-staff, OpenCode, and the Codex plugin. Without Node, check `codex --version`, `agy --version` and `opencode --version` by hand. Report blockers to the user; install only with their consent.

Before the first external job, ask the user one multi-select question: which detected teams may take work in this session (each with its channel and what it would do), or none. Skip it when `subagent-team` already asked, the project policy says `External delegation: roster` or `none`, or the run is non-interactive; then state the choice in one line and record it where the team keeps state.

When the user asks to check, add or drop a team ("can Codex take this?", "stop using agy"), follow [references/roster-and-verification.md](references/roster-and-verification.md). Never interrupt running jobs for it.

## 2. Gate: should this be outsourced at all?

For **implementation**, only when **all four** hold:

1. **Fully specified**: what to do and which files are decided; no product or architecture decisions remain.
2. **No risk**: no business code for billing, payment or auth; no data migrations; no concurrency or data-loss paths; mistakes are easy to see and roll back.
3. **Objective acceptance**: runnable commands, or a checklist anyone can tick (key sets, placeholders, line counts, snapshots).
4. **Bulk or repetitive**: translations from a frozen key list, mechanical renames, filling in from a template, homogeneous integrations, snapshot and exhaustive tests, doc and README syncs. A small pure module with no billing or auth role, a frozen signature and hand-checkable cases also qualifies.

If writing the brief costs as much as doing the job (a ten-line edit), do not outsource. Tests and snapshots *for* a sensitive module are fine; the module's business code is not.

**Read-only review is a separate route.** An authorized external reviewer may inspect money, auth, schema and irreversible-data code; the implementation risk and bulk criteria do not bar this. Freeze the review scope and revision, prohibit edits, and require findings with triggers and evidence. For sensitive work use another vendor's strong model at high effort alongside an independent in-house senior review, not as its replacement. Reproduce or verify findings before fixing; acceptance stays in-house. If no authorized external reviewer is available, retain one independent in-house senior review and record the missing external opinion; stricter project review gates still apply. Brief and closure procedure: [references/read-only-reviews.md](references/read-only-reviews.md).

## 3. Which team?

| Work | Choice | Why |
|---|---|---|
| Translations, bulk copy, mechanical replacement, filling in from a template | agy, fast tier (e.g. `gemini-3.8-flash-high`; `-medium` for purely mechanical), or OpenCode with a cheap fast model | Cheapest. agy has about five minutes of fixed overhead per job, so bigger batches pay off more. |
| Large homogeneous implementation from a fixed spec | agy, strong tier (e.g. `gemini-4-argon-medium`/`-high`), Codex at `medium`, or OpenCode with a strong model | Needs steadier reasoning but no decisions |
| Small, bounded code edits with a frozen spec | An external model around the in-house mid tier, at `medium`, if the gate and brief cost justify it | Stronger implementation effort does not remove the need for review |
| Syncs that require reading the code to get right (docs against code, tests following existing patterns) | Codex at `high` | Reads code on its own initiative and checks facts; modest token use |
| Read-only second opinion on a diff or plan | Codex: the plugin's `/codex:review` or `/codex:adversarial-review`, or `codex-run.mjs` in `read-only`; agy's reviewer persona; OpenCode read-only | Another vendor covers blind spots. The verdict stays with your in-house reviewer. |
| A model family none of the others reach (DeepSeek, GLM, Mistral, Kimi, Qwen) | OpenCode through ACP, or another ACP agent after its admission checklist | OpenCode routes to many providers; its tier is the model's tier |

**agy always means picking one of two levels** (the plugin and the CLI alike): a strong model at about your in-house mid tier (e.g. Gemini 4 Argon, roughly Claude Sonnet 5.5), or a flash model one step below that is cheaper and holds up over long batches (e.g. Gemini 3.8 Flash). Name the level at every dispatch. Rules for choosing and escalating: [agy.md](references/agy.md), "Choosing the model: two levels".

Implementation uses `medium` or `high`; a question that seems to need effort above high returns to an in-house expert before more code is written. Risky read-only review uses `high`. Choose by role and risk, not by the channel's default or the size of the diff.

Model names are examples from 2026-10. List what is actually available: `agy models`, Codex's `~/.codex/models_cache.json` (the doctor lists it), `opencode-acp-run.mjs probe` in that directory. Do not use agy or OpenCode to call your in-house family (Claude models under a Claude host, GPT under a Codex host): that routes work back home and adds cost, not perspective. **Gemini CLI is deprecated** (merged into agy): recommend agy. Under a Codex host, Codex CLI is in-house, not an external team.

## 4. Brief

Write the brief to a file in your scratch directory (start from `subagent-team`'s brief template if installed). Outsourcing rules:

- **Fully self-contained.** Paste the spec, the frozen key list, base-language text and insertion points. The agent cannot ask, and may not read paths outside the workspace.
- **Freeze the list first.** Keys or endpoints added after dispatch will not be handled.
- **A file lease plus "must not touch"**: list the files other agents are editing right now.
- **Acceptance commands use executable paths** (`./node_modules/.bin/tsc --noEmit -p .`), not package-manager scripts. Name the execution owner and environment for each check. A sandboxed job may be unable to run them; it reports refusals as not run, and the liaison runs the checks where authorized in-house or escalates the gap.
- **No end-to-end steps.** External CLIs generally cannot drive a browser, a device or the full stack. Acceptance in the brief is static checks and unit or snapshot tests only.
- **"If anything falls outside this spec, stop and explain it in your final reply; do not decide."**
- **Prohibitions**: no state-changing git operations (read-only `git status` / `git diff` is fine), no installs, builds, dev servers or database commands, no reading `.env*`, nothing outside the lease.
- **Report**: files changed and why, uncertain spots, problems noticed but not fixed.

The wrappers need Node.js 18+ and no dependencies; each refuses an older Node with a clear message. Without Node, use the team's raw command (in its reference page).

## 5. Channels and fallbacks

Each team has a preferred channel and a ladder below it. Move down **the same team's** ladder when the problem is the channel (plugin missing or broken, no Node for the wrapper). Move to **another team of the same tier** when the team itself is unavailable (not signed in, quota, network, model retired). The last step is always in-house.

| Team | Preferred | Next | Without Node.js 18+ | Team unavailable |
|---|---|---|---|---|
| Codex CLI | `scripts/codex-run.mjs` for jobs; the Codex plugin's review commands for read-only second opinions | the plugin's `task` runtime with explicit `--model` and `--effort` | raw `codex exec` ([codex.md](references/codex.md)) | OpenCode or agy with a strong model, else in-house |
| agy | agy-staff plugin | `scripts/agy-run.mjs` | raw `agy -p` ([agy.md](references/agy.md)) | OpenCode with a fast model or Codex at `medium`, else in-house |
| OpenCode | `scripts/opencode-acp-run.mjs` | the same with `--agent <project agent>` if the injected agent is not picked up | raw `opencode run --standalone` with the agent injected by hand ([opencode-acp.md](references/opencode-acp.md)) | Codex or agy for the same tier, else in-house |

- A fallback team must still be another vendor than your in-house team, and fit the job's tier (an external-strong job does not drop to a flash model without saying so).
- **Never answer a refusal with looser permissions**: no `danger-full-access`, no retrying agy `--write` with other flags, no `--allow-shell '*'`. Ask the user, or use a channel with a real sandbox or allow-list.
- Say the switch in one line ("Codex quota exhausted; T4.b goes to OpenCode `<model>` · high") and record it on the job's card.
- Two failed rounds on the same work → take it back in-house, whichever team did them.
- Pin model and effort on every call; never inherit a tool's personal defaults. Bound every job with a timeout.
- Separate an environment failure (effort reset, sandbox refusal, startup failure, timeout) from rejected content. Record actual settings when the runner exposes them, the partial diff and missing checks; escalate for the next step instead of blindly raising model strength, loosening permissions or starting a duplicate.

## 6. Acceptance

The job's report is a claim. Acceptance is yours (or your liaison's, for the mechanical steps):

1. `git status --short` and `git diff --stat`: did it stay inside the lease?
2. Run the acceptance commands yourself, even if the external report says they passed. Refused or skipped checks stay pending until an authorized in-house runner executes them; a successful job exit is not proof of acceptance.
3. Content work (translations, copy, examples) is reviewed and edited, not just accepted: key sets identical across languages, `{placeholders}` and escapes such as `\n` preserved, order matching the base file.
4. Docs work: check every verifiable fact (versions, scripts, paths, environment variables, endpoints).
5. Arrange independent in-house content review of the diff, including generated tests and snapshots. Check cases and expected values against the frozen requirements; passing tests can mirror a wrong implementation. Routine review uses mid tier · medium; money, auth, schema and irreversible-data review requires high or top tier · high, on a model other than the author's. Small issues: fix them in-house where the flow allows; larger ones: continue the same job with the concrete failure. **Two failed rounds → take it back in-house.** A liaison only relays failures and never edits code.
6. **End-to-end checks are the director's job.** For user-facing changes, the main agent walks the affected flows on the real stack (browser, device, real API), itself or through an in-house agent that has those tools; a liaison only lists the flows. Treat any end-to-end claim in an external report as unverified.
7. Commit only after acceptance, and only by the director.

## 7. Tracking through a liaison

When the host can run subagents with shell access, give each external job to a cheap in-house liaison instead of waiting in the main session. It dispatches with the exact command from its brief, records job and conversation ids where the team tracks state, never starts a duplicate, waits in **bounded slices** (not on notifications, which may reach the root session instead), runs the mechanical acceptance steps, and sends one rework round with the concrete failure. When a team is unavailable it reports and does not switch teams itself; the layer above picks the fallback (section 5). With the wrapper scripts, use a **fresh `--out-dir` for every round**. Without a liaison, run the wrapper in the background (Claude Code: `Bash` with `run_in_background: true`) and react to the completion notification; never foreground-`sleep` or poll. The wait loop, per-wrapper variants and host notes: [references/liaison-and-hosts.md](references/liaison-and-hosts.md).

The liaison must not finish after dispatch or when one wait slice expires. It stays until the final result is collected and mechanical checks are complete, or explicitly escalates a blocker with job state, ids and the next action. A timeout or unavailable team is an escalation, not permission to resume or switch teams on its own.

Claude Code is the primary host and the one this was tested with (background `Bash` plus completion notifications). Codex is the secondary host. Other hosts that can run shell commands are *unverified*. Status by team: Codex CLI and agy are used in real projects; OpenCode through ACP was checked against OpenCode 2.2.5 on small jobs; every other agent is *not tested for work*.
