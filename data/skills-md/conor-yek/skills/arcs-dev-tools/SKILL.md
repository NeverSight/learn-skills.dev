---
name: arcs-dev-tools
description: 当用户提到 ARCS/arcs-sdk、交叉编译工具链（riscv64-unknown-elf-gcc）、cskburn、烧录、/dev/ttyACM*、串口日志等任务时使用：负责拉取仓库、环境安装、编译、烧录、运行与日志读取；不负责代码编写/理解，代码开发由 Claude Code 本身负责
license: MIT
---

# ARCS SDK 工具链

为 Claude Code 提供与 ARCS 硬件交互的工具链能力：拉取仓库、安装开发环境、编译、烧录、运行、日志读取。

**本 skill 只负责工具链操作，不负责代码编写和理解。** 代码开发、需求理解、bug 分析由 Claude Code 本身完成。

## 当前状态

本 skill 仍处于**开发阶段**。欢迎在使用过程中反馈：

- 复现稳定的 bug（最好附上命令输出/日志片段）
- 环境兼容性问题（发行版、Python 版本、串口设备类型等）
- 更好的"触发语句/使用示例"（请提交到仓库的 `docs/` 文档中，避免放进 skill 包内）

## 已验证能力（已跑通）

- **运行某个 sample**：模型自行定位示例 → 编译 → 烧录 → 读取日志 → 判定成功/失败
- **UI 显示并迭代**：模型先写一个在 UI 上显示一行字的示例 → 烧录运行 → 再修改文字内容 → 重新烧录并确认生效

## 使用示例

示例与触发语句见 `<skill_dir>/references/usage.md`（按需加载，避免主文件过长）。

### 批量模式

- 逐个串行执行 编译→烧录→验证（串口设备同一时间只能一个操作使用）
- 每个示例独立输出验证结果，最后汇总
- 某个失败不影响后续继续

## 默认配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| BOARD | `arcs_evb` | 目标开发板 |
| 串口设备 | 动态扫描 | 每次操作前扫描 `/dev/ttyACM*` `/dev/ttyUSB*` |
| 烧录波特率 | `3000000` | cskburn 波特率 |
| 串口波特率 | `921600` | 日志读取波特率 |
| 烧录起始地址 | `0x0` | Flash 烧录偏移 |
| 仓库地址 | `https://gitlab.example.com/listenai/arcs-sdk.git` | git clone 地址（需用户提供实际地址） |

## 核心原则：先确认非偶发，再处理

遇到异常现象时，**必须重复验证 2-3 次确认是否稳定复现**，再决定是否处理。
- 每次都复现 → 真实问题，返回给 Claude Code 处理
- 仅偶发 → 标记为环境因素，不作为代码问题

## 工具链操作

### 操作 1：拉取仓库

当用户的环境中还没有 arcs-sdk 仓库时执行。

```bash
# 克隆仓库（用户需提供实际的仓库地址）
git clone <仓库地址> arcs-sdk
cd arcs-sdk
git submodule update --init --recursive
```

- 如果用户未提供仓库地址，询问用户
- 如果仓库已存在，跳过此步骤，直接使用现有仓库
- 支持切换分支：`git checkout <branch>`

### 操作 2：安装开发环境

首次使用或工具链缺失时执行。需要运行**两个**安装脚本：

```bash
# 1. 安装构建工具（cmake、ninja 等）
bash prepare_listenai_tools.sh

# 2. 安装 GCC 交叉编译工具链（riscv64-unknown-elf-gcc）
bash prepare_toolchain.sh

# 3. 确保 cskburn 有执行权限
chmod +x ./tools/burn/cskburn
```

**检查项**：
- `listenai-dev-tools/` 目录是否存在
- `listenai-dev-tools/gcc/bin/riscv64-unknown-elf-gcc` 是否可执行
- `listenai-dev-tools/listenai-tools/cmake/bin/cmake` 是否可执行
- `./tools/burn/cskburn` 是否可执行

如果检查通过，跳过安装。

### 操作 3：编译

**输入**：项目路径（示例目录或用户自建项目目录）
**输出**：`build/arcs.bin` 固件文件，或编译错误信息

```bash
cd <项目目录>
bash ./build.sh -C -DBOARD=arcs_evb && bash ./build.sh -r -w -DBOARD=arcs_evb
```

**build.sh 查找策略**：
- 项目目录下有 `build.sh` → 直接用
- 没有 → 用仓库根目录的 `build.sh -S <项目相对路径>`

**编译失败时**：
- 将完整错误输出返回给 Claude Code，由 Claude Code 分析并修改代码
- 查阅 `<skill_dir>/references/knowledge.md` 对应 topic 看是否有已知解决方案
- Claude Code 修改代码后，再次调用本操作重新编译

**确认编译产物**：
- 在 `build/` 下查找 `.bin` 文件
- 返回固件文件的完整路径和大小

### 操作 4：烧录

**输入**：固件文件路径
**输出**：烧录成功/失败

**烧录前**：
```bash
# 动态扫描串口设备
ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null
# 确认无进程占用
fuser <串口设备> 2>/dev/null
```

