---
name: maafw-interface
description: 编写、修改与审查 MaaFramework interface.json（Project Interface V2）——任务入口声明、controller/resource 配置、GUI 选项接线（pipeline_override 与覆盖顺序）、preset 预设、pretask 启动前任务、agent 子进程配置、import 拆分与结构排错。Use when creating, editing, or reviewing an interface.json for a MaaFW project, adding user-facing options or presets, wiring pipeline_override, configuring pretask or agent child processes, splitting interface files via import, or diagnosing interface structure errors.
---

# MaaFW interface.json（PI V2）开发

interface.json 是项目对外的标准化声明：通用 GUI、打包分发、工具链都靠它认识项目。字段语义一律路由 [MaaLLMWiki](https://github.com/Windsland52/MaaLLMWiki) 的 3.3-ProjectInterfaceV2 协议与官方 schema（interface.schema.json），不凭记忆填（已安装 `maallmwiki` skill 时由其承载完整路由流程）。

本文只承载路由拿不到的三样：**选型决策**（什么时候用什么）、**静默失败面**（不报错但就是不生效的字段交互）、**流程与验证手法**。字段字典（枚举、默认值、字段清单）不在本文复制；文中版本标注均为"该机制自哪版起"的历史事实，不是当前版本快照。

版本双轨防混淆：`interface_version` 固定数字 `2`（JSON 结构主版本，兼容性新增不碰它）；PI 协议另有语义化版本 v2.x.y（独立于 MaaFW release 演进）——判断"目标 Client 支不支持某字段"看的是后者，协议当前到哪以原文变更表为准，不写死。

## 硬护栏

1. **对外契约**：字段改动 = 用户可见行为改动；软件更新走 `github` 字段的 release 约定（通用 UI 只更新资源 release），不自造更新通道。
2. **resource / Bundle 分层**（定义出自官方术语表 1.2-术语解释；3.3-ProjectInterfaceV2 协议行文的"资源包"指 resource 条目，不是 Bundle）：
    - **Bundle**：按 pipeline / model / image 标准结构存储的文件夹；`path[]` 的每个条目指向一个 Bundle 根目录（不是 `pipeline/` 子目录），按序加载、后者覆盖前者。
    - **resource 条目**：声明单位（name / label / option），用户在 Client 里选择的就是它。
    - controller / resource 声明**不能**经 import 合并——资源根永远由主 interface 声明。
3. **不编造字段**：枚举、默认值、版本支持拿不准就路由 schema 与协议原文，宁可少写用默认。
4. **i18n 完整性**：`$` 开头的键必须在 `languages` 指向的翻译文件里有对应键；不配 `languages` 默认仅中文。
5. **密钥卫生**：interface.json 随资源分发，明文密钥不得写入；`password` 输入字段禁 `default`（schema 硬拒）、不入 preset（协议建议，schema 不校验——靠纪律）。

## 工作流

从零编写按 1→7 顺序走；在既有项目上增改，先看下方「存量修改」。

1. **骨架**：`interface_version: 2` + `name` / `version`；adb 的截图/输入方式不配，框架自动探测选优。controller 两个决策（枚举与默认值路由 schema）：
    - **目标形态**（安卓设备 / 桌面窗口 / mac 应用 / 手柄…）定 type。
    - **截图缩放基准**（识别与坐标所在的分辨率空间：短边锁定 / 长边 / Expand / 原始分辨率）——是框架截图的缩放，不是游戏自身 UI 缩放；全不配默认 720 短边（`maafw-pipeline` 的基准分辨率取自这里）。
2. **资源差异怎么组织**四选一：
    - 让用户选 → 多 resource 条目（声明层）。
    - 同一 resource 内叠加 → `path[]` 里 base Bundle + 差异 Bundle，差异 Bundle 只放覆盖文件。
    - 差异绑定控制器 → `controller.attach_resource_path`（v2.2.0+）在该 resource 的 Bundle 全部加载后附加。
    - 整包只服务某控制器 → resource 条目的 `controller` 列表（按 name）——Client 只展示适用的 resource 供选。
    - 发布配 `hash` 校验（v2.6.0+）注意：值是**仅加载 `path` 里的 Bundle** 后算出的——打包脚本把 attach 的 Bundle 算进去会误报警告；不匹配只警告不阻断，调试/预发布版可跳过，未设置不校验。
3. **任务**：每个用户可见功能一个 task：
    - `entry` 写 pipeline **节点名**——interface 与 pipeline 的跨文件引用，不是文件名。
    - 功能多了用 `group`（v2.4.0+）分组。
    - task 级 `resource` / `controller` 过滤按 **name** 引用（不是 type）。
4. **选项与预设**：可调参数定义到顶层 `option` 再逐级引用；task 级 `pipeline_override`（写死在该 task、不经用户选择）与 option 的覆盖优先级见 options.md；`preset`（v2.3.0+）是任务勾选 + 选项值快照。控件选型、声明层级、覆盖顺序与静默坑见 [references/options.md](references/options.md)。
5. **子进程**——让 Client 替你启动程序，两个字段按**时机**选：
    - **任务执行期间常驻**、承接 Custom 识别/动作逻辑 → `agent`（Client 启动如 `python ./agent/main.py` 的子进程并与之通信；要不要上 Custom 见 `maafw-custom`）。
    - **连接设备之前跑一次性准备**（如拉起模拟器、环境自检）→ `pretask`（v2.7.0+，跑完才连 Controller，非零退出即中止启动）；可声明 controller / resource 过滤（v2.8.1+）——协议只约定 Client **可**隐藏/置灰不适用项，不保证跳过执行，"只在某控制器跑"要在程序内自判。
    - 两者 CWD 均为 interface.json 所在目录。
    - `pretask.option` 只把选项取值序列化成末参传给程序，**不参与 pipeline_override 合并**。
    - agent 子进程经 `PI_*` 环境变量（v2.5.0+）读 Client 侧上下文，变量可能缺省，子进程需容错。
6. **长尾字段**：`setting`（设置分区）、`telemetry`（遥测）等知道存在即可，用时路由原文。
7. **拆分与校验**：
    - 任务量大时 `import[]` 拆分（静默坑见 options.md）。
    - 静态校验跑脚本：带 dev-tools 的项目（create-maa-project 生成）跑 `pnpm check`——按官方 schema 校验 interface.json、`tasks/` 下的 import 片段与各 Bundle 的 pipeline 文件，字段拼错、类型与枚举值非法在这里被抓（放 `tasks/` 以外的 import 片段不在校验范围）；无此基建的项目退回编辑器挂 schema 关联。
    - option 分支逐一验证 override 落点（**override 按节点名定向，节点改名 = 静默失联**）。
    - 运行时验证（Client 能加载、任务能跑通、override 真的生效）超出本 skill——交接 `maafw-debug`。

## 存量修改

改名类操作先全库搜引用再动手——漏改的后果不一：option 键名漏改在参考实现里**interface 加载失败**（能抓住），其余多为静默失联：

- **改 pipeline 节点名**：`task.entry`、task 级与 option 的 `pipeline_override` 都按节点名定向，全部同步（pipeline 侧的其余引用清单见 `maafw-pipeline` 修改轨）。
- **改 option 键名 / case 名**：键名漏改 → 参考实现加载失败；case 名漏改 → preset 预设值静默落空。引用面：task / controller / resource / global_option 四级、`setting[].option`、`pretask[].option`、嵌套 case 的 `option[]`。
- **新增 import 文件**：先查主文件与既有拆分文件有无同名 option 键——同名以后导入文件为准，主文件被顶掉。

## 审查清单

- `interface_version` 是 2；每个 `task.entry` 在合并后的 pipeline 里可解析。
- option 引用键存在且逐字符一致——task 级悬空引用在参考实现里直接**加载失败**（不是静默），已存配置里的失效引用被警告后丢弃。
- option 适用当前 controller / resource——不适用时整个 option（含嵌套子项）**静默失效**（v2.3.1；"选项没生效"头号原因（经验值），机制见 options.md 适用性过滤）。
- 多级引用同一 option 按覆盖顺序推演最终值（task > controller > resource > global，后覆盖先）；checkbox 多 case 按定义顺序合并。
- `path[]` 每个条目都是 Bundle 根目录（不是 `pipeline/` 子目录）；import 无同名 option 键（同名以后导入为准）。
- `languages` 文件存在且 `$` 键全覆盖；password 无 default、不入 preset、全文无明文密钥。
- 用到的字段版本前提与目标 Client 的 PI 支持版本兼容，逐项路由核对——协议收录 ≠ schema / 参考实现 / 目标 Client 已支持，发布前实测。

## 深入阅读（按需）

- [references/options.md](references/options.md) — 控件选型判据、声明层级与覆盖顺序、过滤（v2.3.1）、preset 与 import 的静默坑

字段级细节、`PI_*` 变量表与版本变更一律路由 3.3-ProjectInterfaceV2 协议与官方 schema。
