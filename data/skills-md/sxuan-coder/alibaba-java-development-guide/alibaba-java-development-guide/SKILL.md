---
name: alibaba-java-development-guide
description: 《阿里巴巴Java开发手册（黄山版）》总纲与路由入口。涵盖编程规约、异常日志、单元测试、安全规约、MySQL数据库、工程结构、设计规约七大维度。Use when writing, reviewing, or designing Java code; handling exceptions/logging; writing SQL or designing tables; writing unit tests; designing project architecture; or whenever Alibaba Java standards apply. 本 skill 为目录路由，详细规约按需查阅 data/ 下对应章节文件。
---

# 阿里巴巴Java开发手册（黄山版）— 总纲与路由

## 手册定位

**码出高效，码出质量。**

本 skill 是《Java开发手册（黄山版）》（v1.7.1，2022.02.03 发布）的**总纲入口**。手册以 Java 开发者为中心视角，划分为七个维度。本 SKILL.md 只做**导航路由**，不内联全部条文——详细规约按需从 `data/` 目录取对应章节阅读，避免一次性载入全部内容。

## 规约分级

手册每条规约依据约束力强弱及故障敏感性分为三类，查阅 data 文件时以此判断优先级：

| 级别 | 含义 | 处理原则 |
|------|------|----------|
| **【强制】** | 必须严格遵守 | 违反可能导致严重问题或线上故障，review 时必查 |
| **【推荐】** | 建议遵循 | 有助于提升代码质量，无特殊情况应遵循 |
| **【参考】** | 参考性建议 | 可根据实际团队情况选择，灵活应用 |

每条规约通常包含：**说明**（扩展解释）、**正例**（提倡写法）、**反例**（雷区与真实故障案例）。

## 适用边界

明确本 Skill 的启用与豁免场景，避免在不合适的场景下过度套用规约：

| 场景 | 建议 |
|------|------|
| 生产代码编写 / Review | ✅ **正常启用**，所有规约生效 |
| 快速原型、Demo、一次性脚本 | 🔸 **【推荐】级规约可豁免**，仅遵守【强制】级 |
| 性能极敏感的高频并发代码 | 🔸 方法行数、圈复杂度等规约可酌情豁免，需注释说明理由 |
| 公开 SDK / API 设计 | ✅ **正常启用**，且应从严遵守命名规约与版本兼容规约 |
| 重构存量代码 | 🔸 优先遵循「保持行为不变」原则，可渐进式对齐规约，不要求一步到位 |
| 用户明确声明「关闭阿里规约检查」 | 🛑 **完全禁用**，不应用任何条文 |

## 章节路由表（按需查阅 data/）

当任务命中下列场景时，**先定位对应章节文件，再用 Read 工具读取**该文件的相关小节，依据条文给出结论或修改建议。不要一次性读取全部 data 文件。

| 场景关键词 | 章节 | data 文件 |
|------------|------|-----------|
| 命名风格、常量定义、代码格式、OOP、日期时间、集合处理、并发处理、控制语句、注释规约、前后端规约 | 一、编程规约 | `data/01-coding-standards.md` |
| 错误码体系、异常捕获与抛出、try-catch-finally、NPE 防护、日志框架/级别/输出 | 二、异常日志 | `data/02-exception-logging.md` |
| AIR 原则、测试独立性、覆盖率目标、BCDE、Mock、测试目录 | 三、单元测试 | `data/03-unit-testing.md` |
| 权限校验、敏感数据脱敏、SQL 注入、XSS、CSRF、参数校验、文件上传、防重放 | 四、安全规约 | `data/04-security-standards.md` |
| 建表、字段类型、主键/索引命名、组合索引、分页、count/sum、ORM、resultMap | 五、MySQL 数据库 | `data/05-mysql-database.md` |
| 应用分层（Web/Service/Manager/DAO）、DO/DTO/BO/VO/Query、二方库依赖、GAV、服务器与 JVM | 六、工程结构 | `data/06-project-structure.md` |
| 存储方案评审、用例图/状态图/时序图/类图/活动图、弱依赖与降级、SOLID/DRY、系统设计 | 七、设计规约 | `data/07-design-standards.md` |
| 版本历史、专有名词解释（POJO/DO/DTO/NPE/AQS/GAV 等）、错误码全量列表 | 附录 | `data/08-appendix.md` |

## 触发词映射表

当用户输入包含以下关键词时，**优先查表定位**对应章节，无需依赖推理路由：

