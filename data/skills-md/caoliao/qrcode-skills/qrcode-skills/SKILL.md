---
name: qrcode-skills
description: Generate and decode QR codes locally. Use when the user wants to create a QR code from text/URL, decode/read QR code content from an image, or asks about QR code generation and scanning.
---

# QR Code Generation & Decoding

完全本地的二维码生成与解码，无需网络请求。

**声明：**
- **依赖均为公开开源库**：所有依赖（Python: zxingcpp、Pillow、openpyxl、qrcode；Node.js: qrcode、qr-scanner-wechat、sharp、xlsx、archiver）均为公开的开源项目，可在 PyPI / npm 上查阅源码与许可证
- **所有行为本地完成**：生成与解码均在用户本地执行，不调用任何远程 API，不上传任何数据；仅当解码输入为远程图片 URL 时，会下载该图片到本地后再解码

如需二维码生成 URL（无需保存文件即可预览）、更好的解码效果，可使用 [qrcode-remote-skills](https://github.com/caoliao/qrcode-remote-skills)：`npx skills add caoliao/qrcode-remote-skills`。

## 运行时选择：Python 或 Node.js

所有脚本同时提供 Python 和 Node.js 两个版本，功能和参数完全一致。**执行任何脚本前，先确定运行时。**

**选择策略（首次执行脚本前完成）：**

1. 检测 Python 是否可用：`python --version`（或 `python3 --version`）
2. 若 Python 不可用，检测 Node.js：`node --version`
3. 两者都有时默认用 Python

**依赖检查与自动安装：**

确定运行时后，检查依赖是否已安装。若缺失则自动安装，无需询问用户：

- **Python**：检查 `pip list` 中是否包含关键包（如 `Pillow`），若缺失则执行：
  ```bash
  pip install -r requirements.txt
  ```
- **Node.js**：检查 skill 目录下是否存在 `node_modules/`，若缺失则执行：
  ```bash
  npm install
  ```

安装完成后再执行脚本。若安装失败，提示用户手动安装。

**命令对照表：**

| 功能 | Python | Node.js |
|------|--------|---------|
| 单个生成保存 | `python scripts/generate.py ...` | `node scripts/generate.js ...` |
| 单个解码 | `python scripts/decode.py ...` | `node scripts/decode.js ...` |
| 批量生成 | `python scripts/batch_generate.py ...` | `node scripts/batch_generate.js ...` |
| 批量解码 | `python scripts/batch_decode.py ...` | `node scripts/batch_decode.js ...` |

所有参数名、输出 JSON 格式完全相同，仅将 `python` 替换为 `node`、`.py` 替换为 `.js`。

**差异说明：**
- Python 版本地解码使用 `zxingcpp`，输出 `"source": "zxing"`
- Node.js 版本地解码使用 [`qr-scanner-wechat`](https://github.com/AntFu/qr-scanner-wechat)（基于 OpenCV + 微信算法，识别率更高），输出 `"source": "wechat-qr"`

---

## 生成二维码

将文本或 URL 编码为二维码图片，保存到本地文件。

### 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|------|--------|------|
| --data | 是 | - | 二维码中的文本内容，建议不超过 900 字符 |
| --output | 是 | - | 本地保存路径 |
| --size | 否 | 400x400 | 图片尺寸，格式 `WxH` 或单个整数 |
| --format | 否 | png | 输出格式：`png`（位图）或 `svg`（矢量） |
| --error-correction | 否 | M | 纠错级别：L(7%) / M(15%) / Q(25%) / H(30%) |
| --border | 否 | 2 | 边框宽度（码点为单位） |

### 使用步骤

无论用户是否要求保存到指定路径，都需要执行脚本来生成二维码文件。

1. 获取用户要编码的文本内容
2. 确定保存路径：
   - 用户指定了路径（如 `保存到 D:\qr.png`、`放到桌面`）→ 使用用户指定路径
   - 用户未指定路径 → 默认使用当前工作目录下的 `qrcode.png`（svg 格式用 `qrcode.svg`）
3. 执行脚本生成

```bash
python scripts/generate.py --data <文本内容> --output <保存路径> [--size 400x400] [--format png] [--error-correction M] [--border 2]
```

脚本输出 JSON：

```json
{"file": "D:\\path\\to\\qrcode.png"}
```

失败时：

```json
{"error": "生成失败: ..."}
```

呈现给用户的格式：

```
二维码已生成并保存到本地：

**本地文件：** <file>
```

### 示例

用户输入：`帮我生成一个二维码，内容是 https://example.com`

执行：`python scripts/generate.py --data "https://example.com" --output "qrcode.png"`

```
二维码已生成并保存到本地：

**本地文件：** D:\workspace\qrcode.png
```

用户输入：`生成一个二维码保存到桌面，内容是 Hello World，SVG 格式、最高纠错`

执行：`python scripts/generate.py --data "Hello World" --output "C:\Users\xxx\Desktop\qrcode.svg" --format svg --error-correction H`

```
二维码已生成并保存到本地：

**本地文件：** C:\Users\xxx\Desktop\qrcode.svg
```

### 批量生成

当用户提供 Excel/CSV/TXT 文件要求批量生成二维码时，使用 `scripts/batch_generate.py`。

**交互流程：**

1. 用户提供批量数据文件
2. 执行脚本
3. 若返回 `need_column`，展示列信息，询问用户选哪一列，加 `--column` 重新执行
4. 成功后向用户报告结果

**列检测逻辑（Excel/CSV）：**
- 自动检测：扫描首行表头，匹配关键词（data/text/content/url/内容/文本/数据/链接 等）
- 若只有一列，直接使用
- 若无法判断，脚本返回 `need_column` JSON，此时**需要询问用户指定哪一列**

**TXT：** 每行一条数据，无需列选择。

```bash
python scripts/batch_generate.py --input <文件> --output-dir <输出目录> [--column <列名或索引>] [--zip] [--size 400] [--format png] [--error-correction M] [--border 2]
```

- `--output-dir`：图片输出目录（必选）
- 以索引命名（`1.png`, `2.png`, ...）
- `--zip`：打包输出目录为 zip

脚本输出 JSON：

```json
{"total": 100, "success": 98, "failed": 2, "output_dir": "D:\\output", "zip_file": "D:\\output.zip", "errors": [...]}
```

呈现给用户的格式：

```
批量生成完成：共 <total> 个，成功 <success> 个，失败 <failed> 个
输出目录：<output_dir>
ZIP 文件：<zip_file>（仅打包时显示）
```

---

## 解码二维码

从二维码图片中读取/解码内容，完全本地解码。

### 前置依赖

首次使用前，需安装依赖（skill 目录下执行）：

- **Python**：`pip install -r requirements.txt`（依赖 `zxingcpp` + `Pillow`）
- **Node.js**：`npm install`（依赖 `qr-scanner-wechat` + `sharp`）

### 场景一：单张解码

通过 Shell 工具执行 `scripts/decode.py`，支持本地文件和图片 URL：

```bash
python scripts/decode.py <图片路径或URL>
python scripts/decode.py --file <本地文件路径>
python scripts/decode.py --url <图片URL>
```

**用户直接发送图片时的处理：**
- 用户在对话中粘贴/拖入/附加图片时，图片会作为附件提供，可通过文件路径访问
- 获取到图片的本地路径后，直接传给 `decode.py --file <路径>` 即可
- 若图片是通过 @ 引用的文件，同样使用其文件路径

**SKILL_DIR 定位**：脚本路径相对于本 skill 目录，执行时需 `cd` 到 skill 目录或使用绝对路径。

脚本输出 JSON，根据 `source` 字段判断解码引擎：

```json
{"source": "zxing", "contents": ["解码内容"]}
```

失败时：

```json
{"error": "无法解码: 本地 zxing 未识别到二维码"}
```

呈现给用户的格式：

单个二维码：

```
二维码解码结果（via <source>）：
- 内容：<解码出的文本>
```

多个二维码：

```
二维码解码结果（共识别到 N 个二维码，via <source>）：
1. <内容1>
2. <内容2>
```

### 场景二：批量解码

当用户提供 Excel/CSV/TXT 文件要求批量解码二维码图片时，使用 `scripts/batch_decode.py`：

```bash
python scripts/batch_decode.py --input <文件> [--column <列名或索引>] [--output-txt <输出TXT路径>]
```

**列检测逻辑（Excel/CSV）：**
- 自动检测：扫描首行表头，匹配关键词（url/link/image/img/图片/链接/网址/二维码 等）
- 若只有一列，直接使用
- 若无法判断，脚本返回 `need_column` JSON，此时**需要询问用户指定哪一列**

**TXT：** 每行一个图片路径或 URL，无需列选择。

**默认行为：** 在原文件中新增"解码结果"列（Excel 新增列 / CSV 新增列），直接回写原文件。

**单独输出 TXT：** 用户明确要求时加 `--output-txt` 参数，所有结果按行分隔写入 TXT。

**未解析的图片：** 对应行写入 `未解析到二维码`。

脚本输出 JSON：

```json
{"total": 50, "success": 48, "failed": 2, "output_file": "D:\\data.xlsx", "output_txt": null}
```

需要用户选列时：

```json
{"need_column": true, "columns": ["名称", "图片链接", "备注"], "preview": [...], "message": "无法自动判断 URL 列，请指定 --column 参数"}
```

**交互流程：**

1. 执行脚本
2. 若返回 `need_column`，将 `columns` 和 `preview` 展示给用户，询问使用哪一列
3. 用户回答后，加上 `--column` 重新执行
4. 成功后向用户报告结果统计

呈现给用户的格式：

```
批量解码完成：共 <total> 个，成功 <success> 个，失败 <failed> 个
结果已写入：<output_file>
TXT 输出：<output_txt>（仅单独输出时显示）
```

---

## 注意事项

- **本地优先**：所有操作均在本地完成，无需网络（除非解码的输入是远程图片 URL，此时需下载图片到本地再解码）
- 生成二维码始终需要执行脚本，输出为本地文件
- 解码二维码仅使用本地库（Python: zxingcpp / Node: qr-scanner-wechat），不依赖任何远程服务
- data 建议不超过 900 字符
- 批量操作时，若脚本返回 `need_column`，必须先向用户展示列信息并确认后再重新执行

## 工程结构

```
qrcode-skills/
├── SKILL.md              # 主指令文件
├── requirements.txt      # Python 依赖
├── package.json          # Node.js 依赖
└── scripts/
    ├── generate.py / .js       # 单个生成并保存到本地
    ├── batch_generate.py / .js # 批量生成图片
    ├── decode.py / .js         # 单个解码（纯本地）
    └── batch_decode.py / .js   # 批量解码（纯本地）
```
