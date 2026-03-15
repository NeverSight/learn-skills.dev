---
name: rxjava-to-coroutines-migration
description: Guide and execute the migration of asynchronous code from RxJava to Kotlin Coroutines and Flow. Use this skill when a user asks to convert RxJava (Observables, Singles, Completables, Subjects) to Coroutines (suspend functions, Flows, StateFlows).
---

# RxJava to Kotlin Coroutines Migration Skill

A specialized skill designed to safely and idiomatically refactor Android or Kotlin codebases from RxJava to Kotlin Coroutines and Flow.

## Migration Mapping Guide

When migrating RxJava components to Kotlin Coroutines, use the following standard mappings:

### 1. Base Types
- **`Single<T>`** -> `suspend fun ...(): T`
  - A single asynchronous value.
- **`Maybe<T>`** -> `suspend fun ...(): T?`
  - A single asynchronous value that might not exist.
- **`Completable`** -> `suspend fun ...()`
  - An asynchronous operation that completes without a value.
- **`Observable<T>`** -> `Flow<T>`
  - A cold stream of values.
- **`Flowable<T>`** -> `Flow<T>`
  - Coroutines Flow natively handles backpressure.

### 2. Subjects to Hot Flows
- **`PublishSubject<T>`** -> `MutableSharedFlow<T>`
  - Broadcasts events to multiple subscribers. Use `MutableSharedFlow(extraBufferCapacity = ...)` if buffering is needed.
- **`BehaviorSubject<T>`** -> `MutableStateFlow<T>`
  - Holds state and emits the current/latest value to new subscribers. Requires an initial value.
- **`ReplaySubject<T>`** -> `MutableSharedFlow<T>(replay = N)`
  - Replays the last N emitted values to new subscribers.

### 3. Schedulers to Dispatchers
- **`Schedulers.io()`** -> `Dispatchers.IO`
- **`Schedulers.computation()`** -> `Dispatchers.Default`
- **`AndroidSchedulers.mainThread()`** -> `Dispatchers.Main`
- *Context Switching*: `subscribeOn` and `observeOn` are typically replaced by `withContext(Dispatcher)` or `flowOn(Dispatcher)` for Flows.

### 4. Operators
- **`map`** -> `map`
- **`filter`** -> `filter`
- **`flatMap`** -> `flatMapMerge` (concurrent) or `flatMapConcat` (sequential)
- **`switchMap`** -> `flatMapLatest`
- **`doOnNext` / `doOnSuccess`** -> `onEach`
- **`onErrorReturn` / `onErrorResumeNext`** -> `catch { emit(...) }`
- **`startWith`** -> `onStart { emit(...) }`
- **`combineLatest`** -> `combine`
- **`zip`** -> `zip`
- **`delay`** -> `delay` (suspend function) or `onEach { delay(...) }`

### 5. Execution and Lifecycle
- **`subscribe()`** -> `collect {}` (for Flows) or direct invocation (for suspend functions) inside a `CoroutineScope`.
- **`Disposable.dispose()`** -> `Job.cancel()`
- **`CompositeDisposable.clear()`** -> Cancel the parent `CoroutineScope` or `Job`.

## Execution Steps

1. **Analyze the RxJava Chain**: Identify the source type (Single, Observable, etc.), operators used, and where the subscription happens.
2. **Convert the Source**: Change the return type in the repository or data source layer first. Convert to `suspend` functions for one-shot operations, and `Flow` for streams.
3. **Rewrite Operators**: Translate the RxJava operators to their Flow or Coroutine equivalents. Note that many RxJava operators can simply be replaced by standard Kotlin collection/sequence operations inside a `map` or `onEach` block.
4. **Update the Subscription**: Replace `.subscribe(...)` with `launch { ... }` and `.collect { ... }` in the ViewModel or Presenter. Ensure the launch is tied to the correct lifecycle scope (e.g., `viewModelScope`).
5. **Handle Errors**: Replace `onError` blocks with `try/catch` around suspend functions, or `.catch { }` operators on Flows.
6. **Handle Threading**: Remove `.subscribeOn()` and `.observeOn()`. Use `withContext` where necessary, or `.flowOn()` to change the context of the upstream flow.

### Example Transformation

**RxJava:**
```kotlin
fun getUser(id: String): Single<User> { ... }

disposable.add(
    getUser("123")
        .subscribeOn(Schedulers.io())
        .observeOn(AndroidSchedulers.mainThread())
        .subscribe({ user ->
            view.showUser(user)
        }, { error ->
            view.showError(error)
        })
)
```

**Coroutines/Flow:**
```kotlin
suspend fun getUser(id: String): User { ... } // Internally uses withContext(Dispatchers.IO) if needed

viewModelScope.launch {
    try {
        val user = getUser("123")
        view.showUser(user)
    } catch (e: Exception) {
        view.showError(e)
    }
}
```

## Best Practices
- **Favor Suspend Functions:** Default to `suspend` functions instead of `Flow` unless you actually have a stream of multiple values over time. `Single` and `Completable` almost always become `suspend` functions.
- **State Handling:** Use `StateFlow` in ViewModels to expose state to the UI instead of `BehaviorSubject` or `LiveData`.
- **Lifecycle Awareness:** Use `repeatOnLifecycle` or `flowWithLifecycle` in the UI layer when collecting Flows to avoid background work when the view is not visible.
