---
name: borehole-data-management
description: "钻孔数据管理与地层对比 (Mineral Geology & 3D Modeling). 从LAS（Log ASCII Standard）格式文件中读取测井曲线和井头信息，结合岩性解释结果构建Striplog地层剖面。LAS是石油工业标准的测井数据交. Use when user asks about 矿产地质与三维建模 tasks such as: 帮我加载这5口井的LAS文件，生成标准柱状图; 根据GR曲线特征辅助做地层对比; 计算各井的三维井眼轨迹. Core tools: striplog_read_las_well, striplog_read_las_well."
---

# 钻孔数据管理与地层对比

Category: **矿产地质与三维建模** / Mineral Geology & 3D Modeling | Match: **EXACT** | Skill ID: `07-01`

## When to Use

- 批量加载多口井的LAS文件并生成标准柱状图
- 根据测井曲线特征（如GR）辅助进行地层对比
- 计算各井的三维井眼轨迹
- 进行井间地层序列相似度分析

## Instructions
> **Tool calling**: The `_invoke_tool_http()` helper is defined in `scripts/call_tool.py`. Before executing any tool call code, run `exec(open("scripts/call_tool.py").read())` to make the function available.

### Step 1: 数据加载

读取LAS文件，检查曲线名和单位，统一不同来源曲线命名。

Call `_invoke_tool_http("striplog_read_las_well", {...})`:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filename` | str | Yes | LAS格式测井数据文件路径(.las) |
| `lexicon` | striplog.Lexicon | No | 地质术语词典对象，用于解析LAS文件中的岩性描述文本 |
| `legend` | striplog.Legend | No | 图例对象，用于将岩性编码映射为地层组分 |
| `field` | str | No | LAS文件中包含地层描述的字段名或曲线名 |
| `source` | str | No | 数据来源标注元信息 |

```python
well_data = _invoke_tool_http("striplog_read_las_well", {
    "filename": "/shared/geo-runtime-work/data/borehole.las",
    "lexicon": "Lexicon.default()",
    "legend": "<Legend object from previous step>",
    "field": "lithology",
    "source": "LAS_file"
})
# Output: Striplog地层剖面对象
```

确认用户已提供：
- LAS文件路径（支持多口井批量加载）
- 曲线命名规范（如有）
- 岩性图例定义（Legend对象）

### Step 2: 井斜校正

用Wellpathpy从井斜数据计算三维井眼轨迹坐标。

### Step 3: 柱状图生成

用Striplog生成含岩性/测井曲线的标准柱状图。

### Step 4: 地层对比

根据测井曲线特征（如高GR对应泥岩、低GR对应砂岩）辅助地层对比。

Call `_invoke_tool_http("striplog_read_las_well", {...})`:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `other` | striplog.Striplog | Yes | 用于对比的另一口井的Striplog地层剖面对象 |
| `attribute` | str | No | 用于对比的Component属性名称，如'lithology'按岩性对比，'formation'按地层组对比 |
| `metric` | str | No | 相似度度量方式：'jaccard'(Jaccard相似系数)、'cosine'(余弦相似度)等 |
| `step` | float | No | 对比的深度步长(m)，将两口井重采样到统一深度间隔后逐层比较 |

```python
correlation = _invoke_tool_http("striplog_read_las_well", {
    "other": "<Striplog from Well_B>",
    "attribute": "lithology",
    "metric": "jaccard",
    "step": 1.0
})
# Output: 地层对比结果（相似度、对应层段）
```

### Step 5: 多井剖面

将多口钻孔排列在一条剖面线上，标注地层对比线。

输出成果应包含：
- `borehole_log.png`：标准柱状图
- `cross_section.png`：多井对比剖面
- `trajectory.xyz`：三维井眼轨迹坐标
- 明确说明：自动地层对比基于序列相似度，结果需结合地质专家判断进行修正

## Examples

**Example 1: 批量加载5口井LAS文件**

```python
wells = []
for f in ["well_1.las", "well_2.las", "well_3.las", "well_4.las", "well_5.las"]:
    w = _invoke_tool_http("striplog_read_las_well", {
        "filename": f"/shared/geo-runtime-work/data/{f}",
        "field": "lithology"
    })
    wells.append(w)
```

**Example 2: 两口井地层对比**

```python
correlation = _invoke_tool_http("striplog_read_las_well", {
    "other": wells[1],  # Well_2
    "attribute": "lithology",
    "metric": "jaccard",
    "step": 0.5
})
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| LAS文件解析失败 | 检查文件编码（尝试encoding='latin-1'），确认LAS版本（1.2/2.0/3.0） |
| 不同井的曲线命名不一致 | 建立统一的曲线名映射表，在加载时进行重命名 |
| 岩性描述无法自动解析 | 自定义Lexicon词典，添加项目中使用的特定岩性术语 |
| 地层对比相似度低 | 检查两口井的深度基准是否一致（如MD vs TVD），调整step参数 |
| 井斜数据格式不兼容 | Wellpathpy支持多种井斜数据格式，需转换为目标格式后再计算轨迹 |
| 多井剖面排列不合理 | 确认井口坐标与剖面线方向的关系，必要时手动调整排列顺序 |
