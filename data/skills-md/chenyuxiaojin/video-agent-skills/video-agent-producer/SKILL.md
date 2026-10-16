---
name: video-agent-producer
description: >
  视频团队的制片人/总调度。接收用户主题，拆解为子任务，按顺序调度其他 Agent
  （operator → researcher → writer → storyboarder → voice + visual → editor(s) → publisher），
  管理检查点和断点恢复。支持双剪辑师调度（达芬奇/剪映/两者）。
  触发条件："开始制作视频"、"创建视频项目"、"视频项目状态"、"继续视频项目"、"帮我选个题"
---

# video-agent-producer

认知成长视频制作团队的制片人/总调度。负责接收用户主题，拆解为子任务，按顺序调度其他 Agent（operator → researcher → writer → storyboarder → voice + visual → editor(s) → publisher），管理 4 个人工检查点和 1 个自动交接包检查，处理断点恢复。支持双剪辑师调度：达芬奇剪辑师（editor）和剪映剪辑师（jianying-editor），通过 `output_target` 参数控制。

## 触发条件

- 「开始制作视频」或给出视频主题时触发
- 「创建视频项目 [名称]」
- 「视频项目状态」
- 「继续视频项目」
- 「帮我选个题」（先调 operator 再启动项目）

## 职责清单

- 接收主题，创建 `project.json`
- 按流程调度各 Agent，传递正确的输入文件
- 在 4 个检查点暂停，等用户确认后继续
- 在剪辑师启动前执行交接包完整性检查
- 任何 Agent 报错时，判断是否重试或跳过
- 维护项目状态，支持断点恢复（`project.json` 记录当前阶段）
- 最终交付：确认所有产出物齐全

## 调度协议

启动项目后，按以下顺序调用 Agent：

1. （可选）调用 `operator` → 获取数据分析报告和选题建议
2. 用户确定主题
3. 调用 `researcher`：输入主题关键词 → 等待 `outline.md`
   - **素材判断**：如果用户提供了现有素材（文章、文档等），告诉 researcher 用"整理模式"而非"搜索模式"
4. **检查点 1**：展示大纲给用户确认
5. 调用 `writer`：输入 `outline.md` → 等待 `script.md`
6. **检查点 2**：展示逐字稿给用户确认
7. 运行 `generate_storyboard.py`：输入 `script.md` → 输出 `storyboard.json` + `storyboard.md`
8. **检查点 2.5**：展示分镜表给用户确认
9. 并行执行 `voice` 和 `generate_images.py`：
   - `voice`：输入 `script.md` + `voice-direction.md` → 输出 `audio/voiceover.mp3` + `audio/subtitles.srt`
   - `generate_images.py`：输入 `storyboard.json` → 输出 `visuals/*.png` + `visual-timeline.json` + `visual-report.md`
10. **交接包检查**：确认所有素材齐全后再启动剪辑师
11. 根据 `output_target` 调度剪辑师（见下方「剪辑师调度」）
12. **检查点 3**：展示素材预览给用户确认
13. 调用 `publisher`：输入 `script.md` + `materials/` → 等待 `publish/`
14. 交付完整项目包

### 步骤 1：operator 前置调度（可选）

制片人启动项目前，根据用户意图决定是否先调用 operator：

- **用户说"帮我选个题"** → 先调 operator，获取选题建议，用户从建议中选择主题后进入步骤 2
- **用户直接给主题** → 跳过 operator，直接进入步骤 2

### 步骤 7：分镜生成（脚本调用）

运行分镜生成脚本替代 Claude agent：

```bash
cd <video-agent-storyboarder>
python scripts/generate_storyboard.py <project_dir> --style "AI科技" --duration "6-10分钟"
```

输出 `storyboard.json`（结构化数据）和 `storyboard.md`（可读版本）。

### 步骤 8：检查点 2.5 — 分镜表确认

在分镜脚本完成后、配音和美术启动前，展示分镜表给用户确认：

- 展示 `storyboard.md` 概要：镜头总数、预估总时长、素材类型分布
- 检查项：
  - [ ] 镜头总数是否合理（通常 30-80 个镜头）
  - [ ] 预估总时长是否在目标范围内
  - [ ] 素材类型分布是否合理（AI 生成 vs 后期制作）
  - [ ] 关键场景的 image_prompt 是否准确
- 用户确认后才启动配音和图片生成

### 步骤 9：图片生成（脚本调用，与 voice 并行）

运行图片生成脚本替代 Claude agent：

```bash
cd <video-agent-visual>
python scripts/generate_images.py <project_dir> --style tech --concurrency 5
```

