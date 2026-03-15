---
name: produce-mv
description: MV制作技能。根据歌曲歌词或已有MV剧本，结合用户提供的角色/场景参考图片（支持读取指定文件夹），生成完整MV分镜、故事板配置和Seedance视频生成任务。关键词：MV、音乐视频、Music Video、分镜、歌词、storyboard、视频生成。
---

# MV制作技能 (Produce Music Video)

## 概述

本技能用于自动化生成完整MV（音乐视频）作品的全套制作文档和Seedance视频生成任务。支持两种输入模式：

1. **从歌词/剧本创作**：根据用户提供的歌词或MV剧本，自动生成完整的分镜设计和视频生成任务
2. **从已有素材导入**：读取用户指定文件夹下的角色参考图片、场景图片等，结合剧本生成视频任务

### MV特点（与短剧的区别）

| 维度 | 短剧（produce-anime） | MV（produce-mv） |
|------|----------------------|-------------------|
| 结构 | 25集 × 上下两部分 | 按歌曲段落分段（通常8-20段） |
| 驱动 | 剧情驱动 | 音乐/歌词节奏驱动 |
| 编号 | DM-XXX | MV-XXX |
| 子目录 | episodes/EP01-EP25 | segments/SEG01-SEGxx |
| 每段时长 | 固定15s/part | 固定15s/segment |
| 总时长 | 固定12分30秒 | 取决于歌曲长度（通常3-5分钟） |
| 对话 | 中文人物对话 | 歌词（可含念白/独白） |
| 视觉风格 | 统一风格 | 支持多风格交替（如现实/幻想切换） |
| 素材来源 | 自动生成所有角色图 | 支持导入用户已有素材 |

### 完整工作流程（4个阶段）

| 阶段 | 技能 | 产出 |
|------|------|------|
| 1. MV制作 | `produce-mv` | mv_script.md, character_bible.md, storyboard_config.json, video_index.json |
| 2. 媒体生成 | `generate-media` | 角色参考图 + 场景参考图 + 分镜图 |
| 3. 任务生成 | `produce-mv`（第七步） | seedance_project_tasks.json（使用 `(@文件名)` 引用图片） |
| 4. 任务提交 | `submit-anime-project` | 批量推送到 Seedance API |

---

## 视觉风格预设

项目支持从 `/data/dongman/.config/visual_styles.json` 读取视觉风格预设。MV特别支持**多风格交替**（如现实风格A + 幻想风格B交替）。

> **⚠️ 风格选择交互**：在开始制作前，使用 `ask_questions` 工具让用户选择视觉风格。MV可以选择：
> - 单一风格：全片统一
> - 双风格交替：如"现实世界"用风格A，"幻想世界"用风格B（在 `metadata.json` 的 `visual_styles` 数组中记录）

---

## 执行流程

当用户要求制作MV时，按以下步骤顺序执行：

### 第一步：初始化项目

1. 读取 `/data/dongman/projects/index.json` 获取当前作品编号
   - MV项目使用 `MV-XXX` 编号（与短剧 `DM-XXX` 区分）
   - 如 `index.json` 中无 MV 项目，从 `MV-001` 开始
2. 在 `/data/dongman/projects/` 下创建新作品目录，命名规则：`{MV编号}_{作品名称拼音缩写}/`
3. 创建作品目录结构：

```
projects/
├── index.json                              # 所有作品索引（全局，DM+MV共用）
└── MV-001_xxxx/                            # 单部MV作品目录
    ├── metadata.json                       # 作品元数据
    ├── script/
    │   └── mv_script.md                    # 完整MV分镜剧本
    ├── characters/                         # 角色设计
    │   ├── character_bible.md              # 角色圣经
    │   └── ref_index.json                  # 角色参考图索引
    ├── scenes/                             # 场景设计
    │   ├── scene_bible.md                  # 场景圣经
    │   └── ref_index.json
    ├── props/                              # 道具设计
    │   ├── prop_bible.md                   # 道具圣经
    │   └── ref_index.json
    ├── assets/                             # 外部导入素材（用户提供）
    │   └── README.md                       # 素材说明
    ├── segments/                           # 各段内容（每段15s）
    │   ├── SEG01/
    │   │   └── storyboard_config.json      # 本段故事板配置（含9宫格分镜）
    │   ├── SEG02/
    │   │   └── storyboard_config.json
    │   └── ... (SEG01-SEGxx)
    ├── seedance_project_tasks.json         # [阶段3·媒体生成后] 全MV Seedance任务
    └── video_index.json                    # 视频编号管理索引
```

### 第二步：读取/导入素材（可选）

如用户指定了素材文件夹路径，执行素材导入：

#### 2.1 扫描素材文件夹

```python
# 接受用户指定的文件夹路径（绝对路径或相对于workspace的路径）
# 扫描以下类型的文件：
# - 图片：.png, .jpg, .jpeg, .webp
# - 剧本：.md, .txt
# - 音频：.mp3, .wav（记录路径，不处理音频内容）
```

#### 2.2 素材分类与导入

