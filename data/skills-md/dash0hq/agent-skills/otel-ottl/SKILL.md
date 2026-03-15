---
name: otel-ottl
description: OpenTelemetry Transformation Language (OTTL) expert. Use when writing or debugging OTTL expressions for any OpenTelemetry Collector component that supports OTTL (processors, connectors, receivers, exporters). Triggers on tasks involving telemetry transformation, filtering, attribute manipulation, data redaction, sampling policies, routing, or Collector configuration. Covers syntax, contexts, functions, error handling, and performance.
metadata:
  author: dash0
  version: '1.0.0'
---

# OpenTelemetry Transformation Language (OTTL)

Use OTTL to transform, filter, and manipulate telemetry data inside the OpenTelemetry Collector — without changing application code.

## Components that use OTTL

OTTL is not limited to the transform and filter processors.
The following Collector components accept OTTL expressions in their configuration.

### Processors

| Component | Use case |
|-----------|----------|
| [transform](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/transformprocessor) | Modify, enrich, or redact telemetry (set attributes, rename fields, truncate values) |
| [filter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filterprocessor) | Drop telemetry entirely (discard metrics by name, drop spans by status, remove noisy logs) |
| [attributes](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor) | Insert, update, delete, or hash resource and record attributes |
| [span](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/spanprocessor) | Rename spans and set span status based on attribute values |
| [tailsampling](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor) | Sample traces based on OTTL conditions (e.g., keep error traces, drop health checks) |
| [cumulativetodelta](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/cumulativetodeltaprocessor) | Convert cumulative metrics to delta temporality with OTTL-based metric selection |
| [logdedup](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/logdedupprocessor) | Deduplicate log records using OTTL conditions |
| [lookup](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/lookupprocessor) | Enrich telemetry by looking up values from external tables using OTTL expressions |

### Connectors

| Component | Use case |
|-----------|----------|
| [routing](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) | Route telemetry to different pipelines based on OTTL conditions |
| [count](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/countconnector) | Count spans, metrics, or logs matching OTTL conditions and emit as metrics |
| [sum](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/sumconnector) | Sum numeric values from telemetry matching OTTL conditions and emit as metrics |
| [signaltometrics](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/signaltometricsconnector) | Generate metrics from spans or logs using OTTL expressions for attribute extraction |
### Receivers

| Component | Use case |
|-----------|----------|
| [hostmetrics](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver) | Filter host metrics at collection time using OTTL conditions |

## OTTL syntax

### Path expressions

Navigate telemetry data using dot notation:

```
span.name
span.attributes["http.method"]
resource.attributes["service.name"]
```

**Contexts** (first path segment) map to OpenTelemetry signal structures:
- `resource` - Resource-level attributes
- `scope` - Instrumentation scope
- `span` - Span data (traces)
- `spanevent` - Span events
- `metric` - Metric metadata
- `datapoint` - Metric data points
- `log` - Log records

### Enumerations

Several fields accept int64 values exposed as global constants:

```
span.status.code == STATUS_CODE_ERROR
span.kind == SPAN_KIND_SERVER
```

### Operators

| Category | Operators |
|----------|-----------|
| Assignment | `=` |
| Comparison | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| Logical | `and`, `or`, `not` |

### Functions

**Converters** (uppercase, pure functions that return values):

```
ToUpperCase(span.attributes["http.request.method"])
Substring(log.body.string, 0, 1024)
Concat(["prefix", span.attributes["request.id"]], "-")
IsMatch(metric.name, "^k8s\\..*$")
```

**Editors** (lowercase, functions with side-effects that modify data):

```
set(span.attributes["region"], "us-east-1")
delete_key(resource.attributes, "internal.key")
limit(log.attributes, 10, [])
```

### Conditional statements

The `where` clause applies transformations conditionally:

```
span.attributes["db.statement"] = "REDACTED" where resource.attributes["service.name"] == "accounting"
```

### Nil checks

OTTL uses `nil` for absence checking (not `null`):

```
resource.attributes["service.name"] != nil
```

## Common patterns

### Set attributes

```
set(resource.attributes["k8s.cluster.name"], "prod-aws-us-west-2")
```

### Redact sensitive data

```
set(span.attributes["http.request.header.authorization"], "REDACTED") where span.attributes["http.request.header.authorization"] != nil
```

### Drop telemetry by pattern

In a filter processor, matching expressions cause data to be dropped:

```
IsMatch(metric.name, "^k8s\\.replicaset\\..*$")
```

### Drop stale data

```
time_unix_nano < UnixNano(Now()) - 21600000000000
```

