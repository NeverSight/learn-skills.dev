---
name: dreamina-canvas-cli-text2voice
description: 当用户要求即梦画布文本转语音、朗读或全能配音（选音色或参考素材）时使用；仅负责 tts 模式的输入、参数校验、草稿与场景验收，公共画布素材、付费运行和恢复由 dreamina-canvas-cli 维护。
license: Complete terms in LICENSE
---

# 即梦画布文本转语音

## When to use
仅处理 文本转语音（tts）。输入：逐字确认的朗读文本；通过 voice list 选择 --voice-name；legacy 形态不传 --model 和 --count。公开版 1.0.3 起，带 --scenario 的场景形态（text-reading 朗读、omni-dubbing 全能配音）允许并要求显式 --model，全能配音可选一个音色或改用 --ref 参考音频。

## 操作契约

| 项目 | 标准 |
|---|---|
| 输入与前置 | 用户确认的提示词、当前模型规格、projectId 及模式所需参考 |
| 副作用 | 不带 --run 的节点写入保存草稿；付费执行走公共 execution 操作 |
| 输出交接 | 返回的 nodeId 与 projectId；生成后另附 submitId 和校验后的资源 |
| 恢复规则 | 恢复使用原 submitId；只有明确 absent + resubmittable 才按原身份恢复提交 |

## Workflow
### Step 1：复用 `dreamina-canvas-cli` 的公共调用契约和已确认 projectId；缺少安装或登录时按名称交给 setup/auth 技能。
### Step 2：从当前模型/音色查询结果校验模式参数，读取 [参数规范](references/parameter-reference.md)。不套用旧 CLI 的 model_version、resolution_type 或 poll。
### Step 3：保存草稿，记录返回的 nodeId；修改已有节点时先读取当前状态，完整替换生成参数和引用，元数据才是稀疏更新。

```bash
# legacy：音色驱动，不传模型
dreamina-canvas --format json node create audio --project-id <projectId> \
  --prompt "<narration>" --mode tts --voice-name <voice-name>

# 全能配音（公开版 1.0.3 起）：显式模型 + 场景，可选音色或参考素材
dreamina-canvas --format json node create audio --project-id <projectId> \
  --prompt "<dubbing script>" --mode tts \
  --model <scenario-capable-model> --scenario omni-dubbing \
  --voice-name <optional-voice> --ref "node:<audioNodeId>"
```

### Step 4：需要生成时交给 `dreamina-canvas-cli` 的 execution 操作：node quote → node confirm → node run。提交前记录稳定 submitId；任务技能不自行批准预算。
### Step 5：交给同一公共技能查询恢复与下载校验，核对本模式的实际产物。超时不换 submitId 重提。

## Rules
- 占位参数必须替换为当前 CLI 返回或用户确认的值；草稿命令不加 --run。
- 不混用其他模式的必填项，批量上限从模型能力查询。
- Never persist tokens, cookies or signed URLs；恢复只保留非敏感身份。
- 缺少配套技能时安装：`npx skills add full-aigc-skills/dreamina-skills --skill <skill-name>`。

## Progressive disclosure（按需读取）

- 需要逐 flag 的必填/取值/冲突规则时，读取 [参数规范](references/parameter-reference.md)。
- 需要从当前 discovery 结果选模型、比例、分辨率或时长时，读取 [模型或音色选择](references/model-guide.md)。
- 需要批量、异步、多项目、迭代等成段工作流时，读取 [常用场景组合](references/workflow-patterns.md)。
- 遇到超时、部分成功或恢复场景时，读取 [异常处理](references/error-recovery.md)。
- 交付前自检时，读取 [验收清单](references/validation-checklist.md)。
- 首次运行看 [成功场景](examples/happy-path.md)；批量/异步/多项目/拒绝越权/失败恢复样例见 `examples/` 目录。

## Validation checklist
- [ ] 输入与 tts 模式一致，参数经过实时发现。
- [ ] 返回的 projectId、nodeId 与 submitId 正确交接，不能将受理视为完成。
- [ ] 输出终态成功，下载后校验媒体类型、字节数和 SHA-256。

## Gotchas
- 节点生成编辑是 full replace，不能丢失原有引用。
- 登录状态、计费权限与生成成功是不同检查。
- 只生成用户要求的数量，不自动追加尝试。

## 不适用与边界

不适用于音乐生成或语音转文字。音乐使用 text2audio；输入文本未经确认时不改写旁白，不凭印象选择或承诺某个音色。

只读取当前操作必要的账户与素材信息；不存储、记录或输出访问令牌、cookie 和临时签名链接。
