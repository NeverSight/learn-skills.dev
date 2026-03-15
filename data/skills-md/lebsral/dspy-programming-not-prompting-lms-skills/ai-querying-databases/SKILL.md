---
name: ai-querying-databases
description: Build AI that answers questions about your database. Use when you need text-to-SQL, natural language database queries, a data assistant for non-technical users, AI-powered analytics, plain English database search, or a chatbot that talks to your database. Covers DSPy pipelines for schema understanding, SQL generation, validation, and result interpretation.
---

# Build AI That Answers Questions About Your Database

Guide the user through building an AI that takes plain English questions and returns answers from a SQL database. The pattern: understand the schema, generate SQL, validate it, run it, and explain the results.

## When you need this

- Sales reps asking "how many deals closed last month?" without writing SQL
- Executives asking revenue questions in plain English
- Support agents looking up customer records by description
- Internal data assistants for non-technical staff
- Any "chat with your database" feature

## How it's different from document search

| | Document search (`/ai-searching-docs`) | Database querying (this skill) |
|---|---|---|
| Data type | Unstructured text (PDFs, articles, docs) | Structured data (tables, rows, columns) |
| How it works | Embed + retrieve passages | Understand schema + generate SQL |
| Output | Text answer grounded in passages | Data from query results + interpretation |
| Key challenge | Finding relevant passages | Writing correct, safe SQL |

## Step 1: Understand the setup

Ask the user:
1. **What database?** (Postgres, MySQL, SQLite, Snowflake, BigQuery, etc.)
2. **What tables matter?** (all of them, or a subset?)
3. **Who asks questions?** (technical users, business users, customers?)
4. **Read-only access?** (this should always be yes for AI-generated SQL)

## Step 2: Connect to your database

Use SQLAlchemy for provider-agnostic database access:

```python
from sqlalchemy import create_engine, inspect, text

# PostgreSQL
engine = create_engine("postgresql://user:pass@host:5432/mydb")

# MySQL
engine = create_engine("mysql+pymysql://user:pass@host:3306/mydb")

# SQLite (for development)
engine = create_engine("sqlite:///local.db")

# Snowflake
engine = create_engine("snowflake://user:pass@account/db/schema")

# BigQuery
engine = create_engine("bigquery://project/dataset")
```

### Build schema descriptions for the AI

The AI needs to understand your tables to write correct SQL:

```python
def get_schema_description(engine, tables=None):
    """Build a text description of database schema for the AI."""
    inspector = inspect(engine)
    tables = tables or inspector.get_table_names()

    descriptions = []
    for table in tables:
        columns = inspector.get_columns(table)
        col_descs = []
        for col in columns:
            col_descs.append(f"  - {col['name']} ({col['type']})")

        pk = inspector.get_pk_constraint(table)
        pk_cols = pk['constrained_columns'] if pk else []

        desc = f"Table: {table}\n"
        if pk_cols:
            desc += f"  Primary key: {', '.join(pk_cols)}\n"
        desc += "  Columns:\n" + "\n".join(col_descs)
        descriptions.append(desc)

    return "\n\n".join(descriptions)

schema = get_schema_description(engine)
print(schema)
```

### Add business context (optional but helpful)

Raw column names like `cust_ltv_90d` don't mean much to the AI. Add descriptions:

```python
TABLE_DESCRIPTIONS = {
    "orders": "Customer orders with amounts, dates, and status",
    "customers": "Customer profiles with contact info and signup date",
    "products": "Product catalog with names, prices, and categories",
}

COLUMN_DESCRIPTIONS = {
    "orders.cust_ltv_90d": "Customer lifetime value over the last 90 days in USD",
    "orders.gmv": "Gross merchandise value (total order amount before discounts)",
}

def get_enriched_schema(engine, table_descs=None, col_descs=None):
    """Schema description with business context."""
    inspector = inspect(engine)
    table_descs = table_descs or {}
    col_descs = col_descs or {}

    descriptions = []
    for table in inspector.get_table_names():
        desc = f"Table: {table}"
        if table in table_descs:
            desc += f" -- {table_descs[table]}"
        desc += "\n  Columns:\n"

        for col in inspector.get_columns(table):
            col_key = f"{table}.{col['name']}"
            col_desc = f"  - {col['name']} ({col['type']})"
            if col_key in col_descs:
                col_desc += f" -- {col_descs[col_key]}"
            desc += col_desc + "\n"

        descriptions.append(desc)

    return "\n".join(descriptions)
```

## Step 3: Build the text-to-SQL pipeline

Two-stage approach: first pick the relevant tables, then generate SQL.

### Stage 1: Table selection (for databases with many tables)

```python
import dspy

class SelectTables(dspy.Signature):
    """Given a database schema and a user question, select which tables
    are needed to answer the question."""
    schema: str = dspy.InputField(desc="Database schema description")
    question: str = dspy.InputField(desc="User's question in plain English")
    tables: list[str] = dspy.OutputField(desc="List of table names needed")
    reasoning: str = dspy.OutputField(desc="Why these tables are needed")
```

