---
name: weft-ai-language
description: Expert skill for building AI systems with Weft, a Rust-based programming language where LLMs, humans, APIs, and infrastructure are first-class primitives with typed connections and durable execution.
triggers:
  - "help me write a Weft program"
  - "how do I use Weft language"
  - "build an AI workflow with Weft"
  - "connect LLM nodes in Weft"
  - "add a human approval step in Weft"
  - "set up Weft development environment"
  - "create a new Weft node"
  - "debug my Weft pipeline"
---

# Weft AI Language

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Weft is a programming language (implemented in Rust) for AI systems where LLMs, humans, APIs, databases, and agents are base language primitives. You wire nodes together, the compiler type-checks every connection, and the program runs with durable execution backed by Restate (survives crashes, supports multi-day human-in-the-loop pauses). A visual graph view is generated automatically from code.

---

## Installation & Setup

### Prerequisites

- Docker (for PostgreSQL)
- Node.js
- macOS: `brew install bash` (Bash 4+ required)
- Rust, Restate, and pnpm are auto-installed by `dev.sh`

### Clone and Configure

```bash
git clone https://github.com/WeaveMindAI/weft.git
cd weft
cp .env.example .env
# Edit .env — add your API keys
```

### Environment Variables (`.env`)

```bash
OPENROUTER_API_KEY=     # Required for LLM nodes
TAVILY_API_KEY=         # Required for Web Search nodes
ELEVENLABS_API_KEY=     # Required for Speech-to-Text nodes
APOLLO_API_KEY=         # Required for Apollo enrichment nodes
DISCORD_BOT_TOKEN=      # Required for Discord nodes
```

All keys are optional at startup — missing keys surface as runtime errors only when the relevant node executes.

### Start Development

```bash
# Terminal 1 — backend (PostgreSQL, Restate, all services)
./dev.sh server

# Terminal 2 — dashboard (SvelteKit at http://localhost:5173)
./dev.sh dashboard

# Or both at once
./dev.sh all
```

### VS Code

Use the **Dev Local All** task to start server + dashboard in split terminals.

---

## Development Commands

```bash
./dev.sh server               # Start backend services
./dev.sh dashboard            # Start frontend
./dev.sh all                  # Start everything
./dev.sh extension            # Build browser extension

./cleanup.sh                  # Stop everything, wipe Restate + DB
./cleanup.sh --no-db          # Stop services, keep database
./cleanup.sh --services       # Stop services only
./cleanup.sh --db-destroy     # Remove PostgreSQL container entirely

cargo build                   # Build without running PostgreSQL (uses .sqlx snapshots)
cargo test                    # Test without running PostgreSQL
```

### Infrastructure Nodes (Kubernetes)

Only needed if using nodes like Postgres Database that provision K8s resources:

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.31.0/kind-$(uname -s | tr '[:upper:]' '[:lower:]')-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

INFRASTRUCTURE_TARGET=local ./dev.sh server
```

---

## The Weft Language

### Core Concepts

- **Nodes** — typed computational units (LLM, HTTP, Human Query, Gate, etc.)
- **Connections** — typed edges between node ports; compiler validates all types
- **Groups** — collapse any set of nodes into a single reusable node
- **Durable execution** — programs checkpoint via Restate; long pauses are transparent

### Node Syntax

```weft
node_name = NodeType -> (output_port: OutputType) {
  label: "Human-readable name"
  config_key: "value"
}
node_name.input_port = other_node.output_port
```

### Simple Example — Poem Generator

```weft
# Project: Poem Generator
# Description: Writes a short poem about any topic

topic = Text {
  label: "Topic"
  value: "the silence between stars"
}

llm_config = LlmConfig {
  label: "Config"
  model: "anthropic/claude-sonnet-4.6"
  systemPrompt: "Write a short, beautiful poem (4-6 lines) about the given topic."
  temperature: "0.8"
}

poet = LlmInference -> (response: String) {
  label: "Poet"
}
poet.prompt = topic.value
poet.config = llm_config.config

output = Debug { label: "Poem" }
output.data = poet.response
```

---

## Built-in Node Catalog

### AI Nodes
| Node | Purpose |
|---|---|
| `LlmConfig` | Configure model, system prompt, temperature |
| `LlmInference` | Call an LLM, returns `response: String` |

### Data Nodes
| Node | Purpose |
|---|---|
| `Text` | Static or dynamic text value |
| `Number` | Numeric value |
| `Dict` | Key-value map |
| `List` | Ordered list |
| `Pack` / `Unpack` | Bundle/unbundle multiple values |

### Flow Nodes
| Node | Purpose |
|---|---|
| `Gate` | Conditional branching |
| `HumanQuery` | Pause execution, send form to human, resume on response |
| `HumanTrigger` | Start a program from a human action |

### Communication Nodes
`Discord`, `Slack`, `Telegram`, `WhatsApp`, `Email`, `X`

### Storage Nodes
`Postgres`, `Memory`

### Enrichment Nodes
`Apollo`, `WebSearch`, `SpeechToText`

### Trigger Nodes
`Cron`, webhooks, polling

### Utility Nodes
`Debug`, `Template`, `HTTP`, `Code` (Python execution)

---

## Common Patterns

### Pattern 1 — LLM with Structured Config

```weft
# Project: Content Summarizer
# Description: Summarizes a webpage given a URL

