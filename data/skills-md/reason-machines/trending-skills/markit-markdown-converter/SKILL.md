---
name: markit-markdown-converter
description: Convert files, URLs, and media to markdown using the markit-ai CLI and SDK with pluggable converters and LLM support.
triggers:
  - convert PDF to markdown
  - turn a DOCX into markdown
  - extract markdown from a URL
  - convert images or audio to markdown with AI
  - use markit to convert files
  - install markit CLI
  - write a markit plugin
  - use markit as a library in TypeScript
---

# markit-markdown-converter

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

markit converts almost anything to markdown: PDFs, Word docs, PowerPoint, Excel, HTML, EPUB, Jupyter notebooks, RSS feeds, CSV, JSON, YAML, images (with EXIF + AI description), audio (with metadata + AI transcription), ZIP archives, URLs, Wikipedia pages, and source code files. It works as a CLI tool and as a TypeScript/Node.js library, supports pluggable converters, and integrates with OpenAI, Anthropic, and any OpenAI-compatible LLM API.

---

## Installation

```bash
# Global CLI
npm install -g markit-ai

# Or as a project dependency
npm install markit-ai
# bun add markit-ai
# pnpm add markit-ai
```

---

## CLI Quick Reference

```bash
# Convert a file
markit report.pdf
markit document.docx
markit slides.pptx
markit data.xlsx
markit notebook.ipynb

# Convert a URL
markit https://example.com/article
markit https://en.wikipedia.org/wiki/Markdown

# Convert media (requires LLM API key for AI features)
markit photo.jpg
markit recording.mp3
markit diagram.png -p "Describe the architecture and data flow"
markit receipt.jpg -p "List all line items with prices as a table"

# Output options
markit report.pdf -o report.md          # Write to file
markit report.pdf -q                    # Raw markdown only (great for piping)
markit report.pdf --json                # Structured JSON output

# Read from stdin
cat file.pdf | markit -

# Pipe output
markit report.pdf | pbcopy
markit data.xlsx -q | some-other-tool

# List supported formats
markit formats

# Configuration
markit init                              # Create .markit/config.json
markit config show                       # Show resolved config
markit config get llm.model
markit config set llm.provider anthropic
markit config set llm.model claude-haiku-4-5

# Plugins
markit plugin install npm:markit-plugin-dwg
markit plugin install git:github.com/user/markit-plugin-ocr
markit plugin install ./my-plugin.ts
markit plugin list
markit plugin remove dwg

# Agent integration
markit onboard                           # Adds usage instructions to CLAUDE.md
```

---

## AI / LLM Configuration

Images and audio always get free metadata extraction. AI-powered description and transcription requires an API key.

```bash
# OpenAI (default)
export OPENAI_API_KEY=sk-...
markit photo.jpg

# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...
markit config set llm.provider anthropic
markit photo.jpg

# OpenAI-compatible APIs (Ollama, Groq, Together, etc.)
markit config set llm.apiBase http://localhost:11434/v1
markit config set llm.model llama3.2-vision
markit photo.jpg
```

`.markit/config.json` (created by `markit init`):

```json
{
  "llm": {
    "provider": "openai",
    "apiBase": "https://api.openai.com/v1",
    "model": "gpt-4.1-nano",
    "transcriptionModel": "gpt-4o-mini-transcribe"
  }
}
```

Environment variables always override config file values. Never store API keys in the config file — use env vars.

| Provider    | Env Vars                              | Default Vision Model  |
|-------------|---------------------------------------|-----------------------|
| `openai`    | `OPENAI_API_KEY`, `MARKIT_API_KEY`    | `gpt-4.1-nano`        |
| `anthropic` | `ANTHROPIC_API_KEY`, `MARKIT_API_KEY` | `claude-haiku-4-5`    |

---

## SDK Usage

### Basic File and URL Conversion

```typescript
import { Markit } from "markit-ai";

const markit = new Markit();

// Convert a file by path
const { markdown } = await markit.convertFile("report.pdf");
console.log(markdown);

// Convert a URL
const { markdown: webMd } = await markit.convertUrl("https://example.com/article");

// Convert a Buffer with explicit type hint
import { readFileSync } from "fs";
const buffer = readFileSync("document.docx");
const { markdown: docMd } = await markit.convert(buffer, { extension: ".docx" });
```

### With OpenAI for Vision + Transcription

