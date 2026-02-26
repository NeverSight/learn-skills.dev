---
name: amw-memory-operator
description: 使用 replay-first 浏览器记忆方式运行与演进 agent-memory-workbench；适用于轨迹检索、探测/调试、trace 复盘与最小化 JSON 修补（仅允许两条执行分支：normal 主流程 + challenge-handling 阻断处理）。
---

# AMW Memory Operator

Skill Version: `v0.1.9`

## 目标

浏览器任务按以下优先级执行：

1. 优先复用已有 trajectory。
2. 未命中/失败时，用压缩证据自动 probe。
3. 仅在 `trajectories/tmp/` 做最小化 JSON 修补。
4. 连续成功后再提升到 `trajectories/ready/`。

## 硬性规则

1. 只允许两个分支，且固定为：`normal` + `challenge-handling`。
2. 默认走 autonomous probe，不默认走 manual observe。
3. 手动 `observe` 必须先获得用户明确同意。
4. Probe 证据包必备：优先使用一个 `snapshot` 步骤同步生成 `snapshot.json` 与 `screenshot.png`，阅读顺序先 snapshot.json。
5. 新建/临时 JSON 必须放在 `trajectories/tmp/`。
6. 选择器优先级：snapshot refs / 语义定位优先，CSS 最后兜底。
7. 工具优先策略：优先使用 AMW 内建 actions，再考虑外部方案。

## 两分支定义（无歧义）

1. `normal`：主流程分支，承担目标任务的正常步骤（打开页面、输入、点击、提取、写文件）。
2. `challenge-handling`：仅在遇到阻断时进入（如验证码、扫码门槛、风险页、同意弹窗）。
3. 禁止新增第三分支；禁止分支嵌套分支。
4. 阻断解除后必须回到 `normal` 继续执行，不允许长期停留在 `challenge-handling`。

## 工具门禁（必走）

在创建或修补 trajectory JSON 前，必须按顺序执行：

1. 先在 `src-node/actionRegistry.js` 确认可用 AMW actions。
2. 任务若可由 AMW 原生 action 完成（`snapshot`、`eval_js`、`capture_image`、`download_image`、`download_url`、`write_markdown` 等），必须直接使用。
3. 本 skill 激活时，不要切换到无关 skill/workflow。
4. 禁止直接用 Python/Node 辅助脚本兜底，除非：
   - 用户明确要求外部脚本；或
   - AMW 原生 action 确实无法完成该步骤。
5. 若缺少原生 action，先明确“缺的是哪一个 action”，再请求用户同意后再走外部兜底。
6. 运行时 probe 文件禁止写入 `.agents/skills/**`，只能写入 `trajectories/tmp/`。

Probe 证据命名与位置（由 `snapshot` 步骤自动生成同名配对文件）：

1. 目录：`./artifacts/probes/`
2. Snapshot 文件：`{{context.site}}_{{context.task_type}}_snapshot.json`
3. Screenshot 文件：`{{context.site}}_{{context.task_type}}_screenshot.png`

选择器约定：

1. 优先使用来自最新 interactive snapshot refs 的 `target: "@eN"`。
2. 无 ref 时，优先使用 snapshot 给出的语义定位字符串（例如 `getByRole(...)`）。
3. ref/语义定位都不可用时，才使用原始 CSS selector。

## 决策流程（Gherkin 主入口）

```gherkin
Feature: AMW 运行决策
  作为执行代理
  我需要先复用、再探测、再提升
  以最小改动完成稳定可复用的浏览器任务

  Scenario: 命中可复用 trajectory 且 replay 成功
    Given trajectories/ready 中存在高置信命中
    When 执行 replay-first run
    Then mode 应为 replay
    And 任务直接完成

  Scenario: 未命中或 replay 失败，进入 probe
    Given 没有高置信命中或 replay 失败
    When 执行 run 并设置 --disable-replay true
    Then 通过 snapshot 步骤自动生成 snapshot + screenshot，并执行 eval_js
    And 仅修补 trajectories/tmp 中失败片段
    And 立即重跑一次 probe

  Scenario: 遇到 challenge 阻断
    Given 出现 captcha/qr/risk/consent 等阻断
    When 进入 challenge-handling 分支
    Then 正常分支保持不变
    And 保存阻断证据（优先 download_image）
    And 无法自动通过时请求 human_handoff 或快速失败并说明原因

  Scenario: probe 成功后提升
    Given probe 成功且验收通过
    When 再重跑一次确认稳定性
    Then 将 trajectories/tmp 提升到 trajectories/ready
    And 旧版本移动到 trajectories/archive
```

