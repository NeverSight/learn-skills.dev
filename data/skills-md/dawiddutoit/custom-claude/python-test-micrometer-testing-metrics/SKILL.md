---
name: python-test-micrometer-testing-metrics
description: |
  Tests custom Micrometer metrics in unit and integration tests using SimpleMeterRegistry. Use when writing tests for services that record metrics, validating metric values after operations, testing percentiles and histograms, or asserting metric behavior without full Spring context. Essential for ensuring metrics are accurately recorded in business logic.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# Micrometer Testing Metrics

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#quick-start)

**How to Implement** → [Step-by-Step](#instructions) | [Test Registry Setup](#step-1-choose-the-right-registry-for-your-test) | [Examples](#examples)

**Help** → [Anti-Patterns](#anti-patterns-to-avoid) | [Requirements](#requirements)

**Reference** → [Related Skills](#see-also)

## Purpose

Testing metrics requires explicit registry setup since Micrometer doesn't auto-wire in unit tests. This skill shows how to verify that custom metrics are correctly recorded in unit tests (SimpleMeterRegistry), integration tests (@AutoConfigureMetrics), and percentile/histogram calculations.

## When to Use

Use this skill when:
- Writing unit tests for services that record metrics
- Validating metric values after business operations
- Testing percentiles and histogram configurations
- Asserting metric behavior without full Spring context
- Verifying counter increments, timer durations, or gauge values
- Testing integration with Spring Boot Actuator
- Debugging why metrics aren't being recorded in tests

## Quick Start

For unit tests, use `SimpleMeterRegistry`:

```java
class ChargeServiceTest {

    private SimpleMeterRegistry registry;
    private ChargeService chargeService;

    @BeforeEach
    void setUp() {
        registry = new SimpleMeterRegistry();
        chargeService = new ChargeService(registry);
    }

    @Test
    void testChargeProcessingRecordsMetrics() {
        Charge charge = new Charge("SUP123", BigDecimal.valueOf(150.00));

        chargeService.processCharge(charge);

        Counter counter = registry.get("charge.processed").counter();
        assertThat(counter.count()).isEqualTo(1);
    }
}
```

## Instructions

### Step 1: Choose the Right Registry for Your Test

**SimpleMeterRegistry** (unit tests, no Spring):
- Use for testing service logic in isolation
- Fast, no Spring context startup
- Meters accessible immediately after recording
- No percentile calculations (use assertions instead)

**MeterRegistry with @AutoConfigureMetrics** (integration tests):
- Use when testing with Spring context
- Spring auto-configures actual metrics
- Slower but tests real behavior
- Supports percentiles if configured

**CompositeMeterRegistry** (multi-backend testing):
- Use when testing with multiple backends
- Rarely needed in unit tests

```java
// ❌ Wrong: no registry
class ServiceTest {
    private Service service = new Service(); // Needs registry!
}

// ✅ Unit test: SimpleMeterRegistry
class ServiceTest {
    private SimpleMeterRegistry registry = new SimpleMeterRegistry();
    private Service service = new Service(registry);
}

// ✅ Integration test: Spring auto-configures
@SpringBootTest
@AutoConfigureMetrics
class ServiceIntegrationTest {
    @Autowired private MeterRegistry registry;
    @Autowired private Service service;
}
```

### Step 2: Set Up Test Fixtures

Create test fixtures for common patterns:

```java
// Base test class for metrics testing
class MetricsTestBase {

    protected SimpleMeterRegistry registry;

    @BeforeEach
    void setUp() {
        registry = new SimpleMeterRegistry();
    }

    /**
     * Assert that a counter with given name and tags exists and has expected count.
     */
    protected void assertCounterValue(String name, long expectedValue, Tag... tags) {
        Counter counter = registry.get(name)
            .tags(tags)
            .counter();

        assertThat(counter.count())
            .as("Counter %s with tags %s", name, Arrays.asList(tags))
            .isEqualTo(expectedValue);
    }

    /**
     * Assert that a timer with given name has recorded expected count.
     */
    protected void assertTimerCount(String name, long expectedCount, Tag... tags) {
        Timer timer = registry.get(name)
            .tags(tags)
            .timer();

        assertThat(timer.count())
            .as("Timer %s count with tags %s", name, Arrays.asList(tags))
            .isEqualTo(expectedCount);
    }

    /**
     * Assert that a distribution summary has expected count and total.
     */
    protected void assertDistributionSummary(
            String name,
            long expectedCount,
            double expectedTotal,
            Tag... tags) {

        DistributionSummary summary = registry.get(name)
            .tags(tags)
            .summary();

        assertThat(summary.count())
            .as("DistributionSummary %s count", name)
            .isEqualTo(expectedCount);

        assertThat(summary.totalAmount())
            .as("DistributionSummary %s total", name)
            .isCloseTo(expectedTotal, within(0.01));
    }

    /**
     * List all metrics for debugging.
     */
    protected void printMetrics() {
        registry.getMeters().forEach(meter -> {
            System.out.println(meter.getId().getName() +
                             " [" + meter.getId().getTags() + "]: " +
                             meter.measure());
        });
    }
}
```

### Step 3: Test Counter Metrics

Test that counters increment correctly:

```java
class ChargeServiceTest extends MetricsTestBase {

    private ChargeService chargeService;

    @BeforeEach
    void setUp() {
        super.setUp();
        chargeService = new ChargeService(registry);
    }

    @Test
    void testChargeProcessingIncrementsCounter() {
        Charge charge = new Charge("SUP123", BigDecimal.valueOf(150.00));

        chargeService.processCharge(charge);

        assertCounterValue("charge.processed", 1);
    }

    @Test
    void testMultipleChargesIncrementCounter() {
        chargeService.processCharge(new Charge("SUP1", BigDecimal.valueOf(100)));
        chargeService.processCharge(new Charge("SUP2", BigDecimal.valueOf(200)));
        chargeService.processCharge(new Charge("SUP3", BigDecimal.valueOf(300)));

        assertCounterValue("charge.processed", 3);
    }

    @Test
    void testChargeRejectionRecordsWithReason() {
        chargeService.rejectCharge("validation");
        chargeService.rejectCharge("duplicate");
        chargeService.rejectCharge("validation");

        assertCounterValue("charge.rejected", 2, Tag.of("reason", "validation"));
        assertCounterValue("charge.rejected", 1, Tag.of("reason", "duplicate"));
    }
}
```

### Step 4: Test Timer Metrics

Test that timers record duration:

```java
class ChargeProcessingTest extends MetricsTestBase {

    private ChargeService service;

    @BeforeEach
    void setUp() {
        super.setUp();
        service = new ChargeService(registry);
    }

    @Test
    void testChargeApprovalRecordsDuration() {
        Charge charge = new Charge("SUP123", BigDecimal.valueOf(150.00));

        service.processCharge(charge);

        Timer timer = registry.get("charge.approval.duration").timer();

        assertThat(timer.count()).isEqualTo(1);
        assertThat(timer.totalTime(TimeUnit.MILLISECONDS)).isGreaterThan(0);
    }

    @Test
    void testTimerRecordsAllOperations() {
        for (int i = 0; i < 5; i++) {
            service.processCharge(new Charge("SUP" + i, BigDecimal.ONE));
        }

        Timer timer = registry.get("charge.approval.duration").timer();

        assertThat(timer.count()).isEqualTo(5);
        assertThat(timer.totalTime(TimeUnit.MILLISECONDS))
            .isGreaterThan(timer.count() * 1); // At least 1ms per operation
    }

    @Test
    void testTimerTracksMaxDuration() {
        service.recordApprovalTime(Duration.ofMillis(10));
        service.recordApprovalTime(Duration.ofMillis(100));
        service.recordApprovalTime(Duration.ofMillis(50));

        Timer timer = registry.get("charge.approval.duration").timer();

        assertThat(timer.max(TimeUnit.MILLISECONDS)).isEqualTo(100);
    }
}
```

### Step 5: Test Distribution Summary Metrics

Test value distributions:

```java
class ChargeValueMetricsTest extends MetricsTestBase {

    private ChargeService service;

    @BeforeEach
    void setUp() {
        super.setUp();
        service = new ChargeService(registry);
    }

    @Test
    void testChargeValueDistribution() {
        service.recordCharge(new Charge("SUP1", BigDecimal.valueOf(100)));
        service.recordCharge(new Charge("SUP2", BigDecimal.valueOf(200)));
        service.recordCharge(new Charge("SUP3", BigDecimal.valueOf(300)));

        DistributionSummary summary = registry.get("charge.value").summary();

        assertThat(summary.count()).isEqualTo(3);
        assertThat(summary.totalAmount()).isEqualTo(600.0);
        assertThat(summary.mean()).isCloseTo(200.0, within(0.1));
    }

    @Test
    void testChargeValueMax() {
        service.recordCharge(new Charge("SUP1", BigDecimal.valueOf(500)));
        service.recordCharge(new Charge("SUP2", BigDecimal.valueOf(1000)));

        DistributionSummary summary = registry.get("charge.value").summary();

        assertThat(summary.max()).isEqualTo(1000.0);
    }
}
```

### Step 6: Test Gauge Metrics

Test gauges that fetch values on demand:

```java
class SupplierMetricsTest extends MetricsTestBase {

    private SupplierService service;
    private SupplierRepository repository;

    @BeforeEach
    void setUp() {
        super.setUp();
        repository = mock(SupplierRepository.class);
        service = new SupplierService(registry, repository);
    }

    @Test
    void testActiveSupplierCountGauge() {
        // Mock repository to return supplier count
        when(repository.countActive()).thenReturn(5);

        // Gauge is lazy-evaluated on access
        Gauge gauge = registry.get("supplier.active.count").gauge();

        assertThat(gauge.value()).isEqualTo(5.0);
    }

    @Test
    void testGaugeReflectsChanges() {
        when(repository.countActive())
            .thenReturn(5)      // First call
            .thenReturn(8);     // Second call

        Gauge gauge = registry.get("supplier.active.count").gauge();

        assertThat(gauge.value()).isEqualTo(5.0);

        // Gauge re-evaluates on each access
        assertThat(gauge.value()).isEqualTo(8.0);
    }
}
```

### Step 7: Test with Spring Integration Tests

Use `@AutoConfigureMetrics` for testing with Spring context:

```java
@SpringBootTest
@AutoConfigureMetrics
@AutoConfigureMockMvc
class ChargeControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private MeterRegistry registry;

    @BeforeEach
    void setUp() {
        registry.clear();
    }

    @Test
    void testChargeCreationRecordsMetrics() throws Exception {
        mockMvc.perform(post("/charges")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {
                        "supplierId": "SUP123",
                        "amount": 150.00
                    }
                    """))
            .andExpect(status().isCreated());

        // Verify HTTP metrics
        Timer httpTimer = registry.get("http.server.requests")
            .tag("uri", "/charges")
            .tag("status", "201")
            .timer();

        assertThat(httpTimer.count()).isEqualTo(1);

        // Verify business metrics
        Counter chargeCounter = registry.get("charge.processed")
            .counter();

        assertThat(chargeCounter.count()).isEqualTo(1);
    }

    @Test
    void testHttpMetricsIncludeException() throws Exception {
        mockMvc.perform(post("/charges")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {
                        "supplierId": null,
                        "amount": 0
                    }
                    """))
            .andExpect(status().isBadRequest());

        Timer httpTimer = registry.get("http.server.requests")
            .tag("uri", "/charges")
            .tag("status", "400")
            .timer();

        assertThat(httpTimer.count()).isEqualTo(1);
    }
}
```

### Step 8: Test Percentiles

Test that percentiles are calculated correctly:

```java
class PercentileTest {

    private SimpleMeterRegistry registry;

    @BeforeEach
    void setUp() {
        registry = new SimpleMeterRegistry();
    }

    @Test
    void testTimerPercentiles() {
        Timer timer = Timer.builder("test.timer")
            .publishPercentiles(0.5, 0.95, 0.99)
            .register(registry);

        // Record ordered samples
        long[] samples = {10, 50, 100, 200, 500, 1000};
        for (long sample : samples) {
            timer.record(sample, TimeUnit.MILLISECONDS);
        }

        // Get snapshot with percentiles
        Snapshot snapshot = timer.takeSnapshot();

        // Verify percentiles (note: exact values depend on implementation)
        assertThat(snapshot.percentileValues())
            .extracting(ValueAtPercentile::percentile)
            .contains(0.5, 0.95, 0.99);

        assertThat(snapshot.percentileValues()[0].value(TimeUnit.MILLISECONDS))
            .isBetween(50.0, 150.0); // P50 should be around median
    }

    @Test
    void testHistogramBuckets() {
        Timer timer = Timer.builder("test.timer")
            .serviceLevelObjectives(
                Duration.ofMillis(10).toNanos(),
                Duration.ofMillis(100).toNanos(),
                Duration.ofMillis(500).toNanos()
            )
            .register(registry);

        timer.record(5, TimeUnit.MILLISECONDS);
        timer.record(50, TimeUnit.MILLISECONDS);
        timer.record(200, TimeUnit.MILLISECONDS);
        timer.record(1000, TimeUnit.MILLISECONDS);

        List<Measurement> measurements = timer.measure();

        // Verify count
        long count = measurements.stream()
            .filter(m -> m.getStatistic() == Statistic.COUNT)
            .mapToLong(m -> (long) m.getValue())
            .sum();
        assertThat(count).isEqualTo(4);
    }
}
```

## Examples

### Example 1: Complete Service Test

```java
class InvoiceServiceTest extends MetricsTestBase {

    private InvoiceService service;
    private InvoiceRepository repository;

    @BeforeEach
    void setUp() {
        super.setUp();
        repository = mock(InvoiceRepository.class);
        service = new InvoiceService(registry, repository);
    }

    @Test
    void testInvoiceGenerationRecordsMetrics() {
        List<Charge> charges = List.of(
            new Charge("SUP1", BigDecimal.valueOf(100)),
            new Charge("SUP2", BigDecimal.valueOf(200))
        );

        Invoice invoice = service.generateInvoice(charges);

        // Verify counter
        assertCounterValue("invoice.generated", 1);

        // Verify amount distribution
        assertDistributionSummary(
            "invoice.amount",
            1,
            300.0
        );

        // Verify generation time
        Timer generationTimer = registry.get("invoice.generation.duration")
            .timer();
        assertThat(generationTimer.count()).isEqualTo(1);
    }

    @Test
    void testInvoiceSentRecordsMetric() {
        Invoice invoice = service.generateInvoice(List.of());

        service.sendInvoice(invoice);

        assertCounterValue("invoice.sent", 1, Tag.of("channel", "email"));
    }
}
```

### Example 2: Test Metric Cardinality

Ensure tags stay bounded:

```java
class CardinalityTest extends MetricsTestBase {

    private ChargeService service;

    @BeforeEach
    void setUp() {
        super.setUp();
        service = new ChargeService(registry);
    }

    @Test
    void testChargeRejectionReasonsCategorized() {
        // Record many different rejection reasons
        service.rejectCharge("validation_error_supplier_id_null");
        service.rejectCharge("validation_error_amount_zero");
        service.rejectCharge("duplicate_within_24h");
        service.rejectCharge("supplier_inactive");

        // Should map to bounded categories
        Set<Tag> uniqueTags = registry.get("charge.rejected")
            .getMeterRegistry()
            .getMeters()
            .stream()
            .filter(m -> m.getId().getName().equals("charge.rejected"))
            .flatMap(m -> m.getId().getTags().stream())
            .collect(Collectors.toSet());

        // Only a few categories, not 4+ unique values
        assertThat(uniqueTags)
            .extracting(Tag::getValue)
            .containsOnly("validation", "duplicate", "supplier_issue");
    }

    @Test
    void testNoHighCardinalityTags() {
        // Try to create metrics with unbounded tags
        // Should be rejected or normalized by MeterFilter

        int initialMeterCount = registry.getMeters().size();

        // This would normally create unbounded metrics
        // But service should normalize...
        // (actual implementation depends on service)

        int finalMeterCount = registry.getMeters().size();

        assertThat(finalMeterCount)
            .isLessThan(initialMeterCount + 100); // Reasonable growth
    }
}
```

## Requirements

- Spring Boot 2.1+ with `spring-boot-starter-actuator`
- Micrometer core library (included with Spring Boot)
- JUnit 5 with AssertJ for assertions
- Mockito for mocking repositories/services
- Java 11+

## Anti-Patterns to Avoid

```java
// ❌ Wrong: not clearing registry between tests
@Test
void test1() {
    registry.get("counter").counter().increment();
}

@Test
void test2() {
    // counter from test1 still exists!
    registry.get("counter").counter(); // Wrong count
}

// ✅ Right: clear registry in @BeforeEach
@BeforeEach
void setUp() {
    registry = new SimpleMeterRegistry(); // Fresh registry
}

// ❌ Wrong: ignoring registry failures
Counter counter = registry.get("metric").counter(); // May not exist!

// ✅ Right: assert meter exists with proper tags
Counter counter = registry.get("metric")
    .tag("expected", "value")
    .counter();

// ❌ Wrong: testing without proper registry injection
class ServiceTest {
    private Service service = new Service(); // Registry is null!
}

// ✅ Right: inject registry in constructor
class ServiceTest {
    private SimpleMeterRegistry registry;
    private Service service;

    @BeforeEach
    void setUp() {
        registry = new SimpleMeterRegistry();
        service = new Service(registry);
    }
}
```

## See Also

- [python-micrometer-business-metrics](../python-micrometer-business-metrics/SKILL.md) - Creating business metrics
- [python-micrometer-cardinality-control](../python-micrometer-cardinality-control/SKILL.md) - Managing metric cardinality
- [python-micrometer-metrics-setup](../python-micrometer-metrics-setup/SKILL.md) - Initial configuration
