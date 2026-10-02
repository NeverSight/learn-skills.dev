---
name: dreamina-canvas-cli
description: 当需要调用即梦画布 dreamina-canvas 的公共操作时使用，包括模型音色发现、画布与素材管理、节点编辑、时间轴、报价确认运行、状态恢复和下载校验；具体生成模式、安装和登录分别交给对应 CLI 技能。
license: Complete terms in LICENSE
---

# 即梦画布 CLI 公共操作

## When to use
跨模式的公共命令和排障使用本技能。安装由 `dreamina-canvas-cli-setup` 负责，账户由 `dreamina-canvas-cli-auth` 负责。六个生成技能各自负责自己的模式和参数，不再建立辅助技能。

## 操作契约

| 项目 | 标准 |
|---|---|
| 输入与前置 | 已选择的公共命令与其所需身份 |
| 副作用 | 模型查询只读；画布/上传/编辑写入；运行可能计费 |
| 输出交接 | JSON data / error、projectId、nodeId、resourceId、submitId |
| 恢复规则 | 未知写入先核对身份，不能用新 ID 绕过结果不明 |

## Workflow
### Step 1：运行 `dreamina-canvas --help`、`dreamina-canvas version`、`dreamina-canvas schema`，读取当前操作对应的契约。
### Step 2：按需读取下表一个操作文档；核对输入、输出和副作用，再构造 argv。
### Step 3：保存草稿和上传不代表批准生成；付费前读取 execution，已有任务读取 recovery。
### Step 4：按 `--format json` 分离 stdout/stderr，依据 requiredAction 恢复。exit code 20 使用原 submitId 续查。
### Step 5：记录终态与产物校验；未运行的阶段明确报告。

## Progressive disclosure（按需读取）：原子操作索引
- 构造 argv、判定 stdout/stderr、持久化身份或交付前核对时，读取 [参数构造、输出、身份与验收](references/command-contract.md)。
- 选模型/音色、查比例、分辨率、时长白名单时，读取 [模型、音色及能力发现](references/discovery.md)。
- 新建画布、切换当前画布或按 projectId 跨进程续作时，读取 [画布创建与列表](references/canvas.md)。
- 上传本地素材、查询产物或下载并校验哈希时，读取 [素材上传、查询与下载](references/resources.md)。
- 编辑图片节点或处理 node:/res: 引用时，读取 [图片节点共享机制与编辑](references/image-node.md)。
- 编辑视频节点或处理模式与引用时，读取 [视频节点共享机制与编辑](references/video-node.md)。
- 创建/编辑音频节点（tts、music 字段互斥）时，读取 [音频节点共享机制与编辑](references/audio-node.md)。
- 需要 Text/Element 节点、节点查找或 DAG 依赖顺序时，读取 [Text、Element、节点查找及依赖顺序](references/composition.md)。
- 排时间轴、替换轨道或装配音视频时，读取 [时间轴及轨道替换](references/timeline.md)。
- 需要报价、用户批准、提交生成或批量身份时，读取 [报价、确认、运行与批次身份](references/execution.md)。
- 任务在跑、本地等待超时或需要按原身份恢复时，读取 [查询、等待与恢复](references/recovery.md)。
- 一次要串联“查模型→建画布→传素材→引节点”时，读取 [准备画布和素材的组合场景](references/preparation.md)。
- 命令非零退出、需要判定下一步动作时，读取 [退出码与 requiredAction](references/error-routing.md)。

## 场景示例
- [创建画布](examples/canvas-happy-path.md)
- [准备素材](examples/preparation-happy-path.md)
- [素材上传与下载](examples/resources-happy-path.md)
- [报价确认运行](examples/execution-happy-path.md)
- [查询恢复](examples/recovery-happy-path.md)
- [图文元素组合](examples/composition-happy-path.md)
- [时间轴](examples/timeline-happy-path.md)

## Rules
- 一个命令的规范只维护在对应 references；示例用于组合，不定义第二套参数契约。
- 安装缺失的同包技能：`npx skills add full-aigc-skills/dreamina-skills --skill <skill-name>`。按名称交接，不读取相邻安装目录。
- 不存储凭据，不代替用户批准积分，不把不确定提交当作失败重新提交。

## Validation checklist
- [ ] 参数与当前 schema 一致；projectId/nodeId/submitId 各自正确。
- [ ] 草稿、已提交、成功完成和已下载分别有证据。
- [ ] 异常恢复复用身份，文件字节数与 SHA-256 验证。

## Gotchas
- 等待超时不取消服务端任务。
- 编辑生成参数可能清除未传的引用；时间轴替换会重建轨道，先检查现有内容。
- `--yes` 不能替代具体请求的积分批准。

## Progressive disclosure（按需读取）：补充契约与清单
- 需要 audio 字段与模式互斥的完整契约时，读取 [audio-node-audio-node-contract](references/audio-node-audio-node-contract.md)。
- 多 profile 下画布上下文与身份归属不清时，读取 [canvas-canvas-context](references/canvas-canvas-context.md)。
- 需要 CLI 全量命令族的种子契约（版本、flag、退出码）时，读取 [cli-contract](references/cli-contract.md)。
- 需要节点依赖顺序与 DAG 调度细节时，读取 [composition-composition-dag](references/composition-composition-dag.md)。
- 需要完整能力发现字段与边界说明时，读取 [discovery-capability-discovery](references/discovery-capability-discovery.md)。
- 错误难以归类或需要恢复剧本时，读取 [error-recovery](references/error-recovery.md)。
- 需要积分上限、批准语义与批次身份细节时，读取 [execution-credit-approval](references/execution-credit-approval.md)。
- 需要 image 节点字段与引用机制的完整契约时，读取 [image-node-image-node-contract](references/image-node-image-node-contract.md)。
- 需要任务恢复状态机的完整转移时，读取 [recovery-recovery-state-machine](references/recovery-recovery-state-machine.md)。
- 需要产物字节数与 SHA-256 验证细则时，读取 [resources-artifact-verification](references/resources-artifact-verification.md)。
- 需要 resource upload 标志位与幂等细节时，读取 [resources-resource-upload](references/resources-resource-upload.md)。
- 需要时间轴轨道与剪辑参数完整契约时，读取 [timeline-timeline-contract](references/timeline-timeline-contract.md)。
- 交付前逐项核对时，读取 [validation-checklist](references/validation-checklist.md)。
- 需要 video 节点模式与引用机制的完整契约时，读取 [video-node-video-node-contract](references/video-node-video-node-contract.md)。
- 需要本技能级工作流契约（状态、交接、授权）时，读取 [workflow-contract](references/workflow-contract.md)。

## 不适用与边界

具体生成模式不适用本入口作为第二套参数规范；请选择六个对应任务技能。安装与登录分别交给 setup/auth，不因一次只读命令失败就自动重装或切换账户。

只读取当前操作必要的账户与素材信息；不存储、记录或输出访问令牌、cookie 和临时签名链接。
