---
name: audit-report-checker
description: 检查审计报告（财务报表 + 附注），发现勾稽错误、加总错误、文本格式问题。用于"检查审计报告/勾稽验证/报表核对/报告核查/数字核对/加总核对/报表平衡/审计报告复核/报告校对"。即使用户只说"帮我检查这份审计报告""看看这个报告有没有错""核对下报表数字"也应触发。支持分体式（报告+附注分文件）与合体式（单文件）报告，支持 Word/PDF/扫描件/图片报表，覆盖 50-150 页合体大报告，输出 7 sheet Excel + Markdown 复核报告。算术 100% 走代码计算，AI 负责语义定位与结构判断。
metadata:
  author: nigo
  version: "1.0.0"
slug: nigo-audit-report-checker
displayName: 审计报告复核工具
summary: 检查审计报告（财务报表+附注），发现勾稽错误、加总错误、文本格式问题，支持 Word/PDF/扫描件，输出 7 sheet Excel + Markdown 复核报告。
license: MIT
---

# 审计报告核查

> 作者：nigo（公众号：逆行的狗）
> 版本：1.0.0

检查审计报告（财务报表 + 附注），发现勾稽错误、加总错误、文本格式问题。Claude 是主控——负责语义理解（定位报表、理解附注章节、判断列含义、标注表格结构），代码负责确定性算术（求和、核对、reconcile）。两者分工，消除旧工具"硬拆分 + 关键词匹配"导致的系统性误报。

## 最重要的一条原则：算术绝不手算

LLM 直接做数值加减会算错，且无法复现——审计核查中算错等于致命。所有数值计算，哪怕只是三个数相加，都调用 `scripts/calculator.py`。AI 只决定"传哪些数""哪个等于哪个"，代码算出结果。

正确做法：
```
# 从报表/附注提取出数字后，调 calculator 验算
python3 scripts/calculator.py check "113,157,711.68" "113,157,711.68"   # 核对相等
python3 scripts/calculator.py sum "1,234.56 5,678.90 100.00"            # 求和
python3 scripts/calculator.py reconcile "100" "50" "30" "120"           # 期初+增-减=期末
```

错误做法：
```
# 心算"流动资产合计 = 货币资金 + 应收账款 + ..."  ← 会算错，且别人无法核验
```

calculator 支持千分位逗号、括号负数、横线（=0）、全角字符、万元单位，容差默认 0.01，用 `round(diff, 6)` 避免浮点边界误判。这是上一版已验证有效的原则，保留。

---

## 工作流

### Step 0 — 选检查深度（scope）

开始前用 `question` 工具问用户两件事：检查深度（单选）+ 检查类型（多选，可空则按深度档执行）。

**三档深度**：

| 档位 | 覆盖范围 | 耗时 | 适用 |
|---|---|---|---|
| 快速检查 | 四表间勾稽 + 格式（公司名/页码/页眉） | 几分钟 | 初筛、只关心报表平衡 |
| 标准检查（默认） | 快速 + 表内横加竖加 + 高频表注勾稽 + 文本（错别字/病句） | 十几分钟 | 日常复核，覆盖常见错误 |
| 深度检查 | 标准 + 附注所有变动表 reconcile + 跨科目勾稽 + AI 结构标注全表 | 半小时以上，token 消耗大 | 重大报告、终稿复核 |

用户不选就默认标准。选深度检查时先提示 token 消耗较大让用户确认（128 页报告深度检查可能消耗很多）。

**检查类型多选**：勾稽 / 横加竖加 / 表注 / 文本 / 格式。用户可自由组合覆盖深度档（多选全部 ≈ 深度检查）。

为什么要分档：审计师多数时候只需快速验证勾稽，无差别深度检查既慢又费 token。scope 让用户知情选择，按需触发。

**附注-only 自动调整**：若识别到文档只有附注、无四表（如盛屯/博达新材的纯附注 Word），自动跳过报表间/表注勾稽，聚焦附注内勾稽 + 横加竖加 + 文本格式，并告知用户调整了范围。详见后文"附注-only"。

