---
name: cli-to-js-api-wrapper
description: Turn any CLI tool into a fully typed JavaScript/TypeScript API using cli-to-js
triggers:
  - turn a CLI into a JavaScript API
  - wrap a command line tool in TypeScript
  - convert CLI to JS API
  - use cli-to-js to call shell commands
  - generate typed wrapper for CLI tool
  - call CLI tools from Node.js with types
  - spawn CLI commands with JavaScript API
  - introspect CLI help and create API
---

# cli-to-js: Turn Any CLI Into a JavaScript API

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`cli-to-js` reads a binary's `--help` output, parses it into a schema, and returns a fully typed Proxy-based API where subcommands are methods and flags are options. Designed for agent workflows where structured APIs are safer than raw shell strings.

## Install

```sh
npm install cli-to-js
```

## Core Concepts

- `convertCliToJs(binary)` — runs `--help`, parses output, returns typed API proxy
- `fromHelpText(binary, text)` — same but from a static help string
- Every subcommand becomes a method: `api.subcommand({ flag: value })`
- Positional args use the `_` key: `api.command({ _: ["file.txt"] })`
- camelCase keys auto-convert to kebab-case flags: `{ dryRun: true }` → `--dry-run`

## Flag → CLI Mapping

| JS option                 | CLI output                |
|---------------------------|---------------------------|
| `{ verbose: true }`       | `--verbose`               |
| `{ verbose: false }`      | _(omitted)_               |
| `{ output: "file.txt" }`  | `--output file.txt`       |
| `{ dryRun: true }`        | `--dry-run`               |
| `{ v: true }`             | `-v`                      |
| `{ include: ["a","b"] }`  | `--include a --include b` |
| `{ _: ["file.txt"] }`     | `file.txt`                |

## Basic Usage

```ts
import { convertCliToJs } from "cli-to-js";

// Wrap any installed binary
const git = await convertCliToJs("git");
const npm = await convertCliToJs("npm");

// Call subcommands as methods
const result = await git.status();
console.log(result.stdout);
console.log(result.exitCode);

// Pass flags as options
await git.commit({ message: "fix: update logic", all: true });
// → git commit --message "fix: update logic" --all

// Positional arguments via _
const { stdout } = await git.diff({ nameOnly: true, _: ["HEAD~1"] });
const changedFiles = stdout.trim().split("\n");
```

## TypeScript Generics for Full Typing

```ts
import { convertCliToJs } from "cli-to-js";

const git = await convertCliToJs<{
  commit: { message?: string; all?: boolean; amend?: boolean };
  push: { force?: boolean; setUpstream?: string };
  diff: { nameOnly?: boolean; stat?: boolean; _?: string[] };
}>("git");

// Fully autocompleted and type-checked
await git.commit({ message: "hello", all: true });
await git.push({ force: true });

// Type error — foobar doesn't exist
await git.push({ foobar: true }); // ❌ compile error
```

## Output Helpers

```ts
const git = await convertCliToJs("git");

// .text() — trimmed stdout string
const branch = await git.branch({ showCurrent: true }).text();
// "main"

// .lines() — stdout split into array
const files = await git.diff({ nameOnly: true, _: ["HEAD~1"] }).lines();
// ["src/index.ts", "src/utils.ts"]

// .json<T>() — parse stdout as JSON
const packages = await npm.outdated({ json: true }).json<Record<string, { current: string }>>();
// { "lodash": { current: "4.17.20" }, ... }

// Raw result
const result = await git.log({ oneline: true, n: "5" });
result.stdout;   // string
result.stderr;   // string
result.exitCode; // number
```

## Validation (Critical for Agent Use)

Validate options before spawning — catches hallucinated flag names with did-you-mean suggestions:

```ts
const git = await convertCliToJs("git", { subcommands: true });

const errors = git.$validate("commit", { massage: "fix typo" });
// [{ kind: "unknown-flag", name: "massage", suggestion: "message",
//    message: 'Unknown flag "massage". Did you mean "message"?' }]

// Always validate before running in agent workflows
if (errors.length === 0) {
  await git.commit({ message: "fix typo" });
} else {
  // Use errors[0].suggestion to self-correct
  console.log("Suggestion:", errors[0].suggestion);
}

// Validate root command options
const rootErrors = git.$validate({ unknownFlag: true });
```

## Subcommand Parsing

```ts
// Eager: parse all subcommands up front
const git = await convertCliToJs("git", { subcommands: true });
const commitFlags = git.$schema.command.subcommands
  .find((s) => s.name === "commit")?.flags;

// Lazy: parse one subcommand on demand
const git2 = await convertCliToJs("git");
const commitSchema = await git2.$parse("commit");
console.log(commitSchema.flags);

// Parse all subcommands lazily
await git2.$parse();
```

## Streaming Output

