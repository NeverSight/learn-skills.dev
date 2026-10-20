---
name: bytedcli
description: "Unified skill for the entire bytedcli command surface. Use when tasks involve ByteDance internal R&D platforms and the agent should prefer bytedcli through CLI, MCP, or bundled references instead of opening web pages or hand-writing internal API calls. Covers auth and tokens; Feishu/Lark and Cloud Docs/Ticket/Kani approval; FundEye / Fullink rule, diff, and alarm queries; Codebase, BAM, BITS, Devflow, BitsAI, SCM, AGW, Luban, Lynx, Overpass, Goofy, Fornax, Meego, AIME, Tika, Starling, and TikTok Gecko resource queries; Live IM Trace; TCE/TCC/Spark Platform/ENV/TOS/FaaS/Volcano/ByteCloud/Bytetree/Netlink/Neptune/Settings/Kross; RDS, ByteDoc, Merlin, Hive, Dorado, Aeolus, DataQ, TQS, ES, Cache, BMQ; Cronjob, Log, APM, Slardar Web/App/OS, Codecov, Archer; DKMS, KMS v2, IAM; internal knowledge insearch across Feishu/ByteCloud/BitsAI/ByteTech/intranet; ByteStable WCC; MCP server startup and global update flows."
---

# bytedcli

## 如何调用 bytedcli

先选择一种调用方式。下面所有示例默认直接写 `bytedcli`。

```bash
# 方式 1：直接用 npx 运行最新版
NPM_CONFIG_REGISTRY=http://bnpm.byted.org npx -y @bytedance-dev/bytedcli@latest <command> [options]

# 方式 2：先全局安装，再直接调用 bytedcli
NPM_CONFIG_REGISTRY=http://bnpm.byted.org npm install -g @bytedance-dev/bytedcli@latest
bytedcli <command> [options]
```

- 使用 `npx` 时，把后文示例里的 `bytedcli` 替换成 `NPM_CONFIG_REGISTRY=http://bnpm.byted.org npx -y @bytedance-dev/bytedcli@latest`
- 已全局安装时，直接按后文示例执行 `bytedcli ...`

这是 bytedcli 的统一入口说明。任务涉及字节内部研发平台时，先用它判断该走哪个命令域，再按需进入对应领域的详细说明。

## How to use

1. 先判断任务属于哪个平台或对象类型。
2. 先选对命令域，再调用对应的 bytedcli 命令。
3. 需要稳定机器可读输出时，默认加 `--json`，并把它放在 `<domain>` 前面。
4. 不确定命令名或参数时，先看 `--help`，不要猜。
5. 命令支持控制台 URL、文档 URL、仓库上下文自动推断时，优先直接使用这些输入。

## Quick start

```bash
bytedcli --help
bytedcli --json auth status
bytedcli <domain> --help
```

## Route by task

- 登录、状态、JWT、用户信息：`auth`
  - 例子：“帮我登录”“看当前账号”“拿 codebase jwt”
- 仓库、MR、Issue、Review、CI、文件、跨仓搜索：`codebase`
  - 例子：“看这个 MR”“给这个 MR 回复评论”“查这个仓库的 CI”
- 发布任务创建：`devflow`
  - 例子：“创建一个发布任务”“绑定 TCE/TCC 发布项和 Meego”
- Feishu / Lark 文档、评论、日历、待办、消息、表格、多维表格：`feishu`
  - 例子：“读这个 Lark 文档”“在文档里追加一段”“给某人发飞书消息”
- FundEye / Fullink 核对规则、diff、告警：`fundeye`
  - 例子：“查这个规则详情”“按 rule_id 看最近一天的 diff”“查某个 alarm_order_id 对应的 diff”
- Starling 文案平台、项目、空间、文案搜索：`starling`
  - 例子：“查这个 Starling 项目”“创建一个 Starling space”“搜索某个文案 key”
- Luban npm 包查询：`luban`
  - 例子：“查某个 TTP-US npm 包在 Luban 里有没有”“看某个包的 2.1.x 版本”
- Lynx 工具集合、LynxExample 产物元信息与下载：`lynx`
  - 例子：“查 LynxExample 产物”“下载 LynxExample Android 包”
- TikTok Gecko 控制台只读资源查询（工作台、App、Channel、Ticket、Host App、Deployment）：`tiktok-gecko`
  - 例子：“查 Gecko 某个 channel 的详情”“列出 deployment 下所有 channel”“筛选某个 creator 的 Gecko 工单”
- 技术文章、知识问答、AI 对话 / 附件 prompt：、`bitsai`、`tika`、`aime`
- 内部搜索（飞书文档、ByteCloud 文档、内网、ByteTech 文章、BitsAI 问答）：`insearch`
  - 例子："搜索 kitex ppe 环境""查飞书文档里有没有 BMQ 接入指南""用 BitsAI 问一下 TCC 怎么配置"