url_input = Text {
  label: "URL"
  value: "https://example.com/article"
}

search = WebSearch -> (results: String) {
  label: "Fetch Content"
}
search.query = url_input.value

summarizer_config = LlmConfig {
  label: "Summarizer Config"
  model: "anthropic/claude-sonnet-4.6"
  systemPrompt: "Summarize the following content in 3 bullet points."
  temperature: "0.3"
}

summarizer = LlmInference -> (response: String) {
  label: "Summarizer"
}
summarizer.prompt = search.results
summarizer.config = summarizer_config.config

output = Debug { label: "Summary" }
output.data = summarizer.response
```

### Pattern 2 — Human-in-the-Loop Approval

```weft
# Project: Content Approval Pipeline
# Description: AI drafts content, human approves before publishing

draft_config = LlmConfig {
  label: "Drafter Config"
  model: "openai/gpt-4o"
  systemPrompt: "Write a Twitter thread about the given topic. Be engaging."
  temperature: "0.7"
}

topic = Text {
  label: "Topic"
  value: "distributed systems"
}

drafter = LlmInference -> (response: String) {
  label: "Content Drafter"
}
drafter.prompt = topic.value
drafter.config = draft_config.config

# Pauses execution indefinitely until a human responds
approval = HumanQuery -> (approved: Boolean, feedback: String) {
  label: "Human Approval"
  question: "Do you approve this draft for publishing?"
}
approval.content = drafter.response

gate = Gate -> (passed: String) {
  label: "Approval Gate"
}
gate.condition = approval.approved
gate.value = drafter.response

publisher = Discord {
  label: "Publish to Discord"
  channel: "announcements"
}
publisher.message = gate.passed
```

### Pattern 3 — Conditional Branching with Gate

```weft
# Project: Sentiment Router
# Description: Routes messages based on sentiment analysis

message = Text {
  label: "Input Message"
  value: "This product is absolutely terrible!"
}

sentiment_config = LlmConfig {
  label: "Sentiment Config"
  model: "anthropic/claude-haiku-3.5"
  systemPrompt: "Classify sentiment as 'positive' or 'negative'. Respond with one word only."
  temperature: "0.0"
}

classifier = LlmInference -> (response: String) {
  label: "Sentiment Classifier"
}
classifier.prompt = message.value
classifier.config = sentiment_config.config

is_negative = Gate -> (passed: String) {
  label: "Is Negative?"
}
is_negative.condition = classifier.response
is_negative.value = message.value

alert = Slack {
  label: "Alert Team"
  channel: "customer-issues"
}
alert.message = is_negative.passed
```

### Pattern 4 — Cron-Triggered Pipeline

```weft
# Project: Daily Digest
# Description: Sends a daily news digest every morning

schedule = Cron {
  label: "Daily Trigger"
  expression: "0 8 * * *"
}

news = WebSearch -> (results: String) {
  label: "Fetch News"
}
news.query = "AI and technology news today"

digest_config = LlmConfig {
  label: "Digest Config"
  model: "openai/gpt-4o-mini"
  systemPrompt: "Summarize these news items into a concise morning digest."
  temperature: "0.4"
}

digest = LlmInference -> (response: String) {
  label: "Digest Writer"
}
digest.prompt = news.results
digest.config = digest_config.config

send = Email {
  label: "Send Digest"
  to: "team@example.com"
  subject: "Your Daily AI Digest"
}
send.body = digest.response
```

### Pattern 5 — Multi-Step Research Agent

```weft
# Project: Research Agent
# Description: Researches a topic and produces a structured report

query = Text {
  label: "Research Query"
  value: "latest advances in protein folding"
}

search = WebSearch -> (results: String) {
  label: "Search"
}
search.query = query.value

# Enrich with professional data
enrichment = Apollo -> (data: String) {
  label: "Enrichment"
}

analyst_config = LlmConfig {
  label: "Analyst Config"
  model: "anthropic/claude-sonnet-4.6"
  systemPrompt: "You are a research analyst. Given search results, produce a structured report with: Executive Summary, Key Findings, Implications, and Further Reading."
  temperature: "0.2"
}

pack_inputs = Pack -> (bundle: Dict) {
  label: "Combine Sources"
}
pack_inputs.search_results = search.results

analyst = LlmInference -> (response: String) {
  label: "Research Analyst"
}
analyst.prompt = pack_inputs.bundle
analyst.config = analyst_config.config

store = Postgres {
  label: "Store Report"
  table: "research_reports"
}
store.data = analyst.response

