---
name: arkts-static-spec
description: "ArkTS static language specification reference for OpenHarmony. Use this skill when reading or writing ArkTS (.ets), explaining ArkTS type-system and static-semantics rules, validating code against the ArkTS spec, investigating ArkTS compile-time behavior, or comparing ArkTS with TypeScript migration guidance."
---

# ArkTS Static Language Specification

Complete reference for the ArkTS programming language, including official specification and TypeScript migration guide.


## ⚠️ 使用原则（重要）

在使用本 skill 回答问题时，**必须严格遵守**以下原则：

1. **严格按照 skill 文档内容回答**
   - 所有回答必须基于 spec/ 和 cookbook/ 目录下的文档内容
   - 不添加文档之外的假设或推断

2. **明确标注文档未说明的内容**
   - 如果 skill 文档中没有明确说明某个特性，必须在回答中标注：
     - **"⚠️ skill 文档未明确说明，待使用者自行确认"**
   - 不要基于 TypeScript 或其他语言的特性进行假设

3. **将 ArkTS 视为独立的静态语言**
   - ArkTS 是一个独立的静态语言，**不是** TypeScript 的超集
   - 不要假设 TypeScript 的特性在 ArkTS 中都支持
   - 以 ArkTS 官方规范为准，不以 TypeScript 语法为准

---

## 目录结构

本技能分为两个主要部分：

```
arkts-static-spec/
├── spec/              # ArkTS 语言规范
│   ├── types.md       # 类型系统
│   ├── classes.md     # 类声明
│   ├── expressions.md # 表达式和运算符
│   ├── statements.md  # 语句和控制流
│   ├── generics.md    # 泛型
│   ├── annotations.md # 注解和装饰器
│   ├── modules.md     # 模块系统
│   ├── lexical.md     # 词法结构
│   ├── names.md       # 声明和作用域
│   ├── conversions.md # 类型转换
│   ├── interfaces.md  # 接口
│   ├── enums.md       # 枚举
│   ├── errors.md      # 错误处理
│   ├── concurrency.md # 并发和异步
│   ├── stdlib.md      # 标准库
│   └── experimental.md# 实验性特性
│
└── cookbook/          # TypeScript 迁移指南
    ├── index.md       # 迁移指南总览
    ├── recipes.md     # 详细迁移食谱（144+ 项）
    └── compatibility.md # TypeScript vs ArkTS 兼容性详情
```

---

## 第一部分：ArkTS 语言规范 (spec/)

官方 ArkTS 语言规范参考，按主题组织。

### 核心规范文件

| 文件 | 内容 | 适用场景 |
|------|------|---------|
| [types.md](spec/types.md) | 类型系统、预定义类型 | 查询类型、类型推断、默认值 |
| [classes.md](spec/classes.md) | 类声明、访问修饰符、继承 | 定义类、实现接口、继承 |
| [expressions.md](spec/expressions.md) | 运算符、优先级 | 表达式求值、运算符使用 |
| [statements.md](spec/statements.md) | 控制流、循环、try-catch | if/else、for、while、异常处理 |
| [generics.md](spec/generics.md) | 泛型类型和函数 | 编写泛型代码、类型约束 |
| [annotations.md](spec/annotations.md) | 装饰器和元数据 | 使用 @Decorator |
| [modules.md](spec/modules.md) | Import/export、命名空间 | 模块组织、导入导出 |
| [lexical.md](spec/lexical.md) | 标识符、关键字、字面量 | 词法分析、语法规则 |
| [names.md](spec/names.md) | 声明、作用域、可见性 | 变量作用域、命名冲突 |
| [conversions.md](spec/conversions.md) | 类型转换和上下文 | 类型转换规则 |
| [interfaces.md](spec/interfaces.md) | 接口声明和实现 | 定义接口、实现契约 |
| [enums.md](spec/enums.md) | 枚举类型 | 使用枚举 |
| [errors.md](spec/errors.md) | 错误处理和 try 语句 | 异常处理、throw 语句 |
| [concurrency.md](spec/concurrency.md) | Async/await、TaskPool | 异步编程、并发 |
| [stdlib.md](spec/stdlib.md) | 标准库 API | 内置对象和函数 |
| [experimental.md](spec/experimental.md) | 实验性特性 | FixedArray、char、函数重载等 |

---

## 第二部分：TypeScript 迁移指南 (cookbook/)

