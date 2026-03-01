---
name: super-ppt
description: Python-based PPT editor with style presets, natural language animation support, and style extraction from PPT/PDF. Use when users need to "edit existing PPT", "modify slide", "add animation to PPT", "apply promotion style", "extract style from PPT/PDF", "提取样式", "编辑PPT", "修改第X页", "添加动画", "应用晋升风格", or want to maintain consistent styling across PPT slides. Supports editing specific pages, applying theme presets (promotion/tech), extracting styles from existing documents, and adding animations via natural language descriptions.
---

# Super PPT - Python PPT 编辑器

基于 python-pptx 的 PPT 编辑工具，支持风格预设、样式提取和自然语言动画。

## 核心功能

1. **编辑现有 PPT** - 打开、修改指定页面、保存
2. **风格预设系统** - 如 `promotion`（晋升答辩风格），新增/修改页面自动保持一致
3. **样式提取** - 从 PPT/PDF 提取配色、字体，保存为用户自定义主题
4. **动画支持** - 通过自然语言描述添加动画，支持银河系旋转效果

## 快速开始

### 安装依赖

```bash
pip install python-pptx lxml Pillow
# PDF 支持需要 poppler
brew install poppler  # macOS
```

## 🎨 样式提取（新功能）

从现有 PPT 或 PDF 提取样式风格，保存为可复用的主题。

### 提取样式

```python
import sys
sys.path.insert(0, '<skill_directory>/scripts')
from style_extractor import extract_style, list_styles

# 从 PPT 提取样式
style = extract_style("参考文档.pptx", name="my-company")

# 从 PDF 提取样式
style = extract_style("晋升答辩.pdf", name="promotion-v2")

# 查看已保存的样式
print(list_styles())  # ['my-company', 'promotion-v2']
```

### 命令行提取

```bash
# 从 PPT 提取
python scripts/style_extractor.py reference.pptx --name company-style

# 从 PDF 提取
python scripts/style_extractor.py document.pdf --name doc-style

# 列出所有样式
python scripts/style_extractor.py --list

# 删除样式
python scripts/style_extractor.py --delete old-style
```

### 使用提取的样式

```python
from ppt_editor import open_ppt, create_ppt

# 使用用户自定义主题（从 ~/.ppt-styles/ 加载）
editor = open_ppt("my.pptx", theme="my-company")

# 或创建新 PPT 使用自定义主题
editor = create_ppt(theme="promotion-v2")

# 后续所有元素自动使用该主题的配色
editor.add_title(1, "标题")  # 使用提取的主色
editor.add_card(1, ...)       # 使用提取的卡片背景色
```

### 用户样式目录

```
~/.ppt-styles/
├── my-company.json      # 从 PPT 提取的样式
├── promotion-v2.json    # 从 PDF 提取的样式
└── my-corp.json         # 自定义企业样式
```

### 样式配置格式

```json
{
  "name": "my-company",
  "description": "从 参考文档.pptx 提取的样式",
  "colors": {
    "primary": "fc5a1f",      // 主色（标题、强调）
    "secondary": "3669cd",    // 次色（链接、图标）
    "text_dark": "434343",    // 深色文字
    "text_normal": "707070",  // 正文文字
    "text_light": "a4a4a3",   // 辅助文字
    "background": "ffffff",   // 背景色
    "card_bg": "f8f8f8",      // 卡片背景
    "accent_light": "fca787", // 浅色强调
    "success": "51cf66"       // 成功色
  },
  "fonts": {
    "title": "Microsoft YaHei",
    "body": "Microsoft YaHei",
    "title_size": 28,
    "body_size": 14
  },
  "style_prompt": "## 视觉风格指南\n..."  // AI 风格提示词
}
```

### 🤖 风格 Prompt（AI 辅助设计）

提取样式时会自动生成一段描述性的 **风格 Prompt**，用于指导 AI 理解和应用该视觉风格：

```python
# 获取当前主题的风格 prompt
editor = create_ppt(theme="my-company")
prompt = editor.get_style_prompt()

# 打印风格 prompt
editor.print_style_prompt()

# 输出示例：
# ## 视觉风格指南
# ### 整体风格
# 这是一个暖色调、积极活力的演示文稿风格...
# ### 配色方案
# - **主色调**: #fc5a1f（橙色）- 用于标题、强调...
# ### 设计原则
# 1. 简洁留白...
```

**用途**：
- 在使用 AI 辅助创建 PPT 时，将此 prompt 作为上下文
- 确保 AI 生成的内容与视觉风格保持一致
- 作为设计规范文档供团队参考

### 添加银河系旋转动画（一键命令）

```bash
# 为 PPT 第一页的所有圆形添加银河系旋转效果
python scripts/animation_engine.py galaxy your_slide.pptx 1 output.pptx
```

### 在 Python 中使用

```python
import sys
sys.path.insert(0, '<skill_directory>/scripts')
from animation_engine import AnimationEngine, add_galaxy_rotation
from pptx import Presentation

# 方式 1: 一键添加银河系效果
add_galaxy_rotation("cover.pptx", slide_number=1, output_path="cover_animated.pptx")

# 方式 2: 精细控制每个形状的动画
prs = Presentation("cover.pptx")
engine = AnimationEngine(prs)

# 为特定形状添加旋转动画
engine.add_spin(slide_number=1, shape_index=5, duration=10.0, repeat="indefinite", clockwise=True)
engine.add_spin(slide_number=1, shape_index=6, duration=6.0, repeat="indefinite", clockwise=False)

# 保存
prs.save("output.pptx")
```

### 打开并编辑现有 PPT

