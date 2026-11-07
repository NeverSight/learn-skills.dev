---
name: rust-safety
description: 写 Rust 时使用。所有权、错误处理、unsafe 的正确实践。
category: language
tags: [rust, 所有权, 安全]
---

# Rust 安全实践

## 何时用

- 写新的 Rust 函数、结构体或模块时。
- 设计数据结构，思考所有权与生命周期时。
- 处理错误传播、编写库 crate 时。
- 准备写 `unsafe` 块或评估是否真的需要 `unsafe` 时。
- 发现编译器报 borrow checker 错误，想靠 `clone`/`Rc` 强行绕过时。

## 核心规则

### 1. 顺着所有权/借用设计，不靠 `clone`/`Rc` 硬绕；理解生命周期

**规则：** 遇到借用检查报错时，先理解所有权模型要表达的约束，调整数据流或函数签名；只有在语义上确实需要共享所有权时才用 `Rc`/`Arc`，不把它们当"绕过编译器的万金油"；`clone` 有性能代价，大结构体不随意 `clone`。

**为什么：** AI 面对 borrow checker 报错时最常见的反应是加 `.clone()` 或把类型换成 `Rc<RefCell<T>>`——这能让代码编译，但往往意味着绕开了编译器在帮你捕获的真实问题：可能是数据所有权设计不合理，可能是生命周期标注缺失。用 `RefCell` 把静态借用检查变成运行时 panic，在 Rust 里是倒退，不是进步。

**怎么做：**
- 报 borrow 错误 → 先读错误信息，理解哪个变量的生命周期冲突，考虑重组代码顺序或拆分函数。
- 函数返回引用 → 正确标注生命周期参数，让编译器而非运行时来保证安全。
- 确实需要多所有者 → `Arc<T>`（多线程）或 `Rc<T>`（单线程），但要在注释里说明为何需要共享所有权。

---

### 2. 错误用 `Result` + `?`，库代码不 `unwrap`/`panic`；用 `thiserror`/`anyhow` 分场景

**规则：** 可能失败的操作返回 `Result<T, E>`，通过 `?` 传播；库 crate 的公开 API 中不使用 `unwrap()`/`expect()`/`panic!()`（调用方无法捕获 panic）；应用程序层用 `anyhow` 简化错误汇聚，库层用 `thiserror` 定义具体错误类型。

**为什么：** AI 写 Rust 时的典型懒惰：`let val = map.get("key").unwrap()`，在 happy path 下工作，一旦 key 不存在就 unwind panic，且调用方无法在类型层面知道这里会 panic。库的职责是把所有可能的失败都表达在类型里，让调用方决定怎么处理，而不是替调用方决定"遇到这种情况就崩溃"。

**怎么做：**
- 库 crate：`#[derive(thiserror::Error)]` 定义枚举错误类型，每个变体对应一种具体失败场景。
- 应用 crate / 原型：`anyhow::Result<T>` + `?` 快速传播，`context()`/`with_context()` 添加现场信息。
- 确实不可能失败的 `unwrap` → 改写成 `expect("此处 key 在初始化时已保证存在")` 并写明原因，或用 `unreachable!` 配合注释。

---

### 3. `unsafe` 最小化并注释不变量；能安全抽象就封装

**规则：** `unsafe` 块应尽可能小，仅包含无法用安全 API 表达的操作；每个 `unsafe` 块旁必须有注释，说明为何此处安全（维护的不变量是什么）；能把 `unsafe` 封装进一个安全的函数/结构体，就不要让 `unsafe` 泄漏到上层调用方。

**为什么：** AI 倾向于在遇到生命周期或类型系统挑战时直接用 `unsafe` 强行转换（如 `std::mem::transmute`），注释一句"// 应该没问题"就提交了。这类代码的危险性在于它能编译、能通过测试，但在某个边界条件下触发未定义行为，且 Miri / sanitizer 很难覆盖到所有路径。

**怎么做：**
- 写 `unsafe` 前先问：有没有 `std`/`bytemuck`/`zerocopy` 等安全 crate 能做这件事？
- 写了 `unsafe` → 注释格式：`// SAFETY: [解释为何此处满足 XX 的不变量，即...]`。
- 用 `miri`（`cargo miri test`）定期跑，检测未定义行为；CI 里加 `cargo test --sanitize=address`。

---

### 4. 用类型表达约束（枚举状态机、newtype），让非法状态不可表示

**规则：** 把业务约束编码进类型系统：用枚举而非字符串/整数常量表示状态；用 newtype 模式区分语义不同的同类型值；避免用 `bool` 参数区分行为——该拆成两个函数。

