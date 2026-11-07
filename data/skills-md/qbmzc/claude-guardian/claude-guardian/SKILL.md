---
name: claude-guardian
description: 为 Claude 订阅准备、账号与客户端异常、代理和运行环境问题提供分阶段访谈、有限只读检查和离线修复计划。覆盖 macOS/Windows 本机及可选 VM/VPS 路线、清理规划；不承诺免封；也可直接用作 VPS、家宽、线路和封号经验的帖子与论坛搜索工具；默认CLI不自动联网或修改系统，可选宿主库须逐项授权并满足可信目标/运行时前提。
---

# Claude Guardian

**0.2.0 工作流增量版**：访谈、获准的本地元数据检查、离线分析、面板和修复计划。默认CLI不自动联网、付款、清理或配置修改；可选探测库及限定POSIX事务/恢复接口须符合各自可信宿主、精确范围和即时授权契约，不是默认执行权限。原生设备与完整场景仍有未验收项；计划或样本不等于修复完成。

## 开始方式

1. 优先由 **Codex** 编排。分别确认执行宿主与实际目标；云端 shell 的信息不能冒充用户 Mac 的结果。仅使用当前可用且获准的工具；没有结构化提问界面时使用短问句，不伪造按钮。
2. **默认用中文交流、提问、解释报告**，保留技术 ID/命令原文；用户明确选择其他语言时跟随。先复用已有事实，再补缺口。普通订阅准备的首个缺失业务问题是 **Q-J01：首次准备订阅、到期后重新订阅，还是当前已有订阅？** 随后询问 Mac/Windows 与用途。技术熟练度不代表付费状态；紧急事故优先。明确清理任务直接进入目标和保护范围，不要求购买问卷；已报告过去封禁而设备经历缺失时先问 Q-D01，不推定当前设备也有该经历。
3. 本机是默认建议，但要问用户接受本机、选择 VM/VPS，还是先比较。三者是独立方案，不是升级顺序。已明确的目标优先；拥有 VPS 不等于选择远程工作区。
4. 按需读取 [intake.md](references/intake.md)，使用稳定问题 ID 和 G1/G2/G3。**Q-C07 永久停用**，不得换名称恢复账号归属/控制权问题。首次订阅无实际冲突时跳过旧套餐/旧渠道题。
5. 每次工具操作前遵守 [contact-and-safety.md](references/contact-and-safety.md)。从 **PC0** 开始：不接触 Claude/Anthropic、不安装或运行客户端、不登录、不查看订阅页。公开文档、DNS、HEAD、`claude --version` 及委派 Claude 工具也不是例外。使用随包历史依据，待核验的现行事实明确标出。
6. 只在获准目标范围内使用已实现 CLI 检查（先查看 `scripts/guardian.py --help`）。缺依赖不静默安装；未支持的检查记为未知。内置功能未开放时，Agent继续调查实际环境；不得用临时命令绕过权限拒绝、PC0或既有执行门禁。独立Agent修复须按 [agent-remediation.md](references/agent-remediation.md) 取得具体动作许可并提供最小差异、备份与复测。
7. 交付具体问题、目标范围、证据、未知项、最小修复建议、保留项及下一步。`pass/fail/unknown/not_applicable/blocked/skipped` 只描述指定检查。盘点完成不等于 PC-G1 通过；离线测试不证明平台支持或网络隔离。

## 环境入口顺序（2026-10-19 用户确认更新）

先明确本轮任务和本机／VM／VPS 运行路线，再了解网络资源与配置状态，最后进入目标环境检测或修复。未选、比较、拒绝、撤回、冲突、陈旧路线只做访谈和解释，不启动目标检查；本机默认建议必须得到明确接受。拥有 VPS 不等于选择 VPS，作为出口的 VPS 不会把本机运行路线变成 VPS。

选定路线后，仅收集资源是否已有、明确选中哪个非识别别名、代理入口类型、最终出口协议及配置状态；不索取或保存 IP、订阅链接、密码、UUID 或配置全文。HTTP/mixed 本地入口和 SOCKS5 最终出口是不同层；Claude Code 不直接使用 SOCKS 入口。配置已导入不等于已经生效，可经独立授权探测核验。

本机与 VM 做适用的详细检查，VM 宿主和客机分别绑定；VPS 路线是开发机，指引见 [vps-guidance.md](references/vps-guidance.md)；本阶段只做基础非侵入检查；用户给出 VM／VPS 访问方式后，Agent 可按分级授权部署，买服务器、付款、注册、登录由用户本人完成。选定路线但没有代理资源、不清楚资源或选择直连，仍可在具体目标和原授权下做离线预检，不要求先购买。

