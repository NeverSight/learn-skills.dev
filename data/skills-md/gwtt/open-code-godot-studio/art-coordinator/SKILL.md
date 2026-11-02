---
name: art-coordinator
description: 美术与程序协调桥梁。处理资产规格、命名规范、导入管道和美术-程序沟通。
license: MIT
---

# Art Coordinator Skill

协调美术和程序团队，确保资产正确创建、命名、导入和使用。

---

## ⚠️ EXECUTION RULES

1. **ONE PHASE PER TURN** — 一次执行一个阶段
2. **ASK BEFORE ACTING** — 不要自动创建文件
3. **BE PRACTICAL** — 小团队，实用优先
4. **BRIDGE COMMUNICATION** — 帮助美术和程序互相理解

---

## 美术工作流概览

```
美术工作流 (按顺序)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. /art-bible
   └→ 创建视觉规范文档
   └→ 定义色彩、形状语言、资产标准

2. /asset-spec
   └→ 从 GDD 生成资产规格
   └→ 包含 AI 生成提示词

3. /art-coordinator (本技能)
   └→ 创建资产请求
   └→ 协调制作进度
   └→ 验证导入设置

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**前置技能**:
- `/art-bible` — 在有 GDD 后运行，创建视觉规范
- `/asset-spec` — 在美术圣经批准后运行，生成资产规格

---

## Quick Actions

| 用户说 | 执行 |
|--------|------|
| "创建资产请求" | Phase 3: Asset Request |
| "AI 生成资产" | Phase 3B: AI-Driven Generation |
| "检查命名规范" | Phase 4: Naming Convention |
| "导入设置" | Phase 5: Import Settings |
| "同步进度" | Phase 6: Sync Status |
| "查看美术圣经" | Phase 1.5: Check Art Bible |
| "生成资产规格" | → 建议运行 `/asset-spec` |

---

## Phase 1: Team Detection

**ASK**:
```
你的团队结构是什么？

A) 单人（自己做美术）
B) 2人（1程序 + 1美术）
C) 3人（1程序 + 1美术 + 1其他）
D) 其他配置
```

**STOP**: Wait for user response.

---

## Phase 1.5: Check Art Bible

**CHECK**: `design/art/art-bible.md` 是否存在

**IF 存在**:
- 读取美术圣经
- 提取关键规则：视觉身份声明、色彩系统、资产标准
- 告知用户："
```
📐 美术圣经已加载
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
视觉身份: [一行规则]
色彩系统: [主色板摘要]
资产标准: [关键约束]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
资产请求将锚定这些规则。
```
"

**IF 不存在**:
- **ASK**: "未找到美术圣经。是否要运行 `/art-bible` 创建视觉规范？"
- **IF yes**: 引导运行 `/art-bible`
- **IF no**: 继续使用通用规范（警告可能不够具体）

---

## Phase 2: Asset Pipeline Overview

**PRESENT**:
```
Godot 资产管道概览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 创建资产
   └→ 美术: 使用指定规格创建

2. 命名资产
   └→ 程序/美术: 遵循命名规范

3. 导入到 Godot
   └→ 程序: 配置导入设置

4. 使用资产
   └→ 程序: 在代码中引用
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ASK**: "你想做什么？(创建请求/检查规范/配置导入)"

**STOP**: Wait for user's choice.

---

## Phase 3: Asset Request

### 资产类型选择

**ASK**:
```
需要什么类型的资产？

A) Sprite / 角色图
B) UI 元素
C) 背景 / 场景
D) 音效 / 音乐
E) 动画帧
F) 其他
```

**STOP**: Wait for user's choice.

### 生成资产请求

**FOR each asset type, generate specification:**

