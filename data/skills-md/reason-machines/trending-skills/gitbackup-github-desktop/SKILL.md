---
name: gitbackup-github-desktop
description: Desktop application to back up all GitHub repositories locally and optionally to AWS S3 or Cloudflare R2 cloud storage
triggers:
  - backup my github repos
  - clone all my github repositories
  - set up gitbackup
  - configure github backup to s3
  - schedule automatic github backup
  - add cloud storage to gitbackup
  - gitbackup electron app
  - backup github account locally
---

# GitBackup — GitHub Repository Backup Desktop App

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

GitBackup is an Electron + React desktop application that clones all your GitHub repositories locally and optionally uploads compressed `.tar.gz` archives to AWS S3 or Cloudflare R2. It supports incremental updates, scheduled backups, concurrent processing, and encrypted local settings storage.

## Installation

### Download Pre-built Binary

Download from [Releases](https://github.com/hiteshchoudhary/gitbackup/releases/latest):

| Platform | File |
|----------|------|
| macOS | `GitBackup-x.x.x.dmg` |
| Windows | `GitBackup-Setup-x.x.x.exe` |
| Linux | `GitBackup-x.x.x.AppImage` |

**Prerequisite:** Git must be installed and available in PATH.

### Build from Source

```bash
git clone https://github.com/hiteshchoudhary/gitbackup.git
cd gitbackup
npm install

# Development with hot reload
npm run dev

# Package for current platform
npm run package

# Platform-specific builds
npm run package:mac
npm run package:win
npm run package:linux
```

## GitHub Token Setup

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. **Tokens (classic)** → **Generate new token (classic)**
3. Select scopes: `repo` (full access) + `read:org` (for org repos)
4. Copy the token and paste into the app's Setup page

Fine-grained tokens also work — grant **Repository access → All repositories**.

## Project Structure

```
gitbackup/
├── electron/                       # Main process (Node.js)
│   ├── main.ts                     # App window, tray, lifecycle
│   ├── preload.ts                  # Secure IPC bridge
│   ├── tray.ts                     # System tray icon
│   ├── ipc/                        # IPC handler modules
│   ├── services/
│   │   ├── github.service.ts       # GitHub API via Octokit
│   │   ├── git.service.ts          # Clone & fetch repos (simple-git)
│   │   ├── compress.service.ts     # tar.gz archiving
│   │   ├── cloud.service.ts        # S3/R2 uploads (AWS SDK v3)
│   │   ├── backup-orchestrator.ts  # Core backup pipeline
│   │   └── scheduler.service.ts    # Cron scheduling (node-cron)
│   └── store/store.ts              # Encrypted settings (electron-store)
└── src/                            # Renderer process (React 19)
    ├── pages/                      # Setup, Repos, Backup, Settings
    ├── components/                 # UI components
    └── hooks/                      # IPC & state hooks
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Electron 35 |
| Frontend | React 19 + Tailwind CSS |
| Language | TypeScript 5 |
| Bundler | Vite 8 |
| GitHub API | @octokit/rest |
| Git operations | simple-git |
| Cloud storage | AWS SDK v3 (S3-compatible) |
| Settings | electron-store (encrypted) |
| Scheduling | node-cron |
| Packaging | electron-builder |

## Core Services — Code Examples

### GitHub Service (Octokit)

```typescript
// electron/services/github.service.ts
import { Octokit } from "@octokit/rest";

export class GitHubService {
  private octokit: Octokit;

  constructor(token: string) {
    this.octokit = new Octokit({ auth: token });
  }

  async getAuthenticatedUser() {
    const { data } = await this.octokit.users.getAuthenticated();
    return data;
  }

  // Fetch all repos with pagination — handles 200-300+ repos
  async fetchAllRepositories(filters: RepoFilters): Promise<Repository[]> {
    const repos: Repository[] = [];

    if (filters.owned) {
      for await (const response of this.octokit.paginate.iterator(
        this.octokit.repos.listForAuthenticatedUser,
        { affiliation: "owner", per_page: 100 }
      )) {
        repos.push(...response.data);
      }
    }

    if (filters.organizations) {
      const orgs = await this.octokit.orgs.listForAuthenticatedUser();
      for (const org of orgs.data) {
        for await (const response of this.octokit.paginate.iterator(
          this.octokit.repos.listForOrg,
          { org: org.login, per_page: 100 }
        )) {
          repos.push(...response.data);
        }
      }
    }

    if (filters.starred) {
      for await (const response of this.octokit.paginate.iterator(
        this.octokit.activity.listReposStarredByAuthenticatedUser,
        { per_page: 100 }
      )) {
        repos.push(...response.data as any);
      }
    }

    return repos;
  }
}
```

### Git Service (Clone & Fetch)

```typescript
// electron/services/git.service.ts
import simpleGit, { SimpleGit } from "simple-git";
import path from "path";
import fs from "fs";

export class GitService {
  // Clone with all branches or fetch updates if already exists
  async backupRepository(
    repoUrl: string,
    backupPath: string,
    token: string
  ): Promise<void> {
    // Embed token in URL (cleaned after operation)
    const authenticatedUrl = repoUrl.replace(
      "https://",
      `https://x-access-token:${token}@`
    );

    const repoExists = fs.existsSync(path.join(backupPath, ".git"));

    if (repoExists) {
      // Incremental update — only fetch changes
      const git: SimpleGit = simpleGit(backupPath);
      await git.fetch(["--all", "--prune"]);
    } else {
      // First run — full clone with all branches
      fs.mkdirSync(backupPath, { recursive: true });
      const git: SimpleGit = simpleGit();
      await git.clone(authenticatedUrl, backupPath, ["--mirror"]);
    }

    // Remove token from remote URL after operation
    const git: SimpleGit = simpleGit(backupPath);
    await git.remote(["set-url", "origin", repoUrl]);
  }
}
```

### Cloud Service (S3 / Cloudflare R2)

```typescript
// electron/services/cloud.service.ts
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import fs from "fs";

export interface CloudConfig {
  provider: "s3" | "r2";
  bucket: string;
  region?: string;         // AWS S3
  endpoint?: string;       // Cloudflare R2 endpoint
  accessKeyId: string;     // from env: process.env.AWS_ACCESS_KEY_ID
  secretAccessKey: string; // from env: process.env.AWS_SECRET_ACCESS_KEY
}

export class CloudService {
  private client: S3Client;
  private bucket: string;

  constructor(config: CloudConfig) {
    this.bucket = config.bucket;
    this.client = new S3Client({
      region: config.region ?? "auto",
      endpoint: config.endpoint,       // Set for Cloudflare R2
      credentials: {
        accessKeyId: config.accessKeyId,
        secretAccessKey: config.secretAccessKey,
      },
    });
  }

  async uploadArchive(archivePath: string, key: string): Promise<void> {
    const fileStream = fs.createReadStream(archivePath);
    await this.client.send(
      new PutObjectCommand({
        Bucket: this.bucket,
        Key: key,              // e.g. "owner/repo-name.tar.gz"
        Body: fileStream,
        ContentType: "application/gzip",
      })
    );
  }
}
```

### Compress Service

```typescript
// electron/services/compress.service.ts
import tar from "tar";
import path from "path";

export class CompressService {
  async createArchive(
    sourceDir: string,
    outputPath: string
  ): Promise<string> {
    const archiveName = `${path.basename(sourceDir)}.tar.gz`;
    const archivePath = path.join(outputPath, archiveName);

    await tar.create(
      { gzip: true, file: archivePath, cwd: path.dirname(sourceDir) },
      [path.basename(sourceDir)]
    );

    return archivePath;
  }
}
```

### Backup Orchestrator (Pipeline)

```typescript
// electron/services/backup-orchestrator.ts
import pLimit from "p-limit";

export interface BackupOptions {
  repos: Repository[];
  backupPath: string;
  token: string;
  concurrency: number;       // 1-10
  cloudConfig?: CloudConfig;
  onProgress: (repoName: string, status: RepoStatus) => void;
}

export class BackupOrchestrator {
  async run(options: BackupOptions): Promise<void> {
    const limit = pLimit(options.concurrency);
    const gitService = new GitService();
    const compressService = new CompressService();
    const cloudService = options.cloudConfig
      ? new CloudService(options.cloudConfig)
      : null;

    const tasks = options.repos.map((repo) =>
      limit(async () => {
        const repoPath = path.join(
          options.backupPath,
          repo.owner.login,
          repo.name
        );

        try {
          options.onProgress(repo.full_name, { status: "cloning" });
          await gitService.backupRepository(
            repo.clone_url,
            repoPath,
            options.token
          );

          if (cloudService) {
            options.onProgress(repo.full_name, { status: "compressing" });
            const archivePath = await compressService.createArchive(
              repoPath,
              options.backupPath
            );

            options.onProgress(repo.full_name, { status: "uploading" });
            await cloudService.uploadArchive(
              archivePath,
              `${repo.owner.login}/${repo.name}.tar.gz`
            );
          }

          options.onProgress(repo.full_name, { status: "done" });
        } catch (error) {
          options.onProgress(repo.full_name, {
            status: "error",
            error: (error as Error).message,
          });
        }
      })
    );

    await Promise.all(tasks);
  }
}
```

### Scheduler Service

```typescript
// electron/services/scheduler.service.ts
import cron from "node-cron";

export type ScheduleFrequency = "daily" | "weekly" | "monthly";

export class SchedulerService {
  private task: cron.ScheduledTask | null = null;

  schedule(
    frequency: ScheduleFrequency,
    time: string,             // "HH:MM" format
    callback: () => void
  ): void {
    this.stop();

    const [hour, minute] = time.split(":").map(Number);

    const cronExpressions: Record<ScheduleFrequency, string> = {
      daily:   `${minute} ${hour} * * *`,
      weekly:  `${minute} ${hour} * * 0`,
      monthly: `${minute} ${hour} 1 * *`,
    };

    this.task = cron.schedule(cronExpressions[frequency], callback);
  }

  stop(): void {
    this.task?.stop();
    this.task = null;
  }
}
```

### Encrypted Settings Store

```typescript
// electron/store/store.ts
import Store from "electron-store";

interface AppSettings {
  githubToken: string;
  backupPath: string;
  concurrency: number;
  schedule?: {
    enabled: boolean;
    frequency: "daily" | "weekly" | "monthly";
    time: string;
  };
  cloud?: {
    provider: "s3" | "r2";
    bucket: string;
    region?: string;
    endpoint?: string;
    accessKeyId: string;
    secretAccessKey: string;
  };
}

export const store = new Store<AppSettings>({
  encryptionKey: "your-app-encryption-key", // electron-store encrypts at rest
  defaults: {
    githubToken: "",
    backupPath: "",
    concurrency: 3,
  },
});

// Usage
store.set("githubToken", token);
store.get("backupPath");
store.set("cloud", {
  provider: "r2",
  bucket: process.env.R2_BUCKET_NAME!,
  endpoint: process.env.R2_ENDPOINT!,
  accessKeyId: process.env.R2_ACCESS_KEY_ID!,
  secretAccessKey: process.env.R2_SECRET_ACCESS_KEY!,
});
```

### IPC Bridge (Preload → Renderer)

```typescript
// electron/preload.ts
import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("electronAPI", {
  // GitHub
  validateToken: (token: string) =>
    ipcRenderer.invoke("github:validate-token", token),
  fetchRepos: (filters: RepoFilters) =>
    ipcRenderer.invoke("github:fetch-repos", filters),

  // Backup
  startBackup: (options: BackupOptions) =>
    ipcRenderer.invoke("backup:start", options),
  onProgress: (callback: (data: ProgressEvent) => void) =>
    ipcRenderer.on("backup:progress", (_event, data) => callback(data)),

  // Settings
  getSettings: () => ipcRenderer.invoke("settings:get"),
  saveSettings: (settings: Partial<AppSettings>) =>
    ipcRenderer.invoke("settings:save", settings),

  // Folder picker
  selectFolder: () => ipcRenderer.invoke("dialog:select-folder"),
});
```

```typescript
// src/hooks/useBackup.ts — React renderer side
import { useState } from "react";

export function useBackup() {
  const [progress, setProgress] = useState<Record<string, RepoStatus>>({});

  const startBackup = async (repos: Repository[]) => {
    // Listen for per-repo progress events
    window.electronAPI.onProgress((data) => {
      setProgress((prev) => ({
        ...prev,
        [data.repoName]: data.status,
      }));
    });

    await window.electronAPI.startBackup({
      repos,
      concurrency: 5,
    });
  };

  return { startBackup, progress };
}
```

## Configuration Reference

| Setting | Description | Default |
|---------|-------------|---------|
| `githubToken` | PAT with `repo` + `read:org` scopes | — |
| `backupPath` | Local directory for cloned repos | — |
| `concurrency` | Parallel repo operations (1–10) | `3` |
| `schedule.frequency` | `daily` / `weekly` / `monthly` | — |
| `schedule.time` | Time in `HH:MM` format | — |
| `cloud.provider` | `s3` or `r2` | — |
| `cloud.bucket` | S3/R2 bucket name | — |
| `cloud.region` | AWS region (S3 only) | `us-east-1` |
| `cloud.endpoint` | Custom endpoint (R2: `https://<id>.r2.cloudflarestorage.com`) | — |

## Cloudflare R2 vs AWS S3 Configuration

```typescript
// AWS S3
const s3Config: CloudConfig = {
  provider: "s3",
  bucket: process.env.S3_BUCKET!,
  region: process.env.AWS_REGION ?? "us-east-1",
  accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
};

// Cloudflare R2 — uses S3-compatible API
const r2Config: CloudConfig = {
  provider: "r2",
  bucket: process.env.R2_BUCKET!,
  endpoint: `https://${process.env.CF_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  accessKeyId: process.env.R2_ACCESS_KEY_ID!,
  secretAccessKey: process.env.R2_SECRET_ACCESS_KEY!,
};
```

## Repository Filters

```typescript
interface RepoFilters {
  owned: boolean;          // Repos you own
  organizations: boolean;  // Repos in your orgs
  starred: boolean;        // Repos you've starred
  forked: boolean;         // Forked repos
  collaborator: boolean;   // Repos you collaborate on
}

