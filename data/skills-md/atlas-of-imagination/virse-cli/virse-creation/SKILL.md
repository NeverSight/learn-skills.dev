---
name: virse-creation
description: >-
  在 Virse 探索灵感、搜集参考、验收画布作品的品牌一致性，或生成、修改图片、视频、3D 和文本并迭代。提示词与表现方法配合图片／视频技巧；单纯布局走 virse-canvas，完整跨能力项目走 virse-ultra-design。
---
# 创作与迭代

<!-- virse:background:start -->
Virse 是 AI native 的创作系统，用画布连接想法、素材、审美、工具与模型，支持图片、视频、3D 和文本。资源目录管理素材与归属，画布组织创作输入、过程与结果。

只读当前任务所需参考，已读且适用的内容沿用，链接不自动加载内容。
<!-- virse:background:end -->

用户指定后端时，在首条远端命令前设置 `VIRSE_BACKEND_URL`。

## 从目标到作品

你是与用户共同推进作品的创作家。结合宿主已获准的本地、其他应用及画布材料，理解用途、表达、保留项和改变项；目标明确就主动推进。按用户要求、实际输入能力与输出规格选择当前可用模型；质量判断需有依据，目录顺序不证明质量。需要选型细节、授权范围不清或特殊提交时再读[模型与提交方式](references/models-and-submit.md)。

首次生成缺少适用授权时，一次建议模型、关键配置与本轮总输出（含修正版）或迭代范围，确认后执行；用户已确认配置或授予自主权就在范围内推进，超出范围再确认。“偏好高质量”本身不授予自主选型权，查询与准备素材可先做。记住偏好的邀请留到交付后，不打断首次创作。

灵感搜集、品牌验收先读任务参考。准备方案、提示词或诊断效果时，分别取 `virse-image-craft`、`virse-video-craft` 中当前问题需要的方法；已读内容直接沿用，返回执行时无需重读入口导航。本入口负责真实能力与执行。

按目标选择直接生成、图片处理或已有工具，需要新的执行逻辑才制作工具。精确管理与指定模型、工具产物优先 CLI 直做；适合画布内独立创作会话、连续制作与反馈的子任务可主动委派 `virse-composer`。宿主统筹混合任务并验收全部交付。

## 常见任务短路径

| 当前任务 | 最小读取与执行 |
| --- | --- |
| 写图片／视频 prompt、选择表现方法或诊断效果 | 按问题取 `virse-image-craft`／`virse-video-craft` 的相关参考；只要 prompt 时不登录、不提交 |
| 普通生图，目标和品牌依据已明确 | 本入口执行；需要提示表达或参考分工才补相应技巧，不进入品牌中心建设 |
| 参考图生成、改图或图片处理 | 补[图片创作与处理](references/image-and-edit.md)的对应操作；只补当前缺少的参考理解或编辑方法 |
| 查询状态、取消，或按确定配置执行处理 | 直达对应操作或[任务合同](references/shared/contracts/generation.md)，不预读创作技巧 |

普通生图沿用适用授权或完成上述一次确认后即可提交。`ORG/CANVAS` 来自已选空间与画布，`MODEL` 来自当前可用能力查询；已知型号先 `model get`，需要选型才列目录。`KEY` 为本次输入固定保存的幂等键。

```bash
virse --org "$ORG" --canvas "$CANVAS" --json generation image --model "$MODEL" --prompt "$PROMPT" --idempotency-key "$KEY" --wait
virse --org "$ORG" --canvas "$CANVAS" --json generation get "$TASK"
virse --org "$ORG" --canvas "$CANVAS" --json asset preview "$ASSET" --representation content --output ./result.bin
```

`TASK` 来自提交回执，`ASSET` 来自该任务实际成功输出的 asset_id，不能把节点或资源项 ID 代入。若提交尚未终态或受理不明，转[任务合同](references/shared/contracts/generation.md)等待或查证，不再次创建。查看展示文件的真实格式与内容，输出路径必须不存在，扩展名不转换格式；预览不等于原件。需要下载原件、打包或接续时才展开[文件交付](references/shared/contracts/delivery.md)。

当前模型能力已核清且仍适用时无需重复查询。未知操作或特殊输入才查询 `generation operations`；参数不清楚时查对应命令 help。快捷命令没有通用 `--aesthetic`，取用审美必须有当前消费方真实支持的输入合同。

执行后核对 task 和逐输出状态，取得实际内容并按用户要求检查。发现问题时说清具体差异、这次改变和保留项；改变输入是新创作，使用新键。查找原受理结果与按原输入、原键恢复是另一条路径，不能混同为效果迭代。

## 当前任务直达

| 用户正在做什么 | 只读需要的参考 |
| --- | --- |
| 开启 Ultra Design／全能创作，统筹完整创作项目 | `virse-ultra-design` |
| 建设、接续品牌中心或核对整库交付 | `virse-brand-center-creator` |
| 依据已有品牌中心制作作品，尚需定位相关规则与资产 | `virse-brand-center-creator` → `references/deliver-and-reuse.md`；依据已明确时直接创作 |
| 开启灵感探索、找参考或做情绪板，从描述、图片或画布发展概念、故事与视觉方向 | [灵感探索](references/inspiration-exploration.md) |
| 对照品牌标准验收画布作品，将依据、问题与建议写回画布 | [品牌验收](references/brand-review.md) |
| 从画布提炼可复用任务和创作方法、总结成智能工具 | `virse-smart-tool-creator` → `references/from-canvas.md` |
| 理解画布中的视觉偏好、推荐审美方向并沉淀模块 | `virse-aesthetic-creator` → `references/from-canvas.md` |
| 结合外部材料策划创作、选方案、复用原图输入或比较迭代 | [目标、输入依据与效果迭代](references/plan-and-iterate.md) |
| 选模型、管理模型收藏、构造特殊请求或多个输出 | [模型与提交方式](references/models-and-submit.md) |
| 做视频 | [视频创作](references/video.md) |
| 文本或图片建模 | [3D 生成的实际边界](references/3d.md) |
| 生成或改写画布文本 | [文本创作](references/text.md) |
| 选择并运行现有工具 | [固定工具产物与运行合同](references/shared/contracts/tool-run.md) |
| 查阅或取用已有审美 | [审美身份与消费条件](references/shared/context/aesthetics.md) |

只缺连接信息、对象身份或输出解释时，分别直读[连接](references/shared/contracts/connection.md)、[对象](references/shared/context/objects.md)或[执行](references/shared/contracts/execution.md)合同，不将它们全部预读。需要画布结构修改、资源归档或改权时，补该职责的最小合同；职责确实切换时再选相应入口。

## 完成判断

记录本次目标、参考及关键输入、task ID、逐输出状态、节点和资产身份；需要文件交付时核对实际文件。`get` 退出 0 只证明读取成功，`succeeded` 也不能证明文字、构图、审美或品牌要求已满足。无法查看某种产物时说明哪些质量尚未验证。

当前节点配置不保证完整历史 prompt；指定输出节点不自动恢复原模型或输入。画布显示位置不等于图内主体位置，布局尺寸不等于模型输出分辨率。没有实际开放合同的 3D 相机、渲染和截图能力不能由通用 submit 或 Composer 委派补成已支持。
