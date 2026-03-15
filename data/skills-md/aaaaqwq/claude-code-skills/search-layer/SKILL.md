---
name: search-layer
description: >
  DEFAULT search tool for ALL search/lookup needs. Multi-source search and deduplication
  layer with intent-aware scoring. Integrates Brave Search (web_search), Exa, Tavily,
  and Grok to provide high-coverage, high-quality results. Automatically classifies
  query intent and adjusts search strategy, scoring weights, and result synthesis.
  Use for ANY query that requires web search — factual lookups, research, news,
  comparisons, resource finding, "what is X", status checks, etc. Do NOT use raw
  web_search directly; always route through this skill.
---

# Search Layer v2.2 — 意图感知多源检索协议

四源同级：Brave (`web_search`) + Exa + Tavily + Grok。按意图自动选策略、调权重、做合成。

## 执行流程

```
用户查询
    ↓
[Phase 1] 意图分类 → 确定搜索策略
    ↓
[Phase 2] 查询分解 & 扩展 → 生成子查询
    ↓
[Phase 3] 多源并行检索 → Brave + search.py (Exa + Tavily + Grok)
    ↓
[Phase 4] 结果合并 & 排序 → 去重 + 意图加权评分
    ↓
[Phase 5] 知识合成 → 结构化输出
```

---

## Phase 1: 意图分类

收到搜索请求后，**先判断意图类型**，再决定搜索策略。不要问用户用哪种模式。

| 意图 | 识别信号 | Mode | Freshness | 权重偏向 |
|------|---------|------|-----------|---------|
| **Factual** | "什么是 X"、"X 的定义"、"What is X" | answer | — | 权威 0.5 |
| **Status** | "X 最新进展"、"X 现状"、"latest X" | deep | pw/pm | 新鲜度 0.5 |
| **Comparison** | "X vs Y"、"X 和 Y 区别" | deep | py | 关键词 0.4 + 权威 0.4 |
| **Tutorial** | "怎么做 X"、"X 教程"、"how to X" | answer | py | 权威 0.5 |
| **Exploratory** | "深入了解 X"、"X 生态"、"about X" | deep | — | 权威 0.5 |
| **News** | "X 新闻"、"本周 X"、"X this week" | deep | pd/pw | 新鲜度 0.6 |
| **Resource** | "X 官网"、"X GitHub"、"X 文档" | fast | — | 关键词 0.5 |

> 详细分类指南见 `references/intent-guide.md`

**判断规则**：
1. 扫描查询中的信号词
2. 多个类型匹配时选最具体的
3. 无法判断时默认 `exploratory`

---

## Phase 2: 查询分解 & 扩展

根据意图类型，将用户查询扩展为一组子查询：

### 通用规则
- **技术同义词自动扩展**：k8s→Kubernetes, JS→JavaScript, Go→Golang, Postgres→PostgreSQL
- **中文技术查询**：同时生成英文变体（如 "Rust 异步编程" → 额外搜 "Rust async programming"）

### 按意图扩展

| 意图 | 扩展策略 | 示例 |
|------|---------|------|
| Factual | 加 "definition"、"explained" | "WebTransport" → "WebTransport", "WebTransport explained overview" |
| Status | 加年份、"latest"、"update" | "Deno 进展" → "Deno 2.0 latest 2026", "Deno update release" |
| Comparison | 拆成 3 个子查询 | "Bun vs Deno" → "Bun vs Deno", "Bun advantages", "Deno advantages" |
| Tutorial | 加 "tutorial"、"guide"、"step by step" | "Rust CLI" → "Rust CLI tutorial", "Rust CLI guide step by step" |
| Exploratory | 拆成 2-3 个角度 | "RISC-V" → "RISC-V overview", "RISC-V ecosystem", "RISC-V use cases" |
| News | 加 "news"、"announcement"、日期 | "AI 新闻" → "AI news this week 2026", "AI announcement latest" |
| Resource | 加具体资源类型 | "Anthropic MCP" → "Anthropic MCP official documentation" |

---

## Phase 3: 多源并行检索

