---
name: meta-skill-creator
version: 1.0.0
description: 高阶技能创建系统，支持技能生成、自省、组合、优化、版本管理与安全对齐
dependency:
  python:
    - pyyaml>=6.0
---

# Meta Skill Creator

## 任务目标
- 本 Skill 用于: 创建、管理和优化其他技能，提供从基础定义到高阶组合的全生命周期管理
- 能力包含: 结构化技能生成、自省分析、模块化组合、迭代优化、版本控制、安全对齐检查
- 触发条件: 用户需要创建新技能、分析现有技能、组合多个技能、优化技能设计或管理技能版本

## 前置准备
- 依赖说明: scripts 脚本所需的依赖包及版本
  ```
  pyyaml>=6.0
  ```

## 操作步骤
- 标准流程:
  1. 需求分析与上下文理解
     - 智能体分析用户目标、历史记录、约束条件
     - 结合 [references/skill-standards.md](references/skill-standards.md) 确定技能类型和规范
  2. 基础能力执行
     - 生成技能定义: 调用 `scripts/generate_skill.py` 生成标准化的 YAML 前言区和结构
     - 格式验证: 调用 `scripts/validate_skill.py` 检查格式合规性和安全规则
  3. 高阶能力执行（按需）
     - 技能组合: 调用 `scripts/compose_skills.py` 实现技能嵌套、复用和拼接
     - 版本管理: 调用 `scripts/version_skill.py` 处理技能版本迭代、差异对比
     - 自省分析: 智能体分析技能能力边界、优化点、组合可能性
  4. 优化与迭代
     - 智能体根据反馈调整技能设计，参考 [references/composition-patterns.md](references/composition-patterns.md)
     - 执行安全对齐检查，参考 [references/security-guidelines.md](references/security-guidelines.md)
- 可选分支:
  - 当 创建基础技能: 执行步骤 1-2
  - 当 组合多个技能: 执行步骤 1-3（包含组合）
  - 当 优化现有技能: 执行步骤 1-2-4
  -当 版本迭代: 执行步骤 1-2-3（版本管理）-4

## 资源索引
- 必要脚本:
  - [scripts/generate_skill.py](scripts/generate_skill.py) (用途与参数: 生成标准化技能定义，接收 skill_name, description, capabilities, dependencies 等参数)
  - [scripts/validate_skill.py](scripts/validate_skill.py) (用途与参数: 验证技能格式和安全规则，接收 skill_definition, check_security=True 等参数)
  - [scripts/compose_skills.py](scripts/compose_skills.py) (用途与参数: 组合多个技能，接收 skills_list, composition_mode 等参数)
  - [scripts/version_skill.py](scripts/version_skill.py) (用途与参数: 管理技能版本，接收 action, skill_path, target_version 等参数)
- 领域参考:
  - [references/skill-standards.md](references/skill-standards.md) (何时读取: 生成技能定义时参考格式规范)
  - [references/composition-patterns.md](references/composition-patterns.md) (何时读取: 组合技能时参考组合模式)
  - [references/security-guidelines.md](references/security-guidelines.md) (何时读取: 验证技能安全性时参考对齐规则)

## 注意事项
- 充分利用智能体的语言理解与推理能力进行需求分析、创意设计和自省评估
- 仅在涉及结构化数据处理、格式验证、组合逻辑等技术性操作时调用脚本
- 技能描述、流程设计、优化建议等内容由智能体直接生成，无需脚本处理
- 组合技能时注意模块边界，避免能力耦合
- 版本管理遵循语义化版本规范，记录每次变更的影响范围

## 使用示例
- 基础创建: 用户说"创建一个数据清洗技能"，智能体分析需求 → 调用 generate_skill.py 生成定义 → 智能体补充流程说明
- 技能组合: 用户说"把数据处理和报告生成组合起来"，智能体分析组合策略 → 调用 compose_skills.py → 智能体调整接口定义
- 版本迭代: 用户说"给这个技能添加日志功能"，智能体设计变更 → 调用 version_skill.py 记录版本 → 生成新定义
