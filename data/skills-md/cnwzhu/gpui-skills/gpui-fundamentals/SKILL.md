---
name: gpui-fundamentals
description: Core GPUI concepts including contexts, windows, entities, elements, and rendering. Use when learning GPUI basics, understanding the framework architecture, or implementing core UI patterns.
---

# GPUI Fundamentals

This skill covers the core concepts of GPUI framework for building desktop UI applications in Rust.

## Overview

GPUI is a UI framework that provides:
- **Entities**: Handles to state with lifecycle management
- **Contexts**: Access to global state, windows, and system services
- **Elements**: Composable UI building blocks
- **Rendering**: `Render` trait for creating element trees
- **Concurrency**: Async primitives for background work

## Context Types

Context types allow interaction with global state, windows, entities, and system services. They are passed as the argument named `cx`.

### App

`App` is the root context type, providing access to global state and read/update of entities.

```rust
fn do_something(cx: &mut App) {
    // Access global state
    // Read/update entities
}
```

### Context<T>

Provided when updating an `Entity<T>`. This context dereferences into `App`, so functions which take `&App` can also take `&Context<T>`.

```rust
struct MyView {
    count: usize,
}

impl MyView {
    fn increment(&mut self, cx: &mut Context<Self>) {
        self.count += 1;
        cx.notify(); // Tell GPUI to re-render
    }
}
```

### AsyncApp and AsyncWindowContext

Provided by `cx.spawn()` for async operations. These can be held across await points.

```rust
fn start_async_work(&mut self, cx: &mut Context<Self>) {
    cx.spawn(async move |this, cx| {
        // this: WeakEntity<Self>
        // cx: &mut AsyncApp
        
        // Do async work
        Ok(())
    }).detach();
}
```

## Window

`Window` provides access to the state of an application window. It is passed as an argument named `window` and comes **before** `cx` when present.

```rust
impl Render for MyView {
    fn render(&mut self, window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        div().child("Hello")
    }
}
```

Used for:
- Managing focus
- Dispatching actions
- Directly drawing
- Getting user input state

## Entities

An `Entity<T>` is a handle to state of type `T`. Entities enable:
- Shared ownership of UI state
- Automatic lifecycle management
- Safe concurrent access

### Creating Entities

```rust
app.run(move |cx| {
    cx.spawn(async move |cx| {
        cx.open_window(WindowOptions::default(), |window, cx| {
            // Create an entity
            cx.new(|_cx| MyView { count: 0 })
        })?;
        
        Ok::<_, anyhow::Error>(())
    }).detach();
});
```

### Entity Operations

```rust
// Given: thing: Entity<MyView>

// Get entity ID
let id = thing.entity_id();

// Downgrade to weak reference
let weak = thing.downgrade();

// Read (immutable access)
let value = thing.read(cx);
println!("Count: {}", value.count);

// Read with closure
let count = thing.read_with(cx, |view, cx| view.count);

// Update (mutable access)
thing.update(cx, |view, cx| {
    view.count += 1;
    cx.notify();
});

// Update with window access
thing.update_in(cx, |view, window, cx| {
    view.count += 1;
    window.dispatch_action(SomeAction.boxed_clone(), cx);
    cx.notify();
});
```

### Important Rules

1. **Use inner cx**: Within closures, use the inner `cx` provided to the closure, not the outer `cx`

```rust
// ❌ WRONG
entity.update(cx, |view, inner_cx| {
    view.count += 1;
    cx.notify(); // Using outer cx - WRONG!
});

// ✅ CORRECT
entity.update(cx, |view, inner_cx| {
    view.count += 1;
    inner_cx.notify(); // Using inner cx
});
```

2. **Avoid update-while-updating**: Never update an entity while it's already being updated (causes panic)

```rust
// ❌ WRONG - will panic
entity.update(cx, |view, cx| {
    entity.update(cx, |view2, cx2| { // Nested update - PANIC!
        // ...
    });
});
```

## Elements

The `Render` trait is used to render state into an element tree with flexbox layout.

### Render Trait

```rust
use gpui::*;

struct MyView {
    text: SharedString,
}

impl Render for MyView {
    fn render(&mut self, _window: &mut Window, _cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .flex()
            .flex_col()
            .gap_2()
            .child(self.text.clone())
            .child("More text")
    }
}
```

### RenderOnce Trait

For components constructed just to be turned into elements:

```rust
use gpui::*;

#[derive(IntoElement)]
struct Card {
    title: SharedString,
    content: SharedString,
}

impl RenderOnce for Card {
    fn render(self, _window: &mut Window, _cx: &mut App) -> impl IntoElement {
        div()
            .p_4()
            .bg(rgb(0x1a1a1a))
            .rounded(px(8.0))
            .child(
                div().font_bold().child(self.title)
            )
            .child(
                div().text_sm().child(self.content)
            )
    }
}

// Usage
impl Render for MyView {
    fn render(&mut self, _window: &mut Window, _cx: &mut Context<Self>) -> impl IntoElement {
        div().child(Card {
            title: "Hello".into(),
            content: "World".into(),
        })
    }
}
```

