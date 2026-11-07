---
name: karpathytalk-community
description: Run and interact with KarpathyTalk, an open markdown-based developer social network with GitHub auth, SQLite, and an LLM-friendly JSON/markdown API.
triggers:
  - set up KarpathyTalk locally
  - run a developer social network in Go
  - deploy KarpathyTalk to a server
  - use the KarpathyTalk API
  - create posts on KarpathyTalk
  - build an agent that reads KarpathyTalk
  - configure GitHub OAuth for KarpathyTalk
  - self-host a markdown social platform
---

# KarpathyTalk Community Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

KarpathyTalk is a Go-based developer social network (Twitter × GitHub Gists) where posts are plain markdown, the social layer supports likes/reposts/follows/replies, and all data is openly accessible via JSON and markdown APIs — designed for both humans and LLM agents.

---

## What It Does

- GitHub OAuth sign-in (no new credentials)
- Posts are GFM markdown with syntax-highlighted code blocks and image uploads
- Social features: likes, reposts, quote posts, replies, follows
- REST API returns JSON (for agents/code) or markdown (for humans)
- Single Go binary + SQLite + `uploads/` directory — trivial to self-host
- Built with: Go, SQLite, htmx, goldmark

---

## Installation & Local Setup

### 1. Create a GitHub OAuth App

Go to **GitHub → Settings → Developer settings → OAuth Apps → New OAuth App**:

| Field | Value |
|---|---|
| Application name | KarpathyTalk |
| Homepage URL | `http://localhost:8080` |
| Authorization callback URL | `http://localhost:8080/auth/callback` |

Save the **Client ID** and **Client Secret**.

### 2. Clone & Build

```bash
git clone https://github.com/karpathy/KarpathyTalk.git
cd KarpathyTalk
go build -o karpathytalk ./cmd/karpathytalk
```

### 3. Configure Environment

```bash
export GITHUB_CLIENT_ID=$GITHUB_CLIENT_ID
export GITHUB_CLIENT_SECRET=$GITHUB_CLIENT_SECRET
export BASE_URL=http://localhost:8080   # optional, defaults to this
```

### 4. Run

```bash
./karpathytalk
# or with options:
./karpathytalk -addr :9090 -db ./data/karpathytalk.db
```

Visit `http://localhost:8080`.

---

## CLI Flags

```
-addr string    HTTP listen address (default ":8080")
-db string      SQLite database path (default "karpathytalk.db")
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GITHUB_CLIENT_ID` | ✅ | — | GitHub OAuth client ID |
| `GITHUB_CLIENT_SECRET` | ✅ | — | GitHub OAuth client secret |
| `BASE_URL` | ❌ | `http://localhost:8080` | Public URL of the deployed app |

---

## Deployment (Production)

### Build & Copy

```bash
# Build binary
go build -o karpathytalk ./cmd/karpathytalk

# Copy to server (adjust user/host)
scp karpathytalk schema.sql user@yourserver:~/karpathytalk/
scp -r templates static user@yourserver:~/karpathytalk/
```

### Run on Server

```bash
ssh user@yourserver
cd ~/karpathytalk
export GITHUB_CLIENT_ID=$GITHUB_CLIENT_ID
export GITHUB_CLIENT_SECRET=$GITHUB_CLIENT_SECRET
export BASE_URL=https://yourdomain.com
./karpathytalk -addr :8080
```

### Caddy TLS (recommended)

```caddyfile
yourdomain.com {
    reverse_proxy localhost:8080
}
```

### nginx TLS

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### systemd Service

```ini
[Unit]
Description=KarpathyTalk
After=network.target

[Service]
WorkingDirectory=/home/deploy/karpathytalk
ExecStart=/home/deploy/karpathytalk/karpathytalk -addr :8080
Restart=always
Environment=GITHUB_CLIENT_ID=$GITHUB_CLIENT_ID
Environment=GITHUB_CLIENT_SECRET=$GITHUB_CLIENT_SECRET
Environment=BASE_URL=https://yourdomain.com

[Install]
WantedBy=multi-user.target
```

---

## API Usage

All data is open — no auth required for reads. The API returns JSON for programmatic access and markdown for human/agent reading.

### Fetch Posts as JSON

```bash
# Timeline / recent posts
curl https://karpathytalk.com/api/posts

# Single post
curl https://karpathytalk.com/api/posts/{postID}

# User's posts
curl https://karpathytalk.com/api/users/{username}/posts
```

### Fetch Posts as Markdown

```bash
# Human/agent-readable markdown
curl https://karpathytalk.com/api/posts/{postID}.md
```

### Go Agent Example — Read Timeline

```go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

type Post struct {
    ID        int64  `json:"id"`
    Username  string `json:"username"`
    Content   string `json:"content"`
    Likes     int    `json:"likes"`
    Reposts   int    `json:"reposts"`
    CreatedAt string `json:"created_at"`
}

func fetchTimeline(baseURL string) ([]Post, error) {
    resp, err := http.Get(baseURL + "/api/posts")
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }

    var posts []Post
    if err := json.Unmarshal(body, &posts); err != nil {
        return nil, err
    }
    return posts, nil
}

func main() {
    posts, err := fetchTimeline("https://karpathytalk.com")
    if err != nil {
        panic(err)
    }
    for _, p := range posts {
        fmt.Printf("[%s] %s (👍 %d)\n", p.Username, p.Content[:min(80, len(p.Content))], p.Likes)
    }
}

func min(a, b int) int {
    if a < b {
        return a
    }
    return b
}
```

