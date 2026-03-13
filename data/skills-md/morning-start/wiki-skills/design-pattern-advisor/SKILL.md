---
name: "design-pattern-advisor"
version: "1.1.0"
author: "skill-manager"
description: "智能设计模式顾问，提供设计模式识别、推荐、代码优化和架构审查能力。Invoke when user needs to identify design patterns in code, get pattern recommendations for a scenario, optimize code structure with patterns, or review system architecture."
tags: ["design-pattern", "architecture", "code-review", "refactoring"]
use_cases:
  - "代码审查时识别设计模式"
  - "新功能开发时选择合适模式"
  - "重构时优化代码结构"
  - "架构设计时评估方案"
reliability_score: 0.92
cost_estimate: low
execution_time: fast
---

# 设计模式顾问 (Design Pattern Advisor)

> **智能识别设计模式，精准推荐解决方案，专业优化代码结构，系统审查架构设计**

---

## 触发条件

当用户有以下需求时触发本技能：

- 分析代码中使用了哪些设计模式
- 为特定场景选择合适的设计模式
- 优化现有代码的设计结构
- 审查系统架构的合理性
- 识别代码中的设计异味
- 对比多个设计模式的优劣

---

## 原子能力清单

本技能提供8个原子能力，可独立调用或组合使用：

### 1. analyze-pattern-usage（分析模式使用）

**描述**：分析代码中已使用的设计模式及其正确性

**输入**：
```json
{
  "capability": "analyze-pattern-usage",
  "context": {
    "code": "string - 代码片段或文件路径",
    "language": "string - 编程语言",
    "framework": "string - 框架（可选）"
  },
  "parameters": {
    "depth": "basic|detailed - 分析深度",
    "include_examples": "boolean - 是否包含示例"
  }
}
```

**输出**：
```json
{
  "status": "success|error",
  "result": {
    "patterns_found": [
      {
        "name": "string - 模式名称",
        "type": "creational|structural|behavioral",
        "location": "string - 代码位置",
        "correctness": "correct|partial|incorrect",
        "assessment": "string - 评估说明"
      }
    ],
    "summary": "string - 分析总结"
  },
  "metadata": {
    "execution_time_ms": 1200,
    "confidence_score": 0.95
  }
}
```

**示例**：
```
输入：分析 UserService.java 中的设计模式
输出：识别到单例模式（正确）、工厂方法（部分正确，缺少抽象产品）
```

### 2. detect-pattern-misuse（检测模式误用）

**描述**：检测设计模式的不当使用或过度设计

**输入**：
```json
{
  "capability": "detect-pattern-misuse",
  "context": {
    "code": "string - 代码片段",
    "pattern_name": "string - 特定模式（可选）"
  },
  "parameters": {
    "strictness": "low|medium|high - 检测严格度"
  }
}
```

**输出**：
```json
{
  "status": "success|error",
  "result": {
    "misuses": [
      {
        "pattern": "string - 模式名称",
        "issue": "string - 问题描述",
        "severity": "low|medium|high",
        "suggestion": "string - 改进建议"
      }
    ]
  },
  "metadata": {
    "execution_time_ms": 800,
    "confidence_score": 0.88
  }
}
```

**示例**：
```
输入：检测 PaymentProcessor 中的单例模式使用
输出：高风险 - 单例持有可变状态，建议改为无状态实现或使用依赖注入
```

### 3. recommend-pattern（推荐设计模式）

**描述**：根据场景推荐最合适的设计模式

**输入**：
```json
{
  "capability": "recommend-pattern",
  "context": {
    "scenario": "string - 业务场景描述",
    "constraints": ["string - 约束条件"],
    "existing_code": "string - 现有代码（可选）"
  },
  "parameters": {
    "max_recommendations": "number - 最大推荐数",
    "include_alternatives": "boolean - 是否包含替代方案"
  }
}
```

**输出**：
```json
{
  "status": "success|error",
  "result": {
    "recommendations": [
      {
        "pattern": "string - 模式名称",
        "priority": 1,
        "rationale": "string - 推荐理由",
        "applicability": "high|medium|low",
        "trade_offs": ["string - 权衡点"]
      }
    ]
  },
  "metadata": {
    "execution_time_ms": 1500,
    "confidence_score": 0.90
  }
}
```

**示例**：
```
输入：需要支持多种支付方式，且未来可能扩展
输出：推荐策略模式（高优先级）+ 工厂方法（中优先级）
```

