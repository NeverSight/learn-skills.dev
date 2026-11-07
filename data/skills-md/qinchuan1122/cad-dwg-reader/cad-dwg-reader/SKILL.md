---
name: cad-dwg-reader
version: 1.0.0
description: 读 DWG/DXF CAD 图纸的技能。当用户提到 CAD、图纸、DWG、DXF、图层、标注、尺寸、坐标、面积、距离、AutoCAD、建筑图、结构图、机械图,或者说"看看这张图""提取图纸信息""测量""转格式""转 PDF""验证图纸"时使用。五大模块覆盖 格式转换、数据提取、图片渲染、几何测量、视觉双重验证。精确数据走 ezdxf 直读 DXF(100% 可信),Qwen2.5-VL 视觉模型做辅助校验,差异标红报警,所有关键数值双重确认后才输出。
---

# cad-dwg-reader

## 核心原则

1. **还原度优先** — 精确数据(尺寸/坐标/文字/块名)**只走 ezdxf 直读 DXF**,100% 可信;视觉模型仅做辅助校验,不作为唯一数据源
2. **双重验证** — 关键字段由 ezdxf 和视觉模型交叉验证,冲突时明确报警
3. **跨平台零硬编码** — 所有路径通过 `scripts/config.py` 自动检测(支持 Windows/macOS/Linux),或用环境变量自定义

## 首次使用

**第一步:环境自检**

```bash
python scripts/env_check.py
```

- 必需项全 ✅ → 前 4 个模块(转换/提取/渲染/测量)可用
- 可选项(Ollama + Qwen2.5-VL)未装 → 仅视觉双重验证不可用
- 缺什么按提示装,详见对应 references/文档

**路径配置**(可选):

如果自动检测找不到 ODA/Ollama,可设环境变量:

| 环境变量 | 用途 | 示例 |
|---|---|---|
| `ODA_FILE_CONVERTER` | ODA File Converter exe 路径 | `/path/to/ODAFileConverter.exe` |
| `OLLAMA_EXE` | Ollama 可执行文件 | `/path/to/ollama` |
| `OLLAMA_MODELS` | Ollama 模型存储目录 | `/path/to/ollama/models` |
| `OLLAMA_HOST` | Ollama API 地址 | `localhost:11434` |
| `OLLAMA_VISION_MODEL` | 默认视觉模型 | `qwen2.5vl:7b` |
| `CAD_DWG_READER_TEMP` | 临时文件目录 | `/tmp/cad-dwg-reader` |
| `CAD_DWG_READER_LOGS` | 日志目录 | `/var/log/cad-dwg-reader` |

## 模块速查表

**优先用 pipeline.py(一键),特殊情况再用单步脚本**:

| 用户需求 | 用哪个脚本 | 示例 |
|---|---|---|
| **"提取这张图的数据"(大多数场景)** ⭐ | `pipeline.py` | `-i f.dwg -m extract-only` |
| **"完整分析+双重验证"** ⭐ | `pipeline.py` | `-i f.dwg -m full-verify` |
| "把 DWG 转成 DXF" | `dwg_convert.py` | `--input f.dwg --to dxf` |
| "列出所有图层/文字/尺寸/块" | `extract_data.py` | `--input f.dxf all` |
| "渲染 PNG(含尺寸覆盖层)" | `render_png.py` | `-i f.dxf -o out.png` |
| "测距/测面积/边界框" | `measure.py` | `--input f.dxf distance --p1 0,0 --p2 100,50` |
| "视觉识别(支持切片)" | `vision_describe.py` | `-i img.png --tile 2` |
| "主卧面积多大/房间识别" | `extract_data.py`(自动含拓扑) | `--input f.dxf all`(看 topology 字段) |
| "校验数据一致性" | `verify_double.py` | `--ezdxf data.json --vision vision.json` |

## 工作流模式

### 模式 A:快速提取(推荐,大多数场景)

