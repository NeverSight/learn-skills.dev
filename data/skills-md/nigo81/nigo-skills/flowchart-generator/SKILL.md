---
name: flowchart-generator
description: 内控和审计流程图生成工具。当用户需要绘制泳道流程图、审批流程、报销流程、内控流程、资金流程、采购流程或任何业务流程图时使用。支持从自然语言描述生成 .drawio/PNG/SVG/VSDX 格式。即使没有明确说"流程图"，只要涉及"画图"、"可视化"、"绘制"业务流程，也应触发。也适用于用户说"帮我画个XX流程"或"把这个流程可视化"等场景。
slug: nigo-flowchart-generator
displayName: 审计流程图生成器
version: 1.0.0
summary: 内控和审计流程图生成工具，从自然语言描述生成 .drawio/PNG/SVG/VSDX 格式的泳道流程图、审批流程、报销流程等。
license: MIT
---

# Flowchart Generator Skill

> **制作人：nigo** | **微信公众号：逆行的狗**

专业的内控和审计流程图生成工具，用于将业务流程描述转换为标准的泳道流程图。

## 适用场景

当用户遇到以下需求时激活：

- **审计和财务领域**：绘制资金流程、采购流程、报销流程、审批流程
- **内控文档**：业务流程图、控制活动图、SOP 流程图
- **系统设计**：业务流程梳理、数据流程图、系统集成图
- **流程标准化**：将口头/文字描述的可视化

**触发关键词**：
- 流程图、泳道图、审批流程、报销流程、采购流程
- 画图、可视化、绘制流程、生成图表
- 内控、SOP、工作流、业务流程
- draw.io、流程文档、流程设计

## 核心功能

### 1. 流程图生成

自动生成标准泳道流程图，包含：
- **泳道划分**：按责任部门/角色自动分组
- **节点类型**：处理节点、判断节点、开始/结束
- **连线标注**：分支条件（是/否）、流程路径
- **输出文档**：自动标注节点产出的单据/凭证

**内置主题**：
- "内控搭建"主题：浅蓝标题栏 + 白底黑框 + 红色开始/结束
- 支持自定义样式和主题

### 2. 节点数据结构

引擎接收结构化节点数据，格式如下：

```python
nodes_data = [
    {
        "id": "1",                       # 唯一标识
        "step": "提交付款申请\n（附单据）", # 步骤描述（\n 换行）
        "type": "process",               # process=矩形 | decision=菱形
        "swimlane_role": "采购部",        # 泳道（部门名）
        "node_role": "采购经办",          # 节点内角色标签
        "output_docs": "请款单",          # 输出文档（可选）
        "next_steps": [                  # 下游节点
            {"id": "2", "condition": ""}  # condition 空=普通流转
        ]
    },
    {
        "id": "2",
        "step": "金额>2000？",
        "type": "decision",
        "swimlane_role": "财务部",
        "node_role": "财务经理",
        "output_docs": "",
        "next_steps": [
            {"id": "3", "condition": "是"},
            {"id": "4", "condition": "否"}
        ]
    },
    {
        "id": "5",
        "step": "登记账簿",
        "type": "process",
        "swimlane_role": "财务部",
        "node_role": "会计",
        "output_docs": "",
        "next_steps": []  # 空列表=流程终点
    }
]
```

**解析规则**：
- 泳道：从描述中提取部门名（财务部、采购部、总经理等）
- 判断节点：含"是否/判断/大于/匹配"等关键词
- 开始/结束：自动生成，无需手动添加
- 分支条件：判断节点必须标注条件（是/否等）

### 3. 输出格式

- **.drawio**：可编辑的 XML 格式，支持后续修改
- **.png**：高清图片，scale=2.0 为推荐值
- **.svg**：矢量图，无损缩放
- **.vsdx**：Visio 格式，需 draw.io v26.0.16（见下方说明）

### 4. 样式自定义

```python
from engine import StyleManager

sm = StyleManager(theme_name="governance")

# 临时覆盖样式（不影响主题文件）
sm.override({
    'colors': {
        'decision': {'fill': '#FFA500'}  # 判断节点橙色
    },
    'edges': {
        'dashed_for_negative': True  # 否分支虚线
    }
})
```

### 5. 主题管理

```python
# 列出所有主题
sm.list_themes()

# 查看主题详情
sm.get_theme_info("governance")

# 保存自定义主题
sm.save_as_theme(
    name="我的主题",
    description="橙色判断节点，虚线否分支"
)

# 加载自定义主题
sm.load_theme("我的主题")
```

## 工作流程

```
用户描述 → AI 解析为节点数据 → 选择导出格式 → 引擎生成 .drawio → 渲染导出
```