- SQL、数据库平台、数据资产、报表、离线任务：`rds`（子组：`db`/`slow`/`alert`/`ops`/`bpm`）、`bytedoc`、`hive`、`dorado`（子组：`project`/`task`/`instance`/`adhoc`）、`aeolus`、`dataq`、`tqs`
  - 例子：”查我关注的 ByteDoc 数据库””看这个库的慢查询””执行一段 SQL””查这个 dashboard 对应的数据集”
  - 在 hive-sql 上进行语法检查、提交 sql 任务、获取状态和结果：`tqs`
- OneService query 元信息、版本详情、SQL 提取：`oneservice`
  - 例子：“查这个 OneService query 的元信息”“按 queryId 拿当前 ONLINE 版本的 SQL”“按 versionId 看 query detail”
- Merlin job 提交和从中抽取 YAML 描述，Merlin job/trial 的 stdout/stderr 日志查询，Merlin tracking project、run、metrics 和 job 链接读取，`merlin` 计算资源 quota 的 group、cluster、trial、diagnose 只读查询：`merlin`
  - 例子：“提取这个 Merlin job 的 YAML”“把这份 `trial.yaml` 重提到 `seed-cn`”“看这个 Merlin tracking run 的 config/summary”“根据 job id 找 tracking 链接”“拉这个 Merlin trial 的 stdout/stderr”“查这个 trial 为什么还在排队”
- Fornax prompt workspace、prompt 草稿与版本、prompt 发布，以及 experiment 创建与结果查询：`fornax`
  - 例子：“列出这个 Fornax workspace 下的 prompts”“读取 prompt 个人草稿”“发布这个 prompt 到 ppe”“查询 experiment 第一页结果”“配置 Fornax experiment 的 AK/SK 或 JWT”
- Kani 权限审批：`kani`
  - 例子：“查 Kani request 页工单”“看 reviewer 视角的已完结审批”
- 配置中心、配置查询、新建、更新与发布：`tcc`（子组：`namespace`/`config`/`deployment`/`env`/`site`）、`bytestable`（子组：`wcc`）
  - 例子：”查 TCC namespace 下的配置””更新一个 TCC 配置并发布””在 WCC 里新建配置””更新 WCC 配置值””发起 WCC 配置工单”
- 部署、环境、服务树、域名治理、对象存储与云函数资源：`tce`、`env`（子组：`site`/`service`/`device`/`ticket`）、`bytetree`、`goofy`、`netlink`、`neptune`、`tos`、`faas`、`volcano`、`bytecloud`
  - 例子：”查服务实例””看发布单””更新配置””做一个 Goofy preview”
- Spark Platform 空间与链路资源：`spark-platform`
  - 例子：“列出 Spark space”“按业务线 bid 列 link”“某个 space 下的 link”“拿某个 link 的完整 raw（含所有 version 与原始 deployConfig）用 `link get`”“要最新已发布 version + 解析后的 schema（含 schemaUrl / bundle / bundlePath）用 `link summary`”“列某个 link 的 env 配置”“给 link 设置 PPE env，先 `--dry-run` 看 payload 再真实执行”“删除某个 env”“指定非默认 `--app-id`”
- Kross 多平台容器环境（workload）列表、创建、容器内远程执行与文件传输：`kross`
  - 例子：“先用 `kross workspace list` 看我有哪些 workspace，再用 `kross template list` 查这个 workspace 在当前 cluster 下可用模板，然后用 `kross workload list` 看这个 workspace 下已有 workload，最后直接创建 job workload；quick create 默认会带 1000m CPU / 2048 MB memory / 300 秒 timeout / 自动删除”“删除某个 workload”“通过 webshell 在 workload 容器里执行命令”“上传或下载 workload 容器文件”
- 日志、监控、告警、App/OS symbol、Redis / Kafka / RocketMQ：`log`、`apm`（子组：`service`/`redis`）、`slardar`（子组：`web`/`app`/`os`）、`cache`、`bmq`、`rmq`
  - 例子：”查这个 logid””看 Redis 大 key””分析这个告警页””用 Slardar App issue URL retrace native 栈””用 Slardar OS issue URL 解析主线程 native 栈””搜索 RocketMQ topic””查看 RocketMQ consumer group 列表”
- Libra / DataTester A/B 实验、指标组、指标组模版：`libra`
  - 例子：“看这个实验详情”“查这个 flight 的报告”“根据 template 页面 URL 查看 metric-group template”
- OneService 查询：`oneservice`
  - 例子：“查这个 query 的 meta”“查这个 query version detail”“取当前 ONLINE 版本 SQL”
- Life 生活服务生财有数平台：`life live-screen`
  - 例子：“根据直播间 ID 看直播数据工作台核心指标”“按主播昵称 / 主播 ID / 抖音号 / 直播间 ID 获取用户信息”
