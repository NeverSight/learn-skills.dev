---
name: etl-core-patterns
description: Core ETL reliability patterns including idempotency, checkpointing, error handling, chunking, retry logic, and logging.
allowed-tools: Read Write Edit Grep Glob Bash
---

# ETL Core Patterns

Reliability patterns for production data pipelines.

## Idempotency Patterns

```python
# Pattern 1: Delete-then-insert (simple, works for small datasets)
def load_daily_data(date: str, df: pd.DataFrame) -> None:
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM daily_metrics WHERE date = :date"),
            {"date": date}
        )
        df.to_sql('daily_metrics', conn, if_exists='append', index=False)

# Pattern 2: UPSERT (better for large datasets)
def upsert_records(df: pd.DataFrame) -> None:
    for batch in chunked(df.to_dict('records'), 1000):
        stmt = insert(MyTable).values(batch)
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'],
            set_={col: stmt.excluded[col] for col in update_cols}
        )
        session.execute(stmt)

# Pattern 3: Source hash for change detection
def extract_with_hash(df: pd.DataFrame) -> pd.DataFrame:
    hash_cols = ['id', 'name', 'value', 'updated_at']
    df['_row_hash'] = pd.util.hash_pandas_object(df[hash_cols])
    return df
```

## Checkpointing

```python
import json
from pathlib import Path

class Checkpoint:
    def __init__(self, path: str):
        self.path = Path(path)
        self.state = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            return json.loads(self.path.read_text())
        return {}

    def save(self) -> None:
        self.path.write_text(json.dumps(self.state, default=str))

    def get_last_processed(self, key: str) -> str | None:
        return self.state.get(key)

    def set_last_processed(self, key: str, value: str) -> None:
        self.state[key] = value
        self.save()

# Usage
checkpoint = Checkpoint('.etl_checkpoint.json')
last_id = checkpoint.get_last_processed('users_sync')

for batch in fetch_users_since(last_id):
    process(batch)
    checkpoint.set_last_processed('users_sync', batch[-1]['id'])
```

## Error Handling

```python
from dataclasses import dataclass

@dataclass
class FailedRecord:
    source_id: str
    error: str
    raw_data: dict
    timestamp: datetime

class ETLProcessor:
    def __init__(self):
        self.failed_records: list[FailedRecord] = []

    def process_batch(self, records: list[dict]) -> list[dict]:
        processed = []
        for record in records:
            try:
                processed.append(self.transform(record))
            except Exception as e:
                self.failed_records.append(FailedRecord(
                    source_id=record.get('id', 'unknown'),
                    error=str(e),
                    raw_data=record,
                    timestamp=datetime.now()
                ))
        return processed

    def save_failures(self, path: str) -> None:
        if self.failed_records:
            df = pd.DataFrame([vars(r) for r in self.failed_records])
            df.to_parquet(f"{path}/failures_{datetime.now():%Y%m%d_%H%M%S}.parquet")

# Dead letter queue pattern
def process_with_dlq(records: list[dict], dlq_table: str) -> None:
    for record in records:
        try:
            process(record)
        except Exception as e:
            save_to_dlq(dlq_table, record, str(e))
```

## Chunked Processing

```python
from typing import Iterator, TypeVar

T = TypeVar('T')

def chunked(iterable: Iterator[T], size: int) -> Iterator[list[T]]:
    """Yield successive chunks from iterable."""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch

# Memory-efficient file processing
def process_large_csv(path: str, chunk_size: int = 50_000) -> None:
    for i, chunk in enumerate(pd.read_csv(path, chunksize=chunk_size)):
        print(f"Processing chunk {i}: {len(chunk)} rows")
        transformed = transform(chunk)
        load(transformed, mode='append')
        del chunk, transformed  # Explicit memory cleanup
        gc.collect()
```

## Retry Logic

```python
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for retrying failed operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"Attempt {attempt + 1} failed: {e}. Retrying in {current_delay}s")
                        time.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1.0, backoff=2.0)
def fetch_from_api(url: str) -> dict:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
```

## Logging Best Practices

```python
import structlog

logger = structlog.get_logger()

def process_with_logging(batch_id: str, records: list[dict]) -> None:
    log = logger.bind(batch_id=batch_id, record_count=len(records))

    log.info("batch_started")

    try:
        result = process(records)
        log.info("batch_completed",
                 processed=result.processed_count,
                 failed=result.failed_count)
    except Exception as e:
        log.error("batch_failed", error=str(e))
        raise
```
