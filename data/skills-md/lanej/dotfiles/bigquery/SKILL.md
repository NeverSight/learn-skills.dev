---
name: bigquery
description: Use bigquery CLI (instead of `bq`) for all Google BigQuery and GCP data warehouse operations including SQL query execution, data ingestion (streaming insert, bulk load, JSONL/CSV/Parquet), data extraction/export, dataset/table/view management, external tables, schema operations, query templates, cost estimation with dry-run, authentication with gcloud, data pipelines, ETL workflows, and MCP/LSP server integration for AI-assisted querying and editor support. Modern Rust-based replacement for the Python `bq` CLI with faster startup, better cost awareness, and streaming support. Handles both small-scale streaming inserts (<1000 rows) and large-scale bulk loading (>10MB files), with support for Cloud Storage integration.
---
# BigQuery CLI Skill

You are a BigQuery specialist using the `bigquery` CLI tool. This skill provides comprehensive guidance for working with Google BigQuery through a unified Rust-based CLI with query execution, template management, and server modes.

## Core Capabilities

The `bigquery` CLI provides:

1. **Authentication**: Check status and login with gcloud
2. **Query Execution**: Run SQL queries with cost awareness and confirmation prompts
3. **Dry Run**: Estimate query costs without execution
4. **Dataset Operations**: List datasets in a project
5. **Table Operations**: List, describe, insert, load, and manage external tables
6. **Template System**: Named query templates with parameter substitution
7. **MCP Server**: Semantic search via stdio or HTTP modes
8. **LSP Server**: SQL language server for editor integration

## Authentication

### Check Authentication Status

```bash
# Check if authenticated and verify required scopes
bigquery auth check

# Will show:
# - Authentication status
# - Active account
# - BigQuery scopes availability
```

### Login with gcloud

```bash
# Authenticate with gcloud including all required BigQuery scopes
bigquery auth login

# This will:
# 1. Run gcloud auth login
# 2. Ensure all necessary BigQuery scopes are granted
# 3. Verify authentication succeeded
```

**Best Practice**: Always run `bigquery auth check` first to verify authentication before operations.

## Query Operations

### Running Queries

```bash
# Basic query execution (interactive cost confirmation)
bigquery query "SELECT * FROM dataset.table LIMIT 10"

# Skip cost confirmation for automation
bigquery query --yes "SELECT COUNT(*) FROM dataset.table"

# JSON output (default)
bigquery query "SELECT * FROM dataset.table LIMIT 5"

# Text/table output
bigquery query --format text "SELECT * FROM dataset.table LIMIT 5"
```

**Cost Awareness**: The query command automatically:
1. Estimates query cost before execution
2. Displays bytes to be processed
3. Prompts for confirmation (unless `--yes` is used)
4. Prevents accidental expensive queries

### Query Output Formats

```bash
# JSON output (default, machine-readable)
bigquery query "SELECT * FROM dataset.table"
bigquery query --format json "SELECT * FROM dataset.table"

# Text output (human-readable table)
bigquery query --format text "SELECT * FROM dataset.table"
```

### Dry Run (Cost Estimation)

```bash
# Estimate cost without executing
bigquery dry-run "SELECT * FROM large_dataset.table WHERE date >= '2025-01-01'"

# Returns:
# - Bytes that would be processed
# - Estimated cost
# - No actual data
```

**Use dry-run to**:
- Estimate costs before running expensive queries
- Validate query syntax
- Check partition pruning effectiveness
- Test queries in CI/CD pipelines

## Dataset Operations

### Listing Datasets

```bash
# List datasets in current project (text format, default)
bigquery datasets list my-project

# JSON output
bigquery datasets list my-project --format json

# Example output shows:
# - Dataset ID
# - Location
# - Creation time
# - Labels (if any)
```

**Note**: Dataset reference format is `project.dataset` or just `project` to list all datasets.

## Table Operations

### Listing Tables

```bash
# List tables in a dataset (text format, first 10)
bigquery tables list my-project.my-dataset

# JSON output
bigquery tables list my-project.my-dataset --format json

# Limit results
bigquery tables list my-project.my-dataset --limit 20

# Maximum limit is 100
bigquery tables list my-project.my-dataset --limit 100
```

### Describing Table Schema

```bash
# Show table schema and metadata (text format)
bigquery tables describe my-project.my-dataset.my-table

# JSON output
bigquery tables describe my-project.my-dataset.my-table --format json

# Output includes:
# - Column names and types
# - Nullability (NULLABLE, REQUIRED, REPEATED)
# - Mode information
# - Table metadata
```

### Inserting Rows (Small Datasets)

**Best for <1000 rows**. Uses streaming insert API for immediate availability.