### SharedString

Use `SharedString` to avoid copying strings. It's either `&'static str` or `Arc<str>`.

```rust
use gpui::*;

struct MyView {
    // Efficient string storage
    title: SharedString,
}

impl MyView {
    fn new() -> Self {
        Self {
            title: "Hello".into(), // From &str
        }
    }
    
    fn set_title(&mut self, title: String) {
        self.title = title.into(); // From String
    }
}

// SharedString implements IntoElement
impl Render for MyView {
    fn render(&mut self, _window: &mut Window, _cx: &mut Context<Self>) -> impl IntoElement {
        div().child(self.title.clone())
    }
}
```

## Element Composition

### Basic Composition

```rust
div()
    .child("Text")
    .child(div().child("Nested"))
    .child(another_element())
```

### Conditional Rendering

Use `.when()` for conditional attributes/children:

```rust
div()
    .when(is_active, |this| {
        this.bg(rgb(0x3b82f6))
    })
    .when_some(maybe_text, |this, text| {
        this.child(text)
    })
```

### Multiple Children

```rust
div()
    .children(vec![
        div().child("Item 1"),
        div().child("Item 2"),
        div().child("Item 3"),
    ])
```

## Application Lifecycle

### Basic Application

```rust
use gpui::*;

struct AppView;

impl Render for AppView {
    fn render(&mut self, _window: &mut Window, _cx: &mut Context<Self>) -> impl IntoElement {
        div().size_full().child("My App")
    }
}

fn main() {
    let app = Application::new();
    
    app.run(move |cx| {
        cx.spawn(async move |cx| {
            cx.open_window(WindowOptions::default(), |window, cx| {
                cx.new(|_| AppView)
            })?;
            
            Ok::<_, anyhow::Error>(())
        })
        .detach();
    });
}
```

### Window Options

```rust
use gpui::*;

let options = WindowOptions {
    window_bounds: Some(WindowBounds::Windowed(Bounds {
        origin: Point { x: px(100.0), y: px(100.0) },
        size: Size { width: px(1024.0), height: px(768.0) },
    })),
    titlebar: Some(TitlebarOptions {
        title: Some("My Application".into()),
        appears_transparent: false,
        ..Default::default()
    }),
    focus: true,
    show: true,
    ..Default::default()
};

cx.open_window(options, |window, cx| {
    cx.new(|_| MyView::new())
})?;
```

## Common Patterns

### State Update with Notify

When state changes in a way that affects rendering:

```rust
struct Counter {
    count: usize,
}

