---
name: workmanager
description: Android WorkManager for guaranteed background execution - use for deferred tasks, periodic syncs, file uploads, notifications, and task chains. Covers CoroutineWorker, constraints, chaining, testing, and troubleshooting. Use when implementing background work that needs reliable execution across app restarts and doze mode.
---

# Android WorkManager

WorkManager is the recommended solution for persistent, guaranteed background work on Android.

## When to Use WorkManager

Use WorkManager for:
- **Periodic background sync** - Sync data with server every 15+ minutes
- **Deferred tasks** - Upload files, compress images when device is ready
- **Guaranteed execution** - Tasks that must run even if app is killed
- **Constraint-based work** - Run only when WiFi connected, battery charging, etc.

Don't use WorkManager for:
- **Immediate execution** - Use Kotlin coroutines directly
- **Precise timing** - Use AlarmManager for exact scheduling
- **Foreground work** - Use coroutines in ViewModel/Service

## Dependencies

```kotlin
// build.gradle.kts (androidMain or Android module)
dependencies {
    implementation("androidx.work:work-runtime-ktx:2.9.0")
}
```

## CoroutineWorker Basics

### Simple Worker

```kotlin
class SyncWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        return try {
            // Perform background work
            val data = fetchDataFromServer()
            saveToDatabase(data)

            Result.success()
        } catch (e: Exception) {
            Log.e("SyncWorker", "Sync failed", e)

            if (runAttemptCount < 3) {
                Result.retry() // Retry with exponential backoff
            } else {
                Result.failure() // Give up after 3 attempts
            }
        }
    }
}
```

### Worker with Input/Output Data

```kotlin
class UploadWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        // Get input data
        val fileUri = inputData.getString(KEY_FILE_URI) ?: return Result.failure()
        val userId = inputData.getLong(KEY_USER_ID, -1L)

        return try {
            val uploadedUrl = uploadFile(fileUri)

            // Return output data
            val outputData = workDataOf(
                KEY_UPLOADED_URL to uploadedUrl,
                KEY_TIMESTAMP to System.currentTimeMillis()
            )

            Result.success(outputData)
        } catch (e: Exception) {
            Result.retry()
        }
    }

    companion object {
        const val KEY_FILE_URI = "file_uri"
        const val KEY_USER_ID = "user_id"
        const val KEY_UPLOADED_URL = "uploaded_url"
        const val KEY_TIMESTAMP = "timestamp"
    }
}
```

### Worker with Progress

```kotlin
class DownloadWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        val url = inputData.getString(KEY_URL) ?: return Result.failure()

        return try {
            downloadFile(url) { progress ->
                // Update progress (0-100)
                setProgress(workDataOf(KEY_PROGRESS to progress))
            }

            Result.success()
        } catch (e: Exception) {
            Result.failure()
        }
    }

    companion object {
        const val KEY_URL = "url"
        const val KEY_PROGRESS = "progress"
    }
}

// Observe progress
WorkManager.getInstance(context)
    .getWorkInfoByIdLiveData(workId)
    .observe(lifecycleOwner) { workInfo ->
        val progress = workInfo?.progress?.getInt(DownloadWorker.KEY_PROGRESS, 0) ?: 0
        updateProgressBar(progress)
    }
```

### Foreground Worker (with Notification)

```kotlin
class LongRunningWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        // Show notification for long-running work
        setForeground(createForegroundInfo())

        return try {
            performLongOperation()
            Result.success()
        } catch (e: Exception) {
            Result.failure()
        }
    }

    private fun createForegroundInfo(): ForegroundInfo {
        val notification = NotificationCompat.Builder(applicationContext, CHANNEL_ID)
            .setContentTitle("Processing")
            .setContentText("Processing your request...")
            .setSmallIcon(R.drawable.ic_notification)
            .setOngoing(true)
            .build()

        return ForegroundInfo(NOTIFICATION_ID, notification)
    }

    companion object {
        private const val CHANNEL_ID = "work_channel"
        private const val NOTIFICATION_ID = 1
    }
}
```

## Scheduling Work

### One-Time Work

```kotlin
// Simple enqueue
val syncRequest = OneTimeWorkRequestBuilder<SyncWorker>()
    .build()

WorkManager.getInstance(context).enqueue(syncRequest)

// With input data
val uploadRequest = OneTimeWorkRequestBuilder<UploadWorker>()
    .setInputData(workDataOf(
        UploadWorker.KEY_FILE_URI to fileUri,
        UploadWorker.KEY_USER_ID to userId
    ))
    .build()

WorkManager.getInstance(context).enqueue(uploadRequest)

// With constraints (see Constraints section)
val constrainedRequest = OneTimeWorkRequestBuilder<SyncWorker>()
    .setConstraints(
        Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .build()
    )
    .build()

WorkManager.getInstance(context).enqueue(constrainedRequest)
```

### Periodic Work

