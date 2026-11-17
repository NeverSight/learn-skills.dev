---
name: markitdown-ocr
description: 引导 LLM 通过 `markitdown-ocr` 插件(官方插件仓库 microsoft/markitdown/packages/markitdown-ocr)使用 LLM Vision(OpenAI 兼容模型,如 gpt-4o / Azure OpenAI / Gemini / 其它 OpenAI 兼容服务)对 PDF / DOCX / PPTX / XLSX 内嵌图片与扫描页进行 OCR 文本抽取。覆盖安装、配置(`OPENAI_API_KEY` / Azure 凭据 / 自定义 endpoint)、Python API 与 CLI 包装、扫描 PDF 的全页渲染回退、各格式 OCR 行为差异(行内插入 / 表格后追加 / 顶层描述)、自定义 prompt、成本/限制排错。当用户问"扫描 PDF 怎么转 markdown"、"PPT 里图片的文字怎么抽出来"、"怎么用 GPT-4o 做 OCR"、"markitdown-ocr 插件怎么装"、"Azure OpenAI 怎么配 markitdown"时使用本 skill;若只是普通 CLI 用法或 MarkItDown 概览,跳到兄弟 skill `markitdown-cli` 与 `markitdown-awesome`。
license: MIT
---

# MarkItDown OCR (LLM Vision) 完整使用指南

> 用途明确:让 LLM 能基于本 skill **正确配置并调用** `markitdown-ocr` 插件,完成对 PDF/DOCX/PPTX/XLSX 内嵌图片与扫描页的 OCR 抽取。
>
> **离线基线**:基于 [`packages/markitdown-ocr/`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-ocr) main 分支(2026-08 时刻)。
> **任何"插件当前是否支持 X / 参数名是否变更"的问题,以官方 README 与源码为准**:
> - 源码:`packages/markitdown-ocr/src/markitdown_ocr/`
> - 入口: [`_plugin.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown-ocr/src/markitdown_ocr/_plugin.py)
> - OCR 服务抽象: [`_ocr_service.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown-ocr/src/markitdown_ocr/_ocr_service.py)

---

## When to Use This Skill

✅ **什么时候用本 skill**(LLM Vision OCR / 扫描件 / 嵌入图片):
- 用户问 "扫描 PDF 怎么转 markdown"(原 PDF 没可选文本)
- 用户问 "PPT/Word/Excel 里嵌入的图片,文字怎么抽出来"
- 用户想用 GPT-4o / GPT-4o-mini / Claude / Gemini 做 OCR
- 用户问 "Azure OpenAI 怎么配 markitdown-ocr"
- 用户问 "markitdown-ocr 插件怎么装、怎么用"
- 用户要做本地化 OCR(走 vLLM / Ollama)

❌ **什么时候不该用本 skill**:
- 只是普通 CLI 用法(转 PDF / DOCX,没有图片文字需求)→ `markitdown-cli`
- 用户问 "MarkItDown 是什么 / 支持哪些格式 / 怎么选" → `markitdown-awesome`
- 用户问 "Azure Document Intelligence 怎么配" → `markitdown-cli`(那是 MarkItDown 自带后端,不是这个 OCR 插件)
- 用户问 "怎么把 PDF 转纯文本"(用 textract 更合适)→ 转交 `markitdown-awesome`(`references/ecosystem/alternatives.md` 给出 markitdown / textract / unstructured / pandoc / docling 对比)

⚠️ **模糊地带**:
- 用户说 "PDF 转 markdown 但图片文字没有" → 默认走 OCR 插件路径(本 skill)
- 用户说 "想用 LLM 抽取表格" → OCR 可以做,但若对表格精度要求高,优先 Azure Document Intelligence
- 用户已经在用别的 OCR(Tesseract / PaddleOCR) → 不属于本 skill,引导比较工具

---

## Workflow

每次回答 OCR 类问题时,按下面流程走一遍:

### Step 1 — 确认文档类型 & 用户目标

- 输入格式:PDF / DOCX / PPTX / XLSX(本 skill 只覆盖这四种)
- 文字位置:嵌入图片 / 扫描页整页 / 两者都有
- LLM 选型:OpenAI / Azure / Gemini / 本地
- 成本预算:贵 vs 便宜(`gpt-4o` vs `gpt-4o-mini`)

### Step 2 — 检查环境

