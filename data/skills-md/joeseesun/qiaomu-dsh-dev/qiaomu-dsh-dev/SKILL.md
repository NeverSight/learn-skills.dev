---
name: qiaomu-dsh-dev
description: |
  Develop, scaffold, debug, review, test, install and publish persistent DeepSeek Harness (DSH) Cordis plugins and bundles end to end. Use for Host services/tools, Client slots/panels, Remote bridges, native conversations, plugin data, profile integration, build failures, host upgrades and compatibility matrices, UI regressions, live-host verification, GitHub releases, illustrated bilingual plugin README, packaged artifacts and marketplace submissions. Includes standalone doctor, scaffold, artifact audit, installed-file comparison and public-download verification; no other skill installation required. Check the installed Harness version and current API. Exclude Obsidian-only plugins, generic web apps, one-off DSH usage questions, ephemeral Cordis Run packages and skill authoring.
metadata:
  author: 向阳乔木
  version: "0.3.0"
---

# 乔木 DSH 插件开发

面向**持久化、可安装的 DSH 插件**。目标是把用户动作从源码一直验证到实际运行的宿主；注册成功、构建成功、界面可见、功能可用和公开可安装是不同证据。

用户指令与项目 `AGENTS.md` 优先。只读诊断保持只读。开发请求完成实现与测试；发布授权可来自当前请求或该用户已授权的长期偏好，不重复索取。无发布授权时完成本地发布准备。保护当前 profile、用户数据和其他插件，优先独立测试 profile；其他聊天正在操作宿主时协调重载，独立环境继续工作。不要把历史路径或版本当成当前 API。本包内参考、脚本和模板足够完成流程，不要求另装开发、设计或发布 skill。

## DSH 的设计判断

先读 [设计理念与稳定扩展点](references/design-philosophy.md)。一切皆插件意味着配置组合、服务接口和可撤销 effect；session log 是模型上下文的事实来源；共享能力留在 Host，单 Agent 注册归其 context。插件复用宿主调度和增量投影，避免另建循环、轮询或扫全量事件。UI 动作和工具共用 Host operation，授权/审批行为保持用户专属。

## 路由

1. 确认仓库、分支、改动、目标 DSH 版本、运行 profile、已安装包与实际入口；保留用户已有改动。按用户结果选择 **host**（工具、文件、网络、持久化）、**client**（slot、页面、交互）或双端。纯 host 不创建 client。
2. 先查当前版本的官方文档、已安装包 `exports`/类型/源码和可用的 `cordis_inspect`；只读审查不改 profile。按需读 [架构与契约](references/architecture.md)。当官方当前契约与本技能案例冲突时，以目标运行版本为准。
3. 画出最短用户路径：动作 → 入口/slot/工具 → 所需服务与 `inject` → Remote/Host 副作用 → 状态/错误反馈 → 卸载/恢复。明确谁持有数据、谁清理资源、缺服务时如何退化。
4. 在现有架构内最小修改。新增文案同时进入语言字典；输入、菜单、快捷操作要保留键盘、焦点、草稿与失败恢复。AI 伴读、外部内容和写入按 [数据与界面](references/data-and-ui.md) 验证。
5. 跑项目已有 lint/typecheck/test/build，再核对构建产物、`exports`、`files`、bundle patch 与 profile 组合。安装/更新到**明确的测试 profile**，重载/重启后走真实用户路径；按 [验证与发布](references/verification.md) 记录每层证据。
6. 宿主升级、版本拒装或跨产品兼容维护时，读 [宿主升级与兼容演进](references/host-compatibility.md)：公开包与候选源码分别检查，按需调用固定版本 health CLI，再验证真实工具与 UI。
7. 若是故障，先复现并定位哪一层失效，修复后复测原场景和一个邻近场景。按需读 [四个乔木项目案例](references/cases.md)，其中记录的是样本经验而非框架保证。

