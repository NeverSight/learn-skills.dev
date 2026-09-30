---
name: re-javacard
description: >
  Java Card / SIM 卡 applet 逆向：CAP 文件组件解析（规范 12 组件）、CAP 字节码（Java 子集）还原、AID 与安装参数、process(APDU) 分派。
  触发词：Java Card、javacard、CAP 文件、SIM 卡、USIM、applet、AID、银行卡、JCVM。
capabilities: [bytecode-parser]
---

# Java Card / SIM 卡 applet 逆向（CAP 组件解析与字节码还原）

## 何时使用 / 何时不用

- 用：拿到 Java Card applet 的 CAP 文件（Converted Applet Package，.cap）——来自 EEPROM dump、固件镜像、资料包或读卡提取
- 用：SIM / USIM / 银行卡等智能卡应用分析——包 AID 与 applet AID、安装参数、install() 初始化、process(APDU) 分派逻辑还原
- 用：CAP 字节码（Java 子集 + 卡片扩展指令）反汇编、方法体还原、CLA/INS 指令表重建
- 不用：APDU 协议交互与抓包、ISO14443 链路、MIFARE/DESFire 卡族弱点（走 [[re-iot-proto]]）
- 不用：通用 .class/.jar Java 字节码逆向（走 [[re-java]]）；CAP 内嵌原始 .class 可配合 javap 对照，但不替代本技能
- 不用：CAP 尚未取到手——先走读卡器物理交互（[[re-hardware-io]] / [[re-iot-proto]] APDU）或固件提取（[[re-firmware]] / [[re-fw-extract]]），拿到文件再回来
- 不用：只需读/写卡片数据或抓 APDU 流量（[[re-iot-proto]]）

## 工具准备

所有工具先验证再使用。静态解析可免沙箱；涉及真实卡片与读卡器交互先确认授权边界（卡片归属与分析目的），动态执行默认沙箱（[[re-analyze/platform-tips]] 最高原则）。

### CAP 文件解析（开源解析器或自写脚本）

- **capfile**（Java 库，martinpaljak，CAP 解析/验证，ant-javacard 生态）：`git clone https://github.com/martinpaljak/ant-javacard`（capfile 已并入其中）；作为库引用构建。验证：解析样例 CAP 无异常
- **caprunner**（Python，CAP 解析 + 字节码执行器，benallard）：`git clone https://github.com/benallard/caprunner` + `git clone https://github.com/benallard/pythoncard`（pythoncard/pythoncardx 目录放入 caprunner 同级路径）；验证：`python3 readcap.py <file.cap>` 能列出组件信息
- **pysim 的 javacard.py**（osmocom，生产级 SIM 工具链组件）：`git clone https://github.com/osmocom/pysim`；`pySim/javacard.py` 的 CapFile 类——校验 Header 魔数 0xDECAFFED、读包 AID/applet AID、拼安装顺序 load file；验证：`python3 -c "import sys; sys.path.insert(0,'pysim'); from pySim.javacard import CapFile; print(CapFile('x.cap').get_loadfile_aid())"`
- **GlobalPlatformPro**（gp，Java，与卡交互/装应用/列应用 AID）：GitHub releases 下载 JAR（Java 11+）：`java -jar gp.jar --version`；`java -jar gp.jar --list`（列卡上应用与 AID）
- 自写解析器要点：CAP 是 ZIP，组件以文件形式存放，逐文件按「tag + size + info」解析即可，不依赖单一偏移表（结构见操作步骤 2-5）

### javap —— 原始 .class 对照（JDK 自带）

- Linux: `apt install default-jdk` / `dnf install java-17-openjdk` / `pacman -S jdk-openjdk`；macOS: `brew install openjdk`；Windows: 官方 JDK 安装包
- 验证: `javap -version`
- 用途：CAP JAR 内常带编译期等价产物 `APPLET-INF/classes/**/*.class`（SDK 转换器打包，`unzip -l` 可见），`unzip -p x.cap APPLET-INF/classes/com/example/Foo.class > Foo.class && javap -c -p Foo.class` 拿到 Java 视图，与 CAP 字节码互相对照（注意操作码编号与指令名差异，见坑 3）

### 仿真执行（无卡验证，可选）

- **JCardSim**（Java 仿真器，加载编译后的类而非 CAP 字节码）：GitHub releases 下载 JAR；配 vsmartcard 虚拟读卡器后作为 PC/SC 读卡器暴露，供 pyscard 发 APDU 验证行为
  - Linux: `git clone https://github.com/frankmorgner/vsmartcard`，编译 virtualsmartcard 后 `systemctl restart pcscd`；Windows: BixVReader 类虚拟读卡器
