---
name: nexus-mapper
description: "Generate a persistent .nexus-map/ knowledge base that lets any AI session instantly understand a codebase's architecture, systems, dependencies, and change hotspots. Use when starting work on an unfamiliar repository, onboarding with AI-assisted context, preparing for a major refactoring initiative, or enabling reliable cold-start AI sessions across a team. Produces INDEX.md, systems.md, concept_model.json, git_forensics.md and more. Requires shell execution and Python 3.10+. For ad-hoc file queries or instant impact analysis during active development, use nexus-query instead."
---

# nexus-mapper — AI 项目探测协议

> "你不是在写代码文档。你是在为下一个接手的 AI 建立思维基础。"

本 Skill 指导 AI Agent 使用 **PROBE 五阶段协议**，对任意本地 Git 仓库执行系统性探测，产出 `.nexus-map/` 分层知识库。

---

## ⚠️ CRITICAL — 五阶段不可跳过

> [!IMPORTANT]
> **在 PROFILE、REASON、OBJECT、BENCHMARK 完成前，不得产出最终 `.nexus-map/`。**
>
> 这不是为了形式完整，而是为了防止 AI 把第一眼假设直接写成结论。最终产物必须建立在脚本输出、仓库结构、反证挑战和回查验证之上。

❌ **禁止行为**：
- 跳过 OBJECT 直接写输出资产
- 在 BENCHMARK 完成前生成 `concept_model.json`
- PROFILE 阶段脚本失败后继续执行后续阶段

✅ **必须做到**：
- 每个阶段完成后显式确认「✅ 阶段名 完成」再进入下一阶段
- OBJECT 提出足以推翻当前假设的最少一组高价值质疑，通常为 1-3 条，绝不凑数
- `implemented` 节点的 `code_path` 必须在仓库中真实存在；`planned/inferred` 节点不得伪造 `code_path`（见守则2）

---

## 📌 何时调用 / 何时不调用

| 场景 | 调用 |
|------|:----:|
| 用户提供本地 repo 路径，希望 AI 理解其架构 | ✅ |
| 需要生成 `.nexus-map/INDEX.md` 供后续 AI 会话冷启动 | ✅ |
| 用户说「帮我分析项目」「建立项目知识库」「让 AI 了解这个仓库」 | ✅ |
| 运行环境无 shell 执行能力（纯 API 调用模式，无 `run_command` 工具） | ❌ |
| 宿主机无本地 Python 3.10+ | ❌ |
| 目标仓库无任何已知语言源文件（`.py/.ts/.java/.go/.rs/.cpp` 等均无） | ❌ |
| 用户只想查询某个特定文件/函数 → 直接用 `view_file` / `grep_search` | ❌ |

---

## ⚠️ 前提检查（缺失项要显式告知；可降级时优先降级而不是中止）

| 前提 | 检查方式 |
|------|---------|
| 目标路径存在 | `$repo_path` 可访问 |
| Python 3.10+ | `python --version` >= 3.10 |
| 脚本依赖已安装 | `python -c "import tree_sitter"` 无报错 |
| 有 shell 执行能力 | Agent 环境支持 `run_command` 工具调用 |

`git` 历史是加分项，不是硬阻塞项。没有 `.git` 或历史过少时，跳过热点分析，并在输出中明确记录这是一次降级探测。

---

## 📥 输入契约

```
repo_path: 目标仓库的本地绝对路径（必填）
```

**语言支持**：自动按文件扩展名 dispatch，语言配置（扩展名映射 + Tree-sitter 查询）存储在 `scripts/languages.json`，优先用 bundled structural queries 提取模块/类/函数；若 grammar 可加载但当前没有结构 query，则至少保留 Module 级节点并在输出中标注 `module-only coverage`。当前已接入的常见语言包括 Python/JavaScript/TypeScript/TSX/Bash/Java/Go/Rust/C#/C/C++/Kotlin/Ruby/Swift/Scala/PHP/Lua/Elixir/GDScript/Dart/Haskell/Clojure/SQL/Proto/Solidity/Vue/Svelte/R/Perl。

**不支持的语言扩展**：若仓库含有内置未支持的语言文件，agent 可通过命令行参数动态赋予支持：
- `--add-extension .templ=templ` 添加新文件扩展名映射（可重复）
- `--add-query templ struct "(component_declaration ...)"` 为某语言添加结构查询（可重复）

查询参数格式：`--add-query <LANG> <TYPE> <QUERY_STRING>` 其中 `<TYPE>` 为 `struct` 或 `imports`。

