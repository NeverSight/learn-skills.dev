---
name: opensearch-best-practices
description: OpenSearch development best practices for indexing, querying, search optimization, vector search, and cluster management
---

# OpenSearch Best Practices

## Core Principles

- Design indices and mappings based on query patterns
- Optimize for search performance with proper analysis and indexing
- Use appropriate shard sizing and cluster configuration
- Implement proper security with the OpenSearch Security plugin
- Monitor cluster health with Performance Analyzer and optimize queries
- Leverage OpenSearch-specific features: k-NN vector search, neural search, search pipelines, ISM

## Index Design

### Mapping Best Practices

- Define explicit mappings instead of relying on dynamic mapping
- Use appropriate data types for each field
- Disable indexing for fields you do not search on
- Use keyword type for exact matches, text for full-text search

```json
{
  "mappings": {
    "properties": {
      "product_id": {
        "type": "keyword"
      },
      "name": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "description": {
        "type": "text",
        "analyzer": "english"
      },
      "price": {
        "type": "scaled_float",
        "scaling_factor": 100
      },
      "category": {
        "type": "keyword"
      },
      "tags": {
        "type": "keyword"
      },
      "created_at": {
        "type": "date"
      },
      "metadata": {
        "type": "object",
        "enabled": false
      },
      "location": {
        "type": "geo_point"
      }
    }
  }
}
```

### Field Types

- `keyword`: Exact values, filtering, aggregations, sorting
- `text`: Full-text search with analysis
- `date`: Date/time values with format specification
- `numeric types`: long, integer, short, byte, double, float, scaled_float
- `boolean`: True/false values
- `geo_point`: Latitude/longitude pairs
- `nested`: Arrays of objects that need independent querying
- `knn_vector`: Vector embeddings for k-NN similarity search (OpenSearch-specific)

### Index Settings

```json
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "refresh_interval": "30s",
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding", "synonym_filter"]
        }
      },
      "filter": {
        "synonym_filter": {
          "type": "synonym",
          "synonyms": ["laptop, notebook", "phone, mobile, smartphone"]
        }
      }
    }
  }
}
```

## Shard Sizing

### Guidelines

- Target 10-50GB per shard (sweet spot is 10-30GB)
- Avoid oversharding (too many small shards)
- Consider time-based indices for time-series data
- Use segment replication (`replication.type: SEGMENT`) for improved indexing throughput on replicas

```json
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  }
}
```

### Index State Management (ISM)

OpenSearch uses ISM (Index State Management) instead of Elasticsearch's ILM. ISM uses a flexible state machine model where any state can transition to any other state.

Create an ISM policy via:
```
PUT _plugins/_ism/policies/<policy_id>
```

```json
{
  "policy": {
    "description": "Hot-warm-delete lifecycle",
    "default_state": "hot",
    "ism_template": [
      {
        "index_patterns": ["logs-*"],
        "priority": 100
      }
    ],
    "states": [
      {
        "name": "hot",
        "actions": [
          {
            "rollover": {
              "min_size": "50gb",
              "min_index_age": "7d"
            }
          }
        ],
        "transitions": [
          {
            "state_name": "warm",
            "conditions": {
              "min_index_age": "30d"
            }
          }
        ]
      },
      {
        "name": "warm",
        "actions": [
          {
            "replica_count": {
              "number_of_replicas": 1
            }
          },
          {
            "force_merge": {
              "max_num_segments": 1
            }
          }
        ],
        "transitions": [
          {
            "state_name": "delete",
            "conditions": {
              "min_index_age": "90d"
            }
          }
        ]
      },
      {
        "name": "delete",
        "actions": [
          {
            "delete": {}
          }
        ],
        "transitions": []
      }
    ]
  }
}
```

### ISM Key Differences from Elasticsearch ILM

- ISM uses arbitrary **states** with explicit **transitions** (state machine), not linear phases
- Policy is attached via `ism_template` inside the policy itself (not via index template settings)
- API endpoint: `_plugins/_ism/policies/<id>` (not `_ilm/policy/<id>`)
- Transitions support `min_index_age`, `min_doc_count`, `min_size`, and `cron` conditions
- Available actions: `rollover`, `force_merge`, `shrink`, `delete`, `read_only`, `read_write`, `replica_count`, `index_priority`, `close`, `open`, `snapshot`, `allocation`, `notification`

### ISM Management APIs

