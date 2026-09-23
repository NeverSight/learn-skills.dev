---
name: yapi-skill
description: 自动从 Yapi 平台拉取接口定义并以原始 JSON 回传给 LLM。当用户调用 `yapi-skill`、或要求获取后端接口定义、查看 Yapi 接口文档、查询接口字段时，必须使用本 SKILL。工作流：定位并加载 .env 中的 YAPI 配置 → 用 Bash 执行 SKILL 内置的 `scripts/yapi_fetch.py` 调用 Yapi 开放接口 → 把脚本输出的 Yapi 原始 JSON 整理后回传。哪怕用户没有显式说"用 yapi-skill"，只要目标是从 Yapi 拿接口定义来实现/调试代码，也必须使用本 SKILL，禁止使用 yapi-mcp MCP 工具替代。
---

# Yapi 接口定义自动获取 SKILL

## 目标

让 LLM 能够稳定地、自动化地从 Yapi 平台拉取接口定义信息（请求参数、返回结构、字段说明等），并以 **Yapi 原始 JSON** 形式回传，供后续代码生成、接口联调、Bug 定位使用。

**本 SKILL 不直接生成业务代码，只负责"取数据 → 回传 JSON"这两步**。拿到 JSON 后，调用方（LLM 本体）会基于这些字段定义去实现 Flutter / React / Spring Boot 等具体代码。

## 触发场景（满足任一即使用）

- 用户输入 `yapi-skill`、`/yapi-skill`、或在对话中明确说"调 yapi-skill"
- 用户描述需求时提到 Yapi、接口文档、接口字段、请求参数、返回结构
- 用户让 LLM 实现某个后端接口（此时需要先拉接口定义）
- 用户排查某个线上接口问题时（需要拿原始定义做对比）
- 用户给出 .env 中的 `YAPI_TOKEN` 并要求查询接口

## 准备工作：定位 .env 文件

**所有 Yapi 调用都依赖项目里的 `.env` 文件**，本 SKILL 自带的 Python 脚本会从 .env 中读取 `YAPI_URL / YAPI_TOKEN / YAPI_PROJECT_ID` 三项。

按以下顺序确定 .env 路径：

1. **用户显式指定** → 把绝对路径作为 `--env` 参数传给脚本
2. **未指定** → 从当前工作目录（CWD）开始，**逐级向上**查找 `.env`，找到第一个即停止
3. **到达文件系统根目录仍未找到** → 提示用户在工程根目录创建 `.env` 并写入以下三项：

```bash
# API 配置
YAPI_URL=https://yapi.guohanlin.com/
YAPI_TOKEN=你的项目token
YAPI_PROJECT_ID=你的项目ID
```

## 核心执行方式：用 Bash 调内置脚本

**所有 Yapi 调用都通过执行 SKILL 内置的 `scripts/yapi_fetch.py` 脚本完成**，禁止改用 MCP 工具、改用 curl、改用 WebFetch 重新实现一遍。脚本已经处理了 .env 加载、URL 拼接、错误重试、JSON 解析等所有细节。

脚本支持的 action（与 YAPI-OPENAPI.md 一一对应）：

| action | 用途 | 必传参数 |
|--------|------|----------|
| `project_info` | 获取项目基本信息 | 无 |
| `cat_menu` | 获取项目分类菜单 | 无 |
| `interface_menu` | 获取项目接口菜单树（含分类及接口） | 无 |
| `category_interfaces` | 获取某个分类下的接口列表 | `--catid <int>` |
| `interface_detail` | 根据接口 ID 获取完整详情 | `--id <int>` |
| `interface_by_path` | 根据接口路径精确查找接口 | `--path <string>`，`--method <string>` 可选 |
| `search` | 按关键词模糊搜索接口（基于 interface_menu 过滤） | `--keyword <string>` |

### 调用模板

```bash
# 用 .env 默认查找（从 CWD 向上）
python3 .claude/skills/yapi-skill/scripts/yapi_fetch.py \
  --action interface_by_path \
  --path "/api/user/info" \
  --method GET

# 用户指定了 .env 路径
python3 .claude/skills/yapi-skill/scripts/yapi_fetch.py \
  --env /path/to/project/.env \
  --action interface_detail \
  --id 4396

# 关键词搜索
python3 .claude/skills/yapi-skill/scripts/yapi_fetch.py \
  --action search \
  --keyword "用户登录"
```

脚本会把 Yapi 原始 JSON 输出到 stdout（带 `errcode / errmsg / data` 三段），把错误信息也以 JSON 形式输出，**LLM 应直接解析这段 JSON 作为接口定义**。

> **路径说明**：脚本路径相对项目根目录（`.claude/skills/yapi-skill/scripts/yapi_fetch.py`）。如果当前不在项目根目录，应使用绝对路径或用 `cd` 切到项目根后再执行。

## 接口定义拉取工作流

### Step 1：明确要拉取哪些接口

根据用户描述，提取出"接口列表"。判定规则：

| 用户表达 | 识别出的接口 |
|---------|-------------|
| "登录接口"、"用户信息接口"、"订单列表" | 1 个接口（按功能描述） |
| "用户模块的增删改查" | 4 个接口（增、删、改、查） |
| "用户管理" / "用户中心" | 列出该业务域所有接口（先用 `interface_menu` 全量，再用关键词过滤） |
| "/api/user/info" | 1 个接口（路径已知） |
| "接口 ID 4396" | 1 个接口（ID 已知） |

