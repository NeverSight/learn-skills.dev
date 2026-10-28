---
name: pdlc-db-migrate
description: 按数据库设计生成与管理迁移脚本（先沿用项目已有的迁移工具），不直接连库执行 SQL
argument-hint: "<迁移描述 | 版本号>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: engineering
produces:
  - backend/migrations/**
requires: []
next_step: null
terminal_state: null
---

# 数据库迁移管理

<!-- @include templates/prompts/iron-law-tool.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁（工具型命令）**

本命令不是主链路上的阶段：**不追加 `history`，不改 `current_stage` / `next_step` / `last_phase_result`**，也不为此分配功能ID。以下规则不可协商：

1. **文件必须落盘**：正文要求创建的文件必须作为实际文件写入磁盘，不可仅在对话中输出（只要求在对话里输出的，照正文办）。
2. **自检必须执行**：产出后按本命令的自检项逐项核对，不得以"已经很好了"为由跳过。
3. **防循环**：修复只做一次，不递归。修不了的问题记进报告，继续往下走。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law-tool.md -->

根据 db-design 文档管理数据库迁移脚本，支持生成、执行、回滚和状态查看。

## 子命令解析

从本命令的参数中解析子命令和选项：

| 子命令 | 格式 | 说明 |
|--------|------|------|
| `generate <描述>` | 根据 db-design 文档生成版本化迁移脚本（up + down） |
| `status` | 查看迁移状态，列出已执行/待执行的迁移 |
| `up` | 执行所有待执行的迁移 |
| `down [N]` | 回滚最近 N 个迁移（默认 1） |
| `diff <功能名>` | 对比 db-design 文档与现有迁移脚本，生成增量迁移 |

如果未提供子命令或子命令无法识别，输出以上帮助信息后停止。

---

## PDLC 前置检查（仅 generate 和 diff 子命令）

当子命令为 `generate` 或 `diff` 时执行：

1. 从用户输入中提取功能名称关键词
2. 在 `docs/02_design/database/` 目录下搜索包含该关键词的数据库设计文档
   - 匹配新格式：`F<日期>-<编号>-*<关键词>*-db.md`
   - 匹配旧格式：`YYYYMMDD-*<关键词>*-db.md`
   - 同时检查文件内容中是否包含该关键词
3. **未找到** → 输出以下信息后**立即停止，不继续执行**：
   ```
   ⛔ PDLC 守卫：未找到与「<功能名>」相关的数据库设计文档。
   迁移脚本必须基于已有的数据库设计。请先运行：
   👉 /pdlc-db-design <设计目标>
   ```
4. **找到** → 提取功能ID（如 `F20260326-090000`），读取该设计文档内容，继续执行

---

<!-- @include templates/prompts/layout-detect.md（已内联于下方，无需另读） -->
## 先探测项目布局（不要套用写死的目录）

下文出现的 `backend/services/`、`frontend/web/` 等路径只是**空项目时的默认布局**。动手创建或扫描目录之前，先看项目实际长什么样：

1. **monorepo 标志**：`pnpm-workspace.yaml`、`turbo.json`、`nx.json`、`lerna.json`、`package.json` 的 `workspaces`、
   `go.work`、`Cargo.toml` 的 `[workspace]`、`settings.gradle(.kts)` 的 `include` → 按其中声明的目录（如 `apps/`、`packages/`、`services/`、`crates/`）理解布局
2. **已有单元的位置**：在 `backend/services/`、`services/`、`apps/`、`packages/`、`cmd/`、`crates/` 下找已存在的服务 / 应用，新单元放在**同级**，命名与目录结构照着已有的来
3. **单体与全栈框架**：只有一个 `src/`，或是框架默认结构（`manage.py` + 各 app、Rails 的 `app/`、Next.js 的 `app/` / `pages/`、Spring Boot 单模块）→ 按框架约定放，**不要**新建 `services/` 一类平行目录
4. **空项目或判断不了** → 才用下文的默认布局；执行前把将要创建的路径列给用户确认（`--autonomous` 下记入 `auto_decisions[]`）

把探测结论写进本次报告：**布局类型 + 依据的文件 + 新内容的落点**。判断错了的代价是在用户仓库里长出一套平行目录，比多问一句贵得多。
<!-- @include-end templates/prompts/layout-detect.md -->

## 先探测已有的迁移工具

项目已经有迁移体系时，**沿用它**：目录、命名、up / down 写法都照它的来，本命令只按它的约定生成文件，不另起一套。

| 特征 | 工具 | 沿用什么 |
|---|---|---|
| `prisma/schema.prisma`、`prisma/migrations/` | Prisma | 改 schema 后由 `prisma migrate dev --create-only` 生成，不手写 SQL 文件名 |
| `alembic.ini`、`alembic/versions/` | Alembic | `alembic revision -m "<描述>"` 生成，在 `upgrade()` / `downgrade()` 里写 |
| `manage.py` + 各 app 的 `migrations/` | Django | `python manage.py makemigrations` |
| `knexfile.*`、`migrations/*.js` | Knex | `exports.up` / `exports.down` |
| `db/migrate/*.rb` | Rails | `bin/rails generate migration` |
| `flyway.conf`、`db/migration/V*__*.sql` | Flyway | `V<版本>__<描述>.sql`，撤销用 `U` 前缀 |
| `liquibase.properties`、`changelog*.xml/yaml` | Liquibase | changeSet + rollback |
| `migrations/*.up.sql` + `*.down.sql` | golang-migrate / sqlx 等 | 成对的 up / down 文件 |

**都没有**时才用下面的默认约定，并把「本项目此前没有迁移工具」写进报告。

## 迁移文件约定

### 目录结构

- 微服务项目：`backend/services/<service>/migrations/`
- 单服务项目：`migrations/`
- 自动检测：如果存在 `backend/services/` 目录，按微服务项目处理；否则按单服务项目处理

### 文件命名

- UP 脚本：`V<版本号>__<描述>.sql`
- DOWN 脚本（回滚）：`U<版本号>__<描述>.sql`
  > ⚠️ 不要用 `R` 前缀：Flyway 把 `R` 当作**可重复迁移**（内容一变就重跑），回滚脚本会被当成普通迁移执行；Flyway 的撤销前缀正是 `U`。
- 版本号格式：`YYYYMMDD_HHMMSS`（如 `20260402_143052`）

### 文件头部注释

每个迁移文件必须包含以下头部注释：

```sql
-- ==============================================
-- 迁移脚本: V20260402_143052__create_users_table.sql
-- 功能ID: F20260402-090000
-- 描述: 创建用户表
-- 作者: <从 git config 获取>
-- 日期: 2026-04-02
-- ==============================================
```

---

## 子命令执行流程

### generate <描述>

1. 执行前置检查，读取 db-design 文档
2. 读取 本 skill 目录下的 `assets/db-migrate-template.md` 模板
3. 生成版本号：使用当前时间戳 `YYYYMMDD_HHMMSS`
4. 从 db-design 文档中提取 DDL 脚本和回滚脚本
5. 生成 UP 迁移文件：`V<版本号>__<描述>.sql`
   - 包含头部注释
   - 包含 CREATE TABLE / ALTER TABLE / INSERT 等语句
   - 每条语句末尾添加分号
6. 生成 DOWN 迁移文件：`U<版本号>__<描述>.sql`
   - 包含头部注释
   - 包含对应的回滚操作（DROP TABLE / ALTER TABLE DROP COLUMN 等）
   - 操作顺序与 UP 相反
7. 更新迁移历史记录文件 `migrations/migration_history.md`
8. 输出生成结果摘要

### status

1. 查找迁移目录下所有 `V*.sql` 文件
2. 读取 `migrations/migration_history.md`（如不存在则提示无迁移记录）
3. 输出迁移状态表格：

   ```
   📋 迁移状态

   | 版本号 | 描述 | 功能ID | 状态 | 执行时间 |
   |--------|------|--------|------|----------|
   | 20260402_143052 | 创建用户表 | F20260402-090000 | ✅ 已执行 | 2026-04-02 14:35 |
   | 20260402_150000 | 添加订单表 | F20260402-100000 | ⏳ 待执行 | - |

   已执行: 1 | 待执行: 1 | 总计: 2
   ```

### up

1. 读取 `migrations/migration_history.md` 确定已执行的迁移
2. 扫描迁移目录，找出所有待执行的 `V*.sql` 文件
3. 按版本号升序排列
4. 逐个输出待执行的 SQL 内容，并提示用户确认
5. 用户确认后，更新 `migrations/migration_history.md` 中的状态为「已执行」
6. 输出执行结果摘要

> **注意**：本命令不直接连接数据库执行 SQL。它展示待执行的脚本内容，由用户在数据库客户端中手动执行，然后更新迁移历史记录。

### down [N]

1. 读取 `migrations/migration_history.md` 确定已执行的迁移
2. 取最近 N 个已执行的迁移（默认 N=1）
3. 按版本号降序排列
4. 找到对应的 `U*.sql` 回滚文件
5. 逐个输出回滚 SQL 内容，并提示用户确认
6. 用户确认后，更新 `migrations/migration_history.md` 中的状态为「已回滚」
7. 输出回滚结果摘要

> **注意**：与 `up` 相同，本命令不直接执行 SQL，由用户手动执行后更新记录。

### diff <功能名>

1. 执行前置检查，读取 db-design 文档
2. 扫描迁移目录下已有的 `V*.sql` 文件，提取已定义的表结构
3. 对比 db-design 文档中的表结构与已有迁移脚本
4. 识别差异：
   - 新增的表 → 生成 CREATE TABLE
   - 新增的字段 → 生成 ALTER TABLE ADD COLUMN
   - 修改的字段 → 生成 ALTER TABLE MODIFY COLUMN
   - 新增的索引 → 生成 CREATE INDEX
   - 删除的索引 → 生成 DROP INDEX
5. 生成增量迁移的 UP 和 DOWN 文件
6. 更新迁移历史记录
7. 输出差异摘要

---

## 迁移历史记录

在迁移目录下维护 `migration_history.md` 文件：

```markdown
# 迁移历史

| 版本号 | 描述 | 功能ID | 执行时间 | 状态 |
|--------|------|--------|----------|------|
| 20260402_143052 | 创建用户表 | F20260402-090000 | 2026-04-02 14:35 | 已执行 |
| 20260402_150000 | 添加订单表 | F20260402-100000 | - | 待执行 |
```

状态值：`待执行` | `已执行` | `已回滚`

---

## 要求

<!-- @include templates/prompts/output-language.md（已内联于下方，无需另读） -->
🌐 **Output language for generated artifacts**

All generated artifacts (PRDs, design docs, code comments, review reports,
test plans, deployment manuals, changelog entries, etc.) follow this policy:

1. **Default — match the conversation language exactly**:
   - 用户用中文与 Claude 对话 → 产中文文档、中文代码注释、中文报告
   - User talks to Claude in English → produce English artifacts
   - User talks in another language → produce artifacts in that language
   - **Never silently default to a fixed language regardless of the user's input.**

2. **Explicit override always wins**: when the user specifies a language for
   an artifact (e.g. "write the PRD in English", "用英文写 API 设计文档",
   "output the deploy doc in Japanese"), use that language for that artifact,
   regardless of conversation language.

3. **Mixed-language requirements**: if the user wants some artifacts in one
   language and others in a different language (common: Chinese PRD + English
   API docs for partners), honour each per-artifact instruction.

4. **Uncertain**: if you cannot reliably detect the conversation language,
   ask once before producing the first artifact.

This policy applies to **content** (prose, comments, headings). It does
**not** override technical conventions like English variable names, English
git commit subjects, or English error codes when the project's conventions
require them.
<!-- @include-end templates/prompts/output-language.md -->
- SQL 关键字使用大写（CREATE TABLE、ALTER TABLE 等）
- 每个迁移文件只包含一个功能的变更，保持原子性
- 回滚脚本必须能完全撤销对应的 UP 脚本
- 生成的 SQL 遵循 db-design 文档中的字段命名和类型约定
- 版本号严格递增，不允许插入历史版本

迁移操作: $ARGUMENTS

<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->

**本命令的 handoff 输出：**

```
✅ 数据库迁移脚本 完成
📦 产出：backend/migrations/V<版本号>__<描述>.sql
👉 下一步：（本次流程结束，无后续）
```
