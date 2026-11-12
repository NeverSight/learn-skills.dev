---
name: android-arch-generator
description: >-
  Android architecture pattern code generator for MVVM, MVI, Clean Architecture.
  Generate ViewModel, Repository, UseCase, State, Intent, SideEffect boilerplate.
  Use when creating new feature, new screen, new page, new module,
  scaffolding Android architecture code, setting up MVVM with LiveData or StateFlow,
  MVI with unidirectional data flow, Clean Architecture layers.
  Supports Hilt/Koin dependency injection, Coroutines, Flow, LiveData.
  Generates Kotlin code with proper package structure.
  Zero external dependencies — pure Python standard library.
---

# Android 架构模式代码生成器

输入 Feature 名称，自动生成 MVVM/MVI/Clean Architecture 代码骨架。

## 适用场景

- 创建新 Feature / 新页面
- 搭建模块架构骨架
- 统一团队架构模式
- 快速原型开发

## 架构模式对比

| 特性 | MVVM | MVI | Clean Architecture |
|------|------|-----|-------------------|
| 复杂度 | 低 | 中 | 高 |
| 适合场景 | 常规CRUD页面 | 复杂交互/状态管理 | 大型项目/多人协作 |
| 数据流 | 双向 | 单向 | 单向(分层) |
| 核心组件 | ViewModel+LiveData | State+Intent+Reducer | UseCase+Repository+Entity |
| 推荐 | 中小型项目 | 状态复杂的页面 | 企业级项目 |

## 使用方式

脚本位置：`scripts/arch_generator.py`（相对于本 Skill 目录）

### 生成 MVVM 代码

```bash
# 基本用法：生成 MVVM 架构的 Feature
python3 <SKILL_DIR>/scripts/arch_generator.py generate <FeatureName> \
    --pattern mvvm \
    --package com.example.app.feature \
    --output <output_dir>

# 使用 StateFlow (默认 LiveData)
python3 <SKILL_DIR>/scripts/arch_generator.py generate <FeatureName> \
    --pattern mvvm \
    --package com.example.app.feature \
    --flow stateflow

# 指定 DI 框架
python3 <SKILL_DIR>/scripts/arch_generator.py generate <FeatureName> \
    --pattern mvvm \
    --package com.example.app.feature \
    --di hilt
```

### 生成 MVI 代码

```bash
python3 <SKILL_DIR>/scripts/arch_generator.py generate <FeatureName> \
    --pattern mvi \
    --package com.example.app.feature
```

### 生成 Clean Architecture 代码

```bash
python3 <SKILL_DIR>/scripts/arch_generator.py generate <FeatureName> \
    --pattern clean \
    --package com.example.app.feature
```

### 查看模式说明

```bash
# 查看所有支持的架构模式
python3 <SKILL_DIR>/scripts/arch_generator.py patterns

# 查看特定模式的详细说明
python3 <SKILL_DIR>/scripts/arch_generator.py explain mvvm
```

## 生成文件示例 (MVVM)

```
feature/
├── ui/
│   ├── HomeFragment.kt        # Fragment + ViewBinding
│   └── HomeViewModel.kt       # ViewModel + LiveData/StateFlow
├── data/
│   ├── HomeRepository.kt      # 数据仓库
│   └── model/
│       └── HomeUiState.kt     # UI状态模型
└── di/
    └── HomeModule.kt          # DI模块 (Hilt/Koin)
```

## 生成文件示例 (MVI)

```
feature/
├── ui/
│   ├── HomeFragment.kt        # Fragment (收集State, 发送Intent)
│   └── HomeViewModel.kt       # ViewModel (Reducer)
├── mvi/
│   ├── HomeIntent.kt          # 用户意图 (sealed class)
│   ├── HomeState.kt           # UI状态 (data class)
│   └── HomeSideEffect.kt      # 副作用 (sealed class)
├── data/
│   └── HomeRepository.kt
└── di/
    └── HomeModule.kt
```

## AI 使用指南

当用户提到以下场景时，自动使用本工具：
- "创建一个新页面" / "新建Feature" → 确认架构模式后 `generate`
- "帮我搭个MVVM架构" → `generate --pattern mvvm`
- "用MVI写一个" → `generate --pattern mvi`
- "这三种架构有什么区别" → `explain` 或直接参考上方对比表