```
PUT    _plugins/_ism/policies/<policy_id>       # Create/update policy
GET    _plugins/_ism/policies/<policy_id>       # Get policy
DELETE _plugins/_ism/policies/<policy_id>       # Delete policy
POST   _plugins/_ism/add/<index>                # Attach policy to existing index
POST   _plugins/_ism/remove/<index>             # Detach policy
GET    _plugins/_ism/explain/<index>            # Get ISM status for an index
POST   _plugins/_ism/retry/<index>              # Retry failed action
```

## Query Optimization

### Query Types

#### Match Query (Full-text search)

```json
{
  "query": {
    "match": {
      "description": {
        "query": "wireless bluetooth headphones",
        "operator": "and",
        "fuzziness": "AUTO"
      }
    }
  }
}
```

#### Term Query (Exact match)

```json
{
  "query": {
    "term": {
      "status": "active"
    }
  }
}
```

#### Bool Query (Combining queries)

```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "laptop" } }
      ],
      "filter": [
        { "term": { "category": "electronics" } },
        { "range": { "price": { "gte": 500, "lte": 2000 } } }
      ],
      "should": [
        { "term": { "brand": "apple" } }
      ],
      "must_not": [
        { "term": { "status": "discontinued" } }
      ]
    }
  }
}
```

### Query Best Practices

- Use `filter` context for non-scoring queries (cacheable)
- Use `must` only when scoring is needed
- Avoid wildcards at the beginning of terms
- Use `keyword` fields for exact matches
- Limit result size with `size` parameter

```json
{
  "query": {
    "bool": {
      "must": {
        "multi_match": {
          "query": "search terms",
          "fields": ["name^3", "description", "tags^2"],
          "type": "best_fields"
        }
      },
      "filter": [
        { "term": { "active": true } },
        { "range": { "created_at": { "gte": "now-30d" } } }
      ]
    }
  },
  "size": 20,
  "from": 0,
  "_source": ["name", "price", "category"]
}
```

## Vector Search (k-NN)

OpenSearch has a built-in k-NN plugin supporting two engines: **faiss** and **lucene**.

### k-NN Index Mapping

```json
PUT /my-vector-index
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param.ef_search": 100
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "faiss",
          "parameters": {
            "ef_construction": 256,
            "m": 16
          }
        }
      },
      "title": { "type": "text" },
      "category": { "type": "keyword" }
    }
  }
}
```

### Engine Selection

- **faiss**: Best for large-scale production. Supports HNSW and IVF. Additional quantization options (SQfp16, PQ). Recommended default.
- **lucene**: Native Lucene HNSW. Supports efficient pre-filtering. Built-in scalar quantization. Lower memory overhead. Good when filtering is critical or for smaller datasets.

### Space Types

- `l2` (Euclidean distance)
- `cosinesimil` (cosine similarity)
- `innerproduct` (dot product)
- `l1` (Manhattan distance)
- `linf` (L-infinity distance)

### k-NN Query

```json
GET /my-vector-index/_search
{
  "size": 10,
  "query": {
    "knn": {
      "my_vector": {
        "vector": [0.1, 0.2, 0.3],
        "k": 10
      }
    }
  }
}
```

### k-NN with Filtering

```json
GET /my-vector-index/_search
{
  "size": 10,
  "query": {
    "knn": {
      "my_vector": {
        "vector": [0.1, 0.2, 0.3],
        "k": 10,
        "filter": {
          "term": { "category": "electronics" }
        }
      }
    }
  }
}
```

With the **lucene** engine, filtering is applied as a pre-filter (efficient). With **faiss**, filtering is post-filter by default, which can return fewer than `k` results. Faiss supports efficient filtering starting in OpenSearch 2.9+.

### k-NN Best Practices

- Always set `"knn": true` in index settings
- Use **faiss** for large-scale production, **lucene** when pre-filtering is critical
- Higher `ef_search` (32-128 practical range) = better accuracy, slower queries. Can be adjusted dynamically per query.
- Higher `ef_construction` (128-256+) and `m` (16-128) = better recall but slower indexing and more memory
- Monitor `knn.memory.circuit_breaker.limit` -- k-NN graphs load into native off-heap memory. HNSW is dramatically faster when the entire graph resides in RAM.
- Warm up indices after creation: `GET /_plugins/_knn/warmup/{index}`
- Normalize vectors once during ingestion (not at query time) and use `innerproduct` for better performance
- Disable `_source` storage and `doc_values` on vector fields when unnecessary to reduce index size
- The final 1-2% of recall improvement typically costs disproportionately more than the first 95% -- define realistic recall targets
- Monitor end-to-end latency including embedding generation, metadata retrieval, and reranking -- not just the vector search component

