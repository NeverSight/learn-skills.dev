---
name: gpui-testing
description: Testing GPUI applications and components. Use when writing tests, testing async operations, simulating user input, or debugging test failures.
---

# GPUI Testing

This skill covers testing patterns for GPUI applications.

## Overview

GPUI provides testing utilities for:
- **TestAppContext**: Test harness for GPUI apps
- **Async test execution**: with `run_until_parked()`
- **User input simulation**: clicks, key presses
- **Entity testing**: Creating and interacting with test entities

## Test Setup

### Basic Test Structure

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use gpui::*;

    #[gpui::test]
    async fn test_my_view(cx: &mut TestAppContext) {
        // Test code here
    }
}
```

### Creating Test Entities

```rust
#[gpui::test]
async fn test_counter(cx: &mut TestAppContext) {
    let counter = cx.new(|_| Counter { count: 0 });
    
    assert_eq!(counter.read(cx).count, 0);
}
```

## Async Testing

### Using run_until_parked

```rust
#[gpui::test]
async fn test_async_operation(cx: &mut TestAppContext) {
    let view = cx.new(|_| MyView::new());
    
    view.update(cx, |view, cx| {
        view.start_async_work(cx);
    });
    
    // Wait for all async work to complete
    cx.background_executor.run_until_parked();
    
    // Check results
    assert_eq!(view.read(cx).status, "Complete");
}
```

### GPUI Timers in Tests

**IMPORTANT**: Use GPUI executor timers, not `smol::Timer`:

```rust
#[gpui::test]
async fn test_with_delay(cx: &mut TestAppContext) {
    let view = cx.new(|_| MyView::new());
    
    // ✅ CORRECT - Use GPUI timer
    cx.background_executor.timer(Duration::from_secs(1)).await;
    
    // ❌ WRONG - Don't use smol::Timer
    // smol::Timer::after(Duration::from_secs(1)).await;
    
    cx.background_executor.run_until_parked();
}
```

**Why**: GPUI's scheduler tracks GPUI timers but not `smol::Timer`, which can cause "nothing left to run" errors in `run_until_parked()`.

## Testing Entity Updates

### Update and Verify

```rust
#[gpui::test]
async fn test_increment(cx: &mut TestAppContext) {
    let counter = cx.new(|_| Counter { count: 0 });
    
    counter.update(cx, |counter, cx| {
        counter.increment(cx);
    });
    
    assert_eq!(counter.read(cx).count, 1);
}
```

### Testing Notify

```rust
#[gpui::test]
async fn test_notify(cx: &mut TestAppContext) {
    let view = cx.new(|_| MyView::new());
    
    let observed = Arc::new(AtomicBool::new(false));
    let observed_clone = observed.clone();
    
    cx.observe(&view, move |_view, _cx| {
        observed_clone.store(true, Ordering::SeqCst);
    });
    
    view.update(cx, |view, cx| {
        view.data = "changed".into();
        cx.notify();
    });
    
    assert!(observed.load(Ordering::SeqCst));
}
```

## Testing Actions

### Dispatching Actions

```rust
actions!(test, [TestAction]);

#[gpui::test]
async fn test_action_handling(cx: &mut TestAppContext) {
    let view = cx.new(|_| MyView::new());
    
    // Simulate action dispatch
    view.update(cx, |view, cx| {
        view.handle_action(&TestAction, cx);
    });
    
    assert_eq!(view.read(cx).action_count, 1);
}
```

## Testing Subscriptions

### Event Emission

```rust
#[derive(Clone, Debug)]
enum MyEvent {
    ValueChanged(i32),
}

impl EventEmitter<MyEvent> for MyView {}

