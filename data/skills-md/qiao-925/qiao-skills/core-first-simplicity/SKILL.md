---
name: core-first-simplicity
description: 基于 KISS（Keep It Simple, Stupid）与“最小光辉点”的复杂度控制原则。用于项目、系统、模块、代码、函数各层级的设计与实现决策，帮助优先核心价值、减少非必要复杂度、避免过度设计。关键词：KISS、简化、聚焦、复杂度控制、最小光辉点。
metadata:
  type: declarative
  category: complexity-principle
  scope: generic
  role: primary-principle
---

# 核心优先简化原则

> 用最小必要复杂度实现最大核心价值。

---

## ⚠️ 核心强制要求

### 1) 核心优先

- 任何设计都先回答：当前任务最重要的核心价值是什么？
- 无法直接强化核心价值的设计，默认不做或延后。

### 2) KISS 默认优先

- 有两种可行方案时，默认选择更简单、可验证、可维护的一种。
- 不为“未来可能需要”提前引入复杂抽象。

### 3) 复杂度准入门槛

仅当同时满足以下条件，才允许增加复杂度：

1. 直接提升核心目标达成率。
2. 存在明确证据（性能瓶颈、稳定性问题、用户痛点）。
3. 复杂度可被局部封装，不扩散到全局。

### 4) 砍掉与延后

- 锦上添花但不影响核心价值：延后。
- 增加认知负担且收益不明确：砍掉。
- 没有完美方案时，优先“刚好能用”的可迭代版本。

---

## AI Agent 行为要求

### 设计前（必问）

1. 如果只能保留一个能力，应该保留什么？
2. 当前方案是否比上一版更复杂？复杂度收益比是否成立？
3. 是否存在更直接、更短路径的实现？

### 实施中（必做）

- 对每个新增模块/抽象说明其核心价值贡献。
- 若无法明确贡献，主动提出“删除或延后”建议。
- 当用户追求大而全时，优先提供“最小可行实现 + 后续迭代路径”。

### 评审时（必检）

- 是否出现了与核心目标无关的复杂度扩张。
- 是否可以通过减少层级/减少分支/减少接口来简化。
- 是否保留了清晰的默认路径（happy path）。

---

## 分层落地（Progressive Disclosure）

- `references/project-level.md`：项目级聚焦与取舍
- `references/system-level.md`：系统级复杂度预算与架构简化
- `references/module-level.md`：模块级边界与依赖简化
- `references/code-level.md`：代码级结构与抽象简化
- `references/function-level.md`：函数级控制流与职责简化

---

## 反模式（必须避免）

- 为“以后可能会用”而提前设计复杂结构。
- 用高抽象掩盖尚未稳定的需求。
- 同时推进多个非核心优化导致主线停滞。
- 在没有证据时引入中间层、配置层、插件层。

---

## 参考资料

- KISS principle（背景）：https://en.wikipedia.org/wiki/KISS_principle
- `references/project-level.md` - 项目级落地
- `references/system-level.md` - 系统级落地
- `references/module-level.md` - 模块级落地
- `references/code-level.md` - 代码级落地
- `references/function-level.md` - 函数级落地