从 TypeScript 迁移到 ArkTS 的完整指南，包含 144+ 个详细迁移食谱和兼容性说明。

### 迁移指南文件

| 文件 | 内容 | 适用场景 |
|------|------|---------|
| [index.md](cookbook/index.md) | 迁移指南总览 | 了解迁移原因、设计原则、快速入门 |
| [recipes.md](cookbook/recipes.md) | 144+ 详细迁移食谱 | 查询具体语法如何转换、常见问题解决 |
| [compatibility.md](cookbook/compatibility.md) | TypeScript vs ArkTS 兼容性详情 | 了解行为差异、数值语义、数组赋值等 |

---

## 快速开始

### ArkTS 类型注解

```typescript
let num: number = 42
const str: string = "hello"
let arr: number[] = [1, 2, 3]
```

### ArkTS 类声明

```typescript
class Person {
  private name: string
  public age: number

  constructor(name: string, age: number) {
    this.name = name
    this.age = age
  }

  public introduce(): string {
    return `I'm ${this.name}, ${this.age} years old`
  }
}
```

### 泛型函数

```typescript
function identity<T>(value: T): T {
  return value
}

let num = identity<number>(42)
let str = identity<string>("hello")
```

### 异步函数

```typescript
async function fetchData(): Promise<string> {
  const response = await fetch("https://example.com")
  return await response.text()
}
```

---

## 类型系统速查

### 预定义类型

| 分类 | 类型 | 说明 |
|------|------|------|
| 数值 | `byte`, `short`, `int`, `long`, `float`, `double`, `number`, `bigint` | 整数和浮点数 |
| 布尔 | `boolean` | true/false |
| 字符 | `char` | 实验性，使用 `c'A'` 语法 |
| 字符串 | `string` | 文本数据 |
| 特殊 | `void`, `null`, `undefined`, `never` | 特殊用途 |
| 对象 | `Object`, `object` | 对象类型 |

**注意**：`any` 和 `unknown` 在 ArkTS 中不支持，必须使用显式类型。

### 类型运算符

- 联合类型：`T | U`
- 交集类型：`T & U`
- 数组类型：`T[]` 或 `Array<T>`
- 只读数组：`readonly T[]`

---

## TypeScript 迁移速查

### 常见转换

| TypeScript | ArkTS | 说明 |
|-----------|-------|------|
| `var x = 10` | `let x: number = 10` | 必须使用 `let`，明确类型 |
| `let x: any` | `let x: SpecificType` | 禁止 `any`，使用具体类型 |
| `let {a, b} = obj` | `let a = obj.a; let b = obj.b` | 不支持对象解构 |
| `"prop" in obj` | `obj instanceof Class` | 不支持 `in` 运算符 |
| `import m = require("mod")` | `import * as m from "mod"` | 使用 ES6 import |

### 代码保持率

- **完全支持**（无需修改）：90% - 97%
- **部分支持**（少量重构）：约 2% - 8%
- **不支持**（需要重构）：约 1%

---

## 查找指南

### 查询 ArkTS 语言规范

根据主题选择对应的规范文件：

- **类型相关问题**：查看 [spec/types.md](spec/types.md)、[spec/conversions.md](spec/conversions.md)
- **面向对象特性**：查看 [spec/classes.md](spec/classes.md)、[spec/interfaces.md](spec/interfaces.md)、[spec/enums.md](spec/enums.md)
- **语法相关问题**：查看 [spec/lexical.md](spec/lexical.md)、[spec/expressions.md](spec/expressions.md)、[spec/statements.md](spec/statements.md)
- **泛型编程**：查看 [spec/generics.md](spec/generics.md)
- **模块系统**：查看 [spec/modules.md](spec/modules.md)
- **并发编程**：查看 [spec/concurrency.md](spec/concurrency.md)
- **装饰器和注解**：查看 [spec/annotations.md](spec/annotations.md)
- **标准库 API**：查看 [spec/stdlib.md](spec/stdlib.md)
- **实验性特性**：查看 [spec/experimental.md](spec/experimental.md)

### 查询 TypeScript 迁移问题

- **迁移概述和原则**：查看 [cookbook/index.md](cookbook/index.md)
- **具体语法如何转换**：查看 [cookbook/recipes.md](cookbook/recipes.md)
- **行为差异和兼容性**：查看 [cookbook/compatibility.md](cookbook/compatibility.md)

---

## ArkTS vs TypeScript 关键差异

### 1. 静态类型强制执行

| 特性 | TypeScript | ArkTS |
|------|-----------|-------|
| 静态类型 | 可选 | 强制 |
| `any` 类型 | 允许 | 禁止 |
| `unknown` 类型 | 允许 | 禁止 |
| 类型推断 | 可选 | 必须 |

### 2. 对象布局固定

| 特性 | TypeScript | ArkTS |
|------|-----------|-------|
| 运行时添加属性 | 允许（用 `as any` 绕过） | 禁止 |
| 删除属性 | 允许（用 `as any` 绕过） | 禁止 |
| 对象布局 | 可变 | 固定 |

### 3. Null 安全

| 特性 | TypeScript | ArkTS |
|------|-----------|-------|
| `null` 赋值给非空类型 | 可选模式下禁止 | 强制禁止 |
| `undefined` 作为值 | 允许 | 严格限制 |

### 4. 数值语义

```typescript
let n = 1
console.log(n / 2)

