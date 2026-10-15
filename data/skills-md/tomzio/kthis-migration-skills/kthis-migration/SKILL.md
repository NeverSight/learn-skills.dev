---
name: kthis-migration
description: 把遗留 KTHIS / eHealth（Eclipse RCP + SWT，Java 6 / GBK）的某个功能迁移、重写、移植、1:1 还原到 WebHIS（React 18 + antd 4 + dva 前端 / Spring Boot 2.7 + MyBatis 后端）时使用。覆盖「端到端追踪遗留链路 → 逐层映射并落地后端 webhis-<mod>-* 接口 → 落地前端 src/pages/<mod>/ 页面·弹窗·model·注册·i18n → 按门禁验证」的完整流程。当用户提到 KTHIS、eHealth、遗留/旧系统、SWT、RCP、Eclipse 插件、按遗留代码实现，或要在 webhis-front / webhis-server 里落地一个「从旧系统迁过来」的页面 / 弹窗 / 接口时使用 —— 即使用户没有明说「迁移」二字。
---

# KTHIS → WebHIS 功能迁移

本 skill 指导把遗留 HIS（KTHIS / eHealth，Eclipse RCP + SWT 厚客户端）的某个功能，端到端重写为 WebHIS（React 前端 + Spring Boot 后端）。**遗留系统是业务逻辑的唯一事实来源**，新侧只在「技术栈与 UI 控件」上做等价替换，不做像素级复刻。

**核心理念**：先把遗留功能端到端跑通、拿到证据，再动手写新代码；不要凭文档或截图臆测（取舍见「三条硬约束」）。

> **用法**：本文件只给「何时用 + 六阶段流程 + 门禁 + 硬约束速查」；细节都在 `references/*`，**按阶段按需读取**，不要一次全读。

## 何时使用 / 何时不用

- **用**：「把遗留系统的 XX 功能迁移 / 重写到新前端 / 后端」「按遗留代码实现 XX 页面 / 弹窗 / 接口」「XX 功能新侧怎么做、对应遗留哪里」；为实现而**查阅**既有迁移设计文档 / 接口清单（`docs/migration/` 等）—— 本技能只查阅、不产出文档。
- **不用**：单纯的新侧功能增改（没有遗留对应物）—— 直接按仓库规范做即可，但 `references/repos-and-map.md` 的命令与约定仍可参考；遗留系统自身的维护 / 编译；**只写 / 改迁移设计文档、整理截图** —— 用 `kthis-migration-plan` 技能。

## 与其他技能的关系（迁移分两段）

迁移按「**先设计文档，后编码实现**」两段推进，本技能负责**第二段：编码实现** —— 后端 `webhis-<mod>-*` 接口 + 前端 `src/pages/<mod>/` 页面/弹窗/model/注册/i18n + 按门禁验证。

- **分工口径**：说「写 / 生成 / 整理迁移文档、详细设计、分册、实施计划」→ 用 `kthis-migration-plan`（产出 `docs/migration/<NN-模块>/` 分册设计文档：界面布局、字段/控件、UI 交互、关联事件、接口清单、实施计划与阶段门禁）；说「实现 / 迁移 / 还原这个功能、写页面 / 弹窗 / 接口」→ 用本技能。
- 开工前先读设计文档（若已有）：它决定页面拆分、字段与控件顺序、事件清单；实现中若发现文档与遗留源码不符，**回改设计文档**（文档是实现的唯一依据）。没有文档也可直接实现，但建议先用 `kthis-migration-plan` 补齐，降低返工。
- 遗留截图（`docs/migration/images/`）的识别 / 改名 / 引用更新属**文档阶段**，见 `kthis-migration-plan` 技能的 `references/screenshots.md`。

> **前端规范是强制基准**：只要生成或修改前端代码，就必须遵循 **`webhis-front` 技能 + 仓库 `.agents/rules/*`**（`FrontNormalize.md`、`page-norm.md`、`tableRule.md`、`componentUseRule.md`、`componentActionRule.md`、`servicesApiRule.md`、`pageStyleRule.md`）。两个迁移技能都是**可选**加速器，冲突时以 `webhis-front` / `.agents/rules/` 为准。

