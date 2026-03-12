---
name: xcode-build
description: Xcode 构建与配置技能。当涉及 Xcode 项目配置、Build Settings、构建脚本、Archive、导出 IPA、CI/CD 配置、命令行构建 (xcodebuild)、证书管理时使用。覆盖构建优化、Scheme 配置、编译选项、代码签名、自动化构建流程。
---

# Xcode 构建与配置

## Build Settings 核心配置

### 必须显式配置的设置
```
PRODUCT_NAME                    → 产品名称
PRODUCT_BUNDLE_IDENTIFIER       → Bundle ID
MARKETING_VERSION               → 版本号 (CFBundleShortVersionString)
CURRENT_PROJECT_VERSION         → Build 号 (CFBundleVersion)
CODE_SIGN_IDENTITY              → 代码签名身份
DEVELOPMENT_TEAM                → 开发团队 ID
PROVISIONING_PROFILE_SPECIFIER  → 配置文件名称
```

### 优化配置
```
// Debug
SWIFT_OPTIMIZATION_LEVEL = -Onone
SWIFT_COMPILATION_MODE = singlefile
GCC_OPTIMIZATION_LEVEL = 0
ENABLE_TESTABILITY = YES

// Release
SWIFT_OPTIMIZATION_LEVEL = -O
SWIFT_COMPILATION_MODE = wholemodule
GCC_OPTIMIZATION_LEVEL = s         // 二进制大小优化
VALIDATE_PRODUCT = YES
```

### 构建性能
```
COMPILER_INDEX_STORE_ENABLE = NO   // CI 中关闭索引
SWIFT_ENABLE_BATCH_MODE = YES      // 批量编译
```

## Scheme 配置

### 标准 Scheme 设置
- **Build**: 勾选 Parallelize Build，设置正确的依赖顺序
- **Run**: Debug 配置，禁用 Main Thread Checker (UI 测试时)
- **Test**: 指定测试计划，启用代码覆盖率
- **Archive**: Release 配置，Reveal Archive in Organizer

### 多环境配置
```swift
// Configuration 创建
Debug
Release
Staging (基于 Release 修改)

// xcconfig 文件
Config/Debug.xcconfig
Config/Release.xcconfig
Config/Staging.xcconfig
```

示例 xcconfig:
```
// Staging.xcconfig
#include "Release.xcconfig"
PRODUCT_BUNDLE_IDENTIFIER = com.company.app.staging
API_BASE_URL = https://staging.api.company.com
```

## xcodebuild 命令行

### 编译项目
```bash
# workspace
xcodebuild \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -configuration Release \
  -sdk iphoneos \
  -destination 'generic/platform=iOS' \
  clean build

# project
xcodebuild \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -configuration Release \
  build
```

### Archive + Export
```bash
# 1. Archive
xcodebuild archive \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -configuration Release \
  -archivePath ./build/MyApp.xcarchive \
  -destination 'generic/platform=iOS' \
  CODE_SIGN_IDENTITY="Apple Distribution" \
  DEVELOPMENT_TEAM="TEAM_ID"

# 2. Export IPA
xcodebuild -exportArchive \
  -archivePath ./build/MyApp.xcarchive \
  -exportPath ./build/IPA \
  -exportOptionsPlist exportOptions.plist
```

### exportOptions.plist
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>  <!-- app-store / ad-hoc / enterprise / development -->
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>uploadSymbols</key>
    <true/>
    <key>compileBitcode</key>
    <false/>
    <key>signingStyle</key>
    <string>manual</string>
    <key>provisioningProfiles</key>
    <dict>
        <key>com.company.app</key>
        <string>ProfileName</string>
    </dict>
</dict>
</plist>
```

### 运行测试
```bash
# 单元测试
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro,OS=17.0' \
  -resultBundlePath ./test_results.xcresult

# 代码覆盖率
xcodebuild test \
  -enableCodeCoverage YES \
  -resultBundlePath ./coverage.xcresult

# 提取覆盖率报告
xcrun xccov view --report coverage.xcresult
```

## 代码签名

### 自动签名 vs 手动签名
- **自动签名**: 本地开发推荐，Xcode 自动管理证书和配置文件
- **手动签名**: CI/CD 必须，完全控制证书和配置文件

### CI 中配置证书
```bash
# 1. 导入证书
security create-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
security unlock-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
security import cert.p12 -k build.keychain -P "$P12_PASSWORD" -T /usr/bin/codesign
security set-key-partition-list -S apple-tool:,apple: -s -k "$KEYCHAIN_PASSWORD" build.keychain

# 2. 复制配置文件
mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles
cp *.mobileprovision ~/Library/MobileDevice/Provisioning\ Profiles/

# 3. 构建时指定
xcodebuild ... \
  CODE_SIGN_IDENTITY="Apple Distribution: Company Name (TEAM_ID)" \
  PROVISIONING_PROFILE_SPECIFIER="ProfileName"
```

## Build Phases 脚本

### SwiftLint 集成
```bash
# Build Phase: Run Script
if which swiftlint >/dev/null; then
  swiftlint
else
  echo "warning: SwiftLint not installed"