**为什么：** AI 常写出 `fn send_email(address: String, verified: bool)`，然后所有调用方都要记住"第二个参数是是否验证过"，极容易传反。更好的设计是 `fn send_email(address: VerifiedEmail)`——传入未验证的 `String` 在编译时就报错，根本不存在运行时检查的必要。这是 Rust 类型系统最强大的能力，AI 却经常忽视。

**怎么做：**
- 状态流转 → 枚举 + `impl` 方法，非法状态转换不提供方法（类型状态机模式）。
- 同类型但语义不同的值（用户 ID vs 文章 ID，都是 `u64`）→ `struct UserId(u64); struct PostId(u64);`，杜绝混用。
- 函数有多个同类型参数 → 考虑 builder 模式或命名结构体，降低参数传反的风险。

---

### 5. 善用 `Option`/迭代器组合子；遵循 `clippy` 建议

**规则：** 处理 `Option`/`Result` 优先使用 `map`、`and_then`、`unwrap_or_else`、`ok_or` 等组合子，而非嵌套 `match`；所有代码通过 `cargo clippy -- -D warnings`（警告即错误）；`cargo fmt` 格式化。

**为什么：** AI 写 `Option` 处理时常退化成多层嵌套 `match`：`match x { Some(v) => match v.get(...) { Some(r) => ..., None => ... }, None => ... }`。这与 Rust 的迭代器哲学背道而驰，且可读性极差。`clippy` 中有数百条来自社区经验的建议，很多直接指出安全隐患（如使用了 `ptr::null()` 而非 `ptr::null_mut()`），忽视 clippy 等于放弃了免费的代码审查。

**怎么做：**
- `Option<T>` 链式变换 → `opt.map(|v| ...).unwrap_or_default()`。
- 处理集合 → 用迭代器链（`.filter().map().collect()`），避免显式 `for` + `push`。
- CI 中：`cargo clippy -- -D warnings && cargo fmt --check`，有报警就失败。

---

## 正例 / 反例

### 反例：靠 `clone` 绕过借用 + 库代码 `unwrap`

```rust
// 反例 — clone 掩盖设计问题，库函数直接 unwrap
use std::collections::HashMap;

pub fn get_display_name(users: &HashMap<u64, String>, id: u64) -> String {
    let users_clone = users.clone();          // ❌ 为了"方便"克隆整个 map
    users_clone.get(&id).unwrap().clone()     // ❌ 库代码 unwrap，调用方无法处理缺失
}
```

```rust
// 正例 — 零克隆借用，错误用 Result 表达
use std::collections::HashMap;

#[derive(Debug, thiserror::Error)]
pub enum UserError {
    #[error("用户 {0} 不存在")]
    NotFound(u64),
}

pub fn get_display_name(
    users: &HashMap<u64, String>,
    id: u64,
) -> Result<&str, UserError> {
    users
        .get(&id)
        .map(String::as_str)
        .ok_or(UserError::NotFound(id))   // ✅ 调用方决定如何处理缺失
}
```

---

### 反例：`bool` 参数 + 裸字符串状态

```rust
// 反例 — bool 参数语义模糊，字符串状态无法穷举
fn process_order(order_id: u64, is_priority: bool, status: &str) {
    if status == "pendign" { ... }   // ❌ 拼写错误，编译器不报
}

process_order(42, true, "pending");  // ❌ true 是什么意思？
```

```rust
// 正例 — 枚举穷举状态，newtype 明确语义
#[derive(Debug)]
enum OrderStatus { Pending, Processing, Shipped, Cancelled }

struct OrderId(u64);  // ✅ newtype，不会和其他 u64 混淆

fn process_order(id: OrderId, priority: Priority, status: OrderStatus) {
    match status {
        OrderStatus::Pending => { ... }
        OrderStatus::Processing => { ... }
        // 编译器强制穷举 ✅
    }
}
```

---

## 自查清单

- [ ] 遇到 borrow checker 报错，是否先理解根因，而不是立刻加 `.clone()` 或 `Rc`？
- [ ] 库 crate 的公开函数中是否有 `unwrap()`/`expect()` 调用？（应该没有）
- [ ] 每个 `unsafe` 块旁是否有 `// SAFETY:` 注释，说明维护的不变量？
- [ ] 是否用枚举/newtype 把业务约束编码进类型，让非法状态在编译时就不可表示？
- [ ] `Option`/`Result` 处理是否用组合子，而非多层嵌套 `match`？
- [ ] `cargo clippy -- -D warnings` 和 `cargo fmt --check` 全部通过？
- [ ] `unsafe` 代码是否已用 `cargo miri test` 验证过？