1. **角色参考图**：
   - 文件名含 `角色名` 或 `character` 的图片 → 复制到 `characters/`
   - 自动更新 `characters/ref_index.json`
   - 如用户明确指定"xx.png是角色A的参考图"，按指定映射

2. **场景参考图**：
   - 文件名含 `scene` 或 `场景` 的图片 → 复制到 `scenes/`
   - 自动更新 `scenes/ref_index.json`

3. **道具参考图**：
   - 文件名含 `prop` 或 `道具` 的图片 → 复制到 `props/`
   - 自动更新 `props/ref_index.json`

4. **剧本文件**：
   - `.md` 或 `.txt` 文件 → 读取内容作为MV剧本输入

5. **其他素材**：
   - 复制到 `assets/`，记录到 `assets/README.md`

#### 2.3 交互确认

用 `ask_questions` 让用户确认素材映射：
- "检测到以下文件，请确认用途："
- 列出文件名及推测的用途（角色图/场景图/其他）
- 让用户调整映射

> **无素材模式**：如用户未指定素材文件夹，则所有角色/场景参考图在阶段2（generate-media）中自动生成。

### 第三步：读取/创作MV剧本

#### 模式A：从已有剧本读取

如果用户提供了MV剧本文件（如 `notes/mv reffiles/MV剧本：凡人歌的赛博神话.md`），读取并解析：

1. 解析剧本表格/段落，提取：
   - 每个分镜的**序号**
   - **歌词/听觉节奏**（对应时间线）
   - **画面内容**（视觉呈现描述）
   - **镜头运用**（Camera）
   - **画面风格 & 色调**
2. 根据段落数量计算Seedance分段数（每段15秒）
3. 将剧本适配为标准 `mv_script.md` 格式

#### 模式B：从歌词创作

如果用户只提供歌词（或歌曲名，由AI创作剧本），按以下步骤：

1. 分析歌词结构（前奏、主歌、副歌、间奏、尾声等）
2. 根据歌曲节奏设计视觉叙事
3. 确定风格方向（写实/幻想/混合）
4. 生成完整MV分镜剧本

#### 生成 `script/mv_script.md`

```markdown
# 《歌曲名》MV 完整分镜剧本

## 作品信息
- **歌曲名**：[歌曲名称]
- **艺术家/创作者**：[名称]
- **歌曲时长**：[X分X秒]
- **MV类型**：[叙事型/概念型/表演型/混合型]
- **视觉风格**：[风格描述]
  - 风格A（如适用）：[描述]
  - 风格B（如适用）：[描述]
- **核心概念**：[一句话概括MV核心视觉概念]
- **目标受众**：[目标群体]
- **总段数**：[X段 × 15秒 = 总时长]

## 歌曲结构分析
| 段落 | 时间范围 | 类型 | 情绪 |
|------|---------|------|------|
| 前奏 | 0:00-0:15 | instrumental | 压抑/悬念 |
| 主歌1 | 0:15-0:45 | verse | 叙述/平静 |
| 副歌1 | 0:45-1:15 | chorus | 爆发/激昂 |
| ... | ... | ... | ... |

## 世界观/视觉概念设定
[200-300字描述MV的视觉世界观]

## 分镜脚本

### 分镜01：[段落标题]
- **时间**：0:00-0:15（对应Segment SEG01）
- **歌词/音频**：[对应歌词或音乐描述]
- **画面内容**：[100字详细视觉描述]
- **镜头运用**：[镜头类型+运动方式]
- **画面风格**：[风格A/B + 色调描述]
- **出场角色**：[角色列表]
- **使用场景**：[场景ID列表]
- **使用道具**：[道具ID列表]
- **情感基调**：[情绪关键词]
- **AI绘图关键词（英文）**：[用于生成分镜图的Prompt]

### 分镜02：[段落标题]
...（按歌曲结构分段）

## 导演备注
[关于视觉叙事、卡点设计、转场技巧、色彩隐喻等总体执行建议]
```

### 第四步：角色/场景/道具设计

#### 4.1 角色设计 `characters/character_bible.md`

如果已从素材文件夹导入了角色参考图，角色设定基于已有图片描述：

```markdown
# MV角色设定集

## 主角

### 角色1：[名字/代号]
- **角色定位**：[主角/配角/群演]
- **外貌特征**：[详细描述]
- **服装设计**：
  - 风格A造型：[现实世界服装]
  - 风格B造型：[幻想世界服装]（如适用）
- **角色弧光**：[在MV中的情感/状态变化]
- **参考图来源**：[imported/generated]
  - 导入文件：[原始文件名]（如为导入）
- **AI绘图关键词（英文）**：[Prompt]

## 群演/配角
...
```

#### 4.2 场景设计 `scenes/scene_bible.md`

```markdown
# MV场景设定集

## 场景1：[场景名称]
- **场景ID**：scene_01
- **场景类型**：[现实/幻想/过渡]
- **场景描述**：[详细描述]
- **出现段落**：SEG01, SEG03, SEG05...
- **色调/氛围**：[色调描述]
- **参考图来源**：[imported/generated]
- **AI绘图关键词（英文）**：[Prompt]
```

