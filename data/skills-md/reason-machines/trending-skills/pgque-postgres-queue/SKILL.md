---
name: pgque-postgres-queue
description: Expert skill for PgQue – a zero-bloat, snapshot-based Postgres queue using pure PL/pgSQL with no C extensions required.
triggers:
  - set up a postgres queue
  - use pgque for message queue
  - zero bloat postgres queue
  - pgq queue in postgres
  - fan-out event queue postgres
  - postgres queue without skip locked
  - install pgque
  - snapshot based postgres queue
---

# PgQue – Zero-Bloat Postgres Queue

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

PgQue is a pure PL/pgSQL reimplementation of the battle-tested PgQ (Skype/Postgres) architecture. It uses **snapshot-based batching** and **TRUNCATE-based table rotation** instead of row-level locking, delivering zero dead-tuple bloat, predictable performance under sustained load, and native fan-out — all from a single SQL file on any Postgres 14+ instance including managed providers (RDS, Aurora, Cloud SQL, Supabase, Neon).

## Key Concepts

- **Tick**: A periodic snapshot that closes a batch of events. Nothing is delivered until a tick fires.
- **Batch**: A group of events captured in one tick, consumed atomically by a subscriber.
- **Subscriber/Consumer**: A named cursor on the event log. Multiple consumers get independent copies of every batch (fan-out).
- **Zero bloat**: Events are stored in rotating tables and cleared via `TRUNCATE`, never `DELETE`. No dead tuples.
- **Latency trade-off**: End-to-end delivery is ~1–2 s (one tick interval + poll). Per-call function latency is microseconds.

## Installation

### Requirements
- Postgres 14+
- `pg_cron` (recommended) **or** an external scheduler calling `pgque.ticker()` every second

### Install from SQL file

```bash
# Clone the repo
git clone https://github.com/NikolayS/pgque.git
cd pgque

# Install in a single transaction
PAGER=cat psql --no-psqlrc --single-transaction -d mydb -f sql/pgque.sql
```

Or inside a `psql` session:

```sql
begin;
\i sql/pgque.sql
commit;
```

### Start the ticker (pg_cron)

```sql
-- Creates pg_cron jobs for ticker (every 1s) and maintenance (every 30s)
select pgque.start();
```

### Start the ticker (without pg_cron)

Run these externally on a schedule:

```bash
# Every 1 second
psql -d mydb -c "select pgque.ticker()"

# Every 30 seconds
psql -d mydb -c "select pgque.maint()"
```

> **Warning**: Without a running ticker, consumers see nothing. Enqueue works, but no batches are created.

### Uninstall

```sql
\i sql/pgque_uninstall.sql
```

## Roles & Grants

| Role | Use |
|---|---|
| `pgque_reader` | Dashboards, metrics, read-only |
| `pgque_writer` | Producers and consumers (most apps) |
| `pgque_admin` | Operators, migrations |

```sql
-- Grant producer/consumer access to app user
CREATE USER app_worker WITH PASSWORD '...';
GRANT pgque_writer TO app_worker;

-- Grant read-only metrics access
CREATE USER metrics_reader WITH PASSWORD '...';
GRANT pgque_reader TO metrics_reader;
```

## Core API (Modern Style)

### Create a Queue

```sql
SELECT pgque.create_queue('orders');
```

### Subscribe a Consumer

```sql
-- Register a named consumer on the queue
SELECT pgque.subscribe('orders', 'order-processor');
```

### Send Events (Enqueue)

```sql
-- Send a single event (type, data)
SELECT pgque.send('orders', 'new_order', '{"order_id": 42, "amount": 99.99}');

-- Send a batch of events
SELECT pgque.send_batch('orders', ARRAY[
  ROW('new_order', '{"order_id": 43}')::pgque.event_data,
  ROW('new_order', '{"order_id": 44}')::pgque.event_data
]);
```

### Receive and Acknowledge Events

```sql
-- Receive next batch for a consumer (returns batch_id + events)
SELECT * FROM pgque.receive('orders', 'order-processor');

-- Acknowledge successful processing (batch_id from receive)
SELECT pgque.ack('orders', 'order-processor', :batch_id);

-- Negative-acknowledge (retry / dead-letter)
SELECT pgque.nack('orders', 'order-processor', :batch_id);
```

### Unsubscribe

```sql
SELECT pgque.unsubscribe('orders', 'order-processor');
```

## Low-Level PgQ API

These map directly to the original PgQ primitives and are also available via `pgque_writer`:

