---
name: event-driven-architecture
description: >-
  Kafka, RabbitMQ, SQS/SNS, event sourcing, CQRS, saga patterns, dead letter queues, and idempotency. Use when designing asynchronous systems, implementing message-driven workflows, or building event streaming pipelines.
---

# Event-Driven Architecture

## Overview

This skill covers designing and implementing event-driven systems that decouple services through asynchronous message passing. It addresses message broker selection and integration (Kafka, RabbitMQ, SQS/SNS, NATS), event sourcing and CQRS patterns, saga orchestration for distributed transactions, dead letter queues for failure handling, idempotency patterns, event schema evolution, the transactional outbox pattern, and consumer group management.

Use this skill when building microservice architectures, implementing distributed workflows, decoupling services for independent deployment, handling eventual consistency, or replacing synchronous service-to-service calls with asynchronous events.

---

## Core Principles

1. **Events are facts, commands are requests** - Events describe something that happened (`OrderPlaced`, `PaymentReceived`). Commands request an action (`ProcessPayment`, `ShipOrder`). This distinction drives correct system design: events are broadcast, commands are point-to-point.
2. **Idempotency is not optional** - Messages will be delivered at least once (and sometimes more). Every consumer must handle duplicate messages gracefully. Use event IDs, version checks, or database constraints for deduplication.
3. **Schema evolution without breaking consumers** - Event schemas will change. Use backward-compatible evolution (add fields, never remove or rename). Version schemas explicitly and support multiple versions during migration.
4. **Dead letters are not garbage** - Messages that can't be processed go to dead letter queues. These represent bugs, data issues, or edge cases. Monitor DLQs, alert on growth, and build tooling to replay them.
5. **Local transactions, eventual consistency** - Each service owns its data and processes events within local transactions. Cross-service consistency is eventual, not immediate. Design UIs and workflows to handle this.

---

## Key Patterns

### Pattern 1: Event Publishing with Transactional Outbox

**When to use:** When you need to update a database AND publish an event atomically. This prevents the "dual write" problem where the database write succeeds but the event publish fails (or vice versa).

**Implementation:**

```typescript
// The Transactional Outbox Pattern
// 1. Write the event to an outbox table in the SAME database transaction as the business data
// 2. A separate poller/CDC process reads the outbox and publishes to the message broker

interface OutboxEvent {
  id: string;
  aggregateType: string;
  aggregateId: string;
  eventType: string;
  payload: Record<string, unknown>;
  createdAt: Date;
  publishedAt: Date | null;
}

// Step 1: Business operation + outbox write in one transaction
async function placeOrder(order: CreateOrderInput): Promise<Order> {
  return await prisma.$transaction(async (tx) => {
    // Business logic
    const createdOrder = await tx.order.create({
      data: {
        customerId: order.customerId,
        items: { create: order.items },
        total: calculateTotal(order.items),
        status: "PLACED",
      },
      include: { items: true },
    });

    // Write event to outbox (same transaction!)
    await tx.outboxEvent.create({
      data: {
        id: crypto.randomUUID(),
        aggregateType: "Order",
        aggregateId: createdOrder.id,
        eventType: "OrderPlaced",
        payload: {
          orderId: createdOrder.id,
          customerId: createdOrder.customerId,
          items: createdOrder.items,
          total: createdOrder.total,
          placedAt: new Date().toISOString(),
        },
      },
    });

    return createdOrder;
  });
}

// Step 2: Outbox poller publishes events to Kafka/RabbitMQ
async function processOutbox(): Promise<void> {
  const unpublished = await prisma.outboxEvent.findMany({
    where: { publishedAt: null },
    orderBy: { createdAt: "asc" },
    take: 100,
  });

  for (const event of unpublished) {
    try {
      await kafka.producer.send({
        topic: `${event.aggregateType}.${event.eventType}`,
        messages: [
          {
            key: event.aggregateId,
            value: JSON.stringify({
              eventId: event.id,
              eventType: event.eventType,
              aggregateId: event.aggregateId,
              payload: event.payload,
              timestamp: event.createdAt.toISOString(),
            }),
            headers: {
              "event-type": event.eventType,
              "event-id": event.id,
            },
          },
        ],
      });

      await prisma.outboxEvent.update({
        where: { id: event.id },
        data: { publishedAt: new Date() },
      });
    } catch (error) {
      console.error(`Failed to publish outbox event ${event.id}:`, error);
      // Will be retried on next poll cycle
    }
  }
}

// Run poller on interval
setInterval(processOutbox, 5000); // Every 5 seconds
```