#### JSONL (Newline-Delimited JSON) Format

**From JSONL File:**

```bash
# Create sample JSONL file
cat > users.jsonl <<EOF
{"id": "1", "name": "Alice Johnson", "email": "alice@example.com", "age": 30}
{"id": "2", "name": "Bob Smith", "email": "bob@example.com", "age": 25}
{"id": "3", "name": "Charlie Brown", "email": "charlie@example.com", "age": 35}
EOF

# Insert from JSONL file
bigquery tables insert my-project.dataset.users \
  --data users.jsonl --format json
```

**From JSONL Stream (stdin):**

```bash
# Stream from command output
echo '{"id": "1", "name": "Alice", "email": "alice@example.com"}' | \
  bigquery tables insert my-project.dataset.users --data - --format json

# Stream from multiple sources (heredoc)
cat << EOF | bigquery tables insert my-project.dataset.users --data - --format json
{"id": "1", "name": "Alice", "email": "alice@example.com", "age": 30}
{"id": "2", "name": "Bob", "email": "bob@example.com", "age": 25}
{"id": "3", "name": "Charlie", "email": "charlie@example.com", "age": 35}
EOF

# Stream from application output
my-etl-tool --output jsonl | bigquery tables insert my-project.dataset.events --data -

# Stream from compressed file
gunzip -c logs.jsonl.gz | bigquery tables insert my-project.dataset.logs --data -

# Stream from jq transformation
cat raw_data.json | jq -c '.records[]' | \
  bigquery tables insert my-project.dataset.processed --data -
```

**JSONL Format Requirements:**
- Each line is a separate JSON object
- Empty lines are automatically skipped
- No commas between objects
- Ideal for streaming and large datasets
- Format: `{"field1":"value1","field2":"value2"}\n`

#### CSV Format

**From CSV File:**

```bash
# Create sample CSV file
cat > users.csv <<EOF
id,name,email,age
1,Alice Johnson,alice@example.com,30
2,Bob Smith,bob@example.com,25
3,"Charlie Brown, Jr.",charlie@example.com,35
EOF

# Insert from CSV file
bigquery tables insert my-project.dataset.users \
  --data users.csv --format csv
```

**From CSV Stream (stdin):**

```bash
# Stream from heredoc
cat << EOF | bigquery tables insert my-project.dataset.users --data - --format csv
id,name,email,age
1,Alice Johnson,alice@example.com,30
2,Bob Smith,bob@example.com,25
3,Charlie Brown,charlie@example.com,35
EOF

# Stream from application output
./generate_report.sh | bigquery tables insert my-project.dataset.reports --data - --format csv

# Stream from compressed CSV
gunzip -c data.csv.gz | bigquery tables insert my-project.dataset.imports --data -

# Stream from curl/API response
curl -s https://api.example.com/export.csv | \
  bigquery tables insert my-project.dataset.api_data --data - --format csv

# Transform and stream CSV
cat raw.csv | tail -n +2 | awk '{print tolower($0)}' | \
  bigquery tables insert my-project.dataset.cleaned --data - --format csv
```

**CSV Format Requirements:**
- First row must contain column headers matching BigQuery table schema
- Values are inserted as strings (BigQuery will coerce types)
- Supports quoted fields, escaped quotes, and newlines (RFC 4180 compliant)
- Headers are case-sensitive and must match table column names

#### Additional Insert Options

```bash
# Insert inline JSON (single object)
bigquery tables insert my-project.dataset.users \
  --json '{"id": "1", "name": "Alice", "email": "alice@example.com"}'

# Insert inline JSON array
bigquery tables insert my-project.dataset.users \
  --json '[{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]'

# Dry-run validation (no data inserted)
bigquery tables insert my-project.dataset.users \
  --data users.csv --format csv --dry-run

# Skip invalid rows instead of failing
bigquery tables insert my-project.dataset.users \
  --data users.csv --format csv --skip-invalid

# Ignore unknown fields in data
bigquery tables insert my-project.dataset.users \
  --data users.csv --format csv --ignore-unknown

# Combine options for production pipelines
cat production_data.jsonl | \
  bigquery tables insert my-project.dataset.production \
    --data - --format json \
    --skip-invalid \
    --ignore-unknown
```

**Insert Options:**
- `--json <JSON>`: Inline JSON data (object or array)
- `--data <PATH>`: Path to data file, or `-` for stdin
- `--format <FORMAT>`: Data format (json or csv, default: json)
- `--dry-run`: Validate without inserting
- `--skip-invalid`: Skip invalid rows instead of failing
- `--ignore-unknown`: Ignore unknown fields in data
- `--yes`: Skip confirmation prompts

### Loading Data (Large Datasets)

