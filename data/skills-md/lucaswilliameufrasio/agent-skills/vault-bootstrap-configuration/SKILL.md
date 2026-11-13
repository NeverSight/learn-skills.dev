---
name: vault-bootstrap-configuration
description: >-
  Move application configuration into Vault or an existing secret/configuration
  service end to end, leaving environment variables only for bootstrap and
  required platform inputs. Use for startup, workers, seed/import commands,
  pre-deploy hooks, or requests to stop duplicating settings in deployment envs.
---

# Configure consumers end to end

When the requested contract is configuration through Vault, resolving tokens
alone is incomplete if database URLs, endpoints, or buckets still require
deployment environment variables. Non-secret operational settings may also
belong in the configuration service under that contract.

## Trace the complete dependency graph

1. Inspect repository decisions, configuration loaders, client constructors,
   worker startup, observability initialization, and administrative commands.
2. Separate bootstrap needed to reach/authenticate to the store from operational
   settings. Keep platform-provided inputs such as assigned ports where required.
3. Reuse the actual client's path, authentication, timeout, and response contract.
   Verify historical variable aliases rather than assuming equivalence.
4. Resolve settings before constructing dependent pools and clients. Check seed,
   migrations, importers, and pre-deploy commands as well as the server.
5. Avoid adding activation flags when the approved bootstrap contract already
   suffices. Define and test precedence when migrating existing flags.

## Make failure and adoption deliberate

- Required settings missing or unavailable in configured Vault mode should fail
  before dependent effects, without silently accepting old envs or local defaults.
- Preserve a documented no-Vault local-development mode when intended. Do not
  let it contaminate deployed-mode source selection.
- Follow `vault-namespace-ownership`; a missing service key is not permission
  to read another namespace or environment.
- Follow `runtime-configuration-and-policy` for refresh and client adoption.
  Startup resolution does not prove that rotation rebuilds a live connection pool.
- Follow `secrets-safety`; diagnostics must not expose values. Do not read remote
  Vault data or perform deployment merely to qualify local implementation.

## Evidence and handoff

Test the real client against a local fake store with only bootstrap inputs.
Cover server and commands, missing keys, outage, precedence, local-mode behavior,
and prohibited fallback. Use real local databases/brokers for their adapters.
Follow `testing-standard` for the complete repository gate.

Update configuration docs and examples with separate bootstrap, required keys,
optional keys, paths, and defaults. Report any consumer still requiring envs;
do not claim “everything is in Vault” while those paths remain unmigrated.

## Deliver operator-ready configuration templates

When new secret-store entries are required, provide a per-environment import
template under the requested task workspace (for example `work/<task>/`).
Inspect the target provider or administrative UI's actual import schema and
environment-selection behavior first; do not impose one product's JSON format,
namespace structure, authentication, or supported environments on another.

- Keep values empty or use the importer's documented safe placeholder behavior;
  put clearly synthetic examples in supported comments, not runnable credentials.
- For every entry, explain purpose, how to obtain/fill it, an illustrative value,
  required/optional/conditional status, and applicable environment/provider rules.
  If the schema lacks comments, provide an accompanying keyed instruction file
  rather than adding unsupported fields.
- Separate bootstrap from operational entries. Do not retrieve real remote
  secrets or populate templates from environment/credential stores.
- Document replacement behavior, empty-value semantics, partial failures, and
  safe recovery. Generating a template does not authorize applying it.
- Exclude fillable credential files from Git and restrict local permissions.
  Do not reread them once an operator has populated real values.
- Validate against the actual parser where available; otherwise verify the full
  schema constraints and disclose that limitation. Check environment key parity,
  required explanations and synthetic examples, then report artifact paths.
