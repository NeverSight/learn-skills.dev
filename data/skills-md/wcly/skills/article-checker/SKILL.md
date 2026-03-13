---
name: article-checker
description: 基于 LLM 的文章校对助手，检测错别字、病句、拼写错误、逻辑错误等问题
---

# article-checker

文章智能校验工具 - 基于 LLM 的文章校对助手

## Description

一个专业的文章校验技能，可以检测文章中的错别字、病句、拼写错误、逻辑错误、矛盾冲突、语句不通顺等问题，并提供修改建议。

## Triggers

- "文章校验"
- "检查文章"
- "校对文章"
- "文章查错"
- "proofread"
- "article check"

## How It Works

1. 用户输入待校验的文章内容
2. 技能加载 `references/rules.md` 中的检查规则
3. 构建 System Prompt 调用 LLM 进行校验
4. LLM 返回检查结果（JSON 格式）
5. 技能解析结果并呈现给用户
6. **（可选）用户选择自动修复功能**

### 自动修复功能

在校验报告呈现后，用户可以选择以下修复选项：

1. **修复所有问题** - 修复报告中检测到的所有问题
2. **仅修复严重问题** - 只修复 severity 为 high 的问题
3. **修复严重和一般问题** - 修复 severity 为 high 和 medium 的问题
4. **自定义选择** - 用户自行选择要修复的具体问题

用户选择修复选项后，技能会调用 LLM 进行修复，并返回：
- 修复的问题数量和详情
- 修复后的完整文章内容
- 未修复的问题及原因

## Requirements

- 支持 LLM 调用的环境（OpenAI / Claude / 本地模型等）
- 用户需要自行配置 LLM API

## References

- 详细规则说明: `references/rules.md`
- 报告模板: `assets/report-template.md`
- 安装说明: `README.md`

## Usage

```
请帮我校验以下文章：
[在此输入你的文章]
```

或者使用命令：
```
/article-checker
[在此输入你的文章]
```