#### 4.3 道具设计 `props/prop_bible.md`

```markdown
# MV道具设定集

## 道具1：[道具名称]
- **道具ID**：prop_01
- **道具描述**：[外观/材质/尺寸]
- **象征意义**：[在MV中的视觉象征]
- **出现段落**：SEG02, SEG08, SEG15
- **参考图来源**：[imported/generated]
- **AI绘图关键词（英文）**：[Prompt]
```

> **素材优先原则**：如果用户已导入某角色/场景/道具的参考图，则 `character_bible.md` / `scene_bible.md` / `prop_bible.md` 中对应条目的 `参考图来源` 标记为 `imported`，不再通过 `generate-media` 重复生成。

### 第四步B：资产完整性检查与补全

完成第四步角色/场景/道具设计后，**必须执行资产完整性检查**，确保所有在分镜中被引用的资产都有对应的参考图或生成计划。

#### 检查逻辑

```python
def check_asset_completeness(project_dir):
    """检查所有资产是否完整，返回缺失清单"""
    missing = {"characters": [], "scenes": [], "props": []}
    
    # 1. 解析角色圣经，检查每个角色是否有参考图
    characters = parse_character_bible(project_dir / "characters/character_bible.md")
    for char in characters:
        ref_path = project_dir / f"characters/{char['name']}_ref.png"
        if not ref_path.exists():
            missing["characters"].append(char)
    
    # 2. 解析场景圣经，检查每个场景是否有参考图
    scenes = parse_scene_bible(project_dir / "scenes/scene_bible.md")
    for scene in scenes:
        ref_path = project_dir / f"scenes/{scene['id']}_ref.png"
        if not ref_path.exists():
            missing["scenes"].append(scene)
    
    # 3. 解析道具圣经，检查每个道具是否有参考图
    props = parse_prop_bible(project_dir / "props/prop_bible.md")
    for prop in props:
        ref_path = project_dir / f"props/{prop['id']}_ref.png"
        if not ref_path.exists():
            missing["props"].append(prop)
    
    return missing
```

#### 补全策略

资产缺失时，按以下优先级补全：

| 优先级 | 补全方式 | 适用场景 | 说明 |
|--------|---------|---------|------|
| 1 | 用户手动提供 | 用户有现成素材 | 通过 `ask_questions` 询问用户是否有可用素材 |
| 2 | 自动生成 | 无现成素材 | 调用 `generate-media` 技能的对应阶段自动生成 |
| 3 | 标记待生成 | 批量处理模式 | 在 `ref_index.json` 中标记 `status: "pending"`，统一在阶段2生成 |

#### 补全执行流程

1. **汇总缺失资产清单**：
   ```
   ⚠️ 资产完整性检查结果：
   - 角色参考图缺失：3个（主角、配角A、配角B）
   - 场景参考图缺失：2个（scene_01 出租屋、scene_03 地铁站）
   - 道具参考图缺失：1个（prop_01 AR眼镜）
   ```

2. **交互确认补全方式**：
   使用 `ask_questions` 让用户选择补全策略：
   - 选项A：「立即自动生成所有缺失资产」→ 直接调用 `generate-media` 补全
   - 选项B：「我稍后手动提供部分素材」→ 标记为 `pending`，继续后续步骤
   - 选项C：「跳过缺失资产，仅用已有素材」→ 在 prompt 中不引用缺失资产的 `(@xx_ref.png)`

3. **自动补全角色参考图**（选项A时）：
   - 从 `character_bible.md` 读取缺失角色的 `AI绘图关键词（英文）`
   - 调用 Gemini 图片模型生成角色参考图
   - 保存到 `characters/{角色名}_ref.png`
   - 更新 `characters/ref_index.json`，标记 `source: "generated"`

4. **自动补全场景参考图**（选项A时）：
   - 从 `scene_bible.md` 读取缺失场景的 `AI绘图关键词（英文）`
   - 生成四宫格合成图（正面/左45°/右45°/背面）
   - 保存到 `scenes/{场景ID}_ref.png`
   - 更新 `scenes/ref_index.json`，标记 `source: "generated"`

5. **自动补全道具参考图**（选项A时）：
   - 从 `prop_bible.md` 读取缺失道具的 `AI绘图关键词（英文）`
   - 生成三视图合成图（正面/侧面/俯视）
   - 保存到 `props/{道具ID}_ref.png`
   - 更新 `props/ref_index.json`，标记 `source: "generated"`

6. **更新 ref_index.json**：

   补全后的 `ref_index.json` 示例：
   ```json
   {
     "主角": {
       "source": "imported",
       "original_file": "hero_front.png",
       "ref_file": "characters/主角_ref.png",
       "status": "ready"
     },
     "配角A": {
       "source": "generated",
       "ref_file": "characters/配角A_ref.png",
       "status": "ready",
       "generated_date": "2026-02-23"
     },
     "群演B": {
       "source": "pending",
       "ref_file": null,
       "status": "pending",
       "reason": "用户选择稍后提供"
     }
   }
   ```

