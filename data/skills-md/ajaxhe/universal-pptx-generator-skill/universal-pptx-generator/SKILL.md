---
name: universal-pptx-generator
description: 通用 PPT 生成技能。能够根据用户指定的任意 PPT 模板，结合提供的图文素材（文档、图片等），自动生成一份风格统一的演示文稿。支持自动分析模板结构、提取背景图/背景色、解析配色方案和字体规范，然后根据素材内容生成完整 PPT。支持多种图表类型（柱状图、折线图、饼图、雷达图等）的数据可视化展示。关键词：PPT生成、模板分析、演示文稿、幻灯片、图文排版、自动化、图表、数据可视化。
---

# 通用 PPT 生成技能

## 概述

此技能可以根据**任意用户指定的 PPT 模板**，结合提供的**图文素材**（文档、图片等），自动生成一份风格统一的演示文稿。

**⭐⭐⭐ 核心理念：每个模板都是独特的，必须针对性分析！**

不同 PPT 模板使用的字体、对齐方式、字号、颜色、位置、**背景样式**都完全不同。**绝不能**将一个模板的配置直接应用到另一个模板！每次使用新模板时，都必须重新分析 XML 提取精确参数。

**核心能力:**
1. **模板分析** - 自动解析 PPTX 模板结构、配色、字体、**背景图/背景色**、对齐方式
2. **⭐⭐⭐ 分页面类型分析** - 针对封面、目录、章节、内容、结束页分别提取背景和样式
3. **素材处理** - 从 DOCX/PDF/图片等素材中提取内容
4. **智能排版** - 根据模板风格自动排版生成内容
5. **批量生成** - 支持生成多页完整演示文稿
6. **⭐ 图表展示** - 支持柱状图、折线图、饼图、雷达图等多种数据可视化图表

**关键词**: PPT生成、模板分析、演示文稿、幻灯片、图文排版、自动化、pptxgenjs、图表、数据可视化

---

## ⭐⭐⭐ 页面类型与背景处理 (关键！)

### 五种核心页面类型

不同类型的页面可能使用不同的背景处理方式：

| 页面类型 | 典型特征 | 背景处理方式 |
|---------|---------|-------------|
| **封面页 (Cover)** | 主标题 + 副标题 + Logo | 背景图/渐变/斜切形状 |
| **目录页 (TOC)** | 目录列表 + 装饰元素 | 纯色背景 + 装饰形状 |
| **章节页 (Chapter)** | 大号章节编号 + 章节标题 | 纯色背景 + 装饰形状 |
| **内容页 (Content)** | 标题 + 正文/图片/图表 | 纯色背景/背景图 |
| **结束页 (Thanks)** | 感谢语 + 联系方式 | 纯色背景 + 装饰形状 |

### ⭐⭐⭐ 背景类型分析

PPT 背景有三种主要类型：

#### 1. 纯色背景 (SolidFill)

```xml
<!-- XML 特征 -->
<p:bg>
  <p:bgPr>
    <a:solidFill>
      <a:schemeClr val="tx2"/>  <!-- 使用主题色 -->
    </a:solidFill>
  </p:bgPr>
</p:bg>

<!-- 或直接指定颜色 -->
<a:solidFill>
  <a:srgbClr val="0D1E43"/>  <!-- 直接 RGB 值 -->
</a:solidFill>
```

**pptxgenjs 对应代码：**
```javascript
slide.background = { color: '0D1E43' };  // 深蓝色
```

#### 2. 背景图片 (BlipFill)

```xml
<!-- XML 特征 -->
<p:bg>
  <p:bgPr>
    <a:blipFill>
      <a:blip r:embed="rId2"/>  <!-- 引用图片资源 -->
    </a:blipFill>
  </p:bgPr>
</p:bg>

<!-- 或在形状中作为图片填充 -->
<p:pic>
  <p:blipFill>
    <a:blip r:embed="rId2"/>
  </p:blipFill>
</p:pic>
```

**pptxgenjs 对应代码：**
```javascript
slide.background = { path: 'workspace/backgrounds/cover-bg.png' };
```

#### 3. 渐变背景 (GradFill)

```xml
<!-- XML 特征 -->
<a:gradFill>
  <a:gsLst>
    <a:gs pos="0">
      <a:srgbClr val="0052D9"><a:alpha val="50000"/></a:srgbClr>
    </a:gs>
    <a:gs pos="100000">
      <a:srgbClr val="0D1E43"/>
    </a:gs>
  </a:gsLst>
  <a:lin ang="5400000"/>  <!-- 角度：5400000/60000 = 90° -->
</a:gradFill>
```

**pptxgenjs 对应代码：**
```javascript
slide.background = {
  color: '0D1E43',  // 基础色
  // 注：pptxgenjs 对渐变背景支持有限，通常用形状模拟
};

// 用形状模拟渐变
slide.addShape('rect', {
  x: 0, y: 0, w: '100%', h: '100%',
  fill: {
    type: 'gradient',
    gradientType: 'linear',
    degrees: 90,
    stops: [
      { position: 0, color: '0052D9', alpha: 50 },
      { position: 100, color: '0D1E43' }
    ]
  }
});
```

### 主题色映射

很多模板使用主题色（schemeClr）而非直接颜色值：

| schemeClr 值 | 含义 | 典型颜色 |
|-------------|------|---------|
| `dk1` | 深色1 (主要文字) | 000000 |
| `lt1` / `bg1` | 浅色1 (背景) | FFFFFF |
| `dk2` / `tx2` | 深色2 (次要背景) | 0060FF / 0D1E43 |
| `lt2` | 浅色2 | E7E6E6 |
| `accent1` | 强调色1 | 0060F0 |
| `accent2` | 强调色2 | A736FF |

**从 theme1.xml 提取主题色映射：**
```bash
cat workspace/template-analysis/ppt/theme/theme1.xml | grep -E "dk1|lt1|dk2|lt2|accent" | head -20
```

### ⭐⭐⭐ 分页面类型完整分析流程

```python
# 完整的页面背景分析脚本
import re
import os

def analyze_slide_background(slide_path, rels_path):
    """分析单页幻灯片的背景类型"""
    
    with open(slide_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        'background_type': None,
        'background_color': None,
        'background_image': None,
        'decorative_shapes': [],
        'scheme_color': None
    }
    
    # 1. 检查是否有 <p:bg> 背景定义
    bg_match = re.search(r'<p:bg>(.*?)</p:bg>', content, re.DOTALL)
    if bg_match:
        bg_content = bg_match.group(1)
        
        # 纯色背景
        if '<a:solidFill>' in bg_content:
            result['background_type'] = 'solid'
            # 直接颜色
            color = re.search(r'srgbClr val="([^"]+)"', bg_content)
            if color:
                result['background_color'] = color.group(1)
            # 主题色
            scheme = re.search(r'schemeClr val="([^"]+)"', bg_content)
            if scheme:
                result['scheme_color'] = scheme.group(1)
        
        # 渐变背景
        elif '<a:gradFill>' in bg_content:
            result['background_type'] = 'gradient'
        
        # 图片背景
        elif '<a:blipFill>' in bg_content:
            result['background_type'] = 'image'
            embed = re.search(r'r:embed="([^"]+)"', bg_content)
            if embed:
                result['background_image'] = embed.group(1)
    
    # 2. 检查是否有全屏图片作为背景（无 <p:bg> 时）
    if not result['background_type']:
        pics = re.findall(r'<p:pic>(.*?)</p:pic>', content, re.DOTALL)
        for pic in pics:
            # 检查是否是大尺寸图片（可能是背景图）
            ext_match = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"/>', pic)
            if ext_match:
                cx, cy = int(ext_match.group(1)), int(ext_match.group(2))
                # 如果尺寸接近全屏（>80%），视为背景图
                if cx > 10000000 and cy > 5000000:  # EMU 单位
                    result['background_type'] = 'image_shape'
                    embed = re.search(r'r:embed="([^"]+)"', pic)
                    if embed:
                        result['background_image'] = embed.group(1)
                    break
    
    # 3. 如果还是没有找到背景，检查是否使用装饰形状构成背景
    if not result['background_type']:
        result['background_type'] = 'shapes_composite'
    
    # 4. 分析装饰性形状（半透明方块等）
    shapes = re.findall(r'<p:sp>(.*?)</p:sp>', content, re.DOTALL)
    for shape in shapes:
        # 检查是否有透明度设置
        alpha = re.search(r'<a:alpha val="(\d+)"', shape)
        if alpha:
            transparency = 100 - int(alpha.group(1)) / 1000
            color = re.search(r'srgbClr val="([^"]+)"', shape)
            if color and transparency > 0:
                result['decorative_shapes'].append({
                    'color': color.group(1),
                    'transparency': transparency
                })
    
    # 5. 从 rels 文件获取实际图片路径
    if result['background_image'] and os.path.exists(rels_path):
        with open(rels_path, 'r', encoding='utf-8') as f:
            rels_content = f.read()
        img_id = result['background_image']
        img_path = re.search(rf'{img_id}"[^>]*Target="([^"]+)"', rels_content)
        if img_path:
            result['background_image_path'] = img_path.group(1)
    
    return result

# 分析所有关键页面
def analyze_all_pages(template_dir):
    slides_dir = f'{template_dir}/ppt/slides'
    rels_dir = f'{slides_dir}/_rels'
    
    page_types = {
        1: '封面页',
        2: '目录页',
        3: '章节页',
        4: '内容页'
    }
    
    results = {}
    for slide_num, page_type in page_types.items():
        slide_path = f'{slides_dir}/slide{slide_num}.xml'
        rels_path = f'{rels_dir}/slide{slide_num}.xml.rels'
        
        if os.path.exists(slide_path):
            result = analyze_slide_background(slide_path, rels_path)
            result['page_type'] = page_type
            results[f'slide{slide_num}'] = result
            
            print(f"\n=== {page_type} (slide{slide_num}) ===")
            print(f"背景类型: {result['background_type']}")
            if result['background_color']:
                print(f"背景颜色: #{result['background_color']}")
            if result['scheme_color']:
                print(f"主题色引用: {result['scheme_color']}")
            if result['background_image_path']:
                print(f"背景图片: {result['background_image_path']}")
            if result['decorative_shapes']:
                print(f"装饰形状: {len(result['decorative_shapes'])}个")
                for s in result['decorative_shapes'][:3]:
                    print(f"  - 颜色: #{s['color']}, 透明度: {s['transparency']}%")
    
    return results

# 执行分析
# results = analyze_all_pages('workspace/template-analysis')
```

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                     通用 PPT 生成流程                        │
├─────────────────────────────────────────────────────────────┤
│  1. 模板深度分析阶段 (关键!)                                 │
│     └── 解压 PPTX → 精确分析每页 XML → 提取字号/颜色/位置    │
│                                                              │
│  2. 素材处理阶段                                             │
│     └── 解析 DOCX/PDF → 提取文本/图片 → 结构化内容           │
│                                                              │
│  3. 内容规划阶段                                             │
│     └── 分析内容 → 设计结构 → 分配页面                       │
│     └── ⭐ 识别数据 → 选择图表类型 → 准备图表数据            │
│                                                              │
│  4. PPT 生成阶段                                             │
│     └── 应用精确的模板参数 → 填充内容 → 生成图表 → 输出 PPTX │
│                                                              │
│  5. 清理阶段                                                 │
│     └── 删除临时文件 → 保留最终 PPTX                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 第一阶段：模板深度分析 (最关键!)

### ⚠️ 核心原则

**必须精确提取模板中每一页的实际参数，而非使用推测值！**

分析时需要从 slide XML 中提取：
1. **精确字号** - `sz="8000"` 表示 80pt (sz ÷ 100)
2. **精确位置** - `<a:off x="..." y="..."/>` EMU单位，转换为英寸或百分比
3. **精确颜色** - `srgbClr val="FFFFFF"` 直接使用
4. **字体粗细** - `b="1"` 表示粗体
5. **⭐ 对齐方式** - `algn="ctr"` 居中, `algn="r"` 右对齐, `algn="l"` 或无属性表示左对齐