impl Counter {
    fn increment(&mut self, cx: &mut Context<Self>) {
        self.count += 1;
        cx.notify(); // Trigger re-render
    }
}
```

### Event Handlers

```rust
impl Render for Counter {
    fn render(&mut self, _window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .child(format!("Count: {}", self.count))
            .child(
                div()
                    .child("Increment")
                    .on_click(cx.listener(|this, _event, _window, cx| {
                        this.increment(cx);
                    }))
            )
    }
}
```

### Using cx.listener

The `cx.listener()` method creates event handlers that receive `&mut Self`:

```rust
.on_click(cx.listener(|this: &mut Self, event, window, cx| {
    // this: mutable reference to the entity
    // event: the click event
    // window: window reference
### Todo List with Entity Management

```rust
use gpui::*;

#[derive(Clone)]
struct TodoItem {
    id: usize,
    text: String,
    completed: bool,
}

struct TodoList {
    items: Vec<TodoItem>,
    next_id: usize,
    input_text: SharedString,
}

impl TodoList {
    fn new() -> Self {
        Self {
            items: Vec::new(),
            next_id: 1,
            input_text: "".into(),
        }
    }
    
    fn add_item(&mut self, cx: &mut Context<Self>) {
        if !self.input_text.is_empty() {
            self.items.push(TodoItem {
                id: self.next_id,
                text: self.input_text.to_string(),
                completed: false,
            });
            self.next_id += 1;
            self.input_text = "".into();
            cx.notify();
        }
    }
    
    fn toggle_item(&mut self, id: usize, cx: &mut Context<Self>) {
        if let Some(item) = self.items.iter_mut().find(|i| i.id == id) {
            item.completed = !item.completed;
            cx.notify();
        }
    }
    
    fn remove_item(&mut self, id: usize, cx: &mut Context<Self>) {
        self.items.retain(|item| item.id != id);
        cx.notify();
    }
}

impl Render for TodoList {
    fn render(&mut self, _window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .size_full()
            .p_6()
            .bg(rgb(0x0f0f0f))
            .flex()
            .flex_col()
            .gap_4()
            .child(
                div()
                    .text_2xl()
                    .font_bold()
                    .text_color(rgb(0xffffff))
                    .child("Todo List")
            )
            .child(
                div()
                    .flex()
                    .gap_2()
                    .child(
                        div()
                            .flex_1()
                            .px_3()
                            .py_2()
                            .bg(rgb(0x1a1a1a))
                            .border_1()
                            .border_color(rgb(0x4a4a4a))
                            .rounded_md()
                            .child(self.input_text.clone())
                    )
                    .child(
                        div()
                            .px_4()
                            .py_2()
                            .bg(rgb(0x3b82f6))
                            .rounded_md()
                            .cursor_pointer()
                            .child("Add")
                            .on_click(cx.listener(|this, _event, _window, cx| {
                                this.add_item(cx);
                            }))
                    )
            )
            .child(
                div()
                    .flex()
                    .flex_col()
                    .gap_2()
                    .children(
                        self.items.iter().map(|item| {
                            let id = item.id;
                            div()
                                .flex()
                                .items_center()
                                .gap_2()
                                .p_3()
                                .bg(rgb(0x1a1a1a))
                                .rounded_md()
                                .child(
                                    div()
                                        .w(px(20.0))
                                        .h(px(20.0))
                                        .border_2()
                                        .border_color(rgb(0x3b82f6))
                                        .rounded(px(4.0))
                                        .cursor_pointer()
                                        .when(item.completed, |this| {
                                            this.bg(rgb(0x3b82f6))
                                        })
                                        .on_click(cx.listener(move |this, _event, _window, cx| {
                                            this.toggle_item(id, cx);
                                        }))
                                )
                                .child(
                                    div()
                                        .flex_1()
                                        .text_color(if item.completed {
                                            rgb(0x6b7280)
                                        } else {
                                            rgb(0xffffff)
                                        })
                                        .when(item.completed, |this| {
                                            this.line_through()
                                        })
                                        .child(&item.text)
                                )
                                .child(
                                    div()
                                        .px_3()
                                        .py_1()
                                        .bg(rgb(0xef4444))
                                        .rounded(px(4.0))
                                        .cursor_pointer()
                                        .child("×")
                                        .on_click(cx.listener(move |this, _event, _window, cx| {
                                            this.remove_item(id, cx);
                                        }))
                                )
                        })
                    )
            )
    }
}
```

## Performance Tips

### 1. Minimize Entity Updates

```rust
// ❌ BAD - Multiple updates
entity.update(cx, |view, cx| { view.x = 10; cx.notify(); });
entity.update(cx, |view, cx| { view.y = 20; cx.notify(); });
entity.update(cx, |view, cx| { view.z = 30; cx.notify(); });

// ✅ GOOD - Single update
entity.update(cx, |view, cx| {
    view.x = 10;
    view.y = 20;
    view.z = 30;
    cx.notify();
});
```

### 2. Use WeakEntity for Callbacks

```rust
// ❌ BAD - Strong reference can leak
struct Parent {
    child: Entity<Child>,
}

// ✅ GOOD - Weak reference prevents leaks
struct Callback {
    target: WeakEntity<Target>,
}
```

### 3. Batch Notifications

```rust
struct BatchUpdate {
    needs_notify: bool,
}

impl BatchUpdate {
    fn update_multiple(&mut self, cx: &mut Context<Self>) {
        self.field1 = value1;
        self.field2 = value2;
        self.field3 = value3;
        
        // Single notify at the end
        cx.notify();
    }
}
```

### 4. Avoid Unnecessary Clones

```rust
// ❌ BAD - Unnecessary clone
div().child(self.text.clone().to_string())

// ✅ GOOD - Use SharedString directly
div().child(self.text.clone())
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using outer `cx` in update closure | Use the inner `cx` provided to closure |
| Nested entity updates | Restructure to avoid updating entity while updating |
| Forgetting `cx.notify()` | Call after state changes that affect rendering |
| Not using `SharedString` | Use `SharedString` for text to avoid copies |
| Update without window in `Render` | Use Context methods that don't need Window |
| Calling `.unwrap()` on entity operations | Use `?` or handle errors properly |
| Not storing `Subscription` | Store in struct field to keep subscription alive |
| Using `smol::Timer` in tests | Use `cx.background_executor.timer()` |

## Summary

- **Entities** (`Entity<T>`): Handles to shared state
- **Contexts** (`App`, `Context<T>`): Access to framework services
- **Window**: Window-specific operations
- **Elements**: Built with `div()` and styled with methods
- **Render**: Trait for converting state to UI
- **SharedString**: Efficient string type for UI text

## References

- [GPUI Documentation](https://gpui.rs)
- [Zed GEMINI.md](https://github.com/zed-industries/zed/blob/main/GEMINI.md)
```