**DeepSeek 模型选择（启用 AI 时执行）**：标准/深度检查默认启用 DeepSeek 加速（文本错别字、附注表结构标注、warning 二次复核）。涉及 AI 时，问完深度+类型后先选模型，避免 reasoning 模型拖垮批处理：

1. 检查 key 有效性：`python3 scripts/ai_worker.py --test-check-key`（读 ~/.deepseek/config.json；无 key 则全程走 `--no-ai` 纯代码）
2. 查可用模型：`python3 scripts/ai_worker.py --test-list-models`（DeepSeek 503 服务繁忙时可能查不到，可跳过用默认）
3. 用 `question` 让用户选模型，**默认推荐 flash 类模型**（非 reasoning，单请求延迟低，适合大批量并发；reasoning 类如 v4-flash 单请求 25s+ 会拖垮批处理）。用户无偏好直接用 flash。
4. 选定后 run_check 加 `--model <选定>` 传入，或写入 ~/.deepseek/config.json 的 model 字段持久化。

**降级原则**：DeepSeek API 服务繁忙(503)/限流属外部问题。多次失败时降级 `--no-ai`（纯代码 L1+scan+词库），文本/标注/warning 复核由 Claude 终审兜底（Step 5 本就要求 Claude 复核，不完全依赖 API）。

### Step 1 — 解析文档

```bash
python3 scripts/parse_report.py "<文件或目录>" -o <输出目录>
```

脚本四路自动分流，按文档类型和内容特征选最佳提取路径：
- PDF 文本型（首页文本 > 50 字）→ pdfplumber，数字 100% 精确
- PDF 扫描型 → mineru 云端 API（`extract --model vlm`），数字需人工复核
- Word 文本表格为主 → python-docx，精确
- Word 图片报表（inline_shapes 偏多）→ mineru 云端 API

**Word/PDF 双路（重要）**：实际场景大部分是 Word 报告。parse 对同 basename 的 .docx/.pdf **优先 .docx**（去重，Word 表格精确无断字）；无 Word 才用 PDF。两路分开处理：
- **Word 路（.docx）**：python-docx 提取 table 对象→markdown（实测金星90/博达87表全成功）+ 段落文本；**章节定位**（附注五-N 科目，Word 无固定页码）；table 自动归属 chapter（Heading1 大章节 + Heading2/短文本明细）。伪表格（非 table 对象的制表位排版，少数）AI 兜底。
- **PDF 路（.pdf）**：pdfplumber + **页码定位**（page=N，超链接可点击）。

定位差异：Word 用章节（"附注五-3 应收账款"），PDF 用页码（"第N页"）。result 的 chapter（Word）/ page（PDF）字段区分，export 自动适配。

输出两个文件：
- `report.md`：全文 markdown，每段用 `<!-- SOURCE file="..." page=N method=... -->` 标注来源页码和提取路径
- `extracted_tables.json`：原始二维表格（headers + rows），不做列映射、不做报表分类、不做续表合并

解析层只输出原始数据，报表定位、附注识别、列含义判断全部由 Claude 在后续步骤用语义完成。这是消除旧工具"拆分匹配错误"的核心——parse 层不越界做本该人做的事。提取策略原理见 `references/extraction.md`。

mineru 是云端 API，数据会上传 mineru.net。审计报告含敏感财务数据，首次走 mineru 路径前要告知用户并获得知情同意。详见 `references/mineru_usage.md`。

### Step 2 — 理解文档结构（语义，不靠关键词）

