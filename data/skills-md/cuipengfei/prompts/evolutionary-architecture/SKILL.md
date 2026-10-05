---
name: evolutionary-architecture
description: "Knowledge base from \"Building Evolutionary Architectures\" 2nd Edition (2022) by Neal Ford, Rebecca Parsons, Patrick Kua, Pramod Sadalage. Use when applying fitness functions, architectural governance, connascence, architectural quanta, Data Mesh, Team Topologies, or evolutionary architecture concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Building Evolutionary Architectures (2nd Edition)
**Authors**: Neal Ford, Rebecca Parsons, Patrick Kua, Pramod Sadalage | **Pages**: ~269 | **Chapters**: 9 | **Generated**: 2026-07-12

## How to Use This Skill

- **无参数** — 加载核心框架供参考
- **按主题** — 问 `fitness functions`、`connascence`、`Data Mesh`、`Team Topologies` 等主题，找到并读取对应章节
- **按章节** — 问 `ch04`，加载该章节摘要
- **浏览** — 问 "有哪些章节" 查看完整索引

回答具体主题前，先按 Topic Index 读取对应 chapter；跨主题问题只读取直接相关章节，不一次加载全部文件。

---

## Core Frameworks & Mental Models

### Evolutionary Architecture（进化式架构）
当系统面临持续生态变化时使用。三大支柱：增量变更、适应性函数、适当耦合。变化由 fitness functions 引导朝目标演进。2nd edition 强调 governance 与 evolution 的重叠。Prefer evolutionary over adaptable——guided change toward a goal, not jury-rigged patches。