### Stage 2: SQL generation

```python
class GenerateSQL(dspy.Signature):
    """Write a SQL SELECT query to answer the user's question.
    Only use tables and columns that exist in the schema."""
    schema: str = dspy.InputField(desc="Database schema for relevant tables")
    question: str = dspy.InputField(desc="User's question in plain English")
    sql: str = dspy.OutputField(desc="SQL SELECT query (read-only, no mutations)")
```

### The full pipeline

```python
class DatabaseQA(dspy.Module):
    def __init__(self, engine, schema, use_table_selection=False):
        self.engine = engine
        self.full_schema = schema
        self.use_table_selection = use_table_selection

        if use_table_selection:
            self.select_tables = dspy.ChainOfThought(SelectTables)
        self.generate_sql = dspy.ChainOfThought(GenerateSQL)
        self.interpret = dspy.ChainOfThought(InterpretResults)

    def forward(self, question):
        # Pick relevant tables (for large schemas)
        if self.use_table_selection:
            selected = self.select_tables(
                schema=self.full_schema, question=question
            )
            schema = filter_schema(self.full_schema, selected.tables)
        else:
            schema = self.full_schema

        # Generate SQL
        result = self.generate_sql(schema=schema, question=question)
        sql = result.sql.strip().rstrip(";")

        # Validate (see Step 4)
        validate_sql(sql)

        # Execute
        rows = execute_query(self.engine, sql)

        # Interpret results
        interpretation = self.interpret(
            question=question, sql=sql, results=str(rows[:20])
        )
        return dspy.Prediction(
            sql=sql, rows=rows, answer=interpretation.answer
        )
```

### Helper: filter schema to selected tables

```python
def filter_schema(full_schema, table_names):
    """Keep only the schema sections for selected tables."""
    sections = full_schema.split("\n\n")
    filtered = []
    for section in sections:
        for table in table_names:
            if section.startswith(f"Table: {table}"):
                filtered.append(section)
                break
    return "\n\n".join(filtered)
```

## Step 4: Validate SQL before execution

Never run AI-generated SQL without validation. Use `dspy.Assert` for hard constraints and `dspy.Suggest` for style guidance:

```python
import sqlparse

def validate_sql(sql):
    """Validate AI-generated SQL is safe and well-formed."""
    sql_upper = sql.strip().upper()

    # Hard safety constraints
    dspy.Assert(
        sql_upper.startswith("SELECT"),
        "Only SELECT queries are allowed. Do not generate INSERT, UPDATE, DELETE, DROP, or ALTER."
    )

    dangerous = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "EXEC"]
    for keyword in dangerous:
        dspy.Assert(
            keyword not in sql_upper.split("SELECT", 1)[0],
            f"Query contains forbidden keyword: {keyword}"
        )

    # Syntax check
    parsed = sqlparse.parse(sql)
    dspy.Assert(len(parsed) == 1, "Generate exactly one SQL statement")
    dspy.Assert(
        parsed[0].get_type() == "SELECT",
        "Only SELECT statements are allowed"
    )

    # Style suggestions (soft constraints — AI will retry if possible)
    dspy.Suggest(
        "JOIN" not in sql_upper or "ON" in sql_upper,
        "Use explicit JOIN ... ON syntax instead of implicit joins in WHERE"
    )
```

### Execute with safety limits

```python
from sqlalchemy import text

def execute_query(engine, sql, row_limit=100, timeout_seconds=30):
    """Execute validated SQL with safety limits."""
    # Add row limit if not present
    if "LIMIT" not in sql.upper():
        sql = f"{sql} LIMIT {row_limit}"

    with engine.connect() as conn:
        conn = conn.execution_options(timeout=timeout_seconds)
        result = conn.execute(text(sql))
        columns = list(result.keys())
        rows = [dict(zip(columns, row)) for row in result.fetchall()]

    return rows
```

## Step 5: Interpret results

Convert raw query results back to a natural language answer:

```python
class InterpretResults(dspy.Signature):
    """Convert SQL query results into a clear, natural language answer
    to the user's original question."""
    question: str = dspy.InputField(desc="The user's original question")
    sql: str = dspy.InputField(desc="The SQL query that was run")
    results: str = dspy.InputField(desc="Query results as a string")
    answer: str = dspy.OutputField(desc="Natural language answer to the question")
```

## Step 6: Handle large schemas

For databases with 50+ tables, sending the full schema to the AI is expensive and confusing. Use embedding-based schema retrieval:

