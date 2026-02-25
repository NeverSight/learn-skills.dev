---
name: produce-anime
description: 短剧制作技能。用于生成完整短剧作品，包括剧本编写、角色设计、9宫格分镜、故事板配置。每次运行生成1部作品（25集，每集30秒=上下两部分各15秒，每部分9宫格分镜）。关键词：短剧、影视、drama、剧本、分镜、storyboard、角色设计。
---

# 短剧制作技能 (Produce Short Drama)

## 概述

本技能用于自动化生成完整短剧作品的全套制作文档和脚本。每次运行生成 **1部完整作品**，包含 **25集**，每集 **30秒**，分为 **上、下两部分**（各15秒）：
- 每部分包含 **9宫格分镜提示词**（3×3布局，16:9比例）
- 每集生成 **2个文件**：对话脚本 + 故事板配置（9宫格分镜）
- 每个Part在配置中标注引用的`scene_refs`（场景ID列表）和`prop_refs`（道具ID列表）
- Seedance任务JSON在 **媒体生成后** 单独生成（每集2条：Part-A/B，使用 `(@文件名)` 引用角色/场景/道具参考图和分镜图）
- 含氛围描述、中文人物对话、无字幕
- 视频编号管理索引
- 支持**视觉风格预设**（从 `.config/visual_styles.json` 读取，注入到提示词和配置中）

### 完整工作流程（4个阶段）

| 阶段 | 技能 | 产出 |
|------|------|------|
| 1. 剧本制作 | `produce-anime` | full_script.md, character_bible.md, dialogue.md, storyboard_config.json, video_index.json |
| 2. 媒体生成 | `generate-media` | 角色参考图 + 场景四宫格图 + 道具三视图 + 9宫格分镜图 |
| 3. 任务生成 | `produce-anime`（第七步） | seedance_project_tasks.json（使用 `(@文件名)` 引用图片，50条） |
| 4. 任务提交 | `submit-anime-project` | 批量推送到 Seedance API |

---
## 视觉风格预设

项目支持从 `/data/dongman/.config/visual_styles.json` 读取视觉风格预设。用户可通过以下方式指定风格：
- 指定风格名：如 "使用 Vintage Hong Kong 风格"
- 指定风格ID：如 "风格7"
- 指定中文名：如 "港风复古"
- 不指定：使用 `default_style_id` 对应的默认风格

> **⚠️ 风格选择交互**：在生成角色参考图、场景四宫格图和道具三视图时，必须先让用户选择视觉风格。使用 `ask_questions` 工具列出 `visual_styles.json` 中的所有风格选项，让用户确认后再开始生成。风格会同时影响角色/场景/道具的参考图风格和分镜图风格。

选中的风格会：
1. 写入 `metadata.json` 的 `visual_style` 字段
2. 写入每集 `storyboard_config.json` 的 `visual_style` 字段
3. 将 `prompt_suffix` 追加到所有 `ai_image_prompt` 末尾

风格预设字段说明：

| 字段 | 说明 | 示例 |
|------|------|------|
| `camera` | 摄影机/机身 | Panavision Sphero 65 and Hasselblad Lenses |
| `film_stock` | 胶片/传感器 | Vision3 500T 5219 |
| `filter` | 滤镜组合 | ND0.6, Diffusion Filter 1/4 |
| `focal_length` | 焦距 | 65mm |
| `aperture` | 光圈 | f/2.0 |
| `prompt_suffix` | 追加到AI提示词末尾的风格描述 | shot on Panavision... |

---
## 执行流程

当用户要求制作短剧/影视作品时，按以下步骤顺序执行：

### 第一步：初始化项目

1. 读取 `/data/dongman/projects/index.json` 获取当前作品编号（如不存在则从 `DM-001` 开始）
2. 在 `/data/dongman/projects/` 下创建新作品目录，命名规则：`{作品编号}_{作品名称拼音缩写}/`
3. 创建作品目录结构：

