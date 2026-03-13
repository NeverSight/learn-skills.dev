---
name: offline-sync-designer
description: Design local-first architectures and offline sync strategies. Determine conflict resolution policies, implement optimistic UI updates, and architect robust background data synchronization.
---

# Offline Sync Designer Protocol

Mobile networks are inherently unreliable. Users get on subways, drive through tunnels, or experience network drops. A modern app must not block the user's UI with an infinite spinner when the network fails. This skill designs local-first data layers that feel instant, syncing data quietly in the background.

**Core principle:** Read from local, Write to local, Sync to remote.

---

## Workflow

```
1. Map the data domains (What needs to be available offline?)
2. Select the local storage mechanism
3. UI State Strategy (Optimistic vs. Pessimistic updates)
4. Design the Conflict Resolution Policy
5. Define the Background Sync Mechanism
```

---

## Step 1: Data Domain Mapping
Categorize the app's data:
- **Critical & Mutating:** User-generated content (notes, messages, tasks). Must be available offline and syncable.
- **Reference Data:** Catalogs, settings. Can be cached periodically; read-only for the client.
- **Ephemeral/Live:** Stock tickers, live video streams. Irrelevant offline. Apply aggressive timeouts.

## Step 2: Storage Mechanism Selection
Choose the right tool for the job. Do NOT use `AsyncStorage` or `SharedPreferences` for complex relational queries.
- **Key-Value Cache:** MMKV, AsyncStorage (React Native) / SharedPreferences, DataStore (Native). Good for user tokens, theme prefs.
- **Relational / Document DB:** SQLite, WatermelonDB, Realm, CoreData/Room. Good for lists of objects, offline searching.

## Step 3: UI State Strategy
Define how the UI reacts to user actions.
- **Optimistic Update (Default for Local-First):** User clicks "Like". UI updates instantly. Data is saved locally. A background task is queued to tell the server. If server fails, task retries later. UI rarely reverts.
- **Pessimistic Update (For high-stakes data):** User clicks "Transfer $100". UI shows a spinner locking the action. Must wait for the server.

## Step 4: Conflict Resolution Policy
What happens when the client edits a document offline, but the server version was also changed by someone else?
- **Client Wins:** Overwrite server. (Dangerous, acceptable for single-user apps).
- **Server Wins:** Discard mobile changes. (Used for reference data).
- **Last Write Wins (LWW):** Compare timestamps. (Requires accurate clock sync).
- **Merge / CRDT:** Conflict-free Replicated Data Types. Complex, used for collaborative editing (e.g., Google Docs style). Provide guidance if they need this path.

## Step 5: Background Sync Mechanism
How does the queued data get to the server when the user closes the app?
- **iOS:** Background App Refresh, `BGTaskScheduler`.
- **Android:** WorkManager (respects Doze mode, guarantees execution).

---

## Output Format

```markdown
# 🔄 Offline Sync & Local-First Architecture

## 🗄 Storage & Domain Strategy
- **Data Domains to Cache:** [e.g., User Profile, Task List]
- **Recommended DB:** [e.g., WatermelonDB for React Native]

## ⚡ UI State Handling (Optimistic Updates)
**Scenario:** [User creates a new task while offline]
1. **Action:** Generate UUID on client.
2. **Local DB:** Save Task with `sync_status = 'pending'`.
3. **UI:** Update list instantly.
4. **Queue:** Push to local sync queue.

## ⚔️ Conflict Resolution Strategy
**Policy:** [e.g., Last Write Wins (LWW)]
**Implementation:** 
- Every database row requires an `updated_at` (Epoch timestamp).
- On sync, the server compares the client's `updated_at` against the DB's `updated_at`. If client is newer, it overwrites. If older, server sends the newer record down to the client.

## 📡 Background Sync Mechanism
- **Foreground:** Attempt sync immediately when network is restored (listen to `NetInfo` / `ConnectivityManager`).
- **Background:** [Detail the WorkManager / BGTaskScheduler implementation logic].
```

---

## When to Skip
- The user is asking about caching small amounts of text for 5 minutes (use HTTP caching headers / React Query). This skill is for architectural *local-first* designs.

---

## Guardrails
- **UUIDs, not Auto-Increment:** Always instruct the dev to generate UUIDv4 (or UUIDv7) on the client, NEVER rely on the server's auto-incrementing integer IDs for offline-created objects. 
- **Timestamps:** Relying on the device's local clock for `updated_at` is dangerous (users change their clocks). Advise using server-calculated offsets if high accuracy is needed, or state the risk.

---

## References
See `references/EXAMPLES.md` for a worked case.
