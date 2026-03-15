---
name: psd-layer-reader
description: 读取并导出 Photoshop（.psd）图层树为 JSON，包含图层元信息（名称、类型、可见性、bbox）以及详细的文本样式信息。当用户需要分析 PSD 结构、查找特定图层（如弹窗、按钮）、或准备 HTML/CSS 还原所需的数据时，务必使用此技能。即使涉及复杂的嵌套结构或需要精确的文本还原（字体、颜色、间距），此工具也能提供结构化的支撑。
---

# PSD 图层读取器

## 概览
将 PSD 图层树导出为 JSON，可按图层名过滤，仅返回匹配分支。此技能特别适用于将设计稿转化为代码的前期调研阶段，能够快速定位图层、获取坐标和样式。

## 工作流

### 1) 安装依赖（每个环境仅需一次）
```bash
py -3 -m pip install psd-tools
```

### 2) 导出完整图层树 (JSON)
```bash
py -3 -X utf8 scripts/psd_layers.py "path/to/file.psd" --output "psd_layers.json"
```

### 3) 仅导出匹配分支（精确匹配）
```bash
py -3 -X utf8 scripts/psd_layers.py "path/to/file.psd" --name "rule-modal" --output "rule_modal.json"
```

### 4) 仅导出匹配分支（包含匹配）
```bash
py -3 -X utf8 scripts/psd_layers.py "path/to/file.psd" --name "modal" --match contains --output "modal.json"
```

## 输出格式 (JSON)
每个节点包含以下关键字段：
- `name` (字符串): **安全名称**。经过规范化，去除了特殊字符，确保可直接用于变量名或文件名。
- `originalName` (字符串): **原始图层名**。保留 PSD 中的真实名称，用于追溯和调试。
- `layerId` (整数): PSD 内部的唯一 ID，用于消歧。
- `kind` (字符串): 图层类型（如 `group`, `type`, `pixel`）。
- `visible` (布尔值): 是否可见。
- `bbox` ([x1, y1, x2, y2]): 图层边界框坐标。
- `layoutTag` (字符串|null): 从图层名提取的布局标记（如 `flow-y`, `fixed`）。如果图层名为 `[flow-y] content`，则 `layoutTag` 为 `flow-y`。
- `textInfo` (对象|null): 仅针对文本图层 (`kind == 'type'`)。
    - `text`: 完整文本内容。
    - `runs`: 包含不同样式的文本分段列表。
    - `fontSize`, `color`, `fontName`, `leading` 等：首段文本的样式摘要。
- `children` (数组): 子节点列表。

## 最佳实践与提示
- **名称冲突处理**: 如果 PSD 中存在重名图层，`name` 字段会自动附加 `layerId`（如 `button-123`）以确保 JSON 结构的唯一性。
- **布局还原**: 在还原 HTML 时，优先参考 `layoutTag`。带有 `[flow-y]` 或 `[flow-x]` 标记的图层通常对应 Flex 布局。
- **文本提取**: 如果发现文本颜色或大小不准，请检查 `textInfo.runs`。复杂的文本图层可能在同一行内包含多种样式。
- **编码处理**: 在 Windows 下运行脚本时，务必带上 `-X utf8` 参数，否则处理中文图层名可能会报错。

## 资源
- `scripts/psd_layers.py`: PSD 图层树导出核心脚本。支持 `--verbose` 查看转换详情。
- `scripts/layer_parser.py`: 图层信息解析逻辑。
- `references/PSD_TOOLS_TEXT_EXTRACTION_EXAMPLES.md`: psd-tools 文字图层提取技术参考。
