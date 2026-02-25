---
name: tauri-v2
description: Tauri v2 项目开发助手 - 提供 CLI 项目管理、最佳实践指导和代码生成。适用于 (1) 创建和管理 Tauri v2 项目 (2) 开发桌面和移动应用 (3) 配置构建和分发流程 (4) 实现安全的前后端通信 (5) 应用架构设计和性能优化。
---

# Tauri v2 Agent

本技能提供 Tauri v2 项目的全面开发支持，包括 CLI 操作、架构设计、安全实践和部署策略。

## 使用场景

- **项目创建**: 使用 `create-tauri-app` 或手动初始化新项目
- **CLI 管理**: 执行开发、构建、打包等命令
- **代码生成**: 生成命令、状态管理、错误处理等模板代码
- **架构指导**: 项目结构设计、前后端通信模式
- **安全实践**: 权限配置、输入验证、CSP 设置
- **性能优化**: 构建配置、资源管理、缓存策略
- **部署分发**: CI/CD 配置、自动更新、多平台构建

## 快速参考

### 核心命令

```bash
# 创建项目 (自动化环境中必须使用非交互式命令)
# 注意：在使用自动化工具（如 Agent）创建项目时，请先向用户收集以下参数：
# 1. 项目名称 (<PROJECTNAME>)
# 2. 包管理器 (--manager: pnpm, npm, yarn, cargo 等)
# 3. UI 模板 (--template: react-ts, vue-ts, vanilla, svelte-ts 等)
# 4. 唯一标识符 (--identifier: com.your.app)
# 收集完毕后，使用如下非交互式命令创建：
pnpm create tauri-app@latest <项目名称> --manager <包管理器> --template <UI模板> --identifier <唯一标识符> -y

# 开发 (建议在项目根目录下使用包管理器运行)
npm run tauri dev
# 若使用 pnpm 则为: pnpm tauri dev

# 构建
npm run tauri build

# 添加官方插件
npx tauri add fs
```

### 文件结构

```
project/
├── src/                 # 前端代码
├── src-tauri/           # Rust 后端
│   ├── src/
│   │   ├── main.rs      # 入口
│   │   ├── commands.rs  # 命令
│   │   ├── state.rs     # 状态
│   │   └── error.rs     # 错误
│   ├── capabilities/    # 权限配置
│   └── tauri.conf.json  # 配置
```

## 详细指南

### CLI 项目管理

参考 [cli-management.md](references/cli-management.md) 获取完整的 CLI 使用指南：

- 安装与初始化
- 开发命令 (`dev`, `android dev`, `ios dev`)
- 构建命令 (`build`, `android build`, `ios build`)
- 打包命令 (`bundle`)
- 常见工作流和故障排除

### 配置文件解析

参考 [config-reference.md](references/config-reference.md) 获取 `tauri.conf.json` 的详细解析与指南：

- 基础信息配置
- 构建行为 (`build` 节点)
- 应用窗口与安全 (`app` 节点)
- 平台打包选项 (`bundle` 节点)
- 插件参数配置 (`plugins` 节点)
- 环境区分配置 (特定平台配置)
- v1 迁移至 v2 的配置变更点
### 最佳实践

参考 [best-practices.md](references/best-practices.md) 获取架构和安全指南：

- 项目目录结构规范
- 命令设计模式
- 状态管理
- 安全实践 (最小权限、输入验证、CSP)
- 错误处理
- 性能优化
- 测试策略
- 日志与监控
- 部署与分发
- 平台特定处理

## 常用代码模式

### 基础命令模板

```rust
use tauri::State;
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct Request {
    data: String,
}

#[derive(Serialize)]
pub struct Response {
    result: String,
}

#[tauri::command]
pub async fn my_command(
    request: Request,
    state: State<'_, AppState>,
) -> Result<Response, AppError> {
    Ok(Response {
        result: format!("Processed: {}", request.data),
    })
}
```

### 前端调用封装

```typescript
import { invoke } from '@tauri-apps/api/core';

export async function myCommand(data: string): Promise<string> {
  try {
    const response = await invoke<{ result: string }>('my_command', { data });
    return response.result;
  } catch (error) {
    console.error('Command failed:', error);
    throw new Error(`操作失败: ${error}`);
  }
}
```

### 错误类型定义

```rust
use thiserror::Error;
use serde::{Deserialize, Serialize};

#[derive(Error, Debug, Serialize, Deserialize)]
pub enum AppError {
    #[error("IO 错误: {0}")]
    IoError(String),
    #[error("权限被拒绝")]
    PermissionDenied,
    #[error("无效的输入")]
    InvalidInput,
}
```

### 权限配置

```json
{
  "identifier": "default",
  "permissions": [
    "core:default",
    {
      "identifier": "fs:allow-read",
      "allow": [{"path": "$APPDATA/*"}]
    }
  ]
}
```

## 常见问题

### 构建失败

1. 更新 Rust: `rustup update`
2. 清理缓存: `cargo clean`
3. 检查依赖: `npm install`

### 移动开发

- iOS: 需要 Xcode，启用 Web Inspector
- Android: 需要 Android Studio，启用 USB 调试
- 真机调试: 设置 `TAURI_DEV_HOST` 环境变量

### 性能问题

- Release 构建配置 `opt-level = "s"`
- 使用连接池管理数据库连接
- 异步操作避免阻塞主线程
- 前端使用虚拟列表处理大数据

### `__cmd__` 宏重复定义 (E0255)

**症状**: 编译报错 `the name '__cmd__greet' is defined multiple times (E0255)`

**原因**: `#[tauri::command]` 宏和 `generate_handler!` 宏都会生成 `__cmd__<fn_name>` 内部宏。当 command 函数直接定义在 `lib.rs` 或 `main.rs` 中，且同一文件调用了 `generate_handler!` 时，两者在同一 crate root 作用域内产生命名冲突。这是 **Tauri 已知的架构限制**（所有版本 1.x ~ 2.x 均受影响）。

**解决方案**: 将所有 `#[tauri::command]` 函数移到子模块中（如 `commands.rs`），在 `generate_handler!` 中使用完整路径引用：

```rust
// src-tauri/src/lib.rs (或 main.rs)
mod commands;

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            commands::greet,
            commands::open_link,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

> **注意**: 即使函数不加 `pub`，只要它带有 `#[tauri::command]` 并且与 `generate_handler!` 在同一文件，就会产生此冲突。务必始终将命令函数放在独立子模块中。

## 参考链接

- [Tauri v2 文档](https://v2.tauri.app/)
- [Tauri v2 配置文件参考](https://v2.tauri.app/reference/config/)
- [Rust 文档](https://doc.rust-lang.org/)
- [Tauri GitHub](https://github.com/tauri-apps/tauri)