```kotlin
// Minimum interval is 15 minutes
val syncRequest = PeriodicWorkRequestBuilder<SyncWorker>(
    repeatInterval = 15,
    repeatIntervalTimeUnit = TimeUnit.MINUTES
)
    .setConstraints(
        Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .build()
    )
    .build()

WorkManager.getInstance(context).enqueue(syncRequest)

// With flex interval (run within last 5 minutes of 15-minute period)
val flexRequest = PeriodicWorkRequestBuilder<SyncWorker>(
    repeatInterval = 15,
    repeatIntervalTimeUnit = TimeUnit.MINUTES,
    flexTimeInterval = 5,
    flexTimeIntervalUnit = TimeUnit.MINUTES
)
    .build()
```

### Delayed Work

```kotlin
val delayedRequest = OneTimeWorkRequestBuilder<NotificationWorker>()
    .setInitialDelay(1, TimeUnit.HOURS)
    .build()

WorkManager.getInstance(context).enqueue(delayedRequest)
```

### Expedited Work (Android 12+)

```kotlin
// For important user-facing work
val expeditedRequest = OneTimeWorkRequestBuilder<UploadWorker>()
    .setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)
    .build()

WorkManager.getInstance(context).enqueue(expeditedRequest)
```

## Constraints

See [references/constraints.md](references/constraints.md) for detailed constraint patterns and combinations.

Quick reference:

```kotlin
val constraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED) // Any network
    .setRequiresBatteryNotLow(true)
    .setRequiresCharging(false)
    .setRequiresStorageNotLow(true)
    .setRequiresDeviceIdle(false) // API 23+
    .build()

val request = OneTimeWorkRequestBuilder<SyncWorker>()
    .setConstraints(constraints)
    .build()
```

## Work Chaining

See [references/chaining.md](references/chaining.md) for advanced chaining patterns and parallel execution.

### Sequential Chain

```kotlin
WorkManager.getInstance(context)
    .beginWith(downloadRequest)
    .then(processRequest)
    .then(uploadRequest)
    .enqueue()
```

### Parallel Chains

```kotlin
val chain1 = WorkManager.getInstance(context).beginWith(work1A).then(work1B)
val chain2 = WorkManager.getInstance(context).beginWith(work2A).then(work2B)

val finalWork = OneTimeWorkRequestBuilder<FinalWorker>().build()

WorkContinuation.combine(listOf(chain1, chain2))
    .then(finalWork)
    .enqueue()
```

## Unique Work

### Replace Existing Work

```kotlin
WorkManager.getInstance(context)
    .enqueueUniqueWork(
        "daily_sync",
        ExistingWorkPolicy.REPLACE,
        syncRequest
    )
```

### Keep Existing Work

```kotlin
WorkManager.getInstance(context)
    .enqueueUniqueWork(
        "upload_${fileId}",
        ExistingWorkPolicy.KEEP,
        uploadRequest
    )
```

### Append to Existing Work

```kotlin
WorkManager.getInstance(context)
    .enqueueUniqueWork(
        "sync_chain",
        ExistingWorkPolicy.APPEND,
        newSyncRequest
    )
```

### Unique Periodic Work

```kotlin
WorkManager.getInstance(context)
    .enqueueUniquePeriodicWork(
        "periodic_sync",
        ExistingPeriodicWorkPolicy.KEEP,
        periodicRequest
    )
```

## Observing Work

### By ID

```kotlin
WorkManager.getInstance(context)
    .getWorkInfoByIdLiveData(workRequest.id)
    .observe(lifecycleOwner) { workInfo ->
        when (workInfo?.state) {
            WorkInfo.State.ENQUEUED -> showStatus("Queued")
            WorkInfo.State.RUNNING -> showStatus("Running")
            WorkInfo.State.SUCCEEDED -> {
                showStatus("Success")
                val outputUrl = workInfo.outputData.getString(KEY_UPLOADED_URL)
                handleSuccess(outputUrl)
            }
            WorkInfo.State.FAILED -> showStatus("Failed")
            WorkInfo.State.BLOCKED -> showStatus("Blocked")
            WorkInfo.State.CANCELLED -> showStatus("Cancelled")
            null -> showStatus("Unknown")
        }
    }
```

### By Tag

```kotlin
val request = OneTimeWorkRequestBuilder<SyncWorker>()
    .addTag("sync")
    .build()

WorkManager.getInstance(context)
    .getWorkInfosByTagLiveData("sync")
    .observe(lifecycleOwner) { workInfos ->
        val running = workInfos.count { it.state == WorkInfo.State.RUNNING }
        updateUI("$running sync tasks running")
    }
```

### By Unique Name

```kotlin
WorkManager.getInstance(context)
    .getWorkInfosForUniqueWorkLiveData("daily_sync")
    .observe(lifecycleOwner) { workInfos ->
        // Handle work info list
    }
```

### Using Flow (Coroutines)

