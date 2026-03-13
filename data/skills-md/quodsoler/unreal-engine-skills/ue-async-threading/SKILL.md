---
name: ue-async-threading
description: "Use this skill when working with Unreal Engine async operations, threading, parallel execution, or concurrency. Also use when the user mentions 'FRunnable', 'FAsyncTask', 'TaskGraph', 'UE::Tasks', 'ParallelFor', 'TFuture', 'TPromise', 'Async()', 'thread safety', 'FCriticalSection', 'FRWLock', 'background thread', 'game thread dispatch', or 'thread pool'. For networking async (RPCs, replication), see ue-networking-replication. For asset streaming, see ue-data-assets-tables."
metadata:
  version: 1.0.0
---

# UE Async and Threading

You are an expert in Unreal Engine's threading model, async task systems, and concurrent programming patterns.

## Context Check

Read `.agents/ue-project-context.md` before proceeding. Engine version matters: `UE::Tasks::Launch` is the modern preferred API (UE 5.0+), while `FAsyncTask` and TaskGraph remain fully supported. Determine: What work needs to be offloaded? Is UObject access required? What latency/throughput tradeoff is acceptable?

## Information Gathering

Ask the user if unclear:
- **Offload type** — CPU-bound computation, I/O wait, or periodic background work?
- **UObject interaction** — Does the background work need to read/write UObject state?
- **Lifetime** — One-shot task, recurring work, or long-lived thread?
- **Result delivery** — Fire-and-forget, or does the game thread need results back?

---

## UE Threading Model

UE runs several named threads plus a scalable worker pool. Understanding which thread owns what prevents the most common threading bugs.

**Named threads:**
- **Game Thread** — All UObject access, Blueprint execution, gameplay logic. Check with `IsInGameThread()`.
- **Render Thread** — Render commands, scene proxy updates. `IsInRenderingThread()`.
- **RHI Thread** — GPU command submission (platform-dependent).
- **Worker Threads** — Unnamed pool threads for task dispatch. Count scales with CPU cores.

**The golden rule:** UObjects are game-thread-only. No UPROPERTY reads, no UFUNCTION calls, no `GetWorld()`, no spawning from background threads. Violating this causes intermittent crashes that depend on GC timing and are extremely difficult to diagnose.

---

## Pattern Selection Guide

Choose the simplest API that fits your needs.

| Pattern | Best For | Lifetime | Result? |
|---------|----------|----------|---------|
| `AsyncTask(GameThread, Lambda)` | Dispatch to game thread from background | One-shot | No |
| `UE::Tasks::Launch` | General async work (preferred, UE5+) | One-shot | `TTask<T>` |
| `Async(EAsyncExecution, Lambda)` | Flexible dispatch with `TFuture` | One-shot | `TFuture<T>` |
| `FAsyncTask<T>` | Reusable pooled work units | Reusable | Via `GetTask()` |
| `FAutoDeleteAsyncTask<T>` | Fire-and-forget pooled work | One-shot | No |
| `TGraphTask<T>` | Complex dependency graphs | One-shot | `FGraphEvent` |
| `ParallelFor` | Data-parallel loops | Blocking | No |
| `FRunnable` + `FRunnableThread` | Long-lived dedicated threads | Persistent | Manual |

---

## FRunnable and FRunnableThread

Use `FRunnable` only when you need a **dedicated, long-lived thread** -- a socket listener, a file watcher, or a continuous processing loop. For one-shot work, prefer `UE::Tasks::Launch` or `FAsyncTask`.

**Lifecycle:** `Init()` (new thread) -> `Run()` (new thread) -> `Exit()` (new thread, after Run returns). `Stop()` is called externally to request shutdown.

**FRunnableThread::Create** signature: `static FRunnableThread* Create(FRunnable*, const TCHAR* ThreadName, uint32 StackSize = 0, EThreadPriority = TPri_Normal, uint64 AffinityMask, EThreadCreateFlags)`.

**Key points:** `Stop()` signals the thread -- it does not block. `Kill(true)` calls `Stop()` then waits for completion. Always `delete` the `FRunnableThread*` after `Kill`. Use `std::atomic<bool> bShouldStop` in `Run()` loop, set it in `Stop()`.

