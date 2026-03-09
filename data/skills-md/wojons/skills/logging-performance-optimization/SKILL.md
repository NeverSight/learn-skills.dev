---
name: logging-performance-optimization
description: Optimize logging performance including overhead reduction, async logging, buffering, sampling, and performance impact analysis for high-throughput systems
license: MIT
compatibility: opencode
metadata:
  audience: developers, performance engineers, SREs
  category: performance
---

# Logging Performance Optimization

Optimize logging performance by reducing overhead, implementing async logging, buffering strategies, sampling techniques, and analyzing performance impact for high-throughput and latency-sensitive systems.

## When to use me

Use this skill when:
- Logging overhead is impacting application performance
- Building high-throughput systems where logging cost matters
- Optimizing latency-sensitive applications
- Implementing logging for resource-constrained environments
- Diagnosing performance issues related to logging
- Designing logging strategies for large-scale deployments
- Balancing observability needs with performance requirements
- Implementing cost-effective logging for cloud environments
- Tuning logging configurations for optimal performance

## What I do

### 1. Logging Overhead Analysis
- **Measure logging CPU overhead** for different log levels and formats
- **Analyze memory usage** for log buffers and structures
- **Calculate I/O impact** of synchronous vs asynchronous logging
- **Profile logging call sites** to identify performance bottlenecks
- **Benchmark different logging libraries** and configurations
- **Quantify network overhead** for remote log forwarding
- **Measure storage performance impact** for log writing

### 2. Async Logging & Buffering
- **Implement asynchronous loggers** to decouple application from I/O
- **Design buffer strategies** (ring buffers, linked lists, memory-mapped files)
- **Configure buffer sizing** based on throughput and memory constraints
- **Implement backpressure handling** for buffer overflow scenarios
- **Optimize flush strategies** (time-based, size-based, event-based)
- **Handle graceful shutdown** with buffer draining
- **Monitor buffer health** and performance metrics

### 3. Log Sampling Strategies
- **Implement probabilistic sampling** for high-volume logs
- **Design rate-based sampling** to control log volume
- **Create context-aware sampling** based on trace characteristics
- **Implement dynamic sampling** that adjusts based on system load
- **Configure sampling differently per log level** (100% errors, 1% debug)
- **Handle sampled trace completeness** for distributed tracing
- **Implement consistent sampling** for the same trace across services

### 4. Performance Optimization Techniques
- **Lazy evaluation** of log message arguments
- **Conditional logging checks** before expensive operations
- **String building optimization** for log message construction
- **Object serialization minimization** in log statements
- **Thread-local optimizations** for concurrent logging
- **Memory allocation reduction** in logging hot paths
- **CPU cache-friendly logging** data structures

### 5. Cost-Benefit Analysis
- **Calculate observability value** vs performance cost
- **Optimize log detail level** based on environment and needs
- **Implement tiered logging** with different performance characteristics
- **Balance human readability** with machine efficiency
- **Configure environment-specific optimizations**
- **Implement feature flags** for logging performance features
- **Monitor and adjust** based on actual performance impact

## Performance Impact Measurement

### Benchmarking Methodology
```python
import time
import statistics

def benchmark_logging(logger, iterations=10000):
    """Benchmark logging performance"""
    times = []
    
    # Warm up
    for _ in range(1000):
        logger.info("Warm up message")
    
    # Benchmark
    for i in range(iterations):
        start = time.perf_counter_ns()
        logger.info(f"Benchmark message {i}")
        end = time.perf_counter_ns()
        times.append(end - start)
    
    # Calculate statistics
    avg_ns = statistics.mean(times)
    p95_ns = statistics.quantiles(times, n=20)[18]  # 95th percentile
    p99_ns = statistics.quantiles(times, n=100)[98]  # 99th percentile
    
    return {
        "iterations": iterations,
        "average_ns": avg_ns,
        "p95_ns": p95_ns,
        "p99_ns": p99_ns,
        "throughput_per_second": 1_000_000_000 / avg_ns
    }
```