### 4. compare-patterns（对比多个模式）

**描述**：对比多个设计模式的优劣和适用性

**输入**：
```json
{
  "capability": "compare-patterns",
  "context": {
    "patterns": ["string - 模式名称列表"],
    "scenario": "string - 应用场景"
  },
  "parameters": {
    "criteria": ["complexity", "flexibility", "performance"]
  }
}
```

**输出**：
```json
{
  "status": "success|error",
  "result": {
    "comparison": {
      "table": "对比表格数据",
      "winner": "string - 最佳模式",
      "analysis": "string - 详细分析"
    }
  },
  "metadata": {
    "execution_time_ms": 1000,
    "confidence_score": 0.92
  }
}
```

**示例**：
```
输入：对比策略模式和状态模式在订单状态管理中的适用性
输出：策略模式更适合（状态转换简单，行为变化多）
```

### 5. suggest-refactoring（建议重构方案）

**描述**：提供具体的代码重构建议

**输入**：
```json
{
  "capability": "suggest-refactoring",
  "context": {
    "code": "string - 待重构代码",
    "target_pattern": "string - 目标模式（可选）"
  },
  "parameters": {
    "goal": "maintainability|extensibility|performance",
    "preserve_behavior": true
  }
}
```

**输出**：
```json
{
  "status": "success|error",
  "result": {
    "refactoring_plan": [
      {
        "step": 1,
        "action": "string - 重构动作",
        "before": "string - 重构前代码",
        "after": "string - 重构后代码",
        "benefits": ["string - 收益说明"]
      }
    ]
  },
  "metadata": {
    "execution_time_ms": 2000,
    "confidence_score": 0.87
  }
}
```

**示例**：
```
输入：优化包含大量if-else的订单处理代码
输出：建议重构为策略模式，提供分步重构方案
```

### 6. generate-code-example（生成代码示例）

**描述**：生成指定设计模式的代码示例

**输入**：
```json
{
  "capability": "generate-code-example",
  "context": {
    "pattern": "string - 模式名称",
    "language": "string - 编程语言",
    "domain": "string - 业务领域（可选）"
  },
  "parameters": {
    "complexity": "simple|medium|complete",
    "include_comments": true
  }
}
```

**输出**：
```json
{
  "status": "success|error",
  "result": {
    "code_example": "string - 完整代码示例",
    "explanation": "string - 代码说明",
    "key_points": ["string - 关键点"]
  },
  "metadata": {
    "execution_time_ms": 1800,
    "confidence_score": 0.95
  }
}
```

**示例**：
```
输入：生成Java的观察者模式示例，用于订单状态通知
输出：提供完整的OrderSubject、OrderObserver实现及使用示例
```

### 7. evaluate-architecture（评估架构设计）

**描述**：评估系统架构的合理性和设计质量

**输入**：
```json
{
  "capability": "evaluate-architecture",
  "context": {
    "architecture_description": "string - 架构描述",
    "key_modules": ["string - 关键模块"],
    "design_goals": ["string - 设计目标"]
  },
  "parameters": {
    "depth": "high-level|detailed",
    "focus_areas": ["coupling", "cohesion", "scalability"]
  }
}
```

**输出**：
```json
{
  "status": "success|error",
  "result": {
    "assessment": {
      "overall_score": 0.85,
      "strengths": ["string - 优势"],
      "weaknesses": ["string - 劣势"],
      "risks": ["string - 风险"]
    },
    "recommendations": ["string - 改进建议"]
  },
  "metadata": {
    "execution_time_ms": 3000,
    "confidence_score": 0.85
  }
}
```

**示例**：
```
输入：评估微服务架构的订单系统
输出：整体评分85分，指出服务间耦合过高，建议使用外观模式简化调用
```

### 8. identify-design-smell（识别设计异味）

**描述**：识别代码中的设计异味和潜在问题

**输入**：
```json
{
  "capability": "identify-design-smell",
  "context": {
    "code": "string - 代码片段",
    "code_metrics": "object - 代码指标（可选）"
  },
  "parameters": {
    "smell_types": ["all"],
    "threshold": "low|medium|high"
  }
}
```