#### 分镜引用时的缺失处理

在第七步生成 Seedance 任务时，如某资产仍为 `pending` 状态：
- **不在 prompt 头部声明**该资产的 `(@xx_ref.png)` 引用
- **不加入 referenceFiles** 数组
- 在 prompt 的镜头描述中，改用**纯文字描述**替代图片引用（降级方案）
- 在任务的 `tags` 中追加 `"incomplete_refs"` 标记，便于后续排查

> **⚠️ 重要**：资产补全是 MV 制作的关键步骤。缺失参考图会直接影响 Seedance 视频生成的角色一致性和场景准确性。建议优先选择「立即自动生成」，确保所有资产就绪后再进入分镜图生成和任务提交阶段。

### 第五步：逐段生成故事板配置

#### 5.1 确定段数

根据歌曲时长计算段数：
- 总段数 = ceil(歌曲总秒数 / 15)
- 例：4分钟歌曲 = 240秒 = 16段

#### 5.2 生成 `storyboard_config.json`（每段1个）

对每个 Segment（SEG01-SEGxx），生成 `segments/SEGxx/storyboard_config.json`：

```json
{
  "video_id": "MV-001-SEG01",
  "project_type": "mv",
  "segment": 1,
  "total_segments": 16,
  "segment_title": "段落标题",
  "duration_seconds": 15,
  "fps": 24,
  "resolution": "1920x1080",
  "aspect_ratio": "16:9",
  "style": "music_video",
  "visual_style": {
    "style_id": 1,
    "style_name": "Cinematic Film",
    "camera": "...",
    "film_stock": "...",
    "filter": "...",
    "focal_length": "...",
    "aperture": "...",
    "prompt_suffix": "..."
  },
  "active_visual_mode": "style_a",
  "subtitle": false,

  "music_sync": {
    "time_range_in_song": "0:00-0:15",
    "lyrics": "对应歌词文本（可含多句）",
    "music_section": "intro",
    "tempo": "slow",
    "emotion_curve": "building"
  },

  "scene_refs": ["scene_01"],
  "prop_refs": [],
  "character_refs": ["主角"],

  "atmosphere": {
    "overall_mood": "段落氛围总描述",
    "color_palette": ["#色值1", "#色值2", "#色值3"],
    "lighting": "光影描述",
    "weather": "天气/环境"
  },

  "video_prompt": "English prompt for AI video generation of this segment (15s), 16:9 aspect ratio.",

  "bgm": {
    "description": "本段音乐特征",
    "mood": "音乐情绪关键词",
    "instruments": "主要乐器",
    "dynamics": "力度变化（渐强/渐弱/突强等）"
  },

  "storyboard_9grid": [
    {
      "grid_number": 1,
      "time_start": 0.0,
      "time_end": 1.67,
      "scene_description": "画面描述（50字，含人物动作、表情、光影）",
      "lyrics_at_grid": "本格对应的歌词（如有）",
      "camera": {
        "type": "远景|中景|近景|特写",
        "movement": "固定|推|拉|摇|移|跟|环绕|航拍",
        "angle": "平视|俯视|仰视|主观",
        "special": "子弹时间|延时摄影|手持晃动 等（可选）"
      },
      "characters": [
        {
          "name": "角色名",
          "action": "动作描述",
          "expression": "表情",
          "position": "画面位置(左/中/右)"
        }
      ],
      "visual_mode": "style_a|style_b",
      "transition": {
        "type": "cut|dissolve|match_cut|glitch|shatter|none",
        "description": "转场描述（如有）"
      },
      "atmosphere": "本格氛围描述",
      "sfx": "音效描述",
      "ai_image_prompt": "English prompt for this grid's image: character, composition, lighting, mood, 16:9 aspect ratio. [visual_style.prompt_suffix will be appended automatically]"
    },
    {
      "grid_number": 2,
      "time_start": 1.67,
      "time_end": 3.33,
      "...": "同上结构"
    },
    { "grid_number": 3, "time_start": 3.33, "time_end": 5.0, "...": "同上" },
    { "grid_number": 4, "time_start": 5.0, "time_end": 6.67, "...": "同上" },
    { "grid_number": 5, "time_start": 6.67, "time_end": 8.33, "...": "同上" },
    { "grid_number": 6, "time_start": 8.33, "time_end": 10.0, "...": "同上" },
    { "grid_number": 7, "time_start": 10.0, "time_end": 11.67, "...": "同上" },
    { "grid_number": 8, "time_start": 11.67, "time_end": 13.33, "...": "同上" },
    { "grid_number": 9, "time_start": 13.33, "time_end": 15.0, "...": "同上" }
  ]
}
```

**与短剧storyboard的关键差异**：
- 增加 `music_sync` 节：记录歌词、音乐段落类型、节奏信息
- 增加 `active_visual_mode`：标识当前段使用的视觉风格模式
- 增加 `lyrics_at_grid`：每格对应的歌词
- 增加 `visual_mode`：每格的视觉风格（支持格间风格切换）
- 增加 `transition`：转场类型描述（MV转场更丰富）
- 无 `part_a` / `part_b` 划分：MV每段即一个完整的15s片段

