---
name: dev-decompile
description: 反编译与逆向分析 Android 安装包 (APK/XAPK) 及 Java/Android 依赖库 (JAR/AAR)。用于自动化执行包体指纹侦测、环境依赖检测与安装、多引擎反编译(jadx/vineflower)、架构与清单分析、Kotlin混淆还原、调用链追踪、API接口提取与逆向报告沉淀。当用户输入 /dev-decompile 或明确要求反编译 APK、分析安卓包体结构、提取网络 API 接口、恢复混淆代码、追踪调用链或进行逆向工程分析时使用。
---

# Dev Decompile — Android 反编译与逆向工程工作流

**核心原则：指纹优先、循序渐进、严禁臆测、分层提取、产物归档。**

---

## 触发方式

用户输入 `/dev-decompile` 或带有参数：

```
/dev-decompile
/dev-decompile path/to/app.apk
/dev-decompile path/to/bundle.xapk
```

或自然语言触发：
- "反编译这个 APK / XAPK / AAR"
- "逆向分析这个安卓应用"
- "从这个安装包中提取所有 HTTP API 接口"
- "梳理这个应用的架构和核心调用链"
- "帮我还原这个混淆包里的 Kotlin 代码"

---

## 核心设计原则

1. **指纹优先（禁止盲目反编译）**：在全面反编译前，必须先进行技术栈指纹识别（Phase 2）。若判定为 Flutter / React Native / Xamarin / Cordova 等非原生框架，应及时调整策略或分流，避免在无意义的 Java 宿主代码上耗费大量反编译与分析资源。
2. **渐进确认与提问约束**：每轮最多提问 **2~3 个问题**。涉及依赖安装、反编译引擎选择（jadx / fernflower / both）、是否开启混淆还原（`--deobf`）等重大决策，需与用户确认后推进。
3. **严禁凭空臆测**：所有分析结论、接口定义、参数类型、调用路径必须以反编译源码或资源文件为依据。无法确认的内容一律标记为 `【代码中未发现】` 或 `【待运行时抓包验证】`。
4. **分层提取原则（Tier 1 + Tier 2）**：面对数十上百个接口时，禁止一股脑展开全量细节造成上下文膨胀。一律先输出 **Tier 1 全量端点速览表格**，仅对核心高价值接口（认证、支付、核心业务）展开 **Tier 2 详细规格**。
5. **规范化沉淀归档**：分析完成后，统一按照 [TEMPLATE.md](TEMPLATE.md) 将逆向报告与接口清单归档至：
   ```
   docs/decompile/{包名或应用名}/README.md
   docs/decompile/{包名或应用名}/API_INVENTORY.md
   ```

---

## 阶段流程

```
阶段 1: 目标获取与环境自检 ──→ 确认输入文件，检查并引导安装环境依赖
阶段 2: 包体指纹与架构侦测 ──→ 识别框架(Flutter/RN/Native)、HTTP栈、混淆度、.so库
阶段 3: 多引擎解包与反编译 ──→ jadx / fernflower / both 引擎反编译与解包
阶段 4: 架构剖析与关键入口 ──→ 解析 AndroidManifest、BuildConfig、架构模式
阶段 5: 符号还原与调用链   ──→ Kotlin 元数据恢复(@DebugMetadata)，梳理业务调用链
阶段 6: 接口提取与安全审计 ──→ 扫描提取全量 API、鉴权机制、敏感凭据审计
阶段 7: 逆向文档生成与交付 ──→ 按照 TEMPLATE.md 沉淀文档并交付摘要
```

---

### 阶段 1：目标获取与环境自检

#### 1.1 获取目标文件
- 若用户通过命令参数提供了文件路径，验证该文件是否存在。
- 若未提供，询问用户文件路径（支持 `.apk`、`.xapk`、`.apks`、`.jar`、`.aar`）。

#### 1.2 依赖环境检查
运行依赖检查脚本检查 Java 17+、jadx、vineflower/fernflower、dex2jar：

- **Windows (PowerShell)**:
  ```powershell
  & "skills/dev-decompile/scripts/check-deps.ps1"
  ```
- **Linux / macOS (Bash)**:
  ```bash
  bash skills/dev-decompile/scripts/check-deps.sh
  ```

解析输出中的标识：
- `INSTALL_REQUIRED:<dep>`：必须安装项（Java 17+、jadx）
- `INSTALL_OPTIONAL:<dep>`：可选推荐项（vineflower、dex2jar）

**若缺失必须依赖**：询问用户后执行自动安装脚本：
- Windows: `& "skills/dev-decompile/scripts/install-dep.ps1" <dep>`
- Linux/macOS: `bash skills/dev-decompile/scripts/install-dep.sh <dep>`
若系统需要管理员权限但不可用，按脚本给出的命令指导用户手动安装。
必须依赖验证通过后，方可进入下一阶段。

---

### 阶段 2：包体指纹与技术栈侦测

在反编译 Java 源码前，先对包体进行指纹特征扫描：

- **Windows (PowerShell)**:
  ```powershell
  & "skills/dev-decompile/scripts/fingerprint.ps1" <target-file>
  ```