### Step 1: Brave（所有模式）

对每个子查询调用 `web_search`。如果意图有 freshness 要求，传 `freshness` 参数：

```
web_search(query="Deno 2.0 latest 2026", freshness="pw")
```

### Step 2: Exa + Tavily + Grok（Deep / Answer 模式）

对子查询调用 search.py，传入意图和 freshness：

```bash
python3 /home/node/.openclaw/workspace/skills/search-layer/scripts/search.py \
  --queries "子查询1" "子查询2" "子查询3" \
  --mode deep \
  --intent status \
  --freshness pw \
  --num 5
```

**各模式源参与矩阵**：
| 模式 | Exa | Tavily | Grok | 说明 |
|------|-----|--------|------|------|
| fast | ✅ | ❌ | fallback | Exa 优先；无 Exa key 时用 Grok |
| deep | ✅ | ✅ | ✅ | 三源并行 |
| answer | ❌ | ✅ | ❌ | 仅 Tavily（含 AI answer） |

**参数说明**：
| 参数 | 说明 |
|------|------|
| `--queries` | 多个子查询并行执行（也可用位置参数传单个查询） |
| `--mode` | fast / deep / answer |
| `--intent` | 意图类型，影响评分权重（不传则不评分，行为与 v1 一致） |
| `--freshness` | pd(24h) / pw(周) / pm(月) / py(年) |
| `--domain-boost` | 逗号分隔的域名，匹配的结果权威分 +0.2 |
| `--num` | 每源每查询的结果数 |

**Grok 源说明**：
- 通过 completions API 调用 Grok 模型（`grok-4.1-fast`），利用其实时知识返回结构化搜索结果
- 自动检测时间敏感查询并注入当前时间上下文
- 在 deep 模式下与 Exa、Tavily 并行执行
- 需要在 `~/.openclaw/credentials/search.json` 中配置 Grok 的 `apiUrl`、`apiKey`、`model`（或通过环境变量 `GROK_API_URL`、`GROK_API_KEY`、`GROK_MODEL`）
- 如果 Grok 配置缺失，自动降级为 Exa + Tavily 双源

### Step 3: 合并

将 Brave 结果与 search.py 输出合并。按 canonical URL 去重，标记来源。

如果 search.py 返回了 `score` 字段，用它排序；Brave 结果没有 score 的，用同样的意图权重公式补算。

---

## Phase 3.5: 引用追踪（Thread Pulling）

当搜索结果中包含 GitHub issue/PR 链接，且意图为 Status 或 Exploratory 时，自动触发引用追踪。

### 自动触发条件

- 意图为 `status` 或 `exploratory`
- 搜索结果中包含 `github.com/.../issues/` 或 `github.com/.../pull/` URL

### 方式 1: search.py --extract-refs（批量）

在搜索结果上直接提取引用图，无需额外调用：

```bash
python3 search.py "OpenClaw config validation bug" --mode deep --intent status --extract-refs
```

输出中会多一个 `refs` 字段，包含每个结果 URL 的引用列表。

也可以跳过搜索，直接对已知 URL 提取引用：

```bash
python3 search.py --extract-refs-urls "https://github.com/owner/repo/issues/123" "https://github.com/owner/repo/issues/456"
```

### 方式 2: fetch-thread（单 URL 深度抓取）

对单个 URL 拉取完整讨论流 + 结构化引用：

```bash
python3 fetch_thread.py "https://github.com/owner/repo/issues/123" --format json
python3 fetch_thread.py "https://github.com/owner/repo/issues/123" --format markdown
python3 fetch_thread.py "https://github.com/owner/repo/issues/123" --extract-refs-only
```

GitHub 场景（issue/PR）：通过 API 拉取正文 + 全部 comments + timeline 事件（cross-references、commits），提取：
- Issue/PR 引用（#123、owner/repo#123）
- Duplicate 标记
- Commit 引用
- 关联 PR/issue（timeline cross-references）
- 外部 URL

通用 web 场景：web fetch + 正则提取引用链接。

### Agent 执行流程