**9宫格分镜布局**（与短剧一致，3行×3列，16:9比例）：

```
| 格1 (0.0-1.67s)  | 格2 (1.67-3.33s) | 格3 (3.33-5.0s)  |
| 格4 (5.0-6.67s)  | 格5 (6.67-8.33s) | 格6 (8.33-10.0s) |
| 格7 (10.0-11.67s) | 格8 (11.67-13.33s) | 格9 (13.33-15.0s) |
```

### 第六步：生成视频编号管理索引

生成 `video_index.json`：

```json
{
  "project_id": "MV-001",
  "project_type": "mv",
  "project_name": "作品名称",
  "song_title": "歌曲名",
  "total_segments": 16,
  "created_date": "2026-02-23",
  "status": "scripted",
  "videos": [
    {
      "segment": 1,
      "segment_title": "段落标题",
      "video_id": "MV-001-SEG01",
      "duration": 15,
      "music_section": "intro",
      "time_in_song": "0:00-0:15",
      "status": "script_ready",
      "files": {
        "storyboard_config": "segments/SEG01/storyboard_config.json"
      }
    },
    {
      "segment": 2,
      "video_id": "MV-001-SEG02",
      "...": "..."
    }
  ],
  "editing_guide": {
    "total_segments": 16,
    "total_videos": 16,
    "duration_per_segment_seconds": 15,
    "total_duration_seconds": 240,
    "grids_per_segment": 9,
    "total_grids": 144,
    "recommended_export_format": "MP4 H.264",
    "recommended_resolution": "1920x1080",
    "recommended_fps": 24,
    "post_production_note": "最终剪辑时需配合原曲音轨对齐每段节奏"
  }
}
```

### 更新全局索引

更新 `/data/dongman/projects/index.json`，MV项目与DM项目共存：

```json
{
  "last_updated": "2026-02-23",
  "total_projects": 4,
  "next_id": "DM-004",
  "next_mv_id": "MV-002",
  "projects": [
    { "project_id": "DM-001", "...": "..." },
    { "project_id": "DM-002", "...": "..." },
    { "project_id": "DM-003", "...": "..." },
    {
      "project_id": "MV-001",
      "project_type": "mv",
      "project_name": "凡人歌",
      "song_title": "XWOW-凡人歌",
      "directory": "MV-001_frc/",
      "segments": 16,
      "status": "scripted",
      "created_date": "2026-02-23",
      "video_count": 16
    }
  ]
}
```

### 第七步：生成 Seedance 任务（⚠️ 媒体生成后执行）

> **前置条件**：必须先运行 `generate-media` 技能，确保以下文件已生成：
> - 角色参考图：`characters/{角色名}_ref.png`（或从素材导入）
> - 场景参考图：`scenes/{场景ID}_ref.png`（或从素材导入）
> - 道具参考图：`props/{道具ID}_ref.png`（或从素材导入）
> - 分镜参考图：`segments/SEGxx/{project_id}-SEGxx_storyboard.png`

在项目根目录生成 `seedance_project_tasks.json`（任务数 = 段数）。

#### 7.1 seedance_project_tasks.json 格式

```json
{
  "project_id": "MV-001",
  "project_type": "mv",
  "project_name": "凡人歌",
  "song_title": "XWOW-凡人歌",
  "total_tasks": 16,
  "created_date": "2026-02-23",
  "tasks": [
    {
      "prompt": "(@MV-001-SEG01_storyboard.png) 为9宫格分镜参考图，(@主角_ref.png) 为角色「主角」的参考形象。\n\n从镜头1开始，不要展示多宫格分镜参考图片。分镜图制作成电影级别的高清影视级别的视频。严禁参考图出现在画面中。每个画面为单一画幅，独立展示，没有任何分割线或多宫格效果画面。(Exclusions); Do not show speech bubbles, do not show comic panels, remove all text, full technicolor.排除项: No speech bubbles(无对话气泡),No text(无文字), No comic panels(无漫画分镜),No split screen(无分屏),No monochrome(非单色/黑白),No manga effects(无漫画特效线).正向替代:Fullscreen(全屏),Single continuous scene(单一连续场景).表情、嘴型、呼吸、台词严格同步。去掉图片中的水印，不要出现任何水印。没有任何字幕。\n\nMV-001-SEG01 「段落标题」。歌词：[对应歌词]。 氛围：氛围描述。 场景参考 (@scene_01_ref.png)。\n\n镜头1(0.0s-1.67s): ...\n镜头2(1.67s-3.33s): ...\n...\n镜头9(13.33s-15.0s): ...",
      "description": "MV-001 SEG01 「段落标题」 MV分镜→视频",
      "modelConfig": {
        "model": "Seedance 2.0 Fast",
        "referenceMode": "全能参考",
        "aspectRatio": "16:9",
        "duration": "15s"
      },
      "referenceFiles": [
        "segments/SEG01/MV-001-SEG01_storyboard.png",
        "characters/主角_ref.png",
        "scenes/scene_01_ref.png"
      ],
      "realSubmit": false,
      "priority": 1,
      "tags": ["MV-001", "SEG01"]
    }
  ]
}
```