```
projects/
├── index.json                          # 所有作品索引（全局管理）
└── DM-001_xxxx/                        # 单部作品目录
    ├── metadata.json                   # 作品元数据
    ├── script/                         # 剧本
    │   └── full_script.md              # 完整剧本（25集大纲+详细剧本）
    ├── characters/                     # 角色设计
    │   └── character_bible.md          # 角色圣经（所有角色设定）
    ├── scenes/                         # 场景设计（全剧复用）
    │   └── scene_bible.md              # 场景圣经（所有场景设定+AI绘图关键词）
    ├── props/                          # 道具设计（全剧复用）
    │   └── prop_bible.md               # 道具圣经（所有道具设定+AI绘图关键词）
    ├── episodes/                       # 各集内容
    │   ├── EP01/
    │   │   ├── dialogue.md             # 本集对话脚本（中文，覆盖上下两部分）
    │   │   └── storyboard_config.json  # 故事板配置（含上下两部分，每部分9宫格，含scene_refs/prop_refs）
    │   ├── EP02/
    │   │   └── ...
    │   └── ... (EP01-EP25)
    ├── seedance_project_tasks.json     # [阶段3·媒体生成后] 全剧Seedance任务（50条，含@图片引用）
    └── video_index.json                # 视频编号管理索引
```

### 第二步：剧本编写 (Script Writing)

生成 `script/full_script.md`，包含：

```markdown
# 《作品名称》完整剧本

## 作品信息
- **类型**：[冒险/奇幻/科幻/日常/恋爱 等]
- **风格**：[热血/治愈/悬疑/搞笑 等]
- **视觉风格**：[风格预设名称，如 Cinematic Film]
- **目标受众**：[少年/少女/青年/全年龄]
- **总时长**：25集 × 30秒 = 12分30秒
- **核心主题**：一句话概括

## 世界观设定
[200-300字描述世界观]

## 故事大纲
[500字总体故事线]

## 各集概要
### 第1集：[标题]
- **剧情概要**：[50字]
- **关键事件**：[列表]
- **情感基调**：[喜/怒/哀/乐/紧张/温馨]

### 第2集：[标题]
...（共25集）
```

### 第三步：角色设计 (Character Design)

生成 `characters/character_bible.md`，每个角色包含：

```markdown
# 角色设定集

## 主要角色

### 角色1：[名字]
- **全名**：
- **年龄**：
- **性别**：
- **身高/体重**：
- **外貌特征**：[详细描述，用于AI绘图提示词]
  - 发型/发色：
  - 瞳色：
  - 体型：
  - 标志性特征：
- **服装设计**：
  - 日常服装：
  - 战斗/特殊服装：
- **性格特点**：
- **口头禅**：
- **背景故事**：[100字]
- **角色弧光**：[在25集中的成长变化]
- **AI绘图关键词（英文）**：[用于生成角色一致性的Prompt]

## 次要角色
...

## 角色关系图
[用文字描述角色间的关系网络]
```

### 第三步B：场景设计 (Scene Design)

生成 `scenes/scene_bible.md`，记录全剧会**反复出现**的主要场景。每个场景包含 AI 绘图关键词，用于后续生成多视角参考图。

```markdown
# 场景设定集

## 场景1：[场景名称]
- **场景ID**：scene_01
- **场景描述**：[50-100字描述物理空间、装饰、氛围]
- **出现集数**：EP01, EP02, EP05, EP15...
- **关键视觉元素**：[列出该场景的标志性物件、色调、灯光]
- **AI绘图关键词（英文）**：[详细的英文提示词，包含空间布局、光影、陈设风格]

## 场景2：[场景名称]
...
```

> **场景筛选原则**：只收录在 **3集以上** 反复出现的重要场景（一次性出现的场景无需单独建参考图）。通常一部 25 集短剧有 3-6 个核心场景。

### 第三步C：道具设计 (Prop Design)

生成 `props/prop_bible.md`，记录全剧中有**剧情意义**的重要道具。每个道具包含 AI 绘图关键词，用于后续生成三视图。