// Example: back up only owned + org repos
const filters: RepoFilters = {
  owned: true,
  organizations: true,
  starred: false,
  forked: false,
  collaborator: false,
};
```

## Repo Storage Layout

```
~/GitBackup/
├── hiteshchoudhary/
│   ├── gitbackup/        # Mirror clone (all branches)
│   ├── project-a/
│   └── project-b/
├── some-org/
│   └── org-repo/
└── archives/             # .tar.gz files (if cloud upload enabled)
    ├── hiteshchoudhary/
    │   ├── gitbackup.tar.gz
    │   └── project-a.tar.gz
    └── some-org/
        └── org-repo.tar.gz
```

## Common Patterns

### Adding a New IPC Handler

```typescript
// electron/ipc/backup.handler.ts
import { ipcMain } from "electron";
import { BackupOrchestrator } from "../services/backup-orchestrator";

export function registerBackupHandlers(mainWindow: BrowserWindow) {
  ipcMain.handle("backup:start", async (_event, options: BackupOptions) => {
    const orchestrator = new BackupOrchestrator();

    await orchestrator.run({
      ...options,
      onProgress: (repoName, status) => {
        // Send progress back to renderer
        mainWindow.webContents.send("backup:progress", { repoName, status });
      },
    });
  });
}
```

### Adding a New Settings Page (React)

```typescript
// src/pages/Settings.tsx
import { useEffect, useState } from "react";

