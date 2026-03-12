---
name: file-based-routing-for-static-sites
description: Learn how to create a multi-page static site with file-based routing using TypeScript, allowing for quick updates and easy content management.
metadata:
  url: https://rodydavis.com/posts/static-site-file-based-routing
  last_modified: Tue, 03 Feb 2026 20:04:23 GMT
---

# File Based Routing for Static Sites


In this article I will go over how to use file based routing to output as a static site multi page application.

> **TLDR** The final source [here](https://github.com/rodydavis/static-site-file-based-routing) and an online [demo](https://rodydavis.github.io/static-site-file-based-routing/).

## Step 1 

Create a new folder called “static-site-file-based-routing” and open it up in VSCode.

```
mkdir static-site-file-based-routing
cd static-site-file-based-routing
code .
```

## Step 2 

Create a `tsconfig.json` and replace it with the following:

```
{
  "compilerOptions": {
    "incremental": true,
    "target": "es5",
    "module": "es2020",
    "outDir": "dist",
    "strict": true,
    "moduleResolution": "node",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "typeRoots": [
      "node_modules/@types",
      "src/@types"
    ]
  },
  "include": [
    "src/**/*"
  ],
  "exclude": [
    "node_modules",
    "dist"
  ]
}
```

## Step 3 

Create a `package.json` and update it with the following:

```
{
  "name": "static-site-file-based-routing",
  "version": "1.0.0",
  "description": "File based routing for HTML MPA",
  "type": "module",
  "scripts": {
    "start": "wds --node-resolve --root-dir build --base-path /static-site-file-based-routing --open --watch",
    "postinstall": "npm run tsc",
    "build": "node dist/main.js --inputDir ./example --outputDir ./build",
    "dev": "node dist/main.js --inputDir ./example --outputDir ./build -w",
    "tsc": "tsc",
    "tsc:watch": "tsc -w"
  },
  "devDependencies": {
    "@pkgjs/parseargs": "^0.10.0",
    "@types/markdown-it": "^12.2.3",
    "@types/node": "^18.7.23",
    "@web/dev-server": "^0.1.34",
    "chokidar": "^3.5.3",
    "highlight.js": "^11.6.0",
    "html-format": "^1.0.2",
    "markdown-it": "^13.0.1",
    "parse5": "^7.1.1",
    "typescript": "^4.8.4"
  }
}
```

Then run `npm install` to install all the dependencies.

> I am using `@web/dev-server` to serve the site locally. You can use any server you want.

These dependencies are used for various file transformations such as markdown to HTML, HTML formatting, and file watching.

## Step 4 

Create a `src` folder and add 4 files:

### `src/build.ts` 

```
import * as fs from "fs";
import { compileDir, compileTarget } from "./compile.js";
import * as path from "path";
import chokidar from "chokidar";
import { publicDirectory } from "./static.js";

interface Options {
    inputDir?: string;
    outputDir?: string;
    publicDir?: string;
    watch?: boolean;
    clean?: boolean;
}

export default async function build(options: Options) {
    const inputDir = options.inputDir || "www";
    const outputDir = options.outputDir || "build";
    const publicDir = options.publicDir || "public";
    const watch = options.watch || false;
    const clean = options.clean || false;

    if (!fs.existsSync(inputDir)) {
        throw new Error(`Input directory ${inputDir} does not exist`);
    }

    if (clean) {
        if (fs.existsSync(outputDir)) {
            fs.rmdirSync(outputDir, { recursive: true });
        }
    }

    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    if (watch) {
        console.log("Watching for changes...");
        chokidar.watch(inputDir).on("all", async (event, inputFile) => {
            console.log(event, inputFile);
            if (fs.existsSync(inputFile)) {
                const relativePath = path.relative(inputDir, inputFile);
                const outputFile = `${outputDir}/${relativePath}`;

                const stat = fs.statSync(inputFile);
                if (stat.isDirectory()) {
                    await compileDir(inputFile, outputFile);
                } else if (stat.isFile()) {
                    const filename = path.basename(inputFile);
                    if (filename === "layout.html") {
                        // Rebuild all related directories
                        const dir = path.dirname(inputFile);
                        const inDir = path.relative(inputDir, dir);
                        const outDir = `${outputDir}/${inDir}`;
                        await compileDir(dir, outDir);
                    } else {
                        await compileTarget(inputFile, outputFile);
                    }
                }
            }
        });
    } else {
        await compileDir(inputDir, outputDir);
    }

    if (publicDir.split(',').length > 1) {
        for (const dir of publicDir.split(',')) {
            publicDirectory(dir, outputDir, watch);
        }
    } else {
        publicDirectory(publicDir, outputDir, watch);
    }
}
```

### `src/compile.ts` 

```
import * as fs from "fs";
import * as path from "path";
import MarkdownIt from "markdown-it";
import hljs from "highlight.js";
import * as parse5 from "parse5";
import type { Document } from "parse5/dist/tree-adapters/default.js";
import format from 'html-format';

function compile(file: string) {
    const raw = fs.readFileSync(file, "utf-8");
    const ext = path.extname(file);

    switch (ext) {
        case ".md":
        case ".markdown":
            const md = new MarkdownIt({
                html: true,
                linkify: true,
                typographer: true,
                highlight: function (str, lang) {
                    if (lang && hljs.getLanguage(lang)) {
                        try {
                            return (
                                '<pre class="hljs"><code>' +
                                hljs.highlight(str, { language: lang, ignoreIllegals: true })
                                    .value +
                                "</code></pre>"
                            );
                        } catch (__) {
                            console.error(__);
                        }
                    }
                    return "";
                },
            });
            return parse5.parse(md.render(raw));
        case ".html":
            return parse5.parse(raw);
        default:
            break;
    }

    return raw;
}

function createHtml(options?: { head?: string; body?: string; }) {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
${options?.head ?? ""}
</head>
<body>
${options?.body ?? "<slot></slot>"}
</body>
</html>
`;
}