### 1.1 解压 PPTX 模板

PPTX 文件本质是 ZIP 压缩包，包含 XML 和媒体资源：

```bash
# 创建工作目录
mkdir -p workspace/template-analysis workspace/backgrounds workspace/images

# 解压模板 (使用 Python 处理特殊字符文件名)
python3 -c "
import zipfile
import glob
files = glob.glob('模板*.pptx')
if files:
    with zipfile.ZipFile(files[0], 'r') as zip_ref:
        zip_ref.extractall('workspace/template-analysis')
    print('Done:', files[0])
"
```

### 1.2 PPTX 文件结构详解

```
template-analysis/
├── [Content_Types].xml      # 内容类型定义
├── _rels/
├── docProps/
│   ├── app.xml              # 应用属性
│   └── core.xml             # 核心属性（作者、创建时间等）
└── ppt/
    ├── presentation.xml     # 演示文稿主配置（尺寸、幻灯片列表）
    ├── presProps.xml        # 演示属性
    ├── tableStyles.xml      # 表格样式
    ├── viewProps.xml        # 视图属性
    ├── _rels/
    │   └── presentation.xml.rels  # ⭐ 幻灯片关系映射
    ├── media/               # ⭐ 媒体资源（背景图、图片）
    │   ├── image1.png
    │   ├── image2.png
    │   └── ...
    ├── slideLayouts/        # ⭐ 幻灯片布局定义
    │   ├── slideLayout1.xml   # 封面布局
    │   ├── slideLayout2.xml   # 内容布局
    │   └── ...
    ├── slideMasters/        # ⭐ 母版定义（全局样式）
    │   └── slideMaster1.xml
    ├── slides/              # ⭐⭐⭐ 幻灯片内容 (最重要!)
    │   ├── slide1.xml
    │   ├── slide2.xml
    │   └── ...
    └── theme/               # ⭐ 主题配色/字体
        └── theme1.xml
```

### 1.3 精确分析每页幻灯片 (核心步骤!)

**⚠️ 关键：必须分析每一页的实际 XML，提取精确参数！**

**⚠️⚠️⚠️ 特别重要：必须提取每个元素的字体名称！**

**⚠️⚠️⚠️ 新增：必须分析形状边框和背景渐变！**

使用 Python 脚本精确提取参数（**包含字体、边框、渐变信息**）：

```python
# 分析幻灯片的精确参数（含字体、边框、渐变）
import re
import sys

def analyze_slide(slide_path):
    with open(slide_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取文本内容
    texts = re.findall(r'<a:t>([^<]+)</a:t>', content)
    print('=== 文本内容 ===')
    for t in texts:
        if t.strip():
            print(repr(t))
    
    # ⭐⭐⭐ 提取字体名称 - 极其重要！
    latin_fonts = re.findall(r'latin typeface="([^"]+)"', content)
    ea_fonts = re.findall(r'ea typeface="([^"]+)"', content)
    print('\n=== 字体 (Latin/西文) ===')
    for f in set(latin_fonts):
        print(f'  {f}')
    print('\n=== 字体 (EA/东亚) ===')
    for f in set(ea_fonts):
        print(f'  {f}')
    
    # 提取字号 (sz 值 ÷ 100 = pt)
    sizes = re.findall(r'sz="(\d+)"', content)
    print('\n=== 字号 (百分之一点) ===')
    for s in set(sizes):
        print(f'{s} -> {int(s)/100}pt')
    
    # 提取颜色
    colors = re.findall(r'srgbClr val="([^"]+)"', content)
    print('\n=== sRGB颜色 ===')
    for c in set(colors):
        print(f'#{c}')
    
    # 提取位置 (EMU 单位，1英寸=914400 EMU)
    positions = re.findall(r'<a:off x="(\d+)" y="(\d+)"/>', content)
    print('\n=== 位置信息 (转换为20x11.25英寸画布的百分比) ===')
    for i, (x, y) in enumerate(positions):
        x_inch = int(x) / 914400
        y_inch = int(y) / 914400
        x_pct = x_inch / 20 * 100
        y_pct = y_inch / 11.25 * 100
        print(f'{i}: x={x_pct:.1f}%, y={y_pct:.1f}% (x={x_inch:.2f}in, y={y_inch:.2f}in)')
    
    # 提取尺寸
    extents = re.findall(r'<a:ext cx="(\d+)" cy="(\d+)"/>', content)
    print('\n=== 尺寸信息 ===')
    for i, (cx, cy) in enumerate(extents):
        w_inch = int(cx) / 914400
        h_inch = int(cy) / 914400
        w_pct = w_inch / 20 * 100
        h_pct = h_inch / 11.25 * 100
        print(f'{i}: w={w_pct:.1f}%, h={h_pct:.1f}% (w={w_inch:.2f}in, h={h_inch:.2f}in)')
    
    # ⭐⭐⭐ 新增：分析边框设置
    print('\n=== 边框分析 ===')
    lns = re.findall(r'<a:ln[^>]*>(.*?)</a:ln>', content, re.DOTALL)
    for i, ln in enumerate(lns):
        if '<a:noFill/>' in ln:
            print(f'边框{i}: 无边框 (noFill)')
        elif '<a:solidFill>' in ln:
            color = re.search(r'val="([^"]+)"', ln)
            print(f'边框{i}: 有边框，颜色={color.group(1) if color else "未知"}')
        else:
            print(f'边框{i}: ⚠️ 默认黑色边框！需要在生成时设置 line: "none"')
    
    # ⭐⭐⭐ 新增：分析渐变填充
    print('\n=== 渐变分析 ===')
    gradFills = re.findall(r'<a:gradFill[^>]*>(.*?)</a:gradFill>', content, re.DOTALL)
    for i, grad in enumerate(gradFills):
        # 提取角度
        lin = re.search(r'<a:lin ang="(\d+)"', grad)
        if lin:
            angle = int(lin.group(1)) / 60000
            print(f'渐变{i}: 线性渐变，角度={angle}°')
        
        # 提取颜色停止点
        stops = re.findall(r'<a:gs pos="(\d+)">(.*?)</a:gs>', grad, re.DOTALL)
        for pos, gs_content in stops:
            position = int(pos) / 1000
            color = re.search(r'srgbClr val="([^"]+)"', gs_content)
            alpha = re.search(r'<a:alpha val="(\d+)"', gs_content)
            transparency = 100 - int(alpha.group(1))/1000 if alpha else 0
            print(f'  停止点 {position}%: 颜色={color.group(1) if color else "主题色"}, 透明度={transparency}%')
    
    # ⭐⭐⭐ 新增：分析透明度
    print('\n=== 透明度分析 ===')
    alphas = re.findall(r'<a:alpha val="(\d+)"/>', content)
    for a in set(alphas):
        opacity = int(a) / 1000
        transparency = 100 - opacity
        print(f'alpha={a} -> 不透明度={opacity}% -> pptxgenjs transparency={transparency}')
    
    # ⭐⭐⭐ 详细分析每个元素的字体+字号+对齐+文本
    print('\n=== 详细元素分析 (字体+字号+对齐+文本) ===')
    sps = re.findall(r'<p:sp>(.*?)</p:sp>', content, re.DOTALL)
    for i, sp in enumerate(sps):
        texts = re.findall(r'<a:t>([^<]+)</a:t>', sp)
        sizes = re.findall(r'sz="(\d+)"', sp)
        latin = re.findall(r'latin typeface="([^"]+)"', sp)
        ea = re.findall(r'ea typeface="([^"]+)"', sp)
        bold = 'b="1"' in sp
        # ⭐ 提取对齐方式
        algn = re.findall(r'algn="([^"]+)"', sp)
        align_map = {'l': '左对齐', 'ctr': '居中', 'r': '右对齐', 'just': '两端对齐'}
        align_str = align_map.get(algn[0], algn[0]) if algn else '左对齐(默认)'
        # ⭐ 检查是否有边框
        has_border = '<a:ln' in sp and '<a:noFill/>' not in sp
        if texts:
            print(f'元素{i}: 文本="{texts[0][:20]}" 字号={[int(s)/100 for s in sizes[:2]]}pt 字体={latin[:1] or ea[:1]} 粗体={bold} 对齐={align_str} 有边框={has_border}')

# 分析每一页
for i in range(1, 11):
    print(f'\n{"="*60}')
    print(f'SLIDE {i}')
    print("="*60)
    try:
        analyze_slide(f'workspace/template-analysis/ppt/slides/slide{i}.xml')
    except FileNotFoundError:
        print(f'slide{i}.xml not found')
        break
```

### 1.4 分析主题配色

**从 theme1.xml 提取配色方案:**

```bash
cat workspace/template-analysis/ppt/theme/theme1.xml | python3 -c "
import sys
import re
content = sys.stdin.read()

# 提取所有颜色
colors = re.findall(r'srgbClr val=\"([^\"]+)\"', content)
print('主题颜色:')
for c in set(colors):
    print(f'  #{c}')

# 提取字体
fonts = re.findall(r'typeface=\"([^\"]+)\"', content)
print('\n主题字体:')
for f in set(fonts):
    if f:
        print(f'  {f}')
"
```

**关键 XML 结构 - 颜色方案:**
```xml
<a:clrScheme name="主题名称">
  <a:dk1><a:sysClr val="windowText"/></a:dk1>  <!-- 深色1 - 主要文字 -->
  <a:lt1><a:sysClr val="window"/></a:lt1>       <!-- 浅色1 - 背景 -->
  <a:dk2><a:srgbClr val="050E24"/></a:dk2>      <!-- 深色2 -->
  <a:lt2><a:srgbClr val="E7E6E6"/></a:lt2>      <!-- 浅色2 -->
  <a:accent1><a:srgbClr val="79E8F5"/></a:accent1>  <!-- 强调色1 - 青色 -->
  <!-- ... -->
</a:clrScheme>
```

### 1.5 识别幻灯片类型与背景图映射

**查看布局关系:**
```bash
for i in 1 2 3 4 5 6 7 8 9 10; do
  echo "=== Slide $i ===" 
  cat workspace/template-analysis/ppt/slides/_rels/slide$i.xml.rels 2>/dev/null | grep -E "(slideLayout|image)"
done
```

**查看布局对应的背景图:**
```bash
for i in 1 2 3 5 6 12; do
  echo "=== slideLayout$i ===" 
  cat workspace/template-analysis/ppt/slideLayouts/_rels/slideLayout$i.xml.rels 2>/dev/null | grep image
done
```

**建立映射表 (示例):**

| 页面类型 | slide | slideLayout | 背景图 |
|----------|-------|-------------|--------|
| 封面页 | slide1 | slideLayout1 | image1.png |
| 目录页 | slide2 | slideLayout5 | image6.png |
| 章节页 | slide3 | slideLayout6 | image7.png |
| 内容页 | slide4 | slideLayout2 | image4.png |
| 感谢页 | slide10 | slideLayout12 | image13.jpeg |

### 1.6 提取背景图

```bash
# 根据分析结果复制背景图
cp workspace/template-analysis/ppt/media/image1.png workspace/backgrounds/cover-bg.png
cp workspace/template-analysis/ppt/media/image6.png workspace/backgrounds/toc-bg.png
cp workspace/template-analysis/ppt/media/image7.png workspace/backgrounds/chapter-bg.png
cp workspace/template-analysis/ppt/media/image4.png workspace/backgrounds/content-bg.png
cp workspace/template-analysis/ppt/media/image13.jpeg workspace/backgrounds/thanks-bg.jpeg
```

---

## 第二阶段：素材处理

### 2.1 处理 DOCX 文档

