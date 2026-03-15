---
name: multimodal-gen
description: 多模态内容生成（图片、视频）。当用户需要生成图片、生成图像、生成视频、AI绘画、AI作图、画一张图、做个视频、文生图、文生视频时使用此技能。自动调用 multimodal-agent 进行生成。
allowed-tools: sessions_spawn, Bash, Read, Write, Edit
---

# 多模态内容生成

当用户需要生成图片或视频时，自动调用 `multimodal-agent` 进行处理。

## 触发场景

### 图片生成
- "生成一张图片"
- "画一张..."
- "AI 作图"
- "文生图"
- "帮我生成图像"
- "用 flux/imagen/dalle 生成"

### 视频生成
- "生成一个视频"
- "做个视频"
- "文生视频"
- "用 veo/sora/kling 生成视频"

## 使用方式

### 自动调用 multimodal-agent

```python
sessions_spawn(
    agentId="multimodal-agent",
    task="生成图片: {用户描述}, 使用 {模型} 模型"
)
```

### 可用模型

#### 图片生成
| 别名 | 模型 | 特点 |
|------|------|------|
| `flux` | flux-pro-max | 高质量，推荐 |
| `imagen` | google/imagen-4-ultra | Google 最强 |
| `dalle` | gpt-image-1 | DALL-E 3 |
| `doubao` | doubao-seedream-4-5 | 中式美学 |
| `klingimg` | kling-image | 可灵生图 |

#### 视频生成
| 别名 | 模型 | 特点 |
|------|------|------|
| `veopro` | veo3.1-pro | Google 专业版 |
| `veo4k` | veo3.1-pro-4k | 4K 高清 |
| `sora` | sora-2-pro-all | OpenAI Sora |
| `kling` | kling-video | 可灵视频 |

## 执行流程

```
用户请求 "生成一张猫咪图片"
    │
    ▼
┌─────────────────────────────────────┐
│ 1. 识别为图片生成请求              │
│ 2. 提取描述: "猫咪"                │
│ 3. 选择默认模型: flux-pro-max      │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ sessions_spawn(                     │
│   agentId="multimodal-agent",       │
│   task="生成图片: 一只可爱的猫咪,   │
│         使用 flux 模型"             │
│ )                                   │
└─────────────────────────────────────┘
    │
    ▼
multimodal-agent 执行生成并返回结果
```

## 示例

### 生成图片
```
用户: 帮我生成一张日落海滩的图片

执行:
sessions_spawn(
    agentId="multimodal-agent",
    task="生成图片: 日落时分的海滩，金色阳光洒在海面上，使用 flux 模型"
)
```

### 生成视频
```
用户: 用 sora 生成一个猫咪玩耍的视频

执行:
sessions_spawn(
    agentId="multimodal-agent",
    task="生成视频: 一只可爱的猫咪在草地上玩耍，使用 sora 模型"
)
```

### 指定模型
```
用户: 用 doubao 画一张中国风山水画

执行:
sessions_spawn(
    agentId="multimodal-agent",
    task="生成图片: 中国风山水画，云雾缭绕的山峰，使用 doubao 模型"
)
```

## 模型选择建议

| 场景 | 推荐模型 |
|------|----------|
| 通用高质量 | `flux` |
| 中式风格 | `doubao` |
| 写实照片 | `imagen` |
| 创意艺术 | `dalle` |
| 高清视频 | `veo4k` |
| 电影级视频 | `sora` |
| 快速视频 | `kling` |

## 注意事项

1. **提示词优化**: multimodal-agent 会自动优化用户的描述
2. **模型选择**: 如果用户没指定，默认使用 flux (图片) 或 veopro (视频)
3. **异步执行**: 视频生成可能需要较长时间，会在后台执行
4. **结果返回**: 生成完成后会自动发送结果给用户
