---
name: exploring-generative-ai
description: 使用 Martin Fowler 的 Exploring Generative AI 系列评估 coding assistant、agent 自主性、harness engineering（guides 与 sensors、feedback 与 feedforward、computational 与 inferential controls）、AI 辅助开发工作流、context engineering、本地 coding model 可行性或软件工程取舍时使用。
---

# Exploring Generative AI

**系列**：Martin Fowler, *Exploring Generative AI*
**来源**：31 篇官方系列文章（2023-07-26 至 2026-08-10）加 1 篇官方后续文章（ch32，由 ch26 链接而来）。ch26 原 memo 的 URL 已被官方重定向到其现在所概括的完整文章。

## 使用方式

- 需要做决策时先看 **Topic Index**；对某一篇文章的主张下结论前，先读它对应的整章。
- 快速做风险、自主性、context 或本地模型决策时用 `cheatsheet.md`；行动前读它引用的章节。
- 设计工作流或 harness 时用 `patterns.md`；术语不清楚时用 `glossary.md`。
- 把每章的来源 URL、作者、日期当作权威元数据。没有任何章节支撑的主张，要明说「未覆盖」。

## 核心决策规则

| 信号 | 默认动作 | 何时升级 | 读 |
|---|---|---|---|
| 输出看似合理但未经验证 | 加上最快的可信反馈：compiler、test、linter、review 或可观察的产物。 | 反馈慢、含糊或不可得。 | [ch06](chapters/6.md)、[ch08](chapters/8.md)、[ch12](chapters/12.md) |
| 出错概率高、影响大或可检测性低 | 不使用无人监督执行；缩小范围并要求人工 review。 | 涉及公共 API、安全边界、数据变更或生产行为。 | [ch16](chapters/16.md)、[ch19](chapters/19.md)、[ch21](chapters/21.md)、[ch27](chapters/27.md) |
| context 过期、过宽或引发猜测 | 刷新最小的相关 reference、specification 与 workspace 证据；去掉过期噪音。 | agent 无法可靠决定该加载什么 context。 | [ch09](chapters/9.md)、[ch22](chapters/22.md)、[ch25](chapters/25.md) |
| 反复出现的 agent 失误，影响半径在扩大 | 把缺失的判断或约束编码进可复用的 skill 或 harness control。 | 影响已到团队迭代或 codebase 生命周期级别。 | [ch13](chapters/13.md)、[ch24](chapters/24.md)、[ch26](chapters/26.md) |
| 考虑使用本地模型 | 按顺序实测 harness：内存适配、速度、工具调用、正确性、context、任务规模、review 负担。 | 任一更早阶段失败。 | [ch28](chapters/28.md)、[ch29](chapters/29.md) |
| 设计或改进 agent harness | 把 guides（feedforward）与 sensors（feedback）配对——只有 feedback 会重复犯错，只有 feedforward 从不验证规则；能上 computational 就优先，语义判断再补 inferential。 | 需要行为级置信度；sensors 从不触发；或 controls 互相矛盾。 | [ch26](chapters/26.md)、[ch32](chapters/32.md) |
| 反复出现的 agent 问题，改 prompt 仍不消失 | 去 steer harness 而不是 steer 输出：改进相关 guide 或 sensor，让问题更不可能发生。 | 问题是任何 sensor 都无法判断的行为正确性。 | [ch26](chapters/26.md)、[ch13](chapters/13.md) |
| 在 agent loop 内规定流程（如 TDD） | 与其给详细 how-to 指令，不如用 sensors 监控结果；先验证该流程机制在没有人参与步骤时仍然生效。 | 有 eval 或有力论证表明该流程可以迁移。 | [ch31](chapters/31.md)、[ch06](chapters/6.md) |
| agentic codebase 漂移（文件膨胀、单次变更 token 上升） | 主动重构——单次变更的 token 成本可测量、可回收；把最大文件和 files-touched 趋势当 drift sensors 跟踪。 | codebase 是一次性原型工作。 | [ch30](chapters/30.md)、[ch32](chapters/32.md) |

## 章节索引