## 三条硬约束（每次都要记住）

1. **代码优先于文档**。截图表意不完整、文档可能滞后；字段、码表、校验、默认值、显隐/禁用、保存/删除/调价流程一律回遗留源码核对。
2. **GBK ↔ UTF-8，绝不直接拷贝字节**。遗留是 Java 6 + GBK，新侧前端 / 后端都是 UTF-8；跨边界必须转码或重录中文，复制字节会得到乱码。
3. **不要凭模块名猜归属**。模块编码有重命名、拆分、合并、新建，且可能存在「同名却无业务代码的空壳模块」；**必须读新侧代码确认**目标模块与包路径。

## 三仓库与入口

迁移横跨遗留 KTHIS/eHealth（业务真源）、webhis-front（新前端）、webhis-server（新后端）。⚠️ **仓库路径因开发者机器而异，不要假设固定的绝对路径**：从**项目根** `.agents/paths.env` 读 `KTHIS_LEGACY_DIR` / `WEBHIS_FRONT_DIR` / `WEBHIS_SERVER_DIR`（唯一配置文件，可用环境变量 `KTHIS_MIGRATION_CONFIG` 覆盖位置）；缺失或失效时运行 `scripts/setup-paths.sh`（自动探测并写出），或直接问用户。路径配置模板随技能提供（`paths.env.example`）；项目 `.agents/` 缺失时 `scripts/setup-paths.sh` 会自动创建，并把模板落位到项目 `.agents/paths.env.example`。执行自带脚本用「skill 根目录 + 相对路径」。

- 每个仓库的 `AGENTS.md` 是**最新、最权威的本地约定**，动手前先读对应仓库的那一份；本 skill 只做迁移流程的组织与速查。
- 逐层映射、各仓库命令、模块改名速查、主数据通用约定、迁移文档索引、已落地样例 → 读 **[references/repos-and-map.md](references/repos-and-map.md)**。

## 工作流（六阶段）

### 阶段 0 · 定位与定界

明确要迁的**界面/功能**（遗留 Editor / Page 的 ID 或中文标题）与业务域 → 在 `ui.<mod>.*` 插件里定位入口（`plugin.xml` 的 extension / Editor ID / Page ID）→ 新侧确认目标模块（后端 `webhis-<mod>-api`、前端 `src/pages/<mod>/`）。**不要按旧模块码推断。**

### 阶段 1 · 遗留侧端到端追踪（必须产出证据）

链路：**SWT 视图 → 事件 → `action` 契约 / `I*Service` → server impl → iBATIS map（SQL）→ 数据库表**。

- 记录：字段清单与类型、码表与默认值、显隐/禁用/联动规则、校验与提示语、保存/更新/删除/调价的调用顺序与事务边界、系统参数。
- 对照 `docs/migration/` 对应分册，**但以源码复核**（截图只核对标签与控件顺序，不保证完整）；读遗留源码用 GBK 转码，按中文 / 标识符检索用 `scripts/grep-gbk.sh`。
- 产出「证据笔记」：每条结论都标出来源文件（+ 关键行/方法）。

方法、目录结构、GBK 命令、i18n 文案提取、Oracle 表结构对照 → 读 **[references/legacy-tracing.md](references/legacy-tracing.md)**。

### 阶段 2 · 新侧落点确认

- 后端：确认或新建 `webhis-<mod>-api / -server / -server-impl / -model` 四模块下的落点；前端：确认 `src/pages/<mod>/` 的目录、`componentId` 命名、注册表位置、`services/` 位置。
- 先查端点是否已存在：后端仓库的迁移接口清单（若存在，形如 `docs/<功能>/02-接口.md`）或直接 grep controller。
- 复用优先：公共下拉 `/his/common/dropdown/*`、既有 search 接口、共享组件，避免重复造轮子。

### 阶段 3 · 后端接口层（如需新增/改造）

