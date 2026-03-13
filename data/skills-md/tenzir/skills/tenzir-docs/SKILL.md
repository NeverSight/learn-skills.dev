---
name: tenzir-docs
description: >-
  Answer questions using the Tenzir documentation. Use whenever the user asks
  about TQL syntax, pipeline operators, functions, data parsing or
  transformation, normalization, OCSF mapping, enrichment, lookup tables,
  contexts, packages, nodes, platform setup, deployment, configuration,
  integrations with tools like Splunk, Kafka, S3, Elasticsearch, or any other
  Tenzir feature. Also use when the user asks how to collect, route, filter,
  aggregate, or export security data with Tenzir, or needs help writing or
  debugging TQL pipelines, even if they don't mention 'Tenzir' explicitly but
  are clearly working in a Tenzir context.
---

# Tenzir Documentation Map

> The low-code data pipeline solution for security teams

Tenzir is a data pipeline engine for security teams. Run pipelines to collect,
parse, transform, and route security data. Deploy nodes on-prem or in the cloud,
and manage them via the Tenzir Platform.

## How to use this skill

Navigate the documentation based on the type of question:

| Question type | Where to look |
|---|---|
| "How do I…" tasks | [Guides](guides.md) — step-by-step instructions organized by task |
| Operator or function syntax | [Operator Index](reference/operators-index.md) or [Function Index](reference/functions-index.md), then the specific page |
| Integration setup (Splunk, Kafka, S3…) | [Integrations](integrations.md) — per-product setup and pipeline examples |
| Concepts (nodes, pipelines, deployment) | [Explanations](explanations.md) — architecture and design |
| Learning from scratch | [Tutorials](tutorials.md) — guided lessons |
| TQL language rules | [Language](explanations/language.md), [Expressions](reference/expressions.md), [Statements](reference/statements.md) |

Always read the relevant page before answering. Prefer TQL examples from the
documentation over inventing syntax.

## Answer patterns

**Operator syntax question** — *"How does `where` work?"*
→ Read [where](reference/operators/where.md), explain the syntax, show the doc's TQL examples.

**Integration question** — *"How do I send data to Splunk?"*
→ Read [Splunk](integrations/splunk.md), provide the pipeline example from the page.

**Task question** — *"How do I parse syslog?"*
→ Read [Parse delimited text](guides/parsing/parse-delimited-text.md) and
[read_syslog](reference/operators/read_syslog.md). Combine the guide's approach
with the operator reference.

## [Guides](guides.md)

Practical step-by-step explanations to help you achieve a specific goal.
Start here when you're trying to get something done.

### Get Started

#### [Quickstart](guides/quickstart.md)

Drowning in logs, alerts, and rigid tools? Meet Tenzir—your engine for taming security data. In just a few minutes, you’ll be ingesting, transforming, and enriching data on your terms, with full control. Here’s what you’ll accomplish:

#### [Installation](guides/installation.md)

This guide shows you how to install the Tenzir CLI to run pipelines locally or deploy a persistent node. The package includes two binaries:

##### [Create account](guides/installation/create-account.md)

The Tenzir Platform is a web interface for managing pipelines and nodes. Create an account to get started:

#### Basic Usage

##### [Run pipelines](guides/basic-usage/run-pipelines.md)

You can run a pipeline via the platform, on the command line using the `tenzir` binary, or as code via the configuration file.

##### [Manage a pipeline](guides/basic-usage/manage-a-pipeline.md)

This guide shows you how to control pipeline lifecycles through the app or API. A pipeline transitions through the following states:

### Setup

#### [Node Setup](guides/node-setup.md)

The Tenzir Node is the vehicle to run pipelines. It is light-weight server application that can be deployed on-premises or in the cloud.

##### [Provision a node](guides/node-setup/provision-a-node.md)

Provisioning a node means creating one in the platform in your workspace. After provisioning, you can download configuration file with an authentication token—ready to then deploy the node.

##### [Size a node](guides/node-setup/size-a-node.md)

This guide helps you determine the CPU, RAM, and storage resources needed for a Tenzir node. Use the calculator below to get concrete estimates based on your deployment scenario.

##### [Deploy a node](guides/node-setup/deploy-a-node.md)