See `references/threading-patterns.md` for a complete `FRunnable` subclass template with proper shutdown.

---

## FAsyncTask and FAutoDeleteAsyncTask

For **reusable work units** on the engine thread pool (`GThreadPool`). Subclass `FNonAbandonableTask` and implement `DoWork()` + `GetStatId()`.

```cpp
class FMyComputeTask : public FNonAbandonableTask
{
    friend class FAsyncTask<FMyComputeTask>;
    int32 Result = 0;
    TArray<int32> InputData;

    FMyComputeTask(TArray<int32> InData) : InputData(MoveTemp(InData)) {}

    void DoWork()
    {
        for (int32 Val : InputData) { Result += Val; }
    }

    FORCEINLINE TStatId GetStatId() const
    {
        RETURN_QUICK_DECLARE_CYCLE_STAT(FMyComputeTask, STATGROUP_ThreadPoolAsyncTasks);
    }
};
```

**Usage:**

```cpp
// Reusable — you manage lifetime
auto* Task = new FAsyncTask<FMyComputeTask>(MoveTemp(Data));
Task->StartBackgroundTask();          // dispatches to GThreadPool
Task->EnsureCompletion();             // blocks or runs inline if not started
int32 R = Task->GetTask().Result;
delete Task;

// Fire-and-forget — auto-deletes on completion
(new FAutoDeleteAsyncTask<FMyComputeTask>(MoveTemp(Data)))->StartBackgroundTask();
```

`IsWorkDone()` is the non-blocking completion check. `Cancel()` prevents execution if not yet started. `StartSynchronousTask()` runs inline on the calling thread.

---

## TaskGraph

For work with **complex dependency chains**. Each task declares prerequisites; the scheduler handles ordering.

```cpp
class FMyGraphTask
{
public:
    FMyGraphTask(int32 InValue) : Value(InValue) {}

    static ESubsequentsMode::Type GetSubsequentsMode()
    { return ESubsequentsMode::TrackSubsequents; }

    ENamedThreads::Type GetDesiredThread()
    { return ENamedThreads::AnyThread; }

    TStatId GetStatId() const
    { RETURN_QUICK_DECLARE_CYCLE_STAT(FMyGraphTask, STATGROUP_TaskGraphTasks); }

    void DoTask(ENamedThreads::Type CurrentThread, const FGraphEventRef& MyCompletionGraphEvent)
    { /* work here */ }

private:
    int32 Value;
};
```

**Dispatching with prerequisites:**

```cpp
FGraphEventArray Prerequisites;  // TArray<FGraphEventRef, TInlineAllocator<4>>
Prerequisites.Add(SomePriorEvent);

FGraphEventRef TaskEvent = TGraphTask<FMyGraphTask>::CreateTask(&Prerequisites)
    .ConstructAndDispatchWhenReady(42);  // args forwarded to constructor

FTaskGraphInterface::Get().WaitUntilTaskCompletes(TaskEvent, ENamedThreads::GameThread);
```

**Quick dispatch** (no custom class needed):

```cpp
AsyncTask(ENamedThreads::GameThread, [this]()
{
    MyActor->UpdateHealth(NewValue); // safe — runs on game thread
});
```

---

## UE::Tasks::Launch (Modern Preferred API)

Recommended for new code (UE 5.0+). Simpler syntax than TaskGraph, automatic thread pool dispatch, built-in chaining.

```cpp
#include "Tasks/Task.h"

UE::Tasks::TTask<int32> Task = UE::Tasks::Launch(
    UE_SOURCE_LOCATION,
    []() { return ExpensiveComputation(); }
);
int32 Result = Task.GetResult(); // blocks until complete

// With prerequisites
UE::Tasks::TTask<FVector> TaskA = UE::Tasks::Launch(UE_SOURCE_LOCATION,
    []() { return ComputePosition(); });

UE::Tasks::TTask<void> TaskB = UE::Tasks::Launch(UE_SOURCE_LOCATION,
    [&TaskA]() { ProcessPosition(TaskA.GetResult()); },
    UE::Tasks::Prerequisites(TaskA)
);
```

