---
name: gpui-actions
description: Actions and event handling in GPUI applications. Use when implementing user interactions, keyboard shortcuts, custom actions, or event-driven behavior.
---

# GPUI Actions

This skill covers actions, events, and user interaction handling in GPUI.

## Overview

GPUI actions provide:
- **Type-safe event handling** with the Action trait
- **Keyboard shortcut binding** with action dispatch
- **Mouse/touch events** with `.on_click()`, `.on_mouse_down()`, etc.
- **Focus management** for keyboard navigation

## Defining Actions

### Simple Actions

Use the `actions!` macro for actions with no data:

```rust
use gpui::*;

actions!(my_app, [Save, Open, Close, Refresh]);

// These actions have no associated data
```

### Actions with Data

Use `#[derive(Clone, PartialEq)]` with the `Action` derive:

```rust
use gpui::*;

#[derive(Clone, PartialEq)]
struct SetCount {
    value: usize,
}

impl_actions!(my_app, [SetCount]);
```

### Action Documentation

Doc comments on actions are displayed to users:

```rust
actions!(editor, [
    /// Save the current file
    Save,
    /// Open a file
    Open,
]);
```

## Mouse Events

### on_click

```rust
use gpui::*;

impl Render for MyView {
    fn render(&mut self, _window: &mut Window, _cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .child("Click me")
            .on_click(|event, window, cx| {
                println!("Clicked at: {:?}", event.position);
            })
    }
}
```

### on_click with cx.listener

Use `cx.listener()` to access the entity:

```rust
impl Render for Counter {
    fn render(&mut self, _window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .child(format!("Count: {}", self.count))
            .child(
                div()
                    .child("Increment")
                    .on_click(cx.listener(|this, event, window, cx| {
                        this.count += 1;
                        cx.notify();
                    }))
            )
    }
}
```

### Other Mouse Events

```rust
div()
    .on_mouse_down(|event, window, cx| {
        // Mouse button pressed
    })
    .on_mouse_up(|event, window, cx| {
        // Mouse button released
    })
    .on_mouse_move(|event, window, cx| {
        // Mouse moved over element
    })
    .on_hover(|is_hovered, window, cx| {
        // Hover state changed
    })
```

## Keyboard Events

### Key Press Handler

```rust
div()
    .on_key_down(|event, window, cx| {
        if event.keystroke.key == "Enter" {
            println!("Enter pressed");
        }
    })
    .on_key_up(|event, window, cx| {
        // Key released
    })
```

### Modifier Keys

```rust
.on_key_down(|event, window, cx| {
    if event.keystroke.modifiers.control && event.keystroke.key == "s" {
        println!("Ctrl+S pressed");
        // Handle save action
    }
})
```

## Action Handlers

### Registering Action Handlers

```rust
use gpui::*;

actions!(my_app, [Increment, Decrement]);

struct Counter {
    count: i32,
}

impl Render for Counter {
    fn render(&mut self, _window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .child(format!("Count: {}", self.count))
            .on_action(cx.listener(|this, action: &Increment, window, cx| {
                this.count += 1;
                cx.notify();
            }))
            .on_action(cx.listener(|this, action: &Decrement, window, cx| {
                this.count -= 1;
                cx.notify();
            }))
    }
}
```

### Dispatching Actions

```rust
// Dispatch from window
window.dispatch_action(Save.boxed_clone(), cx);

// Dispatch from focus handle
focus_handle.dispatch_action(&Save, window, cx);
```

## Focus Management

### Focus Handles

```rust
use gpui::*;

struct InputField {
    focus_handle: FocusHandle,
    text: SharedString,
}

impl InputField {
    fn new(cx: &mut Context<Self>) -> Self {
        Self {
            focus_handle: cx.focus_handle(),
            text: "".into(),
        }
    }
}

impl Render for InputField {
    fn render(&mut self, _window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .track_focus(&self.focus_handle)
            .on_click(cx.listener(|this, _event, _window, cx| {
                this.focus_handle.focus(cx);
            }))
            .child(self.text.clone())
    }
}
```

### Focus Events

```rust
div()
    .track_focus(&self.focus_handle)
    .on_focus(cx.listener(|this, _event, _window, cx| {
        println!("Gained focus");
    }))
    .on_blur(cx.listener(|this, _event, _window, cx| {
        println!("Lost focus");
    }))
```

