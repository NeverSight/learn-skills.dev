---
name: jq
description: JSON processing, parsing, and manipulation. STRONGLY PREFERRED for all JSON formatting, filtering, transformations, and analysis. Use instead of Python/Node.js scripts for JSON operations.
---

# jq - JSON Processing

**IMPORTANT**: `jq` is the **STRONGLY PREFERRED** tool for ALL JSON formatting, parsing, manipulation, and analysis tasks. Use jq instead of Python/Node.js scripts, grep, awk, or other text processing tools when working with JSON data.

## Core Philosophy

- **Always use jq for JSON**: If the data is JSON or can be converted to JSON, use jq
- **Streaming-friendly**: jq processes JSON as a stream, making it memory-efficient for large files
- **Composable**: jq filters can be chained with pipes, just like shell commands
- **Pure and functional**: jq transformations are predictable and side-effect-free

## Basic Usage Patterns

### Pretty-Printing and Formatting

```bash
# Pretty-print JSON (most common use case)
cat file.json | jq '.'
jq '.' file.json

# Compact output (remove whitespace)
jq -c '.' file.json

# Sort keys alphabetically
jq -S '.' file.json

# Raw output (no quotes for strings)
jq -r '.field' file.json

# Null input (construct JSON from scratch)
jq -n '{name: "value", count: 42}'
```

### Selecting and Filtering

```bash
# Select a single field
jq '.field' file.json

# Select nested field
jq '.user.email' file.json

# Select array element by index
jq '.[0]' array.json
jq '.[2:5]' array.json  # Array slice

# Select multiple fields (create new object)
jq '{name: .name, email: .email}' file.json

# Filter array elements
jq '.[] | select(.age > 21)' users.json

# Filter with multiple conditions
jq '.[] | select(.active == true and .role == "admin")' users.json

# Filter and select fields
jq '.[] | select(.price < 100) | {name, price}' products.json
```

### Array Operations

```bash
# Map over array (transform each element)
jq 'map(.name)' users.json
jq '[.[] | .email]' users.json  # Alternative syntax

# Filter then map
jq 'map(select(.active)) | map(.name)' users.json

# Get array length
jq 'length' array.json
jq '.items | length' file.json

# Sort array
jq 'sort' numbers.json
jq 'sort_by(.created_at)' items.json

# Reverse array
jq 'reverse' array.json

# Unique values
jq 'unique' array.json
jq 'unique_by(.category)' items.json

# Group by field
jq 'group_by(.category)' items.json

# Flatten nested arrays
jq 'flatten' nested.json
jq 'flatten(2)' deeply_nested.json  # Flatten 2 levels
```

### Aggregations and Statistics

```bash
# Sum values
jq 'map(.price) | add' items.json
jq '[.[] | .count] | add' data.json

# Average
jq 'map(.score) | add / length' scores.json

# Min/max
jq 'map(.price) | min' products.json
jq 'map(.price) | max' products.json
jq 'min_by(.created_at)' items.json
jq 'max_by(.score)' results.json

# Count occurrences
jq 'group_by(.status) | map({status: .[0].status, count: length})' items.json
```

### Transforming Data

```bash
# Add field
jq '. + {new_field: "value"}' file.json

# Update field
jq '.price = .price * 1.1' product.json
jq '.updated_at = now' record.json

# Rename field
jq '{name: .old_name, other: .other}' file.json

# Delete field
jq 'del(.sensitive_data)' file.json

# Conditional updates
jq 'if .price > 100 then .category = "premium" else . end' product.json

# Map with transformation
jq 'map(. + {full_name: "\(.first_name) \(.last_name)"})' users.json
```

### Combining and Merging

```bash
# Merge objects
jq '. + {extra: "data"}' file.json
jq '. * {override: "value"}' file.json  # Recursive merge

# Combine arrays
jq '. + [1,2,3]' array.json

# Merge multiple files
jq -s '.[0] + .[1]' file1.json file2.json

# Slurp mode (combine into array)
jq -s '.' file1.json file2.json file3.json
jq -s 'map(.items) | flatten' *.json
```

### Working with Keys

