---
name: tavily
description: AI 优化的网络搜索。使用 Tavily API 进行智能搜索，获取实时信息。当用户需要搜索互联网、获取实时数据、查找最新信息时使用此技能。
allowed-tools: Bash, Read, Write, Edit
---

# Tavily AI 搜索

## 功能说明
此技能使用 Tavily API 提供 AI 优化的网络搜索能力：
- 智能搜索（AI 优化结果）
- 实时信息获取
- 搜索并提取内容
- 支持搜索深度和范围控制

## 使用方式

### 1. 基础搜索
```bash
./scripts/tavily.sh search <query> [max_results]
```

### 2. 深度搜索（包含更多内容）
```bash
./scripts/tavily.sh search <query> --deep
```

### 3. 搜索并提取
```bash
./scripts/tavily.sh extract <query> [max_results]
```

## API Key
存储在: `pass show api/tavily`

## 示例

### 搜索 Polymarket 信息
```bash
./scripts/tavily.sh search "Polymarket Fed interest rate decision 2026"
```

### 搜索 AI 新闻
```bash
./scripts/tavily.sh search "latest AI news today" 5
```

### 深度搜索
```bash
./scripts/tavily.sh search "Bitcoin price analysis" --deep
```

## 注意事项
- Tavily 有使用限制（取决于套餐）
- 搜索结果经过 AI 优化，更适合 LLM 使用
- 支持实时数据获取