```bash
pip show markitdown-ocr openai | grep -E '^(Name|Version)'
markitdown --list-plugins | grep ocr
```

两者都该有输出。

### Step 3 — 选择 Python API 形态

- OpenAI:`MarkItDown(enable_plugins=True, llm_client=OpenAI(), llm_model="gpt-4o")`
- Azure OpenAI:换 `AzureOpenAI(...)`,传 `azure_endpoint` / `api_version`
- 本地 vLLM / Ollama:`OpenAI(base_url=..., api_key=<your-token>)`(本地服务通常不校验 key)
- Gemini:`OpenAI(base_url=..., api_key=<your-key>)`

### Step 4 — 决定 Prompt

- 默认 prompt(插件自带):"Extract all text … maintain layout … no commentary"
- 强调表格:加 "Preserve table layout with Markdown pipes"
- 强调只输出文字:加 "Do not describe, summarize, or comment"

### Step 5 — 自检 & 运行

对照 [Validation 自检清单](#validation自检清单)。

### Step 6 — 处理结果

- 输出含 `*[Image OCR]…[End OCR]*` 块 → 成功
- 没出现 → 检查插件列表、客户端、模型名(详见 §8 排错)

---

## Validation(自检清单)

每次回答 OCR 类问题前/后过一遍:

- [ ] 用户装了 `markitdown-ocr`?(`pip show markitdown-ocr`)
- [ ] 用户装了 OpenAI 兼容 SDK?(`openai` / `azure-openai` / 自定义)
- [ ] 用户配了 `OPENAI_API_KEY`(或等价凭据)?
- [ ] Python 代码里**同时**给了 `enable_plugins=True` **与** `llm_client` **与** `llm_model`?(三者缺一 OCR 都被跳过)
- [ ] 模型支持 vision?(不能拿纯文本模型如 `gpt-3.5-turbo`)
- [ ] 走 Azure OpenAI 时 `azure_endpoint` 没带尾部 `/`、`api_version` 有效?
- [ ] 处理敏感文档 → 推荐私有化后端(vLLM / Ollama)而非云 API?
- [ ] 没误承诺 CLI 能配 `--llm-client`/`--llm-model`?(这两个 CLI 不存在,需要 Python 包装)

---

## Gotchas

按命中频率从高到低:

1. **CLI 没有 `--llm-client` / `--llm-model`** — 任何"命令行直接启用 OCR"的说法都是错的。要么写 Python 包装,要么告诉用户走 Python API。`__main__.py` 的 argparse 注册表确认。
2. **`enable_plugins=True` 漏写** — MarkItDown 默认 `enable_plugins=False`,插件根本不会注册。**必带**。
3. **漏 `llm_client` 或 `llm_model`** — 插件"仍会注册"(无 OCR service),但实际转换静默跳过 OCR。检查清单:三个参数**必须**都给。
4. **LLM 失败被静默吞掉** — `_ocr_service.py::extract_text` 把异常转成 `OCRResult(text="", error=str(e))`;插件的 `convert()` 继续,不抛。表现:某张图的 OCR 块缺失,但文档其它部分 OK。**没有任何 stderr 警告**。
5. **PPTX 描述优先于 OCR** — 若 LLM 返回了"图像描述",OCR 仅作 fallback。这意味着:同一张图,不同调用可能得到不同文本(描述 vs OCR)。
6. **XLSX 位置上下文丢失** — 图片被统一追加在数据表后(`### Images in this sheet:`),不与行交错。表格密集场景慎用。
7. **扫描 PDF 整页 300 DPI 渲染** — 比"嵌入小图"贵很多;50 页扫描件 ≈ 50 次 vision 调用,token 成本高。
8. **OCR 块靠正则识别** — 输出格式 `*[Image OCR]\n…\n[End OCR]*` 是公开契约;后处理依赖它时,改了插件源码会让正则失效。
9. **本地视觉模型可能不支持 `data:` URI** — vLLM / Ollama 部分模型对 Base64 内嵌图片支持不稳;若失败,确认模型本身支持。
10. **Azure OpenAI `api_version` 不匹配** — deployment 与 SDK 版本必须兼容;用太新的版本号可能 404。
11. **每张图一次 LLM 调用 = 高并发风险** — 100 张图直接用线程池可能撞 OpenAI RPM/TPM 限制。429 被静默吞掉表现为"图片没 OCR",不易察觉。
12. **OCR 块污染正文摘要** — 想"只看正文"必须先正则剥离 `*[Image OCR]…[End OCR]*`,否则 LLM 会把 OCR 文本当正文引用。
13. **`gpt-3.5-turbo` 不支持 vision** — 用户填错模型名时,API 会 400,但被插件静默吞;表现是 OCR 块全没。
14. **缺 `Pillow` 或 `PyMuPDF`** — `markitdown-ocr` 依赖列表里已有;若手贱 `pip install markitdown-ocr --no-deps` 会缺这些,导致 `import` 直接报错。
15. **大文件单次 memory spike** — 整 PDF 走 `convert_local` 时,PyMuPDF 渲染 + base64 编码同时在内存中;几十 MB 图片会爆内存。

---

## 1. 是什么 / 解决什么问题

**MarkItDown 内置**的 PDF/DOCX/PPTX/XLSX 转换器**不会**对内嵌图片或扫描页做 OCR——它们只取"已可解析的文本"。如果文档里有图片、扫描页、被转成图像的文字,默认输出里那块就是空的。

**`markitdown-ocr` 插件**接管上述四个内置转换器(优先级 `-1.0`,比内置 `0.0` 更高),通过 **LLM Vision**(任何支持图像输入的 OpenAI 兼容模型)抽取内嵌图片中的文字并按格式插回 Markdown 流。

**核心特性**:

- ✅ PDF / DOCX / PPTX / XLSX 全部支持
- ✅ 扫描 PDF 自动整页 OCR 回退(每页 300 DPI 渲染后整页送 LLM)
- ✅ DOCX 图片关系图完整保留(段落/标题/表格流不被破坏)
- ✅ PPTX 按"上→左"阅读顺序处理图片/占位符/组内图片
- ✅ XLSX 按图像 anchor 还原列/行字母坐标,图片统一追加在表格后
- ✅ 输出用 `*[Image OCR]…[End OCR]*` 包裹每个 OCR 块,便于后处理
- ❌ 不引入新的 ML 库或二进制依赖(依赖已经在内置转换器里)
- ⚠️ LLM 调用失败时**静默跳过**,转换继续

## 2. 安装

```bash
pip install markitdown-ocr
# 同时确保有可用的 OpenAI 兼容客户端
pip install openai            # 官方 OpenAI
# 或
pip install azure-openai      # Azure OpenAI(若走 Azure)
```

源码安装(开发/调试):

```bash
git clone https://github.com/microsoft/markitdown.git
cd markitdown/packages/markitdown-ocr
pip install -e .
```

依赖项(自动拉取):`markitdown>=0.1.0`、`pdfminer.six`、`pdfplumber`、`PyMuPDF`、`mammoth`、`python-docx`、`python-pptx`、`pandas`、`openpyxl`、`Pillow`。

## 3. 配置 — LLM 客户端与模型

**关键约束**:插件本身**不读任何 API key**——它从 `MarkItDown(llm_client=…, llm_model=…, llm_prompt=…)` 拿客户端与模型,认证完全由客户端负责(走其自身的环境变量/凭据链)。

### 3.1 OpenAI(默认)

```bash
export OPENAI_API_KEY=sk-...
```

```python
from openai import OpenAI
client = OpenAI()  # 自动读 OPENAI_API_KEY
```

### 3.2 Azure OpenAI

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],    # 或读其它环境变量
    azure_endpoint="https://<res>.openai.azure.com/",
    api_version="2024-02-01",
)
```

### 3.3 其它 OpenAI 兼容服务(Gemini / Ollama / vLLM / LM Studio / DeepSeek-VL 等)

任何实现了 `client.chat.completions.create(model=…, messages=[…])` 接口的对象都能传进去,**前提是它支持 vision 输入**。示例:

```python
import openai
client = openai.OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ["GOOGLE_API_KEY"],
)
# 之后正常使用,llm_model="gemini-2.0-flash" 等
```

更完整的兼容客户端矩阵见 [backends/compatible-clients.md](references/backends/compatible-clients.md);实战脚本见 [examples/backends/azure-and-local.md](examples/backends/azure-and-local.md)。

### 3.4 缺少 `llm_client` 时的行为

`_plugin.py::register_converters` 中:

```python
if llm_client and llm_model:
    ocr_service = LLMVisionOCRService(client=…, model=…, default_prompt=…)
