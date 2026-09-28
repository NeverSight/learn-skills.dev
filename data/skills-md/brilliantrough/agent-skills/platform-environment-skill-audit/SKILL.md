---
name: platform-environment-skill-audit
description: Audit accelerator environment skills and platform/cluster docs for personal repository, user, Conda, credential, and validation-artifact leakage; use when republishing CUDA, MUSA, PPU, ROCm, or other server environment guidance for multiple users.
---

# Platform Environment Skill Audit

Use this skill before sharing a machine-specific accelerator skill or cluster
runbook with another user or host.

## Audit scope

Inspect the skill, every file it links to, and the commands it asks an agent to
run. Separate portable guidance from local facts.

Search for:

- personal usernames, initials, home directories, repositories, branches, and
  experiment names;
- absolute data, checkpoint, result, cache, Conda, Toolkit, and runtime paths;
- hostnames, IP addresses, ports, mount names, account names, and scheduler
  partitions;
- credentials, tokens, proxy URLs, private package indexes, and shell history;
- validation outputs that expose PIDs, job names, model names, or private data;
- claims copied from another host without a current-host validation date.

## Classification

Classify each fact as one of:

```text
portable       valid for any supported installation
local-platform valid only for the named host or homogeneous host class
workload       belongs to one repository or experiment
sensitive      must not be published
```

Portable skills should use placeholders for user and storage roots. Local
skills may name the host and paths, but must say so in the description and must
not claim that another host has the same state. Workload details belong in the
project, not in a platform skill.

## Specialized accel-* trio (reflux path)

When auditing a specialized `accel-platform-install` / `accel-pytorch-python` /
`accel-pytorch-code-porting` from the agent-skills repo, the platform layer is
meant to be platform-generic but concrete:

- Vendor-standard paths (e.g. `/opt/musa`, `/usr/local/Ascend/...`, `/opt/maca`,
  official versioned user-space prefixes) and platform version facts classify
  as `portable` — valid for any host of that platform following the same
  install. Do not demand placeholders for them; vagueness here is a defect,
  not safety.
- Host-bound facts (user home dirs, this host's `/data` mounts and capacity,
  LVM/raw device names, hostname, IP, local-only tool paths) do not belong in
  the trio — move them to the host-layer skill (`<host>-environment` /
  `system-profile` style, named per host, never refluxed). That host-layer
  skill is the "clearly named local platform skill" this audit prescribes.
- Reject the trio only for host-bound facts, credentials, or claims copied
  from another host without a current-host validation date — never merely for
  containing platform-standard absolute paths.

## Required checks

1. Search recursively for old storage roots, usernames, hostnames, credentials,
   and copied validation dates.
2. Resolve symlinks and report broken or cross-user targets.
3. Verify every advertised path exists on the intended host.
4. Confirm package, driver, Toolkit, library, and Python versions live.
5. Distinguish installation success, native linking, single-device compute,
   collectives, and application validation.
6. Remove secrets rather than masking only their display.
7. Re-run the search after editing and report remaining intentional local facts.

Do not rewrite a local skill into vague portable advice when the local facts are
its purpose. Instead, keep a portable install skill and a clearly named local
platform skill with explicit ownership boundaries.
