---
name: toon-format
description: Expert skill for Token-Oriented Object Notation (TOON) — compact, schema-aware JSON encoding for LLM prompts that reduces tokens by ~40%.
triggers:
  - convert JSON to TOON format
  - reduce LLM prompt tokens
  - encode data for LLM input
  - use TOON for AI prompts
  - serialize data with fewer tokens
  - TOON format encoding and decoding
  - token-efficient data format for language models
  - replace JSON with TOON in my prompt
---

# Token-Oriented Object Notation (TOON)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

TOON is a compact, human-readable encoding of the JSON data model that minimizes tokens for LLM input. It combines YAML-style indentation for nested objects with CSV-style tabular layout for uniform arrays, achieving ~40% token reduction while maintaining or improving LLM comprehension accuracy.

## Installation

```bash
# npm
npm install @toon-format/toon

# pnpm
pnpm add @toon-format/toon

# yarn
yarn add @toon-format/toon
```

## CLI

```bash
# Install globally
npm install -g @toon-format/toon

# Convert JSON file to TOON
toon encode input.json
toon encode input.json -o output.toon

# Convert TOON back to JSON
toon decode input.toon
toon decode input.toon -o output.json

# Pipe support
cat data.json | toon encode
cat data.toon | toon decode

# Pretty-print JSON output
toon decode input.toon --pretty

# Show token count comparison
toon encode input.json --stats
```

## Core API

### encode / stringify

```typescript
import { encode, decode } from '@toon-format/toon';

// Basic encoding (JSON → TOON string)
const data = {
  context: {
    task: 'Our favorite hikes together',
    location: 'Boulder',
    season: 'spring_2025',
  },
  friends: ['ana', 'luis', 'sam'],
  hikes: [
    { id: 1, name: 'Blue Lake Trail', distanceKm: 7.5, elevationGain: 320, companion: 'ana', wasSunny: true },
    { id: 2, name: 'Ridge Overlook', distanceKm: 9.2, elevationGain: 540, companion: 'luis', wasSunny: false },
    { id: 3, name: 'Wildflower Loop', distanceKm: 5.1, elevationGain: 180, companion: 'sam', wasSunny: true },
  ],
};

const toon = encode(data);
console.log(toon);
// context:
//   task: Our favorite hikes together
//   location: Boulder
//   season: spring_2025
// friends[3]: ana,luis,sam
// hikes[3]{id,name,distanceKm,elevationGain,companion,wasSunny}:
//   1,Blue Lake Trail,7.5,320,ana,true
//   2,Ridge Overlook,9.2,540,luis,false
//   3,Wildflower Loop,5.1,180,sam,true
```

### decode / parse

```typescript
import { decode } from '@toon-format/toon';

const toonString = `
context:
  task: Our favorite hikes together
  location: Boulder
friends[2]: ana,luis
hikes[2]{id,name,distanceKm}:
  1,Blue Lake Trail,7.5
  2,Ridge Overlook,9.2
`;

const parsed = decode(toonString);
// Returns the original JavaScript object
console.log(parsed.hikes[0].name); // 'Blue Lake Trail'
```

### Encoding options

```typescript
import { encode } from '@toon-format/toon';

const toon = encode(data, {
  // Force all arrays to tabular format (default: auto-detect uniform arrays)
  tabular: 'always',

  // Never use tabular format
  // tabular: 'never',

  // Indent size for nested objects (default: 2)
  indent: 2,

  // Quote strings that contain special characters (default: auto)
  quoting: 'auto',
});
```

## Format Overview

### Primitive scalars

TOON encodes scalars the same way as YAML — unquoted when unambiguous:

```
name: Alice
age: 30
active: true
score: 98.6
nothing: null
```

### Nested objects (YAML-style indentation)

```
user:
  name: Alice
  address:
    city: Boulder
    zip: 80301
```

### Flat arrays (scalar items)

Square brackets declare the array length, values are comma-separated:

```
tags[3]: typescript,llm,serialization
scores[4]: 10,20,30,40
```

### Uniform object arrays (tabular format)

Curly braces declare the field headers; each subsequent indented line is a row:

```
employees[3]{id,name,department,salary}:
  1,Alice,Engineering,95000
  2,Bob,Marketing,72000
  3,Carol,Engineering,102000
```

### Quoting rules

