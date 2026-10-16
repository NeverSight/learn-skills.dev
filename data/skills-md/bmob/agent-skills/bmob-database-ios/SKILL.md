---
name: bmob-database-ios
description: "Use when implementing Bmob NoSQL database CRUD in an iOS native project — both Objective-C and Swift / SwiftUI / UIKit. Triggers: BmobSDK, BmobSDK.xcframework, pod 'BmobSDK', #import <BmobSDK/Bmob.h>, Bmob registerWithAppKey, [Bmob register(withAppKey:)], BmobObject objectWithClassName, BmobQuery queryWithClassName, BmobUser, BmobInstallation, BmobFile, BmobGeoPoint, BmobRelation, saveInBackgroundWithResultBlock, getObjectInBackgroundWithId, findObjectsInBackground, Bridging-Header.h. NOT for cross-platform JavaScript / WeChat Mini Program (use bmob-database-javascript), Android (use bmob-database-android), Flutter / Dart (use bmob-database-flutter), or any other language via REST (use bmob-database-restful). If Bmob MCP is configured, call get_project_tables via bmob-mcp before writing code."
metadata:
  author: bmob
  version: "0.1.0"
  sdk: "BmobSDK (CocoaPods: pod 'BmobSDK')"
  sdk_repo: "https://github.com/bmob/Bmob-iOS-SDK"
  docs: "https://github.com/bmob/BmobDocs/blob/master/mds/data/ios/develop_doc.md"
  docs_raw: "https://raw.githubusercontent.com/bmob/BmobDocs/master/mds/data/ios/develop_doc.md"
  docs_swift: "https://github.com/bmob/BmobDocs/blob/master/mds/data/ios/swift_develop_doc.md"
  docs_swift_raw: "https://raw.githubusercontent.com/bmob/BmobDocs/master/mds/data/ios/swift_develop_doc.md"
  docs_quickstart: "https://github.com/bmob/BmobDocs/blob/master/mds/data/ios/swift_quick_start.md"
  swift_demo: "https://github.com/bmob/bmob-ios-demo/blob/master/SwiftDemo.zip"
---

# Bmob Database — iOS Native SDK

iOS SDK 名为 `BmobSDK`，是 **Objective-C 编写**的 framework，Swift 项目通过 **Bridging Header** 桥接使用。SDK 数据模型以 `BmobObject` 为核心，不需要为每个表写子类（与 Android 不同）。

## 核心原则

**1. 安装 SDK — 强推 CocoaPods**：

```ruby
# Podfile
target "你的项目名称" do
  platform :ios, "15.6"
  use_frameworks!
  pod 'BmobSDK'
end
```

```bash
pod install
```

> 装完后**只打开 `.xcworkspace`**，不要再打开 `.xcodeproj`，否则找不到 Pod 引入的库。

也可手动导入 `BmobSDK.xcframework`，并链接以下系统库（详见 [`references/install.md`](references/install.md)）。

**2. Swift 必须桥接：** 新建任意 `.m` 文件让 Xcode 弹"Create Bridging Header"，然后在生成的 `项目名-Bridging-Header.h` 加：

```objc
#import <BmobSDK/Bmob.h>
```

**3. 初始化（OC）** — `AppDelegate.m`：

```objc
- (BOOL)application:(UIApplication *)application
  didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    // release 上线时启用备案域名，必须在 registerWithAppKey 之前
    // [Bmob resetDomain:@"https://你的备案域名"];
    [Bmob registerWithAppKey:@"你的Application ID"];
    return YES;
}
```

**3. 初始化（Swift / SwiftUI）** — `AppApp.swift`：

```swift
@main
struct MyApp: App {
    init() {
        Bmob.register(withAppKey: "你的Application ID")
    }
    var body: some Scene { WindowGroup { ContentView() } }
}
```

**4. 域名重置（上线必做）：** 工信部要求正式上线必须用备案域名：