**TTask<T> API:** `GetResult()` blocks and returns result. `IsCompleted()` non-blocking. `Wait()` / `Wait(FTimespan)` for timed blocking. `TryRetractAndExecute()` runs inline if not yet started (work stealing).

**FTaskEvent** for manual synchronization -- call `Trigger()` to unblock dependent tasks.

---

## Async, TFuture, and TPromise

`Async()` is the most flexible one-shot dispatch. Returns `TFuture<T>` with execution context control.

```cpp
TFuture<FMyResult> Future = Async(EAsyncExecution::ThreadPool,
    []() -> FMyResult { return ComputeResult(); },
    []() { /* completion callback — runs on unspecified thread */ }
);
FMyResult R = Future.Get(); // blocks, does NOT invalidate (unlike std::future)
```

**EAsyncExecution modes:**

| Mode | Thread |
|------|--------|
| `TaskGraph` | Worker via TaskGraph |
| `TaskGraphMainThread` | Game thread via TaskGraph |
| `Thread` | New dedicated thread |
| `ThreadPool` | `GThreadPool` worker |
| `LargeThreadPool` | `GLargeThreadPool` (WITH_EDITOR only) |

**Convenience:** `AsyncPool(GThreadPool, Lambda)`, `AsyncThread(Lambda, StackSize, Priority)`.

### TFuture<T> API

Key difference from `std::future`: `Get()` does **not** invalidate. Call it multiple times safely. `Consume()` invalidates like `std::future::get()`.

- `IsReady()` -- non-blocking check
- `Wait()` / `WaitFor(FTimespan)` -- block without consuming
- `Then(Continuation)` / `Next(Continuation)` -- chaining, continuation runs on any thread
- `Share()` -- convert to shared future

### TPromise<T>

For producer-consumer patterns where producing and consuming sides are decoupled.

```cpp
TPromise<FMyData> Promise;
TFuture<FMyData> Future = Promise.GetFuture(); // call once

Async(EAsyncExecution::ThreadPool, [P = MoveTemp(Promise)]() mutable
{
    P.SetValue(GenerateData()); // or EmplaceValue()
});

FMyData Result = Future.Get(); // blocks on game thread
```

---

## ParallelFor

For **data-parallel loops** where each iteration is independent. The calling thread participates -- `ParallelFor` blocks until all iterations complete.

```cpp
ParallelFor(Meshes.Num(), [&Meshes](int32 Index)
{
    ProcessMesh(Meshes[Index]);
});

// With MinBatchSize — prevents overhead for small workloads
ParallelFor(TEXT("ProcessMeshes"), Meshes.Num(), 64,
    [&Meshes](int32 Index) { ProcessMesh(Meshes[Index]); }
);
```

**EParallelForFlags:**

| Flag | Value | Effect |
|------|-------|--------|
| `None` | 0 | Default behavior |
| `ForceSingleThread` | 1 | Debug: run sequentially |
| `Unbalanced` | 2 | Iterations have variable cost |
| `PumpRenderingThread` | 4 | Pump render commands while waiting |
| `BackgroundPriority` | 8 | Lower priority for workers |

`ParallelForWithTaskContext` provides a per-worker context object -- use when workers need scratch memory to avoid per-iteration allocation.

---

## Game Thread Safety

Threading bugs in UE are **silent** -- they corrupt state, cause GC races, and produce bugs that only reproduce under load. See `references/thread-safety-guide.md` for complete patterns.

### UObject Access Rules

1. **All UObject access must happen on the game thread.** No reads, writes, or function calls from background threads.
2. **GC can destroy UObjects between ticks.** A raw `UObject*` captured in a lambda may be dangling by execution time.
3. **Spawning, destroying, modifying components** -- game thread only.

### Safe Dispatch Pattern

```cpp
AsyncTask(ENamedThreads::GameThread, [WeakActor = TWeakObjectPtr<AActor>(MyActor)]()
{
    if (AActor* Actor = WeakActor.Get()) // nullptr if GC'd
    {
        Actor->UpdateFromBackgroundWork(NewData);
    }
});
```

