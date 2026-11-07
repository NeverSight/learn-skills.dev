---
name: design-patterns-rust
description: GoF design patterns and idiomatic Rust alternatives — Builder, Factory, Singleton, Newtype, Adapter, Decorator, Composite, Strategy, Command, Observer, State, Visitor, Typestate, RAII — plus idioms, anti-patterns, trait-vs-enum dispatch, and design principles. Use when implementing or refactoring Rust code involving design patterns or idioms.
---

# Design Patterns in Rust

Apply these patterns when designing or refactoring Rust code. Many GoF patterns translate differently in Rust due to ownership, enums, traits, and lack of inheritance. Distilled from the *Rust Design Patterns* book (rust-unofficial/patterns): **idioms** are the community's social norms — break them only with a good reason; **patterns** solve recurring problems; **anti-patterns** look helpful but cause more problems. Always favor *why* you reach for a pattern over *how* to spell it.

## IDIOMS (social norms)

Foundational habits that make Rust code idiomatic. Prefer these before reaching for a named pattern.

### Borrowed types for arguments

Take the most general borrow. Prefer `&str` over `&String`, `&[T]` over `&Vec<T>`, `&T` over `&Box<T>` — callers with either form can pass in, and you avoid a layer of indirection.

```rust
fn count_words(text: &str) -> usize { text.split_whitespace().count() } // not &String
```

### Concatenate with `format!`

For building a string from pieces, `format!` reads better than a chain of `push_str`/`+`. Use `push_str` only in a hot loop where the extra allocation matters.

```rust
let s = format!("{name} is {age} years old"); // not "..".to_string() + &name + ..
```

### The `Default` trait

Implement (or `#[derive(Default)]`) `Default` for types with a sensible zero value, then use struct-update syntax to override a few fields. Enables `T::default()` in generic code and `..Default::default()` initialization.

```rust
#[derive(Default)]
struct Config { retries: u32, verbose: bool, name: String }
let c = Config { retries: 3, ..Default::default() };
```

### `mem::take` / `mem::replace` to mutate owned values behind `&mut`

You can't move a field out of a `&mut` reference. `mem::take` (leaves `Default::default()`) and `mem::replace` (leaves a supplied value) let you take ownership without cloning — essential when transitioning enum variants in place.

```rust
fn a_to_b(e: &mut MyEnum) {
    if let MyEnum::A { name, x: 0 } = e {
        *e = MyEnum::B { name: std::mem::take(name) }; // moves name out, no clone
    }
}
```

### On-stack dynamic dispatch

Bind differently-typed values to one `&mut dyn Trait` to get dynamic dispatch without a heap allocation. Since Rust 1.79 temporaries in `&`/`&mut` live long enough, so no deferred `let` bindings needed.

```rust
let readable: &mut dyn std::io::Read =
    if arg == "-" { &mut std::io::stdin() } else { &mut std::fs::File::open(arg)? };
// read from `readable` — no Box, no monomorphization of the code that follows
```

### Temporary mutability

When data is mutated only during setup and read-only afterward, make that intent explicit by rebinding to an immutable binding (or use a nested block). The compiler then guarantees no later mutation.

```rust
let mut data = get_vec();
data.sort();
let data = data; // now immutable
```

### Iterating over `Option`

`Option<T>` is `IntoIterator` (0 or 1 element) — use it directly with `.iter()`/`.extend()`/`chain()` instead of `if let`.

```rust
let mut names = vec!["a"];
names.extend(maybe_name.as_ref()); // pushes 0 or 1 item
```

### Return the consumed argument on error

If a fallible function moves an argument, hand it back inside the error so the caller can retry without cloning up front. The std library does this (`String::from_utf8` → `FromUtf8Error::into_bytes`).

```rust
pub struct SendError(String);
pub fn send(value: String) -> Result<(), SendError> {
    if ready() { Ok(()) } else { Err(SendError(value)) } // caller recovers `value`
}
```

### Pass selected variables into a closure

Closures capture the whole environment by borrow, or everything by `move`. To move/clone/borrow *specific* variables, rebind them in an enclosing block before the `move` closure.

```rust
let closure = {
    let num2 = num2.clone();   // cloned
    let num3 = num3.as_ref();  // borrowed
    move || *num1 + *num2 + *num3 // num1 moved
};
```

### `#[non_exhaustive]` for future-proof public types