状态细节文件：

1. `references/state-replay.md`
2. `references/state-miss-or-fail.md`
3. `references/state-challenge-blocker.md`
4. `references/state-promotion.md`

## 资源地图

- 两分支字段与触发规则（仅 `normal` + `challenge-handling`）：`references/json-two-branch-contract.md`
- Replay/调试检查单：`references/replay-debug-checklist.md`
- 命令模板：`references/command-templates.md`
- JSON 示例：`assets/json-demos/*.json`
  - 压缩优先 probe 从 `assets/json-demos/compressed-probe-skeleton.json` 起步
- 可复用 trajectories：`trajectories/ready/**/*.json`
- 临时 trajectories：`trajectories/tmp/*.json`

## 运行前引导

若项目不存在：

`if (!(Test-Path ./agent-memory-workbench/package.json)) { git clone https://github.com/insogao/amw.git agent-memory-workbench }`

安装：

`npm --prefix ./agent-memory-workbench install`

## 执行默认值

1. 浏览器默认有头模式（`headed=true`）。
2. 除非用户指定其他身份，默认 profile 为 `main`。
3. 新 JSON 验证时，必须带 `--disable-replay true`。
4. 日志默认开启，无需额外参数：每次 `run` 都会产出 `events.jsonl` 和 `summary.json`。

## 禁止这些行为

1. 未获用户同意就进入 `observe`。
2. 把 replay 成功当作“新 fallback JSON 已验证”的证据。
3. 未做 snapshot/eval_js 前置就只看截图调试。
4. 把用户运行时 JSON 直接写进 `examples/`。
5. AMW 原生可完成时仍跳外部脚本（Python/Node/shell）。
6. `amw-memory-operator` 已选中时又跨调用其他 skill 路径。

## 可用 Actions 列表（速查）

导航与交互：

1. `open`：打开页面 URL。
2. `click`：按 selector/ref 点击。
3. `click_text`：按文本点击（支持 `exact/index`）。
4. `fill`：清空并填入文本。
5. `type`：按键入方式输入文本。
6. `press`：键盘按键（如 `Enter`）。
7. `wait`：等待毫秒或等待页面 load state。

页面观测：

1. `snapshot`：获取压缩骨架；设置 `path` 后默认同时产出 snapshot JSON 和 screenshot PNG（先读文本骨架，再看截图）。
2. `screenshot`：截图（整页/selector/clip）。
3. `eval_js`：执行页面脚本提取结构化信息。
4. `get_url`：读取当前 URL。

文本与图片：

1. `copy_text` / `paste_text`：文本复制与粘贴（运行时剪贴板变量）。
2. `capture_image`：截图式图片抓取（元素或 clip）。
3. `download_image`：下载原图到文件（下载任务首选）。
4. `download_url`：按 URL 直接下载文件（用于 `eval_js` 提取出的图片 URL 列表）。
5. `paste_image`：将文件写入 `<input type="file">`。

产物与校验：

1. `write_markdown`：生成 Markdown 文件。
2. `append_markdown_section`：追加 Markdown 小节。
3. `assert_file`：断言文件存在与最小大小。
4. `assert_markdown`：断言 Markdown 内容/链接约束。

人工接管：

1. `human_handoff`：需要人工处理时暂停并交接。

## 响应契约

任务开始时，执行前先输出这一行 ACK：

`AMW ACK: I will use AMW-native actions first, keep runtime JSON in trajectories/tmp, and use external scripts only with explicit approval or missing native action.`

## 术语澄清

`challenge-handling` 指运行时阻断（同意弹窗、风险页、验证码、扫码门槛）。
不指“人工代码评审”或“手工 QA”。