**格式选择**：
- .drawio：可编辑源文件（始终生成）
- .png：高清图片（可选）
- .svg：矢量图（可选）
- .vsdx：Visio格式（可选，需要兼容版本）

**默认格式**：.drawio + .png（如用户未选择任何格式）

## 快速开始

### 交互流程

1. **解析用户描述**：将自然语言转换为结构化节点数据
2. **格式选择**：询问用户需要导出哪些格式（可多选）
3. **生成流程图**：生成 .drawio 文件
4. **导出渲染**：根据用户选择导出对应格式

### 格式选择交互

在生成流程图前，使用 `question` 工具询问用户：

```
请选择要导出的格式：
- ✓ .drawio（可编辑源文件，始终生成）
- □ .png（高清图片）
- □ .svg（矢量图）
- □ .vsdx（Visio格式）
```

**默认行为**：如用户未选择或取消，默认导出 .drawio 和 .png。

**注意事项**：
- .drawio 始终生成（可编辑源文件）
- .vsdx 需要 draw.io v26.0.16 或更低版本
- 选择多个格式会依次导出

### 完整示例

```python
import sys
sys.path.insert(0, "/path/to/flowchart-generator")
from engine import StyleManager, FlowchartBuilder, Renderer
from pathlib import Path

# 1. 定义流程节点
nodes_data = [
    {"id": "1", "step": "提交申请", "type": "process",
     "swimlane_role": "部门A", "node_role": "申请人",
     "output_docs": "申请单", "next_steps": [{"id": "2", "condition": ""}]},
    {"id": "2", "step": "部门经理审批", "type": "process",
     "swimlane_role": "部门A", "node_role": "部门经理",
     "output_docs": "", "next_steps": [{"id": "3", "condition": ""}]},
    {"id": "3", "step": "财务审核", "type": "process",
     "swimlane_role": "财务部", "node_role": "财务",
     "output_docs": "", "next_steps": [{"id": "4", "condition": ""}]},
    {"id": "4", "step": "出纳付款", "type": "process",
     "swimlane_role": "财务部", "node_role": "出纳",
     "output_docs": "付款凭证", "next_steps": []},
]

# 2. 格式选择（默认导出 .drawio + .png）
# 实际使用时由 AI 调用 question 工具询问用户
export_formats = ['png']  # 用户选择导出 PNG

# 3. 生成 .drawio（始终生成）
sm = StyleManager(theme_name="governance")
builder = FlowchartBuilder(style_manager=sm, sheet_name="费用报销流程", nodes_data=nodes_data)
xml = builder.generate_xml_content()
drawio_path = Path("费用报销.drawio")
drawio_path.write_text(xml, encoding="utf-8")

# 4. 根据用户选择导出对应格式
renderer = Renderer()

if 'png' in export_formats:
    renderer.export_to_png(drawio_path, Path("费用报销.png"), scale=2.0)

if 'svg' in export_formats:
    renderer.export_to_svg(drawio_path, Path("费用报销.svg"))

if 'vsdx' in export_formats:
    # VSDX 需要 draw.io v26.0.16 或更低版本
    renderer.export_to_vsdx(drawio_path, Path("费用报销.vsdx"), auto_install=True)

print(f"✓ 已生成 .drawio（始终生成）")
if export_formats:
    print(f"✓ 已导出: {', '.join(export_formats)}")
else:
    print("✓ 使用默认格式: .drawio + .png")
```

## Visio (VSDX) 导出说明

**重要**：draw.io v26.2.2 之后官方已移除 VSDX 导出功能。

### 自动安装（推荐）

智能检测版本，如不兼容则自动安装 v26.0.16：

```python
renderer.export_to_vsdx(
    Path("费用报销.drawio"),
    Path("费用报销.vsdx"),
    auto_install=True  # 自动安装兼容版本
)
```

**交互过程**：
1. 检测当前 draw.io 版本
2. 如果支持 VSDX，直接导出
3. 如果不支持，询问用户："检测到当前版本不支持 VSDX 导出。是否自动安装 draw.io v26.0.16（最后一个支持 VSDX 的版本）？[y/n]"
4. 用户确认后，自动下载并安装
5. 导出完成后禁用自动更新，防止版本升级

**支持平台**：
- ✅ macOS (Intel + Apple Silicon)
- ✅ Windows (x64)
- ✅ Linux (x64 + ARM64)

### 手动安装

如需手动控制安装流程：

**macOS**:
- Apple Silicon: https://github.com/jgraph/drawio-desktop/releases/download/v26.0.16/draw.io-arm64-26.0.16.dmg
- Intel: https://github.com/jgraph/drawio-desktop/releases/download/v26.0.16/draw.io-x86_64-26.0.16.dmg

