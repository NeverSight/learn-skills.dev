---
name: android-proguard-helper
description: >-
  Android ProGuard/R8 obfuscation rules generator and analyzer.
  Scan source code for reflection, Gson SerializedName, JNI, AndroidManifest components.
  Auto-generate keep rules for Gson, Retrofit, EventBus, Room, Glide, Dagger, Hilt.
  Use when enabling minification, encountering ClassNotFoundException after obfuscation,
  NoSuchMethodError in release builds, fixing ProGuard warnings, writing keep rules,
  configuring R8 full mode, shrinkResources, debugging mapping.txt.
  Covers proguard-rules.pro syntax, consumer rules, library ProGuard files.
  Zero external dependencies — pure Python standard library.
---

# Android ProGuard/R8 混淆规则助手

自动扫描源码并生成 ProGuard/R8 keep 规则，覆盖反射、序列化、JNI、四大组件等场景。

## 适用场景

- 开启混淆后出现 `ClassNotFoundException` / `NoSuchMethodError`
- 新增依赖库后需要添加 keep 规则
- 检查现有 `proguard-rules.pro` 是否遗漏
- 想要了解 ProGuard/R8 规则语法
- release 构建崩溃但 debug 正常

## 使用方式

脚本位置：`scripts/proguard_analyzer.py`（相对于本 Skill 目录）

### 扫描并生成规则

```bash
# 扫描源码目录，自动生成keep规则
python3 <SKILL_DIR>/scripts/proguard_analyzer.py scan <module_path>

# 仅扫描指定类型 (reflection/serialization/jni/manifest/all)
python3 <SKILL_DIR>/scripts/proguard_analyzer.py scan <module_path> --type reflection

# 输出到文件
python3 <SKILL_DIR>/scripts/proguard_analyzer.py scan <module_path> -o generated_rules.pro
```

### 获取常见库的规则模板

```bash
# 列出所有支持的库模板
python3 <SKILL_DIR>/scripts/proguard_analyzer.py templates

# 获取指定库的规则
python3 <SKILL_DIR>/scripts/proguard_analyzer.py template gson
python3 <SKILL_DIR>/scripts/proguard_analyzer.py template retrofit
python3 <SKILL_DIR>/scripts/proguard_analyzer.py template room
```

### 分析现有规则文件

```bash
# 检查proguard-rules.pro中的潜在问题
python3 <SKILL_DIR>/scripts/proguard_analyzer.py check <module_path>/proguard-rules.pro
```

## ProGuard/R8 规则语法速查

### 基本规则

```proguard
# 保留类及其所有成员
-keep class com.example.MyClass { *; }

# 仅保留类名（成员可混淆）
-keep class com.example.MyClass

# 保留类的所有 public 成员
-keep class com.example.MyClass {
    public *;
}

# 通配符保留整个包
-keep class com.example.model.** { *; }

# 保留实现了某接口的类
-keep class * implements com.example.MyInterface { *; }

# 保留带特定注解的类
-keep @com.example.Keep class * { *; }
```

### 常用修饰符

| 修饰符 | 说明 |
|--------|------|
| `-keep` | 保留类和成员（不被移除也不被混淆） |
| `-keepnames` | 保留名称（可被移除但不被混淆） |
| `-keepclassmembers` | 仅保留成员（类名可混淆） |
| `-keepclasseswithmembers` | 保留匹配成员的类及其成员 |
| `-dontwarn` | 抑制指定类的警告 |
| `-dontnote` | 抑制指定类的说明 |

### R8 特有

```proguard
# R8 全模式（更激进优化）
# gradle.properties: android.enableR8.fullMode=true

# 保留成员的注解
-keepattributes *Annotation*

# 保留泛型信息（Gson/Retrofit需要）
-keepattributes Signature

# 保留异常信息（保留堆栈可读性）
-keepattributes SourceFile,LineNumberTable
```

## AI 使用指南

当用户遇到以下情况时，自动使用本工具：
- "混淆后崩溃了" / "release包闪退" → 先 `scan` 检查缺失规则
- "怎么写keep规则" → 提供语法速查 + `template` 示例
- "加了xxx库需要什么混淆规则" → `template <library>`
- "检查混淆配置" → `check` 分析现有规则