用户:"列出这张图的图层/文字/尺寸" / "提取图纸数据"

```bash
python scripts/pipeline.py -i file.dwg -m extract-only
```

一个命令搞定 DWG→DXF→数据提取(含空间拓扑),输出 `_data.json`。0.3-2 秒完成。

### 模式 B:完整分析+双重验证(需 Ollama)

用户:"完整分析这张图" / "确认数据准确"

```bash
python scripts/pipeline.py -i file.dwg -m full-verify
```

一个命令跑完转换→提取→渲染→视觉→验证,输出 `_report.json` 含置信度。15-30 秒。

### 模式 C:几何测量

用户:"量一下从 A 点到 B 点的距离" / "这块面积多大"

```bash
python scripts/measure.py -i file.dxf distance --p1 0,0 --p2 100,50
python scripts/measure.py -i file.dxf area --points "0,0;100,0;100,50;0,50"
```

或先用 `pipeline.py -m extract-only` 看 topology 字段(自动算出每个房间面积)。

### 模式 D:大图切片识别(高精度)

用户:"这张图很大,细节看不清" / "识别所有小字"

```bash
# 渲染后切片识别(2×2 网格)
python scripts/render_png.py -i file.dxf -o big.png --dpi 300
python scripts/vision_describe.py -i big.png --tile 2 --overlap 0.15
```

大图(>2000px)自动切成网格,每片单独识别后合并去重。

### 单步脚本(特殊情况)

需要单独执行某一步时,直接用对应脚本。所有脚本支持 `--help`。

## 关键约定

### 输出路径

- 所有 JSON / PNG 输出默认放**输入文件同目录**
- 临时文件和日志写入用户目录(跨平台):
  - Windows: `%APPDATA%\cad-dwg-reader\`
  - macOS: `~/Library/Application Support/cad-dwg-reader/`
  - Linux: `~/.local/share/cad-dwg-reader/`
- 可通过环境变量 `CAD_DWG_READER_TEMP` / `CAD_DWG_READER_LOGS` 自定义

### Python 解释器

用系统默认 Python 即可(`python3` 或 `python`),版本 ≥ 3.11。

依赖安装:`pip install -r requirements.txt`

### 数据可信度标记

向用户报告数据时,必须标明来源:

| 标记 | 含义 |
|---|---|
| ✅ **精确数据** | 来自 ezdxf 直读,100% 可信 |
| 👁 **视觉识别** | 来自 Qwen2.5-VL,~90% 可信,仅供参考 |
| ⚠️ **冲突** | 双重验证发现冲突,**必须人工核对** |
| 🟡 **未验证** | 单源数据,建议核对 |

## Reference map

按需加载下列文档(不要默认全读):

- **`references/oda_usage.md`** — ODA File Converter 命令行参数、GUI 卡死规避、日志位置
- **`references/ezdxf_recipes.md`** — ezdxf 常用代码片段(遍历实体、读属性、几何计算)
- **`references/rendering_notes.md`** — matplotlib 渲染 DXF 的已知问题(填充/线型/中文字体)
- **`references/vision_setup.md`** — Ollama + Qwen2.5-VL 安装到 E 盘的完整步骤
- **`references/double_verify.md`** — 双重验证策略、置信度计算、报告解读
- **`references/cad_concepts.md`** — CAD 基础概念(实体/图层/块/标注/坐标系,给非工程背景读者)

## 模块详细用法

### dwg_convert.py(格式转换)

```bash
# 单文件:DWG → DXF
python scripts/dwg_convert.py --input file.dwg --to dxf

# 单文件:DXF → DWG
python scripts/dwg_convert.py --input file.dxf --to dwg

# 批量:整个目录
python scripts/dwg_convert.py --input dir/ --to dxf --output dir_dxf/