四步走：`-api` 加 `@PostMapping` → `-server` 加 `I*Service` 方法 + VO → `-server-impl` 实现 → 需要新 SQL 再加 DAO 方法 + `resources/mapper/*Dao.xml`。

- URL 一律 `/his/<mod>/<resource>`；**无统一 Result 包装**，直接返回 VO/List；分页 `PageableRespVo<T>` + PageHelper（oracle）。
- 主数据通用约定（`defunct_ind` / 审计字段 / `entity_mstr_id`）；iBATIS → MyBatis 3 改写，`$...$` 拼接的表名 / 排序列必须校验防注入。
- 免登录接口进 `RequestAuthInterceptor.IGNORED_PATHS`；遗留里在方法内自建系统会话的接口（如收费 / 退费类），移植时**一并保留**。
- 模块在仓库里**还不存在**时，先按「从零新建业务模块」补齐（四处注册缺一不生效）。

分层细节、新建模块脚手架、四步模板、active-record 写法、事务与异常、系统参数、鉴权、MyBatis 写法、坑 → 读 **[references/backend-porting.md](references/backend-porting.md)**。

### 阶段 4 · 前端实现

- 懒加载 + 注册：`@loadable/component` + `dynamicModule`，在 `<mod>ComponentRegistry.js` 注册。
- model 继承基类（`@webhis/shared/app/model/*`）：页面 `extendPage`（需未保存校验用 `extendEditablePage`）、弹窗 `extendPopup` / `extendEditablePopup`、带患者条 `extendWpbPage`。
- 请求走 `@webhis/shared/utils/request` 的 `get/post/postWithParam`（**最后参数必须传 `this`**）；弹窗统一 `app/openComponentPopup` + `componentId` 打开（`putPromise` 拿返回值），**禁止直接 import baseUi 的 Dialog**。
- 权限：`componentAction.ts` 声明 actions（`require.context` 自动收集），model `init` 里 `mergeComponentAction` 合并；注册与权限不依赖文案，**先落地**。
- i18n：**实现阶段可先写中文字面量（便于调试）**；功能稳定后再按「i18n 补齐」阶段统一抽成 `message.json` —— 细则（每个菜单页面一份、`componentId` 三处一致）见 [references/frontend-porting.md](references/frontend-porting.md) §4。

**动手写界面前，按这个顺序读完再动手**（第一次生成最常见的返工原因就是没读全这几份）：

1. **迁移文档的布局规范**（本模块目录里的 `00-前端布局规范.md`，或迁移文档根的同名册）—— 界面长什么样、怎么排的**具体数值**全在这里（骨架、栅格每行几对、`templateColumns`、分区顺序、组件对照、表格与按钮约定、尺寸）。它是**当前界面的实现依据**，不是参考。
2. **仓库 `.agents/rules/`**：`page-norm.md`（模型 / 注册 / effect / 弹窗打开）、`pageStyleRule.md`（样式与对齐）、`componentUseRule.md`（表单控件）、`tableRule.md`（表格）。
3. **本技能 [references/frontend-porting.md](references/frontend-porting.md)** —— 迁移特有的落点与坑；末尾 **§8 处置顺序**、**§9 表单布局短规则**、**§10 落地前自查清单**。

写完一个界面**立刻**按 §10 逐条自查，并做元素级截图与遗留截图并排比对（见 frontend-porting §7 与 e2e-verification §4.1）—— 不要等整个功能做完再统一查。

### 阶段 5 · 验证门禁与提交

- **G1 静态检查**：改动文件 `yarn lint:js` 无新增错误/警告；`npx tsc --noEmit -p tsconfig.root.json` 通过（跑完删仓库根未跟踪的 `tsconfig.root.tsbuildinfo`）。
- **G2 构建**：改了 `packages/*` 才需 `yarn build:deps`（否则主应用拿旧产物）。
- **G3 端到端手测**：起 dev server（前端 `yarn dev`；后端 `./startup.sh dev` 起 9800，或用本地 mock），按遗留 / 设计文档逐条实测，表现一致。留证可手动浏览器走查 + 人工截图；本地若已装 **Playwright MCP**（可选）可用 `browser_*` 工具驱动。清单（P1–P10）与证据格式见 **[references/e2e-verification.md](references/e2e-verification.md)**。
- **G4 无回归**：重跑前序关键路径手测；**G5 评审确认**：用户确认后再推进 / 提交。

