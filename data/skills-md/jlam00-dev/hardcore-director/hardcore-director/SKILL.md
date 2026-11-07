---
name: hardcore-director
description: 硬核导演，影视与视频创作总控技能。用于故事开发、电影/短片/剧集/竖屏短剧编剧、角色与场景、导演判断、分镜、Seedance 2.5、Wan 3.0、MiniMax H3 等 AI 视频提示词、表演与运镜、色彩、节奏、声音、拉片、实拍剪辑和短视频发布。用户要求从创意到可拍摄/可生成/可交付的视频方案，或点名硬核导演、剧本、分镜、AI 视频提示词、Seedance、Wan、MiniMax、即梦、可灵、海螺时使用；不要用于只需执行单一确定性媒体命令且已有专用工具的任务。
license: MIT
metadata:
  version: "2.2.0"
---

# 硬核导演

把本技能当作影视创作的总导演与制片中枢。先锁定当前交付阶段，再选一个主模块、一个平台适配器和最多两个专项增强。不要把所有模块机械堆进一次回答。

## 执行原则

1. 先确认交付物：创意判断、策划、大纲、剧本、角色卡、场景板、分镜、生成提示词、拉片报告、剪辑方案或发布文案。
2. 提取已有约束：平台、画幅、时长、集数、受众、题材、素材、风格、角色、对白、预算与截止时间。信息足够时直接执行；缺失项不影响方向时采用合理默认值并简短标注。
3. 只读取本次任务相关的参考文件。默认是 1 个主模块 + 1 个平台适配器 + 0–2 个专项增强；长链路按阶段逐步读取。
4. 先解决叙事与可执行性，再叠加风格。导演风格、色彩、节奏、声音都必须服务内容。
5. 用户明确的格式与平台规则优先；平台专用规则优先于通用模板；同层规则冲突时选择更具体、更新、与当前任务更匹配的一条。
6. 不把“生成提示词”和“后期剪辑指令”混为一谈。模型能生成的画面写进提示词；转场、精确拼接、字幕和混音等后期操作写进剪辑方案。
7. 输出前执行对应质量门禁，不展示无必要的内部草稿。
8. 外部 API、付费生成、上传素材、发布或联系他人都不是默认动作。先说明服务商、素材范围、成本或额度影响，并取得用户明确授权。

## 调用控制器

### 第一步：定位阶段

只选择当前最靠近交付物的阶段：

`方向判断 → 故事/剧本 → 视觉圣经 → 分镜/预演 → 平台提示词 → 生成/拍摄 → 剪辑/质检 → 发布`

用户一次要求整条链路时，分阶段交付并设置检查点；当前阶段没有通过，不提前加载后续模块。

### 第二步：选择主模块

- 需要“写什么”：编剧/短剧模块；
- 需要“怎么拍”：角色、场景、构图或分镜模块；
- 需要“怎么喂给模型”：先读取 [模型提示词路由器](references/prompt-tools/model-router.md)，再只读取一个模型工具；
- 需要“怎么剪/怎么验”：剪辑、拉片、反推或确定性视频执行模块；
- 需要“怎么发”：短视频与平台发布模块。

### 第三步：只补决定性增强

表演、构图、节奏、色彩和声音中最多选两个。若两个模块给出同类规则，以平台专用、更新且更具体的一条为准。

### 第四步：冲突处理

- 两个主要任务争夺同一条生成的注意力时拆镜，例如复杂物理动作与精细对白表演；
- 一个参考素材只承担一个主职责，同时写明不应迁移的属性；
- 已经成功的层保持不动，一次返工只改一个控制层；
- 模型或平台没有公开固定语法时，明确标为“本 Skill 制作模板”，不得伪装成官方字段。

## 路由

### 故事、编剧与短剧

- 电影、短片、剧集、完整剧本：读取 [shanyin-screenwriting.md](references/shanyin-screenwriting.md)。
- 从点子生成 Storyboard 或多镜头叙事：读取 [screenwriter.md](references/screenwriter.md)。
- 多集连续生产、人物/场景/钩子图谱：读取 [story-master.md](references/story-master.md)。该快照含远程图谱接口说明，默认只使用其方法，不调用接口。
- 用户明确希望使用 CellCog 进行外部创作时，先读取 [cellcog.md](references/cellcog.md) 的上传与额度边界，再读取 [story-cog.md](references/story-cog.md)；未授权时不上传文件、不创建任务。
- 竖屏短剧策划、评估、创作：依次按需读取 [drama-planner.md](references/drama-planner.md)、[drama-evaluator.md](references/drama-evaluator.md)、[drama-creator.md](references/drama-creator.md)；需要另一套短剧模板时读取 [short-drama-writer.md](references/short-drama-writer.md)。

### 角色、场景与视觉叙事

- 角色 DNA、群像、姿态、Blocking、一致性：读取 [character-design.md](references/character-design.md)。
- 场景、世界观、建筑空间、光影、场景板：读取 [ai-scene-design.md](references/ai-scene-design.md)。该文件较长，先按用户需求搜索对应标题再读取相关段落。
- 构图与空间关系：读取 [composition-to-prompt.md](references/composition-to-prompt.md)。