fi
```

### 版本号自动递增
```bash
# Build Phase: Run Script
buildNumber=$(/usr/libexec/PlistBuddy -c "Print CFBundleVersion" "${INFOPLIST_FILE}")
buildNumber=$(($buildNumber + 1))
/usr/libexec/PlistBuddy -c "Set :CFBundleVersion $buildNumber" "${INFOPLIST_FILE}"
```

### 环境变量注入
```bash
# Build Phase: Run Script
# 从 xcconfig 注入到 Info.plist
/usr/libexec/PlistBuddy -c "Set :APIBaseURL ${API_BASE_URL}" "${BUILT_PRODUCTS_DIR}/${INFOPLIST_PATH}"
```

## CI/CD 集成

### GitHub Actions 示例
```yaml
name: iOS CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: macos-14
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Select Xcode
      run: sudo xcode-select -s /Applications/Xcode_15.2.app
    
    - name: Install Dependencies
      run: |
        brew install swiftlint
        pod install || swift package resolve
    
    - name: Build
      run: |
        xcodebuild clean build \
          -workspace MyApp.xcworkspace \
          -scheme MyApp \
          -configuration Debug \
          -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
          CODE_SIGN_IDENTITY="" \
          CODE_SIGNING_REQUIRED=NO
    
    - name: Test
      run: |
        xcodebuild test \
          -workspace MyApp.xcworkspace \
          -scheme MyApp \
          -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
          -enableCodeCoverage YES \
          -resultBundlePath coverage.xcresult
    
    - name: Upload Coverage
      run: xcrun xccov view --report coverage.xcresult > coverage.txt
```

### Fastlane 配置
```ruby
# fastlane/Fastfile
default_platform(:ios)

platform :ios do
  desc "Run tests"
  lane :test do
    run_tests(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      devices: ["iPhone 15 Pro"],
      code_coverage: true
    )
  end
  
  desc "Build for App Store"
  lane :release do
    increment_build_number
    build_app(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      export_method: "app-store",
      export_options: {
        provisioningProfiles: {
          "com.company.app" => "AppStore Profile"
        }
      }
    )
    upload_to_app_store(
      skip_metadata: true,
      skip_screenshots: true
    )
  end
end
```

## XCFramework 构建

### 创建 XCFramework
```bash
# 1. 编译各平台 archive
xcodebuild archive \
  -scheme MyFramework \
  -archivePath ./build/ios.xcarchive \
  -sdk iphoneos \
  SKIP_INSTALL=NO \
  BUILD_LIBRARY_FOR_DISTRIBUTION=YES

xcodebuild archive \
  -scheme MyFramework \
  -archivePath ./build/ios-simulator.xcarchive \
  -sdk iphonesimulator \
  SKIP_INSTALL=NO \
  BUILD_LIBRARY_FOR_DISTRIBUTION=YES

# 2. 创建 XCFramework
xcodebuild -create-xcframework \
  -framework ./build/ios.xcarchive/Products/Library/Frameworks/MyFramework.framework \
  -framework ./build/ios-simulator.xcarchive/Products/Library/Frameworks/MyFramework.framework \
  -output ./build/MyFramework.xcframework
```

### 开启 Module Stability
```
// Build Settings
BUILD_LIBRARY_FOR_DISTRIBUTION = YES
DEFINES_MODULE = YES
```

## 构建优化

### 加速编译
1. **并行构建**: Xcode → Settings → Locations → Derived Data，移到 SSD
2. **减少依赖**: 避免循环依赖，模块化拆分
3. **增量编译**: 避免修改 public header，使用 `@_spi` 替代 internal
4. **清理缓存**: `rm -rf ~/Library/Developer/Xcode/DerivedData`

### 减小包体积
```
// Build Settings
STRIP_INSTALLED_PRODUCT = YES              // Release
COPY_PHASE_STRIP = YES                     // 去除符号
STRIP_STYLE = non-global                   // 保留 global 符号
DEAD_CODE_STRIPPING = YES                  // 去除死代码
GCC_OPTIMIZATION_LEVEL = s                 // 大小优化
SWIFT_OPTIMIZATION_LEVEL = -Osize          // Swift 大小优化
ENABLE_BITCODE = NO                        // 移除 Bitcode（已废弃）
```

### dSYM 管理
```bash
# 生成 dSYM
DEBUG_INFORMATION_FORMAT = dwarf-with-dsym

# 从 xcarchive 提取
cp -r MyApp.xcarchive/dSYMs ./Symbols/

# 上传到 Firebase Crashlytics
./Pods/FirebaseCrashlytics/upload-symbols \
  -gsp GoogleService-Info.plist \
  -p ios ./Symbols/MyApp.app.dSYM
```

## 问题排查

### 构建失败常见原因
1. **Code signing**: 检查证书有效期、配置文件匹配
2. **依赖问题**: `pod deintegrate && pod install` 或 `swift package reset`
3. **缓存问题**: Clean Build Folder (Cmd+Shift+K)，删除 DerivedData
4. **Xcode 版本**: 确保 CI Xcode 版本与本地一致

### Debug 构建命令
```bash
# 详细输出
xcodebuild -verbose ...

# 仅显示命令
xcodebuild -dry-run ...

# 显示 Build Settings
xcodebuild -showBuildSettings \
  -workspace MyApp.xcworkspace \
  -scheme MyApp
```

## 行为准则
- 所有环境差异用 xcconfig 管理，不在代码中硬编码
- CI 构建必须用手动签名 + 明确的 Code Sign Identity
- Archive 前必须 Clean，避免缓存污染
- 每次发版必须打 Git tag 与 Build Number 对应
- 构建脚本中敏感信息用环境变量，不提交到代码库
- 生产构建必须上传 dSYM 到崩溃分析服务

## ✅ Sentinel（Skill 使用自检）
当且仅当你确定"当前任务已经加载并正在使用本 Skill"时：

- 在回复末尾追加一行：`// skill-used: xcode-build`

规则：
- 只能追加一次
- 如果不确定是否加载，禁止输出 sentinel
- 输出 sentinel 代表你已遵守本 Skill 的配置规范与构建流程
