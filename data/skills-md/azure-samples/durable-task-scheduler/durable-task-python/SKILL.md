---
name: durable-task-python
description: Build durable, fault-tolerant workflows in Python using the Durable Task SDK with Azure Durable Task Scheduler. Use when creating orchestrations, activities, entities, or implementing patterns like function chaining, fan-out/fan-in, human interaction, or stateful agents. Applies to any Python application requiring durable execution, state persistence, or distributed transactions without Azure Functions dependency.
---

# Durable Task Python SDK with Durable Task Scheduler

Build fault-tolerant, stateful workflows in Python applications using the Durable Task SDK connected to Azure Durable Task Scheduler.

## Quick Start

### Required Packages

```bash
pip install durabletask durabletask-azuremanaged azure-identity
```

Or add to `requirements.txt`:

```text
durabletask
durabletask-azuremanaged
azure-identity
```

### Minimal Worker + Client Setup

```python
import os
from azure.identity import DefaultAzureCredential
from durabletask import task
from durabletask.client import OrchestrationStatus
from durabletask.azuremanaged.client import DurableTaskSchedulerClient
from durabletask.azuremanaged.worker import DurableTaskSchedulerWorker


# Activity function
def hello(ctx: task.ActivityContext, name: str) -> str:
    return f"Hello {name}!"


# Orchestrator function
def my_orchestration(ctx: task.OrchestrationContext, input: str):
    result = yield ctx.call_activity(hello, input=input)
    return result


# Configuration - defaults to local emulator
taskhub = os.getenv("TASKHUB", "default")
endpoint = os.getenv("ENDPOINT", "http://localhost:8080")
secure_channel = endpoint != "http://localhost:8080"
credential = None if endpoint == "http://localhost:8080" else DefaultAzureCredential()

# Start worker and run orchestration
with DurableTaskSchedulerWorker(
    host_address=endpoint,
    secure_channel=secure_channel,
    taskhub=taskhub,
    token_credential=credential
) as worker:
    worker.add_orchestrator(my_orchestration)
    worker.add_activity(hello)
    worker.start()

    # Create client and schedule orchestration
    dts_client = DurableTaskSchedulerClient(
        host_address=endpoint,
        secure_channel=secure_channel,
        taskhub=taskhub,
        token_credential=credential
    )
    
    instance_id = dts_client.schedule_new_orchestration(my_orchestration, input="World")
    state = dts_client.wait_for_orchestration_completion(instance_id, timeout=60)
    
    if state and state.runtime_status == OrchestrationStatus.COMPLETED:
        print(f"Result: {state.serialized_output}")
```

## Pattern Selection Guide

| Pattern | Use When |
|---------|----------|
| **Function Chaining** | Sequential steps where each depends on the previous |
| **Fan-Out/Fan-In** | Parallel processing with aggregated results |
| **Human Interaction** | Workflow pauses for external input/approval |
| **Durable Entities** | Stateful objects with operations (counters, accounts) |
| **Sub-Orchestrations** | Reusable workflow components or version isolation |
| **Eternal Orchestrations** | Long-running background processes with `continue_as_new` |
| **Monitoring** | Periodic polling with configurable timeouts |

See [references/patterns.md](references/patterns.md) for detailed implementations.

## Orchestration Structure

### Basic Orchestrator

```python
def my_orchestration(ctx: task.OrchestrationContext, input: str):
    """Orchestrator function - MUST be deterministic"""
    # Call activities sequentially
    step1 = yield ctx.call_activity(step1_activity, input=input)
    step2 = yield ctx.call_activity(step2_activity, input=step1)
    return step2
```

### Basic Activity

```python
def my_activity(ctx: task.ActivityContext, input: str) -> str:
    """Activity function - can have side effects, I/O, non-determinism"""
    # Perform actual work here
    print(f"Processing: {input}")
    return f"Processed: {input}"
```

### Registering with Worker

