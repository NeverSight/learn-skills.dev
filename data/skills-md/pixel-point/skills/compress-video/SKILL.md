---
name: compress-video
description: Compress local videos with FFmpeg, compare codec/CRF quality, audit embedded videos on a website, or scan and optimize videos across a website's source project.
---

Compress videos locally using FFmpeg and FFprobe. Install missing dependencies
needed for the requested workflow. Website workflows require source-code access
and browser tools to verify the rendered site.

## Commands

| Request | Workflow |
| --- | --- |
| A video file, or `compress <file>` | Compress using [compression.md](references/compression.md). |
| `compare <file>` | Compare quality and estimated sizes using [comparison.md](references/comparison.md). |
| `audit [project] [URL or scope]` | Inspect embedded videos and report improvements using [audit.md](references/audit.md). |
| `scan-and-optimize [project] [URL or scope]` | Discover, audit, optimize, and update videos across the project using [scan-and-optimize.md](references/scan-and-optimize.md). |

Infer the workflow from natural-language requests too. Read only the relevant
references. A file without a command uses the compression workflow.

For both website workflows, use the current workspace or a supplied project
path. If source code is unavailable, ask for repository access before starting.
Begin with routes, components, styles, and asset references in the source code;
use a live or local URL to verify rendered video sizes and playback. If no URL
is supplied, reuse a development server or start the project locally.

`audit` reviews the requested page and its source code, or the specified scope.
`scan-and-optimize` covers the whole source project by default; a supplied URL
is its browser starting point. Honor an explicitly narrower scope. Ask for a
missing input only when it cannot be inferred.

Reuse source locations and preferences already provided. Compression defaults,
including CRF values, are defined in [compression.md](references/compression.md).

## Examples

```text
$compress-video demo.mov
$compress-video compare demo.mov
$compress-video audit ./website https://example.com/blog/post
$compress-video scan-and-optimize ./website http://localhost:3000
```

These are agent requests, not terminal commands.
