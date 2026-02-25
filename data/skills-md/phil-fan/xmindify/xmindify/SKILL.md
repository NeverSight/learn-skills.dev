---
name: xmindify
description: XMindify 思维导图生成器，支持场景化模板和自动生成。用于创建 XMindMark 文件并转换为 XMind/SVG 格式。触发场景：(1) 用户要求创建思维导图 (2) 用户需要分析论文/总结内容/头脑风暴 (3) 用户提到"思维导图"、"脑图"、"结构化"等词汇
compatibility: requires xmindmark CLI (install via pnpm install -g xmindmark)
---

# XMindify 思维导图生成器

## 前置检查

执行前先检查 xmindmark CLI 是否已安装：

```bash
xmindmark --version
```

如果未安装，提醒用户运行：

```bash
npm install -g xmindmark
```

```bash
pnpm install -g xmindmark
```


## 工作流程

### 场景路由

根据用户需求选择合适的场景模板：

| 用户意图 | 场景文件 | 触发关键词 |
|---------|---------|-----------|
| 分析学术论文 | [paper.md](scenarios/paper.md) | 论文、学术、research、paper |
| 总结长篇内容 | [summary.md](scenarios/summary.md) | 总结、提炼、梳理、要点 |
| 创意构思/发散思维 | [brainstorm.md](scenarios/brainstorm.md) | 头脑风暴、创意、想法、方案 |
| 问题分析/决策 | [analysis.md](scenarios/analysis.md) | 分析、问题、决策、对比 |
| 项目规划 | [project.md](scenarios/project.md) | 项目、计划、规划、roadmap |
| 无特定场景 | 自动生成 | 根据内容智能推断 |

### 执行步骤

1. **确定场景** - 根据用户意图选择预设模板或自动生成
2. **生成 XMindMark** - 按 [SYNTAX.md](references/SYNTAX.md) 语法创建 `.xmindmark` 文件
3. **转换导出** - 使用 CLI 转换为 XMind 和 SVG

## XMindMark 转换命令

```bash
# 转换为 XMind 文件
xmindmark -f xmind -o output topic.xmindmark

# 转换为 SVG 图片
xmindmark -f svg -o output topic.xmindmark
```

或使用转换脚本：

```bash
./scripts/convert.sh topic.xmindmark output/
```

## 场景模板使用

每个场景模板包含：

- 结构框架（中心主题、主分支层级）
- 常用模式（边界、关联、总结的使用）
- 示例用法

## 语法参考

查看 [SYNTAX.md](references/SYNTAX.md) 了解完整语法。

## 自动生成模式

当用户需求不匹配预设场景时：

1. **提取中心主题** - 从用户输入中识别核心话题
2. **分析内容结构** - 识别关键维度和层次关系
3. **智能组织** - 根据内容类型自动选择最佳组织方式（时间、类别、优先级等）
4. **添加视觉元素** - 适当使用边界分组���关联连接、总结节点

## 全局规则

### 关联 (Relationship) 使用限制

- **最多使用 2 个连接对** - 即最多使用 `[1]`/`[^1]` 和 `[2]`/`[^2]`
- 只连接最重要的因果关系（如：洞察→贡献、挑战→解决方案）
- 避免过度使用关联，保持思维导图清晰

### 边界 (Boundary) 使用限制

- **最多使用 2 个边界** - 即最多使用 `[B1]`/`[B2]`
- 只使用边界分组最重要的概念（如：概念1、概念2、概念3）
- 尽量不用嵌套的边界（如：`[B1][B2]`）

### 结构规范

- 每个主分支控制在 3-7 个子节点
- 层级深度不超过 4 层
- 使用 `[B]` 将相关节点逻辑分组
- 使用 `[S]` 创建可展开的总结节点

### 语法规范

- 1 Tab = 4 空格
- `[]` 标记后不能有空格（在主题内容后）
- 同级子主题之间的空行会被忽略

## 最佳实践

1. **简洁优先** - 思维导图用于提炼要点，不是复制全文
2. **层次清晰** - 中心主题 → 主分支 → 子分支 → 细节
3. **逻辑分组** - 使用边界 `[B]` 将相关概念归类
4. **关键连接** - 仅用 1-2 个关联标记最核心的逻辑关系
5. **总结提炼** - 使用 `[S]` 汇总关键结论或局限性
