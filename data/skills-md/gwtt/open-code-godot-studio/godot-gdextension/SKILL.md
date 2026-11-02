---
name: godot-gdextension
description: GDExtension specialist for C++/Rust native bindings, custom nodes, high-performance modules, and native code integration with Godot 4.
license: MIT
---

# GDExtension Specialist Skill

This skill provides expert guidance for creating native extensions in Godot 4 using C++, Rust, or other languages via GDExtension.

## Purpose

Use this skill when:
- Implementing performance-critical code (>1000 calls/frame)
- Creating custom native nodes or resources
- Integrating existing C++/Rust libraries
- Building specialized systems (pathfinding, physics queries, procedural generation)
- Setting up GDExtension build systems

## GDExtension Overview

GDExtension allows:
- Native performance without modifying engine source
- Custom nodes, resources, and editor plugins
- C++, Rust, Swift, and other language bindings
- Hot-reloading during development (C++ only on some platforms)

## When to Use GDExtension

| Use GDScript | Use GDExtension |
|--------------|-----------------|
| Game logic, state | Heavy math (physics, pathfinding) |
| UI, scene management | Procedural generation |
| Standard gameplay | >1000 calls/frame operations |
| Prototyping | Native library integration |
| Most game code | Custom rendering pipelines |

## Project Structure

```
project/
├── src/                    # GDScript source
├── native/                 # GDExtension source
│   ├── include/            # Header files
│   ├── src/                # Implementation
│   ├── SConstruct          # SCons build script
│   └── .gdextension        # Extension config
└── addons/
    └── my_extension/       # Compiled extension
        ├── bin/
        │   ├── my_extension.dll   # Windows
        │   ├── my_extension.so    # Linux
        │   └── my_extension.dylib # macOS
        └── my_extension.gdextension
```

## .gdextension Configuration

```ini
[configuration]

entry_symbol = "my_extension_library_init"
compatibility_minimum = "4.2"

[libraries]

windows.debug.x86_64 = "res://addons/my_extension/bin/my_extension.dll"
windows.release.x86_64 = "res://addons/my_extension/bin/my_extension.dll"
linux.debug.x86_64 = "res://addons/my_extension/bin/my_extension.so"
linux.release.x86_64 = "res://addons/my_extension/bin/my_extension.so"
macos.debug = "res://addons/my_extension/bin/my_extension.dylib"
macos.release = "res://addons/my_extension/bin/my_extension.dylib"
```

## C++ GDExtension Example

### Header (include/my_node.hpp)

```cpp
#ifndef MY_NODE_HPP
#define MY_NODE_HPP

#include <godot_cpp/classes/node.hpp>
#include <godot_cpp/core/class_db.hpp>

namespace my_extension {

class MyNode : public godot::Node {
    GDCLASS(MyNode, godot::Node)

private:
    double custom_value;

protected:
    static void _bind_methods();

public:
    MyNode();
    ~MyNode();

    void _process(double delta) override;

    void set_custom_value(double value);
    double get_custom_value() const;
};

} // namespace my_extension

#endif // MY_NODE_HPP
```

### Implementation (src/my_node.cpp)

```cpp
#include "my_node.hpp"

namespace my_extension {

void MyNode::_bind_methods() {
    godot::ClassDB::bind_method(godot::D_METHOD("set_custom_value", "value"), &MyNode::set_custom_value);
    godot::ClassDB::bind_method(godot::D_METHOD("get_custom_value"), &MyNode::get_custom_value);

    ADD_PROPERTY(godot::PropertyInfo(godot::Variant::FLOAT, "custom_value"), "set_custom_value", "get_custom_value");
}

MyNode::MyNode() : custom_value(0.0) {}
MyNode::~MyNode() {}

void MyNode::_process(double delta) {
    // High-performance processing here
}

void MyNode::set_custom_value(double value) {
    custom_value = value;
}

double MyNode::get_custom_value() const {
    return custom_value;
}

} // namespace my_extension
```

### Registration (src/register_types.cpp)

```cpp
#include "register_types.hpp"
#include "my_node.hpp"

#include <godot_cpp/core/class_db.hpp>
#include <godot_cpp/core/defs.hpp>
#include <godot_cpp/godot.hpp>

namespace my_extension {

void initialize_my_extension_module(godot::ModuleInitializationLevel p_level) {
    if (p_level != godot::MODULE_INITIALIZATION_LEVEL_SCENE) {
        return;
    }

    godot::ClassDB::register_class<MyNode>();
}

void uninitialize_my_extension_module(godot::ModuleInitializationLevel p_level) {
    if (p_level != godot::MODULE_INITIALIZATION_LEVEL_SCENE) {
        return;
    }
}

} // namespace my_extension

extern "C" {
GDExtensionBool GDE_EXPORT my_extension_library_init(
    GDExtensionInterfaceGetProcAddress p_get_proc_address,
    GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
) {
    godot::GDExtensionBinding::InitObject init_obj(p_get_proc_address, p_library, r_initialization);

    init_obj.register_initializer(initialize_my_extension_module);
    init_obj.register_uninitializer(uninitialize_my_extension_module);
    init_obj.set_minimum_library_initialization_level(godot::MODULE_INITIALIZATION_LEVEL_SCENE);

    return init_obj.init();
}
}
```

## Rust GDExtension (godot-rust)

### Cargo.toml

