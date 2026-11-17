---
name: markitdown-cli
description: MarkItDown 命令行工具(`markitdown` 命令)的完整使用指南——所有 CLI 参数(`-o/-x/-m/-c/-d/-e/-p/--use-cu/--cu-endpoint/--cu-analyzer/--cu-file-types/--list-plugins/--keep-data-uris`)、输入输出模式(文件/管道/stdin)、管道组合、与 shell 工具链的集成(jq/grep/xargs/tee/find),以及典型场景示例(批量转码、Azure 后端切换、插件启用、流式输入)。当用户询问"markitdown 命令怎么用"、"怎么批量转 PDF"、"怎么把 stdin 流喂进去"、"怎么列出已装插件"、"Azure Document Intelligence CLI 怎么配"时使用本 skill;若涉及 OCR 走 LLM Vision,跳到兄弟 skill `markitdown-ocr`。
license: MIT
---

# MarkItDown CLI 完整使用指南

> 用途明确:让 LLM 能基于本 skill 生成**正确、可复制粘贴**的 `markitdown` 命令行调用。
>
> **离线基线**:基于 `markitdown` 命令的 argparse(见 [`packages/markitdown/src/markitdown/__main__.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/__main__.py))。任何"该参数是否存在"的判断,以源码为准;遇到本文与官方 README 冲突时,**以官方为准**。

---

## When to Use This Skill

✅ **什么时候用本 skill**(纯 CLI / 命令行问题):
- 用户问 "markitdown 命令怎么用?有哪些参数?"
- 用户想批量转 PDF/PPT/Word → Markdown
- 用户想把 stdin 流(管道 / curl 输出)喂给 markitdown
- 用户问"怎么列出已装插件"、"怎么启用插件"
- 用户问 Azure Document Intelligence / Content Understanding 的 **CLI** 配法
- 用户问"CLI 怎么把输出写到文件而不是 stdout"

❌ **什么时候不该用本 skill**:
- 想用 Python API → `markitdown-awesome` 的 `references/api/python-api.md`
- 想做 OCR(嵌入图片 / 扫描 PDF / LLM Vision)→ `markitdown-ocr`
- 想了解 MarkItDown 是什么、支持哪些格式 → `markitdown-awesome`
- 用户已经会 `markitdown`,只是问最佳实践 → 直接给示例,不绕到本 skill

⚠️ **模糊地带**:
- 用户问"OCR 怎么做" → 默认走 `markitdown-ocr`(因为 CLI 当前不支持 LLM 参数)。
- 用户问"怎么转 PDF"但没说场景 → 默认 CLI 路径,但同时提示:若是扫描件,推荐 Azure DI。

---

## Workflow

每次回答 CLI 类问题时,按下面流程走一遍:

### Step 1 — 确认输入与输出

- 输入:`<file>` / `stdin` / `http(s)://…`?
- 输出:`stdout` / `-o out.md` / `tee` 复用?
- 是否有特殊格式需要提示(`-x` / `-m`)?

### Step 2 — 选择后端(默认 / Azure DI / Azure CU)

- 默认(本地):不传 `-d` 也不传 `--use-cu`
- 高质量 PDF/扫描:`-d -e <endpoint>`
- 多模态/结构化字段:`--use-cu --cu-endpoint <endpoint>`

### Step 3 — 选择是否启用插件

- OCR(LLM Vision)→ `-p`,但记得 CLI 没有 `--llm-client`/`--llm-model`,**需要 Python 包装**(见 `markitdown-ocr`)
- 自定义插件 → 同上,`-p` 即可

### Step 4 — 组装命令并自检

对照 [Validation 自检清单](#validation自检清单)走一遍。

### Step 5 — 处理错误

若用户给出 `MissingDependencyException` / `UnsupportedFormatException` 等异常,跳到 §8 排错速查。

### Step 6 — 给下一步建议

输出命令后,补一句:"需要批量 / 集成 CI / Docker,看 [examples/advanced/safe-batch-processing.md](examples/advanced/safe-batch-processing.md)"。

---

## Validation(自检清单)

每条命令生成后,过一遍:

- [ ] `-d` 与 `--use-cu` **没有**同时出现?
- [ ] 用 `-d` 时**必带** `-e <endpoint>`?
- [ ] 用 `--use-cu` 时**必带** `--cu-endpoint <endpoint>`?
- [ ] 从 stdin 读但文件无扩展名 → 加了 `-x` 或 `-m`?
- [ ] 走 HTTP URL → 评估了 SSRF 风险?
- [ ] 输出含非 ASCII → 推荐 `-o out.md` 而非 stdout?
- [ ] 用户装了插件但没启用 → 提示加 `-p`?
- [ ] CLI 没有 `--llm-client` → 没误承诺能从命令行启用 OCR?
- [ ] `--list-plugins` 与"转文件"没在同一命令行?

---

## Gotchas

按命中频率从高到低:

1. **`-d` 与 `--use-cu` 互斥** — argparse 强制 mutually_exclusive_group,两条同时出现直接报错。
2. **`-d` 必须配 `-e`** — 否则 `__main__.py` 主动 `_exit_with_error("Document Intelligence Endpoint is required …")`。
3. **`--use-cu` 必须配 `--cu-endpoint`** — 同上逻辑。
4. **CLI 没有 `--llm-client` / `--llm-model`** — 想从命令行启用 OCR,必须用 Python 包装(详见 `markitdown-ocr`)。**不要编一个不存在的 flag**。
5. **`--list-plugins` 触发即 `sys.exit(0)`** — 与"转文件"在同一命令行组合时,转换逻辑根本不会跑。
6. **从 stdin 读时无扩展名 → 必须 `-x` 或 `-m`** — 否则 `accepts()` 全 False,报 `UnsupportedFormatException`。
7. **`-c` charset 用 codecs.lookup 校验** — 写错会 `_exit_with_error("Invalid charset: …")`;常见可用值:`utf-8`、`utf-16`、`latin-1`、`gbk`(需在系统 codecs 注册)。
8. **CLI 输出中文乱码** — 终端 `LANG != *UTF-8` 时,加 `-o out.md` 落盘。
9. **`--keep-data-uris` 默认不保留** — 输出里 base64 图片会被截掉;若用户需要图,用 `--keep-data-uris`。
10. **HTTP URL 走真实 GET** — `convert_uri` 内部会发请求;SSRF 风险由调用方承担。生产建议用 Python `requests.get()` + `convert_response()`。
11. **大文件内存峰** — `convert_local` 一次性 `open(path, "rb")`,几百 MB 的 PDF 内存可能爆。流式场景用 `convert_stream`。
12. **缺可选依赖** — 报 `MissingDependencyException` 时,按格式 `pip install 'markitdown[<extra>]'` 补,不要省略方括号。
13. **Azure 凭据** — DI/CU 默认走默认凭据链;CLI 里**没有**显式传 key 的选项,凭据由环境/SDK 决定。
14. **`--cu-file-types` 接受逗号分隔字符串** — 写错类型名会 `_exit_with_error("Unknown file type: …")`,与 `ContentUnderstandingFileType` 枚举对齐。
15. **管道断裂会导致 BrokenPipeError** — 用 `markitdown f.pdf | head` 时,MarkItDown 会写完整个 markdown 后 `print` 触发 EPIPE;**不影响结果**,但 `head` 退出码非零会让 `set -o pipefail` 失败。

---

## 1. 最简形态

```bash
markitdown <file>            # 转 stdout
markitdown <file> -o out.md  # 写文件
cat <file> | markitdown      # 从 stdin 读
markitdown < <file>          # 等价写法
```

`<file>` 可以省略:省略时强制从 stdin 读取。
**注意**:走 stdin 时,MarkItDown 不知道真实扩展名,需要用 `-x` 或 `-m` 提示。

## 2. 完整参数清单

| 短参 | 长参 | 类型 | 说明 |
|------|------|------|------|
| `-v` | `--version` | flag | 打版本号退出 |
| `-o` | `--output` | str | 输出文件,缺省写到 stdout |
| `-x` | `--extension` | str | 扩展名提示(可省略前导 `.`)。如:`-x pdf` |
| `-m` | `--mime-type` | str | MIME 提示,如 `-m application/pdf` |
| `-c` | `--charset` | str | 字符集提示,如 `-c utf-8` |
| `-d` | `--use-docintel` | flag | 走 Azure Document Intelligence 后端,需同时配 `-e` |
| `-e` | `--endpoint` | str | Document Intelligence endpoint URL |
| — | `--use-cu` / `--use-content-understanding` | flag | 走 Azure Content Understanding,需 `--cu-endpoint` |
| — | `--cu-endpoint` | str | Content Understanding endpoint |
| — | `--cu-analyzer` | str | 自定义 analyzer ID;缺省时按文件类型自动选 |
| — | `--cu-file-types` | str | 逗号分隔,如 `--cu-file-types pdf,jpeg,mp4` |
| `-p` | `--use-plugins` | flag | 启用 `markitdown.plugin` 入口点发现的第三方插件 |
| — | `--list-plugins` | flag | 列出已装插件,列出后退出 |
| — | `--keep-data-uris` | flag | 输出中保留 `data:image/...;base64,…` URI(默认会被截断) |

**互斥组**:`-d`(`--use-docintel`)与 `--use-cu` 互斥,只能选一个。

## 3. 输入/输出矩阵

| 用法 | 命令模板 | 何时用 |
|------|---------|-------|
| 单文件 → stdout | `markitdown a.pdf` | 想要直接管道传给别的工具 |
| 单文件 → 文件 | `markitdown a.pdf -o a.md` | 最常见的"出文件"模式 |
| stdin → stdout | `cat a.pdf \| markitdown` | 程序化调用、不落中间文件 |
| stdin → 文件 | `cat a.pdf \| markitdown -o a.md` | shell 串联 |
| stdin + 提示 | `cat blob \| markitdown -x pdf` | 文件无扩展名或扩展名错 |
| stdin + MIME | `curl … \| markitdown -m application/pdf` | 抓远程后再转 |
| HTTP URL | `markitdown https://example.com/doc.html` | URL 在 CLI 里直接传会被解析为 URI |

> CLI 目前没有 `-i/--input` 参数,只能靠 stdin 或 `<file>` 占位。

## 4. 输出控制

- **stdout 编码容错**:`_handle_output()` 会用 `sys.stdout.encoding` + `errors="replace"` 写,**不会因为终端编码崩溃**。
- **超大输出**:MarkItDown 默认一次性 `print(result.markdown)`,不要把它丢到日志文件里。建议加 `-o`。
- **图片 data URI**:`--keep-data-uris` 控制是否在输出 Markdown 中保留 `data:image/...;base64,…`(默认会被截掉以减小体积)。

## 5. 插件管理

```bash
# 看装了哪些插件
markitdown --list-plugins
# 输出类似:
# Installed MarkItDown 3rd-party Plugins:
#   * ocr              (package: markitdown_ocr)
#   * my-plugin        (package: my_pkg)
# 若没有:打印 "  * No 3rd-party plugins installed."

# 启用插件
markitdown scanned.pdf -p
# 加 LLM 参数配合 markitdown-ocr:
markitdown scanned.pdf -p --llm-client openai --llm-model gpt-4o
```

⚠️ `markitdown --list-plugins` 与 `-p/--use-plugins` 不冲突——但 `__main__.py` 中 `--list-plugins` **触发后立即 `sys.exit(0)`**,所以它和"转文件"不能在同一命令行组合。

### 5.1 通过环境变量配置 OpenAI 兼容客户端(配合 markitdown-ocr)

```bash
export OPENAI_API_KEY=sk-...
markitdown scanned.pdf -p --llm-client openai --llm-model gpt-4o
```

> ⚠️ **注意**:`__main__.py` 当前的 argparse **并未注册 `--llm-client` 与 `--llm-model` 选项**(它们仅在 Python API `MarkItDown(llm_client=…, llm_model=…)` 中可用)。要通过 CLI 启用 OCR,目前最稳妥的方式是写一个 3 行 Python 包装(见 `markitdown-ocr` skill)。**官方未来若加入 CLI 选项,优先遵循官方说明**。

## 6. Azure 后端切换

### 6.1 Document Intelligence(`-d -e`)

```bash
markitdown scan.pdf -d -e "https://<resource>.cognitiveservices.azure.com/"
```

适用:高质量 PDF、扫描件、表格抽取。需要 `pip install 'markitdown[az-doc-intel]'`,且环境需能访问该 endpoint(Azure 凭据走默认链)。

### 6.2 Content Understanding(`--use-cu --cu-endpoint`)

```bash
# 自动选 analyzer(按文件类型:documentSearch/videoSearch/audioSearch)
markitdown report.pdf --use-cu --cu-endpoint "https://<cu>.services.ai.azure.com/"

# 自定义 analyzer
markitdown invoice.pdf --use-cu \
  --cu-endpoint "https://<cu>.services.ai.azure.com/" \
  --cu-analyzer "my-invoice-analyzer"

# 仅对部分类型启用 CU
markitdown mixed_files/ --use-cu \
  --cu-endpoint "https://<cu>.services.ai.azure.com/" \
  --cu-file-types pdf,jpeg,mp4
```

适用:多模态(文档/图像/音频/视频)、需要结构化 YAML front matter、定制分析器。

完整对照(CLI ↔ Python API ↔ 服务端点)见 [azure/endpoint-matrix.md](references/azure/endpoint-matrix.md);实战脚本见 [examples/azure/azure-backends.md](examples/azure/azure-backends.md)。

## 7. 典型工作流示例

### 7.1 批量把目录 PDF 转 Markdown

```bash
find ./inbox -name '*.pdf' -print0 | while IFS= read -r -d '' f; do
  out="./md/$(basename "${f%.pdf}").md"
  markitdown "$f" -o "$out"
done
```

### 7.2 配合 `xargs` 并行(谨慎使用)

```bash
find ./inbox -name '*.pdf' -print0 \
  | xargs -0 -n1 -P4 -I{} sh -c 'markitdown "{}" -o "./md/$(basename "{}" .pdf).md"'
```

> ⚠️ 部分 PDF 处理时占用大量内存与网络 IO,并行度不宜超过 CPU 数。

### 7.3 配 `jq`/`grep` 做后续过滤

```bash
# 把 PDF 转 Markdown,然后保留所有 "##" 开头的章节
markitdown report.pdf | grep -E '^##' > outline.md
```

### 7.4 把抓到的网页存为 Markdown

```bash
curl -sL "https://example.com/article.html" \
  | markitdown -m text/html \
  > article.md
```

### 7.5 Docker 一行命令

参考 `Dockerfile`(`docker build -t markitdown:latest .` 后):

```bash
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
# 等价于:
docker run --rm -v "$PWD":/data markitdown:latest /data/your-file.pdf -o /data/output.md
```

更多批量 / CI / Docker 实战见 [examples/advanced/workflows.md](examples/advanced/workflows.md) 与 [examples/advanced/safe-batch-processing.md](examples/advanced/safe-batch-processing.md)。

## 8. 排错速查

| 现象 | 排查命令 / 思路 |
|------|---------------|
| 报 `MissingDependencyException` | `pip install 'markitdown[对应特性]'`(如 `[pdf]`/`[docx]`/`[pptx]`) |
| `UnsupportedFormatException` | 用 `file <path>` 看真实类型,加 `-x`/`-m` 提示;或确认装了对应 extras |
| 输出中文乱码 | 确保终端 `LANG=*UTF-8*`,或加 `-o out.md` 避免终端编码问题 |
| 走 `-d` 但报错 endpoint 缺失 | CLI 已强制要求 `-e`;若仍报"endpoint required",检查是否同时传了 `-p`,有时需要重排参数顺序 |
| 走 `--use-cu` 但报错 analyzer 不存在 | 先用默认自动选择(不传 `--cu-analyzer`),确认 endpoint 可达 |
| 输出里 data:image… 全没了 | 加 `--keep-data-uris` |
| 装了插件但 `convert` 没生效 | 用 `markitdown --list-plugins` 确认插件被识别;再确认加了 `-p` |
| OCR 完全没跑出来 | 走 `markitdown-ocr` skill —— 必须经 Python API 注入 `llm_client` |

## 9. 安全注意

- MarkItDown 用当前进程权限做 I/O。**不要**把任意 URL 直接喂给 `markitdown https://...`,否则 SSRF 风险由调用方承担。
- 容器场景务必限定 `--user` 与 `--read-only` 卷挂载。

## 10. 何时跳到兄弟 Skill

| 用户问题 | 跳到 |
|---------|------|
| "MarkItDown 是什么、支持哪些格式、架构怎么搭?" | `markitdown-awesome` |
| "怎么用 LLM(GPT-4o / Azure OpenAI)做 OCR、扫描 PDF、嵌入图片 OCR?" | `markitdown-ocr` |
| "怎么用 Python API 而不是 CLI?" | `markitdown-awesome` 的 `references/api/python-api.md` |

## 11. 隐私策略

本 Skill 仅提供本地文档与示例,**不收集、存储或传输任何用户数据**。命令调用与 Azure endpoint 通信由用户在自己的环境中发起,隐私责任由用户承担。

## 12. 参考链接

- [官方 README](https://github.com/microsoft/markitdown)
- [官方 argparse 源码](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/__main__.py)
- [Dockerfile](https://github.com/microsoft/markitdown/blob/main/Dockerfile)
- 参数速记:本仓库内的 `references/cli/cheatsheet.md`
- 兄弟 Skill:`markitdown-awesome` — 用 `npx skills add full-stack-skills/document-skills --skill markitdown-awesome` 装好后按 skill 名引用
- 兄弟 Skill:`markitdown-ocr` — 用 `npx skills add full-stack-skills/document-skills --skill markitdown-ocr` 装好后按 skill 名引用
- 完整安装:`npx skills add full-stack-skills/document-skills`(一次性装齐全部 11 个 skill)