**Best for >10MB files or >1000 rows**. Uses BigQuery load jobs.

**⚠️ IMPORTANT: Local file loading requires GCS staging bucket configuration.**
- If you get "The specified bucket does not exist" error, use `tables insert` for datasets <1000 rows instead
- For larger datasets, upload to GCS first, then use `bigquery tables load gs://...`

```bash
# Load from Cloud Storage URI (RECOMMENDED - no bucket config needed)
bigquery tables load my-project.dataset.users \
  gs://my-bucket/data.csv --format csv

# Load from local CSV file (requires GCS staging bucket configured)
bigquery tables load my-project.dataset.users data.csv --format csv

# Load with schema auto-detection
bigquery tables load my-project.dataset.new_table data.csv \
  --format csv --autodetect

# Load with replace write disposition (truncates table first)
bigquery tables load my-project.dataset.users data.csv \
  --format csv --write-disposition replace

# Load JSON file
bigquery tables load my-project.dataset.events events.json \
  --format json

# Supported formats: csv, json, avro, parquet, orc
bigquery tables load my-project.dataset.table data.parquet \
  --format parquet

# Dry-run validation (no data loaded)
bigquery tables load my-project.dataset.users data.csv \
  --format csv --dry-run

# Allow some bad records (skip up to 100 invalid rows)
bigquery tables load my-project.dataset.users data.csv \
  --format csv --max-bad-records 100

# Ignore unknown fields
bigquery tables load my-project.dataset.users data.csv \
  --format csv --ignore-unknown

# Skip confirmation prompts (for automation/CI)
bigquery tables load my-project.dataset.users data.csv \
  --format csv --write-disposition replace --yes
```

**Load Job Features:**
- **GCS Staging Bucket Required:** Local file loading needs GCS bucket configuration
- Real-time progress tracking with exponential backoff
- Automatic cleanup of temporary files after completion
- Write modes: `append` (default) or `replace` (truncate first)
- Safety confirmations for destructive operations
- Configurable error tolerance with `--max-bad-records`

**When to Use:**
- Large datasets (>1000 rows or >10MB)
- Data already in Cloud Storage
- Bulk data migrations

**When NOT to Use:**
- Small datasets (<1000 rows) → Use `tables insert` instead (no GCS required)
- Don't have GCS staging bucket configured → Use `tables insert` or upload to GCS first

**Load Options:**
- `--format <FORMAT>`: csv, json, avro, parquet, orc (default: csv)
- `--write-disposition <DISPOSITION>`: append or replace (default: append)
- `--autodetect`: Auto-detect schema from source files
- `--dry-run`: Validate without loading
- `--max-bad-records <N>`: Maximum bad records before failing
- `--ignore-unknown`: Ignore unknown fields
- `--yes`: Skip confirmation prompts

### Extracting Data

Export table data to Cloud Storage in various formats:

```bash
# Extract table to Cloud Storage as CSV
bigquery tables extract my-project.dataset.users \
  gs://my-bucket/exports/users.csv --format csv

# Extract as JSON
bigquery tables extract my-project.dataset.events \
  gs://my-bucket/exports/events-*.json --format json

# Extract with compression
bigquery tables extract my-project.dataset.large_table \
  gs://my-bucket/exports/data-*.csv.gz --format csv --compression gzip

# Extract as Avro with Snappy compression
bigquery tables extract my-project.dataset.events \
  gs://my-bucket/exports/events-*.avro --format avro --compression snappy

# Extract as Parquet
bigquery tables extract my-project.dataset.analytics \
  gs://my-bucket/exports/analytics.parquet --format parquet

# CSV with custom delimiter and header
bigquery tables extract my-project.dataset.data \
  gs://my-bucket/data.csv \
  --format csv \
  --field-delimiter "|" \
  --print-header

# Dry-run to validate configuration
bigquery tables extract my-project.dataset.users \
  gs://my-bucket/users.csv --format csv --dry-run

# Skip confirmation prompt
bigquery tables extract my-project.dataset.large \
  gs://my-bucket/export.csv --format csv --yes
```

**Supported Formats:** CSV, JSON (newline-delimited), Avro, Parquet
**Compression:** none, gzip, snappy (Avro/Parquet only)

### External Tables

External tables reference data in Cloud Storage without copying it to BigQuery.

#### Creating External Tables

