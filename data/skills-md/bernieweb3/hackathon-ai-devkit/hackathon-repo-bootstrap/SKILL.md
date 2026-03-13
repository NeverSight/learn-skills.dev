---
name: hackathon-repo-bootstrap
description: >-
  Generate a ready-to-run project scaffold based on the recommended hackathon stack with environment configuration and deployment setup.
---
# hackathon-repo-bootstrap

## Goal
Generate a ready-to-run project scaffold for a hackathon project, configured for the recommended stack (Next.js + Render + Supabase + LLM router), with environment variables, deployment configuration, and folder structure ready for immediate development.

---

## Trigger Conditions

Use this skill when:
- MVP scope is locked and the tech stack is confirmed from `hackathon-task-planner`
- The team is about to begin implementation and needs a project skeleton
- A deployment target (Vercel, Render, Railway) has been chosen
- Environment variables and API keys need to be structured before coding begins
- Invoked once at the start of Phase 5 (Build), immediately before the first `hackathon-code-implementer` call

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `project_title` | string | Yes | Name of the project (used for directory and package naming) |
| `tech_stack` | string[] | Yes | Technologies confirmed from `hackathon-task-planner` |
| `mvp_features` | object[] | Yes | MVP feature list from `hackathon-scope-cutter` |
| `deployment_targets` | object[] | Yes | Frontend and backend deployment platforms |
| `llm_provider` | string | No | LLM routing provider: `groq`, `openrouter`, `nvidia-nim`, `openai` (default: `groq`) |
| `database` | string | No | Database provider: `supabase`, `postgres`, `sqlite`, `none` (default: `supabase`) |
| `team_size` | integer | No | Number of team members (used to suggest monorepo vs. split repos) |

---

## Outputs

| Output | Description |
|---|---|
| `directory_structure` | Full folder and file tree for the project scaffold |
| `env_template` | `.env.example` content with all required environment variables |
| `startup_commands` | Ordered commands to initialise and run the project locally |
| `deployment_config` | Platform-specific deployment configuration snippets |
| `llm_routing_scaffold` | LLM client initialisation code for the chosen provider |
| `database_scaffold` | Database client initialisation and schema bootstrap snippet |
| `recommended_skills` | Suggested next skills to invoke |

---

## Rules

1. Generate a monorepo structure with `frontend/` and `backend/` subdirectories when `team_size >= 3`; otherwise generate a single Next.js full-stack app.
2. Include a `README.md` stub with setup instructions in the scaffold root.
3. All API keys must appear as environment variables — never hardcoded.
4. `env_template` must list every required variable with a descriptive comment.
5. `startup_commands` must be executable from a clean machine with Node and Python installed.
6. `deployment_config` must include both a local run config and a platform deploy config.
7. Flag any required external service (Supabase, Groq, etc.) with a `[REQUIRES ACCOUNT]` note.

---

## Output Format

```yaml
directory_structure: |
  <project-name>/
  ├── frontend/
  │   ├── ...
  ├── backend/
  │   ├── ...
  └── README.md

env_template: |
  # <project-name> Environment Variables
  # Frontend
  NEXT_PUBLIC_API_URL=http://localhost:8000
  # Backend
  <VAR_NAME>=<description>   # [REQUIRES ACCOUNT]

startup_commands:
  - step: <number>
    command: "<shell command>"
    description: "<what it does>"

deployment_config:
  - platform: "<Vercel|Render|Railway>"
    file: "<config file name>"
    content: |
      <config content>

llm_routing_scaffold:
  provider: "<groq|openrouter|nvidia-nim|openai>"
  language: "<python|typescript>"
  snippet: |
    <code>

database_scaffold:
  provider: "<supabase|postgres|sqlite>"
  language: "<python|typescript>"
  snippet: |
    <code>

recommended_skills:
  - "<skill-name>"
```

---

## Example

**Input:**
```yaml
project_title: "AnchorAI"
tech_stack: ["Next.js", "FastAPI", "Supabase", "Groq"]
mvp_features:
  - feature: "GPT-4 emotional check-in conversation"
  - feature: "Session memory"
  - feature: "Crisis escalation (mocked)"
deployment_targets:
  - role: "frontend"
    platform: "Vercel"
  - role: "backend"
    platform: "Render"
llm_provider: "groq"
database: "supabase"
team_size: 3
```

**Output:**
```yaml
directory_structure: |
  anchorai/
  ├── frontend/                  # Next.js 14 app
  │   ├── app/
  │   │   ├── page.tsx
  │   │   └── api/
  │   ├── components/
  │   ├── .env.local.example
  │   ├── next.config.js
  │   └── package.json
  ├── backend/                   # FastAPI service
  │   ├── main.py
  │   ├── routers/
  │   │   └── chat.py
  │   ├── services/
  │   │   ├── llm.py
  │   │   └── memory.py
  │   ├── .env.example
  │   └── requirements.txt
  └── README.md

env_template: |
  # AnchorAI — Backend Environment Variables
  GROQ_API_KEY=                  # [REQUIRES ACCOUNT] https://console.groq.com
  SUPABASE_URL=                  # [REQUIRES ACCOUNT] https://supabase.com
  SUPABASE_ANON_KEY=             # [REQUIRES ACCOUNT]
  DEMO_USER_ID=demo

  # AnchorAI — Frontend Environment Variables
  NEXT_PUBLIC_API_URL=http://localhost:8000

startup_commands:
  - step: 1
    command: "cd anchorai/backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    description: "Install Python dependencies"
  - step: 2
    command: "cp .env.example .env && # fill in API keys"
    description: "Configure environment variables"
  - step: 3
    command: "uvicorn main:app --reload --port 8000"
    description: "Start FastAPI backend"
  - step: 4
    command: "cd anchorai/frontend && npm install && cp .env.local.example .env.local && npm run dev"
    description: "Start Next.js frontend"

deployment_config:
  - platform: "Render"
    file: "render.yaml"
    content: |
      services:
        - type: web
          name: anchorai-api
          runtime: python
          buildCommand: "pip install -r requirements.txt"
          startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
          envVars:
            - key: GROQ_API_KEY
              sync: false
            - key: SUPABASE_URL
              sync: false
  - platform: "Vercel"
    file: "vercel.json"
    content: |
      {
        "env": {
          "NEXT_PUBLIC_API_URL": "@anchorai-api-url"
        }
      }

llm_routing_scaffold:
  provider: "groq"
  language: "python"
  snippet: |
    from groq import Groq

    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    def chat(messages: list[dict], model: str = "llama3-70b-8192") -> str:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content

database_scaffold:
  provider: "supabase"
  language: "python"
  snippet: |
    from supabase import create_client

    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_ANON_KEY"]
    )

    def save_session_summary(user_id: str, summary: str):
        supabase.table("sessions").upsert({
            "user_id": user_id,
            "summary": summary
        }).execute()

    def get_session_summary(user_id: str) -> str:
        result = supabase.table("sessions").select("summary").eq("user_id", user_id).execute()
        return result.data[0]["summary"] if result.data else ""

recommended_skills:
  - "hackathon-code-implementer"
  - "hackathon-risk-analyzer"
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-reference-architecture.md`
- `knowledge/hackathon-tools.md`
- `knowledge/hackathon-mvp-strategy.md`
- `knowledge/hackathon-common-failures.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
- `playbooks/24h-hackathon-playbook.md`
- `playbooks/36h-hackathon-playbook.md`
- `playbooks/48h-hackathon-playbook.md`
