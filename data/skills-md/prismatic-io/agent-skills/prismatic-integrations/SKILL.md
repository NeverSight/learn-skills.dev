---
name: prismatic-integrations
description: Build, update, and verify a Prismatic Code Native Integration (CNI), including local checks and iterative platform testing. Use for new integration requirements, ongoing CNI development, and debugging flow executions. For assessing or replacing an existing non-Prismatic integration system, prefer prismatic-migrate when available.
compatibility: Requires Node.js 22+, npm, Prism CLI (npm package @prismatic-io/prism) v11 or higher on PATH, and network access to documentation and packages. Platform operations also require Prismatic authentication and any connections needed for the intended environment.
---

# Build a Prismatic integration

Start from the user's request and current project. Extend the current CNI when
present; otherwise scaffold one with `prism integrations:init <name>`. Use
`prism --llms` and command `--help` or `--schema` to discover current
capabilities. Prefer Prism's generated project and toolchain over custom
scaffolding.

Research the connected services in their official documentation. Before choosing
an architecture, consult [Prismatic's documentation index](https://prismatic.io/docs/llms.txt)
for relevant patterns and prefer Prismatic's documented approaches when they fit
the request and existing project. Use
[Prismatic's CNI docs](https://prismatic.io/docs/integrations/code-native/),
[CNI examples](https://github.com/prismatic-io/examples/tree/main/integrations/code-native),
installed manifest documentation, and installed `@prismatic-io/spectral` public
types to verify the chosen approach.

Translate the request into triggers, source and destination operations,
deployer-owned configuration, expected volume, customer-specific mapping, and
retry behavior. Infer technical choices from the service contracts and project.
Ask only about missing business decisions that materially change the result.

Check that the chosen event represents the requested business change; filter a
broader event where supported or explain the limitation. For lifecycle-managed
resources, keep remote IDs tied to their issuing service/account, and check that
repeated setup, changed configuration, and cleanup converge on the intended
resources without affecting unrelated ones. When requests are idempotent, key or
reconcile them according to the desired operation and its change semantics. Use
documented provider-managed guarantees where sufficient; report cleanup limits
when access is unavailable.

Prefer existing Prismatic components when they fit, but a direct authenticated
client is equally valid. Expose credentials and customer-owned choices through
the configuration wizard. Do not hard-code tenant IDs, resource selections,
mappings, or secrets.

Design large or incremental workloads so each execution is bounded and progress
is resumable. Ground pagination and checkpoint behavior in the selected API or
component contract, and make retried writes idempotent or define their duplicate
policy. When customer schemas vary, make object and field selection configurable
and test mapping logic without live credentials.

For a reused trigger or client, verify the selected operation's contract from
official documentation and the installed interface. Derive representative local
checks from that contract, preserving response wrappers, wire types, and
continuation data while keeping relevant request construction under test. Where
event selection or persisted progress matters, check recovery after downstream
failure. If an abstraction omits information the request needs, use a supported
boundary that exposes it; when constructing queries, follow the provider's literal
rules.

Install dependencies and run the generated project's typecheck, lint, tests, and
production build when those scripts exist. After building, run
`prism integrations validate` from the project directory to check that Prism can
load the compiled CNI and validate its local definition before importing it.
Loading executes the project module, so use it only with trusted projects. This
local check does not publish the integration or run flows; platform verification
still establishes remote acceptance and behavior.
For lifecycle hooks or polling triggers,
consult [SDK registration boundaries](references/registration.md).

Before importing a requested separate copy, read
[platform verification](references/platform-verification.md) and establish fresh
integration and generated component identities, including inherited publishing
metadata. Preserve the flow and configuration identities needed within the copy.
Omitting an import ID does not establish that the original will remain unchanged.

Carry implementation through platform verification when it is within the user's
request. Use the selected development or test environment and existing authorization
to import, publish versions, configure or deploy test instances, execute flows,
and run smoke tests as needed. Continue ordinary repair and verification cycles
without asking for permission again. Preserve explicit local-only requests; if the
target, credentials, or allowed external effects are unclear, resolve that gap
while continuing independent work. Authentication alone does not identify the
intended target or authorize production changes.

For platform work, follow [platform verification](references/platform-verification.md).
Fix observed failures, rebuild and update the target, then repeat relevant checks
until the requested behavior is demonstrated or a concrete blocker prevents further
progress. Report the project path, architecture, deployer configuration, assumptions,
validation evidence, and any remaining operational work.
