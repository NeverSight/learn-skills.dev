---
name: srt-remotion-video-papercraft
description: SRT 字幕驱动的 A-roll / B-roll 混合视频生成流程。当用户需要从 SRT 生成 Remotion 视频、纸艺知识视频或 A/B-roll 混合视频时使用。
---

# SRT Remotion Video

将 SRT 转换为以 A-roll Remotion 动画为主体、纸艺定格 B-roll 为补充的完整视频。SRT 时间轴始终是唯一权威。

## 流程

```text
SRT
→ 依赖预检与项目初始化
→ Storyboard SubAgent 语义分镜并提出 A/B 类型
→ A/B 分镜校验
→ Gate 1：用户审批 A/B 方案
→ B-roll Director 生成全部图片
→ Gate 2：用户审批全部图片
→ B-roll Director 生成全部视频并准备媒体
→ Gate 3：用户审批全部视频
→ 检测可用的视频高清化 Skill，并询问是否启用
→ 可选 B-roll 高清化与 A-roll Creator 并行执行
→ 等待 A-roll 与已启用的高清化分支全部完成
→ 生成 A/B 联合注册表
→ 最终校验与渲染
```

没有 B-roll 时跳过 B-roll Director 与 Gate 2、Gate 3。只要存在 B-roll，在全部 B-roll 视频获批前不得启动 A-roll Creator。

## 路径契约

- `skillRoot`: 当前 Skill 绝对路径
- `templateRoot`: `{skillRoot}/template`
- `referencesRoot`: `{skillRoot}/references`
- `scriptsRoot`: `{skillRoot}/scripts`
- `srtPath`: 用户提供的 SRT 绝对路径
- `projectRoot`: 默认 `{dirname(srtPath)}/remotion-video-projects/{yyyy-mm-dd-hh-mm-ss}`

所有 Agent prompt 必须传展开后的绝对路径。阶段规则只能从相应 reference 读取，运行态状态必须落盘。

## 0. 输入与初始化

验证 `srtPath` 后执行：

```bash
node "{scriptsRoot}/ensure-template-deps.js" "{templateRoot}"
node "{scriptsRoot}/init-project.js" --srt-path "{srtPath}"
```

模板始终复制到独立项目；旧项目不会自动同步新模板。

## 1. Storyboard SubAgent

启动一个 SubAgent，传入：

- `{referencesRoot}/storyboard-parser.md`
- `skillRoot`
- `projectRoot`
- `srtPath`
- `{scriptsRoot}/generate-storyboard.js`
- `{scriptsRoot}/validate-roll-plan.js`

SubAgent 必须严格执行 Storyboard reference，生成 `groups.json` 与 `storyboard.json`，并让 A/B 分镜校验通过。主 Agent 验证结构化返回结果。

## 2. Gate 1：审批 A/B 方案

主 Agent 展示每场的 ID、时间范围、字幕摘要、`rollType`、`rollReason`、`visualHint`，以及 B-roll 总时长和建议占比。

用户修改类型时：

1. 更新 `groups.json`
2. 重新运行 `generate-storyboard.js`
3. 重新运行 `validate-roll-plan.js`
4. 重新展示 Gate 1

用户批准后，当前 `storyboard.json` 成为冻结事实源。不得用媒体生成结果修改 SRT 时间轴。

## 3. B-roll Director 与 Gate 2、Gate 3

仅在 Storyboard 含 B-roll 时执行。主 Agent解析已安装的 `papercraft-stop-motion-explainer` 入口绝对路径，并启动一个 B-roll Director SubAgent，传入：

- `{referencesRoot}/broll-director.md`
- `papercraftSkillPath`
- `projectRoot`
- `{projectRoot}/storyboard.json`
- `{projectRoot}/broll-production.json`
- `{scriptsRoot}/prepare-broll-asset.js`
- `{scriptsRoot}/validate-broll-assets.js`

主 Agent 持有用户会话与全部 Gate；B-roll Director 负责从整批 B-roll 提炼一次统一纸艺艺术方向与可逐字复用的 Shared Style Anchor，再按图片系列一致性规则生成各场提示词、调用生成 Skill、完成资产落盘和 manifest 更新。该内部艺术方向提炼不新增 Gate、风格预览图或参考图流程。用户提出修改时优先向同一个 Director 发送 follow-up；若其不可用，新 Director 必须从 manifest 恢复。

严格顺序：

