---
name: pytrio-skill
description: 使用 PyTRIO 编写、调试或解释远程大模型训练与推理代码。用户提到 pytrio、TRIO、PyTRIO SDK、ServiceClient、TrainingClient、SamplingClient、LoRA 训练、SFT、异步 SFT、PyTRIO-Jev、PyTRIO Decision Model 决策模型、多模态推理、多模态训练、Vision GRPO、视觉 RLVR、ImageChunk、RL、GRPO、OPD、Search-R1、ReTool、DAPO、GSPO、ALFWorld、TextWorld、Agentic RL、OPSD、On-Policy Self-Distillation、DPO、custom loss、自定义损失函数、forward_backward_custom、forward_backward_custom_async、工具调用强化学习、HuggingFace datasets、PyTRIO OpenAI 兼容 API、SwanLab 训练记录、权重保存、checkpoint 或远程 LLM 后训练时使用。
metadata:
  version: "0.2.3"
---

# PyTRIO Skill

PyTRIO 是远程大模型后训练和推理服务的 Python SDK。本地代码负责准备数据和控制训练循环；前向传播、反向传播、优化器更新、采样和权重存储由 PyTRIO 服务执行。

## 安装与更新

安装这个 skill：执行 `npx skills add SwanHubX/pytrio-skill -g -y`，它会安装到当前用户级别的 `.agents/skills` 并供支持 Agent Skills 的 CLI 使用。
更新这个 skill：执行 `npx skills update pytrio-skill -g -y`，更新后重新启动或刷新 Agent 会话即可使用新版本。

使用 Skill 生成或调试代码前，建议先确认 PyTRIO SDK 为最新版：未锁定依赖时执行 `python -m pip install --upgrade pytrio`，再用 `python -c 'from importlib.metadata import version; print(version("pytrio"))'` 记录实际版本。若项目的 `pyproject.toml`、requirements 或 lockfile 已固定 PyTRIO 版本，不要擅自升级；应以项目锁定版本为准，并检查该版本的 API 签名。

## 使用定位

PyTRIO 代码通常由本地 Python 负责数据准备、训练循环和实验记录，由 PyTRIO 服务负责模型前向、反向、优化器更新和权重保存。

处理训练任务时，先按任务形态选择对应的 `Datum` 构造、loss 和 client 调用方式：

- SFT：监督微调、assistant-only loss mask、同步/异步训练、SwanLab 记录。
- Decision Model / PyTRIO-Jev：固定候选决策、marker 位置的稀疏 SFT、候选概率推理与温度校准。
- 多模态：图文 `ModelInput`、`ImageChunk.expected_tokens`、多模态推理/SFT、Vision GRPO。
- GRPO：student rollout、reward、group-relative advantage、`importance_sampling` 更新。
- OPD：student rollout、teacher logprob、reverse-KL advantage、`importance_sampling` 更新。
- Search-R1：多轮搜索工具环境、结果 reward、group-relative advantage、observation mask。
- ReTool：多轮代码解释器环境、outcome reward、执行结果 mask、本地执行隔离。
- OPSD：同一初始模型的 Student / privileged Teacher、自轨迹逐 token reverse-KL。
- DAPO：Dynamic Sampling、Clip-Higher、token mean、Soft Overlong、自定义 PPO loss。
- GSPO：序列级重要性比率、序列级裁剪、`forward_backward_custom`。
- ALFWorld：同游戏独立环境、长轨迹工具交互、终局 reward、PPO 更新。
- Custom loss：本地 PyTorch objective、闭包元数据、`forward_backward_custom` / async 和 surrogate gradient。
- DPO：chosen/rejected 偏好数据、reference logprob、pairwise custom loss。

示例代码提供可改模板；关键字段和常见错误在 `references/` 中说明。

## 使用顺序

1. 先按“安装与更新”确认项目使用的 PyTRIO SDK 版本；未锁定依赖时建议使用最新版，已锁定时尊重项目版本。
2. 判断任务类型：SFT、Decision Model、多模态推理/训练、Vision GRPO、GRPO、OPD、Search-R1、ReTool、OPSD、DAPO、GSPO、ALFWorld、custom loss、DPO、推理/保存权重，或 API 调试。
3. 按任务路由读取对应 reference 和 example；不要一开始展开全部官方文档。
4. 示例能覆盖时，按示例替换数据集、prompt、reward、teacher/student 模型、超参数和 SwanLab 配置。
5. 示例覆盖不了、API 行为不确定、报错难定位，或需要 checkpoint/OpenAI 兼容 API 等细节时，再读 `references/doc-index.md`，根据任务打开对应官方 Markdown 文档。
6. 若官方文档和本地 SDK 行为不一致，先检查已安装 SDK 签名或写最小复现，再给最终代码。