调用 `scripts/environment_entry.py` 的 `assess_entry` / `require_entry` 严格校验当前投影，再走原有目标、PC0、权限及逐动作授权门。入口资格不是许可或原生绑定证据，不把保存的报告恢复成许可。CLI 的 `--entry-file` 只读取明确提供的有界本地投影，Windows 此文件适配尚未开放；可信宿主可传已校验的字典。路线／资源改变必须使旧适用性和计划失效，不能复用旧检查结论。既有精确恢复义务仍按原回执、目标、保护和本次批准处理，不被新问卷阻断。

## 同一电脑默认统一代理路径，可明确指定分流例外

**2026-10-19 用户确认更新，优先于旧 target-only 默认：** 网络准备／修复默认要求同一目标电脑的所有普通应用、子进程和后台服务的公网 TCP／UDP／DNS 经同一指定代理路径／出口，普通应用到目标采用 `IPv4_ONLY`，禁止 IPv6 fallback；代理失效不得直连或切换未经批准的出口。不是只保护 Claude，也不能因某软件忽略系统代理就排除它。原 `PRODUCT-IPV4-20261018`、设计快照和历史验收保留原义，不改写为整机已实现。

配置前必须先告知将如何接管整机流量，例如 TUN，以及对其他应用、LAN／VPN、DNS和控制连接的影响、明确例外、备份与独立恢复方案，取得具体批准后才执行。TUN 不等于 Clash 的 global 模式，也不天然提供故障防直连；代理上游外层的地址族与必要引导／本地例外须逐项说明，不能自动沿用旧外层 IPv6 例外或直接关闭整机 IPv6。