- **pyscard**（Python PC/SC 交互）：`pip install pyscard`（Linux 依赖 `apt install libpcsclite-dev pcsclite pcscd` / `dnf install pcsc-lite-devel pcsc-lite` / `pacman -S pcsclite ccid`；macOS: `brew install pcsc-lite`）；验证：`python3 -c "from smartcard.System import readers; print(readers())"`
- CAP 字节码直接执行用 caprunner 的 runcap.py（无需硬件）

### 反编译器与读卡器（泛化）

- **Ghidra / IDA 无原生 CAP 加载器与处理器模块**——CAP 字节码需脚本化解析：Ghidra Python / IDA Python 按本技能组件结构导入，或先用解析器导出反汇编再人工对照
- **读卡器（泛化选购）**：接触式 ISO7816（PC/SC CCID 免驱类）与无接触 ISO14443（NFC）两类；选购关注：PC/SC 驱动完备性（CCID 免驱 vs 厂商私有驱动）、SIM 卡座形式与适配器（全尺寸 / micro-SIM 等）、T=0/T=1 协议支持、供电稳定性
- **授权边界**：读卡、提取、写卡均需确认卡归属与分析目的授权；对第三方卡做只读接触也视为需授权场景（[[re-analyze/platform-tips]] 最高原则）

## 操作步骤

按顺序执行，每步产物（解析脚本、反汇编文本、AID/INS 清单）与样本 sha256 存档；动态执行默认沙箱。

1. **CAP 来源与文件识别**：
   - 来源：EEPROM dump（[[re-hardware-io]] flash 读取）、固件镜像提取（[[re-firmware]] / [[re-fw-extract]]）、资料包/测试样本、授权内读卡提取
   - 识别：`file x.cap`（ZIP 归档）→ `unzip -l x.cap`——存在 `META-INF/MANIFEST.MF` + `<包路径>/javacard/*.cap` 组件文件即为 CAP；含 APPLET-INF/classes 说明带原始类文件（步骤 4 可对照 javap）；不含 javacard/ 组件文件则可能是后缀错误、加密负载或其他格式（见坑 4）
   - `sha256sum x.cap` 归档；记下 Header 中的格式版本

2. **组件枚举与 Header 校验**：
   - 组件清单（Java Card 规范，tag 1-12；核心必备 + 可选）：

     | tag | 组件 | 内容与作用 |
     |-----|------|-----------|
     | 1 | Header | 魔数、格式版本、flags、包 AID、包名 |
     | 2 | Directory | 各组件大小表（缺失可选组件记 0）、静态字段尺寸、import/applet 计数 |
     | 3 | Applet（可选） | applet 数、各 applet AID + install() 方法偏移 |
     | 4 | Import | 外部包 AID 列表（供常量池外部引用定位） |
     | 5 | ConstantPool | token → 类/字段/方法引用（6 类条目，每条 4 字节） |
     | 6 | Class | 类/接口定义：标志位、父类引用、虚方法表、实现接口 |
     | 7 | Method | 方法体：异常处理器表 + 方法头（max_stack/nargs/max_locals）+ CAP 字节码 |
     | 8 | StaticField | 静态字段镜像区与数组初始化数据 |
     | 9 | ReferenceLocation | 字节码中常量池 token 操作数的位置列表（安装时打补丁用） |
     | 10 | Export（可选） | 对外可见的类/方法/字段符号（跨包链接用） |
     | 11 | Descriptor | 签名池：方法名、描述符、method_offset 与 bytecode_count |
     | 12 | Debug（可选） | 调试信息字符串表（含方法名），离线验证/还原用 |

   - 网上流传的「九组件」列举（Header/Directory/Import/ConstantPool/Class/Method/Descriptor/Export/Applet）是简化说法，遗漏了字节码链接必需的 StaticField 与 ReferenceLocation——解析以本表为准
   - Header 字节布局：`01 | size(u2) | magic=0xDECAFFED | fmt_minor | fmt_major | flags | pkg_minor | pkg_major | aid_len | 包AID | [包名]`；flags: 0x01=ACC_INT、0x02=ACC_EXPORT、0x04=ACC_APPLET；魔数不是 0xDECAFFED 即非合法 CAP（或已被加密/截断，见坑 4）

