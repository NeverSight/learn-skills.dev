---
name: ast-deobfuscation
description: |
  使用 Babel AST 对 JavaScript 做分层、可回退的定向反混淆。适用于 `_0x` 标识符、字符串表、自执行解码包装、dispatcher 对象、虚假常量分支、`while/for + switch` 控制流平坦化、`if (literal === opcode)` 分发链，以及需要按站点或混淆家族命中特征切换专用脚本的场景。
  用户明确提到 reese84、顶象、极验4、同花顺、网易易盾、小红书、OB 变种或类似站点适配时也使用本 skill。
  触发词：「反混淆」「deobfuscation」「_0x」「解混淆」「字符串表」「控制流平坦化」「OB」。
  边界：本 Skill 只负责 JS 代码的结构性还原，不负责加密算法分析（param-encryptor）、环境模拟（env-patcher）或验证码求解（captcha-solver）。
  反混淆是定位加密逻辑的前置步骤，还原后应将结果转交给对应专业 Skill。
---

# AST 反混淆

优先使用分层入口，而不是继续把站点特有逻辑堆进通用脚本。

## 角色规则

**此 Skill 激活后，以 JS 代码还原专家身份工作。**

- 每一步改写必须可回退（保留原文件 + 中间产物）
- 结构性改写后必须重新 parse 验证语法正确性
- 禁止一次性执行所有变换层，必须逐层验证
- 反混淆的最终目标是让加密函数可读、可定位，不是追求 100% 还原

## 工作流

> 以下脚本引用依赖项目内存在 `scripts/` 目录。如项目中不存在，核心工作流仍可按方法论手动执行。

### Step 1: 模式检测

```bash
node scripts/detect-patterns.js <input.js> [hint]
```

输出：命中的混淆家族 + 检测到的症状列表。

### Step 2: 选择流水线

只读取命中的站点或混淆家族规则文档，不要一次加载所有。

### Step 3: 执行流水线

```bash
node scripts/run-pipeline.js <input.js> <output-dir> [hint]
```

执行选中的变换步骤，记录每步耗时。

### Step 4: 验证产出

- `node --check <output.js>` 语法检查
- 对照参考产物或原始混淆症状，判断是否还需要新增专用适配脚本
- 使用 `scripts/collect-residue-metrics.js` 统计剩余混淆特征

🔴 **CHECKPOINT**：每层变换后都必须通过语法检查 + 人工审查关键函数可读性。

## 支持的混淆类型

| 混淆类型 | 症状 | 处理方式 |
|---------|------|---------|
| `_0x` 标识符 | 变量名全是 `_0x1a2b3c` | 标识符重命名（基于引用分析） |
| 字符串表 | 大型数组 + 解码函数 + 自执行包装 | 字符串数组内联 + 解码函数求值 |
| dispatcher | 对象方法分发 `_0xabc['call'](...)` | dispatcher 内联 |
| 虚假分支 | `if (constant === value)` 永真/永假 | 常量折叠 + 死代码消除 |
| 控制流平坦化 | `while/for + switch` 状态机 | 控制流拍平还原 |
| opcode 分发 | `if (literal === opcode)` 链 | 分发链还原 |
| 逗号表达式 | `(a=1, b=2, c=3)` | 序列化拆分 |
| IIFE 包装 | 自执行函数包裹 | IIFE 内联 |
| 语句提升 | 变量/函数声明提前 | 语句顺序还原 |

## 支持的混淆家族

| 家族 | 站点 | 规则文档 |
|------|------|---------|
| reese84 | — | `references/patterns/reese84.md` |
| 顶象 Verify5 | dingxiang | `references/patterns/dingxiang.md` |
| 极验4 | geetest | `references/patterns/geetest4.md` |
| 同花顺 | tonghuashun | `references/patterns/tonghuashun.md` |
| 网易易盾 | yidun | `references/patterns/yidun.md` |
| 小红书 | xiaohongshu | `references/patterns/xiaohongshu.md` |
| OB 变种 (cn-bidding) | — | `references/patterns/cn-bidding-ob.md` |
| OB 变种 (mps) | — | `references/patterns/mps-ob.md` |

## 设计规则

- 通用脚本只保留低风险、可复用的改写，例如结构标准化、虚假分支清理、dispatcher 内联、控制流拍平和 `if -> switch`。
- 一旦某个模式明显是站点特有的，就同时补齐四部分：规则文档、检测器命中项、专用适配脚本、流水线配置项。
- 对于高开销步骤，优先按家族跳过或重排，不要强行要求所有样本走同一套顺序。像 `reese84` 这种大样本，如果太晚执行 `inline-literals`，很容易卡住。
- 专用适配脚本应当保持窄而准。如果某条规则没有在多个无关样本中复用，不要急着回灌到通用脚本。
- 结构性改写后要重新 parse，并保证每一阶段都可以独立运行和排查。