```markdown
# 道具设定集

## 道具1：[道具名称]
- **道具ID**：prop_01
- **道具描述**：[30-50字描述外观、材质、尺寸]
- **出现集数**：EP10, EP12, EP25...
- **剧情意义**：[此道具在剧中的象征/功能意义]
- **AI绘图关键词（英文）**：[详细的英文提示词，包含材质、颜色、形状、细节]

## 道具2：[道具名称]
...
```

> **道具筛选原则**：只收录具有**剧情推动或象征意义**的道具（如信物、关键文件、标志性物品），不收录日常物件。通常一部 25 集短剧有 2-5 个核心道具。

### 第四步：逐集生成内容

对每一集（EP01-EP25），生成以下 **2个文件**（seedance_tasks.json 在阶段3媒体生成后单独生成）：

#### 4.1 对话脚本 `dialogue.md`

覆盖上、下两部分的全部对话：

```markdown
# 第X集：[标题] 对话脚本

## 注意：本集视频不带字幕，对话通过配音传达

## 上半部分（Part A：00:00-00:15）
## 视频编号：DM-001-EP01-A

| 序号 | 时间 | 角色 | 对话内容（中文） | 语气/情感 | 备注 |
|------|------|------|----------------|----------|------|
| 1 | 00:02 | 角色A | 「对话内容」 | 坚定 | — |
| 2 | 00:06 | 角色B | 「对话内容」 | 惊讶 | — |
| 3 | 00:11 | 角色A | 「对话内容」 | 激动 | — |

## 下半部分（Part B：00:15-00:30）
## 视频编号：DM-001-EP01-B

| 序号 | 时间 | 角色 | 对话内容（中文） | 语气/情感 | 备注 |
|------|------|------|----------------|----------|------|
| 4 | 00:17 | 角色B | 「对话内容」 | 低沉 | — |
| 5 | 00:22 | 角色A | 「对话内容」 | 温柔 | — |
| 6 | 00:27 | 角色C | 「对话内容」 | 神秘 | — |
```

#### 4.2 故事板配置 `storyboard_config.json`

包含上、下两部分，每部分 **9宫格分镜**（3×3布局，16:9比例）：

