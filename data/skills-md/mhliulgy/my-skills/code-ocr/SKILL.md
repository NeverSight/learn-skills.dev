---
name: code-ocr
description: 使用百度 OCR 高精度含位置版将代码截图转换为文本文件，保持原始缩进。使用场景包括：(1) 将代码截图识别为可编辑文本，(2) 从截图提取代码，(3) 图片转代码文字。触发条件：用户提到"截图转文字"、"OCR"、"识别代码"、"图片转文本"、"code screenshot to text"
---

# Code OCR

将代码截图转换为文本文件，使用百度 OCR 高精度含位置版 API，保持原始缩进。

## 环境配置

在使用前需要配置百度 API 密钥（系统环境变量），默认用户已经配置完成：

```bash
# Windows
setx BAIDU_API_KEY "your_api_key"
setx BAIDU_SECRET_KEY "your_secret_key"
```

或者在当前终端设置：
```bash
# Windows (当前终端)
set BAIDU_API_KEY=your_api_key
set BAIDU_SECRET_KEY=your_secret_key
```

## 使用方法

### 基本用法

```bash
# 保存 OCR 中间结果（避免重复调用 API）
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" <图片路径> --save-json <json文件路径>

# 从 JSON 加载结果，多次调整 ratio 参数实验
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" <json文件> --load-json <json文件路径> --ratio <值>

# 仅识别图片（不推荐）
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" <图片路径> [输出目录]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `图片路径` | 可选，截图文件的路径（支持 PNG、JPG、BMP 等格式），或 JSON 文件路径 |
| `输出目录` | 可选，默认保存到图片所在目录 |
| `--ratio` / `-r` | 可选，平均字符宽度的缩放倍率，用于微调缩进计算。默认 0.955 |
| `--save-json FILE` / `-s FILE` | 可选，OCR 成功后保存中间结果到 JSON 文件 |
| `--load-json FILE` / `-l FILE` | 可选，从 JSON 文件加载 OCR 结果，跳过 OCR 步骤 |

### 使用示例

```bash
# 1. 首次运行：OCR 识别并保存中间结果
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" screenshot.png -s screenshot.json

# 2. 后续实验：加载 JSON（使用 -l 参数），多次调整 ratio 参数
# 只需指定 -l JSON文件路径 和 --ratio 值，无需其他参数
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" -l screenshot.json --ratio 0.96
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" -l screenshot.json --ratio 0.955
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" -l screenshot.json --ratio 0.95

# 3. 简写形式
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" -l screenshot.json -r 0.955
```

> **提示**：首次 OCR 识别后会生成 JSON 文件，如需调整缩进效果，请使用 `-l` 参数加载该 JSON 文件重新运行。

### 输出文件

- 文件名格式：`{原文件名}_{时间戳}_{ratio}.txt`
- 例如：`screenshot_20260220_143052_0.955.txt`
- 编码：UTF-8

### AI 工具需要给出的提示

**重要**：当 AI 工具应该主动给出基于 JSON 文件重新运行的命令，例如：

```bash
# 使用 -l 参数加载 JSON 文件，调整 ratio 参数
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" -l screenshot.json --ratio 0.96
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" -l screenshot.json --ratio 0.955
python "C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py" -l screenshot.json --ratio 0.95
```

并向用户解释不同 ratio 值的效果差异，帮助用户选择最佳的缩进参数。

## 工作原理

1. **API 调用**：使用百度 OCR "高精度含位置版"（accurate）接口
2. **位置解析**：利用返回的位置信息（location）计算每个字符的坐标
3. **行重构**：根据字符的 top 坐标分组，识别出所有行
4. **缩进保持**：根据每行第一个字符的 left 坐标计算缩进空格数

## 交叉验证（模型自校验）

当 OCR 结果输出后，AI 模型应主动使用自身的多模态能力对原图进行"视觉 OCR"，并与百度 OCR 的输出结果进行交叉验证。

### 验证流程

1. **读取原图**：AI 模型直接查看用户提供的代码截图
2. **视觉识别**：利用模型的视觉能力识别图片中的代码文本
3. **对比校对**：将视觉识别结果与百度 OCR 输出进行对比
4. **修正错误**：发现差异时，以视觉识别结果为准进行修正

### 常见需要校验的内容

| 校验项 | 说明 | 示例 |
|--------|------|------|
| 相似字符 | `O` vs `0`，`I` vs `l` vs `1`，`S` vs `5` | `list` 被误识别为 `1ist` |
| 符号混淆 | `'` vs `''`，`"` vs `""`，`->` vs `→` | `don't` 被误识别为 `don''t` |
| 特殊符号 | `@`, `#`, `$`, `%`, `&`, `\|`, `\`, `/` | `@staticmethod` 中的 `@` |
| 缩进对齐 | 空格与制表符的混合使用 | Python 代码的缩进层级 |
| 注释符号 | `//`, `/*`, `*/`, `#`, `<!--` | 注释起始和结束位置 |
| 括号匹配 | `()`, `{}`, `[]`, `<>` | 嵌套括号的完整性 |
| 符号遗漏 | 代码行末的分号、逗号等 | `return x` 被误识别为 `return x;` |
| 中英符号 | 英文逗号 `,` vs 中文逗号 `，` | `print("Hello, World")` 被误识别为 `print("Hello，World")` |

灵活校验：根据代码语言和上下文，判断代码语言，并根据该语言语法规则进行更有针对性的校验。

### 校对后输出格式

```
=== 百度 OCR 原始结果 ===
[原始识别文本]

=== 交叉验证修正 ===
- 第 X 行: "原始错误" → "修正后"
- 第 Y 行: "原始错误" → "修正后"

=== 最终修正结果 ===
[校对后的最终文本]
```

### 使用建议

- 对于关键代码（如密钥、配置、正则表达式），**必须**进行交叉验证
- 当 OCR 结果中存在明显语法错误时，优先信任模型的视觉识别
- 若图片模糊或字体特殊，可提示用户提供更清晰的截图

## 脚本位置

脚本路径：`C:\Users\12556\.claude\skills\code-ocr\scripts\code_ocr.py`
