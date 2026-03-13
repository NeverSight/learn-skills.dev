---
name: ljg-the-one
description: Extracts the essential formula (The One) from books, concepts, or ideas using first-principles thinking, then falsifies it by identifying boundary conditions. Generates a visual HTML card. Use for quick single-formula essence extraction. For deep multi-round book analysis, use ljg-xray-book instead. Do NOT use for academic papers (use ljg-xray-paper).
---

## 约束

本 skill 输出为 HTML 文件（浏览器渲染），不适用 L0 中的 Org-mode、Denote 和 ASCII-only 规范。

# LJG-The-One: 本质提取器

The Many (表象) → The One (本质) → The Formula (最小符号表达)

## 执行步骤

### 步骤 1：接收输入

书、概念、文章 URL、一句话、一个道理。

### 步骤 2：解构 → 升维 → 形式化

1. **解构**: 剥离噪音 → 识别核心矛盾与动力机制 → 提取关键要素
2. **升维**: 发现高维模型 → 要素转化为变量 → 建立关系符号
3. **形式化**: 提炼 The One 公式（不超过 5 个变量）→ 每个变量清晰解释

### 步骤 3：证伪

找到公式的边界条件（至少 2-3 个）：
- 哪个变量在什么条件下失去意义
- 边界要真实、尖锐，不是"极端情况下不成立"这种废话

### 步骤 4：情感基调 → 自适应配色

根据核心情感基调，从 `assets/theme-map.json` 读取匹配的色系。

色系映射表概览：

| 情感基调 | 关键词示例 |
|---------|----------|
| 警示/危机 | 风险、陷阱、负面、警告 |
| 成长/生机 | 学习、进化、希望、复利 |
| 智慧/洞察 | 哲学、认知、深度、道 |
| 财富/价值 | 商业、投资、价值、市场 |
| 平衡/和谐 | 系统、平衡、中庸、稳态 |
| 力量/突破 | 变革、颠覆、突破、破坏 |
| 沉稳/经典 | 经典、永恒、真理、传统 |

用 theme-map.json 中的颜色值填充 HTML 模板的配色槽位。

### 步骤 5：生成可视化卡片

1. 读取模版 `assets/template.html`
2. 填充内容槽位：

| 槽位 | 说明 |
|-----|------|
| `{{TITLE}}` | 卡片标题 |
| `{{HEADER_ICON}}` | 头部图标 |
| `{{ORIGIN}}` / `{{ORIGIN_ICON}}` | 来源描述 / 图标 |
| `{{PHENOMENON}}` / `{{PHENOMENON_ICON}}` | 表象（用 `<span class="highlight">` 高亮）/ 图标 |
| `{{CORE_LOGIC}}` / `{{LOGIC_ICON}}` | 核心逻辑 / 图标 |
| `{{FORMULA}}` | The One 公式 |
| `{{FORMULA_VARS}}` | 变量列表 `<li><span class="var-symbol">X</span><span class="var-name">Name</span><span>描述</span></li>` |
| `{{MERMAID_DIAGRAM}}` | Mermaid 流程图代码 |
| `{{BOUNDARY_ICON}}` / `{{BOUNDARY_TITLE}}` | 边界图标 / 标题 |
| `{{BOUNDARY_ITEMS}}` | 边界条目 `<div class="boundary-item">` 含 condition + reason |
| 配色槽位 | `{{THEME_PRIMARY}}` `{{THEME_SECONDARY}}` `{{THEME_GLOW}}` 等，从 theme-map.json 填充 |

3. 写入 `/tmp/essence-card-{概念名称}.html`
4. 执行 `open /tmp/essence-card-{概念名称}.html`

## 输出质量标准

- **公式极简**: 不超过 5 个变量
- **边界尖锐**: 具体失效条件，不说废话
- **解释清晰**: 每个变量有明确现实对应物
- **配色匹配**: 主题色系与情感基调一致
