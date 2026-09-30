---
name: re-android-crypto
type: atomic
description: >
  Android 加密体系审计（crypto audit）：AndroidKeyStore 密钥体系分析（别名/算法/用途/硬件背书）、
  Cipher/KeyInfo 审计、加密调用点 hook（Frida 拦截密钥别名与用途）。
  触发词：Keystore、AndroidKeyStore、Cipher、KeyInfo、StrongBox、加密审计、crypto hook、密钥别名。
capabilities: [crypto-identification, key-extraction]
---

# Android 加密体系审计（crypto audit）

## 任务分类器（intent → 路径）

| 用户目的 | 路径 |
|---|---|
| 密钥来自 AndroidKeyStore / 硬件背书密钥 | → **Keystore 审计**（步骤 1） |
| 定位加密调用点 / 拦截密文与明文 | → **crypto hook**（步骤 2） |
| 分析第三方加密库（BoringSSL / OpenSSL / Tink / libsodium 等） | → **库分析**（步骤 3） |

## 何时使用 / 何时不用

- 用：Android 应用加密体系审计——密钥体系（Keystore）、加解密调用链、库选型还原
- 用：`getEncoded()` 不可用的硬件背书密钥（须走审计而非提取密钥字节）
- 用：加密拦截时需记录密钥别名与用途（不记录密钥字节——安全边界）
- 不用：JNI/so 原生逻辑逆向（走 [[re-android-native]]）；通用加密算法识别（走 [[re-crypto-id]]）；通用密钥提取（[[re-crypto-keys]]，Keystore 硬件密钥除外）
- 不用：非 Android 平台（走通用 crypto 域 [[re-protocol]] 分支）
- 边界：本技能承接 Android crypto audit 全谱——Keystore/Cipher/KeyInfo/hook 为起点，BoringSSL/OpenSSL/Tink/libsodium 等第三方库分析归入本技能（步骤 3），不塞入 re-android-native

## 工具准备

所有工具先验证再使用。动态 hook 默认沙箱（[[re-analyze/platform-tips]] 最高原则）；静态审计可免沙箱。

### frida（[[re-frida]]）—— crypto hook 主力

- 安装与验证见 [[re-frida]] 工具准备；脚本模板见 [[re-frida/frida-scripts]]
- 验证: `frida --version`

### python3 / jadx —— 静态定位加密调用点

- python3 安装与验证见 [[re-python]] 工具准备
- jadx 安装与验证见 [[re-apk]] 工具准备

### 设备侧命令（[[re-apk]] adb 章节）

- `adb shell` 取应用运行态（KeyStore 枚举需应用进程内执行）

## 操作步骤

1. **Keystore 审计**（AndroidKeyStore 密钥体系）：
   ```java
   // 应用进程内枚举（frida 注入或 jadx 反编译定位调用点）
   KeyStore ks = KeyStore.getInstance("AndroidKeyStore");
   ks.load(null);
   java.util.Enumeration<String> aliases = ks.aliases();
   ```
   - **遍历**：`aliases()` 枚举全部条目（密钥别名 = 应用内引用键）
   - **条目属性**：算法（AES/RSA/EC）、用途（encrypt/decrypt/sign/verify）、来源——`KeyInfo.getSecurityLevel()`（API 31+，返回 SOFTWARE / TRUSTED_ENVIRONMENT(TEE) / STRONGBOX 三档）；API 23–30 只有 `isInsideSecureHardware()`（布尔，TEE 与 StrongBox 同为 true，分不开）
   - **生物绑定**：`setUserAuthenticationRequired` 的密钥在认证失败时不可用（绕过与检测见 [[re-analyze/anti-dynamic-workflow]]）
   - 产出：别名 → 算法/用途/硬件背书 清单（不记录密钥字节）

