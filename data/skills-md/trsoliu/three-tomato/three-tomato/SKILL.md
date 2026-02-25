---
name: three-tomato
description: 将需求文档转换为多端原生开发代码，支持 Android、iOS、鸿蒙、小程序、快应用、H5、Web、macOS、Windows 等 17 个平台。原生优先，AI 友好技术栈。
license: MIT
---

# Three-Tomato

将需求文档转换为多端**原生**开发代码，支持 Android、iOS、鸿蒙、小程序、快应用、H5、Web、macOS、Windows 等 17 个平台。

> **核心原则**：原生优先，AI 友好技术栈（数据集大、文档丰富）

## Overview

This skill enables AI Agents to analyze requirement documents and generate **native** platform-specific code using AI-friendly tech stacks with large training datasets.

## Supported Platforms

| Platform | Code | Language/Framework | AI-Friendly Reason |
|----------|------|-------------------|-------------------|
| **原生移动端** | | | |
| Android | `android` | Kotlin + Jetpack Compose | Kotlin 数据集大，Compose 声明式 UI |
| iOS | `ios` | Swift + SwiftUI | Swift 现代语法，SwiftUI 声明式 |
| HarmonyOS | `harmony` | ArkTS + ArkUI | TypeScript 超集，AI 熟悉 |
| **小程序** | | | |
| WeChat Mini Program | `wechat-mp` | TypeScript + 原生 WXML | TS 类型安全，文档丰富 |
| Alipay Mini Program | `alipay-mp` | TypeScript + 原生 AXML | 同上 |
| Baidu Mini Program | `baidu-mp` | TypeScript + 原生 Swan | 同上 |
| Quick App | `quick-app` | TypeScript | 类 Vue 语法 |
| **Web** | | | |
| H5 Mobile | `h5` | TypeScript + React | React 优先，数据集最大 |
| Web Desktop | `web` | TypeScript + React + Next.js | SSR/SSG，企业级首选 |
| **桌面原生** | | | |
| macOS | `macos` | Swift + SwiftUI | 原生 Apple 生态 |
| Windows | `windows` | C# + WinUI 3 | .NET 生态成熟，AI 友好 |
| **跨端移动** | | | |
| Flutter | `flutter` | Dart + Riverpod | 高性能，声明式 UI |
| React Native | `react-native` | TypeScript + Zustand | React 生态，AI 友好 |
| Uni-app | `uni-app` | Vue 3 + TypeScript | 一套代码多端运行 |
| Taro | `taro` | React + TypeScript | 京东出品，React 生态 |
| **跨端桌面** | | | |
| Electron | `electron` | React + TypeScript | Web 技术栈，成熟稳定 |
| Tauri | `tauri` | Rust + React | 高性能，体积小 |

## Trigger Commands

### Code Generation
```
🤖 "transform to [platform]"
🤖 "generate [platform] code"
🤖 "convert requirement to multi-platform"
🤖 "create platform specs"
🤖 "转换为[平台]代码"
🤖 "生成多端代码"
```

### Self-Evolution
```
🧬 "3T evolve" / "3T 总结归纳进化"
🧬 "3T log issue [description]" / "3T 记录问题 [描述]"
🧬 "3T show evolution log" / "3T 查看进化日志"
```

## Workflow

### Evolution Workflow (3T evolve / 3T 总结归纳进化)

When `3T evolve` command is triggered, AI Agent executes:

#### Step 1: Collect Feedback
1. Scan `.three-tomato/feedback/issues/` for issue records
2. Analyze compile/runtime errors in `.three-tomato/output/`
3. Identify patterns from user's manual code fixes

#### Step 2: Categorize Issues
1. Group by platform (Android/iOS/Mini Programs, etc.)
2. Group by type (syntax error/API changes/best practices/architecture)
3. Calculate issue frequency