读 `report.md`，理解整体结构：
- 编制单位、会计期间
- 报告类型：合并报告（含合并 + 母公司共 8 张表）还是单体（4 张）？通过看是否有"母公司"字样和报表数量判断，不靠硬编码关键词字典
- 四张报表的位置（合并资产负债表/利润表/现金流量表/所有者权益变动表，及母公司版本）及其页码范围
- **合并报告同名报表会重复**：合并报告里"资产负债表""所有者权益变动表"等标题通常**出现两次**——第一次是合并口径、第二次是母公司口径，表头往往**都不带"合并"/"母公司"前缀**，靠出现顺序（先合并后母公司）和编制单位行区分。**两套都要提取**，漏掉母公司 4 张表会让母公司层面的勾稽完全缺失。判断方法：同名报表在 report.md 中出现 ≥2 次 → 合并报告，按顺序分别归为合并/母公司。
- 附注章节结构——每章讲哪个科目（如"附注三、货币资金"讲货币资金）
- 是否附注-only（无四表）→ 走附注-only 分支
- **图片报表页检测（重要）**：读 report.md 时留意是否有**连续多页文本为空白**。审计报告中四表（资产负债表等）常被做成图片嵌入 PDF，pdfplumber 对这些页提取为空白（实测盛屯 page 7-16 共10页空白=四表全是图片）。若 parse_report 的 report.md 已标注 `<!-- WARNING: ... 为图片/扫描页 -->`，直接据此处理；否则自己扫描各页文本量。发现四表区域空白时：
  1. 对该页范围用 mineru 云端 OCR 重新提取：`mineru-open-api extract "<报告.pdf>" --pages 7-16 -o <目录> --model vlm --language ch`（需先 `mineru-open-api auth` 配 token，见 references/mineru_usage.md，含数据上传云端隐私提示）
  2. OCR 结果（md）合并回 statements 提取
  3. mineru 不可用时，在报告中明确标注"四表为图片，pdfplumber 未能提取，本次未执行报表间勾稽，建议人工复核或配 mineru token 重跑"——**不要假装做了**

识别同义科目变体靠语义理解，不做映射表：股东权益 = 所有者权益、股本 = 实收资本、股东权益变动表 = 所有者权益变动表。为什么用语义而不是关键词字典：每遇到一个新报告格式就要加规则，关键词爆炸不可持续；Claude 一次调用就能理解，且能处理变体。

**生成 note_map.json（表注勾稽的定位基石，Step 2 必做）**：理解附注结构时，一次性生成「科目→附注明细表」精确映射 `note_map.json`（写入 parse 输出目录）。这是三层分工架构的**定位层**——Claude 语义定位（准、只做一次、低 token），取数/算术交给代码（DeepSeek locate + calculator）。

为什么定位必须 Claude 做：旧工具靠正则匹配标题 + 页码邻近定位，在①标题格式多样 ②同页多科目 ③续表跨页 上系统性失败（详见 `旧报告检查工具_定位研究.md` 的 4 大根因）。Claude 一次语义理解就能准确定位到表级别。

格式（`{科目: {...}}`）：
```json
{"货币资金": {"table_ids": [220], "pages": [16], "field": "期末余额", "formula": "期末余额", "note": "报表数=附注期末余额"},
 "应收账款": {"table_ids": [221,222], "pages": [18,19], "field": "账面价值", "formula": "账面余额-坏账准备=账面价值", "note": "报表数=附注账面价值"}}
```
- `table_ids`：该科目附注明细涉及的表 id（附注文件范围，**绝不混入资产负债表/利润表等报表表**，否则表注勾稽会"自己比自己"）
- `field`：报表数等于附注哪个字段（直接取，如"账面价值"/"期末余额"）
- `formula`：取数口径公式（field 取不到时按此运算，如"账面余额-坏账准备"）
- 定位方法（表 name 常为空，靠多重交叉）：科目章节 page 区间 + 该区间内表 page + headers 内容 + 章节实际文字
- 最低覆盖：标准检查至少 8 科目（货币资金/应收账款/应收票据/预付款项/存货/固定资产/营业收入/应付账款），深度检查覆盖全部报表列示科目。`subjects_index.json`（scan 生成的科目→候选表粗索引）可作为定位参考/校验，但精确定位以 Claude 生成的 note_map 为准

**生成 manifest.json（四表提取的结构契约，Step 2 必做）**：理解四表在文件里的位置/列布局后，写成 `manifest.json`（写入 parse 输出目录）。这是三层分工架构的**结构契约层**——Claude 语义识别结构（准、只做一次），抽数交给 apply_manifest 纯机械执行（零猜测、新格式改 JSON 不改代码）。

**自动生成优先**：`run_check --auto-manifest --auto-note-map` 时 DeepSeek 并发自动生成 manifest.json 和 note_map.json（看 sheet 表头/附注表内容判断列布局/科目归属），代码做结构性校验 + 回原文核对降错。自动生成失败或校验大量不过→回退 Claude 手写（有模板库）。

