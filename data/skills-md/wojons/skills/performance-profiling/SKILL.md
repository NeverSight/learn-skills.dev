---
name: performance-profiling
description: Analyze system and application performance using Linux kernel-level tools (perf, ftrace, eBPF, SystemTap) and application-level profiling to identify bottlenecks and optimize performance
license: MIT
compatibility: opencode
metadata:
  audience: developers, devops engineers, SREs, performance engineers, system administrators
  category: performance
---

# Performance Profiling

Analyze system and application performance using comprehensive profiling techniques including Linux kernel-level tools (perf, ftrace, eBPF, SystemTap), application-level profiling, bottleneck identification, and optimization recommendations to improve system responsiveness, throughput, and resource efficiency.

## When to use me

Use this skill when:
- Application performance is slow or degrading
- System resource utilization is high
- Identifying CPU, memory, I/O, or network bottlenecks
- Optimizing application response times
- Debugging performance regressions
- Capacity planning and resource sizing
- Comparing performance before/after changes
- Analyzing production performance issues
- Creating performance baselines
- Tuning system and application parameters

## What I do

### 1. System-Level Profiling
- **CPU profiling**: Analyze CPU usage, context switches, interrupts, scheduler latency
- **Memory profiling**: Analyze memory usage, page faults, swapping, memory leaks
- **I/O profiling**: Analyze disk I/O, file system performance, storage latency
- **Network profiling**: Analyze network throughput, latency, packet loss, connections
- **Kernel profiling**: Analyze kernel functions, system calls, interrupt handlers

### 2. Application-Level Profiling
- **Application CPU usage**: Profile application-specific CPU consumption
- **Memory allocation**: Track heap allocations, garbage collection, memory leaks
- **Function timing**: Measure function execution times and call frequencies
- **Database query profiling**: Analyze SQL query performance and optimization
- **API endpoint profiling**: Measure API response times and throughput

### 3. Tool Integration
- **Linux perf**: CPU profiling, hardware performance counters, tracepoints
- **eBPF/BCC**: Dynamic tracing, custom performance instrumentation
- **Ftrace**: Kernel function tracing, event tracing, latency measurements
- **SystemTap**: System-wide tracing and profiling
- **Application profilers**: Language-specific profiling tools
- **Container profiling**: Docker, Kubernetes performance analysis

### 4. Bottleneck Identification
- **Hot spot detection**: Identify frequently executed code paths
- **Resource contention**: Detect lock contention, CPU starvation, I/O wait
- **Latency analysis**: Measure and analyze latency distributions
- **Scalability analysis**: Identify scalability limits and bottlenecks
- **Anomaly detection**: Detect performance anomalies and regressions

### 5. Optimization Recommendations
- **Code optimizations**: Suggest algorithmic improvements, caching strategies
- **Configuration tuning**: Recommend system and application tuning parameters
- **Architecture improvements**: Suggest architectural changes for performance
- **Resource allocation**: Recommend optimal resource allocation strategies
- **Monitoring setup**: Recommend performance monitoring configurations

### 6. Visualization & Reporting
- **Flame graphs**: Generate CPU and memory flame graphs for visualization
- **Heat maps**: Create latency heat maps for time-series analysis
- **Performance dashboards**: Create real-time performance dashboards
- **Trend analysis**: Analyze performance trends over time
- **Comparison reports**: Compare performance across versions/environments

## Profiling Tools Covered

### Linux Kernel-Level Tools
- **perf**: Linux performance events for CPU profiling, hardware counters
- **eBPF/BCC**: Extended Berkeley Packet Filter for dynamic tracing
- **bpftrace**: High-level tracing language for eBPF
- **Ftrace**: Linux kernel internal tracer for function tracing
- **SystemTap**: System-wide tracing and profiling framework
- **LTTng**: Linux Trace Toolkit next generation
- **ktap**: Lightweight kernel tracing

### Application-Level Tools
- **Java**: JProfiler, YourKit, VisualVM, Async Profiler
- **Python**: cProfile, py-spy, Scalene, line_profiler
- **Node.js**: clinic.js, 0x, node --prof, v8-profiler
- **Go**: pprof, trace, delve, gops
- **Ruby**: ruby-prof, stackprof, rbspy
- **.NET**: dotnet-counters, dotnet-trace, PerfView
- **PHP**: Xdebug, Blackfire, Tideways
- **C/C++**: gprof, Valgrind, Intel VTune, perf