#[gpui::test]
async fn test_event_emission(cx: &mut TestAppContext) {
    let view = cx.new(|_| MyView::new());
    let received_events = Arc::new(Mutex::new(Vec::new()));
    let events_clone = received_events.clone();
    
    cx.subscribe(&view, move |_this, _emitter, event, _cx| {
        events_clone.lock().unwrap().push(event.clone());
    });
    
    view.update(cx, |view, cx| {
        cx.emit(MyEvent::ValueChanged(42));
    });
    
    let events = received_events.lock().unwrap();
    assert_eq!(events.len(), 1);
}
```

## Testing Async Operations

### Background Task Completion

```rust
#[gpui::test]
async fn test_background_task(cx: &mut TestAppContext) {
    let view = cx.new(|_| MyView::new());
    
    view.update(cx, |view, cx| {
        cx.spawn(async move |this, cx| {
            let result = cx.background_spawn(async {
                // Expensive computation
                42
            }).await;
            
            this.update(&mut *cx, |view, cx| {
                view.result = Some(result);
                cx.notify();
            })?;
            
            Ok(())
        }).detach();
    });
    
    // Wait for all async work
    cx.background_executor.run_until_parked();
    
    assert_eq!(view.read(cx).result, Some(42));
}
```

### Testing Task Cancellation

```rust
#[gpui::test]
async fn test_task_cancellation(cx: &mut TestAppContext) {
    let view = cx.new(|_| MyView::new());
    
    view.update(cx, |view, cx| {
        view.start_long_task(cx);
    });
    
    // Cancel task
    view.update(cx, |view, cx| {
        view.cancel_task();
    });
    
    cx.background_executor.run_until_parked();
    
    // Task should not have completed
    assert_eq!(view.read(cx).task_completed, false);
}
```

## Assertions and Expectations

### Entity State Assertions

```rust
#[gpui::test]
async fn test_state_changes(cx: &mut TestAppContext) {
    let view = cx.new(|_| MyView::new());
    
    // Initial state
    assert_eq!(view.read(cx).count, 0);
    
    // After update
    view.update(cx, |view, cx| {
        view.count = 10;
        cx.notify();
    });
    
    assert_eq!(view.read(cx).count, 10);
}
```

### Using assert Macros

```rust
#[gpui::test]
async fn test_with_assertions(cx: &mut TestAppContext) {
    let view = cx.new(|_| MyView::new());
    
    view.update(cx, |view, cx| {
        view.process_data(vec![1, 2, 3], cx);
    });
    
    cx.background_executor.run_until_parked();
    
    let view_state = view.read(cx);
    assert!(view_state.is_processed);
    assert_eq!(view_state.items.len(), 3);
    assert!(view_state.error.is_none());
}
```

## Testing Patterns

### Setup and Teardown

```rust
#[gpui::test]
async fn test_with_setup(cx: &mut TestAppContext) {
    // Setup
    let state = cx.new(|_| AppState::default());
    cx.set_global(state.clone());
    
    // Test
    let view = cx.new(|_| MyView::new());
    view.update(cx, |view, cx| {
        view.use_global_state(cx);
    });
    
    // Assertions
    assert!(view.read(cx).has_state);
    
    // Teardown is automatic when test ends
}
```

### Testing Error Cases

```rust
#[gpui::test]
async fn test_error_handling(cx: &mut TestAppContext) {
    let view = cx.new(|_| MyView::new());
    
    view.update(cx, |view, cx| {
        cx.spawn(async move |this, cx| {
            // Simulate error
            let result: Result<(), anyhow::Error> = Err(anyhow::anyhow!("Test error"));
            
            this.update(&mut *cx, |view, cx| {
                view.error = result.err().map(|e| e.to_string());
                cx.notify();
            })?;
            
            Ok(())
        }).detach();
    });
    
    cx.background_executor.run_until_parked();
    
    assert!(view.read(cx).error.is_some());
}
```

## Best Practices

1. **Use `#[gpui::test]` attribute**: Required for GPUI tests
2. **Use GPUI timers**: `cx.background_executor.timer()` instead of `smol::Timer`
3. **Call `run_until_parked()`**: For async operations
4. **Test one thing at a time**: Keep tests focused
5. **Use descriptive names**: Test names should describe what they test
6. **Clean up resources**: Though GPUI handles most cleanup automatically

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Using `smol::Timer` | "Nothing left to run" | Use `cx.background_executor.timer()` |
| Not calling `run_until_parked()` | Async work doesn't complete | Call before assertions |
| Forgetting `#[gpui::test]` | Test doesn't run properly | Use `#[gpui::test]` attribute |
Not handling errors in async | Test failures unclear | Propagate errors with `?` |
| Testing too much at once | Hard to debug failures | Split into smaller tests |

## Example Test Suite

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use gpui::*;
    use std::sync::{Arc, atomic::{AtomicBool, Ordering}};

    #[gpui::test]
    async fn test_counter_initialization(cx: &mut TestAppContext) {
        let counter = cx.new(|_| Counter { count: 0 });
        assert_eq!(counter.read(cx).count, 0);
    }

    #[gpui::test]
    async fn test_counter_increment(cx: &mut TestAppContext) {
        let counter = cx.new(|_| Counter { count: 0 });
        
        counter.update(cx, |counter, cx| {
            counter.increment(cx);
        });
        
        assert_eq!(counter.read(cx).count, 1);
    }

    #[gpui::test]
    async fn test_counter_async_increment(cx: &mut TestAppContext) {
        let counter = cx.new(|_| Counter { count: 0 });
        
        counter.update(cx, |counter, cx| {
            cx.spawn(async move |this, cx| {
                // Simulate async delay
                cx.background_executor.timer(Duration::from_millis(100)).await;
                
                this.update(&mut *cx, |counter, cx| {
                    counter.count += 1;
                    cx.notify();
                })?;
                
                Ok(())
            }).detach();
        });
        
        cx.background_executor.run_until_parked();
        assert_eq!(counter.read(cx).count, 1);
    }

    #[gpui::test]
    async fn test_counter_notify(cx: &mut TestAppContext) {
        let counter = cx.new(|_| Counter { count: 0 });
        let notified = Arc::new(AtomicBool::new(false));
        let notified_clone = notified.clone();
        
        cx.observe(&counter, move |_counter, _cx| {
            notified_clone.store(true, Ordering::SeqCst);
        });
        
        counter.update(cx, |counter, cx| {
            counter.count = 5;
            cx.notify();
        });
        
        assert!(notified.load(Ordering::SeqCst));
    }
}
```

## Summary

- Use `#[gpui::test]` for GPUI tests
- Use `cx.background_executor.timer()` for delays
- Call `run_until_parked()` to complete async work
- Test entity updates with `.update()` and `.read()`
- Use `Arc` and `Mutex` for tracking callbacks
- Avoid `smol::Timer` in tests

## References

- [GPUI Testing Documentation](https://gpui.rs)
- [Zed Test Examples](https://github.com/zed-industries/zed)
