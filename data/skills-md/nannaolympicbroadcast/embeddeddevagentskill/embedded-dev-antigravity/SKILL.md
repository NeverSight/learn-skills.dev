---
name: embedded-dev-antigravity
description: >
  嵌入式开发 Agent Skill，专为 Google Antigravity IDE 设计。当用户提到嵌入式开发、单片机、开发板、MCU、RTOS、固件烧录、串口调试、SSH 连接设备、ESP32、STM32、Raspberry Pi、Arduino、Zephyr、FreeRTOS、U-Boot、Linux 内核、设备树、交叉编译等相关话题时，必须立即触发本 Skill。也适用于：读取设备日志、烧录固件、调试硬件问题、配置 toolchain、移植代码到目标板等场景。即使用户只是问"我的板子怎么连串口"或"编译报错了"，只要涉及嵌入式硬件，也应触发本 Skill。
compatibility: "requires: python, fastmcp 3+ (pip install \"fastmcp>=3.0.0\"); tools: web_search, shell"
---

# 🔌 嵌入式开发 Agent Skill — Antigravity IDE

所有终端交互通过 **fastmcp CLI** 完成，直接指向 Electerm MCP Server，
MCP Server 地址：`http://127.0.0.1:30837/mcp`

---

## Step 0 — 建立硬件与目标系统上下文（每次对话首先执行）

**每次对话开始时必须确认以下信息，存入记忆，作为一切操作的前提：**

```
开发板型号    ：___（例：STM32F407, ESP32-S3, Raspberry Pi 4）
主控芯片架构  ：___（例：ARM Cortex-M4, Xtensa LX7, RISC-V）
目标系统/固件 ：___（例：FreeRTOS, Zephyr, Bare-metal, Linux, U-Boot）
工具链        ：___（例：arm-none-eabi-gcc, xtensa-esp32s3-elf-gcc）
连接方式      ：___（串口 / SSH / JTAG / SWD）
串口路径      ：___（例：/dev/ttyUSB0, COM3）
```

未确认前不得给出具体命令。确认后每次回复顶部显示：
`[📋 当前目标：<开发板> / <系统>]`

---

## Step 1 — fastmcp 安装与 Electerm 连接

### 1.1 安装 fastmcp

```powershell
# 通过 pip 安装（推荐，跨平台），注意需要 3.0 或以上版本
pip install "fastmcp>=3.0.0"

# 或通过 uv 安装
uv tool install "fastmcp>=3.0.0"
```

安装后验证：
```powershell
fastmcp version
```

### 1.2 检查 Electerm MCP Server 连通性

```powershell
# 列出 electerm server 的所有可用工具
fastmcp list http://127.0.0.1:30837/mcp
```

若输出工具列表，则连接成功。若报错，执行下方安装引导。

### 1.3 Electerm 未就绪时的引导步骤

**① 下载 Electerm** → https://electerm.html5beta.com/（Win / macOS / Linux）

**② 开启 MCP Server**
1. 打开 Electerm → 左侧 **⚙️ 齿轮**
2. **Widgets** → **MCP Server**
3. **☑ 勾选全部选项** → 点击 **[Start Widgets]**
4. 记录 Widgets 面板中显示的实际端口号

若端口不是 `30837`，将后续命令中的端口号替换为实际端口：
```
http://127.0.0.1:<实际端口>/mcp
```

📖 https://github.com/electerm/electerm/wiki/MCP-Widget-Usage-Guide

---

## Step 2 — fastmcp 命令参考

所有命令均直接指向 MCP Server URL：`http://127.0.0.1:30837/mcp`

```powershell
# 查看 electerm server 所有工具及描述
fastmcp list http://127.0.0.1:30837/mcp

# 查看所有工具的详细参数 schema
fastmcp list http://127.0.0.1:30837/mcp --input-schema

# 搜索工具（Windows 用 findstr，Linux/macOS 用 grep）
fastmcp list http://127.0.0.1:30837/mcp | findstr "session"
fastmcp list http://127.0.0.1:30837/mcp | findstr "terminal"
fastmcp list http://127.0.0.1:30837/mcp | findstr "exec"

# 调用工具（key=value 参数形式）
fastmcp call http://127.0.0.1:30837/mcp <tool_name> key=value

# 调用工具（JSON 参数形式，适合复杂参数）
fastmcp call http://127.0.0.1:30837/mcp <tool_name> '{"key": "value"}'

# 调用无参数工具
fastmcp call http://127.0.0.1:30837/mcp <tool_name>
```

### 标准工作流

```powershell
# 1. 发现工具
fastmcp list http://127.0.0.1:30837/mcp

# 2. 查看目标工具的参数 schema
fastmcp list http://127.0.0.1:30837/mcp --input-schema | findstr -A 10 "<tool_name>"

# 3. 调用
fastmcp call http://127.0.0.1:30837/mcp <tool_name> param=value
```

---

## Step 3 — 每次回答必须搜索并引用官方文档

每个技术回答都必须通过 `web_search` 搜索，结尾附参考链接。

