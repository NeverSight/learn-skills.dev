---
name: electrobun-debugging
description: Development workflow, debugging, and troubleshooting for Electrobun desktop applications. This skill covers debugging the main process (Bun) and webview processes, Chrome DevTools integration, console logging strategies, error handling, performance profiling, memory leak detection, build error troubleshooting, common runtime errors, development environment setup, hot reload configuration, source maps, breakpoint debugging, network inspection, WebView debugging on different platforms, native module debugging, and systematic debugging approaches. Use when encountering build failures, runtime errors, crashes, performance issues, debugging RPC communication, inspecting webview DOM, profiling CPU/memory usage, troubleshooting platform-specific issues, or setting up development workflow. Triggers include "debug", "error", "crash", "troubleshoot", "DevTools", "inspect", "breakpoint", "profiling", "performance issue", "build error", "not working", or "logging".
license: MIT
metadata:
  author: Blackboard
  version: "1.0.0"
---

# Electrobun Debugging

Comprehensive debugging and troubleshooting guide for Electrobun applications.

## Development Environment

### Basic Development Setup

```bash
# Development mode with hot reload
bun run dev

# Development mode with verbose logging
DEBUG=* bun run dev

# Development mode with specific debug namespace
DEBUG=electrobun:* bun run dev
```

### Environment Configuration

**.env.development:**
```bash
# Enable development features
NODE_ENV=development
DEBUG=electrobun:*

# DevTools always open
ELECTRON_ENABLE_DEVTOOLS=1

# Disable security warnings in dev
ELECTRON_DISABLE_SECURITY_WARNINGS=true

# Custom dev server port
DEV_SERVER_PORT=3000
```

## Debugging Main Process

### Console Logging

```ts
// Main process logs appear in terminal
console.log("Main process started");
console.error("Error in main process");
console.warn("Warning in main process");

// Structured logging
const logger = {
  debug: (msg: string, data?: any) => {
    if (process.env.DEBUG) {
      console.log(`[DEBUG] ${msg}`, data || "");
    }
  },
  info: (msg: string, data?: any) => {
    console.log(`[INFO] ${msg}`, data || "");
  },
  error: (msg: string, error?: any) => {
    console.error(`[ERROR] ${msg}`, error || "");
    if (error?.stack) {
      console.error(error.stack);
    }
  }
};

logger.info("Window created", { width: 1200, height: 800 });
logger.error("Failed to load file", error);
```

### Bun Debugger

```bash
# Start with Bun debugger
bun --inspect run dev

# With breakpoint on first line
bun --inspect-brk run dev

# Connect with Chrome DevTools
# Open chrome://inspect in Chrome
# Click "inspect" on your process
```

### Error Handling in Main

```ts
// Global error handlers
process.on("uncaughtException", (error) => {
  logger.error("Uncaught exception", error);
  
  // Show error dialog
  dialog.showMessageBox({
    type: "error",
    title: "Application Error",
    message: "An unexpected error occurred",
    detail: error.message,
  });
  
  // Optional: restart or quit
  // app.relaunch();
  // app.quit();
});

process.on("unhandledRejection", (reason, promise) => {
  logger.error("Unhandled rejection", { reason, promise });
});

// Window error handler
win.on("error", (error) => {
  logger.error("Window error", error);
});

// RPC error handling
win.defineRpc({
  handlers: {
    async someHandler(args: any) {
      try {
        // Handler logic
        return { success: true };
      } catch (error) {
        logger.error("RPC handler error", error);
        throw error; // Re-throw to send to webview
      }
    }
  }
});
```

## Debugging Webview

### Chrome DevTools

```ts
// Open DevTools programmatically
win.openDevTools();

// Open DevTools detached
win.openDevTools({ mode: "detach" });

// Toggle DevTools
win.toggleDevTools();

// Close DevTools
win.closeDevTools();

// Menu item to toggle DevTools
{
  label: "Toggle Developer Tools",
  accelerator: "CmdOrCtrl+Shift+I",
  action: () => win.toggleDevTools()
}
```

### Console Logging in Webview

```ts
// Webview console logs appear in DevTools
console.log("Webview initialized");
console.error("Error in webview");
console.warn("Warning in webview");
console.table({ user: "Alice", age: 30 });

// Custom logger
const logger = {
  log: (msg: string, ...args: any[]) => {
    console.log(`[${new Date().toISOString()}] ${msg}`, ...args);
  },
  group: (label: string) => {
    console.group(label);
  },
  groupEnd: () => {
    console.groupEnd();
  }
};

logger.group("User Login");
logger.log("Validating credentials");
logger.log("Fetching user data");
logger.groupEnd();
```

