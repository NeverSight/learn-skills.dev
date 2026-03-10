---
name: talon
description: Operate Talon, the Rust infrastructure watchdog daemon that supervises the system-bus worker and monitors k8s. ADR-0159.
---

# Talon — Infrastructure Watchdog Daemon

Compiled Rust binary that supervises the system-bus worker AND monitors the full k8s infrastructure stack. ADR-0159.

## Quick Reference

```bash
talon validate         # Parse/validate config + services files, print summary JSON
talon --check          # Single probe cycle, print results, exit
talon --status         # Current state machine position
talon --dry-run        # Print loaded config, exit
talon --worker-only    # Supervisor only, no infra probes
talon                  # Full daemon mode (worker + probes + escalation)
```

## Paths

| What | Where |
|------|-------|
| Binary | `~/.local/bin/talon` |
| Source | `~/Code/joelhooks/joelclaw/infra/talon/src/` |
| Config | `~/.config/talon/config.toml` |
| Service monitors | `~/.joelclaw/talon/services.toml` |
| Default config | `~/Code/joelhooks/joelclaw/infra/talon/config.default.toml` |
| Default services template | `~/Code/joelhooks/joelclaw/infra/talon/services.default.toml` |
| Voice stale cleanup | `~/Code/joelhooks/joelclaw/infra/voice-agent/cleanup-stale.sh` |
| State | `~/.local/state/talon/state.json` |
| Probe results | `~/.local/state/talon/last-probe.json` |
| Log | `~/.local/state/talon/talon.log` (JSON lines, 10MB rotation) |
| Launchd plist | `~/Code/joelhooks/joelclaw/infra/launchd/com.joel.talon.plist` |
| RBAC guard manifest | `~/Code/joelhooks/joelclaw/k8s/apiserver-kubelet-client-rbac.yaml` |
| Worker stdout | `~/.local/log/system-bus-worker.log` |
| Worker stderr | `~/.local/log/system-bus-worker.err` |
| Talon launchd log | `~/.local/log/talon.err` |

## Build

```bash
export PATH="$HOME/.cargo/bin:$PATH"
cd ~/Code/joelhooks/joelclaw/infra/talon
cargo build --release
cp target/release/talon ~/.local/bin/talon
```

## Architecture

```
talon (single binary)
├── Worker Supervisor Thread (only when external launchd supervisor is not loaded)
│   ├── Kill orphan on port 3111
│   ├── Spawn bun (child process)
│   ├── Signal forwarding (SIGTERM → bun)
│   ├── Health poll every 30s
│   ├── PUT sync after healthy startup
│   └── Crash recovery: exponential backoff 1s→30s
│
├── Infrastructure Probe Loop (main thread, 60s)
│   ├── Colima VM alive?
│   ├── Docker socket responding?
│   ├── Talos container running?
│   ├── k8s API reachable?
│   ├── Node Ready + schedulable?
│   ├── Flannel daemonset ready?
│   ├── Redis PONG?
│   ├── Inngest /health 200?
│   ├── Typesense /health ok?
│   └── Worker /api/inngest 200?
│
└── Escalation (on failure)
    ├── Tier 1a: bridge-heal (force-cycle Colima on localhost↔VM split-brain)
    ├── Tier 1b: k8s-reboot-heal.sh (300s timeout, RBAC drift guard, VM `br_netfilter` repair, warmup-aware post-Colima invariants including deployment readiness + ImagePullBackOff pod reset, then voice-agent stale cleanup + launchd kickstart via `infra/voice-agent/cleanup-stale.sh`)
    ├── Tier 2: pi agent (cloud model, 10min cooldown)
    ├── Tier 3: pi agent (Ollama local, network-down fallback)
    └── Tier 4: Telegram + iMessage SOS fan-out (15min critical threshold)
```

## State Machine

