---
name: dev-environment-setup
description: 全栈开发环境配置器。用于检测、选择、安装各类开发运行时与性能测试工具，并为新项目生成脚手架代码。当用户提到"创建开发环境"、"初始化项目"、"设置开发栈"、"安装 Python/Node/Go/Java/JMeter/Locust"、"创建后端项目"、"创建前端项目"、"配置全栈环境"、"新建 Django 项目"、"新建 Vue 项目"、"新建 Next.js 项目"、"设置 Java Spring 项目"、"设置 Go Web 项目"、"性能测试环境"、"压测工具安装"、"环境切换"、"dev-env"、"setup env"时触发此技能。即使用户没有明确说"环境"或"脚手架"，只要意图涉及搭建新项目的开发环境或技术栈初始化，也应触发此技能。
---

# Dev Environment Setup — 全栈开发环境配置器

## 概览

本 skill 帮助开发者快速配置开发环境并初始化项目脚手架。支持以下技术栈：

| 编号 | 环境 | 用途 | 风险等级 |
|------|------|------|---------|
| 1 | Python 3.12 | 后端运行时 / 压测脚本 / Locust / tidevice | L1 |
| 2 | Node.js 22 LTS | 前端运行时 / npm/pnpm/yarn / Hypium | L1 |
| 3 | Go 1.23 | 后端运行时 / Gin / Fiber | L1 |
| 4 | Java JDK 17 | 后端运行时 / Spring Boot / JMeter 依赖 | L1 |
| 5 | Docker Desktop | 容器化运行环境（Windows 需 WSL2） | L1 |
| 6 | Git | 版本控制 | L0 |
| 7 | SVN | 版本控制（Subversion） | L0 |
| 8 | WSL | Windows 子系统 for Linux（Docker 前置） | L1 |
| 9 | Apache JMeter 5.6.2 | HTTP 性能/压力测试 | L1 |
| 10 | Locust | Python 分布式负载测试 | L1 |
| 11 | Android ADB | Android 设备调试 / APP 自动化测试 | L0 |
| 12 | Huawei HDC | 华为鸿蒙设备调试 | L0 |
| 13 | tidevice | iOS 设备调试（Windows 支持有限，推荐 macOS） | L1 |
| 14 | Hypium | 鸿蒙测试框架（@hmos/hypium） | L1 |

---

## 执行流程

### 阶段1：环境探测

运行 `scripts/setup_env.py`（会先调用 `detect_env.py` 扫描）：

```bash
python scripts/setup_env.py
```

探测结果以**逐个环境分行展示**，每项包含编号、名称、状态、版本、路径：

```
============================================================
  Dev Environment Detection
============================================================

  OS: win32
  Drives: C:\
  System Drive: C:\

------------------------------------------------------------
  Runtime & Tool Status
------------------------------------------------------------

  [1] Python       [OK]  Python 3.14.3  -> C:\Python314\python.exe
         后端运行时，支持 Django / FastAPI / 压测脚本

  [2] Node.js      [OK]  v22.16.0  -> C:\nvm4w\nodejs\node.exe
         前后端运行时，支持 npm/pnpm/yarn

   [3] Go           [MISS]  后端运行时，支持 Gin / Fiber

   [4] Java         [MISS]  后端运行时，支持 Spring Boot / JMeter 依赖

   [5] Docker       [MISS]  容器化运行环境（需 WSL2）

   [6] Git          [OK]  git version 2.43.0  -> C:\Program Files\Git\cmd\git.exe
          版本控制

   [7] SVN          [MISS]  版本控制（Subversion）

   [8] WSL          [OK]  WSL 2.7.12  -> C:\Windows\System32\wsl.exe
          Windows 子系统 for Linux

   [9] JMeter       [MISS]  HTTP 性能/压力测试（需 Java）

   [10] Locust      [MISS]  Python 分布式负载测试（需 Python）

   [11] ADB         [OK]  Android Debug Bridge version 1.0.41
          Android 设备调试

   [12] HDC         [OK]  Ver: 3.2.0d
          华为鸿蒙设备调试

   [13] tidevice    [OK]  0.12.11
          iOS 设备调试

   [14] Hypium      [MISS]  鸿蒙测试框架（需 Node.js 18+）

------------------------------------------------------------
  Package Manager Status
------------------------------------------------------------

  [1] pip          [OK]  pip 26.2.1
  [2] npm          [OK]  10.9.2
  [3] pnpm         [OK]  11.3.0
  [4] winget       [OK]  v1.29.290
  ...

============================================================
  Summary
============================================================

  Installed:  7 / 14  (Python, Node.js, Git, WSL, ADB, HDC, tidevice)
  Missing:    7 / 14  (Go, Java, Docker, SVN, JMeter, Locust, Hypium)
```

