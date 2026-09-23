---
name: meshcore-packet-capture
description: >-
  Capture MeshCore Companion packets via BLE, serial, or TCP. Do not use this skill for
  unrelated requests; route to the nearest named specialist.
license: MIT
compatibility: Requires Python 3.11+, a MeshCore Companion radio, and the project's runtime dependencies.
---

# MeshCore Packet Capture

Use this skill when operating, configuring, deploying, or troubleshooting [meshcore-packet-capture](https://github.com/agessaman/meshcore-packet-capture), especially requests involving Companion radios, BLE/serial/TCP capture, MQTT publishing, LetsMesh, TOML configuration, Docker, systemd, launchd, or NixOS.

## Scope boundary

This project captures from MeshCore **Companion radios only**. Do not route repeater or RoomServer capture here; use `meshcoretomqtt` instead.

## Operating workflow

1. Identify the transport before changing configuration:
   - `ble`: direct address, device name, or general scan.
   - `serial`: one or more serial ports; the runtime uses the first configured port.
   - `tcp`: host and port, with SDK auto-reconnect enabled by default.
2. Prefer the installed CLI:
   ```bash
   meshcore-packet-capture --help
   meshcore-packet-capture --debug
   ```
   For a checkout, use `python3 -m meshcore_packet_capture` or `python3 packet_capture.py`.
   **Verified CLI boundary (v2.2.0):** the parser exposes `--output`, `--verbose`, `--debug`, `--no-mqtt`, repeatable `--config`, and the neighbors on-demand pair `--neighbors-now` / `--neighbors-exit` (run one zero-hop neighbor discovery + scopes cycle immediately; with `--neighbors-exit`, quit when the cycle finishes). It does not expose `--show-config` or a dry-run flag. Run the exact installed binary with `--help` before documenting or using any other flag; do not invent a configuration-preview command.
3. Configure one IATA code and at least one MQTT broker before expecting network uploads. `LOC` is a placeholder, not a useful deployment identity.
4. Start with `--no-mqtt` when isolating radio connectivity. Add MQTT only after the device captures packets locally.
5. Verify the actual boundary after every change: device connection logs, packet output, broker connection, and service/container status. Do not treat a successful install as proof of a working capture.

**Mutation gate:** when the request is read-only or plan-only, do not present stop/start/edit/delete/restart commands as actions to perform. Describe future mutations separately, label every example as unexecuted, and require target, scope, and rollback confirmation before the first mutation.

## Configuration rules

Configuration precedence is highest to lowest:

1. Real `PACKETCAPTURE_*` process environment.
2. TOML: `/etc/meshcore-packet-capture/config.toml`, then sorted `config.d/*.toml`.
3. Legacy `.env.local`, then `.env` in the working/package directory.

Use `--config PATH` more than once to load only the named TOML files in order. Later files override earlier files. TOML broker blocks merge by `name`; enabled brokers are flattened into sequential `PACKETCAPTURE_MQTT<n>_*` slots. Keep user overrides in `config.d/99-user.toml`.

Minimal TOML shape:

```toml
[general]
iata = "SEA"

[capture]
connection_type = "serial"
# ble_pin = "123456"   # optional six-digit PIN for BLE connections

[serial]
ports = ["/dev/ttyUSB0"]

[[broker]]
name = "home"
enabled = true
server = "mqtt.example.com"
port = 1883
transport = "tcp"
# include_decoded = true   # publish the nested "decoded" object to this broker
# neighbors = true         # publish the neighbors snapshot to this broker

[broker.auth]
method = "password"
username = "user"
password = "secret"
```

Read `references/configuration.md` for the complete option map, broker authentication, topic templates, packet filters, and precedence edge cases.

### Optional feature blocks (v2.1.0+)

- **Payload decoding** (`decode_payloads`, `include_decoded`, `decode_hashtag_channels`, `decode_channel_keys`, `decode_include_public`): adds a nested `decoded` object with plain-text / structured fields. GRP_TXT channel messages are decrypted (sender, text), ADVERTs are parsed (name, role, lat/lon), and human-readable type/route labels plus path are included. Raw fields are unchanged. Direct messages (TXT_MSG) cannot be decrypted by a passive observer. Off by default; opt in per broker with `include_decoded = true` in its `[[broker]]` block.
- **Neighbors publishing** (`neighbors` per broker plus `neighbors_interval_hours`, `neighbors_discover_window`, `neighbors_command_timeout`, `neighbors_scope_timeout`, `neighbors_scope_min_timeout`, `neighbors_scope_gap`, `neighbors_cycle_timeout`, `neighbors_max`, `neighbors_self_scopes`): publishes a periodic zero-hop neighbor table plus each neighbor's region scopes to the `neighbors` topic. Off by default; the cycle only runs when at least one enabled broker sets `neighbors = true`. Requires an IATA (or an explicit `[broker.topics] neighbors`). The interval is clamped to 12–336 hours to match the observer firmware. `--neighbors-now` / `--neighbors-exit` trigger a cycle on demand.
- **Log rotation** (`log_rotation` = off|size|time, `log_max_bytes`, `log_rotation_when`, `log_backup_count`): only applies when an output file is given with `--output`.

## MQTT and authentication

- Brokers are sequential and have no fixed upper limit. A missing `MQTT<n>_ENABLED` terminates discovery, so do not leave a numbering gap.
- Supported transports are `tcp` and `websockets`; use TLS explicitly for secure transport.
- Password auth uses `username` and `password`.
- Token auth uses Ed25519 JWT-style tokens. On-device signing is preferred when a connected radio supports it; Python signing is the fallback when a valid 64-byte private key is available.
- Never put private keys in a public skill, command transcript, committed `.env`, or shared Docker Compose file. Prefer a protected key file or secret injection.
- Topic placeholders are `{IATA}`, `{IATA_lower}`, `{PUBLIC_KEY}`, and `{TOKEN}`. Per-broker topics override global topics. `RAW` is not published unless explicitly configured. Topics per broker: `status`, `packets`, `decoded`, `debug`, `raw`, `neighbors`. The `decoded` topic carries the nested decoded object when `include_decoded` is enabled; the `neighbors` topic carries the periodic neighbor snapshot when `neighbors` is enabled.
- Per-broker `owner` and `email` override the global `capture.owner_public_key` / `capture.owner_email` for token-auth brokers.
- LetsMesh Analyzer brokers require a configured IATA. Do not silently accept the default `LOC` for a LetsMesh deployment.

## Deployment defaults

Legacy hybrid installs are possible: a systemd or launchd unit may wrap a checkout under a user's home directory and load `.env.local`, without `/opt` or `/etc` TOML files. Inspect the running command, working directory, service unit, and environment/config source before choosing the modern managed-install path.

- **Manual/PyPI:** `pipx install meshcore-packet-capture` gives the CLI and does not install a background service.
- **Managed Linux/macOS:** the root bootstrap installer creates `/opt/meshcore-packet-capture`, `/etc/meshcore-packet-capture`, a virtual environment, and a system service. It installs the latest published release by default; use `--tag` or `--branch` to pin.
- **User service (v2.1.0+):** for a local checkout on Linux, `./install.sh --user-service` creates a per-user systemd service that runs from the checkout's `.venv` (pass `--repo-dir PATH` if the checkout is not the script's directory). Config files live in the repo itself (`.env`, `.env.local`, `config.toml`, `config.d/`). Remove with `./uninstall.sh --user-service` from the same checkout; add `--remove-venv` to also delete the local `.venv`. Manage with `systemctl --user status|restart meshcore-packet-capture` and `journalctl --user -u meshcore-packet-capture -f`.
- **macOS BLE:** use the per-user LaunchAgent because Bluetooth permission belongs to the login user. Serial/TCP can use a LaunchDaemon.
- **Docker:** use the published image or `docker compose up -d`; serial needs a device mapping, while BLE generally needs `privileged: true` and may need host networking. Linux is the most reliable container host for hardware access.
- **NixOS:** use `services.meshcore-packet-capture` and rebuild with `sudo nixos-rebuild switch`.