```bash
# 使用 Python 解压 (处理特殊字符文件名)
python3 -c "
import zipfile
import glob
files = glob.glob('*.docx')
if files:
    with zipfile.ZipFile(files[0], 'r') as zip_ref:
        zip_ref.extractall('workspace/docx-extract')
    print('Done:', files[0])
"

# 提取图片
mkdir -p workspace/images
cp workspace/docx-extract/word/media/*.png workspace/images/ 2>/dev/null
cp workspace/docx-extract/word/media/*.jpeg workspace/images/ 2>/dev/null
```

### 2.2 提取文本内容

```python
import re
with open('workspace/docx-extract/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()
texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', content)
for t in texts:
    if t.strip():
        print(t.strip())
```

### 2.3 内容结构化

```javascript
const contentStructure = {
  title: "主标题",
  subtitle: "副标题",
  author: "作者",
  chapters: [
    {
      number: "01",
      title: "章节标题",
      subtitle: "章节副标题",
      pages: [
        {
          type: "content",  // content | textOnly | dataCards | chart
          subtitle: "页面小标题",
          title: "页面大标题",
          sections: [
            { title: "要点小标题1", desc: ["描述行1", "描述行2"] },
            { title: "要点小标题2", desc: "单行描述" }
          ],
          image: "images/image1.png"
        },
        // ⭐ 图表页示例
        {
          type: "chart",
          title: "数据分析图表",
          chartType: "bar",  // bar | line | pie | doughnut | area | radar
          chartData: {
            labels: ["Q1", "Q2", "Q3", "Q4"],
            datasets: [
              { name: "2024年", values: [100, 150, 200, 180] },
              { name: "2025年", values: [120, 180, 220, 250] }
            ]
          },
          chartOptions: {
            showLegend: true,
            showValue: true,
            showTitle: true
          }
        }
      ]
    }
  ]
};
```

---

## 第三阶段：PPT 生成

### 3.1 pptxgenjs 配置模板

**⚠️⚠️⚠️ 关键原则：所有配置必须从当前模板动态提取，绝不能写死！**

**不同的 PPT 模板会使用不同的字体、对齐方式、字号、颜色等，必须针对每个模板单独分析！**

```javascript
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

// ============================================================
// ⚠️⚠️⚠️ 重要：以下所有配置都是占位符/示例！
// 实际使用时必须通过分析当前模板的 slide XML 获得精确值！
// 不同模板的字体、对齐、字号都不同，绝不能直接复制使用！
// ============================================================

const TEMPLATE_CONFIG = {
  // ⭐⭐⭐ 字体配置 - 必须从当前模板的 slide XML 精确提取！
  // 每个模板使用的字体都不同！必须从 <a:ea typeface="..."/> 提取！
  // 示例：腾讯模板用 "腾讯体 W7"，微软模板可能用 "微软雅黑"，其他模板可能用 "思源黑体" 等
  fonts: {
    // ⚠️ 以下是示例值，必须替换为当前模板实际使用的字体！
    title: '从slide1.xml提取的标题字体',    // 从 <a:ea typeface="..."/> 获取
    titleLatin: '从slide1.xml提取的西文字体', // 从 <a:latin typeface="..."/> 获取
    body: '从slide4.xml提取的正文字体',      // 从内容页提取
    bodyLatin: '从slide4.xml提取的西文字体',
    fallback: 'Microsoft YaHei'              // 备选字体
  },
  
  // 配色配置 (从 slide XML 和 theme1.xml 提取)
  colors: {
    primary: 'FFFFFF',      // 主要文字色
    secondary: 'E7E6E6',    // 次要文字色
    accent: '79E8F5',       // 强调色 (章节编号等)
    dark: '050E24',         // 深色/背景色
    // ⭐⭐⭐ 主题色映射 - 从 theme1.xml 的 <a:clrScheme> 提取
    // 用于将 schemeClr 转换为实际颜色
    schemeColors: {
      dk1: '000000',        // 深色1
      lt1: 'FFFFFF',        // 浅色1 (bg1)
      dk2: '0060FF',        // 深色2 (tx2) - 常用于背景
      lt2: 'FFFFFF',        // 浅色2
      accent1: '0060F0',    // 强调色1
      accent2: 'A736FF',    // 强调色2
      tx2: '0060FF'         // 文本2 - 注意这是常见的背景色引用！
    }
  },
  
  // ⭐⭐⭐ 背景配置 - 分页面类型配置！
  // 不同页面可能使用不同的背景类型（纯色/图片/渐变）
  backgrounds: {
    // 封面页背景 - 通常使用图片或复杂形状组合
    cover: {
      type: 'image',  // 'solid' | 'image' | 'gradient' | 'shapes'
      image: 'workspace/backgrounds/cover-bg.png',  // 如果是图片背景
      color: null,    // 如果是纯色背景
      // 装饰形状（如斜切遮罩）
      overlayShapes: [
        {
          type: 'custom',  // 自定义形状
          color: '0052D9',
          transparency: 50,
          // 形状路径点（从 <a:path> 提取）
        }
      ]
    },
    
    // 目录页背景 - 通常使用纯色 + 装饰形状
    toc: {
      type: 'solid',
      color: '0060FF',  // 从 schemeClr val="tx2" 映射得到
      // 或从 <p:bg><a:solidFill><a:schemeClr val="tx2"/> 提取后映射
      decorativeShapes: [
        { x: 1.22, y: 2.31, w: 1.31, h: 1.31, color: 'FFFFFF', transparency: 90 },
        { x: -0.01, y: 2.66, w: 2.17, h: 2.17, color: 'FFFFFF', transparency: 10 },
        { x: 1.95, y: 4.59, w: 0.58, h: 0.58, color: 'FFFFFF', transparency: 50 }
      ]
    },
    
    // 章节页背景 - 与目录页类似
    chapter: {
      type: 'solid',
      color: '0060FF',
      decorativeShapes: [
        // 同目录页的装饰形状
      ]
    },
    
    // 内容页背景 - 可能是纯色或图片
    content: {
      type: 'solid',
      color: '0060FF',
      // 如果有背景图，设置 type: 'image' 并指定路径
      image: null
    },
    
    // 结束页/感谢页背景
    thanks: {
      type: 'solid',
      color: '0060FF',
      decorativeShapes: [
        // 与目录页类似的装饰形状
      ]
    }
  },
  
  // ⚠️ 字号配置 - 必须从当前模板的 slide XML 精确提取!
  // 不同模板字号差异很大！必须从 sz="..." 属性获取！
  // sz="8000" -> 80pt, sz="4800" -> 48pt
  fontSizes: {
    // ⚠️ 以下是示例结构，必须替换为当前模板实际的字号！
    
    // 封面页 (从 slide1.xml 的 sz 属性提取)
    coverTitle: '从sz属性计算',      // sz值 ÷ 100
    coverSubtitle: '从sz属性计算',
    coverAuthor: '从sz属性计算',
    
    // 目录页 (从 slide2.xml 提取)
    // ⭐⭐⭐ 关键：必须区分"目录"标题和目录项的字号！
    tocHeading: '从sz属性计算',  // "目录"二字的字号（通常较大）
    tocItem: '从sz属性计算',     // 目录项的字号（通常较小，需精确提取！）
    
    // 章节页 (从 slide3.xml 提取)
    chapterNumber: '从sz属性计算',
    chapterTitle: '从sz属性计算',
    chapterSubtitle: '从sz属性计算',
    
    // 内容页 (从 slide4.xml 提取)
    pageSubtitle: '从sz属性计算',
    pageTitle: '从sz属性计算',
    sectionTitle: '从sz属性计算',
    bodyText: '从sz属性计算',
    
    // 感谢页
    thanks: '从sz属性计算'
  },
  
  // ⭐⭐⭐ 对齐方式配置 - 必须从当前模板的 slide XML 的 algn 属性提取!
  // 不同模板的对齐方式完全不同！有的居中，有的左对齐，有的右对齐！
  // 'left' | 'center' | 'right' | 'justify'
  alignments: {
    // ⚠️ 以下是示例结构，必须替换为当前模板实际的对齐方式！
    // 通过分析每页 XML 中的 algn="ctr"|"r"|"l" 属性获取
    
    // 封面页 (从 slide1.xml 的 algn 属性提取)
    coverTitle: '从slide1.xml提取',       // 分析 algn 属性
    coverSubtitle: '从slide1.xml提取',
    coverAuthor: '从slide1.xml提取',
    
    // 目录页 (从 slide2.xml 提取)
    tocHeading: '从slide2.xml提取',
    tocItem: '从slide2.xml提取',
    
    // 章节页 (从 slide3.xml 提取) - 不同模板差异很大！
    chapterNumber: '从slide3.xml提取',
    chapterTitle: '从slide3.xml提取',     // 可能是 center/left/right
    chapterSubtitle: '从slide3.xml提取',  // 可能是 center/left/right
    
    // 内容页 (从 slide4.xml 提取)
    pageSubtitle: '从slide4.xml提取',
    pageTitle: '从slide4.xml提取',
    sectionTitle: '从slide4.xml提取',
    bodyText: '从slide4.xml提取'
  },
  
  // ⚠️ 位置配置 - 必须从 slide XML 精确提取!
  // 使用百分比或英寸
  positions: {
    // 封面页位置 (从 slide1.xml 的 <a:off> 提取)
    cover: {
      title: { x: '26.5%', y: '31%', w: '70%', h: '15%' },
      subtitle: { x: '38.6%', y: '42%', w: '54%', h: '9%' },
      author: { x: '68.4%', y: '60%', w: '22%', h: '5%' },
      authorName: { x: '68.4%', y: '66%', w: '22%', h: '5%' }
    },
    
    // 目录页位置 (从 slide2.xml 提取)
    toc: {
      // 4列布局，起始位置和间距
      startX: 0.92,       // 第一列 x=4.6% -> 0.92 英寸
      colSpacing: 4.95,   // 列间距 (约24.7%)
      numberY: '57.2%',   // 编号 Y 位置
      titleY: '69.9%'     // 标题 Y 位置
    },
    
    // 章节页位置 (从 slide3.xml 提取)
    chapter: {
      number: { x: '43.2%', y: '14.3%', w: '30%', h: '30%' },
      title: { x: '15.2%', y: '35.7%', w: '70%', h: '15%' },
      subtitle: { x: '15.2%', y: '51.5%', w: '70%', h: '8%' }
    },
    
    // 内容页位置 (从 slide4.xml 提取)
    content: {
      subtitle: { x: '3.2%', y: '6.3%', w: '45%', h: '6%' },
      title: { x: '3.6%', y: '21.4%', w: '45%', h: '10%' },
      body: { x: '3.8%', y: '31.3%', w: '45%', h: '60%' },
      image: { x: '51.7%', y: '31.3%', w: '45%', h: '55%' }
    }
  }
};

// 设置 16:9 宽屏尺寸
pptx.defineLayout({ name: 'LAYOUT_WIDE', width: 20, height: 11.25 });
pptx.layout = 'LAYOUT_WIDE';
```

### 3.2 封面页生成函数

**⚠️ 注意：位置、字号、字体必须与模板完全匹配！**

**⚠️⚠️⚠️ 关键问题解决方案：**

#### 问题1：标题文字换行问题
pptxgenjs 默认会根据文本框宽度自动换行。解决方案：
1. **使用 `fit: 'shrink'`** - 自动缩小字号以适应宽度（推荐）
2. **使用足够大的宽度** - 确保文本框宽度足够容纳所有文字
3. **根据文字长度动态计算宽度** - 中文约每字符 0.7-1.0 × 字号(pt) / 72 英寸

```javascript
// ⭐ 计算文本所需宽度的辅助函数
function calculateTextWidth(text, fontSize, isChinese = true) {
  // 中文字符宽度约等于字号，英文约0.5倍
  const avgCharWidth = isChinese ? fontSize / 72 : fontSize / 72 * 0.5;
  let width = 0;
  for (const char of text) {
    width += /[\u4e00-\u9fa5]/.test(char) ? fontSize / 72 : fontSize / 72 * 0.5;
  }
  return width * 1.1; // 留10%余量
}
```

#### 问题2：封面页图片斜切布局（通用方案）

