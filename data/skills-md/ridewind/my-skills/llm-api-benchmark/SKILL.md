---
name: llm-api-benchmark
description: This skill should be used when the user asks to "benchmark LLM API", "test API speed", "measure response time", "check API latency", "test TPS", "benchmark endpoint", "compare endpoint performance", "测试端点性能", "基准测试", "测试LLM速度", or needs to evaluate LLM API performance metrics (TTFT, TPS, latency).
---

# LLM API Benchmark

LLM API 端点性能测试工具，支持两种测试模式：

- **Agent 模式**：测试真实工作负载响应时间（推荐用于相对性能对比）
- **HTTP 模式**：精确测量 TTFT/TPS 指标（使用 Python 脚本直接调用 API）

## Quick Start

### Agent 模式（推荐）

**第一步：确认测试方案**

使用 AskUserQuestion 工具确认：

```
question: "📊 LLM API Benchmark 测试方案

**测试参数**:
- 测试类型: Agent 模式
- 迭代次数: 5（默认）
- 任务类型: implementation（默认，~500-700 tokens）

是否开始测试？"

options:
- "确认开始"
- "修改参数"
- "切换到 HTTP 模式"
```

**第二步：执行测试**

用户确认后，使用 Agent 工具启动 orchestrator subagent。

**Agent 模式工作原理**：
- Orchestrator 会串行执行 N 次迭代
- 每次迭代中，orchestrator 会记录时间 → 直接回答任务提示词（触发 LLM API 调用）→ 记录结束时间
- 记录完整的 LLM 输出内容和时间戳
- 最后计算统计数据并保存 JSON 报告

详细提示词模板见 [references/orchestrator-patterns.md](references/orchestrator-patterns.md)。

**第三步：显示结果**

```
✅ 测试完成！

📊 结果摘要：
- 端点: {endpoint}
- 迭代次数: {iterations}
- 平均响应时间: {avg_time:.2f}s
- 最小: {min_time:.2f}s | 最大: {max_time:.2f}s
- 平均 TPS: {avg_tps:.1f} tokens/s

📁 详细报告: reports/llm-benchmark-subagent/benchmark-{timestamp}.json
```

### HTTP 模式（精确指标）

使用 Python 脚本直接调用 API，获取精确的 TTFT 和 TPS：

```bash
# 默认使用 code preset (~500-1000 tokens)
python skills/llm-api-benchmark/scripts/benchmark.py

# 列出可用预设
python skills/llm-api-benchmark/scripts/benchmark.py --list-presets

# 指定预设和迭代次数
python skills/llm-api-benchmark/scripts/benchmark.py --preset throughput --iterations 10
```

**预设列表**：

| Preset | Description | Output |
|--------|-------------|--------|
| quick | 快速测试 | ~10 tokens |
| standard | 中等长度 | ~20 tokens |
| long | 长输出测试 | ~100+ tokens |
| throughput | 高吞吐测试 | ~300-500 tokens |
| code | 代码生成（默认） | ~500-1000 tokens |
| json | JSON 输出测试 | ~30 tokens |

## Task Prompts

Agent 模式支持多种任务类型，详见 [references/task-prompts.md](references/task-prompts.md)。

| Task Type | Description | Target Output | Use Case |
|-----------|-------------|---------------|----------|
| counting | 数字序列生成 | ~50 tokens | TTFT 测试（最稳定） |
| structured-list | 结构化列表 | ~100-150 tokens | 中等负载测试 |
| code-review | 代码审查报告 | ~300-400 tokens | 代码工作负载 |
| implementation | 完整代码实现（默认） | ~500-700 tokens | 吞吐量测试 |
| comprehensive | 综合分析报告 | ~800-1000 tokens | 真实工作负载 |

## Compare Endpoints

对比多个端点性能：

```bash
python skills/llm-api-benchmark/scripts/compare-results.py
```

## Output Format

### JSON Result Structure

```json
{
  "timestamp": "2026-03-05T10:30:45",
  "endpoint": "https://...",
  "task": "implementation",
  "iterations": 5,
  "avg_time": 1.23,
  "min_time": 1.15,
  "max_time": 1.31,
  "avg_tps": 45.2,
  "total_tokens": 275,
  "details": [
    {
      "iteration": 1,
      "start_time": "2026-03-05T10:30:45.123",
      "end_time": "2026-03-05T10:30:46.353",
      "response_time": 1.23,
      "tokens": 56,
      "tps": 45.5,
      "output": "完整的端点输出内容..."
    }
  ]
}
```

**字段说明**：
- `details[]`: 每次迭代的详细记录
  - `start_time`: 迭代开始时间（ISO 格式）
  - `end_time`: 迭代结束时间（ISO 格式）
  - `output`: 端点输出的完整内容
- **TPS 计算**：输出 token 数按 1 token ≈ 4 字符估算，TPS = tokens / response_time

## Mode Comparison

| Feature | Agent Mode | HTTP Mode |
|---------|------------|-----------|
| Trigger | Agent 工具 | Python 脚本 |
| Measures | LLM 端点响应时间（通过 Agent 回答任务触发 API 调用） | HTTP 响应 + TTFT + TPS（直接调用 API） |
| Auth prompts | 一次确认完成所有迭代 | 无需确认 |
| Use case | 相对性能对比（测试真实 Agent 工作负载） | 精确性能测量（纯 API 性能） |

## Troubleshooting

### Agent 工具不可用

使用 HTTP 模式：

```bash
python skills/llm-api-benchmark/scripts/benchmark.py
```

### 端点配置问题

```
Endpoint: unknown
```

解决方案：
- 使用 `cc-switch <endpoint-name>` 配置
- 或设置 `export ANTHROPIC_BASE_URL=https://your-endpoint`

### API 调用失败

1. 检查 API 密钥是否正确设置
2. 验证端点 URL 是否可访问
3. 使用 HTTP 模式进行诊断

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/benchmark.py` | HTTP 模式基准测试 |
| `scripts/compare-results.py` | 对比多个端点结果 |