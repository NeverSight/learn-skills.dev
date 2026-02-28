---
name: appstash-cli
description: Use appstash for CLI application directory management. Apply when building CLI tools that need config storage, caching, logging, or update checking.
compatibility: Node.js 18+, TypeScript
metadata:
  author: constructive-io
  version: "1.0.0"
---

# appstash CLI Directory Management

Use `appstash` for simple, clean application directory resolution in CLI tools. It provides consistent paths for config, cache, data, logs, and temp directories with graceful fallback handling.

## When to Apply

Use this skill when:
- Building a CLI tool that needs to store configuration
- Implementing persistent caching for CLI operations
- Managing API keys or auth tokens for CLI tools
- Adding logging to CLI applications
- Storing temporary files during CLI operations

## Installation

```bash
npm install appstash
# or
pnpm add appstash
```

## Core Concepts

### Directory Structure

appstash creates a clean directory structure under the user's home directory:

```
~/.<tool>/
  ├── config/    # Configuration files (settings, auth profiles)
  ├── cache/     # Cached data (repos, API responses)
  ├── data/      # Application data (databases, state)
  └── logs/      # Log files

/tmp/<tool>/     # Temporary files (ephemeral)
```

### Fallback Chain

appstash never throws errors. If the home directory is unavailable:
1. Falls back to XDG directories (`~/.config/<tool>`, `~/.cache/<tool>`, etc.)
2. Falls back to system temp (`/tmp/<tool>/`)

## Basic Usage

```typescript
import { appstash, resolve } from 'appstash';

// Get directories for your CLI tool
const dirs = appstash('mycli', { ensure: true });

console.log(dirs.config); // ~/.mycli/config
console.log(dirs.cache);  // ~/.mycli/cache
console.log(dirs.data);   // ~/.mycli/data
console.log(dirs.logs);   // ~/.mycli/logs
console.log(dirs.tmp);    // /tmp/mycli
```

## Common Patterns

### Storing Auth Profiles

Store multiple API endpoints and tokens for CLI tools:

```typescript
import { appstash, resolve } from 'appstash';
import * as fs from 'fs';

interface AuthProfile {
  endpoint: string;
  token?: string;
}

interface CliConfig {
  current?: string;
  profiles: Record<string, AuthProfile>;
}

const dirs = appstash('mycli', { ensure: true });
const configFile = resolve(dirs, 'config', 'auth.json');

function loadConfig(): CliConfig {
  if (fs.existsSync(configFile)) {
    return JSON.parse(fs.readFileSync(configFile, 'utf8'));
  }
  return { profiles: {} };
}

function saveConfig(config: CliConfig): void {
  fs.writeFileSync(configFile, JSON.stringify(config, null, 2));
}

function addProfile(name: string, endpoint: string, token?: string): void {
  const config = loadConfig();
  config.profiles[name] = { endpoint, token };
  if (!config.current) {
    config.current = name;
  }
  saveConfig(config);
}

function useProfile(name: string): void {
  const config = loadConfig();
  if (!config.profiles[name]) {
    throw new Error(`Profile "${name}" not found`);
  }
  config.current = name;
  saveConfig(config);
}

function getActiveProfile(): AuthProfile | null {
  const config = loadConfig();
  if (config.current && config.profiles[config.current]) {
    return config.profiles[config.current];
  }
  return null;
}
```

### Caching API Responses

```typescript
import { appstash, resolve } from 'appstash';
import * as fs from 'fs';
import * as path from 'path';

const dirs = appstash('mycli', { ensure: true });

interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

function getCached<T>(key: string, ttlMs: number): T | null {
  const cachePath = resolve(dirs, 'cache', `${key}.json`);
  
  if (!fs.existsSync(cachePath)) {
    return null;
  }
  
  const entry: CacheEntry<T> = JSON.parse(fs.readFileSync(cachePath, 'utf8'));
  const age = Date.now() - entry.timestamp;
  
  if (age > ttlMs) {
    fs.unlinkSync(cachePath);
    return null;
  }
  
  return entry.data;
}

function setCache<T>(key: string, data: T): void {
  const cachePath = resolve(dirs, 'cache', `${key}.json`);
  fs.mkdirSync(path.dirname(cachePath), { recursive: true });
  
  const entry: CacheEntry<T> = {
    data,
    timestamp: Date.now(),
  };
  
  fs.writeFileSync(cachePath, JSON.stringify(entry));
}
```

### Logging

```typescript
import { appstash, resolve } from 'appstash';
import * as fs from 'fs';

const dirs = appstash('mycli', { ensure: true });
const logFile = resolve(dirs, 'logs', 'cli.log');

function log(level: 'info' | 'warn' | 'error', message: string): void {
  const timestamp = new Date().toISOString();
  const line = `[${timestamp}] [${level.toUpperCase()}] ${message}\n`;
  fs.appendFileSync(logFile, line);
}
```

