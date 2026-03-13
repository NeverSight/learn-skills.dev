---
name: electrobun-rpc-patterns
description: Advanced type-safe RPC patterns for Electrobun desktop applications. Covers bidirectional main↔webview communication, type safety with TypeScript, error handling and validation, performance optimization, streaming data patterns, batch operations, retry strategies, event-based communication, shared type definitions, RPC middleware, request/response patterns, and complex data synchronization. Use this skill when implementing complex communication between main and webview processes, need type-safe RPC with full IntelliSense, handling large data transfers, implementing real-time updates, building type-safe APIs between processes, debugging RPC issues, optimizing RPC performance, or implementing advanced patterns like streaming, batching, or pub/sub. Triggers include "RPC", "main webview communication", "type-safe RPC", "bidirectional RPC", "RPC performance", "RPC error handling", "shared types", "process communication", or "IPC patterns".
license: MIT
metadata:
  author: Blackboard
  version: "1.0.0"
---

# Electrobun RPC Patterns

Advanced patterns for type-safe, performant RPC communication in Electrobun.

## Type-Safe RPC

### Shared Types Definition

Create a shared types file that both main and webview can import:

**src/types/rpc.ts:**
```ts
// Main process handlers (exposed to webview)
export interface MainRpcHandlers {
  getUser(id: string): Promise<User>;
  saveFile(path: string, content: string): Promise<SaveResult>;
  listFiles(directory: string): Promise<FileInfo[]>;
  executeCommand(cmd: string, args: string[]): Promise<CommandResult>;
}

// Webview handlers (exposed to main)
export interface WebviewRpcHandlers {
  updateUI(data: UIUpdate): Promise<void>;
  showNotification(message: string, type: NotificationType): Promise<void>;
  refreshData(): Promise<void>;
}

export interface User {
  id: string;
  name: string;
  email: string;
}

export interface SaveResult {
  success: boolean;
  path?: string;
  error?: string;
}

export interface FileInfo {
  name: string;
  path: string;
  size: number;
  modified: Date;
}

export interface CommandResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

export interface UIUpdate {
  type: "data" | "status" | "error";
  payload: any;
}

export type NotificationType = "info" | "success" | "warning" | "error";
```

### Type-Safe Main Process

**src/bun/main.ts:**
```ts
import { BrowserWindow } from "electrobun/bun";
import type { MainRpcHandlers, WebviewRpcHandlers } from "../types/rpc";

const win = new BrowserWindow({ /* ... */ });

// Define handlers with type checking
win.defineRpc<MainRpcHandlers>({
  handlers: {
    async getUser(id: string) {
      // Full type inference and checking
      const user = await database.users.findById(id);
      return {
        id: user.id,
        name: user.name,
        email: user.email,
      };
    },
    
    async saveFile(path: string, content: string) {
      try {
        await Bun.write(path, content);
        return { success: true, path };
      } catch (error) {
        return { success: false, error: error.message };
      }
    },
    
    async listFiles(directory: string) {
      const entries = await fs.readdir(directory, { withFileTypes: true });
      return entries.map(entry => ({
        name: entry.name,
        path: path.join(directory, entry.name),
        size: entry.size,
        modified: entry.mtime,
      }));
    },
    
    async executeCommand(cmd: string, args: string[]) {
      const proc = Bun.spawn([cmd, ...args]);
      const stdout = await new Response(proc.stdout).text();
      const stderr = await new Response(proc.stderr).text();
      const exitCode = await proc.exited;
      
      return { stdout, stderr, exitCode };
    }
  }
});

// Call webview methods with types
const webviewRpc = win.rpc as WebviewRpcHandlers;
await webviewRpc.updateUI({ type: "data", payload: data });
await webviewRpc.showNotification("File saved", "success");
```

### Type-Safe Webview

**src/views/mainview/index.ts:**
```ts
import { Electroview } from "electrobun/browser";
import type { MainRpcHandlers, WebviewRpcHandlers } from "../../types/rpc";

const electroview = new Electroview();

// Type-safe RPC calls to main
const mainRpc = electroview.rpc as MainRpcHandlers;

async function loadUser(id: string) {
  // Full IntelliSense and type checking
  const user = await mainRpc.getUser(id);
  console.log(user.name, user.email);
}

async function saveDocument(path: string, content: string) {
  const result = await mainRpc.saveFile(path, content);
  if (result.success) {
    await mainRpc.showNotification("File saved successfully", "success");
  } else {
    console.error("Save failed:", result.error);
  }
}

// Define webview handlers with types
electroview.defineRpc<WebviewRpcHandlers>({
  handlers: {
    async updateUI(data) {
      if (data.type === "data") {
        renderData(data.payload);
      } else if (data.type === "error") {
        showError(data.payload);
      }
    },
    
    async showNotification(message, type) {
      const notification = document.createElement("div");
      notification.className = `notification ${type}`;
      notification.textContent = message;
      document.body.appendChild(notification);
      
      setTimeout(() => notification.remove(), 3000);
    },
    
    async refreshData() {
      const data = await mainRpc.getData();
      renderData(data);
    }
  }
});
```

