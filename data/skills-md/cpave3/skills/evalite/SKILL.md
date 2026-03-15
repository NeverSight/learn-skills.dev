---
name: evalite
description: >-
  Write and run LLM evaluations using the evalite TypeScript library (built on Vitest).
  Use when creating .eval.ts files, writing scorers, tracing LLM calls, comparing model
  variants, configuring evalite, running evals in CI, or when the user mentions "evalite",
  "evals", "LLM evaluation", "scoring LLM output", or "eval runner". Also trigger when
  you see imports from "evalite", "evalite/traces", "evalite/ai-sdk", "evalite/config",
  "evalite/runner", or "autoevals".
---

# Evalite

Evalite is a local-first TypeScript eval runner built on Vitest. Eval files use the `.eval.ts` extension. Results are stored in SQLite at `node_modules/.evalite` and viewed via a local UI at `localhost:3006`.

## Setup

```bash
pnpm add -D evalite vitest autoevals
```

package.json scripts:
```json
{ "eval:dev": "evalite watch", "eval": "evalite" }
```

## Core API

### `evalite(name, opts)` — define an eval

```ts
import { evalite } from "evalite";
import { Levenshtein } from "autoevals";

evalite("My Eval", {
  data: [{ input: "Hello", expected: "Hello World!" }],
  task: async (input) => input + " World!",
  scorers: [Levenshtein],
});
```

Generic type params: `evalite<TInput, TOutput, TExpected>(name, opts)`

- **data** — array or async function returning `{ input, expected?, only? }[]`
- **task** — `(input: TInput, variant: TVariant) => Promise<TOutput | AsyncIterable<TOutput>>`
- **scorers** — array of scorer functions or inline scorer objects (optional)
- **columns** — `(result) => RenderedColumn[]` for custom UI columns (optional)
- **trialCount** — run each data point N times for variance measurement (optional)

### `data` field

Can be a static array or an async function:

```ts
data: async () => [
  { input: "What is 2+2?", expected: "4" },
  { input: "Capital of France?", expected: "Paris" },
],
```

Use `only: true` on a data entry to focus on just that input during development:
```ts
data: [
  { input: "test1", expected: "out1" },
  { input: "test2", expected: "out2", only: true }, // only this runs
],
```

### Streams

Return any `AsyncIterable` (including `ReadableStream`) from `task` — evalite collects chunks and joins them:

```ts
import { streamText } from "ai";
task: async (input) => {
  const result = await streamText({ model: myModel, prompt: input });
  return result.textStream;
},
```

### Skipping

```ts
evalite.skip("Disabled Eval", { data: [], task: async () => {}, scorers: [] });
```

## Scorers

Scores are **0 to 1** (not 0 to 100). Return a number or `{ score, metadata }`.

### Inline scorer

```ts
scorers: [
  {
    name: "Contains Paris",
    description: "Checks if output contains 'Paris'.",
    scorer: ({ input, output, expected }) => output.includes("Paris") ? 1 : 0,
  },
],
```

### Reusable scorer with `createScorer`

```ts
import { createScorer } from "evalite";

const exactMatch = createScorer<string, string>({
  name: "Exact Match",
  description: "Checks exact string equality.",
  scorer: ({ output, expected }) => output === expected ? 1 : 0,
});
```

Generic params: `createScorer<TInput, TOutput, TExpected = TOutput>(opts)`

The scorer function receives `{ input, output, expected }`. Return a number (0-1) or `{ score: number, metadata?: unknown }`.

### LLM-as-judge scorer

Use `generateObject` (or any LLM call) inside a scorer to get AI-powered evaluation. Return `{ score, metadata: { rationale } }` so the reasoning shows in the UI. See [references/llm-judge-example.md](references/llm-judge-example.md) for a full Factuality scorer example.

### autoevals library

`autoevals` provides ready-made scorers: `Levenshtein`, `Factuality`, and others. Install with `pnpm add -D autoevals`.

## Traces

Track individual LLM calls within a task for debugging, token usage, and cost tracking.

### Manual tracing with `reportTrace`

```ts
import { reportTrace } from "evalite/traces";

// Inside a task:
const start = performance.now();
const result = await myLLMCall();
reportTrace({
  start,
  end: performance.now(),
  output: result.output,
  input: [{ role: "user", content: input }],
  usage: { inputTokens: 100, outputTokens: 50, totalTokens: 150 },
});
```

`reportTrace` is a no-op outside evalite (safe to leave in production code). Multiple calls per task create multiple trace entries.

### AI SDK auto-tracing with `traceAISDKModel`

