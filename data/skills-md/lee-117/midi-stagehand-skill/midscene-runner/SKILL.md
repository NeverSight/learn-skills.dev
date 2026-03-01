---
name: midscene-runner
version: 2.0.0
description: >
  Execute, validate, and debug Midscene YAML automation files.
  Handles dry-run, execution, report analysis, and iterative debugging.
argument-hint: <yaml-file-path>
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Midscene Runner

## 触发条件

当用户需要执行、调试或验证 Midscene YAML 文件时使用。

常见触发短语：
- "运行这个 YAML"
- "执行 XXX.yaml"
- "测试这个自动化脚本"
- "跑一下这个用例"
- "验证这个 YAML 是否正确"
- "调试这个自动化流程"
- "批量执行这些测试"

English trigger phrases:
- "Run this YAML"
- "Execute XXX.yaml"
- "Test this automation script"
- "Validate this YAML file"
- "Debug this automation flow"
- "Run the test cases"

## 工作流程

### 第 0 步：环境检查

首次执行前，使用一键健康检查确认运行环境就绪：

```bash
node scripts/health-check.js
```

该脚本会检查：Node.js 版本、依赖安装、CLI 脚本、`@midscene/web`、`tsx` 运行时、AI 模型配置、Chrome 浏览器。

**模型未配置？** Midscene 执行 AI 操作需要视觉语言模型。在项目根目录创建 `.env` 文件：

```env
MIDSCENE_MODEL_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MIDSCENE_MODEL_API_KEY=sk-your-key
MIDSCENE_MODEL_NAME=qwen-vl-max-latest
```