- **Linux / macOS (Bash)**:
  ```bash
  bash skills/dev-decompile/scripts/fingerprint.sh <target-file>
  ```

扫描输出包含：
1. **移动端框架**：Flutter、React Native、Cordova/Capacitor、Xamarin/.NET MAUI、原生 Native (Kotlin + Compose / Classic)
2. **HTTP 协议栈**：Retrofit、OkHttp、Ktor、Apollo (GraphQL)、Volley
3. **DI / 序列化框架**：Hilt、Dagger、Koin、Moshi、Gson、kotlinx.serialization、Jackson
4. **混淆级别估计**：基于单/双字母根包名密度（LOW / MODERATE / HIGH）
5. **原生动态库 (.so)**：ABI 架构与第三方 SDK 原生库
6. **已知第三方 SDK**：Firebase、Sentry、AppsFlyer、Datadog、Stripe、支付 SDK 等

**分支策略**：
- **若是 Flutter**：业务核心代码在 `lib/<abi>/libapp.so`，Java 源码仅为宿主壳。提示用户转用 `blutter` / `strings libapp.so` 提取 Dart 符号，避免在 jadx 上浪费时间。
- **若是 React Native**：业务代码在 `assets/index.android.bundle`。提示用户若使用 Hermes 字节码应配合 `hbctool`，纯 JS 可格式化直接搜索。
- **若是 Cordova / Capacitor**：代码在 `assets/www/`，直接解压查看 HTML/JS。
- **若是 原生 Kotlin / Java**：继续推进后续反编译阶段。

---

### 阶段 3：多引擎解包与反编译

执行解包反编译脚本：

- **Windows (PowerShell)**:
  ```powershell
  & "skills/dev-decompile/scripts/decompile.ps1" [OPTIONS] <target-file>
  ```
- **Linux / macOS (Bash)**:
  ```bash
  bash skills/dev-decompile/scripts/decompile.sh [OPTIONS] <target-file>
  ```

常用参数：
- `-o <dir>`：指定输出目录（默认 `<文件名>-decompiled`）
- `--deobf`：开启反混淆命名重命名（混淆严重时强烈推荐）
- `--no-res`：跳过资源文件解码（仅提取代码时提速明显）
- `--engine <jadx|fernflower|both>`：
  - `jadx`（默认）：通用首选，同时提取源码与 XML 资源。
  - `fernflower`：复杂泛型、Lambda 表达式反编译质量更高（处理 APK 时自动调用 dex2jar 转换）。
  - `both`：双引擎并行输出至 `jadx/` 与 `fernflower/`，用于对照疑难代码。

**自动处理特例**：
- **XAPK / APKS**：脚本自动提取 zip 内的所有 Split APK，并分别反编译。
- **Split/Bundle 包**：若主 APK 仅为包含 `base.apk` 的精简壳，脚本自动检测并解包真正的 `base.apk`。

---

### 阶段 4：架构剖析与关键入口识别

反编译完成后，对应用整体骨架进行全面剖析：

1. **阅读 AndroidManifest.xml**（位于 `<output>/resources/AndroidManifest.xml`）：
   - 提取应用包名、VersionName、VersionCode
   - 定位启动入口：带 `android.intent.action.MAIN` 和 `CATEGORY_LAUNCHER` 的 Activity
   - 梳理四大组件（Activity、Service、BroadcastReceiver、ContentProvider）
   - 记录关键权限（尤其是 `INTERNET`, `READ_PRIVILEGED_PHONE_STATE`, `ACCESS_FINE_LOCATION` 等）
   - 查看自定义 Application 类（`android:name`）
2. **扫描 BuildConfig.java**：
   - 执行搜索：在 `<output>/sources` 下搜索所有 `BuildConfig.java`
   - 提取环境常数：`BASE_URL`、`DEBUG`、`FLAVOR`、`BUILD_TYPE`、第三方 AppKey 等高价值未混淆常量
3. **识别架构模式**：
   - 观察包结构命名（`api`, `data`, `domain`, `presentation`, `model`, `viewmodel`, `repository` 等）
   - 判定架构模式（MVVM / Clean Architecture / MVI / MVP）

---

### 阶段 5：Kotlin 混淆还原与调用链追踪

#### 5.1 Kotlin 类名元数据恢复（适用于混淆应用）
若应用存在中高混淆且为 Kotlin 编写，利用 R8 无法抹除的 Kotlin 元数据还原真实类名：

- **执行恢复脚本**：
  ```bash
  python skills/dev-decompile/scripts/recover-kotlin-names.py <output>/sources <output>/mapping
  ```
  *(或使用 PowerShell / Bash 包装脚本 `recover-kotlin-names.ps1` / `recover-kotlin-names.sh`)*
- 生成结果：
  - `mapping.tsv` / `mapping.json`：混淆类名与原始真实类名的映射表
  - `by_package/`：按真实包名归类的类索引
