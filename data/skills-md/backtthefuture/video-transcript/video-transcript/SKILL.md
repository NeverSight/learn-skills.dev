---
name: video-transcript
description: >
  视频与播客文字提取：下载音视频后调用夸克网盘 Skill 云端取稿，再由模型轻校对。
  支持单条和批次、已上传网盘文件、持久对应关系与中断恢复。用于“逐字稿、转文字、提取文案”
  或附音视频链接的提取请求。默认不运行本地 ASR；不承诺说话人分离、句级时间轴或 SRT。
metadata:
  display-name: 视频文案提取
---

# 视频文案提取：夸克云端版

链接 / 本地媒体 / 已指定的网盘文件 → 登记 → 下载或匹配 → 上传并核对 → 单文件问答取正文 → 质量检查 → 模型 patch 轻校对。

## 入口与依赖

使用**本次读取的这份 SKILL.md 所在目录**作为 `VT_HOME`。不要按 WorkBuddy/Codex 等优先级另找一份 video-transcript；不能把其他副本当成这份的运行目录。
`VT_PY` 使用可运行脚本的 Python 3.9+，不必寻找装有 FunASR 的解释器。

首次执行先读已安装 `quarkclouddrive/SKILL.md` 及本次涉及的 `references/file-upload.md`、`references/file-search.md`、`references/assistant.md`。
下载沿用 video-download；平台解析所需登录态仍按该 Skill 处理。夸克 CLI 是外部依赖，不复制其源码或凭据。本脚本会在每次调用夸克命令前运行官方环境检查，并使用同一批次会话 ID。

```bash
python3 "$VT_HOME/scripts/transcript.py" --doctor
```

该体检只检查本地工具与依赖位置，不代表授权或云端链路成功。缺少夸克 Skill 时按其安装说明安装；不要运行旧版 ASR 安装步骤。需要安装下载依赖才运行本 Skill 的 install.sh；已有 .env、outputs 和模型缓存保留。

## 单条与批次

用户明确选择此 Skill 的云端工作流，即按任务范围上传指定媒体。用户要求只下载时转交 video-download。
保存用户本轮原始请求为临时 UTF-8 文件，通过 `--session-input-file` 传入；这是夸克要求的服务质量追踪参数，不应塞入额外对话或凭据。

```bash
python3 "$VT_HOME/scripts/transcript.py" "<链接或本地路径>"   --session-input-file "<原始请求文件>" --wait 1800

python3 "$VT_HOME/scripts/transcript.py" --batch "<inputs.json>"   --session-input-file "<原始请求文件>" --wait 1800
```

等待值是本次进程的复查预算，不是预计完成时间；单次网络请求可能在预算结束后才返回。
批次 JSON 是输入字符串数组，或包含 `input`、可选 `title` 的对象数组。
截图 PDF 保留 `--keep-video` 兼容参数；新版媒体默认持久保存，不自动删本地文件或云端文件。
已上传网盘文件的选定、参数、缓存与错误恢复见 [references/quark-workflow.md](references/quark-workflow.md)。

## 状态和中断恢复

每条文件有固定 asset_id；所有批次复用同一 output-dir 内的条目记录。通过来源链接或本地内容 SHA256 识别任务，不靠标题和完成顺序关联。
上传原始 ID 与搜索返回 FID 分开存。读取完整 Artifact，并按唯一文件名、大小及上传时间（时长返回时另核对）绑定；匹配不唯一就停该条。
一条问答只传一个文件，原始响应与每次请求单独留档。上传结果未知不盲目重传。

- `text_received`：取回了可供审阅的正文，**不是逐字准确或全文已验证**。
- `waiting_analysis`：保持 FID，按 next_poll_at 复查，初期 60 秒，随后 120/300 秒。
- `response_needs_review`：疑似摘要、缺来源、过短或不完整。读 raw.md，不直接润色成“完整稿”。
- `mapping_needs_review` / `upload_outcome_unknown`：核对对应关系，不猜、不重新上传。
- `auth_required`：按夸克 Skill 引导 login，完成后用原批次明确重试。
- `qa_failed` / `failed`：说明原因，修复后恢复，不自动无限重试。

```bash
python3 "$VT_HOME/scripts/transcript.py" --resume "<batch_manifest>" --status
python3 "$VT_HOME/scripts/transcript.py" --resume "<batch_manifest>"   --session-input-file "<原始请求文件>" --wait 1800
```

退出码 0=本次各条已取回正文；2=仍有等待；1=需要处理错误或人工核对。退出码不代表质量验收。
任务终止后没有自动唤醒；只在用户请求后台监测时另接调度。不能用“已保存等待状态”冒充会自动继续。

## 取稿后：模型必须检查并轻校对

输出包含 batch_manifest、各条状态，以及可用的 transcript_path、preorganized_path、polish_brief_path。
先读**完整原始返回与预整理稿**，核对来源是否对应、是否摘要/拒绝/明显截断，条件允许时抽查首中尾字幕或听校。字数和首尾覆盖只能作为抽查，不能证明逐句完整。

普通视频：读 polish_brief，写一份 patch.json，再调用：

```bash
python3 "$VT_HOME/scripts/make_optimized.py"   --from-md "<preorganized_path>" --patch "<patch.json>"   --filename "<asset_id>_整理稿" --output-dir "<该条产物目录>"
```

patch 使用 title、headings、fixes（from/to/confidence/basis）和必要的 paragraph_edits。保留顺序、数字、观点；高确信且有依据才替换，低确信只列待核。不要补写缺段、推测说话人或编造时间轴。渲染器支持无时间标记的章节，并保留补丁记录。
修改后回读，核对没有整段丢失。保留夸克原始返回，润色稿独立交付。单条用户要求全文时在对话输出全文；批次优先交付汇总表与每条稿件链接，避免四份长稿互相混杂。

微信视频号：读 [skills/weixin-layout.md](skills/weixin-layout.md)，保留默认口语稿、文字 PDF、截图 PDF 的分流。无时间轴时截图与正文需实际核对，不得按虚构时间自动配图。
播客：同样先取纯文字，再轻校对。旧 --speakers/--host/--guest 明确报不支持，不转本地模型、不伪造人物归属。

## 交付边界

分别报告：文件对应、正文取回、抽查或听校程度、润色完成。历史专名、古文和无字幕材料要保留待核点。
--force 只重新请求正文，复用原上传；--reformat 只从已保存原文重建预整理。不自动读取旧 FunASR 缓存，旧文件不删除。


## 上游 Skill 的稳定接入

供 deep-search、视频博主拆解使用的适配器为 `scripts/caller_client.py`，不复制夸克运行时。先通过 `--batch ... --status` 本地登记，再持久保存 asset_id/manifest 后开始云端请求；适配器按完整 stdout JSON 和条目 state.json 读取结果，`schema_version=1`。

同一调用方工作目录保存 session.json；`--session-id` 可在新批次登记时指定 `{timestamp}-{6位随机字符}`，已有批次继续使用原值。所有实际云端调用仍传原始请求文件。

适配器保留 waiting_analysis、response_needs_review、mapping_needs_review、upload_outcome_unknown、auth_required 等状态。无音轨标 no_audio，媒体保留且不上传/问答；缺衍生稿可本地重建。取帧只接受记录中且 SHA256 相符的媒体，未核对的目录文件不能作为替代。

调用方显式使用 `--repair-media` 时，适配器仅补下载缺失媒体，要求与原哈希一致；不重新上传或问答。字节不同保留候选并停下核对。没有可核对的原链接或哈希时不能自动修复。