export default function Settings() {
  const [settings, setSettings] = useState<AppSettings | null>(null);

  useEffect(() => {
    window.electronAPI.getSettings().then(setSettings);
  }, []);

  const handleSave = async () => {
    await window.electronAPI.saveSettings(settings!);
  };

  return (
    <div>
      <label>Concurrency (1-10)</label>
      <input
        type="number"
        min={1}
        max={10}
        value={settings?.concurrency ?? 3}
        onChange={(e) =>
          setSettings((s) => ({ ...s!, concurrency: Number(e.target.value) }))
        }
      />
      <button onClick={handleSave}>Save</button>
    </div>
  );
}
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `git: command not found` | Install Git and ensure it's in system PATH |
| Token validation fails | Confirm `repo` + `read:org` scopes are granted |
| macOS "app can't be opened" | Right-click → Open to bypass Gatekeeper |
| Windows Defender warning | Click "More info" → "Run anyway" |
| Rate limit errors (large accounts) | Reduce concurrency to 1–2; app handles pagination automatically |
| R2 upload 403 errors | Verify `CF_ACCOUNT_ID` in endpoint URL and correct R2 API token permissions |
| Incremental fetch not working | Ensure `backupPath` still contains `.git` directory |
| Scheduled backup not triggering | Keep app running in system tray (don't fully quit) |

## Development Tips

```bash
# Run dev server (Vite + Electron with hot reload)
npm run dev

# Type-check without building
npx tsc --noEmit

# Build renderer only
npx vite build

# Inspect electron-store saved data location
# macOS: ~/Library/Application Support/GitBackup/config.json
# Windows: %APPDATA%\GitBackup\config.json
# Linux: ~/.config/GitBackup/config.json
```