> **重要**：先把"要查的接口集合"列清楚，再去查。不要边查边猜。

### Step 2：定位接口（按优先级选择 action）

| 已知信息 | 推荐 action | 说明 |
|---------|-----------|------|
| 接口路径（最常见） | `interface_by_path` | 精确匹配，path 必须以 `/` 开头 |
| 接口标题 / 关键词 | `search` | 支持模糊匹配 title/path/method |
| 接口 ID | `interface_detail` | 直接按 ID 拿详情 |
| 不知道具体接口 | `interface_menu` 或 `cat_menu` | 先看全量分类和接口列表 |

### Step 3：拉取完整定义

定位到接口后，**必须用 `interface_detail` 或 `interface_by_path` 拉取完整 JSON**，而不是只展示 `interface_menu` 里的简略信息。

`interface_menu` / `cat_menu` / `category_interfaces` / `search` 只返回 `_id / title / path / method / status` 等概要信息，**缺少 `req_body_*` / `res_body` / `req_query` 等关键字段**，无法用于代码生成。

### Step 4：批量接口处理

如果要查多个接口，**多次执行脚本**（LLM 应在同一个 turn 内并行发起多次 Bash 调用，标准库实现，并发无副作用）：

- **能用 path 精确定位的**：每个接口跑一次 `interface_by_path`
- **只能用关键词搜的**：先 `search` 拿到 ID 列表，再对每个 ID 跑 `interface_detail`
- **最终回传**：把所有接口的完整 JSON 合并到数组里回传

并发数量建议：单次最多 5 个并行调用，避免触发 Yapi 限流。

## JSON 回传规范

回传给 LLM 的数据**必须是 Yapi 原始 JSON 格式**，不要重新组织结构、不要丢字段、不要自己改名。

### 单个接口回传格式

直接原样透传脚本输出（Yapi 原始格式）：

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": {
    "_id": 4396,
    "title": "用户信息",
    "path": "/api/user/info",
    "method": "GET",
    "req_body_type": "json",
    "res_body_type": "json",
    "res_body": "{\"errcode\":0,\"errmsg\":\"成功\",\"data\":{...}}",
    "req_body_form": [...],
    "req_params": [...],
    "req_headers": [...],
    "req_query": [...],
    "status": "done"
  }
}
```

### 多个接口回传格式

把每个接口的 `data` 字段收集成数组：

```json
{
  "interfaces": [
    { "接口1完整data": {...} },
    { "接口2完整data": {...} }
  ]
}
```

### 回传后必须说明

在 JSON 之后向用户简要说明：
- 拉到了哪些接口（接口名 + 路径 + 方法）
- 关键字段（请求参数 / 返回结构）的位置
- 接口状态（done / undone），提醒用户 undone 的接口定义可能不完整
- 如果有接口查询失败，明确指出是哪个接口、失败原因

## 注意事项

### 必须遵守

1. **永远用脚本**：所有 Yapi 调用都必须通过 `scripts/yapi_fetch.py`，禁止用 `mcp__yapi-mcp__*` 系列工具替代
2. **永远拿 detail 不用 list**：`interface_menu` / `cat_menu` / `category_interfaces` / `search` 只用于定位 ID，不作为最终回传数据
3. **保留原始 JSON**：`res_body` 字段是字符串化的 JSON，不要二次解析后再序列化
4. **失败重试一次**：脚本返回非 0 退出码或 `errcode != 0` 时，单个接口调用可重试 1 次，仍失败则报错并列出已成功的接口

### 禁止行为

- ❌ 不要在 .env 中读取到空值时继续硬猜配置，先停下来让用户补全
- ❌ 不要为了图省事只回传 list 的概要信息给用户（用户拿这个无法实现代码）
- ❌ 不要把多个接口的 detail 合并成一个 object（必须用 array 保持接口独立性）
- ❌ 不要修改字段名（如把 `req_query` 改成 `query`），保持 Yapi 原生字段名
- ❌ 不要重新发明轮子（用 curl 重新实现一遍 Yapi 调用逻辑）

## 快速执行模板

收到用户调用 `yapi-skill` 后，标准执行顺序：

```
1. 解析用户需求 → 列出"要查的接口集合"
2. 对每个接口：
   - 知道 path → 跑 interface_by_path
   - 知道 ID  → 跑 interface_detail
   - 知道关键词 → 跑 search 拿到 ID，再跑 interface_detail
3. 合并所有 data 字段 → 组成 interfaces 数组
4. 简要说明：拉到了哪些接口、关键字段在哪、状态是否 done
```

## 后续工作（不在本 SKILL 范围内）

拿到 JSON 之后，LLM 应根据用户的实际项目类型（Flutter / React / Spring Boot）按对应规范生成代码：

- Flutter → 遵循 `~/.claude/rules/flutter/network.md` 等规范
- React → 遵循 `~/.claude/rules/react/network.md` 等规范
- Spring Boot → 遵循用户 CLAUDE.md 中的"后端代码架构"规范

本 SKILL **不**负责代码生成，**只**负责接口定义数据的获取与回传。
