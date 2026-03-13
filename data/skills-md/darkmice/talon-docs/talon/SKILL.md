---
name: talon
description: "Talon 多模融合数据引擎使用指南。当用户需要使用 Talon 数据库进行开发时触发：包括 SQL 查询、KV 存储、向量搜索、时序数据、消息队列、全文检索、地理空间、图数据库、AI 引擎（Session/Context/Memory/RAG/Agent/Trace）。也适用于：选择 Talon 引擎模块、使用 Go/Python/Node.js/Java/.NET SDK、构建 RAG 管道、Agent 工具缓存、对话管理、embedding 缓存、跨引擎融合查询（GraphRAG、Hybrid Search）。"
---

# Talon 使用指南

Talon 是面向 AI 应用的多模融合数据引擎，单二进制、零外部依赖，提供 8 大开源引擎：SQL、KV、Vector、TimeSeries、MessageQueue、Full-Text Search、GEO、Graph。
AI 引擎通过商业授权的 `talon-ai` 预编译库提供（不含源码）。

## 连接

```rust
use talon::Talon;
let db = Talon::open("./data")?;  // 嵌入式模式，数据目录
```

多语言 SDK 均通过 FFI 绑定 `libtalon`，接口模式一致。详见 [references/sdk.md](references/sdk.md)。

## 引擎选择

| 场景 | 引擎 | 入口 |
|------|------|------|
| 结构化数据 CRUD、JOIN、聚合 | SQL | `db.run_sql()` |
| 缓存、会话 token、分布式锁 | KV | `db.kv()` / Redis 协议 |
| embedding 相似搜索、RAG 检索 | Vector | `db.vector()` / SQL `vec_cosine()` |
| 对话管理、Agent 状态、记忆 | AI (商业) | `db.ai()` (需 talon-ai) |
| 监控指标、token 用量追踪 | TimeSeries | `db.create_timeseries()` |
| 异步任务、事件驱动 | MQ | `db.mq()` |
| 关键词搜索、BM25 排序 | FTS | `db.fts()` |
| LBS、附近推荐 | GEO | `db.geo()` |
| 知识图谱、关系推理 | Graph | `db.graph()` |
| RAG (BM25+向量) | Fusion | `hybrid_search()` |
| GraphRAG | Fusion | `graph_vector_search()` |

## 快速上手

### SQL
```rust
db.run_sql("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, emb VECTOR(384))")?;
db.run_sql("INSERT INTO users VALUES (1, 'Alice', '[0.1, ...]')")?;
db.run_sql("SELECT id, vec_cosine(emb, '[0.1, ...]') AS score FROM users ORDER BY score LIMIT 10")?;
```

### KV
```rust
db.kv()?.set(b"user:1", b"Alice", None)?;           // 无 TTL
db.kv()?.set(b"session:x", b"tok", Some(3600))?;     // 1h TTL
let val = db.kv_read()?.get(b"user:1")?;
```

### Vector
```rust
db.run_sql("CREATE VECTOR INDEX idx ON docs(emb) USING HNSW WITH (metric='cosine')")?;
let ve = db.vector("idx")?;
let hits = ve.search(&query_vec, 10, "cosine")?;      // (id, score)
```

### AI (Session / Memory / RAG) — 需要 talon-ai 预编译库
```rust
use talon_ai::TalonAiExt; // 商业授权预编译库

let ai = db.ai()?;
ai.create_session("chat-1", BTreeMap::new(), None)?;
ai.append_message("chat-1", &ContextMessage { role: "user".into(), content: "Hi".into(), token_count: Some(1) })?;
let history = ai.get_context_window("chat-1", 4096)?; // 自动截断到 token 预算
ai.store_memory("chat-1", "用户偏好 Rust", &embedding, None)?;
let mems = ai.search_memories("chat-1", &query_emb, 5)?;
```

### 跨引擎融合查询
```rust
// Hybrid Search: BM25 + Vector (RRF)
let hits = hybrid_search(&store, &HybridQuery {
    fts_index: "articles", vec_index: "emb_idx",
    query_text: "AI database", query_vec: &emb, limit: 10, ..Default::default()
})?;

// GraphRAG: 图遍历 + 向量相似
let hits = graph_vector_search(&store, &GraphVectorQuery {
    graph: "knowledge", vec_name: "embeddings",
    start: root_id, max_depth: 3, direction: Direction::Out,
    query_vec: &emb, k: 10,
})?;
```

## 详细 API 参考

按需查阅对应 reference 文件：

- **SQL 引擎** (DDL/DML/函数/窗口/CTE/事务): [references/sql.md](references/sql.md)
- **KV 引擎** (CRUD/TTL/计数器/扫描/快照): [references/kv.md](references/kv.md)
- **Vector 引擎** (HNSW/metadata filter/量化/recommend/discover): [references/vector.md](references/vector.md)
- **AI 引擎** (Session/Context/Memory/RAG/Agent/Trace/Intent) — 商业授权: [references/ai.md](references/ai.md)
- **其他引擎** (TS/MQ/FTS/GEO/Graph/Fusion): [references/more-engines.md](references/more-engines.md)
- **多语言 SDK** (Go/Python/Node.js/Java/.NET): [references/sdk.md](references/sdk.md)

## AI 应用最佳实践

### RAG 管道
```
用户问题 → Embedding → hybrid_search(FTS + Vector) → Top-K chunks → LLM Context → 回答
```
用 `ai.store_document()` 存储文档分块，`ai.search_chunks()` 向量检索，`ai.search_chunks_hybrid()` 混合检索。

### Agent 工具缓存
```rust
ai.cache_tool_result("weather", &args_hash, result_bytes, Some(3600))?;
if let Some(cached) = ai.get_cached_tool_result("weather", &args_hash)? { return cached; }
```

### 对话管理
```rust
ai.set_system_prompt("chat-1", "你是一个 Rust 专家")?;
let (prompt, msgs) = ai.get_context_window_with_prompt("chat-1", 4096)?;
// prompt + msgs 直接送入 LLM API
```

### Embedding 缓存
```rust
let hash = sha256(text);
if let Some(emb) = ai.get_cached_embedding(&hash)? { return emb; }
let emb = call_openai_embedding(text)?;
ai.cache_embedding(&hash, &emb)?;
```

### 执行追踪
```rust
ai.log_trace(&TraceRecord {
    run_id: "run-1".into(), session_id: Some("chat-1".into()),
    operation: "llm_call".into(), input: json!({"model": "gpt-4"}),
    output: None, latency_ms: 230, token_usage: Some(150),
})?;
let report = ai.trace_performance_report(Some("chat-1"))?;
```