### Capturing Webview Errors

```ts
// Global error handler
window.addEventListener("error", (event) => {
  console.error("Uncaught error:", event.error);
  
  // Send to main process for logging
  electroview.rpc.logError({
    message: event.error.message,
    stack: event.error.stack,
    url: event.filename,
    line: event.lineno,
    column: event.colno,
  });
});

// Unhandled promise rejections
window.addEventListener("unhandledrejection", (event) => {
  console.error("Unhandled rejection:", event.reason);
  
  electroview.rpc.logError({
    message: "Unhandled rejection",
    reason: event.reason,
  });
});

// Main process handler
win.defineRpc({
  handlers: {
    async logError(error: any) {
      logger.error("Webview error", error);
      
      // Optional: save to file
      await saveErrorLog(error);
    }
  }
});
```

## Debugging RPC Communication

### RPC Logging

```ts
// Main process RPC logger
class RpcLogger {
  wrap(handlers: any) {
    const wrapped: any = {};
    
    for (const [name, handler] of Object.entries(handlers)) {
      wrapped[name] = async (...args: any[]) => {
        const callId = Math.random().toString(36).slice(2);
        
        logger.debug(`[RPC:${callId}] → ${name}`, args);
        const startTime = Date.now();
        
        try {
          const result = await (handler as Function)(...args);
          const duration = Date.now() - startTime;
          logger.debug(`[RPC:${callId}] ← ${name} (${duration}ms)`, result);
          return result;
        } catch (error) {
          const duration = Date.now() - startTime;
          logger.error(`[RPC:${callId}] ✗ ${name} (${duration}ms)`, error);
          throw error;
        }
      };
    }
    
    return wrapped;
  }
}

const rpcLogger = new RpcLogger();

win.defineRpc({
  handlers: rpcLogger.wrap({
    async getUser(id: string) {
      return await database.users.findById(id);
    },
    async saveFile(path: string, content: string) {
      await Bun.write(path, content);
      return { success: true };
    }
  })
});
```

### Testing RPC in DevTools

```ts
// In webview DevTools console:

// Test RPC call
await electroview.rpc.getUser("123")

// Test error handling
try {
  await electroview.rpc.invalidMethod()
} catch (error) {
  console.error("Expected error:", error);
}

// Measure RPC performance
console.time("RPC call");
const result = await electroview.rpc.getUser("123");
console.timeEnd("RPC call");
```

## Performance Profiling

### CPU Profiling

```ts
// Main process CPU profiling
const { performance, PerformanceObserver } = require("perf_hooks");

const obs = new PerformanceObserver((items) => {
  items.getEntries().forEach(entry => {
    logger.debug(`${entry.name}: ${entry.duration}ms`);
  });
});

obs.observe({ entryTypes: ["measure"] });

// Measure operation
performance.mark("operation-start");
await expensiveOperation();
performance.mark("operation-end");
performance.measure("operation", "operation-start", "operation-end");
```

**Webview CPU profiling:**
```ts
// Use Chrome DevTools Performance tab
// Or programmatically:
console.profile("My Operation");
await performOperation();
console.profileEnd("My Operation");

// Simple timing
const start = performance.now();
await operation();
const duration = performance.now() - start;
console.log(`Operation took ${duration}ms`);
```

### Memory Profiling

```ts
// Main process memory usage
function logMemoryUsage() {
  const usage = process.memoryUsage();
  logger.info("Memory usage", {
    heapUsed: `${Math.round(usage.heapUsed / 1024 / 1024)}MB`,
    heapTotal: `${Math.round(usage.heapTotal / 1024 / 1024)}MB`,
    external: `${Math.round(usage.external / 1024 / 1024)}MB`,
    rss: `${Math.round(usage.rss / 1024 / 1024)}MB`,
  });
}

// Monitor memory over time
setInterval(logMemoryUsage, 10000);

// Force garbage collection (development only)
if (global.gc) {
  global.gc();
  logMemoryUsage();
}
```

**Webview memory profiling:**
```ts
// Use Chrome DevTools Memory tab
// Or programmatically:
if (performance.memory) {
  console.log("Memory:", {
    used: `${Math.round(performance.memory.usedJSHeapSize / 1024 / 1024)}MB`,
    total: `${Math.round(performance.memory.totalJSHeapSize / 1024 / 1024)}MB`,
    limit: `${Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024)}MB`,
  });
}
```

## Common Issues & Solutions

### Build Errors

**Issue: "Cannot find module 'electrobun'"**
```bash
# Solution: Install dependencies
bun install

# Verify electrobun is installed
bun pm ls electrobun
```

