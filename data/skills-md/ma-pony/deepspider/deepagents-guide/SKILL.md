---
name: deepagents-guide
description: DeepAgents JS 框架使用指南，包含 Agent 创建、后端存储、子代理、中间件、技能和人机交互配置。
---

# DeepAgents JS 使用指南

## 概述

DeepAgents 是基于 LangGraph 的 Agent 框架，提供：
- 模块化中间件架构
- 多种后端存储方案
- 子代理任务委派
- 人机交互审批流程
- 长期记忆持久化
- 技能系统

## 快速开始

### 安装

```bash
npm install deepagents @langchain/core @langchain/anthropic zod
```

### 基础 Agent

```typescript
import { createDeepAgent, StateBackend } from "deepagents";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

// 定义工具
const myTool = tool(
  async ({ input }) => {
    return `处理结果: ${input}`;
  },
  {
    name: "my_tool",
    description: "工具描述",
    schema: z.object({
      input: z.string().describe("输入参数"),
    }),
  }
);

// 创建 Agent
const agent = createDeepAgent({
  name: "my-agent",
  model: "claude-sonnet-4-20250514",
  tools: [myTool],
  systemPrompt: "你是一个助手。",
  backend: new StateBackend(),
});

// 调用
const config = { configurable: { thread_id: "session-1" } };
const result = await agent.invoke(
  { messages: [{ role: "user", content: "你好" }] },
  config
);
```

## 后端存储

### StateBackend（默认）

临时存储，数据保存在 Agent 状态中，线程结束后丢失。

```typescript
import { StateBackend } from "deepagents";

const agent = createDeepAgent({
  backend: new StateBackend(),
});
```

### FilesystemBackend

基于本地文件系统的持久化存储。

```typescript
import { FilesystemBackend } from "deepagents";

const agent = createDeepAgent({
  backend: new FilesystemBackend({
    rootDir: "./agent-data",
  }),
});
```

### StoreBackend

基于 LangGraph Store 的持久化存储，支持跨线程访问。

```typescript
import { StoreBackend } from "deepagents";
import { InMemoryStore } from "@langchain/langgraph-checkpoint";

const store = new InMemoryStore();

const agent = createDeepAgent({
  store,
  backend: (config) => new StoreBackend(config),
});
```

### CompositeBackend（混合存储）

组合多个后端，按路径前缀路由。

```typescript
import { CompositeBackend, StateBackend, StoreBackend } from "deepagents";

const agent = createDeepAgent({
  store: new InMemoryStore(),
  backend: (config) => new CompositeBackend(
    new StateBackend(config),           // 默认：临时存储
    { "/memories/": new StoreBackend(config) }  // /memories/ 路径：持久化
  ),
});
```

**路径路由规则：**
- `/memories/*` → 持久化存储（跨线程）
- 其他路径 → 临时存储（仅当前线程）

## 中间件

`createDeepAgent` 默认附加三个中间件：
- `TodoListMiddleware` - 任务规划
- `FilesystemMiddleware` - 文件操作
- `SubAgentMiddleware` - 子代理委派

### TodoList 中间件

提供 `write_todos` 工具用于任务管理。

```typescript
import { createAgent, todoListMiddleware } from "langchain";

const agent = createAgent({
  model: "claude-sonnet-4-20250514",
  middleware: [
    todoListMiddleware({
      systemPrompt: "使用 write_todos 工具来...",
    }),
  ],
});
```

### Filesystem 中间件

提供四个文件操作工具：
- `ls` - 列出文件
- `read_file` - 读取文件
- `write_file` - 创建文件
- `edit_file` - 编辑文件

```typescript
import { createFilesystemMiddleware } from "deepagents";

const agent = createAgent({
  middleware: [
    createFilesystemMiddleware({
      backend: undefined,  // 可选自定义后端
      systemPrompt: "当需要保存信息时写入文件系统...",
      customToolDescriptions: {
        ls: "使用 ls 工具来...",
        read_file: "使用 read_file 工具来...",
      },
    }),
  ],
});
```

### SubAgent 中间件

启用任务委派给专门的子代理。

```typescript
import { createSubAgentMiddleware } from "deepagents";

const agent = createAgent({
  middleware: [
    createSubAgentMiddleware({
      defaultModel: "claude-sonnet-4-20250514",
      defaultTools: [],
      subagents: [
        {
          name: "weather",
          description: "获取城市天气信息",
          systemPrompt: "使用 get_weather 工具获取天气",
          tools: [getWeather],
          model: "gpt-4o",  // 可选：覆盖默认模型
        },
      ],
    }),
  ],
});
```

## 子代理 (Subagents)

子代理用于任务委派，保持主代理上下文清洁。

### 使用场景

