---
name: creationix-rx-data-store
description: Expert skill for using RX, an embedded data store for JSON-shaped data with random-access reads, no-parse lookups, and a text-safe binary encoding format.
triggers:
  - encode data with RX
  - use RX data store
  - parse RX format
  - random access JSON data
  - RX encoder decoder TypeScript
  - convert JSON to RX
  - query RX encoded buffer
  - RX format serialization
---

# RX Data Store

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

RX is an embedded data store for JSON-shaped data. Encode once, then query the encoded document in place — no parsing, no object graph, no GC pressure. Think of it as *no-SQL SQLite*: unstructured data with database-style random access.

**Key benefits:**
- O(1) array access, O(log n) object key lookup on encoded data
- Automatic deduplication of values and shared schemas
- Text-safe encoding (copy-paste friendly, no binary tooling needed)
- Minimal heap allocations (~10 vs millions for JSON parsing)
- ~18x compression on real deployment manifests (92 MB → 5.1 MB)

---

## Installation

```sh
npm install @creationix/rx        # library
npm install -g @creationix/rx     # CLI (global)
npx @creationix/rx data.rx        # CLI (one-off)
```

---

## Core API

### String API (most common)

```ts
import { stringify, parse } from "@creationix/rx";

// Encode
const rx = stringify({ users: ["alice", "bob"], version: 3 });
// Returns a string — store it anywhere you'd store JSON text

// Decode (returns a read-only Proxy)
const data = parse(rx) as any;
data.users[0]         // "alice"
data.version          // 3
Object.keys(data)     // ["users", "version"]
JSON.stringify(data)  // works — full JS interop
```

### Uint8Array API (performance-critical paths)

```ts
import { encode, open } from "@creationix/rx";

const buf = encode({ path: "/api/users", status: 200 });
const data = open(buf) as any;
data.path    // "/api/users"
data.status  // 200
```

### Inspect API (lazy AST)

```ts
import { encode, inspect } from "@creationix/rx";

const buf = encode({ name: "alice", scores: [10, 20, 30] });
const root = inspect(buf);

root.tag          // ":"
root[0].tag       // "," (a string key)
root[0].value     // "name"
root.length       // 4 (key, value, key, value)

// Iterate children
for (const child of root) {
  console.log(child.tag, child.b64);
}

// Object helpers
for (const [key, val] of root.entries()) { /* ... */ }
const node = root.index("name");   // key lookup → node
const elem = root.index(2);        // array index → node

// Filtered key search (O(log n + m) on indexed objects)
for (const [key, val] of root.filteredKeys("/api/")) { /* ... */ }
```

### Escape hatch to underlying buffer

```ts
import { handle } from "@creationix/rx";

const h = handle(data.nested);
// h.data: Uint8Array
// h.right: byte offset
```

---

## Encoding Options

```ts
stringify(data, {
  // Add sorted indexes to containers with >= N entries (enables O(log n) lookup)
  // Use 0 for all containers, false to disable entirely
  indexes: 10,

  // External refs — shared dictionary of known values for cross-document dedup
  refs: { R: ["/api/users", "/api/teams"] },

  // Streaming — receive chunks as they're produced
  onChunk: (chunk: string, offset: number) => process.stdout.write(chunk),
});

encode(data, {
  indexes: 10,
  refs: { R: ["/api/users", "/api/teams"] },
  onChunk: (chunk: Uint8Array, offset: number) => { /* ... */ },
});
```

**If the encoder used external refs, pass the same dictionary to the decoder:**

```ts
const data = parse(payload, { refs: { R: ["/api/users", "/api/teams"] } });
const data = open(buf, { refs: { R: ["/api/users", "/api/teams"] } });
```

---

## CLI

```sh
rx data.rx                         # pretty-print as tree (default on TTY)
rx data.rx -j                      # convert to JSON
rx data.json -r                    # convert to RX
cat data.rx | rx                   # read from stdin (auto-detect format)
rx data.rx -s key 0 sub            # select a sub-value: data["key"][0]["sub"]
rx data.rx -o out.json             # write to file
rx data.rx --ast                   # output encoding structure as JSON
rx data.rx -w                      # write converted file (.json↔.rx)
```

**Full CLI flags:**

| Flag | Description |
|------|-------------|
| `<file>` | Input file (format auto-detected) |
| `-` | Read from stdin explicitly |
| `-j`, `--json` | Output as JSON |
| `-r`, `--rexc` | Output as RX |
| `-t`, `--tree` | Output as tree |
| `-a`, `--ast` | Output encoding structure |
| `-s`, `--select <seg>...` | Select a sub-value by path segments |
| `-w`, `--write` | Write converted file |
| `-o`, `--out <path>` | Write to file instead of stdout |
| `-c`, `--color` / `--no-color` | Force or disable ANSI color |
| `--index-threshold <n>` | Index containers above n values (default: 16) |
| `--string-chain-threshold <n>` | Split strings longer than n (default: 64) |
| `--string-chain-delimiter <s>` | Delimiter for string chains (default: `/`) |
| `--key-complexity-threshold <n>` | Max object complexity for dedupe keys (default: 100) |

**Shell completions:**

```sh
rx --completions setup zsh   # or bash
```

**Tip — paged, colorized viewing:**

```sh
p() { rx "$1" -t -c | less -RFX; }
```

---

## Proxy Behavior

The value returned by `parse`/`open` is **read-only**:

```ts
obj.newKey = 1;      // throws TypeError
delete obj.key;      // throws TypeError
"key" in obj;        // works (zero-alloc key search)
obj.nested === obj.nested  // true (container Proxies are memoized)
```

