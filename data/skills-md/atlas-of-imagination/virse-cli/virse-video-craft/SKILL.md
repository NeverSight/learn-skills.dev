---
name: virse-video-craft
description: >-
  视频创意与提示词，选择参考、生成、编辑和续写路径，设计动作、镜头、节奏与声音，判断参数取舍并诊断效果。可只交付 prompt；实际生成配合 virse-creation，状态查询与资产管理走业务入口。
---

# 视频创作技巧

<!-- virse:background:start -->
Virse 是 AI native 的创作系统，用画布连接想法、素材、审美、工具与模型，支持图片、视频、3D 和文本。资源目录管理素材与归属，画布组织创作输入、过程与结果。

只读当前任务所需参考，已读且适用的内容沿用，链接不自动加载内容。
<!-- virse:background:end -->

## 先确定要固定什么

作为与用户共同推进视频的创作家，结合已有且获准使用的素材与上下文，判断用途、核心变化、必须保留的内容和可自由发挥的部分。信息足够就推进，只补问会改变创作路径的缺口，例如“这张图必须作为开场，还是只借人物长相”。不把完整访谈作为写 prompt 的前置。

用户只要提示词、分镜或诊断，就交付相应内容，不提交生成。实际在 Virse 执行时，按名称读取 `virse-creation` 及其当前任务所需合同，已读的只补缺项，查真实模型能力、输入角色和参数，再按已有授权范围执行。创作偏好不等于长期自主生成授权。只有需要重新设计或生成关键图时，才按名称读取 `virse-image-craft`；不将图片技巧设为所有视频任务的前置。

需要其他 Skill 时先确认宿主能够读取；未安装就说明缺少哪个包并帮助定位安装方式，不假设名称已带入其内容。提示词与视频诊断仍可在本 Skill 内完成。

## 生成路径

| Virse 产品任务 | 什么时候选 | 输入固定什么，文字补什么 | 需要时读取 |
| --- | --- | --- | --- |
| 全能参考 `reference` | 要借用人物、产品、场景或动作，未要求媒体就是开场 | 按角色借用参考；写清每份素材借什么、主体如何互动，声音参考须另核模型支持 | [参考与连续性](references/references-and-continuity.md) |
| 首尾帧 `firstLastFrame` | 起点和终点都有明确画面 | 首尾各一张图约束两端；文字说明中间怎么到达 | [参考与连续性](references/references-and-continuity.md) |
| 视频编辑 `edit` | 已有视频，要修改其中内容 | 一份源视频提供已有变化；指令说清改什么、保留什么 | [编辑与续写](references/editing-and-extension.md) |
| 文生视频 `textToVideo` | 没有媒体输入，或希望重新设计画面 | 文字同时建立可见内容与时间变化 | [提示词](references/prompt-craft.md) |
| 图生视频 `imageToVideo` | 一张图必须成为起始画面 | 一张首帧提供起始外观与构图；文字主要推动变化 | [提示词](references/prompt-craft.md)、[参考与连续性](references/references-and-continuity.md) |
| 视频续写 `extend` | 要从原片末状态继续 | 一份源视频提供时序上下文；文字写接下来发生什么 | [编辑与续写](references/editing-and-extension.md) |
| 视频渲染 `render` | 当前产品任务要求以已有视频继续处理 | 同样接收一份源视频，后端使用 `video_mode=edit`；按真实合同理解改动，不据名称推导 3D 渲染能力 | [编辑与续写](references/editing-and-extension.md)、[参数](references/parameters.md) |

这些是产品入口，不是所有模型都支持的能力清单。实时目录的 `generation_capabilities`、模型详情和 operation schema 决定能否提交及如何绑定；不把产品模式名直接当成 CLI flag。

## 按问题取用方法

只读相关参考。专题外链用于溯源，无需逐个打开；需要核实模型特有方法时再查对应官方说明。

| 当前要解决的问题 | 读取 |
| --- | --- |
| 共建品牌系统、探索应用并交付规范和资产文件夹 | `virse-brand-center-creator`；具体视频方法仍按当前问题取用 |
| 验收画布作品是否符合品牌标准，并在画布交付结果 | `virse-creation` → `references/brand-review.md` |
| 写 prompt、消除堆叠与歧义，或适配已选模型的写法 | [提示词](references/prompt-craft.md) |
| 多参考分工、首尾之间的路径、人物或产品保持一致 | [参考与连续性](references/references-and-continuity.md) |
| 动作、速度或运镜不对，主体和相机混淆，首帧运动线索冲突 | [动作与镜头](references/motion-and-camera.md) |
| 修改原片、接着原片生成、选择原生续写或尾帧拼接 | [编辑与续写](references/editing-and-extension.md) |
| 时间分配、停顿、对白、口型、音乐与音效 | [节奏与声音](references/timing-and-audio.md) |
| 选择时长、比例、分辨率、帧率或参考控制 | [参数](references/parameters.md) |
| 看片、定位失败原因、比较并决定下一次改什么 | [查看与迭代](references/review-and-iterate.md) |
| 想看首帧约束、运动问题与最小修正如何串起来 | [图生视频模拟案例](references/image-to-video-case.md) |

实际生成后查看真实视频，按问题选择重放、局部慢看和听音。任务成功、封面可见、抽帧正常都不能证明整片和声音已验收；未能检查的部分要明确说明。