某些模板使用斜切（平行四边形）布局，需要分析模板的精确结构。

**⭐⭐⭐ 分析封面页布局的通用步骤：**

```
1. 解压模板，读取封面页 slide XML (通常是 slide1.xml)
2. 分析 <p:sp> 形状元素，识别：
   - 图片位置和尺寸 (<a:off>, <a:ext>)
   - 形状类型（矩形、自定义路径等）
   - 填充颜色和透明度 (<a:srgbClr>, <a:alpha>)
3. 确定层次结构（从下到上的渲染顺序）
4. 在 pptxgenjs 中按相同顺序重建
```

**⭐⭐⭐ 通用背景处理函数：**

根据模板分析结果，不同页面可能使用不同的背景类型。以下是通用的背景处理方案：

```javascript
// ⭐⭐⭐ 通用背景设置函数
function applySlideBackground(slide, pptx, bgConfig, colors) {
  /**
   * bgConfig 结构:
   * {
   *   type: 'solid' | 'image' | 'gradient' | 'shapes',
   *   color: '0060FF',           // 纯色背景颜色
   *   image: 'path/to/image',    // 图片路径
   *   decorativeShapes: [...],   // 装饰形状数组
   *   overlayShapes: [...]       // 遮罩层数组
   * }
   */
  
  // 1. 基础背景
  switch (bgConfig.type) {
    case 'image':
      if (bgConfig.image) {
        slide.background = { path: bgConfig.image };
      }
      break;
    
    case 'solid':
      slide.background = { color: bgConfig.color || colors.dark };
      break;
    
    case 'gradient':
      // pptxgenjs 背景不直接支持渐变，使用纯色基础 + 渐变形状
      slide.background = { color: bgConfig.baseColor || colors.dark };
      if (bgConfig.gradientStops) {
        slide.addShape(pptx.ShapeType.rect, {
          x: 0, y: 0, w: '100%', h: '100%',
          fill: {
            type: 'gradient',
            gradientType: 'linear',
            degrees: bgConfig.gradientAngle || 90,
            stops: bgConfig.gradientStops
          },
          line: { type: 'none' }
        });
      }
      break;
    
    case 'shapes':
    default:
      // 使用纯色基础
      slide.background = { color: bgConfig.color || colors.dark };
      break;
  }
  
  // 2. 添加遮罩层（如封面的半透明渐变层）
  if (bgConfig.overlayShapes && bgConfig.overlayShapes.length > 0) {
    bgConfig.overlayShapes.forEach(overlay => {
      slide.addShape(pptx.ShapeType.rect, {
        x: overlay.x, y: overlay.y,
        w: overlay.w, h: overlay.h,
        fill: { 
          type: 'solid',
          color: overlay.color,
          transparency: overlay.transparency || 0
        },
        line: { type: 'none' }
      });
    });
  }
  
  // 3. 添加装饰形状（如半透明方块）
  if (bgConfig.decorativeShapes && bgConfig.decorativeShapes.length > 0) {
    bgConfig.decorativeShapes.forEach(shape => {
      slide.addShape(pptx.ShapeType.rect, {
        x: shape.x, y: shape.y,
        w: shape.w, h: shape.h,
        fill: {
          type: 'solid',
          color: shape.color || colors.primary,
          transparency: shape.transparency || 0
        },
        line: { type: 'none' }
      });
    });
  }
}

// ⭐⭐⭐ 从主题色引用获取实际颜色
function resolveSchemeColor(schemeColorName, colors) {
  /**
   * 将 schemeClr 值转换为实际 RGB 颜色
   * 例如: 'tx2' -> '0060FF', 'bg1' -> 'FFFFFF'
   */
  const mapping = colors.schemeColors || {
    dk1: '000000',
    lt1: 'FFFFFF',
    dk2: '0060FF',
    lt2: 'FFFFFF',
    tx2: '0060FF',
    bg1: 'FFFFFF',
    accent1: '0060F0'
  };
  return mapping[schemeColorName] || schemeColorName;
}
```

**⭐ 通用渐变/斜切效果实现方案：**

由于 pptxgenjs 不直接支持自定义路径斜切，可使用以下方案模拟：

```javascript
function createCoverSlide(pptx, config, content) {
  const slide = pptx.addSlide();
  
  // ⭐⭐⭐ 使用通用背景处理函数
  applySlideBackground(slide, pptx, config.backgrounds.cover, config.colors);
  
  // 3. 文字元素使用足够宽度避免换行
  const pos = config.positions.cover;
  const titleWidth = calculateTextWidth(content.title, config.fontSizes.coverTitle);
  
  // 主标题 - 使用动态计算的宽度
  slide.addText(content.title, {
    x: pos.title.x, 
    y: pos.title.y, 
    w: Math.max(titleWidth, 8),  // ⭐ 确保宽度足够
    h: pos.title.h,
    fontSize: config.fontSizes.coverTitle,
    fontFace: config.fonts.title,
    color: config.colors.primary,
    bold: true,
    align: config.alignments.coverTitle || 'left',
    fit: 'shrink'  // ⭐ 如果仍然超出，自动缩小
  });
  
  // 副标题 - 48pt，前面有蓝色圆点装饰
  if (content.subtitle) {
    // 蓝色圆点装饰 (可选)
    slide.addShape('ellipse', {
      x: parseFloat(pos.subtitle.x) - 1.5 + '%',
      y: parseFloat(pos.subtitle.y) + 1.5 + '%',
      w: 0.25, h: 0.25,
      fill: { color: config.colors.accent }  // 79E8F5
    });
    
    slide.addText(content.subtitle, {
      x: pos.subtitle.x, y: pos.subtitle.y, w: pos.subtitle.w, h: pos.subtitle.h,
      fontSize: config.fontSizes.coverSubtitle,  // 48pt
      fontFace: config.fonts.title,
      color: config.colors.primary,
      bold: true,
      align: 'right'
    });
  }
  
  // 主讲人标签
  slide.addText('主讲人', {
    x: pos.author.x, y: pos.author.y, w: pos.author.w, h: pos.author.h,
    fontSize: config.fontSizes.coverAuthor,  // 28pt
    fontFace: config.fonts.body,
    color: config.colors.primary,
    align: 'right'
  });
  
  // 主讲人姓名
  slide.addText(content.author || '', {
    x: pos.authorName.x, y: pos.authorName.y, w: pos.authorName.w, h: pos.authorName.h,
    fontSize: config.fontSizes.coverAuthor,  // 28pt
    fontFace: config.fonts.body,
    color: config.colors.primary,
    align: 'right'
  });
  
  return slide;
}
```

### 3.3 目录页生成函数

**⚠️⚠️⚠️ 目录页字号必须从模板精确提取！不同模板差异很大！**

**⭐ 通用目录页分析步骤：**

```
1. 找到模板的目录页 slide XML（通常是 slide2.xml）
2. 分析所有文本元素的 sz 属性，区分：
   - "目录"标题字号（如果有）
   - 目录项字号（⭐⭐⭐ 关键！不同模板差异很大！）
3. 提取颜色、透明度（alpha）、位置等信息
4. 注意装饰元素（方块、线条等）
```

**⭐⭐⭐ 关键提醒：目录项字号通常比预期小很多！**

常见错误：假设目录项字号是 60pt 或 32pt，但实际可能只有 20-30pt。
必须从模板 XML 的 `sz` 属性精确提取！

```javascript
function createTOCSlide(pptx, config, chapters, currentIndex = 0) {
  const slide = pptx.addSlide();
  
  // ⭐⭐⭐ 使用通用背景处理函数
  applySlideBackground(slide, pptx, config.backgrounds.toc, config.colors);
  
  const pos = config.positions.toc;
  
  // ⭐ "目录"标题（如果模板有）- 从模板精确提取字号！
  if (config.showTocHeading !== false) {
    slide.addText('目录', {
      x: pos.heading?.x || 0.5,
      y: pos.heading?.y || 3,
      w: pos.heading?.w || 2,
      h: pos.heading?.h || 1,
      fontSize: config.fontSizes.tocHeading,  // ⭐ 从模板提取！
      fontFace: config.fonts.title,
      color: config.colors.tocHeading || config.colors.dark,
      bold: false
    });
  }
  
  // ⭐⭐⭐ 目录项列表 - 字号必须从模板精确提取！
  const tocItems = chapters.map((chapter, i) => ({
    text: `${i + 1}. ${chapter.title}`,
    options: {
      fontSize: config.fontSizes.tocItem,  // ⭐⭐⭐ 关键！从模板 sz 属性提取！
      fontFace: config.fonts.title,
      color: config.colors.tocItem || 'FFFFFF',
      // 非当前项使用透明度（如果模板有此效果）
      transparency: config.tocItemTransparency && i !== currentIndex 
        ? config.tocItemTransparency : 0,
      bullet: false,
      paraSpaceAfter: config.tocLineSpacing || 10
    }
  }));
  
  slide.addText(tocItems, {
    x: pos.items?.x || 4,
    y: pos.items?.y || 2,
    w: pos.items?.w || 6,
    h: pos.items?.h || 4,
    valign: pos.items?.valign || 'middle',
    lineSpacing: config.tocLineHeight || 40
  });
  
  // 装饰元素（如果模板有）- 位置从模板精确提取
  // ⭐⭐⭐ 注意：必须设置 line: 'none' 避免黑色边框！
  if (config.tocDecorations) {
    config.tocDecorations.forEach(dec => {
      slide.addShape(dec.type || 'rect', {
        x: dec.x, y: dec.y, w: dec.w, h: dec.h,
        fill: { color: dec.color, transparency: dec.transparency },
        line: 'none'  // ⭐ 必须无边框！
      });
    });
  }
  
  return slide;
}
```

### 3.4 章节页生成函数

**⚠️ 注意：章节标题和副标题必须使用模板的对齐方式（通常是居中）！**

```javascript
function createChapterSlide(pptx, config, chapter) {
  const slide = pptx.addSlide();
  
  // ⭐⭐⭐ 使用通用背景处理函数
  applySlideBackground(slide, pptx, config.backgrounds.chapter, config.colors);
  
  const pos = config.positions.chapter;
  
  // 大号章节编号 - 166pt 青色半透明
  slide.addText(chapter.number, {
    x: pos.number.x, y: pos.number.y, w: pos.number.w, h: pos.number.h,
    fontSize: config.fontSizes.chapterNumber,  // 166pt
    fontFace: config.fonts.title,
    color: config.colors.accent,               // 79E8F5
    transparency: 50,                          // 模拟渐变透明
    align: config.alignments.chapterNumber     // ⭐ 使用模板对齐方式
  });
  
  // 章节主标题 - 72pt 粗体白色 居中对齐
  slide.addText(chapter.title, {
    x: pos.title.x, y: pos.title.y, w: pos.title.w, h: pos.title.h,
    fontSize: config.fontSizes.chapterTitle,  // 72pt
    fontFace: config.fonts.title,
    color: config.colors.primary,
    bold: true,
    align: config.alignments.chapterTitle     // ⭐ 居中对齐 'center'
  });
  
  // 章节副标题 - 24pt 白色 居中对齐
  if (chapter.subtitle) {
    slide.addText(chapter.subtitle, {
      x: pos.subtitle.x, y: pos.subtitle.y, w: pos.subtitle.w, h: pos.subtitle.h,
      fontSize: config.fontSizes.chapterSubtitle,  // 24pt
      fontFace: config.fonts.body,
      color: config.colors.primary,
      align: config.alignments.chapterSubtitle  // ⭐ 居中对齐 'center'
    });
  }
  
  return slide;
}
```

### 3.5 内容页生成函数

**⭐⭐⭐ 关键：正文页背景可能是渐变，需要从模板精确提取！**