### 阶段2：交互式选择

展示缺失项的**编号列表**（每项单独一行），用户通过编号或名称选择：

```
============================================================
  Select environments to install
============================================================

  Number  |  Name      |  Description
  --------+------------+------------------------------------------
  3       |  Go        |  后端运行时，支持 Gin / Fiber
  4       |  Java      |  后端运行时，支持 Spring Boot / JMeter 依赖
  5       |  Docker    |  容器化运行环境（需 WSL2）
  7       |  SVN       |  版本控制（Subversion）
  9       |  JMeter    |  HTTP 性能/压力测试（需 Java）
  10      |  Locust    |  Python 分布式负载测试（需 Python）

  [all]    Install all missing environments
  [skip]   Skip installation, proceed to project scaffold
──────────────────────────────────────────────────────────
```

用户输入方式：
- 单个：`3` 或 `Go`
- 多个：`3, 5, 9` 或 `Go, Docker, JMeter`
- 全部：`all`
- 跳过：`skip`

**依赖自动补齐**：用户选 `9`（JMeter）时自动带 `4`（Java）；选 `10`（Locust）时自动带 `1`（Python，若缺失）。

### 阶段3：离线包探测

运行 `scripts/check_packages.py` 检查 `E:\Tools_Package\` 中是否有已缓存的安装包：

```bash
python scripts/check_packages.py Go Java JMeter
```

输出示例：
```
------------------------------------------------------------
  Offline Package Check
------------------------------------------------------------

  [Go           ] [LOCAL   ]   152 MB  SHA UNKNOWN  E:\Tools_Package\Go\go1.23.4.windows-amd64.msi
  [Java         ] [ONLINE]  Will download from official source
  [JMeter       ] [LOCAL   ]    98 MB  SHA OK       E:\Tools_Package\JMeter\apache-jmeter-5.6.2\apache-jmeter-5.6.2.zip
```

- 有本地包 → 标记 `LOCAL`，跳过在线下载
- 无本地包 → 标记 `ONLINE`，准备从官方源下载
- **禁止从非官方镜像下载**

### 阶段4：安装前强制确认（必须执行，不得跳过）

运行 `scripts/build_plan.py` 生成完整安装计划并展示给用户：

```bash
python scripts/build_plan.py Go Java JMeter --existing detect_result.json
```

计划输出示例：
```
======================================================================
  PRE-INSTALLATION CONFIRMATION PLAN
======================================================================

  Base install directory: E:\Test_tool_enviroment\
  System drive: C:\
  Free space: 125,000 MB  |  Estimated needed: 780 MB (+20% margin)  [OK]

----------------------------------------------------------------------
  Environment Details