### Fitness Functions（适应性函数）
为每个要保护的架构特性定义。客观完整性评估防止特性退化。六条分类轴：scope (atomic/holistic)、cadence (triggered/continual/**temporal**)、result (static/dynamic)、invocation (automated/manual)、proactivity (intentional/emergent)、coverage。Coverage 强调 architecture FFs 与 domain tests 的职责分离。Wire into deployment pipelines。

### Automating Architectural Governance（自动化架构治理）— 2nd ed 新增
FFs 是 governance 的自动化执行层。Code-based FFs：afferent/efferent coupling、abstractness/instability、distance from main sequence。Zone of Pain = low A/low I；Zone of Uselessness = high A/high I。Turnkey tools：ArchUnit、NetArchTest、Pa11y、Black Duck。Linters 作为细粒度 governance。Chaos Engineering 验证 resilience。Scientist 提供 fidelity FFs。Herding 通过逐步收紧阈值引导改进。Frozen Caveman 指旧事故催生的规则脱离上下文后固化为非理性风险规避。

### Connascence（同生耦合）— 2nd ed 新增
比 "coupling" 更精确的度量体系。Static (CoN/CoT/CoM/CoP/CoA) + Dynamic (CoE/CoTi/CoV/CoI)。Properties：strength (strong→weak 越好)、locality、degree。Rules：strong→weak 优先；connascence 随距离增大而减弱。

### Architectural Quantum（架构量子）
可独立部署 + 高功能内聚 + 高静态耦合 + 同步动态耦合的最小组件。Quantum size 是增量变更下限，但缩小 quantum 也会增加分布式协调成本。**Dynamic coupling 3D space**：communication、consistency、coordination。Transactions act as strong nuclear force binding quanta。

### Expand/Contract Pattern（扩展/收缩模式）
当外部系统依赖的 database schema 需要变更时使用。Expand→维护新旧结构→等消费者迁移→Contract。数据库拆分使原生约束不能跨边界工作时，以替代机制和 FF 保护完整性；不是普遍移除 DB constraints。

### Data Mesh & Data Product Quantum — 2nd ed 新增
去中心化数据架构：domain ownership、data as product、self-serve platform、federated governance。DPQ 三类型：source-aligned、aggregate、fit-for-purpose。

### Sidecar Pattern + Service Mesh — 2nd ed 新增
把 operational concerns 放到 sidecar proxy 中，与业务代码正交解耦。Service mesh 管理所有 sidecar。两种 coupling 独立演进。

### Contract Spectrum — 2nd ed 新增
服务间契约存在 strict-to-loose trade-off；RMI、gRPC、REST、GraphQL、name/value payloads 展示不同约束组合，不应机械视为普适线性排名。

### Deployment Pipeline（部署流水线 + 适应性函数）
替代 CI server 作为 FFs 执行机制。Stages：unit tests→container build→atomic FFs→holistic FFs→manual gates→deploy。Manual stages 使瓶颈可见。**Auto-Disintegration** (2nd ed)：自动清理废弃资源（Swabbie）。

### Team Topologies — 2nd ed 新增
四种团队类型：stream-aligned、enabling、complicated-subsystem、platform。Cognitive load balance：超载就拆分或提供 platform 支持。

### Postel's Law for Contracts — 2nd ed 新增
"Be conservative in what you send, liberal in what you accept." 非 breaking change 不 version。

### Guidelines for Building Evolutionary Architectures
1. Remove Needless Variability — immutable infrastructure 锁定可变项
2. Make Decisions Reversible — feature toggles、routing proxies
3. Prefer Evolvable over Predictable
4. Build Anticorruption Layers
5. Build Sacrificial Architectures
6. Mitigate External Change — pull model 管理依赖
7. Update Frameworks Aggressively, Libraries Passively
8. Version Services Internally

### Just Enough Governance
提供少量组织可支持的 technology stacks，让团队按问题规模选择，避免 one-size-fits-all 与无约束 polyglot 两端。

### Fitness Functions as Experimental Media — 2nd ed 新增
FFs 不只是约束——还是实验媒介。用 FFs 测试不同架构决策的影响。

### Hypothesis-Driven Development — 2nd ed 强化
把 feature change 表述成 hypothesis，用 A/B 实验验证。案例：Facebook photo flagging、mobile.de。

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-software-architecture.md) | Evolving Software Architecture | Evolutionary Architecture, Dynamic Equilibrium, Governance Overlap |
| [ch02](chapters/ch02-fitness-functions.md) | Fitness Functions | FF Categories (6 axes), Temporal FFs, Systemwide FFs |
| [ch03](chapters/ch03-engineering-incremental-change.md) | Engineering Incremental Change | Deployment Pipelines, Feature Toggles, Consumer-Driven Contracts, Auto-Disintegration |
| [ch04](chapters/ch04-automating-governance.md) | Automating Architectural Governance | Code-Based FFs, ArchUnit, Chaos Engineering, Fidelity FFs, Documenting FFs |
| [ch05](chapters/ch05-evolutionary-architecture-topologies.md) | Evolutionary Architecture Topologies | Connascence, Architectural Quantum, Dynamic Coupling 3D, Contract Spectrum, Data Mesh, Sidecar/Service Mesh |
| [ch06](chapters/ch06-evolutionary-data.md) | Evolutionary Data | Expand/Contract, Database Migrations, From Native to FF, Strangler Fig for DB |
| [ch07](chapters/ch07-building-evolvable-architectures.md) | Building Evolvable Architectures | 5 Principles (含 Postel's Law), 3-Step Mechanics, LCOM, FF-Driven Architecture |
| [ch08](chapters/ch08-pitfalls-antipatterns.md) | Pitfalls and Antipatterns | Last 10% Trap (+Low-Code), Vendor King, Just Enough Governance, Reporting Antipattern |
| [ch09](chapters/ch09-putting-into-practice.md) | Putting into Practice | Team Topologies, Cognitive Load, FFs as Experimental Media, Hypothesis-Driven Dev, Zero-Day Security |

## Topic Index

- **Adaptation vs. Evolution** → ch01, ch09
- **Anticorruption Layers** → ch07
- **ArchUnit** → ch04
- **Architectural Fitness Function** → ch02, ch04
- **Architectural Quantum** → ch05, ch06
- **Auto-Disintegration** → ch03
- **Afferent/Efferent Coupling** → ch04
- **Abstractness/Instability** → ch04
- **Bit Rot** → ch01
- **Bounded Context** → ch05
- **Chaos Engineering** → ch04
- **Code Reuse Trade-off** → ch05, ch08
- **Cognitive Load** → ch09
- **Connascence** → ch05
- **Consumer-Driven Contracts** → ch03
- **Contract Spectrum** → ch05
- **Continuous Deployment** → ch03
- **Conway's Law** → ch01, ch09
- **Cycle Time** → ch08, ch09
- **Data Mesh** → ch05
- **Data Product Quantum (DPQ)** → ch05
- **Database Migration** → ch06
- **Deployment Pipeline** → ch03, ch07
- **Dependabot/snyk** → ch02, ch09
- **Distance from Main Sequence** → ch04
- **Dynamic Equilibrium** → ch01
- **Dynamic Quantum Coupling** → ch05
- **Expand/Contract** → ch06
- **Feature Toggles** → ch03
- **Fidelity Fitness Function** → ch04, ch09
- **Fitness Functions** → ch02, ch04
- **Fitness Functions as Experimental Media** → ch09
- **Frozen Caveman** → ch04
- **Just Enough Governance** → ch08
- **Herding Governance** → ch04
- **Hypothesis-Driven Development** → ch09
- **Immutable Infrastructure** → ch07
- **Incremental Change** → ch01, ch03
- **Inverse Conway Maneuver** → ch01, ch09
- **Last 10% Trap** → ch08
- **LCOM** → ch07
- **Low-Code/No-Code** → ch08
- **Migrate Method from Database** → ch06
- **Modularity** → ch05
- **Monolithic Listing** → ch05
- **Parallel Change** → ch06
- **PenultimateWidgets** → ch01, ch03, ch06, ch07, ch08, ch09
- **Postel's Law** → ch07
- **Pull Model (Dependencies)** → ch07
- **Reporting Antipattern** → ch08
- **Sacrificial Architecture** → ch07
- **Scientist Framework** → ch04
- **Service Mesh** → ch05
- **Share Nothing** → ch05
- **Sidecar Pattern** → ch05
- **Snowflake Servers** → ch07
- **Spectral** → ch03
- **Stamp Coupling** → ch05
- **Strangler Fig for DB** → ch06
- **Swabbie** → ch03
- **Systemwide Fitness Function** → ch02
- **Team Topologies** → ch09
- **Temporal Fitness Function** → ch02
- **Three Strikes and You Refactor** → ch09
- **Two-Phase Commit** → ch06
- **Vendor King** → ch08
- **Zero-Day Security** → ch09
- **Zone of Pain/Uselessness** → ch04

## Supporting Files

- [glossary.md](glossary.md) — 术语表与定义（2nd ed 更新）
- [patterns.md](patterns.md) — 模式与技术清单（2nd ed 更新）
- [cheatsheet.md](cheatsheet.md) — 决策速查表与判断指南（2nd ed 更新）

---

## Scope & Limits

本 skill 覆盖 2nd edition（2022）全书内容。在代码库中实施时，需结合项目特定工具。超出本书范围的主题，请查看相关 skill 或直接询问 agent。
