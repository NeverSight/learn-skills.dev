---
name: desk-claude-code-runtime
description: How the desk runs in Claude Code with no permission prompts and no human approval - the plugin layout, the settings.json template (bypassPermissions plus explicit allow and deny rules), the PreToolUse guard that still refuses unsafe writes, the slash commands, headless invocation with claude -p, scheduling, roles as subagents or labelled passes, and how to verify the setup is quiet before switching autonomy on. Use when installing or debugging the desk in Claude Code, when a prompt appears that should not, or when a send is refused.
license: MIT
metadata:
  version: "1.1.0"
  author: SWC Studio
  category: desk
---

# Claude Code runtime

In Grok Bot the desk is seven Bots on a floor. In Claude Code it is one session that plays the seven roles as labelled passes (or subagents from `agents/`), with the same files, the same scripts and the same gate. This skill is the part that is specific to Claude Code: how it loads, why it never asks, and what still says no.

## 1. Layout

```
/workspace/hypergrok/            the plugin checkout (this repository)
  .claude-plugin/plugin.json     plugin id `hypergrok`; marketplace at .claude-plugin/marketplace.json
  agents/                        seven roles, loadable as subagents
  skills/                        twenty-four skills, loadable by name
  commands/desk-cycle.md         /hypergrok:desk-cycle [desk-root]
  commands/desk-status.md        /hypergrok:desk-status [desk-root]
  commands/desk-halt.md          /hypergrok:desk-halt <reason>
  commands/strategy-review.md    /hypergrok:strategy-review <strategy-name> [desk-root]
  commands/paper-record.md       /hypergrok:paper-record <strategy-name> [desk-root]
  hooks/hooks.json, hooks/guard.py   PreToolUse guard (runs for Bash, Edit, Write)
  scripts/                       opening_bell, desk_doctor, policy_gate, desk_send, kill_switch, autonomy_cycle, strategy_engine, engine_backtest, strategy_review, paper_record, strategy_rereview, desk_dashboard
  engine/                        the systematic engine package (universe, data, signals, portfolio, backtest, strategies, alerts, secrets)
  deploy/                        hypergrok-engine.service, Dockerfile, docker-compose.yml, engine.env.example, supervisor-cron.example
  template/claude/settings.json  copy to <desk-root>/.claude/settings.json
  template/claude/CLAUDE.md      copy to <desk-root>/CLAUDE.md
  template/autonomy.json         copy to <desk-root>/autonomy.json and edit
  template/strategy-criteria.json  the strategy gate's written bar; strategy_review.py reads it by default
  template/strategies/           hg-systematic/, copy to <desk-root>/strategies/
/workspace/trading-desk/         the desk root: desk.md, risk-limits.md, autonomy.json, strategies/, proposals/, journal/, autonomy/
```

Install:

```
/plugin marketplace add swcstudiospace/hypergrok-autonomous-desk
/plugin install hypergrok@hypergrok
```

Or point a session at a checkout directly: `claude --plugin-dir /workspace/hypergrok`.

`claude plugin validate /workspace/hypergrok` passes on the v2.4.0 checkout (29 skills including the 5 commands, 7 agents, 1 hook). While the v2.4.0 push to GitHub is pending, the local-path install works today: `claude plugin marketplace add /workspace/hypergrok` then `claude plugin install hypergrok@hypergrok`.

## 2. Why nothing prompts

Three layers, and each is enough on its own for the commands the desk actually runs.

1. **Permission mode.** `template/claude/settings.json` sets `"defaultMode": "bypassPermissions"`. Headless runs pass `--permission-mode bypassPermissions` (or `--dangerously-skip-permissions`, the same thing) explicitly, so a machine without the settings file behaves the same. If an organisation policy sets `disableBypassPermissionsMode`, fall back to `"defaultMode": "dontAsk"`: everything in `allow` still runs silently and anything else is denied rather than prompted, which is the right failure for an unattended desk.
2. **Allow rules.** The same file pre-allows `Bash(python3 *)`, `Bash(curl *)`, `Bash(git *)`, file tools, and `WebFetch` for the two Hyperliquid API hosts. In `default` or `acceptEdits` mode these alone keep the cycle quiet.
3. **The hook.** `hooks/guard.py` answers `allow` for the desk's read-only scripts and `/info` reads, so even a session with no settings file sees no prompt for them.

The deny rules and the hook are what stop "no prompts" from meaning "no limits": see section 3.

## 3. What still says no

`hooks/hooks.json` registers `guard.py` as a `PreToolUse` hook for `Bash`, `Edit`, `Write`, `MultiEdit` and `NotebookEdit`. It reads the tool call from stdin and returns a `permissionDecision`. Deny always wins over `bypassPermissions`; the hook cannot be argued with from inside the session.

