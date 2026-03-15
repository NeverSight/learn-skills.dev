---
name: pptx
description: "只要任务与 .pptx 有关（输入、输出或两者都有），就应触发本技能。包括：创建演示文稿、读取提取内容、修改现有模板、合并拆分页面、处理版式/讲稿/批注等。用户提到 deck/slides/presentation 或具体 .pptx 文件时，即便最终用途是摘要或邮件，也应使用本技能。"
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX 技能

## 快速参考

| 任务 | 指引 |
|------|------|
| 读取/分析内容 | `python -m markitdown presentation.pptx` |
| 在现有模板上编辑 | 先读 [editing.md](editing.md) |
| 从零创建新稿 | 先读 [pptxgenjs.md](pptxgenjs.md) |

---

## 读取内容

```bash
# 文本抽取
python -m markitdown presentation.pptx

# 幻灯片缩略图总览
python scripts/thumbnail.py presentation.pptx

# 原始 XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## 编辑工作流

完整细节在 [editing.md](editing.md)。默认执行顺序：

1. 用 `thumbnail.py` 先理解模板结构与视觉密度
2. `unpack -> 调整页面结构/对象 -> 内容替换 -> clean -> pack`
3. 出图后做人眼 QA，再回改

---

## 从零创建

完整约束在 [pptxgenjs.md](pptxgenjs.md)。  
没有模板且用户要全新设计时，按该文档执行。

---

## 设计原则（必须避免“流水线 AI 幻灯片”）

### 开始前

- 先选“有主题感”的配色，不要默认蓝白模板
- 视觉权重遵循 60/30/10（主色/辅色/强调）
- 统一视觉母题（例如圆角卡片、图标圆章、单侧粗边）并贯穿全稿

### 版式与信息组织

每页至少有一个视觉锚点（图、图标、图表、几何块），不要纯文字页。

常用结构：

- 左文右图双栏
- 图标 + 标题 + 描述条目
- 2x2/2x3 卡片网格
- 半屏大图 + 信息覆盖

数据展示建议：

- 大数字 KPI（60-72pt）
- 对比列（before/after、方案 A/B）
- 时间线或流程箭头

### 排版与间距

- 标题 36-44pt，正文 14-16pt，说明 10-12pt
- 最小页边距 0.5"
- 区块间距统一 0.3"-0.5"

### 常见反模式（禁止）

- 每页都同一版式
- 正文居中排（正文与列表应左对齐）
- 字号层级不明显
- 低对比文本或低对比图标
- 只做“标题 + 子弹点”
- 用标题下划线装饰（典型 AI 痕迹）

---

## QA（强制步骤）

默认假设首版一定有问题，目标是“找 bug”，不是“证明没问题”。

### 内容 QA

```bash
python -m markitdown output.pptx
```

检查：

- 内容缺失、错别字、顺序错误
- 模板残留占位词（如 `xxxx`、`lorem ipsum`）

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

### 视觉 QA（建议用子代理或独立视角）

先转图片再审：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

重点检查：

- 重叠、穿插、截断
- 过密间距与对齐漂移
- 边缘安全距离不足（< 0.5"）
- 低对比可读性
- 占位文本残留

### 验证循环

1. 生成 -> 出图 -> 检查
2. 列问题清单
3. 修复
4. 对受影响页面复检
5. 至少完成一轮“修复 + 回归”后再宣布完成

---

## 转图片

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

只重渲某一页：

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

## 依赖

- `pip install "markitdown[pptx]"`：文本抽取
- `pip install Pillow`：缩略图工具
- `npm install -g pptxgenjs`：从零生成
- LibreOffice：通过 `scripts/office/soffice.py` 做 PDF 转换
- Poppler：`pdftoppm` 导出图片