高级用法：若配置复杂，可用 `--language-config <JSON_FILE>` 显式指定一个 JSON 配置文件，格式同前，允许扩展名映射、自定义查询和显式标记不支持的语言。

如果当前任务涉及“补一个暂未适配的语言”或“为某种非标准扩展名补 Tree-sitter 支持”，应继续读取 `references/05-language-customization.md`。该文件不是阶段门控文件，而是命令行扩展与可选 JSON 配置的专项操作说明。

---

## 📤 输出格式

执行完成后，目标仓库根目录下将产出：

```text
.nexus-map/
├── INDEX.md                    ← AI 冷启动主入口（< 2000 tokens）
├── arch/
│   ├── systems.md              ← 系统边界 + 代码位置
│   ├── dependencies.md         ← Mermaid 依赖图 + 时序图
│   └── test_coverage.md        ← 静态测试面：测试文件、覆盖到的核心模块、证据缺口
├── concepts/
│   ├── concept_model.json      ← Schema V1 机器可读图谱
│   └── domains.md              ← 核心领域概念说明
├── hotspots/
│   └── git_forensics.md        ← Git 热点 + 耦合对分析
└── raw/
    ├── ast_nodes.json          ← Tree-sitter 解析原始数据
    ├── git_stats.json          ← Git 热点与耦合数据
    └── file_tree.txt           ← 过滤后的文件树
```

所有生成的 Markdown 文件必须带一个简短头部，至少包含：
- `generated_by`
- `verified_at`
- `provenance`

`concept_model.json` 的人类可读名称字段统一使用 `label`。不要添加 `title`；若某个生成结果出现 `title`，应在 EMIT 阶段删除并并回 `label` 语义。

如果 PROFILE 阶段发现已知但未支持的语言文件，`provenance` 必须明确写出哪些部分属于人工推断或降级分析。
如果 PROFILE 阶段发现 `module-only coverage`，也必须写清楚：这些语言已被计入 AST 文件覆盖，但没有类/函数级结构保证。
如果 PROFILE 阶段发现某个通过覆盖配置声明的语言仍然无法加载 parser，也必须写清楚：这是 `configured-but-unavailable`，不能伪装成已覆盖。

---

## 🔍 按需查询工具

`scripts/query_graph.py` 读取 `raw/ast_nodes.json`，提供精准的局部依赖查询。在 PROBE 各阶段辅助认知生成，也可在后续开发中按需使用。

**零额外依赖**——纯 Python 标准库，输入 `ast_nodes.json` 即可运行。

### 查询模式

```bash
# 查看某个文件的类/函数结构及 import 清单
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --file <path>

# 反向依赖查询：谁引用了这个模块
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --who-imports <module_or_path>

# 影响半径：上游依赖 + 下游被依赖者
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --impact <path>

# 叠加 git 风险与耦合数据（可选）
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --impact <path> \
  --git-stats <git_stats.json>

# 高扇入/扇出核心节点识别
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --hub-analysis [--top N]

# 按目录聚合的结构摘要（为 EMIT 阶段 systems.md 提供数据支撑）
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --summary
```

### 使用时机

| 阶段 | 推荐查询 | 用途 |
|------|---------|------|
| REASON | `--hub-analysis` | 用扇入/扇出数据验证核心系统假说，而不是仅凭目录名猜测 |
| OBJECT | `--impact`, `--impact --git-stats` | 验证边界假设，查看真实上下游依赖；叠加 git 热度和耦合度 |
| EMIT | `--summary`, `--file` | 生成 `systems.md` / `dependencies.md` 的数据支撑 |
| 开发中 | `--file`, `--who-imports`, `--impact` | Bug 调查、修改影响评估、重构分析 |

> **定位**：`.nexus-map/` 是"地图"，`query_graph.py` 是"放大镜"。地图帮你定位大方向，放大镜帮你看清局部细节。

> **五个查询模式的详细使用场景与实战案例**，见 `references/06-query-guide.md`。

---

## 🧠 持久指令

为避免新会话忘记读取既有知识库，请把下面这段精炼规则写入宿主工具的持久指令文件，例如 `AGENTS.md`、`CLAUDE.md` 或同类记忆文件：

