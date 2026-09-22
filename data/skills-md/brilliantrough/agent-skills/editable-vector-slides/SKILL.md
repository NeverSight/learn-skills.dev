---
name: editable-vector-slides
description: 将自包含的 SVG 科研流程图、架构图转换为保留真实文字的矢量 PDF，以及原生可编辑的 PowerPoint PPTX。Use when asked to convert SVG/PDF figures to editable PDF/PPTX, preserve editable text and vector shapes, or avoid a slide that is only a screenshot. Includes a tested SVG→PDF→text-template→native DrawingML workflow; the PPTX helper targets flattened path-based SVGs, not arbitrary SVG artwork.
compatibility: Python 3 with lxml, python-pptx, Pillow, fontTools; Chrome/Chromium, LibreOffice, MuPDF mutool and Poppler pdfimages/pdftoppm. Linux workflow tested; Microsoft PowerPoint opening remains a separate check.
---

# Editable Vector Slides

把图变成可编辑对象，而不是把截图放进幻灯片。默认中文交付，清楚说明哪些对象可编辑、哪些效果仍是图片。

## 先判断目标

- **只要 PDF**：SVG → Chrome 打印。核验真实文字、矢量路径、页面尺寸；不要额外生成 PPTX。
- **要可编辑 PPTX，且有 SVG**：优先从 SVG 恢复原生几何，从 PDF 导入文字；不要只交付整页图片。
- **只有 PDF**：可尝试 LibreOffice 导入文字和图形，但渐变/裁剪可能受损。没有 SVG 就不能使用本 skill 的几何重建脚本；先检查结果，再决定是否需要用户提供源 SVG。
- **只需外观，不需逐元素编辑**：可嵌入 SVG + PNG fallback，但必须说明这不是原生对象版。PowerPoint 的“转换为形状”可作为备选，不承诺所有版本都支持。

先找原始 PPTX；若已有能满足需求的源文件，不做有损往返。

## 安装（一次性，任意机器）

脚本路径相对本 `SKILL.md` 所在目录解析为绝对路径，不相对项目 cwd。把下面示例里的目录换成你实际加载到的 `SKILL.md` 所在目录（常见：`~/.agents/skills/` 或 `~/.pi/agent/skills/`，符号链接会被 `readlink -f` 解开）。

```bash
SKILL_DIR="$(dirname "$(readlink -f ~/.agents/skills/editable-vector-slides/SKILL.md)")"
bash "$SKILL_DIR/scripts/install.sh"
```

`install.sh` 做三件事，幂等可重跑：

1. `pip install python-pptx Pillow fonttools lxml`（失败时依次回退 `--user`、`--break-system-packages`；仍失败提示建 venv 并用 `PYTHON=<venv python>` 重跑）。
2. 检查系统工具并打印各发行版安装提示：Chrome/Chromium 其一、`mutool`（mupdf-tools）、`pdfimages`/`pdftoppm`（poppler-utils）、LibreOffice。**它只检查不安装系统包**——不重装 LibreOffice/Inkscape，不改全局环境变量。
3. 跑 `check.py` 冒烟测试。

输出 `SETUP OK` 才能执行转换；仅 PDF 模式只需 Chrome + mutool。缺字体（尤其 Times New Roman）时先装字体：`fc-match` 要看实际命中的字体名，不能仅凭命令成功判断。

## 执行

```bash
SKILL_DIR="$(dirname "$(readlink -f ~/.agents/skills/editable-vector-slides/SKILL.md)")"

# PDF + 原生可编辑 PPTX（默认）。输出目录必须不存在，防止覆盖用户文件；源 SVG 不动。
python3 "$SKILL_DIR/scripts/convert.py" /absolute/input.svg \
  --format both --output-dir /absolute/new-output-dir

# 只生成 PDF；不需要 python-pptx/LibreOffice/Poppler。
python3 "$SKILL_DIR/scripts/convert.py" /absolute/input.svg \
  --format pdf --output-dir /absolute/new-pdf-dir
```

