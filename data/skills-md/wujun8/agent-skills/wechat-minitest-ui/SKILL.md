---
name: wechat-minitest-ui
description: Use WeChat MiniTest and DevTools CLI to run mini-program automation, capture screenshots, and verify UI via image diff. Use when the user wants to run minitest, automate screenshots, validate UI, or integrate MiniTest/Minium with the WeChat Developer Tools CLI.
alwaysApply: false
---

# 微信 MiniTest 自动化截图与 UI 校验

## 何时使用本 Skill

在以下场景下使用本 skill：

- 用户要求「跑 minitest」「启动微信开发者工具做自动化测试」「自动截图」「验证 UI 是否有问题」
- 需要把微信开发者工具 CLI、MiniTest/录制回放、Minium 脚本、图片对比串联成完整流程
- 需要编写或维护 Minium（Python）截图脚本、或配置 CLI 启动自动化端口

**不适用**：纯 Web 端 E2E、非微信小程序的自动化测试。

---

## 流程概览

1. **确认项目**：项目根目录需包含 `project.config.json`（含 `appid` 等）。Taro 项目一般为仓库根目录，编译产物在 `dist`，由 `miniprogramRoot` 指定。
2. **启动自动化**：用微信开发者工具 CLI 的 `cli auto` 或 `cli auto-replay` 打开项目并开启自动化端口（默认 9420）。
3. **截图**：录制回放中的截屏步骤，或 Minium Python 的 `self.capture(name)` / `self.app.screen_shot(save_path)`。
4. **验证 UI**：MiniTest 云测「图片对比」（SSIM），或本地脚本对比基准图与当前截图。

---

## 1. 微信开发者工具 CLI

- **前置**：在开发者工具 **设置 → 安全设置** 中开启 **服务端口**。
- **CLI 路径**：
  - macOS: `/Applications/wechatwebdevtools.app/Contents/MacOS/cli`
  - Windows: `"<安装路径>/cli.bat"`
- **开启自动化（Minium 脚本用）**：
  ```bash
  cli auto --project "/path/to/project/root" --auto-port 9420
  ```
  项目路径为包含 `project.config.json` 的目录（Taro 项目即仓库根目录）。
- **录制回放（可含截屏）**：
  ```bash
  cli auto-replay --project "/path/to/project/root"
  cli auto-replay --project "/path/to/project/root" --replay-all
  ```
- **仅打开项目**：`cli open --project "/path/to/project/root"`（不开启自动化端口）。

---

## 2. Minium Python（参考 [Minium Python 文档](https://minitest.weixin.qq.com/#/minium/Python/readme)）

### 2.1 环境与安装

- **Python**：3.8 及以上。
- **微信公共库**：>= 2.7.3；开发者工具使用最新版并开启服务端口。
- **安装**：
  ```bash
  pip install minium
  # 或安装最新版
  pip install https://minitest.weixin.qq.com/minium/Python/dist/minium-latest.zip
  ```
- **验证**：`minitest -v`。

### 2.2 入口与配置

- **测试入口**：用例类继承 `minium.MiniTest`（基于 `unittest.TestCase`），通过 `self.page`、`self.app`、`self.native` 等操作小程序。
- **配置文件**：运行时常通过 `-c config.json` 指定配置，关键字段示例：
  ```json
  {
    "project_path": "/absolute/path/to/project/root",
    "dev_tool_path": "/Applications/wechatwebdevtools.app/Contents/MacOS/cli",
    "test_port": 9420,
    "platform": "ide",
    "app": "wx",
    "assert_capture": true,
    "request_timeout": 60
  }
  ```
  `project_path` 为含 `project.config.json` 的目录绝对路径；`test_port` 需与 CLI `--auto-port` 一致（如 9420）。
- **运行用例**（需先已用 CLI 打开项目并 `cli auto --auto-port 9420`）：
  ```bash
  minitest -m test_module_name -c config.json -g
  ```
  报告在 `outputs` 目录，可用 `python -m http.server 12345 -d outputs` 查看。