```md
如果仓库中存在 .nexus-map/INDEX.md，开始任务前必须先阅读它恢复全局上下文。

如果任务需要判断局部结构、依赖关系、影响半径或边界归属，优先回读 nexus-mapper skill 的按需查询说明，并使用 query_graph.py 基于 .nexus-map/raw/ast_nodes.json 做验证；不要重新猜结构。

当一次任务改变了项目的结构认知时，应在交付前评估是否同步更新 .nexus-map。结构认知包括：系统边界、入口、依赖关系、测试面、语言支持、路线图或阶段性进度事实。纯局部实现细节默认不更新。

不要把 .nexus-map 视为静态文档；它是项目记忆的一部分。新对话优先读取，重要变更后按需同步。
```

这是一条 **建议写入宿主持久记忆** 的规则，目的是让 agent 在真正需要时自然想起读取或更新 `.nexus-map`。

---

## 📋 PROBE 阶段硬门控

> [!IMPORTANT]
> **进入每个阶段前必须 `read_file` 对应 reference，不得跳过。**
> 各阶段详细步骤、完成检查清单与边界场景处理均在 reference 中定义。

```
[Skill 激活时]     → read_file references/01-probe-protocol.md  （阶段步骤蓝图）
[REASON 前]        → read_file references/03-edge-cases.md       （边界场景检查）
[OBJECT 前]        → read_file references/04-object-framework.md （三维度质疑模板）
[EMIT 前]          → read_file references/02-output-schema.md    （Schema 校验规范）
```

---

## 🛡️ 执行守则

### 守则1: OBJECT 拒绝形式主义

OBJECT 的存在意义是打破 REASON 的幸存者偏差。大量工程事实隐藏在目录命名和 git 热点背后，第一直觉几乎总是错的。

❌ **无效质疑（禁止提交）**：
```
Q1: 我对系统结构的把握还不够扎实
Q2: xxx 目录的职责暂时没有直接证据
```

▲ 问题不在于用了某几个词，而在于这类表述没有证据线索，也无法在 BENCHMARK 阶段验证。

✅ **有效质疑格式**：
```
Q1: git_stats 显示 tasks/analysis_tasks.py 变更 21 次（high risk），
    但 HYPOTHESIS 认为编排入口是 evolution/detective_loop.py。
    矛盾：若 detective_loop 是入口，为何 analysis_tasks 热度更高？
    证据线索: git_stats.json hotspots[0].path
    验证计划: view tasks/analysis_tasks.py 的 class 定义 + import 树
```

---

### 守则2: implemented 节点必须有真实 code_path

> [!IMPORTANT]
> 写入 `concept_model.json` 前，必须先区分节点是 `implemented`、`planned` 还是 `inferred`。
> 只有 `implemented` 节点允许写入 `code_path`，且必须亲手验证存在。

```bash
# BENCHMARK 阶段验证方式
ls $repo_path/src/nexus/application/weaving/   # ✅ 目录存在 → 节点有效
ls $repo_path/src/nexus/application/nonexist/  # ❌ [!ERROR] → 修正或删除此节点
```

对于 `planned` 或 `inferred` 节点，使用：

```json
{
  "implementation_status": "planned",
  "code_path": null,
  "evidence_path": "docs/architecture.md",
  "evidence_gap": "仓库中未发现 src/agents/monarch/，仅在设计文档中出现"
}
```

❌ 禁止：
- 用一个“勉强相关”的文件冒充 `code_path`
- `implementation_status` 为 `planned/inferred`，却写入伪精确目录
- `code_path: "PLANNED"` 这类把状态塞进路径字段的写法

---

### 守则3: EMIT 原子性

先全部写入 `.nexus-map/.tmp/`，全部成功后整体移动到正式目录，删除 `.tmp/`。

**目的**：中途失败不留半成品。下次执行检测到 `.tmp/` 存在 → 清理后重新生成。

✅ 幂等性规则：

| 状态 | 处理方式 |
|------|----------|
| `.nexus-map/` 不存在 | 直接继续 |
| `.nexus-map/` 存在且 `INDEX.md` 有效 | 询问用户：「是否覆盖？[y/n]」 |
| `.nexus-map/` 存在但文件不完整 | 「检测到未完成分析，将重新生成」，直接继续 |

---

### 守则4: INDEX.md 是唯一冷启动入口

`INDEX.md` 的读者是**从未见过这个仓库的 AI**。两个硬约束：
- **< 2000 tokens** — 超过就重写，不是截断
- **结论必须具体** — 不要用空泛的模糊词搪塞；证据不足时明确写出 `evidence gap` 或 `unknown`，并说明缺了什么证据