| # | 文章 | 作者 |
|---|---|---|
| [1](chapters/1.md) | The toolchain | Birgitta Böckeler |
| [2](chapters/2.md) | Median - A tale in three functions | Birgitta Böckeler |
| [3](chapters/3.md) | In-line assistance - when is it more useful? | Birgitta Böckeler |
| [4](chapters/4.md) | In-line assistance - how can it get in the way? | Birgitta Böckeler |
| [5](chapters/5.md) | Coding assistants do not replace pair programming | Birgitta Böckeler |
| [6](chapters/6.md) | TDD with GitHub Copilot | Paul Sobocinski |
| [7](chapters/7.md) | How is GenAI different from other code generators? | Birgitta Böckeler |
| [8](chapters/8.md) | How to tackle unreliability of coding assistants | Birgitta Böckeler |
| [9](chapters/9.md) | Onboarding to a 'legacy' codebase with the help of AI | Birgitta Böckeler |
| [10](chapters/10.md) | Building an AI agent application to migrate a tech stack | Birgitta Böckeler |
| [11](chapters/11.md) | Expanding the solution size with multi-file editing | Birgitta Böckeler |
| [12](chapters/12.md) | What role does LLM reasoning play for software tasks? | Birgitta Böckeler |
| [13](chapters/13.md) | The role of developer skills in agentic coding | Birgitta Böckeler |
| [14](chapters/14.md) | Guiding an LLM for Robust Java ByteBuffer Code | Unmesh Joshi |
| [15](chapters/15.md) | Building TMT Mirror Visualization with LLM: A Step-by-Step Journey | Unmesh Joshi |
| [16](chapters/16.md) | Coding Assistants Threaten the Software Supply Chain | Jim Gumbley、Lilly Ryan |
| [17](chapters/17.md) | Building Custom Tooling with LLMs | Unmesh Joshi |
| [18](chapters/18.md) | Autonomous coding agents: A Codex example | Birgitta Böckeler |
| [19](chapters/19.md) | I still care about the code | Birgitta Böckeler |
| [20](chapters/20.md) | Partner with the AI, throw away the code | Matteo Vaccari |
| [21](chapters/21.md) | To vibe or not to vibe | Birgitta Böckeler |
| [22](chapters/22.md) | Anchoring AI to a reference application | Birgitta Böckeler |
| [23](chapters/23.md) | Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl | Birgitta Böckeler |
| [24](chapters/24.md) | Assessing internal quality while coding with an agent | Erik Doernenburg |
| [25](chapters/25.md) | Context Engineering for Coding Agents | Birgitta Böckeler |
| [26](chapters/26.md) | Harness engineering for coding agent users | Birgitta Böckeler |
| [27](chapters/27.md) | Humans and Agents in Software Engineering Loops | Kief Morris |
| [28](chapters/28.md) | Viability of local models for coding | Birgitta Böckeler |
| [29](chapters/29.md) | Experiences with local models for coding | Birgitta Böckeler |
| [30](chapters/30.md) | The Economic Benefit of Refactoring | Giles Edwards-Alexander |
| [31](chapters/31.md) | TDD inside the agent loop - theater or actual value? | Birgitta Böckeler |
| [32](chapters/32.md) | Maintainability sensors for coding agents（ch26 官方后续） | Birgitta Böckeler |

## Topic Index

- **AI 输出可能错误 / 不可靠**：[ch04](chapters/4.md)、[ch06](chapters/6.md)、[ch08](chapters/8.md)、[ch12](chapters/12.md)
- **agentic coding / harness engineering**：[ch13](chapters/13.md)、[ch18](chapters/18.md)、[ch24](chapters/24.md)、[ch26](chapters/26.md)、[ch27](chapters/27.md)、[ch32](chapters/32.md)
- **自主性、监督或高风险执行**：[ch16](chapters/16.md)、[ch18](chapters/18.md)、[ch19](chapters/19.md)、[ch21](chapters/21.md)、[ch27](chapters/27.md)
- **代码质量与 review 自满**：[ch04](chapters/4.md)、[ch05](chapters/5.md)、[ch19](chapters/19.md)、[ch24](chapters/24.md)
- **context 漂移 / reference application / context 加载**：[ch09](chapters/9.md)、[ch22](chapters/22.md)、[ch25](chapters/25.md)
- **guides（feedforward controls）**：[ch25](chapters/25.md)、[ch26](chapters/26.md)、[ch32](chapters/32.md)
- **sensors（feedback controls）/ self-correction guidance**：[ch08](chapters/8.md)、[ch26](chapters/26.md)、[ch32](chapters/32.md)
- **computational vs inferential controls**：[ch19](chapters/19.md)、[ch26](chapters/26.md)、[ch32](chapters/32.md)
- **cybernetic governor / steering loop / drift sensors**：[ch26](chapters/26.md)、[ch27](chapters/27.md)、[ch32](chapters/32.md)
- **harnessability / harness templates / regulation categories**：[ch26](chapters/26.md)
- **mutation testing / regression sensor**：[ch31](chapters/31.md)、[ch32](chapters/32.md)
- **重构经济学 / 单次变更的 token 成本**：[ch30](chapters/30.md)、[ch32](chapters/32.md)
- **TDD**：[ch06](chapters/6.md)、[ch14](chapters/14.md)、[ch31](chapters/31.md)
- **本地模型可行性**：[ch28](chapters/28.md)、[ch29](chapters/29.md)
- **原型 vs 生产**：[ch20](chapters/20.md)、[ch21](chapters/21.md)、[ch24](chapters/24.md)
- **风险评估 / vibe coding**：[ch19](chapters/19.md)、[ch21](chapters/21.md)
- **安全与供应链**：[ch16](chapters/16.md)
- **spec-driven development**：[ch23](chapters/23.md)

## 支持文件

- [glossary.md](glossary.md) — 精确术语与其来源章节。
- [patterns.md](patterns.md) — 工作流模式；设计 harness 或重复性 agent 流程前阅读。
- [cheatsheet.md](cheatsheet.md) — 决策表；选择自主性、处理 context 漂移或评估本地模型前阅读。

## 范围与边界

本 skill 覆盖官方系列索引所列 31 篇文章，加 1 篇官方后续文章（ch32），每篇在各自章节文件中注明 URL。ch26 的来源是完整的 Harness Engineering 文章，它正式取代并重定向了早前的 memo。本 skill 不把系列当作单作者的书：章节归属保持按文章区分。不得推断超出所引文章之外的主张。术语遵循作者原词；harness 词汇（guides、sensors、feedforward、feedback、computational、inferential）以 ch26 与 ch32 为规范来源。