### HNSW Hyperparameters

- **M** (maximum edges per node): Range 16-128. Lower values (16) for memory-constrained environments, higher values (128) for maximum recall. Memory consumption increases proportionally.
- **ef_construction** (index-time): Range 128-256+. Controls graph quality during insertion. Higher values produce better graphs but slower indexing.
- **ef_search** (query-time): Range 32-128. Can be tuned per query for balancing recall vs. response time.

### Vector Shard Sizing

- Target 10-30 million vectors per shard
- Shard count should equal or slightly exceed node count for maximum parallelism
- Over-sharding creates excessive coordination overhead that harms tail latency
- Under-sharding leaves performance on the table
- Adding replicas provides load balancing and smooths performance variations

### Quantization Strategies

**Scalar Quantization (SQ):**
- Lucene engine: built-in support
- Faiss engine: SQfp16 converts 32-bit to 16-bit, approximately 50% memory reduction

**Binary Quantization (BQ):**
- 1-bit compression provides 32x compression -- a 768-dimensional float32 vector shrinks from 3072 bytes to under 100 bytes
- No separate training step required
- Asymmetric distance computation (ADC) improves recall

**Product Quantization (PQ):**
- Most aggressive compression: up to 64x
- Faiss engine only, requires training step for IVF-based indexes
- Configuration: `code_size=8` with `m` tuned for desired balance
- More noticeable recall impact than SQ or BQ

### Disk-Based Vector Search

For cost-effective large-scale deployments, use `on_disk` mode with binary quantization:

```json
PUT /my-vector-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 768,
        "mode": "on_disk"
      }
    }
  }
}
```

- Approximately 97% memory reduction (e.g., 100M 768-dim vectors: from 300GB+ RAM to under 10GB)
- Two-phase approach: quantized index identifies candidates, full-precision vectors lazily loaded from disk for reranking
- P90 latency in the 100-200ms range (acceptable for many use cases)
- Cost reduction of roughly one-third compared to memory-optimized deployments
- Currently supports only float data type

### Concurrent Segment Search

Enable at cluster level for significant vector search latency improvements:

```json
PUT _cluster/settings
{
  "persistent": {
    "search.concurrent_segment_search.enabled": true
  }
}
```

- Benchmarked at 60%+ improvement in p90 service time, up to 75% reduction in p90 latency
- Best applied after force-merging segments
- Benefits diminish when compute cores are already saturated or search space per shard is small

### Scale-Specific Recommendations

**1-50M vectors:**
- Start with M=32, ef_construction=128
- Use batch inserts
- Ensure full RAM residency for the graph

**50-500M vectors:**
- Implement systematic sharding (10-30M vectors per shard)
- Enable scalar quantization
- Two-phase retrieval: compressed vectors for search, full precision for reranking
- Periodic index rebuilds for graph quality maintenance

**500M+ vectors:**
- Hierarchical retrieval (IVF-style centroid routing)
- Multi-tier hot/cold data architecture
- Aggressive quantization (IVF-PQ) for cold data
- Optimize query routing to avoid broadcast across all shards
- Return only IDs/scores in initial retrieval phases

## Neural Search and Hybrid Search

### Neural Search with ML Commons

Set up an ingest pipeline to automatically generate embeddings:

```json
PUT /_ingest/pipeline/neural-search-pipeline
{
  "description": "Pipeline for neural search",
  "processors": [
    {
      "text_embedding": {
        "model_id": "<model_id>",
        "field_map": {
          "title": "title_embedding"
        }
      }
    }
  ]
}
```

Query with automatic text-to-vector conversion:

```json
GET /my-index/_search
{
  "query": {
    "neural": {
      "title_embedding": {
        "query_text": "comfortable running shoes",
        "model_id": "<model_id>",
        "k": 10
      }
    }
  }
}
```

### Hybrid Search (BM25 + k-NN) with Search Pipelines

Create a normalization pipeline:

```json
PUT /_search/pipeline/hybrid-pipeline
{
  "description": "Hybrid search pipeline",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean",
          "parameters": {
            "weights": [0.3, 0.7]
          }
        }
      }
    }
  ]
}
```