8. 发布准备、Topics 或市场投稿时，读 [分发与市场提交](references/distribution-and-marketplaces.md)。先证明独立安装，再报告公开发布；目录投稿、审核、可见、安装是不同阶段。

## 可直接执行的工具与配方

所有命令从本 skill 的目录执行，`python3` 需 3.9+，不依赖第三方 Python 包。路径换成实际值；doctor 只读，init 只创建不存在的目标，不安装依赖或改 profile。

```bash
python3 scripts/dsh_dev.py doctor --repo /path/to/plugin --dsh /path/to/dsh
python3 scripts/dsh_dev.py init /path/to/new-plugin --name qiaomu-demo-dsh
python3 scripts/dsh_dev.py audit /path/to/package.tgz
python3 scripts/dsh_dev.py compare-install /path/to/package.tgz --installed /path/to/profile/node_modules/plugin-name
python3 scripts/dsh_dev.py verify-download --url https://example.com/package.tgz --sha256 EXPECTED_HASH
python3 -m unittest discover -s tests -v
```

脚手架是无需依赖的 Host-only 起点，不声称实现业务功能。新增工具、双端 UI、MCP、原生伴读按 [开发配方](references/implementation-recipes.md) 完成；参数、slot 和 externals 均先核实。API 不可查时暂停依赖该契约的实现，继续包审计、测试或文档准备。

发布按 [自包含发布流程](references/release-runbook.md) 执行；用 [插件 README 模板](templates/PLUGIN_README.md) 和 [图文 README 标准](references/illustrated-readme.md) 写用户能安装和使用的产品页。打包审计不能证明 YAML 语义或宿主运行，必须真实安装和启动。

## 关键判断

- Cordis `inject` 是运行依赖；`dsh.client.inject` 是包元数据，二者用途不同。不能因为 host 工具已注册，就认定 client 的 `remote.*`、slot 或面板可用。
- 客户端构建形式由**当前目标宿主**决定。最近乔木项目使用 `window.__ModuleLoader__.load({ id, factory(require) })` 的 CJS 外壳；必须核实目标版本的加载器及可外部化模块，不能照搬旧清单或把浏览器代码打成裸 ESM。
- 新插件优先稳定 Slot + 当前主题 token + 自有控件。官方持久化插件指南不建议运行时导入内部 Harness Client 包；已有编译项目先查精确版本兼容，避免未经迁移验证直接删依赖。`dsh.client.inject` 不等于模块导入许可。
- 停用→重启用→重载配置后不得重复 listener/slot/style/media；Agent context 上的注册还要在插件自身 effect 中持有 disposer。Waterfall 保留未知决策字段并正确委托；不用新自定义 session event 偷存插件状态。
- 声明矩阵、真实宿主启动、工具调用和用户操作分层验收。`engines.dsh` 与 DSH peers 的优先级以目标宿主为准；不靠豁免或放宽范围替代源码适配。
- Bundle 是分发层，profile 是运行组合。核对安装副本与源码摘要、配置覆盖顺序、必需依赖和实际启动日志。修改源码不会自动更新 `file:` 安装副本或已加载模块。
- 只在真实运行面证明用户可见行为：图片、媒体、网络、原生会话、选文、导入导出都要测试成功、失败及状态恢复。自动化冒烟测试是前置证据。
- 公开发布分别核对 PR、CI、合并、Release/包、全新 profile 安装与实际界面；不得由前一层推断后一层。

## 输出合同

交付：触发条件与根因；改动文件及用户可见效果；测试命令与结果；源码/产物/profile/真实界面各层状态；数据迁移与回滚注意点；未覆盖版本/平台；PR、Release、公开下载、干净安装与市场的精确阶段。UI 任务附真实无隐私截图，注明 build/commit/运行来源；不能以示意图证明验收。按 [验收记录模板](templates/ACCEPTANCE.md) 留证。需要用户测试时给最短动作及可观察结果。

版权所有 (c) 向阳乔木 · [X](https://x.com/vista8) · [GitHub](https://github.com/joeseesun/)
