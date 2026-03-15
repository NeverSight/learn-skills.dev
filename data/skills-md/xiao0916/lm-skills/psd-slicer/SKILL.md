---
name: psd-slicer
description: 将 Photoshop（.psd）文件的所有图层导出为独立的 PNG 图片。适用于从 PSD 文件提取图层图片、为网页开发生成切片、或为其他工具准备图层资源。自动处理图层命名、跳过不可见图层、递归导出嵌套图层组。
---

# PSD 切片导出器

## 核心功能

自动将 PSD 文件的可见图层导出为独立 PNG 图片，支持灵活过滤和命名验证。

**特性**：

- ✅ 强制命名合法性检查（支持 `[a-zA-Z0-9_-]` 及布局标签 `[tag]`）
- ✅ 自动处理布局标签（如 `[flow-y]layout` 自动导出为 `layout.png`）
- ✅ 递归处理嵌套图层组
- ✅ 自动处理重名冲突（带有 `layer_id` 级别防抖防词覆盖机制）
- ✅ 支持按组/前缀过滤
- ✅ 跳过不可见/空白图层
- ✅ 默认无需配置即可支持导出中文、日文等非 ASCII 图层命名
- ✅ 支持智能匹配同目录下 JSON 结构文件，或通过 `--auto-rename` 转化为通用切块命名

## 使用方式

### 基础命令

```bash
# 导出所有合法命名的图层
py -3 scripts/export_slices.py --psd design.psd

# 自定义输出目录
py -3 scripts/export_slices.py --psd design.psd -o assets/layers

# 仅导出图层组（跳过单个图层）
py -3 scripts/export_slices.py --psd design.psd -g

# 按前缀过滤（如：slice-button）
py -3 scripts/export_slices.py --psd design.psd -p slice-

# 组合使用
py -3 scripts/export_slices.py --psd design.psd -o ./comps/ -g -p component-
```

### 参数说明

| 参数                    | 短参 | 说明                                  |
| ----------------------- | ---- | ------------------------------------- |
| `--output`              | `-o` | 输出目录（默认：`images/`）           |
| `--groups-only`         | `-g` | 仅导出图层组                          |
| `--prefix`              | `-p` | 前缀过滤（如：`slice-`）              |
| `--strict-naming`       | `-s` | 强制进行命名合法性校验（不合法的名字会被跳过） |
| `--auto-rename`         | 无   | 未命中映射时自动重命名图层为 `layer-xxx` 或 `group-xxx` |
| `--mapping-json`        | `-m` | 显式指定 JSON 映射文件路径。若不填且所在工作目录存在同名或 `layer-tree.json` 等文件将自动匹配。|
| `--skip-type`          | 无   | 跳过文本图层（`kind == 'type'`）      |

## 何时使用名称映射与自动命名

**默认行为：**
现在可以不作任何处理，默认即可直接将含有中文字符的图层导出。当遇到重复中文名称（如都在根组件下叫 `背景`），现在会使用其独立的 `layer_id` 进行关联防重（例如 `背景_13.png` 和 `背景_14.png`），避免了由于 `_1` 这种简单的重叠导致的字典含义丢失。

**推荐使用 `--mapping-json` 参数或让其自动匹配：**
当有 `psd-layer-reader` 处理过的标准结构需要对应时，由于它处理过了树形关系，并且把特殊的布局标签 `[tag]` 也作了统一管理，能够达到切图命名和 JSON 中的 `name` 完全一一对应的效果，这对后续页面生成尤为关键。如果没有带上 `-m` 参数，本工具也会**自动在 PSD 所在目录寻找映射文件**（优先级：`[PSD同名文件].json` > `layer-tree.json` > `psd_layers.json`）。

**使用 `--auto-rename`：**
如果您不需要原设计中乱七八糟没有规范的图层名称，而是想统一直接转化为 `layer-xxx` 的无语义形式供其他引擎或预览体系使用，您可以直接使用 `--auto-rename` 参数使没能被匹配到的图层统统转化其名称。

### 技术实现

**映射关系**:

- PSD 中的 `layer.name` 返回原始名称（可能是中文）
- JSON 中的 `originalName` 保存相同的原始名称
- JSON 中的 `name` 是规范化后的合法文件名
- 映射表结构: `{layer.name: name}` 即 `{原始名称: 规范化名称}`

**工作流程**:

1. 使用 `psd-layer-reader` 分析 PSD 结构并生成 JSON
2. 检查 JSON 中的 `originalName` 和 `name` 映射关系
3. 使用 `psd-slicer` 的 `--mapping-json` 参数导出图层

**示例**:

```bash
# 步骤 1: 生成 JSON 映射
py -3 .claude/skills/psd-layer-reader/scripts/psd_layers.py design.psd -o layer-tree.json

# 步骤 2: 使用映射导出
py -3 .claude/skills/psd-slicer/scripts/export_slices.py --psd design.psd --mapping-json layer-tree.json -o assets/
```

**注意事项**:

