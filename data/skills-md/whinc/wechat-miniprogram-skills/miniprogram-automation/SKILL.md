---
name: miniprogram-automation
description: Use when working with WeChat mini-program automation (小程序自动化、自动化测试、E2E) via miniprogram-automator, especially for standalone Node scripts or Jest tests involving DevTools launch/connect, page navigation, waitFor, custom-component selectors, wx method mocking, console or exception listeners, screenshots, regression checks, or troubleshooting launch failures, connection timeouts, and element-not-found issues.
---

# 微信小程序自动化

## 概述

使用 `miniprogram-automator` 驱动微信开发者工具，完成页面跳转、元素查询、交互、Mock、运行时监听、截图和回归验证。

这个 skill 默认偏向**实战参考型**输出：
- 优先给出**可直接运行的独立 Node.js 脚本模板**
- 用户明确要求接入测试框架时，再输出 Jest 版
- 先确认方案和前置条件，再落地到脚本文件

## 默认输出结构

被触发时，优先按这个结构回答：

1. **先说明你准备怎么做**：会生成哪类脚本、依赖哪些输入
2. **列出前置检查项**：项目目录、CLI 路径、安全设置、页面路径、选择器
3. **给完整脚本**：优先独立脚本，必要时补 Jest 版
4. **给运行命令**：安装依赖、执行命令、可选参数
5. **给验证点和注意事项**：等待策略、Mock 恢复、关闭连接、截图限制

如果用户已经给全了路径、页面、选择器和目标行为，就不要反复盘问，直接产出脚本。

## Step 1：先收集关键输入

如果用户没提供完整信息，先补齐这些字段：

### 1.1 可被开发者工具打开的项目目录
`automator.launch({ projectPath })` 里的 `projectPath` 应该是**开发者工具实际打开的目录**。

不要机械地把它理解成“源码仓库根目录”：
- 原生小程序：通常是包含 `project.config.json` / `app.json` 的目录
- Taro / uni-app / 自定义构建链：通常是开发者工具真正打开的**编译产物目录**，例如 `dist/`、`build/`、`miniprogram/`

拿不准时，先问用户：
- “你平时在微信开发者工具里打开的是源码根目录，还是编译后的 dist/build 目录？”

### 1.2 微信开发者工具 CLI 路径
常见默认路径：
- macOS：`/Applications/wechatwebdevtools.app/Contents/MacOS/cli`
- Windows：`C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat`

如果开发者工具安装在标准位置，`cliPath` 可以省略，SDK 会按默认路径自动查找。

如果用户环境不标准，先让用户确认实际路径。

### 1.3 miniprogram-automator 版本
**必须使用 `0.12.0` 及以上版本**，否则会触发 CLI 命令格式兼容问题。

旧版（`0.5.x` 等）使用已废弃的 `cli --auto <path>` 语法，当前微信开发者工具（3.x）已不支持，表现为：
```
[error] { code: 31, message: "Error: Missing param 'project / appid'" }
```

升级方法：
```bash
npm install miniprogram-automator@latest --save-dev
```

新版（`0.12.x`）使用正确的 `cli auto --project <path> --auto-port <port>` 语法。

### 1.4 安全设置
使用 `automator.launch()` 前，必须提醒用户检查：
- 微信开发者工具 → 设置 → 安全设置 → 开启 **服务端口**

没有这一步，脚本常见表现是：
- launch 失败
- 连接超时
- CLI 可执行但 WebSocket 建不起来

### 1.5 目标页面和断言目标
至少确认：
- 页面路径，如 `/pages/home/index`
- 是否要 `reLaunch` / `navigateTo` / `switchTab`
- 要验证什么：文本、类名、数据、截图、日志、异常、Mock 请求结果
- 关键选择器是否稳定

### 1.6 输出形态
默认先给**独立脚本**。只有在这些场景下优先 Jest：
- 用户明确提到 Jest / 单测 / 回归套件 / CI
- 任务需要 `beforeAll/afterAll`、多 case 组织、批量断言

## Step 2：选择正确的工作流