Mark public structs/enums/variants `#[non_exhaustive]` so downstream crates can't exhaustively match or struct-literal them — letting you add fields/variants later without a breaking change. Costs ergonomics (forces a wildcard arm), so reserve for genuinely evolving APIs.

## GOF & RUST-SPECIFIC PATTERNS — DECISION GUIDE

Full per-pattern code examples live in `references/` — read a category's file only when you need the implementation details. What follows is each pattern's intent and the idiomatic Rust mechanism that replaces the classic OOP formulation.

### Creational patterns — full code in `references/creational.md`

- **Builder** — construct complex structs step-by-step via chained methods. Consuming (`self`) builders are idiomatic and prevent reuse bugs via move semantics; non-consuming (`&mut self`) allows reconfiguration but requires `.clone()` in `build()`.
- **Factory** — encapsulate creation behind an interface: a plain function + `match` returning `Box<dyn Trait>` (dynamic dispatch) or generics (static dispatch, zero cost). No abstract factory class hierarchy needed.
- **Singleton** — single global instance via `LazyLock` (initialized on first access, Rust >= 1.80) or `OnceLock` (set explicitly, get later); wrap mutable state in `Mutex`/`RwLock` since a `static` requires `Sync`. Use sparingly — prefer dependency injection.

### Structural patterns — full code in `references/structural.md`

- **Newtype** — tuple struct `struct X(T)` for distinct semantics, type safety, and the orphan-rule workaround; zero-cost at runtime (`#[repr(transparent)]`).
- **Adapter** — make incompatible interfaces work together: implement your trait on a wrapper struct holding the adaptee.
- **Decorator** — add behavior by wrapping (stackable): generic `W<T: Trait>` for static zero-cost dispatch (real-world: `BufReader<R: Read>`), or `Box<dyn Trait>` for dynamic stacking.
- **Facade** — one struct with simple methods orchestrating subsystems; Rust modules also serve as natural facades via `pub` visibility.
- **Composite** — a recursive enum (leaf and container variants) replaces the Component/Leaf/Composite hierarchy; `match` is exhaustive.
- **Compose structs** — split a struct into independent parts so the borrow checker allows disjoint partial borrows (Rust-specific).
- **Other structural guidance** — prefer small focused crates; contain `unsafe` in small modules exposing a safe API, with `// SAFETY:` notes; fold repeated generic bounds into one custom marker/blanket trait.

### Behavioral patterns — full code in `references/behavioral.md`

- **Strategy** — three approaches: closures (simplest, single-method), trait objects (open set, multiple methods, state), enum dispatch (closed set, ~10x faster than trait objects).
- **Command** — `Box<dyn Command>` with `execute`/`undo` pushed onto a history stack, or plain `Box<dyn Fn()>` closures for simple cases.
- **Observer** — channels. Caution: `std::sync::mpsc` is multi-producer *single*-consumer — a queue, not broadcast. For every-observer-sees-every-event, keep one `Sender` per observer, or use `tokio::sync::broadcast` / `crossbeam-channel`.
- **State** — enum variants hold per-state data; exhaustive `match` forces handling all states on every transition.
- **Iterator** — implement `Iterator::next` (built-in); lazy adaptors (`.map()`, `.filter()`, `.take()`) are zero-cost.
- **Fold** — `.fold()` for accumulation over a collection; per-variant folder functions for transforming an AST/recursive enum into a new structure (the functional alternative to Visitor-as-transform).
- **Template Method** — a trait with required methods, a default-method skeleton, and no-op hooks replaces the abstract base class.
- **Chain of Responsibility** — `Vec<Box<dyn Fn(&mut Request) -> bool>>` (true = handled) replaces the linked list of handler objects.
- **Visitor** — for closed type sets, per-operation functions that `match` on the enum replace visitor classes + `accept()`.

### Rust-specific patterns — full code in `references/rust-specific.md`

- **Typestate** — encode valid state transitions in the type system with `PhantomData<State>` marker types and per-state `impl` blocks; invalid transitions are compile errors, zero runtime cost.
- **RAII / Drop** — tie resource lifetime to scope with `impl Drop` (guards, temp files, timers); cleanup is automatic. Replaces try/finally and IDisposable; ownership makes RAII the default in Rust.

## TRAIT OBJECTS vs ENUM DISPATCH

