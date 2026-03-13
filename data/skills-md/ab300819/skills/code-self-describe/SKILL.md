---
name: code-self-describe
description: Generate and maintain self-describing code structure with module-level CLAUDE.md files and source file header comments (INPUT/OUTPUT/POS). Supports init, update, and audit modes. Use when users want to add AI-friendly code descriptions, improve code navigation, or maintain code documentation. Triggers on keywords like "self-describe", "code description", "CLAUDE.md", "自描述", "代码描述", "模块描述", "生成描述".
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, AskUserQuestion
---

# 代码自描述

为代码库生成和维护自描述结构，利用 Claude Code 的层级加载机制实现渐进式上下文理解。

## 语言规则

- 支持中英文提问
- 统一中文回复
- CLAUDE.md 文件内容使用中文
- 源文件头部注释使用中文

## 触发条件

- 用户需要为项目添加 AI 友好的代码描述
- 用户需要在代码变更后更新描述
- 用户需要检查描述覆盖率和准确性
- 关键词："自描述"、"模块描述"、"生成 CLAUDE.md"、"self-describe"

## 核心概念

### 自分形架构

利用 Claude Code 的**分级加载机制**（搜索到文件时自动加载所在目录的 CLAUDE.md），通过三层自描述结构提升 AI 的代码理解：

```
项目根 CLAUDE.md ← 全局视图
    │
    ├── src/modules/auth/CLAUDE.md ← 模块视图
    │   ├── auth.service.ts  ← 文件头部 INPUT/OUTPUT/POS
    │   ├── auth.guard.ts
    │   └── auth.controller.ts
    │
    └── src/modules/user/CLAUDE.md ← 模块视图
        ├── user.service.ts
        └── user.repository.ts
```

AI 搜索到第五层文件时，已自动加载前四层 CLAUDE.md，对整个模块的了解无比清晰。

### 三层描述体系

| 层级 | 载体 | 内容 |
|------|------|------|
| 项目级 | 根 CLAUDE.md | 模块列表、全局约束 |
| 模块级 | 目录 CLAUDE.md | 地位、逻辑、约束、业务域清单 |
| 文件级 | 源码头部注释 | INPUT、OUTPUT、POS |

### 与代码追溯标注的关系

自描述和 DevDocs 追溯标注服务于不同维度，两者共存互补：

| 维度 | 自描述 (INPUT/OUTPUT/POS) | 追溯标注 (@requirement/@satisfies) |
|------|--------------------------|-----------------------------------|
| 目的 | 帮助 AI 理解模块结构和依赖 | 追踪需求实现状态 |
| 粒度 | 文件级 | 方法/函数级 |
| 维度 | 架构理解（模块做什么） | 需求追溯（为什么做） |
| 更新时机 | 代码结构变更时 | 需求实现/变更时 |
| 位置 | 文件最开始 | 具体的类/函数/方法上方 |

## 运行模式

```
/code-self-describe                         → 智能检测模式
/code-self-describe --init                  → 初始化：为项目生成完整自描述结构
/code-self-describe --init src/modules/auth → 初始化指定模块
/code-self-describe --update                → 更新：根据代码变更更新描述
/code-self-describe --update src/user.ts    → 更新指定文件及其所在模块
/code-self-describe --audit                 → 审计：检查描述新鲜度和准确性
```

### 模式对比

| 模式 | 扫描范围 | 生成 CLAUDE.md | 更新头部注释 | 用户确认 |
|------|---------|---------------|-------------|---------|
| init | 全项目/指定模块 | ✅ 新建 | ✅ 新增 | ✅ 逐模块 |
| update | 变更文件 (git diff) | ✅ 更新现有 | ✅ 更新变更 | 低风险自动 |
| audit | 全项目 | ❌ 仅报告 | ❌ 仅报告 | ❌ |

### 智能检测流程

```
检测项目是否已有模块级 CLAUDE.md
        │
        ├── 无 → 自动进入 init 模式
        │
        └── 有 → 检测是否有代码变更
                │
                ├── 有未同步变更 → 建议 update 模式
                └── 无变更 → 建议 audit 模式
```

## Init 模式

### 工作流程

```
1. 扫描项目结构
   ├── 识别语言/框架（package.json, go.mod, Cargo.toml 等）
   ├── 识别目录结构模式（src/, lib/, modules/ 等）
   └── 识别业务模块边界
           │
           ▼
2. 增强项目根 CLAUDE.md
   ├── 已存在：追加模块描述章节（不覆盖现有内容）
   └── 不存在：生成基础 CLAUDE.md
           │
           ▼
3. 逐模块生成 CLAUDE.md
   ├── 分析模块内文件的导入/导出关系
   ├── 识别模块角色（服务层、数据层、接口层等）
   ├── 生成 CLAUDE.md（地位/逻辑/约束/业务域清单）
   └── 用户确认每个模块的描述
           │
           ▼
4. 逐文件生成头部注释
   ├── 分析 import/依赖关系 → INPUT
   ├── 分析 export/公开接口 → OUTPUT
   ├── 根据目录位置和模块角色 → POS
   └── 插入文件头部注释
           │
           ▼
5. 生成描述清单报告
```

### 模块级 CLAUDE.md 模板

> 详细模板和示例见 [templates/claude-md-template.md](templates/claude-md-template.md)