为什么用 manifest 不靠代码猜：天邑列布局(B/E/F) vs Macko(A/C/D) 不同、Macko 母公司 BS 主表/续表列布局不同、续表项目名带空格（"负 债 合 计"）、非标准名（"股东权益合计"）——每遇到一个新格式，代码猜列/猜 sheet/硬编码 ALIAS 都会崩。manifest 把这些差异声明在 JSON 里，apply_manifest 按声明抽数。

格式（详见 `references/manifest_template.md`，含 4 份报告的 manifest 样例）：
```json
{
  "report_format": "merged_docx | split_xlsx | split_docx | split_pdf",
  "company": "...", "period": "...",
  "files": {"文件名": {"role": "statements|notes|opinion|cover", "loader": "xlsx|docx|pdf|doc"}},
  "statements_map": {
    "合并资产负债表": {
      "source": "文件名", "loader": "xlsx|docx|pdf",
      "sheets": ["sheet名"], "source_table": "表名(docx/pdf按此在extracted_tables定位)",
      "kind": "linear | matrix",
      "item_col": 0, "current_col": 2, "prior_col": 3,
      "field_aliases": {"股东权益合计": "所有者权益合计"},
      "merge_into": null
    }
  }
}
```
- `files.role`+`loader`：分体式文件角色（报表/附注/正文/封面）+ 读取器（xlsx=openpyxl / docx,pdf=读extracted_tables / doc=textutil转）
- `item_col/current_col/prior_col`：列布局（看 dump 确定，不猜）
- `sheets`+`merge_into`：BS 续表/分段合并（同表不同列布局时分两段，merge_into 合并）
- `source_table`：docx/pdf 时按表名/内容在 extracted_tables 定位四表（表 name 常为空，靠内容匹配"资产总计"+"流动资产合计"=BS）
- `field_aliases`：项目名标准化（"股东权益合计"→"所有者权益合计"）
- `kind: linear|matrix`：权益变动表矩阵结构（sheets_main/sheets_prior + value_col）

生成方法：Claude 看每个报表文件的 dump（xlsx 的 sheet 名+表头+前3行 / docx 的 extracted_tables 四表名+列）后手写 manifest（3-5 分钟）。Macko/天邑/巨东/清研的 manifest 已在各自 parse_output 目录，可作为模板。

### Step 3 — 提取 statements.json（apply_manifest 机械执行）

用 Step 2 的 manifest.json，调 apply_manifest 纯机械抽数：

```bash
python3 scripts/apply_manifest.py <parse输出目录>/manifest.json -o statements.json
```

apply_manifest 读 manifest 的 statements_map，按声明的 `source`+`loader`（xlsx 读 sheet / docx,pdf 读 extracted_tables 按 source_table 定位）+ `item_col/current_col/prior_col` 抽数，套 `field_aliases` 标准化项目名，处理 `merge_into` 分段合并，产出 statements.json。**零猜测、零改代码**——所有格式差异已在 manifest 声明。

产物格式（与 calculator_rules 匹配）：
```json
{
  "合并资产负债表": {"流动资产合计": {"current": "113,157,711.68", "prior": "..."}, "资产总计": {"current": "...", "prior": "..."}},
  "合并利润表": {...},
  "合并现金流量表": {...},
  "合并所有者权益变动表": {...},
  "母公司资产负债表": {...}, ...
}
```

**字段名必须精确**：`calculator_rules` 按字段名匹配（如 `"期末现金及现金等价物余额"`），字段名不一致会导致 L1 检查报"缺少必要项目"。提取前先查必需字段清单：

```bash
python3 scripts/calculator_rules.py
```

报表原文项目名与清单不一致时，**在 manifest 的 field_aliases 里声明映射**（如"股东权益合计"→"所有者权益合计"、"负债和股东权益总计"→"负债和所有者权益总计"），不要改代码。

### Step 4 — 代码侧检查（含 scan 代码验算）

```bash
python3 scripts/run_check.py <parse输出目录> \
  --statements <parse输出目录>/statements.json \
  --note-map <parse输出目录>/note_map.json \
  --scope <scope> --scan --use-ai -o <parse输出目录>/results.json
```

