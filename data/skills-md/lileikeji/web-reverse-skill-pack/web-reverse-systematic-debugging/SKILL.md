---
name: web-reverse-systematic-debugging
description: |
  用证据链和根因分析解决逆向中的不一致问题，禁止随机试错。遇到签名不一致、补环境失败、Hook 无效、结果漂移时调用。
  触发词：「不一致」「对不上」「结果差一点」「Hook 不生效」「补环境失败」「结果漂移」「排错」。
  边界：本 Skill 只做诊断和修复建议，不替代其他 Skill 的核心职责。
  签名算法问题转交 param-encryptor；环境差异转交 env-patcher；混淆问题转交 ast-deobfuscation。
---

# 逆向证据链排错

## 何时使用

遇到这些问题就用：

- 签名差一点点
- Hook 有输出但结果不对
- 补环境能跑但不一致
- 结果漂移
- 反混淆后逻辑看着对但跑不对

## 铁律

```text
先观察，再假设，再测试，最后修复。
```

禁止：

- 没有假设就改代码
- 一次改多个变量
- 连续随机试错

## 最小流程

### Observe

先记清：

- 失败在哪一步
- 真实值 / 当前值
- 差异层级：字段 / 字节 / 流程

### Hypothesize

写成一句话：

- 为什么不一致
- 哪个变量最可疑

### Test

一次只测一个变量，例如：

- 固定时间戳
- 固定随机数
- 只改 1 个环境字段
- 只换 1 个 Hook 点
- 只比 1 层中间串

### Fix

只有假设成立后才能修；修完必须重验样本。

## 优先排查顺序

1. 输入是否一致
2. 动态字段是否处理干净
3. 中间串是否一致
4. 编码是否一致
5. 算法参数是否一致
6. 环境是否一致
7. 调用点是否找对

## 按问题类型的专业 Skill 路由

| 根因类型 | 转交 Skill | 典型症状 |
|---------|-----------|---------|
| 算法参数错误（Key/IV/Mode/Padding） | `param-encryptor` | 本地加密输出与浏览器不同 |
| 浏览器 API 缺失或行为不一致 | `env-patcher` | `Illegal invocation` / `undefined` / 指纹不匹配 |
| 混淆还原不完整 | `ast-deobfuscation` | 反混淆后函数调用链断裂 |
| 验证码参数构造错误 | `captcha-solver` | 验证码校验失败 |
| 路线根本错误 | `web-reverse-brainstorming` | 整体方向需要重新评估 |

## 典型问题

- 签名不一致：字段、顺序、空值、hash 输入串
- 补环境失败：缺对象、缺属性、时序不对
- Hook 无效：注入晚了、闭包缓存、逻辑在 iframe/worker/wasm
- 结果漂移：样本会话不同、服务端挑战值参与、cookie/token 演化

## 停止条件

出现这些情况必须停下重整：

- 连续 3 次修改都没有明确假设
- 每次都同时改多个变量
- 证据越来越多但没整理差异
- 已不清楚当前结果来自哪版代码

## Phase Mapping

本 Skill 可在 CLAUDE.md Phase 2-4 任意阶段按需插入：

| Phase | 触发条件 | 与专业 Skill 的协作 |
|-------|---------|-------------------|
| Phase 2 定位加密 | Hook 无效 / 找不到加密入口 | 可能需要 `ast-deobfuscation` 先还原混淆 |
| Phase 3 方案制定 | Plan 假设被证据推翻 | 回到 `web-reverse-brainstorming` 重估路线 |
| Phase 4 代码还原 | 签名不一致 / 结果漂移 | `param-encryptor` 查算法参数；`env-patcher` 查环境差异 |

## 出口

- 需要重整样本时配合 `web-reverse-test-driven-development`
- 根因涉及路线错误时回到 `web-reverse-brainstorming`

## Related Skills

| Skill | 职责 | 何时调用 |
|-------|------|---------|
| `web-reverse-master` | 全流程编排 | 需要完整逆向分析流程 |
| `web-reverse-workflow` | 工作流入口 | 需要判断当前阶段 |
| `web-reverse-test-driven-development` | 样本驱动复现 | 样本需要重整 |
| `web-reverse-brainstorming` | 路线设计 | 根因是路线错误 |
| `captcha-solver` | 验证码求解 | 排查验证码参数问题 |
| `param-encryptor` | 加密参数生成 | 排查签名算法参数 |
| `env-patcher` | 补环境 | 排查环境差异 |
| `ast-deobfuscation` | JS 反混淆 | 排查混淆还原问题 |