```bash
# Create CSV external table
bigquery tables create-external my-project.dataset.external_table \
  --source-uri gs://bucket/data.csv \
  --format csv \
  --schema "id:INTEGER,name:STRING,created_at:TIMESTAMP"

# Create with auto-detected schema
bigquery tables create-external my-project.dataset.external_table \
  --source-uri gs://bucket/data.csv \
  --format csv \
  --autodetect

# Multiple source URIs (comma-separated)
bigquery tables create-external my-project.dataset.external_table \
  --source-uri "gs://bucket/file1.csv,gs://bucket/file2.csv" \
  --format csv \
  --autodetect

# Multiple source URIs (multiple flags)
bigquery tables create-external my-project.dataset.external_table \
  --source-uri gs://bucket/file1.csv \
  --source-uri gs://bucket/file2.csv \
  --format csv \
  --autodetect

# CSV-specific options
bigquery tables create-external my-project.dataset.external_table \
  --source-uri gs://bucket/data.csv \
  --format csv \
  --schema "id:INTEGER,name:STRING" \
  --field-delimiter "," \
  --skip-leading-rows 1

# Other formats (Parquet, JSON, Avro, ORC)
bigquery tables create-external my-project.dataset.parquet_table \
  --source-uri gs://bucket/data.parquet \
  --format parquet \
  --autodetect

bigquery tables create-external my-project.dataset.json_table \
  --source-uri gs://bucket/data.jsonl \
  --format json \
  --autodetect
```

**External Table Options**:
- `--source-uri <URI>`: Cloud Storage URI(s) - required
- `--format <FORMAT>`: csv, json, avro, parquet, orc - required
- `--schema <SCHEMA>`: Schema definition (column:type,column:type,...)
- `--autodetect`: Auto-detect schema from source files
- `--field-delimiter <DELIMITER>`: CSV field delimiter (default: ,)
- `--skip-leading-rows <N>`: CSV header rows to skip

#### Updating External Tables

```bash
# Update source URIs
bigquery tables update-external my-project.dataset.external_table \
  --source-uri gs://bucket/new-data.csv

# Update schema
bigquery tables update-external my-project.dataset.external_table \
  --schema "id:INTEGER,name:STRING,email:STRING"

# Update CSV options
bigquery tables update-external my-project.dataset.external_table \
  --field-delimiter "|" \
  --skip-leading-rows 2

# Update multiple properties
bigquery tables update-external my-project.dataset.external_table \
  --source-uri gs://bucket/new-data.csv \
  --schema "id:INTEGER,name:STRING,updated_at:TIMESTAMP" \
  --skip-leading-rows 1
```

## Template System

Named query templates allow you to save frequently-used queries with parameter placeholders.

### Listing Templates

```bash
# List all available templates (text format)
bigquery templates list

# JSON output
bigquery templates list --format json

# Shows:
# - Template name
# - Description
# - Parameters
# - Query preview
```

### Searching Templates

```bash
# Search by name or description
bigquery templates search "customer"
bigquery templates search "daily metrics"

# JSON output
bigquery templates search "analytics" --format json
```

### Validating Templates

```bash
# Validate template for parameter consistency
bigquery templates validate my-template

# Checks:
# - Parameter definitions match query placeholders
# - Required parameters are defined
# - Parameter types are valid
```

### Running Templates

```bash
# Run template with default parameters
bigquery templates run my-template

# Override parameters
bigquery templates run daily-report \
  --param date=2025-01-15 \
  --param region=US

# Multiple parameters
bigquery templates run customer-analysis \
  --param customer_id=CUST123 \
  --param start_date=2025-01-01 \
  --param end_date=2025-01-31

# JSON output
bigquery templates run my-template --format json

# Skip cost confirmation
bigquery templates run expensive-query --yes
```

**Template Run Options**:
- `--param <KEY=VALUE>`: Parameter override (can be used multiple times)
- `--format <FORMAT>`: Output format (json or text, default: json)
- `--yes`: Skip cost confirmation prompt

### Template Workflow Example

```bash
# 1. Search for templates
bigquery templates search "revenue"

# 2. Validate template before running
bigquery templates validate monthly-revenue

# 3. Run with parameters
bigquery templates run monthly-revenue \
  --param month=2025-01 \
  --param min_amount=1000

# 4. Run in automation (skip confirmation)
bigquery templates run monthly-revenue \
  --param month=2025-01 \
  --yes \
  --format json > output.json
```

**Use templates for**:
- Standardized reporting queries
- Common analytics patterns
- Scheduled data pipelines
- Team query sharing
- Reducing query errors

## MCP Server Integration

The BigQuery MCP server provides semantic search and natural language query capabilities via Model Context Protocol.

### Starting MCP Server

**STDIO Mode** (for local clients):

```bash
# Start MCP server in stdio mode
bigquery mcp stdio

# Server will:
# - Accept MCP protocol messages on stdin
# - Send responses on stdout
# - Expose BigQuery tools to MCP clients
```

**HTTP Mode** (for network clients):

