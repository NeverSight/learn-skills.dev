---
name: create-skill
description: 当你要创建/新增一个 skill，或重写/更新某个 skill 的 SKILL.md（结构、约定、模板）时使用。
---

# Create Skill（本仓库约定）

## 1) 目录结构与命名

每个 skill 一个目录，目录名与 frontmatter 的 `name` **完全一致**：

- `name` 约束：
  - 仅允许小写字母/数字/连字符：`a-z`、`0-9`、`-`
  - 不能以 `-` 开头或结尾
  - 不能包含连续 `--`

推荐结构：

```
skills/<skill-name>/
  SKILL.md
  scripts/        # 可选：可执行工具
  references/     # 可选：按需阅读的资料
  assets/         # 可选：模板/静态文件
```

## 2) SKILL.md（必需）

### 2.1 Frontmatter（必需：name / description）

```yaml
---
name: your-skill-name
description: 用一句话说明“做什么 + 何时使用（包含关键词）”。
---
```

可按需添加其他字段；本仓库不强制要求，但建议保持精简。

`description` 要求：
- 非空
- 必须同时覆盖“做什么”+“何时使用”
- 尽量包含用户会说出口的关键词（提升触发命中率）

### 2.2 正文（只写最短可用流程）

正文只保留“让使用者（人或 AI）直接开始执行”的信息。大段背景/资料放到 `references/`，模板/静态文件放到 `assets/`。

推荐顺序（按需取舍）：
1) 一句话说明（这是什么/解决什么）
2) Quick start（最短可复制示例）
3) 常用场景/命令（3-7 条为宜）
4) 输出约定（如机器可读输出，明确 `--json` 等约定）
5) 冷门参数怎么查（`--help` + reference 指针）
6) 资源（指向脚本/参考资料/模板）

最小骨架（可复制改名）：

````markdown
---
name: your-skill-name
description: 做什么；何时使用（关键词）。
---

一句话说明。

## Quick start

```bash
cd skills/your-skill-name && ./scripts/your_tool.py --help
```

## 常用场景
- `./scripts/your_tool.py ...`

## 冷门参数怎么查
- `./scripts/your_tool.py --help`
- 需要字段细节时读：见 [api.md](references/api.md)

## 资源
- [tool.py](scripts/tool.py)
````

## 3) scripts/（可选）

如果某个流程需要“确定性执行”或经常重复，优先写成可执行脚本放在 `scripts/`，并在 `SKILL.md` 中给出可复制命令。

本仓库对 Python 脚本的约定（SKILL.md 里要写清楚）：
- 统一通过 `./scripts/...` 直接执行（不要用 `uv run python ...` / `python ...`）
- workdir 约定：默认以当前 `SKILL.md` 所在目录作为 workdir；示例命令如需 `cd`，应写清楚（通常 `cd skills/<skill-name>`）
- 在 `SKILL.md` 中引用脚本/资源文件时，优先使用 Markdown URL（链接文本尽量只写文件名）

Python 脚本规范要点：
- **运行模式**：必须使用 uv script 模式（shebang 为 `#!/usr/bin/env -S uv run --script`）。
- **初始化**：新建脚本用 `uv init --script scripts/foo.py`（生成 shebang 与空的 `/// script` 元数据块）。
- **依赖声明（强约束）**：
  - 脚本头部 `/// script` 元数据块是唯一依赖声明位置。
  - 禁止手工编辑依赖块；依赖增删必须通过 `uv add --script ...` / `uv remove --script ...` 完成。
  - 移除依赖引用后，若确认不再使用，应同步移除该依赖。
- **CLI 形态**：
  - 命令行参数优先用 Typer。
  - 输出提示/表格优先用 rich（提升可读性）。
  - 数据模型与参数校验优先用 pydantic（失败信息清晰可定位）。
  - Typer 应用实例变量名使用小写 `app`。
  - 若仅一个 command，优先使用 `typer.run(main)`，避免 `tool.py foo <arg>` 这种多一层子命令。
- **可维护性**：每个模块、函数与类型都应包含简短中文 docstring。
- **质量检查**：完成后建议执行：
  - `uv run ruff check <path>`
  - `uv run ruff format <path>`

常用 `uv --script` 工作流（用于新建/维护脚本依赖）：

```bash
# 在 skill 目录内新建脚本（会生成 shebang 与 /// script 依赖块）
uv init --script scripts/foo.py

# 给脚本添加依赖（会更新脚本头部 dependencies；不要手工改依赖块）
uv add --script scripts/foo.py typer rich

# 从脚本移除依赖
uv remove --script scripts/foo.py rich

# 赋予可执行权限并运行
chmod +x scripts/foo.py
./scripts/foo.py --help
```

## 4) references/ 与 assets/（可选）

- `references/`：放“按需阅读”的长资料（协议/API 字段/术语表）。在 `SKILL.md` 中写清楚“什么时候需要读哪个文件”。
- `assets/`：放模板/静态文件。在 `SKILL.md` 中给出“如何使用该文件”的最短说明。

引用规则（建议）：
- 链接或路径使用相对路径（相对 `skills/<skill-name>/`）
- 尽量“一跳可达”：`SKILL.md` 直接指向目标文件，避免多层链式引用
- 链接文本尽量只写文件名（路径放在链接目标里）

示例（Markdown 链接语法）：

```markdown
见 [api.md](references/api.md)
运行 [tool.py](scripts/tool.py)
```

## 5) 内容长度（token）

- `SKILL.md` 正文推荐 < 5000 tokens
- 可用 [token_count.py](../../scripts/token_count.py) 统计 token 数（脚本与参数不依赖 workdir，只要路径写对即可）：

```bash
cd skills/<skill-name>
../../scripts/token_count.py SKILL.md
```

## 6) 提交前自检清单

- 目录名 == `SKILL.md` 的 `name`
- frontmatter 至少包含 `name` / `description`，且 `description` 写清楚 “做什么 + 何时用（关键词）”
- `SKILL.md` 有可复制的 Quick start（如依赖工作目录或环境变量，需要在示例中写清楚）
- 如有脚本：示例使用 `./scripts/...` 直接执行（不使用 `uv run python`/`python`）
- 如有脚本：依赖只在 `/// script` 里声明（不手改依赖块）；模块/函数/类型有简短中文 docstring
- 如有脚本：建议跑 ruff（`uv run ruff check ...` / `uv run ruff format ...`）
- `references/`/`assets/` 的引用清晰，且 `SKILL.md` 能一跳到达目标文件
- `SKILL.md` token 数在建议范围内