若 Chrome 的沙箱在本机隔离环境不可用，只对可信输入显式加 `--no-sandbox`；不要默认关闭沙箱。输入仍需先经过信任判断；脚本拒绝 DTD、脚本、事件属性和外部资源，但这不是任意不可信 SVG 的安全沙箱。

默认 `both`；`pptx` 也保留中间 PDF 作为参考。脚本最长单条外部命令 180 秒，全部前台运行，不启动常驻 UNO listener；超时/中断只终止本次命令的独立进程组，不匹配或杀死用户其它会话。

### 产物

```text
new-output-dir/
├── input.pdf
├── input.pptx        # 仅 PPTX/both 模式
├── reference.png     # 原 PDF 渲染
├── preview.png       # PPTX → LibreOffice → PDF → PNG
├── report.json       # 尺寸、对象数、检查结果、限制
└── work/             # 临时 XML、文字模板、提取图片、commands.log
```

只有完成验证后才将文件交付或复制到用户指定位置。失败时保留 `work/commands.log` 诊断；不要把一个 ZIP 可打开但零页/空白的文件称为成功。

## 原生 PPTX 辅助脚本的输入范围

**这是有边界的转换方案，不是通用 SVG 引擎。** 预检失败时先读报错，不删掉不认识的节点来“让它通过”。需要扩展时按该文件实际结构做最小适配，重新验证。

支持：
- 自包含的单页 SVG，明确的 width/height 和从 `0 0` 开始的 viewBox；物理尺寸与 viewBox 等比。
- 已展开的 `<path>`：M/L/H/V/C/S/Z（含相对命令），单轮廓；贝塞尔曲线保留为原生 DrawingML 曲线。
- 嵌套分组、填充、描边、线帽/连接方式；`data-name` 可保留为对象名。
- 真实 `<text>/<tspan>`：借助 Chrome PDF 和 LibreOffice 的文字导入，不自行重排复杂字体。
- 直接定义的 `userSpaceOnUse` 线性渐变；数值 stops 从 0 到 1。保留渐变角度与色标。
- 全页背景 rect。
- 单独成组的单 path Gaussian-blur 阴影：提取 PDF 图像 + SMask，并合成正确透明度。按绘制次序匹配，校验数量、尺寸、滤镜边界和 opacity，不硬编码 PDF 对象号。

不支持或需人工处理：
- 几何 transform、use/symbol、非背景 rect/circle/ellipse、复合路径的洞、mask/clipPath、CSS 样式表、径向渐变、其它滤镜、嵌入图像。先在源编辑器展开/转路径，或针对实际需要扩展脚本。
- **所有文字被放在几何上方**。文字应被其它图形遮挡的设计，必须额外重建 z-order；不适合直接使用本方案。
- **渐变起止点偏移未精确重映射**，角度/色标保留但分布可能略变。视觉不合格时再实现端点投影，不声称像素一致。
- 字体子集与 PDF 导入可能将词、上下标拆成多个文本框；LibreOffice 往返可能轻微移动文字基线（小图回归样例已观察到）。需要像素级对齐时，根据预览调整文字位置，不假设导入坐标完全精确。可编辑不等于恢复原始 PowerPoint 段落结构。
- 不恢复原始组、图层、动画、母版或原作者的参数化形状语义；图形可修改填充/描边/节点。

脚本会拒绝已知不支持的结构，但所有转换仍须视觉验收。

## 工作原理（改脚本前读）

1. **SVG → PDF**
   - `width/height` 解析单位：无单位/px 按 96 DPI；`in/cm/mm/pt/pc` 转英寸。
   - 临时 HTML：`@page { size: Win Hin; margin:0 }`，`img` 同尺寸。
   - Chrome headless 打印，无页眉页脚。用独立 profile，不影响现有浏览器会话。
   - `mutool draw -F trace` 校验一页、MediaBox、文字和图像。

2. **PDF → 文字模板**
   - LibreOffice：PDF → ODG；读取 ZIP 内的实际节点类型，而非用文件大小推断“已可编辑”。
   - 在 ODG ZIP 中把 mimetype/manifest 的 graphics 类型改为 presentation；将 content.xml 的 `office:drawing` 改为 `office:presentation`，保存 ODP。
   - ODP → `pptx:Impress MS PowerPoint 2007 XML`；保留其文字框，丢弃导入的图形。
   - `scripts/convert.py` 的 `odg_to_odp()` 可独立复用；仍须验证页数和文字。

