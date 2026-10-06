---
name: web-reverse-executing-plans
description: |
  严格按逆向计划推进并逐步验收，不允许边做边漂移。已有实施计划，准备按证据链一步步执行时调用。
  触发词：「按计划执行」「开始执行」「下一步」「逐步验收」。
  边界：本 Skill 只执行已有计划，不修改计划。遇到计划需要调整时回到 writing-plans。
  执行中需调用专业 Skill 时（captcha-solver / param-encryptor / env-patcher / ast-deobfuscation）可直接调用。
---

# 逆向按计划执行

## 何时使用

计划已经写好，准备正式执行时使用。

## 铁律

```text
一步一验证；证据冲突先停下，不要硬做。
```

禁止：

- 一步没验证就做下一步
- 中途偷偷换路线
- 看到冲突证据还继续硬试
- 因为"差不多"就宣布完成

## 执行前检查

- 计划文件可读
- 输入材料已到位
- 产物目录已确定
- 成功标准明确

不满足就先回到：

- `web-reverse-writing-plans`
- `web-reverse-brainstorming`

## 最小流程

### 1. 读计划并做现实检查

确认：

- 样本是否齐
- 命令是否能跑
- 哪些步骤依赖前置产物

### 2. 逐任务执行

每个任务固定顺序：

1. 执行动作
2. 保存产物
3. 运行验证
4. 记录结论

### 3. 每步留证据

至少保留以下之一：

- HAR
- Hook 日志
- 调用栈
- 环境差异
- 样本对照
- 字节级 diff

### 4. 阶段复盘

完成一个阶段后回答：

- 新证据支持什么
- 推翻什么
- 下一步还是否成立

## 专业 Skill 调用

执行中遇到以下操作时，调用对应专业 Skill：

| 执行操作 | 调用 | 时机 |
|---------|------|------|
| 验证码识别+轨迹+提交 | `captcha-solver` | 任务涉及验证码 |
| 签名/加密参数生成 | `param-encryptor` | 任务涉及加密函数复现 |
| 浏览器环境模拟 | `env-patcher` | 任务涉及 SDK 补环境 |
| JS 代码反混淆 | `ast-deobfuscation` | 任务涉及混淆代码还原 |

## 执行 Trace 示例

> 以下展示一个完整的逆向执行过程，作为执行 trace 的标准模板。

### 示例：还原某站登录接口 sign 参数

```markdown
## 任务 1：导出登录请求 HAR

**执行动作：**
- 打开浏览器 DevTools → Network → 勾选 Preserve log
- 执行登录操作，捕获 POST /api/login 请求
- 右键请求 → Copy as cURL / 导出 HAR

**保存产物：**
- captures/login_request.har ✅
- captures/login_headers.txt ✅

**验证标准：**
- [x] HAR 文件包含 POST /api/login
- [x] 请求 Body 包含 sign 字段（非明文）
- [x] 响应状态码 200

**结论：** 登录接口 sign 参数为 32 位 hex，疑似 MD5。

---

## 任务 2：Hook 定位 sign 生成点

**执行动作：**
- 使用 js-reverse-mcp.search_in_sources 搜 "sign"
- 使用 js-reverse-mcp.break_on_xhr 拦截 /api/login
- get_paused_info 获取调用栈

**保存产物：**
- captures/callstack_sign.txt ✅
- 定位到 app.js:4521 function generateSign(params)

**验证标准：**
- [x] 断点触发
- [x] 调用栈显示 sign 在发送前被赋值
- [x] 确认 generateSign 函数输入为明文 params，输出为 32 位 hex

**结论：** sign = MD5(sorted_params + secret_key)，调用 param-encryptor 配方1。

---

## 任务 3：复现 MD5 签名

**执行动作：**
- 调用 param-encryptor Step 3：导出 3 组输入输出样本
- 调用 param-encryptor Step 4：匹配配方1 (hash-md5)
- 本地实现并对比

**保存产物：**
- captures/sign_samples.json (3 组对照) ✅
- src/signer.py ✅

**验证标准：**
- [x] 3 组样本全部通过
- [x] 本地 MD5 输出与浏览器输出逐字节一致
- [x] 固定时间戳重跑稳定

**结论：** sign = MD5(params_sorted_by_key + "secret_xxx")。进入 Phase 4 集成。
```