### System Monitoring Tools
- **top/htop**: Process monitoring
- **vmstat**: Virtual memory statistics
- **iostat**: I/O statistics
- **netstat/ss**: Network statistics
- **sar**: System activity reporter
- **dstat**: Versatile resource statistics
- **nmon**: Nigel's performance monitor

### Visualization Tools
- **FlameGraph**: CPU and memory flame graphs
- **perfetto**: System tracing and performance visualization
- **grafana**: Performance dashboard visualization
- **prometheus**: Time-series monitoring and alerting
- **jaeger**: Distributed tracing visualization

## Analysis Techniques

### CPU Profiling with perf
```bash
# Sample CPU usage for 30 seconds
perf record -F 99 -ag -- sleep 30

# Generate flame graph
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg

# Analyze hardware performance counters
perf stat -e cycles,instructions,cache-misses,branch-misses ./application

# Trace system calls
perf trace -e syscalls:sys_enter_* ./application
```

### eBPF Tracing with BCC
```python
from bcc import BPF

# eBPF program to trace function calls
bpf_text = """
#include <uapi/linux/ptrace.h>

struct data_t {
    u64 timestamp;
    u32 pid;
    char comm[TASK_COMM_LEN];
    u64 duration_ns;
};

BPF_HASH(start, u32);
BPF_PERF_OUTPUT(events);

int trace_entry(struct pt_regs *ctx) {
    u32 pid = bpf_get_current_pid_tgid();
    u64 ts = bpf_ktime_get_ns();
    
    start.update(&pid, &ts);
    return 0;
}

int trace_return(struct pt_regs *ctx) {
    u32 pid = bpf_get_current_pid_tgid();
    u64 *tsp = start.lookup(&pid);
    
    if (tsp == 0) {
        return 0;
    }
    
    u64 duration = bpf_ktime_get_ns() - *tsp;
    
    struct data_t data = {};
    data.timestamp = bpf_ktime_get_ns();
    data.pid = pid;
    data.duration_ns = duration;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    
    events.perf_submit(ctx, &data, sizeof(data));
    start.delete(&pid);
    
    return 0;
}
"""

# Attach to function entry and return
bpf = BPF(text=bpf_text)
bpf.attach_uprobe(name="application", sym="function_name", fn_name="trace_entry")
bpf.attach_uretprobe(name="application", sym="function_name", fn_name="trace_return")
```

### Memory Leak Detection
```bash
# Monitor memory allocations
valgrind --leak-check=full --show-leak-kinds=all ./application

# Track heap allocations with eBPF
/usr/share/bcc/tools/memleak -p $(pidof application)

# Analyze memory usage over time
cat /proc/$(pidof application)/smaps | grep -i pss | awk '{total+=$2} END {print total}'

# Monitor garbage collection (Java)
jstat -gc $(pidof java) 1s
```

### Latency Analysis
```python
def analyze_latency_distribution(latency_samples):
    """
    Analyze latency distribution and identify outliers.
    """
    import numpy as np
    from scipy import stats
    
    latencies = np.array(latency_samples)
    
    analysis = {
        'count': len(latencies),
        'mean': np.mean(latencies),
        'median': np.median(latencies),
        'p90': np.percentile(latencies, 90),
        'p95': np.percentile(latencies, 95),
        'p99': np.percentile(latencies, 99),
        'std_dev': np.std(latencies),
        'min': np.min(latencies),
        'max': np.max(latencies),
        'outliers': []
    }
    
    # Identify outliers using IQR method
    q1 = np.percentile(latencies, 25)
    q3 = np.percentile(latencies, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers = latencies[(latencies < lower_bound) | (latencies > upper_bound)]
    analysis['outliers'] = outliers.tolist()
    analysis['outlier_percentage'] = len(outliers) / len(latencies) * 100
    
    return analysis
```

## Examples

```bash
# Profile CPU usage for 60 seconds
npm run performance-profiling:cpu -- --duration 60 --output cpu-profile.json

# Generate flame graph
npm run performance-profiling:flamegraph -- --pid $(pidof application) --output flamegraph.svg

# Analyze memory leaks
npm run performance-profiling:memory -- --application myapp --leak-check

# Trace database queries
npm run performance-profiling:database -- --database postgresql --duration 300

# Profile API endpoints
npm run performance-profiling:api -- --endpoints "/api/*" --duration 60 --output api-performance.json

# Compare performance before/after changes
npm run performance-profiling:compare -- --before baseline.json --after new-version.json --output comparison.json

# Analyze system resource usage
npm run performance-profiling:system -- --metrics cpu,memory,disk,network --duration 300

# Create performance dashboard
npm run performance-profiling:dashboard -- --metrics all --interval 1s --duration 3600

# Detect bottlenecks in microservices
npm run performance-profiling:microservices -- --services auth,payment,notification --duration 600

# Optimize configuration based on profiling
npm run performance-profiling:optimize -- --profile profile.json --output optimizations.md

# Monitor production performance
npm run performance-profiling:monitor -- --production --alert-threshold p95:200ms
```