**Issue: Native module compilation fails**
```bash
# macOS: Install Xcode Command Line Tools
xcode-select --install

# Windows: Install Visual Studio Build Tools
# Download from visualstudio.microsoft.com

# Linux: Install build essentials
sudo apt install build-essential
```

**Issue: "WebView2 not found" (Windows)**
```bash
# Install WebView2 Runtime
# Download from microsoft.com/edge/webview2
```

### Runtime Errors

**Issue: Window not showing**
```ts
// Debug checklist:
// 1. Check window is created
console.log("Window created:", win);

// 2. Explicitly show window
win.show();

// 3. Check window bounds
console.log("Window bounds:", win.getBounds());

// 4. Check if window is minimized/hidden
console.log("Window visible:", win.isVisible());
console.log("Window minimized:", win.isMinimized());
```

**Issue: RPC not working**
```ts
// Debug checklist:
// 1. Verify RPC handlers defined
console.log("RPC handlers:", Object.keys(handlers));

// 2. Check webview loaded
win.on("did-finish-load", () => {
  console.log("Webview loaded");
});

// 3. Test RPC with try-catch
try {
  const result = await electroview.rpc.testMethod();
  console.log("RPC working:", result);
} catch (error) {
  console.error("RPC error:", error);
}

// 4. Check for CORS issues in webview
// 5. Verify Electroview initialized in webview
```

**Issue: High memory usage**
```ts
// Common causes:
// 1. Memory leaks from event listeners
window.removeEventListener("resize", handler);

// 2. Large data stored in closures
// Use WeakMap/WeakSet for object references

// 3. Not cleaning up resources
win.on("close", () => {
  // Clean up timers
  clearInterval(intervalId);
  // Close connections
  ws.close();
  // Release resources
  cache.clear();
});
```

### Platform-Specific Issues

**macOS:**
```ts
// Issue: App won't open (Gatekeeper)
// Solution: Code sign and notarize

// Issue: Permissions denied
// Solution: Add Info.plist entries
<key>NSCameraUsageDescription</key>
<string>App needs camera access</string>
<key>NSMicrophoneUsageDescription</key>
<string>App needs microphone access</string>
```

**Windows:**
```ts
// Issue: SmartScreen warning
// Solution: Code sign with trusted certificate

// Issue: Antivirus blocking
// Solution: Code sign and submit to vendors
```

**Linux:**
```ts
// Issue: WebKit crashes
// Solution: Install webkit2gtk-4.1
sudo apt install libwebkit2gtk-4.1-dev

// Issue: Missing libraries
// Solution: Check dependencies
ldd dist/MyApp
```

## Debugging Tools

### Network Inspection

```ts
// Intercept network requests
win.on("will-navigate", (event) => {
  logger.debug("Navigating to:", event.url);
  
  // Block navigation if needed
  if (event.url.includes("blocked.com")) {
    event.preventDefault();
  }
});

// Monitor requests in DevTools Network tab
// Or programmatically:
win.webContents.session.webRequest.onBeforeRequest((details, callback) => {
  logger.debug("Request:", details.url);
  callback({});
});
```

### Source Maps

Ensure source maps are enabled for better debugging:

```ts
// tsconfig.json
{
  "compilerOptions": {
    "sourceMap": true,
    "inlineSourceMap": false,
    "inlineSources": true
  }
}
```

## Systematic Debugging Approach

```ts
// 1. Reproduce the issue consistently
// 2. Isolate the problem (main vs webview)
// 3. Add logging around suspected code
// 4. Use breakpoints in DevTools/debugger
// 5. Check error messages and stack traces
// 6. Review recent changes (git diff)
// 7. Test in isolation (minimal reproduction)
// 8. Check documentation and examples
// 9. Search issues on GitHub
// 10. Ask on Discord

// Debugging template
async function debugIssue() {
  logger.info("=== Debug Session Started ===");
  logger.info("Environment:", {
    platform: process.platform,
    version: app.getVersion(),
    development: process.env.NODE_ENV === "development",
  });
  
  try {
    logger.info("Step 1: Initialize");
    // ...
    
    logger.info("Step 2: Execute");
    // ...
    
    logger.info("Step 3: Verify");
    // ...
    
    logger.info("=== Debug Session Complete ===");
  } catch (error) {
    logger.error("=== Debug Session Failed ===", error);
    throw error;
  }
}
```

## Resources

For more on Electrobun:
- **Core skill**: `electrobun` - Basic setup
- **RPC patterns**: `electrobun-rpc-patterns` - RPC debugging
- **Distribution**: `electrobun-distribution` - Build issues
- **GitHub Issues**: https://github.com/blackboardsh/electrobun/issues
- **Discord**: https://discord.gg/ueKE4tjaCE
