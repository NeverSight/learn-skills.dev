---
name: mijia-geek-console
description: 米家自动化极客版 Web 控制台自动化操作（登录/导出/导入/读改变量/执行日志回放）与导入排错避坑。支持 opencode、OpenClaw、Hermes。
---

# 米家极客版 Web 控制台自动化

> 配套：规则 JSON/节点见 **mijia-geek-rule**；.bak 打包/解包见 **mijia-geek-backup**。
> 入门用户请先加载 **mijia-geek-beginner**。

**控制台地址**：`http://<中枢网关IP>:8086`（IP **因家而异，需用户自填**）。

---

## 工具映射表（按 Agent 优先使用原生能力）

本技能涉及浏览器自动化操作。下表列出各 Agent 的工具名映射：

| 操作 | opencode | OpenClaw | Hermes |
|------|----------|----------|--------|
| 打开页面 | `playwright_browser_navigate` | `browser open` | `browser_navigate` |
| 页面快照 | `playwright_browser_snapshot` | `browser snapshot` | `browser_snapshot` |
| 点击元素 | `playwright_browser_click` | `browser act` | 快照 ref + 交互 |
| 输入文本 | `playwright_browser_type` | `browser act` | 快照 ref + 交互 |
| 上传文件 | `playwright_browser_file_upload` | `browser act`（触发文件选择器）| 文件选择器触发 |
| 控制台日志 | `playwright_browser_console_messages` | 浏览器 console 能力 | 浏览器 console 能力 |
| 等待 | `playwright_browser_wait_for` | `browser wait` | 等待/轮询快照 |

> 🚨 **执行前先确认**：opencode 需 Playwright MCP 已配置（不可用则引导 `npx @anthropic/mcp-server-playwright` + 配置模板）。OpenClaw/Hermes 使用上表原生工具**无需额外安装**。若原生工具不可用 → Playwright MCP 兜底。

---

## 登录（唯一人机协作点）

首页要求 **6 位数字登录码**——用户从米家 App 取（中枢插件→更多设置→自动化极客版→获取登录码）。**一次性、刷新即失效**。

🚨 **任何硬刷新都会登出**，登录态在会话内保持（见下方 SPA 导航避坑）。

---

## 界面导航

🚨 **页面内元素点击切换视图，切勿 `browser_navigate` 跳 hash 路由。**

| 操作 | 路径 | 要点 |
| --- | --- | --- |
| **导出备份** | 自动化列表→「恢复与备份」→「备份至本地」 | 自动下载，含全部规则+变量+真实 did |
| **导入备份** | 「恢复与备份」→「恢复备份」→「上传文件」（传 .bak 绝对路径）→「确定」 | 🚨**全量覆盖**当前数据 |
| **读设备列表** | 「设备列表」 | 名称/房间/品类齐全；did 走 WebSocket 不在 DOM，取 did 从导出 .bak 解包 |
| **读/改变量值** | 「全局变量列表」→变量「编辑」→「当前值」 | 可用于**注入测试** |
| **取经纬度** | 创建自动化→拖「定时」卡→类型选「日落/日出」→「获取经纬度」 | 🚨需用户授权浏览器定位 |
| **执行日志/回放** | 自动化列表点规则名进编辑器→底部「文档」图标→「自动化重载」面板 | 见下「行为验证」 |

**画布编辑**：左侧卡片按类目分组，加卡片须**拖拽**（点击仅弹提示）；退出前没点「保存」不持久化。

---

## 自验证闭环（推荐）

生成规则 JSON → 打包 .bak → 导入（覆盖）→ **三重验证** → 不符则改 JSON 重来：

1. **画布结构自检**：进编辑器看规则渲染成的卡片，逐卡比对设计确认节点语义无误。
2. **读全局变量值**：变量驱动型逻辑可注入/读取全局变量确认。
3. 🔑 **执行日志/回放（最强）**：编辑器底部「文档」图标→选时间范围→点记录在画布上**逐节点回放**每步结果。**无报错执行 + 链路走向符合预期 = 行为验证通过**。

🔑 **调试期缩短长延时，上线前恢复**：长延时先临时改秒级（如 20s）便于快速触发验证，通过后恢复生产值重导。

---

## 🚨 导入排错与避坑

- **校验时机**：节点校验在「上传文件」**选中文件那一刻**就跑，不是点「确定」时。判据——选文件后「确定」**保持可点**=校验通过；若「确定」变 **loading 永不结束**=校验失败。
- **定位违规节点**：失败时查看浏览器控制台报错，搜索 `Uncaught ... Invalid node parameter:<节点id>,<原因>`。
- **失败会污染全局状态**：一次校验失败后「确定」**永久 loading**，后续重开的导入弹窗一打开就是 loading——此时任何重试都无效，看到的报错都是旧的。
- ⚠️ **「导入成功」≠「编辑器能渲染」**：枚举属性用标量而非 `include`+数组（见 mijia-geek-rule）会让编辑器整页白屏崩溃（控制台见 `Uncaught TypeError`，如 `r.includes is not a function`）。崩溃后只能**硬刷新**（=登出重登）。⟹ 导入后**务必进编辑器确认能正常渲染**。
- **必须硬刷新才能恢复**：但硬刷新=登出。⟹ **代价高，别靠反复重试**：改完一版先本地审计（用 mijia_rule_kit 的 `validate`），力求**一次导对**。

---

## 🚨 SPA 导航避坑

- 导航到**相同 hash**= 空操作，脏状态清不掉
- 导航到**不同 hash**= React 白屏，hash 路由救不回，只能硬刷新
- 导航到**无 hash URL**= 硬刷新 = **登出**（需用户重取码）
- ✅ 正确做法：用页面内元素点击切换视图；只有清污染/登出时才有意硬刷新

---

## opencode 配置（若 Playwright MCP 未配）

```json
// opencode.json 或 .mcp.json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@anthropic/mcp-server-playwright"]
    }
  }
}
```

## OpenClaw 配置（MCP 兜底，非必须）

```yaml
# ~/.openclaw/openclaw.json
mcp_servers:
  playwright:
    command: "npx"
    args: ["-y", "@anthropic/mcp-server-playwright"]
```

## Hermes 配置（MCP 兜底，非必须）

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  playwright:
    command: "npx"
    args: ["-y", "@anthropic/mcp-server-playwright"]
```