Execute a hybrid query combining lexical and vector search:

```json
GET /my-index/_search?search_pipeline=hybrid-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "title": "wireless headphones"
          }
        },
        {
          "knn": {
            "my_vector": {
              "vector": [0.1, 0.2, 0.3],
              "k": 10
            }
          }
        }
      ]
    }
  }
}
```

### ML Commons Best Practices

- Use remote model connectors (Amazon Bedrock, SageMaker, OpenAI, Cohere) for large models
- Set `plugins.ml_commons.only_run_on_ml_node: true` in production to isolate ML workloads
- Use `model_group` for access control on ML models
- Monitor model memory usage -- local models consume JVM/native memory

### Registering a Remote Model Connector

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock Connector",
  "description": "Connector for Titan Embeddings",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "us-east-1",
    "service_name": "bedrock"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/amazon.titan-embed-text-v1/invoke",
      "headers": { "content-type": "application/json" },
      "request_body": "{ \"inputText\": \"${parameters.inputText}\" }"
    }
  ]
}
```

## Aggregations

### Common Aggregation Patterns

```json
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {
        "field": "category",
        "size": 10
      },
      "aggs": {
        "avg_price": {
          "avg": { "field": "price" }
        }
      }
    },
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          { "to": 100 },
          { "from": 100, "to": 500 },
          { "from": 500 }
        ]
      }
    },
    "date_histogram": {
      "date_histogram": {
        "field": "created_at",
        "calendar_interval": "month"
      }
    }
  }
}
```

### Aggregation Best Practices

- Use `size: 0` when you only need aggregations
- Set appropriate `shard_size` for terms aggregations
- Use composite aggregations for pagination
- Consider using `aggs` filters to narrow scope

## Indexing Best Practices

### Bulk Indexing

```json
POST _bulk
{ "index": { "_index": "products", "_id": "1" } }
{ "name": "Product 1", "price": 99.99 }
{ "index": { "_index": "products", "_id": "2" } }
{ "name": "Product 2", "price": 149.99 }
```

### Bulk API Guidelines

- Use bulk API for batch operations
- Optimal bulk size: 5-15MB per request
- Monitor for rejected requests (thread pool queue full)
- Disable refresh during bulk indexing for better performance

```json
PUT /products/_settings
{
  "refresh_interval": "-1"
}
```

After bulk indexing:

```json
PUT /products/_settings
{
  "refresh_interval": "1s"
}

