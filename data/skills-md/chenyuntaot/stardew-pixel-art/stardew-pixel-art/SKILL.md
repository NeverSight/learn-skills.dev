---
name: stardew-pixel-art
description: Generate consistent Stardew Valley-style pixel art PNGs with transparent backgrounds. Invoke when user needs pixel art assets, sprites, icons, or UI elements in Stardew Valley aesthetic for app/game development.
---

# Stardew Valley 风格像素图

交付同类资产像素块尺寸一致的 PNG。非瓦片为透明底；瓦片铺满画布、不去白底。

`SKILL_DIR` = 本文件所在目录。后处理代码在 `scripts/`。对齐算法用 PyPI 包 `perfect-pixel`，或工作区根目录的 `perfectPixel/`（独立上游项目，不要整仓拷进 skill）。不要把库或后处理源码抄进对话。

## 按需打开

| 何时 | 打开 |
|------|------|
| 选类型、生成尺寸、网格 | `references/assets.json`（数字唯一来源）和 `references/assets.md` |
| 写 prompt | `references/prompts.md`；风格拿不准再读 `references/style.md` |
| 调后处理参数、排错 | `references/postprocess.md`、`references/quality.md` |

```bash
python ${SKILL_DIR}/scripts/postprocess.py --list-types
```

## 流程

1. 用 `assets.json` 的 `aliases` 定 `id`。记下 `image_size`、`prompt`。
2. 打开 `prompts.md`：通用前缀 + 该类型块，只替换 SUBJECT。
3. 用**当前宿主提供的生图工具**出图（Trae `GenerateImage`、Grok `image_gen`、Claude/Cursor/Codex 各自的 image 工具，不要写死工具名）。白底，不要透明底。能设像素尺寸时用 `assets.json` 的 `image_size`；只能设比例时：正方形资产 `1:1`，人物约 `1:2`，大型植物偏竖图。
4. 按 `quality.md` 初检。不合格重画，不要拿糊图去对齐。
5. 后处理（强制）：

```bash
python ${SKILL_DIR}/scripts/postprocess.py <生成图> <交付.png> --asset <id>
```

需要解释器带 `numpy`、`Pillow` 和 `perfect-pixel`：

```bash
pip install "perfect-pixel[opencv]" pillow
```

没有 pip 包时，脚本会找工作区根目录的 `perfectPixel/src`。

6. 按 `quality.md` 终检后再交给用户。

交付边长 = 网格 × `--scale`（默认 8）。物品是 128×128，不是生成时的 2048×2048。

## 批量

同批次同一个 `--asset`，只改 SUBJECT。不要让每张图自己估网格。

```bash
python ${SKILL_DIR}/scripts/postprocess.py --batch <输入目录> <输出目录> --asset item
```

## 硬性规则

- 禁止跳过后处理，禁止手写一份对齐/去白底脚本
- 生成用白底；不要让模型出透明底
- `--asset tile` 不去白底；其它类型主体不要贴画布边
- 同批次锁定：模板、`image_size`、`--asset`、`--scale`、`--sample`、`--refine`、`--bg-tolerance`

## 示例

红色苹果物品：`prompts.md` 的 item，SUBJECT `a shiny red apple with a small green leaf`，`image_size=2048x2048`，然后 `--asset item`。

一组水果图标：全部 `--asset item`，只换苹果/香蕉/橙子/葡萄的 SUBJECT。