```python
with DurableTaskSchedulerWorker(...) as worker:
    worker.add_orchestrator(my_orchestration)
    worker.add_activity(step1_activity)
    worker.add_activity(step2_activity)
    worker.start()
```

## Critical Rules

### Orchestration Determinism

Orchestrations replay from history - all code MUST be deterministic. When an orchestration resumes, it replays all previous code to rebuild state. Non-deterministic code produces different results on replay, causing failures.

**NEVER do inside orchestrations:**
- `datetime.now()`, `datetime.utcnow()` → Use `ctx.current_utc_datetime`
- `uuid.uuid4()` → Use `ctx.new_uuid()`
- `random.random()` → Pass random values from activities
- Direct I/O, HTTP calls, database access → Move to activities
- `time.sleep()`, `asyncio.sleep()` → Use `ctx.create_timer()`
- Environment variables that may change → Pass as input or use activities
- Global mutable state → Pass state through activity results

**ALWAYS use:**
- `yield ctx.call_activity()` - Call activities
- `yield ctx.call_sub_orchestrator()` - Call sub-orchestrations
- `yield ctx.create_timer()` - Durable delays
- `yield ctx.wait_for_external_event()` - Wait for events
- `ctx.current_utc_datetime` - Current time
- `ctx.new_uuid()` - Generate GUIDs
- `ctx.set_custom_status()` - Set status

### Non-Determinism Patterns (WRONG vs CORRECT)

#### Getting Current Time

```python
# WRONG - datetime.now() returns different value on replay
def bad_orchestration(ctx: task.OrchestrationContext, _):
    current_time = datetime.now()  # Non-deterministic!
    if current_time.hour < 12:
        yield ctx.call_activity(morning_activity)

# CORRECT - ctx.current_utc_datetime is replayed consistently
def good_orchestration(ctx: task.OrchestrationContext, _):
    current_time = ctx.current_utc_datetime  # Deterministic
    if current_time.hour < 12:
        yield ctx.call_activity(morning_activity)
```

#### Generating UUIDs/Random Values

```python
# WRONG - uuid4() generates different value on replay
def bad_orchestration(ctx: task.OrchestrationContext, _):
    order_id = str(uuid.uuid4())  # Non-deterministic!
    yield ctx.call_activity(create_order, input=order_id)

# CORRECT - ctx.new_uuid() replays the same value
def good_orchestration(ctx: task.OrchestrationContext, _):
    order_id = str(ctx.new_uuid())  # Deterministic
    yield ctx.call_activity(create_order, input=order_id)
```

#### Random Numbers

```python
# WRONG - random produces different values on replay
def bad_orchestration(ctx: task.OrchestrationContext, _):
    delay = random.randint(1, 10)  # Non-deterministic!
    yield ctx.create_timer(timedelta(seconds=delay))

# CORRECT - generate random in activity, pass to orchestrator
def get_random_delay(ctx: task.ActivityContext, _) -> int:
    return random.randint(1, 10)  # OK in activity

def good_orchestration(ctx: task.OrchestrationContext, _):
    delay = yield ctx.call_activity(get_random_delay)  # Deterministic
    yield ctx.create_timer(timedelta(seconds=delay))
```

#### Sleeping/Delays

```python
# WRONG - time.sleep blocks and doesn't persist
def bad_orchestration(ctx: task.OrchestrationContext, _):
    yield ctx.call_activity(step1)
    time.sleep(60)  # Non-durable! Lost on restart
    yield ctx.call_activity(step2)

# CORRECT - ctx.create_timer is durable
def good_orchestration(ctx: task.OrchestrationContext, _):
    yield ctx.call_activity(step1)
    yield ctx.create_timer(timedelta(seconds=60))  # Durable timer
    yield ctx.call_activity(step2)
```

#### HTTP Calls and I/O

