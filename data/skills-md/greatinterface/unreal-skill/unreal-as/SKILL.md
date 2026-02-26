---
name: unreal-as
description: 面向进阶开发者的 Unreal Engine AngelScript API 快速查询工具。适用于查询语法、生命周期、输入、物理、AI、工具类与 GAS 相关用法，并需要示例代码或参考文档导航时使用。
---

# Unreal Engine AngelScript API 快速查询

## Skill 定位
为 Unreal Engine AngelScript API 提供快速索引与场景化导航，帮助在常见任务中快速定位参考文档与示例。

## 项目约定
- 遵循当前项目的目录结构与命名规范（如脚本目录、前缀规则等）
- 若仓库要求双语注释或特定注释规范，需严格遵守
- 若项目为单机玩法，避免引入联机/网络逻辑（除非明确要求）

## 快速索引

按开发场景快速定位相关文档：

| 场景                                              | 参考文档                                                     |
| ------------------------------------------------- | ------------------------------------------------------------ |
| 创建自定义 Actor/Component、设置属性、定义函数    | [api-class-system.md](references/api-class-system.md)        |
| 使用数组、映射、结构体、枚举管理数据              | [api-data-structures.md](references/api-data-structures.md)  |
| 实现 BeginPlay、Tick、构造脚本、委托事件          | [api-lifecycle-events.md](references/api-lifecycle-events.md) |
| 绑定输入、处理角色控制、键盘事件                  | [api-input-control.md](references/api-input-control.md)      |
| 检测重叠、移动对象、物理交互                      | [api-physics-collision.md](references/api-physics-collision.md) |
| 创建 Behavior Tree 节点（Decorator/Service/Task） | [api-ai-system.md](references/api-ai-system.md)              |
| 使用数学函数、定时器、格式化字符串                | [api-utilities.md](references/api-utilities.md)              |
| 使用 Mixin 方法、组件系统、访问修饰符             | [api-advanced-features.md](references/api-advanced-features.md) |
| 使用 Gameplay Ability System (GAS) 监听属性变化   | [api-gameplay-ability-system.md](references/api-gameplay-ability-system.md) |

## 常见任务速查
- 创建可配置 Actor、组件与可调用方法 → [api-class-system.md](references/api-class-system.md)
- 角色输入与移动控制 → [api-input-control.md](references/api-input-control.md)
- 碰撞与重叠事件处理 → [api-physics-collision.md](references/api-physics-collision.md)
- 行为树节点扩展 → [api-ai-system.md](references/api-ai-system.md)
- 定时器与工具函数 → [api-utilities.md](references/api-utilities.md)
- GAS 属性与监听 → [api-gameplay-ability-system.md](references/api-gameplay-ability-system.md)

## 使用指南
- 优先使用“快速索引”或“常见任务速查”定位到对应的 reference 文档
- 在 reference 文档中检索关键词（如 `UPROPERTY`、`TArray`、`SetTimer`）
- 按 reference 文档的结构依次查看：场景描述 → API 概览 → 核心示例 → 注意事项

## 注意事项
- ue-as 不支持 `UINTERFACE()` 和 `TScriptInterface`, 如果用户要求需要使用接口（e.g. 交互系统），请告知用户是否用 `Component` 进行代替
- 所有暴露给蓝图/编辑器的成员必须使用 `UPROPERTY()` 或 `UFUNCTION()` 标记
- 修改 struct 属性需要完整重载，无法热重载
- 定时器和委托绑定的函数必须是 `UFUNCTION()`
- 使用 `default` 关键字设置组件和父类属性，等价于 C++ 构造函数
- 访问修饰符可以精细控制不同类别的访问权限
