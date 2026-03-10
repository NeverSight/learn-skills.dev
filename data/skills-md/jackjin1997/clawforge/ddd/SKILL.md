---
name: ddd
version: 1.0.0
description: 领域驱动设计（DDD）建模与架构指导。用于创建领域模型、设计限界上下文、实现聚合根、实体、值对象、领域服务和领域事件。支持战略设计（上下文映射、子域划分）和战术设计（聚合、仓储、工厂模式）。当用户需要进行领域建模、微服务划分、复杂业务逻辑设计时使用。
author: DeepArchi
license: MIT
keywords:
  - ddd
  - domain-driven-design
  - domain-modeling
  - bounded-context
  - aggregate
  - microservices
  - architecture
---

# DDD Skill - 领域驱动设计建模

## 概述

DDD Skill 提供领域驱动设计的完整指导，帮助开发者和架构师进行领域建模、限界上下文划分和战术模式实现。

## 何时使用

当用户需要：
- 分析复杂业务领域并进行领域建模
- 划分限界上下文和子域
- 设计聚合根、实体、值对象
- 实现领域服务和领域事件
- 进行微服务边界划分
- 应用CQRS/事件溯源模式
- 设计六边形架构/洋葱架构

## 快速开始

### 1. 战略设计（Strategic Design）

确定业务领域的边界和上下文关系：

```
核心域（Core Domain）→ 竞争优势所在
支撑域（Supporting Domain）→ 支持核心业务
通用域（Generic Domain）→ 可外购/复用
```

### 2. 战术设计（Tactical Design）

在限界上下文内进行详细建模：

```
聚合根（Aggregate Root）
├── 实体（Entity）- 有唯一标识
├── 值对象（Value Object）- 无标识，不可变
└── 领域事件（Domain Event）- 记录业务变化
```

## 核心概念

### 限界上下文（Bounded Context）

限界上下文是DDD的核心概念，定义了领域模型的边界：

```
┌─────────────────────────────────────────────────────┐
│                    订单上下文                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│  │  订单   │  │ 订单项  │  │ 支付    │              │
│  │ 聚合根  │  │  实体   │  │ 值对象  │              │
│  └─────────┘  └─────────┘  └─────────┘              │
└─────────────────────────────────────────────────────┘
                    │
                    │ 上下文映射
                    ▼
┌─────────────────────────────────────────────────────┐
│                    库存上下文                         │
│  ┌─────────┐  ┌─────────┐                           │
│  │  库存   │  │ 库存项  │                           │
│  │ 聚合根  │  │  实体   │                           │
│  └─────────┘  └─────────┘                           │
└─────────────────────────────────────────────────────┘
```

### 聚合设计规则

1. **保护业务不变式** - 聚合边界内的数据一致性由聚合根保护
2. **小聚合原则** - 聚合应尽可能小，只包含必需的元素
3. **通过ID引用** - 聚合间通过ID引用，不直接持有对象引用
4. **一次事务一个聚合** - 每次事务只修改一个聚合
5. **最终一致性** - 聚合间通过领域事件实现最终一致性

## 建模工作流

### 步骤1：事件风暴（Event Storming）

识别领域中的关键事件：

```
橙色便签：领域事件（发生了什么）
蓝色便签：命令（触发事件的动作）
黄色便签：聚合（处理命令、产生事件）
紫色便签：策略（响应事件的规则）
粉色便签：外部系统
```

### 步骤2：识别限界上下文

根据事件风暴结果划分上下文边界：

- 相关事件和聚合归入同一上下文
- 使用通用语言（Ubiquitous Language）
- 确定上下文之间的关系

### 步骤3：上下文映射

定义上下文间的集成关系：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| 共享内核 | 共享部分模型 | 紧密协作团队 |
| 客户-供应商 | 上下游依赖 | 明确的服务依赖 |
| 防腐层 | 隔离外部模型 | 集成遗留系统 |
| 开放主机服务 | 提供标准API | 多消费者场景 |
| 发布语言 | 共享数据格式 | 事件驱动集成 |