Read `references/deployment-and-troubleshooting.md` for service commands, Docker hardware access, migration/update behavior, and bounded diagnostics.

## Output and verification

Normal mode prints minimal packet information. `--verbose` adds JSON packet data; `--debug` adds connection, retry, packet parsing, and MQTT diagnostics. `--output PATH` writes packet data to a file. Captured records include device identity, timestamp, packet type, route, payload length, raw hex, SNR, RSSI, and a hash. When `decode_payloads` is enabled, records also carry a nested `decoded` object with human-readable fields (channel message sender/text, ADVERT name/role/coordinates, type/route labels).

When troubleshooting, collect evidence in this order:

1. `meshcore-packet-capture --debug --no-mqtt` and confirm a real BLE, serial, or TCP connection.
2. Confirm packet records appear in console or the `--output` file.
3. Enable one broker and inspect broker connection/reconnect messages.
4. Check the resolved environment/config and topic names, without printing secrets.
5. For a managed service, inspect the service's own logs and status. For Docker, use `docker compose config`, `docker compose ps`, and `docker compose logs`.

Do not delete the install directory, state directory, or configuration during diagnosis. The uninstaller is interactive and backs up user configuration, but it still performs destructive removal only after confirmation.

## When not to use

Do not use this skill for MeshCore repeater or RoomServer packet capture, generic MQTT administration, or implementing changes inside the upstream repository. For code changes, use the repository's contribution workflow and verify the project tests separately.

## References

| File | Load when |
|---|---|
| `references/configuration.md` | Writing TOML/env configuration, MQTT topics, authentication, or packet filters |
| `references/deployment-and-troubleshooting.md` | Installing, upgrading, running Docker/systemd/launchd/NixOS, or debugging a failed service |
| `references/source-index.md` | Checking source coverage, version markers, or revalidating this skill against upstream |

## Completion condition

Stop when the selected transport connects, a packet is observed locally, the intended MQTT topic receives data if MQTT is in scope, and the relevant service/container reports healthy. If hardware, credentials, or broker access is unavailable, report that exact unverified boundary instead of claiming success.
