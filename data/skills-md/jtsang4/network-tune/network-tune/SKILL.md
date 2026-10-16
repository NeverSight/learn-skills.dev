---
name: network-tune
description: Diagnose and improve Linux server TCP performance over SSH, including BBR, TCP Brutal, queueing, kernel compatibility, and cleanup of existing network tuning. Use for VPS or proxy-server network optimization, congestion-control installation/configuration, and verification or rollback of tuning changes.
---

# Network Tune

Improve the user's actual network path using host evidence. The agent owns diagnosis, implementation, and verification; this skill supplies decision criteria and operational traps, not a preset tuning profile. Use native host tools and current primary documentation. No bundled installer, upstream tuning project, or fixed kernel is required.

## Establish the target

Identify the server, workload, traffic direction, and desired outcome from the conversation and host. A provider's port speed, a configured sending target, and measured application throughput are different quantities. Honor an explicit user-selected rate; do not silently substitute a universal 100/500/1000 Mbps default.

For a proxy, draw the connection legs before choosing a control point. Server-side congestion control affects data the server sends, including replies on accepted connections. It does not change a remote website's sending algorithm or accelerate UDP. Keep proxy topology, credentials, DNS, and address-family choices within the requested scope.

Use existing authorization to complete routine inspection, fixes, installation, and validation. Do not add repeated confirmation gates. Before a disruptive kernel/boot change, establish the need and recovery path; clarify only unresolved downtime or access constraints that materially affect the operation.

## Inspect, decide, execute

1. **Inspect live state and its owners.** Read the relevant kernel, namespaces, route tables/rules, active qdiscs, socket statistics, service configuration, sysctl sources, and persistence mechanisms. Reveal only the proxy fields needed for diagnosis, not credentials or private keys. See [operations.md](references/operations.md) for useful probes and rollback mechanics.
2. **Form a specific hypothesis.** Distinguish transport loss/latency, receiver limits, buffers, CPU, queueing, and application behavior. Choose a small set of changes with an expected effect and a way to detect regression. A healthy baseline may need no tuning. Use [tuning-policy.md](references/tuning-policy.md) for TCP/BBR and legacy cleanup; use [tcp-brutal.md](references/tcp-brutal.md) for Brutal.
3. **Make the change reviewable.** Explain the consequential choices, save the affected files and live values, and prepare targeted rollback. Inspect what an installer will do before invoking it. Small host-specific scripts or units are appropriate for persistence and rollback; the script must implement the decision, not choose a broad policy.
4. **Apply and inspect the result.** Keep dependent operations sequential. Treat rejected parameters, failed routes, failed builds, and service failures as partial operations requiring repair or rollback. Do not suppress them and declare success. For custom kernels or module failures, read [kernel-compatibility.md](references/kernel-compatibility.md).
5. **Verify the intended behavior.** Check new inbound and outbound sockets on the relevant path, service health, connectivity from a fresh SSH session, and a bounded workload. Check persistence through the actual network owner. Distinguish configured, active, measured, and reboot-tested states.

## Operating principles

- Prefer the working kernel unless a required feature or measured problem justifies replacement. `bbr` in a sysctl does not identify the BBR generation.
- Use measured RTT and throughput needs to reason about buffers; do not map regions or provider plans to magic values.
- Clean up only inspected, attributable configuration. Preserve intentional resolver settings, IPv6, policy routes, shaping, and service-specific limits unless the task and evidence call for changing them.
- Never assume `sysctl --system` reverses removed settings, or that deleting a route restores the route it replaced.
- For dynamic-IP personal proxies, global Brutal can be a valid user choice. Explain the shared rate and routing scope, then implement that choice when feasible.
- Reuse existing services where practical. Give new runtime configuration one owner, defined startup ordering, update behavior, and a tested reversal. Avoid competing boot scripts.
- Keep one host's identifiers, compiler version, gateway, and tuning values out of reusable instructions. Verify version-sensitive facts against the running system and upstream sources.

## Finish

Report the applied scope and rate/algorithm, significant cleanup, observed verification, and remaining limits. Give concrete host-specific status, adjustment, and rollback commands. State when client reconnects are needed, when a reboot was not tested, or when a local compatibility patch will need maintenance. Do not claim a speedup from configuration checks or a loopback test alone.

Do not automatically create a separate report, knowledge-vault entry, or ongoing monitor unless requested or required by applicable workspace instructions.