说明：
- `--statements` 和 `--note-map` 支持相对路径，脚本会优先相对于 `<parse输出目录>` 解析；如果找不到会给出明确报错。
- 建议命令中写绝对路径或 `<parse输出目录>` 前缀，避免不同工作目录下的路径歧义。

可选参数（用于提速/跳过已跑过的慢步骤）：
- `--max-workers N`：DeepSeek 并发数（默认 60）
- `--skip-annotation`：跳过 AI 结构标注（复用本地 `annotations_cache.json`）
- `--skip-text-ai`：跳过 AI 文本错别字/病句检查
- `--skip-ai-review`：跳过 DeepSeek 对 warning/error 的预复核（默认执行，最终终审仍由 Claude Step5 完成）

脚本执行确定性检查（不依赖 LLM），**`--scan` 必加**——它让代码分担横加竖加的粗活，大幅减轻你在 Step 5 的负担：

**`--use-ai` 说明（默认启用）**：
- **默认 `--use-ai`**：启用 DeepSeek 并发（**4 场景**：①文本错别字 ②附注表结构标注 ③**表注勾稽+附注reconcile**（按 Step2 的 note_map 定位→locate 取数→calculator 比较）④warning 预复核；均批量化 + 并发默认 60）。需 DeepSeek API key + 选定 flash 类模型（见 Step 0）。文本检查（错别字/病句）和表注勾稽取数只有 --use-ai 能自动执行，纯代码扫描覆盖不到。`--note-map` 不传时默认读 `<input_dir>/note_map.json`（Step2 生成）。
- **可选 `--no-ai`**：纯代码扫描（无文本 AI 检查），DeepSeek 服务繁忙/无 key 时降级用。此时文本检查只走内置词库，结构标注/warning 复核由 Claude 在 Step 5 手动完成。
  - 代码自动降级点：`run_check.py` 在 AI 结构标注（`run_check.py:2368-2400`）、表注勾稽（`run_check.py:2533-2562`）、文本错别字（`run_check.py:2473-2510`）、warning 二次复核（`run_check.py:2640-2670`）四个场景均捕获 API/取数异常，失败时跳过该场景并在 `results.json` 中生成降级提示，不会中断主流程。
- **模型选择**：`--model <name>` 传入；不传则用 ~/.deepseek/config.json 的 model 字段。优先 flash 类（非 reasoning），详见 Step 0。

**执行的检查**（按 scope）：
- **L1 报表间勾稽**：调 `calculator_rules.py` 四函数，验资产=负债+权益等恒等式
- **页码连续性**、**公司名一致性**、**金额单位**、**错别字词库粗筛**
- **scan 代码验算**（`--scan`）：
  - **竖加验算**：含"合计/小计"行的附注表，代码 sum 明细=合计（排除所有合计/小计/总计行和"其中:"子项）。金星 301 张表能代码验算 64 张，通过的直接记 info（你不用再做这些表）
  - **横加验算**：列名匹配已知模式（账面余额-坏账准备=账面价值、期初+增加-减少=期末、原价-折旧-减值=价值）
  - **通过记 info（减负）**，不平记 **warning**（可能特殊表结构，需你在 Step 5 用 AI 结构标注复核，区分真错 vs 特殊结构）
  - 额外输出 `candidates.json`（代码无法判断的变动表/复杂横加表清单，留给你在 Step 5 做 AI 结构标注）和 `subjects_index.json`（41 科目→附注候选表粗索引，**供你在 Step 2 生成 note_map.json 时参考/校验**，精确定位以 Claude 生成的 note_map 为准）

输出 `results.json`，每条结果含：check_type / rule_name / severity / passed / description / expected / actual / difference / source_location / target_location / evidence / **page** / **context** / **source_file**。

**定位字段（审计师核对原文用，必填）**：
- `page`：页码（纯数字，如 `45`）。从 report.md 的 `<!-- SOURCE ... page=N -->` 注释或附注章节位置获取。
- `context`：原文摘录（约50字，被检查的那行原文片段），审计师在 Excel 里直接看到原文，不用翻 PDF。
- `source_file`：由 run_check 自动回填原始报告路径，你写语义检查结果时无需手动填。
- `rule_name`：用有意义的科目名（如 `货币资金年末竖加`、`存货-原材料横加`），**不要带 `id=N` 前缀**（id 是解析时的表格序号，对审计师无意义）。