#### 7.2 prompt 构建规则（MV版）

1. **头部声明**：列出分镜图和角色参考图
   - `(@{project_id}-SEGxx_storyboard.png) 为9宫格分镜参考图`
   - `(@{角色名}_ref.png) 为角色「{角色名}」的参考形象`（仅列出本段出场角色）

2. **标准排除指令**（与短剧一致，每个prompt必须包含）：
   ```
   从镜头1开始，不要展示多宫格分镜参考图片。分镜图制作成电影级别的高清影视级别的视频。严禁参考图出现在画面中。每个画面为单一画幅，独立展示，没有任何分割线或多宫格效果画面。(Exclusions); Do not show speech bubbles, do not show comic panels, remove all text, full technicolor.排除项: No speech bubbles(无对话气泡),No text(无文字), No comic panels(无漫画分镜),No split screen(无分屏),No monochrome(非单色/黑白),No manga effects(无漫画特效线).正向替代:Fullscreen(全屏),Single continuous scene(单一连续场景).表情、嘴型、呼吸、台词严格同步。去掉图片中的水印，不要出现任何水印。没有任何字幕。
   ```

3. **段落信息行 + 歌词 + 场景/道具内联引用**：
   ```
   {video_id} 「{segment_title}」。歌词：{lyrics}。 氛围：{atmosphere.overall_mood}。 场景参考 (@{场景ID}_ref.png)。道具参考 (@{道具ID}_ref.png)。
   ```

4. **逐镜头描述**（9条，与短剧结构一致）：
   ```
   镜头N(time_start-time_end): 第X段第N格：{scene_description}。{camera.movement}{camera.type}{camera.angle}。歌词：{lyrics_at_grid}。{atmosphere}。 音效:{sfx}。 (@{角色名}_ref.png){角色名}{action}，表情{expression}。
   ```
   - MV中无对话，改为歌词同步描述
   - 如有风格切换，在转场格注明 `[风格切换: A→B]`
   - 每个角色提及时都用 `(@{角色名}_ref.png)` 前缀

5. **referenceFiles 构建规则**（与短剧一致）：
   - 分镜参考图：`segments/SEGxx/{project_id}-SEGxx_storyboard.png`
   - 角色参考图：`characters/{角色名}_ref.png`（按出场顺序，去重）
   - 场景参考图：`scenes/{场景ID}_ref.png`（如有）
   - 道具参考图：`props/{道具ID}_ref.png`（如有）

---

## 素材导入详细规范

### 导入流程

```
用户指定文件夹路径
       ↓
扫描文件夹（递归/非递归可选）
       ↓
按文件类型分类
       ↓
ask_questions 让用户确认映射
       ↓
复制/链接文件到项目目录
       ↓
更新 ref_index.json
```

### 支持的素材类型

| 素材类型 | 扩展名 | 导入目标 | 说明 |
|---------|--------|---------|------|
| 角色参考图 | .png/.jpg/.jpeg/.webp | characters/ | 重命名为 `{角色名}_ref.png` |
| 场景参考图 | .png/.jpg/.jpeg/.webp | scenes/ | 重命名为 `{scene_id}_ref.png` |
| 道具参考图 | .png/.jpg/.jpeg/.webp | props/ | 重命名为 `{prop_id}_ref.png` |
| MV剧本 | .md/.txt | script/ | 读取内容，转为 `mv_script.md` |
| 其他素材 | * | assets/ | 原名保留 |

### 素材映射交互示例

```
检测到以下文件：
1. hero_front.png → 角色参考图（推测角色名：hero）
2. city_night.jpg → 场景参考图
3. keyboard_glow.png → 道具参考图
4. mv_script.md → MV剧本

请确认或调整映射。
```

### ref_index.json 格式（素材导入后）

```json
{
  "主角": {
    "source": "imported",
    "original_file": "hero_front.png",
    "ref_file": "characters/主角_ref.png",
    "import_date": "2026-02-23"
  }
}
```

---

## metadata.json 格式

```json
{
  "project_id": "MV-001",
  "project_type": "mv",
  "project_name": "凡人歌",
  "project_name_en": "FanRenGe",
  "directory": "MV-001_frc/",
  "song_title": "XWOW-凡人歌",
  "song_artist": "XWOW",
  "song_duration_seconds": 240,
  "genre": "摇滚 / 赛博朋克",
  "mv_type": "叙事型+概念型",
  "visual_style": {
    "mode": "dual",
    "style_a": {
      "name": "灰暗现实主义",
      "description": "拥挤、压抑的现代都市，冷灰/暗蓝色调，手持镜头，颗粒感",
      "style_id": null,
      "prompt_suffix": "handheld camera, film grain, desaturated cold tones, blue-grey color palette, urban isolation"
    },
    "style_b": {
      "name": "东方赛博神话",
      "description": "宏大数字神话空间，鎏金色/霓虹蓝，平稳大气镜头，失重感",
      "style_id": null,
      "prompt_suffix": "epic cyber mythology, golden and neon blue palette, weightless atmosphere, digital particles, majestic scale"
    }
  },
  "target_audience": "青年 / 科技从业者",
  "total_segments": 16,
  "segment_duration_seconds": 15,
  "total_duration_seconds": 240,
  "core_concept": "凡人之躯，比肩神迹——平凡程序员在代码世界中创造传奇",
  "status": "scripted",
  "created_date": "2026-02-23",
  "video_count": 16,
  "imported_assets": {
    "characters": 0,
    "scenes": 0,
    "props": 0,
    "other": 0
  }
}
```