```json
{
  "video_id_prefix": "DM-001-EP01",
  "episode": 1,
  "episode_title": "第1集标题",
  "total_duration_seconds": 30,
  "fps": 24,
  "resolution": "1920x1080",
  "aspect_ratio": "16:9",
  "style": "short_drama",
  "visual_style": {
    "style_id": 1,
    "style_name": "Cinematic Film",
    "camera": "Panavision Sphero 65 and Hasselblad Lenses",
    "film_stock": "Vision3 500T 5219",
    "filter": "ND0.6, Diffusion Filter 1/4",
    "focal_length": "65mm",
    "aperture": "f/2.0",
    "prompt_suffix": "shot on Panavision Sphero 65 and Hasselblad Lenses, Vision3 500T 5219, ND0.6, Diffusion Filter 1/4, cinematic film grain, shallow depth of field"
  },
  "subtitle": false,
  "synopsis": "本集剧情概要（100字）",
  "emotion_tone": "情感基调",
  "connection": {
    "from_previous": "与上集的衔接",
    "to_next": "为下集的铺垫"
  },

  "part_a": {
    "video_id": "DM-001-EP01-A",
    "label": "上",
    "time_range": "00:00-00:15",
    "duration_seconds": 15,
    "scene_refs": ["scene_01"],
    "prop_refs": [],
    "atmosphere": {
      "overall_mood": "上半部分氛围总描述",
      "color_palette": ["#色值1", "#色值2", "#色值3"],
      "lighting": "光影描述",
      "weather": "天气/环境"
    },
    "video_prompt": "English prompt for AI video generation of Part A (15s), 16:9 aspect ratio. No subtitles.",
    "bgm": {
      "description": "背景音乐描述",
      "mood": "音乐情绪关键词"
    },
    "storyboard_9grid": [
      {
        "grid_number": 1,
        "time_start": 0.0,
        "time_end": 1.67,
        "scene_description": "画面描述（50字，含人物动作、表情、光影）",
        "camera": {
          "type": "远景|中景|近景|特写",
          "movement": "固定|推|拉|摇|移|跟",
          "angle": "平视|俯视|仰视"
        },
        "characters": [
          {
            "name": "角色名",
            "action": "动作描述",
            "expression": "表情",
            "position": "画面位置(左/中/右)"
          }
        ],
        "dialogue": {
          "speaker": "角色名（无对话则为null）",
          "text": "中文对话内容",
          "emotion": "语气/情感"
        },
        "atmosphere": "本格氛围描述",
        "sfx": "音效描述",
        "ai_image_prompt": "English prompt for this grid's image: character, composition, lighting, mood, 16:9 aspect ratio. [visual_style.prompt_suffix will be appended automatically]"
      },
      {
        "grid_number": 2,
        "time_start": 1.67,
        "time_end": 3.33,
        "scene_description": "...",
        "camera": {},
        "characters": [],
        "dialogue": {},
        "atmosphere": "...",
        "sfx": "...",
        "ai_image_prompt": "..."
      },
      { "grid_number": 3, "time_start": 3.33, "time_end": 5.0, "...": "同上结构" },
      { "grid_number": 4, "time_start": 5.0, "time_end": 6.67, "...": "同上结构" },
      { "grid_number": 5, "time_start": 6.67, "time_end": 8.33, "...": "同上结构" },
      { "grid_number": 6, "time_start": 8.33, "time_end": 10.0, "...": "同上结构" },
      { "grid_number": 7, "time_start": 10.0, "time_end": 11.67, "...": "同上结构" },
      { "grid_number": 8, "time_start": 11.67, "time_end": 13.33, "...": "同上结构" },
      { "grid_number": 9, "time_start": 13.33, "time_end": 15.0, "...": "同上结构" }
    ]
  },

  "part_b": {
    "video_id": "DM-001-EP01-B",
    "label": "下",
    "time_range": "00:15-00:30",
    "duration_seconds": 15,
    "scene_refs": ["scene_02"],
    "prop_refs": ["prop_01"],
    "atmosphere": {
      "overall_mood": "下半部分氛围总描述",
      "color_palette": ["#色值1", "#色值2", "#色值3"],
      "lighting": "光影描述",
      "weather": "天气/环境"
    },
    "video_prompt": "English prompt for AI video generation of Part B (15s), 16:9 aspect ratio. No subtitles.",
    "bgm": {
      "description": "背景音乐描述",
      "mood": "音乐情绪关键词"
    },
    "storyboard_9grid": [
      {
        "grid_number": 1,
        "time_start": 0.0,
        "time_end": 1.67,
        "scene_description": "画面描述（50字）",
        "camera": {},
        "characters": [],
        "dialogue": {},
        "atmosphere": "...",
        "sfx": "...",
        "ai_image_prompt": "..."
      },
      { "grid_number": 2, "time_start": 1.67, "time_end": 3.33, "...": "同上结构" },
      { "grid_number": 3, "time_start": 3.33, "time_end": 5.0, "...": "同上结构" },
      { "grid_number": 4, "time_start": 5.0, "time_end": 6.67, "...": "同上结构" },
      { "grid_number": 5, "time_start": 6.67, "time_end": 8.33, "...": "同上结构" },
      { "grid_number": 6, "time_start": 8.33, "time_end": 10.0, "...": "同上结构" },
      { "grid_number": 7, "time_start": 10.0, "time_end": 11.67, "...": "同上结构" },
      { "grid_number": 8, "time_start": 11.67, "time_end": 13.33, "...": "同上结构" },
      { "grid_number": 9, "time_start": 13.33, "time_end": 15.0, "...": "同上结构" }
    ]
  }
}
```

> **注意**：`seedance_tasks.json` 不在本步骤生成，而是在阶段3（媒体生成后）的第七步中生成，因为 prompt 需要引用实际存在的角色参考图和分镜图文件。