后端改动用 `mvn -pl webhis-<mod>-server-impl -am install`（或 `./startup.sh dev`）；后端验证不止编译——**接口逐个自测 + 落库核对 + 与遗留行为比对**，清单见 **[references/backend-verification.md](references/backend-verification.md)**。提交用 Conventional Commits（中文描述），经 GitLab MR 合入。**不要声称「测试通过」**（前后端都没有可用的测试框架）。

## 硬约定速查（最易踩的坑）

**前端**（细节见 [references/frontend-porting.md](references/frontend-porting.md)）

- effect 的 `context` 挂在**第一个参数（action）上**：必须写 `*effect({ payload, context: { namespace } }, { put, select, callService })`；写成第二个参数会运行时抛错，且 lint / tsc 都发现不了（症状：点了没反应）。
- service 方法最后一个参数必须传 `this`；**禁止用 `updateState` 改二级数据结构**，复杂 state 变更写专门 reducer。
- 别把刷新逻辑塞进 `init`：切回页签的刷新由基类调度到 `refresh` effect。
- 表格 key 用 `${id}_${index}`，不要用 index；`VirtualTable` 的 `vid` 命名 `模块_文件名_xxx`。
- ESLint 禁导：`moment`（用 dayjs）、`lodash` / `lodash/*`（用 `lodash-es`）、`@brickio/ui`（用 `@/base/ui`）；生产构建会剥离所有 `console.log`。

**后端 / 数据**（细节见 [references/backend-porting.md](references/backend-porting.md)）

- 响应形态不统一：有的 controller 返回裸对象/数组（无 `{code,data}`、无分页 total），写前端请求层前先看具体 controller；无全局 `@ControllerAdvice`，业务直接 `throw new BizException(...)`。
- 模块名 ≠ 业务归属；包名多为 `com.karrytech.webhis.<mod>`，个别模块例外（先读代码）。
- 构建需 **JDK 8**；必须用仓库根 `settings.xml`（内网 Nexus）。
- iBATIS `#param#` / `$literal$` → MyBatis `#{param}` / `${literal}`。

## 参考文件

- [references/repos-and-map.md](references/repos-and-map.md) —— 三仓库与路径配置、各仓库命令、逐层映射、模块归属确认、主数据通用约定、迁移文档索引、已落地样例。
- [references/legacy-tracing.md](references/legacy-tracing.md) —— 遗留侧端到端追踪方法、GBK 检索、证据笔记模板。
- [references/backend-porting.md](references/backend-porting.md) —— 后端四模块分层、从零新建模块、四步加接口、active-record model、事务与异常、系统参数、MyBatis、鉴权、坑。
- [references/backend-verification.md](references/backend-verification.md) —— 后端验证：接口自测（E1–E7）、落库核对（D1–D8）、与遗留比对、证据留存格式。
- [references/frontend-porting.md](references/frontend-porting.md) —— **迁移特有**的前端落点与坑、布局 / 对齐问题的处置顺序。
- [references/e2e-verification.md](references/e2e-verification.md) —— 前端端到端验证：起服务走查、留证、采集报错；清单 P1–P10 与证据格式。
- [scripts/grep-gbk.sh](scripts/grep-gbk.sh) / [scripts/setup-paths.sh](scripts/setup-paths.sh) —— GBK 遗留源码中文检索 / 探测并写出本机三仓库路径。
- 项目根 `.agents/paths.env` —— 本机私有路径配置（**唯一配置文件**，已 gitignore）；模板随技能提供（`paths.env.example`），缺失时 `scripts/setup-paths.sh` 会自动落位到项目 `.agents/paths.env.example`。
- **references/fast-path.md** —— 快速路径与准确性红线：哪些提速允许 / 禁止、免文档的适用判据。
