---
name: opengame-agentic-game-creation
description: OpenGame is an open-source agentic framework for end-to-end web game creation from a single text prompt, using LLMs, Game Skill (Template + Debug), and headless browser evaluation.
triggers:
  - generate a web game from a prompt
  - create a playable browser game with AI
  - use OpenGame to build a game
  - agentic game coding framework
  - GameCoder LLM game generation
  - OpenGame-Bench evaluation pipeline
  - scaffold a game with template skill
  - debug game build with OpenGame
---

# OpenGame: Agentic Web Game Creation

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OpenGame is an open-source TypeScript framework that generates fully playable web games end-to-end from a single natural language prompt. It combines **Game Skill** (Template Skill + Debug Skill), an optional specialized **GameCoder-27B** LLM, and **OpenGame-Bench** for automated evaluation across Build Health, Visual Usability, and Intent Alignment.

---

## What OpenGame Does

- Takes a high-level game design prompt and produces a runnable browser game (HTML/JS/CSS)
- **Template Skill**: Maintains a growing library of project skeletons to scaffold stable architectures
- **Debug Skill**: Keeps a living protocol of verified fixes to repair cross-file integration errors systematically
- **OpenGame-Bench**: Evaluates generated games via headless browser execution + VLM judging across 150 diverse prompts
- Supports any OpenAI-compatible LLM backend (GPT-4o, Claude, GameCoder-27B, etc.)

---

## Prerequisites

- **Node.js >= 20.0.0**
- An OpenAI-compatible API key (or self-hosted GameCoder-27B endpoint)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/leigest519/OpenGame.git
cd OpenGame

# Install dependencies
npm install

# Copy and configure environment variables
cp .env.example .env
```

### `.env` Configuration

```bash
# Required: LLM API credentials
OPENAI_API_KEY=$OPENAI_API_KEY
OPENAI_BASE_URL=https://api.openai.com/v1   # or your custom endpoint
MODEL_NAME=gpt-4o                            # or gamecoder-27b, claude-3-5-sonnet, etc.

# Optional: OpenGame-Bench VLM judging
VLM_API_KEY=$VLM_API_KEY
VLM_BASE_URL=https://api.openai.com/v1
VLM_MODEL_NAME=gpt-4o

# Optional: Output directory for generated games
OUTPUT_DIR=./output

# Optional: Max debug iterations
MAX_DEBUG_ITERATIONS=5
```

---

## Key CLI Commands

```bash
# Generate a game from a prompt
npm run generate -- --prompt "Build a top-down shooter where a spaceship avoids asteroids"

# Generate with a specific model
npm run generate -- \
  --prompt "Create a tower defense game with 3 enemy types" \
  --model gpt-4o \
  --output ./my-games

# Run OpenGame-Bench evaluation on a set of prompts
npm run bench -- --prompts ./bench/prompts.json --output ./bench-results

# Evaluate a single already-generated game directory
npm run evaluate -- --game-dir ./output/my-game

# Run the local dev server for a generated game
npm run serve -- --game-dir ./output/my-game

# List available template skeletons
npm run templates -- --list

# Add a new template skeleton from an existing game directory
npm run templates -- --add ./output/my-game --name platformer-base
```

---

## Programmatic API

### Basic Game Generation

```typescript
import { OpenGameAgent } from './src/agent';
import { GameSkill } from './src/skills/gameSkill';
import { TemplateSkill } from './src/skills/templateSkill';
import { DebugSkill } from './src/skills/debugSkill';

async function generateGame(prompt: string) {
  // Initialize skills
  const templateSkill = new TemplateSkill({
    libraryPath: './templates',
  });

  const debugSkill = new DebugSkill({
    protocolPath: './debug-protocol.json',
    maxIterations: 5,
  });

  const gameSkill = new GameSkill({ templateSkill, debugSkill });

  // Create and run the agent
  const agent = new OpenGameAgent({
    apiKey: process.env.OPENAI_API_KEY!,
    baseURL: process.env.OPENAI_BASE_URL ?? 'https://api.openai.com/v1',
    model: process.env.MODEL_NAME ?? 'gpt-4o',
    gameSkill,
    outputDir: './output',
  });

  const result = await agent.generate({ prompt });

  console.log('Game generated at:', result.outputPath);
  console.log('Build status:', result.buildHealth);
  return result;
}

generateGame(
  'Make a Pac-Man style maze game with 3 levels, power-ups, and ghost AI'
).catch(console.error);
```

### Using Template Skill Directly

```typescript
import { TemplateSkill } from './src/skills/templateSkill';