## Output format

### Performance Profiling Report:
```
Performance Profiling Report
────────────────────────────
System: payment-processing-service
Analysis Date: 2026-02-26
Duration: 300 seconds
Profiling Tools: perf, eBPF, Application Profiler

Executive Summary:
⚠️ Performance issues detected: 3 critical, 2 warnings
✅ System resources: Within normal limits
📊 Overall performance score: 72/100

Critical Issues:
1. ❌ Database query bottleneck (Severity: Critical)
   • Query: SELECT * FROM transactions WHERE user_id = ?
   • Average latency: 450ms (p95: 1200ms)
   • Frequency: 1200 executions/minute
   • Root cause: Missing index on user_id column
   • Impact: 40% of API latency
   • Recommendation: Add index on transactions.user_id

2. ❌ Memory leak in cache service (Severity: Critical)
   • Service: redis-cache-service
   • Memory growth: 2MB/minute
   • Total leaked: 120MB over 1 hour
   • Pattern: Cache entries not expired properly
   • Recommendation: Implement TTL and LRU eviction

3. ❌ CPU contention in payment processor (Severity: Critical)
   • Function: processPayment() in payment-service
   • CPU usage: 85% during peak
   • Bottleneck: Cryptographic operations
   • Recommendation: Implement caching or hardware acceleration

Warnings:
1. ⚠️ API endpoint latency degradation (Severity: Warning)
   • Endpoint: POST /api/v1/payments
   • p95 latency increase: 150ms → 320ms (+113%)
   • Timeframe: Last 7 days
   • Recommendation: Profile endpoint and optimize

2. ⚠️ Garbage collection pauses (Severity: Warning)
   • Application: notification-service (Java)
   • GC pauses: 45ms average, 120ms max
   • Frequency: Every 30 seconds
   • Recommendation: Tune JVM garbage collector

System Resource Analysis:
┌────────────────────┬────────────┬────────────┬────────────┐
│ Resource           │ Usage      │ Threshold │ Status     │
├────────────────────┼────────────┼────────────┼────────────┤
│ CPU                │ 65%        │ 80%       ✅ Normal     │
│ Memory             │ 72%        │ 85%       ✅ Normal     │
│ Disk I/O           │ 45%        │ 70%       ✅ Normal     │
│ Network            │ 38%        │ 60%       ✅ Normal     │
│ Database Connections│ 85%       │ 90%       ⚠️ Warning    │
└────────────────────┴────────────┴────────────┴────────────┘

Application Performance:
• API Response Times:
  - p50: 85ms ✅
  - p95: 320ms ⚠️
  - p99: 1200ms ❌
  - Success Rate: 99.8% ✅

• Database Performance:
  - Query Cache Hit Rate: 65% ⚠️
  - Average Query Time: 85ms ✅
  - Slow Queries (>100ms): 12% ⚠️
  - Connection Pool Usage: 85% ⚠️

• Cache Performance:
  - Redis Hit Rate: 92% ✅
  - Cache Latency: 3ms ✅
  - Memory Usage: 78% ⚠️
  - Eviction Rate: 5% ✅

Flame Graph Analysis:
• Hot Functions:
  1. processPayment() - 35% CPU time
  2. validateTransaction() - 22% CPU time
  3. updateDatabase() - 18% CPU time
  4. sendNotification() - 8% CPU time
  5. logActivity() - 5% CPU time

• Optimization Opportunities:
  1. Cache validation results (potential 15% improvement)
  2. Batch database updates (potential 10% improvement)
  3. Async notifications (potential 8% improvement)

Memory Analysis:
• Heap Usage: 2.4GB
• Stack Usage: 320MB
• Native Memory: 450MB
• Garbage Collection:
  - Young GC: 45ms every 30s
  - Full GC: 120ms every 5min
  - Throughput: 98.5%

I/O Analysis:
• Disk Read: 45MB/s (average)
• Disk Write: 28MB/s (average)
• File Descriptors: 1250/4096 (31%)
• Network Throughput:
  - Inbound: 85Mbps
  - Outbound: 120Mbps
  - Connections: 850 active

Bottleneck Timeline:
┌─────────────────────────────────────────────────────────────┐
│ Bottleneck Timeline (Last 60 minutes)                       │
│                                                             │
│ 00:00 ┼───────┬──────────────┬─────────────┬────────────── │
│       │ CPU   │ Database     │ Memory      │ Network       │
│ 15:00 ┼───────┼──────────────┼─────────────┼────────────── │
│       │ ███   │ █████████    │ ███         │ ██            │
│ 30:00 ┼───────┼──────────────┼─────────────┼────────────── │
│       │ █████ │ ████████████ │ █████       │ ███           │
│ 45:00 ┼───────┼──────────────┼─────────────┼────────────── │
│       │ ██████│ █████████████│ ███████     │ ████          │
│ 60:00 ┼───────┴──────────────┴─────────────┴────────────── │
│      0%                   50%                   100%       │
└─────────────────────────────────────────────────────────────┘

Optimization Recommendations:
1. Immediate (High Impact):
   • Add database index on transactions.user_id
   • Implement cache TTL for redis-cache-service
   • Optimize processPayment() cryptographic operations

2. Short-term (Medium Impact):
   • Implement connection pooling for database
   • Add query caching for frequent queries
   • Batch database writes where possible

3. Long-term (Architectural):
   • Implement read replicas for database
   • Add CDN for static assets
   • Implement circuit breakers for external services

Performance Metrics Baseline:
• CPU Usage: < 70% target
• Memory Usage: < 80% target
• API p95 Latency: < 200ms target
• Database Query Time: < 100ms target
• Cache Hit Rate: > 90% target

Monitoring Configuration:
• Alert on: p95 latency > 200ms
• Alert on: CPU usage > 80% for 5 minutes
• Alert on: Memory usage > 85%
• Alert on: Error rate > 1%
• Dashboard: Real-time performance metrics

Next Steps:
1. Implement database index (estimate: 2 hours)
2. Fix memory leak in cache service (estimate: 4 hours)
3. Optimize payment processor CPU usage (estimate: 8 hours)
4. Deploy optimizations with feature flags
5. Monitor performance for 24 hours
6. Schedule performance regression tests
```