```javascript
function createContentSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  
  // ⭐⭐⭐ 使用通用背景处理函数
  applySlideBackground(slide, pptx, config.backgrounds.content, config.colors);
    slide.addShape('rect', {
      x: 0, y: 0, w: '100%', h: '100%',
      fill: {
        type: 'gradient',
        gradientType: 'linear',
        rotate: grad.angle,
        stops: grad.stops.map(s => ({
          position: s.position,
          color: s.color,
          transparency: s.transparency || 0
        }))
      },
      line: 'none'  // ⭐ 必须无边框！
    });
  } else if (config.colors?.contentBackground) {
    // 方案3：纯色背景
    slide.background = { color: config.colors.contentBackground };
  }
  
  const pos = config.positions.content;
  
  // 页面小标题 - 32pt
  if (page.subtitle) {
    slide.addText(page.subtitle, {
      x: pos.subtitle.x, y: pos.subtitle.y, w: pos.subtitle.w, h: pos.subtitle.h,
      fontSize: config.fontSizes.pageSubtitle,  // 32pt
      fontFace: config.fonts.title,
      color: config.colors.primary,
      bold: true
    });
  }
  
  // 页面大标题 - 44pt
  slide.addText(page.title, {
    x: pos.title.x, y: pos.title.y, w: pos.title.w, h: pos.title.h,
    fontSize: config.fontSizes.pageTitle,  // 44pt
    fontFace: config.fonts.title,
    color: config.colors.primary,
    bold: true
  });
  
  // 内容区域
  if (page.sections && page.sections.length > 0) {
    const sectionCount = page.sections.length;
    const startY = 3.5;  // 英寸
    const availableHeight = 6.5;
    const sectionHeight = availableHeight / sectionCount;
    
    page.sections.forEach((section, i) => {
      const y = startY + i * sectionHeight;
      
      // 要点标题 - 28pt 粗体
      slide.addText(section.title, {
        x: '3.5%', y: y, w: '42%', h: 0.5,
        fontSize: config.fontSizes.sectionTitle,  // 28pt
        fontFace: config.fonts.title,
        color: config.colors.primary,
        bold: true
      });
      
      // 要点描述 - 16pt
      if (section.desc) {
        const descLines = Array.isArray(section.desc) ? section.desc : [section.desc];
        const descText = descLines.map(line => ({
          text: '• ' + line,
          options: { breakLine: true }
        }));
        
        slide.addText(descText, {
          x: '3.5%', y: y + 0.55, w: '42%', h: sectionHeight - 0.7,
          fontSize: config.fontSizes.bodyText,  // 16pt
          fontFace: config.fonts.body,
          color: config.colors.primary,
          valign: 'top',
          lineSpacingMultiple: 1.3
        });
      }
    });
  }
  
  // 右侧图片
  if (page.image) {
    slide.addImage({
      path: page.image,
      x: pos.image.x, y: pos.image.y,
      w: pos.image.w, h: pos.image.h,
      sizing: { type: 'contain', w: 9, h: 6.2 }
    });
  }
  
  // ⭐ 添加装饰元素（如果模板有）- 注意无边框！
  if (config.decorations?.content) {
    config.decorations.content.forEach(dec => {
      slide.addShape(dec.type || 'rect', {
        x: dec.x, y: dec.y, w: dec.w, h: dec.h,
        fill: { color: dec.fill.color, transparency: dec.fill.transparency || 0 },
        line: 'none'  // ⭐ 必须无边框！
      });
    });
  }
  
  return slide;
}
```

### 3.6 数据卡片页生成函数

**⭐ 注意：卡片背景形状必须正确处理边框！**

```javascript
function createDataCardsSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  
  // ⭐ 背景处理（同内容页）
  if (config.backgrounds.content) {
    slide.background = { path: config.backgrounds.content };
  } else if (config.gradients?.content) {
    const grad = config.gradients.content;
    slide.addShape('rect', {
      x: 0, y: 0, w: '100%', h: '100%',
      fill: {
        type: 'gradient',
        gradientType: 'linear',
        rotate: grad.angle,
        stops: grad.stops
      },
      line: 'none'
    });
  }
  
  // 页面标题
  slide.addText(page.title, {
    x: '5%', y: '8%', w: '90%', h: '10%',
    fontSize: config.fontSizes.pageTitle,
    fontFace: config.fonts.title,
    color: config.colors.primary,
    bold: true,
    align: 'center'
  });
  
  const cards = page.dataCards || [];
  const cardCount = cards.length;
  const cardWidth = cardCount <= 2 ? 7 : (cardCount === 3 ? 5.5 : 4);
  const cardGap = cardCount <= 2 ? 2 : 0.8;
  const totalWidth = cardCount * cardWidth + (cardCount - 1) * cardGap;
  const startX = (20 - totalWidth) / 2;
  
  cards.forEach((card, i) => {
    const x = startX + i * (cardWidth + cardGap);
    
    // ⭐⭐⭐ 卡片背景 - 必须正确处理边框！
    slide.addShape('rect', {
      x: x, y: 3, w: cardWidth, h: 5.5,
      fill: { type: 'solid', color: 'FFFFFF', transparency: 92 },
      // ⭐ 如果模板卡片有边框，从模板提取颜色和宽度
      // ⭐ 如果模板卡片无边框，使用 line: 'none'
      line: config.cardBorder || 'none',  // ⭐ 默认无边框！
      rectRadius: 0.1
    });
    
    // 大号数字
    slide.addText(card.value, {
      x: x + 0.3, y: 3.5, w: cardWidth - 0.6, h: 1.8,
      fontSize: 64,
      fontFace: config.fonts.title,
      color: config.colors.accent,
      bold: true,
      align: 'center'
    });
    
    // 数据后缀
    if (card.suffix) {
      slide.addText(card.suffix, {
        x: x + 0.3, y: 5.2, w: cardWidth - 0.6, h: 0.8,
        fontSize: 24,
        fontFace: config.fonts.title,
        color: config.colors.primary,
        bold: true,
        align: 'center'
      });
    }
    
    // 数据说明
    slide.addText(card.label, {
      x: x + 0.3, y: 6.1, w: cardWidth - 0.6, h: 1.8,
      fontSize: 16,
      fontFace: config.fonts.body,
      color: config.colors.primary,
      align: 'center',
      valign: 'top',
      wrap: true
    });
  });
  
  return slide;
}
```

### 3.7 图表页生成函数

**⭐⭐⭐ pptxgenjs 内置强大的图表功能，支持多种图表类型！**

#### 支持的图表类型

| 类型 | pptxgenjs 常量 | 说明 |
|------|---------------|------|
| 柱状图 | `pptx.ChartType.bar` | 垂直柱状图 |
| 横向柱状图 | `pptx.ChartType.bar3D` | 3D 柱状图 |
| 折线图 | `pptx.ChartType.line` | 折线趋势图 |
| 面积图 | `pptx.ChartType.area` | 面积趋势图 |
| 饼图 | `pptx.ChartType.pie` | 饼状图 |
| 圆环图 | `pptx.ChartType.doughnut` | 环形图 |
| 雷达图 | `pptx.ChartType.radar` | 雷达/蜘蛛图 |
| 散点图 | `pptx.ChartType.scatter` | 散点图 |

#### 图表数据结构

```javascript
// ⭐ 图表数据的标准格式
const chartData = [
  {
    name: "系列1",
    labels: ["类别A", "类别B", "类别C", "类别D"],
    values: [100, 200, 300, 400]
  },
  {
    name: "系列2",
    labels: ["类别A", "类别B", "类别C", "类别D"],
    values: [150, 250, 350, 450]
  }
];
```

#### 图表页生成函数

```javascript
function createChartSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  
  // 背景
  if (config.backgrounds.content) {
    slide.background = { path: config.backgrounds.content };
  }
  
  // 页面标题
  slide.addText(page.title, {
    x: '5%', y: '5%', w: '90%', h: '10%',
    fontSize: config.fontSizes.pageTitle || 36,
    fontFace: config.fonts.title,
    color: config.colors.primary,
    bold: true,
    align: 'center'
  });
  
  // ⭐ 根据图表类型选择
  const chartTypeMap = {
    'bar': pptx.ChartType.bar,
    'bar3d': pptx.ChartType.bar3D,
    'line': pptx.ChartType.line,
    'area': pptx.ChartType.area,
    'pie': pptx.ChartType.pie,
    'doughnut': pptx.ChartType.doughnut,
    'radar': pptx.ChartType.radar,
    'scatter': pptx.ChartType.scatter
  };
  
  const chartType = chartTypeMap[page.chartType] || pptx.ChartType.bar;
  
  // ⭐ 转换数据格式
  const chartData = page.chartData.datasets.map(ds => ({
    name: ds.name,
    labels: page.chartData.labels,
    values: ds.values
  }));
  
  // ⭐ 图表配置选项
  const chartOptions = {
    x: 1, y: 2, w: 18, h: 8,  // 位置和尺寸
    
    // 标题
    showTitle: page.chartOptions?.showTitle || false,
    title: page.chartOptions?.chartTitle || page.title,
    titleFontFace: config.fonts.title,
    titleFontSize: 18,
    titleColor: config.colors.primary,
    
    // 图例
    showLegend: page.chartOptions?.showLegend !== false,
    legendPos: page.chartOptions?.legendPos || 'b',  // 't', 'b', 'l', 'r', 'tr'
    legendFontFace: config.fonts.body,
    legendFontSize: 12,
    legendColor: config.colors.primary,
    
    // 数据标签
    showValue: page.chartOptions?.showValue || false,
    dataLabelPosition: page.chartOptions?.labelPos || 'outEnd',  // 'outEnd', 'inEnd', 'ctr', 'inBase'
    dataLabelFontFace: config.fonts.body,
    dataLabelFontSize: 10,
    dataLabelColor: config.colors.primary,
    
    // 配色
    chartColors: page.chartOptions?.colors || [
      config.colors.accent || '79E8F5',
      config.colors.secondary || 'E7E6E6',
      '0052D9', 'FF6B6B', '4ECDC4', 'FFE66D', '95E1D3', 'F38181'
    ],
    
    // 背景和边框
    fill: page.chartOptions?.fill || 'FFFFFF',
    border: page.chartOptions?.border || { pt: 0, color: 'FFFFFF' },
    
    // 网格线
    catGridLine: { style: 'none' },
    valGridLine: { 
      style: page.chartOptions?.showGridLine !== false ? 'solid' : 'none',
      color: 'E0E0E0',
      size: 0.5
    }
  };
  
  // ⭐⭐⭐ 添加图表
  slide.addChart(chartType, chartData, chartOptions);
  
  // 添加图表说明（如果有）
  if (page.chartDescription) {
    slide.addText(page.chartDescription, {
      x: '5%', y: '92%', w: '90%', h: '6%',
      fontSize: 12,
      fontFace: config.fonts.body,
      color: config.colors.secondary || 'AAAAAA',
      align: 'center'
    });
  }
  
  return slide;
}
```

#### 柱状图/条形图示例