```kotlin
WorkManager.getInstance(context)
    .getWorkInfoByIdFlow(workId)
    .collect { workInfo ->
        when (workInfo?.state) {
            WorkInfo.State.SUCCEEDED -> handleSuccess()
            WorkInfo.State.FAILED -> handleFailure()
            else -> {}
        }
    }
```

## Cancelling Work

```kotlin
// Cancel by ID
WorkManager.getInstance(context).cancelWorkById(workId)

// Cancel by tag
WorkManager.getInstance(context).cancelAllWorkByTag("sync")

// Cancel by unique name
WorkManager.getInstance(context).cancelUniqueWork("daily_sync")

// Cancel all work
WorkManager.getInstance(context).cancelAllWork()
```

## Testing

See [references/testing.md](references/testing.md) for complete testing guide including TestWorkerFactory and WorkManagerTestInitHelper.

Quick test example:

```kotlin
@Test
fun testSyncWorker() = runTest {
    val context = ApplicationProvider.getApplicationContext<Context>()
    val executor = Executors.newSingleThreadExecutor()

    WorkManagerTestInitHelper.initializeTestWorkManager(context)

    val worker = TestListenableWorkerBuilder<SyncWorker>(context).build()

    val result = worker.doWork()

    assertThat(result).isEqualTo(Result.success())
}
```

## Dependency Injection

### With Metro DI

```kotlin
// Define factory in DI graph
@ModuleScope
class WorkerFactory(
    private val syncRepository: SyncRepository,
    private val uploadService: UploadService
) : WorkerFactory() {

    override fun createWorker(
        appContext: Context,
        workerClassName: String,
        workerParameters: WorkerParameters
    ): ListenableWorker? {
        return when (workerClassName) {
            SyncWorker::class.java.name ->
                SyncWorker(appContext, workerParameters, syncRepository)

            UploadWorker::class.java.name ->
                UploadWorker(appContext, workerParameters, uploadService)

            else -> null
        }
    }
}

// In Application onCreate
class MyApplication : Application(), Configuration.Provider {

    private lateinit var workerFactory: WorkerFactory

    override fun onCreate() {
        super.onCreate()

        // Get factory from DI
        workerFactory = AppGraph.workerFactory
    }

    override val workManagerConfiguration: Configuration
        get() = Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .build()
}

// Worker with dependencies
class SyncWorker(
    context: Context,
    params: WorkerParameters,
    private val repository: SyncRepository
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        return try {
            repository.sync()
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
}
```

## Important Limitations

### Timing Constraints

- **Minimum periodic interval**: 15 minutes
- **Flex interval**: Must be >= 5 minutes and < repeat interval
- **Not for exact timing**: WorkManager is not AlarmManager - execution time is approximate
- **Doze mode delays**: Work can be significantly delayed when device is in doze mode

### Execution Constraints

- **10-minute execution limit**: Workers should complete within 10 minutes
- **Background execution limits**: Subject to Android's background execution limits
- **CoroutineWorker scope**: Uses default Dispatchers.Default, not main thread
- **No guarantee of immediate execution**: Work is scheduled optimally by system

### Data Limitations

- **Input/Output data size**: Limited to 10KB
- **Primitive types only**: WorkData supports only primitives, arrays, and strings
- **No complex objects**: Cannot pass custom objects directly
- **Use serialization**: For complex data, serialize to JSON string or use file paths

### Worker Lifecycle

- **Worker is recreated**: Each execution creates a new Worker instance
- **No shared state**: Cannot rely on instance variables between executions
- **Context is Application**: Worker's context is always Application context, not Activity
- **RunAttemptCount**: Increments on each retry, resets on success

### Device and System Constraints

- **Battery optimization**: Can be affected by manufacturer-specific battery optimizations
- **App standby buckets**: Work frequency limited by app's standby bucket
- **Background restrictions**: Some manufacturers aggressively kill background work
- **Requires Google Play Services**: WorkManager relies on Google Play Services JobScheduler

## Best Practices

### Do's

- Use `CoroutineWorker` for suspend functions
- Set appropriate constraints for network/battery requirements
- Use `setBackoffCriteria()` for custom retry strategies
- Tag work requests for easier management
- Use unique work names to prevent duplicate tasks
- Return `Result.retry()` for transient failures
- Implement proper error handling and logging
- Use `setForeground()` for long-running work (>10 min)

### Don'ts

- Don't use WorkManager for immediate execution
- Don't expect precise scheduling
- Don't pass large data through WorkData (use file URIs)
- Don't block main thread in Worker
- Don't rely on Worker instance state
- Don't schedule periodic work < 15 minutes
- Don't forget to cancel work when no longer needed
- Don't use for foreground services (use actual Service)

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for detailed solutions to common problems.

Common issues:
- Work not executing
- Constraints not working as expected
- Work retrying indefinitely
- DI not working in Workers
- Testing failures

## Resources

- [Official Documentation](https://developer.android.com/topic/libraries/architecture/workmanager)
- [WorkManager Codelab](https://developer.android.com/codelabs/android-workmanager)
- [Background Work Guide](https://developer.android.com/guide/background)
