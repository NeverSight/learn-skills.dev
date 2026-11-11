---
name: ruanzhu-gen
description: >-
  中国软件著作权（软著）材料聚合编排：ruanzhu-gen init 生成一对一 doc/code/intro 配置；
  ruanzhu-gen generator 按配置生成操作手册、源码文档、软著登记信息三套产出。
  Use when the user mentions ruanzhu-gen、软著 init、软著 generator、软著一键生成、
  初始化软著配置、一次生成操作手册与源码与登记信息，或要编排 ruanzhu-gen-doc /
  ruanzhu-gen-code / ruanzhu-gen-intro。
---

# 软著材料聚合（ruanzhu-gen）

编排三个子技能，统一「配置一对一 → 三套产出」：

| 子技能 | 产出 |
| --- | --- |
| **`ruanzhu-gen-doc`** | `〈项目名称〉-操作手册-v*.md` / `.docx` + 截图 |
| **`ruanzhu-gen-code`** | `〈项目名称〉-源码文档-v*.docx` |
| **`ruanzhu-gen-intro`** | `〈项目名称〉-软著登记信息.md` |

**禁止虚构未上线功能。** 多端 = 多套项目名称、多套 config、多套产出，勿混用。

## 何时启用

- 用户说：`ruanzhu-gen init` / `ruanzhu-gen generator`  
- 或：初始化软著配置、一键生成软著三件套  
- 单独只要说明书 / 源码页 / 登记字段时，仍可直接用对应子技能

## 安装与运行依赖

聚合流程需要同时安装本 skill 与三个子技能。运行源码导出需 Node.js 和 `docx`；截图与手册导出的依赖安装见仓库 README 和子技能说明。

资源路径以当前加载的本 skill 目录为准，不假定某个 Agent 的全局安装位置。CLI 默认从本 skill 的相邻目录寻找子技能；目录分散时，使用 `--skills-dir "<包含三个子技能的父目录>"`。缺少所选子技能时会报告错误。

## 命令一览

```bash
# 技能目录（按本机实际路径）
SKILL="<当前加载的 ruanzhu-gen 目录绝对路径>"

# 1) 初始化配置（默认写入 <仓库>/_doc/软著申请/）
node "$SKILL/scripts/cli.js" init \
  --root "<仓库根>" \
  --project-name "示例员工自助系统" \
  --preset h5 \
  --paths "apps/server:40,apps/h5/src:60"

# 2) 生成（Agent 编排 + 可跑的脚本部分）
node "$SKILL/scripts/cli.js" generator \
  --root "<仓库根>" \
  --project-name "示例员工自助系统" \
  --only all
```

| 子命令 | 作用 |
| --- | --- |
| **`init`** | 生成 `*-ruanzhu-doc-config.md`、`*-ruanzhu-code-config.md`、`*-ruanzhu-intro-config.md`（若不存在；`--force` 覆盖） |
| **`generator`** | 校验配置 → 跑源码 Word 脚本 → 输出 doc/intro 的 Agent 待办清单（或由 Agent 当场写完三套） |

Presets 与参数见 [references/cli.md](references/cli.md)。一键提示词见 [references/quick-prompt.md](references/quick-prompt.md)。

---

## Agent 工作流

### A. `ruanzhu-gen init`

1. 向用户确认（缺则推断）：**项目名称**、**端别/preset**（`web` / `h5` / `custom`）、**源码 paths+权重**、**截图目录**。  
2. 运行 CLI `init`（优先），或按 [templates/](templates/) 手写三份 config。  
3. 向用户报告生成路径；提醒按需改 `paths` / `shotDir` / 版式 JSON。

默认产出目录：`_doc/软著申请/`

```text
〈项目名称〉-ruanzhu-doc-config.md
〈项目名称〉-ruanzhu-code-config.md
〈项目名称〉-ruanzhu-intro-config.md
```

### B. `ruanzhu-gen generator`

对**单一**项目名称执行（多项目则多次调用）：

| 步骤 | 动作 | 依赖 |
| --- | --- | --- |
| 0 | 确认三份 config 存在；缺则先 `init` | — |
| 1 | **登记信息**：读 `ruanzhu-gen-intro`，写 `〈项目名称〉-软著登记信息.md` | intro-config 的 paths / 端别 |
| 2 | **源码文档**：跑 `ruanzhu-gen-code` 的 `generate-code-doc.js --config …-code-config.md` | code-config |
| 3 | **操作手册**：读 `ruanzhu-gen-doc` 全流程（盘点→撰写 MD→截图→`md-to-docx`） | doc-config；演示环境 |

`--only intro|code|doc|all` 可只跑子集。

**可脚本化：** `code`（及已有 MD 时的 docx 导出）。  
**需 Agent 撰写：** `intro` 全文、`doc` 操作手册正文与截图编排。

完成后给出三套路径与自检清单。

### C. 质量闸门

- [ ] 项目名称在三份 config 与三套产出中一致  
- [ ] 未串用其他子项目的 config  
- [ ] 登记信息字数合规；功能来自代码事实  
- [ ] 源码文档页数/行数符合 code-config  
- [ ] 操作手册图号与截图目录一致（若已截图）

---

## 与子技能关系

```text
ruanzhu-gen          ← 编排入口（init / generator）
├── ruanzhu-gen-doc    操作说明书
├── ruanzhu-gen-code   程序鉴别材料
└── ruanzhu-gen-intro  登记表基本信息
```

子技能可独立使用；本技能不复制其细则，执行对应步骤时 **Read 对应 SKILL.md**。

---

## 参考

| 文件 | 用途 |
| --- | --- |
| [references/quick-prompt.md](references/quick-prompt.md) | 用户提示词 |
| [references/cli.md](references/cli.md) | CLI 参数与 preset |
| [references/layout.md](references/layout.md) | 目录与一对一约定 |
| [scripts/cli.js](scripts/cli.js) | `init` / `generator` |
| [templates/](templates/) | config 模板 |
