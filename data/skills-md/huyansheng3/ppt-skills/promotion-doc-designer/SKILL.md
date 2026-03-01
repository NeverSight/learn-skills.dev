---
name: promotion-doc-designer
description: Professional promotion/review document designer following corporate presentation standards. Creates clean, minimal PPT/PDF documents with 16:9 layout, strategic color usage (primary brand orange #fc5a1f, secondary blue #3669cd), and sophisticated white-space design. Use when users ask to "create promotion doc", "design review presentation", "make professional PPT", "晋升文档设计", "述职报告", or need corporate-standard presentations with visual hierarchy and data visualization.
---

# Promotion Document Designer

为晋升述职、团队汇报等企业级场景设计专业的演示文档。遵循企业设计规范，打造简洁、清晰、有说服力的视觉呈现。

## 设计原则

### 1. 布局标准（16:9 演示文稿）

- **页面比例**: 16:9 标准演示比例（4000 x 2250 像素 或 等比例）
- **页面边距**: 左右两侧保持充足留白（约页面宽度的 5%）
- **顶部标题栏**: 每页顶部设置标题区域（约页面高度的 6-8%，保持简洁）
- **内容区域**: 中部 80-85% 用于主要内容展示

### 2. 色彩系统

#### 主色调
- **品牌橙色**: `#fc5a1f` - 用于关键标题、重点强调、CTA 元素
- **深橙色**: `#fc4807` - 用于深色变体、hover 状态
- **浅橙色**: `#fca787`, `#fcb59a` - 用于背景、渐变、装饰

#### 辅助色
- **企业蓝色**: `#3669cd`, `#2960ca` - 用于数据可视化、图表
- **中性灰色**: `#707070`, `#585858` - 用于正文、说明文字
- **深色文字**: `#434343`, `#414141` - 用于标题、重要文字

#### 背景色
- **纯白**: `#ffffff` - 主要背景色（占比 60-70%）
- **浅灰**: `#f8f8f8`, `#f0f0f0` - 卡片背景、分区背景
- **极浅灰**: `#fbfbfb`, `#fcfcfc` - 微妙分隔、视觉层次

### 3. 视觉层次

#### 信息架构
1. **一级标题**: 品牌橙色 `#fc5a1f`，大字号，简短有力
2. **二级标题**: 深色灰 `#434343`，中等字号，说明性文字
3. **正文内容**: 中性灰 `#707070`，标准字号，清晰易读
4. **辅助说明**: 浅灰色，小字号，补充信息

#### 留白策略
- **呼吸空间**: 元素之间保持充足间距（至少页面的 3-5%）
- **视觉焦点**: 通过留白引导视线，突出核心内容
- **分组关系**: 相关元素靠近，不相关元素分离

### 4. 内容组织

#### 页面类型模板

**封面页**
```
┌─────────────────────────────────────┐
│  [顶部装饰 - 浅橙色渐变]              │
├─────────────────────────────────────┤
│                                     │
│      主标题 (#fc5a1f, 大字号)        │
│      副标题/作者信息 (#707070)       │
│                                     │
│      [可选: 装饰图形/图标]           │
│                                     │
└─────────────────────────────────────┘
```

**目录页/导航页**
```
┌─────────────────────────────────────┐
│  标题 (#fc5a1f)                     │
├─────────────────────────────────────┤
│  1  [模块名称]    2  [模块名称]      │
│     描述文字          描述文字       │
│                                     │
│  3  [模块名称]    4  [模块名称]      │
│     描述文字          描述文字       │
└─────────────────────────────────────┘
```

**内容页（单列）**
```
┌─────────────────────────────────────┐
│  页面标题 (#fc5a1f)                 │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │  内容区域 (白色/浅灰背景)      │  │
│  │  - 文字内容                   │  │
│  │  - 图表                       │  │
│  │  - 数据可视化                 │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**内容页（多列）**
```
┌─────────────────────────────────────┐
│  页面标题 (#fc5a1f)                 │
├─────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐       │
│  │  左侧内容 │  │  右侧内容 │       │
│  │  (卡片1)  │  │  (卡片2)  │       │
│  └───────────┘  └───────────┘       │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  底部总结/关键点             │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

**数据页**
```
┌─────────────────────────────────────┐
│  页面标题 (#fc5a1f)                 │
├─────────────────────────────────────┤
│  指标卡片组:                         │
│  ┌──────┐ ┌──────┐ ┌──────┐         │
│  │ 114万 │ │ 25%  │ │ 400倍│         │
│  │ 代码量 │ │ 精简 │ │ 体积 │         │
│  └──────┘ └──────┘ └──────┘         │
│                                     │
│  [图表/可视化区域]                   │
└─────────────────────────────────────┘
```

## 实现指南

### 使用 reportlab 创建 PDF

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# 16:9 页面尺寸 (以点为单位, 1点=1/72英寸)
SLIDE_WIDTH = 10 * inch  # 约 25.4 cm
SLIDE_HEIGHT = 5.625 * inch  # 约 14.3 cm

# 颜色定义
BRAND_ORANGE = HexColor('#fc5a1f')
DARK_ORANGE = HexColor('#fc4807')
LIGHT_ORANGE = HexColor('#fca787')
BLUE = HexColor('#3669cd')
DARK_GRAY = HexColor('#434343')
MEDIUM_GRAY = HexColor('#707070')
LIGHT_GRAY = HexColor('#f8f8f8')

def create_slide(c, title, content_func):
    """创建标准页面模板"""
    # 背景
    c.setFillColor(HexColor('#ffffff'))
    c.rect(0, 0, SLIDE_WIDTH, SLIDE_HEIGHT, fill=1)
    
    # 顶部标题栏
    c.setFillColor(BRAND_ORANGE)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(0.5 * inch, SLIDE_HEIGHT - 0.6 * inch, title)
    
    # 内容区域
    content_func(c)
    
    # 翻页
    c.showPage()

# 示例: 创建文档
c = canvas.Canvas("promotion_doc.pdf", pagesize=(SLIDE_WIDTH, SLIDE_HEIGHT))

def cover_page(c):
    c.setFillColor(BRAND_ORANGE)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(SLIDE_WIDTH/2, SLIDE_HEIGHT*0.6, "秋季述职报告")
    c.setFillColor(MEDIUM_GRAY)
    c.setFont("Helvetica", 16)
    c.drawCentredString(SLIDE_WIDTH/2, SLIDE_HEIGHT*0.45, "张三 / 技术部")

create_slide(c, "", cover_page)
c.save()
```

### 使用 Mermaid 生成图表

对于架构图、流程图等，可以使用 Mermaid 语法生成 SVG，然后嵌入到 PDF 中：

```markdown
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fc5a1f','primaryTextColor':'#fff','primaryBorderColor':'#fc4807','lineColor':'#3669cd','secondaryColor':'#f8f8f8','tertiaryColor':'#fca787'}}}%%
graph LR
    A[需求分析] --> B[技术设计]
    B --> C[开发实现]
    C --> D[测试验证]
    D --> E[上线部署]
```

### 使用 Python-PPTX 创建 PPT

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# 16:9 演示文稿
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)

# 颜色定义
BRAND_ORANGE = RGBColor(252, 90, 31)
DARK_GRAY = RGBColor(67, 67, 67)
LIGHT_GRAY = RGBColor(248, 248, 248)

# 添加封面
slide_layout = prs.slide_layouts[6]  # 空白布局
slide = prs.slides.add_slide(slide_layout)

# 标题
title_box = slide.shapes.add_textbox(
    Inches(1), Inches(2), 
    Inches(8), Inches(1)
)
title_frame = title_box.text_frame
title_frame.text = "秋季述职报告"
title_para = title_frame.paragraphs[0]
title_para.font.size = Pt(36)
title_para.font.color.rgb = BRAND_ORANGE
title_para.alignment = PP_ALIGN.CENTER

prs.save('promotion_deck.pptx')
```

## 内容策略

### 标题设计
- **简洁有力**: 5-8 个字，直击要点
- **层次清晰**: 使用编号、图标区分层级
- **视觉引导**: 颜色和大小差异突出重点

### 数据呈现
- **关键指标**: 大字号展示核心数字（如 "114万行代码"）
- **对比展示**: 使用前后对比、环比增长突出成果
- **可视化**: 柱状图、折线图、饼图等图表形式
- **单位说明**: 清晰标注单位和计算方式

### 文字规范
- **字体层级**: 标题/正文/注释三级字号体系
- **行距控制**: 1.5 倍行距，保持呼吸感
- **对齐方式**: 左对齐为主，标题可居中
- **避免拥挤**: 每页不超过 3-4 个主要信息点

### 图标与装饰
- **功能图标**: 使用简洁的线性图标表示功能模块
- **装饰元素**: 细微渐变、圆角矩形、虚线分隔
- **品牌一致**: 所有装饰元素使用品牌色系

## 常见场景模板

### 个人简介页
```python
def create_profile_page(c):
    # 左侧: 时间轴
    x_timeline = 1 * inch
    y_start = SLIDE_HEIGHT - 1.5 * inch
    
    events = [
        ("2020.3", "某互联网公司", "前端专家"),
        ("2015-2020", "某SaaS公司", "前端团队负责人"),
        ("2013-2015", "某创业公司", "合伙人 | CTO"),
    ]
    
    for i, (time, company, role) in enumerate(events):
        y = y_start - i * 0.8 * inch
        c.setFillColor(BRAND_ORANGE)
        c.circle(x_timeline, y, 5, fill=1)
        c.setFillColor(DARK_GRAY)
        c.setFont("Helvetica", 10)
        c.drawString(x_timeline + 0.2 * inch, y, f"{time} {company}")
        c.setFillColor(MEDIUM_GRAY)
        c.setFont("Helvetica", 9)
        c.drawString(x_timeline + 0.2 * inch, y - 0.15 * inch, role)
```

### 工作成果页
```python
def create_achievement_page(c):
    # 指标卡片
    metrics = [
        ("114万行", "工程代码", (1*inch, SLIDE_HEIGHT-2*inch)),
        ("86.3万行", "精简 25%", (3*inch, SLIDE_HEIGHT-2*inch)),
        ("400倍", "体积压缩", (5*inch, SLIDE_HEIGHT-2*inch)),
    ]
    
    for value, desc, (x, y) in metrics:
        # 卡片背景
        c.setFillColor(LIGHT_GRAY)
        c.roundRect(x, y, 1.5*inch, 1*inch, 10, fill=1)
        
        # 数值
        c.setFillColor(BRAND_ORANGE)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(x + 0.75*inch, y + 0.6*inch, value)
        
        # 描述
        c.setFillColor(MEDIUM_GRAY)
        c.setFont("Helvetica", 10)
        c.drawCentredString(x + 0.75*inch, y + 0.3*inch, desc)
```

### 架构图页
```python
def create_architecture_page(c):
    # 使用矩形和箭头展示系统架构
    # 保持简洁，避免过度复杂
    
    # 示例: 三层架构
    layers = [
        ("业务层", SLIDE_HEIGHT - 2*inch),
        ("应用层", SLIDE_HEIGHT - 3*inch),
        ("数据层", SLIDE_HEIGHT - 4*inch),
    ]
    
    for name, y in layers:
        c.setFillColor(LIGHT_GRAY)
        c.rect(2*inch, y, 6*inch, 0.6*inch, fill=1)
        c.setFillColor(DARK_GRAY)
        c.setFont("Helvetica", 12)
        c.drawCentredString(5*inch, y + 0.25*inch, name)
```

## 最佳实践

1. **保持一致性**: 所有页面使用相同的颜色、字体、间距体系
2. **突出重点**: 每页只有 1-2 个核心观点
3. **数据说话**: 用具体数字和可视化支撑结论
4. **视觉引导**: 通过颜色、大小、位置引导阅读顺序
5. **留白呼吸**: 不要填满所有空间，让内容有呼吸感
6. **移动友好**: 确保在投影仪和小屏幕上都清晰可读

## 质量检查清单

- [ ] 所有页面使用 16:9 比例
- [ ] 品牌色 `#fc5a1f` 用于关键元素
- [ ] 背景色以白色 `#ffffff` 为主（占比 60%+）
- [ ] 每页留白充足（边距 ≥ 5%）
- [ ] 字体层级清晰（大中小三级）
- [ ] 数据可视化简洁明了
- [ ] 所有文字清晰可读
- [ ] 无拼写错误和排版错误
- [ ] 逻辑顺序合理
- [ ] 总页数控制在 30-50 页

## 导出与分享

### PDF 导出设置
- 分辨率: 300 DPI 或更高
- 颜色模式: RGB（屏幕显示）或 CMYK（印刷）
- 字体嵌入: 全部嵌入，确保跨平台一致性

### PPT 导出设置
- 格式: .pptx (兼容性最佳)
- 嵌入字体: 是
- 压缩图片: 否（保持高质量）
- 备注: 添加演讲者备注，方便汇报

## 参考资源

分析的原始文档包含以下特点：
- 46 页晋升述职报告
- 标准 16:9 演示比例（4000 x 2250 像素）
- 极简白色背景（60-70% 纯白）
- 品牌橙色 `#fc5a1f` 作为主色调
- 企业蓝色 `#3669cd` 作为辅助色
- 充足的留白和视觉呼吸感
- 清晰的信息层级和数据可视化
