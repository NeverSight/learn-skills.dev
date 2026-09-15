---
name: openmaic-classroom
description: OpenMAIC — Open Multi-Agent Interactive Classroom platform for generating immersive AI-powered learning experiences with slides, quizzes, simulations, and multi-agent discussions.
triggers:
  - set up OpenMAIC classroom
  - create multi-agent interactive classroom
  - generate AI lesson with OpenMAIC
  - configure OpenMAIC with LLM providers
  - deploy OpenMAIC to Vercel
  - build interactive classroom from documents
  - integrate OpenMAIC with OpenClaw
  - add quiz or simulation scene to OpenMAIC
---

# OpenMAIC — Multi-Agent Interactive Classroom

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OpenMAIC (Open Multi-Agent Interactive Classroom) is a Next.js 16 / React 19 / TypeScript platform that converts any topic or document into a full interactive lesson. A multi-agent pipeline (LangGraph 1.1) generates slides, quizzes, HTML simulations, and project-based learning activities delivered by AI teachers and AI classmates with voice (TTS) and whiteboard support.

---

## Project Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 16 (App Router) |
| UI | React 19, Tailwind CSS 4 |
| Agent orchestration | LangGraph 1.1 |
| Language | TypeScript 5 |
| Package manager | pnpm >= 10 |
| Runtime | Node.js >= 20 |

---

## Installation

```bash
git clone https://github.com/THU-MAIC/OpenMAIC.git
cd OpenMAIC
pnpm install
```

### Environment Configuration

```bash
cp .env.example .env.local
```

Edit `.env.local` — at minimum one LLM provider key is required:

```env
# LLM Providers (configure at least one)
OPENAI_API_KEY=$OPENAI_API_KEY
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
GOOGLE_API_KEY=$GOOGLE_API_KEY

# Recommended default model (Gemini 3 Flash = best speed/quality balance)
DEFAULT_MODEL=google:gemini-3-flash-preview

# Optional: MinerU for advanced PDF/table/formula parsing
PDF_MINERU_BASE_URL=https://mineru.net
PDF_MINERU_API_KEY=$MINERU_API_KEY

# Optional: access code for hosted mode
ACCESS_CODE=$OPENMAIC_ACCESS_CODE
```

### Provider Config via YAML (alternative to env vars)

Create `server-providers.yml` in the project root:

```yaml
providers:
  openai:
    apiKey: $OPENAI_API_KEY
  anthropic:
    apiKey: $ANTHROPIC_API_KEY
  google:
    apiKey: $GOOGLE_API_KEY
  deepseek:
    apiKey: $DEEPSEEK_API_KEY
  # Any OpenAI-compatible endpoint
  custom:
    baseURL: https://your-proxy.example.com/v1
    apiKey: $CUSTOM_API_KEY
```

---

## Running the App

```bash
# Development
pnpm dev
# → http://localhost:3000

# Production build
pnpm build && pnpm start

# Type checking
pnpm tsc --noEmit

# Linting
pnpm lint
```

---

## Docker Deployment

```bash
cp .env.example .env.local
# Edit .env.local with your API keys

docker compose up --build
# → http://localhost:3000
```

---

## Vercel Deployment

```bash
# Fork the repo, then import at https://vercel.com/new
# Set env vars in Vercel dashboard:
#   OPENAI_API_KEY or ANTHROPIC_API_KEY or GOOGLE_API_KEY
#   DEFAULT_MODEL (optional, e.g. google:gemini-3-flash-preview)
```

One-click deploy button is available in the README; it pre-fills env var descriptions automatically.

---

## Lesson Generation Pipeline

OpenMAIC uses a two-stage pipeline:

| Stage | Description |
|---|---|
| **Outline** | AI analyzes topic/document and produces a structured lesson outline |
| **Scenes** | Each outline item is expanded into a typed scene: `slides`, `quiz`, `interactive`, or `pbl` |

### Scene Types

| Type | Description |
|---|---|
| `slides` | AI teacher lectures with TTS narration, spotlight, laser pointer |
| `quiz` | Single/multiple choice or short-answer with AI grading |
| `interactive` | HTML-based simulation (physics, flowcharts, etc.) |
| `pbl` | Project-Based Learning — choose a role, collaborate with agents |

---

## API Usage — Generating a Classroom

### REST: Start Generation Job

