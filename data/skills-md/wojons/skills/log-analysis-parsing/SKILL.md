---
name: log-analysis-parsing
description: Parse, analyze, search, and extract insights from logs using various techniques including regex, parsing engines, and log analysis tools
license: MIT
compatibility: opencode
metadata:
  audience: developers, SREs, data analysts, security analysts
  category: observability
---

# Log Analysis & Parsing

Parse, analyze, search, filter, and extract insights from log data using regex patterns, parsing engines, log analysis tools, and data processing techniques to transform raw logs into actionable information.

## When to use me

Use this skill when:
- Need to extract specific information from unstructured log files
- Building log parsing pipelines for observability platforms
- Searching through large volumes of logs for specific patterns or errors
- Creating dashboards and alerts based on log content
- Analyzing log data for security incidents or performance issues
- Converting legacy text logs to structured formats
- Building custom log analysis tools or scripts
- Debugging complex issues requiring correlation across multiple log sources
- Performing forensic analysis on historical log data

## What I do

### 1. Log Parsing Techniques
- **Regex pattern matching** for extracting structured data from unstructured logs
- **Grok pattern parsing** using named capture groups and reusable patterns
- **JSON parsing** for already-structured log formats
- **Key-value pair extraction** from delimited log formats
- **Multi-line log handling** for stack traces and exception details
- **Timestamp parsing** from various date/time formats
- **Log format inference** for unknown log formats

### 2. Log Analysis Methods
- **Pattern recognition** to identify common log message types
- **Anomaly detection** for unusual log patterns or volumes
- **Trend analysis** for log volume, error rates, performance metrics
- **Correlation analysis** across multiple log sources
- **Sequence analysis** for understanding event flows
- **Statistical analysis** of log attributes and metrics
- **Machine learning approaches** for log classification and prediction

### 3. Search & Filter Operations
- **Full-text search** across log messages and fields
- **Field-specific queries** for structured log data
- **Boolean operations** (AND, OR, NOT) for complex queries
- **Time-range filtering** for temporal analysis
- **Regular expression search** for pattern matching
- **Fuzzy search** for approximate matching
- **Saved searches** and query templates for repeated analysis

### 4. Insight Extraction
- **Error rate calculation** from log patterns
- **Performance metric extraction** (latency, duration, throughput)
- **User behavior analysis** from application logs
- **Security event detection** from access and audit logs
- **Business metric derivation** from transaction logs
- **System health indicators** from infrastructure logs
- **Dependency health** from service interaction logs

### 5. Visualization & Reporting
- **Time-series charts** for log volume and error rates
- **Heat maps** for pattern frequency
- **Top-N lists** for most common errors or users
- **Distribution charts** for performance metrics
- **Correlation matrices** for related events
- **Alert dashboards** for real-time monitoring
- **Export capabilities** for external analysis tools

## Parsing Patterns

### Common Log Formats

#### Apache/Nginx Access Logs
```
127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
```

**Parsing pattern:**
```regex
^(?P<ip>\S+) \S+ (?P<user>\S+) \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\d+)
```

#### JSON Logs (Structured)
```json
{
  "timestamp": "2026-02-26T18:00:00Z",
  "level": "ERROR",
  "service": "api-service",
  "message": "Database connection failed",
  "error": {
    "code": "DB_CONN_001",
    "message": "Connection timeout"
  }
}
```

**Parsing approach:** Direct JSON parsing with field extraction

#### Key-Value Logs
```
timestamp=2026-02-26T18:00:00Z level=ERROR service=api-service message="Database connection failed" error_code=DB_CONN_001
```

**Parsing pattern:**
```regex
(\w+)=("[^"]*"|\S+)
```

#### Multi-line Stack Traces
```
ERROR 2026-02-26 18:00:00 - Database connection failed
java.sql.SQLException: Connection timeout
    at com.example.Database.connect(Database.java:123)
    at com.example.Service.process(Service.java:456)
    ...
```

**Parsing approach:** Capture first line as header, subsequent lines as stack_trace field

### Grok Patterns
Grok provides reusable named regex patterns for common log components.

**Common Grok patterns:**
- `%{TIMESTAMP_ISO8601:timestamp}`
- `%{IP:client_ip}`
- `%{WORD:http_method}`
- `%{URIPATHPARAM:request_path}`
- `%{NUMBER:response_status}`
- `%{NUMBER:response_size}`
- `%{GREEDYDATA:message}`

**Example Grok pattern for Apache logs:**
```
%{IP:client_ip} %{USER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] "%{WORD:method} %{URIPATHPARAM:request} HTTP/%{NUMBER:http_version}" %{NUMBER:response_status} %{NUMBER:bytes_sent}
```

## Analysis Techniques

### Pattern Frequency Analysis
Identify most common log messages, error types, or user actions.