用户明确要求某软件／进程独立路径时，核实精确范围、路径、协议／地址族和失败行为，作为明确例外分别配置与验收；也可明确选择仅 Claude 的窄范围模式。存在例外就不能仍称全软件同一路径。完整默认、例外、能力与证据边界以 [Agent 整机路径要求](references/agent-remediation.md#ipv4-only-policy) 为准；[网络参考](references/network-and-remedies.md)的旧目标范围方法仅用于相应窄范围方案或局部诊断。

现有 `traffic_policy`、CLI、访谈评估和面板仍输出旧目标范围契约，不代表整机合规；不能改返回字段假装升级能力。规则声明、应用载入、进程采用和端到端观察分别报告；同一代理链不保证同一公网 IP，样本一致只支持测量范围。整机强制覆盖或持续保护未建立时如实标 unknown／unsupported／未建立，不能 pass，G2或单次curl成功也不能代证。PC0、具体动作许可、取消、拒绝及事故优先级保持不变，不给无关任务强加网络修改。

## 完整访谈入口

完整状态化访谈使用 `scripts/interview_cli.py`：默认仅输出下一题和阶段评估；已确认答案通过本地 answer JSON 传入；用户明确要求保存时才指定 `--output`。普通读档或连续轮次用 `--input`；真正中断后继续须加 `--resume <本次事件别名>`，按 [intake.md 的续接规则](references/intake.md#interruption-and-resume) 先核实相关变化，再规划。问题 ID 按条件调度，Q-C07 始终停用。`guardian.py interview` 保留为兼容的简化入口，不把它的八字段流程当作完整访谈。

由 Agent 编排检测、解释、选择内置动作、具体确认、执行和复测，详见 [agent-remediation.md](references/agent-remediation.md)。`scripts/agent_remediation.py select --input <本地报告.json> --target-ref <目标别名>` 生成结构化动作清单；只读脚本、候选、宿主库和 Agent 环境修复分开，不执行清单或从JSON恢复权限。当前尚无开放的内置生产配置写入适配器；内置脚本修不了时，由 Agent 继续检查实际环境，使用具体获准的宿主工具或经审阅的限定临时脚本完成独立最小修复、备份恢复和复测。内置门禁仍不能绕过；选择器本身不是已完成修复。不能自行提供一个返回 True 的授权回调代替用户确认。

## Agent内部修复入口（按动作能力分流）

已核实目标使用2.5.8且选定独占rules扩展时，可用 [Agent 应用编辑任务](references/agent-rules-task.md) 生成单个DOMAIN变更的私有候选和供给内容核验。实际保存／重载由Agent通过受支持应用界面执行，须具体许可；该辅助接口不执行写入或证明实际网络效果。

`scripts/repair_cli.py`提供精确文件的`preflight / plan / diff / execute`接口。`plan`显式指定`--plan-file`和`--backup-directory`才写入新的私有计划文件，不修改目标；`--private-review`可在获准的私有Agent会话中非交互展示选定规则及policy前后差异，不输出无关配置。私有差异不得混入公开报告。

已确认交互是Agent展示具体改动、目标、影响、备份及恢复路径，用户在对话确认后，由可信宿主核对该次授权并调用固定内部脚本；不要求第二次终端确认码。宿主将确切`retained_plan_digest`、目标与备份范围绑定到本次操作；摘要只是完整性检查，不是授权。不能用JSON布尔值、任意回调、临时shell改写或终端模拟绕过权限。

`scripts/repair_execution.py`保留计划有效期、请求摘要、原文件身份和内容、候选一致性复核、事务备份及读回链路；生产原生适配门禁只开放一个固定范围：macOS 上 Clash Verge Rev 2.5.8 的 `rules-prepend` 扩展（`native_clash_verge_mac.py`，要求应用及其核心已退出，写入前后复查，检测到变化即失败；macOS 无强制文件锁，这是发现并失败，不是阻止）。其他系统、产品、版本和 `merge-policy` 仍返回`NATIVE_REPAIR_ADAPTER_UNAVAILABLE`，不得宣称实际修复完成。该适配器只有合成和 CI 测试，未在真实 Mac 上验收；写入后的应用重载和实际路由仍是单独步骤。Linux临时夹具中替换适配器的测试不开放用户Mac/Windows能力。恢复仍遵循独立`recovery_cli.py`契约，不自动覆盖后续改动。

`scripts/clash_verge_258.py`只校验调用方提供的2.5.8应用plist、配置索引和扩展字节之间的声明一致性：current→活动profile→显式option.merge或option.rules→唯一同类型扩展及basename。拒绝跨profile共享扩展、全局默认UID及路径/文件别名歧义。该库不读取真实文件，不证明实际安装/运行归属；输出始终为supplied_metadata_only。merge的rules数组替换基础数组，不能将rules扩展的prepend/append/delete混当此格式；脚本/后续链、内核版本、真实写入者排除和验收仍阻塞，不能以该结果开启execute。

`--candidate-kind rules-prepend`提供独立的rules扩展候选：必须显式给出`--base-path`、`--app-info`、`--profile-index`及`--extension-uid`，经安全读取核对所提供的2.5.8声明链和当前基础profile路径。只向现有空`prepend: []`插入用户明确排序的DOMAIN/DOMAIN-SUFFIX规则；`delete`必须为空，`append`与其他字节保持不变。拒绝已知受保护规则冲突，不把调用方声明的控制路径或优先级当作验证。私有差异包含已知优先级影响；未知链和原生执行继续阻塞。

保留计划格式为`guardian-retained-repair/0.3`，绑定当前环境入口摘要、候选类型、UID和基础配置/plist/索引的精确路径、父目录及文件快照。执行参数必须一致，提交前与读回后复核；旧0.1/0.2计划必须重建并重新展示确认。完整输入格式及命令见仓库`docs/rules-extension-plan.md`。不得用此入口初始化空merge、替换完整rules数组或绕过xattr限制。

## 限定静态盘点入口

`scripts/inventory_cli.py capabilities` 查看实际开放范围；`workflow-status` 仅显示新建且关闭的门禁。`static-audit` 只读取用户明确列出的本地配置，要求新的精确范围终端确认，拒绝保存的授权字段；目标身份/本地文件性质仍需可信宿主核实，终端输入不能代替宿主或操作系统权限。缺少可选PyYAML时停止，不自动安装。静态声明不代表运行时路由。Windows安全静态读取、控制器原生绑定、系统改写与自动恢复未开放。

控制器盘点与Windows只读计划是供可信宿主集成的库，不能绕过尚缺的原生身份/权限适配。workflow_guard提供即时资格判定，不是进程隔离或可持久化执行授权。

`scripts/remedy_plans.py` 提供四种方向的离线语义计划：保留现状、显式代理规则、TUN规则、限定兼容处理。它不生成可执行配置补丁，不开放apply；需要可信宿主提供私有快照绑定和公开别名。现有inventory CLI不能直接提供全部输入。结果中的DNS图、协议、控制路径和规则范围只依据投影事实；缺失或冲突保持阻塞，不推导已修复。

Windows监听者核对库 `scripts/windows_listener_binding.py` 仅供可信宿主显式集成：核对限定回环端口的PID、创建时间和同用户关系，不发控制器请求；为此会在私有内存读取有界监听表再筛选，必须向用户披露并获准。命名空间仍为宿主断言，不能据此声称独立原生核实或完整应用实例绑定。

网络库收到429时只报告有界Retry-After提示，不自动等待或重试。日期提示需要可信的响应接收时钟；未知、无效或过长值保持未知。

独立STUN库 `scripts/stun_probe.py` 仅在可信宿主提供当前精确范围授权、目标和取消检查后使用。没有CLI或自动触发，名称到固定数值地址的绑定由宿主另行核验；本模块不解析DNS。Cloudflare候选选择不等于任何一次公网执行授权，映射响应不认证提供方，也不证明浏览器或Claude路径。

POSIX独立恢复入口为 `scripts/recovery_cli.py`，须与 `transactions.py` 预先保留在可信本地位置。inspect只读用户选定回执；preview/rollback仍只接纳已应用回执。reconcile须绑定独立确认的目标、备份批次与回执摘要，只读观察选定记录；仅v2 prepared的候选匹配状态可用restore-prepared另行恢复，并要求上次私有观察的完整摘要、实际排除其他写入者及真实终端逐阶段新确认。旧prepared或冲突状态不写入，不重放apply；摘要和回执不是授权，Windows不支持。Agent宿主的对应调用及失败处理见 [agent-remediation.md](references/agent-remediation.md#prepared-recovery)。仅验证精确文件字节，不代表应用/网络效果已恢复；生产原生修复门禁不因此开放。

单轮多个已明确事实可通过 `--answer-file` 的 `{"answers":[...]}` 批量提交；每项沿用 `question_id/value/state/source` 格式，旧单项格式仍支持。宿主负责从自然语言提取事实，CLI不做自由文本解析或猜测未给出的套餐。整批验证失败不保存部分状态；重复/别名冲突、订阅阶段与老用户任务矛盾须澄清。当前本机默认建议可用Q-C05值 `accepted_default` 接受，不再重复确认路线；不会覆盖已选VM/VPS，也不构成动作或保存许可。

历史紧凑访谈迁移由 `scripts/interview_migration.py` 的纯宿主接口完成，不自动替换CLI续接。仅识别明确旧schema，按命名字段复用事实为过期证据；旧Q-C07/旧Q-C08和权限不继承。需要新的目标/账号别名及事实复核；旧账号停用提示须先确认是否仍需处理，不能凭旧设备历史认定当前账号停用。

## 首问示例

“这次先在 Codex 中做环境准备。你是第一次准备订阅、以前订阅过现在准备重订，还是目前已有订阅来处理问题？”

已回答就跳过。后续每轮一个主要决策，必要时合并少量同主题事实；不要整页展示问题库。报告摘要使用“已确认／尚未核实／建议下一步”，不报虚假的完成百分比。

## 来源原文阅读

**资料随答附带（2026-10-21 所有者要求，ADR-011）：** 所有者提供的资料不能静默使用。凡回答涉及某主题，回答末尾必须附“参考资料”，给出对应本地文件链接并指出章节或 PDF 页码，不必等用户来问。按主题只附相关的几份，不一次塞入全部资料；完整对应表见 [来源资料库](references/source-library.md)：

| 回答主题 | 必附资料 |
| --- | --- |
| 支付、订阅渠道、礼品卡、虚拟卡、API 充值 | **第一项：[AI 所有支付方式汇总（核验版）](sources/S02-ai-payments.md)**，核心参考，Agent 可据此向用户推荐支付方式（规则见 accounts-and-payments.md 的 B1） |
| 账号阶段、IP、设备、注册与养号节奏 | [S03 经验 PDF](sources/S03-claude-experience.pdf)、[S04 指南](sources/S04-claude-guide.md)、[account-onboarding.md](references/account-onboarding.md) |
| 本地防护、代理、浏览器档案、WebRTC 检查 | [S05 本地防护](sources/S05-local-protection.md)；WebRTC 可用包内的[本地探测页](assets/webrtc-probe.html)（由 `scripts/serve_webrtc.py` 在本机回环临时提供，用户点击确认后才发起 STUN） |
| macOS 清理 | [S06 清理教程](sources/S06-macos-cleanup-sanitized.md) |
| 在用户的机器上做改动时的授权方式（路线选定后；A、B、C 档） | [authorization-tiers.md](references/authorization-tiers.md)（必附） |
| 手机端（注册、选择 Apple/Google 内购、仅手机） | [mobile-guidance.md](references/mobile-guidance.md)、[S03 经验 PDF 第 4 页](sources/S03-claude-experience.pdf)（必附） |
| VM 路线（客机系统、网卡、出口、防火墙脚本） | [vm-guidance.md](references/vm-guidance.md)、[egress-ip-options.md](references/egress-ip-options.md)（必附）、[VPS 推荐报告索引 R01](sources/vps-recommendations/INDEX.md)（出口选自建梯、要选 VPS 时）、[S07 IP 质量清单](sources/S07-vps-script-catalog.md)（检查出口 IP 时）、[VM 搭建脚本](assets/vm-killswitch/enable-guest-ssh.sh)（开客机 SSH）、[FlClash TUN 安装](assets/vm-killswitch/install-flclash-tun.sh)、[VM 防火墙脚本](assets/vm-killswitch/install-flclash-killswitch.sh)（Linux 客机，按这个顺序） |
| 本机路线：Clash（TUN）与防火墙（Windows 系统防火墙、Mac 用第三方 LuLu），提示词引导、无脚本 | [local-firewall-prompts.md](references/local-firewall-prompts.md)、[macOS DNS 经验](references/macos-dns-case-lessons.md)（Mac）、[S05 本地防护](sources/S05-local-protection.md) |
| Windows 本机：网卡 IPv6 旁路、出口泄漏 | [agent-remediation.md 的 Windows 网卡 IPv6 提示词](references/agent-remediation.md#windows-adapter-ipv6-hint)（只提示，用户同意后才由用户或经批准执行，不自动改网卡） |
| Windows 清理 Claude 本机数据（官方路径、分档、备份、隔离、还原；无内置宿主） | [windows-cleanup.md](references/windows-cleanup.md)（必附）、官方 [.claude 目录说明](https://code.claude.com/docs/en/claude-directory) |
| 整机统一出口：只走 IPv4、不走 IPv6（TUN、DNS、规则兜底、泄漏与故障演练；判定用 `scripts/egress_verifier.py`） | [whole-machine-ipv4.md](references/whole-machine-ipv4.md)（必附）、[agent-remediation.md 整机统一路径](references/agent-remediation.md#ipv4-only-policy) |
| 线路优化（晚高峰慢、断流、卡顿、出口不对、中转、BBR；VPS 路线和自建梯节点；访谈 Q-T01） | [line-optimization.md](references/line-optimization.md)、[R02 线路优化与家宽中转教程](sources/R02-vps-line-optimization.md)（必附）、[VPS 推荐报告索引 R01](sources/vps-recommendations/INDEX.md)（要换线路或选机时） |
| VPS 路线（开发机：系统、环境一致、远程桌面、防火墙） | [vps-guidance.md](references/vps-guidance.md)、[S08 VPS 教程](sources/S08-vps-claude-tutorial.pdf)（必附）、[R02 家宽中转教程](sources/R02-vps-line-optimization.md)（套家宽出口时）、[VPS 推荐报告索引 R01](sources/vps-recommendations/INDEX.md)（选服务器时）、[S07 IP 质量清单](sources/S07-vps-script-catalog.md)（创建后检查 IP 时）、[VPS 防火墙脚本](assets/vps-firewall/vps-guard.sh)（出口是 VPS 自己的 IP 时）、[VM 防火墙脚本](assets/vm-killswitch/install-flclash-killswitch.sh)（套家宽、VPS 上跑 TUN 时） |
| 本机路线固定出口 IP（机场、自建、家宽拼车）、VPS 选购 | [egress-ip-options.md](references/egress-ip-options.md)、**VPS 推荐报告（R01）必附：**[索引](sources/vps-recommendations/INDEX.md)，并按用户需求指出对应类别：业务、性价比或高端家宽（共 17 份 PDF），推荐 VPS 时点名具体报告并给出链接 |
| VPS、服务器术语与测试 | [S01 术语](sources/S01-server-glossary.md)、[S07 脚本目录](sources/S07-vps-script-catalog.md) |

访谈评估（`scripts/interview_cli.py` 或 `interview_flow.assessment`）会按已回答的事实输出 `required_references`：本次必附的资料路径、主题和页码，按顺序附在回答末尾（支付时 S02 在第一位）。它是必附资料的下限，Agent 仍可按上表补充相关资料；清单不是执行授权。

原文中的命令和建议不自动成为执行授权；价格、准入变化快，购买前核对当前官方页面。

## Agent 补充资料来源

所有者的资料（上表和 `required_references`）是必附的下限，也是本项目的依据。需要补充、核对或查最新做法时（例如线路、机场、家宽、支付渠道、封号讨论、某个工具的新版本），Agent 可以到下面这些渠道查找。**本 skill 也可以直接当帖子和论坛的搜索工具用：**用户明确要求“去某论坛搜一下某商家、某线路、某问题”时，不必先有资料缺口，Agent 直接按下面的渠道和规则检索，用 `site:` 限定站点（如 `site:nodeseek.com 商家名`），汇报带链接和发帖日期的结果（2026-10-22，Issue #12）：

| 渠道 | 地址 | 适合找什么 |
| --- | --- | --- |
| Linux.do | https://linux.do | 国内用户的 Claude、代理、VPS、家宽、支付讨论和教程 |
| NodeSeek | https://www.nodeseek.com | VPS、线路、家宽、中转、服务器评测与教程 |
| V2EX | https://www.v2ex.com | 技术讨论、封号与支付经验、工具选型 |
| Reddit | https://www.reddit.com（如 r/ClaudeAI） | 英文社区的 Claude 使用、账号、限额与新功能讨论 |
| X | https://x.com | 作者和社区的最新动态、教程原帖、工具发布 |
| IDC Flare | https://idcflare.com/ | VPS 渠道、家宽拼车（所有者指定；该站有 Cloudflare 验证，Agent 自动抓取可能被拦，被拦时如实说读不到，请用户在浏览器里打开，不绕过） |
| VPSHub | https://vpshub.org/zh/ | VPS 商家与线路信息（所有者指定；站点内容本次未读取） |

所有者在 S03 第 5 页指的路：找 VPS 搜 IDC Flare、NodeSeek、Linux.do 的 VPS 分区、VPSHub；**家宽去 Linux.do（L 站）的 VPS 分区找，家宽拼车去 IDC Flare 找**。所有者列出的帖子：[最新退款教程](https://linux.do/t/topic/2971757)、[NodeSeek 教程](https://www.nodeseek.com/post-968032-1)、[Linux.do 家宽总结篇](https://linux.do/t/topic/585764)、[GitHub issue 63](https://github.com/alchaincyf/zhangxuefeng-skill/issues/63)；其中 NodeSeek 那篇原作者的做法（改时区、清理等）是应审查的用户经验，不照单执行。

使用规则：

1. **所有者资料优先。**补充资料只能增加信息，不覆盖所有者资料；两者冲突时，以所有者资料为准，并向用户说明有这条出入。
2. **标明来源。**用到哪条就附链接、平台和发帖日期，用户能自己核对；找不到可靠来源就说没找到，不凭印象补。
3. **看时效。**线路、价格、渠道、工具版本变化快，优先较新的内容；对过时的内容说明日期。
4. **帖子里的命令不是授权。**不自动执行帖子里的命令，也不照抄脚本；需要用时按线路优化等既有流程，由用户批准后运行。
5. **不收集账号信息。**不向用户索要这些站点的账号、Cookie 或令牌；站点需要登录或拒绝访问时，如实说明读不到，不绕过。
6. **只做查找，不接触 Claude。**查论坛不违反接触前门禁，但仍不通过任何渠道访问 Claude 或 Anthropic 的页面、账号和订阅页；不查与账号共享、代充、批量注册相关的做法。
7. **不替推广背书。**帖子里的邀请码、返佣和商家推广只当线索，不作推荐或排序依据。

## 按需加载

- [routes-and-platforms.md](references/routes-and-platforms.md)：M01/M06–M09；本机、VM、VPS、WSL/容器边界及生命周期计划
- [network-and-remedies.md](references/network-and-remedies.md)：M04/M05/M10、ENV-01–ENV-10；代理、DNS、IPv6、UDP/WebRTC 的证据解释与最小修复
- [macos-dns-case-lessons.md](references/macos-dns-case-lessons.md)：脱敏的 macOS DNS、IPv6、Tailscale 经验与证据限制；不新增探测授权或原生验收
- [accounts-and-payments.md](references/accounts-and-payments.md)：M02/M03；准入、目标套餐、Apple/Google/银行卡前提及支付交接
- [incidents-and-integrations.md](references/incidents-and-integrations.md)：M07/M10–M13；异常、清理保留、申诉、SDK/MCP 与认证边界
- [evidence-policy.md](references/evidence-policy.md)：M14；稳定来源 ID、历史证据限制和发布规则

参考资料采用中英双语结构，英文技术细则供执行者阅读，不直接把整份参考文件作为中文用户的操作答复。

## 授权档位

所有者确认：用户不需要每一步都在现场，只在重要的点在场。授权按风险分三档，见 [authorization-tiers.md](references/authorization-tiers.md)：**A** 范围内自行做（只读诊断、查资料、出方案、预演），范围确认后不再问；**B** 整个计划批准一次（可自行撤销、不切断访问、不涉及账号钱和凭据的改动），Agent 可在计划范围内按环境调整参数；**C** 必须当场确认（可能锁死自己、账号和钱、凭据、删除和不可逆、组织管理的设备、接触 Claude）。到 C 档 Agent 暂停并写确认单，用户可稍后回复，沉默不是授权。范围确认、计划批准和确认单会写进访谈状态的 `authorization` 段，来源必须是用户的明确回复，换路线或会话恢复后失效（见 authorization-tiers.md 的“状态机里的可追溯记录”）。本文和各 reference 里的“逐项授权／具体授权”按此档位理解；硬规则（PC0、付款本人、不收集凭据、宿主策略优先）不变。

## 始终保护

不收集秘密，不输出原始环境变量、配置或完整日志。使用别名和必要字段；保存进度前取得同意，不默认写入公开仓库。保护项目、未提交修改、CLI、历史、skills/hooks/plugins、自定义配置与 Codex 控制通道。

不编造免封概率、IP 纯净度门槛、退款保证或身份/设备/时区伪装收益。注册与养号节奏（邮箱选择、Free→Pro→Max 间隔、额度使用、教育邮箱、KYC 原因）按 [account-onboarding.md](references/account-onboarding.md) 提供，不承诺免封或免 KYC。出口位置不代表服务资格。不提供欺诈支付、伪造身份、轮换账号或绕过额度的流程；不因旧设备经历断言设备已被拉黑。

## 本地环境状态面板

使用 `scripts/status_dashboard.py --input <已授权的本地报告.json> --output <新HTML路径>` 可将 `guardian-report/0.1` 或 `env-inventory/0.2` 投影为离线HTML。由用户自行打开，不启动后台或联网。显示系统、代理、TUN、IPv4/IPv6、DNS配置与泄露、UDP、独立STUN、浏览器/WebRTC、故障防直连及授权状态。现有报告缺少的网络检测证据明确为未执行，采集完成不等于验证通过。仅展示白名单事实和逐字段时效，隐藏地址、路径、身份与秘密。页面是生成时快照，不随浏览时间刷新；分享前仍需核对。该入口不授权任何新的采集或探测。


### DNS 库与离线样本

`scripts/dns_probe.py` 仅生成/解析有界 A/AAAA 消息，无网络传输或 CLI。
`scripts/mihomo_dns_probe.py` 为可选宿主库：每次要求可信宿主核实控制器绑定、精确名称/类型/单请求范围与新的探测授权，才能查询其数值回环端点。该请求可能让控制器联系上游解析器并披露查询名称；配置只读授权不能替代网络探测同意。无扫描、凭据、重试、备用路径、缓存清理或配置写入；认证要求交接，不能禁用认证绕过。没有原生绑定/授权 UI 集成，不自动执行。

面板的 `--probes <已授权本地证据附件.json>` 可导入 HTTPS/STUN 及 Mihomo DNS 白名单摘要；只读本地输入，不触发上述库。输入来源、目标及时间声明仍不可信，样本不会变成操作许可、verified 或 workflow_guard 通过。Mihomo 查询不证明系统/浏览器 DNS 路径、上游实际发包、DNS 无泄露或完整 ENV-04 验收。


### 系统 DNS 样本库

`scripts/os_dns_probe.py`（macOS getaddrinfo）和 `scripts/windows_dns_probe.py`（Windows Resolve-DnsName -DnsOnly）是独立宿主库，无 CLI 或自动执行。每次须由可信宿主核实当前设备/用户/命名空间、绝对运行时及依赖来源，并取得精确中性名称、A 或 AAAA 类型、预算和可能上游披露的授权。不同类型分别授权，不指定新服务器、不清缓存、不安装运行时。PC0 门禁保持关闭。

系统调用置于受控子进程，预算、取消、输出上限与终止/回收均检查；进程创建、宿主回调及异常 OS 状态不保证硬实时界限。已发出的请求不能撤回。离线面板保留来源、地址族和计数等有限样本；缓存/hosts、真实解析器及路径仍未知，不推断 RCODE、DNS 无泄露或浏览器采用情况。没有原生绑定证明或真实设备 DNS 验收，导入 JSON 不构成权限。


### 窄范围上下文与终端会话

`scripts/native_context.py` 与 `scripts/windows_native_context.py` 为独立当前进程/控制台观察库。短时句柄只在原进程重查，不序列化、不构成设备归属、命名空间或完整运行时证明；读取本身仍需真实宿主授权。

在已独立确认可信的目标 Mac 或 Windows 主机，`scripts/diagnostic_session.py --target-ref <目标别名>` 提供终端元数据流程：显示精确范围，30秒内输入新随机 nonce 确认；无 `--yes`、导入授权、DNS选项、自动浏览器或默认保存。可选 `--dashboard-output <明确批准的新本地文件>` 仅保存新文件，须先核实目录本地/已水合；不覆盖旧文件；取消或拒绝会话不创建报告文件。

Mac严格上下文仅因 `RUNTIME_PATH_INVALID` 阻塞时，会话可在原剩余期限内返回无句柄的部分元数据；路径错误保持可见，不继续DNS、宿主核验或查询授权。独立元数据API不产生可恢复权限；完整严格上下文与可信宿主集成仍未验收。

路径失败的 `runtime_path_diagnostic` 只含固定 `path_field/path_reason` 枚举，可区分executable/cwd/prefix/base_prefix与symlink/类型/语法等原因；不含路径、不跟随链接，严格capture仍阻塞。`check` 的Mac S04仅表示采集进程视图，不确认硬件或Rosetta。面板可展示已有Mac默认代理开关摘要，scoped详情与真实路径仍未知。这些观察不能代替可信宿主或操作授权；测试与原生证据须分开看。

可调用 DNS 会话必须额外提供真正的宿主绑定、运行时与中性端点核验实现，并为每个 A/AAAA 查询重新取得具体授权；独立CLI尚未实现这些前提，因此保持元数据范围。核验异常或否定、上下文复核和取消回调异常在会话内不可由后来成功重查解除；严格复核前后检查原60秒会话期限，不因延迟重新计时。后端按实际平台选择；Windows元数据仍保留控制台账户关系未知/绑定阻塞，Windows DNS会话未接入。Windows输出拒绝ADS/设备名等危险语法，但权限继承父目录ACL，0600不证明Windows隐私。所有结果保持PC0关闭；未经真实设备验收，不把测试成功等同于可安全执行探测。


### 私有配置候选（不可应用）

`scripts/config_edit_plan.py` 在内存中把原始语义修复请求与精确哈希绑定的已拥有扩展配置，编译为有限规则policy token修改候选。仅支持keep-existing中的特定已有DOMAIN/DOMAIN-SUFFIX三字段规则，保留其他字节并重新解析核对；不读写文件、无CLI、无apply、不触发事务。重复/歧义选择、无效域名标签、已能证明的前置MATCH/DOMAIN-SUFFIX覆盖、未知版本和无效修订被拒绝；局部检查不证明完整规则图或合并后首次命中。版本声明仍不等于兼容验收。候选私有材料含原文与精确差异，只能在获准私有本地审查，不上传或混入公开报告。所有原生适配、版本/归属、实际路由和动作授权阻塞保留，apply_supported始终false。


## 选定设备经历与完整本地数据清理

已有 `scripts/cleanup_transactions.py` 的受限 POSIX 隔离／恢复接口，可供 Agent 在独立核实实际目标、数据归属、应用停用与独占条件后调用。默认 CLI 和访谈 assessment 不执行清理；Windows、凭据、浏览器和应用卸载需要各自的适配与授权。

`Q-D01` 区分本次选定设备曾使用当前受限账号、历史受限账号、普通报错、仅其他设备经历、没有这类经历及未知／拒答。账号历史不等于设备历史，设备经历不等于当前账号受限；不推定硬件黑名单。切换目标、账号、路线或恢复任务时重新检查事实绑定。

用户明确要求完整清理时，记录 `Q-D02=full_claude_data_reset`，无需先证明存在封禁史。选定设备的已确认历史经历只触发审计／清理计划提议，不自动选 C5 或执行。当前事故先处理，保留必要证据。

macOS 上 C5 执行用 `scripts/native_cleanup_mac.py`：只处理可再生缓存/日志和桌面端持久数据，`~/.claude` 里的对话记录、历史、设置、skills、插件、凭据始终受保护（整个 `~/.claude` 不能当根）；Claude 已退出、不由 Claude Code 启动；先备份并校验内容；同意须由用户在真实终端输入 `CONFIRM <操作> <摘要前8位>`，Agent 不能代输；仍属 C 档，只有合成与 CI 测试。钥匙串退出登录、最小提示词模式（`CLAUDE_CODE_SIMPLE`）、用户指定的系统时区各有独立命令 `scripts/native_claude_state_mac.py`，同样终端确认；不提供设备标识（userID、machineID）轮换。Windows 见 [windows-cleanup.md](references/windows-cleanup.md)，没有内置宿主，按官方路径用 PowerShell 分步做。C5 可以逐项选择经核实属于 Claude 的本地历史、配置、skills/hooks/plugins/extensions 和 Desktop 数据。源码、未提交工作、Codex、其他应用、共享或归属不明对象仍受保护；保护清单与“全清”冲突时先解决冲突。凭据／浏览器站点数据／应用卸载分别出范围和确认。默认采用可恢复的私有隔离，不永久清除，不轮换设备身份，不承诺解封或解除关联。

实际 Agent 调用顺序与限制见 [清理、迁移与恢复](references/incidents-and-integrations.md#cleanup-migration-and-recovery-m13--env-09)。只显示 assessment 不代表清理已实现或完成；调用成功也只证明已验证范围内的文件结果。