Deploying a node means spinning it up in one of the supported runtimes. The primary choice is between a containerized with Docker or a native deployment with our static binary that runs on amd64 and arm64 architectures.

##### [Configure a node](guides/node-setup/configure-a-node.md)

The default node configuration is optimized for most common scenarios. But you can fine-tune the settings to match your specific requirements.

##### [Configure TLS](guides/node-setup/configure-tls.md)

Tenzir supports Transport Layer Security (TLS) for encrypting network connections. You can configure TLS settings centrally in `tenzir.yaml` so they apply to all compatible operators, or override them per-operator as needed.

##### [Start the API](guides/node-setup/start-the-api.md)

The node offers a REST API for CRUD-style pipeline management. By default, the API is not accessible from the outside. Only the platform can access it internaly through the existing node-to-platform connection. To enable the API for direct access, you need to configure the built in web server that exposes the API.

##### [Tune performance](guides/node-setup/tune-performance.md)

This guide covers configuration options that affect node performance. You’ll learn how to tune demand scheduling, memory usage, and throughput settings.

#### [Platform Setup](guides/platform-setup.md)

The Tenzir Platform acts as a fleet management control plane for Tenzir Nodes. Use its web interface to explore data, create pipelines, and build dashboards.

##### [Deploy on AWS](guides/platform-setup/deploy-on-aws.md)

This guide walks you through deploying the Tenzir Platform Sovereign Edition on AWS using CloudFormation. The template automates the setup of all required infrastructure components.

##### [Choose a scenario](guides/platform-setup/choose-a-scenario.md)

We provide several examples of possible platform deployment scenarios. Pick one that best suits your needs.

##### [Configure reverse proxy](guides/platform-setup/configure-reverse-proxy.md)

This guide shows you how to configure a reverse proxy for the Tenzir Platform. The proxy terminates TLS and routes traffic to these four entry points:

##### [Configure internal services](guides/platform-setup/configure-internal-services.md)

This guide shows you how to configure the three internal Tenzir services: the UI, Gateway, and Platform API. You’ll set environment variables that control authentication, connectivity, and feature settings.

##### [Configure identity provider](guides/platform-setup/configure-identity-provider.md)

The identity provider (IdP) handles authentication for the Tenzir Platform. When you click the Login button in the Tenzir UI, the system redirects you to your chosen identity provider, which creates a signed token that certifies your identity.

##### [Configure database](guides/platform-setup/configure-database.md)

A PostgreSQL database stores the internal state of the platform.

##### [Configure blob storage](guides/platform-setup/configure-blob-storage.md)

The blob storage service exists for exchanging files between the platform and nodes. It facilitates not only downloading data from nodes, but also uploading files from your browser to the platform.

##### [Configure secret store](guides/platform-setup/configure-secret-store.md)

The Tenzir Platform provides a secret store for each workspace. All Tenzir Nodes connected to the workspace can access its secrets. You can manage secrets using the CLI or the web interface. Alternatively, you can use an external secret store.

##### [Run the platform](guides/platform-setup/run-the-platform.md)

This guide shows you how to start the Tenzir Platform using Docker Compose. Complete this step after configuring all services.

#### Platform Management

##### [Configure workspaces](guides/platform-management/configure-workspaces.md)

Workspaces in the platform logically group nodes, secrets, and dashboards.

##### [Configure dashboards](guides/platform-management/configure-dashboards.md)

You can pre-define dashboards for your static workspaces. This practice provides users with ready-to-use visualizations when they access the workspace.

##### [Use ephemeral nodes](guides/platform-management/use-ephemeral-nodes.md)

An ephemeral node is ideal for temporary or auto-scaling deployments. It is a temporary node that you do not have to provision manually first, and it disappears from the workspace when the connection to the platform ends.

#### [AI Workbench](guides/ai-workbench.md)

Build your own AI Workbench by bringing an AI agent and configuring it with Tenzir’s agent skills. Once set up, use it to write TQL pipelines, understand OCSF schemas, generate parsers, and create data mappings.

##### [Use agent skills](guides/ai-workbench/use-agent-skills.md)

This guide shows you how to install and manage Tenzir’s agent skills. You’ll learn how to add skills globally or per project, install individual skills, and keep them up to date.

### Work with Data

#### [Collecting](guides/collecting.md)

This guide provides an overview of data collection in TQL. You’ll learn about the different approaches for ingesting data from various sources.