```

如果 `llm_client` 或 `llm_model` 缺失,插件**仍然注册**(注册的是无 OCR service 的版本),但实际转换时**静默跳过 OCR**,回退到内置转换器的行为。验证插件存在:

```bash
markitdown --list-plugins
# 应当看到: ocr   (package: markitdown_ocr)
```

## 4. Python API — 三种典型用法

### 4.1 最简(OpenAI + gpt-4o)

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,        # ← 必须
    llm_client=OpenAI(),        # ← 必须
    llm_model="gpt-4o",         # ← 必须
)
result = md.convert("document_with_images.pdf")
print(result.markdown)
```

### 4.2 Azure OpenAI

```python
from markitdown import MarkItDown
from openai import AzureOpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint="https://<res>.openai.azure.com/",
        api_version="2024-02-01",
    ),
    llm_model="gpt-4o",
)
print(md.convert("report.docx").markdown)
```

### 4.3 自定义 Prompt

```python
md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
    llm_prompt="Extract all text from this image, preserving table structure.",
)
```

## 5. CLI — 当前没有原生 `--llm-client` / `--llm-model`

> ⚠️ **重要**:`markitdown` 当前 CLI(`__main__.py`)未注册 `--llm-client` / `--llm-model`。要通过命令行启用 OCR,**用 Python 写一个 3 行包装**即可。