```sql
-- Enqueue a single event
SELECT pgque.insert_event('orders', 'new_order', '{"order_id": 42}');

-- Register a consumer
SELECT pgque.register_consumer('orders', 'order-processor');

-- Get the next available batch ID
SELECT pgque.next_batch('orders', 'order-processor');
-- Returns: batch_id (bigint), or NULL if nothing ready

-- Fetch all events in a batch
SELECT * FROM pgque.get_batch_events(:batch_id);
-- Returns: ev_id, ev_time, ev_txid, ev_retry, ev_type, ev_data, ev_extra1..4

-- Mark batch as successfully processed
SELECT pgque.finish_batch(:batch_id);

-- Schedule an event for retry (with delay in seconds)
SELECT pgque.event_retry(:batch_id, :ev_id, 60);  -- retry in 60s

-- Unregister consumer
SELECT pgque.unregister_consumer('orders', 'order-processor');
```

## Complete Working Example

### Producer (Python with psycopg2)

```python
import psycopg2
import json
import os

conn = psycopg2.connect(os.environ["DATABASE_URL"])
conn.autocommit = False

def enqueue_order(order_id: int, amount: float):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT pgque.send(%s, %s, %s)",
            ("orders", "new_order", json.dumps({"order_id": order_id, "amount": amount}))
        )
    conn.commit()

enqueue_order(42, 99.99)
```

### Consumer (Python with psycopg2)

```python
import psycopg2
import psycopg2.extras
import json
import os
import time

conn = psycopg2.connect(os.environ["DATABASE_URL"])
conn.autocommit = False

QUEUE = "orders"
CONSUMER = "order-processor"

def setup():
    with conn.cursor() as cur:
        cur.execute("SELECT pgque.subscribe(%s, %s)", (QUEUE, CONSUMER))
    conn.commit()

def process_batch():
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM pgque.receive(%s, %s)", (QUEUE, CONSUMER))
        rows = cur.fetchall()

    if not rows:
        conn.rollback()
        return False

    batch_id = rows[0]["batch_id"]
    for row in rows:
        event = json.loads(row["ev_data"])
        print(f"Processing order {event['order_id']}")
        # ... your processing logic ...

    with conn.cursor() as cur:
        cur.execute("SELECT pgque.ack(%s, %s, %s)", (QUEUE, CONSUMER, batch_id))
    conn.commit()
    return True

setup()
while True:
    if not process_batch():
        time.sleep(1)  # wait for next tick
```

### Fan-Out Example (Multiple Independent Consumers)

```sql
-- One queue, multiple consumers each get ALL events independently
SELECT pgque.create_queue('user-events');

SELECT pgque.subscribe('user-events', 'analytics-service');
SELECT pgque.subscribe('user-events', 'notification-service');
SELECT pgque.subscribe('user-events', 'audit-log');

-- Producer sends once
SELECT pgque.send('user-events', 'user_signup', '{"user_id": 1}');

-- Each consumer independently receives the same event
SELECT * FROM pgque.receive('user-events', 'analytics-service');
SELECT * FROM pgque.receive('user-events', 'notification-service');
SELECT * FROM pgque.receive('user-events', 'audit-log');
```

### Retry / Dead Letter Pattern

```sql
-- Using low-level API with retry logic
DO $$
DECLARE
  v_batch_id bigint;
  v_ev       record;
BEGIN
  -- Get next batch
  SELECT pgque.next_batch('orders', 'order-processor') INTO v_batch_id;

  IF v_batch_id IS NULL THEN
    RAISE NOTICE 'No batch available';
    RETURN;
  END IF;

  -- Process each event
  FOR v_ev IN SELECT * FROM pgque.get_batch_events(v_batch_id) LOOP
    BEGIN
      -- Attempt processing
      RAISE NOTICE 'Processing event % type %', v_ev.ev_id, v_ev.ev_type;

      -- On transient failure, retry after 30 seconds
      -- SELECT pgque.event_retry(v_batch_id, v_ev.ev_id, 30);

    EXCEPTION WHEN OTHERS THEN
      -- Schedule retry
      PERFORM pgque.event_retry(v_batch_id, v_ev.ev_id, 60);
      RAISE NOTICE 'Event % queued for retry', v_ev.ev_id;
    END;
  END LOOP;

  -- Finish batch (events not retried are acked)
  PERFORM pgque.finish_batch(v_batch_id);
END;
$$;
```

## Monitoring & Introspection