### Go Agent Example — Fetch User Posts as Markdown

```go
package main

import (
    "fmt"
    "io"
    "net/http"
)

func fetchUserPostsMarkdown(baseURL, username string) (string, error) {
    url := fmt.Sprintf("%s/api/users/%s/posts.md", baseURL, username)
    resp, err := http.Get(url)
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()
    body, err := io.ReadAll(resp.Body)
    return string(body), err
}

func main() {
    md, err := fetchUserPostsMarkdown("https://karpathytalk.com", "karpathy")
    if err != nil {
        panic(err)
    }
    fmt.Println(md)
}
```

---

## Content Limits

| Content Type | Max Length | Rate Limit |
|---|---|---|
| Posts | 10,000 characters | 30 per hour |
| Replies | 5,000 characters | 60 per hour |
| Images | 5 MB | PNG/JPEG/GIF/WebP only |

---

## Database — Direct SQLite Access

The SQLite database is a single file. You can query it directly for analytics, backups, or migrations:

```bash
# Open database
sqlite3 karpathytalk.db

# List tables
.tables

# Recent posts
SELECT username, substr(content, 1, 80), created_at
FROM posts
ORDER BY created_at DESC
LIMIT 20;

# Most liked posts
SELECT username, likes, substr(content, 1, 60)
FROM posts
ORDER BY likes DESC
LIMIT 10;

# User follower counts
SELECT username, COUNT(*) as followers
FROM follows
GROUP BY username
ORDER BY followers DESC;
```

### Backup

```bash
# Simple file copy (safe while running with WAL mode)
cp karpathytalk.db karpathytalk.db.backup

# Or use sqlite3 online backup
sqlite3 karpathytalk.db ".backup karpathytalk_backup.db"
```

---

## Project Structure

```
KarpathyTalk/
├── cmd/
│   └── karpathytalk/      # main entrypoint
├── templates/             # HTML templates (htmx-powered)
├── static/                # CSS, JS assets
├── uploads/               # User image uploads
├── schema.sql             # SQLite schema
└── karpathytalk.db        # Database (created at runtime)
```

---

## Common Patterns

### Pattern: Agent That Monitors New Posts

```go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "time"
)

type Post struct {
    ID        int64  `json:"id"`
    Username  string `json:"username"`
    Content   string `json:"content"`
    CreatedAt string `json:"created_at"`
}

func pollNewPosts(baseURL string, sinceID int64) ([]Post, error) {
    url := fmt.Sprintf("%s/api/posts?since_id=%d", baseURL, sinceID)
    resp, err := http.Get(url)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    var posts []Post
    json.NewDecoder(resp.Body).Decode(&posts)
    return posts, nil
}

func main() {
    var lastSeenID int64 = 0
    for {
        posts, err := pollNewPosts("https://karpathytalk.com", lastSeenID)
        if err != nil {
            fmt.Println("Error:", err)
        } else {
            for _, p := range posts {
                fmt.Printf("New post by @%s: %s\n", p.Username, p.Content[:min(60, len(p.Content))])
                if p.ID > lastSeenID {
                    lastSeenID = p.ID
                }
            }
        }
        time.Sleep(30 * time.Second)
    }
}

func min(a, b int) int {
    if a < b { return a }
    return b
}
```

### Pattern: Embedding KarpathyTalk Content in an LLM Prompt

```go
package main

import (
    "fmt"
    "io"
    "net/http"
)

// Fetch markdown content to inject into an LLM system prompt or context window
func getContextForLLM(baseURL, username string) (string, error) {
    url := fmt.Sprintf("%s/api/users/%s/posts.md", baseURL, username)
    resp, err := http.Get(url)
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()
    body, err := io.ReadAll(resp.Body)
    return string(body), err
}

func main() {
    context, _ := getContextForLLM("https://karpathytalk.com", "karpathy")
    systemPrompt := fmt.Sprintf(`You are a helpful assistant. Here are recent posts from the community:

%s

Answer questions about these posts.`, context)
    fmt.Println(systemPrompt)
}
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `GITHUB_CLIENT_ID not set` | Missing env var | Export `GITHUB_CLIENT_ID` before running |
| OAuth callback fails | Callback URL mismatch | Ensure GitHub OAuth App callback URL exactly matches `BASE_URL/auth/callback` |
| Binary not found after build | Wrong output path | Run `go build -o karpathytalk ./cmd/karpathytalk` from repo root |
| `templates: no such file` | Missing templates dir | Run the binary from the repo root, or copy `templates/` and `static/` next to the binary |
| Database locked | Concurrent writers | SQLite WAL mode is set by default; avoid multiple binary instances against same `.db` |
| Images not serving | Missing `uploads/` dir | The directory is created automatically on first upload; check write permissions |
| Port already in use | Another process on 8080 | Use `-addr :9090` to change the port |

### Check the App is Running

```bash
curl -I http://localhost:8080/
# Expect: HTTP/1.1 200 OK
```

### Rebuild After Code Changes

```bash
go build -o karpathytalk ./cmd/karpathytalk && ./karpathytalk
```

### Run Tests

```bash
go test ./...
```
