---
name: nexus-query
description: "Precise, instant code structure queries for active development — answer 'who depends on this interface before I refactor it', 'how many modules break if I change this', 'what is the real impact radius of this feature change', 'which module is the true high-coupling hotspot in this legacy codebase'. Essential before any interface change, continuous refactoring task, sprint work estimation, or when navigating unfamiliar or large legacy codebases. Requires Python 3.10+ and shell. Use nexus-mapper instead when building a full .nexus-map/ knowledge base."
---

# nexus-query — 代码结构精准查询

> "改之前先算清楚——数字比猜测更有力。"

本 Skill 将 `extract_ast.py`、`git_detective.py`、`query_graph.py` 三个脚本
封装成一个**开发辅助工具**：按需生成数据、精确回答问题。

---

## 📌 和 nexus-mapper 的区别

| 维度 | nexus-mapper | nexus-query |
|------|-------------|-------------|
| 目的 | 为 AI 建立项目持久记忆（`.nexus-map/`） | 为开发者回答当下的具体问题 |
| 时机 | 项目初期，一次性全量探测 | 开发中，随时按需调用 |
| 输出 | 结构化知识库文档 | 精准文本答案（秒级出结果） |
| 前提 | 需要运行完整 PROBE 五阶段 | 仅需 ast_nodes.json 存在即可 |

**nexus-query 是 nexus-mapper 的轻量伴侣**：如果 `.nexus-map/` 已存在，直接复用；
如果不存在，先运行 `extract_ast.py` 生成 ast_nodes.json，再开始查询。

---

## 📌 何时调用

| 场景 | 调用 |
|------|:----:|
| 「这个文件有哪些类/方法，依赖什么」 | ✅ |
| 「改这个接口/模块，哪些文件受影响」 | ✅ |
| 「这个改动的影响半径是多大」 | ✅ |
| 「项目里谁是真正的核心依赖节点」 | ✅ |
| 「整个项目大概分哪几块」 | ✅ |
| 用户希望生成完整的 `.nexus-map/` 知识库 | ❌ → 改用 nexus-mapper |
| 运行环境无 shell 执行能力 | ❌ |
| 宿主机无本地 Python 3.10+ | ❌ |

---

## ⚙️ 前提：确保 ast_nodes.json 可用

```
进入查询前 → 检查是否有 ast_nodes.json
├── 有（.nexus-map/raw/ast_nodes.json 或用户指定路径）→ 直接查询
└── 没有 → 运行 extract_ast.py 生成 → 再查询
```

```bash
# 默认路径（和 nexus-mapper 的 .nexus-map/ 兼容，可互通）
AST_JSON="$repo_path/.nexus-map/raw/ast_nodes.json"
GIT_JSON="$repo_path/.nexus-map/raw/git_stats.json"    # 可选

# 若 ast_nodes.json 不存在，先创建目录再生成（约数秒）
mkdir -p "$repo_path/.nexus-map/raw"
python $SKILL_DIR/scripts/extract_ast.py $repo_path > $AST_JSON

# 若需要 git 风险数据（可选，仅在存在 .git 时）
python $SKILL_DIR/scripts/git_detective.py $repo_path --days 90 \
  > $GIT_JSON
```

> `$SKILL_DIR` 为本 Skill 的安装路径（`.agent/skills/nexus-query` 或独立 repo 路径）。

**依赖安装（首次使用）**：
```bash
pip install -r $SKILL_DIR/scripts/requirements.txt
```

---

## 🔍 五个查询模式

```bash
# 查看某个文件的类/函数结构及 import 清单
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --file <path>
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --file <path> --git-stats $GIT_JSON

# 反向依赖查询：谁 import 了这个模块
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --who-imports <module_or_path>

# 影响半径：上游依赖 + 下游被依赖者（推荐叠加 git-stats）
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --impact <path>
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --impact <path> --git-stats $GIT_JSON

# 高扇入/扇出核心节点识别
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --hub-analysis [--top N]

# 按顶层目录聚合的结构摘要
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --summary
```

---

### --file \<路径\> — 文件骨架解剖

**输出**：类、方法、行号范围、所有 import（内部 import 解析成真实路径）。加 `--git-stats` 追加变更热度和耦合文件。

**深层价值**：AI 不读源码也能掌握文件结构，精确到行号；针对大型遗留代码库尤其有效——一个 3000 行的 legacy 模块可能有数十个类，逐行阅读效率极低，`--file` 秒出骨架，按行号精准跳转。

**适用场景**：
- 接手超大遗留模块（"屎山"代码），建立结构地图再动手
- 连续重构任务中，确认当前目标文件的完整方法签名，避免改了一处遗漏其他重载
- Bug 调查：快速确认候选类/函数的行号范围，缩小 `view_file` 的读取区间
- Code Review：确认一个 PR 涉及到的方法是否在预期边界内

---

### --who-imports \<路径或模块名\> — 反向依赖追踪

**输出**：所有引用了该模块的文件（区分源码文件和测试文件）。

**深层价值**：改接口之前唯一必须跑的命令。任何修改公共函数签名、删除方法、重命名类的操作如果跳过这步，都是在赌不会炸。