### Backfill missing timestamps

```yaml
processors:
  transform:
    log_statements:
      - context: log
        statements:
          - set(log.observed_time, Now()) where log.observed_time_unix_nano == 0
          - set(log.time, log.observed_time) where log.time_unix_nano == 0
```

### Filter processor example

```yaml
processors:
  filter:
    metrics:
      datapoint:
        - 'IsMatch(ConvertCase(String(metric.name), "lower"), "^k8s\\.replicaset\\.")'

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [filter, batch]
      exporters: [debug]
```

### Transform processor example

```yaml
processors:
  transform:
    trace_statements:
      - context: span
        statements:
          - set(span.status.code, STATUS_CODE_ERROR) where span.attributes["http.response.status_code"] >= 500
          - set(span.attributes["env"], "production") where resource.attributes["deployment.environment"] == "prod"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [transform, batch]
      exporters: [debug]
```

### Defensive nil checks

Always check for `nil` before operating on optional attributes:

```
resource.attributes["service.namespace"] != nil
and
IsMatch(ConvertCase(String(resource.attributes["service.namespace"]), "lower"), "^platform.*$")
```

## Error handling

### Compilation errors

Occur during processor initialization and prevent Collector startup:
- Invalid syntax (missing quotes)
- Unknown functions
- Invalid path expressions
- Type mismatches

### Runtime errors

Occur during telemetry processing:
- Accessing non-existent attributes
- Type conversion failures
- Function execution errors

### Error mode configuration

Always set `error_mode` explicitly.
The default (`propagate`) stops processing the current item on any error, which can silently drop telemetry in production.

| Mode | Behavior | When to use |
|------|----------|-------------|
| `propagate` (default) | Stops processing current item | Development and strict environments where you want to catch every error |
| `ignore` | Logs error, continues processing | **Production** — set this unless you have a specific reason not to |
| `silent` | Ignores errors without logging | High-volume pipelines with known-safe transforms where error logs are noise |

```yaml
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: span
        statements:
          - set(span.attributes["parsed"], ParseJSON(span.attributes["json_body"]))
```

## Performance

OTTL statements compile once at startup and execute as optimized function chains at runtime.
There is no need to optimize for compilation speed — focus on reducing the number of statements that evaluate per telemetry item.
Use `where` clauses to skip items early rather than applying unconditional transforms.

## Function reference

### Editors

Editors modify telemetry data in-place. They are lowercase.

| Function | Signature | Description |
|----------|-----------|-------------|
| `append` | `append(target, Optional[value], Optional[values])` | Appends single or multiple values to a target field, converting scalars to arrays if needed |
| `delete_key` | `delete_key(target, key)` | Removes a key from a map |
| `delete_matching_keys` | `delete_matching_keys(target, pattern)` | Removes all keys matching a regex pattern |
| `flatten` | `flatten(target, Optional[prefix], Optional[depth])` | Flattens nested maps to the root level |
| `keep_keys` | `keep_keys(target, keys[])` | Removes all keys NOT in the supplied list |
| `keep_matching_keys` | `keep_matching_keys(target, pattern)` | Keeps only keys matching a regex pattern |
| `limit` | `limit(target, limit, priority_keys[])` | Reduces map size to not exceed limit, preserving priority keys |
| `merge_maps` | `merge_maps(target, source, strategy)` | Merges source into target (strategy: `insert`, `update`, `upsert`) |
| `replace_all_matches` | `replace_all_matches(target, pattern, replacement)` | Replaces matching string values using glob patterns |
| `replace_all_patterns` | `replace_all_patterns(target, mode, regex, replacement)` | Replaces segments matching regex (mode: `key` or `value`) |
| `replace_match` | `replace_match(target, pattern, replacement)` | Replaces entire string if it matches a glob pattern |
| `replace_pattern` | `replace_pattern(target, regex, replacement)` | Replaces string sections matching a regex |
| `set` | `set(target, value)` | Sets a telemetry field to a value |
| `truncate_all` | `truncate_all(target, limit)` | Truncates all string values in a map to a max length |

### Converters: type checking

| Function | Signature | Description |
|----------|-----------|-------------|
| `IsBool` | `IsBool(value)` | Returns true if value is boolean |
| `IsDouble` | `IsDouble(value)` | Returns true if value is float64 |
| `IsInt` | `IsInt(value)` | Returns true if value is int64 |
| `IsMap` | `IsMap(value)` | Returns true if value is a map |
| `IsList` | `IsList(value)` | Returns true if value is a list |
| `IsMatch` | `IsMatch(target, pattern)` | Returns true if target matches regex pattern |
| `IsRootSpan` | `IsRootSpan()` | Returns true if span has no parent |
| `IsString` | `IsString(value)` | Returns true if value is a string |