# 指定版本(默认 ACAD2018)
python scripts/dwg_convert.py --input file.dwg --to dxf --version ACAD2013
```

底层调 ODA File Converter,封装在 `scripts/_oda_runner.py`(超时杀进程、临时目录隔离、自动清理)。

### extract_data.py(数据提取)

```bash
# 各类数据单独提取
python scripts/extract_data.py --input file.dxf layers
python scripts/extract_data.py --input file.dxf text
python scripts/extract_data.py --input file.dxf dimensions
python scripts/extract_data.py --input file.dxf blocks

# 汇总(JSON 输出)
python scripts/extract_data.py --input file.dxf all --output data.json
```

输出 JSON 结构(详见 `assets/output_schema.json`):

```json
{
  "summary": {...},
  "layers": [...],
  "text": [{"type": "TEXT", "content": "...", "insert": [...], ...}],
  "dimensions": [{"type": "linear", "measurement": 1199.5, "text_override": "1200", ...}],
  "blocks": [{"name": "DOOR", "insert_count": 5, ...}]
}
```

### render_png.py(渲染)

```bash
python scripts/render_png.py -i file.dxf -o out.png --dpi 200
python scripts/render_png.py -i file.dxf -o out.png --layout paper
```

自动注册中文字体(SimHei/YaHei),避免乱码。复杂图纸可能渲染不全,详见 `references/rendering_notes.md`。

### measure.py(几何测量)

```bash
# 两点距离
python scripts/measure.py -i file.dxf distance --p1 0,0 --p2 100,50

# 指定图层线段总长
python scripts/measure.py -i file.dxf length --layer WALLS

# 多边形面积(鞋带公式,顶点列表)
python scripts/measure.py -i file.dxf area --points "0,0;100,0;100,50;0,50"

# 整图边界框
python scripts/measure.py -i file.dxf bbox

# 列出所有 LINE 实体的起止点
python scripts/measure.py -i file.dxf coords --entity LINE
```

精度:双精度浮点,100% 基于原始 DXF 坐标。

### vision_describe.py(视觉描述,需 Ollama)

```bash
python scripts/vision_describe.py -i out.png -o vision.json
```

prompt 已针对 CAD 优化,要求模型输出 JSON:

```json
{
  "summary": "...",
  "components": ["墙体", "门", "窗"],
  "dimensions_seen": ["1200", "50.5"],
  "text_seen": ["客厅", "卧室"],
  "symbols_seen": [...],
  "anomalies": [...]
}
```

模型缺失时友好降级,提示用户安装(不会崩溃)。

### verify_double.py(双重验证,核心)

```bash
python scripts/verify_double.py \
    --ezdxf data.json \
    --vision vision.json \
    --output report.json
```

输出 4 类 + 置信度:

- **verified** — ezdxf 与视觉模型一致(高可信)
- **ezdxf_only** — 视觉模型漏识别(可能渲染丢失)
- **vision_only** — ezdxf 没读到(可能视觉幻觉,**警惕**)
- **conflict** — 数值冲突(**必须人工核对**)
- **confidence** — high / medium / low

详见 `references/double_verify.md`。

## 常见问题

### Q:用户给的是 DWG 怎么办?

先 `dwg_convert.py --to dxf` 转成 DXF,后续所有模块都用 DXF。

### Q:用户问的"X 在哪里",怎么定位?

1. 先 `extract_data.py all` 拿到所有坐标
2. 找到对应实体的 `insert` 字段
3. 或 `measure.py coords --entity POINT/TEXT` 列出所有点

### Q:用户说"这张图好像不对" / "校验一下"

走模式 D(双重验证),冲突项和低置信度就是问题点。

### Q:视觉模型报错"model not found"?

```bash
ollama pull qwen2.5vl:7b
```

详见 `references/vision_setup.md`。

### Q:PNG 里中文是方块?

`render_png.py` 已自动注册中文字体。如果还是乱码,确认 `C:\Windows\Fonts\msyh.ttc` 或 `simhei.ttf` 存在。详见 `references/rendering_notes.md`。
