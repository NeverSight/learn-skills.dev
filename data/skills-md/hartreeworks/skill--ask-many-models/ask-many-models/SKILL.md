---
name: ask-many-models
description: This skill should be used when the user asks to "ask many models", "query multiple AI models", "get opinions from different AIs", "compare AI responses", "ask GPT and Gemini", "ask several models", or mentions wanting to send the same prompt to multiple AI models and synthesise the results.
---

# Ask Many Models

Send the same prompt to multiple AI models in parallel and synthesise their responses into a unified analysis.

## When this skill is invoked

**IMPORTANT**: When this skill is triggered (via `/ask-many-models` or natural language), follow the execution steps below. Do NOT just describe what the skill does.

### Execution Steps

#### Step 1: Get or draft the prompt

**A) Cold start** (conversation just began, no prior discussion):
If the user provided a prompt/question, use it. Otherwise ask: "What question would you like to send to multiple AI models?"

**B) Mid-conversation** (there's been substantive discussion before this):
When invoked after a conversation, ALWAYS draft a comprehensive prompt that:

1. **Captures the full context** - Include relevant background, constraints, and goals discussed
2. **Includes substantive content** - Don't just summarise files; include actual excerpts, code snippets, or data that other models need to answer well
3. **States the core question clearly** - What specific insight/decision/analysis is needed
4. **Notes any constraints or preferences** - Technical requirements, style preferences, etc.

**Prompt drafting checklist:**
- [ ] Background context (2-4 paragraphs minimum)
- [ ] Any relevant file contents or code (include actual content, not just "see attached")
- [ ] The specific question(s) to answer
- [ ] What format/depth of response is useful

**IMPORTANT**: Err on the side of including MORE context than seems necessary. Other models don't have access to this conversation—they only see the prompt you write. A prompt that seems "too long" to you is usually about right.

Save the drafted prompt to a file and show it to the user for approval before proceeding:
```bash
echo "<prompt>" > /tmp/amm-prompt-draft.md && open /tmp/amm-prompt-draft.md
```

Ask: "I've drafted a prompt capturing our discussion. Please review and let me know if you'd like any changes, or say 'go' to proceed."

#### Step 2: Model selection

**Do NOT use AskUserQuestion for model selection** (it has a 4-option limit which is too restrictive). Instead, print this menu and wait for user input:

```
Which models should I query?

1. ⚡ Defaults - GPT-5.2 Thinking, Claude 4.6 Opus Thinking, Gemini 3.1 Pro, Grok 4.1 (Recommended)
2. 🚀 Quick - Gemini 3 Flash, Grok 4.1 Fast, Claude 4.5 Sonnet (~10s)
3. 📊 Comprehensive - Defaults + GPT-5.2 Pro (slow, extra compute)
4. 🔬 Deep Research - OpenAI/Gemini deep research + GPT-5.2 Pro (10-20 min)
5. 🔧 Pick models - Choose individual models

Enter a number (1-5):
```

If user selects **5 (Pick models)**, print this list and ask for comma-separated numbers:

```
Available models:
1. gpt-5.2-thinking (default)
2. claude-4.6-opus-thinking (default)
3. gemini-3.1-pro (default)
4. grok-4.1 (default)
5. gemini-3-flash
6. grok-4.1-non-reasoning
7. claude-4.5-sonnet
8. gpt-5.2
9. gpt-5.2-pro (slow, extra compute)
10. claude-4.6-opus
11. openai-deep-research (10-20 min)
12. gemini-deep-research (10-20 min)

Enter numbers (e.g. 1,2,5):
```

Then map user's numbers to model IDs.

#### Step 3: Check for images

If an image is in the conversation, save it to:
`/Users/ph/.claude/skills/ask-many-models/data/model-outputs/image-TIMESTAMP.png`

#### Step 4: Run the query

Map selection to model IDs:
- **Defaults**: `gpt-5.2-thinking,claude-4.6-opus-thinking,gemini-3.1-pro,grok-4.1`
- **Quick**: `gemini-3-flash,grok-4.1-non-reasoning,claude-4.5-sonnet`
- **Comprehensive**: `gpt-5.2-thinking,claude-4.6-opus-thinking,gemini-3.1-pro,grok-4.1,gpt-5.2-pro`
- **Deep Research**: `openai-deep-research,gemini-deep-research,gpt-5.2-pro`

Generate slug from prompt (lowercase, non-alphanumeric → hyphens, max 50 chars).

```bash
cd /Users/ph/.claude/skills/ask-many-models && yarn query \
  --models "<model-ids>" \
  --synthesise \
  --output-format both \
  [--image "<path>"] \
  "<prompt>"
```

The script auto-generates an output directory at `data/model-outputs/<timestamp>-<slug>/` containing `results.md`, `results.html`, and individual model responses.

#### Step 5: Open results

Say "Querying: [models]" and open the results file. Check `data/user-defaults.json` for `open_preference`:
- `"html"` → `open "<output-dir>/results.html"`
- `"markdown"` (or absent) → `open "<output-dir>/results.md"`

---

## Reference Documentation

### Terminal CLI (Fastest)

Run `amm` directly from your terminal for instant model selection:

```bash
amm "What are the key considerations for X?"
```

Options:
- `--quick` or `-q` - Skip model selection, use defaults
- `--no-synthesise` - Skip the synthesis step

**Default models** are configured in `data/user-defaults.json`.

### Output format

Results can be output as markdown, HTML, or both. The preference is stored in `data/user-defaults.json` under `output_format`. On first run via `amm`, you'll be prompted to choose. The HTML version uses serif typography optimised for long-form reading.

- `--output-format markdown` — markdown only (default for script invocation)
- `--output-format html` — HTML only
- `--output-format both` — both markdown and HTML

### Image Support

Paste an image into your message along with your question to have vision-capable models analyse it:

```
/amm "What's in this image?" [paste image]
```

Vision-capable models: GPT-5.2 Thinking, Claude 4.6 Opus Thinking, Claude 4.5 Sonnet, Gemini 3.1 Pro, Gemini 3 Flash

Models without vision support will receive just the text prompt with a note that an image was provided.

### Direct Script Invocation

Run the query script directly:

```bash
cd /Users/ph/.claude/skills/ask-many-models
yarn query "Your question here"
```

Options:
- `--preset <name>` - Use a preset: `quick`, `comprehensive`
- `--models <list>` - Specify models: `gpt-4o,gemini-2.0-flash`
- `--timeout <seconds>` - Timeout per model (default: 180)
- `--image <path>` - Include an image file for vision models

### Available Commands

```bash
yarn query presets    # List available presets
yarn query models     # List available models
yarn query list       # List recent queries
yarn query show <dir> # Display responses from a query
yarn query synthesise <dir> # Generate synthesis prompt
```

## Workflow

### Step 1: Query Models

```bash
yarn query --preset frontier "What are the key considerations for..."
```

This will:
- Query all models in the preset in parallel
- Save responses to `data/model-outputs/<timestamp>-<slug>/`
- Print a summary of successful/failed queries

### Step 2: Synthesise Responses

The skill generates a synthesis prompt. To synthesise:

1. Generate the prompt:
   ```bash
   yarn query synthesise data/model-outputs/<your-query-dir>
   ```

2. Copy the output and send it to Claude

3. Save Claude's synthesis to the query directory as `synthesis.md`

Alternatively, read the individual responses from the `individual/` subdirectory and ask Claude directly to synthesise them.

## Model Presets

| Preset | Models | Use Case |
|--------|--------|----------|
| `quick` | Gemini 3 Flash, Grok 4.1 (Fast), Claude 4.5 Sonnet | Fast responses (~10s) |
| `comprehensive` | Defaults + GPT-5.2 Pro | Thorough coverage (~60s) |
| `deep-research` | OpenAI Deep Research, Gemini Deep Research | In-depth research (API, 10-20 min) |
| `comprehensive-deep` | Quick models + deep research | Best of both worlds |

## Deep Research Mode

Deep research models (OpenAI o3-deep-research and Gemini Deep Research) conduct comprehensive web research and take 10-20 minutes per model.

### Using Deep Research

From the `amm` CLI, select "🔬 Deep Research" or "🔬📊 Comprehensive + Deep Research":

```bash
amm "What are the latest developments in quantum computing?"
```

When deep research is selected:
1. **Duration warning** is shown (10-20 minutes expected)
2. **Context picker** lets you add files/folders as background context
3. **Quick models** return results in ~30 seconds with preliminary synthesis
4. **Deep research** shows progress updates every 10 seconds
5. **Final synthesis** updates when deep research completes
6. **Desktop notification** fires on completion

### Context Files

Add context to your deep research queries:

1. When prompted, select "Add context file/folder..."
2. Choose a file (`.md`, `.txt`) or folder
3. Context is prepended to the prompt for all models

This is useful for:
- Research related to a specific project
- Questions about documents you've written
- Follow-up research with prior findings

### How It Works

1. Quick models (GPT, Claude, Gemini, Grok) query in parallel → results in ~30s
2. Deep research models start in background with progress polling
3. Preliminary synthesis runs with quick model responses
4. Deep research updates show status every 10 seconds
5. Final synthesis incorporates deep research findings when complete

## Synthesis Approach

The synthesis identifies:

1. **Consensus** - Points where multiple models agree (high confidence)
2. **Unique insights** - Valuable points only one model mentioned
3. **Disagreements** - Contradictions with pros/cons analysis
4. **Confidence assessment** - Overall reliability based on agreement

### Synthesis Depths

| Depth | Output | Use Case |
|-------|--------|----------|
| `brief` | 2-3 sentences | Quick sanity check |
| `executive` | 1-2 paragraphs + bullets | Default, most queries |
| `full` | Multi-section document | Important decisions |

## Configuration

### API Keys

Create `.env` from `.env.example`:
```bash
cp .env.example .env
```

Required keys:
- `OPENAI_API_KEY` - For GPT models
- `ANTHROPIC_API_KEY` - For Claude models
- `GOOGLE_GENERATIVE_AI_API_KEY` - For Gemini models
- `XAI_API_KEY` - For Grok models

### Model Configuration

Model definitions and presets are in `models.json` (shipped with the skill). To customise, create a `config.json` with just the keys you want to override—it merges on top of `models.json`. See `config.example.json` for the format.

## Output Structure

```
data/model-outputs/
└── 2026-01-12-1430-your-question/
    ├── results.md          # Live results + synthesis (markdown)
    ├── results.html        # Live results + synthesis (HTML)
    ├── responses.json      # Raw API responses
    └── individual/
        ├── gpt-5.2-thinking.md
        ├── claude-4.6-opus-thinking.md
        ├── gemini-3.1-pro.md
        └── grok-4.md
```

## Available Models

### Quick/Standard Models

| Model ID | Display Name | Provider | Vision |
|----------|--------------|----------|--------|
| gpt-5.2-thinking | GPT-5.2 Thinking | OpenAI | ✓ |
| claude-4.6-opus-thinking | Claude 4.6 Opus Thinking | Anthropic | ✓ |
| grok-4.1 | Grok 4.1 (Reasoning) | xAI | |
| gemini-3.1-pro | Gemini 3.1 Pro | Google | ✓ |
| gemini-3-flash | Gemini 3 Flash | Google | ✓ |
| gpt-5.2 | GPT-5.2 | OpenAI | ✓ |
| gpt-5.2-pro | GPT-5.2 Pro | OpenAI | ✓ |
| claude-4.6-opus | Claude 4.6 Opus | Anthropic | ✓ |
| claude-4.5-sonnet | Claude 4.5 Sonnet | Anthropic | ✓ |
| grok-4.1-non-reasoning | Grok 4.1 (Fast) | xAI | |

### Deep Research Models

| Model ID | Display Name | Provider | Duration |
|----------|--------------|----------|----------|
| openai-deep-research | OpenAI Deep Research | OpenAI | 10-20 min |
| gemini-deep-research | Gemini Deep Research | Google | 10-20 min |

## Notifications

Desktop notifications via terminal-notifier:
- Install: `brew install terminal-notifier`
- Notifications sent when:
  - Query completes
  - Async request (deep research) completes
  - Errors occur

## Slow Models & Progressive Synthesis

Some models (like GPT-5.2 Pro) use extra compute and can take 10-60 minutes for complex queries. These are marked as "slow" in the config.

When slow models are included:
1. **Progress display** shows real-time status of all models with ✓/✗/◐ icons
2. **Fast models complete first** → preliminary synthesis runs immediately
3. **Slow models continue** in background with "(slow)" indicator
4. **Final synthesis** replaces preliminary when all models complete

The live markdown file updates continuously so you can read responses as they arrive.

## Error Handling

- **Model timeout**: Marked as failed, other responses still synthesised
- **API error**: Retries with exponential backoff (3 attempts)
- **Partial failure**: Synthesis proceeds with available responses
- **Browser not available**: Warns user to restart with `--chrome`

## Tips

1. **Start with `quick` preset** for rapid iteration
2. **Use defaults for important questions** where quality matters
3. **Save synthesis prompts** for consistent formatting
4. **Check individual responses** when synthesis seems off
5. **Override model IDs** via `config.json` as providers release new models