**Why:** The dual-write problem is the most common source of data inconsistency in event-driven systems. If you write to the database and then publish an event, the publish can fail after the database write succeeds. The outbox pattern guarantees that if the business data is written, the event will eventually be published.

---

### Pattern 2: Idempotent Event Consumer

**When to use:** Every event consumer. Messages are delivered at least once in all major brokers.

**Implementation:**

```typescript
// Kafka consumer with idempotency
import { Kafka, EachMessagePayload } from "kafkajs";

const kafka = new Kafka({
  clientId: "order-service",
  brokers: [process.env.KAFKA_BROKERS!],
});

const consumer = kafka.consumer({ groupId: "payment-processor" });

interface DomainEvent {
  eventId: string;
  eventType: string;
  aggregateId: string;
  payload: Record<string, unknown>;
  timestamp: string;
}

// Event handler registry
const handlers: Record<string, (event: DomainEvent) => Promise<void>> = {
  OrderPlaced: async (event) => {
    const { orderId, total, customerId } = event.payload as {
      orderId: string;
      total: number;
      customerId: string;
    };

    // Create payment intent (idempotent via orderId)
    await processPayment(orderId, total, customerId);
  },

  PaymentFailed: async (event) => {
    const { orderId } = event.payload as { orderId: string };
    await cancelOrder(orderId);
  },
};

async function startConsumer() {
  await consumer.connect();
  await consumer.subscribe({
    topics: ["Order.OrderPlaced", "Payment.PaymentFailed"],
    fromBeginning: false,
  });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }: EachMessagePayload) => {
      const event: DomainEvent = JSON.parse(message.value!.toString());

      // 1. Idempotency check - have we already processed this event?
      const alreadyProcessed = await prisma.processedEvent.findUnique({
        where: { eventId: event.eventId },
      });

      if (alreadyProcessed) {
        console.log(`Skipping duplicate event: ${event.eventId}`);
        return;
      }

      // 2. Process the event
      const handler = handlers[event.eventType];
      if (!handler) {
        console.warn(`No handler for event type: ${event.eventType}`);
        return;
      }

      try {
        await prisma.$transaction(async (tx) => {
          // Record event as processed (within the same transaction as business logic)
          await tx.processedEvent.create({
            data: {
              eventId: event.eventId,
              eventType: event.eventType,
              processedAt: new Date(),
            },
          });

          // Execute business logic
          await handler(event);
        });
      } catch (error) {
        console.error(`Error processing event ${event.eventId}:`, error);
        // Don't commit offset - message will be redelivered
        throw error;
      }
    },
  });
}
```

**Why:** Kafka, RabbitMQ, and SQS all guarantee at-least-once delivery, meaning consumers will see duplicates during rebalances, retries, and network issues. Recording processed event IDs in the same transaction as business logic ensures exactly-once processing semantics.

---

### Pattern 3: Saga Orchestration

**When to use:** When a business process spans multiple services and needs coordinated rollback if any step fails.

**Implementation:**

