---
name: virse-canvas
description: 理解 Virse 画布内容、节点和引用关系，放入素材，商定整理方式并编辑分组、布局、复制、恢复与讨论。生成或修改作品走 virse-creation；资源目录整理走 virse-assets。
---

# 画布操作

<!-- virse:background:start -->
Virse 是 AI native 的创作系统，用画布连接想法、素材、审美、工具与模型，支持图片、视频、3D 和文本。资源目录管理素材与归属，画布组织创作输入、过程与结果。

只读当前任务所需参考，已读且适用的内容沿用，链接不自动加载内容。
<!-- virse:background:end -->

用户指定后端时，在首条远端命令前设置 `VIRSE_BACKEND_URL`。

## 先理解当前对象

画布自身是资源，但节点与组合属于画布空间。`canvas get` 使用画布空间 ID，`canvas contents` 使用画布资源路径或资源项 ID；不互换。缺少连接时读[连接与空间](references/shared/contracts/connection.md)，身份关系见[对象关系](references/shared/context/objects.md)。示例变量均来自本次真实查询或用户明确给出的身份。

普通读取和放置可直接做：

```bash
virse canvas get "$CANVAS" --json
virse canvas element get "$ELEMENT" --org "$ORG" --canvas "$CANVAS" --json
virse canvas add --resource '/项目素材/产品.png' --x 100 --y 200 --org "$ORG" --canvas "$CANVAS" --json
```

用户要“看看这块是什么”时，先读标题、文本、组合成员、坐标与连线，再查看必要的真实媒体；区分保存的结构与用途推断。坐标尺寸描述画布显示，不能充当图内主体位置或 3D 相机视角；当前没有画布范围截图或 3D 视角渲染专用入口。

节点 `generation.config` 是当前保存的配置，不保证任意图片原始 prompt、供应商最终 prompt 或完整历史参考。只复用实际读到的信息；后续生成交给创作职责，不因为读取配置就重跑任务。

手动连线把已有内容作为目标创作框的输入或参考，供其继续创作；一般说明与阅读顺序用文字、分组和布局表达。系统维护的 Composer 产物来源边另作区分。创建或调整前读[编辑对象与关系](references/edit-graph.md)。

## 整理与明确对象的调整

用户要整理画布、归类收纳或重新分组排版时，先按[画布整理](references/organize-canvas.md)查看内容、提出方案并确认，再执行；已有确认的约定沿用。具体对象和调整方式已明确时，按用户指令处理。

```bash
virse canvas element name "$ELEMENT" '产品主图' --org "$ORG" --canvas "$CANVAS" --json
virse canvas layout --group "$GROUP" --mode row --gap 40 --x 100 --y 200 --org "$ORG" --canvas "$CANVAS" --json
```

命名和排版保留内容，已有对象的写入检查修订号。明确节点与范围后处理用户要求，不把布局整理扩展为重新生成媒体或修改分享。

## 按任务补充

| 当前任务 | 读取 |
| --- | --- |
| 开启 Ultra Design／全能创作，统筹完整创作项目 | `virse-ultra-design` |
| 在画布共同发展品牌系统，最终交付品牌文件夹 | `virse-brand-center-creator`；本入口承担画布操作 |
| 把资源目录中的多张画布及素材按项目归档或重新分类 | `virse-assets` → `references/organize-library.md` |
| 把当前画布、本地或外部平台的素材汇集成个人或团队资产库 | `virse-assets` → `references/build-library.md` |
| 整理画布、归类收纳、重新分组排版，先理解现状并商定整理方式 | [画布整理](references/organize-canvas.md) |
| 对照品牌标准验收画布作品，并把结果对应到作品 | `virse-creation` → `references/brand-review.md` |
| 从画布自动发现可复用流程，推荐并总结为智能工具 | `virse-smart-tool-creator` → `references/from-canvas.md` |
| 从画布理解视觉偏好、推荐发展方向并总结审美模块 | `virse-aesthetic-creator` → `references/from-canvas.md` |
| 找画布、理解区域、读取文字、成员、连线或生成配置 | [理解与取材](references/read-select.md) |
| 创建画布、节点、组合、连线，修改字段或组合事务 | [编辑对象与关系](references/edit-graph.md) |
| 放入现有素材、执行已明确的排版、复制到当前或另一画布 | [放置、排版与复制](references/layout-copy.md) |
| 创建、回复、编辑、移动或解决画布讨论 | [画布讨论](references/discussions.md) |
| 查询近期删除并恢复媒体 | [媒体恢复](references/recovery.md) |
| 下载素材或把画布媒体打包 | [文件交付](references/shared/contracts/delivery.md) |
| 识别或取用已有审美 | [审美取用](references/shared/context/aesthetics.md)，不先进入作者流程 |

## 完成与恢复

支持幂等键的写入，为新操作使用独立键；恢复同一原操作时才复用。没有幂等合同的创建先查询对账。

核对实际对象、保存字段与修订，复制时核对新身份和内部关系，讨论核对真实状态。连线保存不表示下游任务已经运行，节点删除不等于取消任务或永久删除资产。通用 JSON 写入口没有全量节点字段 Schema，不猜任意类型和属性都可写。

使用[执行与恢复](references/shared/contracts/execution.md)解释未知结果与冲突，并按当前参考保留原内容、目标与请求键。连线没有名称，`canvas edge name` 会被拒绝。