## Error Handling

### Robust Error Handling Pattern

```ts
// Custom error types
class RpcError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: any
  ) {
    super(message);
    this.name = "RpcError";
  }
}

class ValidationError extends RpcError {
  constructor(message: string, details?: any) {
    super(message, "VALIDATION_ERROR", details);
  }
}

class NotFoundError extends RpcError {
  constructor(resource: string) {
    super(`${resource} not found`, "NOT_FOUND");
  }
}

// Main process with error handling
win.defineRpc({
  handlers: {
    async getUser(id: string) {
      // Validate input
      if (!id || typeof id !== "string") {
        throw new ValidationError("Invalid user ID", { id });
      }
      
      const user = await database.users.findById(id);
      
      if (!user) {
        throw new NotFoundError("User");
      }
      
      return user;
    },
    
    async saveFile(path: string, content: string) {
      try {
        // Validate path
        if (path.includes("..")) {
          throw new ValidationError("Invalid file path");
        }
        
        await Bun.write(path, content);
        return { success: true };
      } catch (error) {
        if (error instanceof RpcError) {
          throw error;
        }
        
        // Wrap unknown errors
        throw new RpcError(
          "Failed to save file",
          "SAVE_ERROR",
          { originalError: error.message }
        );
      }
    }
  }
});

// Webview with error handling
async function loadUser(id: string) {
  try {
    const user = await mainRpc.getUser(id);
    displayUser(user);
  } catch (error) {
    if (error.code === "NOT_FOUND") {
      showError("User not found");
    } else if (error.code === "VALIDATION_ERROR") {
      showError("Invalid input");
    } else {
      showError("Failed to load user");
      console.error(error);
    }
  }
}
```

### Retry Strategy

```ts
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  delay = 1000
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries - 1) {
        throw error;
      }
      
      console.warn(`Attempt ${attempt + 1} failed, retrying...`);
      await new Promise(resolve => setTimeout(resolve, delay * (attempt + 1)));
    }
  }
  
  throw new Error("Max retries exceeded");
}

// Usage in webview
const user = await withRetry(() => mainRpc.getUser(id));
```

## Performance Optimization

### Batching Requests

```ts
class BatchRpc {
  private batch: Array<{
    method: string;
    args: any[];
    resolve: (value: any) => void;
    reject: (error: any) => void;
  }> = [];
  
  private batchTimeout: Timer | null = null;
  private readonly batchDelay = 10; // ms
  
  constructor(private rpc: any) {}
  
  async call(method: string, ...args: any[]) {
    return new Promise((resolve, reject) => {
      this.batch.push({ method, args, resolve, reject });
      
      if (!this.batchTimeout) {
        this.batchTimeout = setTimeout(() => this.flush(), this.batchDelay);
      }
    });
  }
  
  private async flush() {
    if (this.batch.length === 0) return;
    
    const currentBatch = this.batch.splice(0);
    this.batchTimeout = null;
    
    try {
      const results = await this.rpc.executeBatch(
        currentBatch.map(({ method, args }) => ({ method, args }))
      );
      
      currentBatch.forEach((item, index) => {
        if (results[index].error) {
          item.reject(results[index].error);
        } else {
          item.resolve(results[index].result);
        }
      });
    } catch (error) {
      currentBatch.forEach(item => item.reject(error));
    }
  }
}

// Main process batch handler
win.defineRpc({
  handlers: {
    async executeBatch(requests: Array<{ method: string; args: any[] }>) {
      return await Promise.all(
        requests.map(async ({ method, args }) => {
          try {
            const result = await this.handlers[method](...args);
            return { result };
          } catch (error) {
            return { error: error.message };
          }
        })
      );
    }
  }
});

// Usage
const batchRpc = new BatchRpc(mainRpc);
const [user1, user2, user3] = await Promise.all([
  batchRpc.call("getUser", "1"),
  batchRpc.call("getUser", "2"),
  batchRpc.call("getUser", "3"),
]);
```

### Caching Layer