| 触发词 / 关键词 | 命中章节 |
|:---|:---|
| JWT、OAuth2、Token、权限注解、@PreAuthorize、认证、授权、登录态 | `04-security-standards.md`（及补充章节） |
| 数据脱敏、加密、加解密、敏感数据、个人信息 | `04-security-standards.md` |
| 防重放、重放攻击、时间戳、nonce、签名校验 | `04-security-standards.md` |
| 分布式事务、Seata、TCC、Saga、最终一致性 | `07-design-standards.md` + 参考微服务专项 |
| 服务降级、熔断、Sentinel、Hystrix、@SentinelResource | `07-design-standards.md` |
| Testcontainers、@SpringBootTest、集成测试、@DynamicPropertySource | `03-unit-testing.md` |
| Mockito、@Mock、@InjectMocks、单元测试覆盖率、AIR | `03-unit-testing.md` |
| 金额、BigDecimal、精度、舍入、setScale | `01-coding-standards.md`(集合/类型) + `05-mysql-database.md` |
| 分页、PageHelper、COUNT 性能、深分页 | `05-mysql-database.md` |
| 索引、联合索引、最左前缀、索引下推、覆盖索引 | `05-mysql-database.md` |
| 线程池、ThreadPoolExecutor、异步、@Async、CompletableFuture | `01-coding-standards.md`(并发) |
| 锁、synchronized、ReentrantLock、分布式锁、Redisson | `01-coding-standards.md`(并发) |
| 日期、时间、LocalDateTime、Date、SimpleDateFormat、时区 | `01-coding-standards.md`(日期时间) |
| 异常、NPE、空指针、try-catch、全局异常处理、@ControllerAdvice | `02-exception-logging.md` |
| 日志、Logback、log4j2、@Slf4j、日志级别、日志规范 | `02-exception-logging.md` |
| 分层、Controller、Service、Manager、DAO、DDD、充血模型 | `06-project-structure.md` |
| DO、DTO、VO、BO、POJO、实体转换、MapStruct | `06-project-structure.md` |
| 二方库、GAV、依赖冲突、maven、gradle、pom | `06-project-structure.md` |

## 按使用场景推荐阅读

根据当前任务类型，只读取对应视角的章节，提高效率：

| 任务类型 | 推荐阅读 | 侧重视角 |
|:---|:---|:---|
| 🖊️ **编写新代码** | `01`（编程规约）+ `02`（异常日志） | **编写视角**：命名、格式、集合、并发、异常处理等即时决策类规约 |
| 🔍 **审查存量代码** | `04`（安全）+ `05`（数据库）+ `06`（工程结构）+ `07`（设计） | **审查视角**：安全漏洞、事务边界、架构分层、设计合理性等全局判断类规约 |
| 🧪 **补充单元测试** | `03`（单元测试） | **测试视角**：AIR/BCDE 原则、Mock、覆盖率、测试隔离 |
| ⚙️ **设计表结构 / 写 SQL** | `05`（MySQL 数据库）+ `07`（设计规约-存储方案） | **数据视角**：建表规范、索引、SQL 性能、ORM |
| 🏗️ **系统架构 / 模块设计** | `07`（设计规约）+ `06`（工程结构） | **架构视角**：分层、依赖、降级、图文档 |
| 🐛 **排查问题 / 分析日志** | `02`（异常日志）+ `04`（安全） | **排查视角**：日志规范、异常处理、安全审计 |

## 规约冲突处理

当同一条代码同时命中多条规约且它们给出的方向不一致时，按以下优先级裁决：

1. **安全优先**【最高】：安全规约优先级高于其他所有规约。涉及数据泄露、越权、注入风险时，其他规约可合理豁免
2. **强制优先**：【强制】> 【推荐】> 【参考】。强制规约覆盖推荐规约
3. **业务合理豁免**：如确因业务场景需要违背某条规约，**必须在代码中添加注释说明理由**，格式建议：`// Alibaba-Java: 豁免原因——<具体理由>`
4. **渐进式改进**：重构存量代码时，「保持行为不变」优先于「一次性对齐所有规约」，可规划分阶段完成

### 常见冲突示例

| 冲突场景 | 裁决 |
|:---|:---|
| 【强制】方法不超 80 行 vs 【推荐】单一职责 | 优先满足单一职责。若拆出的小方法导致类膨胀，是合理的——加注释说明即可 |
| 【强制】禁止魔法数字 vs 性能敏感场景需硬编码 | 加具名常量（`private static final int MAX_RETRY = 3`）而非直接写字面量，两全其美 |
| 【强制】禁止 null 返回 vs 远程调用超时可返回 null | 建议改抛自定义业务异常或返回 Optional，避免调用方 NPE |

## 规约推荐 API 速查（生成 Java 代码时强制使用）

> **本节为代码生成的「主动应用」清单。** 当你在写或修改 Java 代码时，**不要等用户问、不要凭默认习惯**——下列场景命中时，必须直接采用规约推荐的 API/写法，并在注释中标注「阿里规约」以示区分。这是本 Skill 与模型默认行为拉开差距的关键。