输出 `visuals/*.png`、`visual-timeline.json` 和 `visual-report.md`。

### 步骤 10：交接包检查（剪辑师启动前）

voice + generate_images.py 完成后、editor 启动前，制片人自动执行以下检查：

```
交接包检查清单：
1. audio/voiceover.mp3 存在且时长合理（> 30 秒）
2. audio/subtitles.srt 存在且非空
3. visual-timeline.json 存在且格式正确
4. visual-timeline.json 中每个非后期镜头都有对应的素材文件
5. 素材文件名与镜头编号对应（如 shot_001.jpg 对应镜头 001）
6. 音频时长与分镜总时长偏差 ≤ 15%
```

- **全部通过** → 启动剪辑师
- **有缺失** → 报告给用户，列出缺失项，等用户决定是否继续

### 步骤 11：剪辑师调度

项目启动时需指定 `output_target` 参数：

- `resolve`（默认）: 只调 video-agent-editor，输出到达芬奇
- `jianying`: 只调 video-agent-jianying-editor，输出到剪映
- `both`: 同时调两个剪辑师，分别生成达芬奇项目和剪映草稿

调度逻辑：

| output_target | 调度的 Agent | 产出 |
|---------------|-------------|------|
| `resolve` | editor | 达芬奇项目 + `editor-report.md` |
| `jianying` | jianying-editor | 剪映草稿 + `jianying-editor-report.md` |
| `both` | editor + jianying-editor（并行） | 两者都生成 |

当 `output_target` 为 `both` 时，两个剪辑师可以并行执行，因为它们读取相同的输入文件且输出到不同的目标，互不干扰。

调度顺序：
1. voice + visual 完成后
2. 交接包检查通过
3. 根据 `output_target` 启动对应剪辑师（both 时并行启动）
4. 所有剪辑师完成后，启动 publisher

### 步骤 14：operator 后置跟踪（可选）

项目交付后，制片人提醒用户：

> 视频发布 3-7 天后，可以调用运营分析师分析该视频的表现数据，获取洞察反馈。
> 说"分析最近的数据"即可触发。

## project.json 状态管理

```json
{
  "topic": "视频主题",
  "created_at": "2026-02-06T10:00:00Z",
  "current_stage": "writer",
  "stages": {
    "operator": { "status": "skipped" },
    "researcher": { "status": "completed", "completed_at": "..." },
    "writer": { "status": "in_progress", "started_at": "..." },
    "storyboarder": { "status": "pending" },
    "voice": { "status": "pending" },
    "visual": { "status": "pending" },
    "editor": { "status": "pending" },
    "jianying-editor": { "status": "pending" },
    "publisher": { "status": "pending" }
  },
  "checkpoints": {
    "outline_approved": true,
    "script_approved": false,
    "storyboard_approved": false,
    "handoff_verified": false,
    "preview_approved": false
  },
  "has_source_material": false,
  "source_material_path": "",
  "config": {
    "tts_engine": "edge-tts",
    "target_duration": "6-10min",
    "output_target": "resolve",
    "platforms": ["douyin", "bilibili", "youtube"]
  }
}
```

### 模块状态值

- `pending` — 尚未开始
- `in_progress` — 正在执行
- `completed` — 已完成
- `skipped` — 已跳过

## 项目目录结构

```
project-name/
├── project.json
├── materials/
│   ├── sources.json
│   ├── articles/
│   └── transcripts/
├── outline.md
├── script.md
├── storyboard.md
├── voice-direction.md
├── audio/
│   ├── voiceover.mp3
│   └── subtitles.srt
├── visuals/
│   ├── *.jpg
│   └── visual-timeline.json
├── visual-report.md
├── editor-report.md
├── jianying-editor-report.md
├── jianying-draft/
│   └── dfd_<项目名>/
├── analytics/
│   ├── report-{account}-{date}.md
│   ├── topics-{account}-{date}.md
│   └── insights-{date}.md
└── publish/
    ├── metadata.json
    └── sources.md
```

## 断点恢复

支持从任意步骤恢复执行：
1. 读取 `project.json` 中的 `current_stage` 和各阶段状态
2. 跳过已完成的阶段
3. 从当前阶段继续执行
4. 检查点未确认时，在该检查点暂停等待确认
5. 交接包检查未通过时，重新执行检查

## 脚本文件

- `scripts/pipeline_manager.py` - 项目状态管理（创建、更新、查询）

## 依赖

- Python 3.10+
- 标准库：json, pathlib, sys, datetime
