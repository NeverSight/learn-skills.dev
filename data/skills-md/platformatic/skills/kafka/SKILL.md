---
name: kafka
description: |
  Set up Kafka-based event-driven microservices with Platformatic Watt.
  Use when users ask about:
  - "kafka", "event-driven", "messaging"
  - "kafka hooks", "kafka webhooks"
  - "kafka producer", "kafka consumer"
  - "dead letter queue", "DLQ"
  - "request response pattern" with Kafka
  - "migrate from kafkajs", "kafkajs migration", "replace kafkajs"
  Covers @platformatic/kafka, @platformatic/kafka-hooks, consumer lag monitoring,
  and OpenTelemetry instrumentation.
argument-hint: "[hooks|producer|consumer|monitoring]"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Kafka Integration Skill

You are an expert in integrating Apache Kafka with Platformatic Watt for event-driven microservices.

## Prerequisites Check

Before any Kafka setup, verify:

1. **Node.js Version**: Watt requires Node.js v22.19.0+
   ```bash
   node --version
   ```
   If below v22.19.0, inform user they must upgrade Node.js first.

2. **Existing Watt Config**: Check if `watt.json` already exists
   ```bash
   ls watt.json 2>/dev/null
   ```
   If no `watt.json`, suggest running `/watt init` first to set up Watt.

## Command Router

Based on user input ($ARGUMENTS), route to the appropriate workflow:

| Input Pattern | Action |
|--------------|--------|
| `hooks`, `webhooks`, (empty) | Run **Kafka-Hooks Setup** |
| `producer`, `consumer`, `client` | Run **Kafka Client Setup** |
| `monitoring`, `lag`, `health` | Run **Consumer Lag Monitoring Setup** |
| `tracing`, `opentelemetry`, `otel` | Run **Kafka Tracing Setup** |
| `migrate`, `kafkajs`, `migration` | Run **KafkaJS Migration Workflow** |

---

## Kafka-Hooks Setup

When user requests Kafka webhook/hook integration:

1. Read [references/kafka.md](references/kafka.md)
2. Choose integration approach:
   - **@platformatic/kafka-hooks**: Kafka-to-HTTP webhooks (recommended for Watt)
   - **@platformatic/kafka**: Direct producer/consumer in your services
3. Create kafka-hooks service with `npx wattpm@latest create`
4. Configure topics, webhooks, and request/response patterns

### Kafka-Hooks Patterns

- **Webhook**: Kafka messages → HTTP endpoints (with DLQ)
- **Request/Response**: HTTP → Kafka → HTTP (correlation IDs)
- **HTTP Publishing**: POST to `/topics/{topicName}`

---

## Kafka Client Setup

When user requests direct Kafka producer/consumer integration:

1. Read [references/kafka.md](references/kafka.md)
2. Install `@platformatic/kafka`:
   ```bash
   npm install @platformatic/kafka
   ```
3. Set up producer and/or consumer in the target service
4. Configure serializers/deserializers based on message format

---

## Consumer Lag Monitoring Setup

When user requests Kafka consumer lag monitoring:

1. Read [references/kafka.md](references/kafka.md)
2. Install `@platformatic/watt-plugin-kafka-health`:
   ```bash
   npm install @platformatic/watt-plugin-kafka-health
   ```
3. Add plugin to service `watt.json`
4. Configure lag threshold and check interval

---

## Kafka Tracing Setup

When user requests OpenTelemetry tracing for Kafka:

1. Read [references/kafka.md](references/kafka.md)
2. Install `@platformatic/kafka-opentelemetry`:
   ```bash
   npm install @platformatic/kafka-opentelemetry
   ```
3. Enable instrumentation in the service

---

## KafkaJS Migration Workflow

When user wants to migrate from KafkaJS to @platformatic/kafka:

1. Read [references/migration.md](references/migration.md)
2. Scan the project for KafkaJS usage patterns:
   - `require('kafkajs')` or `from 'kafkajs'` imports
   - `new Kafka({...})` factory instantiation
   - `.producer()`, `.consumer()`, `.admin()` calls
   - `connect()` / `disconnect()` lifecycle calls
   - `subscribe()` + `run({ eachMessage })` consumer pattern
   - `sendBatch()` calls
   - `CompressionTypes` usage
   - `transaction()` calls
   - Error handling with `KafkaJS*` error classes
3. Apply the migration checklist from the reference, transforming each pattern
4. Verify the migration covers all areas:
   - Client creation (factory → direct instantiation)
   - Connection lifecycle (`connect`/`disconnect` → lazy/`close`)
   - Producer API (topic per-send → topic per-message, serializers)
   - Consumer API (callback → stream, offset modes)
   - Admin API (new method signatures)
   - Error handling (`retriable` → `canRetry`, new error classes)
   - Events (custom events → `diagnostics_channel`)

---

## Important Notes

- Internal service URLs: `http://{service-id}.plt.local`
- Environment variables in watt.json use `{VAR_NAME}` (curly braces, no dollar sign)
- Kafka-hooks is the recommended approach for Watt multi-service architectures
- Always configure Dead Letter Queues (DLQ) for production webhook topics
