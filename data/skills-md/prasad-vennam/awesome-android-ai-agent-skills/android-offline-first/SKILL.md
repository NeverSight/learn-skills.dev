---
name: android-offline-first
description: "Use when implementing local data persistence, offline synchronization, or background data fetching for Android."
category: architecture
risk: low
source: community
date_added: "2026-03-31"
metadata:
  triggers:
    - "@offline-first"
    - "room-database"
    - "work-manager"
    - "offline-sync"
    - "local-first"
---

# Android Offline-First Excellence 📶🛡️

Standard patterns for architecting professional-grade Android applications that are resilient to poor network conditions and function seamlessly offline.

## ⚡ When to Use
- **Local Persistence**: Caching API responses in Room.
- **Sync Logic**: Synchronizing local changes with remote APIs.
- **Background Work**: Using WorkManager for data-heavy tasks.
- **Reliable Data Fetching**: Building "SSOT" (Single Source of Truth) repositories.
- **Conflict Resolution**: Managing data versioning between local and remote.

## 🏗️ The Single Source of Truth (SSOT)

- **Rule**: The UI ALWAYS reads from the Local Database (Room).
- **Rule**: The Network Layer ALWAYS writes to the Local Database (Room).
- **Architecture**:
  ```kotlin
  class MyRepository(
      private val localSource: RoomDao,
      private val remoteSource: APIInterface
  ) {
      fun getItems(): Flow<List<Item>> = localSource.observeAll()

      suspend fun refreshItems() {
          val items = remoteSource.fetchItems()
          localSource.insertAll(items) // UI updates automatically via Flow
      }
  }
  ```
- **Advanced (Paging 3)**: For large lists, you MUST use `RemoteMediator`. The RemoteMediator intercepts the pagination request, fetches the remote page, dumps it into Room, and signals the `PagingSource` to re-read from the DB.

## 🛠️ Essential Tools

### 1. Room (SQL Persistence)
- Use **Kotlin Flows** for observing database changes.
- Use **Transactions** for atomic operations.
- Always implement **Migrations** for schema changes.

### 2. WorkManager (Guaranteed Execution)
- Use for tasks that MUST complete even if the app closes (e.g., uploading a post).
- Set constraints: `NetworkType.CONNECTED`, `RequiresCharging(true)`.

### 3. DataStore (Key-Value)
- Use for user preferences, simple settings, or session tokens.
- Choose `Preferences DataStore` or `Proto DataStore` (Type-safe).

## 🚀 Sync Strategies

- **On Demand**: Refresh data when the user opens the screen.
- **Periodic Sync**: Use WorkManager to sync data every few hours.
- **Immediate Push**: Sync with network changes via a BroadcastReceiver or callback.

## 📦 Data Resiliency Checklist

- [ ] **Error Handling**: Differentiate between network errors (Retry later) and server errors (Alert user).
- [ ] **Optimistic UI**: Update the local state immediately, then sync with the server in the background.
- [ ] **Data Expiration**: Add `timestamp` to local entries to decide when to refresh from the network.
- [ ] **Conflict Resolution**: Use `onConflict = OnConflictStrategy.REPLACE` or custom logic based on "last modified" fields.

## 🧪 Testing and Verification

- **Room Tests**: Test migrations and DAO queries in a separate `androidTest`.
- **WorkManager Tests**: Use `WorkManagerTestInitHelper` for unit testing workers.
- **Network Simulation**: Manually test the app in "Airplane Mode".

## 🔗 Related Resources
- [Android Offline-First Guide](https://developer.android.com/topic/architecture/data-layer/offline-first)
- [Clean Architecture Skill](../android-clean-architecture/SKILL.md)