### 2.1 `launch` 还是 `connect`

三种工作流，按场景选择：

| 场景 | 推荐方式 |
|---|---|
| 全自动：脚本自己启动开发者工具 | `automator.launch()` |
| 开发者工具已开着，直接连 | CLI v2 + `automator.connect()` |
| 开发者工具已开着且自动化端口已就绪 | 直接 `automator.connect()` |

---

**方式一：`automator.launch()`（全自动启动）**

SDK 内部调用 CLI 启动开发者工具，无需手动操作。两个硬性前提：
1. **开发者工具必须完全退出（Cmd+Q）**，否则报 `Failed to launch wechat web devTools`——launch 不能与已运行实例共存。
2. **首次运行弹出「信任项目」确认框**，需用户手动点击，因此 `timeout` 建议 `120000`（2 分钟）。

```js
miniProgram = await automator.launch({
  cliPath: CLI_PATH,
  projectPath: PROJECT_PATH,
  timeout: 120000,
})
```

---

**方式二：CLI v2 + `automator.connect()`（开发者工具已在运行）**

当开发者工具已打开项目（不想关掉重开），用 CLI v2 命令开启自动化 WebSocket 端口，再用 `connect()` 连入。

> `automator.launch()` 内部其实仍在使用旧版 CLI 格式（`cli --auto <path>`），在某些新版开发者工具上可能失败。如果遇到 `launch()` 报错，改用这个方式通常更稳。