----------------------------------------------------------------------

  [Go] [ONLINE]
    Source:       OFFLINE (official source)
    Download URL: https://go.dev/dl/go1.23.4.windows-amd64.msi
    Install dir:  E:\Test_tool_enviroment\Go\
    Est. size:    180 MB (+20% margin)
    Risk:         L1
    Env vars:
      GOROOT (Machine) = E:\Test_tool_enviroment\Go
      Path   (Machine) = E:\Test_tool_enviroment\Go\bin

  [Java] [ONLINE]
    Source:       OFFLINE (official source)
    Download URL: https://api.adoptium.net/v3/binary/latest/17/ga/windows/x64/jdk/hotspot/normal/eclipse
    Install dir:  E:\Test_tool_enviroment\Java\
    Est. size:    360 MB (+20% margin)
    Risk:         L1
    Env vars:
      JAVA_HOME (Machine) = E:\Test_tool_enviroment\Java
      Path       (Machine) = E:\Test_tool_enviroment\Java\bin

  [JMeter] [LOCAL] (dependency: Java[OK])
    Source:       LOCAL (E:\Tools_Package\JMeter\)
    Install dir:  E:\Test_tool_enviroment\JMeter\apache-jmeter-5.6.2\
    Est. size:    144 MB (+20% margin)
    Risk:         L1
    Env vars:
      Path    (Machine) = E:\Test_tool_enviroment\JMeter\apache-jmeter-5.6.2\bin
      JMETER_HOME (Machine) = E:\Test_tool_enviroment\JMeter\apache-jmeter-5.6.2\

  Network access required: YES
  Domains to access: go.dev, api.adoptium.net

======================================================================
  CONFIRMATION REQUIRED
======================================================================

  The following actions will be performed upon your confirmation:
    - Download installers from official sources (Go, Java)
    - Verify downloaded files with SHA-256 checksums
    - Create directories under: E:\Test_tool_enviroment\
    - Modify environment variables (listed above)
    - Run installation commands (may require admin/UAC elevation)
    - Reopen terminal to apply PATH changes

  Type 'confirm' to proceed, or 'cancel' to abort.
```

**规则：**
- 用户明确输入 `confirm` 前不得下载、解压、安装、修改任何环境变量
- **OS 不兼容时 BLOCK**：当前系统不支持该环境时，标记 `[SKIP]` 并说明原因，不纳入安装计划
- **空间不足时 BLOCK**：磁盘剩余空间 < 预估占用（含 20% 余量）时，输出 `BLOCKED` 并询问用户是否指定其他盘符；未获确认前不得自动切换
- 用户输入 `cancel` 输出 `CANCELLED`，流程终止
- 用户确认后，授权本次安装所需的本地文件写入、目录创建、注册表修改和 UAC 提权，不再单独询问

### 阶段5：在线安装包下载与执行

仅在有本地包不可用时才执行下载，且**必须校验完整性**：

```powershell
# 统一下载安装器（内置超时+重试+镜像降级+SHA-256校验）
python scripts/installer.py --tool Python --url "https://..." --dest-dir "%TEMP%\python-installer" --timeout 600
```

**超时配置：**

| 工具类型 | 默认超时 | 说明 |
|---------|---------|------|
| Python / Node.js / Go / Java | 600s | 大文件下载 + MSI 安装 |
| Docker | 1200s | 超大安装包（~2GB） |
| winget / pip / npm | 300s | 包管理器操作 |
| brew / apt | 600s | 系统包管理器 |
| 其他 | 120s | 快速操作 |

**重试机制：**
- 每个镜像源下载失败后**自动重试 3 次**（间隔 5 秒）
- 所有重试耗尽后，**自动切换到下一个镜像源**
- 全部镜像均失败后，标记 `TIMEOUT`，不中断整体流程
- 输出明确的下一步建议（重试命令、手动下载链接）

**国内镜像源（固定优先）：**

| 环境 | 主镜像 | 备用1 | 备用2 |
|------|--------|-------|-------|
| Python | `mirrors.huaweicloud.com/python/` | `registry.npmmirror.com/.../python/` | `python.org/ftp/python/` |
| Node.js | `mirrors.huaweicloud.com/nodejs-release/` | `mirrors.tuna.tsinghua.edu.cn/nodejs-release/` | `nodejs.org/dist/` |
| Go | `mirrors.aliyun.com/golang/` | `mirrors.tuna.tsinghua.edu.cn/golang/` | `go.dev/dl/` |
| Java | `mirrors.huaweicloud.com/adoptium/` | `mirrors.tuna.tsinghua.edu.cn/Adoptium/` | `api.adoptium.net/...` |
| JMeter | `mirrors.tuna.tsinghua.edu.cn/apache/jmeter/` | `archive.apache.org/dist/jmeter/` | `downloads.apache.org/jmeter/` |
| Git | `mirrors.huaweicloud.com/git-for-windows/` | `mirrors.tuna.tsinghua.edu.cn/git-for-windows/` | `github.com/git-for-windows/` |

**安装包清理（需用户确认）：**

安装成功后，自动提示是否删除临时安装包以释放磁盘空间：
```
  Cleanup: Remove 1 downloaded installer(s) to free space?
    - C:\Users\EDY\AppData\Local\Temp\python-installer\installer.tmp  (245 MB)
  Confirm deletion? (y/n): y
  [+] Cleaned up 1 installer(s)
