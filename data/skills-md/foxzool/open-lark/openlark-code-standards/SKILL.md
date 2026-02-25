---
name: openlark-code-standards
description: OpenLark 项目代码规范检查技能。用于快速审查仓库内的架构一致性、API 实现套路、参数校验、命名与导出规范，并输出可执行检查清单与证据路径。
argument-hint: "[crate-name|path]"
allowed-tools: Read, Grep, Glob, Bash
---

# OpenLark 代码规范检查（Skill）

## 适用场景

- 用户要求“检查项目代码规范”
- 新增 API 前想确认实现套路是否一致
- 评审 PR 时需要快速验证是否遵循 OpenLark 既有约定
- 发现模块风格漂移，想做一次统一体检

## 目标

输出一份可落地的规范检查结果，包含：

- 规范结论（通过/风险）
- 规则-证据对（每条规则附 `path:line`）
- 风险分级（P0/P1/P2）
- 新 API 最小检查清单（可直接用于 PR Review）

## 检查范围

优先覆盖：

- `crates/openlark-core`
- `crates/openlark-client`
- `crates/openlark-docs`
- `crates/openlark-communication`

可按参数缩小为某个 crate 或目录。

## 核心检查项

### 1) API 实现套路一致性

- 是否使用 `Request/Response + Builder` 模式
- 是否提供 `execute()` 与 `execute_with_options(RequestOption)`
- 是否通过 `Transport::request(...)` 发送请求

### 2) 端点定义规范

- 是否使用 `ApiEndpoint` 枚举/端点常量
- 是否避免手写业务 URL
- 是否通过 `to_url()` 或统一端点入口生成路径

### 3) 参数校验规范

- 必填校验是否统一用 `openlark_core::validate_required!`
- 字符串是否优先 `trim()` 后再校验
- 列表字段是否校验非空与长度上限（如 `validate_required_list!`）

### 4) 命名与公开 API 表达

- `Client/Service/Resource/Request/Builder` 命名是否语义清晰
- 对外入口是否统一（避免同义入口并存）
- meta 调用链命名是否与仓库约定一致

### 5) 导出与 feature gating

- `mod.rs` 与 `prelude` 是否完整导出新增 API
- `Cargo.toml` feature 与 `#[cfg(feature = "...")]` 是否对齐
- 是否存在导出但不可编译或不可访问路径

## 输出模板（必须）

1. 结论概览（3-6 条）
2. 规则-证据对（至少 8 条）
   - 规则
   - 证据（`path:line`）
   - 风险等级（P0/P1/P2）
   - 修复建议
3. 新 API 最小检查清单（5-8 条）
4. 建议行动项（按优先级排序）

## 推荐执行顺序

1. 先读 `AGENTS.md` 与目标 crate 的 `AGENTS.md/CLAUDE.md`
2. 再扫规则高频证据：`api_endpoints`、`execute_with_options`、`validate_required`、`prelude`、`mod.rs`
3. 最后输出规则-证据对与整改建议

## 重点提醒

- 结论必须基于代码证据，不做“纯经验判断”
- 证据至少精确到文件路径，推荐精确到 `path:line`
- 不在规范检查中进行大规模重构，先给出可执行清单

## 与其他技能的关系

- 需要审查整体架构与公共 API：`openlark-design-review`
- 只聚焦校验写法统一：`openlark-validation-style`
- 需要新增/重构具体 API：`openlark-api`
- 需要做覆盖率统计：`openlark-api-validation`

## 技能分流决策表

| 场景 | 优先技能 | 何时转交 |
|---|---|---|
| 只想做一次项目规范体检（给出规则-证据对和风险清单） | `openlark-code-standards` | 若发现架构级冲突/公共 API 设计分歧，转 `openlark-design-review` |
| 重点是架构收敛、范式选型、兼容策略（含 breaking 评估） | `openlark-design-review` | 若需要补充全仓规范一致性证据，可回补 `openlark-code-standards` |
| 只处理 `validate()`、`validate_required!`、空白字符串与校验聚合 | `openlark-validation-style` | 若校验问题已扩展到命名/导出/端点体系，转 `openlark-code-standards` |
| 新增或重构某个具体 API 文件（Request/Response/Builder/导出） | `openlark-api` | 若实现前需先做规范体检，先跑 `openlark-code-standards` |
| 关注 API 覆盖率、实现数量、缺失清单 | `openlark-api-validation` | 若覆盖率问题背后是设计不一致，转 `openlark-design-review` |

### 快速判断

- 问题是“这个项目现在规范是否一致” → `openlark-code-standards`
- 问题是“这个设计该怎么收敛” → `openlark-design-review`
- 问题是“这个校验写法到底怎么统一” → `openlark-validation-style`
- 问题是“我现在就要实现某个 API” → `openlark-api`

## 关键词触发映射

| 用户关键词/表述 | 建议技能 |
|---|---|
| 代码规范、规范检查、风格一致性、体检、对齐约定 | `openlark-code-standards` |
| 架构设计、public API、收敛方案、feature gating、兼容策略、breaking change | `openlark-design-review` |
| validate、必填校验、validate_required、空白字符串、校验聚合 | `openlark-validation-style` |
| 新增 API、重构 API、Builder、Request/Response、mod.rs 导出 | `openlark-api` |
| 覆盖率、实现数量、缺失 API、统计、对比 CSV | `openlark-api-validation` |

### 组合关键词优先级

- 同时出现“规范检查 + 覆盖率”时，先用 `openlark-api-validation` 产出缺失清单，再用 `openlark-code-standards` 做规范归因。
- 同时出现“规范检查 + 架构收敛”时，先用 `openlark-code-standards` 做现状证据，再转 `openlark-design-review` 定迁移方案。
- 同时出现“新增 API + 校验统一”时，实现阶段用 `openlark-api`，校验规则判定用 `openlark-validation-style`。