详细配置说明见 [Midscene 模型配置文档](https://midscenejs.com/zh/model-common-config.html)。

**首次使用？运行一键环境初始化**：

```bash
npm run setup
```

`setup` 会自动完成以下工作：
- 智能检测网络环境，自动选择最快的 npm 镜像（国内自动使用淘宝源加速）
- 安装所有项目依赖
- 预热 `@midscene/web` 和 `tsx` 到 npx 缓存（避免首次执行时等待下载）
- 检测系统 Chrome，若无则自动下载 Chromium
- 输出环境就绪报告

**Chrome 浏览器检测**（Web 平台）：

框架会自动按以下顺序查找系统 Chrome/Chromium/Edge：
- Windows: `Program Files\Google\Chrome`、`Chromium`、`Microsoft\Edge` (LOCALAPPDATA/PROGRAMFILES)
- macOS: `/Applications/Google Chrome.app`、`/Applications/Chromium.app`
- Linux: `/usr/bin/google-chrome`、`/usr/bin/chromium`、`/snap/bin/chromium`、`which google-chrome`

如果未找到系统 Chrome，有两种解决方案：
1. 安装 Chrome 浏览器（推荐）
2. 运行 `npx puppeteer browsers install chrome` 安装 Chromium

如果 Chrome 在非标准路径，设置环境变量：
```bash
# Linux/macOS
export PUPPETEER_EXECUTABLE_PATH="/path/to/chrome"
# Windows PowerShell
$env:PUPPETEER_EXECUTABLE_PATH="C:\path\to\chrome.exe"
```

**平台特定前提条件**：

| 平台 | 依赖 |
|------|------|
| Web | Chrome/Chromium 浏览器（自动检测，见上方说明） |
| Android | ADB 已连接设备（`adb devices` 验证） |
| iOS | WebDriverAgent 已配置 |
| Extended 模式 | `tsx` 运行时（`npx tsx --version`） |

如果缺少依赖，提示用户安装：
```bash
npm install && npm run setup
```

### 第 1 步：定位 YAML 文件

确定要执行的 YAML 文件路径。如果用户没有指定完整路径：
- 检查 `./midscene-output/` 目录下最近生成的文件
- 检查 `./templates/` 目录下的模板文件
- 检查当前目录下的 `.yaml` / `.yml` 文件
- 提示用户提供文件路径

多文件场景：如果用户要求执行多个文件，可逐个执行并汇总结果。

### 第 2 步：预验证

在执行前，调用验证器检查 YAML 文件：

```bash
node scripts/midscene-run.js <yaml-file> --dry-run
```

如果验证失败，分析错误原因并向用户建议修复方案：

| 常见错误 | 原因 | 修复建议 |
|---------|------|---------|
| YAML 语法错误 | 缩进不正确或格式问题 | 检查缩进，统一使用 2 空格 |
| 缺少平台配置 | 没有 web/android/ios/computer | 添加 `web: { url: "..." }` |
| 缺少 tasks | 没有定义任务 | 添加 tasks 数组和 flow |
| 未声明 engine | 使用超集关键字但未标记 | 添加 `engine: extended` |
| 变量未定义 | 引用了未声明的 `${var}` | 在 variables 中声明变量 |
| 未声明 features | Extended 模式未列出使用的特性 | 添加 `features: [...]` |
| 循环缺少必要字段 | repeat 缺 count、while 缺 condition | 补充对应必要字段 |
| 导入文件不存在 | import 引用的路径不正确 | 检查文件路径是否正确 |

**自动修复流程**：如果错误可以自动修复（如缺少 engine 声明），直接修复后重新验证，避免往返确认。

### 第 3 步：执行

根据项目环境选择执行方式：

**方式 1（推荐）: 使用项目 CLI**

如果项目中有 `scripts/midscene-run.js`（midi-stagehand-skill 完整项目）：
```bash
# 单文件执行
node scripts/midscene-run.js <yaml-file> [options]

# 批量执行（glob 模式）
node scripts/midscene-run.js "tests/**/*.yaml"
```

**方式 2: 直接使用 Midscene CLI**

如果在外部项目中（没有 `scripts/midscene-run.js`），直接使用 `@midscene/web`：
```bash
# 安装（仅首次）
npm install @midscene/web dotenv

# 执行（--headed 表示有界面）
npx @midscene/web <yaml-file> --headed

# 批量执行（官方 CLI 选项）
npx @midscene/web "tests/**/*.yaml" --concurrent --continue-on-error
```

> **注意**: 包名是 `@midscene/web`（不是 `@midscene/cli`）。官方 CLI 语法是 `npx @midscene/web <yaml-file>`，支持 `run` 子命令（`npx @midscene/web run <yaml-file>`），两种形式均可。

**可用选项**（方式 1）：
- `--dry-run` — 仅验证和转换，不实际执行（注意：不检测模型配置，AI 操作需配置 `MIDSCENE_MODEL_API_KEY`）
- `--timeout <ms>` — 执行超时（默认 300000 = 5 分钟）。**注意**：timeout 包含浏览器启动时间，建议最低设置 60000ms
- `--retry <count>` — 失败后自动重试次数（默认 0，即不重试）。适合 flaky 场景
- `--output-ts <path>` — 保存转换后的 TypeScript 文件（仅 Extended 模式）。排查转译错误时，建议配合 `--dry-run` 一起使用
- `--report-dir <path>` — 报告输出目录（默认 `./midscene-report`）
- `--template puppeteer|playwright` — 选择 TS 模板（默认 puppeteer；playwright 适合需要多浏览器兼容的场景）
- `--clean` — 清理 `.midscene-tmp/` 中超过 24 小时的过期临时文件
- `--verbose` / `-v` — 显示详细输出（验证详情、检测信息、环境信息、错误分类）
- `--help` / `-h` — 显示帮助信息

**Extended 模式的执行流程**：
1. YAML → Transpiler → TypeScript
2. TypeScript → tsx 运行时 → Playwright + Midscene SDK
3. 生成执行报告

可以使用 `--output-ts` 保存中间 TypeScript 文件以便调试：
```bash
node scripts/midscene-run.js test.yaml --output-ts ./debug-output.ts
```

### 第 4 步：分析结果

执行完成后：

#### 成功
- 汇报执行摘要（通过/失败的任务数）
- 告知报告文件位置
- 如果有 `aiQuery` 结果，展示提取的数据
- 如果有 `output` 导出，确认文件生成位置

#### 失败
按以下决策树分析错误并修复：

```
错误消息包含什么？
├─ "API key" / "401" / "Unauthorized"
│   → 模型未配置。设置 MIDSCENE_MODEL_API_KEY 环境变量或 .env 文件
│
├─ "Timeout" / "exceeded"
│   ├─ 页面能在浏览器中正常打开？
│   │   ├─ 是 → 页面加载慢，增加 timeout 值（如 timeout: 30000）
│   │   └─ 否 → 检查 URL 是否正确、网络是否可达
│   └─ 出现在 aiWaitFor？→ 条件描述可能不准确，检查 assertion 文本
│
├─ "Element not found" / "not found"
│   ├─ 第一次就失败？→ AI 描述不够精确，改用更具体的文字描述
│   ├─ 之前能成功？→ 页面结构可能变了，查看报告截图对比
│   └─ 仍然失败？→ 尝试 deepThink: true 或改用 xpath 定位
│
├─ "Assertion failed"
│   → 查看报告截图，对比实际页面状态 vs 预期描述，调整 aiAssert 文本
│
├─ "Navigation failed" / "net::ERR_"
│   → 检查 URL 协议（https://）和可访问性
│
├─ "Transpiler error"
│   → 使用 --dry-run --output-ts ./debug.ts 查看生成的代码排查语法问题
│
├─ "Permission denied"
│   → 页面需要登录或特殊权限，添加登录步骤或 cookie 配置
│
└─ "javascript" 步骤报错
    → 检查 JS 代码语法，注意浏览器环境 vs Node 环境的 API 差异
```

**迭代修复流程**：
1. 分析错误原因
2. 修改 YAML 文件
3. 重新执行 `--dry-run` 验证
4. 验证通过后重新执行

### 第 5 步：报告解读

解读 Midscene 生成的报告：

- 报告默认在 `./midscene-report/` 目录
- **HTML 报告**：在浏览器中打开，每个步骤展示执行状态和截图（绿色 ✓ = 通过，红色 ✗ = 失败），点击可展开详情
- **JSON 报告**：结构化数据，包含每步的状态、耗时、截图路径，适合 CI/CD 自动解析
- 截图路径为相对于报告目录的路径
- `recordToReport` 步骤产生的自定义截图也包含在报告中

报告摘要格式：
```
Total : N
Passed: N
Failed: N
Status: passed|failed
```

## 快速执行命令参考

### 使用项目 CLI（完整项目）

```bash
# 基本执行
node scripts/midscene-run.js test.yaml

# 仅验证，不执行
node scripts/midscene-run.js test.yaml --dry-run

# 保存生成的 TS（仅 extended 模式）
node scripts/midscene-run.js test.yaml --output-ts ./output.ts

# 使用 Playwright 模板
node scripts/midscene-run.js test.yaml --template playwright

# 指定报告目录
node scripts/midscene-run.js test.yaml --report-dir ./reports

# 设置超时为 10 分钟
node scripts/midscene-run.js test.yaml --timeout 600000

# 验证 + 保存 TS（排查转译问题）
node scripts/midscene-run.js test.yaml --dry-run --output-ts ./debug.ts

# 查看帮助
node scripts/midscene-run.js --help
```

### 直接使用 Midscene CLI（外部项目）

```bash
# 有界面执行（调试推荐）
npx @midscene/web test.yaml --headed

# 无头模式执行（CI/CD 推荐）
npx @midscene/web test.yaml
```

## YAML 配置速查

### agent 配置（可选）

```yaml
agent:
  testId: "test-001"
  groupName: "回归测试"
  groupDescription: "每日回归测试套件"
  cache: true                        # 或对象格式: { strategy: "read-write", id: "cache-key" }
  generateReport: true
  autoPrintReportMsg: true
  reportFileName: "custom-report"
  replanningCycleLimit: 20           # 默认 20, UI-TARS 模型设 40
  aiActContext: "这是一个中文电商网站"  # AI 背景知识
  screenshotShrinkFactor: 0.5        # 截图缩放（节省 token）
  waitAfterAction: 500               # 每次操作后等待 ms（默认 300）
```

### continueOnError（可选）

当一个任务失败后继续执行后续任务：

```yaml
tasks:
  - name: 任务 A
    continueOnError: true
    flow: [...]
  - name: 任务 B（即使 A 失败也会执行）
    flow: [...]
```

### 平台配置选项

```yaml
# Web 平台完整配置
web:
  url: "https://example.com"
  headless: false       # true = 无头模式（适合 CI/CD）; false = 有界面（适合调试）
  viewportWidth: 1920   # 默认 1280；移动端模拟可用 375
  viewportHeight: 1080  # 默认 720；移动端模拟可用 667
  userAgent: "Custom User Agent"
  waitForNetworkIdle:
    timeout: 2000
    continueOnNetworkIdleError: true

# Android 平台（需先 adb devices 确认设备已连接）
android:
  deviceId: "emulator-5554"   # adb devices 输出中的设备 ID
# 在 flow 中使用 launch: "com.example.app" 启动应用

# iOS 平台（需先配置 WebDriverAgent）
ios:
  wdaPort: 8100              # WebDriverAgent 端口
  wdaHost: "localhost"       # WebDriverAgent 主机
# 在 flow 中使用 launch: "com.example.app" 启动应用
```

## 调试技巧

1. **查看报告截图**: 执行后查看 HTML 报告，每一步都有截图
2. **分段执行**: 先只写前几步验证通过，再逐步添加
3. **增加等待**: 在关键步骤后添加 `aiWaitFor` 确保页面就绪
4. **插入断言**: 在中间步骤插入 `aiAssert` 验证当前状态
5. **查看 TS 代码**: Extended 模式使用 `--output-ts` 查看生成的代码排查问题
6. **使用 deepThink**: 元素定位不准时开启 `deepThink: true`
7. **降级到 xpath**: 自然语言无法定位时使用 `xpath` 精确选择
8. **使用 javascript**: 通过 `javascript` 步骤直接执行 JS 代码调试页面状态
9. **使用 recordToReport**: 在关键节点插入 `recordToReport` 截图记录

## 注意事项

- 执行 Web 平台测试需要安装 Chrome/Chromium 浏览器
- 首次运行可能需要安装依赖：`npm install`
- Android 测试需要 ADB 连接设备，iOS 测试需要 WebDriverAgent
- Extended 模式的 YAML 会先转换为 TypeScript 再执行，需要 tsx 运行时
- 报告中的截图路径为相对路径，在报告目录内查找
- 如果需要生成新的 YAML 文件，可以使用 **Midscene YAML Generator** skill
- 环境变量通过系统环境或 `.env` 文件传入，在 YAML 中用 `${ENV:NAME}` 或 `${ENV.NAME}` 引用（两种语法等价）
- `parallel` 分支在独立浏览器上下文中运行，执行期间互不影响；各分支的 `aiQuery` 结果在全部完成后可合并访问（通过 `merge_results: true`）
- `--dry-run` 仅检查 YAML 语法和结构，不检测模型配置和网络可达性
- 如果 `npx skills check` 检测不到已有更新，可能是 lock 文件格式过旧（v1），需要重新安装以升级为 v3 格式：`npx skills add https://github.com/lee-117/midi-stagehand-skill -a claude-code`

## 协作协议

与 Generator Skill 配合时：

1. **优先检查** `./midscene-output/` 目录中最近生成的文件
2. **执行失败时**，提供结构化错误信息：
   - 错误类型、错误位置（步骤/行号）、建议修复
3. 如果错误可通过修改 YAML 修复，直接修改并重新执行（无需回调 Generator）