```

- 绿色解压类工具（JMeter、SVN、ADB 等）：**不产生安装包**，无此步骤
- MSI/EXE 下载类工具：安装完成后询问是否删除临时文件
- 用户选择 `n` 则保留文件，可用于后续手动排查

### 阶段6：环境安装（含环境变量配置 + 超时处理）

按用户确认的计划逐项安装：

**安装优先级：**
1. 已校验的本地包（`E:\Tools_Package\`）→ 解压/复制
2. `winget install`（Windows 首选）→ 静默安装 + 自动配置 PATH
3. `brew install`（macOS 首选）
4. 官方安装器手动安装（用户确认后运行）

**环境变量配置：**

| 环境 | 变量名 | 作用域 | 值 |
|------|--------|--------|---|
| Python | `PYTHON_HOME` | Machine | `E:\Test_tool_enviroment\Python\` |
| Python | `Path` | Machine | 追加 `%PYTHON_HOME%\` + `%PYTHON_HOME%\Scripts\` |
| Go | `GOROOT` | Machine | `E:\Test_tool_enviroment\Go\` |
| Go | `Path` | Machine | 追加 `%GOROOT%\bin\` |
| Java | `JAVA_HOME` | Machine | `E:\Test_tool_enviroment\Java\` |
| Java | `Path` | Machine | 追加 `%JAVA_HOME%\bin\` |
| JMeter | `JMETER_HOME` | Machine | `E:\Test_tool_enviroment\JMeter\apache-jmeter-5.6.2\` |
| JMeter | `Path` | Machine | 追加 `%JMETER_HOME%\bin\` |
| Node.js | `Path` | Machine | 追加安装目录 |
| SVN | `Path` | Machine | 追加 `%INSTALL_DIR%\bin\` |

**配置方式：**
- Windows: 使用 `setx` 设置 Machine 级 PATH；同时设置 `PYTHON_HOME` / `GOROOT` / `JAVA_HOME`
- macOS/Linux: 写入 `~/.zshrc` 或 `~/.bashrc`

> **重要**：如果自动配置失败，必须打印出需要手动添加的路径，不能跳过。

### 阶段7：安装验证

安装完成后重新探测，逐项验证：

```
----------------------------------------------------------------------
  Post-Installation Verification
----------------------------------------------------------------------
  Go           [OK]  go version go1.23.4
  Java         [OK]  openjdk version "17.0.11"
  JMeter       [OK]  jmeter -v → Apache JMeter Version 5.6.2
  Locust       [OK]  locust --version → 2.32.0