```sql
-- Queue info (depth, consumer count, last tick)
SELECT * FROM pgque.get_queue_info();
SELECT * FROM pgque.get_queue_info('orders');

-- Consumer lag and position
SELECT * FROM pgque.get_consumer_info();
SELECT * FROM pgque.get_consumer_info('orders');
SELECT * FROM pgque.get_consumer_info('orders', 'order-processor');

-- Batch details
SELECT * FROM pgque.get_batch_info(:batch_id);

-- Version
SELECT pgque.version();
```

## Configuration & Tuning

### Tick Frequency

```sql
-- Default: ticker called every 1 second via pg_cron
-- To change tick interval, update the pg_cron job:
SELECT cron.alter_job(
  job_id := (SELECT jobid FROM cron.job WHERE command LIKE '%pgque.ticker%'),
  schedule := '* * * * *'  -- every minute (coarser)
);
```

### Force Immediate Tick (Testing/Demos)

```sql
-- Force a tick right now without waiting for pg_cron
SELECT pgque.force_tick('orders');
-- or
SELECT pgque.ticker();
```

### pg_cron Log Hygiene

```sql
-- Disable run logging (ticker runs every second = 3600 rows/hour)
ALTER SYSTEM SET cron.log_run = off;
SELECT pg_reload_conf();

-- Or periodically purge:
SELECT cron.schedule('pgque-cron-purge', '0 * * * *',
  $$DELETE FROM cron.job_run_details WHERE end_time < now() - interval '1 hour'$$
);
```

### pg_cron in Different Database

If pg_cron is in `postgres` DB but PgQue is in `mydb`:

```sql
-- Run from the pg_cron database (postgres)
SELECT cron.schedule_in_database(
  'pgque-ticker', '* * * * *',
  'SELECT pgque.ticker()', 'mydb'
);
SELECT cron.schedule_in_database(
  'pgque-maint', '* * * * *',
  'SELECT pgque.maint()', 'mydb'
);
```

## Common Patterns

### Transactional Enqueue (Send with Business Logic)

```sql
-- Event is only enqueued if the whole transaction commits
BEGIN;
  INSERT INTO orders (id, amount) VALUES (42, 99.99);
  SELECT pgque.send('orders', 'new_order', '{"order_id": 42}');
COMMIT;
```

### Queue Depth Check Before Scaling

```sql
SELECT
  queue_name,
  ev_per_sec,
  consumer_count,
  pending_events
FROM pgque.get_queue_info()
WHERE pending_events > 1000;
```

### List All Consumers with Lag

```sql
SELECT
  queue_name,
  consumer_name,
  pending_events AS lag,
  last_seen
FROM pgque.get_consumer_info()
ORDER BY lag DESC;
```

## Troubleshooting

### Consumers receive nothing

**Cause**: Ticker is not running.

```sql
-- Check if ticker has fired recently
SELECT * FROM pgque.get_queue_info('orders');
-- Look at last_tick timestamp

-- Manually fire a tick
SELECT pgque.ticker();

-- Check pg_cron jobs exist
SELECT * FROM cron.job WHERE command LIKE '%pgque%';
```

### Events not appearing after send

```sql
-- Confirm ticker is running; force one
SELECT pgque.ticker();

-- Check queue exists
SELECT * FROM pgque.get_queue_info('orders');

-- Check consumer is registered
SELECT * FROM pgque.get_consumer_info('orders', 'my-consumer');
```

### Performance / VACUUM pressure

PgQue is immune to dead-tuple bloat in the event path by design. If you see VACUUM activity, it's from your own application tables, not from PgQue's queue tables.

### Retry events not reappearing

```sql
-- Maintenance job handles retry scheduling
-- Make sure pgque.maint() is running every ~30s
SELECT pgque.maint();

-- Check for events in retry state
SELECT * FROM pgque.get_queue_info('orders');
```

### Upgrade / Reinstall

Upgrade paths are still being stabilized. To safely reinstall:

```bash
psql -d mydb -c "\i sql/pgque_uninstall.sql"
psql -d mydb --single-transaction -f sql/pgque.sql
psql -d mydb -c "select pgque.start()"
```

## Architecture Summary

```
Producer → pgque.send() → event tables (rotating)
                                    ↓
                           pgque.ticker()  ←── pg_cron (every 1s)
                                    ↓
                           batch snapshot created
                                    ↓
Consumer A → pgque.receive() → batch events → pgque.ack()
Consumer B → pgque.receive() → same batch  → pgque.ack()
Consumer C → pgque.receive() → same batch  → pgque.ack()
                                    ↓
                           pgque.maint() → TRUNCATE old tables
                                           (zero dead tuples)
```