Values containing commas, colons, or newlines are quoted:

```
notes[2]: "hello, world","line1\nline2"
messages[1]{from,text}:
  alice,"See you at 3:00, okay?"
```

### Mixed nesting

```
company:
  name: Acme Corp
  founded: 1987
  offices[2]: NYC,SF
  teams[2]{name,headcount}:
    Engineering,45
    Marketing,20
```

## Using TOON with LLMs

### Direct prompt injection

```typescript
import { encode } from '@toon-format/toon';
import OpenAI from 'openai';

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function queryWithToon(data: unknown, question: string) {
  const toon = encode(data);

  const response = await client.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      {
        role: 'system',
        content: [
          'You are a data analyst. The user will provide data in TOON format.',
          'TOON is a compact encoding of JSON: indentation = nesting,',
          'key[N]: v1,v2 = array of N scalars,',
          'key[N]{f1,f2}: rows = array of N objects with fields f1, f2.',
        ].join(' '),
      },
      {
        role: 'user',
        content: `Data:\n\`\`\`\n${toon}\n\`\`\`\n\nQuestion: ${question}`,
      },
    ],
  });

  return response.choices[0].message.content;
}

// Usage
const employees = [
  { id: 1, name: 'Alice', dept: 'Eng', salary: 95000 },
  { id: 2, name: 'Bob', dept: 'Marketing', salary: 72000 },
];

const answer = await queryWithToon(
  { employees },
  'Who has the highest salary?'
);
```

### Anthropic / Claude

```typescript
import { encode } from '@toon-format/toon';
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

async function analyzeWithClaude(data: unknown, prompt: string) {
  const toon = encode(data);

  const message = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 1024,
    system:
      'Data is in TOON format: indented = nested objects, key[N]: vals = scalar array, key[N]{fields}: rows = object array.',
    messages: [
      {
        role: 'user',
        content: `\`\`\`toon\n${toon}\n\`\`\`\n\n${prompt}`,
      },
    ],
  });

  return message.content[0].type === 'text' ? message.content[0].text : null;
}
```

### Token count comparison utility

```typescript
import { encode } from '@toon-format/toon';
import { encode as gptEncode } from 'gpt-tokenizer';

function compareTokens(data: unknown) {
  const jsonStr = JSON.stringify(data);
  const toonStr = encode(data);

  const jsonTokens = gptEncode(jsonStr).length;
  const toonTokens = gptEncode(toonStr).length;
  const savings = (((jsonTokens - toonTokens) / jsonTokens) * 100).toFixed(1);

  console.log(`JSON:  ${jsonTokens} tokens`);
  console.log(`TOON:  ${toonTokens} tokens`);
  console.log(`Saved: ${savings}%`);

  return { jsonTokens, toonTokens, savings: parseFloat(savings) };
}
```

## Common Patterns

### Batch API calls with TOON

```typescript
import { encode } from '@toon-format/toon';

// Encode each record separately for independent LLM calls
function encodeRecords<T>(records: T[]): string[] {
  return records.map((r) => encode(r));
}

// Encode all records as one TOON document (most efficient for bulk)
function encodeAll<T>(records: T[], key = 'records'): string {
  return encode({ [key]: records });
}
```

### RAG / retrieval context injection

```typescript
import { encode } from '@toon-format/toon';

interface SearchResult {
  id: string;
  title: string;
  snippet: string;
  score: number;
  url: string;
}

function buildRagContext(results: SearchResult[]): string {
  // TOON is ideal here — uniform objects collapse into a compact table
  return encode({ results });
}

// Output:
// results[5]{id,title,snippet,score,url}:
//   doc1,Introduction to TOON,...,0.95,https://...
//   doc2,TOON vs JSON,...,0.87,https://...
```

### Streaming encode for large datasets

```typescript
import { encode } from '@toon-format/toon';
import { createReadStream, createWriteStream } from 'fs';

// For large JSON files: read → parse → encode → write
async function convertFile(inputPath: string, outputPath: string) {
  const raw = await fs.promises.readFile(inputPath, 'utf-8');
  const data = JSON.parse(raw);
  const toon = encode(data);
  await fs.promises.writeFile(outputPath, toon, 'utf-8');

  const jsonBytes = Buffer.byteLength(raw);
  const toonBytes = Buffer.byteLength(toon);
  console.log(`Reduced size by ${(((jsonBytes - toonBytes) / jsonBytes) * 100).toFixed(1)}%`);
}
```

### Schema-aware encoding (TypeScript)

```typescript
import { encode, decode } from '@toon-format/toon';