### 证据记录模板

```markdown
### 任务 N 执行记录

| 字段 | 内容 |
|------|------|
| 任务 | [任务名称] |
| 开始时间 | HH:MM |
| 结束时间 | HH:MM |
| 执行动作 | 1. xxx  2. xxx |
| 产物 | [文件路径列表] |
| 验证结果 | ✅ 通过 / ❌ 失败 |
| 失败原因 | [如失败] |
| 下一步 | [继续/回退/调整] |
```

### 常用执行命令模板

```bash
# 抓包：从 HAR 中提取目标请求
# 使用浏览器 DevTools 或 mitmproxy 捕获

# 源码搜索：在 JS 中定位参数名
# js-reverse-mcp → search_in_sources "sign"

# Hook 注入：在导航前注入 Hook
# js-reverse-mcp → inject_before_load [Hook 代码]

# 断点：拦截含目标参数的请求
# js-reverse-mcp → break_on_xhr "/api/login"

# 调用栈：断点触发后获取调用链
# js-reverse-mcp → get_paused_info

# 样本导出：追踪加密函数输入输出
# js-reverse-mcp → trace_function "generateSign"

# 本地验证：逐字节对比
# Python: assert local_sign == browser_sign
```

## 允许调整

以下情况允许改步骤，但必须说明原因并更新计划：

- 当前步骤缺输入
- Hook 点太晚
- 原假设已被证据推翻

## 必须停止

出现这些情况就切到 `web-reverse-systematic-debugging`：

- 样本拿不到
- 结果持续漂移
- Hook 有输出但不知是不是最终值
- 复现器长期不一致
- 计划假设与证据冲突

## 完成标准

- 关键任务都执行了
- 每阶段都有产物
- 结论有证据
- 复现或定位结果经验证成立

## Phase Mapping

本 Skill 对应 CLAUDE.md Phase 2-4（加密定位→方案执行→代码还原）：

| Phase | 本 Skill 的角色 | 与专业 Skill 的协作 |
|-------|----------------|-------------------|
| Phase 2 定位加密 | ✅ 核心参与：按计划执行 Hook + 源码搜索 | 需反混淆时调用 `ast-deobfuscation` |
| Phase 3 方案制定 | ✅ 辅助：执行 Plan 中的验证步骤 | — |
| Phase 4 代码还原 | ✅ 核心参与：执行 signer.py / main.py 编码 | 签名/加密调用 `param-encryptor`；补环境调用 `env-patcher`；验证码调用 `captcha-solver` |

## 出口

- 实现/校验阶段配合 `web-reverse-test-driven-development`
- 遇到异常切 `web-reverse-systematic-debugging`

## Related Skills

| Skill | 职责 | 何时调用 |
|-------|------|---------|
| `web-reverse-master` | 全流程编排 | 需要完整逆向分析流程 |
| `web-reverse-workflow` | 工作流入口 | 需要判断当前阶段 |
| `web-reverse-writing-plans` | 拆步骤 | 计划需要调整 |
| `web-reverse-test-driven-development` | 样本驱动复现 | 进入编码复现阶段 |
| `web-reverse-systematic-debugging` | 证据链排错 | 结果不一致 |
| `captcha-solver` | 验证码求解 | 执行中涉及验证码 |
| `param-encryptor` | 加密参数生成 | 执行中涉及签名/加密 |
| `env-patcher` | 补环境 | 执行中涉及环境模拟 |
| `ast-deobfuscation` | JS 反混淆 | 执行中涉及混淆代码 |