### Converters: type conversion

| Function | Signature | Description |
|----------|-----------|-------------|
| `Bool` | `Bool(value)` | Converts value to boolean |
| `Double` | `Double(value)` | Converts value to float64 |
| `Int` | `Int(value)` | Converts value to int64 |
| `String` | `String(value)` | Converts value to string |

### Converters: string manipulation

| Function | Signature | Description |
|----------|-----------|-------------|
| `Concat` | `Concat(values[], delimiter)` | Concatenates values with a delimiter |
| `ConvertCase` | `ConvertCase(target, toCase)` | Converts to `lower`, `upper`, `snake`, or `camel` |
| `HasPrefix` | `HasPrefix(value, prefix)` | Returns true if value starts with prefix |
| `HasSuffix` | `HasSuffix(value, suffix)` | Returns true if value ends with suffix |
| `Index` | `Index(target, value)` | Returns first index of value in target, or -1 |
| `Split` | `Split(target, delimiter)` | Splits string into array by delimiter |
| `Substring` | `Substring(target, start, length)` | Extracts substring from start position |
| `ToCamelCase` | `ToCamelCase(target)` | Converts to CamelCase |
| `ToLowerCase` | `ToLowerCase(target)` | Converts to lowercase |
| `ToSnakeCase` | `ToSnakeCase(target)` | Converts to snake_case |
| `ToUpperCase` | `ToUpperCase(target)` | Converts to UPPERCASE |
| `Trim` | `Trim(target, Optional[char])` | Removes leading/trailing characters |
| `TrimPrefix` | `TrimPrefix(value, prefix)` | Removes leading prefix |
| `TrimSuffix` | `TrimSuffix(value, suffix)` | Removes trailing suffix |

### Converters: Hashing

| Function | Signature | Description |
|----------|-----------|-------------|
| `FNV` | `FNV(value)` | Returns FNV hash as int64 |
| `MD5` | `MD5(value)` | Returns MD5 hash as hex string |
| `Murmur3Hash` | `Murmur3Hash(target)` | Returns 32-bit Murmur3 hash as hex string |
| `Murmur3Hash128` | `Murmur3Hash128(target)` | Returns 128-bit Murmur3 hash as hex string |
| `SHA1` | `SHA1(value)` | Returns SHA1 hash as hex string |
| `SHA256` | `SHA256(value)` | Returns SHA256 hash as hex string |
| `SHA512` | `SHA512(value)` | Returns SHA512 hash as hex string |

### Converters: encoding and decoding

| Function | Signature | Description |
|----------|-----------|-------------|
| `Decode` | `Decode(value, encoding)` | Decodes string (base64, base64-raw, base64-url, IANA encodings) |
| `Hex` | `Hex(value)` | Returns hexadecimal representation |

### Converters: Parsing

| Function | Signature | Description |
|----------|-----------|-------------|
| `ExtractPatterns` | `ExtractPatterns(target, pattern)` | Extracts named regex capture groups into a map |
| `ExtractGrokPatterns` | `ExtractGrokPatterns(target, pattern, Optional[namedOnly], Optional[defs])` | Parses unstructured data using grok patterns |
| `ParseCSV` | `ParseCSV(target, headers, Optional[delimiter], Optional[headerDelimiter], Optional[mode])` | Parses CSV string to map |
| `ParseInt` | `ParseInt(target, base)` | Parses string as integer in given base (2-36) |
| `ParseJSON` | `ParseJSON(target)` | Parses JSON string to map or slice |
| `ParseKeyValue` | `ParseKeyValue(target, Optional[delimiter], Optional[pair_delimiter])` | Parses key-value string to map |
| `ParseSeverity` | `ParseSeverity(target, severityMapping)` | Maps log level value to severity string |
| `ParseSimplifiedXML` | `ParseSimplifiedXML(target)` | Parses XML string to map (ignores attributes) |
| `ParseXML` | `ParseXML(target)` | Parses XML string to map (preserves structure) |

### Converters: Time and Date