```javascript
// ⭐ 基础柱状图
function createBarChartSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  slide.background = { path: config.backgrounds.content };
  
  const chartData = [
    {
      name: "销售额",
      labels: ["一月", "二月", "三月", "四月", "五月", "六月"],
      values: [120, 180, 150, 200, 250, 220]
    }
  ];
  
  slide.addChart(pptx.ChartType.bar, chartData, {
    x: 1, y: 2, w: 18, h: 8,
    showLegend: true,
    legendPos: 'b',
    showValue: true,
    dataLabelPosition: 'outEnd',
    chartColors: [config.colors.accent],
    barGapWidthPct: 50,  // 柱子间距
    // 3D 效果（可选）
    // bar3DShape: 'cylinder',
    // shadow: { type: 'outer', blur: 3, offset: 3, angle: 45, opacity: 0.4 }
  });
  
  return slide;
}

// ⭐ 多系列柱状图（对比图）
function createGroupedBarChartSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  
  const chartData = [
    {
      name: "2024年",
      labels: ["Q1", "Q2", "Q3", "Q4"],
      values: [100, 150, 200, 180]
    },
    {
      name: "2025年",
      labels: ["Q1", "Q2", "Q3", "Q4"],
      values: [120, 180, 220, 250]
    }
  ];
  
  slide.addChart(pptx.ChartType.bar, chartData, {
    x: 1, y: 2, w: 18, h: 8,
    showLegend: true,
    showValue: true,
    chartColors: ['79E8F5', '0052D9'],
    barGrouping: 'clustered'  // 'clustered' 分组, 'stacked' 堆叠, 'percentStacked' 百分比堆叠
  });
  
  return slide;
}

// ⭐ 堆叠柱状图
function createStackedBarChartSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  
  const chartData = [
    { name: "产品A", labels: ["Q1", "Q2", "Q3", "Q4"], values: [50, 60, 70, 80] },
    { name: "产品B", labels: ["Q1", "Q2", "Q3", "Q4"], values: [30, 40, 50, 60] },
    { name: "产品C", labels: ["Q1", "Q2", "Q3", "Q4"], values: [20, 30, 40, 50] }
  ];
  
  slide.addChart(pptx.ChartType.bar, chartData, {
    x: 1, y: 2, w: 18, h: 8,
    barGrouping: 'stacked',  // ⭐ 堆叠模式
    showLegend: true,
    showValue: true,
    chartColors: ['79E8F5', '0052D9', 'FF6B6B']
  });
  
  return slide;
}
```

#### 折线图/面积图示例

```javascript
// ⭐ 折线图（趋势分析）
function createLineChartSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  
  const chartData = [
    {
      name: "用户增长",
      labels: ["1月", "2月", "3月", "4月", "5月", "6月"],
      values: [1000, 1500, 2200, 3100, 4500, 6800]
    },
    {
      name: "活跃用户",
      labels: ["1月", "2月", "3月", "4月", "5月", "6月"],
      values: [800, 1200, 1800, 2600, 3800, 5500]
    }
  ];
  
  slide.addChart(pptx.ChartType.line, chartData, {
    x: 1, y: 2, w: 18, h: 8,
    showLegend: true,
    legendPos: 'r',  // 右侧图例
    
    // 线条样式
    lineSize: 2,           // 线条粗细
    lineSmooth: true,      // 平滑曲线
    
    // 数据点标记
    lineDataSymbol: 'circle',  // 'circle', 'dash', 'diamond', 'dot', 'none', 'square', 'triangle'
    lineDataSymbolSize: 8,
    
    // 显示数据值
    showValue: true,
    dataLabelPosition: 'outEnd',
    
    chartColors: ['79E8F5', '0052D9']
  });
  
  return slide;
}

// ⭐ 面积图（带填充）
function createAreaChartSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  
  const chartData = [
    {
      name: "收入",
      labels: ["Q1", "Q2", "Q3", "Q4"],
      values: [100, 200, 300, 400]
    }
  ];
  
  slide.addChart(pptx.ChartType.area, chartData, {
    x: 1, y: 2, w: 18, h: 8,
    showLegend: true,
    chartColors: ['79E8F5'],
    // 透明度
    chartColorsOpacity: 50  // 50% 透明
  });
  
  return slide;
}
```

#### 饼图/圆环图示例

```javascript
// ⭐ 饼图（占比分析）
function createPieChartSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  slide.background = { path: config.backgrounds.content };
  
  // 标题
  slide.addText(page.title || '市场份额分析', {
    x: '5%', y: '5%', w: '90%', h: '10%',
    fontSize: 36,
    fontFace: config.fonts.title,
    color: config.colors.primary,
    bold: true,
    align: 'center'
  });
  
  const chartData = [
    {
      name: "市场份额",
      labels: ["产品A", "产品B", "产品C", "其他"],
      values: [45, 25, 20, 10]
    }
  ];
  
  slide.addChart(pptx.ChartType.pie, chartData, {
    x: 4, y: 2.5, w: 12, h: 7,  // 居中放置
    showLegend: true,
    legendPos: 'r',
    
    // 显示百分比
    showValue: true,
    showPercent: true,       // ⭐ 显示百分比
    showLabel: true,         // 显示标签
    
    // 饼图特有选项
    firstSliceAng: 0,        // 第一块起始角度
    
    chartColors: ['79E8F5', '0052D9', 'FF6B6B', 'E7E6E6']
  });
  
  return slide;
}

// ⭐ 圆环图（带中心说明）
function createDoughnutChartSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  
  const chartData = [
    {
      name: "项目进度",
      labels: ["已完成", "进行中", "未开始"],
      values: [65, 25, 10]
    }
  ];
  
  slide.addChart(pptx.ChartType.doughnut, chartData, {
    x: 4, y: 2.5, w: 12, h: 7,
    showLegend: true,
    legendPos: 'b',
    showValue: true,
    showPercent: true,
    
    // 圆环特有选项
    holeSize: 50,  // ⭐ 中心空洞大小（百分比）
    
    chartColors: ['4ECDC4', 'FFE66D', 'FF6B6B']
  });
  
  // ⭐ 在圆环中心添加说明文字
  slide.addText('65%\n完成率', {
    x: 7.5, y: 5, w: 5, h: 1.5,
    fontSize: 32,
    fontFace: config.fonts.title,
    color: config.colors.primary,
    bold: true,
    align: 'center',
    valign: 'middle'
  });
  
  return slide;
}
```

#### 雷达图示例

```javascript
// ⭐ 雷达图（多维度对比）
function createRadarChartSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  
  const chartData = [
    {
      name: "产品A",
      labels: ["性能", "易用性", "稳定性", "安全性", "可扩展性"],
      values: [90, 75, 85, 80, 70]
    },
    {
      name: "产品B",
      labels: ["性能", "易用性", "稳定性", "安全性", "可扩展性"],
      values: [70, 90, 75, 85, 90]
    }
  ];
  
  slide.addChart(pptx.ChartType.radar, chartData, {
    x: 3, y: 2, w: 14, h: 8,
    showLegend: true,
    legendPos: 'b',
    
    // 雷达图特有选项
    radarStyle: 'standard',  // 'standard' 或 'marker' 或 'filled'
    
    chartColors: ['79E8F5', '0052D9']
  });
  
  return slide;
}
```

#### 组合图表示例

```javascript
// ⭐ 柱状图+折线图组合（双坐标轴）
function createComboChartSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  
  // 销售额数据（柱状图）
  const barData = [
    {
      name: "销售额(万)",
      labels: ["Q1", "Q2", "Q3", "Q4"],
      values: [100, 150, 200, 180]
    }
  ];
  
  // 增长率数据（折线图）
  const lineData = [
    {
      name: "增长率(%)",
      labels: ["Q1", "Q2", "Q3", "Q4"],
      values: [10, 50, 33, -10]
    }
  ];
  
  // ⭐ 使用 addChart 的组合模式
  slide.addChart(
    [pptx.ChartType.bar, pptx.ChartType.line],
    [barData, lineData],
    {
      x: 1, y: 2, w: 18, h: 8,
      showLegend: true,
      
      // 双坐标轴
      catAxisTitle: '季度',
      valAxisTitle: '销售额',
      secondaryValAxis: true,       // ⭐ 启用第二纵坐标轴
      secondaryValAxisTitle: '增长率',
      
      chartColors: ['79E8F5', 'FF6B6B']
    }
  );
  
  return slide;
}
```

#### 图表样式美化

```javascript
// ⭐⭐⭐ 通用图表美化配置
const chartStyleOptions = {
  // 标题样式
  showTitle: true,
  title: '图表标题',
  titleFontFace: '腾讯体 W7',
  titleFontSize: 18,
  titleColor: 'FFFFFF',
  titlePos: { x: 0, y: 0 },
  
  // 图例样式
  showLegend: true,
  legendPos: 'b',  // 底部
  legendFontFace: '方正兰亭黑简体',
  legendFontSize: 12,
  legendColor: 'FFFFFF',
  
  // 坐标轴样式
  catAxisTitle: 'X轴标题',
  valAxisTitle: 'Y轴标题',
  catAxisLabelColor: 'FFFFFF',
  valAxisLabelColor: 'FFFFFF',
  catAxisLabelFontSize: 11,
  valAxisLabelFontSize: 11,
  catAxisLineShow: true,
  valAxisLineShow: false,
  
  // 网格线
  catGridLine: { style: 'none' },
  valGridLine: { 
    style: 'dash',   // 'solid', 'dash', 'dot', 'none'
    color: 'FFFFFF',
    size: 0.5
  },
  
  // 数据标签
  showValue: true,
  dataLabelPosition: 'outEnd',
  dataLabelFontFace: '方正兰亭黑简体',
  dataLabelFontSize: 10,
  dataLabelColor: 'FFFFFF',
  dataLabelFontBold: false,
  
  // 图表区域
  fill: 'TRANSPARENT',  // 透明背景
  border: { pt: 0, color: 'FFFFFF' },
  
  // 阴影效果
  shadow: {
    type: 'outer',
    blur: 3,
    offset: 2,
    angle: 45,
    opacity: 0.3
  }
};
```

#### 从数据自动生成图表

```javascript
// ⭐ 智能图表类型推荐
function recommendChartType(data) {
  const seriesCount = data.datasets?.length || 1;
  const labelCount = data.labels?.length || 0;
  const isTimeSeries = data.labels?.some(l => /^\d{4}|[Q季月]/.test(l));
  const isPercentage = data.datasets?.every(ds => 
    ds.values.reduce((a, b) => a + b, 0) <= 100
  );
  
  // 占比数据 -> 饼图/圆环图
  if (isPercentage && labelCount <= 6) {
    return labelCount <= 4 ? 'pie' : 'doughnut';
  }
  
  // 时间序列 -> 折线图
  if (isTimeSeries) {
    return 'line';
  }
  
  // 多系列对比 -> 柱状图
  if (seriesCount > 1 && labelCount <= 10) {
    return 'bar';
  }
  
  // 多维度评估 -> 雷达图
  if (labelCount >= 5 && labelCount <= 8 && seriesCount <= 3) {
    return 'radar';
  }
  
  // 默认柱状图
  return 'bar';
}

// ⭐ 根据数据自动生成图表页
function createAutoChartSlide(pptx, config, page) {
  const chartType = page.chartType || recommendChartType(page.chartData);
  
  // 根据推荐类型调用对应函数
  switch (chartType) {
    case 'pie':
    case 'doughnut':
      return createPieChartSlide(pptx, config, { ...page, chartType });
    case 'line':
    case 'area':
      return createLineChartSlide(pptx, config, { ...page, chartType });
    case 'radar':
      return createRadarChartSlide(pptx, config, { ...page, chartType });
    default:
      return createBarChartSlide(pptx, config, { ...page, chartType });
  }
}
```

#### 表格展示

```javascript
// ⭐ 数据表格（配合图表使用）
function addDataTable(slide, config, tableData, options = {}) {
  const { 
    x = 1, y = 8, w = 18, h = 2,
    headerColor = config.colors.accent,
    headerTextColor = config.colors.dark,
    bodyColor = 'FFFFFF',
    bodyTextColor = config.colors.dark,
    fontSize = 12
  } = options;
  
  // 表头
  const header = tableData.headers.map(h => ({
    text: h,
    options: {
      fill: headerColor,
      color: headerTextColor,
      bold: true,
      align: 'center',
      fontFace: config.fonts.title
    }
  }));
  
  // 表格数据
  const rows = [header];
  tableData.rows.forEach((row, i) => {
    rows.push(row.map(cell => ({
      text: String(cell),
      options: {
        fill: i % 2 === 0 ? bodyColor : 'F5F5F5',
        color: bodyTextColor,
        align: 'center',
        fontFace: config.fonts.body
      }
    })));
  });
  
  slide.addTable(rows, {
    x, y, w, h,
    fontSize,
    border: { pt: 0.5, color: 'E0E0E0' },
    colW: Array(tableData.headers.length).fill(w / tableData.headers.length)
  });
}

// ⭐ 图表+表格组合页
function createChartWithTableSlide(pptx, config, page) {
  const slide = pptx.addSlide();
  slide.background = { path: config.backgrounds.content };
  
  // 标题
  slide.addText(page.title, {
    x: '5%', y: '3%', w: '90%', h: '8%',
    fontSize: 32,
    fontFace: config.fonts.title,
    color: config.colors.primary,
    bold: true,
    align: 'center'
  });
  
  // 图表（上半部分）
  const chartData = page.chartData.datasets.map(ds => ({
    name: ds.name,
    labels: page.chartData.labels,
    values: ds.values
  }));
  
  slide.addChart(pptx.ChartType.bar, chartData, {
    x: 1, y: 1.5, w: 18, h: 5.5,
    showLegend: true,
    showValue: true,
    chartColors: ['79E8F5', '0052D9', 'FF6B6B']
  });
  
  // 表格（下半部分）
  const tableData = {
    headers: ['指标', ...page.chartData.labels],
    rows: page.chartData.datasets.map(ds => [ds.name, ...ds.values])
  };
  
  addDataTable(slide, config, tableData, {
    x: 1, y: 7.5, w: 18, h: 2.5
  });
  
  return slide;
}
```