### 5.1 推荐做法:shell 包装

写一个小文件 `mdocr`:

```python
#!/usr/bin/env python3
# mdocr — 命令行包装 markitdown-ocr
import os, sys, argparse
from markitdown import MarkItDown

ap = argparse.ArgumentParser()
ap.add_argument("filename")
ap.add_argument("-o", "--output")
ap.add_argument("--model", default=os.environ.get("MD_OCR_MODEL", "gpt-4o"))
ap.add_argument("--prompt", default=None)
args = ap.parse_args()

client = OpenAI()  # ← 替换为你要用的客户端构造
md = MarkItDown(
    enable_plugins=True,
    llm_client=client,
    llm_model=args.model,
    llm_prompt=args.prompt,
)
# 注意:请在环境变量 OPENAI_API_KEY / AZURE_OPENAI_API_KEY / OLLAMA_HOST 等中配置凭据
# 切勿把真实 key 写进源代码或 commit。
result = md.convert(args.filename)
sys.stdout.write(result.markdown)
if args.output:
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(result.markdown)
```

```bash
chmod +x mdocr
./mdocr scan.pdf -o scan.md --model gpt-4o
```

### 5.2 一行 `python -c`(临时用)

```bash
python -c "
from markitdown import MarkItDown
from openai import OpenAI
import sys
md = MarkItDown(enable_plugins=True, llm_client=OpenAI(), llm_model='gpt-4o')
sys.stdout.write(md.convert(sys.argv[1]).markdown)
" scan.pdf > scan.md
```

## 6. 格式级行为差异(OCR 结果插回方式)

| 格式 | OCR 块插回位置 | 说明 |
|------|--------------|------|
| **PDF** | 行内(穿插在周围文本中),按"上下垂直阅读顺序"插入;扫描页整页送 LLM | 嵌入图像按 `page.images` / page XObjects 抽取;malformed PDF 自动改用 PyMuPDF 整页渲染 |
| **DOCX** | OCR 在 "DOCX→HTML→Markdown" 流水线**之前**执行;文档流(标题/段落/表格)100% 保留 | 通过 `doc.part.rels` 抽取图片关系 |
| **PPTX** | 按幻灯片内"上→左"阅读顺序;若 LLM 返回"图像描述"则优先用描述,OCR 仅作 fallback | 支持 Picture shape、placeholder shape、组内图片 |
| **XLSX** | 每张工作表的图片统一追加在数据表后,标注为 `### Images in this sheet:` | 位置从图像 anchor 算列字母/行号;**位置上下文会丢失**(与其它三个格式不同) |

**OCR 输出格式**:每块都用 Markdown 强调包裹,方便后处理识别:

```
*[Image OCR]
<抽取到的文字>
[End OCR]*
```

> 想批量剥离 OCR 块、做"只看正文"摘要,可以用一行 sed:
>
> ```bash
> sed -e '/^\*\[Image OCR\]$/,/^\[End OCR\]\*$/d' input.md > cleaned.md
> ```

## 7. 限制与代价(部署前必读)

