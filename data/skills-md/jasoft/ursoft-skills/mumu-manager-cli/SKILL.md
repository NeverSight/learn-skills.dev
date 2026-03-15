---
name: mumu-manager-cli
description: 使用 MuMuManager.exe 对 MuMu 模拟器 12 实例进行统一管理与操作，包含实例配置、创建/克隆/删除/重命名、导入/导出、启动/关闭/重启/窗口控制、应用安装/卸载/启动/关闭、设备信息、系统工具、ADB 命令、驱动与排序等。适合编写脚本批量自动化管理 MuMu 模拟器时使用。
---

# MuMuManager CLI

## 用途

使用命令行查询和管理 MuMu 模拟器 12 的实例与应用配置，适合账号矩阵、批量开关、自动化脚本、运维排障等场景。

## 前置要求

- 确保模拟器版本 **V4.0.0.3179 或以上**，否则部分命令不可用。
- 定位 `MuMuManager.exe`，常见路径：`X:\Program Files\Netease\MuMuPlayer-12.0\shell\MuMuManager.exe`；本机路径示例：`C:\Program Files\Netease\MuMu\nx_main\MuMuManager.exe`。
- 建议使用绝对路径，或将 `nx_main` 目录加入 `PATH`。

## 使用流程

1. 先用 `info` 确认可用实例；`-v` 支持逗号分隔列表或 `all`。
2. 选择需要的任务（创建/克隆/删除/重命名/导入/导出/ADB/应用/控制/设置）。
3. 尽量缩小作用范围，谨慎对 `all` 执行写操作。

## 功能速查

### 实例管理

- `info` 查看实例状态与字段说明
- `create / clone / delete / rename` 创建/克隆/删除/重命名实例
- `import / export` 备份与恢复 `.mumudata`（可选 `--zip`）

## 常见坑与规避

- 删除实例前先关闭该实例：`control -v <index> shutdown`。未关闭时可能返回 `{"errcode": -1, "errmsg": "not handle cmd"}`。

### 启动与窗口控制

- `control launch / shutdown / restart` 启动/关闭/重启实例
- `control show_window / hide_window / layout_window` 显示/隐藏/布局窗口

### 应用管理

- `control app install / uninstall / launch / close / info` 使用包名或 apk 路径
- `control app info -i` 查看已安装应用与当前前台应用

### 系统工具

- `control tool func` 常用功能（截图、刷新、主页、设置、安全等）
- `control tool downcpu` 降低 CPU
- `control tool location / gyro` 虚拟定位与重力感应
- `control shortcut create / delete` 创建/删除桌面快捷方式

### 设备配置与仿真

- `setting` 读取/修改配置，支持 `--all / --all_writable / --info / --path`
- `simulation` 修改仿真属性（IMEI/IMSI/Android ID/MAC 等）

### ADB 命令

- `adb -c` 常用快捷命令（清理缓存/截图/录屏等）
- `adb -c "shell ..."` 执行自定义 shell 命令

### 其他

- `sort` 自动排列窗口
- `driver install / uninstall -n lwf` 安装/卸载驱动（可能需要管理员权限）
- 辅助接口 `api` 仅在必要时使用，稳定性依赖版本

## 参考

- 详见 `references/mumu-manager-cli.md`
- 快速定位关键词：
  - `control app` 应用管理
  - `setting` 配置项与 JSON 修改
  - `simulation` 仿真属性
  - `adb` ADB 命令
  - `driver` 驱动管理