```toml
[package]
name = "my_godot_extension"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
godot = { git = "https://github.com/godot-rust/gdext" }

[profile.release]
opt-level = 3
lto = "thin"
```

### Rust 完整示例

```rust
use godot::prelude::*;

#[derive(GodotClass)]
#[class(base=Node3D)]
struct TerrainGenerator {
    base: Base<Node3D>,
    
    #[export]
    chunk_size: i32,
    
    #[export]
    seed: i64,
}

#[godot_api]
impl INode3D for TerrainGenerator {
    fn init(base: Base<Node3D>) -> Self {
        Self { 
            base, 
            chunk_size: 64, 
            seed: 0 
        }
    }

    fn ready(&mut self) {
        godot_print!("TerrainGenerator ready");
    }
}

#[godot_api]
impl TerrainGenerator {
    #[func]
    fn generate_chunk(&self, x: i32, z: i32) -> Dictionary {
        // Rust 中执行重计算
        let mut result = Dictionary::new();
        // ... 大量计算 ...
        result
    }
}
```

### Rust 性能优势

- **rayon** — 并行迭代（程序化生成、批处理）
- **nalgebra / glam** — 优化数学运算
- **零成本抽象** — 迭代器、泛型编译为最优代码
- **无 GC 停顿** — 内存安全但无垃圾回收

---

## ⚠️ ABI 兼容性警告

**关键**: GDExtension 二进制文件在 Godot 次版本之间**不兼容**：

- 为 Godot 4.3 编译的 `.gdextension` **无法**在 Godot 4.4 中运行
- 升级 Godot 版本时**必须重新编译**扩展
- `.gdextension` 文件中的 `compatibility_minimum` 必须匹配项目目标版本

**在建议任何 GDExtension 模式前**：
1. 读取 `docs/engine-reference/godot/VERSION.md` 确认引擎版本
2. 检查 `breaking-changes.md` 了解可能影响原生绑定的变更
3. 告知用户："此扩展在 Godot 版本变更后需要重新编译。次版本之间不保证 ABI 兼容性。"

---

## 性能模式

### SCons (C++)

```python
# SConstruct
SConscript("godot-cpp/SConstruct")

env = SConscript("godot-cpp/SConstruct")

env.Append(CPPPATH=["#include"])
env.Append(LIBPATH=["godot-cpp/bin"])

sources = Glob("src/*.cpp")

library = env.SharedLibrary(
    "bin/my_extension",
    source=sources,
    SHLIBSUFFIX=".dll"  # Adjust for platform
)
```

### Cargo (Rust)

```bash
cargo build --release
# Output in target/release/my_godot_extension.dll
```

## Performance Best Practices

### 数据导向设计

- **连续数组处理** — 不要分散的对象，使用连续内存
- **结构数组 (SoA)** — 批处理优于对象数组 (AoS)
- **最小化 Godot API 调用** — 批量数据，原生处理，返回结果
- **使用 SIMD** — 数学密集代码使用 SIMD 内置函数

### 线程安全

```cpp
// ✅ 正确 — 后台线程计算，主线程应用
std::thread worker([this]() {
    auto results = heavy_computation();
    call_deferred("apply_results", results);
});

// ❌ 错误 — 从后台线程访问场景树
std::thread worker([this]() {
    add_child(node);  // 崩溃！场景树只能在主线程操作
});
```

### C++ 性能要点

- **热路径零分配** — 预分配缓冲区
- **使用 POD 类型** — 优先用 `double` 而非 `Variant`
- **缓存 Godot 对象访问** — 不要重复查询同一节点
- **批量操作** — 一次调用处理数组
- **正确使用 `Ref<T>`** — 理解引用计数

### Rust 性能要点

- **零拷贝** — 避免不必要的克隆
- **高效使用 `godot::prelude::*`** — 只导入需要的
- **正确处理所有权** — 理解 Rust 所有权模型
- **使用原生分析工具** — Rust 性能分析器

---

## GDScript ↔ Native 边界

### 边界模式

```
GDScript 拥有: 游戏逻辑、场景管理、UI、高层协调
Native 拥有: 重计算、数据处理、性能关键热路径
接口: Native 暴露节点、资源、GDScript 可调用的函数
数据流: GDScript 调用 Native 方法 → Native 计算 → 返回结果
```

### 避免的陷阱

- ❌ 将所有代码移到 Native（过度工程 — GDScript 对大多数逻辑足够快）
- ❌ 紧密循环中频繁 Godot API 调用（每次调用有边界开销）
- ❌ 不处理热重载（扩展应能在编辑器重导入后存活）
- ❌ 平台特定代码无跨平台抽象
- ❌ 忘记注册类/方法（对 GDScript 不可见）
- ❌ 使用原始指针而非 `Ref<T>` / `Gd<T>`（生命周期问题）
- ❌ 热路径分配而非预分配缓冲区

---

## 常见错误

| 错误 | 修正 |
|------|------|
| .gdextension 中 Godot 版本不匹配 | 确保 `compatibility_minimum` 正确 |
| 缺少 `entry_symbol` 配置 | 添加入口符号配置 |
| 错误的库路径格式 | 使用平台特定路径 |
| 类未正确注册 | 使用 `ClassDB::register_class<T>()` |
| 忽略引用计数 | 理解 `Ref<T>` 和 `Gd<T>` |
| 过度使用 Variant | 优先使用类型化参数 |
| 未处理线程安全 | 使用 `call_deferred()` |