```bash
# Start HTTP MCP server on default port 8080
bigquery mcp http

# Specify custom port
bigquery mcp http --port 3000

# Server provides:
# - HTTP endpoint for MCP protocol
# - JSON-RPC over HTTP
# - Remote access to BigQuery tools
```

### MCP Server Capabilities

The MCP server exposes these tools through the Model Context Protocol:

1. **semantic_search**: Search tables using natural language
2. **execute_query**: Run SQL queries with automatic formatting
3. **get_schema**: Retrieve table schemas
4. **list_tables**: List available tables
5. **list_datasets**: List available datasets
6. **explain_query**: Get query execution plan
7. **optimize_query**: Suggest query optimizations
8. **run_template**: Execute named templates with parameters

### MCP Configuration

Configure in Claude Code or other MCP-enabled applications:

**STDIO Mode** (`.claude/mcp.json` or similar):

```json
{
  "mcpServers": {
    "bigquery": {
      "command": "bigquery",
      "args": ["mcp", "stdio"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "my-project"
      }
    }
  }
}
```

**HTTP Mode**:

```json
{
  "mcpServers": {
    "bigquery": {
      "url": "http://localhost:8080",
      "transport": "http"
    }
  }
}
```

### MCP Usage Patterns

When using BigQuery MCP through clients:

**Semantic Search**:
```
"Find all tables containing customer purchase data from the last 30 days"
→ MCP translates to appropriate SQL query
```

**Schema Discovery**:
```
"What columns are in the analytics.events table?"
→ MCP returns schema information
```

**Natural Language Queries**:
```
"Show me total revenue by region for Q1 2025"
→ MCP generates and executes SQL
```

**Template Execution**:
```
"Run the monthly revenue template for January 2025"
→ MCP executes template with parameters
```

## LSP Integration

The BigQuery LSP provides SQL language features in text editors.

### Starting LSP Server

```bash
# Start LSP server
bigquery lsp

# Server provides:
# - Language Server Protocol communication
# - SQL syntax validation
# - Schema-aware completions
# - Query formatting
# - Hover documentation
```

### LSP Features

- **SQL syntax highlighting**: Proper tokenization and highlighting
- **Schema completion**: Table and column suggestions based on project schema
- **Query validation**: Real-time syntax and semantic checks
- **Hover documentation**: Table and column info on hover
- **Go to definition**: Navigate to table definitions
- **Query formatting**: Auto-format SQL queries
- **Diagnostics**: Show errors and warnings inline

### Editor Configuration

**Neovim**:

```lua
-- In nvim/lua/bigquery-lsp.lua or init.lua
vim.api.nvim_create_autocmd("FileType", {
  pattern = { "sql", "bq", "bigquery" },
  callback = function()
    vim.lsp.start({
      name = "bigquery-lsp",
      cmd = { "bigquery", "lsp" },
      root_dir = vim.fn.getcwd(),
    })
  end,
})
```

**VS Code** (in `settings.json` or language server config):

```json
{
  "bigquery-lsp": {
    "command": "bigquery",
    "args": ["lsp"],
    "filetypes": ["sql", "bq", "bigquery"]
  }
}
```

**Helix** (in `languages.toml`):

```toml
[[language]]
name = "sql"
language-servers = ["bigquery-lsp"]

[language-server.bigquery-lsp]
command = "bigquery"
args = ["lsp"]
```

## Common Workflows

### Workflow 1: Exploratory Data Analysis

```bash
# 1. Verify authentication
bigquery auth check

# 2. List available datasets
bigquery datasets list my-project

# 3. List tables in dataset
bigquery tables list my-project.analytics

# 4. Check table schema
bigquery tables describe my-project.analytics.events

# 5. Preview data (text format for readability)
bigquery query --format text \
  "SELECT * FROM my-project.analytics.events LIMIT 10"

# 6. Get row count
bigquery query "SELECT COUNT(*) as total FROM my-project.analytics.events"

# 7. Check data distribution
bigquery query --format text "
  SELECT
    DATE(timestamp) as date,
    COUNT(*) as events
  FROM my-project.analytics.events
  GROUP BY date
  ORDER BY date DESC
  LIMIT 30
"
```

### Workflow 2: Cost-Aware Query Development

```bash
# 1. Dry run to estimate cost
bigquery dry-run "
  SELECT *
  FROM my-project.large_dataset.table
  WHERE date >= '2025-01-01'
"

# 2. If cost is acceptable, run query
bigquery query "
  SELECT *
  FROM my-project.large_dataset.table
  WHERE date >= '2025-01-01'
"

# 3. For automation, skip confirmation
bigquery query --yes "
  SELECT *
  FROM my-project.large_dataset.table
  WHERE date >= '2025-01-01'
" > results.json
```