### Overhead Calculation
```
Logging Performance Analysis
───────────────────────────
Configuration: JSON structured logging, file appender

Baseline (no logging):
- Average request latency: 45ms
- Throughput: 2,222 requests/second
- CPU utilization: 35%

With INFO-level logging:
- Average request latency: 52ms (+15.5%)
- Throughput: 1,923 requests/second (-13.5%)
- CPU utilization: 42% (+7 percentage points)

With DEBUG-level logging:
- Average request latency: 89ms (+97.8%)
- Throughput: 1,124 requests/second (-49.4%)
- CPU utilization: 58% (+23 percentage points)

Cost Analysis:
- INFO logging: Acceptable overhead for production
- DEBUG logging: Unacceptable for production at scale
- Recommendation: Sample DEBUG logs at 1% rate
```

## Async Logging Patterns

### Ring Buffer Implementation
```java
public class AsyncLogger {
    private final RingBuffer<LogEvent> buffer;
    private final Thread writerThread;
    private volatile boolean running = true;
    
    public AsyncLogger(int bufferSize) {
        this.buffer = new RingBuffer<>(bufferSize);
        this.writerThread = new Thread(this::writeLoop);
        this.writerThread.start();
    }
    
    public void log(LogLevel level, String message, Map<String, Object> context) {
        LogEvent event = new LogEvent(level, message, context, System.currentTimeMillis());
        
        // Non-blocking offer, drop if buffer full (backpressure)
        if (!buffer.offer(event)) {
            droppedEvents.increment();
            if (shouldLogDropWarning()) {
                syncLogWarning("Log buffer full, dropped event");
            }
        }
    }
    
    private void writeLoop() {
        while (running || !buffer.isEmpty()) {
            LogEvent event = buffer.poll(100, TimeUnit.MILLISECONDS);
            if (event != null) {
                writeToDestination(event);
            }
        }
    }
}
```

### Lazy Evaluation Pattern
```python
class LazyLogger:
    def __init__(self, logger):
        self.logger = logger
    
    def debug(self, message_factory, **context):
        """Only evaluate message if debug logging is enabled"""
        if self.logger.isEnabledFor(logging.DEBUG):
            # Evaluate the expensive message factory
            message = message_factory()
            self.logger.debug(message, extra=context)

# Usage
logger.debug(lambda: f"Expensive debug: {expensive_operation()}", user_id=user.id)
```

## Sampling Strategies

### Probabilistic Sampling
```go
type Sampler struct {
    rate    float64 // 0.0 to 1.0
    rng     *rand.Rand
    mu      sync.Mutex
}

func (s *Sampler) ShouldSample(traceID string) bool {
    s.mu.Lock()
    defer s.mu.Unlock()
    
    // Use trace ID for consistent sampling decision
    hash := fnv.New64a()
    hash.Write([]byte(traceID))
    seed := hash.Sum64()
    s.rng.Seed(int64(seed))
    
    return s.rng.Float64() < s.rate
}

// Usage in logging
if sampler.ShouldSample(traceID) || level >= WARN {
    logger.Log(level, message, fields...)
}
```

### Rate-Based Sampling
```typescript
class RateLimitingSampler {
    private buckets = new Map<string, { count: number, resetTime: number }>();
    private readonly windowMs = 60000; // 1 minute
    
    shouldSample(key: string, limitPerMinute: number): boolean {
        const now = Date.now();
        let bucket = this.buckets.get(key);
        
        if (!bucket || now > bucket.resetTime) {
            bucket = { count: 0, resetTime: now + this.windowMs };
            this.buckets.set(key, bucket);
        }
        
        if (bucket.count < limitPerMinute) {
            bucket.count++;
            return true;
        }
        
        return false;
    }
}

// Sample debug logs at 100 per minute per user
if (level === 'DEBUG') {
    if (!sampler.shouldSample(`debug:${userId}`, 100)) {
        return; // Don't log
    }
}
```

## Performance Optimization Examples

### Conditional Logging Check
```java
// BAD: Expensive toString() always called
logger.debug("User object: " + user.toString());

// GOOD: Check level before expensive operation
if (logger.isDebugEnabled()) {
    logger.debug("User object: " + user.toString());
}

// BETTER: Use parameterized logging with lazy evaluation
logger.debug("User object: {}", () -> user.toString());
```

### String Building Optimization
```python
# BAD: Multiple string concatenations
logger.info(f"User {user.id} with email {user.email} performed action {action} on {timestamp}")

# GOOD: Structured logging with separate fields
logger.info("User action performed",
    user_id=user.id,
    user_email=user.email,
    action=action,
    timestamp=timestamp.isoformat()
)

# BETTER: Use logging adapter that accepts kwargs
structured_logger.info(
    "User action performed",
    **user.to_log_dict(),
    action=action,
    timestamp=timestamp
)
```