```ts
const api = await convertCliToJs("my-tool");

// Callbacks: real-time output + buffered result
const result = await api.build(
  { watch: false },
  {
    onStdout: (data) => process.stdout.write(data),
    onStderr: (data) => process.stderr.write(data),
  }
);

// Async iterator via $spawn
const proc = api.$spawn.test({ _: ["--watch"] });
for await (const line of proc) {
  console.log(line);
  if (line.includes("failed")) proc.kill();
}
console.log("Exit code:", await proc.exitCode);

// Direct spawnCommand
import { spawnCommand } from "cli-to-js";
const dev = spawnCommand("npm", ["run", "dev"]);
for await (const line of dev) {
  if (line.includes("ready")) {
    console.log("Server started");
    break;
  }
}
```

## Per-Call Execution Config

```ts
const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);

await api.build(
  { minify: true },
  {
    cwd: "/my/project",
    env: { ...process.env, NODE_ENV: "production" },
    timeout: 60_000,
    signal: controller.signal,
    stdio: "inherit",  // pass through to terminal for interactive CLIs
  }
);
```

## Command Strings (Without Executing)

```ts
const git = await convertCliToJs("git");

// Get the shell string instead of running it
git.$command.commit({ message: "deploy", all: true });
// "git commit --message deploy --all"

// Compose into a script
import { script } from "cli-to-js";

const deploy = script(
  git.$command.commit({ message: "deploy", all: true }),
  git.$command.push({ force: false })
);

console.log(`${deploy}`);
// "git commit --message deploy --all && git push"

deploy.run(); // executes sequentially, stops on failure
```

## From Help Text String

```ts
import { fromHelpText } from "cli-to-js";

const helpText = `
Usage: mytool [options]
  --output <dir>   Output directory
  --minify         Minify output
  --watch          Watch for changes
`;

const api = fromHelpText("mytool", helpText, { cwd: "/project" });
await api({ output: "dist", minify: true });
```

## CLI Code Generation

```sh
# TypeScript wrapper to stdout
npx cli-to-js git

# Write to file
npx cli-to-js git -o git.ts

# Plain JavaScript
npx cli-to-js git --js -o git.js

# Include per-subcommand flags
npx cli-to-js git --subcommands -o git.ts

# Type declarations only
npx cli-to-js git --dts -o git.d.ts

# Dump raw schema as JSON
npx cli-to-js git --json
```

Generated files are **standalone** with zero runtime dependencies on `cli-to-js`.

## Agent Workflow Pattern

```ts
import { convertCliToJs } from "cli-to-js";

async function agentTask() {
  const git = await convertCliToJs("git", { subcommands: true });
  const claude = await convertCliToJs("claude");

  // Get changed files
  const files = await git.diff({ nameOnly: true, _: ["HEAD~1"] }).lines();

  for (const file of files) {
    // Validate before calling
    const errors = claude.$validate({ print: true, model: "sonnet" });
    if (errors.length > 0) {
      console.error("Invalid flags:", errors);
      continue;
    }

    const review = await claude({
      print: true,
      model: "sonnet",
      _: [`Review ${file} for bugs`],
    });

    if (!review.stdout.includes("no issues")) {
      console.log(`Issues in ${file}:`, review.stdout);
    }
  }
}
```

## Schema Inspection

```ts
const git = await convertCliToJs("git", { subcommands: true });

// Full parsed schema
console.log(git.$schema);
// { binary: "git", command: { name: "git", flags: [...], subcommands: [...] } }

// List subcommands
git.$schema.command.subcommands.forEach((s) => {
  console.log(s.name, s.flags.map((f) => f.name));
});
```

## Common Patterns

**Wrap with default config:**
```ts
const docker = await convertCliToJs("docker", {
  cwd: process.env.PROJECT_DIR,
  env: { ...process.env, DOCKER_BUILDKIT: "1" },
  timeout: 120_000,
});
```

**Root command call (no subcommand):**
```ts
const result = await api({ version: true });
// or
const result = await api("subcommand", { flag: true });
```

**Interactive CLI passthrough:**
```ts
const gh = await convertCliToJs("gh");
await gh.auth({ login: true }, { stdio: "inherit" });
```

## Troubleshooting

**Binary not found:** Ensure the binary is in `PATH`. Test with `which <binary>` in terminal.

**Help text not parsed correctly:** Use `fromHelpText` with manually fetched help, or set `helpFlag` to the correct flag (`-h`, `help`, etc.):
```ts
const api = await convertCliToJs("mytool", { helpFlag: "-h" });
```

**Subcommand flags missing:** Subcommand flags only populate when `subcommands: true` is set or `$parse("sub")` is called:
```ts
await git.$parse("commit"); // now git.$validate("commit", opts) works
```

**Type errors on dynamic subcommands:** Pass a generic type to `convertCliToJs<T>` for per-subcommand option types.

**Timeout on slow help output:** Increase the help fetch timeout:
```ts
const api = await convertCliToJs("slow-tool", { timeout: 30_000 });
```