**9宫格分镜布局说明**（3行×3列，16:9比例）：

```
| 格1 (0.0-1.67s)  | 格2 (1.67-3.33s) | 格3 (3.33-5.0s)  |
|:---:|:---:|:---:|
| 格4 (5.0-6.67s)  | 格5 (6.67-8.33s) | 格6 (8.33-10.0s) |
|:---:|:---:|:---:|
| 格7 (10.0-11.67s) | 格8 (11.67-13.33s) | 格9 (13.33-15.0s) |
```

- 每格约 **1.67秒**，9格覆盖 **15秒**
- 上下两部分各有独立的9宫格
- 每集共 **18格分镜**（上9格 + 下9格）
- 每个Part包含 `scene_refs`（引用的场景ID数组）和 `prop_refs`（引用的道具ID数组）

### 第五步：生成视频编号管理索引

生成 `video_index.json`：

```json
{
  "project_id": "DM-001",
  "project_name": "作品名称",
  "total_episodes": 25,
  "created_date": "2026-02-14",
  "status": "scripted",
  "videos": [
    {
      "episode": 1,
      "episode_title": "第1集标题",
      "part_a": {
        "video_id": "DM-001-EP01-A",
        "label": "上",
        "duration": 15,
        "status": "script_ready",
        "files": {
          "dialogue": "episodes/EP01/dialogue.md",
          "storyboard_config": "episodes/EP01/storyboard_config.json"
        }
      },
      "part_b": {
        "video_id": "DM-001-EP01-B",
        "label": "下",
        "duration": 15,
        "status": "script_ready",
        "files": {
          "dialogue": "episodes/EP01/dialogue.md",
          "storyboard_config": "episodes/EP01/storyboard_config.json"
        }
      }
    }
  ],
  "editing_guide": {
    "total_episodes": 25,
    "parts_per_episode": 2,
    "total_videos": 50,
    "duration_per_part_seconds": 15,
    "total_duration_seconds": 750,
    "grids_per_part": 9,
    "total_grids": 450,
    "recommended_export_format": "MP4 H.264",
    "recommended_resolution": "1920x1080",
    "recommended_fps": 24
  }
}
```

### 第六步：更新全局索引

更新 `/data/dongman/projects/index.json`：

```json
{
  "last_updated": "2026-02-14",
  "total_projects": 1,
  "next_id": "DM-002",
  "projects": [
    {
      "project_id": "DM-001",
      "project_name": "作品名称",
      "directory": "DM-001_xxxx/",
      "episodes": 25,
      "status": "scripted",
      "created_date": "2026-02-14",
      "video_count": 50
    }
  ]
}
```

### 第七步：生成 Seedance 任务（⚠️ 媒体生成后执行）

> **前置条件**：必须先运行 `generate-media` 技能，确保以下文件已生成：
> - 角色参考图：`characters/{角色名}_ref.png`
> - 分镜参考图：`episodes/EPxx/{project_id}-EPxx-{A|B}_storyboard.png`

本步骤读取所有集的 `storyboard_config.json` 和 `dialogue.md`，结合已生成的媒体文件，在项目根目录生成 **唯一一份** `seedance_project_tasks.json`（50条任务，每集Part-A/B各一条）。

**不再在每集目录下生成 `seedance_tasks.json`**，所有任务集中在项目根目录的 `seedance_project_tasks.json` 中。

#### 7.1 seedance_project_tasks.json 格式

