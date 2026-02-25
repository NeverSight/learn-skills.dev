---
name: gcp-pubsub
description: |
  Implements Google Cloud Pub/Sub integration in Python by configuring topics, subscriptions,
  publishing/subscribing, dead letter queues, and local emulator setup. Use when building
  event-driven architectures, implementing message queuing, or managing high-throughput systems.
  Triggers on "setup Pub/Sub", "publish messages", "create subscription", "configure DLQ",
  or "test with emulator". Works with google-cloud-pubsub library and includes reliability,
  idempotency, and testing patterns.

---

# Google Cloud Pub/Sub

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Requirements](#requirements)
- [See Also](#see-also)

## Purpose

Build robust, production-ready event-driven systems using Google Cloud Pub/Sub with Python. Covers setup, publishing, subscribing, error handling, dead letter queues, and local development with the emulator.

## When to Use

Use this skill when you need to:
- Build event-driven architectures with message-based communication
- Implement reliable message queuing between services
- Handle at-least-once message delivery guarantees
- Manage high-throughput message systems (1000+ msgs/sec)
- Configure local development with Pub/Sub emulator
- Implement dead letter queues for failed message handling

## Quick Start

**Install and authenticate:**

```bash
pip install google-cloud-pubsub
gcloud auth application-default login
python -c "from google.cloud import pubsub_v1; print('Ready')"
```

**Publish a message:**

```python
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("my-project", "my-topic")

# Create topic
try:
    publisher.create_topic(request={"name": topic_path})
except Exception as e:
    if "ALREADY_EXISTS" not in str(e):
        raise

# Publish
future = publisher.publish(topic_path, b"Hello, World!")
print(f"Published: {future.result()}")
```

**Subscribe to messages:**

```python
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("my-project", "my-subscription")

def callback(message):
    print(f"Received: {message.data.decode()}")
    message.ack()

future = subscriber.subscribe(subscription_path, callback=callback)

try:
    future.result(timeout=30)
except Exception:
    future.cancel()
```

## Instructions

### Step 1: Set Up Development Environment

Install dependencies and configure authentication:

```bash
pip install google-cloud-pubsub
gcloud auth application-default login
```

For production, use service account:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### Step 2: Create Topics and Subscriptions

```python
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# Create topic
topic_path = publisher.topic_path("my-project", "my-topic")
publisher.create_topic(request={"name": topic_path})

# Create subscription
subscription_path = subscriber.subscription_path("my-project", "my-subscription")
subscription_config = {
    "name": subscription_path,
    "topic": topic_path,
    "ack_deadline_seconds": 60,
}
subscriber.create_subscription(request=subscription_config)
```

See [references/detailed-guide.md](./references/detailed-guide.md) for advanced configuration options.

### Step 3: Publish Messages

**Simple publishing:**

```python
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("my-project", "my-topic")

future = publisher.publish(topic_path, b"Message data")
message_id = future.result()
```

**Publish with attributes:**

```python
import json

data = json.dumps({"event": "user.created", "user_id": "123"}).encode()
future = publisher.publish(
    topic_path,
    data,
    event_type="user.created",
    timestamp="2024-01-15T10:30:00Z"
)
```

See [references/detailed-guide.md](./references/detailed-guide.md) for production-ready publisher with batching and error handling.

### Step 4: Subscribe to Messages

**Basic subscriber:**

```python
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("my-project", "my-subscription")

def callback(message):
    try:
        print(f"Received: {message.data.decode()}")
        # Process message
        message.ack()
    except Exception as e:
        print(f"Error: {e}")
        message.nack()  # Will be redelivered

future = subscriber.subscribe(subscription_path, callback=callback)

try:
    future.result()  # Block indefinitely
except KeyboardInterrupt:
    future.cancel()
```

**With flow control:**

```python
future = subscriber.subscribe(
    subscription_path,
    callback=callback,
    flow_control=pubsub_v1.types.FlowControl(
        max_messages=100,
        max_bytes=100 * 1024 * 1024,  # 100 MB
    ),
)
```

See [references/detailed-guide.md](./references/detailed-guide.md) for production subscriber with monitoring.

### Step 5: Configure Dead Letter Queue

```python
from google.cloud import pubsub_v1
from google.protobuf.duration_pb2 import Duration

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# Create dead letter topic
dlq_topic_path = publisher.topic_path("my-project", "my-topic-dlq")
publisher.create_topic(request={"name": dlq_topic_path})

# Create subscription with DLQ
subscription_path = subscriber.subscription_path("my-project", "my-subscription")
subscription = pubsub_v1.types.Subscription(
    name=subscription_path,
    topic=publisher.topic_path("my-project", "my-topic"),
    dead_letter_policy=pubsub_v1.types.DeadLetterPolicy(
        dead_letter_topic=dlq_topic_path,
        max_delivery_attempts=5,
    ),
    retry_policy=pubsub_v1.types.RetryPolicy(
        minimum_backoff=Duration(seconds=10),
        maximum_backoff=Duration(seconds=600),
    ),
)
subscriber.create_subscription(request=subscription)
```

See [references/detailed-guide.md](./references/detailed-guide.md) for complete DLQ setup with monitoring.

### Step 6: Implement Idempotency

Track processed messages to avoid duplicate processing:

```python
class IdempotentProcessor:
    def __init__(self):
        self.processed_ids = set()

    def process(self, message):
        msg_id = message.message_id

        if msg_id in self.processed_ids:
            print(f"Already processed: {msg_id}")
            message.ack()
            return

        try:
            # Process message
            print(f"Processing: {message.data.decode()}")
            self.processed_ids.add(msg_id)
            message.ack()
        except Exception as e:
            print(f"Failed: {e}")
            message.nack()
```

See [references/detailed-guide.md](./references/detailed-guide.md) for production-ready idempotency patterns.

### Step 7: Local Development with Emulator

```bash
# Install and start emulator
gcloud components install pubsub-emulator
gcloud beta emulators pubsub start

# In another terminal
export PUBSUB_EMULATOR_HOST=localhost:8085
python your_script.py  # Uses emulator automatically
```

See [references/detailed-guide.md](./references/detailed-guide.md) for emulator configuration patterns.

### Step 8: Monitor Operations

Enable logging and track metrics:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Query subscription stats
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("my-project", "my-subscription")
subscription = subscriber.get_subscription(request={"subscription": subscription_path})

print(f"Topic: {subscription.topic}")
print(f"Ack deadline: {subscription.ack_deadline_seconds}s")
```

See [references/detailed-guide.md](./references/detailed-guide.md) for comprehensive monitoring patterns.

## Requirements

- **Python:** 3.7+
- **Dependencies:**
  ```bash
  pip install google-cloud-pubsub>=2.18.0
  ```
- **GCP Project:** Active project with Pub/Sub API enabled
- **Authentication:** Application Default Credentials or service account key
- **IAM Permissions:**
  - `roles/pubsub.publisher` - Publish messages
  - `roles/pubsub.subscriber` - Subscribe to messages
  - `roles/pubsub.admin` - Create/delete topics and subscriptions
- **For Local Development:**
  ```bash
  gcloud components install pubsub-emulator
  ```

## See Also

- [references/detailed-guide.md](./references/detailed-guide.md) - Comprehensive implementation guide with production patterns
- [examples/examples.md](./examples/examples.md) - Working code examples including async patterns and testing
- [scripts/setup_emulator.sh](./scripts/setup_emulator.sh) - Emulator setup utility
- [scripts/pubsub_utils.py](./scripts/pubsub_utils.py) - Helper utilities for common operations
