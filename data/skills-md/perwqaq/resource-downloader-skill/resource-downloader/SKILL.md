---
name: "resource-downloader"
description: "自动从免费资源网站下载图片、音频、视频等资源。触发指令：'帮我下载'。当用户需要下载项目资源或提及需要图片/音频等素材时自动调用。"
---

# 资源下载器 (Resource Downloader)

智能资源下载技能，自动从免费资源网站获取项目所需素材，并按项目规范组织文件。

## 触发条件

当用户消息包含以下关键词时自动触发：
- "帮我下载"
- "下载资源"
- "需要图片"
- "需要音频"
- "找素材"
- "获取资源"

## 工作流程

### 1. 需求分析
首先与用户确认下载需求：
- 资源类型（图片/音频/视频/图标/字体等）
- 资源主题或关键词
- 数量要求
- 质量要求（分辨率、格式等）

### 2. 资源源选择
根据资源类型选择合适的免费资源网站，详见 [resources.md](./resources.md)

### 3. 搜索与筛选
- 使用关键词在资源网站搜索
- 筛选符合项目需求的资源
- 确认资源许可协议（CC0/免费商用）

### 4. 下载与组织
- 下载资源到项目指定目录
- 按照命名规范重命名文件
- 记录资源来源信息

## 支持的资源类型

| 类型 | 推荐格式 | 默认目录 |
|------|----------|----------|
| 图片 | png, jpg, svg, webp | assets/images/ |
| 图标 | svg, png | assets/icons/ |
| 音频 | mp3, wav, ogg | assets/audio/ |
| 视频 | mp4, webm | assets/videos/ |
| 字体 | ttf, woff, woff2 | assets/fonts/ |
| 3D模型 | glb, gltf | assets/models/ |

## 文件命名规范

### 基本规则
```
[类型前缀]-[主题]-[描述]-[序号].[扩展名]

示例：
img-hero-background-01.jpg
icon-menu-hamburger.svg
audio-notification-success.mp3
video-intro-animation.webm
font-heading-bold.woff2
```

### 类型前缀
- `img-` 图片
- `icon-` 图标
- `audio-` 音频
- `video-` 视频
- `font-` 字体
- `model-` 3D模型

### 命名约定
1. 全部小写字母
2. 使用连字符 `-` 分隔单词
3. 避免特殊字符和空格
4. 序号使用两位数字（01, 02, ...）
5. 描述性名称，体现资源用途

## 目录结构

```
project/
├── assets/
│   ├── images/
│   │   ├── backgrounds/
│   │   ├── logos/
│   │   └── content/
│   ├── icons/
│   │   ├── ui/
│   │   └── social/
│   ├── audio/
│   │   ├── effects/
│   │   └── music/
│   ├── videos/
│   └── fonts/
└── resources-manifest.json
```

## 执行步骤

当用户请求下载资源时，按以下步骤执行：

### Step 1: 确认需求
```
询问用户：
1. 需要什么类型的资源？
2. 资源的主题/关键词是什么？
3. 大概需要多少个？
4. 有特殊要求吗（尺寸、风格等）？
```

### Step 2: 搜索资源
访问对应的免费资源网站进行搜索，详见 [resources.md](./resources.md)

### Step 3: 下载资源
使用以下方式下载：
- PowerShell: `Invoke-WebRequest -Uri "URL" -OutFile "路径"`
- curl: `curl -o "路径" "URL"`

### Step 4: 组织文件
1. 创建必要的目录结构
2. 移动文件到对应目录
3. 按规范重命名
4. 更新资源清单

## 资源清单文件

每次下载后更新 `resources-manifest.json`：

```json
{
  "resources": [
    {
      "file": "assets/images/img-hero-sunset-01.jpg",
      "type": "image",
      "source": "https://unsplash.com/photos/xxx",
      "license": "Unsplash License",
      "downloadedAt": "2026-02-12T10:00:00Z",
      "description": "日落背景图"
    }
  ]
}
```

## 注意事项

1. **版权合规**：只下载明确标注可免费商用的资源
2. **许可记录**：记录每个资源的来源和许可信息
3. **文件大小**：注意控制资源文件大小，必要时进行压缩
4. **格式转换**：根据项目需要转换格式（如 PNG 转 WebP）
5. **备份来源**：保留资源原始URL以便追溯

## 示例对话

**用户**: 帮我下载一些科技感的背景图片

**助手**: 
好的，我来帮你下载科技感背景图片。

1. 首先确认需求：
   - 类型：背景图片
   - 主题：科技感
   - 建议数量：5张
   - 建议来源：Unsplash/Pexels

2. 正在搜索并下载...

3. 下载完成，文件已保存：
   - `assets/images/backgrounds/img-bg-tech-circuit-01.jpg`
   - `assets/images/backgrounds/img-bg-tech-network-02.jpg`
   - `assets/images/backgrounds/img-bg-tech-digital-03.jpg`
   - `assets/images/backgrounds/img-bg-tech-futuristic-04.jpg`
   - `assets/images/backgrounds/img-bg-tech-abstract-05.jpg`

4. 资源清单已更新到 `resources-manifest.json`
