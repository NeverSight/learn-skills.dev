---
name: ministack-aws-emulator
description: MiniStack is a free, open-source local AWS emulator (LocalStack replacement) that emulates 25+ AWS services on a single port with no account or license required.
triggers:
  - "set up local AWS emulator"
  - "replace LocalStack with free alternative"
  - "emulate AWS services locally"
  - "test boto3 code locally without AWS"
  - "run DynamoDB S3 Lambda locally"
  - "ministack local development"
  - "mock AWS services for testing"
  - "local AWS endpoint for CI/CD"
---

# MiniStack AWS Emulator

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

MiniStack is a free, MIT-licensed drop-in replacement for LocalStack that emulates 25+ AWS services (S3, SQS, DynamoDB, Lambda, SNS, IAM, STS, Kinesis, EventBridge, SecretsManager, SSM, CloudWatch, SES, and more) on a single port (`4566`). No account, no API key, no telemetry. Works with `boto3`, AWS CLI, Terraform, CDK, and any SDK.

---

## Installation

### Option 1: PyPI (simplest)
```bash
pip install ministack
ministack
# Server runs at http://localhost:4566
# Change port: GATEWAY_PORT=5000 ministack
```

### Option 2: Docker Hub
```bash
docker run -p 4566:4566 nahuelnucera/ministack
```

### Option 3: Docker Compose (from source)
```bash
git clone https://github.com/Nahuel990/ministack
cd ministack
docker compose up -d
```

### Verify it's running
```bash
curl http://localhost:4566/_localstack/health
```

---

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `GATEWAY_PORT` | `4566` | Port to listen on |
| `S3_PERSIST` | `0` | Set to `1` to persist S3 data to disk |

---

## AWS CLI Usage

```bash
# Set credentials (any non-empty values work)
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

# S3
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-bucket
aws --endpoint-url=http://localhost:4566 s3 cp ./file.txt s3://my-bucket/
aws --endpoint-url=http://localhost:4566 s3 ls s3://my-bucket

# SQS
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name my-queue
aws --endpoint-url=http://localhost:4566 sqs list-queues

# DynamoDB
aws --endpoint-url=http://localhost:4566 dynamodb list-tables
aws --endpoint-url=http://localhost:4566 dynamodb create-table \
  --table-name Users \
  --attribute-definitions AttributeName=userId,AttributeType=S \
  --key-schema AttributeName=userId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# STS (identity check)
aws --endpoint-url=http://localhost:4566 sts get-caller-identity

# Use a named profile instead
aws configure --profile local
# Enter: test / test / us-east-1 / json
aws --profile local --endpoint-url=http://localhost:4566 s3 ls
```

### awslocal wrapper (from source)
```bash
chmod +x bin/awslocal
./bin/awslocal s3 ls
./bin/awslocal dynamodb list-tables
```

---

## boto3 Usage Patterns

### Universal client factory
```python
import boto3

ENDPOINT = "http://localhost:4566"

def aws_client(service: str):
    return boto3.client(
        service,
        endpoint_url=ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

def aws_resource(service: str):
    return boto3.resource(
        service,
        endpoint_url=ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )
```

### S3
```python
s3 = aws_client("s3")

# Create bucket and upload
s3.create_bucket(Bucket="my-bucket")
s3.put_object(Bucket="my-bucket", Key="hello.txt", Body=b"Hello, MiniStack!")

# Download
obj = s3.get_object(Bucket="my-bucket", Key="hello.txt")
print(obj["Body"].read())  # b'Hello, MiniStack!'

# List objects
response = s3.list_objects_v2(Bucket="my-bucket")
for item in response.get("Contents", []):
    print(item["Key"])

# Copy object
s3.copy_object(
    Bucket="my-bucket",
    CopySource={"Bucket": "my-bucket", "Key": "hello.txt"},
    Key="hello-copy.txt",
)

# Enable versioning
s3.put_bucket_versioning(
    Bucket="my-bucket",
    VersioningConfiguration={"Status": "Enabled"},
)

# Presigned URL (works locally)
url = s3.generate_presigned_url(
    "get_object",
    Params={"Bucket": "my-bucket", "Key": "hello.txt"},
    ExpiresIn=3600,
)
```