----------------------------------------------------------------------
```

对验证失败的项目，给出具体排查建议。

### 阶段8：项目脚手架生成

确认环境就绪后，根据用户需求生成项目脚手架：

| 选择 | 脚本 |
|------|------|
| Python Django | `python scripts/scaffold_django.py <项目名>` |
| Python FastAPI | `python scripts/scaffold_fastapi.py <项目名>` |
| Node.js Express | `python scripts/scaffold_node.py <项目名> --framework express` |
| Node.js Next.js | `python scripts/scaffold_node.py <项目名> --framework nextjs` |
| Vue 3 + TypeScript | `python scripts/scaffold_vue.py <项目名>` |
| Go Gin | `python scripts/scaffold_go.py <项目名> --framework gin` |
| Go Fiber | `python scripts/scaffold_go.py <项目名> --framework fiber` |
| Java Spring Boot | `python scripts/scaffold_java.py <项目名>` |

### 阶段9：依赖安装与工具链配置

脚手架生成后，自动安装项目依赖：

**Python 项目：**
```bash
cd <项目目录>
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install black isort flake8 mypy pre-commit
pre-commit install
```

**Node.js/TypeScript 项目：**
```bash
cd <项目目录>
npm install
npm install -D eslint prettier typescript
npx eslint --init
```

**Go 项目：**
```bash
cd <项目目录>
go mod tidy
go install golang.org/x/tools/gopls@latest
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

### 阶段10：最终报告

安装完成后，运行 `scripts/report.py` 生成结构化报告：

```bash
python scripts/report.py \
  --operation install \
  --selected Go Java JMeter Locust \
  --completed Go Java JMeter \
  --failed Locust \
  --failed-reasons "Locust:pip install network timeout" \
  --base-dir "E:\Test_tool_enviroment" \
  --system-drive "C:\"
```

报告输出示例：
```
======================================================================
  INSTALL REPORT
======================================================================

  Time:       2026-09-04 14:30:00
  Base dir:   E:\Test_tool_enviroment
  System:     C:\

  ┌─────────────────────────────┐
  │  Summary                     │
  ├─────────────────────────────┤
  │  Requested:   4             │
  │  Success:     3             │
  │  Failed:      1             │
  │  Status:      PARTIAL       │
  └─────────────────────────────┘

  Completed: Go, Java, JMeter
  Failed:    Locust — pip install network timeout

  Next Steps:
    请重新打开终端以使新环境变量生效
    验证命令: python scripts/verify_env.py Go Java JMeter
    报告已保存至: reports/report_install_20260904_143000.json
```

---

## 安装后验证

安装完成后，运行 `scripts/verify_env.py` 逐项验证：

```bash
python scripts/verify_env.py Go Java JMeter Locust
```

输出格式：
```
======================================================================
  ENVIRONMENT VERIFICATION REPORT
======================================================================

  Total checked: 4
  PASS:          3
  FAIL:          1
  MISSING:       0

  PASSED
  ----
    [PASS] Go            go version go1.23.4
    [PASS] Java          openjdk version "17.0.11"
    [PASS] JMeter        Apache JMeter Version 5.6.2

  FAILED
  ----
    [FAIL] Locust        command not found; env: 
```

**规则：**
- 每个环境独立验证，一个失败不影响其他环境的验证结果
- 未安装的环境标记 `MISSING`
- 已安装但验证失败的环境标记 `FAIL`，给出排查建议

---

## 卸载环境

运行 `scripts/uninstall_env.py` 卸载已安装的环境：

```bash
# 卸载单个环境
python scripts/uninstall_env.py Python

# 卸载多个环境
python scripts/uninstall_env.py Go Java

# 仅查看计划，不执行（dry-run）
python scripts/uninstall_env.py Python Go --dry-run
```

