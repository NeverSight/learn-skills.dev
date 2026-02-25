---
name: duckdb-cli
description: Query and analyze data using the DuckDB CLI. Use when the user needs to run SQL queries, analyze CSV/Parquet/JSON files, create or query databases, export data, or perform any ad-hoc data analysis from the command line. Triggers include requests to "query a file", "analyze data", "run SQL", "read a CSV/Parquet/JSON", "create a database", "export to CSV/Parquet", or any data analysis task that benefits from SQL.
---

# DuckDB CLI

DuckDB is a fast, in-process analytical database. The CLI is a single, dependency-free executable.

## Core Usage

```bash
duckdb                          # In-memory database
duckdb my.duckdb                # Persistent database
duckdb :memory: "SELECT 42"    # One-shot query
duckdb -c "SELECT 42"          # One-shot query (in-memory)
duckdb < script.sql             # Run SQL file
duckdb -f script.sql            # Run SQL file (alternative)
```

## Command Line Arguments

| Argument | Description |
|----------|-------------|
| `-c COMMAND` | Run SQL command and exit |
| `-f FILENAME` | Run script file and exit |
| `-csv` | Set output to CSV |
| `-json` | Set output to JSON |
| `-markdown` | Set output to markdown |
| `-table` | Set output to ASCII table |
| `-box` | Set output to box-drawing table |
| `-line` | Set output to one-value-per-line |
| `-list` | Set output to pipe-delimited list |
| `-readonly` | Open database read-only |
| `-header` / `-noheader` | Toggle column headers |
| `-separator SEP` | Set column separator |
| `-nullvalue TEXT` | Set NULL display text |
| `-unsigned` | Allow unsigned extensions |
| `-bail` | Stop after first error |
| `-batch` | Force batch I/O (non-interactive) |

Arguments are processed in order:

```bash
duckdb -csv -c 'SELECT 42 AS x' -json -c 'SELECT 84 AS y'
# First outputs CSV, then JSON
```

## Dot Commands

| Command | Description |
|---------|-------------|
| `.open FILE` | Close current db, open FILE |
| `.databases` | List attached databases |
| `.tables [PATTERN]` | List tables (optional LIKE pattern) |
| `.schema [PATTERN]` | Show CREATE statements |
| `.mode MODE` | Set output format |
| `.headers on/off` | Toggle column headers |
| `.timer on/off` | Toggle query timing |
| `.output FILE` | Redirect all output to FILE |
| `.output` | Revert to stdout |
| `.once FILE` | Redirect next query output only |
| `.once -x` / `.excel` | Open next result in spreadsheet app |
| `.read FILE` | Execute SQL from FILE |
| `.import FILE TABLE` | Import data from FILE into TABLE |
| `.show` | Show current settings |
| `.quit` / `.exit` | Exit CLI |

## Output Formats

Set via `.mode MODE` or CLI arguments (`-csv`, `-json`, etc.):

`duckbox` (default), `box`, `table`, `csv`, `json`, `jsonlines`, `markdown`, `latex`, `html`, `insert`, `line`, `list`, `tabs`, `column`, `trash`

## Querying Files Directly

```sql
-- CSV
SELECT * FROM 'data.csv';
SELECT * FROM read_csv('data.csv');
SELECT * FROM read_csv('data/*.csv');  -- glob

-- Parquet
SELECT * FROM 'data.parquet';
SELECT * FROM read_parquet('data.parquet');
SELECT * FROM read_parquet('s3://bucket/data.parquet');  -- remote

-- JSON
SELECT * FROM 'data.json';
SELECT * FROM read_json('data.json');

-- Multiple files
SELECT * FROM read_csv(['file1.csv', 'file2.csv']);
SELECT * FROM 'data/**/*.parquet';  -- recursive glob
```

## Exporting Data

```sql
-- To CSV
COPY (SELECT * FROM tbl) TO 'output.csv' (HEADER, DELIMITER ',');

-- To Parquet
COPY (SELECT * FROM tbl) TO 'output.parquet' (FORMAT PARQUET);

-- To JSON
COPY (SELECT * FROM tbl) TO 'output.json' (FORMAT JSON, ARRAY true);
```

Or via dot commands:

```
.mode csv
.output results.csv
SELECT * FROM tbl;
.output
```

## Piping (stdin/stdout)

```bash
# Read from stdin
cat data.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"

# Write to stdout
duckdb -c "COPY (SELECT 1 AS x) TO '/dev/stdout' WITH (FORMAT csv, HEADER)"

# Chain
cat data.csv | duckdb -c "COPY (SELECT * FROM read_csv('/dev/stdin') WHERE x > 10) TO '/dev/stdout' WITH (FORMAT csv, HEADER)" | wc -l
```

## Non-Interactive Patterns

