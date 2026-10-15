---
name: yichen-asr
description: 逸尘自用的统一音视频转写入口，在 StepFun Step ASR 与火山引擎豆包 ASR 之间按输出需求、安全边界和可用状态路由。用于本地音频或视频的纯文本转写、时间戳、SRT 字幕、口播粗剪，以及转写前体检；用户明确指定服务商时不得静默切换。Use when a local audio or video file needs transcription and the correct ASR backend is unclear, or when the user explicitly invokes $yichen-asr.
---

# 逸尘统一 ASR

这是一个统一路由层，不是第三套 ASR 引擎。Step ASR 与豆包 ASR 继续作为底层执行器，由本 Skill 负责选择、体检、失败收敛和交接。

## 路由规则

| 需求 | 默认后端 | 原因 |
|---|---|---|
| 只要全文、摘要或内容分析 | Step ASR | 30 秒切片，失败片段可缩成 10/5 秒重试 |
| 需要较细时间戳、SRT 字幕 | 豆包 ASR | 返回结构化 utterances 和时间信息 |
| 需要口播停顿、填充词分析或自动粗剪 | 豆包 ASR | 现有脚本包含 SRT 与 ffmpeg 粗剪链 |
| 用户明确说“只用 Step” | Step ASR | 不得跨服务商补齐 |
| 用户明确说“只用豆包/火山” | 豆包 ASR | 不得跨服务商补齐 |

自动路由只允许在“尚未向任何服务商提交任务”时切换。如果某个请求已经上传、提交或留下 request ID，必须恢复或报告该任务，不得再向另一家提交同一媒体，以免重复计费。

用离线路由器确认选择：

```bash
python3 ~/.agents/skills/yichen-asr/scripts/route_asr.py \
  --provider auto --text-only
```

需要字幕时：

```bash
python3 ~/.agents/skills/yichen-asr/scripts/route_asr.py \
  --provider auto --need-timestamps --need-srt
```

## 执行前体检

先运行只读体检；它只报告密钥是否存在，不显示密钥内容，也不会调用付费接口：

```bash
python3 ~/.agents/skills/yichen-asr/scripts/asr_doctor.py
```

体检中的 `token_present` 仅表示本机配置了调用凭证，不代表账户有余额。ASR Token 无权读取火山引擎财务余额；余额和欠费状态必须登录费用中心核验。

## Step ASR

执行器：

```bash
python3 "$YICHEN_STEP_ASR_SCRIPT" \
  --input "/absolute/path/input.mp4" \
  --output-dir "/absolute/path/output" \
  --title "标题" \
  --resume
```

公开版不内置 Step ASR 执行器。通过 `YICHEN_STEP_ASR_SCRIPT` 指向你已安装并审计过的兼容脚本；也可把它安装为同级 `step-asr/scripts/step_asr_transcribe.py`。执行时完整遵守该执行器的 `SKILL.md`。不得删除失败标记，也不得用豆包结果静默填补 Step 失败片段。

## 豆包 ASR

执行器：

```bash
python3 ~/.agents/skills/yichen-volc-asr/scripts/transcribe.py \
  "/absolute/path/input.mp4" \
  --transcribe-only
```

需要 SRT 与口播粗剪时，去掉 `--transcribe-only`；只生成分析和命令、不执行剪辑时加 `--no-execute`。

执行时完整遵守 `~/.agents/skills/yichen-volc-asr/SKILL.md`。发现同媒体的 `.asr_pending.json` 时，优先恢复原任务；除非用户明确授权，不得使用 `--force-new`。

豆包调用不需要每次网页登录。公开版不包含 App ID、Token 或钥匙串名称：试用与付费 App ID 分别通过 `VOLC_ASR_TRIAL_APP_ID`、`VOLC_ASR_PAID_APP_ID` 提供，Token 分别通过 `VOLC_ASR_TRIAL_TOKEN`、`VOLC_ASR_PAID_TOKEN` 提供。脚本直接把本地媒体提交到极速版接口；视频先由 ffmpeg 在内存中提取音轨。

财务余额只能在火山引擎控制台登录后查看：

- 账户概览与余额：https://console.volcengine.com/finance/account-overview/
- 充值说明：https://www.volcengine.com/docs/3019/1176800?lang=zh

## 失败与回退

1. 用户指定服务商：失败后只报告该服务商的错误和恢复路径，不自动换服务商。
2. 自动路由且尚未提交：若默认后端缺少脚本、密钥或必要能力，可改用满足输出要求的另一后端，并明确说明。
3. 自动路由且已经提交：不得跨服务商重提；优先用 request ID、缓存或 `--resume` 恢复。
4. 豆包余额未知：不得说成“余额充足”或“余额不足”。只有费用中心、账单或明确的接口欠费错误可确认。
5. 精确 SRT 需求不能因豆包不可用而悄悄降级为 Step 的分块 Markdown；应说明能力差异。

## 费用与安全

- 单个文件的明确转写请求可按选定后端执行；批量任务或可能产生显著付费额度时，先说明文件数、总时长和后端，再取得用户确认。
- 不输出 Cookie、Token、API Key；长期凭据只存 macOS 钥匙串，不写入 Skill、脚本、日志或记忆。
- 不把密钥提交到 Skill、产物、日志或记忆文件。
- 不自动充值、购买资源包或开通后付费。
- 不覆盖既有产物。不得自动删除临时文件；任何清理都要用户明确允许，并且只能移入废纸篓。

## 交接

向上层研究流程至少交接：

```json
{
  "provider": "step|doubao",
  "mode": "text|timestamps|srt|rough_cut",
  "input": "/absolute/path/input",
  "outputs": [],
  "request_id": null,
  "billing_status": "unknown|verified_ok|verified_insufficient",
  "errors": []
}
```

本 Skill 是 `$yichen-web-research` 的转写子路由。研究总入口负责决定何时需要转写；本 Skill 只负责已有本地音视频的 ASR，不负责搜索、下载或归档。