**适用场景**：
- 删函数/改签名/迁移模块前，确认「炸弹清单」——列出所有需要同步修改的调用方
- 连续开发任务中，修改了 step 1 的接口后，确认后续 step 2~N 哪些受影响，规划工作顺序
- 决定测试策略：知道谁依赖了目标模块，才能做精准回归测试而不是全量跑
- 评估「是否值得重构这个老接口」：依赖方越多，重构成本越高；0 个依赖方 = 可以随意重构

---

### --impact \<路径\> [--git-stats] — 影响半径量化

**输出**：上游依赖（这个文件引用了谁）+ 下游被依赖（谁引用了这个文件），最终给出 `X upstream, Y downstream` 数字。加 `--git-stats` 追加 git 风险等级和耦合对。

**深层价值**：最有实战价值的单一命令。`0 upstream, 24 downstream` 一眼告诉你这是基础层，改动影响最广；`upstream` 数字高往往意味着它依赖很多东西，自己也容易被连锁影响。与 git-stats 叠加后：**high-risk + high downstream = 当前最危险的改动点**。

**适用场景**：
- 衡量一个功能修改的风险与实际工作量，在 Sprint 估时/技术债偿还决策时有直接参考价值
- 评估「当前这个改动是局部手术还是全局手术」——downstream 数字决定了测试范围
- 架构评审时，对「候选重构模块」做影响量化：改哪个代价最小？
- 遗留系统拆分规划：downstream 很高的模块先不动，从边缘模块开始清理

---

### --hub-analysis [--top N] — 架构核心节点识别

**输出**：按扇入（被多少模块引用）和扇出（引用了多少模块）排序的全仓库模块列表，直接揭示真实核心节点。

**深层价值**：目录名 ≠ 重要性。命名为 `core/` 的不一定是实际核心；真正的高耦合节点往往藏在不起眼的工具类、数据模型或配置模块里。扇入高 = 很多人依赖它，扇出高 = 它依赖很多人，两者都高 = 「蛛网中心」，改动最危险。

**适用场景**：
- 架构评审：找出「明星模块」——被所有人依赖却从不在路线图里出现的那个
- 技术债优先级排序：扇入高 + git-stats risk high = 最值得重构的目标（风险高、影响大）
- 遗留代码清理入口：扇出极高但扇入很低的模块，是可以安全替换或拆分的「孤立节点」
- 新同学接手项目：先看扇入 Top 5，这几个模块搞懂了，项目的一半架构就清楚了

---

### --summary — 全局目录聚合

**输出**：按顶层目录分区统计模块数/类数/函数数/行数，附带各区域的 import 关系。

**深层价值**：用一条命令建立系统分层意识。哪个目录是「业务逻辑层」、哪个是「基础设施层」、哪个是「测试层」，从 import 关系图里直接读出来比读任何文档都客观。

**适用场景**：
- 项目初次接触（5 秒摸清全局）：比读 README 更客观，比手动 ls 更结构化
- 识别循环依赖风险区域：两个顶层目录互相 import 是架构坏味道，`--summary` 立刻暴露
- 项目交接给新成员：一张聚合表替代冗长的架构介绍文档
- 评估测试覆盖均衡性：tests 目录的函数数 vs src 目录的函数数，比例是否合理

---

### 场景速查

| 你此刻的问题 | 用哪个 |
|-------------|--------|
| 这个文件有哪些类/方法，各在哪几行 | `--file` |
| 改这个接口/删这个函数，哪些文件跟着改 | `--who-imports` |
| 这个改动最终会影响多少模块 | `--impact` |
| 这个改动风险有多高（加 git 热度） | `--impact --git-stats` |
| 项目里谁是真正的高耦合中心 | `--hub-analysis` |
| 整个项目的模块分布和层级关系 | `--summary` |
| 连续重构任务，改完一处要看影响链 | `--who-imports` → `--impact` |
| 估算技术债改造的工作量 | `--hub-analysis` → `--impact` |

---

## 🧠 执行守则

### 守则1: 先读引用再查询

在使用 `--impact` 或 `--who-imports` 分析某个模块前，建议先用 `--file` 读取其骨架，
理解它的职责和现有 import，避免对查询结果产生误判。

### 守则2: git-stats 是加分项，不是硬阻塞

没有 `.git` 或 git 历史不足时，跳过 `git_detective.py`，只用 AST 数据查询。
不要因为缺少 git 数据而停止查询，降级继续。

### 守则3: 路径匹配灵活但要验证

`query_graph.py` 支持路径片段匹配（如 `vision.py` 可匹配 `src/core/vision.py`）。
当结果返回 `[NOT FOUND]` 时，先用 `--summary` 确认仓库中存在的模块路径格式，再重新查询。

### 守则4: 结果直接呈现，不过度解读

`--impact` 返回的 `X upstream, Y downstream` 是客观数字，直接告知用户。
不要用「可能影响较大」这类模糊词替代数字——让数字说话。

---

## ✅ 输出质量自检

- [ ] 查询前确认 `ast_nodes.json` 路径正确，文件非空
- [ ] 若 `[NOT FOUND]`：已用 `--summary` 核实路径格式，重新查询
- [ ] `--impact` 结果：已明确给出 upstream/downstream 的具体数字
- [ ] `--who-imports` 结果：按源码文件 / 测试文件分类展示，更直观
- [ ] 若叠加 `--git-stats`：已说明 git 风险等级的含义（high=90天内改动多）