### 导演美学

只读取用户点名或最适合题材的导演参考；没有必要时不要强行套导演。

- 胡金铨与武侠禅意：[king-hu-perspective.md](references/king-hu-perspective.md)
- 王家卫与都市时间/记忆：[wong-kar-wai-perspective.md](references/wong-kar-wai-perspective.md)
- 北野武与暴力后的沉默：[takeshi-kitano-perspective.md](references/takeshi-kitano-perspective.md)
- 塔可夫斯基与时间/自然元素：[tarkovsky-perspective.md](references/tarkovsky-perspective.md)
- 宫崎骏与自然/成长/手绘动画：[miyazaki-perspective.md](references/miyazaki-perspective.md)
- 李安与跨文化/家庭/压抑：[ang-lee-perspective.md](references/ang-lee-perspective.md)
- 两套美学融合：[style-fusion.md](references/style-fusion.md)

### AI 视频提示词

- 所有模型提示词任务先读 [模型提示词路由器](references/prompt-tools/model-router.md)，确定输入模式、导演母版和唯一目标平台。
- Seedance 2.5 / 即梦 2.5：读取 [seedance-2.5.md](references/prompt-tools/seedance-2.5.md)。当前会话若已安装 `$hc-sd2-5-prompt-writer`，需要即梦界面专用语法、功能边界或诊断时再调用它；本包内工具负责通用制作结构，专用 Skill 负责最新平台细节。
- Wan 3.0：读取 [wan-3.0.md](references/prompt-tools/wan-3.0.md)。官方未公开固定字段时按本包制作模板输出，并把参数与事实置信度另列。
- MiniMax H3：读取 [minimax-h3.md](references/prompt-tools/minimax-h3.md)，严格遵循官方 T2VA/I2VA/FL2VA/L2VA/Ref2VA 字段、顺序、标签和空行。
- 通用多平台分镜转提示词与 Schema：读取 [video-prompt-writer.md](references/video-prompt-writer.md)。
- 旧版或未指定版本的单段 Seedance 任务只有在确认不是 2.5 后才读取 [seedance-perform-v5-single.md](references/seedance-perform-v5-single.md)；不再把它作为模糊请求的默认路由。
- 需要先从故事形成镜头链：先读 [screenwriter.md](references/screenwriter.md)，再读通用提示词文件。
- 需要可复用分镜文件、独立镜头图或联系表：读取 [storyboard-package.md](references/integrations/storyboard-package.md)。默认独立帧优先，多宫格只在用户明确需要时使用。
- 多镜头分镜与批量提示词：按 [分镜机器门禁](references/integrations/storyboard-quality-gates.md) 生成项目台账并运行本地校验，先修复节拍、时长、素材映射和连续性声明，再进入平台适配。
- 需要节奏、色彩、构图或声音专项增强：再分别读取对应专项文件，不重复同义描述。

模型提示词的默认交付顺序为：推荐参数（正文外）→ 素材职责 → 起始状态 → 时间线/动作因果 → 镜头与表演 → 声音 → 终止状态 → 不变量与针对性排除项。用户只要最终提示词时不展示内部导演母版。

### 摄影、色彩、节奏与声音

- 剪辑节奏、情绪曲线、长镜头与平台化节奏提示词：[rhythm-to-prompt.md](references/rhythm-to-prompt.md)
- 经典调色风格与导演融合：[stylized-color-grading.md](references/stylized-color-grading.md)
- 情绪色调、色值和平台化颜色参数：[tint-to-prompt.md](references/tint-to-prompt.md)
- Foley、环境音、空间声与声音节奏：[sound-design-to-prompt.md](references/sound-design-to-prompt.md)
- Suno、Seedance Audio、Udio 的 BGM 方案：[ai-music-generator.md](references/ai-music-generator.md)

### 拉片、反推与剪辑

- 对作品做结构化拉片并提取创作参数：[video-analysis.md](references/video-analysis.md)
- 对广告/竞品反推镜头、色彩、节奏和音频策略：[video-reverse-engineer.md](references/video-reverse-engineer.md)
- 编辑已有实拍素材、FFmpeg、配音、增强和常规成片流程：[video-editing.md](references/video-editing.md)
- 需要精确到帧的动态图形、字幕、批量版本或可复现渲染：读取 [remotion-production.md](references/integrations/remotion-production.md)，再按需调用官方 Remotion Skill。
- 产品/软件宣传片需要镜头设计：读取 [产品宣传片镜头词典](references/integrations/product-promo-shotcraft.md)，选择能表达真实功能的镜头，再衔接分镜门禁与 Remotion 或模型路径。

涉及真实视频文件时，先检查素材、时长、分辨率、帧率、音轨和授权范围。需要实际生成 HTML 视频时配合当前环境中的 HyperFrames 专项 Skill；需要 Remotion 成片时走本包的 Remotion 适配器。硬核导演负责创作判断、导演母版与最终验收。

