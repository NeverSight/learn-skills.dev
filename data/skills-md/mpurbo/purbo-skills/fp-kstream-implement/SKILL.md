---
name: fp-kstream-implement
description: >
  Kafka Streams topology implementation using functional core / imperative shell architecture.
  Use this skill when implementing a Kafka Streams topology in code. Triggers:
  "implement this topology", "write the KStream code", "create the processor",
  "set up kafka locally", "write tests for the topology", "kafka docker setup",
  "KStream implementation", "stream processor code", or any request to write, test,
  or run Kafka Streams application code.
  Do NOT use for design, brainstorming, or architecture — use fp-kstream-design for those.
---

# Kafka Topology Implementation Skill

Implement Kafka Streams topologies as testable, deterministic code where all business logic is pure and infrastructure concerns are pushed to the edges.

## Required Reading

Before responding, load the shared reference:

```
cat ${SKILL_PATH}/references/KSA.md
```

Pay special attention to §1 Principles and §6 Compliance Checklist.

For templates:

```
cat ${SKILL_PATH}/templates/build.gradle.kts
cat ${SKILL_PATH}/templates/docker-compose.yml
```

---

## Architecture Rule

Every KStream processor follows three layers:

```
Pure Core (business logic)
  - Stateless transforms: Event → Event
  - State transitions: (State, Event) → State
  - Decision functions: EnrichedEvent → Decision
  - No Kafka imports. No I/O. No side effects.
  - Testable with plain unit tests.
───────────────────────────────────
Topology Wiring (Kafka Streams DSL)
  - Reads from topics
  - Calls pure core functions
  - Writes to topics / state stores
  - Only layer that knows about Kafka
───────────────────────────────────
Infrastructure Shell (entry point + config)
  - KafkaStreams app bootstrap
  - Config, serdes, health checks, shutdown hooks
```

The pure core has **zero dependencies** on Kafka libraries. This is the primary design constraint.

---

## Project Structure

```
src/main/kotlin/com/example/service/
├── core/                    # Pure business logic — NO Kafka imports
│   ├── Models.kt            # Domain types, ADTs, event types
│   ├── Validators.kt        # Event → Result<CleanEvent, Error>
│   ├── Enrichers.kt         # (Event, RefData) → EnrichedEvent
│   ├── StateMachine.kt      # (State, Event) → (State, List<Output>)
│   └── Decisions.kt         # EnrichedEvent → Decision
├── topology/                # Kafka Streams wiring
│   └── ServiceTopology.kt   # StreamsBuilder → Topology
├── serde/                   # Serialization
│   └── JsonSerde.kt
└── App.kt                   # Entry point, config, bootstrap

test/kotlin/com/example/service/
├── core/                    # Unit tests — NO Kafka dependency
│   ├── ValidatorsTest.kt
│   ├── StateMachineTest.kt
│   └── DecisionsTest.kt
└── topology/                # TopologyTestDriver tests
    └── ServiceTopologyTest.kt
```

Java: same structure, replace `.kt` with `.java`. Core package still has zero Kafka imports.

---

## Code Patterns

### Pattern A — Stateless Transform

**Pure core** (no Kafka imports):

```kotlin
// core/Validators.kt
data class RawPayment(val id: String, val amount: Double, val currency: String)
data class ValidPayment(val id: String, val amount: Double, val currency: String)
sealed class ValidationResult {
    data class Valid(val payment: ValidPayment) : ValidationResult()
    data class Invalid(val reason: String) : ValidationResult()
}

fun validate(raw: RawPayment): ValidationResult {
    if (raw.amount <= 0) return ValidationResult.Invalid("amount must be positive")
    if (raw.currency.length != 3) return ValidationResult.Invalid("invalid currency code")
    return ValidationResult.Valid(ValidPayment(raw.id, raw.amount, raw.currency.uppercase()))
}
```

**Topology wiring:**

```kotlin
// topology/ServiceTopology.kt
fun buildTopology(builder: StreamsBuilder): Topology {
    val raw: KStream<String, RawPayment> = builder.stream("raw-payments")
    val (valid, invalid) = raw
        .mapValues { _, v -> validate(v) }  // pure function call
        .branch(
            { _, v -> v is ValidationResult.Valid },
            { _, v -> v is ValidationResult.Invalid }
        )
    valid.mapValues { _, v -> (v as ValidationResult.Valid).payment }.to("valid-payments")
    invalid.mapValues { _, v -> (v as ValidationResult.Invalid).reason }.to("invalid-payments-dlq")
    return builder.build()
}
```

