---
name: article-producer
description: 一站式文章创作流水线，一键产出可发布稿件（大齐风格）；触发词：文章创作流程、文章一键产出、写文章（全流程）
---

# 文章创作全流程 (article-producer)

## 核心目标
将原始素材（Source）通过“分析、策划、撰写、打磨”四个阶段，转化为 3 篇具有“大齐”风格、洞察深刻且已排版优化的成品文章。

## 目录与文件规范
所有产物必须存储在 `posts/YYYY/MM/DD/[slug]/` 目录下。`[slug]` 需根据素材核心主题提取关键词（英文小写 + 连字符）。

### 文件命名清单：
- `source-1.md`, `source-2.md`... (原始素材)
- `analysis.md` (深度分析报告)
- `outline-a/b/c.md` (三套差异化提纲)
- `article-a/b/c.md` (最终润色后的成稿)

## 执行流水线 (Pipeline)

### 1. 初始化与分析 (Initialize & Analyze)
- **动作**：创建目录并保存素材。
- **调用**：使用 `article-analyzer` 分析素材。
- **产物**：保存分析结果至 `analysis.md`。

### 2. 多维度策划 (Multi-angle Outlining)
- **动作**：基于分析报告，构思 3 个不同的写作方向。
- **调用**：使用 `article-outliner` 生成三套大纲。要求：
  - **方案 A**：理性分析，侧重行业趋势与逻辑推演。
  - **方案 B**：实操指南，侧重于“手把手”教读者如何应用。
  - **方案 C**：争议思辨，侧重于挑战常规认知或探讨伦理/安全风险。
- **产物**：保存至 `outline-a.md`, `outline-b.md`, `outline-c.md`。

### 3. “大齐”风格撰写 (Daqi-style Writing)
- **动作**：模拟大齐的口吻，将 3 套大纲转化为初稿。
- **调用**：使用 `article-writer`。
- **核心要求**：
  - 加比喻，避说教，去“AI 味”（禁用“综上所述”、“首先其次”等）。
  - 段落短小，适合移动端阅读。
- **产物**：保存至 `article-a.md`, `article-b.md`, `article-c.md`。

### 4. 深度打磨 (Global Polishing)
- **动作**：对 3 篇稿件进行最后的质量把关。
- **调用**：使用 `article-polish`。
- **规范检查**：
  - 强制执行中英文空格标准。
  - 修正全角/半角标点符号。
  - 检查术语统一性。
- **产物**：覆盖更新 `article-a.md`, `article-b.md`, `article-c.md`。

## 使用须知
- **不可简化流程**：中间产物（analysis/outline）是评估成稿质量的重要依据。
- **自动触发条件**：当用户提供资料并要求“写篇文章”、“走流程”或显式提及本技能时。