```json
{
  "project_id": "DM-001",
  "project_name": "作品名称",
  "total_tasks": 50,
  "created_date": "2026-02-21",
  "tasks": [
    {
      "prompt": "(@DM-001-EP01-A_storyboard.png) 为9宫格分镜参考图，(@角色A_ref.png) 为角色「角色A」的参考形象，(@角色B_ref.png) 为角色「角色B」的参考形象。\n\n从镜头1开始，不要展示多宫格分镜参考图片。分镜图制作成电影级别的高清影视级别的视频。严禁参考图出现在画面中。每个画面为单一画幅，独立展示，没有任何分割线或多宫格效果画面。(Exclusions); Do not show speech bubbles, do not show comic panels, remove all text, full technicolor.排除项: No speech bubbles(无对话气泡),No text(无文字), No comic panels(无漫画分镜),No split screen(无分屏),No monochrome(非单色/黑白),No manga effects(无漫画特效线).正向替代:Fullscreen(全屏),Single continuous scene(单一连续场景).表情、嘴型、呼吸、台词严格同步。去掉图片中的水印，不要出现任何水印。没有任何字幕。\n\nDM-001-EP01-A 第1集「集标题」上半部分。剧情概要。 氛围：氛围描述。\n\n镜头1(0.0s-1.67s): 第1集上半第1格：场景描述。 (@角色A_ref.png)角色A动作，表情表情。 (@角色A_ref.png)角色A说：\"对话内容\"\uff08情感\uff09\n镜头2(1.67s-3.33s): ...\n...\n镜头9(13.33s-15.0s): ...",
      "description": "DM-001 EP01 Part-A 「集标题」上半部分 9宫格分镜→视频",
      "modelConfig": {
        "model": "Seedance 2.0 Fast",
        "referenceMode": "全能参考",
        "aspectRatio": "16:9",
        "duration": "15s"
      },
      "referenceFiles": [
        "episodes/EP01/DM-001-EP01-A_storyboard.png",
        "characters/角色A_ref.png",
        "characters/角色B_ref.png"
      ],
      "realSubmit": false,
      "priority": 1,
      "tags": ["DM-001", "EP01", "A"]
    },
    {
      "prompt": "... Part-B prompt ...",
      "description": "DM-001 EP01 Part-B 「集标题」下半部分 6宫格分镜→视频",
      "...":  "同上结构"
    }
  ]
}
```

**任务排列顺序**：EP01-A, EP01-B, EP02-A, EP02-B, ..., EP25-A, EP25-B（共50条）

#### 7.2 prompt 构建规则

1. **头部声明**：列出分镜图和角色参考图
   - `(@{project_id}-EPxx-{A|B}_storyboard.png) 为9宫格分镜参考图`
   - `(@{角色名}_ref.png) 为角色「{角色名}」的参考形象`（仅列出本part出场的角色）
   - **注意**：场景和道具参考图**不在头部声明**，在后文内联引用

2. **标准排除指令**（每个prompt必须包含）：
   ```
   从镜头1开始，不要展示多宫格分镜参考图片。分镜图制作成电影级别的高清影视级别的视频。严禁参考图出现在画面中。每个画面为单一画幅，独立展示，没有任何分割线或多宫格效果画面。(Exclusions); Do not show speech bubbles, do not show comic panels, remove all text, full technicolor.排除项: No speech bubbles(无对话气泡),No text(无文字), No comic panels(无漫画分镜),No split screen(无分屏),No monochrome(非单色/黑白),No manga effects(无漫画特效线).正向替代:Fullscreen(全屏),Single continuous scene(单一连续场景).表情、嘴型、呼吸、台词严格同步。去掉图片中的水印，不要出现任何水印。没有任何字幕。
   ```

3. **集信息行 + 场景/道具内联引用**：
   ```
   {video_id} 第X集「{episode_title}」{上/下}半部分。{synopsis}。 氛围：{atmosphere.overall_mood}。 场景参考 (@{场景ID}_ref.png) (@{场景ID}_ref.png)。道具参考 (@{道具ID}_ref.png)。
   ```
   - 场景/道具参考以 `(@xx_ref.png)` 形式直接在氛围描述后内联，不额外说明"为场景XXX的参考图"
   - 无场景/道具引用时省略该段