**输出**：
```json
{
  "status": "success|error",
  "result": {
    "smells": [
      {
        "type": "string - 异味类型",
        "location": "string - 代码位置",
        "description": "string - 问题描述",
        "severity": "low|medium|high",
        "refactoring": "string - 重构建议"
      }
    ]
  },
  "metadata": {
    "execution_time_ms": 1200,
    "confidence_score": 0.89
  }
}
```

**示例**：
```
输入：分析UserManager类的设计异味
输出：识别到上帝类（高严重）、紧耦合（中严重），建议拆分为多个职责单一的类
```

---

## 复合能力组合

原子能力可组合为4个复合能力，对应常见使用场景：

### pattern-recognition（模式识别）

**组合**：analyze-pattern-usage + detect-pattern-misuse

**适用场景**：
- 代码审查时识别设计模式
- 学习项目中的设计模式应用
- 评估模式使用的正确性

**调用示例**：
```
分析这段代码使用了哪些设计模式，是否有误用？
```

### pattern-recommendation（模式推荐）

**组合**：recommend-pattern + compare-patterns

**适用场景**：
- 新功能开发选择设计模式
- 对比多个模式的优劣
- 确定最佳设计方案

**调用示例**：
```
我需要实现一个支持多种通知方式的功能，推荐合适的设计模式
```

### code-optimization（代码优化）

**组合**：suggest-refactoring + generate-code-example

**适用场景**：
- 重构遗留代码
- 优化复杂条件判断
- 提取重复代码

**调用示例**：
```
优化这段包含大量if-else的代码，并给出重构后的示例
```

### architecture-review（架构审查）

**组合**：evaluate-architecture + identify-design-smell

**适用场景**：
- 系统架构评估
- 识别架构层面的设计问题
- 改进系统整体设计

**调用示例**：
```
审查这个微服务架构设计，识别潜在问题
```

---

## 错误处理

### 错误码定义

| 错误码 | 消息 | 回退策略 |
|--------|------|----------|
| INVALID_CODE_FORMAT | 提供的代码格式无法解析 | 请提供有效的代码片段或文件路径 |
| PATTERN_NOT_FOUND | 未识别到已知的设计模式 | 尝试使用更完整的代码示例，或手动描述设计意图 |
| AMBIGUOUS_SCENARIO | 场景描述不够清晰，无法确定推荐 | 请提供更多上下文信息，如业务目标、约束条件 |
| ARCHITECTURE_TOO_COMPLEX | 架构过于复杂，无法完成全面审查 | 建议分模块进行审查，或提供架构图辅助分析 |
| UNSUPPORTED_LANGUAGE | 不支持的编程语言 | 请使用Java、Python、JavaScript等主流语言 |
| INSUFFICIENT_CONTEXT | 上下文信息不足 | 请提供更多代码上下文或项目背景 |

### 回退策略

当遇到错误时，按以下优先级执行回退：

1. **请求用户提供更多信息**
   - 说明需要补充的具体信息
   - 提供信息模板或示例

2. **缩小分析范围**
   - 建议用户指定特定模块或功能
   - 分段处理复杂代码

3. **提供通用建议而非具体方案**
   - 基于设计原则给出方向性建议
   - 推荐相关设计模式文档

4. **推荐人工审查**
   - 当自动化分析无法满足需求时
   - 建议咨询架构师或资深开发者

---

## 使用示例

### 示例1：识别代码中的设计模式

**用户输入**：
```
分析这个数据库连接池类的设计模式使用
```

**技能执行**：
1. 调用 analyze-pattern-usage 分析代码
2. 调用 detect-pattern-misuse 检测潜在问题

**输出结果**：
```
识别到的设计模式：
✓ 单例模式 - 正确实现，使用双重检查锁定
✓ 工厂方法 - 部分正确，缺少抽象产品接口
⚠ 潜在问题：单例持有可变状态，建议改为无状态实现
```

### 示例2：推荐设计模式

**用户输入**：
```
我需要实现一个支持多种支付方式的系统，推荐合适的设计模式
```

**技能执行**：
1. 调用 recommend-pattern 获取推荐列表
2. 调用 compare-patterns 对比候选模式

**输出结果**：
```
推荐方案：
1. 策略模式（高优先级）- 封装不同支付算法
2. 工厂方法（中优先级）- 创建具体支付策略
3. 外观模式（低优先级）- 简化支付流程调用

对比分析：策略模式 vs 状态模式
- 策略模式更适合：支付方式间无状态转换
- 实现更简单，扩展性更好
```

### 示例3：代码优化

