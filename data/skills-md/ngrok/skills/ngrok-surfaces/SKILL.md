---
name: ngrok-surfaces
description: How to apply an ngrok endpoint and Traffic Policy on whichever surface the user is actually working in - the agent CLI and ngrok.yml, the ngrok SDKs (Go, JavaScript, Python, Rust), the REST API at api.ngrok.com, the Terraform provider, and the Kubernetes Operator. Routes from signals in the user's project to the right surface, then to that surface's reference file. Other ngrok skills point here once they know what to build. Not a standalone task - load when another skill references it.
license: MIT
metadata:
  author: ngrok
  version: "1.0"
  category: reference
  surface: all
compatibility: Reference skill. Loaded by other ngrok skills; not invoked directly.
---

# Applying ngrok on the user's surface

Job skills decide *what* to build - the endpoint type and the policy, both in `ngrok-engine`. This skill decides *where* to apply it and hands off to the mechanics.

**The configuration itself does not change across surfaces.** The same policy body, the same endpoint URL, the same internal hostname. Only the wrapper differs. So never re-derive a policy because the user switched surfaces; re-wrap it.

## Pick the surface

Read it off the user's project rather than asking:

| Signal | Surface | Reference |
| --- | --- | --- |
| A terminal, a port, "just give me a URL" | agent CLI / `ngrok.yml` | `references/cli.md` |
| `package.json`, `pyproject.toml`, `go.mod`, or `Cargo.toml` with an ngrok dependency; or the endpoint should live and die with the process | SDK | `references/sdk.md` |
| A controlplane creating resources per tenant/sandbox/device at runtime | REST API | `references/api.md` |
| `*.tf` files | Terraform | `references/terraform.md` |
| `Chart.yaml`, `kustomization.yaml`, k8s manifests | Kubernetes Operator | `references/kubernetes-operator.md` |

If none of these is obvious, the CLI is the safe default for a one-off task.

## The axis that actually separates them

Surfaces differ by **when the resource is created and what owns its lifetime**:

- **CLI and SDK** create it at run time, from inside the workload. It lives as long as the agent or process does.
- **Terraform and the Operator** declare it at deploy time, for a set of endpoints known in advance and checked into a repo.
- **The REST API** creates it at run time from outside the workload, for a set that is *not* known in advance - one per sandbox, customer, or device, with thousands of them.

Terraform and the API look interchangeable and are not. "My account has these three endpoints" is Terraform. "Every sandbox gets one" is the API. See `provision-sandbox-access` for the latter.

A single setup often uses two: the API or Terraform provisions the public cloud endpoint, and the CLI or SDK brings up the internal endpoint from inside the workload. They rendezvous on an agreed internal hostname.

## Auth differs by surface

- **CLI and SDK** use an **agent authtoken** (`NGROK_AUTHTOKEN`). It starts agent sessions and nothing else.
- **REST API, Terraform, and the Operator** use an **API key**. It administers the account. The Operator needs both.

These are not interchangeable and have very different blast radii. If a call fails with an auth error, check which credential is in play before rotating anything. See `ngrok-setup`.

## Notes for agents

- Run the commands yourself when you have a shell; hand back the result, not instructions.
- Keep the policy in its own `policy.yaml` and reference it. That is what makes it portable when the user adds a second surface later, which they usually do.
- TCP endpoints are **not** supported by the Kubernetes Operator. If the user needs TCP on k8s, surface that early rather than discovering it late.
- Do not port config between surfaces from memory - the shapes differ enough to fail in ways that look like network problems. Read the target surface's reference file.
