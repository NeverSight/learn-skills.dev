---
name: Oracle AI Architect
description: Extended reference material for Oracle AI architecture with deep technical implementations
version: 1.0.0
---

# Oracle AI Architect - Extended Reference

## Purpose
Comprehensive implementation reference for Oracle AI Architects building enterprise AI solutions. Covers OCI Generative AI APIs, Database 26ai Vector Search, Select AI, NVIDIA NIM deployment, and multi-agent patterns with Oracle ADK.

This document provides extended reference material for the Oracle AI Architect skill.

## OCI Generative AI API Examples

### Chat Completion
```python
import oci
from oci.generative_ai_inference import GenerativeAiInferenceClient
from oci.generative_ai_inference.models import (
    ChatDetails,
    CohereChatRequest,
    OnDemandServingMode
)

config = oci.config.from_file()
client = GenerativeAiInferenceClient(config)

chat_request = CohereChatRequest(
    message="Explain Oracle AI Vector Search",
    max_tokens=500,
    temperature=0.7
)

response = client.chat(
    chat_details=ChatDetails(
        compartment_id=compartment_id,
        serving_mode=OnDemandServingMode(model_id="cohere.command-a"),
        chat_request=chat_request
    )
)

print(response.data.chat_response.text)
```

### Embeddings
```python
from oci.generative_ai_inference.models import (
    EmbedTextDetails,
    OnDemandServingMode
)

embed_request = EmbedTextDetails(
    inputs=["Document text to embed"],
    serving_mode=OnDemandServingMode(model_id="cohere.embed-english-v3.0"),
    compartment_id=compartment_id
)

response = client.embed_text(embed_request)
embeddings = response.data.embeddings
```

## Database 26ai AI Vector Search Examples

### Creating Vector Tables
```sql
-- Basic vector column
CREATE TABLE docs (
    id NUMBER GENERATED ALWAYS AS IDENTITY,
    content CLOB,
    embedding VECTOR(1536, FLOAT32),
    CONSTRAINT docs_pk PRIMARY KEY (id)
);

-- With automatic embedding generation
CREATE TABLE smart_docs (
    id NUMBER GENERATED ALWAYS AS IDENTITY,
    content CLOB,
    embedding VECTOR GENERATED ALWAYS AS (
        VECTOR_EMBEDDING(content USING 'doc-embed-model')
    ) VIRTUAL
);
```

### Vector Search Queries
```sql
-- Cosine similarity search
SELECT id, content,
       VECTOR_DISTANCE(embedding, :query_vec, COSINE) AS distance
FROM docs
WHERE VECTOR_DISTANCE(embedding, :query_vec, COSINE) < 0.3
ORDER BY distance
FETCH FIRST 10 ROWS ONLY;

-- Euclidean distance
SELECT id, content
FROM docs
ORDER BY VECTOR_DISTANCE(embedding, :query_vec, EUCLIDEAN)
FETCH FIRST 5 ROWS ONLY;

-- Dot product (for normalized vectors)
SELECT id, content
FROM docs
ORDER BY VECTOR_DISTANCE(embedding, :query_vec, DOT) DESC
FETCH FIRST 5 ROWS ONLY;
```

### Hybrid Search (Vector + Traditional)
```sql
-- Combine vector similarity with filters
SELECT id, content,
       VECTOR_DISTANCE(embedding, :query_vec, COSINE) AS semantic_score
FROM docs
WHERE category = 'technical'
  AND created_date > SYSDATE - 30
ORDER BY semantic_score
FETCH FIRST 10 ROWS ONLY;
```

## Select AI Configuration

### Setup
```sql
-- Enable Select AI for a schema
BEGIN
    DBMS_CLOUD_AI.CREATE_PROFILE(
        profile_name => 'GENAI_PROFILE',
        attributes => JSON('{
            "provider": "oci",
            "credential_name": "OCI_CRED",
            "model": "cohere.command-a",
            "object_list": [
                {"owner": "SALES", "name": "CUSTOMERS"},
                {"owner": "SALES", "name": "ORDERS"},
                {"owner": "SALES", "name": "PRODUCTS"}
            ]
        }')
    );
END;
/

-- Set as default
BEGIN
    DBMS_CLOUD_AI.SET_PROFILE('GENAI_PROFILE');
END;
/
```

