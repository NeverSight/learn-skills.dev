---
name: prismatic-migrate
description: Migrate existing integrations to Prismatic from vendor exports, workflow projects, or bespoke scripts and services. Use when assessing or replacing an existing integration system while preserving its required behavior, including when the source format is unfamiliar or incomplete.
compatibility: Requires Node.js 22+, npm, Prism CLI (npm package @prismatic-io/prism) v11 or higher on PATH, and network access to documentation and packages. Platform operations also require Prismatic authentication and any connections needed for the intended environment.
---

# Migrate an integration to Prismatic

Start from the existing system and the user's desired outcome. Inspect supplied
exports, code, configuration, and examples; research unfamiliar formats and
runtime behavior in official documentation. Follow dependencies that affect the
requested behavior. Keep original evidence available: exports may omit deployed
settings, external code, or operational state. Incomplete evidence is a reason
to investigate and deliver supported work, not invent a missing contract.

For a recognized source, read the relevant runtime and export notes:
[Workato](references/workato.md), [Paragon](references/paragon.md),
[Boomi](references/boomi.md), [Cyclr](references/cyclr.md), or
[Logic Apps](references/logic-apps.md). The [additional sources](references/additional-sources.md)
guide covers n8n, Node-RED, MuleSoft, Make, Tray, and Zapier. These are starting
points for interpreting evidence; unfamiliar and bespoke systems remain in scope.

Establish what needs to survive: relevant transformations, external effects,
customer configuration, failure recovery, and execution-level contracts such as
batch completion, cadence, and acknowledgment boundaries. Distinguish observed behavior,
documented guarantees, assumptions, and agreed changes. When changing execution
boundaries, preserve meaningful ordering and recovery guarantees; idempotent
writes can still be unsafe to reorder. Ask about missing evidence or business
decisions when they materially affect correctness or scope, while continuing
independent work. Routine implementation choices are yours.

When implementing a port, extend the existing Prismatic project or scaffold with
`prism integrations init`.
Use `prism --llms` and command `--help` or `--schema` to discover current
capabilities, including component inspection and manifest generation. Prefer its
generated toolchain. Consult [CNI documentation](https://prismatic.io/docs/integrations/code-native/),
official service contracts, and installed Spectral types. Choose components,
authenticated clients, or custom code by behavioral fit; source steps need not
map one-to-one to target flows. Establish the actual contract behind replacement
dependencies; a configurable endpoint and a mock of an imagined API do not supply
missing behavior. Expose customer-owned choices and credentials as configuration.

Check target execution and state limits where they affect the design. Prismatic
[instance, cross-flow, and integration state](https://prismatic.io/docs/integrations/persist-data/)
are saved after successful execution: assigning a checkpoint before a later failure
does not establish durable progress. Concurrent writers can overwrite state.
Establish the chosen mechanism's actual commit boundary, including trigger-specific
state. Verify recovery against that runtime and already committed external effects.

Derive verification expectations from source evidence independently of the port.
Treat supplied code and dependencies as untrusted. Inspect install hooks and
commands before execution, and use a disposable environment without unrelated
credentials. Keep external effects within the user-authorized scope; when suitable
isolation is unavailable, inspect the source without executing it.
When the source can run, compare observable results and effects against it using
isolated services or recorded boundaries. Compare equivalent public invocations;
calling the target repeatedly to match one source run can hide changed batching,
cadence, or recovery policy. Include source-accepted and
source-rejected inputs, and failures that could disprove the proposed design.
For stateful work, test subsequent invocations from durable state, not a mutated
object left over from a failed execution. Exercise registered flows and their input/output
boundaries, including source batch cardinality and relevant carried metadata, as well as helpers. Ground doubles in observed or documented contracts.
Resolve demonstrated discrepancies in implemented behavior or obtain an agreed
change. Distinguish partial work from preserved behavior; passing self-authored
tests does not establish equivalence. For implemented ports, run project checks
and the production build.

Before importing a requested separate copy, read
[platform verification](references/platform-verification.md) and establish fresh
integration and generated component identities, including inherited publishing
metadata. Preserve the flow and configuration identities needed within the copy.
Omitting an import ID does not establish that the original will remain unchanged.

When the request includes platform verification, use the selected development or
test environment and existing authorization to import, publish versions, configure
or deploy test instances, execute flows, and run smoke tests as needed. Continue
repair and verification cycles without asking for permission again. Follow
[platform verification](references/platform-verification.md), comparing observed
behavior with the source contract. Preserve explicit local-only requests and
resolve missing target, credentials, or allowed external effects while continuing
independent work. Authentication alone does not authorize production changes.
For managed components, exercise their actual behavior in the Prismatic runner
or identify it as unverified. A verified test instance does not establish customer
cutover; keep live traffic changes within the requested scope.

When moving customers, account for instance/version, configuration, connection
scope, and authentication handoff. Prismatic supports
[importing existing OAuth connections](https://prismatic.io/docs/api/common-queries/updating-config-variables/#importing-an-oauth-20-connection);
verify grant compatibility and refresh ownership before promising reuse or
requiring reconnection. The import's `refreshAt` schedules the next Prismatic
refresh; a past value forces immediate refresh. Deployment and redeployment can
themselves cause external effects through [lifecycle hooks](https://prismatic.io/docs/integrations/lifecycle/).

When planning cutover or rollback, establish which system may act during each
transition and how accepted or running work, state, and credentials are reconciled.
A concurrency setting within one system does not coordinate both systems.
Pausing new work or reverting code does not undo completed effects. Keep platform
operations within the requested scope. Explain what migrated, intentional
differences, unresolved dependencies, and what was actually verified. Local
validation does not establish that live state or traffic has moved.