### Step 5 — 语义检查（必须执行，skill 的核心价值）

`run_check.py` 只是**代码侧的确定性粗筛**（L1 报表间恒等式 + 页码/单位/错别字词库）。以下四类语义检查是本 skill 区别于普通脚本的核心能力，**必须执行，不可跳过**——跳过等于只做了 20% 的工作。

**Agent 终审输出习惯（D2.4）**：
- Agent 在 Step 5 回原文核对时，**不必把每一条思考过程都输出给用户**。可在内部快速按表分组、批量判断、直接修正 `results.json`。
- 修正完成后直接执行 Step 6 导出，最后一次性告知用户报告保存路径和核心结论（几个错误、几个存疑、分别是什么）。仅在需要用户决策或确认存疑时才展开细节。

**⚠️ Claude 终审强制（D2.1 核心，最重要）**

- **所有 error/warning 必须经 Claude 整体语义复核**才能输出
- **终审必须回原文核对，不能只看 results.json 的字段**：
  - 横加竖加 warning：读 extracted_tables.json 里该表的完整 headers+rows（用 source_location 的表格ID定位），**整体看这张表**判断：①这列是不是百分比列（不该加金额）②这几行是不是"其中"子项（重复加）③是不是两期混算（明细和≈合计的整数倍）④明细是否真漏加/多加（真错）。**禁止只看 expected/actual/ratio 数字猜**——ratio 相同的可能是真错也可能是跨列，只有看表原文才能区分。
  - 表注勾稽 warning：按 note_map 的 table_ids 去 extracted_tables 看那张表的实际内容，**确认 table_id 指对了附注表**（不是别的科目表/风险汇总表/坏账表）。subjects_index 的粗匹配常指错表，note_map 必须回原文核对定位。取数差异时看附注表合计行 vs 报表值。
  - 错别字 error：**grep report.md + 解压 docx XML 全文搜索该词**，确认原文确实存在（AI 会编造原文没有的词，如"先讲先出"幻觉）。不存在→删除（幻觉）。
- 复核规则：
  - **确认真错**（回原文确认加总不平/勾稽对不上/错别字确实存在）→ 保留 error
  - **特殊结构**（百分比列、子项重复、减项、不同口径、note_map 指错表）→ 降为存疑或删除
  - **误报**（AI幻觉、PDF空格断词、DeepSeek过度报告）→ 删除不显示
- **evidence 必须含"Agent复核：确认/存疑/删除 + 回原文核对依据"**，无标记视为未复核必须补做

**表注勾稽**（check_type="表注"）：**run_check --use-ai 已自动执行**（三层分工：Step2 的 note_map 定位 → DeepSeek locate 取数 → calculator 比较"报表数 vs 附注数"）。你只需做 Claude 终审 + 兜底：
1. **抽查 note_map 定位准确性**：随机几个科目对照附注原文，确认 table_ids 指对了附注明细表（不是报表行）
2. **终审 results.json 里 check_type=表注 的 warning**（报表数≠附注数 / 取数失败），区分：①真错（数值确实对不上）②口径差异（附注按账龄/类别拆分，口径不同属正常）③locate 取数失败（→手动补）。按"确认真错/存疑/删除"复核，evidence 加"Agent复核"标记
3. **--no-ai 或取数失败的科目降级为 Claude 手动**：按 note_map 定位去附注原文提数，调 `calculator check` 比较（算术绝不手算，全走 calculator）
- **最低工作量（硬性门槛）**：note_map 覆盖的科目每科目一条结果（标准≥8、深度全覆盖报表列示科目）。附注-only 无四表→跳过，记一条 info 说明原因

**横加竖加**（check_type="横加"/"竖加"）：Step 4 的 scan 已对含合计行的表做了代码验算，你在这里做 scan 做不了的部分：