##### [Read and watch files](guides/collecting/read-and-watch-files.md)

This guide shows you how to read files and monitor directories using the `from_file` operator. You’ll learn to read individual files, batch process directories, and set up real-time file monitoring.

##### [Fetch via HTTP and APIs](guides/collecting/fetch-via-http-and-apis.md)

This guide shows you how to fetch data from HTTP APIs using the `from_http` and `http` operators. You’ll learn to make GET requests, handle authentication, and implement pagination for large result sets.

##### [Read from message brokers](guides/collecting/read-from-message-brokers.md)

This guide shows you how to receive events from message brokers using TQL. You’ll learn to subscribe to topics and queues from Apache Kafka (including Amazon MSK), AMQP-based brokers (like RabbitMQ), Amazon SQS, and Google Cloud Pub/Sub.

##### [Get data from the network](guides/collecting/get-data-from-the-network.md)

This guide shows you how to receive data directly from network sources using TQL. You’ll learn to listen on TCP and UDP sockets for incoming data and capture raw packets from network interfaces.

#### Parsing

##### [Parse delimited text](guides/parsing/parse-delimited-text.md)

This guide shows you how to parse text streams into structured events. You’ll learn to split byte streams on newlines or custom delimiters, and parse line-based formats like JSON lines, CSV, TSV, key-value pairs, Syslog, and CEF.

##### [Parse binary data](guides/parsing/parse-binary-data.md)

This guide shows you how to parse binary data formats into structured events. You’ll learn to work with columnar formats like Parquet and Feather, packet captures in PCAP format, Tenzir’s native Bitz format, and compressed data.

##### [Parse string fields](guides/parsing/parse-string-fields.md)

This guide shows you how to extract structured data from string fields using TQL’s parsing functions. You’ll learn to parse JSON, YAML, XML, key-value pairs, delimited data, timestamps, and log formats like Syslog, CEF, LEEF, and Windows Event Logs. For custom formats, Grok patterns provide flexible pattern matching.

#### Transformation

##### [Filter and select data](guides/transformation/filter-and-select-data.md)

Filtering and selecting are fundamental operations when working with data streams. This guide shows you how to filter events based on conditions and select specific fields from your data.

##### [Transform values](guides/transformation/transform-values.md)

Transforming values is a fundamental part of data processing. This guide shows you how to convert between different data types, perform basic calculations, and manipulate simple values within your events.

##### [Manipulate strings](guides/transformation/manipulate-strings.md)

String manipulation is essential for cleaning, formatting, and transforming text data. This guide covers TQL’s comprehensive string functions, from simple case changes to complex pattern matching and encoding operations.

##### [Work with time](guides/transformation/work-with-time.md)

Time is fundamental in data analysis. Whether you’re analyzing logs, tracking events, or monitoring systems, you need to parse timestamps, calculate durations, and format dates. This guide shows you how to work with time values in TQL.

##### [Shape lists](guides/transformation/shape-lists.md)

Lists (arrays) contain ordered sequences of values. This guide shows you how to work with lists — accessing elements, sorting and slicing, transforming values, and combining data structures.

##### [Shape records](guides/transformation/shape-records.md)

Records (objects) contain key-value pairs. This guide shows you how to work with records — accessing fields, extracting keys, merging, and transforming values.

##### [Reshape complex data](guides/transformation/reshape-complex-data.md)

Real-world data is rarely flat. It contains nested structures, arrays of objects, and deeply hierarchical information. This guide shows advanced techniques for reshaping complex data structures to meet your analysis needs.

##### [Convert data formats](guides/transformation/convert-data-formats.md)

Data comes in many formats. Converting between formats is essential for integration, export, and interoperability. This guide shows you how to transform data between JSON, CSV, YAML, and other common formats using TQL’s print functions.

#### [Normalization](guides/normalization.md)

This guide provides an overview of data normalization in TQL. Normalization transforms raw, inconsistent data into a clean, standardized format that’s ready for analysis, storage, and sharing.

##### [Clean up values](guides/normalization/clean-up-values.md)

This guide shows you how to clean and normalize values in your data before mapping to a schema. You’ll learn to handle null placeholders, normalize sentinel values, fix types, and provide defaults.