```typescript
import OpenAI from "openai";
import { Markit } from "markit-ai";

const openai = new OpenAI(); // reads OPENAI_API_KEY from env

const markit = new Markit({
  describe: async (image: Buffer, mime: string) => {
    const res = await openai.chat.completions.create({
      model: "gpt-4.1-nano",
      messages: [
        {
          role: "user",
          content: [
            { type: "text", text: "Describe this image in detail." },
            {
              type: "image_url",
              image_url: {
                url: `data:${mime};base64,${image.toString("base64")}`,
              },
            },
          ],
        },
      ],
    });
    return res.choices[0].message.content ?? "";
  },

  transcribe: async (audio: Buffer, mime: string) => {
    const res = await openai.audio.transcriptions.create({
      model: "gpt-4o-mini-transcribe",
      file: new File([audio], "audio.mp3", { type: mime }),
    });
    return res.text;
  },
});

const { markdown } = await markit.convertFile("photo.jpg");
```

### With Anthropic for Vision

```typescript
import Anthropic from "@anthropic-ai/sdk";
import OpenAI from "openai";
import { Markit } from "markit-ai";

const anthropic = new Anthropic(); // reads ANTHROPIC_API_KEY from env
const openai = new OpenAI();       // reads OPENAI_API_KEY from env

// Mix providers: Claude for images, OpenAI Whisper for audio
const markit = new Markit({
  describe: async (image: Buffer, mime: string) => {
    const res = await anthropic.messages.create({
      model: "claude-haiku-4-5",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: {
                type: "base64",
                media_type: mime as "image/jpeg" | "image/png" | "image/gif" | "image/webp",
                data: image.toString("base64"),
              },
            },
            { type: "text", text: "Describe this image." },
          ],
        },
      ],
    });
    return (res.content[0] as { text: string }).text;
  },

  transcribe: async (audio: Buffer, mime: string) => {
    const res = await openai.audio.transcriptions.create({
      model: "gpt-4o-mini-transcribe",
      file: new File([audio], "audio.mp3", { type: mime }),
    });
    return res.text;
  },
});
```

### Using Built-in Providers via Config

```typescript
import { Markit, createLlmFunctions, loadConfig, loadAllPlugins } from "markit-ai";

// Reads .markit/config.json and env vars automatically
const config = loadConfig();

// Load any installed plugins
const plugins = await loadAllPlugins();

// Create instance with built-in providers + plugins
const markit = new Markit(createLlmFunctions(config), plugins);

const { markdown } = await markit.convertFile("report.pdf");
```

---

## Writing a Plugin

Plugins let you add new formats or override built-in converters. Plugin converters run before built-ins.

### Basic Converter Plugin

```typescript
// my-plugin.ts
import type { MarkitPluginAPI } from "markit-ai";

export default function (api: MarkitPluginAPI) {
  api.setName("my-format");
  api.setVersion("1.0.0");

  api.registerConverter(
    {
      name: "myformat",
      accepts: (info) => [".myf", ".myfmt"].includes(info.extension ?? ""),
      convert: async (input: Buffer, info) => {
        // info.extension, info.mimeType, info.fileName available
        const text = input.toString("utf-8");
        const markdown = `# Converted\n\n\`\`\`\n${text}\n\`\`\``;
        return { markdown };
      },
    },
    // Optional: declare so it appears in `markit formats`
    { name: "My Format", extensions: [".myf", ".myfmt"] },
  );
}
```

### Override a Built-in Converter

```typescript
// better-pdf-plugin.ts
import type { MarkitPluginAPI } from "markit-ai";

export default function (api: MarkitPluginAPI) {
  api.setName("better-pdf");
  api.setVersion("1.0.0");

  // Runs before built-in PDF converter, effectively replacing it
  api.registerConverter({
    name: "pdf",
    accepts: (info) => info.extension === ".pdf",
    convert: async (input: Buffer, info) => {
      // Custom PDF extraction logic
      const markdown = `# PDF Content\n\n(extracted with custom logic)`;
      return { markdown };
    },
  });
}
```

### Register a Custom LLM Provider

```typescript
import type { MarkitPluginAPI } from "markit-ai";

export default function (api: MarkitPluginAPI) {
  api.setName("gemini-provider");

  api.registerProvider({
    name: "gemini",
    envKeys: ["GOOGLE_API_KEY"],
    defaultBase: "https://generativelanguage.googleapis.com/v1beta",
    defaultModel: "gemini-2.0-flash",
    create: (config, prompt) => ({
      describe: async (image: Buffer, mime: string) => {
        // Call Gemini API here
        return "Image description from Gemini";
      },
    }),
  });
}
```

### Install and Use a Plugin

```bash
# Install from file
markit plugin install ./my-plugin.ts

