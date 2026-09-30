---
name: re-plugin-dev
description: >
  Ghidra/IDA 插件开发：脚本→插件工程化。
  触发词：插件开发、Ghidra插件、IDA插件、插件工程
capabilities: [plugin-development]
---

# Ghidra / IDA 插件开发

## 何时使用 / 何时不用

- 用：重复性分析步骤需要固化成可复用工具（批量标注、解密循环、自定义格式解析、特殊协议字段标注）
- 用：需要交互式 UI（菜单/快捷键/面板）或"工程加载即自动执行"的常驻功能
- 用：团队内分发/多机器统一分析环境（[[re-ghidra]] / [[re-ida]] 脚本升级为工程化插件）
- 不用：一次性分析任务（脚本即用即走，[[re-ghidra]] 步骤 4 / [[re-ida]] 步骤 4 的轻量脚本足够）
- 不用：只是把已有逻辑换个语言重写（先确认场景，见步骤 1）

## 工具准备

静态分析工具开发可免沙箱；插件跑在分析工具进程内，不执行样本代码（免沙箱，[[re-analyze/platform-tips]] 静态优先）。

### Ghidra —— Java 扩展 / Python 脚本

- Ghidra 安装（JDK 21+，Ghidra 11.3+ 要求）见 [[re-ghidra]] 工具准备
- GhidraDev Eclipse 插件（官方，GitHub `NationalSecurityAgency/ghidra` 仓库内 GhidraDev 目录）: 需要 Eclipse（Linux `apt install eclipse` / Fedora `dnf install eclipse-platform` / Arch `pacman -S eclipse-java`；macOS `brew install --cask eclipse-java`；Windows 官网 zip 解压）；非必需——纯 Gradle 也能构建扩展；GhidraDev 版本与 Eclipse 版本有配套表，装不上先在官方 release notes 核对组合
- Gradle（可选，构建 Java 扩展）: Debian/Ubuntu `apt install gradle` / Fedora `dnf install gradle` / Arch `pacman -S gradle`；macOS `brew install gradle`；Windows `choco install gradle`；验证 `gradle --version`；发行版仓库的 Gradle 可能过旧（构建 Ghidra 扩展失败）——优先用 GhidraDev 工程自带的 gradle wrapper（`./gradlew`）
- 验证: Ghidra GUI Script Manager 能列出脚本；`File > Install Extensions` 能看到安装的扩展

### IDA —— idapython 插件