**Always capture `TWeakObjectPtr`**, never raw `UObject*`. For non-UObject shared data, use `TSharedPtr<T, ESPMode::ThreadSafe>` -- the default `ESPMode::NotThreadSafe` has non-atomic refcounting.

---

## Synchronization Primitives

### FCriticalSection (Recursive Mutex)

`FCriticalSection` is `UE::FPlatformRecursiveMutex`. Same thread can lock multiple times without deadlocking.

```cpp
FCriticalSection DataLock;
void AddPosition(const FVector& Pos)
{
    FScopeLock Lock(&DataLock);  // RAII — unlocks on scope exit
    SharedPositions.Add(Pos);
}
```

### FRWLock (Read-Write Lock)

Multiple readers OR one exclusive writer. `FRWLock` is **not** recursive -- do not nest.

```cpp
FRWLock CacheLock;
FVector Read(FName Key)  { FReadScopeLock  RL(CacheLock); return Cache.FindRef(Key); }
void Write(FName K, FVector V) { FWriteScopeLock WL(CacheLock); Cache.Add(K, V); }
```

### FEventRef and Atomics

`FEventRef` is the RAII wrapper for thread signaling. Prefer over raw `FEvent*`.

```cpp
FEventRef WorkReady(EEventMode::AutoReset);
WorkReady->Trigger(); // producer signals
WorkReady->Wait();    // consumer blocks
```

`FThreadSafeCounter` and `FThreadSafeBool` are deprecated -- use `std::atomic<int32>` and `std::atomic<bool>` directly.

---

## TQueue (Lock-Free Queue)

Thread-safe queue for producer-consumer without locks.

```cpp
TQueue<FMyMessage, EQueueMode::Mpsc> MessageQueue;

// Producer (any thread)
MessageQueue.Enqueue(FMyMessage{...});

// Consumer (game thread tick)
FMyMessage Msg;
while (MessageQueue.Dequeue(Msg)) { ProcessMessage(Msg); }
```

`Spsc` -- single-producer, single-consumer (slightly faster). `Mpsc` -- multiple-producer, single-consumer (most common). `Peek()` reads without dequeuing.

---

## Common Mistakes

**Accessing UObject from background thread -- dispatch results back:**
```cpp
// WRONG — UObject access off game thread
Async(EAsyncExecution::ThreadPool, [this]()
{ MyActor->Health = ComputeNewHealth(); });

// RIGHT — compute off-thread, apply on game thread via weak pointer
Async(EAsyncExecution::ThreadPool, [WeakActor = TWeakObjectPtr<AActor>(MyActor)]()
{
    float NewHealth = ComputeNewHealth();
    AsyncTask(ENamedThreads::GameThread, [WeakActor, NewHealth]()
    { if (AActor* A = WeakActor.Get()) { A->SetHealth(NewHealth); } });
});
```

**TSharedPtr with default ESPMode across threads:**
```cpp
// WRONG — non-atomic refcount
auto Data = MakeShared<FMyData>();
// RIGHT
auto Data = MakeShared<FMyData, ESPMode::ThreadSafe>();
```

**FRWLock nested acquisition -- deadlock:**
```cpp
// WRONG — FRWLock is NOT recursive
FReadScopeLock Outer(Lock);
FReadScopeLock Inner(Lock);  // DEADLOCK on some platforms
// RIGHT — acquire once, do all reads, release
```

**ParallelFor with shared mutable state:**
```cpp
// WRONG — concurrent writes
int32 Total = 0;
ParallelFor(Data.Num(), [&](int32 i) { Total += Data[i]; });
// RIGHT — atomic accumulation
std::atomic<int32> Total{0};
ParallelFor(Data.Num(), [&](int32 i)
{ Total.fetch_add(Data[i], std::memory_order_relaxed); });
```

---

## Related Skills

- `ue-cpp-foundations` -- TSharedPtr, TWeakObjectPtr, GC lifetime, smart pointer rules
- `ue-gameplay-framework` -- game thread tick flow, actor lifecycle ordering
- `ue-networking-replication` -- RPC dispatch threads, replication callbacks
- `ue-data-assets-tables` -- FStreamableManager async loading, soft references