4. **逐镜头描述**（基于 `storyboard_9grid` 生成9条）：
   ```
   镜头N(time_start-time_end): 第X集{上/下}半第N格：{scene_description}。{camera.movement}{camera.type}{camera.angle}。{atmosphere}。 音效:{sfx}。 (@{角色名}_ref.png){角色名}{action}，表情{expression}。 (@{角色名}_ref.png){角色名}说：\"{dialogue.text}\"（{dialogue.emotion}）
   ```
   - 旁白格式：`旁白，{emotion}：\"{text}\"`
   - 无对话的角色仅描述动作表情
   - 每个角色提及时都用 `(@{角色名}_ref.png)` 前缀

5. **referenceFiles 构建规则**：
   - 分镜参考图：`episodes/EPxx/{project_id}-EPxx-{A|B}_storyboard.png`
   - 本part出场角色参考图：`characters/{角色名}_ref.png`（按出场顺序，去重）
   - 本part涉及场景参考图：`scenes/{场景ID}_ref.png`（四宫格合成图，如有；prompt中以内联 `(@xx_ref.png)` 引用，不在头部声明）
   - 本part涉及道具参考图：`props/{道具ID}_ref.png`（三视图合成图，如有；同上内联引用）

#### 7.3 提交流程

`seedance_project_tasks.json` 即为整部作品的唯一任务文件，供 `submit-anime-project` 技能直接读取并批量推送。

---

## 编号规则

### 作品编号
- 格式：`DM-XXX`（XXX为三位数字，从001递增）
- 示例：`DM-001`, `DM-002`, `DM-003`

### 视频编号
- **上半部分**：`{作品编号}-EP{集数两位}-A`
  - 示例：`DM-001-EP01-A`, `DM-001-EP25-A`
- **下半部分**：`{作品编号}-EP{集数两位}-B`
  - 示例：`DM-001-EP01-B`, `DM-001-EP25-B`

### 集数编号
- 格式：`EP{两位数字}`，从 `EP01` 到 `EP25`

---

## 内容创作规范

### 剧本要求
1. **故事完整性**：25集需要有完整的起承转合
   - 第1-3集：世界观介绍、角色登场、引入冲突
   - 第4-8集：冲突升级、角色关系建立
   - 第9-15集：高潮前奏、多线叙事、伏笔布局
   - 第16-20集：高潮阶段、转折、揭示
   - 第21-24集：最终决战、情感爆发
   - 第25集：结局、余韵
2. **每集30秒约束**：每集聚焦一个核心场景/事件，信息密度高
3. **上下结构**：每集上半部分（15s）铺垫/展开，下半部分（15s）高潮/转折
4. 每集结尾留悬念或情感钩子

### 对话要求
1. **语言**：所有对话必须为中文
2. **风格**：符合角色性格，简洁有力（每句不超过15字为佳）
3. **无字幕**：对话通过配音传达，不添加任何字幕
4. 每集对话控制在3-6句（上下各1-3句）

### 9宫格分镜要求
1. **时长**：每部分固定15秒
2. **格数**：固定9格（3×3布局，16:9比例）
3. 每格约 **1.67秒**
4. 9格之间需要有视觉连续性和叙事逻辑
5. 每格必须包含：画面描述、镜头类型、对话（如有）、氛围描述
6. 上半部分和下半部分各有独立的整体氛围描述
7. 每部分附带 `video_prompt`（英文，简洁描述）
8. 每个Part包含 `scene_refs` 和 `prop_refs` 数组，列出本Part引用的场景/道具ID

### 故事板配置要求
1. JSON格式，可被程序直接解析
2. 包含 `part_a` 和 `part_b` 两个完整部分
3. 每部分包含：氛围、9宫格分镜、scene_refs、prop_refs
4. 包含AI图像生成的英文Prompt
5. `subtitle` 字段始终为 `false`

---

## 运行指令

用户可以通过以下方式触发本技能：
- "制作一部短剧"
- "生成短剧作品"
- "produce short drama"
- "创建新短剧"
- "开始制作短剧"
- "运行"（在技能上下文中）