```js
const { spawnSync } = require('node:child_process')

const CLI_PATH = process.env.WECHAT_DEVTOOLS_CLI ||
  '/Applications/wechatwebdevtools.app/Contents/MacOS/cli'
const PROJECT_PATH = process.env.MINIPROGRAM_PROJECT_PATH || '/path/to/project'
const AUTO_PORT = Number(process.env.WECHAT_AUTO_PORT || 9420)

// Step 1：用 CLI v2 开启自动化 ws 端口
// 若开发者工具 HTTP 服务端口不是默认值，需通过 --port 传入
function enableAutomation(httpPort) {
  const args = ['auto', '--project', PROJECT_PATH, '--auto-port', String(AUTO_PORT)]
  if (httpPort) args.push('--port', String(httpPort))
  const result = spawnSync(CLI_PATH, args, { encoding: 'utf8', timeout: 20000 })
  return { success: result.status === 0, output: (result.stdout || '') + (result.stderr || '') }
}

const { success, output } = enableAutomation()
if (!success) throw new Error(`CLI auto 命令失败:\n${output}`)

// Step 2：connect 到自动化 ws 端点
const miniProgram = await automator.connect({
  wsEndpoint: `ws://127.0.0.1:${AUTO_PORT}`,
})
```

**端口冲突问题**：如果开发者工具 HTTP 服务端口不是默认值（例如因为多实例），CLI v2 命令加 `--port` 时会冲突报错。探测实际端口的方法：先用一个占位端口调用一次 CLI，从输出里解析实际端口。完整示例见模板 E。

---

**方式三：直接 `automator.connect()`（端口已就绪）**

开发者工具已手动开启自动化端口（工具菜单或之前已调用 CLI v2），直接连：

```js
const miniProgram = await automator.connect({
  wsEndpoint: 'ws://localhost:9420',
})
```

注意：`connect()` 拿到的 `miniProgram` 的 `close()` 只断开 WebSocket 连接，不会关闭开发者工具。

### 2.2 独立脚本还是 Jest
| 场景 | 建议 |
|---|---|
| 临时验证、单页面调试、做脚本工具 | 独立 Node.js 脚本 |
| 回归测试、多个 case、团队协作、CI | Jest |

### 2.3 等待策略怎么选
优先级如下：
1. `await page.waitFor('稳定选择器')`
2. `await page.waitFor(async () => 条件成立)`
3. `await page.waitFor(数字毫秒)` 作为兜底

不要一上来就全靠固定 `sleep(2000)`。固定等待只能兜底，不能当主同步手段。

## Step 3：核心规则

### 3.1 页面等待优先用 `waitFor`
`page.waitFor()` 支持三种形式：

```js
await page.waitFor('.page-title')
await page.waitFor(async () => (await page.$$('.loaded-item')).length > 0)
await page.waitFor(500)
```

推荐写法：先用选择器或真正的条件断言等待，再补一个很短的兜底等待。不要写永远返回 `true` 的条件函数。

### 3.2 页面级选择器不能穿透自定义组件
这是最容易答错的地方。

**错误思路：**
```js
const input = await page.$('form-panel input')
```

**正确思路：**
```js
const panel = await page.$('form-panel')
const input = await panel.$('input')
```

原因：`page.$` / `page.$$` 的查询作用域是**页面根节点**，无法直接选取自定义组件内部的元素；即使用 `form-panel input` 这种后代选择器也不行。要选组件内部元素，先拿到组件宿主元素，再用 `element.$` / `element.$$` 在组件作用域内继续查。

### 3.3 读输入值时，优先 `value()` 或 `property('value')`
如果目标是原生 `input` / `textarea`：

```js
const value = await input.value()
// 或
const value2 = await input.property('value')
```

如果目标是**自定义组件实例**，再考虑：

```js
const data = await panel.data()
```

不要把“读原生输入框值”和“读组件内部 data”混为一谈。`data()` 更适合组件实例，不是通用的输入框读取方法。

### 3.4 Mock 微信 API 时优先官方 `mockWxMethod`
如果任务是 mock `wx.request`、`wx.getLocation` 等，优先用：

```js
await miniProgram.mockWxMethod('request', (options = {}) => {
  const res = {
    data: { code: 0, list: [{ id: 1, title: 'Mock Item A' }] },
    statusCode: 200,
    header: { 'content-type': 'application/json' },
    cookies: [],
    errMsg: 'request:ok',
  }

  Promise.resolve().then(() => {
    if (typeof options.success === 'function') options.success(res)
    if (typeof options.complete === 'function') options.complete(res)
  })

  return {
    abort() {},
    onHeadersReceived() {},
    offHeadersReceived() {},
    onChunkReceived() {},
    offChunkReceived() {},
  }
})
```

结束时恢复：

```js
await miniProgram.restoreWxMethod('request')
```

补充说明：
- `mockWxMethod` 也支持直接传固定结果对象；简单场景不必总写函数
- 如果传入函数，函数体会被序列化执行，不要依赖闭包引用外部变量
- 如果需要调用原始 wx 方法，可在函数内部使用 `this.origin`

只有当用户明确需要做更深层运行时注入，或者 `mockWxMethod` 无法覆盖目标场景时，再考虑 `evaluate()`。

### 3.5 截图使用 `miniProgram.screenshot()`，且仅限开发者工具模拟器
```js
await miniProgram.screenshot({ path: '/abs/path/to/file.png' })
```

补充说明：
- 传 `{ path }` 时会把截图保存到文件
- 不传参数时会返回图片数据的 base64 编码，适合做内存中的比对或上传

必须提醒：
- 截图只适用于**开发者工具模拟器**
- 不适用于真机调试画面
- 截图前要确保页面已经稳定渲染

### 3.6 清理动作必须放进 `finally`
无论是独立脚本还是 Jest，都要确保：
- 恢复被 mock 的 wx 方法
- 解绑事件监听（如果用了）
- 关闭小程序实例

```js
try {
  // 执行测试逻辑
} finally {
  await miniProgram.restoreWxMethod('request').catch(() => {})
  await miniProgram.close().catch(() => {})
}
```

## 模板 A：独立脚本通用骨架

当用户说“给我一个脚本”“先别改测试框架”“想快速跑一下”，优先从这个模板起步。

```js
const automator = require('miniprogram-automator')
const path = require('node:path')
const fs = require('node:fs/promises')