| | Enum | `dyn Trait` |
|---|---|---|
| Performance | ~10x faster (inlining, no vtable) | Vtable lookup, no inlining |
| Memory | Stack, contiguous in Vec | Heap (Box), pointer indirection |
| Extensibility | Closed — adding variant modifies enum | Open — new types impl trait anywhere |
| Use when | You control all variants | Plugins, extensibility, downstream crates |

```rust
// Enum: fastest, closed set
enum Shape { Circle(f64), Rect(f64, f64) }
impl Shape {
    fn area(&self) -> f64 {
        match self {
            Shape::Circle(r) => std::f64::consts::PI * r * r,
            Shape::Rect(w, h) => w * h,
        }
    }
}

// Trait object: extensible, open set
trait ShapeTrait { fn area(&self) -> f64; }
fn total_area(shapes: &[Box<dyn ShapeTrait>]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}
```

**Rule:** If all variants known at compile time, use enum. If third-party extensibility needed, use trait objects.

## ANTI-PATTERNS

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `clone()` to appease borrow checker | Hides ownership issues | Restructure borrows, decompose structs |
| `Deref` polymorphism | Faking inheritance via `Deref` | Use composition + traits |
| `#[deny(warnings)]` in code | Breaks on new Rust versions | Use `RUSTFLAGS=-Dwarnings` in CI only |

## QUICK REFERENCE

| Pattern | Rust Mechanism | OOP Equivalent |
|---|---|---|
| Builder | `self`/`&mut self` chaining | Builder class + Director |
| Factory | Functions + `match` + trait objects | Factory Method / Abstract Factory |
| Singleton | `LazyLock` / `OnceLock` | `getInstance()` + locks |
| Newtype | Tuple struct `struct X(T)` | Wrapper subclass |
| Adapter | Trait impl on wrapper struct | Adapter class |
| Decorator | Generic `W<T: Trait>` | Decorator hierarchy |
| Composite | Recursive enum | Component/Leaf/Composite |
| Strategy | Closures / trait objects / enums | Strategy interface |
| Command | `Box<dyn Command>` or `Box<dyn Fn()>` | Command interface |
| Observer | `mpsc` / `broadcast` channels | Observer/Subject |
| State | Enum variants + `match` | State interface + subclasses |
| Typestate | `PhantomData<S>` + impl blocks | N/A (Rust-specific) |
| Iterator | `impl Iterator` (built-in) | Iterator interface |
| Template Method | Trait default methods | Abstract base class |
| Chain of Resp. | `Vec<Box<dyn Fn>>` | Handler linked list |
| Visitor | `match` on enum | Visitor + accept() |
| RAII/Drop | `impl Drop` | Destructor / IDisposable |
| Fold | `.fold()` / per-variant folders | Visitor-as-transform |

## DESIGN PRINCIPLES

Why-level guidance the patterns serve. In Rust these map onto traits, modules, and ownership.

- **SOLID** — *SRP*: one reason to change per type. *OCP*: extend via new trait impls, don't edit existing code. *LSP*: trait impls must honor the trait's contract. *ISP*: many small traits beat one fat trait (`Read`/`Write` not `ReadWrite`). *DIP*: depend on traits (abstractions), inject concretions.
- **Composition over inheritance (CRP)** — Rust has no inheritance; compose by embedding structs and delegating to traits. This is the default, not a workaround.
- **DRY** — every piece of knowledge has one authoritative representation; factor shared logic into functions/traits/generics.
- **KISS** — simplest design that works; avoid unnecessary generics, indirection, and premature abstraction. Pairs with **YAGNI** (don't build it until needed).
- **Law of Demeter** — talk to immediate collaborators, not their internals (`a.do_x()` not `a.b().c().do_x()`); supports encapsulation.
- **Encapsulation** — keep fields private, expose behavior through methods; modules gate visibility with `pub`.
- **Command-Query Separation (CQS)** — a method either returns data *or* mutates state, not both; mirrors `&self` (query) vs `&mut self` (command).
- **Design by Contract (DbC)** — state preconditions/postconditions/invariants; encode them in the type system (newtypes, typestate) where possible, `assert!`/`debug_assert!` otherwise.
- **Principle of Least Astonishment (POLA)** — behave the way users expect; follow std naming/trait conventions (`Default`, `From`, `Iterator`) so APIs feel familiar.
- **Single Choice** — exactly one module knows the exhaustive list of alternatives; centralize a closed set in one enum + `match` rather than scattering `if mode == ..` checks.
