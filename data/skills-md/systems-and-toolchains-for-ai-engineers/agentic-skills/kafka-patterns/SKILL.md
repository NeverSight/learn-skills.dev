---
name: kafka-patterns
description: Apache Kafka patterns for topic design, reliable producers and consumers, exactly-once processing, retry and dead-letter handling, schema evolution, testing, and operations. Use when writing Kafka producers or consumers, designing topics and keys, debugging consumer lag or duplicate delivery, or reviewing event-driven code.
metadata:
  origin: ECC
---

# Kafka Patterns

Production patterns for building on Apache Kafka. The examples use the Java client, KafkaJS (Node), and confluent-kafka (Python), but the rules apply to any client that speaks the Kafka protocol.

## When to Activate

- Designing topics, partitions, keys, or retention for a new event stream
- Writing or reviewing a producer or consumer in any language
- Choosing between at-least-once, at-most-once, and exactly-once delivery
- Handling poison messages, retries, and dead-letter topics
- Evolving an event schema without breaking existing consumers
- Debugging consumer lag, rebalance storms, duplicate delivery, or lost messages
- Writing integration tests that need a real broker

## Core Concepts

| Concept | What it means in practice |
|---------|---------------------------|
| Topic | Append-only log split into partitions. Ordering is guaranteed only within a partition. |
| Key | Decides the partition. Same key, same partition, so same relative order. |
| Consumer group | Each partition is read by exactly one consumer in a group. More consumers than partitions leaves some idle. |
| Offset | Position in a partition. A committed offset says "everything before this is done". |
| Replication | `replication.factor` copies per partition. `min.insync.replicas` says how many must acknowledge a write. |
| Retention | Time or size based deletion, or log compaction that keeps the latest record per key. |

Delivery semantics come from the combination of producer settings, consumer commit timing, and what the processing side does. No single flag gives you exactly-once.

## Topic Design

### Naming and layout

Use a stable, hierarchical name that encodes ownership and meaning, and keep one event type per topic unless the events must be ordered together.

```text
orders.order.created        # <domain>.<entity>.<event>
orders.order.created.retry  # retry companion
orders.order.created.dlq    # dead-letter companion
inventory.stock.changelog   # compacted state topic
```

### Choosing partitions

- Start from target throughput divided by per-partition throughput, then round up to leave headroom. Increasing partitions later changes key routing, so plan for growth up front.
- Set the count to a multiple of the expected consumer count so load balances evenly.
- Thousands of partitions per broker slow leader elections and recovery. Aim for hundreds per broker, not thousands.

### Choosing keys

- Key by the identity whose ordering matters (order id, account id, device id).
- A null key round-robins across partitions and destroys ordering. Use it only for events where order is irrelevant.
- Watch for hot keys. One tenant producing 40 percent of traffic pins one partition. Add a secondary discriminator to the key or move that tenant to its own topic.

### Retention and compaction

```bash
# Event stream: keep 7 days, delete after that
kafka-configs --alter --entity-type topics --entity-name orders.order.created \
  --add-config retention.ms=604800000,cleanup.policy=delete

# State topic: keep latest value per key forever
kafka-configs --alter --entity-type topics --entity-name inventory.stock.changelog \
  --add-config cleanup.policy=compact,min.compaction.lag.ms=60000
```

Compacted topics need a non-null key on every record. A record with a null value is a tombstone that deletes the key after `delete.retention.ms`.

### Durability baseline

```properties
replication.factor=3
min.insync.replicas=2
unclean.leader.election.enable=false
```

With `acks=all` on the producer this survives one broker loss without losing acknowledged writes.

## Producer Patterns

### Reliable producer configuration (Java)

```java
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker-1:9092,broker-2:9092");
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);   // dedupes broker-side retries
props.put(ProducerConfig.ACKS_CONFIG, "all");
props.put(ProducerConfig.DELIVERY_TIMEOUT_MS_CONFIG, 120_000);
props.put(ProducerConfig.LINGER_MS_CONFIG, 20);               // batch for throughput
props.put(ProducerConfig.BATCH_SIZE_CONFIG, 64 * 1024);
props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "lz4");

try (KafkaProducer<String, OrderCreated> producer = new KafkaProducer<>(props)) {
    ProducerRecord<String, OrderCreated> record =
        new ProducerRecord<>("orders.order.created", order.getId(), event);
    record.headers().add("trace-id", traceId.getBytes(StandardCharsets.UTF_8));

    producer.send(record, (metadata, exception) -> {
        if (exception != null) {
            log.error("publish failed key={} topic={}", order.getId(), record.topic(), exception);
            return;
        }
        log.debug("published partition={} offset={}", metadata.partition(), metadata.offset());
    });
}
```