export async function compileFile(file: string, target: string) {
    // Use regex to check if ends with index.*
    const isIndex = /index\.([a-z]+)$/i.test(file);

    if (!isIndex && !fs.statSync(file).isDirectory()) {
        // Skipping for nested layouts
        return;
    }

    const parent = path.dirname(target);

    // Render up the directory tree until we hit the root directory
    const files: string[] = [file];
    let filePath = file;
    while (filePath !== parent) {
        filePath = path.dirname(filePath);
        // Check for root level layout
        const layout = path.join(filePath, "layout.html");
        if (fs.existsSync(layout)) {
            files.unshift(layout);
        }
        if (filePath === ".") break;
    }

    // Check for root level index markdown or html
    const layout = path.join(parent, "layout.html");
    if (fs.existsSync(layout)) {
        if (
            fs.existsSync(path.join(parent, "index.html")) ||
            fs.existsSync(path.join(parent, "index.md")) ||
            fs.existsSync(path.join(parent, "index.markdown"))
        ) {
            files.unshift(layout);
        }
    }

    let output = createHtml();

    for (const item of files) {
        const doc = compile(item);
        if (typeof doc !== 'string') {
            const content = parse5.serialize(doc);
            output = mergeDocuments(output, content);
        }
    }

    // Replace extension
    const ext = path.extname(file);
    const newFile = target.replace(ext, '.html');

    // Check if parent directory exists
    const parentDir = path.dirname(newFile);
    if (!fs.existsSync(parentDir)) {
        fs.mkdirSync(parentDir, { recursive: true });
    }

    fs.writeFileSync(newFile, output);
    console.log(`--> ${newFile}`);
}

function mergeDocuments(current: string, source: string) {
    let raw = current;

    // Merge body
    const html = extractDoc(parse5.parse(source));
    // Check for <slot></slot>
    const hasSlot = raw.includes("<slot></slot>");
    if (hasSlot) {
        raw = raw.replace("<slot></slot>", parse5.serialize(html.body));
    } else {
        // Append to body
        const endBodyIdx = raw.lastIndexOf("</body>");
        const start = raw.slice(0, endBodyIdx);
        const end = raw.slice(endBodyIdx);
        const body = parse5.serialize(html.body);
        raw = start + body + end;
    }

    // Merge head
    const endHeadIdx = raw.lastIndexOf("</head>");
    const start = raw.slice(0, endHeadIdx);
    const end = raw.slice(endHeadIdx);
    const head = parse5.serialize(html.head);
    raw = start + head + end;

    // Format
    raw = format(raw);

    // Remove duplicate title tags
    const lastTitle = raw.lastIndexOf("<title>");
    const lastTitleEnd = raw.lastIndexOf("</title>");
    const title = raw.slice(lastTitle, lastTitleEnd + 8);
    raw = raw.replace(/<title>.*<\/title>/, "");
    raw = raw.replace("</head>", title + "</head>");

    return raw;
}

function extractDoc(doc: Document) {
    const html = (doc.childNodes[1] ?? doc.childNodes[0]) as unknown as Document;
    const head = html.childNodes.find(
        (node) => node.nodeName === "head"
    ) as unknown as Document;
    const body = html.childNodes.find(
        (node) => node.nodeName === "body"
    ) as unknown as Document;
    return { head, body };
}