- 确保 JSON 文件和 PSD 文件对应同一设计稿（版本必须同步）
- 如果 PSD 被修改，必须重新生成 JSON 文件
- 映射功能会自动处理嵌套的图层组（递归遍历 children）
- 如果图层在 JSON 中找不到映射且名称不合法，会被跳过并输出警告
- 映射匹配使用 PSD 的 `layer.name` 作为查找键

### 实战案例：share-modal.psd

**完整工作流**（含中文图层导出）：

```bash
# 步骤 1: 创建输出目录并生成 JSON 映射
py -3 .claude/skills/psd-layer-reader/scripts/psd_layers.py \
  --psd assets/share-modal.psd \
  --output verify-flow/verify-010/layer-tree.json

# 步骤 2: 使用映射导出中文图层
py -3 .claude/skills/psd-slicer/scripts/export_slices.py \
  --psd assets/share-modal.psd \
  --output verify-flow/verify-010/sliced-images \
  --mapping-json verify-flow/verify-010/layer-tree.json
```

**实际输出示例**：

```
Loaded 177 name mappings
Mapped '背景' -> 'layer-npdngy.png'
Exported Layer: layer-npdngy.png
Mapped '图层 1' -> 'layer-9dgwjr.png'
Exported Layer: layer-9dgwjr.png
Mapped '唱片' -> 'group-9bi971.png'
Exported Group: group-9bi971.png
...
Done! Exported to: verify-flow/verify-010/sliced-images
```

**常见警告处理**：

1. **重复名称警告**（正常现象）：

   ```
   Warning: Duplicate originalName '唱片'
   Warning: Duplicate originalName '雨滴'
   ```

   这是因为 PSD 中存在同名图层，系统会自动添加 `_1`、`_2` 后缀区分。

2. **图层效果警告**（需安装依赖）：
   ```
   Warning: Could not export '活动规则': Layer effects require: scikit-image
   ```
   **解决方案**：
   ```bash
   pip install scikit-image
   # 或
   pip install 'psd-tools[composite]'
   ```

**导出统计示例**：

- 总图层映射：177 个
- 成功导出：126 个图层（31 个组 + 95 个图片）
- 带图层效果需额外依赖：约 10 个（如"活动规则"、"SLOGAN"、"标题"等）

### 排除文本图层

如果您计划在 HTML 中使用真实的文本（而不是图片），请使用 `--skip-type` 参数：

```bash
py -3 scripts/export_slices.py --psd design.psd --skip-type
```

配合 `psd-json-preview` 的 `--include-text` 参数，可以实现设计稿文字的完美还原。

### 向后兼容

- 废弃了 `--allow-illegal-names`（但传入不再引发崩溃，空执行），取而代之的是，现在脚本默认直接放行中文及特殊名称。如果需要强一致校验，必须明确传入 `--strict-naming` 或 `-s`。
- 如果图层找不到映射且当前目录也未存在合适的 JSON 文件，则以当前的名称导出；除非开启了 `--auto-rename` 它会被自动清洗转换。

## 命名规则

**合法✅**：`button`、`btn-primary`、`[flow-y]layout`（自动剥离标签）、`[abs]icon`
**非法❌**：`按钮`（中文）、`Button<>`（特殊字符）

**规则**：默认仅导出符合 `[a-zA-Z0-9_-]` 的图层。若图层名以 `[tag]name` 形式命名，系统将自动识别并剥离标签，提取 `name` 作为文件名，确保文件系统兼容性。

## 依赖说明

### 必需依赖

- `psd-tools`: PSD 文件解析核心库

### 可选依赖

- `scikit-image`: 用于导出包含图层效果的元素（如阴影、发光、渐变等）

### 手动安装命令

```bash
# 安装依赖
py -3 -m pip install psd-tools
py -3 -m pip install scikit-image
```

**注意**：当前脚本在检测到缺少依赖时只会打印警告，不会自动安装。建议使用 `psd-to-preview` 技能的预检查功能，让 AI 在执行前检查并安装依赖。

## 常见场景

- **网页开发**：提取设计元素为 HTML/CSS 资源
- **组件导出**：使用 `-g -p component-` 导出标记的组件
- **预览生成**：为 psd-json-preview 技能准备切片图片
- **设计交付**：批量导出设计文件的所有图层

### 快速参考

| 用户关键词              | AI 应执行                                      |
| ----------------------- | ---------------------------------------------- |
| "中文图层" / "中文命名" | 默认即可直接满足。为了与代码生成相性好，依然推荐先执行 JSON 提取生成结构以被切图器自动应用。|
| "统一重命名" / "转ID化" | 使用 `--auto-rename` 参数                     |
| "只导出组" / "图层组"   | 使用 `-g` / `--groups-only` 参数               |
| "icon-" 开头            | 使用 `-p icon-` 参数                           |
| "严格名称检查"          | 使用 `-s` / `--strict-naming` 参数             |
| "保存到 xxx"            | 使用 `-o xxx` 参数                             |
| "不导出文字" / "文字转代码" | 使用 `--skip-type` 参数                       |

---

## 资源文件

- **scripts/export_slices.py** - 核心导出脚本（219行）