### 2.3 截图 API

| API | 说明 |
|-----|------|
| **`self.capture(name)`** | 用例内截屏并命名，便于报告与图片对比；配合配置中 `assert_capture` 可做断言。 |
| **`self.app.screen_shot(save_path, format='raw')`** | 整屏截图保存到 `save_path`；`format` 可为 `'raw'` 或 `'pillow'`。 |

**注意**：在开发者工具模拟器中，截图仅包含 WXML 页面内容，弹窗、授权框等覆盖层可能无法截到。

### 2.4 元素与操作示例

- 定位：`self.page.get_element(selector, inner_text='...')` 等。
- 操作：`.click()`、设置/获取页面数据等，详见 [Minium Python 文档](https://minitest.weixin.qq.com/#/minium/Python/readme)。

---

## 3. 其他截图方式

| 方式 | 说明 |
|------|------|
| **录制回放** | 在开发者工具中录制用例时加入「截屏」步骤；云测回放时生成截图，可用于图片对比。 |
| **Minium** | 见上文 `capture` / `screen_shot`。 |

---

## 4. UI 验证（图片对比）

- **云测报告**：在 MiniTest 云测的「图片对比」中，选择基准图与当前截图，用 SSIM 等算法对比，可忽略区域、顶部 banner 等。
- **本地/脚本**：将 Minium 截得的图与基准图做像素/区域对比，或在脚本中根据结果断言通过/失败。

---

## 5. 当前项目注意点

- 项目根目录即包含 `project.config.json` 的目录，`miniprogramRoot` 为 `./dist`，先执行 Taro 编译（如 `pnpm build:weapp`）再跑自动化。
- CLI 的 `--project` 与 Minium 配置的 `project_path` 均使用**项目根目录的绝对路径**。
- 仓库内已有 `config.json`（含 `project_path`、`test_port: 9420` 等）和示例用例 `test_poster.py`（继承 `minium.MiniTest`，使用 `self.capture`）。
- **测试脚本**：Minium Python 用例统一放在当前项目下的 `tests` 目录（如 `tests/test_poster.py`），便于管理和运行。
- **测试输出**：Minium 默认将报告与截图输出到 `tests/outputs` 目录，需将 `tests/outputs/` 加入 `.gitignore`，避免把测试产物提交到仓库。

---

## 6. 执行清单（Agent 可逐步执行）

1. [ ] 确认 `project.config.json` 存在且含 `appid`（可为 touristappid）。
2. [ ] 若为 Taro 项目，确认已构建（如 `pnpm build:weapp`），使 `dist` 存在。
3. [ ] 使用 CLI 启动自动化：`cli auto --project <项目根绝对路径> --auto-port 9420`；或录制回放：`cli auto-replay --project <项目根绝对路径>`。
4. [ ] 若用 Minium：确认 `config.json` 中 `project_path`、`test_port` 正确，运行 `minitest -m <模块> -c config.json -g`，在关键步骤使用 `self.capture(name)` 或 `self.app.screen_shot(save_path)`。
5. [ ] 若用云测：在云测任务中配置录制回放或 Minium 用例，在报告中查看「图片对比」结果。
6. [ ] 根据对比结果或脚本断言，向用户汇报 UI 是否通过验证。

---

## 参考链接

- **[Minium Python 文档（官方）](https://minitest.weixin.qq.com/#/minium/Python/readme)** — 安装、配置、API、示例
- [MiniTest 云测服务简介](https://developers.weixin.qq.com/miniprogram/dev/devtools/minitest/)
- [自动化测试（Monkey / 录制回放 / 自定义测试）](https://developers.weixin.qq.com/miniprogram/dev/devtools/minitest/autotest.html)
- [图片对比能力说明](https://developers.weixin.qq.com/miniprogram/dev/devtools/minitest/image_diff.html)
- [命令行 V2](https://developers.weixin.qq.com/miniprogram/dev/devtools/cli.html)