const templateSkill = new TemplateSkill({ libraryPath: './templates' });

// Find the best matching template for a game type
const template = await templateSkill.match({
  prompt: 'side-scrolling platformer with double jump',
  gameType: 'platformer',
});

console.log('Matched template:', template.name);
console.log('Skeleton files:', template.files);

// Scaffold a new project from a template
const scaffolded = await templateSkill.scaffold({
  template,
  outputDir: './output/my-platformer',
  context: { gameName: 'MyPlatformer', playerSpeed: 300 },
});

// Save a successful game as a new template for future use
await templateSkill.save({
  sourceDir: './output/successful-game',
  name: 'tower-defense-base',
  tags: ['tower-defense', 'wave-based', 'grid'],
});
```

### Using Debug Skill for Iterative Repair

```typescript
import { DebugSkill } from './src/skills/debugSkill';
import { BuildRunner } from './src/build/runner';

const debugSkill = new DebugSkill({
  protocolPath: './debug-protocol.json',
  maxIterations: 5,
});

const buildRunner = new BuildRunner({ gameDir: './output/my-game' });

// Run the debug loop
const debugResult = await debugSkill.repair({
  gameDir: './output/my-game',
  buildRunner,
  onIteration: (iter, error, fix) => {
    console.log(`Iteration ${iter}: fixing "${error.message}" with "${fix.description}"`);
  },
});

if (debugResult.success) {
  console.log('Game repaired after', debugResult.iterations, 'iterations');
  // Protocol is automatically updated with the new verified fix
} else {
  console.log('Could not repair after max iterations:', debugResult.lastError);
}
```

### OpenGame-Bench Evaluation

```typescript
import { OpenGameBench } from './src/bench/evaluator';

const bench = new OpenGameBench({
  vlmApiKey: process.env.VLM_API_KEY!,
  vlmBaseURL: process.env.VLM_BASE_URL ?? 'https://api.openai.com/v1',
  vlmModel: process.env.VLM_MODEL_NAME ?? 'gpt-4o',
  headlessBrowser: true,
});

// Evaluate a single game
const scores = await bench.evaluate({
  gameDir: './output/my-game',
  originalPrompt: 'Make a Pac-Man style maze game with 3 levels',
});

console.log('Build Health:     ', scores.buildHealth);      // 0–100
console.log('Visual Usability: ', scores.visualUsability);  // 0–100
console.log('Intent Alignment: ', scores.intentAlignment);  // 0–100
console.log('Overall:          ', scores.overall);

// Batch evaluation across multiple prompts
import promptsData from './bench/prompts.json';

const batchResults = await bench.evaluateBatch({
  prompts: promptsData,
  agent,                    // OpenGameAgent instance
  outputDir: './bench-results',
  concurrency: 4,
});

console.log('Mean Build Health:     ', batchResults.mean.buildHealth);
console.log('Mean Intent Alignment: ', batchResults.mean.intentAlignment);
```

---

## Project Structure

```
OpenGame/
├── src/
│   ├── agent/              # Core OpenGameAgent orchestration
│   ├── skills/
│   │   ├── gameSkill.ts    # Combines Template + Debug skills
│   │   ├── templateSkill.ts# Template library management & matching
│   │   └── debugSkill.ts   # Debug protocol & iterative repair
│   ├── build/
│   │   └── runner.ts       # Headless build execution & error capture
│   ├── bench/
│   │   └── evaluator.ts    # OpenGame-Bench scoring pipeline
│   └── llm/
│       └── client.ts       # OpenAI-compatible LLM client
├── templates/              # Template skeleton library (grows over time)
├── bench/
│   └── prompts.json        # 150 benchmark game prompts
├── output/                 # Generated games land here
├── debug-protocol.json     # Living verified-fix protocol
├── .env.example
└── package.json
```

---

## Common Patterns

### Full Pipeline: Prompt → Playable Game

```typescript
import { OpenGameAgent } from './src/agent';
import { GameSkill } from './src/skills/gameSkill';
import { TemplateSkill } from './src/skills/templateSkill';
import { DebugSkill } from './src/skills/debugSkill';
import { OpenGameBench } from './src/bench/evaluator';