## 反混淆后的下游路由

反混淆完成后，代码中的加密函数已可读。根据目标转交对应专业 Skill：

| 反混淆后发现 | 转交 Skill | 示例 |
|-------------|-----------|------|
| 加密/签名函数（MD5/AES/RSA/自定义） | `param-encryptor` | `CryptoJS.AES.encrypt(data, key)` |
| 验证码计算逻辑 | `captcha-solver` | 滑块距离计算 + 轨迹生成 |
| 浏览器环境检测代码 | `env-patcher` | `navigator.webdriver` 检测 |
| VM 字节码（非 AST 可处理） | `web-reverse-master` | JSVMP / 字节码解释器 |

## 入口脚本

> 以下脚本为本 Skill 的配套工具，非必需。首次使用时需创建。如项目中不存在，核心工作流仍可按方法论手动执行。

- `scripts/detect-patterns.js`
  根据文件路径、可选 hint 和源码症状判断最可能命中的站点或混淆家族。
- `scripts/run-pipeline.js`
  把样本复制到测试目录，执行选中的步骤，记录耗时并输出流水线报告。
- `scripts/collect-residue-metrics.js`
  统计仍未解开的症状，例如 `split('|')`、直接 `loop/switch` 平坦化、opcode `if` 链、dispatcher wrapper 和 `_0x` 标识符。
- `scripts/compare-with-reference.js`
  将最新流水线输出与 `decode.js` 对比，汇总剩余差距。

## 参考文档

> 以下参考文档位于本 Skill 的 `references/` 子目录中。如不存在，核心工作流仍可执行，但缺少特定混淆家族的适配细节。

- 新增或调整适配器时，先读 `references/pattern-layering.md`。
- 任何逻辑想放进通用脚本前，先读 `references/safe-rewrite-rules.md`。
- 处理字符串表、解码 stub、最小运行时求值时，读 `references/string-array-and-minimal-eval.md`。
- 处理控制流平坦化、opcode 分发器和 VM 类 handler 时，读 `references/control-flow-and-opcode-patterns.md`。
- 处理逗号表达式、IIFE、语句提升时，读 `references/sequence-normalization.md`。
- 检测器命中后，只读取对应的一份站点规则文档：
  - `references/patterns/reese84.md`
  - `references/patterns/dingxiang.md`
  - `references/patterns/geetest4.md`
  - `references/patterns/tonghuashun.md`
  - `references/patterns/yidun.md`
  - `references/patterns/xiaohongshu.md`
  - `references/patterns/cn-bidding-ob.md`
  - `references/patterns/mps-ob.md`

## 校验

- 每个新增或改过的 JavaScript 辅助脚本，在接入流水线前都要至少过一次 `node --check` 或等价的加载校验。
- 测试案例时，把中间产物、检测结果、对比结果和流水线耗时都保留在案例目录里，方便定位慢步骤和失败步骤。

## Phase Mapping

本 Skill 主要在 CLAUDE.md Phase 2（定位加密）作为前置步骤：

| Phase | 本 Skill 的角色 | 与专业 Skill 的协作 |
|-------|----------------|-------------------|
| Phase 2 定位加密 | ✅ 前置步骤：混淆代码必须先还原才能 Hook/搜索 | 还原后转交 `param-encryptor` 分析加密函数 |
| Phase 3 方案制定 | 🟡 按需：Plan 中如涉及混淆处理方案 | — |
| Phase 4 代码还原 | 🟡 按需：最终 signer.js 可能需要局部反混淆 | — |

**典型调用链：**
```
web-reverse-master Phase 2 发现目标 JS 被混淆
  → ast-deobfuscation Step 1-4 还原代码
  → 还原后发现 CryptoJS.MD5 调用
  → param-encryptor 配方1 匹配 + 本地对照
  → Phase 4 代码还原
```

## Related Skills

| Skill | 职责 | 何时调用 |
|-------|------|---------|
| `web-reverse-master` | 全流程编排 | 需要完整逆向分析流程 |
| `web-reverse-workflow` | 工作流入口 | 需要判断当前阶段 |
| `captcha-solver` | 验证码求解 | 反混淆后发现验证码计算逻辑 |
| `param-encryptor` | 加密参数生成 | 反混淆后发现加密/签名函数 |
| `env-patcher` | 补环境 | 反混淆后发现环境检测代码 |