const CLI_PATH = process.env.WECHAT_DEVTOOLS_CLI || '/Applications/wechatwebdevtools.app/Contents/MacOS/cli'
const PROJECT_PATH = process.env.MINIPROGRAM_PROJECT_PATH || '/absolute/path/to/devtools-project'
const TARGET_PAGE = '/pages/home/index'  // 必须以 / 开头
const OUTPUT_DIR = path.resolve(process.cwd(), 'outputs')

async function main() {
  let miniProgram
  try {
    await fs.mkdir(OUTPUT_DIR, { recursive: true })

    // 前提：开发者工具已完全退出（Cmd+Q）；首次运行需在界面确认信任项目
    miniProgram = await automator.launch({
      cliPath: CLI_PATH,
      projectPath: PROJECT_PATH,
      timeout: 120000,  // 给首次启动 + 用户确认信任留足时间
    })

    const page = await miniProgram.reLaunch(TARGET_PAGE)

    // 主同步手段优先用稳定选择器，固定等待只做短兜底
    await page.waitFor('.page-title')
    await page.waitFor(100)
    const title = await page.$('.page-title')
    const titleText = await title.text()

    console.log('当前标题：', titleText)

    await miniProgram.screenshot({
      path: path.join(OUTPUT_DIR, 'current-page.png'),
    })

    console.log('截图完成')
  } finally {
    if (miniProgram) {
      await miniProgram.close()
    }
  }
}

main().catch((error) => {
  console.error(error)
  process.exit(1)
})
```

## 模板 B：自定义组件内输入与校验

当用户提到“组件里有 input”“为什么 page.$ 选不到”“要读 value 或 data”，用这个模板。

```js
const automator = require('miniprogram-automator')

async function run() {
  let miniProgram
  try {
    miniProgram = await automator.launch({
      cliPath: process.env.WECHAT_DEVTOOLS_CLI || '/Applications/wechatwebdevtools.app/Contents/MacOS/cli',
      projectPath: process.env.MINIPROGRAM_PROJECT_PATH || '/absolute/path/to/devtools-project',
    })

    const page = await miniProgram.reLaunch('/pages/form/index')
    await page.waitFor(300)

    const panel = await page.$('form-panel')
    if (!panel) throw new Error('未找到 form-panel')

    const input = await panel.$('input')
    if (!input) throw new Error('未找到组件内 input')

    await input.tap()
    await input.input('13800138000')

    await page.waitFor(100)

    const value = await input.value()
    if (value !== '13800138000') {
      throw new Error(`输入框值不符合预期: ${value}`)
    }

    // panel 必须是自定义组件实例；原生组件或普通元素不适合用 data() 读取内部状态
    const panelData = await panel.data().catch(() => null)
    console.log('panel.data() =', panelData)
  } finally {
    if (miniProgram) await miniProgram.close()
  }
}

run().catch((error) => {
  console.error(error)
  process.exit(1)
})
```

回答时要明确解释：
- `page.$` 不能跨组件边界
- 读原生输入值优先 `value()` / `property('value')`
- 读组件内部状态用组件实例的 `data()`

## 模板 C：Mock `wx.request` + 监听 `console/exception`

当用户要做回归脚本、接口伪造、无网验证、异常监控时，优先给这个模板。

先核对目标页面的真实反馈路径：有些页面只会在请求成功后更新 `loading`、打印 `console`、弹出 toast，而不会渲染列表或表格。像官方 demo 的 `packageAPI/pages/network/request/request` 就属于这种页面，因此断言应围绕按钮状态、日志、toast 或页面数据来设计，不要凭空假设页面一定会出现列表渲染。

```js
const automator = require('miniprogram-automator')