```python
# WRONG - HTTP call in orchestrator is non-deterministic
def bad_orchestration(ctx: task.OrchestrationContext, url: str):
    import requests
    response = requests.get(url)  # Non-deterministic!
    return response.json()

# CORRECT - move I/O to activity
def fetch_data(ctx: task.ActivityContext, url: str) -> dict:
    import requests
    response = requests.get(url)  # OK in activity
    return response.json()

def good_orchestration(ctx: task.OrchestrationContext, url: str):
    data = yield ctx.call_activity(fetch_data, input=url)  # Deterministic
    return data
```

#### Database Access

```python
# WRONG - database query in orchestrator
def bad_orchestration(ctx: task.OrchestrationContext, user_id: str):
    import sqlite3
    conn = sqlite3.connect('db.sqlite')  # Non-deterministic!
    cursor = conn.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    # ...

# CORRECT - database access in activity
def get_user(ctx: task.ActivityContext, user_id: str) -> dict:
    import sqlite3
    conn = sqlite3.connect('db.sqlite')  # OK in activity
    cursor = conn.execute("SELECT * FROM users WHERE id=?", (user_id,))
    return dict(cursor.fetchone())

def good_orchestration(ctx: task.OrchestrationContext, user_id: str):
    user = yield ctx.call_activity(get_user, input=user_id)
    # ...
```

#### Environment Variables

```python
# WRONG - env var might change between replays
def bad_orchestration(ctx: task.OrchestrationContext, _):
    api_endpoint = os.getenv("API_ENDPOINT")  # Could change!
    yield ctx.call_activity(call_api, input=api_endpoint)

# CORRECT - pass config as input or read in activity
def good_orchestration(ctx: task.OrchestrationContext, config: dict):
    api_endpoint = config["api_endpoint"]  # From input, deterministic
    yield ctx.call_activity(call_api, input=api_endpoint)

# ALSO CORRECT - read env var in activity
def call_api(ctx: task.ActivityContext, _) -> str:
    api_endpoint = os.getenv("API_ENDPOINT")  # OK in activity
    # make the call...
```

#### Conditional Logic Based on External State

```python
# WRONG - file existence can change between replays
def bad_orchestration(ctx: task.OrchestrationContext, path: str):
    if os.path.exists(path):  # Non-deterministic!
        yield ctx.call_activity(process_file, input=path)

# CORRECT - check in activity
def check_file_exists(ctx: task.ActivityContext, path: str) -> bool:
    return os.path.exists(path)  # OK in activity

def good_orchestration(ctx: task.OrchestrationContext, path: str):
    exists = yield ctx.call_activity(check_file_exists, input=path)
    if exists:  # Deterministic - based on activity result
        yield ctx.call_activity(process_file, input=path)
```

#### Dictionary/Set Iteration Order

```python
# POTENTIALLY WRONG - dict iteration order may vary (Python < 3.7)
def risky_orchestration(ctx: task.OrchestrationContext, items: dict):
    for key in items:  # Order might not be guaranteed
        yield ctx.call_activity(process, input=key)

# CORRECT - use sorted keys for deterministic order
def good_orchestration(ctx: task.OrchestrationContext, items: dict):
    for key in sorted(items.keys()):  # Guaranteed order
        yield ctx.call_activity(process, input=key)
```

#### Thread-Local or Global State

```python
# WRONG - global state can change
counter = 0

def bad_orchestration(ctx: task.OrchestrationContext, _):
    global counter
    counter += 1  # Non-deterministic across replays!
    yield ctx.call_activity(process, input=counter)

# CORRECT - pass state through orchestration input/output
def good_orchestration(ctx: task.OrchestrationContext, counter: int):
    counter += 1  # Local variable, deterministic
    yield ctx.call_activity(process, input=counter)
    # If continuing, pass counter forward
    ctx.continue_as_new(counter)
```

### Using yield

In Python, orchestrator functions use `yield` to await durable operations:

```python
# CORRECT - use yield
result = yield ctx.call_activity(my_activity, input="data")

# WRONG - will not work
result = ctx.call_activity(my_activity, input="data")  # Missing yield!
```

### Error Handling

```python
def orchestrator_with_error_handling(ctx: task.OrchestrationContext, input: str):
    try:
        result = yield ctx.call_activity(risky_activity, input=input)
        return result
    except task.TaskFailedError as e:
        # Activity failed - implement compensation
        ctx.set_custom_status({"error": str(e)})
        yield ctx.call_activity(compensation_activity, input=input)
        return "Compensated"
```

### Retry Policies

```python
from durabletask.task import RetryPolicy

retry_policy = RetryPolicy(
    first_retry_interval=5,  # seconds
    max_number_of_attempts=3,
    backoff_coefficient=2.0,
    max_retry_interval=60,  # seconds
    retry_timeout=300  # seconds
)

def orchestrator(ctx: task.OrchestrationContext, _):
    result = yield ctx.call_activity(
        unreliable_activity, 
        input="data",
        retry_policy=retry_policy
    )
    return result
```

## Working with Custom Types

The SDK supports dataclasses, namedtuples, and custom classes:

```python
from dataclasses import dataclass

@dataclass
class Order:
    product: str
    quantity: int
    cost: float

def process_order(ctx: task.ActivityContext, order: Order) -> str:
    return f"Processed {order.quantity}x {order.product}"

def order_workflow(ctx: task.OrchestrationContext, order: Order):
    result = yield ctx.call_activity(process_order, input=order)
    return result
```

## Connection & Authentication

### Local Emulator (Default)

```python
# No authentication required
taskhub = "default"
endpoint = "http://localhost:8080"
credential = None
secure_channel = False
```

### Azure with DefaultAzureCredential

```python
from azure.identity import DefaultAzureCredential

taskhub = "my-taskhub"
endpoint = "https://my-scheduler.region.durabletask.io"
credential = DefaultAzureCredential()
secure_channel = True
```

### Authentication Helper

```python
def get_connection_config():
    endpoint = os.getenv("ENDPOINT", "http://localhost:8080")
    taskhub = os.getenv("TASKHUB", "default")
    
    is_local = endpoint == "http://localhost:8080"
    
    return {
        "host_address": endpoint,
        "taskhub": taskhub,
        "secure_channel": not is_local,
        "token_credential": None if is_local else DefaultAzureCredential()
    }

config = get_connection_config()
worker = DurableTaskSchedulerWorker(**config)
client = DurableTaskSchedulerClient(**config)
```

## Local Development with Emulator

```bash
# Pull and run the emulator
docker pull mcr.microsoft.com/dts/dts-emulator:latest
docker run -d -p 8080:8080 -p 8082:8082 --name dts-emulator mcr.microsoft.com/dts/dts-emulator:latest

# Dashboard available at http://localhost:8082
```

## Client Operations

```python
# Schedule new orchestration
instance_id = client.schedule_new_orchestration(my_orchestration, input="data")

# Schedule with custom instance ID
instance_id = client.schedule_new_orchestration(
    my_orchestration, 
    input="data",
    instance_id="my-custom-id"
)

# Wait for completion
state = client.wait_for_orchestration_completion(instance_id, timeout=60)

# Get current status
state = client.get_orchestration_state(instance_id)

# Raise external event
client.raise_orchestration_event(instance_id, "approval_received", data=approval_data)

# Terminate orchestration
client.terminate_orchestration(instance_id, reason="User cancelled")

# Suspend/Resume
client.suspend_orchestration(instance_id, reason="Pausing for maintenance")
client.resume_orchestration(instance_id, reason="Resuming operation")
```

## References

- **[patterns.md](references/patterns.md)** - Detailed pattern implementations (Fan-Out/Fan-In, Human Interaction, Entities, Sub-Orchestrations)
- **[setup.md](references/setup.md)** - Azure Durable Task Scheduler provisioning and deployment
