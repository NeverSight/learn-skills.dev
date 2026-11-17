---
name: film-scan-lab
description: "分析、反相、修复并归档胶片扫描或相机翻拍文件，支持 C-41 彩色负片、黑白负片和 E-6 幻灯片；自动或手动测量片基，提取胶片边码并匹配片种，使用红外通道除尘，合并多次扫描 HDR，应用扫描仪/翻拍相机配置与胶片曲线，保留或重建颗粒，生成大划痕人工确认界面，并输出 16-bit TIFF、JPEG、接触表、HTML 报告及 Lightroom/Photoshop 可用的 XMP 参数。用于用户提出负片反相、胶片扫描、胶片翻拍、橙色片基校正、除尘修复、胶片 HDR、片种识别、胶片数字化或档案扫描时。"
---

# 胶片扫描实验室 Film Scan Lab

把胶片扫描当作密度测量与数字暗房流程，不要把它简化成 RGB 直接反相。保留源文件，区分直接测量、自动推断和风格解释。

## 工作流

1. 运行能力检测：

```bash
python scripts/capability_check.py
```

缺少 NumPy、OpenCV、Pillow 或 tifffile 时停止。`rawpy` 仅用于相机翻拍 RAW；Tesseract 缺失时仍提取边码区域，并允许用 `--edge-code` 手动提供边码。

2. 处理单张扫描：

```bash
python scripts/film_scan_lab.py INPUT --output-dir OUTPUT
```

优先使用保留片边的 16-bit TIFF。JPEG 可以处理，但必须在报告中标记位深和动态范围限制。

3. 对已知彩负、配置和片基运行：

```bash
python scripts/film_scan_lab.py INPUT --output-dir OUTPUT \
  --film-type color-negative --capture-profile generic-scanner-srgb \
  --base-roi 20,20,300,100 --film-profile generic-c41
```

4. 使用多次曝光扫描和红外通道：

```bash
python scripts/film_scan_lab.py SCAN_MID.tif --hdr SCAN_DARK.tif SCAN_BRIGHT.tif \
  --ir IR_SCAN.tif --output-dir OUTPUT
```

HDR 输入必须是同一帧、同一裁切、不同曝光的扫描。脚本先对齐，再估计相对曝光并在非饱和区域合并。红外通道先对齐，再生成独立缺陷蒙版。

5. 边码与片种：

- 自动保存 `edge-code-strip.png`。
- Tesseract 可用时运行 OCR，并用 [assets/film-profiles.json](assets/film-profiles.json) 的模式匹配片种。
- OCR 低置信度时使用 `--edge-code "KODAK 400-3"` 或 `--film-profile PROFILE_ID`。
- 不要把模糊边码猜测写成确定片种。

6. 大划痕确认：

- 打开 `scratch-review.html`。
- 勾选要修复的划痕并下载 `scratch-decisions.json`。
- 使用 `--review-decisions scratch-decisions.json` 重新运行。
- 默认只自动修复高置信度小灰尘，不自动填补穿过面部、文字或关键边缘的大损伤。

7. 批量处理同一卷：

```bash
python scripts/film_scan_lab.py ROLL_FOLDER --output-dir OUTPUT --film-type color-negative
```

目录模式从全部画面边缘汇总片基估计和片种结果，再为每帧建立独立输出目录及整卷接触表。不要混合不同胶卷或不同扫描设置。

8. 检查 `validation.json`。只有状态为 `pass`、三套 TIFF/JPEG 完整、TIFF 为 RGB uint16、ICC 存在、HTML 引用有效时，才报告完成。

## 三套版本

- `01-neutral-positive`：中性正片。使用片基密度、通道归一和克制的趾肩曲线。
- `02-print-interpretation`：印相解释。使用胶片配置中的反差、纸白、色温和印相曲线；没有真实纸张配置时不要声称精确 RA-4 模拟。
- `03-archive-master`：档案正片。保留更宽密度范围、16-bit、ICC 和最少干预；不应用大划痕自动修复。

另保留 `00-source-master.tiff`，不得覆盖原始输入。

## 色彩与配置

读取 [references/color-pipeline.md](references/color-pipeline.md) 了解密度空间反相、片基、配置文件和限制。

- 扫描仪/翻拍相机配置来自 [assets/capture-profiles.json](assets/capture-profiles.json)。
- 胶片配置来自 [assets/film-profiles.json](assets/film-profiles.json)。
- 用户配置可通过 `--capture-profile-file` 或 `--film-profile-file` 加载。
- 只有存在色卡或经过验证的设备配置时才能声称色彩准确；否则使用“中性解释”或“印相解释”。

## 除尘、划痕与颗粒

读取 [references/restoration-and-review.md](references/restoration-and-review.md)。

- 红外蒙版优先；无红外时使用多尺度局部残差、形态学和连通区域。
- `--dust conservative|normal|off` 控制小缺陷阈值。
- `--grain preserve|clean|rebuild` 控制颗粒。默认 `preserve`，不要把胶片颗粒当作扫描噪声全部抹掉。
- `rebuild` 必须记录颗粒尺度、强度和随机种子。

## Adobe 参数输出

输出的 `.xmp` sidecar 面向已经反相的正片 TIFF/JPEG，作为 Lightroom、Adobe Camera Raw 或 Photoshop Camera Raw Filter 的后续起点。基础 ACR 参数无法重现密度空间反相，因此不要把 XMP 描述成完整负片转换配方。另输出 `photoshop-adjustments.json`，记录曲线、色彩平衡和修复蒙版路径。

## 输出

- `00-source-master.tiff`
- `01-neutral-positive.tiff/.jpg/.xmp`
- `02-print-interpretation.tiff/.jpg/.xmp`
- `03-archive-master.tiff/.jpg`
- `edge-code-strip.png` 与 `edge-code.json`
- `dust-mask.png`、`scratch-mask.png`、`scratch-review.json`
- `scratch-review.html` 与 `review-preview.jpg`
- `grain-map.png`
- `contact-sheet.jpg`
- `analysis.json`、`parameters.json`、`photoshop-adjustments.json`
- `report.html`、`validation.json`

读取 [references/output-and-limitations.md](references/output-and-limitations.md) 解释 HDR、OCR、XMP、红外与档案限制。

## 质量规则

- 保留原始扫描及源 ICC，不修改用户文件。
- 片基区域不足时降低置信度，并要求手动 ROI；不要伪造精确片基。
- 传统银盐黑白片的红外缺陷图可能与影像本身冲突，检测异常时回退到可见光方法。
- 大面积缺失无法从邻域可靠恢复；人工确认不等于内容真实重建。
- 批量同卷处理要共享片基和配置，但保留逐帧曝光与裁切。
- 输出 XMP 时明确它作用于正片输出，不作用于原始负片扫描。