> **双风格模式说明**：当 `visual_style.mode` 为 `"dual"` 时，`style_a` 和 `style_b` 分别描述两种交替使用的视觉风格。每个 segment 的 `storyboard_config.json` 通过 `active_visual_mode` 字段指定使用哪种风格，每格通过 `visual_mode` 字段可进一步控制格级别的风格切换。

---

## 编号规则

### 作品编号
- MV格式：`MV-XXX`（XXX为三位数字，从001递增）
- 示例：`MV-001`, `MV-002`, `MV-003`
- 与短剧 `DM-XXX` 序列独立计数

### 视频编号
- 格式：`{作品编号}-SEG{段号两位}`
- 示例：`MV-001-SEG01`, `MV-001-SEG16`

### 段号编号
- 格式：`SEG{两位数字}`，从 `SEG01` 开始
- 段数根据歌曲时长动态确定

---

## 内容创作规范

### MV剧本要求
1. **音乐同步**：每段的视觉节奏必须与音乐段落（前奏/主歌/副歌/间奏/尾声）匹配
2. **情感曲线**：副歌部分的画面必须配合最强烈的视觉变化，与音乐爆点同步
3. **视觉叙事**：即使是概念型MV也需要有基本的视觉叙事线（情绪弧线）
4. **卡点设计**：鼓点/重拍处应对应画面硬切或关键动作
5. **转场设计**：MV转场比短剧更丰富（匹配剪辑/故障效果/空间碎裂等）
6. **色彩隐喻**：不同情绪段落使用不同色调，形成视觉对比
7. **15秒约束**：每段聚焦一个音乐段落的核心视觉表达

### 分镜要求
1. **时长**：每段固定15秒
2. **格数**：固定9格（3×3布局，16:9比例）
3. 每格约 **1.67秒**
4. 9格之间需要有视觉连续性和音乐节奏逻辑
5. 如有风格切换，在对应格标注 `visual_mode` 和 `transition`
6. 歌词同步：每格标注对应的歌词（`lyrics_at_grid`）

### 故事板配置要求
1. JSON格式，可被程序直接解析
2. 包含 `music_sync` 节（歌曲时间映射）
3. 包含 `storyboard_9grid`（9宫格分镜）
4. 包含AI图像生成的英文Prompt
5. `subtitle` 字段始终为 `false`

---

## 与 generate-media 技能的兼容

`generate-media` 技能已支持 DM 项目，MV 项目需要以下适配（兼容已有逻辑）：

1. **目录结构适配**：
   - DM 项目：`episodes/EPxx/`
   - MV 项目：`segments/SEGxx/`
   - `generate-media` 需同时检查两种目录结构

2. **角色/场景/道具参考图（资产补全感知）**：
   - 已导入的资产（`ref_index.json` 中 `source: "imported"`，`status: "ready"`）→ **跳过生成**
   - 已生成的资产（`source: "generated"`，`status: "ready"`）→ **跳过生成**
   - 标记待生成的资产（`status: "pending"`）→ **执行生成**
   - 无 `ref_index.json` 或条目不存在 → **按 bible 文件中的 AI 绘图关键词正常生成**
   - 生成完成后更新 `ref_index.json`，将 `status` 改为 `"ready"`，`source` 标记为 `"generated"`

3. **分镜图片命名**：
   - DM 项目：`{project_id}-EPxx-{A|B}_storyboard.png`
   - MV 项目：`{project_id}-SEGxx_storyboard.png`（无A/B划分）

4. **配置文件路径**：
   - DM 项目：`episodes/EPxx/storyboard_config.json` → 读取 `part_a` / `part_b`
   - MV 项目：`segments/SEGxx/storyboard_config.json` → 直接读取根级 `storyboard_9grid`

### generate-media 兼容检测逻辑

```python
# detect project type
metadata_path = PROJECT_DIR / "metadata.json"
if metadata_path.exists():
    with open(metadata_path) as f:
        metadata = json.load(f)
    project_type = metadata.get("project_type", "drama")
else:
    project_type = "drama"

if project_type == "mv":
    CONTENT_DIR = PROJECT_DIR / "segments"
    dir_prefix = "SEG"
else:
    CONTENT_DIR = PROJECT_DIR / "episodes"
    dir_prefix = "EP"
```

---

## 与 submit-anime-project 技能的兼容