**按表分组复核（效率关键，禁止逐条）**：同一张表的多个竖加/横加 warning（如某账龄表4列各报1条=4条warning）**合并成一次复核**——读该表完整原文一次，批量判断该表所有 warning。用 source_location（表格ID）分组：
```python
# 按表分组 warning，一张表一次复核
from collections import defaultdict
by_table = defaultdict(list)
for w in warnings: by_table[w.get("source_location")].append(w)
for table_loc, table_warns in by_table.items():
    # 读这张表的完整 headers+rows（一次），批量判断该表所有 warning
```
**判断标准（必须给明确结论，禁止骑墙存疑）**：
- **删除（确认误报）**：百分比列误参与竖加 / "其中"子项重复 / 两期混算（明细和≈合计整数倍）/ 跨列对比（数量级悬殊）/ note_map 指错表 / 合计行空值
- **确认错误（真错）**：calculator 确认明细和≠合计，且排除了上述结构原因（同一张表同一列，明细确实漏加/多加）
- **通过（确认无误）**：差异<0.5%且能判断是四舍五入（calculator 确认差几分钱）
- **存疑（仅当回原文仍无法判断）**：附注口径与报表口径确实不同（如附注按账龄拆分、报表是净值），需审计师判断口径——**这是唯一允许存疑的情况**。看不懂表结构不是存疑理由，要继续读到懂或标删除。

为什么必须明确结论：审计师拿到报告要能直接行动（改/不改/人工核），"存疑"过多等于没核查。DeepSeek 会误报，但你回原文后应能判断，判断不了说明原文读得不够。

**附注内变动表 reconcile**（check_type="附注内"）：调 `calculator reconcile` 验证期初 + 增加 − 减少 = 期末（固定资产、应付职工薪酬、应交税费等，见 rules.md C1）。凡识别为四列变动结构的表都做。

**文本复核**（check_type="文本"）：通读 `report.md`，找错别字、病句、前后矛盾、数据口径不一致。这是 LLM 擅长而脚本词库只是粗筛的部分。

执行完以上四类才能进 Step 6。若某类确实无目标（如附注-only 文档无四表→无表注勾稽对象），在 results 里记一条 info 说明"未执行表注勾稽（原因：附注-only 无四表）"，**不要静默跳过**——让用户知道哪些检查做了、哪些没做、为什么。

**每条语义检查结果必须填定位信息**（审计师要回原文核对）：从 report.md 找到被检查内容的 `<!-- SOURCE page=N -->` 标记，填入 `page`；把被检查的那行原文摘录（约50字）填入 `context`。这样审计师在 Excel 里点页码能打开原报告、看原文摘录能直接核对，不用逐页翻 PDF。

把补充结果按统一格式追加到 `results.json`（字段同 Step 4）。

### Step 6 — 输出报告

```bash
python3 scripts/export_report.py results.json -o <输出目录>
```

 生成两个文件：
- **7 sheet Excel**：按审计师友好分类，通过项不进详细 sheet（只在摘要统计）：
  - **摘要**：检查范围 / 通过 / 问题 / 存疑统计 + 按类别统计 + 严重程度说明
  - **报表内勾稽**：资产负债表平衡、利润表推导、现金流量表、权益变动表（L1恒等式 + 表内竖加）
  - **表注勾稽**：报表数 vs 附注数（应收账款=账面余额-坏账准备等41科目）
  - **附注内勾稽**：附注变动表 reconcile（期初+增加-减少=期末）、跨附注表关系
  - **横加竖加**：附注明细表的横向纵向加总（账面余额-坏账=账面价值、明细之和=合计）
  - **文本格式**：错别字、页眉、页码、公司名、单位、编号
  - **检查项**：所有检查项列表（包括通过项）
- **Markdown 复核报告**：按问题/存疑分章，给人读

**Severity 二元化**：
- **问题**：确认错误需修改（Agent复核确认）
- **存疑**：可疑需人工核实（Agent复核存疑）
- **通过**：通过项不在详细 sheet 显示，仅在摘要统计

输出只读不改源报告（audit-only）。

### Step 7 — 解读结果