### 3.8 感谢页生成函数

```javascript
function createThanksSlide(pptx, config) {
  const slide = pptx.addSlide();
  
  // ⭐⭐⭐ 使用通用背景处理函数
  applySlideBackground(slide, pptx, config.backgrounds.thanks, config.colors);
  
  slide.addText('THANKS', {
    x: '5%', y: '40%', w: '50%', h: '20%',
    fontSize: config.fontSizes.thanks,
    fontFace: config.fonts.title,
    color: config.colors.primary,
    bold: true
  });
  
  return slide;
}
```

### 3.9 完整生成流程

```javascript
async function generatePPT(config, content) {
  const pptx = new pptxgen();
  
  pptx.defineLayout({ name: 'LAYOUT_WIDE', width: 20, height: 11.25 });
  pptx.layout = 'LAYOUT_WIDE';
  
  // 1. 封面页
  createCoverSlide(pptx, config, content);
  
  // 2. 目录页
  createTOCSlide(pptx, config, content.chapters);
  
  // 3. 各章节
  content.chapters.forEach(chapter => {
    // 章节页
    createChapterSlide(pptx, config, chapter);
    
    // 内容页
    chapter.pages.forEach(page => {
      switch(page.type) {
        case 'dataCards':
          createDataCardsSlide(pptx, config, page);
          break;
        case 'textOnly':
          createTextOnlySlide(pptx, config, page);
          break;
        case 'chart':
          createChartSlide(pptx, config, page);
          break;
        case 'chartWithTable':
          createChartWithTableSlide(pptx, config, page);
          break;
        default:
          createContentSlide(pptx, config, page);
      }
    });
  });
  
  // 4. 感谢页
  createThanksSlide(pptx, config);
  
  // 5. 保存
  await pptx.writeFile({ fileName: 'output.pptx' });
}
```

---

## 第四阶段：清理临时文件

```bash
# 清理所有临时文件
rm -rf workspace/template-analysis
rm -rf workspace/docx-extract
rm -rf workspace/backgrounds
rm -rf workspace/images
rm -rf workspace/node_modules
rm -f workspace/package*.json
rm -f workspace/create-pptx.js

# 只保留最终 PPT
ls workspace/*.pptx
```

---

## 关键要点总结

### ⚠️ 必须遵守的原则

**⭐⭐⭐ 核心原则：所有配置必须从当前模板动态提取，绝不能写死或复制其他模板的值！**

1. **精确提取参数** - 所有字号、位置、颜色必须从 slide XML 精确提取
2. **精确提取字体** - ⭐⭐⭐ **字体名称必须从 `<a:latin typeface="..."/>` 和 `<a:ea typeface="..."/>` 精确提取，不同模板字体完全不同！**
3. **精确提取对齐方式** - ⭐⭐ **对齐方式必须从 `algn` 属性提取，不同模板的对齐设置差异很大！**
4. **不要添加额外元素** - 如果模板目录页没有"目录"标题，就不要添加
5. **保持布局一致** - 位置和尺寸必须与模板匹配
6. **单位换算正确** - sz ÷ 100 = pt, EMU ÷ 914400 = inch

### 常见错误避免

| 错误 | 正确做法 |
|------|----------|
| 使用推测的字号 | 从 XML 的 `sz` 属性精确提取 |
| 使用推测的位置 | 从 XML 的 `<a:off>` 精确提取 |
| 添加模板没有的元素 | 只复制模板实际有的元素 |
| 使用错误的颜色 | 从 XML 的 `srgbClr` 精确提取 |
| **使用默认字体（如等线）** | **⭐ 从 XML 精确提取字体名称** |
| **使用错误的对齐方式** | **⭐ 从 XML 的 `algn` 属性提取** |
| **复制其他模板的配置** | **⭐⭐⭐ 每个模板必须单独分析！** |
| **文本框宽度不足导致换行** | **⭐ 使用动态宽度计算或 `fit: 'shrink'`** |
| **封面图片布局不正确** | **⭐ 分析模板的斜切/遮罩层次结构** |
| **形状出现黑色边框** | **⭐⭐⭐ 必须设置 `line: { color: 'FFFFFF', width: 0 }` 或 `line: 'none'`** |
| **背景渐变方向/颜色错误** | **⭐ 从 `<a:gradFill>` 精确提取渐变参数** |

### ⭐⭐⭐ 文本宽度处理（防止换行）

**问题：** 标题文字超出文本框宽度时会自动换行，破坏布局。

**解决方案 1：动态计算宽度**
```javascript
// 根据文字内容动态计算所需宽度
function calculateTextWidth(text, fontSize) {
  let width = 0;
  for (const char of text) {
    // 中文字符宽度约等于字号，英文约0.5倍
    width += /[\u4e00-\u9fa5]/.test(char) ? fontSize / 72 : fontSize / 72 * 0.5;
  }
  return width * 1.15; // 留15%余量
}

// 使用
const titleWidth = calculateTextWidth(content.title, 66);
slide.addText(content.title, {
  w: Math.max(titleWidth, 8),  // 确保最小宽度
  // ...
});
```

**解决方案 2：使用 fit 选项**
```javascript
slide.addText(content.title, {
  w: 10, h: 1.5,
  fit: 'shrink',  // 自动缩小字号以适应宽度
  // ...
});
```

**解决方案 3：使用 autoFit 选项（推荐）**
```javascript
slide.addText(content.title, {
  w: '80%',  // 使用较大的百分比宽度
  autoFit: true,  // 自动调整
  // ...
});
```

### ⭐⭐⭐ 封面页斜切布局处理（通用方案）

**问题：** 某些模板使用斜切（平行四边形）图片和遮罩布局。

**⭐ 通用分析步骤：**

```
1. 解压模板，读取封面页 slide XML
2. 识别所有 <p:sp> 形状元素及其层次顺序
3. 分析每个形状的：
   - 类型：<a:prstGeom prst="rect"/> 或 <a:custGeom>
   - 位置：<a:off x="..." y="..."/>
   - 尺寸：<a:ext cx="..." cy="..."/>
   - 填充：<a:solidFill> + <a:srgbClr val="..."/>
   - 透明度：<a:alpha val="..."/> (50000 = 50%)
4. 按顺序重建层次结构
```

**⭐ pptxgenjs 实现方案（通用框架）：**

```javascript
function createCoverSlide(pptx, config, content) {
  const slide = pptx.addSlide();
  
  // 1. 背景（从模板提取）
  slide.background = { color: config.colors.dark };
  
  // 2. 图片层（如果模板有）- 位置从模板精确提取！
  if (config.coverLayout?.photo) {
    const photo = config.coverLayout.photo;
    slide.addImage({
      path: config.backgrounds.coverPhoto,
      x: photo.x, y: photo.y, w: photo.w, h: photo.h
    });
  }
  
  // 3. 遮罩层（如果模板有）- 参数从模板精确提取！
  // pptxgenjs 不支持自定义路径，使用多层矩形模拟
  if (config.coverLayout?.overlays) {
    config.coverLayout.overlays.forEach(overlay => {
      slide.addShape('rect', {
        x: overlay.x, y: overlay.y, w: overlay.w, h: overlay.h,
        fill: { color: overlay.color, transparency: overlay.transparency || 0 },
        line: { width: 0 }
      });
    });
  }
  
  // 4. 文字元素...
}
```

**关键点：**
- 图片位置从模板 XML 的 `<a:off>` 和 `<a:ext>` 精确提取
- 斜切角度从模板的 `<a:path>` 路径计算
- 遮罩透明度从 `<a:alpha val="50000"/>` 提取（50000 = 50%）

### 字体提取关键点

**⚠️ pptxgenjs 会使用默认字体（如"等线"），必须显式指定模板字体！**

```xml
<!-- 模板 XML 中的字体定义示例 -->
<a:rPr lang="zh-CN" sz="8000" b="1">
  <a:latin typeface="Calibri"/>           <!-- 西文字体 -->
  <a:ea typeface="腾讯体 W7"/>            <!-- 东亚/中文字体 -->
</a:rPr>
```

**提取字体的 Python 命令：**
```bash
cat ppt/slides/slide1.xml | python3 -c "
import sys, re
content = sys.stdin.read()
print('Latin字体:', set(re.findall(r'latin typeface=\"([^\"]+)\"', content)))
print('EA字体:', set(re.findall(r'ea typeface=\"([^\"]+)\"', content)))
"
```

**在 pptxgenjs 中正确使用字体：**
```javascript
// ⭐ 必须使用模板提取的字体名称
slide.addText('标题文本', {
  fontFace: '腾讯体 W7',  // 从模板提取的实际字体
  fontSize: 80,
  // ...
});
```

### 单位换算公式

```
字号: sz 值 ÷ 100 = pt
位置/尺寸: EMU ÷ 914400 = inch
百分比: inch ÷ 画布尺寸 × 100%

画布尺寸 (16:9): 20 × 11.25 inch
```

### 字体/对齐映射表模板（每次分析模板后填写）

**⚠️⚠️⚠️ 以下是空白模板！每次分析新模板时，必须填写该模板的实际值！**

**不同模板的字体、对齐方式完全不同，绝不能复制其他模板的配置！**

| 元素类型 | EA字体(从XML提取) | Latin字体(从XML提取) | 字号(从sz计算) | 对齐(从algn提取) |
|----------|------------------|---------------------|---------------|-----------------|
| 封面主标题 | `<填写>` | `<填写>` | `<填写>pt` | `<填写>` |
| 封面副标题 | `<填写>` | `<填写>` | `<填写>pt` | `<填写>` |
| 目录编号 | `<填写>` | `<填写>` | `<填写>pt` | `<填写>` |
| 目录标题 | `<填写>` | `<填写>` | `<填写>pt` | `<填写>` |
| 章节编号 | `<填写>` | `<填写>` | `<填写>pt` | `<填写>` |
| 章节标题 | `<填写>` | `<填写>` | `<填写>pt` | `<填写>` |
| 章节副标题 | `<填写>` | `<填写>` | `<填写>pt` | `<填写>` |
| 内容大标题 | `<填写>` | `<填写>` | `<填写>pt` | `<填写>` |
| 内容正文 | `<填写>` | `<填写>` | `<填写>pt` | `<填写>` |

**示例（某腾讯模板分析结果，仅供参考格式）：**

| 元素类型 | EA字体 | Latin字体 | 字号 | 对齐 |
|----------|--------|-----------|------|------|
| 封面主标题 | 腾讯体 W7 | Calibri | 80pt | right |
| 章节标题 | 腾讯体 W7 | Calibri | 72pt | center |
| 内容正文 | 方正兰亭黑简体 | 方正兰亭黑简体 | 16pt | left |

**⚠️ 上面的示例值只是参考格式，实际使用时必须分析当前模板获取！**

### 对齐方式映射

