---
name: virse-assets
description: 汇集本地和其他平台素材，构建或整理个人、团队资产库；查找、上传替换、批量导入、恢复、下载打包与查阅已有审美。画布内部布局走 virse-canvas，访问与分享走 virse-sharing。
---

# 资产管理

<!-- virse:background:start -->
Virse 是 AI native 的创作系统，用画布连接想法、素材、审美、工具与模型，支持图片、视频、3D 和文本。资源目录管理素材与归属，画布组织创作输入、过程与结果。

只读当前任务所需参考，已读且适用的内容沿用，链接不自动加载内容。
<!-- virse:background:end -->

用户指定后端时，在首条远端命令前设置 `VIRSE_BACKEND_URL`。

## 对象与短路径

按用户指定的组织处理资源。资源路径是该组织内的绝对目录路径，`/` 是组织根；资源项 ID、资产 ID、画布空间 ID 是不同身份。缺少连接或身份时读[连接与空间](references/shared/contracts/connection.md)，身份不明确时读[对象关系](references/shared/context/objects.md)。已有上下文足够时直接做任务。

普通查找可以直接用：

```bash
virse resource ls '/项目素材' --org "$ORG" --json
virse resource search '产品' '/' --kind image --org "$ORG" --json
virse resource get "$RESOURCE" --org "$ORG" --json
```

示例变量均替换为本次真实查询或用户明确给出的身份。列表未读完不作全集判断；遇到同名候选先辨明对象，不选第一个。已知资源路径时优先使用它的读取、预览或下载入口，不猜 asset ID。

跨来源汇集素材、构建个人或企业素材库先读[资产库构建](references/build-library.md)。已有整库或多目录的归类收纳读[资产库整理](references/organize-library.md)，理解范围与内容后，与用户敲定详细方案再执行；具体对象与调整方式已明确时按用户指令处理。

上传一个文件：

```bash
virse resource upload ./product.png '/项目素材' --conflict rename --idempotency-key "$KEY" --org "$ORG" --json
```

先确认这是新增还是替换。上传返回资源和资产，不自动放入画布。需要组织大量本地文件时使用持久导入批次；要替换原件时先读取内容修订号。文件格式、恢复与同名策略见[上传与替换](references/upload-replace.md)。

## 按任务补充

| 当前任务 | 读取 |
| --- | --- |
| 开启 Ultra Design／全能创作，统筹完整创作项目 | `virse-ultra-design` |
| 共建品牌叙事、规范和应用，交付或核对品牌文件夹 | `virse-brand-center-creator`；仅归档已有品牌资料沿用本入口 |
| 从本地、其他平台或项目汇集素材，迁入并组织成方便取用的个人或团队资产库 | [资产库构建](references/build-library.md) |
| 整理资产库、商定分类收纳方案、保存现状，或按记录评估撤回本次整理 | [资产库整理](references/organize-library.md) |
| 找到素材、浏览目录、判断来源与身份 | [查找与读取](references/browse.md) |
| 建目录、改名移动、复制、置顶收藏、排序、移除外部入口或画布另存 | [整理与归档](references/organize.md) |
| 上传单文件或保留身份替换原件 | [上传与替换](references/upload-replace.md) |
| 导入目录、查看进度、暂停取消或恢复未确认项 | [导入批次](references/import-batches.md) |
| 查看回收站、恢复或永久清理 | [回收与清理](references/recycle.md) |
| 跟踪资源变化或从快照接续增量 | [资源变化](references/resource-changes.md) |
| 查看预览、下载原件、断点续传或打包 ZIP | [文件交付](references/shared/contracts/delivery.md) |
| 读取或复用审美资源 | [审美取用](references/shared/context/aesthetics.md)，不先读完整作者流程 |

资源移动可能改变继承权限；设置分享规则属于 `virse-sharing`。要把资产放入画布、布局或建立连线，按 `virse-canvas` 的职责继续，不要求安装全部兄弟 Skill。

## 完成与恢复

支持幂等键的写入，为新操作使用独立键；恢复同一原操作时才复用。没有幂等合同的创建先查询对账。

回报实际资源身份、最终位置和逐项结果；有本地交付时确认文件与清单。不能把 `skip` 当作字节一致、把部分成功当作全部完成、把收藏或隐藏入口当作权限变更。任务只要求整理时，不额外生成内容或扩大分享范围。

按[执行与恢复](references/shared/contracts/execution.md)解释回执、退出码和未知结果，再用当前任务参考中的具体恢复方式；不统一套用重试循环。