### SQS
```python
sqs = aws_client("sqs")

# Standard queue
queue = sqs.create_queue(QueueName="my-queue")
queue_url = queue["QueueUrl"]

sqs.send_message(QueueUrl=queue_url, MessageBody='{"event": "user_signup"}')

messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
for msg in messages.get("Messages", []):
    print(msg["Body"])
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"])

# FIFO queue
fifo = sqs.create_queue(
    QueueName="my-queue.fifo",
    Attributes={"FifoQueue": "true", "ContentBasedDeduplication": "true"},
)

# Dead-letter queue setup
dlq = sqs.create_queue(QueueName="my-dlq")
dlq_attrs = sqs.get_queue_attributes(
    QueueUrl=dlq["QueueUrl"], AttributeNames=["QueueArn"]
)
sqs.set_queue_attributes(
    QueueUrl=queue_url,
    Attributes={
        "RedrivePolicy": json.dumps({
            "deadLetterTargetArn": dlq_attrs["Attributes"]["QueueArn"],
            "maxReceiveCount": "3",
        })
    },
)
```

### DynamoDB
```python
import json
ddb = aws_client("dynamodb")

# Create table
ddb.create_table(
    TableName="Users",
    KeySchema=[
        {"AttributeName": "userId", "KeyType": "HASH"},
        {"AttributeName": "createdAt", "KeyType": "RANGE"},
    ],
    AttributeDefinitions=[
        {"AttributeName": "userId", "AttributeType": "S"},
        {"AttributeName": "createdAt", "AttributeType": "N"},
    ],
    BillingMode="PAY_PER_REQUEST",
)

# Put / Get / Delete
ddb.put_item(
    TableName="Users",
    Item={
        "userId": {"S": "u1"},
        "createdAt": {"N": "1700000000"},
        "name": {"S": "Alice"},
        "active": {"BOOL": True},
    },
)

item = ddb.get_item(
    TableName="Users",
    Key={"userId": {"S": "u1"}, "createdAt": {"N": "1700000000"}},
)
print(item["Item"]["name"]["S"])  # Alice

# Query
result = ddb.query(
    TableName="Users",
    KeyConditionExpression="userId = :uid",
    ExpressionAttributeValues={":uid": {"S": "u1"}},
)

# Batch write
ddb.batch_write_item(
    RequestItems={
        "Users": [
            {"PutRequest": {"Item": {"userId": {"S": "u2"}, "createdAt": {"N": "1700000001"}, "name": {"S": "Bob"}}}},
        ]
    }
)

# TTL
ddb.update_time_to_live(
    TableName="Users",
    TimeToLiveSpecification={"Enabled": True, "AttributeName": "expiresAt"},
)
```

### SNS + SQS Fanout
```python
sns = aws_client("sns")
sqs = aws_client("sqs")

topic = sns.create_topic(Name="my-topic")
topic_arn = topic["TopicArn"]

queue = sqs.create_queue(QueueName="fan-queue")
queue_attrs = sqs.get_queue_attributes(
    QueueUrl=queue["QueueUrl"], AttributeNames=["QueueArn"]
)
queue_arn = queue_attrs["Attributes"]["QueueArn"]

sns.subscribe(TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_arn)

# Publish — message is fanned out to subscribed SQS queues
sns.publish(TopicArn=topic_arn, Message="hello fanout", Subject="test")
```

### Lambda
```python
import zipfile, io

# Create a zip with handler code
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as zf:
    zf.writestr("handler.py", """
def handler(event, context):
    print("event:", event)
    return {"statusCode": 200, "body": "ok"}
""")
buf.seek(0)

lam = aws_client("lambda")

lam.create_function(
    FunctionName="my-function",
    Runtime="python3.12",
    Role="arn:aws:iam::000000000000:role/role",
    Handler="handler.handler",
    Code={"ZipFile": buf.read()},
)

# Invoke synchronously
import json
response = lam.invoke(
    FunctionName="my-function",
    InvocationType="RequestResponse",
    Payload=json.dumps({"key": "value"}),
)
result = json.loads(response["Payload"].read())
print(result)  # {"statusCode": 200, "body": "ok"}

# SQS event source mapping
lam.create_event_source_mapping(
    EventSourceArn=queue_arn,
    FunctionName="my-function",
    BatchSize=10,
    Enabled=True,
)
```