`submit-anime-project` 读取 `seedance_project_tasks.json`，该文件格式与短剧一致，无需额外适配。唯一区别是：

- MV任务的 `tags` 中包含 `SEGxx` 而非 `EPxx`
- MV任务无 `A`/`B` 标签
- 提交逻辑完全复用

---

## 运行指令

用户可以通过以下方式触发本技能：
- "制作一个MV"
- "生成MV"
- "produce music video"
- "制作音乐视频"
- "用这个剧本做MV" + 指定剧本文件
- "根据这首歌的歌词做MV" + 提供歌词
- "读取xx文件夹的素材做MV"

可附带参数：
- **歌曲名/歌词**：如 "为《凡人歌》制作MV"
- **剧本文件路径**：如 "使用 notes/mv reffiles/MV剧本.md"
- **素材文件夹路径**：如 "读取 /path/to/assets/ 下的角色图"
- **视觉风格**：如 "赛博朋克风格"、"双风格：现实+幻想"
- **MV类型**：如 "叙事型MV"、"概念型MV"

如用户未指定素材来源，则所有素材通过 `generate-media` 自动生成。

---

## 执行检查清单

### 阶段1：MV制作完成后自查
- [ ] `index.json` 全局索引已更新（含MV项目）
- [ ] `metadata.json` 作品元数据已创建（`project_type: "mv"`）
- [ ] `mv_script.md` 完整MV分镜剧本已生成
- [ ] `character_bible.md` 角色设计已完成
- [ ] `scenes/scene_bible.md` 场景设计已完成
- [ ] `props/prop_bible.md` 道具设计已完成（如有）
- [ ] 所有导入素材已正确复制到对应目录
- [ ] 各 `ref_index.json` 已记录导入素材信息
- [ ] **资产完整性检查已执行**（第四步B）
- [ ] 缺失资产已补全或标记为 `pending`（含用户确认）
- [ ] 每个角色在 `ref_index.json` 中 `status` 为 `ready` 或 `pending`
- [ ] 每个场景在 `ref_index.json` 中 `status` 为 `ready` 或 `pending`
- [ ] 每个道具在 `ref_index.json` 中 `status` 为 `ready` 或 `pending`
- [ ] SEG01-SEGxx 所有段目录均已创建
- [ ] 每段包含 `storyboard_config.json`
- [ ] 每段配置包含 `music_sync` 节（歌词/音乐段落同步信息）
- [ ] 所有视频编号遵循 `MV-XXX-SEGxx` 命名规则
- [ ] `video_index.json` 已生成
- [ ] 所有配置标注 `subtitle: false`
- [ ] 段落之间视觉叙事连贯，与音乐节奏同步

### 阶段3：媒体生成后，Seedance任务生成自查
- [ ] **资产补全二次校验**：所有 `ref_index.json` 中 `status: "pending"` 的条目已处理
- [ ] 角色参考图已存在：`characters/{角色名}_ref.png`（导入或生成），或已确认跳过
- [ ] 场景参考图已存在：`scenes/{场景ID}_ref.png`（导入或生成），或已确认跳过
- [ ] 道具参考图已存在：`props/{道具ID}_ref.png`（导入或生成），或已确认跳过
- [ ] 分镜参考图已存在：`segments/SEGxx/{project_id}-SEGxx_storyboard.png`
- [ ] 项目根目录 `seedance_project_tasks.json` 已生成
- [ ] 每条任务的 prompt 使用 `(@文件名)` 格式引用参考图
- [ ] 每条任务的 prompt 包含标准排除指令
- [ ] 每条任务的 prompt 包含歌词同步信息
- [ ] 每条任务的 prompt 包含逐镜头描述（9条）
- [ ] 每条任务的 `referenceFiles` 列出所有引用的图片路径

---

## 输出示例

### 阶段1完成后报告：

```
✅ MV制作完成！

📋 作品信息
- 作品编号：MV-001
- 歌曲：《XWOW-凡人歌》
- MV类型：叙事型+概念型
- 视觉风格：双风格交替
  - 风格A「灰暗现实主义」：冷灰/暗蓝，手持镜头，颗粒感
  - 风格B「东方赛博神话」：鎏金/霓虹蓝，史诗感，失重感
- 总段数：16段（每段15秒）
- 总时长：4分钟

📁 项目目录：/data/dongman/projects/MV-001_frc/

📊 生成内容统计
- MV分镜剧本：1份
- 角色设定：X个角色
- 场景设定：X个场景
- 道具设定：X个道具
- 导入素材：X个（角色X + 场景X + 道具X）
- 故事板配置：16份（每段1份，含9宫格分镜）
- 视频总数：16个
- 总分镜格数：144格（16段 × 9格）

🎬 视频编号范围
MV-001-SEG01 ~ MV-001-SEG16

📂 每段文件
- storyboard_config.json → 故事板配置（含9宫格分镜 + 音乐同步）

⏭️ 下一步
1. 运行 generate-media 技能生成参考图 + 分镜图
2. 运行本技能第七步生成 seedance_project_tasks.json
3. 运行 submit-anime-project 技能提交任务
```