### Natural Language Queries
```sql
-- Simple query
SELECT AI 'Show me top 10 customers by revenue';

-- Complex analysis
SELECT AI 'What is the month-over-month growth rate for each product category?';

-- With context
SELECT AI 'Compare Q3 and Q4 sales performance by region,
           highlighting regions with declining trends';
```

## NVIDIA NIM Deployment on OCI

### Terraform Configuration
```hcl
# NVIDIA NIM deployment on OCI
resource "oci_core_instance" "nim_instance" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  compartment_id      = var.compartment_id
  display_name        = "nvidia-nim-inference"
  shape               = "BM.GPU.H100.8"  # 8x H100 GPUs

  source_details {
    source_type = "image"
    source_id   = var.nvidia_image_ocid
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key
    user_data = base64encode(templatefile("nim-setup.sh", {
      nim_model = var.nim_model_name
    }))
  }
}
```

### NIM API Usage
```python
import requests

NIM_ENDPOINT = "http://nim-instance:8000/v1"

# Chat completion
response = requests.post(
    f"{NIM_ENDPOINT}/chat/completions",
    json={
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {"role": "user", "content": "Explain RAG architecture"}
        ],
        "max_tokens": 500
    }
)

# Embeddings
response = requests.post(
    f"{NIM_ENDPOINT}/embeddings",
    json={
        "model": "nvidia/nv-embedqa-e5-v5",
        "input": ["Text to embed"]
    }
)
```

## AI Data Platform Workbench Examples

### Spark Data Processing
```python
from pyspark.sql import SparkSession
from oci.ai_data_platform import AIDataPlatformClient

spark = SparkSession.builder \
    .appName("AIDP Processing") \
    .config("spark.oracle.datasource.enabled", "true") \
    .getOrCreate()

# Read from bronze layer (Object Storage)
raw_df = spark.read.parquet("oci://bronze-bucket@namespace/raw-data/")

# Transform to silver
cleaned_df = raw_df \
    .dropDuplicates() \
    .filter("quality_score > 0.8") \
    .withColumn("processed_date", current_timestamp())

# Write to silver layer
cleaned_df.write \
    .mode("overwrite") \
    .parquet("oci://silver-bucket@namespace/cleaned-data/")

# Load to gold (Autonomous DB)
cleaned_df.write \
    .format("oracle") \
    .option("adbId", adb_ocid) \
    .option("user", "ADMIN") \
    .option("password", password) \
    .option("dbtable", "GOLD.PROCESSED_DATA") \
    .save()
```

## Oracle ADK Complete Example

### Multi-Agent Sales Assistant
```python
from oci_adk import Agent, FunctionTool, Workflow, Step
import oci

# Initialize OCI config
config = oci.config.from_file()

# Define tools
@FunctionTool(
    name="query_sales_data",
    description="Query sales data from Autonomous Database",
    parameters={
        "query_type": {"type": "string", "enum": ["revenue", "orders", "customers"]},
        "time_period": {"type": "string"},
        "region": {"type": "string", "required": False}
    }
)
def query_sales_data(query_type: str, time_period: str, region: str = None):
    # ADB connection and query logic
    return execute_adb_query(query_type, time_period, region)

@FunctionTool(
    name="generate_report",
    description="Generate formatted report from analysis",
    parameters={
        "data": {"type": "object"},
        "format": {"type": "string", "enum": ["summary", "detailed", "executive"]}
    }
)
def generate_report(data: dict, format: str):
    return format_report(data, format)

# Create specialized agents
data_analyst = Agent(
    name="data_analyst",
    model="cohere.command-a",
    system_prompt="""You are a data analyst specializing in sales analytics.
    Query the database to gather relevant data for analysis requests.""",
    tools=[query_sales_data],
    oci_config=config
)

report_writer = Agent(
    name="report_writer",
    model="cohere.command-a",
    system_prompt="""You are a business report writer.
    Create clear, actionable reports from data analysis.""",
    tools=[generate_report],
    oci_config=config
)

# Create orchestrated workflow
sales_workflow = Workflow([
    Step("analyze", data_analyst),
    Step("report", report_writer)
])

# Execute
result = sales_workflow.execute(
    "Analyze Q4 sales performance by region and create an executive summary"
)
print(result.output)
```

## Cost Optimization Strategies