卸载前会打印计划，用户确认后执行：
```
======================================================================
  UNINSTALL PLAN
======================================================================

  [Python] [INSTALLED] — Python 3.14.3 -> C:\Python314\python.exe
    Risk: L2
    Will remove:
      ✗  E:\Test_tool_enviroment\Python\
      env: PYTHON_HOME (user) → remove
      env: Path (user) → remove PATH entries containing 'Python'
    Note: 会删除 E:\Test_tool_enviroment\Python\；不会删除系统级 Python

  [Go] [INSTALLED] — go version go1.23.4
    Risk: L1
    Will remove:
      ✗  E:\Test_tool_enviroment\Go\
      env: GOROOT (user) → remove
      env: Path (user) → remove PATH entries containing 'Go\bin'
    Note: 会删除 E:\Test_tool_enviroment\Go\；不会删除 winget 安装的 Go

  Type 'confirm' to proceed, 'cancel' to abort:
```

**卸载范围说明：**
- `E:\Test_tool_enviroment\<工具名>\` 目录下的安装 — 自动删除
- 系统级环境变量（Machine）— 自动清理
- 用户级环境变量（User）— 自动清理
- **不触碰**：winget/apt/brew 安装的系统级工具、其他路径的 Python/Node.js/Go 等

---

## 脚本参考

| 脚本 | 用途 |
|------|------|
| `scripts/setup_env.py` | 主入口：探测 → 选择 → 安装 → 验证 → 报告（含进度条/日志/共存提示） |
| `scripts/detect_env.py` | 环境检测：14个运行时 + OS 兼容性 + 包管理器状态 |
| `scripts/check_packages.py` | 离线包探测与 SHA-256 校验 |
| `scripts/build_plan.py` | 安装前计划生成（动态版本 + 镜像URL + 超时） |
| `scripts/resolve_versions.py` | 版本解析器（最近 5 版本列表 + URL 生成） |
| `scripts/installer.py` | 下载+安装引擎（超时/重试/镜像降级/SHA-256/清理） |
| `scripts/verify_env.py` | 安装后验证（独立检查，不阻塞） |
| `scripts/report.py` | 报告生成（JSON + HTML 双格式） |
| `scripts/uninstall_env.py` | 卸载已安装环境（dry-run + confirm） |
| `scripts/add_new_env.py` | 未知工具添加向导（交互式生成 catalog 条目） |
| `scripts/logging.py` | 会话日志（每会话独立 txt 文件） |
| `scripts/scaffold_*.py` | 6 种项目脚手架生成器 |

---

## 参考文档

- `references/env_catalog.md` — 完整环境编号清单（用途/版本/来源/目录/网络/变量/风险）
- `references/installation-guide.md` — 各运行时详细安装说明
- `references/project-templates.md` — 各技术栈推荐的目录结构

---

## 新增功能说明

### 多环境共存（Python 示例）

本机已有 Python 3.14，安装 Python 3.12 时自动检测并提示：
```
  [INFO] Python coexistence detected:
    Current:  Python 3.14.3  ->  C:\Python314\python.exe
    Target:   3.12.x         ->  E:\Test_tool_enviroment\Python\
    Note:     Use 'py -3.12' to invoke the new Python
              Use 'py -3.14' to invoke the current Python
              The py launcher handles version selection automatically.
```
- 新安装的 Python 不会覆盖系统 Python
- 使用 `py -3.12` / `py -3.14` 选择版本
- 各工具的 `PYTHON_HOME` 指向独立目录，互不干扰

### 安装日志

每次安装会话自动生成独立日志文件：
```
logs/install_20260904_143000.txt
```
记录内容：时间戳、操作类型、每个环境的安装状态、错误详情、环境变量变更。

### 进度条

安装过程中实时显示进度：
```
  [####------------] 3/14 (21%)  [OK]  Python
  [#####-----------] 4/14 (28%)  [OK]  Node.js
  [#######---------] 5/14 (35%)  [FAIL]  Go — network timeout
  [########--------] 6/14 (42%)  [OK]  Java
```

### 未知工具添加

当用户请求不在 1-14 编号内的工具时，运行交互式向导：
```bash
python scripts/add_new_env.py
```
向导引导用户填写：名称、描述、验证命令、版本列表、镜像源、安装方法、依赖、环境变量、风险等级，输出可直接粘贴到各配置文件的代码片段。