```
healthy → degraded (1 critical probe failure)
degraded → failed (3 consecutive failures)
failed → investigating (agent spawned)
investigating → healthy (probes pass again)
investigating → critical (agent failed to fix)
critical → sos (SOS sent via Telegram + iMessage)
any → healthy (all probes pass)
```

## Probes

| Probe | Command | Critical? |
|-------|---------|-----------|
| colima | `colima status` | Yes |
| docker | `docker ps` (Colima socket) | Yes |
| talos_container | `docker inspect joelclaw-controlplane-1` | Yes |
| k8s_api | `kubectl get nodes` | Yes |
| node_ready | kubectl jsonpath for Ready condition | Yes |
| node_schedulable | kubectl jsonpath for spec (taints/cordon) | Yes |
| flannel | `kubectl -n kube-system get daemonset kube-flannel -o jsonpath=...` | No |
| redis | `kubectl exec redis-0 -- redis-cli ping` | Yes |
| kubelet_proxy_rbac | `kubectl auth can-i --as=<apiserver-kubelet-client*> {get,create} nodes --subresource=proxy` | Yes |
| vm:docker | `ssh -F ~/.colima/_lima/colima/ssh.config lima-colima docker ps` | No |
| vm:k8s_api | `ssh ... python socket probe :64784` | No |
| vm:redis | `ssh ... python socket probe :6379` | No |
| vm:inngest | `ssh ... python socket probe :8288` | No |
| vm:typesense | `ssh ... python socket probe :8108` | No |
| inngest | `curl localhost:8288/health` | No |
| typesense | `curl localhost:8108/health` | No |
| worker | `curl localhost:3111/api/inngest` | No |

Critical probes trigger escalation immediately. Non-critical need 3 consecutive failures.

VM probes are witness probes only. They let Talon classify "service alive in VM but dead on localhost" as a Colima bridge split-brain and run bridge-heal instead of full recovery first.

### Dynamic service probes

Add probes in `~/.joelclaw/talon/services.toml` without rebuilding talon:

```toml
[launchd.gateway]
label = "com.joel.gateway"
critical = true
timeout_secs = 5

[http.gateway_slack]
url = "http://127.0.0.1:3018/health/slack"
critical = true
critical_after_consecutive_failures = 3
timeout_secs = 5

[launchd.voice_agent]
label = "com.joel.voice-agent"
critical = false
timeout_secs = 5

[script.gateway_telegram_409]
command = "test $(tail -20 /tmp/joelclaw/gateway.err 2>/dev/null | grep -c '409: Conflict') -lt 5"
critical = true
critical_after_consecutive_failures = 3
timeout_secs = 5

[script.colima_orphan_usernet]
command = "test $(pgrep -f 'limactl usernet' | wc -l) -le 2"
critical = true
critical_after_consecutive_failures = 2
timeout_secs = 5

[script.k8s_disk_pressure]
command = "! kubectl get nodes -o jsonpath='{.items[0].spec.taints}' 2>/dev/null | grep -q disk-pressure"
critical = true
critical_after_consecutive_failures = 1
timeout_secs = 10
```

- `launchd.<name>` passes when `launchctl list <label>` reports a non-zero PID
- `http.<name>` passes on HTTP `200`
- `script.<name>` passes on exit code 0, fails on non-zero (runs via `sh -c`)
- `critical = true` escalates when the probe is marked critical (or after debounce if configured)
- `critical_after_consecutive_failures = N` debounces critical alerts for dynamic probes (default `1` = immediate)
- `http.gateway_slack` uses gateway endpoint `GET /health/slack`, fails (503) when Slack channel is not started, and should be debounced (recommended `3` cycles)
- **Do not probe `http://127.0.0.1:8081/` for `voice_agent` by default** — root returns `503` when idle and causes false SOS noise
- Service-heal pre-cleanup for `voice_agent` now clears stale `uv/main.py` listeners on `:8081` before `launchctl kickstart` to avoid bind conflicts after force-cycles
- Talon hot-reloads service probes when `services.toml` mtime changes (no restart required)
- `kill -HUP $(launchctl print gui/$(id -u)/com.joel.talon | awk '/pid =/{print $3; exit}')` forces immediate reload