### Workflow 3: Template-Based Reporting

```bash
# 1. Search for relevant templates
bigquery templates search "daily"

# 2. Validate template
bigquery templates validate daily-metrics

# 3. Run template with parameters
bigquery templates run daily-metrics \
  --param date=$(date +%Y-%m-%d) \
  --param region=US \
  --format json > daily-report.json

# 4. Schedule in cron or CI/CD
# 0 1 * * * bigquery templates run daily-metrics --param date=$(date +%Y-%m-%d) --yes
```

### Workflow 4: External Data Analysis

```bash
# 1. Create external table pointing to GCS
bigquery tables create-external my-project.staging.raw_logs \
  --source-uri gs://logs-bucket/2025-01-*.json \
  --format json \
  --autodetect

# 2. Query external table
bigquery query "
  SELECT
    timestamp,
    user_id,
    action
  FROM my-project.staging.raw_logs
  WHERE action = 'purchase'
  LIMIT 100
"

# 3. Update external table when new files arrive
bigquery tables update-external my-project.staging.raw_logs \
  --source-uri gs://logs-bucket/2025-02-*.json
```

### Workflow 5: Data Loading Pipeline

```bash
# 1. Load initial data
bigquery tables load my-project.dataset.events \
  gs://bucket/events-2025-01-01.csv \
  --format csv \
  --write-disposition replace

# 2. Append incremental data
bigquery tables load my-project.dataset.events \
  gs://bucket/events-2025-01-02.csv \
  --format csv \
  --write-disposition append

# 3. Verify data loaded
bigquery query "
  SELECT
    DATE(timestamp) as date,
    COUNT(*) as count
  FROM my-project.dataset.events
  GROUP BY date
  ORDER BY date
"
```

### Workflow 6: Real-Time Data Insertion

```bash
# 1. Insert single event (inline JSON)
bigquery tables insert my-project.dataset.events \
  --json '{"user_id": "U123", "event": "click", "timestamp": "2025-01-15T10:00:00Z"}'

# 2. Stream JSONL from application
my-app --output jsonl | bigquery tables insert my-project.dataset.events --data - --format json

# 3. Insert batch from JSONL file
bigquery tables insert my-project.dataset.events \
  --data events.jsonl --format json

# 4. Stream with transformation and error handling
cat raw_events.json | jq -c '.events[]' | \
  bigquery tables insert my-project.dataset.events \
    --data - --format json \
    --skip-invalid \
    --ignore-unknown
```

## Best Practices

### Query Development

1. **Always dry-run first**: Use `bigquery dry-run` to estimate costs
2. **Use templates**: Create templates for repeated queries
3. **Validate before running**: Check syntax and cost before execution
4. **Use text format for exploration**: `--format text` for human-readable tables
5. **Use JSON for automation**: `--format json` for machine processing
6. **Skip confirmations in scripts**: Use `--yes` flag for automation

### Cost Management

1. **Dry run expensive queries**: Always estimate with `bigquery dry-run`
2. **Monitor bytes processed**: Check query cost estimates before running
3. **Use partition pruning**: Filter on partitioned columns in WHERE clauses
4. **Limit result sets**: Use LIMIT for exploratory queries
5. **Use templates**: Standardize queries to avoid mistakes
6. **Leverage external tables**: Avoid copying data when querying directly from GCS

### Authentication

1. **Check auth first**: Run `bigquery auth check` before operations
2. **Use service accounts**: For automation and CI/CD
3. **Verify scopes**: Ensure all required BigQuery scopes are granted
4. **Re-authenticate when needed**: `bigquery auth login` if check fails

### Template Management

1. **Use descriptive names**: Make templates easy to find
2. **Document parameters**: Include parameter descriptions in templates
3. **Validate before use**: Run `bigquery templates validate` before execution
4. **Search before creating**: Check if similar template exists
5. **Version control templates**: Store template definitions in git

### Data Loading

1. **Choose the right method**:
   - Use `insert` for <1000 rows (streaming insert API, immediate availability)
   - Use `load` for >10MB files or >1000 rows (load jobs with GCS upload)
2. **Use JSONL for streaming**: Newline-delimited JSON is ideal for streaming pipelines
3. **Stream from stdin**: Use `--data -` to pipe data from applications or transformations
4. **Validate before loading**: Use `--dry-run` flag to test configurations
5. **Handle bad records**: Set `--max-bad-records` for messy data
6. **Choose write disposition**: `replace` for full refresh, `append` for incremental
7. **Use external tables**: For data that changes frequently in GCS (no data copying)
8. **Use appropriate formats**: CSV for simple data, JSON/JSONL for complex, Parquet/Avro for large datasets

### MCP Server