**适合使用：**
- 多步骤任务（避免主上下文膨胀）
- 需要专门指令/工具的领域
- 需要不同模型能力的任务

**不适合：**
- 简单单步任务
- 需要中间上下文的场景

### 字典式子代理

```typescript
const researchSubagent = {
  name: "research-agent",
  description: "深度研究问题",
  systemPrompt: "你是一个优秀的研究员",
  tools: [internetSearch],
  model: new ChatAnthropic({ model: "claude-sonnet-4-20250514" }),
};

const agent = createDeepAgent({
  model: new ChatAnthropic({ model: "claude-sonnet-4-20250514" }),
  subagents: [researchSubagent],
});
```

### CompiledSubAgent

使用预构建的 LangGraph 图作为子代理：

```typescript
import { CompiledSubAgent } from "deepagents";

const customSubagent: CompiledSubAgent = {
  name: "data-analyzer",
  description: "复杂数据分析任务",
  runnable: customGraph.compile(),
};
```

### 通用子代理

DeepAgents 自动提供 `general-purpose` 子代理：
- 共享主代理的系统提示
- 访问相同工具
- 用于上下文隔离

## 人机交互 (Human-in-the-Loop)

配置敏感工具需要人工审批。

### 配置

```typescript
import { MemorySaver } from "@langchain/langgraph";

const agent = createDeepAgent({
  model: "claude-sonnet-4-20250514",
  tools: [deleteFile, sendEmail],
  interruptOn: {
    delete_file: true,
    send_email: { allowedDecisions: ["approve", "reject"] },
  },
  checkpointer: new MemorySaver(),  // 必需！
});
```

### 决策类型

- `approve` - 使用原参数执行
- `edit` - 修改参数后执行
- `reject` - 跳过工具调用

### 处理中断

```typescript
import { Command } from "@langchain/langgraph";

let result = await agent.invoke({
  messages: [{ role: "user", content: "删除 temp.txt" }]
}, config);

if (result.__interrupt__) {
  const decisions = [{ type: "approve" }];
  result = await agent.invoke(
    new Command({ resume: { decisions } }),
    config
  );
}
```

## 长期记忆

使用 `CompositeBackend` 实现跨线程持久化。

### 配置

```typescript
const agent = createDeepAgent({
  store: new InMemoryStore(),
  backend: (config) => new CompositeBackend(
    new StateBackend(config),
    { "/memories/": new StoreBackend(config) }
  ),
});
```

### 跨线程访问

```typescript
// 线程 1: 写入
await agent.invoke({
  messages: [{ role: "user", content: "保存偏好到 /memories/prefs.txt" }],
}, { configurable: { thread_id: "thread-1" } });

// 线程 2: 读取（不同会话）
await agent.invoke({
  messages: [{ role: "user", content: "读取我的偏好" }],
}, { configurable: { thread_id: "thread-2" } });
```

### 用例

- **用户偏好**: `/memories/user_preferences.txt`
- **自改进指令**: `/memories/instructions.txt`
- **知识库**: `/memories/research/notes.txt`

## 技能系统 (Skills)

技能是可复用的 Agent 能力，遵循 Agent Skills 标准。

### 目录结构

```
skills/
├── langgraph-docs/
│   └── SKILL.md
└── arxiv_search/
    ├── SKILL.md
    └── arxiv_search.ts
```

### SKILL.md 格式

```markdown
---
name: skill-name
description: 技能描述
---

# 技能标题

详细使用说明...
```

### 配置技能

```typescript
const agent = await createDeepAgent({
  skills: ["/skills/"],
});
```

### 技能 vs 工具

| 场景 | 选择 |
|------|------|
| 大量上下文需要减少 token | 技能 |
| 多能力捆绑 | 技能 |
| 简单原子操作 | 工具 |

## 最佳实践

### 子代理描述

```typescript
// ✅ 好
"分析财务数据并生成投资建议"

// ❌ 差
"处理财务"
```

### 最小化工具集

```typescript
// ✅ 好: 专注
const emailAgent = {
  name: "email-sender",
  tools: [sendEmail, validateEmail],
};

// ❌ 差: 分散
tools: [sendEmail, webSearch, databaseQuery]
```

### 按任务选模型

```typescript
const subagents = [
  { name: "contract-reviewer", model: "claude-sonnet-4-20250514" },
  { name: "quick-lookup", model: "gpt-4o-mini" },
];
```

### 生产环境存储

```typescript
import { PostgresStore } from "@langchain/langgraph-checkpoint-postgres";

const store = new PostgresStore({
  connectionString: process.env.DATABASE_URL,
});
```

## 参考链接

- [DeepAgents 文档](https://docs.langchain.com/oss/javascript/deepagents)
- [LangGraph JS](https://langchain-ai.github.io/langgraphjs/)
- [Agent Skills 标准](https://agentskills.io/)