## 任务路由

| 用户任务 | 读取内容 |
|---|---|
| 安装、登录、第一次训练或推理 | `references/doc-index.md` -> 快速开始 |
| 编写简单 SFT 训练代码 | `references/sft.md`；`examples/quickstart_sft.py` |
| 编写角色 SFT 或 Chat-甄嬛类微调 | `references/sft.md`；`references/chat-huanhuan.md`；`examples/chat-huanhuan.py` |
| 编写异步 SFT 或异步记录 SwanLab | `references/sft.md`；`examples/chat-huanhuan-async.py` |
| 编写多轮对话 SFT 蒸馏 | `references/sft.md`；`examples/sft-distill-conversation.py` 或 `examples/sft-distill-conversation-async.py` |
| 用 PyTRIO 训练 Decision Model / PyTRIO-Jev / 固定候选分类或工单路由 | `references/decision-model.md`；完整项目读取其中的源码目录 |
| 调试决策位置 mask / 候选概率推理 / 决策模型温度校准 | `references/decision-model.md`；按问题读取完整案例的 data、inference、calibrate 或 eval |
| 编写多模态推理 / 图像输入 / 多模态 SFT | `references/vision.md`；API 细节再读 `references/doc-index.md` -> 多模态 |
| 编写 Vision GRPO / GeoQA / 视觉 RLVR | `references/vision.md`；`examples/vision-grpo.py`；需要固定评测时读取其中的完整源码目录 |
| 编写 GRPO / GSM8K / reward-based RLVR | `references/grpo.md`；`examples/grpo-gsm8k.py` 或 `examples/grpo-gsm8k-async.py` |
| 编写 OPD / Medical OPD / multi-teacher / teacher-KL 蒸馏 | `references/opd.md`；`examples/opd-deepmath.py` 或 `examples/opd-deepmath-async.py` |
| 编写 Search-R1 / Agentic RL / 多轮搜索工具训练 | `references/search-r1.md`；完整项目读取其中的源码目录 |
| 编写 ReTool / 代码解释器 Agent / code-interlaced RL | `references/retool.md`；完整项目读取其中的源码目录 |
| 编写 OPSD / On-Policy Self-Distillation / privileged teacher | `references/opsd.md`；完整项目读取其中的源码目录 |
| 编写 DAPO / Dynamic Sampling / Clip-Higher / Soft Overlong | `references/dapo.md`；完整项目读取其中的源码目录 |
| 编写 GSPO / sequence-level ratio / sequence clipping | `references/gspo.md`；完整项目读取其中的源码目录 |
| 编写 ALFWorld / TextWorld / 长轨迹环境 Agentic RL | `references/alfworld.md`；完整项目读取其中的源码目录 |
| 编写通用自定义损失函数 / `forward_backward_custom` / async | `references/custom-loss.md` |
| 编写 DPO / preference training | `references/custom-loss.md`；`references/dpo.md`；`examples/dpo-hh-rlhf.py` |
| 接入 HuggingFace datasets | `references/doc-index.md` -> HuggingFace datasets |
| 编写推理或采样代码 | `references/doc-index.md` -> 推理、SamplingClient、SamplingParams |
| 保存用于推理的权重 | `references/doc-index.md` -> 训练、TrainingClient、保存/续训、下载权重 |
| 从 checkpoint 恢复训练 | `references/doc-index.md` -> 保存/续训、ServiceClient、TrainingClient |
| 使用 OpenAI 兼容 API | `references/doc-index.md` -> OpenAI API |
| 加入 SwanLab 训练记录 | 优先看同类 example；需要查询实验时同时使用 swanlab-skill |

## 核心规则

