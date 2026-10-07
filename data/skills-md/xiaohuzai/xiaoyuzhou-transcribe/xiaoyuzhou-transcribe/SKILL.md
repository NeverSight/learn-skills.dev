---
name: xiaoyuzhou-transcribe
description: "小宇宙 (XiaoyuzhouFM) 播客转写 skill. 端到端把播客链接转成带说话人标注的完整转写 + 主题分组结构化总结的 markdown. 设计原则: skill 是提示 + 工具, 机械部分用 bash/python, AI 总结部分由 agent 自己的 LLM 完成."
version: 1.2.0
license: MIT
source_repo: https://github.com/xiaohuzai/xiaoyuzhou-transcribe
related_skills:
  - media-transcription   # orchestrates YouTube/B站/小宇宙; delegates 小宇宙 ASR/diarization work HERE
triggers:
  - 小宇宙链接
  - xiaoyuzhoufm.com/episode/
  - 播客转写
  - 音频转文字
  - podcast to markdown
---

# xiaoyuzhou-transcribe

小宇宙 (xiaoyuzhoufm.com) 播客转写 skill。**这是给 LLM agent 用的**。

## 上游与定位

- **上游仓库**: <https://github.com/xiaohuzai/xiaoyuzhou-transcribe> (MIT, 公开)
- **本地副本**: `~/.hermes/skills/media/xiaoyuzhou-transcribe/`
- **跨 agent 安装**: `hermes skills install <SKILL.md URL>` (Hermes) / `git clone ... ~/.claude/skills/...` (Claude Code) / 同理 Cursor / Codex
- **被委托关系**: 当用户给的是小宇宙链接 + 想要完整转写（不是 show notes 摘要），`media-transcription` orchestrator 会路由到这里来跑 pipeline.sh。本 skill 是深路径（ASR + 说话人识别），`media-transcription` §3 是浅路径（web scrape 摘要）。
- **凭据安全**: `DASHSCOPE_API_KEY` 不在仓库里，从以下位置加载（按优先级）: 环境变量 → `~/.config/xiaoyuzhou-transcribe/.env` → `~/.hermes/.env`

## 设计原则

| 步骤 | 谁做 | 怎么干 |
|------|------|--------|
| **Step 1: ASR 转写** | bash 工具 | `transcribe_async.sh` 调 DashScope 异步 API |
| **Step 2: 格式化** | python 工具 | `format_transcript.py` 说话人 + 时间戳 + 分段 |
| **Step 3: LLM 总结** | **agent (你)** | 用 `references/ai-summary-prompt.md` 拼 prompt，**调用你自己**的 LLM |

**本 skill 不替你调 LLM**。你的 agent 拿到 Step 1+2 的 Part A 后，**自己用 prompt 模板 + 自己的 LLM 生成 Part B**。

## 快速开始（agent 视角）

```bash
# 1. 跑机械部分, 拿到 Part A
bash scripts/pipeline.sh "https://www.xiaoyuzhoufm.com/episode/xxx"
# 输出: /tmp/xy_pipeline_<ts>/transcript_formatted.md

# 2. 读 Part A, 用 prompt 模板调 LLM 生成 Part B
# 读 references/ai-summary-prompt.md 拿 prompt 模板
# 拼装 prompt, 调你的 LLM (Anthropic / OpenAI / Gemini / 任何都行)

# 3. 拼装 Part A + Part B 成最终 transcript.md
# 4. 给用户 (粘 Notion / Obsidian / 飞书 web / Word / 任何下游)
```

**端到端**: 60 分钟播客，机械部分 ~70 秒（ASR）+ <1 秒（格式化），LLM 总结看你模型速度。

## 详细工作流

### Step 1: ASR 转写（bash）

`scripts/transcribe_async.sh` 调 DashScope 异步 URL 模式 (`qwen3-asr-flash-filetrans`)：

- 传音频公网 URL 给云端处理（**不下载到本地**）
- 支持 ≤ 8 小时长音频
- 输出 JSON 含 `sentences[]` 毫秒级时间戳

**协议详情**: `references/dashscope-async-filetrans.md`

### Step 2: 格式化（python）

`scripts/format_transcript.py`：

- 关键词表驱动说话人识别（`speakers/<podcast>.json`）
- `[MM:SS]` 时间戳标注
- 300 字自动分段

**说话人识别细节**: `references/speaker-detection-strategies.md`

### Step 3: LLM 总结（agent）

读 `references/ai-summary-prompt.md` 拿 prompt 模板。模板说明：

- 输入：Part A transcript + 节目元数据
- 输出：Part A 修正版 + Part B 结构化总结
- 设计要点：说话人标注、错误修正、主题分组、关键金句、Q&A

**LLM 选什么自己定**——本 skill 不限制。

## 核心脚本