1. **Use stdio for local**: Prefer stdio mode for local MCP clients
2. **Use HTTP for remote**: Use HTTP mode for networked deployments
3. **Secure HTTP endpoints**: Put HTTP server behind authentication/firewall
4. **Monitor server logs**: Check for errors and performance issues
5. **Set appropriate port**: Choose non-conflicting port for HTTP mode

### LSP Integration

1. **Configure per-project**: Set up LSP for SQL files in your editor
2. **Use schema completion**: Leverage auto-complete for table/column names
3. **Check diagnostics**: Fix errors and warnings shown inline
4. **Format queries**: Use LSP formatting for consistent style

## Configuration

### Environment Variables

```bash
# Set default project
export GOOGLE_CLOUD_PROJECT=my-project

# Set credentials (for service accounts)
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Add to ~/.zshrc or ~/.bashrc for persistence
echo 'export GOOGLE_CLOUD_PROJECT=my-project' >> ~/.zshrc
```

### Authentication Methods

**User Credentials** (interactive):
```bash
bigquery auth login
# Opens browser for Google authentication
```

**Service Account** (automation):
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa-key.json
bigquery auth check
```

**Application Default Credentials** (gcloud):
```bash
gcloud auth application-default login
bigquery auth check
```

## Troubleshooting

### Issue: "Not authenticated" or "Permission denied"

**Solution**: Check authentication and scopes

```bash
# Check current auth status
bigquery auth check

# Re-authenticate if needed
bigquery auth login

# Verify gcloud is set to correct project
gcloud config get-value project

# Set project if needed
gcloud config set project my-project
```

### Issue: "Table not found"

**Solution**: Use fully qualified table names

```bash
# Wrong - missing project/dataset
bigquery query "SELECT * FROM table"

# Correct - fully qualified
bigquery query "SELECT * FROM my-project.my-dataset.my-table"

# Or use backticks for reserved words
bigquery query "SELECT * FROM \`my-project.my-dataset.my-table\`"
```

### Issue: "Query too expensive"

**Solution**: Check cost with dry-run and optimize

```bash
# Check estimated cost
bigquery dry-run "SELECT * FROM large_table WHERE date >= '2025-01-01'"

# Optimize with partition filters
bigquery dry-run "
  SELECT * FROM large_table
  WHERE _PARTITIONDATE = '2025-01-15'
"
```

### Issue: "Template not found"

**Solution**: Search for templates and verify name

```bash
# List all templates
bigquery templates list

# Search for template
bigquery templates search "keyword"

# Use exact template name
bigquery templates run exact-template-name
```

### Issue: "The specified bucket does not exist"

**Cause**: `bigquery tables load` with a local file requires GCS staging bucket configuration.

**Solutions**:

1. **Preferred for small datasets (<1000 rows)**: Use `tables insert` instead (no GCS required)
   ```bash
   bigquery tables insert my-project.dataset.table \
     --data /tmp/data.jsonl \
     --format json
   ```

2. **For larger datasets**: Upload to GCS first, then load
   ```bash
   gsutil cp /tmp/large-file.jsonl gs://my-bucket/
   bigquery tables load my-project.dataset.table \
     gs://my-bucket/large-file.jsonl \
     --format json
   ```

3. **Last resort**: Configure GCS staging bucket in BigQuery CLI config (requires additional setup)

### Issue: "Invalid schema"

**Solution**: Check schema format for external tables

```bash
# Schema format: column:type,column:type,...
bigquery tables create-external my-project.dataset.table \
  --source-uri gs://bucket/file.csv \
  --format csv \
  --schema "id:INTEGER,name:STRING,created_at:TIMESTAMP"

# Or use autodetect
bigquery tables create-external my-project.dataset.table \
  --source-uri gs://bucket/file.csv \
  --format csv \
  --autodetect
```

### Issue: "MCP server not responding"

**Solution**: Check server mode and connectivity

```bash
# For stdio mode, ensure client is using stdio transport
bigquery mcp stdio

# For HTTP mode, check port and firewall
bigquery mcp http --port 8080

# Test HTTP endpoint
curl http://localhost:8080
```

### Issue: "LSP not starting in editor"

**Solution**: Verify LSP configuration and binary path

```bash
# Check bigquery is in PATH
which bigquery

# Test LSP manually
bigquery lsp

# Verify editor configuration points to correct command
# Neovim: check cmd = { "bigquery", "lsp" }
# VS Code: check "command": "bigquery", "args": ["lsp"]
```

## Quick Reference

```bash
# Authentication
bigquery auth check                          # Check auth status
bigquery auth login                          # Login with gcloud