```swift
Bmob.resetDomain("https://sdk.yourapp.com")    // 必须在 register 前
Bmob.register(withAppKey: "...")
```

OC 端用 `[Bmob resetDomain:@"https://sdk.yourapp.com"];`。

**5. 不要硬编码 Master Key** 到 App bundle。客户端只用 Application ID（必要时配 Secret Key + 加密授权）。

## 安全清单

- [ ] **release 关闭调试输出**：测试期 `[Bmob setDebug:YES]`，上架前删掉。
- [ ] **App Transport Security（ATS）**：如果备案域名是 HTTP（不推荐），需要在 `Info.plist` 加 `NSAppTransportSecurity → NSAllowsArbitraryLoads = YES`，但 App Store 审核可能拒；尽量用 HTTPS。
- [ ] **写入的表必须配 ACL**：否则任意用户可改任意行。
- [ ] **Bridging Header 不要 commit 真实 AppKey**：用配置文件 / xcconfig / environment 注入。
- [ ] **release 前替换备案域名**：参见上面"4. 域名重置"。

## 常见问题

跨平台 Q&A：[`shared/faq.md`](../../shared/faq.md)。

## 反模式

见 [`shared/anti-patterns.md`](../../shared/anti-patterns.md)。本端重点：勿 commit 真实 AppKey；ATS 尽量 HTTPS。

## 单条 CRUD（Swift 现代写法）

### 添加

```swift
let gameScore = BmobObject(className: "GameScore")
gameScore.setObject("John Smith", forKey: "playerName")
gameScore.setObject(90, forKey: "score")
gameScore.setObject(false, forKey: "cheatMode")
gameScore.saveInBackground { (isSuccessful, error) in
    if let error = error {
        print("保存失败: \(error.localizedDescription)")
    } else {
        print("保存成功: \(gameScore.objectId ?? "")")
    }
}
```

### 查询单条

```swift
let bquery = BmobQuery(className: "GameScore")
bquery.getObjectInBackground(withId: "0c6db13c") { (object, error) in
    if let error = error { print(error); return }
    guard let object = object else { return }
    let playerName = object.object(forKey: "playerName") as? String
    let score = object.object(forKey: "score") as? NSNumber
    print(playerName ?? "", score ?? 0)
}
```

### 更新（按 objectId）

```swift
let gameScore = BmobObject(outDatatWithClassName: "GameScore", objectId: "0c6db13c")
gameScore.setObject(91, forKey: "score")
gameScore.updateInBackground { (isSuccessful, error) in
    if let error = error { print(error) }
}
```

> 注意 API 名称是 `outDatatWithClassName`（拼写历史遗留，不要改）——用这个方法获取的 `BmobObject` 不会先发 GET 查询，直接拿来 update / delete。

### 删除

```swift
let gameScore = BmobObject(outDatatWithClassName: "GameScore", objectId: "0c6db13c")
gameScore.deleteInBackground { (isSuccessful, error) in /* ... */ }
```

### 查询列表（带条件 + 排序 + 分页）

```swift
let query = BmobQuery(className: "GameScore")
query.whereKey("score", greaterThan: 100)
query.orderByDescending("createdAt")
query.limit = 20
query.skip = 0
query.findObjectsInBackground { (array, error) in
    guard let results = array as? [BmobObject] else { return }
    for obj in results {
        print(obj.objectId ?? "", obj.object(forKey: "playerName") ?? "")
    }
}
```

## 单条 CRUD（Objective-C）