```typescript
// Saga orchestrator for order fulfillment
// Order -> Payment -> Inventory -> Shipping

interface SagaStep {
  name: string;
  execute: (context: SagaContext) => Promise<void>;
  compensate: (context: SagaContext) => Promise<void>;
}

interface SagaContext {
  orderId: string;
  customerId: string;
  items: OrderItem[];
  total: number;
  // Accumulated state from previous steps
  paymentId?: string;
  reservationId?: string;
  shipmentId?: string;
}

const orderFulfillmentSaga: SagaStep[] = [
  {
    name: "processPayment",
    execute: async (ctx) => {
      const payment = await paymentService.charge({
        orderId: ctx.orderId,
        amount: ctx.total,
        customerId: ctx.customerId,
      });
      ctx.paymentId = payment.id;
    },
    compensate: async (ctx) => {
      if (ctx.paymentId) {
        await paymentService.refund(ctx.paymentId);
      }
    },
  },
  {
    name: "reserveInventory",
    execute: async (ctx) => {
      const reservation = await inventoryService.reserve({
        orderId: ctx.orderId,
        items: ctx.items,
      });
      ctx.reservationId = reservation.id;
    },
    compensate: async (ctx) => {
      if (ctx.reservationId) {
        await inventoryService.release(ctx.reservationId);
      }
    },
  },
  {
    name: "createShipment",
    execute: async (ctx) => {
      const shipment = await shippingService.create({
        orderId: ctx.orderId,
        items: ctx.items,
        customerId: ctx.customerId,
      });
      ctx.shipmentId = shipment.id;
    },
    compensate: async (ctx) => {
      if (ctx.shipmentId) {
        await shippingService.cancel(ctx.shipmentId);
      }
    },
  },
];

async function executeSaga(
  steps: SagaStep[],
  context: SagaContext
): Promise<void> {
  const completedSteps: SagaStep[] = [];

  for (const step of steps) {
    try {
      console.log(`Executing saga step: ${step.name}`);
      await step.execute(context);
      completedSteps.push(step);
    } catch (error) {
      console.error(`Saga step "${step.name}" failed:`, error);

      // Compensate in reverse order
      for (const completedStep of completedSteps.reverse()) {
        try {
          console.log(`Compensating: ${completedStep.name}`);
          await completedStep.compensate(context);
        } catch (compensateError) {
          // Log compensation failure for manual intervention
          console.error(
            `CRITICAL: Compensation for "${completedStep.name}" failed:`,
            compensateError
          );
          await alertOps({
            type: "saga_compensation_failure",
            saga: "orderFulfillment",
            step: completedStep.name,
            orderId: context.orderId,
            error: compensateError,
          });
        }
      }

      throw new SagaFailedError(step.name, error as Error);
    }
  }
}
```

