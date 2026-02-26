---
name: cs-rag-architecture-guideline
description: CS-RAG 项目专用架构总规范，统一全局架构认知与架构设计约束，提供分层检查、影响面分析、接口契约、依赖注入与可插拔治理入口。
metadata:
  type: declarative
  category: architecture
  scope: project-specific
  project: cs-rag
  classification: project-architecture
  merge_mode: lossless
  merged_from:
    - architecture-cognition
    - architecture-design
  related_generic_skill: architecture-governance
---

# CS-RAG 架构总规范

> CS-RAG 项目专用架构总规范。已无损合并 `architecture-cognition` 与 `architecture-design` 的规则内容，可在原 skill 删除后独立使用。

---

## ⚠️ 核心强制要求

### 统一三层架构约束

- 前端层 → 业务层 → 基础设施层（单向依赖）
- 禁止反向依赖：基础设施层不能依赖业务层或前端层
- 禁止跨层访问：前端层不能直接访问基础设施层
- 基础设施层不得夹带业务逻辑

### 认知与设计的组合治理顺序

1. 先执行架构认知检查：层级位置、组件关系、数据流影响
2. 再执行架构设计检查：接口契约、依赖注入、可插拔设计
3. 最后执行合规复核：跨层、反向依赖、循环依赖、兼容性

### 升级给用户决策的场景

- 涉及跨层依赖修改
- 涉及核心组件接口变更（尤其破坏性变更）
- 涉及数据流向/主路径改变
- 涉及全局策略、性能、资源消耗或数据一致性风险

---

## AI Agent 行为要求

### 阶段 A：架构认知（原 `architecture-cognition` 全量迁入）

修改代码前必须回答：

1. **位置识别**：属于哪一层？影响哪些组件？有跨层依赖风险？
2. **影响范围**：影响哪些数据流？有组件依赖此接口？需更新测试？
3. **架构约束**：是否违反三层架构？是否引入循环依赖？

创建新组件时必须明确：

1. **职责定位**：属于哪一层？单一职责是什么？与现有组件关系？
2. **接口设计**：需要抽象基类/Protocol？需要工厂模式？
3. **依赖管理**：依赖哪些组件？是否可依赖注入？是否违反依赖方向？

快速参考（项目上下文）：

| 层 | 核心组件 | 职责 |
|----|----------|------|
| 前端层 | `frontend/main.py` | 用户交互、UI 展示 |
| 业务层 | `RAGService`, `QueryEngine` | 业务逻辑、流程编排 |
| 基础设施层 | `IndexManager`, `Embedding`, `LLM` | 技术实现、无业务逻辑 |

### 阶段 B：架构设计（原 `architecture-design` 全量迁入）

设计变更时检查项：

- [ ] 标注影响到的层级与上下游模块
- [ ] 确认无循环依赖
- [ ] 确认无跨层访问

接口设计要求：

- 以抽象基类或 Protocol 定义契约
- 新接口默认向后兼容
- 使用构造函数依赖注入，禁止静态单例

可插拔设计要求：

- 使用工厂或注册表模式注册新实现
- 所有可切换组件通过配置项启用

新模块规划时：

- [ ] 每个模块/类仅负责单一领域
- [ ] 命名遵循 `src/<layer>/<role>/module.py` 结构

### 阶段 C：合规复核

- 复核是否引入跨层访问或反向依赖
- 复核接口变更是否具备兼容策略
- 复核是否出现循环依赖

---

## 判断标准

- 是否完成“认知 + 设计 + 复核”三阶段检查
- 是否保持三层依赖方向正确且无循环依赖
- 是否保留接口兼容性与实现可替换性

---

## 无损合并声明

- 本 skill 已承载两套原始规则的**内容级迁移**，不是仅链接跳转。
- 原始 `SKILL.md` 文本已复制到：
  - `references/architecture-cognition-skill.md`
  - `references/architecture-design-skill.md`
- 原始 references 文本已全量复制到本 skill 的 `references/`。
- 详细映射见 `references/lossless-merge-routing.md`。

### 删除源 skill 就绪说明

- 删除 `architecture-cognition` 与 `architecture-design` 后，本 skill 仍可独立运行。
- 删除前后仅路径变化，不会丢失规则内容。

---

## 参考资料

- `references/lossless-merge-routing.md` - 无损合并路由与原文映射
- `references/architecture-cognition-skill.md` - 原 `architecture-cognition` 全文
- `references/architecture-cognition-system-overview.md` - 原认知参考：系统定位
- `references/architecture-cognition-three-layer-architecture.md` - 原认知参考：三层架构
- `references/architecture-cognition-component-map.md` - 原认知参考：组件地图
- `references/architecture-cognition-data-flow.md` - 原认知参考：数据流
- `references/architecture-design-skill.md` - 原 `architecture-design` 全文
- `references/architecture-design-layer-guidelines.md` - 原设计参考：分层指南
- `references/architecture-design-module-planning.md` - 原设计参考：模块规划
- `references/architecture-design-interface-design.md` - 原设计参考：接口设计
