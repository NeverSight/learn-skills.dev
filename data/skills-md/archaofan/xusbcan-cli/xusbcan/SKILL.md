---
name: xusbcan
description: >
  Use when working with xusbcan-cli, xusbcan-mcp, or an xusbcan.toml CAN device
  alias—send, receive, monitor, periodic transmit, scenario, or session setup.
  Also when the adapter vendor/model is still unknown and must be identified
  from config before opening the bus. Load only the matching model reference
  via references/catalog.md; do not preload every vendor page.
license: MIT
compatibility: >
  Python 3.11+. Drivers depend on the backend in config. Progressive disclosure:
  read catalog.md, then at most one model reference.
metadata:
  author: xusbcan-cli
  version: "2.1.2"
---

# xusbcan

## Progressive disclosure (required)

1. Read `interface` or `vendor` / `model` from `xusbcan.toml` (or ask the user). Do not invent a vendor.
2. Open [references/catalog.md](references/catalog.md) and find **one** matching row.
3. Open **only** that model file (if any). Do **not** read other `references/zlg-*`, `vector-*`, or `chuangxin-*` pages in the same turn unless the config names another device.
4. Shared optional pages: [references/examples.md](references/examples.md) (how to call), [references/pitfalls.md](references/pitfalls.md) (contracts + labeled field notes).

On each model page, prefer **Quick start** and **How this backend behaves**. Treat **Field notes** as earlier contributors’ bench reports: they may not reproduce and are not formal “unsupported” claims—match the current symptom before acting.

**Channel is part of open readiness:** Published TOML snippets often use `channel = 0` as a shape. On dual-channel cards, confirm which physical port is wired and that the alias `channel` matches it before opening. Model-page rules (including what not to trust from vendor device-info APIs) live on the catalog-selected page.

Vendor SDK variables and channel rules live **only** on the model page. Copying another card’s env var or timing into this session is wrong.

## Overview

Command names do not change with the vendor. The driver, channel, and `extra` keys do.

- Set `interface` to a backend python-can already declares → opens through CLI/MCP; no model row required.
- `vendor` / `model` are optional shortcuts (channel map or fixed options). If `interface` is set, those shortcuts are skipped.
- A card python-can does not declare needs a backend under `adapters/<vendor>/`. A known interface name does not mean this repo verified that hardware.

Do not invent vendor DLL calls. Do not put machine-local paths or private notes into committed files.

## When to use

- One-shot send, receive, monitor, or status
- A session that stays open (periodic transmit, repeated receive)
- Millisecond scenarios or MCP tool calls
- An offline script that must keep running after the agent exits
- The config names any python-can backend, or the backend is not chosen yet

When not to use: changing product firmware, or editing ignored local design notes.

## Which interface

| Need | Use |
|------|-----|
| One command, then exit | CLI: `list` `send` `receive` `monitor` `status` `periodic` |
| Millisecond send→wait→send | CLI: `scenario --file`, or `xusbcan.scenario.run_scenario` |
| Agent tools / session | MCP: `open_device`, `send_frame`, `receive_frame`, `monitor`, `periodic_start` / `periodic_stop` / `periodic_list`, `set_frame_filter`, `accept_all_frames`, `run_scenario`, `close_device` |
| Hours-long with no agent | One process holding `can.Bus` or a core session |

`receive` / `monitor` accept `--from-id` / `--to-id`. `set_frame_filter` does the same on an open session; `accept_all_frames` restores full reception. CLI `periodic` needs `--duration`. MCP and scenario `periodic_start` need `duration_s` (max 300s) and auto-stop. Longer runs: local resident process, not unbounded MCP.

CLI one-shots open and close each time—do not loop them for a long job. Stdout is one JSON object; branch on `status` and `error.code`. A receive timeout is success with no frame.

## Long-running script shape

Use the config’s `interface` and `channel`. The snippet is a shape only:

```python
import can

bus = can.Bus(interface="socketcan", channel="can0", bitrate=500_000)
task = bus.send_periodic(
    can.Message(arbitration_id=0x123, data=[0x01, 0x02], is_extended_id=False),
    period=0.1,
)
try:
    while True:
        msg = bus.recv(timeout=0.5)
        if msg is not None:
            pass  # handle msg
finally:
    task.stop()
    bus.shutdown()
```

Stop the periodic task before shutdown. For vendor SDK env vars, read the catalog-selected model page—do not assume socketcan.

## Privacy

Public skills may name an env var the backend documents and neutral IDs such as `0x123`. No absolute paths, customer/ECU names, or text from local-only notes. Before `git add` / `commit` in this repo, follow the desensitization checklist in `CLAUDE.md`.

## Maintenance

- CLI/MCP renames → update this file and [examples.md](references/examples.md).
- New card → copy [references/_template-model.md](references/_template-model.md), fill Quick start first, add one row in [catalog.md](references/catalog.md). Keep Field notes short and labeled as non-guarantees. **Do not** grow the YAML `description` with per-model symptoms.
- Keep board-specific notes out of git. Wrapped vendor SDKs → README disclaimer bullet.