**Why:** Distributed transactions across services are impractical (two-phase commit doesn't scale). Sagas provide an alternative: a sequence of local transactions with compensating actions for rollback. If payment succeeds but inventory reservation fails, the saga refunds the payment automatically.

---

### Pattern 4: Dead Letter Queue Handling

**When to use:** Every event-driven system needs a strategy for messages that cannot be processed.

**Implementation:**

```typescript
// SQS dead letter queue handling pattern
import { SQSClient, SendMessageCommand, ReceiveMessageCommand } from "@aws-sdk/client-sqs";

// Configure main queue with DLQ
const queueConfig = {
  RedrivePolicy: JSON.stringify({
    deadLetterTargetArn: process.env.DLQ_ARN,
    maxReceiveCount: 3, // Move to DLQ after 3 failed processing attempts
  }),
};

// DLQ monitoring and replay
async function monitorDLQ(): Promise<void> {
  const messages = await sqs.send(new ReceiveMessageCommand({
    QueueUrl: process.env.DLQ_URL,
    MaxNumberOfMessages: 10,
    WaitTimeSeconds: 20,
    MessageAttributeNames: ["All"],
  }));

  if (messages.Messages && messages.Messages.length > 0) {
    // Alert operations team
    await alertOps({
      type: "dlq_messages",
      count: messages.Messages.length,
      queue: "order-events-dlq",
      sample: messages.Messages[0].Body,
    });
  }
}

// Replay DLQ messages back to the main queue
async function replayDLQMessages(
  count: number,
  filter?: (msg: Record<string, unknown>) => boolean
): Promise<{ replayed: number; skipped: number }> {
  let replayed = 0;
  let skipped = 0;

  for (let i = 0; i < count; i++) {
    const response = await sqs.send(new ReceiveMessageCommand({
      QueueUrl: process.env.DLQ_URL,
      MaxNumberOfMessages: 1,
      WaitTimeSeconds: 0,
    }));

    const message = response.Messages?.[0];
    if (!message) break;

    const body = JSON.parse(message.Body!);

    if (filter && !filter(body)) {
      skipped++;
      continue;
    }

    // Replay to main queue
    await sqs.send(new SendMessageCommand({
      QueueUrl: process.env.MAIN_QUEUE_URL,
      MessageBody: message.Body!,
      MessageAttributes: message.MessageAttributes,
    }));

    // Delete from DLQ
    await sqs.send(new DeleteMessageCommand({
      QueueUrl: process.env.DLQ_URL,
      ReceiptHandle: message.ReceiptHandle!,
    }));

    replayed++;
  }

  return { replayed, skipped };
}
```

**Why:** Dead letter queues capture messages that fail processing after all retries. Without DLQs, failed messages block the queue or are silently dropped. DLQ monitoring catches bugs (malformed events, missing handlers). Replay tooling recovers from transient issues (downstream service outage) without data loss.

---

## Message Broker Selection Guide

| Broker | Best For | Ordering | Throughput | Persistence |
|---|---|---|---|---|
| **Kafka** | High-throughput event streaming, log compaction | Per-partition | Very high (millions/sec) | Configurable retention |
| **RabbitMQ** | Task queues, routing, request-reply | Per-queue | High (100k/sec) | Optional |
| **SQS/SNS** | Serverless, AWS-native, low ops | Per-FIFO queue | High (3k/sec FIFO, unlimited standard) | 14-day retention |
| **NATS** | Low-latency, cloud-native, lightweight | JetStream | Very high | JetStream for persistence |

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|---|---|---|
| Dual writes (DB + event) without outbox | Data inconsistency when one write fails | Transactional outbox pattern |
| No idempotency in consumers | Duplicate processing on redelivery | Dedup by event ID in same transaction |
| Event payloads too large (> 1MB) | Slow processing, broker limits | Store data in a service, send reference (claim check) |
| Synchronous event handling | Defeats purpose of async architecture | Process events asynchronously with queues |
| No DLQ configured | Failed messages block queue or disappear | Always configure DLQ with alerting |
| Tightly coupled event schemas | Breaking consumers on schema changes | Backward-compatible evolution, explicit versioning |
| Publishing domain events from multiple places | Inconsistent event shapes, missed events | Single publish point (aggregate root / service layer) |

---

## Checklist

- [ ] Transactional outbox pattern for atomic DB + event writes
- [ ] Every consumer is idempotent (event ID deduplication)
- [ ] Dead letter queues configured with alerting and replay tooling
- [ ] Event schemas versioned with backward-compatible evolution
- [ ] Consumer groups configured for each service
- [ ] Retry policy with exponential backoff before DLQ
- [ ] Saga or choreography pattern for cross-service workflows
- [ ] Monitoring: consumer lag, DLQ depth, processing errors
- [ ] Event ordering preserved where required (partition keys)
- [ ] Message broker cluster is fault-tolerant (replication)

---

## Related Resources

- **Skills:** `monitoring-observability` (consumer lag monitoring), `serverless-development` (SQS/Lambda)
- **Skills:** `payment-integration` (payment event flows), `email-systems` (email as async event)
- **Rules:** `rules/stacks/fullstack-nextjs-nestjs.md` (NestJS CQRS modules)