#### Sprite / 角色图
```markdown
# 资产请求: [名称]

## 基本信息
| 字段 | 值 |
|------|-----|
| **类型** | Sprite |
| **优先级** | P0/P1/P2 |
| **请求人** | [Name] |
| **截止日期** | [Date] |

## 规格说明
- **尺寸**: [W x H] pixels
- **格式**: PNG (透明背景)
- **命名**: `[type]_[name]_[variant].png`
- **数量**: [多少变体]

## 技术要求
- 像素对齐: 是/否
- Pivot点: 中心/底部
- 动画帧数: [N] (如适用)

## 参考素材
- [链接或描述]

## Godot导入设置
- Filter: Nearest (像素风) / Linear (平滑)
- Compression: VRAM Compressed
- Repeat: Disabled
```

#### UI 元素
```markdown
# 资产请求: [名称]

## 基本信息
| 字段 | 值 |
|------|-----|
| **类型** | UI |
| **优先级** | P0/P1/P2 |

## 规格说明
- **尺寸**: [W x H] pixels
- **格式**: PNG
- **命名**: `ui_[element]_[state].png`

## 状态变体
- [ ] Normal
- [ ] Hover
- [ ] Pressed
- [ ] Disabled

## 九宫格切片
- 边距: Left [X] Top [Y] Right [X] Bottom [Y]
```

#### 音效 / 音乐
```markdown
# 资产请求: [名称]

## 基本信息
| 字段 | 值 |
|------|-----|
| **类型** | 音效 / 音乐 |
| **优先级** | P0/P1/P2 |

## 规格说明
- **时长**: [秒数]
- **格式**: WAV (音效) / OGG (音乐)
- **命名**: `sfx_[action]_[variant].wav`

## 技术要求
- 采样率: 44100 Hz
- 声道: Mono (音效) / Stereo (音乐)
- 循环: 是/否 (音乐)

## 参考风格
- [描述期望的感觉]
```

**ASK**: "这个规格正确吗？要保存为请求文档吗？"

**STOP**: Wait for user approval.

---

## Phase 3B: AI-Driven Generation (MCP)

> **触发条件**: MCP 服务已启用 (PixelLab/ElevenLabs)

### MCP 服务状态检查

**CHECK**: `.opencode/mcp.json` 中 MCP 服务状态