## Examples

```bash
# Benchmark logging performance
npm run logging-performance:benchmark -- --iterations 100000 --levels "DEBUG,INFO,ERROR"

# Analyze logging overhead in production
npm run logging-performance:analyze-overhead -- --duration 300 --output overhead.json

# Configure async logging
npm run logging-performance:configure-async -- --buffer-size 10000 --flush-interval 1000

# Implement log sampling
npm run logging-performance:configure-sampling -- --debug-rate 0.01 --info-rate 1.0 --error-rate 1.0

# Optimize existing logging
npm run logging-performance:optimize -- --path src/ --transform "conditional-checks,string-optimization"
```

## Output format

### Performance Optimization Configuration:
```yaml
performance:
  async_logging:
    enabled: true
    buffer_size: 10000
    flush_interval_ms: 1000
    overflow_policy: "drop"
    
  sampling:
    enabled: true
    strategies:
      - type: "probabilistic"
        level: "DEBUG"
        rate: 0.01  # 1% of debug logs
      - type: "probabilistic"
        level: "TRACE"
        rate: 0.001  # 0.1% of trace logs
      - type: "rate_limiting"
        level: "INFO"
        per_minute: 1000  # Max 1000 INFO logs per minute per service
      - type: "none"
        level: "ERROR"  # All errors logged
        
  optimization:
    lazy_evaluation: true
    conditional_checks: true
    structured_format: true
    buffer_pooling: true
    thread_local_buffers: true
    
  monitoring:
    metrics:
      - logging_latency_p50
      - logging_latency_p99
      - buffer_utilization
      - dropped_logs
      - sampling_rate
    alerts:
      - logging_latency > 10ms
      - buffer_utilization > 90%
      - dropped_logs > 100/minute
      
  cost_control:
    max_logs_per_second: 1000
    storage_budget_per_day_gb: 10
    network_bandwidth_mbps: 100
```

### Performance Analysis Report:
```
Logging Performance Analysis
────────────────────────────
Application: payment-service
Environment: production
Analysis Period: 2026-02-26 18:00-19:00

Performance Metrics:
- Average logging latency: 1.2ms
- 95th percentile latency: 4.5ms
- 99th percentile latency: 12.3ms
- Throughput: 850 logs/second
- CPU overhead: 8.5%
- Memory usage: 45MB (buffers)

Bottleneck Analysis:
1. JSON serialization: 45% of logging latency
2. File I/O blocking: 30% of logging latency
3. String formatting: 15% of logging latency
4. Context extraction: 10% of logging latency

Optimization Opportunities:
✅ Already implemented: Async logging with 10K buffer
⚠️  Opportunity: JSON serialization optimization (potential 45% reduction)
⚠️  Opportunity: Lazy evaluation for debug logs (potential 30% reduction)
⚠️  Opportunity: Conditional level checks (potential 15% reduction)
❌ Critical: File I/O blocking main thread in 2% of cases

Cost Analysis:
- Current logging cost: $450/month (storage + processing)
- Optimized cost estimate: $225/month (50% reduction)
- Performance improvement estimate: 65% latency reduction

Recommendations:
1. HIGH PRIORITY: Fix file I/O blocking main thread
2. MEDIUM PRIORITY: Implement JSON serialization optimization
3. MEDIUM PRIORITY: Add lazy evaluation for debug logs
4. LOW PRIORITY: Implement conditional level checks
5. LOW PRIORITY: Review sampling rates for further optimization

Expected Impact:
- Latency reduction: 65% (from 1.2ms to 0.42ms average)
- CPU overhead reduction: 50% (from 8.5% to 4.25%)
- Cost reduction: 50% (from $450 to $225/month)
- Throughput improvement: 40% (from 850 to 1190 logs/second)
```

## Notes

- **Measure before optimizing** - use profiling to identify actual bottlenecks
- **Balance performance with debuggability** - don't optimize away necessary logs
- **Consider different optimization strategies** for different environments
- **Monitor optimization impact** to ensure no regressions
- **Test under load** - logging performance characteristics change under pressure
- **Consider GC impact** - logging can generate garbage collection pressure
- **Document performance optimizations** for maintenance and understanding
- **Regularly review and update** optimizations as code and requirements change
- **Consider trade-offs** between latency, throughput, and memory usage
- **Implement gradual rollout** of performance optimizations with monitoring