##### [Map to OCSF](guides/normalization/map-to-ocsf.md)

This guide shows you how to write OCSF mapping operators in TQL. You’ll learn to organize mappings by attribute groups, handle unmapped fields, and validate your output. The guide assumes you’ve already identified your target OCSF event class and profiles.

##### [Map to other schemas](guides/normalization/map-to-other-schemas.md)

This guide provides brief guidance on mapping data to schemas other than OCSF. While OCSF is the recommended choice for security data, you may need to support Elastic Common Schema (ECS), Google UDM, or Microsoft ASIM for integration with specific platforms.

#### Enrichment

##### [Work with lookup tables](guides/enrichment/work-with-lookup-tables.md)

A lookup table is a specific type of context in Tenzir’s enrichment framework. It has “two ends” in that you can use pipelines to update it, as well as pipelines to perform lookups and attach the results to events. Lookup tables live in a node and multiple pipelines can safely use the same lookup table. All update operations propagate to disk, persisting the changes and making them resilient against node restarts.

##### [Enrich with network inventory](guides/enrichment/enrich-with-network-inventory.md)

Tenzir’s enrichment framework features lookup tables that you can use to enrich data in your pipelines. Lookup tables have a unique property that makes them attractive for tracking information associated with CIDR subnets: when you use `subnet` values as keys, you can probe the lookup table with `ip` values and will get a longest-prefix match.

##### [Enrich with threat intel](guides/enrichment/enrich-with-threat-intel.md)

Tenzir has a powerful enrichment framework for real-time contextualization. The heart of the framework is a context—a stateful object that can be managed and used with pipelines.

##### [Execute Sigma rules](guides/enrichment/execute-sigma-rules.md)

Tenzir supports executing Sigma rules using the `sigma` operator. This allows you to run your Sigma rules in the pipeline. The operator transpiles the provided rules into an expression, and wraps matching events into a sighting record along with the matched rule.

#### Optimization

##### [Slice and sample data](guides/optimization/slice-and-sample-data.md)

When working with data streams, you often need to control which events flow through your pipeline. This guide shows you how to slice event streams, sample data, and control event ordering using TQL operators.

##### [Deduplicate events](guides/optimization/deduplicate-events.md)

The `deduplicate` operator provides a powerful mechanism to remove duplicate events in a pipeline.

#### Routing

##### [Send to destinations](guides/routing/send-to-destinations.md)

This guide shows you how to send data to various destinations using TQL output operators. You’ll learn about destination operators, file output patterns, and expression-based serialization.

##### [Split and merge streams](guides/routing/split-and-merge-streams.md)

This guide shows you how to connect pipelines using `publish` and `subscribe` operators. You’ll learn to split event streams for parallel processing and merge multiple sources into a single pipeline.

##### [Load-balance pipelines](guides/routing/load-balance-pipelines.md)

This guide shows you how to distribute events across multiple destinations using the `load_balance` operator. You’ll learn to route events to multiple endpoints for high availability and throughput.

#### Analytics

##### [Aggregate and summarize data](guides/analytics/aggregate-and-summarize.md)

Aggregation transforms streams of events into meaningful summaries. Whether you’re calculating statistics, counting occurrences, or finding extremes, the `summarize` operator combined with aggregation functions provides powerful data analysis capabilities.

##### [Collect metrics](guides/analytics/collect-metrics.md)

Tenzir keeps track of metrics about node resource usage, pipeline state, and runtime performance.

#### Edge Storage

##### [Import into a node](guides/edge-storage/import-into-a-node.md)

Importing (or ingesting) data can be done by running a pipeline that ends with the `import` output operator. When managing a pipeline through the app or the API, all pipeline operators run within the node. When using the CLI, at least the `import` operator runs within the node.

##### [Export from a node](guides/edge-storage/export-from-a-node.md)

Exporting (or querying) data can be done by running a pipeline that begins with the `export` input operator. When managing a pipeline through the app or the API, all pipeline operators run within the node. When using the CLI, at least the `export` operator runs within the node.

##### [Show available schemas](guides/edge-storage/show-available-schemas.md)

When you write a pipeline, you often reference field names. If you do not know the shape of your data, you can look up available schemas, i.e., the record types describing top-level events.

##### [Transform data at rest](guides/edge-storage/transform-data-at-rest.md)