**Test** (no Kafka):

```kotlin
// core/ValidatorsTest.kt
@Test fun `rejects negative amount`() {
    val result = validate(RawPayment("p1", -10.0, "USD"))
    assertIs<ValidationResult.Invalid>(result)
    assertEquals("amount must be positive", result.reason)
}

@Test fun `normalizes currency to uppercase`() {
    val result = validate(RawPayment("p1", 100.0, "usd"))
    assertIs<ValidationResult.Valid>(result)
    assertEquals("USD", result.payment.currency)
}
```

### Pattern B — Stateful FSM

**Pure core** (no Kafka imports):

```kotlin
// core/StateMachine.kt
enum class OrderStatus { CREATED, PAYMENT_PENDING, PAID, SHIPPED, FAILED }
data class OrderState(val orderId: String, val status: OrderStatus)

sealed class OrderEvent {
    data class Created(val orderId: String, val amount: Double) : OrderEvent()
    data class PaymentConfirmed(val orderId: String) : OrderEvent()
    data class PaymentFailed(val orderId: String, val reason: String) : OrderEvent()
    data class Shipped(val orderId: String) : OrderEvent()
}

sealed class OrderOutput {
    data class StateChanged(val state: OrderState) : OrderOutput()
    data class RequestPayment(val orderId: String, val amount: Double) : OrderOutput()
    data class InvalidTransition(val orderId: String, val from: OrderStatus, val event: String) : OrderOutput()
}

// Pure function: (State?, Event) → (State, List<Output>)
fun transition(current: OrderState?, event: OrderEvent): Pair<OrderState, List<OrderOutput>> =
    when (event) {
        is OrderEvent.Created -> {
            if (current != null) current to listOf(OrderOutput.InvalidTransition(event.orderId, current.status, "Created"))
            else {
                val state = OrderState(event.orderId, OrderStatus.PAYMENT_PENDING)
                state to listOf(OrderOutput.StateChanged(state), OrderOutput.RequestPayment(event.orderId, event.amount))
            }
        }
        is OrderEvent.PaymentConfirmed -> {
            if (current?.status != OrderStatus.PAYMENT_PENDING)
                (current ?: OrderState(event.orderId, OrderStatus.FAILED)) to
                    listOf(OrderOutput.InvalidTransition(event.orderId, current?.status ?: OrderStatus.FAILED, "PaymentConfirmed"))
            else {
                val state = current.copy(status = OrderStatus.PAID)
                state to listOf(OrderOutput.StateChanged(state))
            }
        }
        is OrderEvent.PaymentFailed -> {
            val state = (current ?: OrderState(event.orderId, OrderStatus.FAILED)).copy(status = OrderStatus.FAILED)
            state to listOf(OrderOutput.StateChanged(state))
        }
        is OrderEvent.Shipped -> {
            if (current?.status != OrderStatus.PAID)
                (current ?: OrderState(event.orderId, OrderStatus.FAILED)) to
                    listOf(OrderOutput.InvalidTransition(event.orderId, current?.status ?: OrderStatus.FAILED, "Shipped"))
            else {
                val state = current.copy(status = OrderStatus.SHIPPED)
                state to listOf(OrderOutput.StateChanged(state))
            }
        }
    }
```

**Topology wiring:**

```kotlin
// topology/ServiceTopology.kt — Processor only calls pure function
override fun process(record: Record<String, OrderEvent>) {
    val current = store.get(record.key())
    val (newState, outputs) = transition(current, record.value()) // pure function
    store.put(record.key(), newState)
    outputs.forEach { context.forward(record.withValue(it)) }
}
```

**Test** (no Kafka):

```kotlin
// core/StateMachineTest.kt
@Test fun `created order transitions to payment pending`() {
    val (state, outputs) = transition(null, OrderEvent.Created("o1", 100.0))
    assertEquals(OrderStatus.PAYMENT_PENDING, state.status)
    assertTrue(outputs.any { it is OrderOutput.RequestPayment })
}

@Test fun `duplicate creation is invalid transition`() {
    val existing = OrderState("o1", OrderStatus.PAYMENT_PENDING)
    val (_, outputs) = transition(existing, OrderEvent.Created("o1", 100.0))
    assertTrue(outputs.any { it is OrderOutput.InvalidTransition })
}
```

### Pattern C — Enrichment

**Pure core** (no Kafka imports):