// TypeScript: 0.5（浮点除法）
// ArkTS: 0（整数除法）
```

---

## 访问修饰符

| 修饰符 | 可访问性 |
|--------|---------|
| `public` | 任何地方（默认） |
| `private` | 仅类内部 |
| `protected` | 类和子类 |
| `readonly` | 初始化后不可变 |
| `static` | 类级别，非实例级别 |

---

## 常见设计模式

### 单例模式

```typescript
class Singleton {
  private static instance: Singleton
  private constructor() {}

  public static getInstance(): Singleton {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton()
    }
    return Singleton.instance
  }
}
```

### 工厂模式

```typescript
interface Product {
  operation(): string
}

class ConcreteProductA implements Product {
  operation(): string {
    return "Product A"
  }
}

class Factory {
  static create(type: string): Product {
    if (type === "A") {
      return new ConcreteProductA()
    }
    throw new Error("Unknown product type")
  }
}
```

---

## 为什么选择 ArkTS？

### 优势

1. **程序稳定性**
   - 严格类型检查，减少运行时错误
   - 编译时类型验证
   - 字段必须初始化

2. **程序性能**
   - 编译为字节码，执行更快
   - 消除运行时类型检查开销
   - 针对移动设备优化

3. **代码可读性**
   - 静态类型让代码意图清晰
   - 对象布局固定，行为可预测

### 迁移成本

- **代码保持率**：90% - 97%（遵循最佳实践）
- **主要调整**：移除 `any`、使用 `let` 代替 `var`
- **学习曲线**：TypeScript 开发者易于上手

---

## 控制流速查

### if-else

```typescript
if (condition) {
  // ...
} else {
  // ...
}
```

### 循环

```typescript
// while 循环
while (condition) {
  // ...
}

// for 循环
for (let i: int = 0; i < 10; i++) {
  // ...
}

// for-of 循环
for (const item of array) {
  // ...
}
```

### 错误处理

```typescript
try {
  // 可能抛出错误的代码
} catch (e: Error) {
  // 处理错误
} finally {
  // 清理（总是执行）
}
```

---

## 迁移检查清单

### 优先级 1：必须修复（ERROR 级别）

- [ ] 替换所有 `var` 为 `let`
- [ ] 移除所有 `any` / `unknown` 类型
- [ ] 移除 `Symbol()` API 使用
- [ ] 移除私有 `#` 标识符
- [ ] 确保类型和命名空间名称唯一
- [ ] 移除非标识符属性名
- [ ] 移除调用签名和构造签名类型
- [ ] 移除 `in` 运算符
- [ ] 移除对象解构
- [ ] 替换 `require` 为标准 `import`
- [ ] 移除 `export =` 语法

### 优先级 2：代码改进建议（WARNING 级别）

- [ ] 检查字段初始化
- [ ] 审查对象属性访问模式
- [ ] 确保类型安全

---

## 完整参考

- **ArkTS 语言规范**：[spec/](spec/)
- **TypeScript 迁移指南**：[cookbook/](cookbook/)
- **原始规范文档**：`D:\arkcompiler\runtime_core\static_core\plugins\ets\doc\spec\`
- **原始 Cookbook**：`D:\arkcompiler\runtime_core\static_core\plugins\ets\doc\cookbook\`