This guide shows you how to transform data already stored in a node. You’ll learn to apply compaction, manage storage quotas, and run retroactive pipelines.

### Build

#### Packages

##### [Install a package](guides/packages/install-a-package.md)

Packages provide a flexible approach for combining operators, pipelines, contexts, and examples into a unified deployable unit.

##### [Create a package](guides/packages/create-a-package.md)

This guide shows you how to create a package from scratch. You’ll learn how to set up the directory structure, write the manifest, and add runnable examples.

##### [Test packages](guides/packages/test-packages.md)

This guide shows you how to add tests to your package. You’ll learn how to write test files, use inline inputs, and run the test harness.

##### [Add operators](guides/packages/add-operators.md)

This guide shows you how to create user-defined operators (UDOs) for your package. You’ll learn how to define operators with positional and named arguments, and how to test them with the Test Framework.

##### [Add pipelines](guides/packages/add-pipelines.md)

This guide shows you how to add deployable pipelines to your package. You’ll learn about pipeline frontmatter options and when to use pipelines versus operators.

##### [Add contexts](guides/packages/add-contexts.md)

This guide shows you how to add enrichment contexts to your package. You’ll learn how to define contexts in the manifest, populate them with data, and test context interactions.

##### [Configure inputs](guides/packages/configure-inputs.md)

This guide shows you how to make packages configurable with inputs. You’ll learn how to define input variables, use templating syntax, and provide values during installation.

##### [Maintain a changelog](guides/packages/maintain-a-changelog.md)

This guide shows you how to manage changelog entries and publish releases with `tenzir-ship`. You’ll learn the complete workflow from adding your first entry to publishing a release on GitHub.

##### [Publish a package](guides/packages/publish-a-package.md)

This guide shows you how to publish your package. You’ll learn how to contribute to the Tenzir Community Library and how to set up your own package repository with automated testing.

#### Testing

##### [Run tests](guides/testing/run-tests.md)

This guide shows you how to run existing integration tests with the `tenzir-test` framework. You’ll learn how to execute the test suite, control output verbosity, select specific tests, handle flaky scenarios, and run multi-project setups.

##### [Write tests](guides/testing/write-tests.md)

This guide shows you how to create integration tests with the `tenzir-test` framework. You’ll set up a standalone repository, write test scenarios, and record reference output to verify your pipelines work as expected. If you already have tests and want to run them, see the run tests guide.

##### [Run fixtures](guides/testing/run-fixtures.md)

This guide shows you how to start fixtures in standalone mode without running tests. You’ll learn how to use the `--fixture` CLI option to bring up managed services, inspect their environment variables, and tear them down cleanly.

##### [Create fixtures](guides/testing/create-fixtures.md)

This guide shows you how to create a fixture, wire it into the test harness, and use it from a test. You will build an HTTP echo server as a running example and then learn how to share fixtures across suites, handle missing dependencies, manage containers, add structured options, and validate test behavior with fixture assertions.

##### [Add custom runners](guides/testing/add-custom-runners.md)

Runners tell `tenzir-test` how to execute a discovered file. This guide shows you how to register the XXD runner from the example project so you can compare binary artifacts by dumping their hexadecimal representation with `xxd`.

### Contribute

#### Contribution

##### [Code of Conduct](guides/contribution/code-of-conduct.md)

##### [Git and GitHub Workflow](guides/contribution/workflow.md)

The following diagram visualizes our branching model:

##### [Documentation](guides/contribution/documentation.md)

The source code of the Tenzir documentation is at <https://github.com/tenzir/docs>. We use Astro with Starlight as our site framework.

##### [Security Policy](guides/contribution/security.md)

Security is a serious matter for us. We want to ensure and maintain a secure environment for our customers and the open-source community.

#### Development

##### [Setup syntax highlighting](guides/development/setup-syntax-highlighting.md)

This guide shows you how to set up TQL syntax highlighting in your editor. You’ll get proper colorization, language detection, and basic language support for `.tql` files.

##### [Build from source](guides/development/build-from-source.md)

Tenzir uses CMake as build system with a C++23 compiler.

##### [Write a node plugin](guides/development/write-a-node-plugin.md)

This guide shows you how to extend Tenzir with custom operators, formats, or connectors by writing a C++ plugin. The implementation requires the following steps:

## [Tutorials](tutorials.md)

Learning-oriented lessons that take you through a series of steps.
Start here when you want to get started with Tenzir.

### Fundamentals

#### [Learn idiomatic TQL](tutorials/learn-idiomatic-tql.md)

This tutorial teaches you to write TQL that is clear, efficient, and maintainable. It assumes you already know basic TQL syntax and operators, and shows you how experienced TQL developers approach common patterns.

#### [Write a package](tutorials/write-a-package.md)

This tutorial teaches you how packages bundle pipelines, operators, contexts, and examples. You’ll build a package for an SSL blacklist that detects malicious certificates. You can then install packages from the Tenzir Library or deploy them as code.

#### [Map data to OCSF](tutorials/map-data-to-ocsf.md)

In this tutorial you’ll learn how to map events to Open Cybersecurity Schema Framework (OCSF). We walk you through an example of events from a network monitor and show how you can use Tenzir pipelines to transform them into OCSF-compliant events.

### Analytics

#### [Plot data with charts](tutorials/plot-data-with-charts.md)

In this tutorial, you will learn how to use pipelines to plot data as charts.

## [Explanations](explanations.md)

Big-picture explanations of higher-level concepts.
Start here to build understanding of a particular topic.

### Architecture

#### [Deployment](explanations/deployment.md)

This page explains Tenzir’s deployment architecture, which separates data processing from management through a layered design. Three primary abstractions work together:

#### [Pipeline](explanations/pipeline.md)

A Tenzir pipeline is a chain of operators that represents a dataflow. Operators are the atomic building blocks that produce, transform, or consume data. Think of them as Unix or Powershell commands where the result from one command is feeding into the next:

#### [Node](explanations/node.md)

A node is a running process that manages and executes pipelines.

#### [Platform](explanations/platform.md)

The platform provides fleet management for nodes. With an API and web interface, the platform offers user and workspace administration, authentication via external identity providers (IdP), and dashboards consisting of pipeline-powered charts.

#### [Language](explanations/language.md)

The Tenzir Query Language (TQL) is a dataflow language designed for processing of unstructured byte-streams and semi-structured events.

### Concepts

#### [Configuration](explanations/configuration.md)

This page explains how to configure the Tenzir CLI and Node. Configuration flows through four layers, sorted by precedence:

#### [Secrets](explanations/secrets.md)

Operators accept secrets as parameters for sensitive values, such as authentication tokens, passwords, or even URLs.

#### [Enrichment](explanations/enrichment.md)

Enrichment means adding contextual data to events. The purpose of this added context is to allow for making better decisions, e.g., to triage alerts and weed out false positive, to leverage country information to classify logins as malicious, or to flag a sighting of an indicator of compromise.

#### [Packages](explanations/packages.md)

This page explains how packages bundle pipelines, operators, contexts, and examples into a deployable unit. You’ll learn about package design principles and how the components fit together.

### Help

#### [Glossary](explanations/glossary.md)

This page defines central terms in the Tenzir ecosystem.

#### [FAQs](explanations/faqs.md)

This page answers frequently asked questions about Tenzir.

## [Reference](reference.md)

Nitty-gritty technical descriptions of how Tenzir works.
Start here when you need detailed information about building blocks.

### Language (TQL)

#### [Type System](reference/types.md)

This page explains TQL’s type system, which provides strong typing with automatic inference. You get type safety without requiring explicit declarations. Key characteristics include:

#### [Expressions](reference/expressions.md)

Expressions form the computational core of TQL. They range from simple literals to complex evaluations.

#### [Statements](reference/statements.md)

TQL programs are a sequence of statements. Operator statements perform various actions on data streams. Each operator statement can be thought of as a modular unit that processes data and can be combined with other operators to create complex dataflows.

#### [Programs](reference/programs.md)

TQL programs compose statements into complete data processing workflows that can execute. Valid TQL programs adhere to the following rules:

#### [Operators](reference/operators.md)

Tenzir comes with a wide range of built-in pipeline operators.

#### [Functions](reference/functions.md)

Functions appear in expressions and take positional and/or named arguments, producing a value as a result of their computation.

### Tools

#### [Test Framework](reference/test-framework.md)