向用户解释发现的问题，按严重程度说明，**保持简洁**：
- **错误（红）**：calculator 算出确定差异，如资产 ≠ 负债 + 权益。给出应为值、实际值、差异、页码定位、修复建议。
- **异常（黄）**：AI + 代码双验证不一致，如报表数 vs 附注数对不上。提示人工复核。
- **提示（蓝）**：AI 发现可疑但无法量化，如营业外收入为负。避免漏报但不制造噪音。

对标记"异常"的项做二次判断，排除规则误触（如附注口径不同导致的正常差异）后再呈现给用户。

**输出习惯**：完成 Step 5 终审和 Step 6 导出后，直接告诉用户报告保存路径（Excel + Markdown），并给出核心统计（问题数/存疑数/主要问题）。不必逐项展开，除非用户要求。

---

## 关键指引

细节在各 reference 文件，这里只给骨架和读取时机。

**定位四表**：看编制单位、会计期间、项目结构，语义识别合并 + 母公司 8 张或单体 4 张。识别变体（股东权益 = 所有者权益）。读 `references/rules.md` 了解科目覆盖范围。

**附注语义索引**：理解"附注三、货币资金"讲货币资金、"（三）应收账款"讲应收账款，不穷举正则匹配标题。按科目索引后按需取数，不全量加载。

**列含义判断**：看表头和内容判断期末/期初/附注编号/项目名列，不硬编码列数。3 列、4 列、8 列左右两栏都能处理。

**AI 结构标注**：读 `references/structure_annotation.md`，用里面的 prompt 模板标注行 type/op、列 type、横加关系，批量标注提效。标注失败降级为仅合计行验证。

**附注-only**：无四表 → 跳过报表间/表注勾稽，做附注内勾稽 + 横加竖加 + 文本格式。报告中明确标注"本文档为附注-only，未执行报表间/表注勾稽"。

---

## 算术纪律 + 大报告分批

50-150 页合体大报告（如盛屯 128 页）容易上下文爆炸。分批策略：
1. 先读四表（通常在报告前部，页数少）→ 执行报表间/表内检查
2. 按科目逐个去附注找明细（用语义索引定位，不全量加载附注）
3. 分批处理避免上下文爆炸

算术纪律全程不变：任何数值加减都调 calculator，AI 只决定传哪些数。

---

## 跨平台依赖安装 + mineru 隐私

**Python 依赖**（mac/Windows 通用）：
```bash
pip install pdfplumber python-docx openpyxl openai
```

**mineru**（仅扫描件/图片报表才需要）：
```bash
npm install -g mineru-open-api
mineru-open-api auth   # 配置免费 token
```

脚本纯 Python 跨平台（pathlib、无平台特定命令），mac/Windows 双平台、中文路径、含空格路径均支持。

**mineru 数据隐私**：审计报告含敏感财务数据，上传云端前必须告知用户并获得知情同意。上市公司公开报告无隐私问题；未公开/保密报告建议优先用文本路径（pdfplumber/python-docx，数据不出本机）。详见 `references/mineru_usage.md`。

---

## references 索引

| 文件 | 何时读 |
|---|---|
| `references/rules.md` | 做表注勾稽时查 41 科目对照表；做变动表时查 reconcile 规则；用户问覆盖哪些科目时 |
| `references/structure_annotation.md` | 做横加竖加时用 prompt 模板标注附注表格；标注失败查降级策略；批量标注查提效建议 |
| `references/extraction.md` | 看到 report.md 中 mineru 来源标记时判断数字置信度；用户问为什么分四路/为什么文本优先时 |
| `references/mineru_usage.md` | 首次遇扫描件/图片报表需引导安装配置 mineru；mineru 调用失败排查；用户问数据安全时 |
| `references/user_rules.md` | 每次检查时加载用户自定义规则并执行；用户描述新需求时写入 |

---

## 用户自定义规则

读 `references/user_rules.md`。用户可在对话中描述特殊检查需求（如"我们事务所要求核对关联方披露完整性""金融行业客户重点查贷款五级分类"），你理解后整理成"自然语言描述 + 适用场景 + 期望结果"格式写入该文件的"## 我的规则"章节。规则跟着 skill 走（不绑定具体报告目录），所有报告共用。检查时一并执行这些规则。规则失效或需修改时，用户在对话里说即可，你更新文件。
