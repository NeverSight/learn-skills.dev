---
name: swift-async-stream-patterns
description: Patterns and best practices for building robust AsyncStream and AsyncSequence types, learned from swift-async-algorithms.
---

# AsyncStream & AsyncSequence Patterns

## When to use

- Building custom `AsyncSequence` types that produce values over time
- Bridging synchronous/callback-based APIs to async/await
- Implementing channels, buffers, or multi-consumer broadcasting
- Handling backpressure in producer/consumer scenarios
- Creating "CurrentValue"-like semantics where late subscribers receive buffered values

## Core Patterns from swift-async-algorithms

### 1. State Machine Pattern

Use explicit state machines with enums to model complex async behavior. State machines return **actions** rather than performing side effects directly. This separates state logic from async operations.

```swift
struct ChannelStateMachine<Element: Sendable> {
  private enum State: Sendable {
    case idle
    case buffered(Element)
    case streaming(continuation: Continuation)
    case finished
  }

  private var state: State = .idle

  // Each mutation returns an Action describing what to do
  enum SendAction {
    case yield(continuation: Continuation, element: Element)
    case buffer(element: Element)
    case ignore
  }

  mutating func send(_ element: Element) -> SendAction {
    switch state {
    case .idle:
      state = .buffered(element)
      return .buffer(element: element)
    case .buffered:
      state = .buffered(element)
      return .buffer(element: element)
    case .streaming(let continuation):
      return .yield(continuation: continuation, element: element)
    case .finished:
      return .ignore
    }
  }
}
```

**Key insight**: Compute state transitions inside locks, execute side effects (like resuming continuations) OUTSIDE locks.

### 2. Thread-Safe State with Mutex

Use `Mutex` from the Synchronization framework (iOS 18+, macOS 15+). The pattern from swift-async-algorithms:

```swift
import Synchronization

@available(macOS 15.0, iOS 18.0, *)
final class Channel<Element: Sendable>: Sendable {
  // State is a simple Sendable struct (NOT ~Copyable)
  private struct State: Sendable {
    var bufferedElement: Element?
    var continuation: AsyncStream<Element>.Continuation?
    var isFinished: Bool = false
  }

  // Mutex is stored in the class (class can hold ~Copyable types)
  private let state: Mutex<State>

  init() {
    self.state = Mutex(State())
  }

  func send(_ element: Element) {
    // 1. Determine action INSIDE lock
    let continuation = state.withLock { state -> AsyncStream<Element>.Continuation? in
      guard !state.isFinished else { return nil }
      if let cont = state.continuation {
        return cont
      } else {
        state.bufferedElement = element
        return nil
      }
    }
    // 2. Execute side effect OUTSIDE lock
    continuation?.yield(element)
  }
}
```

**Critical rules**:
1. Use `final class` to hold `Mutex` (Mutex is `~Copyable`)
2. State struct should be `Sendable`, not `~Copyable`
3. Extract continuations inside the lock, resume OUTSIDE to prevent deadlocks
4. Keep lock durations minimal - no async operations while holding a lock

### 3. Continuation Safety Patterns

Always handle cancellation properly with continuations:

```swift
func next() async -> Element? {
  await withTaskCancellationHandler {
    await withUnsafeContinuation { continuation in
      // Determine action inside lock
      let immediateResult = state.withLock { state -> Element?? in
        if let element = state.buffer.popFirst() {
          return .some(element)
        }
        state.waitingContinuation = continuation
        return nil  // Will be resumed later
      }

      // Handle immediate result OUTSIDE lock
      if let result = immediateResult {
        continuation.resume(returning: result)
      }
    }
  } onCancel: {
    // Called concurrently - must be thread-safe
    let continuation = state.withLock { state -> UnsafeContinuation<Element?, Never>? in
      let cont = state.waitingContinuation
      state.waitingContinuation = nil
      return cont
    }
    continuation?.resume(returning: nil)
  }
}
```

**Critical rules**:
1. `onCancel` runs concurrently with the main operation - use locks
2. Never call user code or resume continuations while holding a lock
3. Always ensure continuations are eventually resumed (success, nil, or cancellation)

### 4. Buffering Strategies

Model buffering policies explicitly:

```swift
enum BufferPolicy: Sendable {
  /// Buffer up to N elements, then suspend producers
  case bounded(Int)

  /// Buffer without limit (use with caution)
  case unbounded

  /// Keep newest N elements, drop oldest when full
  case bufferingNewest(Int)

  /// Keep oldest N elements, drop newest when full
  case bufferingOldest(Int)
}
```

### 5. Single-Value Buffering (CurrentValue Pattern)

For scenarios where late subscribers should receive the most recent value. Uses explicit state machine with enum states to make invalid states unrepresentable:

```swift
@available(macOS 15.0, iOS 18.0, *)
public final class SingleValueBufferedStream<Element: Sendable>: Sendable {

  private struct StateMachine: Sendable {
    private enum State: Sendable {
      case idle
      case buffered(Element)
      case streaming(AsyncStream<Element>.Continuation, generation: UInt64)
      case finished
    }

    private var state: State = .idle
    private var nextGeneration: UInt64 = 0

    enum SendAction: Sendable {
      case yield(AsyncStream<Element>.Continuation, Element)
      case buffer
      case ignore
    }

    mutating func send(_ element: Element) -> SendAction {
      switch state {
      case .idle:
        state = .buffered(element)
        return .buffer
      case .buffered:
        state = .buffered(element)
        return .buffer
      case .streaming(let continuation, let generation):
        state = .streaming(continuation, generation: generation)
        return .yield(continuation, element)
      case .finished:
        return .ignore
      }
    }

    enum SubscribeAction: Sendable {
      case streamActive(buffered: Element?, generation: UInt64)
      case streamFinished
      case replaceSubscriber(old: AsyncStream<Element>.Continuation, buffered: Element?, generation: UInt64)
    }

    mutating func subscribe(_ continuation: AsyncStream<Element>.Continuation) -> SubscribeAction {
      nextGeneration &+= 1
      let generation = nextGeneration

      switch state {
      case .idle:
        state = .streaming(continuation, generation: generation)
        return .streamActive(buffered: nil, generation: generation)
      case .buffered(let element):
        state = .streaming(continuation, generation: generation)
        return .streamActive(buffered: element, generation: generation)
      case .streaming(let oldContinuation, _):
        state = .streaming(continuation, generation: generation)
        return .replaceSubscriber(old: oldContinuation, buffered: nil, generation: generation)
      case .finished:
        return .streamFinished
      }
    }
  }

  private let stateMachine: Mutex<StateMachine>

  public func send(_ element: Element) {
    let action = stateMachine.withLock { $0.send(element) }
    switch action {
    case .yield(let continuation, let element):
      continuation.yield(element)
    case .buffer, .ignore:
      break
    }
  }
}
```

**Key benefits of enum state machine**:
- Invalid states are unrepresentable (can't have buffered element AND streaming simultaneously)
- State transitions are explicit and documented via switch cases
- Actions returned describe side effects, executed outside the lock

### 6. Lifecycle Management with Reference Types

Use `final class` wrappers for cleanup on deinit:

```swift
struct AsyncShareSequence<Base: AsyncSequence> {
  // Extent manages lifetime - cancels iteration on deinit
  final class Extent: Sendable {
    let iteration: Iteration

    deinit {
      iteration.cancel()
    }
  }

  let extent: Extent
}
```

### 7. Testing Patterns

Use gates for deterministic async testing. Gate is a synchronization primitive from swift-async-algorithms tests:

```swift
import Synchronization

@available(macOS 15.0, iOS 18.0, *)
struct Gate: Sendable {
  private enum State {
    case closed
    case open
    case pending(UnsafeContinuation<Void, Never>)
  }

  private let state: Mutex<State>

  init() {
    self.state = Mutex(.closed)
  }

  func open() {
    let continuation = state.withLock { state -> UnsafeContinuation<Void, Never>? in
      switch state {
      case .closed:
        state = .open
        return nil
      case .pending(let continuation):
        state = .closed
        return continuation
      case .open:
        return nil
      }
    }
    continuation?.resume()
  }

  func enter() async {
    await withUnsafeContinuation { continuation in
      let resume = state.withLock { state -> UnsafeContinuation<Void, Never>? in
        switch state {
        case .closed:
          state = .pending(continuation)
          return nil
        case .open:
          state = .closed
          return continuation
        case .pending:
          fatalError("Only one waiter supported")
        }
      }
      resume?.resume()
    }
  }
}
```

**Testing best practices from swift-async-algorithms**:
- Use `Task.sleep` sparingly and only for timing-sensitive tests
- Use `Gate` for synchronization between producer and consumer tasks
- Always call `finish()` or ensure the stream terminates to avoid hanging tests
- Test edge cases: empty sequences, cancellation, errors, late subscribers

## Anti-patterns to Avoid

### ❌ Using @unchecked Sendable without synchronization

```swift
// BAD: No actual thread safety
final class Storage: @unchecked Sendable {
  var state: State = .idle  // Data race!
}

// GOOD: Use Mutex for thread-safe state
private let state: Mutex<State>
```

### ❌ Making State struct ~Copyable

```swift
// BAD: ~Copyable makes Mutex<State> non-copyable, unusable in classes
private struct State: ~Copyable { ... }

// GOOD: State should be Sendable, not ~Copyable
private struct State: Sendable { ... }
```

### ❌ Resuming continuations inside locks

```swift
// BAD: Resume inside critical region - can deadlock with Swift runtime
state.withLock { state in
  continuation.resume(returning: value)
}

// GOOD: Extract continuation, resume outside
let cont = state.withLock { $0.takeContinuation() }
cont?.resume(returning: value)
```

### ❌ Ignoring stream termination in tests

```swift
// BAD: Test hangs forever if finish() not called
let stream = source.makeStream()
for await value in stream {  // Never terminates!
  collected.append(value)
}

// GOOD: Always ensure stream terminates
source.finish()
for await value in stream {
  collected.append(value)
}
```

### ❌ Race between subscription and first event

```swift
// BAD: Event can fire before stream is subscribed
let stream = AsyncStream { continuation in
  self.continuation = continuation  // Race window here!
}

// GOOD: Buffer for late subscribers using SingleValueBufferedStream
let source = SingleValueBufferedStream<Event>()
source.send(event)  // Safe even if no subscriber yet
let stream = source.makeStream()  // Gets buffered event
```

## Implementation Checklist

- [ ] Use `final class` to hold `Mutex` (Mutex is ~Copyable)
- [ ] Use `Sendable` State struct (not ~Copyable)
- [ ] Extract continuations inside lock, resume OUTSIDE
- [ ] Handle task cancellation with `withTaskCancellationHandler`
- [ ] Consider buffering strategy for producer/consumer mismatch
- [ ] Add lifecycle cleanup via `deinit` or `onTermination`
- [ ] Ensure streams terminate in tests (call `finish()`)
- [ ] Never use `@unchecked Sendable` without actual synchronization

## References

- swift-async-algorithms: https://github.com/apple/swift-async-algorithms