interface Employee {
  id: number;
  name: string;
  department: string;
  salary: number;
  active: boolean;
}

interface EmployeeReport {
  generatedAt: string;
  employees: Employee[];
}

// Encode is generic-friendly — pass any serializable object
const report: EmployeeReport = {
  generatedAt: new Date().toISOString(),
  employees: [
    { id: 1, name: 'Alice', department: 'Engineering', salary: 95000, active: true },
    { id: 2, name: 'Bob', department: 'Marketing', salary: 72000, active: true },
  ],
};

const toon = encode(report);

// Decode back with type assertion
const recovered = decode(toon) as EmployeeReport;
console.log(recovered.employees[0].name); // 'Alice'
```

### Express middleware for TOON content-type

```typescript
import express from 'express';
import { encode, decode } from '@toon-format/toon';

const app = express();

// Parse incoming TOON bodies
app.use((req, res, next) => {
  if (req.headers['content-type']?.startsWith('text/toon')) {
    let body = '';
    req.on('data', (chunk) => (body += chunk));
    req.on('end', () => {
      try {
        (req as any).toonBody = decode(body);
        next();
      } catch (e) {
        res.status(400).json({ error: 'Invalid TOON body' });
      }
    });
  } else {
    next();
  }
});

// Respond with TOON when client requests it
app.get('/api/employees', (req, res) => {
  const employees = [
    { id: 1, name: 'Alice', dept: 'Eng' },
    { id: 2, name: 'Bob', dept: 'Marketing' },
  ];

  if (req.headers.accept?.includes('text/toon')) {
    res.setHeader('Content-Type', 'text/toon; charset=utf-8');
    res.send(encode({ employees }));
  } else {
    res.json({ employees });
  }
});
```

## When to Use TOON vs JSON

| Scenario | Recommendation |
|---|---|
| Uniform arrays of objects | ✅ TOON (biggest savings) |
| Deeply nested / non-uniform | ⚠️ Benchmark both; JSON-compact may win |
| Pure flat tabular data | Consider CSV (smaller) or TOON (structured) |
| Latency-critical (local models) | Benchmark TTFT + tokens/sec |
| Programmatic API calls | Keep JSON; encode to TOON only for LLM input |
| Semi-uniform (~40–60% tabular) | Benchmark; savings diminish |

## Troubleshooting

### Values with commas parse incorrectly

Wrap them in double quotes in your TOON string, or ensure `encode()` handles it automatically:

```typescript
// encode() automatically quotes values containing commas
const data = { tags: ['hello, world', 'foo,bar'] };
encode(data);
// tags[2]: "hello, world","foo,bar"
```

### Round-trip type loss (numbers vs strings)

TOON uses unquoted values for numbers and booleans. Ensure your data uses proper JS types before encoding — don't pass `"95000"` (string) when you mean `95000` (number):

```typescript
// ✅ Correct
{ salary: 95000, active: true }

// ❌ Will decode as string "95000" and string "true"
{ salary: '95000', active: 'true' }
```

### LLM misreads tabular rows

Add a brief TOON format explanation to your system prompt:

```
TOON format rules:
- Indentation = nested object
- key[N]: v1,v2,v3 = array of N scalar values
- key[N]{field1,field2}: followed by N indented rows = array of objects
```

### CLI not found after global install

```bash
# Verify global bin path is on your PATH
npm bin -g   # or: npm root -g

# Alternatively use npx
npx @toon-format/toon encode input.json
```

### Decoding fails on hand-written TOON

Common mistakes in hand-written TOON:
- Missing length declaration: `items{id,name}:` → must be `items[2]{id,name}:`
- Inconsistent indentation (mix of tabs/spaces)
- Unquoted values containing `:` as first character

## Resources

- [Official Specification (SPEC v3.0)](https://github.com/toon-format/spec/blob/main/SPEC.md)
- [npm package: @toon-format/toon](https://www.npmjs.com/package/@toon-format/toon)
- [Online Playground](https://toonformat.dev)
- [GitHub Repository](https://github.com/toon-format/toon)