### Model Selection by Use Case
| Use Case | Recommended Model | Cost Tier |
|----------|-------------------|-----------|
| Simple chat | Cohere Command Light | $ |
| Complex reasoning | Cohere Command A | $$ |
| Fine-tuned tasks | Llama 3.3 + LoRA | $$ |
| Embeddings | Cohere Embed 4 | $ |
| Private inference | NVIDIA NIM | $$$ |

### Caching Strategy
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=10000)
def cached_embedding(text_hash: str):
    """Cache embeddings to reduce API calls"""
    return generate_embedding(text)

def get_embedding(text: str):
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    return cached_embedding(text_hash)
```

### Reserved Capacity
```hcl
# Terraform for reserved GPU capacity
resource "oci_core_compute_capacity_reservation" "gpu_reservation" {
  compartment_id = var.compartment_id
  availability_domain = var.ad

  instance_reservation_configs {
    instance_shape = "BM.GPU.H100.8"
    reserved_count = 2
  }
}
```

## Security Best Practices

### IAM Policies for AI Services
```
# Allow data scientists to use Generative AI
Allow group DataScientists to use generative-ai-family in compartment AI-Workloads

# Allow agents to access database
Allow dynamic-group AgentInstances to use autonomous-database-family in compartment Data

# Allow NIM instances to read model storage
Allow dynamic-group NIMInstances to read object-family in compartment Models
```

### Data Encryption
```python
# Use OCI Vault for API keys
from oci.secrets import SecretsClient

secrets_client = SecretsClient(config)
secret = secrets_client.get_secret_bundle(secret_id=vault_secret_ocid)
api_key = base64.b64decode(secret.data.secret_bundle_content.content)
```

## Monitoring and Observability

### Metrics to Track
```python
# Custom metrics for AI workloads
from oci.monitoring import MonitoringClient

def post_ai_metrics(agent_id: str, metrics: dict):
    monitoring_client.post_metric_data(
        post_metric_data_details={
            "metric_data": [{
                "namespace": "ai_agents",
                "compartment_id": compartment_id,
                "name": "inference_latency",
                "dimensions": {"agent_id": agent_id},
                "datapoints": [{"timestamp": now, "value": metrics["latency_ms"]}]
            }, {
                "namespace": "ai_agents",
                "name": "tokens_used",
                "dimensions": {"agent_id": agent_id},
                "datapoints": [{"timestamp": now, "value": metrics["tokens"]}]
            }]
        }
    )
```

### Logging
```python
import oci.loggingingestion

def log_agent_action(agent_id: str, action: str, result: str):
    logging_client.put_logs(
        log_id=log_ocid,
        put_logs_details={
            "specversion": "1.0",
            "log_entry_batches": [{
                "entries": [{
                    "data": json.dumps({
                        "agent_id": agent_id,
                        "action": action,
                        "result": result,
                        "timestamp": datetime.utcnow().isoformat()
                    }),
                    "id": str(uuid.uuid4())
                }]
            }]
        }
    )
```

## Resources

**Official Documentation:**
- [OCI Generative AI](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm)
- [Database 26ai AI Vector Search](https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/)
- [Select AI](https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/sql-generation-ai-autonomous.html)
- [Oracle ADK](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/adk/)

**Tutorials:**
- [Getting Started with OCI GenAI](https://docs.oracle.com/en-us/iaas/Content/generative-ai/getting-started.htm)
- [Vector Search Quick Start](https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/get-started-oracle-ai-vector-search.html)

---

*Deep technical implementations for Oracle AI Architects building enterprise-scale solutions.*

---

## Quality Checklist

Before deploying AI solutions:

**Vector Search:**
- [ ] Appropriate embedding model selected
- [ ] Vector dimension matches model output
- [ ] Index created for large datasets
- [ ] Hybrid search considered (vector + filters)

**Select AI:**
- [ ] Profile configured with correct tables
- [ ] Sensitive columns excluded
- [ ] Query validation enabled
- [ ] Audit logging active

**GenAI Integration:**
- [ ] Model selection matches use case complexity
- [ ] Token limits configured
- [ ] Caching implemented for repeated queries
- [ ] Cost monitoring enabled

**RAG Pipeline:**
- [ ] Chunking strategy appropriate for content
- [ ] Embedding quality validated
- [ ] Retrieval accuracy tested
- [ ] Hallucination mitigation in place