### Update Checking with @inquirerer/utils

Combine appstash with `@inquirerer/utils` for update checking:

```typescript
import { appstash, resolve } from 'appstash';
import { checkForUpdates } from '@inquirerer/utils';
import * as fs from 'fs';

const dirs = appstash('mycli', { ensure: true });
const updateCacheFile = resolve(dirs, 'cache', 'update-check.json');

async function checkUpdates(pkgName: string, pkgVersion: string): Promise<void> {
  // Check if we've checked recently (within 24 hours)
  if (fs.existsSync(updateCacheFile)) {
    const cache = JSON.parse(fs.readFileSync(updateCacheFile, 'utf8'));
    const age = Date.now() - cache.timestamp;
    if (age < 24 * 60 * 60 * 1000) {
      return; // Skip check
    }
  }
  
  const result = await checkForUpdates({
    pkgName,
    pkgVersion,
    toolName: 'mycli',
  });
  
  // Cache the check timestamp
  fs.writeFileSync(updateCacheFile, JSON.stringify({ timestamp: Date.now() }));
  
  if (result.hasUpdate && result.message) {
    console.warn(result.message);
    console.warn('Run `npm update -g mycli` to upgrade.');
  }
}
```

## Integration with inquirerer CLI

When building CLIs with `inquirerer`, use appstash for all persistent storage:

```typescript
import { CLI, CLIOptions, Inquirerer, ParsedArgs } from 'inquirerer';
import { appstash, resolve } from 'appstash';

const dirs = appstash('mycli', { ensure: true });

// Auth command using appstash
const authCommand = async (argv: Partial<ParsedArgs>, prompter: Inquirerer) => {
  const configFile = resolve(dirs, 'config', 'auth.json');
  
  // ... implement auth management
};

// Main CLI setup
const commands = async (argv: Partial<ParsedArgs>, prompter: Inquirerer, options: CLIOptions) => {
  // ... command routing
};

const app = new CLI(commands, {
  minimistOpts: {
    alias: { v: 'version', h: 'help' }
  }
});

app.run();
```

## Environment Variable Override

Always allow environment variables to override stored config:

```typescript
import { appstash, resolve } from 'appstash';

function getEndpoint(): string {
  // Environment variable takes precedence
  if (process.env.MYCLI_ENDPOINT) {
    return process.env.MYCLI_ENDPOINT;
  }
  
  // Fall back to stored profile
  const profile = getActiveProfile();
  return profile?.endpoint || 'http://localhost:3000';
}

function getAuthToken(): string | undefined {
  // Environment variable takes precedence
  if (process.env.MYCLI_TOKEN) {
    return process.env.MYCLI_TOKEN;
  }
  
  // Fall back to stored profile
  const profile = getActiveProfile();
  return profile?.token;
}
```

## Testing

Isolate tests using custom `baseDir`:

```typescript
import { appstash } from 'appstash';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';

describe('CLI config', () => {
  let testDirs: ReturnType<typeof appstash>;
  
  beforeEach(() => {
    testDirs = appstash('mycli', {
      baseDir: fs.mkdtempSync(path.join(os.tmpdir(), 'test-')),
      ensure: true
    });
  });
  
  afterEach(() => {
    fs.rmSync(testDirs.root, { recursive: true, force: true });
  });
  
  it('should store config', () => {
    // Test with isolated directories
  });
});
```

## API Reference

### `appstash(tool, options?)`

Get application directories for a tool.

**Parameters:**
- `tool` (string): Tool name (e.g., 'pgpm', 'mycli')
- `options.baseDir` (string): Custom base directory (default: `os.homedir()`)
- `options.ensure` (boolean): Create directories if missing (default: `false`)
- `options.useXdgFallback` (boolean): Use XDG fallback if home fails (default: `true`)
- `options.tmpRoot` (string): Root for temp directory (default: `os.tmpdir()`)

**Returns:** `AppStashResult` with `root`, `config`, `cache`, `data`, `logs`, `tmp` paths

### `resolve(dirs, kind, ...parts)`

Resolve a path within a specific directory.

**Parameters:**
- `dirs`: Result from `appstash()`
- `kind`: 'config' | 'cache' | 'data' | 'logs' | 'tmp'
- `parts`: Path segments to join

**Returns:** Resolved path string

### `ensure(dirs)`

Create directories if they don't exist.

**Parameters:**
- `dirs`: Result from `appstash()`

**Returns:** `{ created: string[], usedFallback: boolean }`

## References

- Package: https://www.npmjs.com/package/appstash
- Source: https://github.com/constructive-io/dev-utils/tree/main/packages/appstash
- Related: `inquirerer` for CLI building, `@inquirerer/utils` for update checking