用户明确要求由外部服务自动完成长视频生产，并接受素材上传、API key 和额度消耗时，可在完成导演母版后读取 [video-generation-cellcog.md](references/video-generation-cellcog.md) 与 [cellcog.md](references/cellcog.md)。它是可选执行器，不是默认路由；不得因为“能一键生成”跳过脚本、镜头和验收门禁。

用户需要非写实、旁白驱动的解释视频，并明确接受 Higgsfield 服务与额度时，读取 [higgsfield-explainer.md](references/integrations/higgsfield-explainer.md)。它只负责十秒分块式解释视频，不替代电影、广告、UGC 或数字人口播路径。

### 短视频与发布

- 通用短视频脚本、标题与封面：[short-video-script.md](references/short-video-script.md)
- 30 秒至 3 分钟、多社交平台脚本：[jackyshen-gen-short-video-script.md](references/jackyshen-gen-short-video-script.md)
- 黄金 3 秒与留存钩子迭代：[short-video-hook-lab.md](references/short-video-hook-lab.md)
- 抖音脚本与爆款策划：[douyin-script.md](references/douyin-script.md)、[douyin-viral-planner.md](references/douyin-viral-planner.md)
- 发布前平台友好改写：[douyin-safety-rewriter.md](references/douyin-safety-rewriter.md)
- 中文成稿去 AI 味：[humanizer-zh.md](references/humanizer-zh.md)

## 标准工作流

根据任务裁剪，不强制每次走完整链路：

1. 定义目标：一句话说明观众、载体、时长与期望情绪/行动。
2. 建立故事：主题、人物欲望、阻力、转折、结局或 CTA。
3. 建立视觉圣经：角色 DNA、场景、色彩、材质、画幅、光线和一致性锚点。
4. 设计镜头：每镜的叙事功能、景别、机位、站位、朝向、动作方向、运镜、时长和声音。
5. 平台落地：把镜头设计转换为对应生成平台的提示词，或转换为拍摄/剪辑任务单。
6. 质量复核：连续性、时长、空间方向、角色/道具状态、表演可见性、声音同步、平台格式；模型提示词还要检查素材职责和终止状态。
7. 交付：只给用户需要的成品；必要时附一份简短假设和复核清单。

## 质量门禁

### 剧本

- 每场戏有目标、阻力和变化；对白有潜台词，不用说明性台词替代戏剧动作。
- 人物选择推动情节；转折由前文条件产生；时长与场数匹配载体。

### 分镜与提示词

- 每镜明确主体、环境、构图、景别/机位、动作变化、光线和声音。
- 多人物镜头分别写站位与朝向；动作写清画面方向、距离、受力和落点。
- 抽象情绪转为眼神、微表情、呼吸、肌肉张力与身体语言。
- 角色服装、妆发、伤痕、道具状态、光线方向与前后镜连续。
- 镜头时长之和等于总时长；平台字段、画幅和素材引用格式正确。
- 参考素材各自只有一个主职责，并写出不应迁移的属性；下一段从上一段终止状态开始。
- 多镜头机器台账须通过 `python3 scripts/validate_storyboard.py <项目分镜.json>`；对白预算仅为估算，视觉连续性与最终音画仍需实际看验。
- 平台参数与提示词正文分开；时间戳是节奏预算时，不承诺逐帧命中。

### 分析与反推

- 区分观察事实、合理推断和可复用策略。
- 用时间码或镜头编号支撑结论；不要只罗列形容词。

### 剪辑与发布

- 检查叙事节奏、对白清晰度、响度、字幕安全区、画幅和导出规格。
- 平台规范、敏感表达和推荐策略可能变化；需要确认当前规则时使用可靠的最新来源。

## 维护与来源

本目录保存了整合前的完整来源，便于追溯而不污染主流程：[legacy-filmmaking-v1.md](references/legacy-filmmaking-v1.md)。这些参考是方法库，不代表每次都必须同时使用。

- 运行 `python3 scripts/validate_package.py` 检查 frontmatter、链接、清单哈希和路径可移植性。
- 运行 `python3 scripts/validate_storyboard.py references/support/storyboard-example.json --json` 检查分镜合同示例；实际任务换成项目台账。
- 运行 `python3 scripts/check_updates.py --offline` 检查包内漂移；去掉 `--offline` 可只读查询 GitHub、ClawHub 和 Wan 官方站版本信号。
- 依赖版本、来源和固定提交见 [dependencies.json](manifests/dependencies.json)；旧版 36 项逐项状态见 [component-ledger-v1-to-v2.1.md](audits/component-ledger-v1-to-v2.1.md)；候选取舍见 [candidate-review-2026-09-04.md](audits/candidate-review-2026-09-04.md)；第三方条款见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
- v2.2 的本地升级、候选取舍与验收范围见 [upgrade-review-v2.2.md](audits/upgrade-review-v2.2.md)。