写完后执行 token 估算：行数 × 平均 30 tokens/行 = 粗估值。

---

## 🧭 不确定性表达规范

```
避免只写：待确认 · 可能是 · 疑似 · 也许 · 待定 · 暂不清楚 · 需要进一步 · 不确定
避免只写：pending · maybe · possibly · perhaps · TBD · to be confirmed
```

如果证据不足，可以这样写：
- `unknown: 未发现直接证据表明 api/ 是主入口，当前仅能确认 cli.py 被 README 引用`
- `evidence gap: 仓库没有 git 历史，因此 hotspots 部分跳过`

原则：允许诚实地写不确定，但必须解释不确定来自哪一条缺失证据，而不是把模糊词当结论。

---

### 守则5: 最小执行面与敏感信息保护

> [!IMPORTANT]
> 默认只运行本 Skill 自带脚本和必要的只读检查。不要因为“想更懂仓库”就执行目标仓库里的构建脚本、测试脚本或自定义命令。

- 默认允许：`extract_ast.py`、`git_detective.py`、目录遍历、文本搜索、只读文件查看
- 默认禁止：执行目标仓库的 `npm install`、`pnpm dev`、`python main.py`、`docker compose up` 等命令，除非用户明确要求
- 遇到 `.env`、密钥文件、凭据配置时：只记录其存在和用途，不抄出具体值

---

### 守则6: 降级与人工推断必须显式可见

> [!IMPORTANT]
> 如果 AST 覆盖不完整，或者某部分依赖图/系统边界来自人工阅读而非脚本产出，必须在最终文件中显式标注 provenance。

- `dependencies.md` 中凡是非 AST 直接支持的依赖关系，必须标注 `inferred from file tree/manual inspection`
- `domains.md`、`systems.md`、`INDEX.md` 如果涉及未支持语言区域，必须显式说明 `unsupported language downgrade`
- 若写入进度快照、Sprint 状态、路线图，必须附 `verified_at`，避免过期信息伪装成当前事实

---

## 🛠️ 脚本工具链

```bash
# 设置 SKILL_DIR（根据实际安装路径）
# 场景 A: 作为 .agent/skills 安装
SKILL_DIR=".agent/skills/nexus-mapper"
# 场景 B: 独立 repo（开发/调试时）
SKILL_DIR="/path/to/nexus-mapper"

# PROFILE 阶段调用 — 基础用法
python $SKILL_DIR/scripts/extract_ast.py <repo_path> [--max-nodes 500] \
  > <repo_path>/.nexus-map/raw/ast_nodes.json

# 若仓库包含非标准语言，可通过命令行参数添加支持
python $SKILL_DIR/scripts/extract_ast.py <repo_path> [--max-nodes 500] \
  --add-extension .templ=templ \
  --add-query templ struct "(component_declaration name: (identifier) @class.name) @class.def" \
  > <repo_path>/.nexus-map/raw/ast_nodes.json

# 若配置复杂，用 JSON 文件（格式参见 --language-config 说明）
python $SKILL_DIR/scripts/extract_ast.py <repo_path> [--max-nodes 500] \
  --language-config /custom/path/to/language-config.json \
  > <repo_path>/.nexus-map/raw/ast_nodes.json

# PROFILE 阶段同时生成过滤后的文件树
python $SKILL_DIR/scripts/extract_ast.py <repo_path> [--max-nodes 500] \
  --file-tree-out .nexus-map/raw/file_tree.txt \
  > <repo_path>/.nexus-map/raw/ast_nodes.json
```

**依赖安装（首次使用）**：
```bash
pip install -r $SKILL_DIR/scripts/requirements.txt
```

---

## ✅ 质量自检（EMIT 前必须全部通过）

- [ ] 五个阶段均已完成，每阶段有显式「✅ 完成」标记
- [ ] OBJECT 的质疑数量没有凑数；每条都带证据线索和可执行验证计划
- [ ] `implemented` 节点的 `code_path` 已亲手验证存在；`planned/inferred` 节点使用了 `implementation_status + evidence_path + evidence_gap`
- [ ] `responsibility` 字段：具体、可验证；证据不足时明确说明缺口
- [ ] `INDEX.md` 全文 < 2000 tokens，结论具体不过度装确定（守则4）
- [ ] 若发现未支持语言文件，最终 Markdown 头部和相关章节已显式标注降级与人工推断范围
- [ ] `arch/test_coverage.md` 已生成，并明确这是静态测试面而不是运行时覆盖率