```kotlin
// core/Enrichers.kt
data class Transaction(val id: String, val merchantId: String, val amount: Double)
data class MerchantConfig(val merchantId: String, val category: String, val feeRate: Double)
data class EnrichedTransaction(val id: String, val merchantId: String, val amount: Double, val category: String, val fee: Double)

fun enrich(tx: Transaction, config: MerchantConfig?): EnrichedTransaction? {
    config ?: return null  // missing-state policy: drop (caller routes to DLQ)
    return EnrichedTransaction(tx.id, tx.merchantId, tx.amount, config.category, tx.amount * config.feeRate)
}
```

**Test** (no Kafka):

```kotlin
@Test fun `enriches with merchant config`() {
    val result = enrich(Transaction("t1", "m1", 100.0), MerchantConfig("m1", "food", 0.02))
    assertNotNull(result)
    assertEquals("food", result.category)
    assertEquals(2.0, result.fee)
}

@Test fun `returns null when config missing`() {
    assertNull(enrich(Transaction("t1", "m1", 100.0), null))
}
```

---

## Testing Strategy

| Layer | What | How | Coverage Target |
|-------|------|-----|-----------------|
| 1. Unit (Pure Core) | Every state transition, validation, edge case | Plain functions, no Kafka | 80%+ of tests, milliseconds each |
| 2. Topology (TopologyTestDriver) | Wiring: events flow to correct branches, state stores populated, policies triggered | `TopologyTestDriver` in-process | Wiring verification only |
| 3. Integration (Real Kafka) | Serialization, topic config, consumer groups | Testcontainers + real broker | Optional, not for business logic |

**Key rule:** Test business logic directly via pure functions (Layer 1), not through TopologyTestDriver (Layer 2). The topology test verifies wiring, not logic.

```kotlin
// BAD — tests logic through Kafka harness (slow, indirect)
@Test fun `payment on non-existent order fails`() {
    inputTopic.pipeInput("o1", OrderEvent.PaymentConfirmed("o1"))
    val output = outputTopic.readValue()
    assertIs<OrderOutput.InvalidTransition>(output)
}

// GOOD — tests logic directly (fast, direct)
@Test fun `payment on non-existent order fails`() {
    val (_, outputs) = transition(null, OrderEvent.PaymentConfirmed("o1"))
    assertTrue(outputs.any { it is OrderOutput.InvalidTransition })
}
```

---

## Local Development

Docker Compose for local Kafka: `cat ${SKILL_PATH}/templates/docker-compose.yml`

```bash
docker compose up -d                    # start
docker compose exec kafka kafka-topics --list --bootstrap-server kafka:29092  # verify
docker compose exec kafka kafka-topics --create --topic raw-payments --partitions 6 --replication-factor 1 --bootstrap-server kafka:29092
docker compose down                     # stop (preserves data)
docker compose down -v                  # destroy everything
```

macOS with Colima:

```bash
brew install colima docker docker-compose
colima start --cpu 4 --memory 8 --disk 60
docker compose up -d
```

---

## Build Configuration

Gradle template: `cat ${SKILL_PATH}/templates/build.gradle.kts`

Key dependencies:

```kotlin
dependencies {
    implementation("org.apache.kafka:kafka-streams:3.7.0")
    implementation("io.confluent:kafka-streams-avro-serde:7.6.0")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
    testImplementation("org.apache.kafka:kafka-streams-test-utils:3.7.0")
    testImplementation("org.testcontainers:kafka:1.19.7")
}
```

---

## Implementation Checklist

Before submitting a PR:

- [ ] All business logic in `core/` with zero Kafka imports
- [ ] Unit tests cover every state transition and validation rule (fast, no containers)
- [ ] Topology test exists using `TopologyTestDriver`
- [ ] Serdes tested (round-trip serialize/deserialize for every event type)
- [ ] Missing-state policy implemented and tested (not just documented)
- [ ] State store has bounded retention (TTL configured)
- [ ] DLQ topics wired (invalid transitions, failed validations, missing enrichment)
- [ ] No side effects in processors (no HTTP, no DB, no external state)
- [ ] Topology runs against TopologyTestDriver before real Kafka
- [ ] docker-compose.yml exists for local development

---

## Common Mistakes

| Mistake | Bad | Good |
|---------|-----|------|
| Business logic inside Processor class | Inline if/when logic in `process()` | `process()` calls pure `transition()` function |
| Testing logic through TopologyTestDriver | Pipe input → assert output (slow, indirect) | Call pure function directly (fast, direct) |
| GlobalKTable for large data | `builder.globalTable("product-catalog")` loads ALL data everywhere | `builder.table("product-catalog")` with partition-aligned joins |