## Practical Examples

### Button Component

```rust
use gpui::*;

#[derive(IntoElement)]
struct Button {
   label: SharedString,
    on_click: Option<Box<dyn Fn(&mut App) + 'static>>,
}

impl Button {
    fn new(label: impl Into<SharedString>) -> Self {
        Self {
            label: label.into(),
            on_click: None,
        }
    }
    
    fn on_click(mut self, handler: impl Fn(&mut App) + 'static) -> Self {
        self.on_click = Some(Box::new(handler));
        self
    }
}

impl RenderOnce for Button {
    fn render(self, _window: &mut Window, _cx: &mut App) -> impl IntoElement {
        let mut div = div()
            .px_4()
            .py_2()
            .bg(rgb(0x3b82f6))
            .text_color(rgb(0xffffff))
            .rounded(px(6.0))
            .cursor_pointer()
            .child(self.label);
        
        if let Some(handler) = self.on_click {
            div = div.on_click(move |_event, _window, cx| {
                handler(cx);
            });
        }
        
        div
    }
}
```

### Form with Multiple Actions

```rust
actions!(form, [Submit, Cancel, Reset]);

struct LoginForm {
    username: SharedString,
    password: SharedString,
}

impl Render for LoginForm {
    fn render(&mut self, _window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .v_flex()
            .gap_4()
            .on_action(cx.listener(|this, _: &Submit, window, cx| {
                println!("Submitting: {}", this.username);
                // Handle submit
            }))
            .on_action(cx.listener(|this, _: &Cancel, window, cx| {
                println!("Cancelled");
                // Handle cancel
            }))
            .on_action(cx.listener(|this, _: &Reset, window, cx| {
                this.username = "".into();
                this.password = "".into();
                cx.notify();
            }))
            .child("Login Form")
    }
}
```

### Drag and Drop

```rust
struct DraggableItem {
    position: Point<Pixels>,
    is_dragging: bool,
    drag_offset: Point<Pixels>,
}

impl Render for DraggableItem {
    fn render(&mut self, _window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .absolute()
            .left(self.position.x)
            .top(self.position.y)
            .w(px(100.0))
            .h(px(100.0))
            .bg(rgb(0x3b82f6))
            .cursor_pointer()
            .on_mouse_down(cx.listener(|this, event, _window, cx| {
                this.is_dragging = true;
                this.drag_offset = event.position - this.position;
                cx.notify();
            }))
            .on_mouse_up(cx.listener(|this, _event, _window, cx| {
                this.is_dragging = false;
                cx.notify();
            }))
            .on_mouse_move(cx.listener(|this, event, _window, cx| {
                if this.is_dragging {
                    this.position = event.position - this.drag_offset;
                    cx.notify();
                }
            }))
            .child("Drag me")
    }
}
```

## Event Propagation

### Stopping Propagation

```rust
div()
    .on_click(|event, _window, cx| {
        println!("Child clicked");
        // Prevent parent from receiving event
        event.stop_propagation();
    })
```

## Best Practices

1. **Use cx.listener()**: For accessing entity state in event handlers
2. **Call cx.notify()**: After state changes that affect rendering
3. **Use actions for keyboard shortcuts**: More maintainable than key handlers
4. **Handle focus properly**: Use `track_focus()` and `FocusHandle`
5. **Document actions**: Add doc comments for better UX
6. **Use type-safe actions**: Prefer actions over string-based events

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Forgetting cx.notify() | UI doesn't update | Call after state changes |
| Not using cx.listener() | Can't access entity | Use `cx.listener()` |
| Nested event handlers | Confusing behavior | Use event propagation control |
| Missing focus tracking | Keyboard events don't work | Use `.track_focus()` |
| Not boxing actions | Type errors | Use `.boxed_clone()` for dispatch |

## Summary

- Use `actions!()` macro for simple actions
- Use `.on_click(cx.listener(...))` for clickable elements
- Use `.on_action()` for action handlers
- Use `FocusHandle` for keyboard focus
- Call `cx.notify()` after state changes
- Dispatch actions with `window.dispatch_action()`

## References

- [GPUI Actions Documentation](https://gpui.rs)
- [Zed Keyboard Shortcuts](https://github.com/zed-industries/zed)
