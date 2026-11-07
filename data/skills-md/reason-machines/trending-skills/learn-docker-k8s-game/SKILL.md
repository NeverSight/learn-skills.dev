---
name: learn-docker-k8s-game
description: Interactive AI-driven game for learning Docker, Linux, networking, and Kubernetes through story-driven challenges in your AI editor.
triggers:
  - "let's play the docker learning game"
  - "start the docker k8s tutorial"
  - "help me learn docker with the game"
  - "play the nocappuccino game"
  - "how do I use learn-docker-and-k8s"
  - "start the kubernetes learning adventure"
  - "teach me docker interactively"
  - "open the devops learning game"
---

# Learn Docker & K8s Game

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

An open-source, AI-driven interactive learning game that teaches Docker, Linux, networking, and Kubernetes through a story-driven simulation. No web app, no video courses — just you, your AI editor, a terminal, and the chaotic coffee startup NoCappuccino Inc.

---

## How It Works

The game runs entirely inside your AI editor. Markdown prompt files in this repo act as the game engine. When a user says "let's play," the AI reads `AGENTS.md` (or the editor-specific entry point), becomes "Sarah" (the mentor character), and walks the learner through real Docker/K8s scenarios using their actual terminal.

```
User says "let's play"
    → AI reads AGENTS.md + engine/rules.md + engine/narrator.md
    → AI becomes Sarah, the senior DevOps mentor
    → Story begins: Dave broke staging, fix it with containers
    → Lessons → Challenges → verify.sh → next chapter
```

---

## Installation

```bash
git clone https://github.com/ericboy0224/learn-docker-and-k8s.git
cd learn-docker-and-k8s
```

Open the directory in your AI editor, then type: **"let's play"**

### Prerequisites

| Requirement | Chapters | Notes |
|---|---|---|
| Docker | Ch 1–7 | Required |
| Docker Compose v2 | Ch 1–7 | Required |
| kubectl | Ch 6–7 | Optional |
| kind | Ch 6–7 | Optional |
| AI Editor | All | Claude Code, Cursor, Windsurf, Copilot, Cline, Codex, Gemini CLI |

### Environment Check

```bash
bash engine/environment-check.sh
```

This verifies Docker, Docker Compose, and optional Kubernetes tools are installed and running.

---

## Editor Entry Points

Each AI editor reads a different config file automatically:

| Editor | Entry File |
|---|---|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| Windsurf | `.windsurfrules` |
| Cline / Roo Code | `.clinerules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` |
| All others | `AGENTS.md` |

The AI editor will read the appropriate file on startup and load game context from `engine/` and `curriculum/`.

---

## Game Commands

Type these naturally in your AI editor chat:

```
/play           — start or resume the game
/env-check      — verify Docker/K8s setup before starting
/progress       — view save file (.player/progress.yaml)
/hint           — progressive hint (3 levels: nudge → direction → near-answer)
/verify         — check your challenge solution
/next           — advance to next lesson or challenge
/skip-to <N>    — jump to chapter N (triggers a quiz gate)
/cleanup        — remove all learn-* Docker resources safely
```

You can also speak naturally:
- `"I'm stuck on the port mapping"`
- `"check my work"`
- `"what does -p do again?"`
- `"skip to chapter 4"`

---

## Curriculum Overview

```
Ch1 → Ch2 → Ch3 → Ch4 → Ch5 → Ch6 → Ch7
```

| Chapter | Title | Core Skills |
|---|---|---|
| 1 | 📦 It Works on My Machine | containers, images, port mapping |
| 2 | 🏋️ The 2GB Espresso | multi-stage builds, layer caching, .dockerignore |
| 3 | 💾 The Vanishing Beans | volumes, bind mounts, persistence |
| 4 | 🔌 The Silent Grinder | DNS, bridge networks, isolation |
| 5 | 🎼 The Symphony of Steam | Docker Compose, health checks, secrets |
| 6 | ⎈ The Giant Roaster | Pods, Deployments, Services, self-healing |
| 7 | 🔥 The Great Latte Leak | rolling updates, Secrets, HPA, chaos triage |

