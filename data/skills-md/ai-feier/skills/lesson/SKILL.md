---
name: lesson
description: "Use when user mentions '/lesson', '记录经验', '铁律', or wants to capture lessons learned. Automatically extracts insights from conversation and writes them to project's MEMORY.md. Also triggers when agent makes mistakes or discovers important patterns."
---

# Lesson Skill — 铁律捕获

## Overview

自动从对话中提取踩坑经验和关键教训，写入项目的 `MEMORY.md`。

## Prerequisites

- 项目根目录需要有 `MEMORY.md` 文件
- 如果没有，运行安装脚本自动创建

## Installation

```bash
# 自动安装（如果项目没有 MEMORY.md）
curl -sL https://raw.githubusercontent.com/Ai-feier/skills/main/docs/INSTALL.sh | bash
```

## Usage

### 触发方式

1. 显式命令：`/lesson`、`记录经验`、`铁律`
2. Agent 自动检测到重要经验时

### 写入内容

- 开发规范
- 调试经验
- 工具配置
- 代码风格
- 任何值得记录的经验

## 示例

```
You: 这个项目的 API 总是返回 401，可能是我 token 过期了
Agent: 记录下来，写入 MEMORY.md
```

会写入：
```markdown
## 调试经验

- 401 错误通常是 token 过期，检查 Auth 头部
```