export async function compileDir(inputDir: string, outputDir: string) {
    const files = fs.readdirSync(inputDir);
    for (const file of files) {
        const inputFile = `${inputDir}/${file}`;
        const outputFile = `${outputDir}/${file}`;

        await compileTarget(inputFile, outputFile);
    }
}

export async function compileTarget(input: string, output: string) {
    const stat = fs.statSync(input);
    if (stat.isDirectory()) {
        if (!fs.existsSync(output)) {
            fs.mkdirSync(output, { recursive: true });
        }
        await compileDir(input, output);
    } else if (stat.isFile()) {
        const ext = path.extname(input);
        if (['.html', '.md', '.markdown'].includes(ext)) {
            await compileFile(input, output);
        } else {
            const current = fs.readFileSync(input);
            const parentDir = path.dirname(output);
            if (!fs.existsSync(parentDir)) {
                fs.mkdirSync(parentDir, { recursive: true });
            }
            if (fs.existsSync(output)) {
                // Check if content is the same
                const previous = fs.readFileSync(output);
                if (Buffer.compare(current, previous) !== 0) {
                    fs.writeFileSync(output, current);
                }
            } else {
                // Copy the file
                fs.copyFileSync(input, output);
            }
        }
    }
}
```

### `src/static.ts` 

```
import * as fs from "fs";
import * as path from "path";
import chokidar from "chokidar";

export function publicDirectory(publicDir: string, outputDir: string, watch: boolean) {
    if (watch) {
        if (fs.existsSync(publicDir)) {
            chokidar.watch(publicDir).on("all", (event, inputFile) => {
                console.log(event, inputFile);
                if (fs.existsSync(inputFile)) {
                    const relativePath = path.relative(publicDir, inputFile);
                    const outputFile = `${outputDir}/${relativePath}`;

                    const stat = fs.statSync(inputFile);
                    if (stat.isDirectory()) {
                        copyStaticFiles(inputFile, outputFile);
                    } else if (stat.isFile()) {
                        fs.copyFileSync(inputFile, outputFile);
                    }
                }
            });
        }
    } else {
        // Copy static files
        if (fs.existsSync(publicDir)) {
            copyStaticFiles(publicDir, outputDir);
        }
    }
}

function copyStaticFiles(inDir: string, outDir: string) {
    const files = fs.readdirSync(inDir);
    for (const file of files) {
        const inputFile = `${inDir}/${file}`;
        const outputFile = `${outDir}/${file}`;

        const stat = fs.statSync(inputFile);
        if (stat.isDirectory()) {
            if (!fs.existsSync(outputFile)) {
                fs.mkdirSync(outputFile, { recursive: true });
            }

            copyStaticFiles(inputFile, outputFile);
        } else if (stat.isFile()) {
            fs.copyFileSync(inputFile, outputFile);
        }
    }
}
```

### `src/main.ts` 

```
#!/usr/bin/env node

// @ts-ignore
import { parseArgs } from "@pkgjs/parseargs";
import build from "./build.js";

export async function main() {
  const {
    values: { inputDir, outputDir, watch },
  } = parseArgs({
    options: {
      inputDir: {
        type: "string",
        short: "i",
      },
      outputDir: {
        type: "string",
        short: "o",
      },
      watch: {
        type: "boolean",
        short: "w",
      },
    },
    allowPositional: true,
  });

  if (inputDir === undefined || outputDir === undefined) {
    console.log("Usage: build -i <inputDir> -o <outputDir> [-w]");
    return;
  }

  await build({
    inputDir,
    outputDir,
    watch,
  });
}

main();
```

## Step 5 

Now that the project is setup we can start the typescript compiler in watch mode.

```
npm run ts:watch
```

## Step 6 

Now create a folder that will contain the source files for the website.

### `example/index.md` 

```
# Hello World

This is a test
```

### `example/style.css` 

```
body {
    background-color: #000;
    color: #fff;
}
```

### `example/layout.html` 

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Example</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <slot></slot>
</body>
</html>
```

## Step 7 

With the source files created we can now run the build script.

For a one time build run:

```
npm run build
```

For a watch mode run:

```
npm run dev
```

Now start the http server:

```
npm run start
```

## Conclusion 

As you make changes it will only update affected files and be very fast to update.

> Note that this does not bundle the javascript and will be up to you if you are using `node_modules` in any files (for the example in the repo I show how to use **UNPKG**).

If you want to find the source code you can check it out [here](https://github.com/rodydavis/static-site-file-based-routing) otherwise thanks for reading and let me know if you have any questions!