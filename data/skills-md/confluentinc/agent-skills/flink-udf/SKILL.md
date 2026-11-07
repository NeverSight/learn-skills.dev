---
name: flink-udf
description: "Build and deploy Apache Flink user-defined functions (UDFs) in Java for stream processing over Kafka. Use this skill when users want to create scalar UDFs, user-defined table functions (UDTFs), or process table functions (PTFs) in Java, deploy them to Confluent Cloud or local Docker environments, and invoke them from Flink SQL or the Table API. Trigger on: Flink UDF, custom Flink function, process table function, PTF, UDTF, Flink user defined, extend Flink SQL, stateful stream processing with Flink. Do NOT trigger for: Kafka Streams UDFs (use kafka-streams-programming skill), general Flink job development without custom functions, CDC streaming data piplines that include Flink (prefer the confluent-cloud-cdc-tableflow skill), Flink connector setup, or Kafka producer/consumer code."
metadata:
  version: "1.0.0"
---

# Flink User-Defined Functions (UDFs)

Build and deploy custom functions in Java for Apache Flink to extend SQL and Table API capabilities with custom logic.

## Function Types

Before proceeding, identify which type of function the user needs:

- **Scalar UDF**: Maps input values to a single output value (e.g., custom hash, string manipulation, calculations)
- **User-Defined Table Function (UDTF)**: Maps input to multiple output rows (e.g., split strings, explode arrays)
- **Process Table Function (PTF)**: Advanced stateful processing with N-to-M semantics, managed state, and timers (e.g., windowing, deduplication, state machines)

## Gather Requirements

Ask the user these questions to determine the implementation path (if not already clear from context):

1. **Deployment target**: Confluent Cloud or local Docker?
2. **Infrastructure**: Deploy new infrastructure (Kafka + Flink) or use existing?
3. **Invocation method**: Flink SQL or Table API?

## Route to Implementation Guide

Based on the answers above, read the appropriate reference file:

### Confluent Cloud Deployment

- **Scalar UDF or UDTF** → Read `references/udf-udtf-java-confluent-cloud.md`
- **Process Table Function (PTF)** → Read `references/ptf-java-confluent-cloud.md`

If infrastructure setup is needed, also read `references/confluent-cloud-setup.md` first.

### Local Docker Deployment

- **Scalar UDF or UDTF** → Read `references/udf-udtf-java-local.md`
- **Process Table Function (PTF)** → Read `references/ptf-java-local.md`

If infrastructure setup is needed, also read `references/local-docker-setup.md` first.

## Implementation Workflow

After reading the appropriate reference:

1. **Set up infrastructure** (if needed)
2. **Generate boilerplate code** for the function
3. **Implement the business logic**
4. **Build and package** the JAR
5. **Confirm the deployment plan with the user.** Before any resource-modifying call (`confluent flink artifact create`, `docker cp` into a running container, `CREATE FUNCTION`, etc.), present the plan and wait for explicit approval. Show:
   - Artifact name and JAR path
   - Function name to register
   - Target environment (Confluent Cloud env + compute pool ID, or local Docker container name)
   - The exact commands and SQL that will run
   Do not proceed to steps 6–7 until the user confirms.
6. **Deploy the artifact**
7. **Register the function** in Flink
8. **Test the function** with sample data
9. **Provide usage examples** (SQL or Table API)

Keep code scaffolding concise and focused on the user's specific requirements. Avoid over-engineering.