async function fullPipeline(prompt: string) {
  const agent = new OpenGameAgent({
    apiKey: process.env.OPENAI_API_KEY!,
    baseURL: process.env.OPENAI_BASE_URL!,
    model: process.env.MODEL_NAME ?? 'gpt-4o',
    gameSkill: new GameSkill({
      templateSkill: new TemplateSkill({ libraryPath: './templates' }),
      debugSkill: new DebugSkill({
        protocolPath: './debug-protocol.json',
        maxIterations: 5,
      }),
    }),
    outputDir: './output',
  });

  // Step 1: Generate
  const result = await agent.generate({ prompt });
  console.log('Generated:', result.outputPath);

  // Step 2: Evaluate
  const bench = new OpenGameBench({
    vlmApiKey: process.env.VLM_API_KEY!,
    vlmModel: 'gpt-4o',
    headlessBrowser: true,
  });

  const scores = await bench.evaluate({
    gameDir: result.outputPath,
    originalPrompt: prompt,
  });

  console.log('Scores:', scores);

  // Step 3: If good quality, promote to template library
  if (scores.overall >= 80) {
    const templateSkill = new TemplateSkill({ libraryPath: './templates' });
    await templateSkill.save({
      sourceDir: result.outputPath,
      name: `auto-${Date.now()}`,
      tags: ['auto-promoted'],
    });
    console.log('Promoted to template library!');
  }

  return { result, scores };
}
```

### Custom LLM Endpoint (e.g., GameCoder-27B self-hosted)

```typescript
const agent = new OpenGameAgent({
  apiKey: process.env.GAMECODER_API_KEY!,
  baseURL: process.env.GAMECODER_BASE_URL!, // e.g. http://localhost:8000/v1
  model: 'gamecoder-27b',
  gameSkill,
  outputDir: './output',
});
```

### Loading Prompts from File and Batch Generating

```typescript
import fs from 'fs/promises';

async function batchGenerate(promptsFile: string) {
  const prompts: string[] = JSON.parse(await fs.readFile(promptsFile, 'utf8'));

  for (const [i, prompt] of prompts.entries()) {
    console.log(`Generating ${i + 1}/${prompts.length}: ${prompt.slice(0, 60)}...`);
    try {
      const result = await agent.generate({ prompt });
      console.log('  ✅ Output:', result.outputPath);
    } catch (err) {
      console.error('  ❌ Failed:', err);
    }
  }
}

batchGenerate('./bench/prompts.json');
```

---

## Troubleshooting

### Build fails immediately with no output
- Ensure `NODE_VERSION >= 20.0.0`: `node --version`
- Verify your API key and base URL are set correctly in `.env`
- Check that `OUTPUT_DIR` exists and is writable

### LLM returns incomplete or truncated code
- Increase the model's max token limit in your API settings or agent config
- Switch to a larger/more capable model: `MODEL_NAME=gpt-4o` or `gamecoder-27b`
- The Debug Skill will attempt iterative repair; raise `MAX_DEBUG_ITERATIONS` if needed

### Debug loop exhausted without success
- Inspect `debug-protocol.json` — it may need a manual verified fix entry for a novel error pattern
- Check `./output/<game>/build.log` for the raw build errors
- Reduce game complexity in the prompt and regenerate

### OpenGame-Bench headless browser errors
- Ensure Chromium/Chrome is installed: `npx playwright install chromium`
- For CI environments, set `DISPLAY=:99` or use a virtual framebuffer

### Template matching returns wrong skeleton
- Add a better-matched template: `npm run templates -- --add ./output/good-example --name my-game-type`
- Templates are matched by semantic similarity to the prompt; more diverse templates improve accuracy

### Rate limits or API quota errors
- Add retry logic or use `concurrency: 1` in batch evaluation
- For self-hosted GameCoder-27B, verify the vLLM/TGI server is healthy: `curl $GAMECODER_BASE_URL/health`

---

## Benchmark: OpenGame-Bench

OpenGame-Bench evaluates 150 diverse game prompts across three axes:

| Metric | Description |
|---|---|
| **Build Health** | Does the game compile and run without errors in a headless browser? |
| **Visual Usability** | Are UI elements visible, legible, and interactable? (VLM-judged) |
| **Intent Alignment** | Does the generated game match the original prompt's design intent? (VLM-judged) |

```bash
# Run full benchmark (150 prompts)
npm run bench -- \
  --prompts ./bench/prompts.json \
  --output ./bench-results \
  --concurrency 4

# Results are saved to ./bench-results/summary.json
```

---

## Resources

- **Project Page**: https://www.opengame-project-page.com/
- **arXiv Paper**: https://arxiv.org/abs/2604.18394
- **Hugging Face**: https://huggingface.co/papers/2604.18394
- **License**: Apache-2.0
