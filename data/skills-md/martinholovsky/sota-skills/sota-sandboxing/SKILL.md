---
name: sota-sandboxing
description: State-of-the-art sandboxing and isolation engineering (2026). Use when designing isolation for untrusted code, untrusted input parsing, multi-tenant workloads, or AI/agent execution — and when auditing existing systems for isolation gaps. Covers least privilege, defense in depth, isolation boundary selection (VM/microVM/gVisor/container/process/WASM), Linux primitives (namespaces, cgroups v2, seccomp-bpf, Landlock, AppArmor/SELinux, capabilities), Docker/OCI and Kubernetes hardening, privilege separation and broker patterns, subprocess hygiene, and agent tool/egress scoping. Trigger keywords — sandboxing, sandbox, isolation, least privilege, container hardening, container escape, seccomp, Landlock, namespaces, gVisor, Kata, Firecracker, microVM, pod security, untrusted code, untrusted input processing, risky parser, privilege separation, WASM sandbox, V8 isolate, agent code execution, egress allowlist, multi-tenant isolation.
---

# SOTA Sandboxing & Isolation

## Purpose

Engineer and audit isolation boundaries so that compromise of a workload —
untrusted code, a parser fed attacker bytes, a tenant, or an AI agent — is
contained by design. The skill encodes 2026 state of the art: allowlist-first
least privilege, boundary strength matched to threat class, kernel primitives
composed correctly, hardened container/microVM deployment, application-level
privilege separation, and agent-specific containment (lethal trifecta, egress
control, ephemeral execution).

Two modes. Pick one explicitly at the start of the task.

---

## BUILD mode

Use when designing or implementing isolation for new or changed workloads.

1. **Classify the threat** before any mechanism talk: untrusted CODE, untrusted
   INPUT, or MULTI-TENANT ([`rules/01`](rules/01-isolation-boundaries.md) §3). State the classification in your output.
2. **Pick the boundary floor** from the decision table in [`rules/01`](rules/01-isolation-boundaries.md); never go
   below it silently. If constraints force a weaker boundary, write the risk
   acceptance into the design.
3. **Enumerate needs first** — files, syscalls, network destinations, CPU/memory/
   wall-clock, credentials. The sandbox config is the needs-list, inverted:
   everything else denied.
4. **Compose layers from the rules files**: kernel primitives ([`rules/02`](rules/02-linux-os-hardening.md)),
   container/orchestrator hardening ([`rules/03`](rules/03-containers-microvms.md)), in-app separation ([`rules/04`](rules/04-process-app-sandboxing.md)),
   agent-specific controls ([`rules/05`](rules/05-ai-agent-sandboxing.md)). Layers must be independent
   (different failure modes), each failing closed.
5. **Make it ephemeral and observable**: one sandbox per trust unit, destroyed
   after; action/egress logs outside the boundary; runtime detection where the
   platform supports it.
6. **Verify from inside**: ship a probe (attempt secret reads, metadata access,
   denied syscalls, egress) and run it in CI. A sandbox is config until tested.

Deliverables: threat classification, boundary choice + rationale, concrete
configs (seccomp JSON, securityContext, run flags, broker interface), the
inside-the-sandbox verification probe, and the residual-risk list.

## AUDIT mode

**Coverage:** every `rules/` file's Audit checklist applies in AUDIT mode. Mark one *not applicable* only with its reason in the report — never skip a file because the thing it checks for is absent, since that absence may be the finding.

Use when reviewing existing code/infra for isolation gaps.

Procedure: inventory workloads touching untrusted code/input/tenants → classify
each → compare actual boundary vs the floor ([`rules/01`](rules/01-isolation-boundaries.md) §3) → walk the relevant
rules-file audit checklists → verify empirically where possible (inspect running
specs, exec probes, grep for `shell=True`/`--privileged`/`docker.sock`/
`automountServiceAccountToken`).

**Severity conventions**
- **Critical** — untrusted code or fully attacker-reachable parsing with no
  effective boundary, or a boundary trivially bypassed by present config
  (`--privileged`, docker.sock mounted, secrets/metadata reachable from inside,
  language-jail-only sandbox, agent with full lethal trifecta and no gating).
- **High** — boundary below the floor for the threat class; a key layer missing
  or fail-open (no seccomp on untrusted code, root user + writable rootfs,
  flat network with no policies, shared sandbox across tenants).
- **Medium** — boundary correct but a defense-in-depth layer absent or weak
  (default seccomp where custom is warranted, missing pids/memory limits,
  broad RBAC, no runtime detection, missing `--` in argv).
- **Low** — hygiene/hardening polish (image not pinned by digest, missing
  `RLIMIT_CORE=0`, audit-only PSA labels, log gaps).

**Finding format**
```
[SEV] <one-line title>
Where: <file:line | resource | runtime evidence>
Threat class: <untrusted code | untrusted input | multi-tenant | agent>
Gap: <which rule (file §rule) is violated and how>
Impact: <what the attacker holds when this is exploited>
Fix: <concrete change — config snippet or pattern reference>
```

