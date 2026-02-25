---
name: easytouch-mcp
description: 使用 EasyTouch 进行跨平台桌面自动化。适用于鼠标键盘控制、截图、窗口管理、系统信息、剪贴板，以及基于 browserId 的浏览器自动化流程。
---

# EasyTouch Automation Skill

该技能用于指导 AI 助手通过 `et` 命令执行桌面自动化任务。  
适用于 CLI 调用和 MCP 集成场景，重点是稳定的操作流程与可复现命令。

## 何时使用

- 需要控制鼠标、键盘执行桌面操作
- 需要截图、取色、识别前台窗口状态
- 需要查询系统信息、进程、剪贴板
- 需要浏览器自动化，且操作是多步骤任务（启动 -> 导航 -> 点击/输入 -> 截图）

## 前置条件

- 已安装 EasyTouch，可执行文件可通过 `et` 调用
- 如使用浏览器能力，确保本机可启动 Playwright 浏览器
- `skills` 仓库仅提供文档，不内置二进制；需先安装程序本体（例如 `easytouch-windows`）

## 快速自检

```bash
et --version
et mouse_position
et screen_list
```

## 常用命令域

- 鼠标：`mouse_move` `mouse_click` `mouse_scroll` `mouse_position`
- 键盘：`key_press` `type_text`
- 屏幕：`screenshot` `pixel_color` `screen_list`
- 窗口：`window_list` `window_find` `window_activate` `window_foreground`
- 系统：`os_info` `cpu_info` `memory_info` `disk_list` `process_list`
- 剪贴板：`clipboard_get_text` `clipboard_set_text` `clipboard_get_files`
- 浏览器：`browser_*`

## 浏览器自动化操作手册（重点）

### 1) 执行模型（先理解这个）

- 所有浏览器动作都依赖 `browserId`
- `browser_launch` 只负责创建会话，不会替你完成后续业务步骤
- 当前实现通过后台 daemon 持有会话，所以命令结束后会话仍可复用
- 你必须显式管理会话：创建、使用、关闭

支持浏览器：
- `chromium`
- `firefox`
- `webkit`
- `edge`（内部使用 `msedge` 通道）

注意：通过 npm 安装 EasyTouch 时已内置 Playwright 运行能力，本技能不包含手动安装步骤。

### 2) 标准操作逻辑（AI 必须遵守）

每个浏览器任务按固定顺序执行：

1. 创建会话：`browser_launch`
2. 确认会话：`browser_list`，提取目标 `browserId`
3. 打开目标页：`browser_navigate`
4. 等待页面可交互：`browser_wait_for`
5. 执行交互：`browser_click` / `browser_fill` / `browser_select` / `browser_upload`
6. 验证结果：`browser_get_text` / `browser_assert_text` / `browser_page_info`
7. 留证据：`browser_screenshot`
8. 结束任务：`browser_close`

如果中途失败，不要直接重启所有步骤，优先：
- 先 `browser_page_info` 看当前 URL/标题
- 再 `browser_wait_for` 重试关键元素
- 仍失败才考虑关闭旧会话并重新 `browser_launch`

### 3) CLI 流程模板

```bash
# 创建会话
et browser_launch --browser edge --headless false

# 读取 browserId（以下示例假设为 browser_1）
et browser_list

# 导航
et browser_navigate --browser-id browser_1 --url "https://example.com"

# 等待并操作
et browser_wait_for --browser-id browser_1 --selector "input[name='q']" --state visible --timeout 15000
et browser_fill --browser-id browser_1 --selector "input[name='q']" --value "EasyTouch"
et browser_click --browser-id browser_1 --selector "button[type='submit']"

# 验证与截图
et browser_get_text --browser-id browser_1 --selector "body"
et browser_screenshot --browser-id browser_1 --output "./result.png" --full-page true

# 收尾
et browser_close --browser-id browser_1
```

### 4) MCP 命令映射（AI 调用重点）

CLI 参数名与 MCP 参数名不同，常用映射如下：

| CLI 命令 | MCP `name` | 关键 `arguments` |
|---|---|---|
| `browser_launch` | `browser_launch` | `browserType`, `headless`, `executablePath`, `userDataDir` |
| `browser_navigate` | `browser_navigate` | `browserId`, `url`, `waitUntil`, `timeout` |
| `browser_click` | `browser_click` | `browserId`, `selector`, `selectorType`, `button`, `clickCount` |
| `browser_fill` | `browser_fill` | `browserId`, `selector`, `selectorType`, `value`, `clear` |
| `browser_wait_for` | `browser_wait_for` | `browserId`, `selector`, `selectorType`, `state`, `timeout` |
| `browser_screenshot` | `browser_screenshot` | `browserId`, `selector`, `fullPage`, `outputPath`, `type` |
| `browser_close` | `browser_close` | `browserId`, `force` |
| `browser_list` | `browser_list` | `{}` |