```objc
// 添加
BmobObject *gameScore = [BmobObject objectWithClassName:@"GameScore"];
[gameScore setObject:@"小明" forKey:@"playerName"];
[gameScore setObject:@78 forKey:@"score"];
[gameScore setObject:[NSNumber numberWithBool:YES] forKey:@"cheatMode"];
[gameScore saveInBackgroundWithResultBlock:^(BOOL isSuccessful, NSError *error) {
    // ...
}];

// 查询单条
BmobQuery *bquery = [BmobQuery queryWithClassName:@"GameScore"];
[bquery getObjectInBackgroundWithId:@"0c6db13c"
                              block:^(BmobObject *object, NSError *error) {
    if (object) {
        NSString *playerName = [object objectForKey:@"playerName"];
        BOOL cheat = [[object objectForKey:@"cheatMode"] boolValue];
        NSLog(@"%@ %d", playerName, cheat);
    }
}];

// 更新（不预先 GET，直接构造 + objectId）
BmobObject *gs = [BmobObject objectWithoutDatatWithClassName:@"GameScore" objectId:@"0c6db13c"];
[gs setObject:@91 forKey:@"score"];
[gs updateInBackground];

// 删除
BmobObject *gs = [BmobObject objectWithoutDatatWithClassName:@"GameScore" objectId:@"0c6db13c"];
[gs deleteInBackground];
```

## 与 MCP 联动

如已配置 [Bmob MCP](../bmob-mcp/SKILL.md)，先 `get_project_tables` 拿真实 schema，避免：

- 字段名拼错（`setObject:forKey:` 不校验 schema）
- BmobObject 与 BmobUser 混用

## 排错速查

跨平台现象先查 [`shared/faq.md`](../../shared/faq.md)。

| 现象 | 排查 |
|---|---|
| 100 报错 | 请求内容（查询条件）有误 |
| 20003 none objectid | 更新 / 删除 / 查询单条没传 objectId |
| 20004 none object | 查询结果为空 |
| 20006 cloud function failed | 云函数执行报错 |
| 20017 init not finish | 在 `register` 完成前调用了 SDK；检查 `init {}` 顺序 |
| Swift "use of undeclared identifier 'BmobObject'" | Bridging Header 没建或没 `#import <BmobSDK/Bmob.h>` |
| Xcode 14+ 找不到 Pod 库 | 打开了 `.xcodeproj` 而不是 `.xcworkspace` |
| App Store 审核拒 ATS | 备案域名换 HTTPS，移除 `NSAllowsArbitraryLoads` |
| release 包请求被拒 / 403 | 没配 SDK 类型备案域名；或 `resetDomain` 调用顺序错（必须在 `register` 前） |
| 9015 | 兜底错误码，必读响应描述 |

## 进阶能力（按需读 references/）

| 主题 | 路径 |
|---|---|
| 端到端场景 | [`shared/recipes/`](../../shared/recipes/) |
| BmobDocs 同步代码片段 | [`references/snippets/`](references/snippets/) |
| 完整安装 + Bridging + framework 链接 + ATS 配置 | [`references/install.md`](references/install.md) |
| 高级查询（or / 子查询 / 地理位置 / include） | [`references/query.md`](references/query.md) |
| Pointer / Relation | [`references/pointer-and-relation.md`](references/pointer-and-relation.md) |
| 用户系统 / SMS / 第三方登录 | （P1: `bmob-auth-ios`） |
| 文件上传 / BmobFile | （P1: `bmob-storage-ios`） |

## 参考

- OC 完整 API：[develop_doc.md](https://github.com/bmob/BmobDocs/blob/master/mds/data/ios/develop_doc.md)
- Swift 完整 API：[swift_develop_doc.md](https://github.com/bmob/BmobDocs/blob/master/mds/data/ios/swift_develop_doc.md)
- Swift Quickstart：[swift_quick_start.md](https://github.com/bmob/BmobDocs/blob/master/mds/data/ios/swift_quick_start.md)
- SDK 源码：<https://github.com/bmob/Bmob-iOS-SDK>
- Swift Demo：<https://github.com/bmob/bmob-ios-demo/blob/master/SwiftDemo.zip>
- 错误码：[`bmob-error-codes`](../bmob-error-codes/SKILL.md)
- MCP 联动：[`bmob-mcp`](../bmob-mcp/SKILL.md)