Idempotence removes duplicates caused by producer retries within a session. It does not protect against the application calling `send` twice for the same business event.

### Reliable producer (KafkaJS)

```typescript
const kafka = new Kafka({ clientId: 'orders-api', brokers: ['broker-1:9092'] })
const producer = kafka.producer({ idempotent: true, maxInFlightRequests: 5 })

await producer.connect()
await producer.send({
  topic: 'orders.order.created',
  acks: -1, // all in-sync replicas
  messages: [{
    key: order.id,
    value: JSON.stringify(event),
    headers: { 'trace-id': traceId },
  }],
})
```

### Reliable producer (confluent-kafka, Python)

```python
producer = Producer({
    "bootstrap.servers": "broker-1:9092",
    "enable.idempotence": True,
    "acks": "all",
    "linger.ms": 20,
    "compression.type": "lz4",
})

def on_delivery(err, msg):
    if err is not None:
        log.error("publish failed key=%s err=%s", msg.key(), err)

producer.produce("orders.order.created", key=order_id, value=payload, on_delivery=on_delivery)
producer.poll(0)      # serve delivery callbacks without blocking
...
producer.flush()      # on shutdown, wait for in-flight records
```

### Transactional outbox

Writing to a database and publishing to Kafka in the same request is two commits and cannot be atomic. Store the event in an `outbox` table inside the database transaction, then relay it to Kafka with a separate poller or a CDC connector. Consumers must still tolerate duplicates, because the relay is at-least-once.

## Consumer Patterns

### Manual commit after processing (Java)

```java
props.put(ConsumerConfig.GROUP_ID_CONFIG, "billing-service");
props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 200);
props.put(ConsumerConfig.MAX_POLL_INTERVAL_MS_CONFIG, 300_000);
props.put(ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG,
    CooperativeStickyAssignor.class.getName());   // avoids stop-the-world rebalances

consumer.subscribe(List.of("orders.order.created"));
while (running) {
    ConsumerRecords<String, OrderCreated> records = consumer.poll(Duration.ofMillis(500));
    for (ConsumerRecord<String, OrderCreated> record : records) {
        process(record);
    }
    if (!records.isEmpty()) {
        consumer.commitSync();    // commit only after every record in the batch is done
    }
}
```

Committing after processing gives at-least-once delivery. A crash between `process` and `commitSync` replays the batch, so `process` must be idempotent (see Idempotent Consumers below).

### Manual commit (KafkaJS)

```typescript
const consumer = kafka.consumer({ groupId: 'billing-service' })
await consumer.subscribe({ topic: 'orders.order.created' })

await consumer.run({
  autoCommit: false,
  eachMessage: async ({ topic, partition, message }) => {
    await process(message)
    await consumer.commitOffsets([
      { topic, partition, offset: (Number(message.offset) + 1).toString() },
    ])
  },
})
```

Committed offsets point to the next record to read, so commit `offset + 1`.

### Manual commit (confluent-kafka, Python)

```python
consumer = Consumer({
    "bootstrap.servers": "broker-1:9092",
    "group.id": "billing-service",
    "enable.auto.commit": False,
    "auto.offset.reset": "earliest",
})
consumer.subscribe(["orders.order.created"])

try:
    while running:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        process(msg)
        consumer.commit(message=msg, asynchronous=False)
finally:
    consumer.close()   # triggers a clean rebalance instead of waiting for session timeout
```

### Idempotent consumers

Every at-least-once consumer needs a deduplication strategy. Pick one of the following.

- **Natural idempotence.** `UPSERT` by business key, or `SET balance = :value` instead of `balance += :delta`.
- **Processed-id table.** Insert the event id into a unique-constrained table in the same transaction as the side effect. A duplicate fails the insert and the handler skips it.
- **Version check.** Carry a version or timestamp in the event and ignore anything older than what is stored.

### Keep the poll loop alive

The broker evicts a consumer that does not call `poll` within `max.poll.interval.ms`. Long-running work inside the loop causes a rebalance, which reassigns the partition to another consumer that then reprocesses the same records. Either lower `max.poll.records`, raise `max.poll.interval.ms`, or hand work to a bounded worker pool and pause the partition until it drains.

