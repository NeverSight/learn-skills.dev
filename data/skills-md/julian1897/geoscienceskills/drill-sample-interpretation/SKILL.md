---
name: drill-sample-interpretation
description: "钻孔样品数据解释 (Geochemistry & Mineral Exploration). 根据多口钻孔的岩性编录和井口坐标数据，绘制连井地质剖面图（drill section / cross section）。将多口钻孔沿剖面线排列，在钻孔之间通过地. Use when user asks about 地球化学与矿产勘查 tasks such as: 帮我整理这口钻孔的数据，做柱状图并圈定Cu品位>0.3%的矿体; 绘制Au品位随深度的变化曲线; 用这3口钻孔做地层对比剖面. Core tools: ogp_drill_section, ogp_drill_section."
---

# 钻孔样品数据解释

Category: **地球化学与矿产勘查** / Geochemistry & Mineral Exploration | Match: **EXACT** | Skill ID: `06-06`

## When to Use

- 整理单口钻孔数据，制作柱状图并圈定矿体
- 绘制元素含量（如Au、Cu品位）随深度的变化曲线
- 多口钻孔地层对比，绘制连井地质剖面图
- 按边界品位圈定矿体段，计算矿体厚度和平均品位

## Instructions
> **Tool calling**: The `_invoke_tool_http()` helper is defined in `scripts/call_tool.py`. Before executing any tool call code, run `exec(open("scripts/call_tool.py").read())` to make the function available.

### Step 1: 数据整理

加载钻孔数据，检查深度连续性，建立三维坐标。

确认用户已提供：
- 钻孔数据文件（包含岩性编录、品位数据）
- 井口坐标信息
- 目标元素和边界品位（如Cu>0.2%）

### Step 2: 柱状图生成

用Striplog生成标准钻孔柱状图（岩性+品位曲线）。

Call `_invoke_tool_http("ogp_drill_section", {...})`:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `legend` | striplog.Legend | No | 图例对象，定义各岩性的显示颜色和填充图案。若不提供则使用默认颜色方案 |
| `width` | float | No | 柱状图宽度（英寸） |
| `aspect` | float | No | 图形纵横比，控制柱状图的高度与宽度比例 |
| `interval_label` | str | No | 区间标注显示的Component属性名（如'lithology'），在每个区间旁标注岩性名称 |
| `ax` | matplotlib.axes.Axes | No | 目标matplotlib Axes对象，用于将柱状图嵌入已有的多子图布局中 |

```python
log_plot = _invoke_tool_http("ogp_drill_section", {
    "legend": "<Legend object from previous step>",
    "width": 1.5,
    "aspect": 10,
    "interval_label": "formation",
    "match_only": "lithology"
})
# Output: 钻孔柱状图
```

### Step 3: 矿体圈定

按边界品位（如Cu>0.2%）圈定矿体段，计算矿体厚度和平均品位。

- 边界品位仅作为技术筛选参数，不直接等同于经济可采边界
- 输出矿体见矿段信息（深度、厚度、平均品位）

### Step 4: 地化剖面

绘制元素含量随深度变化曲线，识别矿化富集段。

### Step 5: 多孔对比

按地层对比多口钻孔，绘制连井地质剖面图。

Call `_invoke_tool_http("ogp_drill_section", {...})`:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `boreholes` | str | Yes | 钻孔数据CSV文件路径（含井口坐标和岩性编录） |
| `correlation_lines` | array | No | 地层对比线定义，连接同一地层层位 |
| `vertical_exaggeration` | float | No | 垂直放大比例，用于强调地层垂向细节，典型值5-50 |
| `equal_spacing` | bool | No | 是否等间距排列钻孔（True）或按实际水平距离排列（False） |
| `figsize` | tuple | No | 图形尺寸(宽, 高)，单位英寸 |
| `color_map` | dict | No | 岩性到填充颜色的映射字典 |

```python
section = _invoke_tool_http("ogp_drill_section", {
    "boreholes": "/shared/geo-runtime-work/data/boreholes.csv",
    "correlation_lines": [],
    "vertical_exaggeration": 10.0,
    "equal_spacing": false,
    "figsize": [16, 8],
    "color_map": {}
})
# Output: 连井地质剖面图
```

### Step 6: 报告成果

输出成果应包含：
- `borehole_log.png`：钻孔柱状图
- `ore_intercepts.csv`：矿体见矿段信息（深度、厚度、平均品位）
- `cross_section.png`：多孔对比剖面
- 明确说明：边界品位仅为技术筛选参数，矿体圈定结果不直接等同于经济可采边界

## Examples

**Example 1: 单孔柱状图与矿体圈定**

```python
# Step 2: 生成柱状图
log = _invoke_tool_http("ogp_drill_section", {
    "legend": "<Legend>",
    "width": 1.5,
    "aspect": 10,
    "interval_label": "lithology"
})

# Step 3: 按Cu品位>0.3%圈定矿体
# (品位筛选逻辑由用户指定边界品位)
```

**Example 2: 三口钻孔地层对比剖面**

```python
section = _invoke_tool_http("ogp_drill_section", {
    "boreholes": "/shared/geo-runtime-work/data/three_boreholes.csv",
    "correlation_lines": [],
    "vertical_exaggeration": 15.0,
    "equal_spacing": false,
    "figsize": [20, 8]
})
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 钻孔深度不连续 | 检查原始数据缺失段，标记缺口位置，必要时进行插补或标注 |
| 岩性编码不统一 | 统一不同来源的岩性命名（如"砂岩"/"sandstone"映射为同一编码） |
| 矿体圈定结果与地质认识不符 | 检查边界品位设置是否合理，结合地质背景综合判断，不可仅依赖数值筛选 |
| 多孔对比时地层无法对应 | 确认各孔使用统一的地层命名体系，可借助标志层（特征性岩层）辅助对比 |
| 柱状图岩性填充图案缺失 | 检查Legend对象是否包含对应岩性的定义，补充缺失的图例项 |
| 垂直放大比例不合适 | 调整vertical_exaggeration参数，典型值5-50，根据地层厚度选择 |
