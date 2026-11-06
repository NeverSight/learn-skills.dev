---
name: nice-lark-doc
description: >
  美化飞书文档排版，通过 6 种风格配方（Recipe）智能匹配，生成结构清晰、视觉专业的飞书文档。
  支持画板（SVG/Mermaid）、表格、Callout、Grid 等富视觉元素。
  Use when：创建新飞书文档并希望排版美观、美化/优化现有文档视觉和结构、
  将素材整理为专业文档、为技术方案/产品文档/会议纪要生成配套画板。
  触发词：美化飞书文档、nice doc、漂亮文档、飞书排版、写一份好看的文档、
  文档排版、lark doc 美化、文档视觉优化、专业文档、文档设计。
---

# Nice Lark Doc

## 前置检查

首次使用：`bash scripts/setup.sh`（安装 lark-cli + 飞书 skill + auth 授权）。详见 `references/setup-guide.md`。

## 核心原则

**文字墙是头号敌人。** 连续纯文本 ≤ 3 段，第 4 段前必须插入视觉元素。

| 规则 | 说明 |
|---|---|
| 3 段打断 | 连续纯文本不得超过 3 段 |
| 画板优先 | 架构、流程、关系、对比 → 画板，而非段落 |
| 视觉节奏 | 画板、表格、Callout 均匀分布，不扎堆 |
| 多画板策略 | 每个画板聚焦一个主题，不塞一张大图 |

### 画板双路径

| 路径 | 适用 | 标签 |
|---|---|---|
| **Mermaid** | 思维导图、时序图、类图、饼图、甘特图 | `<whiteboard type="mermaid">` |
| **SVG** | 架构图、流程图、关系图、自定义图形 | `<whiteboard type="svg">` |

SVG 路径核心心智：打破矩形牢笼，大胆使用色彩、渐变、阴影。画板会解析 SVG 为可编辑节点。

**对比度铁律**（最高优先级）：
- 深色底（#4A6FA5 及更深）→ 白色文字 `#FFFFFF`
- 浅色底（#60A0E0 及更浅）→ 深色文字 `#1E293B`
- ❌ 禁止：浅色背景 + 白色文字
- 生成 SVG 前必须对照 `references/color-palette.md` 速查表

## 工作流

### Phase 1：理解意图

1. 新建 or 美化现有文档？
2. 文档 URL（美化）或内容来源（新建）
3. 受众和场景？（一个问题即可）

### Phase 2：评估与配方匹配

**5 维度评分**（1-5 分）：

| 维度 | 1 分 | 5 分 |
|---|---|---|
| 结构复杂度 | 单页通知 | 多章节技术报告 |
| 数据密度 | 纯叙述 | 数据对比密集 |
| 视觉需求 | 纯文字 | 每节需配图 |
| 行动导向 | 阅读思考 | 执行清单 |
| 正式程度 | 内部随手记 | 对外正式文档 |

**配方匹配逻辑**：
- 从 `references/recipe-index.json` 匹配候选
- 单一 Recipe 明显领先（≥ 3 维度最高 且 总分高 ≥ 3）→ 自动应用，交付时注明理由
- 得分接近（差值 ≤ 2）或类型模糊 → 展示 3 个候选让用户选

| Recipe | 风格 | 最佳场景 |
|---|---|---|
| 素雅编辑 | 安静、克制、长文 | 深度分析、研究报告 |
| 技术严谨 | 结构化、编号、mermaid | 技术方案、架构设计 |
| 产品叙事 | 视觉化、用户故事 | 产品方案、需求评审 |
| 行动导向 | 紧凑、checkbox、待办 | 会议纪要、Sprint 计划 |
| 数据密集 | 表格主导、对比清晰 | 复盘报告、竞品分析 |
| 演示风格 | 大留白、视觉冲击 | 对外演示、品牌介绍 |

### Phase 3：内容创作

1. 加载 Recipe 文件（`references/recipes/{slug}.md`）
2. 按 Recipe 规则组织内容：
   - 标题体例（编号、层级）
   - 段落规则（句数限制）
   - 每 3 段纯文本后插入视觉元素
   - 画板：标准图表 → Mermaid；自定义/品牌化 → SVG（可启动 SubAgent 并行）
   - Callout 按语义色（详见 `references/reference-gallery.md` 的四色系统）
   - 可视化转译：段落描述 → 画板或表格
3. 产出前对照 `references/quality-checklist.md` 自检

### Phase 4：渲染到飞书

通过 lark-doc skill 的 `docs +create` / `docs +update` 写入文档。画板通过 `<whiteboard>` 标签嵌入。

- 多个独立 SVG 画板 → SubAgent 并行生成
- 插入后导出 PNG 预览审查，不满意则修改重插
- 渲染细节（SDK 选择、分页、错误恢复）见 `references/delivery-templates.md`
- 画板详细接入见 `references/whiteboard-bridge.md`

### Phase 5：交付确认

1. 展示文档链接
2. 输出设计决策摘要 + 画板审查记录 + 质量自评卡（模板见 `references/delivery-templates.md`）
3. 提示可微调：「太密/太松/换风格/画板重做，告诉我」

## 美化现有文档

用户提供文档 URL 时的差异流程：

```
lark-doc 读取内容 → Phase 2 评分（识别问题）→ 展示诊断报告
→ 匹配 Recipe → Phase 3 改写（不删减原文信息）
→ Phase 4 渲染（新建保留原稿 or 覆盖）→ Phase 5 交付
```

诊断报告关注：标题层次、文字墙、数据对比是否用表格、关键约束是否有 Callout、视觉元素占比。

## 参考文件

| 文件 | 说明 |
|---|---|
| `references/recipe-index.json` | Recipe 索引与元数据 |
| `references/recipes/*.md` | 6 种 Recipe 详细规则 |
| `references/blocks-mapping.md` | 设计规则 → blocks API 映射 |
| `references/whiteboard-bridge.md` | 画板渲染接入指南 |
| `references/color-palette.md` | 配色系统（对比度规则 + 主题 + 渐变） |
| `references/quality-checklist.md` | 质量自检清单 |
| `references/reference-gallery.md` | 优秀文档参考库（风格模式 + 配色范例） |
| `references/flowchart-theme.md` | 流程图主题规范（Rail Release 风格） |
| `references/delivery-templates.md` | 交付模板、SDK 细节、错误恢复 |
| `references/setup-guide.md` | 环境设置指南 |
