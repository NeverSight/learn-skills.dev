---
name: ruanzhu-gen-intro
description: >-
  中国软件著作权（软著）登记表「软件基本信息/申请信息」字段生成：开发与运行环境、编程语言、源程序量、
  开发目的、面向领域、主要功能、技术特点等，按字数限制输出可分段复制的 Markdown。
  Use when the user mentions 软著登记信息、软著申请信息、开发的硬件环境、运行的硬件环境、
  开发目的、主要功能、技术特点、源程序量、编程语言、ruanzhu-gen-intro，
  或要填写版权中心/代理机构在线登记表的软件基本信息字段。
---

# 软著登记信息生成（ruanzhu-gen-intro）

把「仓库事实 → 字数合规的登记表字段 → 分块可复制 Markdown」固化为可复用流程。  
**以当前仓库已实现功能与真实技术栈为准，禁止虚构未上线能力。**

| 姊妹技能 | 用途 |
| --- | --- |
| **`ruanzhu-gen-doc`** | 用户操作说明书（Markdown/Word + 截图） |
| **`ruanzhu-gen-code`** | 程序鉴别材料 / 源码 Word（前30+后30） |
| **本技能** | 在线登记表「软件基本信息」短字段与简介文案 |

## 何时启用

- 用户说：软著登记信息、申请信息、硬件环境、开发目的、主要功能、技术特点、源程序量  
- 或点名：`ruanzhu-gen-intro`  
- 或贴出登记表字段截图 / 其他项目提交案例，要求按格式为本仓库补齐

## 快速提示词（给用户）

```text
按 ruanzhu-gen-intro 生成本仓库软著登记信息。
项目名称：〈全称〉
端别：〈管理端 Web / 员工 H5 / …〉
源码统计路径：〈如 apps/hr-web + apps/hr-server〉
有提交案例则环境类字段对齐案例写法，业务文案按本仓库改写。
输出：_doc/软著申请/〈项目名称〉-软著登记信息.md
```

完整模板见 [references/quick-prompt.md](references/quick-prompt.md)。

---

## 字段与字数（必须遵守）

详见 [references/field-limits.md](references/field-limits.md)。默认限制：

| 字段 | 限制 |
| --- | --- |
| 开发的硬件环境 | ≤50 字 |
| 运行的硬件环境 | ≤50 字 |
| 开发该软件的操作系统 | ≤50 字 |
| 软件开发环境 / 开发工具 | ≤50 字 |
| 该软件的运行平台 / 操作系统 | ≤50 字 |
| 软件运行支撑环境 / 支持软件 | ≤50 字 |
| 编程语言 | 无空格拼接，如 `HTMLJavaScriptPythonSQL` |
| 源程序量 | 正整数（行数） |
| 开发目的 | ≤50 字 |
| 面向行业 / 领域 | ≤50 字 |
| 软件的主要功能 | **500～1300** 字 |
| 软件技术特点 | ≤100 字 |

字数按 **Unicode 字符数**（`[...str].length`）计；生成后必须实测并写入各节「字数」。

若用户登记通道字数与上表不同，**以用户当场给出的限制为准**。

---

## Agent 工作流

### Phase 0 — 立项输入

确认或从仓库推断：

| 项 | 说明 |
| --- | --- |
| 项目名称 | 全文唯一；多端 = **多套独立软著、多份登记信息文件**，名称勿混用 |
| 端别 | Web 管理端 / 员工 H5 / 桌面端等 |
| 案例对齐 | 用户若提供其他项目提交案例，环境类短字段可对齐其写法（机型、WINDOWS 11、Chrome 内核等），**业务文案必须改写为本项目** |
| 输出目录 | 默认 `_doc/软著申请/` |

### Phase 1 — 事实盘点（只读）

1. **技术栈**：`package.json` / `pyproject.toml` / README / 操作手册「运行环境」  
2. **已实现功能**：路由/菜单/`pages.json`、侧栏、业务页；**禁止**把规划未做模块写入主要功能  
3. **端边界**：管理端勿写员工端专属能力，反之亦然  

### Phase 2 — 源程序量

用本技能脚本统计（可改路径/后缀）：

```bash
node "<SKILL_DIR>/scripts/count-source-lines.js" \
  --root "<仓库根>" \
  --paths "apps/hr-web,apps/hr-server" \
  --ext ".vue,.ts,.tsx,.js,.py,.scss,.css,.html,.sql,.json"
```

- 默认排除：`node_modules`、`dist`、`.git`、`__pycache__`、`.venv`、`coverage`、`unpackage` 等  
- 采用物理行口径，包含注释与空白行；空文件计 0，末尾换行不额外计行。与源码 Word 的有效行口径不同。
- 在 Markdown 中注明统计范围；数字用脚本输出值  
- 若仓库已有 `*-ruanzhu-code-config.md`，优先用其 `paths` 作为统计范围（可再加同端前端根目录）

### Phase 3 — 撰写字段

写作风格见 [references/style-guide.md](references/style-guide.md)。要点：

1. **环境类**：可对齐用户案例的简短格式；开发工具、支撑环境须与本仓库技术栈一致（勿照抄案例里的 IDEA/MySQL5.7/Java 等）  
2. **编程语言**：按实际栈拼接，常见 `HTMLJavaScriptPythonSQL` / `HTMLJavaScriptJavaSQL`  
3. **开发目的 / 面向领域**：一句话，命中业务价值与行业，≤50  
4. **主要功能**：B/S（或实际架构）开篇 → 技术栈一句 → 模块清单 → 分模块叙述；控制在 500～1300  
5. **技术特点**：架构 + 鉴权/存储 + 核心业务能力，≤100；勿堆砌与本项目无关的 AI/物联网话术  

### Phase 4 — 产出 Markdown

路径：`_doc/软著申请/〈项目名称〉-软著登记信息.md`

结构要求（便于复制）：

1. 标题 + 软件名称/端别说明  
2. **每个字段独立一节**，正文放在 fenced code block（\`\`\`）内，便于整块复制  
3. 每节标注实测字数  
4. 文末「字数速查」表  

模板：[templates/软著登记信息.example.md](templates/软著登记信息.example.md)

### Phase 5 — 自检

- [ ] 字数全部合规（主要功能 ≥500 且 ≤1300）  
- [ ] 功能均来自代码盘点  
- [ ] 项目名称全文一致；多端文件未串写  
- [ ] 源程序量有统计范围说明  
- [ ] 与用户案例对齐时，未把案例业务（如设备运维）误写入本项目  

---

## 多端 / 多软著

| 场景 | 做法 |
| --- | --- |
| 管理端 + 员工端 | 两套项目名称、两份 `*-软著登记信息.md`；源码路径各算各的 |
| 仅补缺字段 | 可只改用户点名的字段，保持其余不变 |
| 用户改字数上限 | 以用户为准，更新文内「限制」标注 |

---

## 参考文件

| 文件 | 用途 |
| --- | --- |
| [references/field-limits.md](references/field-limits.md) | 字段与字数细则 |
| [references/style-guide.md](references/style-guide.md) | 案例对齐与文案写法 |
| [references/quick-prompt.md](references/quick-prompt.md) | 用户一键提示词 |
| [templates/软著登记信息.example.md](templates/软著登记信息.example.md) | 产出骨架 |
| [scripts/count-source-lines.js](scripts/count-source-lines.js) | 源程序量统计 |