### 步骤4：战术建模

在每个上下文内进行详细设计：

```python
# 聚合根示例
class Order(AggregateRoot):
    def __init__(self, order_id: OrderId, customer_id: CustomerId):
        self.id = order_id
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.status = OrderStatus.DRAFT
    
    def add_item(self, product_id: ProductId, quantity: int, price: Money):
        """添加订单项 - 业务逻辑封装在聚合内"""
        if self.status != OrderStatus.DRAFT:
            raise DomainException("只能向草稿订单添加商品")
        item = OrderItem(product_id, quantity, price)
        self.items.append(item)
        self.add_event(OrderItemAdded(self.id, item))
    
    def submit(self):
        """提交订单 - 触发领域事件"""
        if not self.items:
            raise DomainException("订单不能为空")
        self.status = OrderStatus.SUBMITTED
        self.add_event(OrderSubmitted(self.id, self.total_amount))
```

```python
# 值对象示例 - 不可变，无标识
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str
    
    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("货币类型不匹配")
        return Money(self.amount + other.amount, self.currency)
```

```python
# 领域事件示例
@dataclass(frozen=True)
class OrderSubmitted(DomainEvent):
    order_id: OrderId
    total_amount: Money
    occurred_at: datetime = field(default_factory=datetime.utcnow)
```

## 架构模式

### 六边形架构（端口与适配器）

```
                    ┌─────────────────────────────────┐
                    │         应用层（Application）    │
    ┌───────────┐   │  ┌─────────────────────────┐   │   ┌───────────┐
    │   REST    │◄──┼──│      端口（Ports）       │──┼──►│  数据库   │
    │   API     │   │  └─────────────────────────┘   │   │ 适配器    │
    └───────────┘   │              │                  │   └───────────┘
                    │              ▼                  │
    ┌───────────┐   │  ┌─────────────────────────┐   │   ┌───────────┐
    │  消息     │◄──┼──│      领域层（Domain）    │──┼──►│  消息     │
    │  队列     │   │  │    聚合、实体、值对象     │   │   │ 适配器    │
    └───────────┘   │  └─────────────────────────┘   │   └───────────┘
                    └─────────────────────────────────┘
```

### CQRS模式

```
命令端（Command Side）          查询端（Query Side）
      │                              │
      ▼                              ▼
┌──────────────┐              ┌──────────────┐
│ Command Bus  │              │  Query Bus   │
└──────────────┘              └──────────────┘
      │                              │
      ▼                              ▼
┌──────────────┐              ┌──────────────┐
│   聚合根     │──事件──►     │   读模型     │
│（写模型）    │              │（优化查询）  │
└──────────────┘              └──────────────┘
      │                              │
      ▼                              ▼
┌──────────────┐              ┌──────────────┐
│  事件存储    │              │  查询数据库  │
└──────────────┘              └──────────────┘
```

## 资源文件

详细参考文档：
- `references/strategic-design.md` - 战略设计详解
- `references/tactical-design.md` - 战术设计模式
- `references/patterns.md` - DDD架构模式
- `assets/ddd-model-template.drawio` - 领域模型模板

## 常见问题

### Q: 如何确定聚合边界？

1. 识别业务不变式（必须始终为真的规则）
2. 不变式涉及的实体应在同一聚合内
3. 优先小聚合，通过领域事件实现跨聚合一致性

### Q: 何时使用领域服务？

- 业务逻辑不自然属于任何实体或值对象
- 需要协调多个聚合的操作
- 例如：转账服务（协调两个账户聚合）

### Q: 如何处理跨聚合事务？

- 使用Saga模式编排长事务
- 通过领域事件实现最终一致性
- 避免分布式事务，拥抱补偿机制

## 相关链接

- [Eric Evans - Domain-Driven Design](https://domainlanguage.com/)
- [Vaughn Vernon - Implementing Domain-Driven Design](https://vaughnvernon.co/)
- [事件风暴工作坊](https://www.eventstorming.com/)
