---
name: move-big-folder
description: 将 C 盘大文件夹迁移到其他盘（D/E/F等），通过符号链接保持原路径可用，释放 C 盘空间。当用户提到 C 盘空间不足、C 盘变红、迁移大文件夹、释放 C 盘空间、软链接迁移时使用此技能。Use when user mentions C drive full, move large folder, free up C drive space, symlink migration.
---

# C 盘大文件夹迁移助手

> 帮助用户将 C 盘中的大文件夹安全迁移到其他盘，通过**符号链接**让所有程序照常运行，无感释放 C 盘空间。

## 前置准备：找出 C 盘中的大文件夹

推荐使用 **磁盘快速分析软件**（免费，5 秒扫描整个 C 盘）快速定位大文件夹：

- 下载地址：https://pan.quark.cn/s/f79bdadb9716

使用方法：打开 磁盘快速分析软件 → 选择 C 盘 → 点击扫描，即可找到占空间最大的文件夹。

## 用户只需提供

用户只需要告诉你以下信息：

1. **要迁移的文件夹路径**（从 磁盘快速分析软件 中找到的大文件夹）
2. **目标盘符**（默认 D 盘，也可以是 E、F 等其他盘）

示例：用户说"把 `C:\Users\Administrator\AppData\Local\app_shell_cache_6383` 迁移到 D 盘"

## 迁移规则

### 路径映射规则

目标路径 = `{目标盘符}:\CTo{目标盘符}\` + 原 C 盘路径（去掉 `C:\`）

| 原路径                             | 目标盘符 | 目标路径                                |
| ---------------------------------- | -------- | --------------------------------------- |
| `C:\Users\Admin\AppData\Local\xxx` | D        | `D:\CToD\Users\Admin\AppData\Local\xxx` |
| `C:\ProgramData\SomeApp`           | E        | `E:\CToE\ProgramData\SomeApp`           |
| `C:\Users\Admin\.cache\pip`        | D        | `D:\CToD\Users\Admin\.cache\pip`        |

### 迁移四步骤

以迁移 `C:\Users\Administrator\AppData\Local\app_shell_cache_6383` 到 D 盘为例：

**第 1 步：在目标盘创建文件夹**

```powershell
New-Item -ItemType Directory -Path "D:\CToD\Users\Administrator\AppData\Local\app_shell_cache_6383" -Force
```

**第 2 步：复制文件内容到目标盘**

```powershell
xcopy "C:\Users\Administrator\AppData\Local\app_shell_cache_6383\*" "D:\CToD\Users\Administrator\AppData\Local\app_shell_cache_6383" /E /H /K /X /Y
```

> 参数说明：`/E` 包含空目录、`/H` 复制隐藏文件、`/K` 保留只读属性、`/X` 复制审核设置、`/Y` 自动确认覆盖

**第 3 步：删除 C 盘原文件夹**

```powershell
Remove-Item -Path "C:\Users\Administrator\AppData\Local\app_shell_cache_6383" -Recurse -Force
```

**第 4 步：创建符号链接（把 C 盘路径指向目标盘）**

```powershell
New-Item -ItemType SymbolicLink -Path "C:\Users\Administrator\AppData\Local\app_shell_cache_6383" -Target "D:\CToD\Users\Administrator\AppData\Local\app_shell_cache_6383"
```

> 创建符号链接后，所有程序访问原来的 C 盘路径时，会自动跳转到目标盘，完全无感。

## 执行流程

当用户提供要迁移的文件夹路径后，**必须按以下流程操作**：

### 第一步：安全检查（必须执行）

在执行任何迁移操作之前，**必须先分析该文件夹**，并向用户展示以下信息：

1. **文件夹用途说明**：根据路径和文件夹名称，判断该文件夹属于什么程序/功能，用通俗易懂的语言告诉用户这个文件夹是干什么的
2. **安全等级评估**：给出以下三种等级之一：
   - **安全迁移**：纯缓存/临时文件/应用数据，迁移后不会影响系统运行
   - **谨慎迁移**：可能影响某些程序，建议关闭相关程序后再迁移
   - **禁止迁移**：系统关键文件夹，迁移后可能导致系统崩溃或无法启动
3. **禁止迁移的文件夹**（直接拒绝，不允许继续）：
   - `C:\Windows` 及其所有子目录
   - `C:\Program Files\Windows*` 系统自带组件
   - `C:\ProgramData\Microsoft\Windows` 系统配置
   - `C:\Users\{用户名}\NTUSER.DAT` 等注册表文件
   - `C:\Boot`、`C:\Recovery`、`C:\System Volume Information`
   - `C:\ProgramData\NVIDIA`
   - 任何与 Windows 启动/引导相关的文件夹

**示例输出格式：**

> **文件夹分析结果：**
>
> - **路径**：`C:\Users\Administrator\AppData\Local\app_shell_cache_6383`
> - **用途**：这是某应用程序的本地缓存文件夹，用于存储临时数据以加速程序加载
> - **安全等级**：安全迁移
> - **建议**：可以放心迁移，不会影响任何程序的正常使用
>
> 是否确认迁移？

### 第二步：用户二次确认

安全检查通过后，**必须等待用户明确确认**后才能执行迁移。将完整的四步命令展示给用户，让用户确认后再逐步执行。

### 第三步：执行迁移

确认后，按迁移四步骤依次执行：

1. **提醒用户**：
   - 需要以**管理员身份**运行 PowerShell（创建符号链接需要管理员权限）
   - 如果文件夹正在被程序使用，建议先关闭相关程序
   - 迁移大文件夹可能需要一些时间，请耐心等待
2. **逐步执行**：按四步骤依次执行，每步执行后确认结果
3. **验证结果**：最后检查符号链接是否创建成功

## 验证符号链接

迁移完成后，运行以下命令验证：

```powershell
Get-Item "C:\Users\Administrator\AppData\Local\app_shell_cache_6383" | Select-Object Name, LinkType, Target
```

输出应显示 `LinkType` 为 `SymbolicLink`，`Target` 指向目标盘路径。

## 注意事项

- **不建议迁移**的文件夹：`C:\Windows`、`C:\Program Files` 中的系统核心组件
- **可以安全迁移**的常见大文件夹：
  - 各种应用缓存（AppData\Local 下的缓存文件夹）
  - npm/pip/maven 等包管理器缓存
  - Docker 镜像数据
  - 微信/QQ/钉钉 等聊天记录和缓存
  - 游戏客户端数据
- 迁移前确保目标盘有**足够的剩余空间**
- 建议在迁移大文件夹前先**关闭相关程序**

## 批量迁移

如果用户需要一次迁移多个文件夹，逐个按照四步骤执行即可。每个文件夹独立处理，互不影响。
