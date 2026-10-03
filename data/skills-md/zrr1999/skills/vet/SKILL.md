---
name: vet
description: >
  有证据的代码质量审查与清理，按范围分两种轨道：diff 级（写完代码/提交前清扫 AI 味：comment slop、防御性过度、过度抽象、幻觉 API、重复逻辑、泛泛命名、test theater，deletion-first 收敛到最小补丁）和仓库级（维护型技术债、architecture findings、测试/依赖/配置审计，以及公开发布/开源/v1.0/package publish 前的 release readiness 预检）。触发：deslop、去 AI 味、清理或 review 刚才的改动、提交前自查、PR diff 质量、技术债/质量/架构审计、开源前检查、Scorecard、REUSE。不用于正确性 bug 调试、纯安全渗透测试或设计未来方案；设计取舍与推进顺序交给 pilot，目标仓库自己的 review/ownership 指南优先。
---

# Vet

把"代码质量"变成有证据、可决策、可修复的 finding。先定范围，再进对应轨道。

## 定范围

- **diff 轨道**（默认）：写完代码后、提交前、PR/diff review，或用户说 deslop / 清理 / review 刚才的改动。范围按优先级取：用户显式指定 > `git diff`（含 staged）> 本次会话改动。走下方 diff 流程。
- **repo 轨道**：全仓技术债/架构/质量审计、公开发布或开源前的 release preflight。加载 `references/repo-audit.md` 执行。
- 用户只要审查意见时（review-only）：不改代码，只输出 findings。
- 不扩散：范围外发现记一句 backlog 即可；内部 CI/tag 检查不触发 release preflight。

## 共享纪律

- 每个 finding 带 `file:line` 或具体工具证据；拿不到证据就明说，不用猜测填充。
- 先跑项目已有的 lint/typecheck/test 拿基线再动手；修复后重跑同一组，不借红绿模糊蒙混。
- 修复一律 deletion-first：删代码、删抽象、删注释优先于新增；复用仓库已有工具函数；不引入新依赖；patch 保持最小。
- 纯风格好恶（无具体 failure mode）不是 finding；仓库既有约定（命名风格、注释密度、抽象层级）优先于通用口味。
- 幻觉指控先核实再定性：被指控的 API/flag/config key 对本地类型、`--help`、lockfile 或文档验证；建议的替代写法同样先验证存在且版本兼容——不以一个幻觉替换另一个幻觉。
- 同一模式出现多次：合并成一条 finding 加代表性例子，不逐条刷屏。

## Diff 轨道：deslop 流程

1. **锁行为**：跑项目快速检查（typecheck + 相关测试）拿基线；已经失败的先记录。
2. **读 diff 和上下文**：读完整改动块及足够周边代码，弄清已有 invariant 与可复用工具——"重复"和"防御过度"的判断必须锚在真实 invariant 上，不能凭感觉。
3. **按 smell 表排查**，每条 finding 归类：`delete` / `consolidate` / `fix` / `consider`（判断题交给用户）。
4. **deletion-first 修复**，顺序：死代码 → 重复 → 抽象 → 命名/注释 → 错误处理 → 测试。
5. **重跑同一组检查**，报告删了什么、验证证据是什么。

### Smell checklist

| Smell | 检测信号 | 处理 |
|---|---|---|
| Comment slop | 注释复述下一行；docstring 复述签名；无信息的分节符；hedging（"this should work"） | 删。注释只解释 why；代码需要 what 注释时改写代码本身 |
| Defensive overkill | 内部函数校验已由 invariant 保证的值；catch-log-reraise 零信息；给必需配置兜默认值；边界内层层重复校验 | 删。只在系统边界（用户输入/网络/反序列化/env）校验，内部信任 invariant；必需配置缺失要响亮失败 |
| Over-abstraction | 单实现 interface；纯转发 wrapper；只调一次的 helper；一个操作套 Manager/Service/Factory；为假想需求预留的配置项 | inline 或删。测试 DI、确有多个实现、隔离外部依赖的除外 |
| Hallucination | API/flag/config key/schema 字段"长得像真的"但未核实；从相邻生态抄来的参数；用 try/optional-chain 兜底掩盖不理解 | 按共享纪律核实；删除 invented surface |
| Duplication | 不同文件里近乎相同的实现；sibling 目录下只换了名字的孪生模块 | 收敛到一个实现或参数化差异；新写 helper 前先查仓库是否已有 |
| Generic naming | `data`/`result`/`temp`/`handler`/`manager`/`utils`/`helpers`/`common` 出现在非平凡作用域 | 换领域名；`utils.*` 垃圾抽屉按职责拆 |
| Test theater | mock 掉所有依赖只断言调用次数；镜像实现控制流；snapshot 当唯一断言；只测 happy path | 改为断言行为/规格；mock 留在边界。判断标准：实现以同样方式写错时测试仍绿 = 摆设 |
| Boilerplate | `result = f(); return result`；`return x ? true : false`；手写循环替代语言内建 | 用该语言的 idiomatic 短形式 |

语言专属气味（Rust clone 滥用、Python 裸 except、TS any 等）见 `references/languages.md`，按 diff 实际涉及的语言加载，不涉及的不要套。

### 审查独立性

写完代码立刻自己宣布"质量很好"等于没审。

- 同会话自查：当作独立一轮——从 diff 重新读起，不依赖写代码时的记忆和假设。
- 需要独立审查时由宿主编排层根据当前任务决定 reviewer 和调度方式；本 skill 不要求或优先指定子代理。
- review-only 模式下不动手；修改模式下改完后必须重跑检查收尾，不允许"我改的就是对的"直接宣布通过。

### Do not flag

- 安全相关：auth、边界输入校验、TLS、rate limit——即使"看起来防御过度"。
- 框架要求的结构与目录约定。
- 没有具体 failure mode 的口味差异。

## Output

- 两条轨道的 findings 都标记为 `delete` / `consolidate` / `fix` / `consider`，每条带定位、具体 failure mode 或仓库约定、证据和最小处理建议。
- review-only 只输出 findings 与验证证据，不要求或暗示 patch；用户要求修改时才交付最小 patch，并报告修复后检查。
- repo 轨道同时遵守 `references/repo-audit.md` 的范围、优先级和 release-readiness 输出约定；默认在对话中完成，不生成报告文件。

## Stop

- diff：范围内清单过完、修复验证通过即停，不为"还能更完美"追加第二轮。
- repo：见 `references/repo-audit.md` 的停止规则。