Report findings ordered by severity; end with the boundary-vs-floor table for
every workload audited.

---

## Rules index

| File | Read this when... |
|---|---|
| [`rules/01-isolation-boundaries.md`](rules/01-isolation-boundaries.md) | choosing or judging the isolation boundary itself: threat classification (untrusted code vs input vs multi-tenant), boundary strength ranking (hardware > VM > microVM > gVisor > container > process > runtime), defense-in-depth layering, verifying a boundary with a probe, fail-closed, ephemerality, anti-patterns, model inference runtimes and native-object deserialization as named workloads. Read first in every engagement. |
| [`rules/02-linux-os-hardening.md`](rules/02-linux-os-hardening.md) | building or auditing anything on a Linux kernel: namespaces (incl. userns dual nature), cgroups v2 budgets, deny-by-default seccomp-bpf (with JSON fragment + never-allow syscall list), Landlock, capabilities drop-ALL, no-new-privileges, read-only rootfs, AppArmor/SELinux, systemd sandboxing directives. |
| [`rules/03-containers-microvms.md`](rules/03-containers-microvms.md) | Docker/OCI images and run flags (good/bad Dockerfile, prohibited flags/mounts, read-only data mounts, GPU and network-bandwidth limits, published ports vs host firewall, default bridge), choosing gVisor vs Kata vs Firecracker (GPU tenant sharing and memory scrubbing), Kubernetes pod security (restricted PSA, securityContext template incl. AppArmor and procMount, RBAC/service-account tokens, default-deny NetworkPolicy), runtime detection (Falco/Tetragon; device-node and metadata-endpoint alerts). |
| [`rules/04-process-app-sandboxing.md`](rules/04-process-app-sandboxing.md) | isolating risky code inside your own app: sandboxed parser workers for image/PDF/archive handling, broker/privilege-separation pattern, pledge/unveil-style lockdown sequencing, WASM/wasmtime + WASI capabilities, V8 isolates' real guarantees, subprocess hygiene (no shell=True, argv, clean env), macOS (sandbox-exec reality, App Sandbox, ES). |
| [`rules/05-ai-agent-sandboxing.md`](rules/05-ai-agent-sandboxing.md) | any LLM/agent workload: model-generated code execution, prompt injection as confused-deputy, lethal trifecta analysis, the in-sandbox verification probe, tool permission scoping/broker design, per-instance agent identity, MCP server risk and local MCP server sandboxing, developer-machine agent permission baselines, FQDN egress allowlists + DNS exfil, time/memory/output/spend limits, fleet-wide out-of-band kill switch and rollback, high-risk action audit fields and named agent detection thresholds, graduated automatic containment, multi-agent and computer-use containment. |

---

## Top-10 non-negotiables

1. **Classify the threat, then meet the boundary floor**: untrusted code from the
   internet gets gVisor at minimum, microVM preferred — never bare runc, never a
   language-level jail (`01`).
2. **Allowlist, never blocklist**, at every layer: syscalls, paths, capabilities,
   network destinations, tool verbs. Blocklists always leak (`01`,`02`).
3. **Fail closed**: if any sandbox layer cannot be applied, the workload does not
   run (`01`).
4. **No secrets inside the sandbox**: no env keys, dotfiles, cloud metadata,
   orchestrator credentials; privileged actions go through a broker that returns
   results, not credentials (`04`,`05`).
5. **Drop ALL capabilities, `no_new_privs`, non-root numeric user, read-only
   rootfs** — the baseline four for every container and sandboxed process (`02`,`03`).
6. **Resource budgets on every sandbox**: `memory.max` (+swap off), `pids.max`,
   CPU quota, *and* a wall-clock kill — quotas throttle, they don't terminate; GPUs
   granted by count or ID, never all, and bandwidth shaped where tenants share (`02`,`03`,`05`).
   Where no cgroup is available, cap memory with `RLIMIT_DATA`, **never `RLIMIT_AS`**: an AS cap
   kills Go, the JVM and native binaries at startup on legitimate input (`02` R7.2a). On Linux:
   macOS accepts no memory rlimit at all, so there it is a container or an RSS watchdog (`02` R7.2b).
7. **Never mount the Docker/CRI socket; never `--privileged`; never host
   pid/net/ipc namespaces** for anything touching untrusted data (`03`).
8. **Default-deny network egress** with explicit FQDN allowlists; metadata
   endpoint and RFC1918 blocked from untrusted contexts (`03`,`05`).
9. **Sandbox the parser**: attacker-supplied images/PDFs/archives are decoded in
   a one-shot, fd-only, no-network worker — never in the main process; no
   `shell=True`-class subprocess spawning anywhere (`04`).
10. **Ephemeral per trust domain**: one sandbox per session/tenant/input,
    destroyed after; never reused across users; actions logged append-only
    outside the boundary (`01`,`05`).