- IDA 安装见 [[re-ida]] 工具准备（idapython 内置，无需单独安装）
- 插件目录: Windows `%APPDATA%\Hex-Rays\IDA Pro\plugins\`（或 IDA 安装目录 `plugins\`）；Linux/macOS `~/.idapro/plugins/`
- 验证: 插件文件放入目录后 IDA 启动日志出现 `Loading plugin ...`；`File > Script command` 执行 `print(idaapi.IDA_SDK_VERSION)` 输出 SDK 版本

## 操作步骤

按顺序执行；每个插件产物（源码/构建产物/测试样本与输出）存档 sha256 + 路径，供报告与复用（[[re-ioc]] 证据链要求）。

1. **场景识别（批处理脚本 vs 交互插件）**：
   - 一次性/简单重复 → 脚本（[[re-ghidra]] 的 GhidraScript / [[re-ida]] 的 idapython 脚本）
   - 常驻/需 UI/加载即执行/多机分发 → 插件（Ghidra Java Extension / IDA idapython 插件）
   - 判据四条，命中其一即该做插件: ① 需要交互 UI（菜单/快捷键/对话框）② 工程加载后自动执行 ③ 团队多机分发（版本统一）④ 需要与外部服务/API 集成
   - 记录决策: 场景 + 工具链 + 维护责任人（坑 4 的维护成本先摊开说）

2. **Ghidra 插件骨架（Java 扩展 / 程序脚本）**：
   - Python 脚本（最轻）: `@category` 头注释 + 存 GhidraScripts 目录，Script Manager 运行（注意内置 Jython 2.7，见坑 2 与 [[re-ghidra]] 坑）
   - Java 扩展（工程化）: GhidraDev `New > Ghidra Module Project` 选 Extension → 实现 `Plugin` 类（覆写 `init`/`dispose`，在 `init` 里注册菜单动作）→ Gradle `gradle buildExtension` 产出 .zip → 目标机器 `File > Install Extensions` 安装
   - 骨架要点: 动作注册用 `ToolAction`/`AbstractAction` 挂到菜单；无头环境用 `-postScript` 测试（[[re-ghidra]] 步骤 4）；脚本与扩展的边界见 [[re-ghidra]] 坑（脚本 vs 扩展选型）
   - 扩展结构: 构建产物 .zip 内含 extension.properties（声明适用的 Ghidra 版本范围）——装到范围外版本会被拒载，分发时注明版本并锁范围
   - 验证: 安装后在菜单触发动作；无头 `analyzeHeadless ... -postScript MyPluginTest.java` 跑通输出；`gradle buildExtension` 产出 zip 后先查 extension.properties 版本范围再分发

3. **IDA 插件骨架（idapython）**：
   ```python
   # myplugin.py —— 放到 plugins 目录，IDA 启动自动加载
   import idaapi
   class MyPlugin(idaapi.plugin_t):
       flags = idaapi.PLUGIN_KEEP
       comment = "demo plugin"
       help = ""
       wanted_name = "MyPlugin"
       wanted_hotkey = "Ctrl-Shift-M"
       def init(self):
           idaapi.register_action(idaapi.action_desc_t(
               "my:action", "My Action", MyAct(), "Ctrl-Shift-M"))
           return idaapi.PLUGIN_KEEP
       def run(self, arg):
           print("hello from MyPlugin")
   def PLUGIN_ENTRY():
       return MyPlugin()
   ```
   - 菜单注册: `idaapi.register_action` + `idaapi.attach_action_to_menu("Edit/...", "my:action")`；对话框: `ida_kernwin.ask_str` / `ask_buttons`（注意 IDA 9.x 中部分 API 迁到 `ida_kernwin`，见坑 1）
   - 无头测试: `idat64 -A -S"plugin_test.py" sample`（脚本内 `ida_auto` 等按 [[re-ida]] 步骤 4 写法）
   - 验证: 启动日志有 `Loading plugin ... MyPlugin`；快捷键触发动作输出正常

4. **与现有脚本复用（[[re-ghidra]] / [[re-ida]] 的脚本）**：
   - 起步素材: [[re-ghidra]] 步骤 4 的批量重命名/解密循环脚本、[[re-ida]] 步骤 4 的批量 patch/标注脚本——把"手动跑一遍"包成"菜单触发"
   - 场景示例: 自动扫描常量表（[[re-crypto-id]] 的 FindCrypt 思路）、花指令清除批处理（[[re-deobfuscate]] 的 D-810 思路）、PE/ELF 自定义格式解析（[[re-format-pe]] / [[re-format-elf]]）
   - 复用纪律: 脚本里的易变逻辑（模式串/表/阈值）外置为配置文件或插件选项，别硬编码进代码（降低坑 4 的维护成本）
   - 旧脚本先跑一遍验证基线输出，再包成插件——插件上线前后输出必须一致（回归测试）

5. **测试与分发**：
   - 测试矩阵: 多版本工具（IDA/Ghidra，见坑 1）、多架构样本（x86/x64/ARM）、有/无符号样本；修改型脚本先在副本 .i64/.idb 或独立工程上跑（[[re-ida]] 坑）
   - 只读验证先行: 先跑只读统计脚本确认预期，再上修改型逻辑（[[re-ida]] 坑: 修改型脚本直接在原库上跑改坏难回滚）
   - 分发: Ghidra 扩展 .zip（`gradle buildExtension`，README 注明 Ghidra 版本）；IDA 插件单 .py 文件或打包，注明 IDA 版本与 Python 版本；商业 IDA 的分发还要过插件签名（坑 3）
   - 验收: 干净环境（新工程/新 IDB）从零安装 → 触发 → 输出与开发环境一致，才算发布完成

## 跨域联合

- [[re-binary-core]]：本技能是其工具链扩展环节（网关工作流第 5 步反编译之后的可选工程化动作）
- [[re-ghidra]]：Ghidra 脚本/扩展开发起点（工作流步骤 4 的脚本即插件素材）
- [[re-ida]]：idapython 插件开发起点（工作流步骤 4 的脚本即插件素材；无头测试写法）
- [[re-deobfuscate]]：插件化脱混淆场景（D-810 思路）
- [[re-crypto-id]]：插件化常量表指纹扫描（FindCrypt 思路）
- [[re-format-pe]] / [[re-format-elf]] / [[re-format-macho]]：格式解析类插件的目标对象
- [[re-binaryninja]]：Binary Ninja 脚本 API 插件（多工具插件体系可互参考）
- 引用 [[re-analyze/platform-tips]] 静态优先原则（插件开发与测试免沙箱）

## 常见坑与陷阱

- **API 版本差异（Ghidra/IDA 升级破坏）**：现象——插件在旧版工具正常，升级后加载失败/运行报错/菜单消失；原因——Ghidra 11.x 有破坏性 API 变更（如函数管理类迁移）、IDA 9.x 把部分 `idc`/`idaapi` 函数重组织到新模块（`ida_bytes` 等）；对策——插件文档锁版本（写明测试过的 Ghidra/IDA 版本），测试矩阵覆盖新旧版本（步骤 5），升级工具后先跑只读脚本再改代码（[[re-ida]] 坑）
- **Java 环境要求**：现象——Ghidra 扩展构建或运行报 `UnsupportedClassVersionError`、Python 脚本语法错误；原因——JDK 版本不匹配（Ghidra 11.3+ 需 JDK 21，见 [[re-ghidra]]）、内置解释器是 Jython 2.7（Python 2 语法，不支持 f-string/海象运算，也无法 import pip 包）；对策——`java -version` 确认 21+ 且 `JAVA_HOME` 正确；脚本按 Python 2 兼容语法写，需要现代 Python 时用 ghidra-bridge 外接 Python 3（[[re-ghidra]] 坑）
- **插件签名（IDA 商业版）**：现象——插件放进 plugins 目录但商业版 IDA 不加载（启动日志无该插件，无任何报错）；原因——IDA 商业版对第三方插件做签名验证，未签名插件被拒；对策——确认 IDA 版本（Freeware 不做签名验证），开发期用 Freeware/无头模式测试，正式分发走 Hex-Rays 官方插件签名申请流程；把"签名状态"写进分发文档
- **维护成本失控**：现象——插件发布三个月后跟不上升级/新样本形态，没人修，反而拖慢分析；原因——插件是长期承诺（API 升级 + 场景变化都要跟进），一次性脚本没有这个成本；对策——步骤 1 先判值不值: 逻辑简单/变化快 → 脚本；稳定且复用高 → 插件；插件内把易变逻辑（模式串/表/阈值）外置配置，减少改码面；每次发布记录版本与对应工具版本
- **修改型插件直接改库，改坏不可逆**：现象——批量改名/patch 插件跑完，IDB 标注错乱且撤销困难；原因——跳过只读验证、没在副本上跑；对策——先跑只读统计脚本确认预期（[[re-ida]] 坑），修改逻辑先在副本 .i64/.idb 或独立 Ghidra 工程上验证，验收通过再上正式库
- **Ghidra 扩展版本范围拒载**：现象——扩展装进 Ghidra 无报错但列表里不出现；原因——extension.properties 声明的适用版本范围与当前 Ghidra 不匹配，被安装器拒载；对策——先解压 zip 核对 extension.properties 的版本范围（`ghidra.version` 字段），用 GhidraDev 生成工程时按目标版本建；分发文档写明测试过的 Ghidra 版本
- **无头/批处理环境不能依赖交互对话框**：现象——`analyzeHeadless` 或 `idat64 -A` 下插件行为异常/卡住；原因——批处理模式没有 UI 事件循环，ask_* 对话框类 API 与菜单触发逻辑不可用；对策——交互参数（路径/阈值/模式串）改从命令行参数或配置文件读取，插件内先判断运行环境（是否 GUI 会话）再决定走哪条分支；无头测试脚本只验证纯计算逻辑