**Windows**:
- https://github.com/jgraph/drawio-desktop/releases/download/v26.0.16/draw.io-26.0.16-windows-installer.exe

**Linux**:
- x64: https://github.com/jgraph/drawio-desktop/releases/download/v26.0.16/draw.io-amd64-26.0.16.deb
- ARM64: https://github.com/jgraph/drawio-desktop/releases/download/v26.0.16/draw.io-arm64-26.0.16.deb

**手动安装后配置**：
```python
# 禁用自动更新
import os
import json

config_path = Path.home() / "Library" / "Application Support" / "draw.io" / ".preferences"  # macOS
# Windows: Path(os.environ['APPDATA']) / 'draw.io' / '.preferences'
# Linux: Path.home() / '.config' / 'draw.io' / '.preferences'

config = {
    "checkForUpdates": False,
    "disableUpdate": True
}
with open(config_path, 'w') as f:
    json.dump(config, f)
```

### VSDX 导出回退策略

如果用户不需要 VSDX 导出，可以：
- 跳过 `export_to_vsdx` 调用
- 使用最新版本的 draw.io（PNG/SVG 效果更好）
- 使用在线版 app.diagrams.net 手动导出 VSDX

## 错误处理

### 常见问题

1. **draw.io 未安装**
   - 错误："未找到 draw.io 可执行文件"
   - 解决：https://github.com/jgraph/drawio-desktop/releases

2. **VSDX 导出失败**
   - 错误："导出的文件不是有效的VSDX格式"
   - 原因：使用了不支持的 draw.io 版本
   - 解决：设置 `auto_install=True` 或手动安装 v26.0.16

3. **节点数据验证失败**
   - 错误："数据校验警告"
   - 原因：缺少必填字段或格式错误
   - 解决：检查 id、step、type、swimlane_role、node_role 是否完整

4. **导出超时**
   - 错误："draw.io导出超时"
   - 原因：流程图过于复杂或 draw.io 响应慢
   - 解决：增加 timeout 参数（默认 60 秒）

## 健壮性设计

### 平台兼容性

- 自动检测操作系统（Windows/macOS/Linux）
- 自动识别架构（x86/ARM）
- 自动查找 draw.io 安装路径
- 支持多版本 draw.io 并存

### 边界处理

- 节点 ID 重复：自动去重
- 节点顺序错误：自动修复依赖关系
- 空流程图：生成最小可用的占位图
- 超长文本：自动换行或截断
- 中文路径：完整支持

### 版本兼容性

- VSDX 导出：自动检测版本并提供解决方案
- 样式兼容：新版本样式可降级兼容
- 主题兼容：自定义主题与内置主题兼容

## 扩展性

### 自定义主题

```python
# 保存新主题
sm.save_as_theme(
    name="审计专用",
    description="深色主题，高对比度"
)

# 加载自定义主题
sm2 = StyleManager(theme_name="审计专用")
```

### 扩展节点类型

如需添加新的节点类型（如子流程、调用、并行节点），需要修改 `flowchart_builder.py` 中的样式构建器和 XML 生成逻辑。

### 自定义布局参数

```python
# 调整间距和尺寸
sm.override({
    'layout': {
        'y_gap': 60,  # 行间距
        'node_width': 140,  # 节点宽度
        'swimlane_width': 300  # 泳道宽度
    }
})
```

## AI 调用流程

当用户描述一个业务流程时，按以下步骤执行：

1. **解析用户描述**，提取节点数据（节点数据结构见上方）
2. **调用 question 工具**询问格式：
    ```python
    question(questions=[{
        "question": "请选择要导出的格式（.drawio始终生成）：",
        "header": "格式选择",
        "options": [
            {"label": ".png（高清图片）", "description": "适合插入文档，高分辨率"},
            {"label": ".svg（矢量图）", "description": "无损缩放，适合网页和打印"},
            {"label": ".vsdx（Visio格式）", "description": "需 draw.io v26.0.16，兼容 Visio 2013+"}
        ],
        "multiple": True
    }])
    ```
3. **根据用户选择**执行导出（.drawio 始终生成）
4. 生成后读取 PNG 图片**检查布局**，确认无碰撞越界等问题

## 技术架构

详见 `references/architecture.md`：
- 引擎模块结构
- 布局算法详解
- 样式系统机制
- 错误处理策略
- 性能优化建议

## 注意事项

- 内置"内控搭建"主题对齐主流内控手册规范
- VSDX 是 Beta 功能，可能存在兼容性问题
- 导出后请在 Visio 2013+ 中打开测试
- 自动安装会禁用 draw.io 的自动更新
- 如遇格式错误，可尝试简化流程图后重新导出