# Queries
bigquery query "SELECT ..."                  # Execute query
bigquery query --yes "SELECT ..."            # Skip confirmation
bigquery query --format text "SELECT ..."    # Table output
bigquery dry-run "SELECT ..."                # Estimate cost

# Datasets
bigquery datasets list PROJECT               # List datasets

# Tables
bigquery tables list PROJECT.DATASET                          # List tables
bigquery tables describe PROJECT.DATASET.TABLE               # Show schema
bigquery tables insert TABLE --json '{"id": 1}'              # Insert rows (inline)
bigquery tables insert TABLE --data file.jsonl --format json # Insert from JSONL
cat data.jsonl | bigquery tables insert TABLE --data -       # Stream insert
bigquery tables load TABLE file.csv                          # Load data (bulk)
bigquery tables load TABLE gs://bucket/file.csv              # Load from GCS
bigquery tables extract TABLE gs://bucket/output.csv         # Extract to GCS
bigquery tables create-external TABLE --source-uri ...       # External table
bigquery tables update-external TABLE --source-uri ...       # Update external

# Templates
bigquery templates list                              # List templates
bigquery templates search "keyword"                  # Search templates
bigquery templates validate TEMPLATE                 # Validate template
bigquery templates run TEMPLATE --param key=value    # Run template

# MCP Server
bigquery mcp stdio                   # Start MCP (stdio mode)
bigquery mcp http                    # Start MCP (HTTP mode)
bigquery mcp http --port 3000        # Custom port

# LSP Server
bigquery lsp                         # Start LSP server
```

## Integration Examples

### CI/CD Pipeline

```bash
#!/bin/bash
# daily-etl.sh

# Authenticate with service account
export GOOGLE_APPLICATION_CREDENTIALS=/secrets/sa-key.json
bigquery auth check || exit 1

# Run daily ETL template
bigquery templates run daily-etl \
  --param date=$(date +%Y-%m-%d) \
  --yes \
  --format json > /tmp/etl-result.json

# Check result
if [ $? -eq 0 ]; then
  echo "ETL completed successfully"
else
  echo "ETL failed"
  exit 1
fi
```

### Data Quality Checks

```bash
#!/bin/bash
# check-data-quality.sh

# Run data quality template
RESULT=$(bigquery templates run data-quality-check \
  --param table=my-project.dataset.table \
  --yes \
  --format json)

# Parse result and check quality metrics
INVALID_ROWS=$(echo $RESULT | jq '.invalid_rows')

if [ "$INVALID_ROWS" -gt 100 ]; then
  echo "Data quality check failed: $INVALID_ROWS invalid rows"
  exit 1
else
  echo "Data quality check passed"
fi
```

### Scheduled Reporting

```bash
#!/bin/bash
# generate-report.sh

# Generate weekly report
bigquery templates run weekly-revenue-report \
  --param week_start=$(date -d "last monday" +%Y-%m-%d) \
  --param week_end=$(date -d "next sunday" +%Y-%m-%d) \
  --yes \
  --format json > /reports/weekly-$(date +%Y-%m-%d).json

# Upload to GCS
gsutil cp /reports/weekly-*.json gs://reports-bucket/
```

## Summary

**Primary commands:**
- `bigquery auth {check,login}` - Authentication management
- `bigquery query` - Execute SQL with cost awareness
- `bigquery dry-run` - Estimate query costs
- `bigquery datasets list` - List datasets
- `bigquery tables {list,describe,insert,load,extract,create-external,update-external}` - Table operations
- `bigquery templates {list,search,validate,run}` - Named templates
- `bigquery mcp {stdio,http}` - MCP server modes
- `bigquery lsp` - LSP server

**Key features:**
- Cost-aware query execution with confirmation prompts
- Named query templates with parameter substitution
- Streaming insert API for real-time data (<1000 rows)
- Bulk load jobs for large datasets (>10MB or >1000 rows)
- JSONL streaming support with stdin (`--data -`)
- Data extraction to Cloud Storage (CSV, JSON, Avro, Parquet)
- External table support for GCS data
- MCP server with stdio and HTTP modes
- LSP integration for editor support

**Best practices:**
- Always check authentication first with `auth check`
- Use `dry-run` to estimate costs before expensive queries
- Create templates for frequently-used queries
- Use `--yes` flag for automation and CI/CD
- Use `insert` for <1000 rows, `load` for larger datasets
- Use JSONL format for streaming pipelines
- Stream from stdin with `--data -` for data transformations
- Use external tables to avoid data duplication
- Configure MCP for natural language query capabilities
- Set up LSP in your editor for SQL development

**MCP Integration:**
- Semantic search across datasets
- Natural language to SQL translation
- Schema discovery and exploration
- Template execution via MCP tools
- Available in both stdio and HTTP modes