```ts
class CachedRpc {
  private cache = new Map<string, { data: any; timestamp: number }>();
  private readonly ttl = 60000; // 1 minute
  
  constructor(private rpc: any) {}
  
  async call(method: string, ...args: any[]) {
    const cacheKey = `${method}:${JSON.stringify(args)}`;
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.ttl) {
      return cached.data;
    }
    
    const result = await this.rpc[method](...args);
    this.cache.set(cacheKey, { data: result, timestamp: Date.now() });
    
    return result;
  }
  
  invalidate(method?: string) {
    if (method) {
      // Invalidate specific method
      for (const [key] of this.cache) {
        if (key.startsWith(method + ":")) {
          this.cache.delete(key);
        }
      }
    } else {
      // Invalidate all
      this.cache.clear();
    }
  }
}

// Usage
const cachedRpc = new CachedRpc(mainRpc);
const user = await cachedRpc.call("getUser", id); // Fetches
const user2 = await cachedRpc.call("getUser", id); // Cached
```

## Streaming Data

### Chunk-based Streaming

```ts
// Main process - stream large data in chunks
win.defineRpc({
  handlers: {
    async* streamFile(path: string, chunkSize = 1024 * 64) {
      const file = Bun.file(path);
      const reader = file.stream().getReader();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        yield {
          chunk: Array.from(value),
          progress: (file.size - reader.closed) / file.size
        };
      }
    },
    
    async streamLogs(processId: string) {
      const process = processes.get(processId);
      const reader = process.stdout.getReader();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        yield { line: new TextDecoder().decode(value) };
      }
    }
  }
});

// Webview - consume stream
for await (const chunk of mainRpc.streamFile("/large/file.dat")) {
  processChunk(chunk.chunk);
  updateProgress(chunk.progress);
}
```

### Event-Based Updates

```ts
// Main process - emit events
class DataService {
  private listeners = new Set<(data: any) => void>();
  
  subscribe(callback: (data: any) => void) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }
  
  emit(data: any) {
    this.listeners.forEach(cb => cb(data));
  }
  
  async watch(path: string) {
    const watcher = fs.watch(path);
    
    for await (const event of watcher) {
      this.emit({ type: "file-change", path, event });
    }
  }
}

const dataService = new DataService();

win.defineRpc({
  handlers: {
    async subscribeToUpdates() {
      const unsubscribe = dataService.subscribe(async (data) => {
        await win.rpc.handleUpdate(data);
      });
      
      return { success: true };
    }
  }
});

// Webview - handle updates
electroview.defineRpc({
  handlers: {
    async handleUpdate(data: any) {
      console.log("Received update:", data);
      updateUI(data);
    }
  }
});

// Subscribe
await mainRpc.subscribeToUpdates();
```

## Advanced Patterns

### Request/Response Correlation

```ts
class CorrelatedRpc {
  private pending = new Map<string, {
    resolve: (value: any) => void;
    reject: (error: any) => void;
    timeout: Timer;
  }>();
  
  private requestId = 0;
  
  constructor(private electroview: any) {
    electroview.defineRpc({
      handlers: {
        handleResponse: async (id: string, result: any, error: any) => {
          const pending = this.pending.get(id);
          if (!pending) return;
          
          clearTimeout(pending.timeout);
          this.pending.delete(id);
          
          if (error) {
            pending.reject(error);
          } else {
            pending.resolve(result);
          }
        }
      }
    });
  }
  
  async call(method: string, ...args: any[]) {
    const id = `req-${++this.requestId}`;
    
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error("Request timeout"));
      }, 30000);
      
      this.pending.set(id, { resolve, reject, timeout });
      
      this.electroview.rpc.sendRequest(id, method, args);
    });
  }
}
```

### Bi-directional Sync

```ts
class DataSync {
  private localData: any = {};
  private syncing = false;
  
  constructor(
    private mainRpc: any,
    private electroview: any
  ) {
    this.setupHandlers();
  }
  
  private setupHandlers() {
    this.electroview.defineRpc({
      handlers: {
        syncFromMain: async (data: any) => {
          if (!this.syncing) {
            this.localData = data;
            this.render();
          }
        }
      }
    });
  }
  
  async syncToMain() {
    this.syncing = true;
    try {
      const serverData = await this.mainRpc.updateData(this.localData);
      this.localData = serverData;
      this.render();
    } finally {
      this.syncing = false;
    }
  }
  
  async pull() {
    const serverData = await this.mainRpc.getData();
    this.localData = serverData;
    this.render();
  }
  
  private render() {
    // Update UI with localData
  }
}
```

## Resources

For more on Electrobun:
- **Core skill**: `electrobun` - Basic RPC setup
- **Window management**: `electrobun-window-management` - Window-to-window RPC
- **Debugging**: `electrobun-debugging` - Debug RPC issues