```typescript
// POST /api/generate
const response = await fetch('/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    topic: 'Quantum Entanglement',
    // Optional: attach document content
    document: markdownString,
    // Optional: model override
    model: 'google:gemini-3-flash-preview',
  }),
});

const { jobId } = await response.json();
```

### REST: Poll Job Status

```typescript
// GET /api/generate/status?jobId=<jobId>
const poll = async (jobId: string) => {
  while (true) {
    const res = await fetch(`/api/generate/status?jobId=${jobId}`);
    const data = await res.json();

    if (data.status === 'completed') {
      console.log('Classroom URL:', data.classroomUrl);
      break;
    }
    if (data.status === 'failed') {
      throw new Error(data.error);
    }
    // status === 'pending' | 'running'
    await new Promise(r => setTimeout(r, 3000));
  }
};
```

### REST: Export Slides

```typescript
// GET /api/export/pptx?classroomId=<id>
const exportPptx = async (classroomId: string) => {
  const res = await fetch(`/api/export/pptx?classroomId=${classroomId}`);
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  // trigger download
  const a = document.createElement('a');
  a.href = url;
  a.download = 'lesson.pptx';
  a.click();
};

// GET /api/export/html?classroomId=<id>
const exportHtml = async (classroomId: string) => {
  const res = await fetch(`/api/export/html?classroomId=${classroomId}`);
  const html = await res.text();
  return html;
};
```

---

## OpenClaw Integration