# Install from npm
markit plugin install npm:markit-plugin-dwg

# Install from git
markit plugin install git:github.com/user/markit-plugin-ocr

# Verify
markit plugin list

# Remove
markit plugin remove my-format
```

---

## Common Patterns

### Batch Convert a Directory

```typescript
import { Markit } from "markit-ai";
import { readdirSync, readFileSync, writeFileSync } from "fs";
import { extname, basename, join } from "path";

const markit = new Markit();
const inputDir = "./docs";
const outputDir = "./docs-md";

const files = readdirSync(inputDir);
for (const file of files) {
  const ext = extname(file);
  if (![".pdf", ".docx", ".html"].includes(ext)) continue;

  const buffer = readFileSync(join(inputDir, file));
  const { markdown } = await markit.convert(buffer, { extension: ext });
  const outName = basename(file, ext) + ".md";
  writeFileSync(join(outputDir, outName), markdown);
  console.log(`Converted: ${file} → ${outName}`);
}
```

### Convert URL List

```typescript
import { Markit } from "markit-ai";

const markit = new Markit();
const urls = [
  "https://example.com/article-1",
  "https://example.com/article-2",
  "https://en.wikipedia.org/wiki/TypeScript",
];

const results = await Promise.all(
  urls.map(async (url) => {
    const { markdown } = await markit.convertUrl(url);
    return { url, markdown };
  })
);

for (const { url, markdown } of results) {
  console.log(`\n## ${url}\n\n${markdown.slice(0, 200)}...`);
}
```

### CLI in Agent/Automation Scripts

```bash
# Structured JSON for programmatic parsing
markit report.pdf --json

# Raw markdown for piping (no spinner, no extra output)
markit report.pdf -q > report.md

# Pipe into another CLI tool
markit https://example.com/article -q | wc -w

# Process multiple files in a shell loop
for f in docs/*.pdf; do
  markit "$f" -o "out/$(basename "$f" .pdf).md"
done
```

---

## Supported Formats Reference

| Format      | Extensions                              |
|-------------|-----------------------------------------|
| PDF         | `.pdf`                                  |
| Word        | `.docx`                                 |
| PowerPoint  | `.pptx`                                 |
| Excel       | `.xlsx`                                 |
| HTML        | `.html`, `.htm`                         |
| EPUB        | `.epub`                                 |
| Jupyter     | `.ipynb`                                |
| RSS/Atom    | `.rss`, `.atom`, `.xml`                 |
| CSV/TSV     | `.csv`, `.tsv`                          |
| JSON        | `.json`                                 |
| YAML        | `.yaml`, `.yml`                         |
| XML/SVG     | `.xml`, `.svg`                          |
| Images      | `.jpg`, `.png`, `.gif`, `.webp`         |
| Audio       | `.mp3`, `.wav`, `.m4a`, `.flac`         |
| ZIP         | `.zip`                                  |
| Code        | `.py`, `.ts`, `.go`, `.rs`, and more    |
| Plain text  | `.txt`, `.md`, `.rst`, `.log`           |
| URLs        | `http://`, `https://`                   |

Run `markit formats` to see the full live list including any installed plugins.

---

## Troubleshooting

**AI description/transcription not working**
- Ensure the correct env var is set: `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- Run `markit config show` to verify the resolved provider and model
- For custom API bases (Ollama, etc.), confirm the server is running and the model supports vision

**Plugin not loading**
- Run `markit plugin list` to confirm it's installed
- Check the plugin exports a default function matching `(api: MarkitPluginAPI) => void`
- Try reinstalling: `markit plugin remove <name>` then `markit plugin install <source>`

**PDF returns empty or garbled markdown**
- The built-in converter uses text extraction (not OCR). Scanned PDFs need an OCR plugin.
- Try a custom plugin or pre-process with an OCR tool first.

**Stdin (`markit -`) not working**
- Pipe content directly: `cat file.pdf | markit -`
- Ensure the file type can be detected from content; use explicit hints if needed.

**Config not being read**
- Config is loaded from `.markit/config.json` relative to the current working directory
- Run `markit init` to create it, then `markit config show` to verify