### SecretsManager
```python
sm = aws_client("secretsmanager")

sm.create_secret(Name="db-password", SecretString='{"password":"s3cr3t"}')
secret = sm.get_secret_value(SecretId="db-password")
print(secret["SecretString"])  # {"password":"s3cr3t"}

sm.update_secret(SecretId="db-password", SecretString='{"password":"newpass"}')
sm.delete_secret(SecretId="db-password", ForceDeleteWithoutRecovery=True)
```

### SSM Parameter Store
```python
ssm = aws_client("ssm")

ssm.put_parameter(Name="/app/db/host", Value="localhost", Type="String")
ssm.put_parameter(Name="/app/db/password", Value="secret", Type="SecureString")

param = ssm.get_parameter(Name="/app/db/host")
print(param["Parameter"]["Value"])  # localhost

# Fetch all params under a path
params = ssm.get_parameters_by_path(Path="/app/", Recursive=True)
for p in params["Parameters"]:
    print(p["Name"], p["Value"])
```

### Kinesis
```python
import base64

kin = aws_client("kinesis")

kin.create_stream(StreamName="events", ShardCount=1)
kin.put_record(StreamName="events", Data=b'{"event":"click"}', PartitionKey="user1")

# Get records
shards = kin.list_shards(StreamName="events")
shard_id = shards["Shards"][0]["ShardId"]

iterator = kin.get_shard_iterator(
    StreamName="events",
    ShardId=shard_id,
    ShardIteratorType="TRIM_HORIZON",
)
records = kin.get_records(ShardIterator=iterator["ShardIterator"])
for r in records["Records"]:
    print(base64.b64decode(r["Data"]))
```

### EventBridge
```python
eb = aws_client("events")

# Create a custom bus
eb.create_event_bus(Name="my-bus")

# Put a rule targeting a Lambda
eb.put_rule(
    Name="my-rule",
    EventBusName="my-bus",
    EventPattern='{"source": ["myapp"]}',
    State="ENABLED",
)
eb.put_targets(
    Rule="my-rule",
    EventBusName="my-bus",
    Targets=[{"Id": "1", "Arn": "arn:aws:lambda:us-east-1:000000000000:function:my-function"}],
)

# Emit an event (triggers Lambda target)
eb.put_events(Entries=[{
    "Source": "myapp",
    "DetailType": "UserSignup",
    "Detail": '{"userId": "123"}',
    "EventBusName": "my-bus",
}])
```

### CloudWatch Logs
```python
import time

logs = aws_client("logs")

logs.create_log_group(logGroupName="/app/service")
logs.create_log_stream(logGroupName="/app/service", logStreamName="stream-1")

logs.put_log_events(
    logGroupName="/app/service",
    logStreamName="stream-1",
    logEvents=[
        {"timestamp": int(time.time() * 1000), "message": "App started"},
        {"timestamp": int(time.time() * 1000), "message": "Request received"},
    ],
)

events = logs.get_log_events(
    logGroupName="/app/service",
    logStreamName="stream-1",
)
for e in events["events"]:
    print(e["message"])

# Filter with glob patterns (* and ?), AND terms, -exclusions
filtered = logs.filter_log_events(
    logGroupName="/app/service",
    filterPattern="Request*",
)
```

---

## Testing Patterns