| 场景 | ❌ 禁止（反例） | ✅ 强制使用（正例） | 对应章节 |
|:---|:---|:---|:---|
| **日期/时间** | `new Date()`、`new SimpleDateFormat()`、`Calendar` | `LocalDateTime` / `LocalDate` / `Instant` + `DateTimeFormatter`（static final 复用） | 01-(九)日期时间 |
| **入参校验** | `if (id == null) throw new RuntimeException(...)` 手写 | `Objects.requireNonNull(id, "id 不能为空")` 或 `StringUtils.isBlank(id)`（依赖 Spring 时用 `Assert.hasText`） | 02-(二)NPE 防护 |
| **返回空集合** | `return null;` 或 `return Collections.emptyList()` 仅在只读场景 | `return Collections.emptyList();` / `List.of()` / `new ArrayList<>()`（需可变时）——**禁止返回 null** | 01-(六)集合处理 |
| **金额计算** | `double` / `float`、`==` 比浮点 | `BigDecimal`（用 `String` 构造器）+ `compareTo` 比大小 | 01-(六)集合处理 + 05-MySQL |
| **并发 Map/List** | `new HashMap<>()`、`new ArrayList<>()` 用于多线程 | `ConcurrentHashMap<>()` / `CopyOnWriteArrayList<>` / `Collections.synchronizedXxx` | 01-(七)并发处理 |
| **字符串比较** | `==`、`!=` | `.equals()`、`Objects.equals()`；忽略大小写用 `equalsIgnoreCase` | 01-(一)命名风格 |
| **线程创建** | `new Thread()` 裸建 | `ThreadPoolExecutor`（显式命名线程池）或 `CompletableFuture.supplyAsync` | 01-(七)并发处理 |
| **ORM 字段映射** | `${}` 拼接 SQL、字符串拼接查询条件 | `#{}` 参数化 / `PreparedStatement` / `setParameter` | 05-(八)ORM |
| **异常处理** | `catch (Exception e) { }` 吞异常、`e.printStackTrace()` | 捕获具体类型 + 记日志（`log.error("xx 失败", e)`）+ 抛自定义业务异常 | 02-(三)try-catch |
| **布尔命名** | `boolean flag`、`Boolean canRun`（字段加 `is` 前缀） | 字段不加 `is` 前缀：`boolean deleted`；方法用 `isXxx()`/`hasXxx()`：`isDeleted()` | 01-(一)命名风格 |
| **常量定义** | 魔法数字 `if (status == 3)` | `private static final int STATUS_PAID = 3;` 具名常量 | 01-(二)常量定义 |
| **循环拼接字符串** | `String s = ""; for(...) s += x;` | `StringBuilder.append(...)` | 01-(六)集合处理 |

**应用原则**：
1. **生成代码时默认套用**：命中上表场景时，直接写出正例写法，无需询问用户。
2. **review 代码时显式引用**：发现反例时，指出违反的章节编号 + 级别（如「违反 01-(九)【强制】」），并给出正例。
3. **禁止弱化**：即使用户说「简单写一下」，上述【强制】行仍需遵守——可省略注释，但 API 选择不能退化。

## 使用方式

1. **识别任务主题**：根据用户问题（写 Java 代码、review、设计表、写 SQL、异常处理、测试等）匹配上表场景关键词。
2. **按需读取**：只 Read 命中的 `data/*.md` 文件，定位到对应小节（如「(一) 命名风格」「(六) 集合处理」）。
3. **对照条文**：引用规约编号与级别（【强制】/【推荐】/【参考】），给出正例或指出反例风险。
4. **跨章节场景**：如「写一个 Service 方法并设计表」，分别读 `01`、`02`、`05`、`06`，不要凭记忆作答。
5. **动态交互（上下文不足时）**：如果无法从当前对话确定用户项目的技术栈、团队已有规范、或场景边界（如分不清是生产代码还是 Demo），应使用 `AskUserQuestion` 工具询问开发者，而非自行假设。典型场景：
   - 金额字段精度设计——问「用 `BigDecimal` 还是 `Long`（分）？」
   - 新接口幂等需求——问「调用方是否要求幂等？」
   - 代码上下文不明——问「这是生产代码还是原型 Demo？」
6. **个性化配置**：分两层读取，按优先级合并生效。

   **第一层 — 个人偏好（`memory.md`）**：
   - 读取 `memory.md`，载入个人跨项目编码习惯（金额类型、Lombok 偏好等）
   - 不存在则跳过

   **第二层 — 项目规范（`project/<项目名>.md`）**：
   - 从当前工作目录路径推断项目名（取顶层目录名，如 `D:\code\物业系统\contract-service` → `物业系统`）
   - 查找 `project/<项目名>.md`，若存在则读取并合并到 `memory.md` 之上
   - 不存在则跳过

   **初始化流程**（首次加载且对应文件不存在时）：
   - 扫描项目构建文件（`pom.xml`/`build.gradle`）和现有 Java 代码
   - 通过 `AskUserQuestion` 询问关键偏好（个人 1~2 个，项目 2~3 个）
   - 写入对应文件，告知开发者已创建

   **持续维护**：
   - 每次应用规约前按上述合并顺序读取
   - 发现团队隐性规范时，询问是否加入 `project/<项目名>.md`
   - 发现个人新习惯时，询问是否加入 `memory.md`
   - 保持更新日志

## 注意事项

- 内容源自 PDF 转换，少量排版噪声可能残留，引用时以条文语义为准。
- 团队已有规范优先于本手册；本手册用于无团队约定或需参考业界实践的场景。
- 版本：黄山版 1.7.1（2022.02.03），共 7 大维度、附 3 张表（版本历史、专有名词、错误码列表）。