The `tenzir-test` harness discovers and runs integration tests for pipelines, fixtures, and custom runners. Use this page as a reference for concepts, configuration, and CLI details. For step-by-step walkthroughs, see the guides for running tests, writing tests, creating fixtures, and adding custom runners.

#### [Ship Framework](reference/ship-framework.md)

`tenzir-ship` helps you ship faster with automated release engineering. Manage changelogs, generate release notes, and publish GitHub releases. Use this page as a reference for concepts, configuration, and CLI details. For step-by-step walkthroughs, see the guide for maintaining a changelog.

#### Node Index

- [Node Configuration](reference/node/configuration.md)

#### Platform Index

- [Platform command line interface](reference/platform/command-line-interface.md)
- [Platform Configuration](reference/platform/configuration.md)

### Indexes

For the complete operator listing by category, read [Operator Index](reference/operators-index.md).

For the complete function listing by category, read [Function Index](reference/functions-index.md).

## [Integrations](integrations.md)

Turn-key packages and native connectors for security tools.
Start here to connect Tenzir with Splunk, Elastic, CrowdStrike, etc.

### Cloud Providers

#### [Amazon](integrations/amazon.md)

Tenzir integrates with the services from Amazon Web Services (AWS) listed below.

##### [MSK](integrations/amazon/msk.md)

Amazon Managed Streaming for Apache Kafka (Amazon MSK) is a managed Kafka service on AWS. It handles infrastructure and operations, making it easier to run Kafka applications and Kafka Connect connectors without becoming a Kafka expert.

##### [S3](integrations/amazon/s3.md)

Amazon Simple Storage Service (S3) is an object storage service. Tenzir can treat it like a local filesystem to read and write files.

##### [Security Lake](integrations/amazon/security-lake.md)

Amazon Security Lake is a managed security data lake on AWS. It collects and stores security data in the Open Cybersecurity Schema Framework (OCSF) format.

##### [SQS](integrations/amazon/sqs.md)

Amazon Simple Queuing Service (SQS) is a managed message queue on AWS. It supports microservices, distributed systems, and serverless applications.

#### Google

##### [Cloud Logging](integrations/google/cloud-logging.md)

Google Cloud Logging is Google’s log management solution. Tenzir can send events to Google Cloud Logging.

##### [Cloud Storage](integrations/google/cloud-storage.md)

Cloud Storage is Google’s object storage service. Tenzir can treat it like a local filesystem to read and write files.

##### [Cloud Pub/Sub](integrations/google/cloud-pubsub.md)

Google Cloud Pub/Sub ingests events for streaming into BigQuery, data lakes, or operational databases. Tenzir can act as a publisher that sends messages to a topic, and as a subscriber that receives messages from a subscription.

##### [SecOps](integrations/google/secops.md)

Google Security Operations (SecOps) is Google’s security operations platform. Tenzir can send events to Google SecOps using the unstructured logs ingestion API.

#### Microsoft

##### [Azure Blob Storage](integrations/microsoft/azure-blob-storage.md)

Azure Blob Storage is Azure’s object storage service. Tenzir can treat it like a local filesystem to read and write files.

##### [Azure Event Hubs](integrations/microsoft/azure-event-hubs.md)

Azure Event Hubs is a real-time event ingestion service. It can receive and process millions of events per second, and it provides a Kafka endpoint for streaming data from Microsoft services to Tenzir.

##### [Defender](integrations/microsoft/defender.md)

Microsoft Defender offers protection, detection, investigation, and response to threats. Defender comes in multiple editions, Defender for Office 365, Defender for Endpoint, Defender for IoT, Defender for Identity, and Defender for Cloud. All Defender products can stream events in real time to Tenzir using Azure Event Hubs.

##### [Sentinel & Log Analytics](integrations/microsoft/sentinel-log-analytics.md)

Send security logs and events from Tenzir to Microsoft’s Log Analytics platform. You can analyze them with Microsoft Sentinel, create alerts with Azure Monitor, or query them with KQL.

##### [Windows Event Logs](integrations/microsoft/windows-event-logs.md)

Windows Event Logs record system, security, and application events on Windows. You can collect them into Tenzir for monitoring, troubleshooting, and analysis.

### Messaging

#### [AMQP](integrations/amqp.md)

The Advanced Message Queuing Protocol (AMQP) is an open standard for message-oriented middleware. It defines how producers, exchanges, queues, and consumers route messages between systems.