### JSON Output Format:
```json
{
  "analysis": {
    "system": "payment-processing-service",
    "analysis_date": "2026-02-26",
    "duration_seconds": 300,
    "profiling_tools": ["perf", "ebpf", "application_profiler"],
    "overall_score": 72
  },
  "critical_issues": [
    {
      "id": "issue-db-001",
      "description": "Database query bottleneck",
      "severity": "critical",
      "component": "database",
      "metric": "query_latency",
      "average_value": 450,
      "p95_value": 1200,
      "unit": "ms",
      "frequency": "1200 executions/minute",
      "root_cause": "Missing index on user_id column",
      "impact": "40% of API latency",
      "recommendation": "Add index on transactions.user_id",
      "estimated_effort_hours": 2,
      "priority": "high"
    },
    {
      "id": "issue-memory-001",
      "description": "Memory leak in cache service",
      "severity": "critical",
      "component": "cache",
      "metric": "memory_growth",
      "average_value": 2,
      "unit": "MB/minute",
      "total_leaked": 120,
      "total_leaked_unit": "MB",
      "timeframe": "1 hour",
      "pattern": "Cache entries not expired properly",
      "recommendation": "Implement TTL and LRU eviction",
      "estimated_effort_hours": 4,
      "priority": "high"
    }
  ],
  "system_resources": {
    "cpu": {
      "usage_percentage": 65,
      "threshold": 80,
      "status": "normal",
      "breakdown": {
        "user": 45,
        "system": 20,
        "iowait": 8,
        "steal": 2
      }
    },
    "memory": {
      "usage_percentage": 72,
      "threshold": 85,
      "status": "normal",
      "breakdown": {
        "heap": 2400,
        "stack": 320,
        "native": 450,
        "cached": 1200
      }
    },
    "disk_io": {
      "usage_percentage": 45,
      "threshold": 70,
      "status": "normal",
      "read_mbps": 45,
      "write_mbps": 28
    },
    "network": {
      "usage_percentage": 38,
      "threshold": 60,
      "status": "normal",
      "inbound_mbps": 85,
      "outbound_mbps": 120,
      "connections": 850
    }
  },
  "application_performance": {
    "api_response_times": {
      "p50_ms": 85,
      "p95_ms": 320,
      "p99_ms": 1200,
      "success_rate": 99.8
    },
    "database_performance": {
      "query_cache_hit_rate": 65,
      "average_query_time_ms": 85,
      "slow_queries_percentage": 12,
      "connection_pool_usage": 85
    },
    "cache_performance": {
      "hit_rate": 92,
      "latency_ms": 3,
      "memory_usage_percentage": 78,
      "eviction_rate": 5
    }
  },
  "flame_graph_analysis": {
    "hot_functions": [
      {
        "function": "processPayment",
        "cpu_percentage": 35,
        "optimization_opportunity": "Cache validation results"
      },
      {
        "function": "validateTransaction",
        "cpu_percentage": 22,
        "optimization_opportunity": "Batch validation"
      }
    ],
    "optimization_opportunities": [
      {
        "description": "Cache validation results",
        "estimated_improvement": 15,
        "effort_hours": 8
      },
      {
        "description": "Batch database updates",
        "estimated_improvement": 10,
        "effort_hours": 6
      }
    ]
  },
  "optimization_recommendations": {
    "immediate": [
      "Add database index on transactions.user_id",
      "Implement cache TTL for redis-cache-service",
      "Optimize processPayment() cryptographic operations"
    ],
    "short_term": [
      "Implement connection pooling for database",
      "Add query caching for frequent queries",
      "Batch database writes where possible"
    ],
    "long_term": [
      "Implement read replicas for database",
      "Add CDN for static assets",
      "Implement circuit breakers for external services"
    ]
  },
  "performance_baseline": {
    "cpu_usage_target": 70,
    "memory_usage_target": 80,
    "api_p95_latency_target": 200,
    "database_query_time_target": 100,
    "cache_hit_rate_target": 90
  },
  "next_steps": [
    {
      "action": "Implement database index",
      "estimate_hours": 2,
      "priority": "high"
    },
    {
      "action": "Fix memory leak in cache service",
      "estimate_hours": 4,
      "priority": "high"
    },
    {
      "action": "Optimize payment processor CPU usage",
      "estimate_hours": 8,
      "priority": "medium"
    }
  ]
}
```