**用户输入**：
```
优化这段订单处理代码，它有很多if-else判断
```

**技能执行**：
1. 调用 suggest-refactoring 生成重构方案
2. 调用 generate-code-example 生成示例代码

**输出结果**：
```
重构建议：将条件判断重构为策略模式

步骤1：定义策略接口
步骤2：提取各支付方式为具体策略
步骤3：修改上下文类使用策略

重构收益：
- 代码复杂度降低60%
- 新增支付方式无需修改现有代码
- 符合开闭原则
```

### 示例4：架构审查

**用户输入**：
```
审查这个微服务架构的设计
```

**技能执行**：
1. 调用 evaluate-architecture 评估整体架构
2. 调用 identify-design-smell 识别设计异味

**输出结果**：
```
架构评估报告：
整体评分：82/100

优势：
- 服务职责划分清晰
- 使用API网关统一入口

风险：
- 服务间直接调用过多，建议引入外观模式
- 缺少熔断机制，建议使用断路器模式

改进建议：
1. 封装外部服务调用为外观接口
2. 添加Hystrix实现服务熔断
3. 考虑使用事件驱动减少同步调用
```

---

## 注意事项

### 使用限制

1. **代码长度限制**
   - 单次分析代码不超过1000行
   - 超大文件建议分模块分析

2. **语言支持**
   - 主要支持：Java、Python、JavaScript/TypeScript、C#、Go
   - 其他语言可能分析精度降低

3. **架构复杂度**
   - 超大型系统建议分层次审查
   - 需要提供关键模块而非全部代码

### 最佳实践

1. **提供完整上下文**
   - 包含相关类和方法
   - 说明业务背景和目标

2. **明确优化目标**
   - 可维护性、扩展性、性能
   - 不同目标可能推荐不同方案

3. **迭代优化**
   - 先识别问题，再逐步优化
   - 避免一次性大规模重构

4. **验证建议**
   - 自动化分析仅供参考
   - 关键决策需要人工确认

---

## 设计模式知识库

本技能基于以下23种经典设计模式：

### 创建型模式（5种）
- [单例模式](references/creational/singleton.md) - 全局唯一实例
- [工厂方法](references/creational/factory-method.md) - 延迟实例化到子类
- [抽象工厂](references/creational/abstract-factory.md) - 创建相关对象家族
- [建造者模式](references/creational/builder.md) - 分步构建复杂对象
- [原型模式](references/creational/prototype.md) - 通过复制创建对象

### 结构型模式（7种）
- [适配器模式](references/structural/adapter.md) - 接口转换
- [桥接模式](references/structural/bridge.md) - 抽象与实现分离
- [组合模式](references/structural/composite.md) - 树形结构
- [装饰器模式](references/structural/decorator.md) - 动态添加职责
- [外观模式](references/structural/facade.md) - 简化接口
- [享元模式](references/structural/flyweight.md) - 共享细粒度对象
- [代理模式](references/structural/proxy.md) - 控制对象访问

### 行为型模式（11种）
- [责任链模式](references/behavioral/chain-of-responsibility.md) - 多对象处理请求
- [命令模式](references/behavioral/command.md) - 请求参数化
- [解释器模式](references/behavioral/interpreter.md) - 语言解释
- [迭代器模式](references/behavioral/iterator.md) - 顺序访问集合
- [中介者模式](references/behavioral/mediator.md) - 封装对象交互
- [备忘录模式](references/behavioral/memento.md) - 保存恢复状态
- [观察者模式](references/behavioral/observer.md) - 一对多依赖通知
- [状态模式](references/behavioral/state.md) - 状态决定行为
- [策略模式](references/behavioral/strategy.md) - 算法族封装
- [模板方法模式](references/behavioral/template-method.md) - 算法骨架
- [访问者模式](references/behavioral/visitor.md) - 作用于元素操作

---

## 版本历史

### v1.1.0 (2026-03-01)

**优化内容**：
- 应用 skill-manager 优化策略
- 原子化拆分8个原子能力
- 定义4个复合能力组合
- 标准化输入输出接口
- 完善错误处理机制
- 添加元数据增强（use_cases、reliability_score等）

### v1.0.0 (2026-03-01)

**初始版本**：
- 整合23种经典设计模式知识库
- 提供四大核心能力：识别、推荐、优化、审查
- 支持完整的工作流程

---

**开始使用设计模式顾问，提升你的代码设计质量！**