**Example analysis:**
```
Top 5 Error Messages (last 24 hours):
1. "Database connection timeout" (1,234 occurrences)
2. "Invalid API key" (987 occurrences)
3. "Rate limit exceeded" (654 occurrences)
4. "File not found" (543 occurrences)
5. "Memory allocation failed" (432 occurrences)
```

### Time-Series Analysis
Track metrics over time to identify trends and anomalies.

**Metrics to track:**
- Log volume per minute/hour/day
- Error rate as percentage of total logs
- Average response time from access logs
- Peak usage periods and patterns
- Seasonal trends (daily, weekly, monthly)

### Correlation Analysis
Link related events across different log sources.

**Correlation examples:**
- Link application errors with infrastructure alerts
- Correlate user actions with performance degradation
- Connect security events across multiple systems
- Trace request flow through microservices

### Anomaly Detection
Identify unusual patterns that may indicate issues.

**Anomaly types:**
- Sudden increase in error rate
- Unusual access patterns
- Unexpected service interactions
- Abnormal resource usage patterns
- Geographic access anomalies

## Examples

```bash
# Parse Apache access logs and extract statistics
npm run log-analysis:parse -- --format apache --file access.log --output stats.json

# Search for error patterns in application logs
npm run log-analysis:search -- --pattern "ERROR.*timeout" --files "app*.log" --time-range "last-24h"

# Analyze log trends over time
npm run log-analysis:trends -- --metric "error_rate" --window "7d" --granularity "1h"

# Create parsing pipeline for custom log format
npm run log-analysis:pipeline -- --input-format "custom" --output-format "json" --mapping mapping.yaml

# Perform correlation analysis across log sources
npm run log-analysis:correlate -- --sources "app.log,nginx.log,db.log" --time-window "5m"
```

## Output format

### Parsing Configuration:
```yaml
parsing:
  format: "apache_access"
  pattern: '^(?P<ip>\S+) \S+ (?P<user>\S+) \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\d+)'
  timestamp_format: "%d/%b/%Y:%H:%M:%S %z"
  fields:
    - name: "ip"
      type: "string"
    - name: "timestamp"
      type: "datetime"
    - name: "method"
      type: "string"
    - name: "status"
      type: "integer"
    - name: "size"
      type: "integer"
  
  processing:
    - transform: "status >= 400 => error"
    - transform: "size > 1000000 => large_response"
    - enrich: "geoip(ip)"
    - enrich: "user_agent_parse(user_agent)"
  
  output:
    format: "json"
    include_fields: ["timestamp", "ip", "method", "path", "status", "size", "error"]
```

### Log Analysis Report:
```
Log Analysis Report
───────────────────
Source: payment-service logs
Period: 2026-02-25 to 2026-02-26
Total logs analyzed: 1,234,567

Parsing Summary:
✅ Successfully parsed: 1,200,123 logs (97.2%)
⚠️  Partially parsed: 23,456 logs (1.9%)
❌ Failed to parse: 10,988 logs (0.9%)

Common Patterns Identified:
1. "Payment processed" (45,678 occurrences)
2. "Database query executed" (32,456 occurrences)
3. "API call to gateway" (28,901 occurrences)
4. "Validation error" (12,345 occurrences)
5. "Cache hit/miss" (9,876 occurrences)

Error Analysis:
- Total errors: 15,678 (1.27% error rate)
- Top error: "Payment gateway timeout" (4,567 occurrences)
- Error trend: Increasing over last 24 hours (+15%)
- Peak error time: 14:00-15:00 (1,234 errors/hour)

Performance Metrics:
- Average response time: 245ms
- 95th percentile: 567ms
- 99th percentile: 1,234ms
- Slowest endpoint: /api/v1/reports (avg 890ms)

Security Insights:
- Unusual access patterns detected: 12
- Failed authentication attempts: 456
- Suspicious user agents: 23
- Geographic anomalies: 5

Recommendations:
1. Investigate increasing error rate trend
2. Optimize /api/v1/reports endpoint performance
3. Review 12 unusual access patterns
4. Consider adding more context to validation errors
5. Implement parsing for currently failed logs
```

## Notes

- **Parsing performance matters** - inefficient regex can slow down log processing
- **Handle parsing failures gracefully** - don't lose data because of parsing errors
- **Standardize log formats** across applications to simplify parsing
- **Consider log volume** - parsing millions of logs requires efficient algorithms
- **Cache parsing results** for repeated analysis of the same logs
- **Validate parsed data** - ensure extracted fields are accurate and consistent
- **Document parsing rules** - especially for custom or complex log formats
- **Test parsing with sample data** from all log sources and formats
- **Monitor parsing success rate** - alert on sudden drops in parsing success
- **Plan for log format changes** - version parsing rules and handle migration