OpenMAIC ships a skill for [OpenClaw](https://github.com/openclaw/openclaw), enabling classroom generation from Feishu, Slack, Discord, Telegram, etc.

### Install the Skill

```bash
# Via ClawHub (recommended)
clawhub install openmaic

# Manual install
mkdir -p ~/.openclaw/skills
cp -R /path/to/OpenMAIC/skills/openmaic ~/.openclaw/skills/openmaic
```

### Configure OpenClaw

Edit `~/.openclaw/openclaw.json`:

```jsonc
{
  "skills": {
    "entries": {
      "openmaic": {
        "config": {
          // Hosted mode — get access code from https://open.maic.chat/
          "accessCode": "$OPENMAIC_ACCESS_CODE",

          // Self-hosted mode — local repo + server URL
          "repoDir": "/path/to/OpenMAIC",
          "url": "http://localhost:3000"
        }
      }
    }
  }
}
```

### OpenClaw Skill Lifecycle

| Phase | What Happens |
|---|---|
| Clone | Detect existing checkout or clone fresh |
| Startup | Choose `pnpm dev`, `pnpm build && pnpm start`, or Docker |
| Provider Keys | Guide user to edit `.env.local` |
| Generation | Submit async job, poll, return classroom link |

---

## Custom Scene Development Pattern

Scenes are typed React components. To add a new scene type:

```typescript
// types/scene.ts
export type SceneType = 'slides' | 'quiz' | 'interactive' | 'pbl' | 'custom';

export interface CustomScene {
  type: 'custom';
  title: string;
  content: string;
  // your fields
  metadata: Record<string, unknown>;
}
```

```typescript
// components/scenes/CustomScene.tsx
'use client';

import { type CustomScene } from '@/types/scene';

interface Props {
  scene: CustomScene;
  onComplete: () => void;
}

export function CustomSceneComponent({ scene, onComplete }: Props) {
  return (
    <div className="flex flex-col gap-4 p-6">
      <h2 className="text-2xl font-bold">{scene.title}</h2>
      <div dangerouslySetInnerHTML={{ __html: scene.content }} />
      <button
        className="mt-4 rounded-lg bg-blue-600 px-6 py-2 text-white"
        onClick={onComplete}
      >
        Continue
      </button>
    </div>
  );
}
```

---

## Multi-Agent Interaction Modes

| Mode | Trigger | Description |
|---|---|---|
| Classroom Discussion | Automatic | Agents proactively start discussions; user can jump in or get called on |
| Roundtable Debate | Scene config | Multiple agent personas debate a topic with whiteboard illustrations |
| Q&A | User asks question | AI teacher responds with slides, diagrams, or whiteboard drawings |
| Whiteboard | During any scene | Agents draw equations, flowcharts, or concept diagrams in real time |

---

## MinerU Advanced Document Parsing

For complex PDFs with tables, formulas, or scanned images:

```env
# Use MinerU hosted API
PDF_MINERU_BASE_URL=https://mineru.net
PDF_MINERU_API_KEY=$MINERU_API_KEY

# Or self-hosted MinerU instance (Docker)
PDF_MINERU_BASE_URL=http://localhost:8888
```

Without MinerU, OpenMAIC falls back to standard PDF text extraction.

---

## Supported LLM Providers & Model Strings

```typescript
// Model string format: "provider:model-name"
const models = {
  // Google (recommended)
  geminiFlash: 'google:gemini-3-flash-preview',   // best speed/quality
  geminiPro: 'google:gemini-3.1-pro',             // highest quality

  // OpenAI
  gpt4o: 'openai:gpt-4o',
  gpt4oMini: 'openai:gpt-4o-mini',

  // Anthropic
  claude4Sonnet: 'anthropic:claude-sonnet-4-5',
  claude4Haiku: 'anthropic:claude-haiku-4-5',

  // DeepSeek
  deepseekChat: 'deepseek:deepseek-chat',

  // OpenAI-compatible (custom base URL)
  custom: 'custom:your-model-name',
};
```

---

## Export Formats

| Format | Endpoint | Notes |
|---|---|---|
| PowerPoint `.pptx` | `GET /api/export/pptx?classroomId=` | Fully editable slides |
| Interactive `.html` | `GET /api/export/html?classroomId=` | Self-contained HTML page |

---

## Common Patterns

### Generate a Classroom from a Document String

```typescript
const generateFromDocument = async (markdownContent: string, topic: string) => {
  const res = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      topic,
      document: markdownContent,
      model: process.env.DEFAULT_MODEL ?? 'google:gemini-3-flash-preview',
    }),
  });

  const { jobId } = await res.json();

  // Poll until done
  let classroomUrl: string | null = null;
  while (!classroomUrl) {
    await new Promise(r => setTimeout(r, 4000));
    const status = await fetch(`/api/generate/status?jobId=${jobId}`).then(r => r.json());
    if (status.status === 'completed') classroomUrl = status.classroomUrl;
    if (status.status === 'failed') throw new Error(status.error);
  }

  return classroomUrl;
};
```

### Check Provider Health

```typescript
// GET /api/providers
const checkProviders = async () => {
  const res = await fetch('/api/providers');
  const { providers } = await res.json();
  // providers: Array<{ name: string; available: boolean; models: string[] }>
  return providers.filter((p: { available: boolean }) => p.available);
};
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `No LLM provider configured` | Set at least one of `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GOOGLE_API_KEY` in `.env.local` |
| Generation hangs at outline stage | Check API key quota; try switching to `google:gemini-3-flash-preview` for higher rate limits |
| TTS not working | TTS requires a browser with Web Speech API support; check browser console for errors |
| PDF parsing produces garbled text | Enable MinerU by setting `PDF_MINERU_BASE_URL` in `.env.local` |
| Vercel timeout during generation | Increase function timeout in `vercel.json`; generation is async so the API should return a `jobId` immediately |
| Docker build fails | Ensure `DOCKER_BUILDKIT=1` and that `.env.local` exists before running `docker compose up --build` |
| OpenClaw skill not found | Run `clawhub install openmaic` or manually copy `skills/openmaic` to `~/.openclaw/skills/` |
| `pnpm install` fails on Node < 20 | Upgrade Node.js to >= 20 (`nvm use 20`) |
| Port 3000 already in use | Set `PORT=3001` in `.env.local` or run `PORT=3001 pnpm dev` |

---

## Key File Structure

```
OpenMAIC/
├── app/                    # Next.js App Router pages & API routes
│   ├── api/
│   │   ├── generate/       # POST lesson generation, GET status
│   │   ├── export/         # pptx / html export endpoints
│   │   └── providers/      # LLM provider health check
│   └── classroom/          # Classroom viewer pages
├── components/
│   ├── scenes/             # Slide, Quiz, Interactive, PBL components
│   ├── whiteboard/         # Real-time whiteboard rendering
│   └── agents/             # Agent avatar & TTS components
├── lib/
│   ├── agents/             # LangGraph agent graph definitions
│   ├── providers/          # LLM provider abstractions
│   └── generation/         # Outline + scene generation pipeline
├── skills/
│   └── openmaic/           # OpenClaw skill definition
├── server-providers.yml    # Optional YAML provider config
├── .env.example            # Environment variable template
└── docker-compose.yml      # Docker deployment config
```