- 使用 `import pytrio as trio` 导入。
- 创建 client 前先用 `trio login` 或 `trio login -k <API_KEY>` 完成认证。CLI 命令是 `trio`，不是 `pytrio`。
- 使用 `trio.ServiceClient()` 作为主入口。
- 纯文本 `Datum.model_input` 和 `SamplingClient.sample(prompt=...)` 使用 `trio.ModelInput.from_ints(...)`；多模态输入显式构造包含文本与图片 chunk 的 `trio.ModelInput(chunks=[...])`。
- 采样参数传 `trio.SamplingParams(...)` 对象，不要传普通 dict。
- 同步远程调用通常返回 future，需要调用 `.result()` 取得结果。
- 异步 API 有两种返回边界：`sample_async()`、`compute_logprobs_async()`、`save_weights_and_get_sampling_client_async()` 通常一次 `await` 直接得到结果；`forward_backward_async()`、`optim_step_async()` 的第一次 `await` 返回 `APIFuture`，还要再次 `await` 该 future 才算远程任务完成。始终以当前 SDK 签名为准。
- `ServiceClient`、`TrainingClient`、`SamplingClient` 都没有 `close()` / `close_async()` 等显式关闭方法；训练结束、保存权重后直接退出即可，不要自行添加 client 清理调用。
- SFT 默认手动做自回归右移，除非明确使用 `auto_shift=True`：`model_input=tokens[:-1]`、`target_tokens=tokens[1:]`、`weights=weights[1:]`。
- SFT 用 `weights` 屏蔽 prompt token，不要使用 HuggingFace 风格的 `-100` labels。
- Decision Model 使用 `cross_entropy` 做稀疏监督：输入保留 marker 骨架，仅在 marker 前一位置设置正确候选 target 和非零 weight。训练与推理共用模板、marker 定位和候选映射，细节见 `references/decision-model.md`。
- 多模态能力要求 `pytrio>=0.2.7`。先确认基模支持图片输入，再按模型 chat template 的真实顺序组织 `EncodedTextChunk` 与 `ImageChunk`；不要把 Qwen 的特殊 token 或 `<|image_pad|>` 规则直接套到其他模型。
- `ImageChunk.data` 传原始图片字节，`format` 与真实编码保持一致。多模态训练和任何依赖本地序列长度的对齐都要用匹配远端模型的 image processor 计算 `expected_tokens`，不要写死视觉 token 数。
- chat template 已写入特殊 token 时，拆分图片占位符后的文本使用 `add_special_tokens=False` 编码。采样后校验 `response.input_tokens == len(prompt)`，长度不一致时停止训练并修正 image processor 或 chunk 顺序。
- 多模态 SFT 与 Vision GRPO 都保留完整图文 prompt，并只拼接 `completion[:-1]`；prompt/image 区间从 `prompt_length - 1` 开始右移对齐。SFT 的 `target_tokens`/`weights` 在该区间填零，Vision GRPO 的 `target_tokens`/old `logprobs`/`advantages` 在该区间填零。
- GRPO、OPD、Search-R1 和 OPSD 通常使用 `loss_fn="importance_sampling"`，`Datum.loss_fn_inputs` 必须包含右移对齐后的 `target_tokens`、旧策略 `logprobs` 和 `advantages`。
- `importance_sampling` 的 prompt/observation 区间不训练时，用 `target_tokens=0`、`logprobs=0.0`、`advantages=0.0` 占位，保证长度和 `model_input` 一致。
- GRPO 的 advantage 来自同一 prompt 的 group 内 reward 相对均值；如果整组 reward 完全相同，advantage 全为 0，通常跳过该组。
- OPD 的 teacher 只对 student 实际采样出来的 completion 计算 logprob；不要用 teacher 自己生成的 completion 替代 student 轨迹。
- Search-R1 的 tool observation 进入后续上下文但不进入 loss；先在完整同题 group 内计算 advantage，再拆 micro-batch 累积梯度，搜索后端本身不参与训练。
- ReTool 的代码执行结果进入后续上下文但不进入 loss；保持真实 token 前缀连续。本地 subprocess 只能限制资源，处理不可信模型代码时使用容器或专用沙箱，并移除环境凭证。
- OPSD 的 Student 和 Teacher 来自同一初始模型；Teacher 固定在 step 0，通过包含参考解答的 privileged prompt 对 Student completion 计算 logprob，参考解答不是 SFT label。
- DAPO 使用 `forward_backward_custom` 实现非对称 PPO clip 和 token-level reduction；Dynamic Sampling 被丢弃的候选也要计入 token 与 wall-clock 成本。
- GSPO 的 sequence ratio 是 completion token 概率比的几何平均；只裁剪一次完整序列比率，prompt token 不参与 ratio。
- ALFWorld 的同组轨迹必须来自同一个游戏和相同初始 observation，同时持有独立环境状态；环境 observation token 的 advantage 为 0。
- Custom loss 的函数签名是 `loss_fn(data, logprobs) -> (loss, metrics)`；函数在本地用 torch 执行，返回的 loss 必须保留 autograd 计算图。
- `forward_backward_custom` 的 `Datum.loss_fn_inputs` 只放与 `model_input` 等长的 `target_tokens`；sampling/reference logprob、mask、advantage、分组和归一化参数使用每个 batch 独立的闭包传入。
- Custom loss 回调中不要采样、访问网络或调用其他 PyTRIO client。异步版第一次 `await` 返回 `APIFuture`，第二次 `await` 才等待远程任务完成。
- DPO 使用 `forward_backward_custom(data, loss_fn)` 完成 pairwise objective；不要用 `cross_entropy` 或 `importance_sampling` 代替。
- DPO batch 保持 `[chosen_0, rejected_0, chosen_1, rejected_1, ...]` 顺序，reference logprobs 要提前计算并通过闭包传给 custom loss。
- 推理用权重保存使用 `save_weights_for_sampler()`；完整断点续训使用 `save_state()`。
- 模型名优先使用当前官方文档或 `client.get_supported_models()` 返回值，不要硬编码旧模型名。
- 训练脚本建议默认接入 SwanLab。SFT 记录 loss；Decision Model 记录按监督位置归一化的 loss、supervised tokens，并单独评测 Accuracy、ECE、Brier；Vision GRPO 记录 reward、format rate、degenerate group 比例、completion 长度和 trainer metrics；GRPO 记录 reward、degenerate group 比例和 trainer metrics；OPD/OPSD 记录 reverse KL、completion token 数和 trainer metrics；Search-R1 记录 format、search success/error、turns 和 search calls；ReTool 记录 tool-call、sandbox 与轨迹指标；DAPO 记录候选/有效组、token 利用率和 refill 时间；GSPO 记录 sequence ratio、clip 与原始分母；ALFWorld 记录成功率、非法动作、环境步数和 prefill/训练成本；DPO 记录 loss、accuracy、margin、chosen/rejected reward。