### pytest fixture (recommended)
```python
import pytest
import boto3

MINISTACK_ENDPOINT = "http://localhost:4566"

@pytest.fixture(scope="session")
def aws_endpoint():
    return MINISTACK_ENDPOINT

@pytest.fixture
def s3_client(aws_endpoint):
    return boto3.client(
        "s3",
        endpoint_url=aws_endpoint,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

@pytest.fixture
def test_bucket(s3_client):
    bucket = "test-bucket"
    s3_client.create_bucket(Bucket=bucket)
    yield bucket
    # Cleanup
    objs = s3_client.list_objects_v2(Bucket=bucket).get("Contents", [])
    for obj in objs:
        s3_client.delete_object(Bucket=bucket, Key=obj["Key"])
    s3_client.delete_bucket(Bucket=bucket)

def test_upload_download(s3_client, test_bucket):
    s3_client.put_object(Bucket=test_bucket, Key="test.txt", Body=b"hello")
    resp = s3_client.get_object(Bucket=test_bucket, Key="test.txt")
    assert resp["Body"].read() == b"hello"
```

### GitHub Actions CI integration
```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      ministack:
        image: nahuelnucera/ministack
        ports:
          - 4566:4566
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest
        env:
          AWS_ACCESS_KEY_ID: test
          AWS_SECRET_ACCESS_KEY: test
          AWS_DEFAULT_REGION: us-east-1
          AWS_ENDPOINT_URL: http://localhost:4566
```

### Using AWS_ENDPOINT_URL env var (boto3 >= 1.28)
```python
import os
import boto3

# If AWS_ENDPOINT_URL is set, boto3 uses it automatically — no endpoint_url kwarg needed
# export AWS_ENDPOINT_URL=http://localhost:4566
s3 = boto3.client("s3")  # picks up AWS_ENDPOINT_URL automatically
```

---

## Supported Services (25+)

| Service | Key Operations |
|---|---|
| S3 | CRUD, multipart, versioning, encryption, lifecycle, CORS, ACL, notifications |
| SQS | Standard & FIFO queues, DLQ, batch ops |
| SNS | Topics, subscriptions, fanout to SQS/Lambda, platform endpoints |
| DynamoDB | Tables, CRUD, Query, Scan, TTL, transactions, batch ops |
| Lambda | Python runtimes, invoke, SQS event sources, Function URLs |
| IAM | Users, roles, policies, groups, instance profiles, OIDC |
| STS | GetCallerIdentity, AssumeRole, GetSessionToken |
| SecretsManager | Full CRUD, rotation, versioning |
| SSM Parameter Store | String, SecureString, StringList, path queries |
| EventBridge | Buses, rules, targets, Lambda dispatch |
| Kinesis | Streams, shards, records, iterators |
| CloudWatch Metrics | PutMetricData, alarms, dashboards, CBOR protocol |
| CloudWatch Logs | Log groups/streams, filter with globs, metric filters |
| SES | Send email, templates, configuration sets |
| Step Functions | State machine CRUD |
| RDS | Spins up real Postgres/MySQL containers |
| ElastiCache | Spins up real Redis containers |
| Athena | Real SQL via DuckDB |
| ECS | Real Docker containers |

---

## Troubleshooting

**Connection refused on port 4566**
```bash
# Check if ministack is running
curl http://localhost:4566/_localstack/health
# Start it
ministack
# or
docker run -p 4566:4566 nahuelnucera/ministack
```

**`NoCredentialsError` from boto3**
```bash
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
# Any non-empty values work — MiniStack doesn't validate credentials
```

**`InvalidSignatureException`**
- This is usually a region mismatch. Ensure `region_name="us-east-1"` matches across all clients.

**Lambda function not found after create**
- MiniStack executes Python runtimes with a warm worker pool. Wait briefly or invoke with `InvocationType="Event"` for async.

**S3 data lost on restart**
```bash
# Enable persistence
S3_PERSIST=1 ministack
# or in Docker
docker run -p 4566:4566 -e S3_PERSIST=1 -v $(pwd)/data:/data nahuelnucera/ministack
```

**Port conflict**
```bash
GATEWAY_PORT=5000 ministack
# Then use http://localhost:5000 as endpoint
```

**Migrating from LocalStack**
- Replace all `http://localhost:4566` endpoint URLs — they stay the same.
- Remove `LOCALSTACK_AUTH_TOKEN` / `LOCALSTACK_API_KEY` env vars (not needed).
- Replace `localstack/localstack` Docker image with `nahuelnucera/ministack`.
- All `boto3` client code works without modification.