1. Director 生成全部图片并返回。
2. 主 Agent 展示全部图片（附每张图的本地绝对路径），执行 Gate 2。
3. 用户逐场修改，直到所有图片获批。
4. Director 才能生成全部视频、运行媒体准备脚本并返回。
5. 主 Agent 展示全部视频（附每个视频的本地绝对路径），执行 Gate 3。
6. 用户逐场修改，直到所有视频获批。
7. 将审批结果交回 Director，由其更新 manifest 并运行 `validate-broll-assets.js`；主 Agent确认结构化校验结果后再继续。

图片修改时仅让该场景的视频失效并退回 Gate 2。失败时说明原因与可行建议，等待用户决定；禁止自动重试、降级、改回 A-roll或增加静态注册模式。

## 4. 可选 B-roll 高清化与 A-roll Creator

Gate 3 通过后，主 Agent 检查当前环境的可用 Skill 中是否存在明确支持视频高清化或视频超分辨率的 Skill，不写死具体 Skill 名称。

- 没有可用 Skill：告知用户，并直接启动 A-roll Creator。
- 找到一个：说明已发现的能力，询问用户是否启用。
- 找到多个：列出候选，让用户选择。
- 用户跳过：直接启动 A-roll Creator。
- 用户同意：创建独立 `{projectRoot}/broll-upscale.json`，启动一个 Upscale SubAgent，并与全部 A-roll Creator 并行执行。

高清化是可插拔后处理模块，不得修改原始 B-roll 资产、`broll-production.json` 或 Gate 3 批准状态。详细协议见 `{referencesRoot}/broll-upscaler.md`。主 Agent 必须把选中 Skill 的绝对入口路径作为 `upscaleSkillPath` 传给 Upscale SubAgent；同一个 SubAgent 负责整批 B-roll，不为每场单独启动 Agent。

用户同意高清化后，主 Agent 按 `broll-upscaler.md` 的 manifest 契约完成启动准备：

1. 确认所有 Storyboard B-roll 在 `broll-production.json` 中均为 `video-approved`。
2. 创建 `decision: accepted`、批次 `status: pending` 的 `broll-upscale.json`，记录选中的 Skill 名称与绝对入口路径。
3. 为每个 B-roll 创建逐场 `pending` 记录和固定资产路径，默认选择高清版本。
4. 将批次状态改为 `running`，再同时启动 Upscale SubAgent 和 A-roll Creator。

具体逐场字段、资产路径、媒体信息和源文件指纹只以 `broll-upscaler.md` 为事实源，`SKILL.md` 不重复定义。用户跳过或本地没有可用 Skill 时，主 Agent仍记录相应 `decision`，使恢复流程不会重复询问。缺少该文件的旧项目按未启用高清化处理。

### 4.1 A-roll Creator

读取冻结 Storyboard，仅计算 A-roll 数量：

```text
aRollCount = scenes.filter(rollType !== "b-roll").length
creatorCount = ceil(aRollCount / 5)
```

对每个 `creator-XX` 执行：

```bash
node "{scriptsRoot}/generate-creator-scenes.js" \
  "{projectRoot}/storyboard.json" \
  "{creatorId}" \
  "5" \
  "{projectRoot}/scene-plans/{creatorId}.scenes.json"
```

并行启动 Creator SubAgent，传入：

- `{referencesRoot}/scene-component-creator.md`
- `skillRoot`
- `projectRoot`
- `creatorId`
- `scenesDataPath`
- `planPath`
- `{scriptsRoot}/validate-scene-plan.js`

Creator 的全部规则以 reference 为事实源。Creator 只生成分配到的 A-roll `SceneXXX.tsx`，不得修改宿主、注册表或 B-roll。

### 4.2 并行汇合

A-roll Creator 全部完成后：

1. 若未启用高清化，直接进入注册。
2. 若高清化仍为 `pending / running`，等待 Upscale SubAgent 完成。
3. 若任一场景或批次为 `failed`，向用户报告失败场景、原因和可选处理方式，禁止自动使用原视频、自动重试或进入注册。
4. 只有所有选择高清版本的场景均为 `completed`，或失败场景已经由用户明确改选原视频，并且 `{scriptsRoot}/validate-broll-upscale.js` 通过，才能进入注册。

用户可以在失败后明确选择重试失败场景、逐场回退原视频或放弃全部高清化；主 Agent 必须先按 `broll-upscaler.md` 的契约将决定写入高清化 manifest，再继续。不存在 Gate 4：全部高清化任务和技术校验完成后自动使用高清化资产。

