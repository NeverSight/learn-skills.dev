---
name: ios-base
description: iOS/Swift 核心开发技能。当编写或修改 Swift/SwiftUI/UIKit 代码、设计 UI 架构、优化性能、创建组件、处理导航时使用。覆盖 Swift 编码规范、SwiftUI 最佳实践、UIKit 开发、导航架构（Coordinator/NavigationStack）、动画、组件设计、性能优化。
---

# iOS/Swift 核心开发

## Swift 编码规范

### 命名规则
- 类型名 UpperCamelCase: `class NetworkManager`, `struct UserProfile`
- 变量/函数 lowerCamelCase: `var isLoading`, `func fetchUser()`
- Bool 属性用 `is`/`has`/`should`/`can` 前缀: `isEnabled`, `hasPermission`
- Protocol 描述能力用 `-able`/`-ing`: `Codable`, `DataProviding`；描述角色用名词: `Delegate`
- 缩写: 首位全小写 `urlString`；非首位两字母全大写 `userID`，三字母以上首字母大写 `userUrl`

### 类型选择
- **默认用 struct**，需要引用语义/继承/deinit/ObjC 互操作才用 class
- 穷举状态用 enum + associated value: `case loaded(Data)`, `case failed(Error)`
- 常量命名空间用无 case 的 enum: `enum Constants { static let timeout = 30.0 }`

### 访问控制
- 默认最严格: `private` > `fileprivate` > `internal` > `public` > `open`
- 对外 API 显式标注 `public`
- ViewModel 的 `@Published` 属性用 `private(set)`
- SwiftUI 的 `@State` 必须标记为 `private`

### 错误处理
- 定义领域错误 enum 遵循 `LocalizedError`，实现 `errorDescription`
- 用 `throws` 传播错误，避免静默失败
- 禁止生产代码中 `try!`/`as!`/`!`，除非有绝对安全理由并写注释

### 并发 (async/await)
- 优先 async/await 而非回调或 Combine
- 并行独立任务用 `async let`
- UI 更新必须在 `@MainActor`
- 简单共享状态保持单一写入源；复杂隔离策略交由 `swift-expert`
- ViewModel 类标注 `@MainActor`
- SwiftUI View 中用 `.task` 启动异步任务，自动取消

### 闭包
- 始终用 `[weak self]`，然后 `guard let self else { return }`
- 确定被引用对象生命周期更长才用 `[unowned self]`

### 代码组织
- 用 `// MARK: - Section` 分区
- Protocol 实现放 extension
- 函数不超过 40 行，文件不超过 400 行
- 用 `guard` 提前返回，最多 3 层缩进
- SwiftUI View body 不超过 40 行，复杂部分提取为 computed property 或子 View

### 注释
- 公开 API 用 `///` 文档注释，含参数/返回值/异常说明
- 注释解释 **why**，代码本身解释 **what**
- 删除被注释掉的代码

## 项目结构

### 默认目录布局
```
App/                    → AppDelegate, SceneDelegate, 启动配置
Core/                   → 基础设施 (Network, Storage, Extensions, Utilities)
Features/<FeatureName>/ → 功能模块 (Views, ViewModels, Models, Services)
UI/Components/          → 可复用 UI 组件
Resources/              → Assets, Localizable, Info.plist
```

### 架构选择
- SwiftUI 默认: View + ViewModel (@Observable) + Model + Service
- UIKit 默认: MVVM + Coordinator（中型以上项目）
- 复杂 SDK/大型项目用 Clean Architecture: Domain → Data → Presentation

### 依赖注入
- 通过 init 注入，不直接引用单例
- 定义 Protocol 抽象，注入协议类型
- SwiftUI 用 `@Environment` 或 custom EnvironmentKey
- UIKit 通过 Coordinator 或 init 注入

### 模块化
- 用 SPM 拆分本地模块
- Core 模块零外部依赖
- Feature 模块依赖 Core，不互相依赖
- 每个模块有独立 Tests target

### 文件规则
- 一文件一主类型，文件名与类型名一致
- Extension 文件: `String+Validation.swift`
- 测试文件: `UserServiceTests.swift`

## SwiftUI 核心规则