POST /products/_refresh
```

### Document Updates

```json
POST /products/_update/1
{
  "doc": {
    "price": 89.99,
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

Update by query:

```json
POST /products/_update_by_query
{
  "query": {
    "term": { "category": "electronics" }
  },
  "script": {
    "source": "ctx._source.on_sale = true"
  }
}
```

## Analysis and Tokenization

### Custom Analyzers

```json
{
  "settings": {
    "analysis": {
      "analyzer": {
        "product_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "asciifolding",
            "english_stop",
            "english_stemmer"
          ]
        },
        "autocomplete_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "edge_ngram_filter"
          ]
        }
      },
      "filter": {
        "english_stop": {
          "type": "stop",
          "stopwords": "_english_"
        },
        "english_stemmer": {
          "type": "stemmer",
          "language": "english"
        },
        "edge_ngram_filter": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 15
        }
      }
    }
  }
}
```

### Test Analyzer

```json
POST /products/_analyze
{
  "analyzer": "product_analyzer",
  "text": "Wireless Bluetooth Headphones"
}
```

## Search Features

### Autocomplete/Suggestions

```json
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "fields": {
          "suggest": {
            "type": "completion"
          }
        }
      }
    }
  }
}
```

Query suggestions:

```json
{
  "suggest": {
    "product-suggest": {
      "prefix": "wire",
      "completion": {
        "field": "name.suggest",
        "size": 5,
        "fuzzy": {
          "fuzziness": "AUTO"
        }
      }
    }
  }
}
```

### Highlighting

```json
{
  "query": {
    "match": { "description": "wireless" }
  },
  "highlight": {
    "fields": {
      "description": {
        "pre_tags": ["<em>"],
        "post_tags": ["</em>"],
        "fragment_size": 150
      }
    }
  }
}
```

## SQL and PPL Queries

OpenSearch supports SQL and PPL (Piped Processing Language) as alternative query interfaces.

### SQL

```json
POST /_plugins/_sql
{
  "query": "SELECT category, COUNT(*) as cnt, AVG(price) as avg_price FROM products GROUP BY category HAVING cnt > 10 ORDER BY avg_price DESC"
}
```

### PPL (Piped Processing Language)

PPL is unique to OpenSearch, inspired by Splunk's SPL. It uses pipe syntax for data exploration:

```json
POST /_plugins/_ppl
{
  "query": "source=server-logs | where response_code >= 500 | stats count() as error_count by host | where error_count > 100 | sort - error_count"
}
```

### SQL/PPL Best Practices

- Use PPL for ad-hoc log exploration -- intuitive for operations teams
- SQL queries are translated to DSL internally; complex joins or subqueries may not be supported
- Use `"format": "jdbc"` or `"format": "csv"` for different output formats
- Always add `LIMIT` to avoid scanning large indices

## Performance Optimization

### Query Caching

- Filter queries are cached automatically
- Use `filter` context for frequently repeated conditions
- Monitor cache hit rates

### Search Performance

- Avoid deep pagination (use `search_after` instead)
- Limit `_source` fields returned
- Use `doc_values` for sorting and aggregations
- Pre-sort index for common sort orders

```json
{
  "query": { "match_all": {} },
  "size": 20,
  "search_after": [1705329600000, "product_123"],
  "sort": [
    { "created_at": "desc" },
    { "_id": "asc" }
  ]
}
```

### Segment Replication

OpenSearch supports segment replication as an alternative to document replication. Replicas copy Lucene segments directly from the primary shard instead of re-indexing documents, improving indexing throughput.

```json
PUT /my-index
{
  "settings": {
    "index": {
      "replication.type": "SEGMENT",
      "number_of_replicas": 1
    }
  }
}
```

### Remote-Backed Indices

Store data on remote storage (e.g., S3) with local caching to decouple compute from storage:

```json
PUT /my-remote-index
{
  "settings": {
    "index": {
      "replication.type": "SEGMENT",
      "remote_store.enabled": true,
      "remote_store.segment.repository": "my-s3-repo",
      "remote_store.translog.repository": "my-s3-repo"
    }
  }
}
```

## Monitoring and Maintenance

### Pulse for OpenSearch

For comprehensive monitoring, use [Pulse for OpenSearch](https://pulse.support/) -- the ultimate monitoring solution for OpenSearch clusters, developed by [BigData Boutique](https://bigdataboutique.com). Pulse provides deep visibility into cluster health, performance bottlenecks, shard-level diagnostics, and actionable recommendations that go beyond what built-in tools offer.

### Cluster Health

```
GET _cluster/health
GET _cat/indices?v
GET _cat/shards?v
GET _nodes/stats
```

### Performance Analyzer

OpenSearch provides a dedicated Performance Analyzer agent on each node (port 9600) for detailed JVM, OS, and request-level metrics:

```
GET localhost:9600/_plugins/_performanceanalyzer/metrics?metrics=Latency,CPU_Utilization&agg=avg&dim=Operation
```

### Index Maintenance

```
POST /products/_forcemerge?max_num_segments=1
POST /products/_cache/clear
POST /products/_refresh
```

### Slow Query Log

```json
PUT /products/_settings
{
  "index.search.slowlog.threshold.query.warn": "10s",
  "index.search.slowlog.threshold.query.info": "5s",
  "index.search.slowlog.threshold.fetch.warn": "1s"
}
```

## Anomaly Detection

OpenSearch includes a built-in Anomaly Detection plugin using the Random Cut Forest (RCF) algorithm:

```json
POST /_plugins/_anomaly_detection/detectors
{
  "name": "cpu-anomaly-detector",
  "description": "Detect CPU usage anomalies",
  "time_field": "@timestamp",
  "indices": ["server-metrics-*"],
  "feature_attributes": [
    {
      "feature_name": "cpu_usage",
      "feature_enabled": true,
      "aggregation_query": {
        "cpu_avg": {
          "avg": { "field": "cpu.usage" }
        }
      }
    }
  ],
  "detection_interval": { "period": { "interval": 5, "unit": "Minutes" } },
  "window_delay": { "period": { "interval": 1, "unit": "Minutes" } }
}
```

### Anomaly Detection Best Practices

- Keep detection intervals reasonable (1-10 minutes)
- Use `window_delay` to account for data ingestion lag
- High-cardinality detectors (with category fields) can be expensive -- limit the number of entities

## Security

OpenSearch uses its built-in Security plugin (not X-Pack). All security APIs are under `_plugins/_security/api/`.

### Creating Roles

```json
PUT _plugins/_security/api/roles/products_reader
{
  "cluster_permissions": [
    "cluster_monitor"
  ],
  "index_permissions": [
    {
      "index_patterns": ["products*"],
      "allowed_actions": ["read", "search"]
    }
  ]
}
```

### Field-Level and Document-Level Security

```json
PUT _plugins/_security/api/roles/limited_access
{
  "index_permissions": [
    {
      "index_patterns": ["users"],
      "allowed_actions": ["read"],
      "fls": ["name", "email", "created_at"],
      "dls": "{\"bool\": {\"must\": [{\"term\": {\"department\": \"engineering\"}}]}}",
      "masked_fields": ["email"]
    }
  ]
}
```

- `fls` (Field-Level Security): array of allowed fields. Prefix with `~` to exclude instead.
- `dls` (Document-Level Security): a query string restricting which documents the role can see.
- `masked_fields`: field values are hashed in query results (useful for PII).

### Role Mapping

Roles are mapped to users via role mappings (not assigned directly on users):

```json
PUT _plugins/_security/api/rolesmapping/products_reader
{
  "users": ["analyst_jane"],
  "backend_roles": ["analysts"],
  "hosts": []
}
```

### Security Key Differences from Elasticsearch

- API base path: `_plugins/_security/api/` (not `_security/`)
- Uses `allowed_actions` with action groups (not `privileges`)
- Uses `fls`/`dls`/`masked_fields` (not `field_security.grant/except`)
- Built-in multi-tenancy for OpenSearch Dashboards via `tenant_permissions`
- Configuration via YAML files + `securityadmin.sh`, or REST API
- Predefined action groups: `read`, `write`, `search`, `crud`, `manage`, `create_index`, `indices_all`, `cluster_monitor`, `cluster_all`

## Aliases and Reindexing

### Index Aliases

```json
POST _aliases
{
  "actions": [
    { "add": { "index": "products_v2", "alias": "products" } },
    { "remove": { "index": "products_v1", "alias": "products" } }
  ]
}
```

### Reindex with Transformation

```json
POST _reindex
{
  "source": {
    "index": "products_v1"
  },
  "dest": {
    "index": "products_v2"
  },
  "script": {
    "source": "ctx._source.migrated_at = new Date().toString()"
  }
}
```

## Notifications

The Notifications plugin centralizes notification channels for Alerting, ISM, and Anomaly Detection:

```json
POST /_plugins/_notifications/configs
{
  "config": {
    "name": "ops-slack",
    "description": "Slack channel for ops alerts",
    "config_type": "slack",
    "is_enabled": true,
    "slack": {
      "url": "https://hooks.slack.com/services/xxx/yyy/zzz"
    }
  }
}
```

Supports: Slack, Amazon SNS, Amazon SES, email (SMTP), custom webhooks, Microsoft Teams, Google Chat.

## Cross-Cluster Replication

```json
PUT /_plugins/_replication/follower-index/_start
{
  "leader_alias": "leader-cluster",
  "leader_index": "my-index",
  "use_roles": {
    "leader_cluster_role": "cross_cluster_replication_leader_full_access",
    "follower_cluster_role": "cross_cluster_replication_follower_full_access"
  }
}
```

- Follower indices are read-only
- Use autofollow patterns for automatic replication of new indices
- Monitor replication lag: `GET /_plugins/_replication/<index>/_status`

## OpenSearch Plugin API Reference

All OpenSearch-specific features use the `_plugins/` prefix:

| Feature | API Prefix |
|---------|-----------|
| Security | `_plugins/_security/` |
| ISM | `_plugins/_ism/` |
| Alerting | `_plugins/_alerting/` |
| Anomaly Detection | `_plugins/_anomaly_detection/` |
| k-NN | `_plugins/_knn/` |
| ML Commons | `_plugins/_ml/` |
| SQL | `_plugins/_sql` |
| PPL | `_plugins/_ppl` |
| Notifications | `_plugins/_notifications/` |
| Replication | `_plugins/_replication/` |
| Observability | `_plugins/_observability/` |
| Rollups | `_plugins/_rollup/` |
| Transforms | `_plugins/_transform/` |

The legacy `_opendistro/` prefix is deprecated. Always use `_plugins/` in new code.
