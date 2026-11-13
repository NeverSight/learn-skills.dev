---
name: vault-namespace-ownership
description: >-
  Choose and review secret-store namespaces by ownership and actual consumers.
  Use when creating, moving, recommending, or resolving Vault secrets, adding
  shared fallbacks, or debugging missing configuration. Shared namespaces require
  intentional shared values, not matching key names or convenience.
---

# Secret namespaces express ownership

Keep service-specific configuration and credentials in the owning service's
namespace. Two services using a key called `DATABASE_URL` or `API_KEY` need not
use the same database, principal, privileges, or rotation schedule.

## Decide the scope before writing

1. Identify the owner, environment, consumers, resource, and permissions.
2. Inspect the real client's path contract and environment isolation. Do not
   invent environment segments or copy another consumer's path convention.
3. Default to the service namespace. A shared namespace is appropriate only
   when multiple consumers intentionally use the same value under an explicit
   ownership and access policy.
4. For shared entries, document consumers, rotation ownership, and impact.
   Sharing an endpoint does not imply sharing its credential.

## Keep resolution boundaries explicit

- Do not introduce universal shared fallback to make missing keys disappear.
  Required service configuration must not silently connect to another resource.
- Distinguish a legacy resolver's behavior from the intended policy. Its ability
  to read shared entries is not a reason to recommend creating one there.
- Preserve intentionally shared integrations with explicit per-key policies;
  do not remove legitimate sharing indiscriminately.
- Errors should identify missing keys and stages, not resolved values.
- Ensure cache keys and refresh paths preserve the namespace boundary too.

Use `secrets-safety` for custody and write operations. Do not retrieve/copy
existing secret values to migrate them. Provision or rotate through an approved
secure path; check consumers and obtain authorization before deleting old entries.

## Verify and report

Use the production client against a local fake secret server. Verify own-key
success, a missing own key with a shared entry present, unavailable service,
cache/refresh isolation, and legitimate shared resolution where allowed.
Report names, paths, and consumers without reading remote credential values.