### 状态管理
- **优先 `@Observable` 而非 `ObservableObject`**（iOS 17+）
- `@State` 必须标记 `private`，用于 View 拥有的状态
- `@State` + `@Observable` class 替代 `@StateObject`
- `@Binding` 仅用于子视图需要**修改**父状态
- `@Bindable` 用于注入的 `@Observable` 对象需要绑定时
- 只读值用 `let`，不要用 `@State` 或 `@Binding`
- `@Observable` 类必须标注 `@MainActor`

### 现代 API（必须使用）
- `foregroundStyle()` 而非 `foregroundColor()`
- `clipShape(.rect(cornerRadius:))` 而非 `cornerRadius()`
- `NavigationStack` 而非 `NavigationView`
- `navigationDestination(for:)` 实现类型安全导航
- `Tab` API（iOS 18+）而非 `tabItem()`
- `.onChange(of:) { old, new in }` 双参数版本
- `.task` 而非 `.onAppear` 启动异步任务
- `Button` 而非 `onTapGesture`（除非需要位置/次数）

### 性能优化
- 只传递 View 需要的具体值，避免传整个大对象
- 避免热路径中的冗余状态更新（检查值变化再赋值）
- ForEach 必须用稳定 ID，禁止 `.indices`（动态内容）
- 大列表用 `LazyVStack`/`LazyHStack`
- 避免在 ForEach 中内联过滤，预先过滤并缓存
- View body 保持纯净，无副作用或复杂逻辑
- 复杂性能剖析（热路径量化、复制开销建模）交由 `swift-expert`

### 动画
- 用 `.animation(_:value:)` 而非已废弃的 `.animation(_:)`
- 按钮点击用 `withAnimation`
- 动画修饰符放在被动画属性之后
- 过渡用 `.transition()` + `withAnimation`

## UIKit 核心规则

### ViewController 结构
按顺序组织：Properties → UI Components → Lifecycle → Setup → Methods → Actions → Protocol Extensions

### 布局
- 优先 SnapKit（如可用）或 `NSLayoutConstraint.activate([])`
- 优先 `UIStackView` 减少约束
- 复杂列表用 `UICollectionViewCompositionalLayout` + `DiffableDataSource`

### 内存管理
- Delegate 必须 `weak`
- 闭包捕获 `[weak self]`
- Timer/观察者在 deinit 中清理

## 专项参考

深入学习特定主题时，查阅以下详细指南：

- **[SwiftUI 开发](references/swiftui.md)** - 状态管理、现代 API、列表性能、动画、布局最佳实践
- **[UIKit 开发](references/uikit.md)** - ViewController 结构、布局、Cell 复用、自定义控件
- **[导航架构](references/navigation.md)** - Coordinator Pattern（UIKit）、NavigationStack + Router（SwiftUI）、深度链接
- **[动画系统](references/animations.md)** - SwiftUI 动画（隐式/显式/过渡）、UIKit 动画、性能优化
- **[性能优化](references/performance.md)** - SwiftUI 热路径优化、UIKit 视图层级优化、内存管理
- **[组件设计](references/component-design.md)** - 自定义组件、可配置 API、可复用模式
- **[内存管理](references/memory-management.md)** - 循环引用、泄漏预防、weak/unowned 使用

## 与其他技能的关系

- 默认 iOS 业务开发优先使用本技能
- 当任务进入以下任一场景时切换 `swift-expert`：
	- 需要协议导向深度抽象（PAT、类型擦除、复杂泛型约束）
	- 需要并发隔离设计（`Sendable`、actor 边界、重入与取消策略）
	- 需要基于可观测数据的深入性能与内存剖析
	- 需要跨平台（iOS/macOS/watchOS/tvOS）可用性差异设计

## ✅ Sentinel（Skill 使用自检）
当且仅当你确定本 Skill 已被加载并用于当前任务时，在回复末尾追加：
`// skill-used: ios-base`

规则：
- 只能输出一次
- 如果不确定是否加载，禁止输出 sentinel
- 输出 sentinel 代表你已遵守本 Skill 的硬性规则与交付格式
- 只有当任务与本 skill 的 description 明显匹配时才允许输出 sentinel