**执行**：
```bash
# 必须使用仓库自带的 cskburn，必须带 -C arcs 参数
./tools/burn/cskburn -C arcs -s <串口设备> -b 3000000 0x0 <固件文件路径>
```

> **重要**：必须使用 `./tools/burn/cskburn`（仓库根目录下），**不要**使用 `listenai-dev-tools/listenai-tools/cskburn/cskburn`。
> 后者是通用版本，不支持 `-C arcs` 参数，缺少烧录前自动擦除步骤，会导致写入失败。

**正常烧录输出示例**：
```
Waiting for device...
Entering update mode...
Detected flash size: 16 MB
Erasing region 0x00000000-0x00021000...
Burning partition 1/1... (0x00000000, 130.88 KB)
130.88 KB / 130.88 KB (100.00%)
Resetting...
Finished
```

**失败处理**：
- `Failed opening device` → 板子未进入烧录模式，提示用户按 BOOT+RESET 进入烧录模式
- `EBUSY` → `fuser` 找到占用进程，提示用户释放
- `ETIMEDOUT` → 等 3 秒，重新扫描设备号，重试
- 设备消失 → 等待后重新扫描 `/dev/ttyACM*`
- `Failed burning partition: 01` → 检查是否误用了 `listenai-dev-tools` 中的 cskburn，换用 `./tools/burn/cskburn`

### 操作 5：运行（日志读取）

**输入**：无（烧录完成后自动执行）或独立调用
**输出**：串口日志文本

**使用 `serial_read.py`**（技能自带脚本，纯 Python stdlib，零外部依赖）：
```bash
python3 <skill_dir>/serial_read.py <串口设备> -b 921600 -t <读取秒数>
```

> **`<skill_dir>`** 即本技能安装目录，与 SKILL.md 同级。

**参数说明**：
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-b, --baudrate` | `921600` | 波特率 |
| `-t, --timeout` | `5` | 读取超时（秒） |
| `--dtr` | 不传（拉低） | 传入则拉高 DTR |
| `--rts` | 不传（拉低） | 传入则拉高 RTS |

**特性**：
- 非 TTY 环境兼容（`O_NOCTTY` + `select()` 非阻塞读取）
- 默认拉低 DTR 和 RTS（通过 `ioctl TIOCMBIC`）
- 打开后自动 flush 缓冲区，避免读到残留数据
- 实时输出到 stdout

**串口问题处理**：
- **乱码** → 确保波特率设置正确（921600），或等板子完全启动后再读
- **设备断连** → 关闭连接 → 等 2-3 秒 → 重新扫描设备 → 重连
- **无输出** → 提醒用户按 Reset 键，或重新烧录
- **权限问题** → 确保用户在 uucp/dialout 组中
- **设备占用** → 读取前检查是否有其他进程占用（fuser <串口设备>）

**日志返回给 Claude Code**，由 Claude Code 判断程序是否正常运行。

### 操作 6：检查硬件连接

独立操作，可在任意时刻调用。

```bash
ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null
```

- 找到唯一设备 → 返回设备路径
- 找到多个 → `udevadm info` 识别后询问用户
- 找不到 → `lsusb` + `dmesg | tail -20` 后告知用户

## 常用流水线

### 流水线 A：运行现有示例

Claude Code 调用顺序：
1. 检查硬件连接
2. 定位示例目录，阅读 README 和源码（Claude Code 自己做）
3. **编译**（操作 3）
4. **烧录**（操作 4）
5. **日志读取**（操作 5）
6. Claude Code 对比日志和预期输出，判断结果

### 流水线 B：编写新代码并验证

Claude Code 调用顺序：
1. 检查硬件连接
2. Claude Code 参考仓库中的示例和 API，编写代码
3. **编译**（操作 3）→ 失败则 Claude Code 改代码 → 重新编译（循环）
4. **烧录**（操作 4）
5. **日志读取**（操作 5）
6. Claude Code 判断是否符合预期 → 不符合则改代码 → 回到步骤 3（循环）

## 经验知识库

文件：`<skill_dir>/references/knowledge.md`

按 5 个 topic 组织：**仓库管理 / 环境安装 / 编译 / 烧录 / 串口**。遇到问题时只读对应 topic。

> 本文件由维护者手动维护，**模型不要修改**。

### 自优化 SKILL.md

发现应沉淀到 skill 的通用性问题时，**不要直接修改 SKILL.md**，告知用户，**用户同意后**再更新。

## 注意事项

1. **本 skill 只做工具链操作**：代码编写、需求理解、bug 分析由 Claude Code 本身完成
2. **串口独占**：烧录和日志读取不能同时使用同一串口
3. **设备号动态扫描**：每次操作前都扫描，不硬编码
4. **异常先确认再处理**：重复验证 2-3 次，确认非偶发后再处理
5. **安全优先**：不执行 `rm -rf` 等危险操作
6. **避免使用的方法**：
   - **picocom/minicom**: 在非交互式环境中无法正常工作（需要 TTY）
   - **pyserial**: 需要额外安装 Python 包，在受限环境中可能不可用
   - **stty + cat**: 在非 TTY 环境下会回显波特率，且无法控制 DTR/RTS 信号线