```markdown
# <模块名>

## 地位
<在系统中的角色和位置，1-2 句话>

## 逻辑
<模块做什么，核心功能描述，3-5 句话>

## 约束
- <使用规则>
- <依赖限制>

## 业务域清单
| 文件/子模块 | 职责 |
|-------------|------|
| `xxx.ts` | <职责描述> |
```

### 源文件头部注释格式

> 多语言示例见 [templates/header-comment-examples.md](templates/header-comment-examples.md)

```typescript
// INPUT: UserRepository (数据访问), ValidatorService (校验)
// OUTPUT: createUser(), getUser(), updateUser() (用户 CRUD 操作)
// POS: 用户模块核心服务层，处理用户业务逻辑
```

**注释必须放在文件最开始**（在 import 语句之前），因为 AI 加载文件从头部开始。

## Update 模式

### 工作流程

```
1. 检测变更范围
   ├── git diff --name-only（对比上次提交）
   ├── 或用户指定文件/目录
   └── 识别受影响的模块
           │
           ▼
2. 分析变更影响
   ├── 文件级：INPUT/OUTPUT 是否变化
   ├── 模块级：模块职责是否变化
   └── 跨模块：模块间依赖是否变化
           │
           ▼
3. 更新源文件头部注释
   ├── 更新变更文件的 INPUT/OUTPUT/POS
   └── 保留手动添加的额外注释
           │
           ▼
4. 更新模块 CLAUDE.md
   ├── 更新业务域清单（新增/删除文件）
   ├── 更新逻辑描述（如模块职责变化）
   └── 更新约束（如新增依赖规则）
           │
           ▼
5. 向上传播更新
   ├── 子模块变更 → 更新父模块 CLAUDE.md
   └── 直到项目根 CLAUDE.md 为止
```

### 更新传播规则

> 详细规则见 [templates/update-rules.md](templates/update-rules.md)

- **仅在公共接口变化时向上传播**（内部重构不触发）
- **标记区分自动/手动内容**（`<!-- auto-generated -->` 标记自动生成部分）
- **不修改手动编写的描述**

## Audit 模式

### 审计内容

```
1. 扫描所有 CLAUDE.md 和源文件头部注释
2. 对比实际代码状态
3. 生成审计报告：
   ├── 缺失描述的模块/文件
   ├── 过期描述（代码已变更但描述未更新）
   ├── 不准确描述（INPUT/OUTPUT 与实际不符）
   └── 描述覆盖率统计
```

### 审计报告格式（终端输出）

```
📊 代码自描述审计报告

覆盖率:
  模块级 CLAUDE.md: 8/12 (67%)
  文件头部注释:     45/62 (73%)

⚠️  缺失描述:
  - src/modules/payment/CLAUDE.md (缺失)
  - src/services/cache.ts (无头部注释)

🔄 过期描述:
  - src/modules/user/CLAUDE.md (user.service.ts 新增了 deleteUser 方法)
  - src/auth/auth.guard.ts (INPUT 缺少 RoleService 依赖)
```

## 约束

### 生成约束

- [ ] **CLAUDE.md 文件名必须使用大写**（Claude Code 约定）
- [ ] **不覆盖已有的项目根 CLAUDE.md**（追加或合并）
- [ ] **模块级 CLAUDE.md 必须基于实际代码分析生成**
- [ ] **头部注释必须基于实际 import/export 分析**
- [ ] 不为空目录或配置目录生成 CLAUDE.md
- [ ] 不为第三方依赖目录生成描述（node_modules, vendor 等）

### 更新约束

- [ ] **只更新实际发生变化的文件**
- [ ] **不修改手动编写的描述内容**（通过标记区分）
- [ ] **向上传播仅在公共接口变化时触发**
- [ ] 更新前必须读取现有描述

### 审计约束

- [ ] **审计模式不修改任何文件**
- [ ] 必须生成覆盖率统计
- [ ] 必须标注过期描述的具体原因

### 范围约束

- [ ] **忽略隐藏目录**（.git, .vscode, .idea 等）
- [ ] **忽略构建产物**（dist/, build/, __pycache__/ 等）
- [ ] **忽略依赖目录**（node_modules/, vendor/, Pods/ 等）
- [ ] **忽略测试目录的 CLAUDE.md 生成**（测试文件仍生成头部注释）
- [ ] 可通过参数指定扫描范围

## Skill 协作

| 阶段 | 协作 Skill | 说明 |
|------|-----------|------|
| 开发完成后 | `/devdocs-dev-workflow` | 被调用：完成检查步骤中触发 --update |
| 重构后 | `/refactor` | 被调用：重构完成后更新描述 |
| 项目上下文 | `/devdocs-onboard` | 互补：CLAUDE.md 提供模块级上下文 |
| 代码追溯 | `/devdocs-sync` | 互补：不同维度的代码标注 |
| 文件操作 | `/git-safety` | 配合：模块移动/重命名时同步更新 CLAUDE.md |

## 参考资料

- [claude-md-template.md](templates/claude-md-template.md) - 模块级 CLAUDE.md 模板
- [header-comment-examples.md](templates/header-comment-examples.md) - 多语言头部注释示例
- [update-rules.md](templates/update-rules.md) - 层级更新传播规则