#### [Fluent Bit](integrations/fluent-bit.md)

Fluent Bit is a an open source observability pipeline. Tenzir embeds Fluent Bit, exposing all its inputs via `from_fluent_bit` and outputs via `to_fluent_bit`

#### [Kafka](integrations/kafka.md)

Apache Kafka is a distributed open-source message broker. The Tenzir integration can publish (send messages to a topic) or subscribe (receive) messages from a topic.

#### [ZeroMQ](integrations/zeromq.md)

ZeroMQ (0mq) is a light-weight messaging framework with various socket types. Tenzir supports writing to PUB sockets and reading from SUB sockets, both in server (listening) and client (connect) mode.

### Protocols

#### [Email](integrations/email.md)

Tenzir supports sending events as email using the `save_email` operator. To this end, the operator establishes a connection with an SMTP server that sends the message on behalf of Tenzir.

#### [File](integrations/file.md)

Tenzir can read from and write to files. This includes non-regular files such as Unix domain sockets, standard input, standard output, and standard error.

#### [FTP](integrations/ftp.md)

Tenzir supports the File Transfer Protocol (FTP), both downloading and uploading files.

#### [HTTP](integrations/http.md)

Tenzir supports HTTP and HTTPS, both as sender and receiver.

#### [Network Interface](integrations/nic.md)

Tenzir supports reading packets from a network interface card (NIC).

#### [Syslog](integrations/syslog.md)

Tenzir supports parsing and emitting Syslog messages across multiple transport protocols, including both UDP and TCP. This enables seamless integration with Syslog-based systems for ingesting or exporting logs.

#### [TCP](integrations/tcp.md)

The Transmission Control Protocol (TCP) provides a bidirectional byte stream over IP. Tenzir supports reading from and writing to TCP sockets in both server (listening) and client (connect) mode.

#### [UDP](integrations/udp.md)

The User Datagram Protocol (UDP) is a connection-less protocol to send messages on an IP network. Tenzir supports writing to and reading from UDP sockets, both in server (listening) and client (connect) mode.

### Data Tools

#### [ClickHouse](integrations/clickhouse.md)

ClickHouse is an open-source analytical database. It lets you run real-time analytics with SQL queries.

#### [Elasticsearch](integrations/elasticsearch.md)

Elasticsearch is a search and observability suite for unstructured data. Tenzir can send events to Elasticsearch and emulate and Elasticsearch Bulk API endpoint.

#### [Graylog](integrations/graylog.md)

Graylog is a log management solution based on top of OpenSearch. Tenzir can send data to and receive data from Graylog.1

#### [OpenSearch](integrations/opensearch.md)

OpenSearch is a search and observability suite for unstructured data. Tenzir can send events to OpenSearch and emulate and OpenSearch Bulk API endpoint.

#### [Snowflake](integrations/snowflake.md)

Snowflake is a multi-cloud data warehouse. Tenzir can send events from a pipeline to Snowflake databases.

#### [Splunk](integrations/splunk.md)

Splunk is a SIEM solution for storing and processing logs. Tenzir can send data to Splunk via HEC.

### Security Tools

#### [SentinelOne Data Lake](integrations/sentinelone-data-lake.md)

SentinelOne is a cybersecurity platform that provides endpoint protection and threat detection. The SentinelOne Singularity Data Lake allows you to store and analyze security events at scale. Tenzir provides bidirectional integration with the SentinelOne Data Lake via its REST API.

#### [Suricata](integrations/suricata.md)

Suricata is network monitor with a rule matching engine to detect threats. Use Tenzir to acquire, process, and store Suricata logs.

#### [Velociraptor](integrations/velociraptor.md)

Velociraptor is a digital forensics and incident response (DFIR) tool for interrogating endpoints.

#### [Zeek](integrations/zeek.md)

The Zeek network monitor translates raw packets into structured logs. Tenzir supports various Zeek use cases, such as continuous ingestion, ad-hoc log file processing, and even generating Zeek logs.

#### [Zscaler](integrations/zscaler.md)

Zscaler’s Nanolog Streaming Service (NSS) streams Zscaler logs to external systems. You can use Zscaler’s Cloud NSS or deploy an on-prem NSS server, and Tenzir can receive logs in either case.
