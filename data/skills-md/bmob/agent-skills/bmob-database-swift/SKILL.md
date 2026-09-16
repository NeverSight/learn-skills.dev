---
name: bmob-database-swift
description: "Use when implementing Bmob NoSQL database CRUD with the pure Swift BmobSwiftSDK for iOS 15+ / macOS 12+ using Swift Package Manager or CocoaPods, import BmobSDK, async/await, Bmob.initialize(appKey:), BmobObject, BmobQuery, BmobUser, BmobFile, BmobPointer, BmobRelation, BmobGeoPoint, BmobACL, CloudFunction. NOT for legacy Objective-C BmobSDK / Bridging Header projects (use bmob-database-ios), JavaScript / WeChat Mini Program (use bmob-database-javascript), Android (use bmob-database-android), Flutter / Dart (use bmob-database-flutter), or raw HTTP from other languages (use bmob-database-restful). If Bmob MCP is configured, call get_project_tables via bmob-mcp before writing code."
metadata:
  author: bmob
  version: "0.1.0"
  sdk: "BmobSwiftSDK (Swift Package Manager / CocoaPods)"
  sdk_repo: "https://github.com/bmob/BmobSwiftSDK"
  docs: "https://github.com/bmob/BmobDocs/blob/master/mds/data/swift/develop_doc.md"
  docs_raw: "https://raw.githubusercontent.com/bmob/BmobDocs/master/mds/data/swift/develop_doc.md"
  docs_quickstart: "https://github.com/bmob/BmobDocs/blob/master/mds/data/swift/index.md"
  docs_example: "https://github.com/bmob/BmobDocs/blob/master/mds/data/swift/example.md"
---

# Bmob Database — Pure Swift SDK

纯 Swift SDK `BmobSwiftSDK` 面向 iOS 15+ / macOS 12+，使用 Swift Package Manager 或 CocoaPods 安装，API 以 `async/await`、`Bmob.initialize(appKey:)`、`BmobObject`、`BmobQuery` 为核心。

如果项目使用旧版 Objective-C `BmobSDK`、`BmobSDK.xcframework`、Bridging Header 或 `saveInBackgroundWithResultBlock`，改读 [`bmob-database-ios`](../bmob-database-ios/SKILL.md)。

## 核心原则

1. **先确认 SDK 形态**：纯 Swift SDK 的包名是 `BmobSwiftSDK`，导入模块通常是 `import BmobSDK`；旧 iOS SDK 是 Objective-C framework + Bridging Header。
2. **最低环境**：Xcode 15.0+、Swift 5.9+、iOS 15.0+、macOS 12.0+。
3. **初始化是异步的**：启动早期 `try await Bmob.initialize(appKey:)`；业务请求前必要时检查 `await Bmob.isReady`。
4. **数据表默认用 `BmobObject(className:)`**：字段通过下标读写，更新 / 删除必须带 `objectId`。
5. **查询用链式 `BmobQuery`**：`whereKey`、`order`、`limit`、`skip`、`includeKey` 都返回 query，最后 `try await find()` / `get(objectId:)`。
6. **上线域名必须在初始化前设置**：私有云或备案域名用 `Bmob.resetDomain(...)`，顺序在 `initialize` 之前。

## 安全清单

- [ ] 示例只放 `"YOUR_APP_KEY"` / `"your-application-id"`，不要 commit 真实 AppKey。
- [ ] 客户端不要携带 Master Key；需要管理能力时改走服务端、REST 管理脚本或 MCP。
- [ ] 写入业务表时设置 ACL（如 `BmobACL`），避免默认权限导致任意用户读写。
- [ ] 用户密码只通过 `BmobUser` 注册、登录、改密 API 处理，不要当普通字段更新。
- [ ] 文件上传前确认来源、大小、MIME 类型；不要把本地绝对路径写进业务表。
- [ ] release 前确认 `resetDomain` 使用备案/私有云域名，且调用顺序早于初始化。

## 快速开始

### 安装

Swift Package Manager:

```swift
dependencies: [
    .package(url: "https://github.com/bmob/BmobSwiftSDK", from: "1.0.6")
],
targets: [
    .target(name: "YourApp", dependencies: [
        .product(name: "BmobSDK", package: "BmobSwiftSDK")
    ])
]
```

CocoaPods:

```ruby
platform :ios, '15.0'
use_frameworks!

target 'YourApp' do
  pod 'BmobSwiftSDK', '~> 1.0.6'
end
```

### 初始化

```swift
import SwiftUI
import BmobSDK

@main
struct MyApp: App {
    init() {
        Task {
            do {
                // 私有云或备案域名必须在 initialize 前设置：
                // Bmob.resetDomain("https://your-private-cloud.com")
                try await Bmob.initialize(appKey: "YOUR_APP_KEY")
            } catch {
                print("Bmob 初始化失败: \(error)")
            }
        }
    }

    var body: some Scene {
        WindowGroup { ContentView() }
    }
}
```

### 单条 CRUD

```swift
// 新增
let note = BmobObject(className: "Note")
note["title"] = "我的第一条笔记"
note["content"] = "Hello Bmob!"
note["score"] = 100
try await note.save()
print(note.objectId ?? "")

// 查询单条
let query = BmobQuery(className: "Note")
let fetched = try await query.get(objectId: "abc123")
print(fetched["title"] ?? "")

// 更新
let updating = BmobObject(className: "Note", data: ["objectId": "abc123"])
updating["content"] = "更新后的内容"
try await updating.update()

// 删除
let deleting = BmobObject(className: "Note", data: ["objectId": "abc123"])
try await deleting.delete()
```

### 条件查询与关联

```swift
let query = BmobQuery(className: "Note")
    .whereKey("score", greaterThan: 80)
    .whereKey("author", equalTo: BmobPointer(className: "_User", objectId: "user123"))
    .includeKey("author")
    .order(byDescending: "createdAt")
    .limit(10)

let notes = try await query.find()
```

### 用户 / 文件 / 云函数速查

```swift
// 用户
let user = BmobUser()
user.username = "testuser"
user.password = "password123"
try await user.signUp()
let loggedIn = try await BmobUser.login(username: "testuser", password: "password123")

// 文件（上传走加密客户端协议 POST /8/files；成功后可读 file.url / file.cdn）
let file = BmobFile(data: imageData, filename: "avatar.jpg", mimeType: "image/jpeg")
try await file.upload { progress in
    print("上传进度: \(Int(progress * 100))%")
}
// 删除：上传后的实例可直接 delete()；仅凭 URL 重建时请传入上传响应里的 cdn（如 "aliyun"）
// let again = BmobFile(url: file.url!, cdn: file.cdn)
// try await again?.delete()

// 云函数
let result = try await BmobCloud.run(function: "hello", params: ["name": "Swift"])
```

### 云函数参数（已知行为）

> **已知行为**：Bmob 服务端会将云函数参数的所有值转为字符串后再传入 `request.body`，因此云函数中 `typeof(param)` 始终为 `"string"`。Int/Bool/Array/Dict 等类型均会被序列化为字符串形式（如 `42`→`"42"`、`true`→`"true"`、`[1,2,3]`→`"[1,2,3]"`）。这是 Bmob 后端的设计行为，非 SDK bug。如需在云函数中使用特定类型，请在云函数内手动解析（如 `parseInt(request.body.name)`、`JSON.parse(request.body.items)`）。

客户端 `params` 可传 Swift 原生类型，但云函数侧一律按字符串处理；写云函数或联调时勿假设 `request.body` 中仍是数字 / 布尔 / 对象。

该行为适用于通过 Android、iOS、Swift 等加密客户端 SDK 以 POST 方式调用云函数的场景。

## 常见问题

跨平台问题见 [`shared/faq.md`](../../shared/faq.md)。Swift 特有判断：

