---
name: vmos-edge-control-api
description: Use this skill when controlling a VMOS Edge Android cloud phone through the Android Control API. If the current session also has `vmos-edge-container-api`, use `host_ip` and resolve the target `db_id` through the container APIs first. If this skill is installed alone, prefer `cloud_ip`; if `host_ip` and `db_id` are already known, the host route can also be used. If no IP is provided and local `cbs_go` is running, default `host_ip` to `127.0.0.1`.
---

# VMOS Edge Android Control

在需要通过 VMOS Edge Android Control API 控制单台安卓云机时使用这个 skill。MCP 是可选通道，不是前置依赖。

## 连接入口

- 如果用户已经明确给了 `host_ip` 或 `cloud_ip`，优先使用用户给的值
- 如果用户没有明确给 IP，先检查本地是否存在 `cbs_go` 进程；存在则默认 `host_ip=127.0.0.1`
- 如果用户没有明确给 IP，且本地没有 `cbs_go`，引导用户提供 `host_ip`、`cloud_ip`，或在已知宿主机场景下提供 `db_id`
- 如果当前会话里同时安装了 `vmos-edge-container-api`：
  - 使用宿主机路由 `http://{host_ip}:18182/android_api/v2/{db_id}`
  - 必须先通过 container API 的 `POST /container_api/v1/get_db` 或 `GET /container_api/v1/get_android_detail/{db_id}` 拿到目标 `db_id`
- 如果当前只有 `vmos-edge-control-api`：
  - 默认优先使用云机直连 `http://{cloud_ip}:18185/api`
  - 仅支持开启了局域网模式的云机
- 如果当前只有 `vmos-edge-control-api`，而当前路径要走 `host_ip`：
  - 如果用户已经给了 `db_id`，直接使用 `http://{host_ip}:18182/android_api/v2/{db_id}`
  - 如果没有 `db_id`，明确说明还缺少 `db_id` 或 `vmos-edge-container-api`
- 如果直连 `http://{cloud_ip}:18185/api/base/version_info` 连不上、超时，或返回 `5xx`，明确说明当前云机没有暴露 Control API，或没有开启局域网模式

## 核心流程

- 始终遵循 `Observe -> Plan -> Act -> Verify`
- 第一次连接先查 `/base/version_info`
- `/base/version_info` 能成功返回，就视为当前环境支持 Control API；拿不到返回再说明当前环境不支持或没有暴露接口
- 本地检查 `cbs_go` 时，优先用精确匹配，例如 `pgrep -x cbs_go >/dev/null 2>&1`
- 再用 `/base/list_action` 做能力发现：
  - 需要低成本查看当前设备支持哪些接口时，先取接口列表
  - 需要某个接口的详细用法时，再按 `paths` 定向查询并带上 `detail`
- 观察优先级：
  - 截图接口 `screenshot/format`、`screenshot/raw`、`screenshot/data_url`
  - `/accessibility/dump_compact`
  - `/accessibility/node` 的无动作查询
  - `/display/info`、`/activity/top_activity`、`/package/list`
- 观察策略：
  - 需要看视觉布局、图标、颜色、弹窗遮挡、坐标点击位置时优先截图
  - 需要低成本获取文本、层级、bounds，或要衔接 `/accessibility/node` 时优先 `dump_compact`
  - 能同时用时，先截图理解界面，再用 `dump_compact` / `node` 做结构化定位
  - 截图回显给用户时：先用 bash/exec 的 `curl -o` 把截图落盘到 workspace 目录（如 `~/.openclaw/workspace/`），再用 read 工具读取该文件让模型看到图片内容
  - 回图时优先把 `screenshot/format` 或 `screenshot/raw` 落成文件；只有 `screenshot/data_url` 可用时，再 base64 解码落盘
  - 不要在文本回复里写 `MEDIA:` 或直接贴 base64 / data_url —— 这些不会渲染为图片
  - 如果需要把图片转发到消息渠道（Telegram 等），使用 `message --media <路径>` 工具发送
- 不要把旧版无障碍导出 / 查找接口写进默认流程
- 交互优先级：
  - 先根据截图、`dump_compact` 或 `/accessibility/node` 规划动作
  - 结构化节点定位 / 操作优先 `/accessibility/node`
  - 点击 / 滑动优先 `/input/click`、`/input/swipe`、`/input/scroll_bezier`
  - 输入优先 `/input/text`
  - 启动应用优先 `/activity/start`；需要首启授权时优先 `/activity/launch_app`
  - 浏览器 / 网页场景优先 `/activity/start_activity` 打开指定浏览器；浏览器包名优先 `mark.via`，没有再用 `com.android.chrome`
  - 安装优先 `/package/install_sync` 或 `/package/install_uri_sync`
  - 读取或修改 Settings 优先 `/system/settings_get`、`/system/settings_put`
- 每个关键动作后重新观察，不要做聚合式批量动作
- 没有专用接口时才考虑 `/system/shell`

## 必读参考

- 先看 `references/api-reference.md` 里的索引，再按模块只打开需要的 reference 文件
- 优先先用 `/base/list_action` 按需确认能力，再决定要不要展开更多接口细节
- 只有在需要精确路径、字段、示例请求时，才读取对应模块 reference
- 如果任务是“安装、下载并打开某个第三方应用”，再读取 `references/app-installation.md`
- 如果任务是“在云机浏览器里搜索、打开网页、提取网页内容”，再读取 `references/browser-search-and-reading.md`

## 安全边界

- 删除应用、清数据、系统设置、权限修改、shell 操作前先确认用户意图
- 没有明确要求时，不要改时区、语言、国家、Google 状态、设备信息、定位或传感器