```python
import sys
sys.path.insert(0, '<skill_directory>/scripts')
from ppt_editor import open_ppt, create_ppt

# 打开现有 PPT（自动应用 promotion 风格）
editor = open_ppt("path/to/your.pptx", theme="promotion")

# 查看所有页面
editor.print_slides()

# 获取指定页面
slide = editor.get_slide(3)  # 第 3 页

# 清空并重建某一页
editor.clear_slide(3)
editor.set_background(3)
editor.add_header_bar(3, "新标题")
editor.add_text(3, "这是正文内容", x=0.5, y=1.5)

# 保存
editor.save("output.pptx")
```

### 添加动画

```python
from animation_engine import AnimationEngine, animate

# 方式 1: 自然语言描述
engine = AnimationEngine(editor)
engine.add_from_description("标题从左侧飞入", slide_number=1)
engine.add_from_description("内容依次淡入", slide_number=1)

# 方式 2: 直接 API
engine.add_entrance("fade", slide_number=1, shape_index=0, duration=0.5)
engine.add_slide_transition(1, "push")
```

## 可用主题

### 内置主题

| 主题 | 说明 | 主色 |
|------|------|------|
| `promotion` | 晋升答辩风格 | 橙色 #fc5a1f |
| `tech` | 技术分享风格 | 紫色 #4a00e0 |

### 用户自定义主题

通过 `style_extractor.py` 提取的主题保存在 `~/.ppt-styles/` 目录，可直接通过名称使用：

```python
# 使用用户主题
editor = open_ppt("my.pptx", theme="my-corp")  # 从 ~/.ppt-styles/my-corp.json 加载
```

## 核心 API

### SuperPPTEditor

```python
editor = open_ppt(path, theme="promotion")  # 打开 PPT
editor = create_ppt(theme="promotion")       # 创建新 PPT

# 页面操作
editor.get_slide(n)      # 获取第 n 页
editor.add_slide()       # 添加新页
editor.clear_slide(n)    # 清空第 n 页
editor.print_slides()    # 打印所有页面概览

# 添加元素（自动应用主题样式）
editor.add_header_bar(n, "标题")
editor.add_title(n, "标题", "副标题")
editor.add_text(n, "内容", x, y, width, height)
editor.add_card(n, x, y, w, h, title, content, card_type)
editor.add_feature_grid(n, features, columns=3)

# 保存
editor.save("output.pptx")
```

### AnimationEngine

```python
engine = AnimationEngine(editor)

# 进入动画
engine.add_entrance("fade", slide_number, shape_index, duration)
# 类型: fade, fly_in, fly_in_left, zoom, bounce, float_up, wipe, split

# 强调动画
engine.add_emphasis("pulse", slide_number, shape_index)
# 类型: pulse, flash, spin, grow

# 旋转动画（银河系效果专用）
engine.add_spin(slide_number, shape_index, duration=10.0, repeat="indefinite", clockwise=True)
# repeat: "1", "2", "indefinite"

# 银河系效果（自动为所有圆形添加旋转）
engine.add_galaxy_effect(slide_number)

# 退出动画
engine.add_exit("fade_out", slide_number, shape_index)
# 类型: fade_out, fly_out, zoom_out

# 页面切换
engine.add_slide_transition(slide_number, "push")
# 类型: fade, push, wipe, split, cube, flip, gallery

# 自然语言
engine.add_from_description("标题淡入", slide_number)
engine.add_from_description("圆形一直旋转", slide_number)
```

## 卡片类型

`add_card()` 支持以下类型：

| 类型 | 效果 | 使用场景 |
|------|------|----------|
| `normal` | 灰色背景 | 普通内容 |
| `highlight` | 橙色强调 | 重要内容 |
| `problem` | 红色标记 | 问题/痛点 |
| `solution` | 绿色标记 | 解决方案 |

## 示例：完整工作流

```python
# 1. 打开现有晋升 PPT
editor = open_ppt("晋升答辩.pptx", theme="promotion")
editor.print_slides()

# 2. 修改第 5 页 - 技术架构
editor.clear_slide(5)
editor.set_background(5)
editor.add_header_bar(5, "技术架构演进")

# 添加对比卡片
editor.add_card(5, x=0.5, y=1.2, width=4.5, height=2,
                title="🚫 旧架构", content="描述旧架构的问题...",
                card_type="problem")

editor.add_card(5, x=5.3, y=1.2, width=4.5, height=2,
                title="✅ 新架构", content="描述新架构的优势...",
                card_type="solution")

# 3. 添加动画
from animation_engine import AnimationEngine
engine = AnimationEngine(editor)
engine.add_from_description("卡片依次从底部弹出", slide_number=5)
engine.add_slide_transition(5, "push")

# 4. 保存
editor.save("晋升答辩-修改版.pptx")
```

## 参考文档

- **配色方案**: `references/color-palette.md`
- **动画命令**: `references/animation-commands.md`

## 常见任务

### 修改指定页面保持风格一致

```python
editor = open_ppt("existing.pptx", theme="promotion")
# 主题已加载，后续所有 add_* 方法自动使用 promotion 配色
editor.add_title(3, "新标题")  # 自动使用橙色 #fc5a1f
editor.add_text(3, "内容")     # 自动使用灰色 #707070
```

### 批量添加动画

```python
engine = AnimationEngine(editor)
for i in range(1, editor.get_slide_count() + 1):
    engine.add_slide_transition(i, "fade")
    engine.add_from_description("所有元素依次淡入", slide_number=i)
```

### 创建新页面

```python
n = editor.add_slide()
editor.add_header_bar(n, "新增内容")
editor.add_feature_grid(n, [
    {"icon": "🎯", "text": "目标明确"},
    {"icon": "📈", "text": "数据驱动"},
    {"icon": "🔧", "text": "工具支持"},
])
```
