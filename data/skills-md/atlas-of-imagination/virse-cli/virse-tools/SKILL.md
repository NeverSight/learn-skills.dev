---
name: virse-tools
description: >-
  查找、添加、放置、运行和管理 Virse 已有智能工具，读取固定产物的输入表单、观察控制运行，管理个人列表与作者可见范围。编写或修改执行逻辑、构建发布走 virse-smart-tool-creator。
---
# 使用与管理已有智能工具

<!-- virse:background:start -->
Virse 是 AI native 的创作系统，用画布连接想法、素材、审美、工具与模型，支持图片、视频、3D 和文本。资源目录管理素材与归属，画布组织创作输入、过程与结果。

只读当前任务所需参考，已读且适用的内容沿用，链接不自动加载内容。
<!-- virse:background:end -->

用户指定后端时，在首条远端命令前设置 `VIRSE_BACKEND_URL`。

## 当前任务直达

| 用户正在做什么 | 需要的参考 |
| --- | --- |
| 从画布发现创作流程并总结成新工具 | `virse-smart-tool-creator` → `references/from-canvas.md` |
| 搜索、添加移除、启停收藏、修改作者范围或删除定义 | [查找与管理工具](references/find-and-manage.md) |
| 填输入、固定版本、放置、执行、观察与控制 | [工具运行合同](references/shared/contracts/tool-run.md) |
| 判断产物是否符合要求并交付 | [检查工具结果](references/inspect-results.md)与[文件交付](references/shared/contracts/delivery.md) |
| Schema 明确支持审美输入，需理解其身份或资格 | [审美消费条件](references/shared/context/aesthetics.md) |

先按上表选择当前任务所需参考。查详情、收藏、启停或范围等管理任务不强制读取运行合同或输入 Schema。仅在缺连接、对象或输出概念时直读[连接](references/shared/contracts/connection.md)、[对象](references/shared/context/objects.md)、[执行](references/shared/contracts/execution.md)合同。修改包内容、拉源码、构建或发布时进入作者职责；作者测试未发布 artifact 直接复用运行合同，不必先读整个工具使用入口。

## 固定产物再运行

区分工具定义、正式版本标签、不可变 artifact、画布实例节点与 run。添加到个人列表、启用、放置实例和真正运行是四个不同结果。团队可用不授予源码、编辑或发布权限。

已指定工具时不重复搜索。涉及生成的运行，先确认工具可见配置与执行范围，或沿用适用授权；不把固定工具内部模型当作可选择参数。读取输入 Schema，固定返回的 artifact，再按真实字段 ID 准备 `inputs.json`：

```bash
virse --org "$ORG" --canvas "$CANVAS" --json tool schema "$TOOL"
virse --org "$ORG" --canvas "$CANVAS" --json tool run "$TOOL" --artifact-id "$ARTIFACT" --inputs inputs.json --idempotency-key "$KEY" --wait
```

`ARTIFACT` 来自 Schema 的固定身份，不是 release ID。输入与资格按运行合同核对，不推导通用参考、审美或模型字段。用户只需待运行实例时用 `tool place`，不启动运行。

运行控制与未知结果恢复见运行合同；管理写入使用自身合同，不能把生成的重试方式套到收藏、可见范围或删除上。

## 完成判断

管理任务报告目标工具及对应关系或状态；放置任务报告固定 artifact、实例与未启动状态；执行任务报告运行身份、实际状态和具体产物，并检查内容是否满足本次要求。“添加成功”“运行已受理”“run 成功”“作品经过检查”分别说明。