### Static membership for stateful consumers

```properties
group.instance.id=billing-service-pod-3
session.timeout.ms=45000
```

A restart within `session.timeout.ms` keeps its partitions, so rolling deploys do not trigger a rebalance for every pod.

## Exactly-Once Processing

Exactly-once in Kafka means read-process-write within Kafka is atomic. It does not extend to external systems such as a database or an HTTP call.

```java
props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "enrich-orders-" + instanceId);
producer.initTransactions();

consumerProps.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");

while (running) {
    ConsumerRecords<String, OrderCreated> records = consumer.poll(Duration.ofMillis(500));
    if (records.isEmpty()) continue;

    producer.beginTransaction();
    try {
        for (ConsumerRecord<String, OrderCreated> record : records) {
            producer.send(new ProducerRecord<>("orders.order.enriched", record.key(), enrich(record.value())));
        }
        producer.sendOffsetsToTransaction(currentOffsets(records), consumer.groupMetadata());
        producer.commitTransaction();
    } catch (KafkaException e) {
        producer.abortTransaction();
    }
}
```

Use Kafka Streams when the pipeline is Kafka-to-Kafka and involves joins, windows, or state. Set `processing.guarantee=exactly_once_v2` and the framework manages the transaction boundaries.

## Error Handling

### Classify before retrying

| Failure | Example | Action |
|---------|---------|--------|
| Transient | Downstream timeout, connection reset | Retry with backoff |
| Permanent | Deserialization error, validation failure | Send to DLQ immediately |
| Unknown | Uncaught exception | Retry a bounded number of times, then DLQ |

### Retry topic with dead-letter fallback

```java
void handle(ConsumerRecord<String, byte[]> record) {
    int attempt = headerInt(record, "x-attempt", 0);
    try {
        process(record);
    } catch (TransientException e) {
        if (attempt < MAX_ATTEMPTS) {
            republish(record, "orders.order.created.retry", attempt + 1, e);
        } else {
            republish(record, "orders.order.created.dlq", attempt, e);
        }
    } catch (PermanentException e) {
        republish(record, "orders.order.created.dlq", attempt, e);
    }
}

void republish(ConsumerRecord<String, byte[]> src, String topic, int attempt, Exception cause) {
    ProducerRecord<String, byte[]> out = new ProducerRecord<>(topic, src.key(), src.value());
    src.headers().forEach(h -> out.headers().add(h));
    out.headers()
        .add("x-attempt", Integer.toString(attempt).getBytes(UTF_8))
        .add("x-origin-topic", src.topic().getBytes(UTF_8))
        .add("x-origin-partition", Integer.toString(src.partition()).getBytes(UTF_8))
        .add("x-origin-offset", Long.toString(src.offset()).getBytes(UTF_8))
        .add("x-exception", cause.getClass().getName().getBytes(UTF_8))
        .add("x-failed-at", Instant.now().toString().getBytes(UTF_8));
    producer.send(out);
}
```

The retry consumer sleeps for its backoff before processing, or reads the `x-failed-at` header and pauses the partition until the delay has elapsed. Keep the original key so retries stay ordered relative to each other.

Every DLQ needs an owner, an alert on non-zero lag, and a documented replay procedure. A DLQ nobody reads is a silent data loss.

### Poison pills