```
MCP 服务状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PixelLab (图片): [已启用/未启用]
ElevenLabs (音频): [已启用/未启用]
Godot MCP: [已启用/未启用]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**IF MCP 未启用**:
- **ASK**: "检测到 MCP 服务未启用，是否要配置？"
- **IF yes**: 指导运行 `scripts/setup-mcp.ps1` 或手动配置
- **IF no**: 回退到 Phase 3 人工创建

### AI 资产生成流程

#### 图片生成 (PixelLab MCP)

**可用工具**:
| 工具 | 功能 | 输出目录 |
|------|------|----------|
| `create_character` | 像素角色 | `assets/sprites/generated/` |
| `create_topdown_tileset` | 俯视角瓦片 | `assets/sprites/generated/` |
| `create_sidescroller_tileset` | 横版瓦片 | `assets/sprites/generated/` |
| `create_map_object` | 地图装饰物 | `assets/sprites/generated/` |

**生成流程**:
```
1. 定义资产规格 (尺寸、风格、方向数)
2. 构建生成提示词
3. 调用 PixelLab MCP 工具
4. 验证生成结果
5. 重命名并移动到正确目录
6. 更新 Godot 项目
```

**示例调用**:
```typescript
// 生成像素角色
pixellab_create_character({
  description: "16x16 pixel knight character, top-down view, 4 directions",
  n_directions: 4,
  size: 16
})
// 输出: assets/sprites/generated/char_knight_16x16.png
```

#### 音频生成 (ElevenLabs MCP)

**可用工具**:
| 工具 | 功能 | 输出目录 |
|------|------|----------|
| `text_to_sound_effects` | 音效生成 | `assets/audio/generated/` |
| `compose_music` | 音乐生成 | `assets/audio/generated/` |
| `text_to_speech` | 语音生成 | `assets/audio/generated/` |

**生成流程**:
```
1. 定义音频规格 (时长、风格、情绪)
2. 构建生成提示词
3. 调用 ElevenLabs MCP 工具
4. 验证生成结果
5. 重命名并移动到正确目录
6. 更新 Godot 项目
```

**示例调用**:
```typescript
// 生成跳跃音效
elevenlabs_text_to_sound_effects({
  text: "cartoon jump sound, quick whoosh, playful",
  duration_seconds: 0.5
})
// 输出: assets/audio/generated/sfx_jump_01.wav
```

### 自动化导入 (Godot MCP)

**IF Godot MCP 已启用**:
```
生成完成后的自动化步骤:
1. godot_load_sprite → 自动加载图片到场景
2. 更新 .import 文件
3. 验证资源路径 (res://assets/...)
```

### AI 生成估算时间

| 资产类型 | 简单 | 中等 | 复杂 |
|----------|------|------|------|
| Sprite (角色) | 30秒 | 1分钟 | 3分钟 |
| Sprite (道具) | 15秒 | 30秒 | 1分钟 |
| UI 元素 | 10秒 | 20秒 | 30秒 |
| Tileset | 30秒 | 1分钟 | 3分钟 |
| 音效 | 15秒 | 30秒 | 1分钟 |
| 音乐循环 | 30秒 | 1分钟 | 3分钟 |

> **包含**: 提示词编写 + MCP 调用 + 结果验证 + 重命名导入

### 质量验证清单

生成后必须验证:
- [ ] 尺寸是否符合规格
- [ ] 风格是否一致
- [ ] 命名是否正确
- [ ] 文件格式是否正确
- [ ] Godot 导入是否成功
- [ ] 游戏内显示是否正常

**IF 质量不满意**:
- **ASK**: "生成结果不满意，是否重新生成？"
- **IF yes**: 调整提示词，重新调用 MCP
- **IF no**: 标记为"需人工调整"，记录问题

**STOP**: Wait for user confirmation or regeneration request.

---

## Phase 4: Naming Convention Check

### Godot 资产命名规范

| 资产类型 | 命名格式 | 示例 |
|----------|----------|------|
| Sprite | `[type]_[name]_[variant].png` | `char_player_idle.png` |
| UI | `ui_[element]_[state].png` | `ui_button_hover.png` |
| Background | `bg_[location]_[variant].png` | `bg_forest_night.png` |
| Tile | `tile_[set]_[index].png` | `tile_dungeon_01.png` |
| Audio SFX | `sfx_[action]_[variant].wav` | `sfx_jump_01.wav` |
| Audio Music | `music_[location]_[mood].ogg` | `music_forest_calm.ogg` |
| Animation | `anim_[character]_[action].png` | `anim_player_attack.png` |

### 检查现有资产

**IF user wants to check existing assets**:
- 读取 `assets/` 目录
- 报告不符合规范的文件名
- 建议重命名

**REPORT**:
```markdown
# 命名规范检查报告

## ✅ 符合规范
- [file1]
- [file2]

## ⚠️ 需要重命名
| 当前名称 | 建议名称 |
|----------|----------|
| [old] | [new] |

## 行动项
- [ ] 重命名 [file]
- [ ] 更新代码引用
```

**ASK**: "要帮助重命名吗？"

**STOP**: Wait for user decision.

---

## Phase 5: Import Settings

### Godot 导入设置指南

#### Sprite (2D)

```
纹理导入设置:
├── Texture Type: 2D
├── Filter:
│   ├── Nearest (像素风)
│   └── Linear (平滑风格)
├── Repeat: Disabled
├── Mipmaps: Disabled (2D通常不需要)
└── Compression:
    ├── VRAM Compressed (大图)
    └── VRAM Uncompressed (UI/小图)
```

#### 动画帧

```
Sprite Sheet 设置:
├── 创建 SpriteFrames 资源
├── 设置 Animation 名称
├── 导入帧序列:
│   ├── 手动添加每帧
│   └── 或使用 AnimatedSprite2D 自动加载
└── 设置 FPS
```

#### 音频

```
音频导入设置:
├── 音效 (WAV):
│   ├── Sample Rate: 44100
│   ├── Channels: Mono
│   └── Compression: IMA ADPCM
└── 音乐 (OGG):
    ├── Loop: 是
    ├── Loop Offset: [秒]
    └── BPM: [值] (如适用)
```

**ASK**: "需要具体哪个资产类型的导入配置？"

**STOP**: Wait for user's question.

---

## Phase 6: Sync Status

### 美术-程序同步模板

```markdown
# 同步报告: [Date]

## ✅ 已完成资产
| 资产 | 规格 | 状态 |
|------|------|------|
| [name] | [spec] | 已导入/待调整 |

## 🔄 进行中
| 资产 | 负责人 | 预计完成 |
|------|--------|----------|
| [name] | [artist] | [date] |

## 📋 待请求
- [资产1]
- [资产2]

## ⚠️ 问题
| 问题 | 影响 | 解决方案 |
|------|------|----------|
| [issue] | [impact] | [solution] |

## 下周计划
- [ ] [任务1]
- [ ] [任务2]
```

**ASK**: "要保存这个同步报告吗？"

**STOP**: Wait for user approval.

---

## Godot Asset Organization

### 推荐目录结构

```
assets/
├── sprites/
│   ├── characters/
│   │   ├── player/
│   │   └── enemies/
│   ├── ui/
│   │   ├── buttons/
│   │   └── icons/
│   └── environment/
│       ├── tiles/
│       └── props/
├── audio/
│   ├── sfx/
│   │   ├── player/
│   │   └── ui/
│   └── music/
├── fonts/
└── resources/
    ├── sprites/
    └── audio/
```

---

## Common Issues & Solutions

| 问题 | 原因 | 解决 |
|------|------|------|
| Sprite模糊 | Filter设置错误 | 改为 Nearest |
| 透明背景变黑 | PNG导入设置 | 启用 Detect 3D -> Convert to 2D |
| 动画不播放 | 帧设置错误 | 检查 SpriteFrames 配置 |
| 音频有爆音 | 采样率不匹配 | 统一使用 44100 Hz |
| 资产找不到 | 路径错误 | 使用 `res://` 路径 |

---

## Error Handling

| Error | Fallback |
|-------|----------|
| Artist不熟悉规格 | 提供简化版模板 |
| 导入设置复杂 | 提供预设配置 |
| 命名冲突 | 自动添加后缀建议 |
| 沟通不畅 | 提供检查清单模板 |

---

## Quick Reference

| 场景 | 行动 |
|------|------|
| 新资产请求 | 创建规格文档 → 发给美术 |
| 接收资产 | 检查规格 → 正确命名 → 配置导入 |
| 问题资产 | 记录问题 → 反馈美术 → 等待修改 |
| 周同步 | 生成同步报告 → 分享团队 |

---

## 与其他技能协作

### 工作流整合

| 阶段 | 使用技能 | 输出 |
|------|----------|------|
| 视觉规范制定 | `/art-bible` | `design/art/art-bible.md` |
| 资产规格生成 | `/asset-spec` | `design/assets/specs/*.md` |
| 资产协调制作 | `/art-coordinator` | 资产请求、同步报告 |

### 何时委托到其他技能

**委托到 `/art-bible`** 当：
- 用户想要定义整体视觉风格
- 需要创建色彩系统、形状语言
- 项目刚开始，需要视觉规范

**委托到 `/asset-spec`** 当：
- 用户有具体系统/关卡需要资产
- 需要生成 AI 图像提示词
- 需要创建资产清单

### 资产规格引用

当美术圣经存在时，资产请求应引用具体规则：

```markdown
## 美术圣经锚点
- 视觉身份: [规则]
- 色彩系统: [使用的语义色]
- 形状语言: [应用的形状规则]
```

---

## 相关技能

- **art-bible** — 创建视觉规范文档
- **asset-spec** — 生成详细资产规格
- **design-system** — 创建 GDD（资产规格的输入）
- **godot-specialist** — 技术实现指导