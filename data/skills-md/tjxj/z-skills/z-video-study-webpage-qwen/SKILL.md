---
name: z-video-study-webpage-qwen
description: 当用户要求“理解视频内容”“完整学习视频”“解读视频”“视频学习总结网页”“图文并茂学习网页”“用 Qwen 多模态分析视频”“用 qwen3.7-plus 看视频”“关键知识点匹配画面”“把视频做成学习网页”时必须使用。本 skill 会把本地 MP4 或已下载视频拆成音频转录、时间轴帧图、Qwen 多模态逐段分析，并用既有学习总结网页模板生成图文并茂 HTML，要求每个关键知识点绑定到正确视频画面。
---

# Qwen 多模态视频学习网页

把一个视频真正拆开学习：先抽音频转全文，再抽关键时间点画面，用 DashScope OpenAI-compatible API 的 `qwen3.7-plus` 逐段理解，最后生成学习总结网页。网页沿用当前 `study-summary.html` 的视觉模板：米色纸张、卡片、时间线、风险矩阵、本地视频播放器、关键帧图文卡片。

## 适用场景

- 用户给本地 MP4，要求完整理解视频、做学习总结网页。
- 用户给 YouTube / B 站 / 主流平台链接并要求下载后理解；先调用 `z-video-downloader` 下载，再用本 skill 分析本地 MP4。
- 用户明确要求“关键知识点要匹配正确画面”，优先用本 skill。
- 用户提到 DashScope、Qwen 多模态、`qwen3.7-plus`、OpenAI-compatible base_url，也用本 skill。

## 安全约定

- API Key 只从环境变量读取，默认变量名：`DASHSCOPE_API_KEY`。
- 不要把用户给的 key 写入 `SKILL.md`、脚本、报告、HTML、终端日志或最终回复。
- 默认 base URL：`https://dashscope.aliyuncs.com/compatible-mode/v1`。
- 默认模型：`qwen3.7-plus`。如果接口返回模型不存在，提醒用户用 `--model` 改成实际可用模型名。

## 输入输出

输入可以是：

- 本地 MP4：`/path/to/video.mp4`
- 已下载视频所在目录
- 平台链接：先用 `z-video-downloader` 得到本地 MP4

默认输出在视频同级目录或指定目录：

```text
study-qwen/
├── study-summary-qwen.html        # 最终学习网页
├── qwen-analysis.json             # 模型结构化结果
├── storyboard.json                # 关键帧清单
├── transcript.txt                 # 完整转录文本，若成功
├── transcript.json                # 带时间戳转录，若成功
├── assets/
│   ├── frame-001.jpg
│   ├── frame-002.jpg
│   └── ...
└── run-report.json
```

## 推荐命令

```bash
export DASHSCOPE_API_KEY="放在你本机环境里，不要写进文件"

/Users/zz/miniconda3/bin/python3 .agent/skills/z-video-study-webpage-qwen/scripts/qwen_video_study.py \
  --video "/path/to/video.mp4" \
  --title "视频主题" \
  --out-dir "/path/to/output/study-qwen" \
  --model "qwen3.7-plus"
```

如果已经有字幕或 transcript：

```bash
/Users/zz/miniconda3/bin/python3 .agent/skills/z-video-study-webpage-qwen/scripts/qwen_video_study.py \
  --video "/path/to/video.mp4" \
  --transcript "/path/to/transcript.txt" \
  --title "视频主题" \
  --out-dir "/path/to/output/study-qwen"
```

只验证抽帧和网页模板，不调用模型：

```bash
/Users/zz/miniconda3/bin/python3 .agent/skills/z-video-study-webpage-qwen/scripts/qwen_video_study.py \
  --video "/path/to/video.mp4" \
  --title "视频主题" \
  --out-dir "/path/to/output/study-qwen" \
  --mock-analysis
```

## 执行流程

1. **确认视频本地路径**
   - 如果用户给的是 URL，先用 `z-video-downloader` 下载。
   - 找到实际 MP4 后再执行本 skill。

2. **抽取关键帧**
   - 默认抽 12 段，每段 1-3 张代表画面。
   - 每张图写入 `storyboard.json`，字段包括 `frame_id`、`timestamp`、`time_label`、`path`。
   - 这些 `frame_id` 是后续知识点绑定画面的唯一依据。

3. **完整转录**
   - 优先使用用户提供的 `--transcript`。
   - 没有 transcript 时，脚本尝试用本机 Whisper 转录音频。
   - 如果 Whisper 不可用，继续执行视觉分析，但报告里要标明“缺少全文转录，结论更依赖画面和已有标题信息”。

4. **Qwen 多模态逐段分析**
   - 每个段落发送：该段 transcript、时间范围、对应关键帧图片。
   - 提示模型输出 JSON：段落主题、关键知识点、证据、画面绑定、待确认信息。
   - 关键知识点必须引用实际存在的 `frame_id`。

5. **全局学习结构合成**
   - 再调用一次 Qwen，把分段结果合成为：
     - 30 秒总览
     - 学习地图
     - 关键知识点 × 正确画面
     - 时间线
     - 风险 / 机会矩阵
     - 复盘问题
     - 行动清单
   - 若模型给出不存在的 `frame_id`，脚本自动降级到同段第一张图，并在 JSON 里记录修正。

6. **渲染 HTML**
   - 沿用当前学习网页模板的视觉语言。
   - 顶部必须有本地视频播放器。
   - 每个关键知识点卡片必须带一张本地帧图。
   - HTML 只引用本地图片和本地视频。

7. **收尾检查**
   - 校验 HTML 中所有本地媒体路径存在。
   - 校验 `qwen-analysis.json` 可解析。
   - 检查没有把 API key 写入任何输出文件。
   - 如果任务产出 `.md` 且包含外链图片，再按项目规则调用 `1-upload-images-to-picgo`；本 skill 默认产出 HTML，无需图床。

## 质量标准

- 不能只用视频标题泛泛总结。
- 不能只截几张图后写空泛结论。
- 关键知识点要来自 transcript、画面或二者交叉验证。
- 每个关键知识点都要有对应画面：图片应能直观看出人物、产品、图示、场景或风险主题。
- 对不确定内容要标注“待核验”，不要伪装成事实。

## 测试

编辑脚本后运行：

```bash
/Users/zz/miniconda3/bin/python3 -m py_compile \
  .agent/skills/z-video-study-webpage-qwen/scripts/qwen_video_study.py \
  .agent/skills/z-video-study-webpage-qwen/tests/test_qwen_video_study.py

/Users/zz/miniconda3/bin/python3 .agent/skills/z-video-study-webpage-qwen/tests/test_qwen_video_study.py
```