搜索 Query 模板：
```
site:docs.espressif.com <关键词>
site:docs.zephyrproject.org <关键词>
"<开发板型号>" <问题> site:github.com
<芯片型号> <错误信息>
```

每次回答末尾附：
```
📚 参考资料：
- [标题](URL) — 来源
```

---

## Step 4 — 初始化开发板：串口连接引导

当用户首次连接开发板时：

**① 搜索目标板串口文档**
```
<开发板型号> serial console UART setup
<开发板型号> TX RX UART pins pinout
```

**② 硬件连接检查清单**
```
□ USB-TTL 转换器（CH340 / CP2102 / FTDI）已插入 PC
□ TX-RX 交叉：板子 TX → 转换器 RX；板子 RX → 转换器 TX
□ GND 共地
□ 波特率确认（常见：115200 / 921600 / 9600）

查看串口设备：
  Linux/macOS：ls /dev/ttyUSB* /dev/ttyACM* /dev/cu.*
  Windows：设备管理器 > 端口(COM和LPT)
```

**③ Electerm 建立串口会话**
1. Electerm **+** → **Serial** → 填入路径和波特率 → 连接
2. `fastmcp list http://127.0.0.1:30837/mcp | findstr "session"` 找到列举会话的工具
3. `fastmcp call http://127.0.0.1:30837/mcp <list_tool>` 获取 session_id

---

## Step 5 — 在目标设备执行命令

```powershell
# 先发现工具
fastmcp list http://127.0.0.1:30837/mcp

# 找执行命令类工具
fastmcp list http://127.0.0.1:30837/mcp | findstr "exec"
fastmcp list http://127.0.0.1:30837/mcp | findstr "command"

# 查看工具参数
fastmcp list http://127.0.0.1:30837/mcp --input-schema

# 执行（key=value 简洁写法）
fastmcp call http://127.0.0.1:30837/mcp <exec_tool> sessionId=<session_id> command="uname -a"

# 执行（JSON 写法，适合含特殊字符或复杂命令）
fastmcp call http://127.0.0.1:30837/mcp <exec_tool> '{"sessionId": "<session_id>", "command": "dmesg | grep -i error | tail -20"}'
```

### 常用嵌入式调试命令

```bash
# Embedded Linux
dmesg -w                           # 实时内核日志
cat /proc/cpuinfo | head -20       # CPU 信息
free -h && df -h                   # 内存/磁盘
i2cdetect -y 1                     # I2C 设备扫描
cat /sys/class/thermal/*/temp      # 温度传感器

# Zephyr Shell（串口直连）
kernel threads   # 任务列表
kernel stacks    # 栈使用情况
device list      # 已注册驱动列表

# ESP-IDF
idf.py -p /dev/ttyUSB0 flash monitor

# STM32 / OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
  -c "program build/app.elf verify reset exit"
```

---

## Step 6 — 网络配置与文件传输 (SFTP)

当用户需要**向开发板同步或传输文件**时，首选通过网络（如 SFTP）进行高速传输。
请遵循以下引导流程：

**① 提醒用户建立网络连接环境**
告知用户需要将开发板与电脑连接至同一局域网，有两种推荐方式：
- 打开电脑的“移动热点”，准备让开发板连接电脑热点；
- 或将开发板和电脑同时连接到同一个家庭/办公路由器 Wi-Fi。

**② 获取凭据并操作开发板连网**
主动向用户询问要连接的 Wi-Fi 名称（SSID）和密码。
获取信息后，Agent 应主动利用现有的串口会话（参考 Step 5），在目标系统终端执行联网命令（如 Linux 系统通过 `nmcli dev wifi connect <SSID> password <PWD>`，或 Zephyr/ESP32 等环境的 wifi 指令）让开发板连上该 Wi-Fi。

**③ 验证网络与 SFTP 传输**
连接成功后，在串口执行 `ifconfig` 或 `ip a` 命令获取开发板分配到的局域网 IP 地址。
拿到 IP 后，即可使用 SFTP 或 scp 进行文件传输。

---

## Step 7 — 决策树

```
用户输入
  ├─ "连串口" / "初始化开发板"      → [Step 4] 串口引导 + web_search
  ├─ "执行命令" / "查日志" / "调试" → [Step 2] list 发现工具 → call 执行
  ├─ "编译报错" / "配置 toolchain"  → [Step 3] web_search → 方案 → MCP 验证
  ├─ "烧固件" / "flash"             → 搜索文档 → 生成命令 → 用户确认 → call 执行
  ├─ "传文件" / "同步代码"          → [Step 6] 提示连局域网/开热点 → 询问WiFi账密 → call 串口连WiFi → SFTP
  └─ 对话开始（无硬件上下文）        → [Step 0] 确认开发板 + 目标系统
```

---

## 约束

- 未确认开发板型号前不给出具体命令
- `flash erase` / `rm -rf` / `dd` 等破坏性操作前必须用户明确确认
- 每次技术回答必须附官方文档链接
- 工具名通过 `fastmcp list` 动态发现，不硬编码

## 附录

详细平台速查（工具链、串口引脚、文档链接）见 `references/platforms.md`
