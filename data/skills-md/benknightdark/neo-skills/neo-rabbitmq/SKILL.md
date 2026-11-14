---
name: neo-rabbitmq
description: >
  Use this skill when a request involves RabbitMQ message-topology design, reliability
  analysis, Broker operations, cluster or security configuration, monitoring,
  troubleshooting, or performance optimization. Use stable RabbitMQ 4.3 by default
  and keep development guidance language-neutral. Do not use this skill for
  language-specific Client APIs, website implementation, or Blog content.
compatibility: No runtime is required; verify current RabbitMQ official documentation for version-sensitive commands, configuration defaults, or security behavior.
metadata:
  version: "1.0.0"
  pattern: "tool-wrapper,pipeline"
  domain: "messaging-operations-performance"
  default-version: "4.3"
  source-revision: "2b61ea8d840a42e1ba46ee2f1fdf0f9aeec63bd9"
---

# Neo RabbitMQ

Use RabbitMQ 4.3 as the default baseline for language-neutral guidance on message design, Broker operations, and performance optimization.

## Scope Boundaries

Cover:

- Development design: protocols, Virtual Hosts, Exchanges, Bindings, Queues, Publishers, Consumers, Acknowledgements, Publisher Confirms, Prefetch, TTL, Dead Lettering, reliability, and queue-type selection.
- Operations and management: installation, configuration, CLI tools, Management, permissions, TLS, Plugins, Policies, clusters, backups, upgrades, Kubernetes Operator, and production checks.
- Performance optimization: connection and Channel lifecycles, flow control, memory, disk, CPU, network, queues, Quorum Queues, Streams, monitoring, capacity, and bottleneck isolation.
- Troubleshooting: connectivity, authentication, routing, consumer backlog, resource alarms, cluster health, and upgrade risks.

Do not cover:

- Client APIs, SDK code, and language-specific tutorials for Java, Python, C#, Go, Ruby, or any other programming language.
- RabbitMQ website React, Docusaurus, styling, deployment, or other website implementation.
- RabbitMQ Blog, material outside the documented license scope, and documentation unrelated to the three focus areas.
- Production operations using rabbitmqadmin publish or rabbitmqadmin get; the source instructions explicitly omit these commands.

If a request crosses the boundary, answer the language-neutral portion and identify the missing language-specific or product-specific documentation. Never invent a Client API.

## Workflow

1. Classify the request as topology design, reliability, routine operations, security, performance, troubleshooting, upgrade, or capacity planning.
2. Identify the version. Use RabbitMQ 4.3 when no version is specified. For current-version behavior, development releases, release notes, Feature Flags, commands, or configuration defaults, consult current official documentation before answering.
3. Load only the required references:
   - Development and message semantics: references/development.md
   - Operations, management, and upgrades: references/operations.md
   - Performance, capacity, and monitoring: references/performance.md
   - Layered troubleshooting: references/troubleshooting.md
   - Version, sources, and exclusions: references/sources-and-scope.md
4. Gather evidence before drawing conclusions. At minimum, identify the RabbitMQ version, protocol, Virtual Host, Exchange, Queue type, message size and rate, durability, confirmation mode, Consumer behavior, node count, CPU, RAM, disk, network, and relevant metrics. State when the available data is insufficient.
5. Separate source facts, recommendations, and inferences. Label inferences explicitly. Do not present a documentation example or single-environment value as a universal default.
6. Start with non-destructive checks before proposing changes. For configuration changes, deletion, clearing, restart, failover, or upgrade, state the impact, backup, rollback, and verification conditions.
7. Before using CLI examples, consult the corresponding help output when RabbitMQ tools are available locally. Mark every command with its applicable version and required permissions. Never invent parameters.

## Decision Rules

- Define delivery, ordering, retry, loss, and duplicate-processing semantics before discussing throughput or latency.
- Treat Publisher Confirms and Consumer Acknowledgements as separate reliability boundaries. Check message persistence together with Queue durability.
- Select a Queue type based on data safety, replication, ordering, retention, replay, consumption model, and resource characteristics. Never claim that one type is faster for every workload.
- Prefer long-lived Connections, Channel reuse, Publisher and Consumer separation, avoiding polling, and a controlled number of unconfirmed messages. Do not treat adding Consumers or increasing Prefetch as a universal solution.
- Treat Resource Alarms and Flow Control as protection mechanisms and bottleneck signals. Find the root cause in memory, disk, consumption rate, writes, replication, or network before changing alarm settings.
- Use Policies for settings that can be applied dynamically to groups of objects. Handle Queue or Stream types and other creation-time semantics during design and declaration because they cannot be changed afterward.
- Establish workload-specific monitoring baselines. Without evidence, do not assume fixed thresholds, capacity, ports, defaults, or security status.
- Prefer least privilege, Virtual Host isolation, TLS, restricted listeners, secret-free examples, and non-public management endpoints in security guidance.

## Response Contracts

### Topology or Development Design

State assumptions, protocol and topology, routing, Queue type, delivery semantics, failure and retry behavior, monitoring metrics, trade-offs, and verification cases. Use concepts, textual topology diagrams, configuration semantics, and protocol fields only. Do not produce Client code in a programming language.

### Operations or Management Runbook

Present impact, prerequisites, read-only checks, change steps, rollback steps, health verification, and follow-up monitoring in that order. For clusters, TLS, permissions, backups, and upgrades, state node scope and risks. Never present one unverified command as the complete procedure.

### Performance Analysis

Start with the baseline and success criteria. Locate the bottleneck across the end-to-end path: publishing, routing, storage, replication, transport, consumption, or application processing. Change one primary variable at a time and explain expected impact, resource cost, and rollback.

### Troubleshooting

Describe symptoms and missing evidence first. Check version and configuration, network and listeners, authentication, clusters, resource alarms, Queues, Publishers, and Consumers in that order. Tie every conclusion to observed evidence and list reproducible verification signals after remediation.

## Fact-Checking Gate

- Use sources-and-scope.md as the default RabbitMQ 4.3 source snapshot. The snapshot is not a substitute for current documentation.
- Treat versions, Feature Flags, Plugins, CLI syntax, configuration keys, defaults, ports, limits, compatibility, and security advisories as changeable information. Consult current official sources before answering.
- Do not use RabbitMQ Blog content or turn language examples from tutorials or Client Libraries into assumed universal APIs.
- For production data, message deletion, Queue clearing, permission changes, node shutdown, or upgrades, require sufficient environment evidence and provide rollback and verification steps.
