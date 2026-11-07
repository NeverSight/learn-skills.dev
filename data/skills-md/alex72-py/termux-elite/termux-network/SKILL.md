---
name: termux-network
description: Diagnose network problems inside Termux (DNS, TLS certificate errors, clock skew, proxies, binding ports, reaching a Termux server from the phone or LAN) given Android's restrictions on interfaces and low ports. Use when curl, pip, git, or a local server cannot connect, when ifconfig or netstat show nothing, or when TLS reports a certificate not yet valid. Do NOT use for Wi-Fi or carrier faults outside the device, or for sshd specifics (see termux-sshd).
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "low"
  triggers: "termux no internet,dns failure,certificate verify failed,ifconfig empty,cannot bind port,curl failed termux,certificate not yet valid,no internet,dns lookup fails,certificate error,trust error"
---
# Termux Network

## Purpose
Locate a connection failure at the right layer (clock, DNS, TLS trust, proxy, bind address, port range, or the network itself) using checks that work under Android's restrictions.

## When to use
- `curl`, `pip`, `npm`, `git`, or `pkg` cannot connect or time out.
- `SSL: CERTIFICATE_VERIFY_FAILED` or a certificate that is not yet valid.
- A local server cannot be reached from the phone's browser or from another device.
- `ifconfig`, `ip`, or `netstat` print nothing useful.

## When NOT to use
- Faults outside the device (router, carrier, Wi-Fi password).
- SSH-specific access problems: `termux-sshd`.

## Preconditions
Run `sh scripts/check-network.sh` (read-only). Pass a hostname as the single argument only if one outbound request is acceptable.

## Decision tree
1. Check the clock first. A wrong date breaks TLS and package signatures (`not yet valid`). Fix the date in Android settings.
2. TLS errors with a correct clock: confirm the CA bundle exists (`ca_bundle` in the script output; Termux keeps it under `$PREFIX/etc/tls`) and that no proxy or interception certificate is in the path.
3. Name resolution: Termux uses its own resolver configuration, which can differ from Android's Private DNS or VPN settings. Compare behavior with a literal IP address to separate DNS from connectivity.
4. Proxy variables (`http_proxy`, `https_proxy`, `ALL_PROXY`): report which are set, never their values, since values can carry credentials.
5. IPv6 trouble on some networks: retry once forcing IPv4 (`curl -4`) before concluding the host is down.
6. Android restricts listing network interfaces for apps, so empty `ifconfig` or `ip` output is not proof of no network. Test with a real connection instead.
7. Binding a server: ports below 1024 cannot be bound without root; use 1024 or above. Bind `127.0.0.1` for local-only use, `0.0.0.0` to accept LAN clients.
8. Reaching Termux from the phone's own browser works through `127.0.0.1:<port>`. From another device it needs the phone's LAN address, a `0.0.0.0` bind, and a network that does not isolate clients.
9. A hotspot or guest Wi-Fi often blocks device-to-device traffic. Test on a normal LAN before debugging the server.

## Example
- Situation: pip fails with certificate is not yet valid.
- Without the skill: Adds `--trusted-host` or disables verification.
- With the skill: Checks the clock first, finds the date wrong, asks the user to enable automatic time in Android settings, and re-runs the unchanged command.

## Safety
Read-only by default. Do not print proxy URLs, tokens, or full environment dumps. Never disable TLS verification (`-k`, `verify=False`, `StrictHostKeyChecking=no`) as a fix; at most use it for a single labeled diagnostic probe and say so.

## Verification
Repeat the original failing request and show its status. For a server, request it from the intended client and report the result.

## Handoffs
- `termux-environment` for Android version and side.
- `package-troubleshooting` when only `pkg` or `apt` downloads fail.
- `git-credentials` when the host is reachable but authentication fails.
- `termux-sshd` when the failing service is the SSH server.

## Report
The layer at fault (clock, trust store, DNS, proxy, bind, port, network), the evidence, the single change, and the repeat-request result.