```
Step 1: search-layer 搜索 → 获取初始结果
Step 2: search.py --extract-refs 或 fetch-thread → 提取线索图
Step 3: Agent 筛选高价值线索（LLM 判断哪些值得追踪）
Step 4: fetch-thread 深度抓取每个高价值线索
Step 5: 重复 Step 2-4，直到信息闭环或达到深度限制（建议 max_depth=3）
```

---

## Phase 4: 结果排序

### 评分公式

```
score = w_keyword × keyword_match + w_freshness × freshness_score + w_authority × authority_score
```

权重由意图决定（见 Phase 1 表格）。各分项：

- **keyword_match** (0-1)：查询词在标题+摘要中的覆盖率
- **freshness_score** (0-1)：基于发布日期，越新越高（无日期=0.5）
- **authority_score** (0-1)：基于域名权威等级
  - Tier 1 (1.0): github.com, stackoverflow.com, 官方文档站
  - Tier 2 (0.8): HN, dev.to, 知名技术博客
  - Tier 3 (0.6): Medium, 掘金, InfoQ
  - Tier 4 (0.4): 其他

> 完整域名评分表见 `references/authority-domains.json`

### Domain Boost

通过 `--domain-boost` 参数手动指定需要加权的域名（匹配的结果权威分 +0.2）：
```bash
search.py "query" --mode deep --intent tutorial --domain-boost dev.to,freecodecamp.org
```

推荐搭配：
- Tutorial → `dev.to, freecodecamp.org, realpython.com, baeldung.com`
- Resource → `github.com`
- News → `techcrunch.com, arstechnica.com, theverge.com`

---

## Phase 5: 知识合成

根据结果数量选择合成策略：

### 小结果集（≤5 条）
逐条展示，每条带源标签和评分：
```
1. [Title](url) — snippet... `[brave, exa]` ⭐0.85
2. [Title](url) — snippet... `[tavily]` ⭐0.72
```

### 中结果集（5-15 条）
按主题聚类 + 每组摘要：
```
**主题 A: [描述]**
- [结果1] — 要点... `[source]`
- [结果2] — 要点... `[source]`

**主题 B: [描述]**
- [结果3] — 要点... `[source]`
```

### 大结果集（15+ 条）
高层综述 + Top 5 + 深入提示：
```
[一段综述，概括主要发现]

**Top 5 最相关结果：**
1. ...
2. ...

共找到 N 条结果，覆盖 [源列表]。需要深入哪个方面？
```

### 合成规则
- **先给答案，再列来源**（不要先说"我搜了什么"）
- **按主题聚合，不按来源聚合**（不要"Brave 结果：... Exa 结果：..."）
- **冲突信息显性标注**：不同源说法矛盾时明确指出
- **置信度表达**：
  - 多源一致 + 新鲜 → 直接陈述
  - 单源或较旧 → "根据 [source]，..."
  - 冲突或不确定 → "存在不同说法：A 认为...，B 认为..."

---

## 降级策略

- Exa 429/5xx → 继续 Brave + Tavily + Grok
- Tavily 429/5xx → 继续 Brave + Exa + Grok
- Grok 超时/错误 → 继续 Brave + Exa + Tavily
- search.py 整体失败 → 仅用 Brave `web_search`（始终可用）
- **永远不要因为某个源失败而阻塞主流程**

---

## 向后兼容

不带 `--intent` 参数时，search.py 行为与 v1 完全一致（无评分，按原始顺序输出）。

现有调用方（如 github-explorer）无需修改。

---

## 快速参考

| 场景 | 命令 |
|------|------|
| 快速事实 | `web_search` + `search.py --mode answer --intent factual` |
| 深度调研 | `web_search` + `search.py --mode deep --intent exploratory` |
| 最新动态 | `web_search(freshness="pw")` + `search.py --mode deep --intent status --freshness pw` |
| 对比分析 | `web_search` × 3 queries + `search.py --queries "A vs B" "A pros" "B pros" --intent comparison` |
| 找资源 | `web_search` + `search.py --mode fast --intent resource` |