```bash
# One-shot query
duckdb :memory: "SELECT 42 AS answer"

# Multiple statements
duckdb :memory: -c "CREATE TABLE t AS SELECT 1 AS x; SELECT * FROM t;"

# From file
duckdb my.duckdb < queries.sql

# JSON output for scripting
duckdb -json -c "SELECT * FROM 'data.csv' LIMIT 5"

# CSV output
duckdb -csv -noheader -c "SELECT col FROM 'data.csv'"
```

## Extensions

```sql
INSTALL httpfs;    -- HTTP/S3 access
LOAD httpfs;

INSTALL spatial;   -- Geospatial
INSTALL fts;       -- Full-text search
INSTALL vss;       -- Vector similarity search
INSTALL postgres;  -- PostgreSQL scanner
INSTALL sqlite;    -- SQLite scanner
INSTALL excel;     -- Excel support
```

## Text Analysis Functions

### Tier 1: Built-in Text Functions (no extension needed)

**Exact matching:**

```sql
SELECT * FROM docs WHERE CONTAINS(text, 'search term');
SELECT * FROM docs WHERE text ILIKE '%pattern%';
SELECT * FROM docs WHERE text LIKE '%pattern%';
```

**Fuzzy string matching** (approximate, not semantic):

```sql
SELECT jaccard('duck', 'luck');                       -- 0-1, higher = more similar
SELECT jaro_winkler_similarity('duckdb', 'duckbd');   -- 0-1, higher = more similar
SELECT damerau_levenshtein('duck', 'dukc');            -- edit distance with transpositions
SELECT editdist3('kitten', 'sitting');                 -- Levenshtein edit distance
```

**Regex:**

```sql
SELECT regexp_matches(text, 'pattern');
SELECT regexp_extract(text, '(\d+)-(\d+)', 1);
SELECT regexp_replace(text, 'old', 'new', 'g');
```

**Tokenization:**

```sql
SELECT regexp_split_to_table(text, '\s+') AS token FROM docs;
```

### Tier 2: Full Text Search (fts extension)

Keyword-based search with BM25 ranking. Handles word forms via stemming, but not semantic meaning.

```sql
INSTALL fts; LOAD fts;

-- Create a full-text index
PRAGMA create_fts_index('docs', 'id', 'text', stemmer = 'english');

-- Search with BM25 scoring
SELECT d.*, score
FROM docs d
JOIN (
    SELECT *, fts_main_docs.match_bm25(id, 'search query') AS score
    FROM docs
) s ON d.id = s.id
WHERE score IS NOT NULL
ORDER BY score DESC;

-- Stemming function
SELECT stem('learning', 'english');  -- returns 'learn'
```

### Tier 3: Vector Similarity Search (vss extension)

Semantic search using vector embeddings. DuckDB provides index and distance functions; generate embeddings externally (e.g., sentence-transformers, OpenAI API).

```sql
INSTALL vss; LOAD vss;

-- Table with embedding column
CREATE TABLE docs (id INT, text VARCHAR, embedding FLOAT[384]);

-- HNSW index for fast nearest-neighbor search
CREATE INDEX idx ON docs USING HNSW (embedding) WITH (metric = 'cosine');

-- Distance functions
SELECT array_cosine_distance(a.embedding, b.embedding) FROM ...;
SELECT array_distance(a.embedding, b.embedding) FROM ...;           -- L2
SELECT array_negative_inner_product(a.embedding, b.embedding) FROM ...;

-- Nearest-neighbor search (uses HNSW index)
SELECT * FROM docs
ORDER BY array_cosine_distance(embedding, [0.1, 0.2, ...]::FLOAT[384])
LIMIT 10;

-- Fuzzy join / top-K macros
SELECT * FROM vss_join(table_a, table_b, a_embed, b_embed, 10, 'cosine');
SELECT * FROM vss_match(docs, embedding, query_vector, 10, 'cosine');
```

## Common Recipes

```bash
# Analyze a CSV
duckdb -c "SUMMARIZE SELECT * FROM 'data.csv'"
duckdb -c "DESCRIBE SELECT * FROM 'data.csv'"
duckdb -c "SELECT count(*) FROM 'data.csv'"

# Convert between formats
duckdb -c "COPY (SELECT * FROM 'input.csv') TO 'output.parquet' (FORMAT PARQUET)"
duckdb -c "COPY (SELECT * FROM 'input.parquet') TO 'output.csv' (HEADER)"
duckdb -c "COPY (SELECT * FROM 'input.json') TO 'output.parquet' (FORMAT PARQUET)"
```

```sql
-- Query remote files
INSTALL httpfs; LOAD httpfs;
SELECT * FROM 'https://example.com/data.parquet' LIMIT 10;

-- Attach multiple databases
ATTACH 'other.duckdb' AS other;
SELECT * FROM other.main.my_table;
```