- Live Trace / 消息链路排查：`live trace`
  - 例子：“发起 ack_trace”“查这个 task_id 的明细”“解析这段 pb_payload”
- 跨区域数据交换：`decc`
  - 例子："创建 DECC channel""注册 DECC data""申请 channel 权限"
- 安全与权限：`dkms`、`kmsv2`、`iam`
  - 例子："查 data key 权限""给 key 加 ACL""搜一个员工"
- 将 bytedcli 暴露给宿主或升级本地安装：`mcp`、`self`

## Common inputs

- 如果用户给的是 MR / issue / 文档 / 配置 / 告警控制台 URL，优先直接用 URL，不要先手拆 ID。
- 如果任务是 Meego，优先直接使用工作项 / 视图 URL；很多命令支持 `--url` 自动回填 `project_key`、`work_item_id`、`view_id` 等标识。
- 如果用户给的是仓库目录上下文，优先让 Codebase 自动从当前 `origin` 推断仓库；当前支持 `code.byted.org` 和 `code-tx.byted.org` remote。如果推断失败，CLI 会继续说明是非 Git 仓库、缺少 `origin`、host 不支持，还是 remote 无法解析。
- 如果任务跨站点，先确认 `--site` 或 `BYTEDCLI_CLOUD_SITE`。
- 如果命令失败，优先看 `error.hint`、`error.auth_command`，或参考排障说明。

## Domain guides

任务已经收敛到某个具体领域时，继续看对应领域说明：

- Codebase: [references/subskills/bytedance-codebase/GUIDE.md](references/subskills/bytedance-codebase/GUIDE.md)
- Feishu: [references/subskills/bytedance-feishu/GUIDE.md](references/subskills/bytedance-feishu/GUIDE.md)
- FundEye: [references/subskills/bytedance-fundeye/GUIDE.md](references/subskills/bytedance-fundeye/GUIDE.md)
- Starling: [references/subskills/bytedance-starling/GUIDE.md](references/subskills/bytedance-starling/GUIDE.md)
- Luban: [references/subskills/bytedance-luban/GUIDE.md](references/subskills/bytedance-luban/GUIDE.md)
- Lynx: [references/subskills/bytedance-lynx/GUIDE.md](references/subskills/bytedance-lynx/GUIDE.md)
- TCC: [references/subskills/bytedance-tcc/GUIDE.md](references/subskills/bytedance-tcc/GUIDE.md)
- WCC: [references/subskills/bytedance-bytestable-wcc/GUIDE.md](references/subskills/bytedance-bytestable-wcc/GUIDE.md)
- TCE: [references/subskills/bytedance-tce/GUIDE.md](references/subskills/bytedance-tce/GUIDE.md)
- TQS: [bytedance-tqs/SKILL.md](bytedance-tqs/SKILL.md)
- Kross: [references/subskills/bytedance-kross/GUIDE.md](references/subskills/bytedance-kross/GUIDE.md)
- Bytetree: [references/subskills/bytedance-bytetree/GUIDE.md](references/subskills/bytedance-bytetree/GUIDE.md)
- RDS: [references/subskills/bytedance-rds/GUIDE.md](references/subskills/bytedance-rds/GUIDE.md)
- OneService: [references/subskills/bytedance-oneservice/GUIDE.md](references/subskills/bytedance-oneservice/GUIDE.md)
- Merlin: [references/subskills/bytedance-merlin/GUIDE.md](references/subskills/bytedance-merlin/GUIDE.md)
- Fornax: [references/subskills/bytedance-fornax/GUIDE.md](references/subskills/bytedance-fornax/GUIDE.md)
- Libra: [references/subskills/bytedance-libra/references/libra.md](references/subskills/bytedance-libra/references/libra.md)
- FaaS: [references/subskills/bytedance-faas/GUIDE.md](references/subskills/bytedance-faas/GUIDE.md)
- Log: [references/subskills/bytedance-log/GUIDE.md](references/subskills/bytedance-log/GUIDE.md)
- Archer: [references/subskills/bytedance-archer/GUIDE.md](references/subskills/bytedance-archer/GUIDE.md)
- Slardar: [references/subskills/bytedance-slardar/GUIDE.md](references/subskills/bytedance-slardar/GUIDE.md)
- Life: [references/subskills/bytedance-life/GUIDE.md](references/subskills/bytedance-life/GUIDE.md)
- Live Trace: [references/subskills/bytedance-live/GUIDE.md](references/subskills/bytedance-live/GUIDE.md)
- Search: [references/subskills/bytedance-insearch/GUIDE.md](references/subskills/bytedance-insearch/GUIDE.md)
- 其他领域路径索引: [references/subskills-index.md](references/subskills-index.md)

## References

- `references/command-surface.md`
- `references/invocation.md`
- `references/troubleshooting.md`