```python
import chromadb

def build_schema_index(engine, table_descriptions=None):
    """Build a searchable index of table schemas."""
    client = chromadb.PersistentClient(path="./schema_index")
    collection = client.get_or_create_collection("table_schemas")

    inspector = inspect(engine)
    table_descriptions = table_descriptions or {}

    for table in inspector.get_table_names():
        columns = inspector.get_columns(table)
        col_names = [c["name"] for c in columns]

        # Searchable description
        desc = table_descriptions.get(table, table)
        searchable = f"{table}: {desc}. Columns: {', '.join(col_names)}"

        collection.upsert(
            documents=[searchable],
            ids=[table],
            metadatas=[{"table": table}],
        )

    return collection

class SchemaRetriever(dspy.Retrieve):
    """Retrieve relevant table schemas based on the question."""
    def __init__(self, collection, engine, k=5):
        super().__init__(k=k)
        self.collection = collection
        self.engine = engine

    def forward(self, query, k=None):
        k = k or self.k
        results = self.collection.query(query_texts=[query], n_results=k)

        # Get full schema for matched tables
        tables = [m["table"] for m in results["metadatas"][0]]
        schema = get_schema_description(self.engine, tables=tables)
        return dspy.Prediction(passages=[schema])
```

Then use it in your pipeline:

```python
class LargeSchemaQA(dspy.Module):
    def __init__(self, engine, schema_collection):
        self.engine = engine
        self.schema_retriever = SchemaRetriever(schema_collection, engine, k=5)
        self.generate_sql = dspy.ChainOfThought(GenerateSQL)
        self.interpret = dspy.ChainOfThought(InterpretResults)

    def forward(self, question):
        schema = self.schema_retriever(question).passages[0]
        result = self.generate_sql(schema=schema, question=question)
        sql = result.sql.strip().rstrip(";")
        validate_sql(sql)
        rows = execute_query(self.engine, sql)
        interpretation = self.interpret(
            question=question, sql=sql, results=str(rows[:20])
        )
        return dspy.Prediction(sql=sql, rows=rows, answer=interpretation.answer)
```

## Step 7: Test and optimize

### SQL execution accuracy metric

```python
def sql_accuracy(example, prediction, trace=None):
    """Check if the generated SQL returns the correct answer."""
    try:
        # Compare results (not SQL text — many valid SQL queries per question)
        expected = set(str(r) for r in example.expected_rows)
        actual = set(str(r) for r in prediction.rows)
        return float(expected == actual)
    except Exception:
        return 0.0

def answer_quality(example, prediction, trace=None):
    """Check if the natural language answer is correct."""
    judge = dspy.Predict("question, expected_answer, predicted_answer -> is_correct: bool")
    result = judge(
        question=example.question,
        expected_answer=example.answer,
        predicted_answer=prediction.answer,
    )
    return float(result.is_correct)
```

### Build training data

```python
trainset = [
    dspy.Example(
        question="How many orders were placed last month?",
        answer="There were 1,247 orders placed last month.",
        expected_sql="SELECT COUNT(*) FROM orders WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')",
    ).with_inputs("question"),
    # Add 20-50 question/answer pairs covering your common queries
]
```

### Optimize

```python
optimizer = dspy.MIPROv2(metric=answer_quality, auto="medium")
optimized = optimizer.compile(DatabaseQA(engine, schema), trainset=trainset)
optimized.save("optimized_db_qa.json")
```

## Step 8: Security and production

### Security checklist

| Control | How |
|---------|-----|
| Read-only database user | `GRANT SELECT ON ALL TABLES TO ai_reader` |
| Query timeout | `execution_options(timeout=30)` in SQLAlchemy |
| Row limit | Always append `LIMIT` to queries |
| Table allowlist | Only include permitted tables in the schema |
| SQL validation | `dspy.Assert` for SELECT-only, no dangerous keywords |
| Audit logging | Log every question, generated SQL, and results |
| No raw credentials | Use environment variables or secrets manager |

### Audit logging

```python
import json
from datetime import datetime

def log_query(question, sql, row_count, user_id=None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "question": question,
        "sql": sql,
        "row_count": row_count,
    }
    with open("query_audit.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
```

### Table allowlist

```python
ALLOWED_TABLES = {"orders", "products", "customers", "categories"}

def get_safe_schema(engine, allowed=ALLOWED_TABLES):
    inspector = inspect(engine)
    all_tables = set(inspector.get_table_names())
    tables = list(all_tables & allowed)
    return get_schema_description(engine, tables=tables)
```

## Key patterns

- **Two-stage pipeline**: table selection + SQL generation works better than one giant prompt
- **Validate before executing**: never run AI-generated SQL without safety checks
- **Compare results, not SQL**: many valid SQL queries produce the same answer
- **Business context matters**: column descriptions improve accuracy more than extra examples
- **Start with a small table allowlist**: expand as you build confidence
- **Read-only, always**: the AI database user should never have write permissions

## Additional resources

- For worked examples, see [examples.md](examples.md)
- Use `/ai-serving-apis` to put your database assistant behind a REST API
- Use `/ai-building-pipelines` for complex multi-step query workflows
- Use `/ai-checking-outputs` for additional SQL validation patterns
- Use `/ai-following-rules` to enforce query policies (e.g., no queries on PII columns)
- Use `/ai-improving-accuracy` to measure and optimize query quality
- Use `/ai-tracing-requests` to debug individual query failures