| 路径 | 作用 | 跑在 |
|------|------|------|
| `scripts/pipeline.sh` | **机械部分 wrapper**: Step 1+2 + 输出 Part A | bash |
| `scripts/transcribe_async.sh` | Step 1: DashScope 异步 ASR | bash |
| `scripts/format_transcript.py` | Step 2: 说话人 + 时间戳 + 分段 | python |
| `scripts/fix_monolog_speakers.py` | **Step 2.5**: 嘉宾主导型播客的说话人修正（自动分段 + 主持人提问检测）| python |
| `references/ai-summary-prompt.md` | Step 3: 给 LLM 的 prompt 模板 | **agent (你)** |
| `speakers/silicon101.json` | 关键词表示例（泓君/傅盛/徐老师）| 配置文件 |

## ASR 模式

### 模式 A: DashScope 异步 URL（默认, 唯一推荐）

- **API**: `POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription`
- **模型**: `qwen3-asr-flash-filetrans`
- **核心优势**: 传公网 URL 给云端，**不下载到本地**、**不走 VAD 切片**、**不消耗 CPU**、**不受 server→CDN 速度影响**
- **支持时长**: ≤ 8 小时
- **输出**: `sentences[]` 含毫秒级 `begin_time / end_time / language / emotion`

### 模式 B: 本地 Toolkit 同步（兜底）

仅适用于音频**已经是本地文件**的场景（其他机器 scp 过来、用户提供的录音）：

```bash
# 用户自己装 qwen3-asr (任选一种):
#   pip install qwen3-asr-toolkit
#   或从 https://github.com/QwenLM/Qwen3-ASR-Toolkit 装

qwen3-asr \
  --input-file /tmp/<audio> \
  --dashscope-api-key "$DASHSCOPE_API_KEY" \
  --num-threads 2 --save-srt
```

## 说话人检测（关键词表）

`format_transcript.py` 读取 `speakers/<podcast>.json` 关键词表，匹配"我是XXX"等自我介绍段切换 speaker。

**添加新播客**: 复制 `silicon101.json` 改名字 + 关键词列表即可。

JSON 格式：

```json
{
  "_comment": "嘉宾关键词表, _ 前缀字段自动跳过",
  "_usage": "format_transcript.py raw.json out.md --speakers this.json",
  "泓君": ["我是红军", "泓君", "大家好欢迎收听硅谷101"],
  "傅盛": ["我是傅盛", "傅盛你好", "傅盛总"]
}
```

**注意**: `_comment` / `_usage` 等 `_` 前缀的 key 必须以 `_` 开头，否则会被当人名匹配。

## 已知限制

1. **Step 1 文件 URL 必须公网可达**: 私网 / 鉴权 URL 失败。小宇宙 `media.xyzcdn.net` 公开 URL 没问题。
2. **小宇宙 mediaKey 过期**: 签名 URL 含时间戳，几个月前链接 404，需重新从 HTML 提取。
3. **无 speaker diarization**: 所有 ASR 方案均不支持，靠关键词表 + LLM 推断说话人。
4. **关键词表说话人识别有限**: 仅识别**自我介绍段**（"我是XXX"），对话中段只能标"主持人"或保留上次识别。需要 LLM 第二阶段处理才能完整归类。
5. **嘉宾主导型播客陷阱** ⚠️: 商业访谈类节目（如张小俊、晚点 LatePost）主持人只问 5-8 个问题，嘉宾连续讲 30-50 分钟——机械 Step 2 输出会**全标"主持人"**。详见 `references/speaker-detection-strategies.md` 末尾「嘉宾主导型访谈的说话人陷阱」章节。**可执行修复**：`scripts/fix_monolog_speakers.py <transcript_formatted.md> <host_name> <guest_name>` —— 在 Step 2 之后、Step 3 之前跑一遍，自动按"自我介绍锚点分段 + 主持人提问检测 + 主持人结束锚点分段"重新打标，再用 `HOST_SEGMENT_OVERRIDES` dict 手动覆盖没识别出来的提问段（运行一次后目测再 patch dict 重跑）。
6. **B站/YouTube 不在本 skill 范围**: 本 skill 专攻小宇宙链接。

## 依赖

**机械部分（agent 不需要装 LLM 也能跑 Step 1+2）**:

```bash
# 系统
curl, jq

# Python (format_transcript.py 仅用标准库)
python3 ≥ 3.8

# 凭据
# DASHSCOPE_API_KEY 从以下位置加载 (跨 agent 兼容):
#   1. 环境变量
#   2. ~/.config/xiaoyuzhou-transcribe/.env (推荐, 跨 agent)
#   3. ~/.hermes/.env (Hermes Agent 兼容)
# 申请: https://dashscope.console.aliyun.com/apiKey
```

**LLM 总结（agent 自己的）**: 不限制，Anthropic / OpenAI / Gemini / 本地模型都支持。

## 参考

- Qwen3-ASR Toolkit: https://github.com/QwenLM/Qwen3-ASR-Toolkit
- DashScope 文档: https://help.aliyun.com/zh/dashscope/

## 文档索引

| 文档 | 何时读 |
|------|--------|
| `references/dashscope-async-filetrans.md` | 改 ASR 集成时 |
| `references/ai-summary-prompt.md` | **改 LLM prompt 模板时 (Step 3)** |
| `references/speaker-detection-strategies.md` | 改说话人识别逻辑时 |