2. **crypto hook**（加密调用点拦截）：
   ```js
   // frida：拦截加密调用点，记录算法/模式/密钥别名
   // 别名来源：Key 对象本身不携带别名（KeyStore 无 getKeyAlias），须在 getKey 处记录
   const KeyStore = Java.use('java.security.KeyStore');
   KeyStore.getKey.overload('java.lang.String', '[C').implementation = function (alias, password) {
     console.log('KeyStore.getKey', alias);
     return this.getKey(alias, password);
   };
   const Cipher = Java.use('javax.crypto.Cipher');
   Cipher.init.overload('int', 'java.security.Key', 'java.security.spec.AlgorithmParameterSpec').implementation =
     function (opmode, key, params) {
       console.log('Cipher.init', opmode, key.getClass().getName(), params);  // 对应别名见上方 getKey 输出
       return this.init(opmode, key, params);
     };
   // 另路取回别名：SecretKeyFactory.getInstance(key.getAlgorithm(), 'AndroidKeyStore')
   //   .getKeySpec(key, KeyInfo.class) → KeyInfo.getKeystoreAlias()
   ```
   - hook 目标：`Cipher.init` 系列（算法/模式/IV 来源）、`KeyStore.getKey` / `getEntry`（别名与用途）、`Signature`/`Mac` 初始化（验签/校验链）
   - 记录：别名与用途，**不记录密钥字节**（安全边界，见坑 2）
   - 静态定位辅助：jadx 搜 `AndroidKeyStore` / `KeyStore.getInstance` / `Cipher.getInstance` 调用点，与 hook 结果互证

3. **第三方加密库分析**（BoringSSL / OpenSSL / Tink / libsodium 等）：
   - 识别：导入表/符号（`SSL_*`/`EVP_*`/`crypto_*`/`sodium_*` 前缀）+ jadx 依赖声明
   - 定位调用点：库 API 的 xref（静态）或 hook 库导出函数（动态）
   - 与 [[re-android-native]] 衔接：库以 .so 形态存在 → 其 JNI/内部逻辑走 [[re-android-native]]，本技能管加密语义（算法/密钥来源/用途）

4. **产出与存证**：密钥体系图（别名/算法/用途/背书来源）+ 加密调用点清单 + hook 脚本，sha256 存档供 [[re-ioc]] 引用

## 跨域联合

- [[re-android-native]]：JNI/so 原生逻辑逆向（本技能的 .so 库内部逻辑承接方；Keystore 审计自其转出）
- [[re-frida]]：hook 执行层（[[re-frida/frida-scripts]] 模板）
- [[re-crypto-id]] / [[re-crypto-keys]]：算法识别与通用密钥提取（Keystore 硬件密钥除外——走本技能审计）
- [[re-apk]]：应用静态定位（jadx 调用点）
- [[re-mobile]]：工作流移动分支（加密审计子路径）

## 常见坑与陷阱

- **把 Keystore 当普通密钥提取**：现象——`getEncoded()` 拿不到密钥字节，误判「密钥不存在」；原因——AndroidKeyStore 硬件背书密钥不可导出，这是设计而非缺失；对策——改走审计（步骤 1：别名/算法/用途/背书），不追求密钥字节
- **TEE 与 StrongBox 混为一谈**：现象——`isInsideSecureHardware` 为 true 就断言 StrongBox；原因——Secure Hardware 含 TEE 与 StrongBox 两级，该接口是布尔、分不开（`isStrongBoxBacked` 在 `KeyGenParameterSpec` 上，只管生成侧，`KeyInfo` 没有）；对策——API 31+ 用 `KeyInfo.getSecurityLevel()` 取 SOFTWARE / TEE / STRONGBOX 三档；API 23–30 无法细分，结论按「secure hardware（TEE 或 StrongBox）」标注层级
- **记录密钥字节**：现象——hook 脚本把 Keystore 密钥内容打印/落盘；原因——把审计当提取，越过安全边界；对策——只记录别名与用途，密钥字节不落盘（见步骤 2 注）
- **库语义当 JNI 逻辑分析**：现象——第三方加密库的 .so 被按 native 逻辑深挖而忽略加密语义；原因——域不清；对策——库 API 的加密语义（算法/密钥来源/用途）归本技能，内部实现细节才走 [[re-android-native]]
