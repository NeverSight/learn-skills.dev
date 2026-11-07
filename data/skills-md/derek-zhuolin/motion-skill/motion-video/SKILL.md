---
name: motion-video
description: 显式调用 Motion Skill / Motion video 时，优先继承已选影片的实际镜头与素材，制作连续品牌短片或原声解释视频；按需检查，不自动调用模型、上传或发布。
---

# Motion Skill · Motion video

公开测试版 **1.1.1-beta.1**，整合本地 `1.1.1-local.4`。旧公开示范片与版本保留。

## 默认入口：规范 → 编排清单 → 实现

只要本次要写或改 Remotion，先运行 `python3 scripts/motion.py preflight-remotion --project /absolute/project`，读取它定位的 **remotion-best-practices/SKILL.md**，再按任务读取具体分支。无需用户重复点名。只是找到文件不等于已读；记录实际读取路径、版本与 hash。缺失时按 `references/remotion-integration.md` 处理，不假称已调用、不静默联网安装。保留已可运行工程与内容准备工作。

动手前按 `references/semantic-orchestration.md` 给用户一张**简短镜头编排清单**：时间/本段意思、主焦点、主效果编号与名字、辅助效果、进出场和交接对象、选择原因、可读窗口。先说再做；这份清单不是新增逐镜审批。数字快照、数字变化、关键词层级、证据截图、主体运动的视频要分别判断。每镜一个主表达；效果数量随内容，不规定10或15组。

由当前 Agent 读内容和核对素材。对已覆盖的数字、关键词、真实素材等关系，填写 `assets/semantic-plan.example.json` 的结构，再运行 `select-motion plan.json --out selection.json --explain shot-plan.md`。这一步按语义与近期使用记录给适配候选，不能把同一套 AME 镜头顺序套到所有内容；相关性优先，变化不靠随机或硬凑。返回 planned 不代表已调用。实际导入 `production-registry.json` 中的组件后，记录 actual-used 清单并审查源代码与画面；没实现的研究保持 study_only。仅修改某一镜时只重选受影响镜头。新关系不必硬塞进这几类：可按 catalog 选研究并定制实现，在同一编排表中标 custom、来源编号和代码位置；用相关源码与实际画面验证，不冒称选择器或生产接线审计已通过。

## 先走最短的正确路径

读取项目 AGENTS、当前任务及用户选定的视觉基准。新 run 保留原件。本机已登记授权基准时运行 `python3 scripts/motion.py baselines`，有已选原片就使用 `reuse` 继承实际影片代码、字体和授权素材；**不要先用五类默认卡片模板重建它**。

- **连续 Launch**：沿用用户选定影片的视觉语言。让一个载体贯穿发现、选中、展开、协作；按语义选少量转折，保留阅读停顿。
- **原声解释**：沿用用户选定影片的字体、材质与节奏。同一视觉跨多句话，真实影像与示意关系分工；原声保持 1×，无视频不生成说话人脸。
- **修改/复盘**：直接读目标工程的相关镜头和时间表，不重跑转写、信源研究、模板生成或全研究库。
- **没有可用基准**：才用 `new` 建标注清楚的结构草稿，并按实际内容写镜头。默认五类 renderer 不是电影感模板，也不会自动调用研究适配器。

`reuse` 只复制本机已登记源，不执行源脚本，不联网、不转写、不渲染。新工程初始是 reference_copy，旧时间和旧口播属于旧片；换内容时更新语义事件、字幕和资产映射后才能称为新片。没有登记源时准确报缺失，不静默降级为卡片片。

```sh
python3 scripts/motion.py baselines
python3 scripts/motion.py reuse --baseline my-reference --dest /absolute/new-run --deps /absolute/existing-node_modules
# 基准需登记自己的授权工程；公开包不含作者私人基准。见 references/local-fastpatch.md。
```

## 语音：同一段只转写一次

先查已核对的项目 transcript 和 source hash；没有就查询缓存：

```sh
python3 scripts/transcript_cache.py get --media /absolute/audio
python3 scripts/transcript_cache.py put --media /absolute/audio --transcript /absolute/transcript.json  --engine existing-local-engine
```

缓存默认位于本 Skill 的 `.local/transcript-cache`，不进入分享包。命中只证明源与转写文件匹配，仍需检查语言、词时标、覆盖范围和专名；不自动把 verified 改为 true。只做短样片时优先处理选段及少量上下文，不默认整段转写两遍。复用现有可用本地引擎；启动前记录输入 hash、范围、引擎、预计时长和超时。已有转写任务仍在运行时不要并行开第二种实现；确需切换时先确认旧任务已退出，再只补缺失范围。不因尾部卡住重复跑完全部内容。本 Skill 不内置 ASR 模型或自动切换服务。

## 已选视觉保持，编排按内容调整

用户要求延续已选效果时，先锁定字体、字号角色、配色、布局密度、材质、阴影、素材裁切与组件外观。调整的是当前内容的机制选择、对象交接与运动路径，不把换风格当作工作流升级。抽取通用组件不能丢掉原片的细节（如数字滚轮边缘渐隐、运动模糊、分隔符尺度）；用参数继承这些视觉属性。无法对应时先报告差异，不静默换成默认皮肤。

合并或替换组件时，优先用同内容、同原声、同帧对照确认视觉变化。该检查只证明本次接入的范围，不能宣称所有片子自动保持同样审美。新内容仍需重新选择有意义的动效，不固定照搬已选片的镜头序列。