可附带可选参数：
- **题材/类型**：如 "制作一部科幻短剧"、"生成一部校园恋爱短剧"
- **视觉风格**：如 "港风复古"、"Vintage Hong Kong"、"风格7"（指定 visual_styles.json 中的预设）
- **风格**：如 "赛博朋克风格"、"中国风"
- **角色数量**：如 "主角3人"

如用户未指定题材，则随机选择一个有趣的原创题材。
如用户未指定视觉风格，则使用 `visual_styles.json` 中 `default_style_id` 对应的默认风格。

---

## 执行检查清单

### 阶段1：剧本制作完成后自查
- [ ] `index.json` 全局索引已更新
- [ ] `metadata.json` 作品元数据已创建
- [ ] `full_script.md` 完整剧本已生成（含25集概要）
- [ ] `character_bible.md` 角色设计已完成
- [ ] `scenes/scene_bible.md` 场景设计已完成（3-6个核心场景）
- [ ] `props/prop_bible.md` 道具设计已完成（2-5个核心道具）
- [ ] EP01-EP25 所有25个集目录均已创建
- [ ] 每集包含2个文件：`dialogue.md`, `storyboard_config.json`
- [ ] 每集的 `storyboard_config.json` 包含 `part_a` 和 `part_b`
- [ ] 每部分包含9宫格分镜
- [ ] 所有视频编号遵循命名规则（`-A` / `-B` 后缀）
- [ ] `video_index.json` 已生成且包含50条视频记录（25集×2部分）
- [ ] 所有对话为中文
- [ ] 所有配置标注 `subtitle: false`
- [ ] 每集剧情有起承转合的衔接

### 阶段3：媒体生成后，Seedance任务生成自查
- [ ] 角色参考图已存在：`characters/{角色名}_ref.png`
- [ ] 场景四宫格图已存在：`scenes/{场景ID}_ref.png`（每场景1张合成图）
- [ ] 道具三视图已存在：`props/{道具ID}_ref.png`（每道具1张合成图）
- [ ] 分镜参考图已存在：`episodes/EPxx/{project_id}-EPxx-{A|B}_storyboard.png`
- [ ] 项目根目录 `seedance_project_tasks.json` 已生成（总计50条任务）
- [ ] 每条任务的 prompt 使用 `(@文件名)` 格式引用参考图
- [ ] 每条任务的 prompt 包含标准排除指令
- [ ] 每条任务的 prompt 包含逐镜头描述（9条）
- [ ] 每条任务的 `referenceFiles` 列出所有引用的图片路径（分镜图 + 角色 + 场景 + 道具）
- [ ] 不存在每集目录下的 `seedance_tasks.json`（已统一到项目根目录）

---

## 输出示例

### 阶段1完成后报告：

```
✅ 短剧剧本制作完成！

📋 作品信息
- 作品编号：DM-001
- 作品名称：《xxxxx》
- 视觉风格：Cinematic Film（电影质感）
- 类型：xxxxx
- 总集数：25集（每集上下两部分）

📁 项目目录：/data/dongman/projects/DM-001_xxxx/

📊 生成内容统计
- 完整剧本：1份
- 角色设定：X个角色
- 场景设定：X个核心场景
- 道具设定：X个核心道具
- 对话脚本：25份（每集1份，覆盖上下两部分）
- 故事板配置：25份（每集1份，含上下两部分9宫格+场景/道具引用+视频提示词）
- 视频总数：50个（25集 × 上下2部分）
- 总分镜格数：450格（50个视频 × 9格）

🎬 视频编号范围
- 上半部分：DM-001-EP01-A ~ DM-001-EP25-A
- 下半部分：DM-001-EP01-B ~ DM-001-EP25-B

📂 每集文件（2个）
- dialogue.md            → 对话脚本
- storyboard_config.json → 故事板配置（含9宫格分镜 + scene_refs/prop_refs）

⏭️ 下一步
1. 运行 generate-media 技能生成角色参考图 + 分镜图
2. 运行本技能第七步生成 seedance_project_tasks.json（含 @图片引用，50条任务）
3. 运行 submit-anime-project 技能提交任务
```