- **快速查询与标注检索**：
  ```bash
  python skills/dev-decompile/scripts/lookup-name.py <output>/mapping --grep '"/api/' <output>/sources
  ```
  *(在搜索匹配结果后方自动标注原始类名 `// com.example.service.UserService`)*

#### 5.2 核心业务调用链追踪
按照业务优先级（如：启动初始化、用户登录/认证、核心数据拉取），梳理端到端调用流：
```text
UI 入口 (Activity / Fragment / Composable)
  ↓ 事件触发 (Click / Event / Intent)
ViewModel / Presenter (数据状态流转)
  ↓ 业务调用 (UseCase / Interactor)
Repository (数据仓储，本地缓存 or 远端)
  ↓ 协议封装
Network Service (Retrofit / Ktor / OkHttp)
  ↓ 真实请求
HTTP / WebSocket / RPC (远端接口)
```

---

### 阶段 6：API 接口提取与安全审计

#### 6.1 自动化扫描提取
运行接口提取扫描脚本：

- **Windows (PowerShell)**:
  ```powershell
  & "skills/dev-decompile/scripts/find-api-calls.ps1" <output>/sources/
  ```
- **Linux / macOS (Bash)**:
  ```bash
  bash skills/dev-decompile/scripts/find-api-calls.sh <output>/sources/
  ```

可附加专项参数：
- `-Retrofit` / `--retrofit`：仅提取 Retrofit 注解接口
- `-OkHttp` / `--okhttp`：仅提取 OkHttp 构造与拦截器
- `-Ktor` / `--ktor`：提取 Ktor 客户端请求
- `-Apollo` / `--apollo`：提取 Apollo GraphQL 查询
- `-Urls` / `--urls`：仅提取硬编码 URL 与 IP
- `-Paths` / `--paths`：提取端点路径字面量（混淆穿透扫描）
- `-Auth` / `--auth`：仅提取认证头（Bearer / Basic / Token / 签名）

#### 6.2 敏感信息安全审计
检索敏感凭证与潜在漏洞：
- 密码学硬编码：AES/DES 密钥、硬编码 IV、RSA 公私钥字面量
- 平台与云凭据：AWS S3 Key、阿里云 OSS Key、腾讯云 Secret、Firebase API Key
- 自定义签名算法：HMAC-SHA256 签名逻辑、动态 Token 生成机制、时间戳校验
- 内网/测试域名泄漏：如包含 `staging`, `dev`, `internal`, `10.`, `192.168.` 等 IP 与主机

---

### 阶段 7：逆向文档生成与交付

按照 [TEMPLATE.md](TEMPLATE.md) 组织生成标准逆向文档。

#### 7.1 文档保存路径
```
docs/decompile/{包名或应用名}/README.md          # 综合逆向工程分析报告
docs/decompile/{包名或应用名}/API_INVENTORY.md   # 全量 API 接口清单与规格
```

若文件已存在，使用 `-v2.md` 命名或询问用户是否覆盖。

#### 7.2 交付内容清单
向用户输出结构化总结：
1. **反编译产物目录**（源码路径、映射表路径）
2. **应用基本信息与指纹摘要**（包名、版本、框架、混淆程度）
3. **核心发现摘要**：
   - 架构模式与关键组件入口
   - 提取的 API 数量（按 Retrofit / Ktor / 其他分类）
   - 发现的敏感信息或潜在风险点
4. **生成的文档链接**（指向生成的 Markdown 报告文件）
5. **后续分析建议**（针对深入抓包、Hook 注入、算法还原的下一步指引）

---

## 依赖脚本与参考资料

本技能内置了以下辅助工具与详细参考：

### Scripts
- `check-deps.ps1` / `check-deps.sh`：依赖检测脚本
- `install-dep.ps1` / `install-dep.sh`：依赖一键安装脚本
- `decompile.ps1` / `decompile.sh`：多引擎反编译包装脚本
- `fingerprint.ps1` / `fingerprint.sh`：包体指纹侦测脚本
- `find-api-calls.ps1` / `find-api-calls.sh`：网络接口扫描提取脚本
- `recover-kotlin-names.py` / `recover-kotlin-names.ps1` / `recover-kotlin-names.sh`：Kotlin 混淆元数据恢复工具
- `lookup-name.py` / `lookup-name.ps1` / `lookup-name.sh`：符号反查与搜索注解工具

### References
- [setup-guide.md](references/setup-guide.md)：Java 17、jadx、vineflower、dex2jar 安装指南
- [jadx-usage.md](references/jadx-usage.md)：jadx 命令行参数与实用技巧
- [fernflower-usage.md](references/fernflower-usage.md)：Fernflower / Vineflower 高级配置与对照分析
- [api-extraction-patterns.md](references/api-extraction-patterns.md)：各网络库搜索模式与提取规则
- [call-flow-analysis.md](references/call-flow-analysis.md)：业务调用链追踪技战法
- [kotlin-name-recovery.md](references/kotlin-name-recovery.md)：Kotlin R8 混淆恢复原理与限制
- [third_party_hosts.txt](references/third_party_hosts.txt)：常见第三方 SDK 域名黑名单（排除噪音）