## 代码骨架

先用本地 reference + example 解决问题；示例不够时，再读官方文档补足 API 细节。若官方文档和本地 SDK 行为不一致，先检查已安装 SDK 签名或写最小复现。

Decision Model 的稀疏监督构造见 `references/decision-model.md`。下面是普通生成式 SFT 的 assistant-only `weights` 与自回归右移：

```python
tokens = prompt_tokens + completion_tokens
weights = [0.0] * len(prompt_tokens) + [1.0] * len(completion_tokens)
datum = trio.Datum(
    model_input=trio.ModelInput.from_ints(tokens[:-1]),
    loss_fn_inputs={
        "target_tokens": np.asarray(tokens[1:], dtype=np.int32),
        "weights": np.asarray(weights[1:], dtype=np.float32),
    },
)
training_client.forward_backward([datum], loss_fn="cross_entropy").result()
```

GRPO/OPD 都用 `importance_sampling`，区别只在 advantage 来源：

```python
obs_len = len(prompt_tokens) - 1
datum = trio.Datum(
    model_input=trio.ModelInput.from_ints(prompt_tokens + completion_tokens[:-1]),
    loss_fn_inputs={
        "target_tokens": np.asarray([0] * obs_len + completion_tokens, dtype=np.int64),
        "logprobs": np.asarray([0.0] * obs_len + old_logprobs, dtype=np.float32),
        "advantages": np.asarray([0.0] * obs_len + advantages, dtype=np.float32),
    },
)
training_client.forward_backward([datum], loss_fn="importance_sampling").result()
```

- GRPO：`advantages = reward - mean(group_rewards)`，old logprobs 来自同组 rollout 的 student sampler。
- Vision GRPO：沿用 GRPO 的 reward 与 advantage；把纯文本 prompt 换成有正确 `expected_tokens` 的图文 chunks，并按 `references/vision.md` 对齐 prompt/image 零占位。
- OPD：teacher 对 `prompt + student_completion` 调 `compute_logprobs`，`advantages = -kl_coef * (student_logprobs - teacher_logprobs)`。
- OPSD：沿用 OPD 的逐 token advantage，但 teacher 是同一初始模型，并通过 privileged prompt 看到参考解答。
- Search-R1：沿用 GRPO 的轨迹级 advantage；assistant token 使用 rollout old logprob 和 trajectory advantage，tool observation token 的 logprob/advantage 都填 0。
- ReTool：沿用多轮 observation mask，最终答案给 outcome reward；本地代码执行器属于环境，不参与训练。
- DAPO：用 custom PPO loss 同时实现 Clip-Higher 和 token mean；Dynamic Sampling 与 Soft Overlong 在 rollout/reward 层完成。
- GSPO：用 custom loss 对 completion 计算一个 sequence ratio，再做序列级裁剪。
- ALFWorld：按同一游戏计算轨迹级 advantage；assistant action token 参与 PPO，环境 observation token 全部 mask。

通用 custom loss 的 Datum 只放服务端 forward 所需的 `target_tokens`，算法元数据通过闭包传入；完整契约见 `references/custom-loss.md`。DPO 的 pairwise loss 形态如下：

```python
def loss_fn(data, logprobs_list):
    # data、reference_logprobs、response_masks 保持 chosen/rejected 同序。
    loss = compute_dpo_loss(logprobs_list, reference_logprobs, response_masks)
    return loss, {"dpo/loss": float(loss.detach().item())}

training_client.forward_backward_custom([chosen, rejected], loss_fn).result()
```

每次 `forward_backward*` 后调用 `training_client.optim_step(trio.AdamParams(...))`；保存推理权重使用 `save_weights_for_sampler(...).result()`。
