---
name: view_model
description: Guide for building and using ViewModels with reference-counted lifecycle and reactive binding in Flutter.
mintlify-proj: flutter-view-model
---

# view_model Skill

This skill provides comprehensive instructions for using the `view_model` state management library in Flutter. It focuses on architecture, reactivity, and lifecycle management.

## 核心设计哲学 (Core Philosophy)

`view_model` 是一个基于 **类型键 (Type-keyed)** 和 **引用计数 (Reference Counting)** 的状态管理系统.
- **自动生命周期**: ViewModel 的存活取决于是否有活跃的 Binding。
- **跨 Context 自由**: 在任何混入了 `ViewModelBinding` 的类中都可以访问 ViewModel，无需 `BuildContext`。
- **高性能**: 自动处理 暂停/恢复 逻辑，不可见时不刷新。

## 1. 核心 Mixins

### `with ViewModel`
用于定义受管实例。
- 提供 `onCreate`, `onBind`, `onUnbind`, `onDispose` 钩子。
- 使用 `notifyListeners()` 或 `update(() => ...)` 触发通知。
- 可通过 `viewModelBinding` 访问其他依赖。
- 使用 `addDispose(callback)` 注册清理逻辑。

### `with ViewModelBinding`
用于访问 ViewModels (Binding Host)。
- 在 Widget 中通常使用 `ViewModelStateMixin` 或 `ViewModelStatelessMixin`。
- 提供 `viewModelBinding.watch()` (响应式) 和 `viewModelBinding.read()` (非响应式)。

## 2. 定义 ViewModelSpec

`ViewModelSpec` 是 ViewModel 的工厂定义。

```dart
// 1. 无参数，单例共享
final authSpec = ViewModelSpec<AuthViewModel>(
  builder: () => AuthViewModel(),
  key: 'global_auth',
  aliveForever: true, // 全局常驻
);

// 2. 带参数，按需创建
final userSpec = ViewModelSpec.arg<UserViewModel, String>(
  builder: (id) => UserViewModel(id),
  key: (id) => 'user-$id', // 相同 ID 共享同一实例
);
```

## 3. Widget 集成

### 在 StatefulWidget 中
```dart
class MyPage extends StatefulWidget { ... }

class _MyPageState extends State<MyPage> with ViewModelStateMixin {
  late final vm = viewModelBinding.watch(counterSpec);

  @override
  Widget build(BuildContext context) {
    return Text(vm.count.toString());
  }
}
```

### 在 StatelessWidget 中
```dart
class MyWidget extends StatelessWidget with ViewModelStatelessMixin {
  late final vm = viewModelBinding.watch(counterSpec);
  
  @override
  Widget build(BuildContext context) => Text(vm.count.toString());
}
```

## 4. viewModelBinding 常用接口

| 方法 | 说明 |
| :--- | :--- |
| `watch(spec)` | 创建/获取并监听。UI 随通知刷新。 |
| `read(spec)` | 创建/获取但不监听。常用于事件回调。 |
| `watchCached<T>(key: ...)` | 寻找已存在的实例并监听。若无则报错。 |
| `readCached<T>(key: ...)` | 寻找已存在的实例但不监听。 |
| `listenState(spec, onChanged: ...)` | 监听 StateViewModel 的完整状态变化。 |
| `listenStateSelect(spec, selector: ..., onChanged: ...)` | 针对性地监听某个字段。 |
| `recycle(vm)` | 强制销毁实例，解绑所有连接。 |

## 5. 状态管理进阶

### `StateViewModel<T>`
用于不可变状态。
```dart
class CounterViewModel extends StateViewModel<CounterState> {
  CounterViewModel() : super(state: const CounterState());
  
  void inc() => setState(state.copyWith(count: state.count + 1));
}
```

### 细粒度更新
使用 `StateViewModelValueWatcher` 只在特定字段变化时 rebuild。

## 6. 暂停/恢复 (Pause / Resume)

为了让自动暂停生效，必须在 `MaterialApp` 中注册 `ViewModel.routeObserver`。

```dart
MaterialApp(
  navigatorObservers: [ViewModel.routeObserver],
  ...
)
```

## 7. 自动测试 (Testing)

`view_model` 使单元测试变得非常简单，因为它不强依赖于 `BuildContext`。

```dart
test('counter increments', () {
  final binding = ViewModelBinding(); // 创建测试用的 Binding
  final vm = binding.watch(counterSpec);

  expect(vm.count, 0);
  vm.increment();
  expect(vm.count, 1);

  binding.dispose(); // 销毁并解绑
});
```

## 8. 代码生成 (Code Generation)

使用 `@GenSpec` 可以自动生成 `ViewModelSpec` 代码，减少样板代码。

```dart
@GenSpec()
class CounterViewModel with ViewModel { ... }
```

生成的文件将包含 `counterViewModelSpec`。

## 9. 最佳实践

1. **依赖注入**: 在 ViewModel 内部直接使用 `viewModelBinding.read(otherSpec)` 获取依赖。
2. **清理**: 永远优先使用 `addDispose()` 注册清理回调，而非手动覆写 `dispose()`。
3. **单例**: 对全局状态（如 Auth, Config）使用 `aliveForever: true`。
4. **性能**: 在 `ListView` 的 Item 中，如果只是为了获取数据而不期望整个 Item 随全局状态刷新，优先使用 `read`。
5. **代码生成**: 配合 `view_model_annotation` 和 `view_model_generator` 使用 `@GenSpec` 减少样板代码。
