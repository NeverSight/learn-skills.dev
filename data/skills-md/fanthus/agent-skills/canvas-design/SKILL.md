---
name: canvas-design
description: Generates visual art as .png or .pdf from design philosophy or from WeChat public account content. Use when the user asks for a poster, cover image, piece of art, or static visual; when they provide 微信公众号内容 for a cover; or when they want design philosophy expressed on a canvas. Creates original work only; no copying existing artists.
license: Complete terms in LICENSE.txt
---

# Canvas Design

## 使用场景

1. **微信公众号封面**（优先）：用户提供公众号内容 → 输出一张封面图。
2. **设计哲学 + 画布**：用户要海报/艺术图/静态视觉 → 先写视觉哲学 (.md)，再在画布上表达 (.pdf/.png)。

---

## 微信公众号封面

- **输入**：用户给出的微信公众号文章内容（或标题、摘要等）。
- **输出**：一张图片，默认保存为 `imagen_output.png`。

**执行**：在 skill 目录 `canvas-design` 下执行脚本，将用户输入的公众号内容（可原样或整理/翻译为一段描述）作为 prompt 传入：

```bash
python scripts/generate_cover.py "<用户输入的微信公众号内容>"
```

脚本内部调用 `generate_image_correctly(prompt)`；Imagen 对英文 prompt 效果更佳时，可先对文案做简洁翻译或摘要再传入。

---

## 设计哲学 + 画布

两步：1）撰写视觉哲学并输出为 .md；2）在画布上视觉化表达，输出为单页 .pdf 或 .png（字体见 `canvas-fonts/`）。

完整流程、哲学示例、原则与精修步骤见 **[reference.md](reference.md)**。

---

## 资源

- 脚本：`scripts/generate_cover.py`（微信公众号封面用）
- 字体：`canvas-fonts/`
- 依赖：`requirements-imagen.txt`（封面生图用）