## 5. 注册、校验与渲染

全部 A-roll 完成后执行：

```bash
node "{scriptsRoot}/generate-scenes-registry.js" \
  "{projectRoot}" \
  "{projectRoot}/storyboard.json"

node "{scriptsRoot}/validate-project.js" \
  "{projectRoot}" \
  "{projectRoot}/storyboard.json"
```

校验失败时不得渲染。通过后执行：

```bash
cd "{projectRoot}"
npx remotion render Main out/output.mp4
```

通知用户输出路径、场景数、A/B 场景数和总时长。

## 恢复规则

已有 `projectRoot` 时先读取：

- `storyboard.json`
- `broll-production.json`（如存在）
- `scene-plans/`
- `src/scenes/`

根据已完成 Gate 和资产状态继续，不重复已批准的生产。任何 `rollType` 修改都必须从 `groups.json` 重新生成 Storyboard、重新校验并重新计算 Creator 分组；未受影响的已批准 B-roll 资产可以保留。

若存在 `broll-upscale.json`：

- `accepted + running/pending`：恢复或等待同一批高清化任务。
- `accepted + failed`：等待用户指令，不得自动回退。
- `accepted + completed`：校验后使用高清化资产。
- `skipped / unavailable`：使用原始 B-roll，不重复询问。
- 原始 `clip.mp4` 发生变化时，对应高清化结果因源指纹不一致而失效。
- 已记录的高清化 Skill 入口不可用时，重新发现同名或同能力 Skill，并在用户确认前不得自行更换实现。

## 调试、重新渲染与高分辨率

- 所有 B-roll 在 Remotion 合并层必须静音；`BrollScene.tsx` 的 `<OffthreadVideo>` 必须设置 `muted`，不得把 B-roll 资产自带音轨写入最终成片。
- 调试音频复制到 `public/audio.mp3`，在 `Main.tsx` 宿主层加入全局 `<Audio>`；B-roll 仍保持静音。
- 最终重新渲染时只移除全局调试音频，不得移除 B-roll 的 `muted` 设置。
- 输出规格来自 `src/video-settings.json`；设计坐标始终为 1920x1080。
- 4K 使用现有输出 profile 或 `--scale 2`，不要重写 Creator 布局。
- 改 fps 后必须重新生成注册表，使 `totalDurationInFrames` 与 fps 一致。

## 资源职责

- `references/storyboard-parser.md`: 语义分镜与 A/B 决策
- `references/broll-director.md`: B-roll 图片/视频生产与 Gate 状态
- `references/broll-upscaler.md`: 可选 B-roll 高清化后处理与恢复协议
- `references/scene-component-creator.md`: A-roll 规划与实现
- `scripts/validate-roll-plan.js`: A/B 数据与 4-8 秒硬校验
- `scripts/prepare-broll-asset.js`: 媒体探测与尾帧提取
- `scripts/prepare-upscaled-broll-asset.js`: 归一化高清化结果、媒体探测、源指纹与高清尾帧提取
- `scripts/validate-broll-assets.js`: B-roll 资产与批准状态校验
- `scripts/validate-broll-upscale.js`: 可选高清化状态、资产、媒体信息与源指纹校验
- `scripts/broll-upscale-utils.js`: 独立高清化 manifest 读取与最终渲染资产解析
- `scripts/generate-creator-scenes.js`: 过滤并分配 A-roll
- `scripts/generate-scenes-registry.js`: A/B 联合注册
- `scripts/validate-project.js`: 最终完整性校验

## 核心不变量

1. SRT 时间轴、总时长和 Scene ID 不随媒体生成结果改变。
2. B-roll 单场内容时长必须为 4-8 秒；建议占比约 15%，不设比例硬限制。
3. A/B 场景之间保持硬切，不增加视觉转场。
4. B-roll 视频按原速播放；短于插槽时冻结真实尾帧，长于插槽时在下一场开始处裁断。
5. B-roll 资产可以包含音轨，但最终合并时必须静音；成片音频只能来自宿主层明确挂载的全局音轨。
6. 最终渲染只接受已通过 Gate 3 的标准 B-roll 视频。
7. 缺失 `rollType` 的旧项目按纯 A-roll兼容处理。
8. 高清化未启用时，原 B-roll 生产、注册和渲染行为保持不变。
9. 高清化不得改写 Storyboard；最终使用高清化文件的真实时长和真实尾帧执行既有裁切与补帧规则。