```ts
import { traceAISDKModel } from "evalite/ai-sdk";
import { openai } from "@ai-sdk/openai";

const tracedModel = traceAISDKModel(openai("gpt-4o-mini"));
// Use tracedModel with generateText/streamText — all calls auto-traced
```

Also a no-op outside evalite. Works with both `generateText` and `streamText`.

## Variant Comparison with `evalite.each`

Compare models, prompts, or configs on the same dataset:

```ts
evalite.each([
  { name: "GPT-4o mini", input: { model: "gpt-4o-mini", temp: 0.7 } },
  { name: "GPT-4o", input: { model: "gpt-4o", temp: 0.7 } },
])("Compare models", {
  data: async () => [
    { input: "Capital of France?", expected: "Paris" },
  ],
  task: async (input, variant) => {
    return generateText({
      model: openai(variant.model),
      temperature: variant.temp,
      prompt: input,
    });
  },
  scorers: [Factuality, Levenshtein],
});
```

The second argument to `task` receives `variant.input` from the array entry. Each variant appears as a separate eval in the UI, named `"Compare models [GPT-4o mini]"` etc.

## Custom Columns

Override the default Input/Expected/Output columns in the UI:

```ts
columns: async ({ input, output, expected, scores, traces }) => [
  { label: "Question", value: input },
  { label: "Answer", value: output },
  { label: "Tokens", value: traces.reduce((sum, t) => sum + (t.usage?.totalTokens || 0), 0) },
],
```

## Multi-Modal (Files)

Evalite detects `Uint8Array`/`Buffer` values anywhere in data, output, traces, or columns and saves them to `node_modules/.evalite/files`, rendering them in the UI.

For files on disk without reading into memory:
```ts
import { EvaliteFile } from "evalite";
data: [{ input: EvaliteFile.fromPath("path/to/image.jpg") }],
```

## Configuration — `evalite.config.ts`

```ts
import { defineConfig } from "evalite/config";

export default defineConfig({
  testTimeout: 60_000,     // ms, default 30000
  maxConcurrency: 100,     // parallel test cases, default 5
  scoreThreshold: 80,      // 0-100, fail if avg score below
  hideTable: false,        // hide terminal table output
  trialCount: 3,           // run each test case N times
  setupFiles: ["dotenv/config"], // run before tests (env vars)
  server: { port: 3006 },  // UI server port
});
```

Per-eval `trialCount` overrides config-level `trialCount`.

### Environment Variables

To load `.env` files, install `dotenv` and add `setupFiles: ["dotenv/config"]` to `evalite.config.ts`.

## CLI

| Command | Description |
|---|---|
| `evalite` | Run all evals once and exit |
| `evalite watch` | Watch mode with live reload UI |
| `evalite serve` | Run once, keep UI server running |
| `evalite my-eval.eval.ts` | Run specific file |
| `evalite --threshold=70` | Fail if avg score < 70 |
| `evalite export` | Export static HTML bundle |
| `evalite export --output=./dir --basePath=/path` | Export with custom path |
| `evalite watch --hideTable` | Hide detailed table in terminal |

## Programmatic API

```ts
import { runEvalite } from "evalite/runner";

await runEvalite({
  mode: "run-once-and-exit",  // or "watch-for-file-changes" | "run-once-and-serve"
  path: "my-eval.eval.ts",   // optional file filter
  cwd: "/path/to/project",   // optional, defaults to process.cwd()
  scoreThreshold: 80,        // optional
  outputPath: "./results.json", // optional JSON export
});
```

## CI/CD

Run evals in CI with threshold enforcement and static UI export:

```yaml
- run: npx evalite --threshold=70
- run: npx evalite export --output=./ui-export
- uses: actions/upload-artifact@v3
  with:
    name: evalite-ui
    path: ui-export
```

JSON export for programmatic analysis: `evalite --outputPath=./results.json`

The exported JSON is typed as `Evalite.Exported.Output` (import `type { Evalite } from "evalite"`).

## Caching (Important for Watch Mode)

Implement a caching layer for LLM calls in watch mode to avoid burning API credits. Wrap your model with a cache middleware — see [references/caching-pattern.md](references/caching-pattern.md) for the full pattern using `wrapLanguageModel` from the AI SDK.

## Import Map

| Import | Exports |
|---|---|
| `evalite` | `evalite`, `createScorer`, `EvaliteFile`, `type Evalite` |
| `evalite/traces` | `reportTrace` |
| `evalite/ai-sdk` | `traceAISDKModel` |
| `evalite/config` | `defineConfig` |
| `evalite/runner` | `runEvalite` |
