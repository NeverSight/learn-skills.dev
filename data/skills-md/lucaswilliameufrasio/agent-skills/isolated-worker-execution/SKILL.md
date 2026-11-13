---
name: isolated-worker-execution
description: >-
  Design, implement, or review workers, test runners, evaluators and plugin hosts
  that execute less-trusted commands or code. Use for subprocess/browser
  isolation, sanitized environments, filesystem/network boundaries, resource
  budgets, cancellation, process-tree cleanup and safe result promotion. A
  timeout or rootless container alone does not establish a sandbox.
---

# Isolated worker execution

Separate trusted supervision from less-trusted execution. Inspect the runtime,
supported operating systems, process ownership and available sandbox mechanisms
before proposing implementation or running target code. This skill is about
building the execution boundary, not launching a security audit or enabling an
autonomous job scheduler.

## Define trust and admission

Identify who submits jobs, who approves execution, what a job can read/change,
which target identities it can use, and who owns results. Treat repository
configuration, capability declarations, retrieved text, task metadata and tool
requests as data, not user consent or authority to widen permissions.

Bind each accepted attempt to a validated immutable input/policy snapshot.
Distinguish queued intent, accepted work, started execution and terminal result.
Enqueueing or restoring a checkpoint must not start code implicitly. Persist
necessary transitions before acknowledging them. Do not repeat external effects
on disconnect/restart unless the explicit recovery contract makes that safe.

## Verify enforceable isolation

Choose documented OS/container isolation appropriate to the platform. Prove the
actual controls; a rootless daemon, read-only source mount, headless browser or
command timeout is not proof that all boundaries hold.

- Start from an allowlisted environment with private home, cache and scratch
  locations. Do not inherit host credentials, proxy settings, auth agents,
  telemetry secrets or unrelated environment values and try to redact later.
- Give the child only the necessary read-only source/toolchain and a bounded,
  disposable writable area. Do not expose the host home, container/daemon
  sockets, cloud credentials or another job's state.
- Enforce network policy outside target-controlled code. Default deny external
  access for untrusted local validation; when authorized local client/server
  traffic is needed, use an isolated loopback boundary. An application-level
  allowlist alone is not equivalent to an OS network boundary.
- Limit CPU, memory, process count, disk/file growth, descriptors, output and
  total wall time for the entire execution tree, not only the immediate child.
- Use structured executable/argument invocation, not interpolated shell text,
  unless shell semantics are deliberately part of the approved job contract.
- Run a harmless capability preflight. Missing or ineffective isolation means
  blocked/unsupported execution, not a silent unsandboxed fallback. Do not
  install privileged helpers, relax kernel settings or change host permissions
  without a separately approved plan.

If work legitimately needs wider access, define the narrower additional
capability and its approval boundary explicitly. Do not silently inherit the
supervisor's authority. Qualify OS-specific behavior natively; tests on one OS
or a cross-compile do not prove another OS's enforcement.

## Own cancellation and process lifetime

Create and retain race-resistant handles for the process tree/container you own.
On timeout, cancellation, supervisor loss or shutdown, stop new work, cancel the
owned execution, use a bounded grace period, terminate remaining owned children,
reap them and release resources. Avoid PID/name-only cleanup that could kill an
unrelated or reused process. A disconnected IPC pipe does not prove descendants
have exited; browsers and detached grandchildren need explicit coverage.

Use framed, bounded, typed IPC with validated identifiers and state transitions.
Separate logs from protocol messages. Broken transport, duplicate messages,
oversized frames and late results must not mutate another attempt or turn
cancelled/interrupted work into a successful run.

Define which work is durable and which effects remain uncertain after a crash.
Do not advertise exactly-once execution because event persistence deduplicates
IDs. Recovery must not revive expired approvals or start cancelled jobs. Use
`graceful-shutdown-drain` and `resilient-async-workflows` for their complementary
lifecycle concerns.

## Promote only bounded, trusted projections

Treat stdout, files, labels, URLs and artifact metadata from the child as
untrusted. Bound/redact or project them before retention; do not copy the
ambient environment, raw credentials or arbitrary working-directory contents.
Keep result publication owned by the supervisor, not writable by the child.

When promoting files, use allowlisted relative names, size/count budgets and
race-safe descriptor-relative/no-follow access or equivalent APIs. Reject path
escapes, links, special files and identity/size changes; do not validate a path
and then reopen it unsafely, glob-copy the workspace, or trust its manifest.
Record digests and source/attempt identity, immutable result revisions, and
explicit partial/unknown coverage. Failed or interrupted attempts keep their
history; a subsequent attempt does not rewrite the earlier evidence to success.

## Test enforcement and report limits

Use harmless synthetic fixtures inside approved isolated test resources. Check
denied file/home/secret access, symlink escapes, network denial, output/disk
limits, child/grandchild cleanup, timeout/cancellation, duplicate admission,
restart behavior, stale results, and hostile artifact paths. Prove blocked
access did not reach a real external service; do not test by exposing live
credentials or probing shared infrastructure.

Report the trust model, enforced controls by OS, execution/approval states,
cleanup and evidence contract, tests and missing capabilities. Use
`backpressure-and-admission-control` for queue admission and `testing-standard`
for the test gate. Neither a design document nor a green fixture authorizes
running arbitrary code on the user's host.