A record that fails deserialization will block the partition forever if the consumer crashes on it. Use an error-handling deserializer (Spring's `ErrorHandlingDeserializer`, or wrap the deserializer yourself) that yields a marker value the handler routes straight to the DLQ.

## Schema Management

- Use a schema registry with Avro, Protobuf, or JSON Schema. Raw JSON with no contract is the top cause of consumer breakage in event-driven systems.
- Default compatibility is `BACKWARD`, which means new schemas can read old data. Under `BACKWARD` you may add optional fields with defaults and remove fields, but you may not add required fields or rename existing ones.
- Upgrade consumers before producers under `BACKWARD`. Reverse the order under `FORWARD`. Use `FULL` when deployment order cannot be controlled.
- Never change the key schema. A different key encoding routes the same entity to a different partition and breaks ordering and compaction.
- Version topics only for breaking changes (`orders.order.created.v2`), then run both until every consumer has migrated.

## Testing

### Integration test against a real broker

```java
@Testcontainers
class OrderConsumerIT {

    @Container
    static final KafkaContainer kafka = new KafkaContainer("apache/kafka:3.8.0");

    @Test
    void processesOrderAndCommitsOffset() {
        String bootstrap = kafka.getBootstrapServers();
        createTopic(bootstrap, "orders.order.created", 3);

        publish(bootstrap, "orders.order.created", "order-1", sampleEvent());

        OrderConsumer consumer = new OrderConsumer(bootstrap, "billing-service");
        consumer.pollOnce();

        assertThat(repository.findById("order-1")).isPresent();
        assertThat(committedOffset(bootstrap, "billing-service", "orders.order.created")).isEqualTo(1L);
    }
}
```

Equivalents exist for other stacks (`@testcontainers/kafka` for Node, `testcontainers.kafka` for Python). Mock the client only for unit tests of serialization or routing logic. Anything involving commits, rebalances, or transactions needs a broker.

### What to cover

- Duplicate delivery of the same event leaves the system in the same state
- A processing failure does not advance the committed offset
- A record that fails deserialization lands in the DLQ with origin headers
- Consumer restart resumes from the committed offset, not from the beginning

## Operations Checklist

```bash
# Consumer lag per partition (the primary health signal)
kafka-consumer-groups --bootstrap-server broker-1:9092 --describe --group billing-service

# Under-replicated partitions (should be zero)
kafka-topics --bootstrap-server broker-1:9092 --describe --under-replicated-partitions

# Reset a group to reprocess from a timestamp (stop consumers first)
kafka-consumer-groups --bootstrap-server broker-1:9092 --group billing-service \
  --topic orders.order.created --reset-offsets --to-datetime 2026-09-01T00:00:00.000 --execute
```

Alert on consumer lag growth rate rather than an absolute number, on any under-replicated partition, on DLQ lag above zero, and on rebalance frequency. Export client metrics (`records-lag-max`, `commit-latency-avg`, `record-error-rate`) to the same dashboard as broker metrics.

## Anti-Patterns

```java
// WRONG: auto-commit with side effects. A crash after the commit timer fires and
// before process() finishes loses the record.
props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, true);
for (ConsumerRecord<String, Event> record : consumer.poll(timeout)) {
    process(record);
}

// WRONG: commit before processing. Same loss window, made explicit.
consumer.commitSync();
process(records);

// WRONG: swallow and skip. The failure is invisible and the record is gone.
try { process(record); } catch (Exception e) { log.warn("skipping", e); }

// WRONG: null key when downstream needs per-entity ordering.
new ProducerRecord<>("orders.order.created", null, event);

// WRONG: 20 MB payloads. Store the blob in object storage and publish a reference.
new ProducerRecord<>("documents.uploaded", docId, pdfBytes);
```

Other patterns to reject in review include the following.

- Using Kafka as a request-reply RPC bus. Latency and correlation handling make HTTP or gRPC the better fit.
- Using Kafka as the system of record without compaction, backups, and a replay plan.
- One consumer group per instance for a workload that should share partitions.
- Blocking network calls inside `eachMessage` or the poll loop with no timeout, which starves heartbeats.
- Creating topics from application code at startup with defaults (`replication.factor=1`).
- Sharing a `transactional.id` between instances, which fences the older producer.

## Best Practices

- Producers use `enable.idempotence=true` and `acks=all`. Consumers use manual commit after processing. Handlers are idempotent.
- Every topic is created deliberately with explicit partitions, replication factor, `min.insync.replicas`, and retention.
- Every consumer group has a retry path, a DLQ, an owner, and lag alerts.
- Schemas live in a registry with compatibility enforced in CI.
- Headers carry trace ids and origin metadata. Payloads carry business data only.
- Set `client.id` on every client so broker logs and quotas can identify it.
- Load-test with production-shaped keys to surface hot partitions before launch.
- Graceful shutdown closes the consumer so partitions are reassigned immediately.

## Related Skills

- `springboot-patterns` for Spring Kafka listeners, error handlers, and transaction integration
- `quarkus-patterns` for SmallRye Reactive Messaging channels
- `backend-patterns` for the outbox pattern and idempotent API design
- `clickhouse-io` for Kafka table engines and streaming ingestion into ClickHouse
- `redis-patterns` for deduplication caches used by idempotent consumers
- `docker-patterns` for local broker setups in Compose
