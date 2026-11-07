---
name: codeguard-detect
license: Apache-2.0
description: 使用 Codeguard 通过扩展名、文件名和项目标记识别仓库语言构成；当用户询问这是什么语言项目、需要为 lint 选路、调整 codeguard.json 映射/排除，或初始化治理时使用。
compatibility: 仅需 Python 标准库和可读的本地目录；默认不上传文件、不跟随生成或 vendor 目录。
---

# codeguard detect

## Capability Boundaries

### ✅ Strengths
1. 55 种语言/文件类型识别（扩展名 + 文件名 + 项目标记文件三重）
2. 项目根 `codeguard.json` 自定义扩展映射（借鉴 codegraph 的零配置 + 可覆盖设计）
3. 输出 JSON，供其他工具/技能消费

### ⚠️ Prerequisites
1. 无（纯 Python 标准库）

### ❌ Out of Scope
1. 框架级识别（Spring/React 等框架探测在路线图）
2. 语言版本检测（.nvmrc / pom java.version 解析）

## 命令

```bash
bin/codeguard detect              # 当前目录
bin/codeguard detect path/to/pkg  # 指定目录
# 等价：python3 scripts/detect_lang.py path/
```

## 输出示例

```text
["java"]
["typescript", "vue"]
["go", "markdown"]
```

## 自定义扩展映射

项目根 `codeguard.json`：

```json
{
  "extensions": {
    ".dota_lua": "lua",
    ".tpl": "php"
  },
  "exclude": ["vendor/**", "generated/**"]
}
```

- `extensions`：合并/覆盖内置默认映射
- `exclude`：扫描时排除的文件模式（glob/正则字符串）

## 不适用范围（什么时候不该用）

- 要求精确判定语言或框架版本：检测器只识别类型，不解析完整依赖图。
- 要求执行 lint 或修复：转交 **`codeguard-check`** 或 **`codeguard-fix`**。
- 希望仅凭扩展名证明仓库可构建：检测结果不是构建证据。

## 数据与安全

检测应在本地完成，不收集、上传或存储源码和凭据。只读取相对路径、文件名和必要的标记文件；报告中对用户目录和内部模块名做必要脱敏。

## 标准 Workflow

### Step 1：确定根目录

先找 Git 根或用户指定的 monorepo 模块，不在上级工作区全盘扫描。

### Step 2：读取排除规则

合并仓库既有 ignore 策略与 `codeguard.json` 的 `exclude`，明确生成代码、vendor、缓存和子仓库的边界。

### Step 3：执行检测

运行 `bin/codeguard detect <path>`，保存实际命令、范围、退出码与结构化输出。

### Step 4：交叉验证

用标记文件和主要源文件复核结果。扩展名冲突时报告歧义，不静默猜测。

### Step 5：路由门禁

对 `stable` 语言进入对应检查技能；对 `planned` 语言明确说明仅可识别、尚不能执行门禁。

## Rules

1. 语言“被识别”不等于“linter 已接入”。
2. 自定义映射必须有仓库事实或用户确认，不得为过门禁伪造类型。
3. 不跟随超出仓库根的符号链接。
4. 大仓库优先指定模块范围，不用无限制全盘扫描。

## 输出模板

```text
Codeguard detect 结果
- 根目录：<path>
- 排除：<patterns>
- 识别：<language -> evidence>
- 状态：<stable/planned>
- 歧义：<conflicting extensions or markers>
- 下一步：<matching check skill or missing gate>
```

## Gotchas

1. **`.h` 等扩展名有歧义**：需结合构建文件判断 C/C++/Objective-C。
2. **模板文件可能混合语言**：`.vue`、`.astro` 等不能靠内嵌片段数量猜测主语言。
3. **vendor 会污染结果**：未排除第三方代码时，识别到的语言不一定由项目维护。
4. **标记文件可以是残留物**：需与真实源文件和 CI 交叉验证。
5. **子仓库与 worktree**：不要把外层工作区的配置错用到内层仓库。
6. **planned 能力**：仅能路由到说明，不得输出 PASS。

## 按需加载资源

- 需要解释识别优先级时读取 `references/rules/detection-precedence.md`。
- 需要配置 `codeguard.json` 时读取 `references/operations/configuration-guide.md`。
- 只打开 `examples/` 中与当前场景匹配的示例。