MCP 调用范式：

```json
{
  "jsonrpc": "2.0",
  "id": "browser-1",
  "method": "tools/call",
  "params": {
    "name": "browser_launch",
    "arguments": {
      "browserType": "edge",
      "headless": false
    }
  }
}
```

```json
{
  "jsonrpc": "2.0",
  "id": "browser-2",
  "method": "tools/call",
  "params": {
    "name": "browser_navigate",
    "arguments": {
      "browserId": "browser_1",
      "url": "https://example.com",
      "waitUntil": "load",
      "timeout": 30000
    }
  }
}
```

### 4.1) 截图文件路径规范（必须遵守）

AI 调用 `browser_screenshot` 时，必须显式传 `outputPath`，不要依赖默认路径。

原因：
- 不传 `outputPath` 时，截图会落到系统临时目录（`Path.GetTempPath()`）
- AI 往往不会在后续步骤自动定位临时目录，导致“找不到截图文件”

执行规则：
1. 每次截图都传明确路径  
2. 优先使用当前任务可访问目录（如仓库下 `artifacts/screenshots`）  
3. 截图后始终读取返回值里的 `imagePath`，后续一律用这个实际路径  
4. 不要自行猜测文件位置，不要硬编码与返回值不一致的路径

CLI 示例：

```bash
et browser_screenshot --browser-id browser_1 --full-page true --output "./artifacts/screenshots/search-result.png"
```

MCP 示例：

```json
{
  "jsonrpc": "2.0",
  "id": "browser-3",
  "method": "tools/call",
  "params": {
    "name": "browser_screenshot",
    "arguments": {
      "browserId": "browser_1",
      "fullPage": true,
      "outputPath": "E:\\workspace\\EasyTouch\\artifacts\\screenshots\\search-result.png",
      "type": "png"
    }
  }
}
```

收到响应后：
- 记录 `data.imagePath`
- 后续如果要读取/上传/展示截图，使用 `data.imagePath`，不要改写成其他路径

### 5) 选择器策略（提高成功率）

优先级建议：
1. 稳定属性选择器：`[data-testid='xxx']`、`[name='xxx']`
2. 语义化 CSS：`form button[type='submit']`
3. 文本选择：`selectorType=text`（仅在文案稳定时使用）
4. XPath：仅在复杂结构时兜底

每次点击/输入前，都先 `browser_wait_for`：
- `state=visible` 用于可见元素操作
- `state=attached` 用于只要求在 DOM 中存在的元素

### 6) 常见任务模板

登录流程模板：
1. `browser_navigate` 打开登录页
2. `browser_wait_for` 等待用户名框
3. `browser_fill` 填用户名/密码
4. `browser_click` 提交按钮
5. `browser_wait_for` 等待登录后标志元素
6. `browser_screenshot` 存证

搜索流程模板：
1. `browser_wait_for` 搜索框
2. `browser_fill` 关键词
3. `browser_click` 搜索按钮
4. `browser_wait_for` 结果列表
5. `browser_get_text` 读取前几条结果摘要

### 7) 会话与异常恢复

`browser_list` 为空：
- 先查 `et browser_daemon_status`
- 若 daemon 不在，重新 `browser_launch`

`browserId` 无效：
- 会话可能已关闭或 daemon 重启
- 重新创建会话，替换为新 `browserId`

页面跳转后元素找不到：
- 增大 `browser_wait_for --timeout`
- 改用更稳定的选择器
- 用 `browser_page_info` 确认是否跳到了预期页面

执行完成必须收尾：
- 单任务结束：`browser_close --browser-id ...`
- 需要彻底结束后台持久化：`browser_daemon_stop`

## MCP 使用建议

如需供 AI 客户端长期调用，使用 MCP 模式：

```bash
et --mcp
```

示例配置：

```json
{
  "mcpServers": {
    "easytouch": {
      "command": "et",
      "args": ["--mcp"]
    }
  }
}
```

## 参考文档

- 项目说明：`README.md`
- 技能文档：`skills/SKILLS.md`