**Supported operations on the Proxy:**
- Property access: `data.key`, `data[0]`
- `Object.keys()`, `Object.entries()`, `Object.values()`
- `for...of`, `for...in`
- `Array.isArray()`
- `.map()`, `.filter()`, `.find()`, `.reduce()`
- Spread and destructuring
- `JSON.stringify()`

---

## Common Patterns

### Build-step: convert JSON artifact to RX

```ts
import { readFileSync, writeFileSync } from "fs";
import { stringify } from "@creationix/rx";

const json = JSON.parse(readFileSync("manifest.json", "utf-8"));
const rx = stringify(json, { indexes: 10 });
writeFileSync("manifest.rx", rx, "utf-8");
```

### Runtime: sparse read from large RX file

```ts
import { readFileSync } from "fs";
import { parse } from "@creationix/rx";

const manifest = parse(readFileSync("manifest.rx", "utf-8")) as any;

// Only the accessed values are decoded — everything else is skipped
const route = manifest.routes["/dashboard/projects"];
console.log(route.title, route.component, route.auth);
```

### Streaming encode to stdout

```ts
import { stringify } from "@creationix/rx";

stringify(largeData, {
  onChunk: (chunk, offset) => process.stdout.write(chunk),
});
```

### Using external refs for cross-document deduplication

```ts
import { stringify, parse } from "@creationix/rx";

const sharedRefs = { R: ["/api/users", "/api/teams", "/api/projects"] };

// Encode multiple documents sharing the same ref dictionary
const doc1 = stringify(data1, { refs: sharedRefs });
const doc2 = stringify(data2, { refs: sharedRefs });

// Decode with the same dictionary
const val1 = parse(doc1, { refs: sharedRefs }) as any;
const val2 = parse(doc2, { refs: sharedRefs }) as any;
```

### Low-level inspect traversal (zero allocation)

```ts
import { encode, inspect } from "@creationix/rx";

const buf = encode(routes);
const root = inspect(buf);

// Walk object entries without creating JS objects
if (root.tag === ":") {
  for (const [key, val] of root.entries()) {
    if (key.value === "/dashboard") {
      console.log("Found:", val.index("title").value);
      break;
    }
  }
}
```

### Type-safe usage pattern

```ts
import { parse } from "@creationix/rx";

interface Route {
  title: string;
  component: string;
  auth: boolean;
}

interface Manifest {
  routes: Record<string, Route>;
  version: number;
}

// Cast after parse — RX Proxy supports all read operations
const manifest = parse(rxString) as unknown as Manifest;
const dashboard = manifest.routes["/dashboard"];
```

---

## Format Reference

RX is a **text encoding** — not human-readable like JSON, but safe to copy-paste.

Every value is read **right-to-left**. The parser scans left past base64 digits to find a **tag** character:

```
[body][tag][b64 varint]
            ◄── read this way ──
```

| JSON | RX | Description |
|------|----|-------------|
| `42` | `+1k` | tag `+` (integer), b64 `1k` = 84, zigzag → 42 |
| `"hi"` | `hi,2` | tag `,` (string), length = 2 |
| `true` | `'t` | tag `'` (ref), built-in literal |
| `[1,2,3]` | `+6+4+2;6` | tag `;` (array), b64 `6` = content size |
| `{"a":1}` | `+2a,1:a` | tag `:` (object), interleaved keys/values |

**Tags:** `+` integer · `*` decimal · `,` string · `'` ref/literal · `:` object · `;` array · `^` pointer · `.` chain · `#` index

---

## When to Use RX vs Alternatives

| Scenario | Use |
|----------|-----|
| Large artifact, sparse reads | **RX** |
| Build manifests, route tables | **RX** |
| Small config files | JSON |
| Human-authored config | JSON/YAML |
| Write-heavy / mutable data | Real database |
| Fixed schema, minimize wire size | Protobuf |
| Relational/tabular data | SQLite |
| Minimizing compressed transfer | gzip/zstd + JSON |

---

## Troubleshooting

**`TypeError: Cannot set property` on decoded value**
The Proxy returned by `parse`/`open` is read-only by design. To mutate, spread into a plain object first:
```ts
const mutable = { ...parse(rx) };
mutable.newKey = "value"; // works
```

**Decoded value looks correct but `instanceof Array` fails**
Use `Array.isArray(val)` instead — this is correctly intercepted by the Proxy.

**External refs mismatch / wrong values decoded**
Ensure the exact same `refs` dictionary (same keys, same arrays, same order) is passed to both `stringify`/`encode` and `parse`/`open`.

**CLI not found after global install**
```sh
npm install -g @creationix/rx
# If still not found, check your npm global bin path:
npm bin -g
```

**Inspecting encoded bytes**
```sh
rx data.rx --ast    # shows encoding structure with tags and offsets
```
Or use the live viewer at **[rx.run](https://rx.run/)** — paste RX or JSON directly.

**Performance: lookups slower than expected**
Ensure `indexes` threshold is set appropriately when encoding. For large objects (e.g., 35k keys), use `indexes: 0` to index all containers:
```ts
stringify(data, { indexes: 0 });
```

---

## Resources

- **[rx.run](https://rx.run/)** — live web viewer, paste RX or JSON to inspect
- **[docs/rx-format.md](https://github.com/creationix/rx/blob/main/docs/rx-format.md)** — full format spec with grammar and railroad diagrams
- **[docs/cursor-api.md](https://github.com/creationix/rx/blob/main/docs/cursor-api.md)** — low-level zero-allocation cursor API
- **[samples/](https://github.com/creationix/rx/tree/main/samples)** — example datasets (route manifest, RPG state, emoji metadata, sensor telemetry)