Linux fundamentals (namespaces, cgroups, mounts) and networking (DNS, NAT, subnets, iptables) are taught contextually throughout — no dedicated lecture needed.

---

## Project Structure

```
learn-docker-and-k8s/
├── AGENTS.md                        # Universal AI entry point
├── CLAUDE.md                        # Claude Code entry + skill definitions
├── GEMINI.md                        # Gemini CLI entry point
├── .cursorrules                     # Cursor entry point
├── .clinerules                      # Cline/Roo Code entry point
├── .windsurfrules                   # Windsurf entry point
├── .github/
│   └── copilot-instructions.md      # GitHub Copilot entry point
│
├── engine/
│   ├── rules.md                     # Teaching vs challenge mode rules
│   ├── narrator.md                  # Story, characters (Sarah/Dave/Marcus), tone
│   ├── validation.md                # How AI should verify challenge solutions
│   ├── environment-check.sh         # Pre-flight Docker/K8s check
│   └── cleanup.sh                   # Remove all learn-* resources
│
├── curriculum/
│   ├── ch01-containers/
│   │   ├── README.md                # Chapter story + learning objectives
│   │   ├── lessons/                 # 3 teaching lessons per chapter
│   │   ├── challenges/              # Hands-on tasks + verify.sh scripts
│   │   └── quiz.md                  # Skip-level assessment questions
│   ├── ch02-image-optimization/
│   ├── ch03-persistence/
│   ├── ch04-networking/
│   ├── ch05-compose/
│   ├── ch06-k8s-intro/
│   └── ch07-k8s-production/
│
└── .player/
    └── progress.yaml                # Save file — AI reads/writes this
```

---

## The Game Engine: Key Files

### `engine/rules.md`
Defines the two game modes:
- **Teaching mode** — AI explains concepts, answers questions freely
- **Challenge mode** — AI gives only progressive hints; never reveals the answer directly

### `engine/narrator.md`
Defines character voices and story tone:
- **Sarah** — friendly senior DevOps mentor, uses coffee metaphors
- **Dave** — CTO who breaks things and says "just restart it"
- **Marcus** — PM who sets impossible deadlines ("demo is at 3")

### `engine/validation.md`
Tells the AI how to run and interpret `verify.sh` scripts — it will execute them in the terminal and parse output to determine pass/fail.

### `.player/progress.yaml`
The save file. The AI manages this automatically:

```yaml
# .player/progress.yaml (example structure)
player:
  name: ""
  started_at: ""
current:
  chapter: 1
  lesson: 2
  challenge: 1
completed:
  chapters: []
  challenges: []
hints_used: 0
```

---

## Challenge Verification Scripts

Each challenge has a `verify.sh` that the AI runs to check the learner's work:

```bash
# curriculum/ch01-containers/challenges/verify.sh (example pattern)
#!/bin/bash
set -e

echo "🔍 Checking Chapter 1 Challenge..."

# Check container is running
if docker ps --filter "name=learn-api" --filter "status=running" | grep -q "learn-api"; then
  echo "✅ Container 'learn-api' is running"
else
  echo "❌ Container 'learn-api' not found or not running"
  exit 1
fi

# Check port mapping
if docker inspect learn-api | grep -q '"HostPort": "8080"'; then
  echo "✅ Port 8080 is mapped correctly"
else
  echo "❌ Port mapping incorrect — expected 8080:8080"
  exit 1
fi

# Check endpoint responds
if curl -sf http://localhost:8080/health > /dev/null; then
  echo "✅ API is responding on port 8080"
else
  echo "❌ API not responding — check the container logs"
  exit 1
fi

echo ""
echo "🎉 Challenge complete! Sarah is proud of you."
```

---

## Real Docker Commands Used in the Game

The game teaches these patterns through hands-on challenges:

```bash
# Ch1 — Run a container with port mapping
docker run -d --name learn-api -p 8080:8080 my-api-image

# Ch2 — Multi-stage build to reduce image size
docker build -t learn-api:optimized .
docker images learn-api  # compare sizes

# Ch3 — Named volume for persistence
docker volume create learn-beans-data
docker run -d -v learn-beans-data:/app/data --name learn-db postgres:15

# Ch3 — Bind mount for development
docker run -d -v $(pwd)/src:/app/src --name learn-dev my-app

# Ch4 — Custom bridge network
docker network create learn-coffee-net
docker run -d --network learn-coffee-net --name learn-api my-api
docker run -d --network learn-coffee-net --name learn-db postgres:15

# Ch5 — Docker Compose
docker compose up -d
docker compose ps
docker compose logs -f api
docker compose down -v

# Ch6 — Kubernetes basics
kubectl apply -f curriculum/ch06-k8s-intro/manifests/
kubectl get pods -l app=learn-api
kubectl rollout status deployment/learn-api

# Ch7 — Horizontal Pod Autoscaler
kubectl apply -f curriculum/ch07-k8s-production/hpa.yaml
kubectl get hpa learn-api-hpa
```

---

## Example Docker Compose (Ch5 Pattern)

```yaml
# curriculum/ch05-compose/docker-compose.yml (game example)
version: "3.9"

services:
  api:
    build: ./api
    container_name: learn-api
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:${DB_PASSWORD}@db:5432/nocappuccino
    depends_on:
      db:
        condition: service_healthy
    networks:
      - learn-coffee-net

  db:
    image: postgres:15-alpine
    container_name: learn-db
    volumes:
      - learn-beans-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=nocappuccino
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - learn-coffee-net

volumes:
  learn-beans-data:

networks:
  learn-coffee-net:
    driver: bridge
```

> Note: `DB_PASSWORD` is read from a `.env` file — never hardcoded.

---

## Example Kubernetes Manifests (Ch6–7 Pattern)

```yaml
# curriculum/ch06-k8s-intro/manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: learn-api
  labels:
    app: learn-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: learn-api
  template:
    metadata:
      labels:
        app: learn-api
    spec:
      containers:
        - name: api
          image: learn-api:latest
          ports:
            - containerPort: 8080
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: learn-db-secret
                  key: password
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: learn-api-svc
spec:
  selector:
    app: learn-api
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

---

## Cleanup

Remove all game-created Docker resources safely (uses `learn-` prefix convention):

```bash
bash engine/cleanup.sh
```

Or via AI editor:
```
/cleanup
```

This removes containers, images, volumes, and networks prefixed with `learn-`. It never touches your other Docker resources.

---

## Contributing

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/learn-docker-and-k8s.git

# Key contribution areas:
# 1. New challenges → curriculum/chXX-*/challenges/
# 2. New chapters   → curriculum/ch08-helm/, ch09-argocd/, etc.
# 3. Fix verify.sh  → make sure exit codes are correct (0=pass, 1=fail)
# 4. New AI editor  → add entry point file + update AGENTS.md
# 5. Translations   → keep technical terms (Docker, kubectl) in English
```

Each chapter follows this structure:
```
chXX-topic/
├── README.md          # Story hook + learning objectives
├── lessons/
│   ├── 01-concept.md  # Teaching content
│   ├── 02-concept.md
│   └── 03-concept.md
├── challenges/
│   ├── README.md      # Challenge instructions
│   └── verify.sh      # Auto-verification script (chmod +x)
└── quiz.md            # 5 questions for /skip-to gate
```

---

## Troubleshooting

**"Docker daemon not running"**
```bash
# macOS
open -a Docker

# Linux
sudo systemctl start docker
sudo usermod -aG docker $USER  # then log out and back in
```

**"verify.sh permission denied"**
```bash
chmod +x curriculum/ch01-containers/challenges/verify.sh
```

**"Port already in use"**
```bash
# Find what's using port 8080
lsof -i :8080
# or
docker ps  # check if a previous learn-* container is still running
bash engine/cleanup.sh
```

**"AI isn't staying in character"**
Remind it: `"You are Sarah from NoCappuccino. Read engine/narrator.md and continue the game."`

**"Progress file is corrupted"**
```bash
rm .player/progress.yaml
# Then: /play to restart
```

**kubectl not found for Ch6–7**
```bash
# Install kind for local Kubernetes
brew install kind kubectl       # macOS
# or
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-amd64
chmod +x kind && sudo mv kind /usr/local/bin/kind

# Create a local cluster
kind create cluster --name learn-k8s
```