3. **Directory 驱动组件一致性校验**：
   - Directory 组件：按 tag 顺序的组件大小 u2 数组（Header/Directory/Applet/Import/ConstantPool/Class/Method/StaticField/ReferenceLocation/Export/Descriptor/Debug）+ 静态字段 image_size/array_init + import_count + applet_count
   - 与 JAR 内组件文件逐项核对：存在性、tag 顺序、size 字段一致；可选组件（Applet/Export/Descriptor/Debug）缺失时目录记 0
   - 可拼出安装顺序 load file（Header→Directory→Import→Applet→Class→Method→StaticField→Export→ConstantPool→RefLocation→Descriptor），与固件/读卡器中的安装序列对照（联动 [[re-iot-proto]] 实测）

4. **Method 组件方法体还原**：
   - Method 组件布局：`07 | size(u2) | handler_count(u1) | 异常处理器表（每条 8 字节：start_offset u2、active_length 位域 u2、handler_offset u2、catch_type_index u2）| 方法体序列（方法头 + 字节码）`
   - 方法头：2 字节（首字节高 4 位 flags——0x8=ACC_EXTENDED、0x4=ACC_ABSTRACT，低 4 位 max_stack；次字节高 4 位 nargs、低 4 位 max_locals）或扩展 4 字节；方法在组件内的偏移与字节码长度由 Descriptor 组件给出（method_offset + bytecode_count）
   - applet 的 install() 入口偏移在 Applet 组件（install_method_offset）
   - 反汇编按 CAP 指令集（见坑 3 的操作码表）：操作数多为 2 字节常量池 token，方法以 return 系/athrow 结尾
   - 有 Debug 组件时用其字符串表直接还原方法名；否则方法名靠 Descriptor 签名池 + 调用点语义推断（框架方法对照 SDK export 文件）

5. **Import / 常量池 / Export 跨组件引用解析**：
   - ConstantPool 条目（每条 4 字节：tag u1 + 引用 3 字节）：1=classref、2=instance fieldref、3=virtual methodref、4=super methodref、5=static fieldref、6=static methodref；引用首字节高位 0x80 区分内部（类内偏移/token）与外部（package_token + class_token + token）
   - 调用指令与条目类型对应：invokevirtual → tag 3（虚方法），invokespecial 调超类方法 → tag 4（super methodref），invokespecial/invokestatic 调构造器与私有方法 → tag 6（静态方法）
   - Import 组件：外部包 AID 列表，顺序即常量池外部引用的 package_token 编号
   - 字节码中 token 操作数的位置由 ReferenceLocation 组件标注（增量偏移表）；解析脚本据此定位引用点并替换为常量池条目
   - 外部符号名解析：本包导出看 Export 组件；框架包（javacard.framework）按 SDK 的 .exp 导出文件对照——javacard.framework 是 SIM/银行卡 applet 几乎必引的包，其常量（OFFSET_CLA=0、OFFSET_INS=1、OFFSET_P1=2、OFFSET_P2=3、OFFSET_LC=4；SW1/SW2，0x9000=成功）是还原分派逻辑的锚点

6. **Applet 入口与 process(APDU) 分派还原**：
   - 生命周期：install(APDU)（Applet 组件 install_method_offset 定位）→ register() → 应用选中后每次 APDU 调 process(APDU)；定位 process：Descriptor 方法表找 process 描述符，或从 install 调用链进入
   - 分派还原：典型形态——invokevirtual APDU.getBuffer()（外部 classref 虚方法调用）→ baload + sconst_*/bipush/sspush 取 CLA/INS → icmp/if_* 比较链或 switch 系指令（itableswitch/slookupswitch 等）分支表 → 每 INS 一个处理分支 → ISOException.throwIt(SW1SW2) 异常路径
   - 产出 INS → 处理逻辑映射表：各分支入口、P1/P2/Lc/数据解析、返回 SW；与 [[re-iot-proto]] 的 APDU 抓包/实测对照，双向验证分派表
   - 安装参数：install 方法读取安装 APDU 数据（初始化参数/持卡人数据），写入静态字段或文件系统，影响后续行为分支——从 install 开始跟参数写入点，别只看 process（见坑 6）

## 跨域联合