### Performance Dashboard:
```
Performance Dashboard
────────────────────
Status: ACTIVE
Last Update: 2026-02-26 19:45:00
Update Interval: 1 second

Real-time Metrics:
┌────────────────────┬────────────┬────────────┬────────────┐
│ Metric             │ Current    │ 1min Avg   │ Trend      │
├────────────────────┼────────────┼────────────┼────────────┤
│ CPU Usage          │ 65%        │ 62%        │ ↗️ Rising   │
│ Memory Usage       │ 72%        │ 71%        │ → Stable   │
│ API Latency (p95)  │ 320ms      │ 310ms      ↗️ Rising     │
│ Database Latency   │ 85ms       │ 82ms       → Stable     │
│ Cache Hit Rate     │ 92%        │ 91%        ↘️ Falling    │
│ Error Rate         │ 0.2%       │ 0.3%       ↘️ Falling    │
└────────────────────┴────────────┴────────────┴────────────┘

Alerts:
• ⚠️  API p95 latency above threshold (200ms): 320ms
• ✅  CPU usage within limits
• ✅  Memory usage within limits
• ⚠️  Database connections approaching limit (85%)

Hotspots:
1. processPayment(): 35% CPU (🔥 Hot)
2. validateTransaction(): 22% CPU (⚠️ Warm)
3. updateDatabase(): 18% CPU (⚠️ Warm)

Resource Utilization Trend:
CPU:    ████████████████████████████████████░░░░ 65%
Memory: ██████████████████████████████████████░░ 72%
Disk:   █████████████████████░░░░░░░░░░░░░░░░░░░ 45%
Network:████████████████░░░░░░░░░░░░░░░░░░░░░░░░ 38%

Recent Events:
• 19:40: Database query slowdown detected
• 19:35: Cache miss rate increased by 15%
• 19:30: API latency spike (p95: 450ms)
• 19:25: Memory usage increased by 2%

Recommendations:
1. Add index on transactions.user_id (pending)
2. Implement cache TTL (in progress)
3. Optimize payment processor (planned)

Performance Score: 72/100
Status: Needs Improvement
```

## Notes

- **Profile in production-like environments** for accurate results
- **Use appropriate sampling rates** to balance overhead and accuracy
- **Compare against baselines** to identify regressions
- **Monitor profiling overhead** to avoid affecting production performance
- **Use flame graphs** for visual bottleneck identification
- **Combine multiple tools** for comprehensive analysis
- **Profile representative workloads** that match production usage
- **Consider security implications** of profiling in production
- **Document profiling methodology** for reproducibility
- **Automate performance regression testing** in CI/CD pipelines