notify = Slack {
  label: "Notify Team"
  channel: "research"
}
notify.message = analyst.response
```

---

## Adding a Custom Node

New nodes are two files in the `catalog/` directory. No registration needed — the `inventory` crate auto-discovers nodes at startup.

### Step 1 — Create the folder

```
catalog/
└── my_category/
    └── my_node/
        ├── backend.rs
        └── frontend.ts
```

### Step 2 — Implement `backend.rs`

```rust
use weft_nodes::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct MyNodeConfig {
    pub label: String,
    pub my_setting: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MyNodeInputs {
    pub text: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MyNodeOutputs {
    pub result: String,
}

pub struct MyNode;

#[async_trait]
impl Node for MyNode {
    type Config = MyNodeConfig;
    type Inputs = MyNodeInputs;
    type Outputs = MyNodeOutputs;

    async fn run(
        config: Self::Config,
        inputs: Self::Inputs,
    ) -> Result<Self::Outputs, NodeError> {
        let result = format!("{}: {}", config.my_setting, inputs.text);
        Ok(MyNodeOutputs { result })
    }
}
```

### Step 3 — Define `frontend.ts`

```typescript
import type { NodeDefinition } from "@/types/nodes";

export const MyNode: NodeDefinition = {
  type: "MyNode",
  label: "My Node",
  icon: "sparkles",       // Lucide icon name
  category: "my_category",
  inputs: [
    { name: "text", type: "String", required: true },
  ],
  outputs: [
    { name: "result", type: "String" },
  ],
  config: [
    { name: "label", type: "string", default: "My Node" },
    { name: "my_setting", type: "string", default: "prefix" },
  ],
};
```

After adding both files, run `./dev.sh server` — the node is available immediately.

---

## Type System

Weft has generics, unions, type variables, and null propagation.

| Type | Description |
|---|---|
| `String` | Text value |
| `Number` | Numeric value |
| `Boolean` | True/false |
| `Dict` | Key-value map |
| `List` | Ordered collection |
| `T?` | Nullable type — null propagates through the graph |
| `T \| U` | Union type |

The compiler validates every connection before execution. Type mismatches, missing required connections, and broken architecture are caught at compile time.

---

## Project Layout Reference

```
weft/
├── catalog/                # Node definitions — source of truth
│   ├── ai/                 # LlmConfig, LlmInference
│   ├── code/               # Python execution
│   ├── communication/      # Discord, Slack, Telegram, WhatsApp, Email, X
│   ├── data/               # Text, Number, Dict, List, Pack, Unpack
│   ├── enrichment/         # Apollo, WebSearch, SpeechToText
│   ├── flow/               # Gate, HumanQuery, HumanTrigger
│   ├── storage/            # Postgres, Memory
│   └── triggers/           # Cron, webhooks, polling
├── crates/
│   ├── weft-core/          # Type system, compiler, executor, Restate objects
│   ├── weft-nodes/         # Node trait, registry, sandbox, node runner
│   ├── weft-api/           # REST API (triggers, files, infra, usage)
│   └── weft-orchestrator/  # Restate services + Axum project executor
├── dashboard/              # Web UI (SvelteKit + Svelte 5)
├── extension/              # Browser extension for human-in-the-loop (WXT)
└── scripts/
    └── catalog-link.sh     # Symlinks catalog into crates + dashboard
```

---

## Troubleshooting

### `./dev.sh server` fails immediately

- Ensure Docker is running (`docker ps`)
- Check that ports 5432 (Postgres), 8080 (Restate), and 9070 (Restate admin) are free
- Run `./cleanup.sh` then retry

### Node shows "API key missing" at runtime

- Add the required key to `.env`
- Restart the server (`./cleanup.sh --services && ./dev.sh server`)

### Type mismatch compiler error

- Check that the output port type of the source node matches the input port type of the destination node
- Use `Pack` to bundle multiple values into a `Dict` before passing to a node that expects `Dict`
- Nullable types (`T?`) can propagate null — use a `Gate` node to guard against null before consuming

### Restate state is stale after a crash

```bash
./cleanup.sh        # Wipes Restate journal and DB, full reset
```

### `cargo build` fails without running Postgres

The `.sqlx` directory is committed — offline mode is supported:

```bash
cargo build         # Works without a running database
cargo test          # Works without a running database
```

### New node not appearing in dashboard

- Confirm both `backend.rs` and `frontend.ts` exist under `catalog/<category>/<node>/`
- Run `./scripts/catalog-link.sh` manually then restart the server
- Check server logs for inventory discovery errors

---

## Key Resources

- **Documentation:** https://weavemind.ai/docs
- **Getting Started:** https://weavemind.ai/docs/hello-world
- **Language Reference:** Nodes, Connections, Types, Groups, Parallel — all at https://weavemind.ai/docs
- **Architecture:** `DESIGN.md` in the repo root
- **Roadmap:** `ROADMAP.md` in the repo root
- **Contributing:** `CONTRIBUTING.md` in the repo root
- **Community Discord:** https://discord.com/invite/FGwNu6mDkU
- **License:** O'Saasy License (MIT + no competing hosted service) — https://osaasy.dev