```bash
# Get all keys
jq 'keys' object.json
jq 'keys_unsorted' object.json

# Check if key exists
jq 'has("field")' file.json

# Get values
jq 'values' object.json
jq '.[] | values' array.json  # Filter out nulls

# Convert object to array of key-value pairs
jq 'to_entries' object.json
jq 'to_entries | map({key: .key, value: .value})' object.json

# Convert array of pairs back to object
jq 'from_entries' pairs.json
```

### String Operations

```bash
# String interpolation
jq '"\(.first_name) \(.last_name)"' user.json

# String functions
jq '.name | ascii_downcase' file.json
jq '.email | ascii_upcase' file.json
jq '.text | ltrimstr("prefix:")' file.json
jq '.url | rtrimstr(".html")' file.json

# Split and join
jq '.tags | split(",")' file.json
jq '.words | join(" ")' file.json

# Regular expressions
jq '.email | test("@example\\.com$")' user.json
jq '.text | match("\\b\\w+@\\w+\\.\\w+\\b")' content.json
jq '.name | sub("old"; "new")' file.json
jq '.text | gsub("\\s+"; " ")' file.json  # Replace all
```

### Conditional Logic

```bash
# Simple if-then-else
jq 'if .age >= 18 then "adult" else "minor" end' user.json

# Multiple conditions
jq 'if .score > 90 then "A" elif .score > 80 then "B" else "C" end' result.json

# Alternative operator (handle null/false)
jq '.optional_field // "default"' file.json

# Try-catch (handle errors gracefully)
jq 'try .field.nested catch "not found"' file.json
```

### Type Conversions

```bash
# Convert to string
jq 'tostring' number.json

# Convert to number
jq 'tonumber' string.json

# Type checking
jq 'type' value.json
jq '.[] | select(type == "number")' mixed.json

# Array/object detection
jq 'if type == "array" then length else 1 end' value.json
```

### Output Formatting

```bash
# Tab-separated values
jq -r '.[] | [.name, .email, .age] | @tsv' users.json

# CSV output
jq -r '.[] | [.name, .email, .age] | @csv' users.json

# URL encoding
jq -r '@uri' string.json

# Base64 encoding/decoding
jq -r '@base64' string.json
jq -r '@base64d' encoded.json

# HTML encoding
jq -r '@html' string.json

# Shell escaping
jq -r '@sh' command.json
```

### Advanced Patterns

```bash
# Recursive descent (search all levels)
jq '.. | .id? | select(. != null)' nested.json

# Walk (apply transformation recursively)
jq 'walk(if type == "string" then ascii_downcase else . end)' file.json

# Path queries
jq 'path(.items[].name)' file.json
jq 'getpath(["items", 0, "name"])' file.json

# Limit output
jq 'limit(5; .[] | select(.active))' items.json

# Until condition
jq 'until(. > 100; . * 2)' number.json

# Reduce (fold)
jq 'reduce .[] as $item (0; . + $item.count)' items.json
jq 'reduce .[] as $item ({}; . + {($item.key): $item.value})' pairs.json
```

### Working with API Responses

```bash
# Pretty-print API response
curl -s api.example.com/data | jq '.'

# Extract specific fields from API
curl -s api.example.com/users | jq '.[] | {id, name, email}'

# Filter and transform
curl -s api.example.com/items | jq 'map(select(.active)) | sort_by(.created_at) | reverse | .[0:10]'

# Pagination handling
for page in {1..5}; do
  curl -s "api.example.com/items?page=$page" | jq '.items[]'
done | jq -s '.'

# Error handling
curl -s api.example.com/data | jq 'if .error then .error.message else .data end'
```

### Log Analysis

```bash
# Parse JSON logs
cat app.log | jq -R 'fromjson? | select(.level == "error")'

# Group errors by type
cat app.log | jq -R 'fromjson? | select(.level == "error")' | jq -s 'group_by(.error_type) | map({type: .[0].error_type, count: length})'

# Time-based filtering
cat app.log | jq -R 'fromjson? | select(.timestamp > "2024-01-01")'

# Extract stack traces
cat app.log | jq -R 'fromjson? | select(.stack_trace) | .stack_trace'
```

### Multi-File Processing