- 看到 `Bridging-Header.h`、`#import <BmobSDK/Bmob.h>`、`saveInBackground`：这是旧 iOS SDK，读 [`bmob-database-ios`](../bmob-database-ios/SKILL.md)。
- 看到 `BmobSwiftSDK`、`import BmobSDK`、`try await note.save()`：这是纯 Swift SDK，使用本 skill。

## 反模式

见 [`shared/anti-patterns.md`](../../shared/anti-patterns.md)。本 skill 特有：

- 把旧 iOS SDK 的 `setObject(_:forKey:)`、`saveInBackground`、`Bmob.register(withAppKey:)` 混进纯 Swift SDK 示例。
- 在 `Bmob.initialize` 前后顺序写反：`resetDomain` 必须更早。
- 忘记 `objectId` 就调用 `update()` / `delete()`。

## 进阶能力（按需读 references/）

| 主题 | 路径 |
|---|---|
| BmobDocs 同步代码片段 | [`references/snippets/`](references/snippets/) |
| 完整 API 文档 | `metadata.docs_raw` |
| 完整 Todo 示例 | `metadata.docs_example` |

## 应用场景食谱

| 场景 | 食谱 |
|---|---|
| 用户自有 Todo（行级 ACL） | [`shared/recipes/user-owned-todos.md`](../../shared/recipes/user-owned-todos.md) |
| 博客 / CMS | [`shared/recipes/blog-cms.md`](../../shared/recipes/blog-cms.md) |
| 头像上传 | [`shared/recipes/avatar-upload.md`](../../shared/recipes/avatar-upload.md) |

## 与 MCP 联动

如已配置 [Bmob MCP](../bmob-mcp/SKILL.md)，写 Swift 代码前先 `get_project_tables` 拿真实 schema，避免：

- 表名 / 字段名拼错（Swift 下标不会提前校验 schema）。
- Pointer 目标表或 objectId 写错。
- ACL 设计与业务所有权不匹配。

## 排错速查

跨平台现象见 [`shared/faq.md`](../../shared/faq.md)。

| 现象 | 排查 |
|---|---|
| `No such module 'BmobSDK'` | SPM 是否添加 `.product(name: "BmobSDK", package: "BmobSwiftSDK")`；CocoaPods 是否打开 `.xcworkspace` |
| 初始化后请求失败 | AppKey 是否正确；`resetDomain` 是否在 `initialize` 前；release 域名是否已备案 |
| 更新 / 删除无效 | `BmobObject(className:data:)` 的 data 里必须有 `objectId` |
| 关联查询没展开 | 查询时是否 `.includeKey("author")`；Pointer 字段名和目标 objectId 是否存在 |
| `BmobError.serverError(code, message)` | 取出数字 `code` 后查 [`bmob-error-codes`](../bmob-error-codes/SKILL.md) |
| 云函数里数字 / 布尔判断不对 | `request.body` 值均为字符串；用 `parseInt`、`=== "true"`、`JSON.parse` 解析，见上文「云函数参数（已知行为）」 |
| Swift 并发警告或 UI 更新问题 | SDK 调用用 `async/await`；UI 状态更新回到 `@MainActor` / 主线程上下文 |

## 参考

- Quickstart：[index.md](https://github.com/bmob/BmobDocs/blob/master/mds/data/swift/index.md)
- 完整 API：[develop_doc.md](https://github.com/bmob/BmobDocs/blob/master/mds/data/swift/develop_doc.md)
- 完整示例：[example.md](https://github.com/bmob/BmobDocs/blob/master/mds/data/swift/example.md)
- Agent fetch：`metadata.docs_raw`
- SDK 源码：<https://github.com/bmob/BmobSwiftSDK>
- 操作路由：[`shared/operation-routing.md`](../../shared/operation-routing.md)
- 旧 iOS SDK：[`bmob-database-ios`](../bmob-database-ios/SKILL.md)
- MCP：[`bmob-mcp`](../bmob-mcp/SKILL.md)
- 写作规范：[`shared/skill-authoring.md`](../../shared/skill-authoring.md)
