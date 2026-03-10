---
name: staged-review-validator
description: Validate staged-changes-review findings with evidence-based verdicts and minimal-fix guidance. Use when you need to confirm whether each reported issue is valid and actionable.
metadata:
  author: adonis
---

# Staged Review Validator

用于对已有审查报告做二次验证，不负责重新发起完整扫描。

## 何时使用

- 用户已经有一份 `staged-changes-review` 结果，想确认每条问题是否真实成立
- 用户问“这个问题到底要不要改”
- 用户希望获得“逐条裁决 + 证据 + 修改建议”

## 输入契约

### 必需输入

- 用户提供一段 `staged-changes-review` 文本（至少包含问题描述）

### 推荐输入

- 文件路径
- 行号
- 风险级别
- 置信度
- 原始建议

### 缺失输入处理

如果用户没有粘贴审查结果：

1. 明确提示“请先粘贴 staged-changes-review 结果”
2. 提供一个最小输入模板（见 `references/output-template.md`）
3. 不自动改为扫描 `git diff --cached`

## 核验流程

### 1. 解析问题清单

从用户提供的报告提取每条问题：

- 标题
- 文件与行号
- 原风险级别
- 原置信度
- 原建议

### 2. 逐条证据核验

对每条问题进行核验：

- 文件/行号是否存在
- 代码上下文是否匹配问题描述
- 该问题是否已经在当前变更中修复
- 是否存在上下文导致“看似问题但实际合理”

可使用但不限于以下命令：

```bash
git diff --cached
rg -n "关键符号" <path>
sed -n '<start>,<end>p' <path>
git show HEAD:<path>
```

### 3. 给出裁决

每条问题只能输出以下三种之一：

- `成立`：证据直接支持问题描述
- `不成立`：证据与描述冲突，或问题已修复
- `待确认`：证据不足（路径/行号缺失、上下文不完整等）

### 4. 推导“是否需要修改”

- `成立` 且风险为中/高：`需要修改`
- `成立` 且风险低：`建议修改`
- `不成立`：`不需要修改`
- `待确认`：`暂不修改，先补充信息`

## 输出要求（固定）

先给总览，再给逐条裁决。

### 总览

- 问题总数
- 成立数
- 不成立数
- 待确认数
- 建议修改数

### 逐条裁决块（每条必含）

- 问题标题
- 文件位置
- 风险级别
- 置信度
- 裁决（成立/不成立/待确认）
- 是否需要修改（是/否/待补充）
- 证据（命令结果或代码定位）
- 最小改动建议

结尾给出编号式“可执行下一步”。

## 与 staged-changes-review 的关系

- `staged-changes-review`：发现候选问题
- `staged-review-validator`：验证候选问题是否真实成立

串联时，后者不重复完整扫描逻辑，重点做证据核验与裁决。

## 参考文档

- `references/verification-rubric.md`：裁决标准、证据优先级、置信度映射
- `references/output-template.md`：固定输出模板与示例