#### Step 3: Update Knowledge
1. Update `references/patterns/known-issues.yaml` - known issues database
2. Update `references/patterns/best-practices.yaml` - best practices
3. Update platform-specific `plugins/[platform]-generator/PLUGIN.md`
4. Log changes to `.three-tomato/evolution/changelog.md`

#### Step 4: Validate Improvements
1. Generate test cases for high-frequency issues
2. Verify improved templates resolve the issues
3. Output evolution report to `.three-tomato/evolution/reports/`

---

### Phase 1: Requirement Analysis
1. Read requirement document from `.three-tomato/requirements/` or specified path
2. Parse and extract:
   - Feature specifications
   - UI/UX requirements
   - Data models
   - API interfaces
   - Business logic flows

### Phase 2: Platform Selection
1. Read `.three-tomato/config.yaml` for target platforms
2. Check enabled plugins in `plugins/_registry.yaml`
3. Determine output platforms based on user command or config

### Phase 3: Code Generation
For each target platform:
1. Load platform-specific templates from `references/templates/[platform]/`
2. Apply tech stack configurations
3. Generate:
   - Project structure
   - UI components
   - Data models
   - API clients
   - Business logic
   - Platform-specific configurations

### Phase 4: Output & Validation
1. Write generated code to `.three-tomato/output/[platform]/`
2. Generate comparison matrix
3. Create migration guides between platforms

## Configuration

Read configuration from `.three-tomato/config.yaml`:

```yaml
# Target platforms to generate
platforms:
  - android
  - ios
  - wechat-mp
  - h5

# AI-Friendly Tech Stack (原生优先，数据集大)
tech_stack:
  android:
    language: kotlin              # AI 数据集大
    ui: compose                   # 声明式，AI 友好
    architecture: mvvm
    di: hilt
    network: retrofit + okhttp
    async: coroutines
    
  ios:
    language: swift               # 现代语法，AI 熟悉
    ui: swiftui                   # 声明式 UI
    architecture: mvvm
    network: urlsession           # 原生优先
    async: async-await
    
  harmony:
    language: arkts               # TypeScript 超集
    ui: arkui
    architecture: mvvm
    
  wechat-mp:
    language: typescript          # 类型安全，AI 友好
    framework: native             # 原生开发
    
  alipay-mp:
    language: typescript
    framework: native
    
  baidu-mp:
    language: typescript
    framework: native
    
  quick-app:
    language: typescript
    
  h5:
    language: typescript
    framework: react              # React 优先，数据集最大
    ui: antd-mobile
    bundler: vite
    
  web:
    language: typescript
    framework: react              # React 优先
    meta_framework: nextjs        # SSR/SSG 支持
    ui: antd / shadcn-ui
    state: zustand
    
  macos:
    language: swift
    ui: swiftui
    architecture: mvvm
    
  windows:
    language: csharp              # C# AI 数据集大
    ui: winui3                    # 现代 Windows UI
    architecture: mvvm

# Output settings
output:
  directory: .three-tomato/output
  include_tests: true
  include_docs: true
  language: zh-CN
```

## Plugin System

### Hook Points
Plugins can extend functionality at these hooks:
- `before_analyze` - Pre-process requirement documents
- `after_analyze` - Post-process extracted requirements
- `before_generate` - Modify generation parameters
- `on_generate` - Custom code generation logic
- `after_generate` - Post-process generated code
- `on_export` - Custom export formats

### Plugin Commands
```
📋 "list platform plugins"
📦 "install plugin <source>"
✅ "enable plugin <name>"
❌ "disable plugin <name>"
```