## 镜头与时间

先一个主焦点，再安排对象交接。保护正在读的对象，不冻结整幅画面；允许配角提前准备。转场必须解释深入、选择、联系、对比等语义，不能每句重开“标题＋中央卡片”。音频、文字、遮罩与机位共用命名事件；需要新的组合时才读 `references/motion-combinations.md`。继承好片的字体、材质、运动习惯与连续性；镜头结构按当前语义重选。复用轨道原件，不固定使用旧片的镜头顺序。先写两种简短构思及取舍，再实现更适合当前意思的一种；不同关系不要总用同一组合。

真实素材和原 Logo 保留身份与来源；Interflow 默认蓝 #0070DB、黑 #141414、白和灰，不自动改米白。粘土适度，禁止为了动效加无意义漂移。音乐和效果音按已有授权复用；没有音源就明确静音，不编造节拍识别或效果数据。

## 只检查本次改动，不绕回整座研究库

默认先交 15–20 秒、包含完整意思的真实内容样片。用户验收通过后才扩整片；明确要求其他片长或直接整片时，以该次用户要求为准，不额外设确认。验收按 `references/pilot-acceptance.md`，技术检查通过不自动将用户验收改成 accepted。

继承工程运行 `npm run check && npm run build && npm run verify:assets`；默认结构工程运行 `npm run check && npm run build && npm run verify:frames`；涉及命名事件再运行 `verify:score`。`build:studies` / `verify:studies` 仅在修改研究库或用户要看研究库时执行。96 项是灵感研究，不是每片配额。当前 adapter 数量以 production-registry.json 为准，需真实导入才算接入。只改文案不重复渲染无关帧；只看 Playground 不默认导出整片。

关键交接检查前、中、后画面；原速连看一次，再确认文字与声音。真实 MP4 用于区分浏览器预览性能和影片编排，不把数学连续或测试通过说成审美通过。

导出使用独立 public 素材目录和每次新建的 bundle 目录；不要把历史 MP4、下载链接、研究页面一起打包。缺依赖准确报错，不自动下载。导出之后检查音轨、时长和解码；不顺带更新浏览器或系统配置。

本地素材优先。先查现有来源与实际图像/视频内容，按“证据、解释、情境”决定用途。缺关键素材再在当前授权范围内检索公开源并核对许可、裁切与语义；不以关键词搜索命中当作适配证据。此过程由当前 Agent 编排，不宣称本包内置全自动素材识别模型。

## 字幕与真实素材（公开内测版）

voice 模式默认补底部同步字幕，不用主标题代替字幕。Agent核对文字与断句，把帧级cues写入story.captions，或以new --captions传入。默认缺字幕会被plan拦截；只有用户明确不要字幕才写captions.enabled=false。字幕不抢主视觉，实际复看深色画面、实拍和片尾。字段见[入门](docs/GETTING_STARTED.md)。

用户要求混剪时，具体场景用有来源的实拍，抽象关系用动效。用户明确授权联网获取素材、但未提供实拍时，可由Codex使用可用搜索与下载工具，按口播场景自行寻找有明确使用许可的公开照片和短视频，不逐张索取确认；记录作者、原始页面和许可证。搜索/下载受限时报告缺口，不自动购买，不把示意图或生成画面标成实拍。真实素材获取与镜头编排由Agent按已授权能力完成，不把源码中的示意图当实拍；示范工程见examples/voice-to-video。下载来源与作者保留，原件不自动打包。


## 画幅与文案模式

文案可用 script 模式，无音源就静音，不要求转写。默认为 16:9；用户要求其他比例时重排 Composition、Player、字幕和安全区并实际检查，不能只改尺寸。保留 `new --captions` 与 voice 默认字幕校验，详见 [入门](docs/GETTING_STARTED.md) 和 [画幅](docs/CUSTOMIZATION.md)。

## 按需资料，不要求全部通读

- 前置选型、镜头编号与内容适配：`references/semantic-orchestration.md`。
- Remotion 依赖安装、定位及 GitHub 说明：`references/remotion-integration.md`。
- 新音频：`references/audio-contract.md`。
- 新语义计划 / 阅读预算：`references/direction.md`、`references/story-contract.md`。
- 需要新机制：`catalog --relation ... --limit 4`，再读具体 adapter；不要整读 catalog。
- 实际接入新 adapter：`references/production-pipeline.md`。
- 再次出现停走或读不完：`references/continuity-review-20261027.md`。
- 完整命令和旧兼容流程：`references/workflow-detailed.md`，仅查相关段落；旧文档与当前入口冲突时以本入口为准。
- 本补丁来源和测量边界：`references/local-fastpatch.md`。

不修改原声速度、不编造内容、未知写未知；个人音视频和 `.local` 本机索引不得进入分享包。默认只做已授权本地修改；推送或发布需用户明确授权。交付说明基准、实际改动、准备/转写/编排/渲染用时和未确认的观感；不要把已有原片副本当新完成片。

## 许可

遵守 [LICENSE_SCOPE.md](LICENSE_SCOPE.md) 与 [ATTRIBUTION.md](ATTRIBUTION.md) 的分目录边界；96 项历史研究不新授 MIT，生产 adapter 是独立的通用实现，不授予第三方作品、素材或商标权。