| Call | Decision |
| --- | --- |
| `desk_send.py --ticket X` | `allow` only if `policy_gate.py verify` accepts `X.approval.json` now; else `deny` with the gate's reason |
| `desk_send.py ... --dry-run` | `allow` |
| any command containing `https://api.hyperliquid*.xyz/exchange` or `Exchange(` outside `desk_send.py` | `deny` |
| any fund-moving or agent-approving action name (`usdSend`, `withdraw3`, `usd_transfer`, `approveAgent`, `vaultTransfer`...) | `deny` |
| `kill_switch.py resume` | `deny` (the user runs it) |
| a write (`>`, `sed -i`, `tee`, `mv`, `cp`, `rm`, Python `open(..., "w")`) touching `autonomy.json`, `risk-limits.md`, `gate.key`, `sends.jsonl`, `HALT`, `engine-state.json`, `review.json` or `paper-record.json` | `deny` |
| any read or write touching `engine.env` (the service's environment file, which may hold the key or the command that fetches it) | `deny` in `settings.json` |
| a write touching `strategies/*/RULES.md` or `params.json` when that strategy is `status: live` | `deny` (only the user changes a live strategy) |
| any command, `Edit` or `Write` whose content sets `status: live` | `deny` (only the user writes that word) |
| `Edit`/`Write` on those files or on `*.approval.json` / `*.execution.json` | `deny` |
| `opening_bell.py`, `desk_doctor.py`, `policy_gate.py`, `kill_switch.py halt/status`, `check.sh`, `curl .../info`, `git status/log/diff`, `ls`, `cat`... | `allow` |
| anything else | no decision; the permission mode applies |

`template/claude/settings.json` repeats the important denies as permission rules (`Edit(**/autonomy.json)`, `Read(~/.hyperliquid/**)`, `Read(**/gate.key)`, `Read(**/engine.env)`, `Edit` and `Write` on `strategies/*/paper-record.json`), so the key file, the policy and the paper record are protected even if the hook is not installed.

Test the guard without a session:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"curl -X POST https://api.hyperliquid.xyz/exchange"},"cwd":"/tmp"}' | python3 /workspace/hypergrok/hooks/guard.py
python3 /workspace/hypergrok/scripts/test_guard.py
```

## 4. Headless invocation

```bash
cd /workspace/trading-desk
claude -p "/hypergrok:desk-cycle /workspace/trading-desk" \
  --permission-mode bypassPermissions --max-turns 40 --output-format json
```

`scripts/autonomy_cycle.py` wraps exactly that with a lock (`autonomy/cycle.lock`), a heartbeat (`autonomy/heartbeat.json`), a log per cycle (`autonomy/cycles/<UTC>.log`) and a timeout (default 900 s). `--print-command` shows the invocation; `--once` is for cron or systemd timers; `--loop` sleeps `cycle_interval_minutes` between cycles. A stopped cycle leaves nothing half-done that the next cycle cannot reconcile, because intent is in the ledger before any send.

Environment for the session or the timer: `HYPERLIQUID_NETWORK`, `HYPERLIQUID_ACCOUNT_ADDRESS`, and the key resolvable by `engine/secrets.py`: `HYPERLIQUID_PRIVATE_KEY`, else a `HYPERGROK_KEY_COMMAND` that fetches it from a secrets manager, else `HYPERGROK_KEY_FILE` or `~/.hyperliquid/api-wallet.key` (mode 600, owned by the user). The session must never print, copy or `cat` the key; the settings deny reading the key file and `engine.env`, and `desk_send.py` resolves the key only to sign and reports the source, never the value (`desk-operations` section 1).

`/hypergrok:strategy-review <name>` runs `scripts/strategy_review.py` on a strategy folder and reads back the verdict, the failed checks and the worst perturbation; it may set `status: paper` on an eligible folder when the policy is on testnet and never `live` (`desk-strategy-research`). `/hypergrok:paper-record <name>` runs `scripts/paper_record.py`, which compares the strategy's testnet trades with its backtest and writes the signed `paper-record.json` the engine requires before it will run a `live` strategy; the command reports the checks and, on `ready`, the one-line edit the user would make by hand.

Two more cron lines belong beside the cycle's, both in `deploy/supervisor-cron.example`: the weekly `strategy_rereview.py`, which reruns every paper and live strategy's review and demotes one rung on rejection, and the ten-minute `desk_dashboard.py`, which renders the read-only `autonomy/dashboard.html`.

`/loop 15m /hypergrok:desk-cycle` inside an interactive session is fine for watching a few cycles; it stops when the session ends, so it is not the scheduler.

The strategy engine is not part of the cycle: it runs as its own service beside the cron (`deploy/hypergrok-engine.service`, or the Dockerfile and compose file in `deploy/`), reads the same desk root, and writes its own tickets through the same gate and sender. When `autonomy/engine-heartbeat.json` is fresh and the engine is trading, the cycle supervises it per `desk-strategy-engine` section 6 and writes no ticket of its own. Start the engine only after step 5 of section 6 below has passed; `desk-multi-runtime` section 5 has the order.

## 5. Roles in one session

`agents/*.md` are loadable as subagents. Where the runtime allows it, run the analysts and the Strategist as subagents (they only read) and keep the Risk Manager, gate and Execution Trader passes in the main session so the ticket file, approval file and send happen in one place. Where subagents are not available, label each pass in the transcript (`[Risk Manager]`) and in the proposal file. Either way: the Risk Manager pass writes the JSON ticket, the gate script decides, the Execution Trader pass calls the sender, and nobody edits anyone else's section.

## 6. Verifying a quiet, safe setup

Before switching `mode` from `off`:

1. `bash /workspace/hypergrok/scripts/check.sh` passes (structure, manifests, gate and guard tests).
2. `python3 /workspace/hypergrok/scripts/desk_doctor.py --desk-root /workspace/trading-desk` passes, including the autonomy checks (policy valid, gate key present, settings file present, hook registered).
3. `claude -p "/hypergrok:desk-status /workspace/trading-desk" --permission-mode bypassPermissions` completes with no prompt and a sourced brief.
4. A `desk_send.py --dry-run` on a hand-written testnet ticket prints the built action, names the key source it would use, and refuses without an approval.
5. One full cycle on testnet with the user watching the transcript.

If a prompt appears anywhere in 3-5, the desk is not ready: find which layer in section 2 is missing rather than answering the prompt by hand.

## Never

- Never answer a permission prompt on behalf of the user or suggest disabling the hook to get past a `deny`. A deny is the desk working.
- Never put the key in settings, CLAUDE.md, a command file or an environment file inside the repository.
- Never run a cycle in a session whose working directory is the plugin checkout; the desk root is the project.
- Never rely on `/loop` as the scheduler for money.