| 项 | 说明 |
|----|------|
| **每张图片一次 LLM 调用** | 100 张图片 = 100 次 vision 调用,成本随图像数量线性增长 |
| **扫描 PDF 更贵** | 扫描页按 300 DPI 整页送 LLM,占 token 比"嵌入式小图"大很多 |
| **LLM 错误静默** | "If the LLM call fails, conversion continues without that image's text"——失败被吞,需要监控 |
| **PPTX 描述优先** | 若 LLM 返回了"图像描述",OCR 仅作 fallback,最终文本是描述而非原文字 |
| **XLSX 位置丢失** | 图片被追加到表后,不会出现在原本所在单元格附近 |
| **图像 MIME** | OCR 服务用 `stream_info.mimetype` 或 PIL 探测;若都不识别则按 `image/png` |

## 8. 排错速查

| 现象 | 排查 |
|------|------|
| OCR 块一个都没出现 | `markitdown --list-plugins` 看是否含 `ocr`;确认传了 `enable_plugins=True` 和 `llm_client` + `llm_model` |
| 报 `ModuleNotFoundError: markitdown_ocr` | `pip install markitdown-ocr`,或 `pip install -e packages/markitdown-ocr` |
| 报 `ModuleNotFoundError: openai` | `pip install openai` 或换用其它 OpenAI 兼容 SDK |
| OCR 部分图片缺失 | 该次 LLM 调用失败被静默吞掉;加日志/重试,或换更稳定的模型 |
| `BadRequestError: image_url invalid` | 客户端/MIME 不识别;在 `_ocr_service.py` 中确认 `content_type` 推断正确,或换客户端 |
| Azure OpenAI 鉴权失败 | 确认 `api_version` 是该 deployment 支持的版本(如 `2024-02-01`)、`azure_endpoint` 不带尾部 `/` |
| 输出里 data:image 全没了 | 是 MarkItDown 主体的行为,与 OCR 无关——加 `--keep-data-uris`(CLI) 或在 Python API 中传 `keep_data_uris=True` |

## 9. 测试 / 二次开发

```bash
# 跑插件自带的测试套件
cd packages/markitdown-ocr
pytest tests/ -v

# 本地装好后做最小冒烟
python -c "
from markitdown import MarkItDown
from openai import OpenAI
print(MarkItDown(enable_plugins=True, llm_client=OpenAI(), llm_model='gpt-4o').convert('sample.pdf').markdown[:500])
"
```

插件内部机制(注册流程、OCRService 实现细节、各转换器差异)见 [plugin/internals.md](references/plugin/internals.md)。

## 10. 何时跳到兄弟 Skill

| 用户问题 | 跳到 |
|---------|------|
| "MarkItDown 是什么?支持哪些格式?" | `markitdown-awesome` |
| "markitdown 命令怎么用、参数怎么传?" | `markitdown-cli` |
| "我用 Azure Document Intelligence / Content Understanding,不需要 OCR 插件" | `markitdown-cli` 的"Azure 后端"章节 |

## 11. 隐私策略

本 Skill 提供本地文档与示例代码,不收集、存储或传输任何用户数据。**实际 OCR 调用会把你传入的图片内容(可能含敏感信息)发送给所选 LLM 服务商**,请遵守相应服务商的隐私条款与用户所在地区法规。生产部署建议:

- 高敏感文档走私有化 LLM(如本地 vLLM / Ollama + OpenAI 兼容协议)
- 关闭请求日志 / 临时审计

## 12. 参考链接

- 插件 README: <https://github.com/microsoft/markitdown/blob/main/packages/markitdown-ocr/README.md>
- 插件源码入口: <https://github.com/microsoft/markitdown/blob/main/packages/markitdown-ocr/src/markitdown_ocr/_plugin.py>
- OCR 服务抽象: <https://github.com/microsoft/markitdown/blob/main/packages/markitdown-ocr/src/markitdown_ocr/_ocr_service.py>
- MarkItDown 主仓库: <https://github.com/microsoft/markitdown>
- 兄弟 Skill:`markitdown-awesome` — 用 `npx skills add full-stack-skills/document-skills --skill markitdown-awesome` 装好后按 skill 名引用
- 兄弟 Skill:`markitdown-cli` — 用 `npx skills add full-stack-skills/document-skills --skill markitdown-cli` 装好后按 skill 名引用
- 完整安装:`npx skills add full-stack-skills/document-skills`(一次性装齐全部 11 个 skill)