3. **SVG 几何 → DrawingML**
   - `fontTools` 解析曲线和边界；依据页面/viewBox 比例换算为 EMU。
   - 标准换算：1 inch = 914400 EMU；1 pt = 12700 EMU。只有 viewBox 恰为 1/100mm 时才是 `360 EMU/SVG unit`，不能把这个常数用于其它 SVG。
   - 每条路径生成 `a:custGeom`；去掉自动主题样式，以免覆盖源 fill/stroke。
   - 原生 `a:gradFill` 代替 LibreOffice 拆出的渐变条带。
   - 从 PDF 恢复阴影位置、RGB、SMask、组透明度。**不能假定 SMask 对象号就是 RGB + 1，也不能漏乘组 opacity。**
   - 加回文字，修正本方案遇到的 `TimesNewRoman` → `Times New Roman` 名称；重新编号所有 `cNvPr id`。

4. **验证并交付**
   - 见下一节；能读取 ZIP 不是渲染正确的证明。

## 验收清单

自动脚本已检查：
- 单页、SVG/PDF/幻灯片尺寸匹配，PPTX ZIP 能正常读取。
- 原生路径数、阴影数、文字框数；输出 `report.json`，不用硬编码 1540/139/9。
- 源文字与 PPTX 文字的**去空白字符多重集**相等。这只检查字符丢失/增加，不证明顺序、排版或语义正确。
- 阴影数量、像素尺寸、资源/绘制次序、位置和 opacity 一致。
- PPTX 能通过 LibreOffice 重新渲染。

Agent 还必须做：
1. 用 `read` 查看 `reference.png` 与 `preview.png`；检查文字换行/上下标、箭头端点、圆角、阴影、渐变条纹、模块遮挡。
2. 查看对象构成：必须有文本框和矢量路径，而非只有整页图片；数清实际 raster 内容。
3. 对复杂字体/遮挡/渐变明确剩余偏差；若不能看图，直说只完成结构验证。
4. 尚未在 Microsoft PowerPoint 打开时，不宣称已做 Office 实机兼容测试。建议有同名字体的 PowerPoint 打开检查。
5. 交付简短：清晰路径、可编辑内容、保留为图片的部分、实际验证范围。

## 已踩过的坑

- 某些机器的 LibreOffice 缺 `libreglo.so`：需给子进程加 `LD_LIBRARY_PATH=<program dir>`；脚本从 soffice 位置和常见安装目录自动探测（/usr/lib*/libreoffice/program、/opt、/snap），探测不到才报错。UNO 若确实要用，使用系统 python3，不是 conda Python。
- Draw 直接导出 PPTX 曾生成 **零页** 小文件。强行指定 Impress filter、仅改扩展名都不能证明成功。
- SVG → ODG 常只是一个 graphic frame + SVG/预览图片，不代表拆成了原生对象。
- PDF 导入图形会把渐变拆成条带，丢掉裁剪，产生白缝/方块。把它当文字模板，不作最终高保真图形来源。
- UNO 中 `while source.getCount(): target.add(source.getByIndex(0))` 并不保证源计数减少，可能无限复制。这里完全绕过跨文档 shape 搬运。
- 不用 `pkill -f` 匹配包含在当前命令行中的字符串，会杀掉执行 shell；本方案不做全局杀进程。
- SVG 高斯模糊在本次 Chrome PDF 中变成栅格阴影；不要扩大成“所有渲染器都必然栅格化”或“无画质损失”的断言。

## 最小回归检查

```bash
python3 "$SKILL_DIR/scripts/check.py"
# 对实际输入完成端到端转换后，仍要按验收清单看图。
```

已用 `SPAR_Editable_Pipeline.svg` 验证的参考规模：18×9 inch，1,540 原生路径、139 文字框、83 渐变填充、9 透明阴影；这些是例子的验收结果，不是脚本输入限制。