| Function | Signature | Description |
|----------|-----------|-------------|
| `Day` | `Day(value)` | Returns day component from time |
| `Duration` | `Duration(duration)` | Parses duration string (e.g. `"3s"`, `"333ms"`) |
| `FormatTime` | `FormatTime(time, format)` | Formats time to string using Go layout |
| `Hour` | `Hour(value)` | Returns hour component from time |
| `Hours` | `Hours(value)` | Returns duration as floating-point hours |
| `Minute` | `Minute(value)` | Returns minute component from time |
| `Minutes` | `Minutes(value)` | Returns duration as floating-point minutes |
| `Month` | `Month(value)` | Returns month component from time |
| `Nanosecond` | `Nanosecond(value)` | Returns nanosecond component from time |
| `Nanoseconds` | `Nanoseconds(value)` | Returns duration as nanosecond count |
| `Now` | `Now()` | Returns current time |
| `Second` | `Second(value)` | Returns second component from time |
| `Seconds` | `Seconds(value)` | Returns duration as floating-point seconds |
| `Time` | `Time(target, format, Optional[location], Optional[locale])` | Parses string to time |
| `TruncateTime` | `TruncateTime(time, duration)` | Truncates time to multiple of duration |
| `Unix` | `Unix(seconds, Optional[nanoseconds])` | Creates time from Unix epoch |
| `UnixMicro` | `UnixMicro(value)` | Returns time as microseconds since epoch |
| `UnixMilli` | `UnixMilli(value)` | Returns time as milliseconds since epoch |
| `UnixNano` | `UnixNano(value)` | Returns time as nanoseconds since epoch |
| `UnixSeconds` | `UnixSeconds(value)` | Returns time as seconds since epoch |
| `Weekday` | `Weekday(value)` | Returns day of week from time |
| `Year` | `Year(value)` | Returns year component from time |

### Converters: Collections

| Function | Signature | Description |
|----------|-----------|-------------|
| `ContainsValue` | `ContainsValue(target, item)` | Returns true if item exists in slice |
| `Format` | `Format(formatString, args[])` | Formats string using `fmt.Sprintf` syntax |
| `Keys` | `Keys(target)` | Returns all keys from a map |
| `Len` | `Len(target)` | Returns length of string, slice, or map |
| `SliceToMap` | `SliceToMap(target, Optional[keyPath], Optional[valuePath])` | Converts slice of objects to map |
| `Sort` | `Sort(target, Optional[order])` | Sorts array (`asc` or `desc`) |
| `ToKeyValueString` | `ToKeyValueString(target, Optional[delim], Optional[pairDelim], Optional[sort])` | Converts map to key-value string |
| `Values` | `Values(target)` | Returns all values from a map |

### Converters: IDs and Encoding

| Function | Signature | Description |
|----------|-----------|-------------|
| `ProfileID` | `ProfileID(bytes\|string)` | Creates ProfileID from 16 bytes or 32 hex chars |
| `SpanID` | `SpanID(bytes\|string)` | Creates SpanID from 8 bytes or 16 hex chars |
| `TraceID` | `TraceID(bytes\|string)` | Creates TraceID from 16 bytes or 32 hex chars |
| `UUID` | `UUID()` | Generates a new UUID |
| `UUIDv7` | `UUIDv7()` | Generates a new UUIDv7 |

### Converters: XML

| Function | Signature | Description |
|----------|-----------|-------------|
| `ConvertAttributesToElementsXML` | `ConvertAttributesToElementsXML(target, Optional[xpath])` | Converts XML attributes to child elements |
| `ConvertTextToElementsXML` | `ConvertTextToElementsXML(target, Optional[xpath], Optional[name])` | Wraps XML text content in elements |
| `GetXML` | `GetXML(target, xpath)` | Returns XML elements matching XPath |
| `InsertXML` | `InsertXML(target, xpath, value)` | Inserts XML at XPath locations |
| `RemoveXML` | `RemoveXML(target, xpath)` | Removes XML elements matching XPath |

### Converters: Miscellaneous

| Function | Signature | Description |
|----------|-----------|-------------|
| `CommunityID` | `CommunityID(srcIP, srcPort, dstIP, dstPort, Optional[proto], Optional[seed])` | Generates network flow hash |
| `IsValidLuhn` | `IsValidLuhn(value)` | Returns true if value passes Luhn check |
| `Log` | `Log(value)` | Returns natural logarithm as float64 |
| `URL` | `URL(url_string)` | Parses URL into components (scheme, host, path, etc.) |
| `UserAgent` | `UserAgent(value)` | Parses user-agent string into map (name, version, OS) |

## References

- [OTTL Guide](https://www.dash0.com/guides/opentelemetry-transformation-language-ottl)
- [OTTL Specification](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/pkg/ottl)
- [OTTL Functions Reference](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/pkg/ottl/ottlfuncs)
- [OTTL Playground](https://ottl.run)