async function run() {
  let miniProgram
  const consoleEvents = []
  const exceptionEvents = []

  try {
    miniProgram = await automator.launch({
      cliPath: process.env.WECHAT_DEVTOOLS_CLI || '/Applications/wechatwebdevtools.app/Contents/MacOS/cli',
      projectPath: process.env.MINIPROGRAM_PROJECT_PATH || '/absolute/path/to/devtools-project',
    })

    miniProgram.on('console', (payload) => {
      consoleEvents.push(payload)
    })

    miniProgram.on('exception', (payload) => {
      exceptionEvents.push(payload)
    })

    await miniProgram.mockWxMethod('request', (options = {}) => {
      const res = {
        data: {
          code: 0,
          list: [
            { id: 1, title: 'Mock Item A' },
            { id: 2, title: 'Mock Item B' },
          ],
        },
        statusCode: 200,
        header: { 'content-type': 'application/json' },
        cookies: [],
        errMsg: 'request:ok',
      }

      Promise.resolve().then(() => {
        if (typeof options.success === 'function') options.success(res)
        if (typeof options.complete === 'function') options.complete(res)
      })

      return {
        abort() {},
        onHeadersReceived() {},
        offHeadersReceived() {},
        onChunkReceived() {},
        offChunkReceived() {},
      }
    })

    const page = await miniProgram.reLaunch('/packageAPI/pages/network/request/request')
    await page.waitFor('button')

    const button = await page.$('button')
    if (!button) {
      throw new Error('未找到 request 页面按钮')
    }

    await button.tap()
    await page.waitFor(100)

    const pageData = await page.data().catch(() => ({}))
    if (pageData.loading !== false) {
      throw new Error(`请求结束后 loading 状态异常: ${JSON.stringify(pageData)}`)
    }

    const successLogs = consoleEvents.filter((event) => {
      if (!event || typeof event !== 'object' || !Array.isArray(event.args)) return false
      return event.args.some((arg) => String(arg).includes('request success'))
    })

    if (!successLogs.length) {
      throw new Error(`未观察到 request success 日志: ${JSON.stringify(consoleEvents)}`)
    }

    const consoleErrors = consoleEvents.filter((event) => {
      return event && typeof event === 'object' && event.type === 'error'
    })

    if (consoleErrors.length) {
      throw new Error(`存在 console.error: ${JSON.stringify(consoleErrors)}`)
    }

    if (exceptionEvents.length) {
      throw new Error(`存在 exception: ${JSON.stringify(exceptionEvents)}`)
    }
  } finally {
    if (miniProgram) {
      await miniProgram.restoreWxMethod('request').catch(() => {})
      await miniProgram.close().catch(() => {})
    }
  }
}

run().catch((error) => {
  console.error(error)
  process.exit(1)
})
```

补充说明：
- `console` 事件回调拿到的 payload 通常包含 `type` 和 `args`
- 做失败判定时，优先按 `payload.type === 'error'` 过滤，不要把正常 `log` 一起算成失败

## 模板 E：CLI v2 + `connect()` 完整脚本

当用户说"开发者工具已经开着""不想重启工具""launch 报错想换一种方式"，用这个模板。

```js
const automator = require('miniprogram-automator')
const path = require('node:path')
const fs = require('node:fs/promises')
const { spawnSync } = require('node:child_process')

const CLI_PATH =
  process.env.WECHAT_DEVTOOLS_CLI ||
  '/Applications/wechatwebdevtools.app/Contents/MacOS/cli'

// projectPath 是开发者工具实际打开的目录（含 project.config.json）
const PROJECT_PATH =
  process.env.MINIPROGRAM_PROJECT_PATH || '/absolute/path/to/project'

// 自动化 WebSocket 端口，默认 9420
const AUTO_PORT = Number(process.env.WECHAT_AUTO_PORT || 9420)

const TARGET_PAGE = '/pages/home/index'
const OUTPUT_DIR = path.resolve(process.cwd(), 'outputs')

/**
 * 探测开发者工具当前 HTTP 服务端口。
 * 原理：先用占位端口调用一次 CLI，从错误输出里解析实际端口。
 * 如果工具还没启动，返回 null（CLI 会自行启动）。
 */
function detectHttpPort() {
  if (process.env.WECHAT_DEVTOOLS_PORT) {
    return Number(process.env.WECHAT_DEVTOOLS_PORT)
  }
  try {
    const result = spawnSync(
      CLI_PATH,
      ['auto', '--project', PROJECT_PATH, '--port', '9999'],
      { encoding: 'utf8', timeout: 8000 },
    )
    const output = (result.stdout || '') + (result.stderr || '')
    const match = output.match(/started on http:\/\/127\.0\.0\.1:(\d+)/)
    if (match) return Number(match[1])
  } catch (_) {}
  return null
}