### Health endpoint

- `GET http://127.0.0.1:9999/health` returns Talon state JSON
- Gateway heartbeat consumes this as an additional watchdog signal
- Configure via `[health]` in `~/.config/talon/config.toml`

### SOS channel config

- Tier 4 sends to both Telegram and iMessage
- Telegram fields in `[escalation]`:
  - `sos_telegram_chat_id`
  - `sos_telegram_secret_name` (defaults to `telegram_bot_token`)
- Talon now leases Telegram tokens via `secrets lease <name> --ttl ...` (no `--raw`). If you still see `curl: (3) URL rejected: Malformed input to a URL function`, redeploy the latest Talon binary.
- iMessage recipient remains `sos_recipient`

## Launchd Management

**Talon is active as `com.joel.talon`:**
```bash
launchctl print gui/$(id -u)/com.joel.talon | rg "state =|pid =|program =|last exit code ="
```

**Reload binary/config after deploy:**
```bash
launchctl kickstart -k gui/$(id -u)/com.joel.talon
```

**Single owner for worker supervision is mandatory:**
- If `com.joel.system-bus-worker` is loaded, Talon now auto-disables its internal worker supervisor to prevent port-3111 thrash.
- Preferred end-state is Talon-only supervision, but coexistence no longer causes kill/restart loops.

```bash
launchctl list com.joel.system-bus-worker
```

**Legacy services should stay disabled when fully cut over:**
```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.joel.k8s-reboot-heal.plist
```

## Troubleshooting

```bash
# Validate config + service monitor files
talon validate | python3 -m json.tool

# Check what talon sees right now
talon --check | python3 -m json.tool

# Check state machine
talon --status | python3 -m json.tool

# Broken-pipe robustness smoke test (should exit 0)
talon --check | head -n 1 >/dev/null

# Check health endpoint payload
curl -sS http://127.0.0.1:9999/health | python3 -m json.tool

# Check talon's own logs
tail -20 ~/.local/state/talon/talon.log | python3 -m json.tool

# Check launchd
launchctl list | grep talon
tail -50 ~/.local/log/talon.err

# Manual probe test
DOCKER_HOST=unix:///Users/joel/.colima/default/docker.sock docker inspect --format '{{.State.Status}}' joelclaw-controlplane-1
kubectl exec -n joelclaw redis-0 -- redis-cli ping
kubectl auth can-i --as=apiserver-kubelet-client get nodes --subresource=proxy --all-namespaces
kubectl auth can-i --as=apiserver-kubelet-client create nodes --subresource=proxy --all-namespaces
ssh -F ~/.colima/_lima/colima/ssh.config lima-colima 'curl -sS http://127.0.0.1:8288/health'

# Force bridge repair (same behavior Talon uses for split-brain)
colima stop --force && colima start

# Manual voice-agent stale cleanup (same post-gate step k8s-reboot-heal runs)
~/Code/joelhooks/joelclaw/infra/voice-agent/cleanup-stale.sh
```

## Key Design Decisions

- **Zero external deps** — no tokio, no serde, no reqwest. Pure std. Keeps binary at ~444KB.
- **Compiles its own PATH** — immune to launchd environment brittleness (the class of bug that caused the 6-day outage).
- **Worker is a child process** — not a separate launchd service. Signal forwarding prevents orphans.
- **TOML config parsed by hand** — same pattern as worker-supervisor. No dependency just for config.
- **Probes use Colima docker socket** for critical host checks and add VM witness probes over Colima SSH for split-brain detection.

## Related

- ADR-0159: Talon proposal
- ADR-0158: Worker supervisor (superseded by talon)
- `infra/k8s-reboot-heal.sh`: Tier 1 heal script
- `infra/worker-supervisor/`: Original standalone worker supervisor (superseded)
- Ollama + qwen3:8b: Tier 3 local fallback model
