---
name: submit-anime-project
description: 整部作品提交技能。读取全剧 seedance_project_tasks.json，按 Seedance 任务提交协议批量推送到 /api/tasks/push，并生成提交报告。关键词：提交任务、Seedance、批量推送、整部作品、task submit、api/tasks/push。
---

# 整部作品提交技能 (Submit Project)

## 概述

本技能用于将一整部短剧项目的分镜任务（通常 50 条）批量提交到 Seedance 任务服务。

输入来源：
- `seedance_project_tasks.json`（项目根目录下的唯一任务文件）

输出结果：
- 提交成功的 `taskCodes`
- 失败任务清单
- `submission_report.json`

---

## 依赖协议

遵循 `seedance-video-task-submit` 协议（详见 `skill-task-submit.md`）：
- 服务地址默认：`http://localhost:3456`
- 核心接口：`POST /api/tasks/push`
- 支持单任务或批量（`tasks` 数组）

任务对象关键字段：
- `prompt` (必填，使用 `(@fileName)` 语法引用参考图)
- `description`
- `modelConfig`（`model` / `referenceMode` / `aspectRatio` / `duration`）
- `referenceFiles` (对象数组，每项包含 `fileName` / `base64` / `fileType`)
- `realSubmit` (默认 `false`)
- `priority` (默认 `1`)
- `tags` (建议包含 `project_id`,`EPxx`,`A|B`)

### referenceFiles 存储与展开

**存储格式（seedance_tasks.json 中）**：`referenceFiles` 为**相对路径字符串数组**，相对于项目根目录。包含分镜参考图、角色参考图、场景参考图和道具参考图。

```json
"referenceFiles": [
  "episodes/EP01/DM-002-EP01-A_storyboard.png",
  "characters/林策_ref.png",
  "characters/沈璃_ref.png",
  "scenes/scene_01_ref.png",
  "props/prop_01_ref.png"
]
```

**提交时展开**：提交前将每个路径展开为对象，读取文件转 base64：

```json
"referenceFiles": [
  {
    "fileName": "DM-002-EP01-A_storyboard.png",
    "base64": "data:image/png;base64,iVBOR...",
    "fileType": "image/png"
  }
]
```

展开逻辑（Python 伪代码）：
```python
import base64, os, mimetypes

def expand_reference_files(ref_paths, project_dir):
    result = []
    for rel_path in ref_paths:
        abs_path = os.path.join(project_dir, rel_path)
        file_name = os.path.basename(rel_path)
        mime_type = mimetypes.guess_type(abs_path)[0] or "image/png"
        with open(abs_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        result.append({
            "fileName": file_name,
            "base64": f"data:{mime_type};base64,{b64}",
            "fileType": mime_type
        })
    return result
```

---

## 目录约定

目标项目目录（示例 `DM-002_tjkc/`）应包含：

```
DM-002_tjkc/
├── seedance_project_tasks.json          # 必须，唯一任务文件
├── episodes/
│   ├── EP01/
│   │   ├── dialogue.md
│   │   └── storyboard_config.json
│   └── ...
└── submission_report.json               # 本技能生成
```

---

## 执行流程

### 第一步：定位项目

1. 若用户指定项目编号（如 `DM-002`），定位对应目录
2. 若未指定，使用 `projects/index.json` 最新项目

### 第二步：加载任务

1. 优先读取 `seedance_project_tasks.json`
2. 若不存在，遍历 `episodes/EP01-EP25/seedance_tasks.json` 聚合
3. 若用户指定单集（如 EP01），只读取该集的 `seedance_tasks.json`
4. 校验任务结构：
   - 每个任务必须有 `prompt`
   - `modelConfig` 缺失时补默认值
   - `realSubmit` 缺失时默认 `false`

### 第三步：展开 referenceFiles

对每个任务的 `referenceFiles`（相对路径字符串数组），执行 base64 展开：

1. 拼接绝对路径：`项目根目录 + 相对路径`
2. 读取文件二进制内容
3. 转换为 `{fileName, base64: "data:mime;base64,...", fileType}` 对象
4. 替换原 `referenceFiles` 数组

### 第四步：批量提交

1. 按批次提交（推荐每批 20~50 条）到 `/api/tasks/push`
2. 请求体格式：

```json
{
  "tasks": [
    {
      "prompt": "...",
      "description": "...",
      "modelConfig": {
        "model": "Seedance 2.0 Fast",
        "referenceMode": "全能参考",
        "aspectRatio": "16:9",
        "duration": "15s"
      },
      "referenceFiles": [
        {
          "fileName": "DM-002-EP01-A_storyboard.png",
          "base64": "data:image/png;base64,...",
          "fileType": "image/png"
        },
        {
          "fileName": "林策_ref.png",
          "base64": "data:image/png;base64,...",
          "fileType": "image/png"
        },
        {
          "fileName": "scene_01_ref.png",
          "base64": "data:image/png;base64,...",
          "fileType": "image/png"
        }
      ],
      "realSubmit": true,
      "priority": 1,
      "tags": ["DM-002", "EP01", "A"]
    }
  ]
}
```

3. 收集返回的 `taskCodes`
4. 记录失败批次与错误信息

### 第五步：生成报告

在项目根目录生成 `submission_report.json`，格式示例：

```json
{
  "project_id": "DM-002",
  "submitted_at": "2026-02-16T12:00:00Z",
  "api_base": "http://localhost:3456",
  "total_tasks": 300,
  "submitted_tasks": 300,
  "failed_tasks": 0,
  "task_codes": ["SD-20260216-0001"],
  "failed_items": []
}
```

---

## 推荐默认值

当字段缺失时，按以下默认值补齐：

```json
{
  "modelConfig": {
    "model": "Seedance 2.0 Fast",
    "referenceMode": "全能参考",
    "aspectRatio": "16:9",
    "duration": "15s"
  },
  "referenceFiles": [],
  "realSubmit": false,
  "priority": 1,
  "tags": []
}
```

---

## 运行指令

可通过以下表达触发：
- "提交整部作品任务"
- "把 DM-002 全部分镜提交到 Seedance"
- "batch submit drama tasks"
- "提交所有 seedance_tasks"

可附带参数：
- 项目编号：如 `DM-002`
- `realSubmit`：`true/false`
- 批次大小：如 `batch=30`
- API 地址：如 `api_base=http://localhost:3456`

---

## 检查清单

- [ ] 已定位正确项目目录
- [ ] 任务来源文件存在（项目级或分集级）
- [ ] 每个任务包含 `prompt`
- [ ] 批量提交到 `/api/tasks/push` 成功
- [ ] 已收集全部 `taskCodes`
- [ ] 失败项已记录并可重试
- [ ] `submission_report.json` 已生成

---

## 输出示例

```text
✅ 整部作品任务提交完成

项目：DM-002
总任务数：300
成功提交：300
失败：0

报告文件：/data/dongman/projects/DM-002_tjkc/submission_report.json
```