/**
 * 用 CLI v2 命令开启自动化 WebSocket 端口。
 * 命令：cli auto --project <path> --auto-port <port> [--port <httpPort>]
 */
function enableAutomation(httpPort) {
  const args = ['auto', '--project', PROJECT_PATH, '--auto-port', String(AUTO_PORT)]
  if (httpPort) args.push('--port', String(httpPort))
  const result = spawnSync(CLI_PATH, args, { encoding: 'utf8', timeout: 20000 })
  return {
    success: result.status === 0,
    output: (result.stdout || '') + (result.stderr || ''),
  }
}

async function main() {
  let miniProgram
  try {
    await fs.mkdir(OUTPUT_DIR, { recursive: true })

    // Step 1：探测 HTTP 端口，避免 CLI 因端口冲突报错
    const httpPort = detectHttpPort()
    console.log(httpPort ? `HTTP 端口: ${httpPort}` : '未检测到 HTTP 端口，由 CLI 启动')

    // Step 2：用 CLI v2 开启自动化 ws 端口
    const { success, output } = enableAutomation(httpPort)
    if (!success) throw new Error(`CLI auto 命令失败:\n${output}`)
    console.log('自动化端口已就绪')

    // Step 3：connect 到 ws 端点
    miniProgram = await automator.connect({
      wsEndpoint: `ws://127.0.0.1:${AUTO_PORT}`,
    })
    console.log('已连接')

    // Step 4：跳转页面并操作
    const page = await miniProgram.reLaunch(TARGET_PAGE)
    await page.waitFor('.page-title')
    await page.waitFor(200)

    await miniProgram.screenshot({ path: path.join(OUTPUT_DIR, 'page.png') })
    console.log('截图完成')
  } finally {
    if (miniProgram) {
      // connect 模式下 close() 只断开 ws 连接，不关闭开发者工具
      await miniProgram.close().catch(() => {})
    }
  }
}

main().catch((error) => {
  console.error(error)
  process.exit(1)
})
```

补充说明：
- `connect()` 的 `close()` **只断开 WebSocket 连接**，不会关闭开发者工具窗口——这与 `launch()` 后的 `close()` 行为不同
- `--auto-port` 是自动化 ws 端口（automator 连接用），`--port` 是工具 HTTP 服务端口（CLI 管理用），两者不同
- 如果不确定工具 HTTP 端口，可先用 `detectHttpPort()` 探测；如果工具没有运行，CLI 会自行启动

## 模板 D：批量截图脚本片段

当用户要批量截图多个页面、做视觉回归、输出 PNG 清单时，可以复用这一段。

```js
const PAGES = [
  { id: 'home', path: '/pages/home/index' },
  { id: 'list', path: '/pages/list/index' },
]