```bash
# Merge multiple JSON files
jq -s 'add' file1.json file2.json file3.json

# Process each file separately, collect results
jq -s 'map(.)' *.json

# Cross-file analysis
jq -s 'map(.items) | flatten | group_by(.category)' *.json

# Join files (like SQL join)
jq -s '.[0].users as $users | .[1].orders | map(. + {user: ($users[] | select(.id == .user_id))})' users.json orders.json
```

### Performance Optimization

```bash
# Streaming mode for large files (don't load entire file)
jq --stream 'select(length == 2)' huge.json

# Process line-by-line for NDJSON (newline-delimited JSON)
cat data.ndjson | jq -c '.'

# Use compact output to reduce size
jq -c '.' file.json > compressed.json

# Limit memory by processing incrementally
cat stream.json | jq -c 'select(.important)' >> filtered.json
```

### Debugging

```bash
# Debug mode (show intermediate values)
jq --debug '.field' file.json

# Print to stderr while continuing
jq 'debug | .field' file.json

# Add debugging output
jq '. as $orig | .field | debug | $orig' file.json

# Validate JSON
jq empty file.json  # No output = valid JSON

# Check for null fields
jq 'paths(. == null)' file.json
```

## Common Patterns for Claude Code Tasks

### Extract Configuration Values

```bash
# Get specific config value
jq -r '.database.host' config.json

# Get all environment variables
jq -r '.env | to_entries | .[] | "\(.key)=\(.value)"' config.json
```

### Process API Responses

```bash
# Extract IDs from response
gh api /repos/owner/repo/issues | jq '.[].number'

# Format for display
gh api /repos/owner/repo/pulls | jq -r '.[] | "\(.number): \(.title)"'
```

### Transform Test Results

```bash
# Parse test output
cat test-results.json | jq '{total: .stats.tests, passed: .stats.passes, failed: .stats.failures}'

# Find failed tests
cat test-results.json | jq '.tests[] | select(.state == "failed") | .title'
```

### Modify Package Files

```bash
# Update package.json version
jq '.version = "2.0.0"' package.json > package.json.tmp && mv package.json.tmp package.json

# Add dependency
jq '.dependencies["new-package"] = "^1.0.0"' package.json > package.json.tmp && mv package.json.tmp package.json

# Remove dev dependency
jq 'del(.devDependencies["old-package"])' package.json > package.json.tmp && mv package.json.tmp package.json
```

## When NOT to Use jq

- **Binary data**: jq is for text-based JSON only
- **Very simple extraction**: For trivial field access where grep would suffice
- **Modifying files in place**: jq doesn't support in-place editing (use temp files)
- **Non-JSON data**: Use appropriate tools (xsv for CSV, yq for YAML, etc.)

## Error Messages and Troubleshooting

### Common Errors

```bash
# "parse error: Invalid numeric literal"
# → JSON has invalid syntax, validate with: jq empty file.json

# "jq: error: Cannot index string with string"
# → Trying to access field on non-object, check types first

# "jq: error: null cannot be parsed as JSON"
# → Input is null or empty, use: jq -R 'fromjson?'

# "Cannot iterate over null"
# → Field doesn't exist, use: jq '.field // []'
```

### Validation

```bash
# Validate JSON syntax
jq empty file.json && echo "Valid JSON" || echo "Invalid JSON"

# Pretty-print to find errors
jq '.' file.json
```

## Performance Considerations

1. **Use `-c` for compact output** when piping to other commands
2. **Stream large files** with `--stream` or process line-by-line for NDJSON
3. **Filter early** to reduce data size before complex transformations
4. **Avoid unnecessary array creation** - use streaming operations when possible
5. **Use built-in functions** like `map`, `select`, `group_by` instead of manual loops

## Integration with Other Tools

```bash
# With curl
curl -s api.example.com/data | jq '.results[]'

# With grep (for NDJSON)
cat logs.ndjson | grep "error" | jq '.'

# With awk
cat data.json | jq -r '.[] | @tsv' | awk -F'\t' '{print $1, $3}'

# With xargs
jq -r '.files[]' list.json | xargs -I {} cp {} dest/

# With parallel processing
cat items.json | jq -c '.[]' | parallel -j4 'echo {} | jq ".id"'
```

## Resources

- Official manual: https://stedolan.github.io/jq/manual/
- jq play (online tester): https://jqplay.org/
- Cookbook: https://github.com/stedolan/jq/wiki/Cookbook
