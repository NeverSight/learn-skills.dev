---
name: prototype-mode
description: 快速原型开发指南。验证想法、一次性代码模式、最小可行原型。
license: MIT
---

# Prototype Mode Skill

快速原型开发，验证想法，最小可行实现。代码可抛弃，重点是"这个有趣吗？"

---

## ⚠️ EXECUTION RULES

1. **SPEED OVER QUALITY** — 原型代码不需要生产质量
2. **SCOPE TIGHT** — 只验证一个核心假设
3. **BE HONEST** — 明确标注这是原型代码
4. **DISPOSABLE** — 准备好扔掉重来

---

## 原型 vs 生产代码

| 方面 | 原型代码 | 生产代码 |
|------|----------|----------|
| **质量** | 能跑就行 | 可维护、可扩展 |
| **文档** | 不需要 | 必须 |
| **测试** | 手动测试 | 自动化测试 |
| **命名** | 临时命名 | 清晰命名 |
| **注释** | 给自己看 | 给团队看 |
| **架构** | 单文件最好 | 模块化设计 |
| **时间** | 小时级 | 天/周级 |

---

## Phase 1: Define What to Validate

**ASK**:
```
你想验证什么？

A) 核心机制是否有趣
B) 技术可行性
C) 性能是否达标
D) 玩家体验流畅度
```

**STOP**: Wait for user's answer.

---

## Phase 2: Scope the Prototype

### 最小范围原则

**Ask these questions:**

1. **最小可行版本是什么？**
   - 剥离所有非必要元素
   
2. **可以复用什么？**
   - Godot自带节点
   - 免费素材
   - 现有代码

3. **时间限制？**
   - 建议: 1-4小时
   - 如果超过1天，范围太大

### Prototype Scope Template

```markdown
# 原型: [Name]

## 核心假设
[一句话: 这个原型验证什么？]

## 包含
- [核心功能1]
- [核心功能2]

## 不包含
- [被排除的1] (可以后续加)
- [被排除的2] (可以后续加)

## 时间限制
[X]小时

## 成功标准
- [ ] [如何判断成功]
```

**ASK**: "这个范围够小吗？"

**STOP**: Wait for user confirmation.

---

## Phase 3: Implementation Guidance

### Godot 原型捷径

#### 使用内置节点

```
不要自己写，用Godot自带:
├── CharacterBody2D/3D → 角色控制
├── Area2D → 触发区域
├── AnimationPlayer → 动画
├── Timer → 计时
├── Tween → 补间动画
├── RayCast2D/3D → 射线检测
└── ShaderMaterial → 快速特效
```

#### 原型代码模式

```gdscript
# ✅ 原型代码 - 简单直接
extends CharacterBody2D

var speed = 200
func _process(delta):
    velocity = Input.get_vector("left", "right", "up", "down") * speed
    move_and_slide()

# ❌ 原型不需要这样 - 过度工程
class_name PlayerMovementController
extends Node

@export var movement_config: MovementConfigResource
var _state_machine: FiniteStateMachine
# ...50行配置代码...
```

#### 临时素材

```
用占位符:
├── 彩色方块代替角色
├── 纯色矩形代替UI
├── 内置形状代替精灵
├── DebugDraw画碰撞框
└── print()代替UI显示数值
```

### Quick Prototype Patterns

| 需求 | 快速实现 |
|------|----------|
| 角色移动 | `CharacterBody2D` + `move_and_slide()` |
| 射击 | `@onready` + `preload()` + `instantiate()` |
| 敌人AI | 简单状态: `if distance < X: chase` |
| 碰撞检测 | `Area2D` + `body_entered` signal |
| UI数值 | `Label.text = str(value)` |
| 计时 | `Timer` node + `timeout` signal |
| 动画 | `AnimationPlayer` + 录制 |

---

## Phase 4: Test & Evaluate

### Playtest Questions

在原型完成后，回答:

```
原型评估
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 核心假设验证了吗？
   [是/否/部分]

2. 最有趣的部分是什么？
   [描述]

3. 最无聊的部分是什么？
   [描述]

4. 有意外发现吗？
   [描述]

5. 值得继续开发吗？
   [是/否/需要修改]

6. 下一步是什么？
   [放弃/迭代/进入生产]
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ASK**: "原型测试结果如何？"

**STOP**: Wait for user's feedback.

---

## Phase 5: Next Steps

### Decision Tree

```
原型结果
    │
    ├── 放弃 → 记录学到的，删除代码
    │
    ├── 迭代 → 缩小范围，再做一个原型
    │
    └── 进入生产 → 清理/重写代码
                    │
                    ├── 原型代码可以复用？
                    │   └── 重构为生产质量
                    │
                    └── 原型代码太乱？
                        └── 参考原型，从头写
```

### Prototype to Production Checklist

**IF moving to production:**

```markdown
# 原型到生产转换

## 保留
- [核心设计决策]
- [验证有效的数值]

## 重写
- [乱七八糟的代码]
- [硬编码的值]

## 新增
- [ ] 状态机
- [ ] 信号解耦
- [ ] 类型标注
- [ ] 错误处理
- [ ] 测试
```

---

## Common Prototype Types

### Movement Prototype

```gdscript
# 最小移动原型 - 10分钟
extends CharacterBody2D

const SPEED = 300.0
const JUMP = -400.0
const GRAVITY = 1000.0

func _physics_process(delta):
    velocity.y += GRAVITY * delta
    velocity.x = Input.get_axis("left", "right") * SPEED
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = JUMP
    move_and_slide()
```

### Combat Prototype

```gdscript
# 最小战斗原型 - 30分钟
extends Area2D

@onready var sprite = $Sprite2D
var health = 100

signal died

func take_damage(amount: int):
    health -= amount
    sprite.modulate = Color.RED
    await get_tree().create_timer(0.1).timeout
    sprite.modulate = Color.WHITE
    if health <= 0:
        died.emit()
        queue_free()
```

### UI Prototype

```gdscript
# 最小UI原型 - 15分钟
extends Control

@onready var health_bar = $HealthBar
@onready var score_label = $ScoreLabel

var health = 100:
    set(v):
        health = v
        health_bar.value = health

var score = 0:
    set(v):
        score = v
        score_label.text = str(score)
```

---

## Prototype Gallery

### Save Your Prototypes

```
prototypes/
├── 2024-01-15-movement-test/
│   ├── readme.md  ← 记录结论
│   └── scene.tscn
├── 2024-01-20-combat-test/
│   ├── readme.md
│   └── scene.tscn
└── archived/  ← 失败的原型
```

### Prototype README Template

```markdown
# 原型: [Name]

**日期**: [Date]
**耗时**: [Hours]
**结论**: 成功/失败/迭代

## 验证的问题
[What were we testing?]

## 结论
[What did we learn?]

## 有趣发现
[Any surprises?]

## 代码状态
[可复用/需重写/丢弃]

## 截图/视频
[If any]
```

---

## Error Handling

| Error | Fallback |
|-------|----------|
| Prototype takes too long | Reduce scope further |
| Code gets complex | Delete and restart simpler |
| Can't decide if fun | Test with someone else |
| Feature creep | Refer to scope document |

---

## Quick Reference

| 目标 | 时间 | 范围 |
|------|------|------|
| 验证机制 | 1-2小时 | 单一核心循环 |
| 验证技术 | 2-4小时 | 最小可行实现 |
| 验证体验 | 4-8小时 | 包含基础美术 |

**Remember: Done is better than perfect. You can always make another prototype.**