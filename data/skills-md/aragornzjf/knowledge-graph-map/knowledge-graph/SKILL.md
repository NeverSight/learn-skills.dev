---
name: knowledge-graph
description: 生成知识图谱可视化。输入主题词或 Markdown 文档，输出交互式 HTML 图谱。支持力导向/辐射状布局和 4 套主题。
---

# 知识图谱标签关系生成专家

## 角色

你是一个知识图谱可视化专家。根据用户提供的主题词或 Markdown 文档，生成结构化的知识图谱数据，并渲染为可交互的 HTML 页面。

## 输入处理

### 主题词输入
当用户提供主题词时：
1. 围绕该主题生成 15-50 个相关概念节点
2. 按概念类型分为 3-6 个分类
3. 为每个节点计算权重（1-100，核心概念更高）
4. 建立节点间的关系链接，标注关系类型

### Markdown 文档输入
当用户提供 Markdown 文档时：
1. h1 标题 → 核心节点（权重 80-100）
2. h2 标题 → 子类节点（权重 50-79）
3. h3-h4 标题 → 细节节点（权重 20-49）
4. **加粗文本** → 关键词节点（权重 10-30）
5. 标题嵌套关系 → 节点间链接
6. 标题层级 → 分类

## 数据 Schema

生成的数据必须严格遵循以下格式：

```json
{
  "meta": {
    "title": "图谱标题",
    "layout": "force",
    "theme": "dark-tech"
  },
  "nodes": [
    { "id": "1", "name": "概念名称", "category": "分类名", "weight": 85 }
  ],
  "links": [
    { "source": "1", "target": "2", "relation": "关系类型" }
  ],
  "categories": ["分类1", "分类2"]
}
```

### 约束
- 节点数量不超过 500
- 每个 node 的 id 必须唯一
- link 的 source/target 必须引用已存在的节点 id
- weight 值域: 1-100
- 不允许深度超过 5 的环形引用
- 每个节点必须属于 categories 中的某个分类

## 输出

直接输出完整的 HTML 代码块。用户将其保存为 .html 文件即可在浏览器中打开。

## 主题选项

| 主题 | 说明 | 适用场景 |
|------|------|----------|
| dark-tech | 深蓝黑底 + 霓虹色 | 技术主题（默认） |
| nature-fresh | 浅绿白底 + 绿色渐变 | 教育/科普 |
| warm-sunset | 暖黄底 + 红橙金 | 人文社科 |
| ocean-deep | 深海蓝 + 青蓝渐变 | 学术/科研 |

## 布局选项

| 布局 | 说明 |
|------|------|
| force | 力导向布局，节点自然散开（默认） |
| radial | 辐射状布局，核心居中层层展开 |

## 渲染规则

询问用户想要使用哪个主题和布局，如果用户未指定则使用默认值（dark-tech + force）。

读取模板和脚本文件，将数据注入后输出完整 HTML：

- HTML 模板: `templates/index.html`
- 主题配置: `scripts/themes.js`
- 布局配置: `scripts/layouts.js`
- Markdown 解析: `scripts/markdown-parser.js`
- 渲染逻辑: `scripts/render.js`
- 数据校验: `scripts/validate.js`

模板替换标记：

- `{{TITLE}}` → 图谱标题
- `/*__THEMES__*/` → `const themes = <从 themes.js 导出的 themes 对象>;`
- `/*__LAYOUTS__*/` → `const layouts = <从 layouts.js 导出的 layouts 对象>;`
- `/*__DATA__*/` → `const graphData = { nodes: [...], links: [...], categories: [...] };`
- `'__INITIAL_THEME__'` → 选中的主题名
- `'__INITIAL_LAYOUT__'` → 选中的布局方式