| XML algn 值 | pptxgenjs align 值 | 说明 |
|-------------|-------------------|------|
| 无属性 | 'left' | 默认左对齐 |
| l | 'left' | 左对齐 |
| ctr | 'center' | 居中对齐 |
| r | 'right' | 右对齐 |
| just | 'justify' | 两端对齐 |

### 模板分析脚本模板

```python
#!/usr/bin/env python3
import re
import sys

def analyze_slide(content):
    """分析单页幻灯片的精确参数"""
    result = {
        'texts': [],
        'sizes': {},
        'colors': set(),
        'positions': []
    }
    
    # 提取文本
    result['texts'] = [t for t in re.findall(r'<a:t>([^<]+)</a:t>', content) if t.strip()]
    
    # 提取字号
    for s in set(re.findall(r'sz="(\d+)"', content)):
        result['sizes'][s] = f'{int(s)/100}pt'
    
    # 提取颜色
    result['colors'] = set(re.findall(r'srgbClr val="([^"]+)"', content))
    
    # 提取位置
    for x, y in re.findall(r'<a:off x="(\d+)" y="(\d+)"/>', content):
        x_pct = int(x) / 914400 / 20 * 100
        y_pct = int(y) / 914400 / 11.25 * 100
        result['positions'].append({'x': f'{x_pct:.1f}%', 'y': f'{y_pct:.1f}%'})
    
    return result

# 使用示例
with open('workspace/template-analysis/ppt/slides/slide1.xml', 'r') as f:
    result = analyze_slide(f.read())
    print(result)
```

---

## ⭐⭐⭐ 关键细节：形状边框和背景渐变处理

### 形状边框问题（黑色边框修复）

**问题现象：** 模板中的形状是无边框的，但生成的PPT中出现了黑色边框。

**原因分析：**

模板 XML 中形状的边框定义方式：
```xml
<!-- 方式1：有 <a:ln> 但无填充定义 = 默认黑色边框 -->
<a:ln w="12700">
  <a:miter lim="400000"/>
</a:ln>

<!-- 方式2：显式无边框 -->
<a:ln w="12700" cap="flat">
  <a:noFill/>          <!-- ⭐ 这才是真正的无边框 -->
  <a:miter lim="400000"/>
</a:ln>
```

**⭐⭐⭐ pptxgenjs 解决方案：**

```javascript
// ❌ 错误：会产生默认黑色边框
slide.addShape('rect', {
  x: 1, y: 2, w: 3, h: 4,
  fill: { color: 'FFFFFF', transparency: 90 }
  // 没有指定 line，默认会有黑色边框！
});

// ✅ 正确方案1：显式设置 line 为透明或同色
slide.addShape('rect', {
  x: 1, y: 2, w: 3, h: 4,
  fill: { color: 'FFFFFF', transparency: 90 },
  line: { color: 'FFFFFF', width: 0 }  // ⭐ 无边框
});

// ✅ 正确方案2：使用 line: 'none'（推荐）
slide.addShape('rect', {
  x: 1, y: 2, w: 3, h: 4,
  fill: { color: 'FFFFFF', transparency: 90 },
  line: 'none'  // ⭐ 最简洁的无边框写法
});

// ✅ 正确方案3：line 宽度设为 0
slide.addShape('rect', {
  x: 1, y: 2, w: 3, h: 4,
  fill: { color: 'FFFFFF', transparency: 90 },
  line: { width: 0 }
});
```

**⭐ 分析模板边框的方法：**

```python
# 检查形状是否有边框
import re
with open('slide.xml', 'r') as f:
    content = f.read()
    
# 查找所有 <a:ln> 定义
lns = re.findall(r'<a:ln[^>]*>(.*?)</a:ln>', content, re.DOTALL)
for ln in lns:
    if '<a:noFill/>' in ln:
        print('无边框')
    elif '<a:solidFill>' in ln:
        print('有边框，颜色:', re.findall(r'val="([^"]+)"', ln))
    else:
        print('⚠️ 默认黑色边框（需要在生成时设置 line: none）')
```

### 背景渐变处理

**问题现象：** 正文页背景色与模板不一致（颜色、渐变方向、渐变位置不对）。

**⭐⭐⭐ 模板渐变分析方法：**

模板中的渐变定义示例（来自 slide6.xml）：
```xml
<a:gradFill flip="none" rotWithShape="1">
  <a:gsLst>
    <!-- pos="0" 表示渐变起点(0%) -->
    <a:gs pos="0">
      <a:srgbClr val="0052D9">
        <a:alpha val="0"/>           <!-- 0% 透明度 = 完全透明 -->
        <a:lumMod val="78000"/>      <!-- 亮度调整 -->
        <a:lumOff val="22000"/>
      </a:srgbClr>
    </a:gs>
    <!-- pos="62000" 表示渐变中间点(62%) -->
    <a:gs pos="62000">
      <a:schemeClr val="accent1"/>   <!-- 使用主题色 -->
    </a:gs>
    <!-- pos="100000" 表示渐变终点(100%) -->
    <a:gs pos="100000">
      <a:schemeClr val="accent1"/>
    </a:gs>
  </a:gsLst>
  <!-- 渐变角度：ang="11400000" = 114° (值 ÷ 60000) -->
  <a:lin ang="11400000" scaled="0"/>
</a:gradFill>
```

**⭐ 渐变参数解析：**

```
1. 渐变颜色停止点 (<a:gs>):
   - pos="0"       -> 0% 位置
   - pos="50000"   -> 50% 位置
   - pos="100000"  -> 100% 位置

2. 渐变角度 (<a:lin ang="...">):
   - ang 值 ÷ 60000 = 实际角度（度）
   - ang="0"        -> 0° (从左到右)
   - ang="5400000"  -> 90° (从上到下)
   - ang="10800000" -> 180° (从右到左)
   - ang="11400000" -> 190° (略微从右上到左下)

3. 透明度 (<a:alpha val="...">):
   - val="0"       -> 完全透明
   - val="50000"   -> 50% 透明
   - val="100000"  -> 完全不透明
```

**⭐⭐⭐ pptxgenjs 实现渐变：**

```javascript
// 方案1：使用渐变填充（推荐）
slide.addShape('rect', {
  x: 0, y: 0, w: '100%', h: '100%',
  fill: {
    type: 'gradient',
    gradientType: 'linear',
    // ⭐ 角度：pptxgenjs 使用 0-360 度
    rotate: 190,  // 从模板 ang="11400000" 计算: 11400000/60000 = 190°
    stops: [
      // ⭐ position 是 0-100 的百分比
      { position: 0, color: '0052D9', transparency: 100 },  // 起点透明
      { position: 62, color: '0052D9' },                    // 62% 位置不透明
      { position: 100, color: '0052D9' }                    // 终点不透明
    ]
  },
  line: 'none'
});

// 方案2：使用背景图片（如果渐变太复杂）
slide.background = { path: 'backgrounds/gradient-bg.png' };

// 方案3：多层叠加模拟渐变（兼容性更好）
// 底层纯色
slide.background = { color: '0052D9' };
// 上层半透明渐变遮罩
slide.addShape('rect', {
  x: 0, y: 0, w: '100%', h: '100%',
  fill: {
    type: 'gradient',
    gradientType: 'linear',
    rotate: 190,
    stops: [
      { position: 0, color: 'FFFFFF', transparency: 100 },
      { position: 100, color: 'FFFFFF', transparency: 0 }
    ]
  },
  line: 'none'
});
```

**⭐ 从模板提取渐变参数的脚本：**

```python
import re

def extract_gradient(xml_content):
    """从 XML 提取渐变参数"""
    result = {
        'type': None,
        'angle': None,
        'stops': []
    }
    
    # 检查是否有渐变
    gradFill = re.search(r'<a:gradFill[^>]*>(.*?)</a:gradFill>', xml_content, re.DOTALL)
    if not gradFill:
        return None
    
    grad_content = gradFill.group(1)
    
    # 提取角度
    lin = re.search(r'<a:lin ang="(\d+)"', grad_content)
    if lin:
        result['type'] = 'linear'
        result['angle'] = int(lin.group(1)) / 60000  # 转换为度
    
    # 提取颜色停止点
    for gs in re.finditer(r'<a:gs pos="(\d+)">(.*?)</a:gs>', grad_content, re.DOTALL):
        position = int(gs.group(1)) / 1000  # 转换为百分比
        gs_content = gs.group(2)
        
        stop = {'position': position}
        
        # 提取颜色
        color = re.search(r'srgbClr val="([^"]+)"', gs_content)
        if color:
            stop['color'] = color.group(1)
        
        # 提取透明度
        alpha = re.search(r'<a:alpha val="(\d+)"', gs_content)
        if alpha:
            stop['transparency'] = 100 - int(alpha.group(1)) / 1000
        
        result['stops'].append(stop)
    
    return result

# 使用
with open('ppt/slides/slide6.xml', 'r') as f:
    grad = extract_gradient(f.read())
    print('渐变参数:', grad)
```

### 装饰形状的透明度处理

**模板中常见的装饰形状：**

```xml
<!-- 白色低透明度方块（约10%可见） -->
<a:solidFill>
  <a:srgbClr val="FFFFFF">
    <a:alpha val="9876"/>   <!-- 9876/100000 ≈ 10% 不透明 = 90% 透明 -->
  </a:srgbClr>
</a:solidFill>

<!-- 白色半透明方块（约50%可见） -->
<a:solidFill>
  <a:srgbClr val="FFFFFF">
    <a:alpha val="49687"/>  <!-- 约50% 不透明 = 50% 透明 -->
  </a:srgbClr>
</a:solidFill>
```

**⭐ pptxgenjs 透明度计算：**

```javascript
// XML alpha 值转换为 pptxgenjs transparency
// pptxgenjs: transparency = 100 - (alpha值/1000)

// 示例：alpha val="9876" -> 约10%不透明 -> transparency=90
slide.addShape('rect', {
  x: 1, y: 2, w: 1.3, h: 1.3,
  fill: { 
    color: 'FFFFFF', 
    transparency: 90  // ⭐ 90%透明 = 10%可见
  },
  line: 'none'  // ⭐ 必须！否则有黑边
});

// 示例：alpha val="49687" -> 约50%不透明 -> transparency=50
slide.addShape('rect', {
  x: 2, y: 4, w: 0.6, h: 0.6,
  fill: { 
    color: 'FFFFFF', 
    transparency: 50  // ⭐ 50%透明
  },
  line: 'none'
});
```

### 配置模板示例（包含边框和渐变）

```javascript
const TEMPLATE_CONFIG = {
  // ... 其他配置 ...
  
  // ⭐⭐⭐ 渐变背景配置（从模板 gradFill 提取）
  gradients: {
    // 正文页渐变（从 slide6.xml 提取）
    content: {
      type: 'linear',
      angle: 190,  // ang="11400000" / 60000
      stops: [
        { position: 0, color: '0052D9', transparency: 100 },  // 起点透明
        { position: 62, color: '0052D9', transparency: 0 },   // 62%位置不透明
        { position: 100, color: '0052D9', transparency: 0 }   // 终点不透明
      ]
    }
  },
  
  // ⭐⭐⭐ 装饰形状配置（从模板 sp 元素提取）
  decorations: {
    // 章节页装饰方块
    chapter: [
      {
        type: 'rect',
        x: 1.22, y: 2.31, w: 1.31, h: 1.31,
        fill: { color: 'FFFFFF', transparency: 90 },  // alpha=9876
        line: 'none'  // ⭐ 无边框！
      },
      {
        type: 'rect',
        x: 1.95, y: 4.59, w: 0.58, h: 0.58,
        fill: { color: 'FFFFFF', transparency: 50 },  // alpha=49687
        line: 'none'
      }
    ],
    // 目录页装饰方块
    toc: [
      // ... 从模板提取
    ]
  }
};
```

---

## 依赖

- Node.js 14+
- pptxgenjs 3.x
- Python 3.x (用于文件处理)

```bash
npm install pptxgenjs
```