- [[re-iot-proto]]：APDU 协议交互/抓包/卡族判型——本技能还原的 CLA/INS 分派表与其实测 APDU 行为互相验证
- [[re-firmware]] / [[re-fw-extract]]：CAP 从固件镜像/OTA 包提取
- [[re-hardware-io]]：EEPROM/flash dump 获取、JTAG 调试、读卡器物理访问
- [[re-java]]：通用 JVM 字节码逆向底座（CAP 内嵌 .class 的 javap 对照）
- [[re-crypto-id]] / [[re-crypto-keys]] / [[re-crypto-decrypt]]：applet 内加密算法识别、密钥提取与数据解密（智能卡应用常见）
- [[re-variant]]：同 applet 多版本 CAP 对比定位差异（升级/补丁分析）
- [[re-patching]]：改动 CAP 字节码后重打包重装（需对应安装/签名授权）
- [[re-sandbox]]：一切动态执行/读卡交互强制前置（[[re-analyze/platform-tips]] 最高原则）
- [[re-triage]]：初勘前置（文件类型/熵/哈希/架构识别）

## 常见坑与陷阱

- **组件结构用错（把「九组件」当规范）**：现象——按流传的九组件列举解析，缺 StaticField/ReferenceLocation，字节码引用解不出、静态字段错位；原因——简化列举遗漏了与字节码链接直接相关的两个组件；对策——以规范 12 组件表为准（见操作步骤 2），用 Directory 大小表 + 各组件文件自身 tag/size 双重校验边界
- **JAR 结构与拼接格式混淆**：现象——按单一偏移表从文件头连续切组件，全部错位；原因——CAP 是 ZIP（组件分文件存储，还可能带 META-INF、APPLET-INF/classes 等文件）；旧格式（2.2 之前）或非标准转换产物才是组件拼接式；对策——先 `unzip -l` 确认结构，组件边界以各组件文件自身的 tag+size 为准
- **CAP 字节码当 JVM 字节码反汇编**：现象——操作码表对不上、指令长度错位，反汇编全乱；原因——CAP 指令集是独立编号：return=0x7A（JVM 0xB1）、new=0x8F（0xBB）、invokevirtual/invokespecial/invokestatic/invokeinterface=0x8B-0x8E（JVM 0xB6-0xB9，且操作数为 2 字节常量池 token 而非符号引用）、aload_0=0x18；另有 JVM 没有的类型化变体（getfield/putfield 的 *_a/*_b/*_s/*_i 及 *_this/*_w、sadd/ssub/smul 等 short 专用指令、icmp/if_scmp*、iipush/sspush 常量装载）；无 ldc 系（常量走 sconst_*/bipush/sspush/iipush + 常量池 token）、无 multianewarray（仅一维数组）、无 monitorenter/monitorexit（单线程）、无 invokedynamic、无 long/double 运算指令（Classic 2.2.2；3.0.5 起语言子集支持 long）；「无 invokevirtual」是误传——四类调用指令齐备，框架类实例方法（如 APDU.getBuffer）就走 invokevirtual；对策——用 CAP 专用反汇编（caprunner 指令表/自写脚本按上表），与 javap 对照原 .class 时注意同名指令编号不同
- **Import 外部引用断链**：现象——调用点 token 解不出目标方法名，逻辑断在框架调用处；原因——applet 的依赖在外部包（框架包/其他 CAP），本 CAP 只含引用 token；对策——Import 组件列外部包 AID，外部符号经 Export 组件或 SDK .exp 文件解析；javacard.framework 的方法名与常量按 SDK 导出文件对照
- **卡片 dump 是密文或片段**：现象——「CAP」魔数不对或组件解不开，内容熵高；原因——dump 被卡 OS 加密（GlobalPlatform 域密钥/安全消息封装），或截断/跨区提取不完整；对策——先用熵与魔数判断明文/加密负载，加密走 [[re-crypto-id]] / [[re-crypto-keys]] 思路；用 Directory 大小表核对组件完整性，从固件提取时同样核对
- **只还原 process 忽略 install 与 AID**：现象——分派表还原了但行为对不上，或同包多应用互相混淆；原因——install() 的安装参数（初始化数据/持卡人数据）写入静态字段或文件系统，影响后续分支；Applet 组件可含多个 applet AID（同包多实例）；对策——从 install 开始跟踪参数写入点，按 AID 区分实例；AID 格式：5 字节 RID + 0-11 字节 PIX（总长 5-16，ISO/IEC 7816-5；0xA0 开头为国际注册 RID，如 SIM/USIM 应用通用 RID A000000087，PIX 为应用自定义）
- **读卡/写卡授权越界**：现象——对真实卡片读写分析未确认归属与目的；对策——第三方卡接触默认需授权，优先实验室样本与文档资料（[[re-analyze/platform-tips]] 最高原则）