for (const item of PAGES) {
  const page = await miniProgram.reLaunch(item.path)
  await page.waitFor(500)
  await miniProgram.screenshot({
    path: path.join(OUTPUT_DIR, `${item.id}.png`),
  })
}
```

补充说明：
- 如果页面依赖异步请求或动画，不要只靠 `waitFor(500)`，要配合选择器等待
- 最好输出 `index.json` 汇总每页是否成功
- 用户只想截图时，也可以直接按这个方向生成专门脚本

## Jest 版何时给

如果用户明确说“写成 Jest 用例”“接入 CI”“做回归套件”，把独立脚本改写为：
- `beforeAll`：启动 `miniProgram`
- `afterAll`：恢复 Mock、关闭 `miniProgram`
- `test/it`：执行页面跳转、交互和断言

但不要在用户只想要“一个脚本模板”时，默认切到 Jest。那会把简单问题变复杂。

## 常见错误与修正

| 常见错误 | 正确做法 |
|---|---|
| 把 `projectPath` 固定写成源码仓库根目录 | 写成"开发者工具实际打开的目录"，Taro 等场景可能是 `dist/` |
| 只提醒安装依赖，不提醒安全设置 | 必须提醒开启服务端口 |
| 全靠固定 `sleep` | 优先 `page.waitFor(selector/condition)` |
| 用 `page.$('form-panel input')` 查组件内部元素 | 先 `page.$('form-panel')`，再 `panel.$('input')` |
| 用运行时 patch `wx.request` 作为默认方案 | 默认优先 `miniProgram.mockWxMethod('request', ...)` |
| 忘记恢复 mock | 在 `finally` 或 `afterAll` 里 `restoreWxMethod` |
| 把截图当成真机能力 | 明确说明截图仅支持开发者工具模拟器 |
| 直接读 `input.data()` 当通用方案 | 原生输入框优先 `value()` / `property('value')`；组件状态读组件实例 `data()` |
| 使用 `miniprogram-automator` 旧版本（0.5.x 等） | 升级到 `0.12.0+`，旧版 CLI 命令格式已废弃，会报 code 31 错误 |
| `automator.launch()` 在开发者工具已开着时调用 | launch 前必须确保开发者工具完全退出（Cmd+Q） |
| `launch()` 不设置 timeout 或 timeout 太短 | 首次启动 + 用户确认信任需要时间，建议 `timeout: 120000` |
| 页面路径不以 `/` 开头（如 `page/component/index`） | 必须以 `/` 开头（`/page/component/index`），否则路径会被错误拼接 |
| 用选择器等待可能超时的页面（如首页列表）直接截图 | 首页等复杂页面用固定等待 `waitFor(2000)` 兜底更可靠 |
| 开发者工具已开着时还用 `launch()`，或 `launch()` 总是报错 | 改用 CLI v2 + `connect()` 方式：先 `cli auto --project <path> --auto-port <port>` 开端口，再 `automator.connect({ wsEndpoint })` |
| `connect()` 后 `close()` 关掉了开发者工具 | `connect()` 模式下 `close()` 只断 ws 连接，不关闭工具窗口，行为与 `launch()` 不同 |

## 排障提示

### 启动失败 / 超时
优先检查：
1. `miniprogram-automator` 版本是否 `>= 0.12.0`（旧版会报 code 31）
2. 开发者工具是否已**完全退出**（`launch()` 不能与已运行实例共存）
3. 开发者工具是否已安装并登录
4. CLI 路径是否正确
5. 安全设置 → 服务端口是否已开启
6. `projectPath` 是否真的是开发者工具打开的目录（含 `project.config.json`）
7. 是否设置了足够长的 `timeout`（首次启动建议 `120000`）

如果 `launch()` 持续失败（尤其是开发者工具已在运行时），换用 **CLI v2 + `connect()`** 方式（见模板 E）：
- 先执行 `cli auto --project <path> --auto-port <port>` 开启自动化 ws 端口
- 再用 `automator.connect({ wsEndpoint: 'ws://127.0.0.1:<port>' })` 连接
- 用 `detectHttpPort()` 探测当前 HTTP 端口可避免端口冲突报错

### 跳页成功但选不到元素
优先检查：
1. 选择器是否稳定
2. 页面是否仍在异步渲染
3. 是否误把组件内部节点当成页面级节点查找

### Mock 没生效
优先检查：
1. 是否在页面首次请求前就安装了 mock
2. 业务层是否最终真的调用了被 mock 的 wx 方法
3. 用例结束时是否有前一轮残留污染

### 截图失败
优先检查：
1. 是否在开发者工具模拟器里运行
2. 页面是否已稳定渲染
3. 输出目录是否可写

## 回答时的落地习惯

如果用户要你直接改项目文件，优先遵循这条路径：
1. 先说明你准备创建或修改哪个脚本文件
2. 先确认路径、页面、CLI、目标行为
3. 再写文件
4. 最后给运行命令和成功判定方式

如果用户只是在问“怎么做”，就先输出模板，不要擅自创建一堆文件。
