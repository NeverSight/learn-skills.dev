---
name: ruanzhu-gen-code
description: >-
  中国软件著作权（软著）程序鉴别材料/源码文档生成：按版权局惯例前30+后30共60页、每页不少于50行有效代码，
  可配置路径占比与忽略规则并导出 Word。Use when the user mentions 软著源码、程序鉴别材料、
  源码文档、60页源码、前后各30页、有效代码行、ruanzhu-gen-code，
  或要从仓库抽取固定页数源码用于软著登记。
---

# 软著源码文档生成（ruanzhu-gen-code）

从仓库抽取源码，生成符合版权局「程序鉴别材料」要求的 **Word 源码文档**（默认 **前 30 + 后 30 = 60 页**）。

与 **`ruanzhu-gen-doc`**（用户操作说明书）互补：本技能只做**源码页**，不做操作手册/截图。

## 何时启用

- 用户说：软著源码、程序鉴别材料、60 页源码、前后各 30 页、源码 Word  
- 或点名：`ruanzhu-gen-code`

## 用户可配置项（必须支持）

| 参数 | 含义 | 默认 |
| --- | --- | --- |
| **路径** `paths` | 扫描根；字符串均分，或 `{path, weight}` 按占比 | 智能推断 `apps/`、`src/` 等 |
| **占比** `paths[].weight` | 百分数（之和 ≤100）或小数（之和 ≤1） | 均分 |
| **后缀** `extensions` | 文件后缀列表，如 `.vue,.ts,.py` | 见下方默认后缀 |
| **忽略目录** `excludeDirs` / `ignore` | 额外跳过的目录名（如 `__pycache__`） | 内置 + 可追加 |
| **忽略文件** `excludeFiles` | 额外跳过的文件名/glob（如 `__init__.py`） | 默认含 `__init__.py` |
| **打乱** `shuffle` | 是否打乱**各目录内**文件顺序 | `false` |
| **页数** `pages` | 目标页数（足量时） | **60**（前30+后30） |
| **每页行数** `linesPerPage` | 每页有效代码行，版权局要求 ≥50 | **50** |
| **模式** `mode` | `head-tail` 前/后各半；`consecutive` 从头连续 | **`head-tail`** |
| **去空行** `stripBlank` | 去掉空行；**有效行 > 50 时强制保留空行** | `false` |
| **去注释** `stripComments` | 去掉纯注释行与块注释 | `true` |
| **项目名称** `projectName` | 页眉项目名称 | 必填 |
| **版本** `version` | 页眉版本号 | `V1.0` |

**版权局对齐：** 足量时输出 60×50=**3000** 行（前 1500 + 后 1500）；有效行不足 3000 则**提交全部**（不凑页）。  
多目录 `weight`：拼入连续程序时的占比；不足目录全取后回填。

## 快速提示词（给用户）

```text
按 ruanzhu-gen-code 生成本仓库软著源码文档。
项目名称：〈名称〉
路径占比：apps/hr-server/app 40%；apps/hr-web/src 60%
忽略：__pycache__、__init__.py
后缀：〈.py,.ts,.vue,.scss〉
是否打乱：〈是/否〉
页数：60（前30+后30）；每页50行有效代码
输出到：_doc/软著申请/
```

完整模板见 [references/quick-prompt.md](references/quick-prompt.md)。

每个子项目一份 `〈项目名称〉-ruanzhu-code-config.md`（内含 **配置：code** + **配置：docx-style**），与产出一对一。说明见 [references/docx-style.md](references/docx-style.md)。

## Agent 工作流

### 1. 收集参数

确认**项目名称**；创建或使用对应 `*-ruanzhu-code-config.md`。多子项目时 `--config` 必填，禁止混用其他项目的 config。

### 2. 运行生成脚本

优先使用本技能脚本（可复制到项目再跑）：

```bash
node "<SKILL_DIR>/scripts/generate-code-doc.js" \
  --root "<仓库根>" \
  --project-name "〈项目名称〉" \
  --paths "apps/hr-web/src,apps/hr-server/app" \
  --ext ".vue,.ts,.py" \
  --pages 60 \
  --lines-per-page 50 \
  --shuffle false \
  --mode head-tail \
  --config "_doc/软著申请/〈项目名称〉-ruanzhu-code-config.md"
```

Windows PowerShell 注意引号。参数以 config 为准；CLI 可覆盖单项。

脚本说明见 [scripts/README.md](scripts/README.md)。

依赖：项目或临时目录需能 `require('docx')`（可与 `_doc/软著申请/.docx-tools` 共用）。

### 3. 质量检查

- [ ] 足量时 60 页、每页约 50 行有效代码（共约 3000 行；前/后各约 1500）  
- [ ] 不足 3000 有效行时提交全部，不空行凑页  
- [ ] 未包含 `node_modules` / lock / 二进制  
- [ ] 页眉含项目名称与版本；页脚有页码  
- [ ] 若 `shuffle=true`，报告所用 `seed`  
- [ ] 向用户给出：输出路径、文件数、有效行、页数、head/tail、是否 submitAll  


### 4. 与操作说明书并存

建议目录：

```text
_doc/软著申请/
├── 〈项目名称〉-ruanzhu-doc-config.md    # 操作手册配置（一对一）
├── 〈项目名称〉-ruanzhu-code-config.md   # 源码文档配置（一对一）
├── 〈项目名称〉-操作手册-v3.docx
└── 〈项目名称〉-源码文档-v1.docx
```

## 默认后缀（可被覆盖）

`.vue,.ts,.tsx,.js,.jsx,.py,.java,.go,.cs,.rs,.php,.sql,.scss,.css,.html`

## 默认排除目录名

`node_modules`,`.git`,`dist`,`build`,`.venv`,`venv`,`coverage`,`.next`,`target`,`vendor`,`.docx-tools`,`Screenshot-web`,`Screenshot-h5`

## 模式说明

| mode | 行为 |
| --- | --- |
| `consecutive` | 文件排序（或打乱）后从头拼接，取前 N 行 |
| `head-tail` | 先得到全文行流，取前 `⌊N/2⌋` 行 + 后 `⌈N/2⌉` 行（经典「前后各约一半」） |

`shuffle` 只打乱**文件列表顺序**，不打乱单文件内行序。

## 参考

- [references/quick-prompt.md](references/quick-prompt.md)  
- [references/format.md](references/format.md)  
- [scripts/generate-code-doc.js](scripts/generate-code-doc.js)  
- [templates/code-doc-config.example.json](templates/code-doc-config.example.json)  