### Built-in Plugins
| Plugin | Description |
|--------|-------------|
| **原生平台** | |
| `android-generator` | Android 原生 (Kotlin + Compose) |
| `ios-generator` | iOS 原生 (Swift + SwiftUI) |
| `harmony-generator` | HarmonyOS (ArkTS + ArkUI) |
| `wechat-mp-generator` | 微信小程序 (TypeScript) |
| `alipay-mp-generator` | 支付宝小程序 (TypeScript) |
| `baidu-mp-generator` | 百度智能小程序 (TypeScript) |
| `quick-app-generator` | 快应用 (TypeScript) |
| `h5-generator` | H5 移动端 (React + TypeScript) |
| `web-generator` | Web 桌面端 (Next.js + React) |
| `macos-generator` | macOS 原生 (Swift + SwiftUI) |
| `windows-generator` | Windows 原生 (C# + WinUI 3) |
| **跨端框架** | |
| `flutter-generator` | Flutter (Dart + Riverpod) |
| `rn-generator` | React Native (TypeScript + Zustand) |
| `uni-app-generator` | Uni-app (Vue 3 + TypeScript) |
| `taro-generator` | Taro (React + TypeScript) |
| `electron-generator` | Electron (React + TypeScript) |
| `tauri-generator` | Tauri (Rust + React) |
| **工具类** | |
| `api-sync` | 跨平台 API 定义同步 |
| `ui-converter` | UI 组件跨平台转换 |
| `i18n-sync` | 国际化资源同步 |
| `diff-report` | 平台差异报告生成 |

## Output Structure

```
.three-tomato/
├── config.yaml              # Main configuration
├── requirements/            # Input requirement documents
│   ├── PRD.md              # Product requirement document
│   ├── api.yaml            # API specifications
│   └── ui-specs/           # UI design specs
├── cache/                   # Incremental cache
├── output/                  # Generated code
│   ├── android/            # Kotlin + Compose
│   ├── ios/                # Swift + SwiftUI
│   ├── harmony/            # ArkTS + ArkUI
│   ├── wechat-mp/          # TypeScript 原生
│   ├── alipay-mp/          # TypeScript 原生
│   ├── baidu-mp/           # TypeScript 原生
│   ├── quick-app/          # TypeScript
│   ├── h5/                 # React + TypeScript
│   ├── web/                # Next.js + React
│   ├── macos/              # Swift + SwiftUI
│   ├── windows/            # C# + WinUI 3
│   └── _shared/            # 共享资源
│       ├── models/         # 数据模型定义
│       ├── api/            # API 接口定义
│       └── assets/         # 共享资源文件
├── reports/                 # Analysis reports
│   ├── comparison.md       # Platform comparison
│   ├── migration.md        # Migration guide
│   └── compatibility.md    # Compatibility matrix
└── i18n/                    # Multi-language docs
    ├── en/
    └── zh/
```

## Important Instructions

### For AI Agent:

1. **Always read config first**: Check `.three-tomato/config.yaml` before generation
2. **Respect tech stack**: Use configured frameworks and libraries
3. **Maintain consistency**: Ensure data models and API calls are consistent across platforms
4. **Platform idioms**: Follow each platform's best practices and conventions
5. **Protocol Retention**: 
   - If requirement/legacy uses **gRPC**:
     - **Supported Platforms** (iOS, Android, Windows, macOS, Flutter): **MUST use gRPC** to maintain high performance and type safety.
     - **Restricted Platforms** (Mini Programs, H5): **Fallback to HTTP/JSON** (via Envoy/Gateway).
   - If requirement uses REST/GraphQL: Use standard HTTP clients.
6. **Incremental updates**: Only regenerate changed parts using cache
7. **Preserve user content**: Content marked with `<!-- user-content -->` must not be overwritten

### Code Quality Standards:
- Follow platform-specific coding guidelines
- Include proper error handling
- Add necessary comments (in configured language)
- Generate unit tests when `include_tests: true`
- Create platform-specific README with setup instructions

### Cross-Platform Consistency:
- Unified data model definitions
- Consistent API interface naming
- Shared business logic documentation
- Synchronized i18n resources

## References

- Templates: `references/templates/`
- Prompts: `references/prompts/`
- Examples: `references/examples/`
- Platform Guides: `docs/platforms/`

## Version

- Skill Version: 1.0.1
- Last Updated: 2026-01-30
- Author: three-tomato
