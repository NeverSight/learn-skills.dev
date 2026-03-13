---
name: windmill-workflows
description: |
  Windmill workflow engine deployment and scripting. Use when:
  (1) Setting up Windmill self-hosted with Docker Compose
  (2) Building custom worker images with PDF/image processing tools
  (3) Writing scripts for PDF text extraction, manipulation, or conversion
  (4) Writing scripts for image processing with libvips
  (5) Configuring workers, scaling, and resource limits
  (6) Troubleshooting job execution or worker issues
  (7) Integrating Windmill with Caddy reverse proxy
---

# Windmill Workflow Engine

Windmill is an open-source workflow engine for building internal tools with TypeScript, Python, Go, Bash, and more. This skill focuses on self-hosting and custom worker images for PDF/image processing.

## Quick Reference

| Task | Command/Location |
|------|------------------|
| Web UI | `https://windmill.example.com` |
| Default login | `admin@windmill.dev` / `changeme` |
| View logs | `docker compose logs -f windmill-worker` |
| Restart workers | `docker compose restart windmill-worker` |
| Build custom worker | `docker compose build windmill-worker` |
| Scale workers | Set `replicas: N` in docker-compose.yml |

## Architecture

```
Caddy → Server (port 8000) → PostgreSQL
              ↓
         Workers (N replicas) → Job Containers
              ↓
            LSP (port 3001)
```

- **Server**: API + frontend
- **Workers**: Execute jobs, spawn Docker containers
- **LSP**: Editor intellisense
- **PostgreSQL**: State and job queue

## Custom Worker with PDF/Image Tools

Build a worker with pdfcpu, Poppler, and libvips (~150MB overhead):

```dockerfile
FROM ghcr.io/windmill-labs/windmill:main

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libvips-tools \
    && rm -rf /var/lib/apt/lists/*

# Add pdfcpu
RUN curl -fsSL "https://github.com/pdfcpu/pdfcpu/releases/download/v0.11.1/pdfcpu_0.11.1_Linux_x86_64.tar.xz" \
    | tar -xJf - -C /usr/local/bin --strip-components=1
```

### Included Tools

| Tool | Purpose |
|------|---------|
| `pdftotext` | Extract text from PDFs |
| `pdfimages` | Extract embedded images |
| `pdftoppm` | Convert PDF to images |
| `pdfcpu` | Merge, split, watermark, encrypt |
| `vips` | Fast image resize/convert |
| `vipsthumbnail` | Ultra-fast thumbnails |

## Common Scripts

### Extract text from PDF

```typescript
import { $ } from "bun";

export async function main(pdfPath: string): Promise<string> {
  return await $`pdftotext -layout ${pdfPath} -`.text();
}
```

### Convert PDF to images

```typescript
import { $ } from "bun";

export async function main(pdfPath: string): Promise<string[]> {
  const outDir = `/tmp/pdf_${Date.now()}`;
  await $`mkdir -p ${outDir}`;
  await $`pdftoppm -png -r 300 ${pdfPath} ${outDir}/page`;
  return (await $`ls ${outDir}/*.png`.text()).trim().split('\n');
}
```

### Resize image (fast, memory-efficient)

```typescript
import { $ } from "bun";

export async function main(imagePath: string, width: number): Promise<string> {
  const output = `/tmp/resized_${Date.now()}.jpg`;
  await $`vipsthumbnail ${imagePath} -s ${width} -o ${output}[Q=85,strip]`;
  return output;
}
```

### Merge PDFs

```typescript
import { $ } from "bun";

export async function main(pdfs: string[]): Promise<string> {
  const output = `/tmp/merged_${Date.now()}.pdf`;
  await $`pdfunite ${pdfs.join(' ')} ${output}`;
  return output;
}
```

## libvips vs ImageMagick

libvips is chosen for memory-constrained environments:
- **4-8x faster** than ImageMagick
- **90% less memory** (~200MB vs ~3GB for large images)
- Streaming architecture (processes in chunks)

## Docker Compose Example

```yaml
windmill-worker:
  build:
    context: ./windmill-worker
    dockerfile: Dockerfile
  image: windmill-worker-custom:latest
  environment:
    - DATABASE_URL=${DATABASE_URL}
    - MODE=worker
    - WORKER_GROUP=default
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
  mem_limit: 1.5g
  cpus: 1.0
  deploy:
    replicas: 2
```

## Resource Guidelines

| Component | Memory | CPU |
|-----------|--------|-----|
| Server | 1GB | 1.0 |
| Worker | 1.5GB | 1.0 |
| LSP | 512MB | 0.5 |

**Scaling rule**: 1 worker per 1 vCPU and 1-2 GB RAM

## Reference Files

| File | When to Read |
|------|--------------|
| [configuration.md](references/configuration.md) | Environment variables, Docker setup |
| [custom-worker.md](references/custom-worker.md) | Building worker with PDF/image tools |
| [pdf-image-scripts.md](references/pdf-image-scripts.md) | Script examples for processing |
| [troubleshooting.md](references/troubleshooting.md) | Common issues and diagnostics |

## Official Documentation

| Topic | URL |
|-------|-----|
| Introduction | https://www.windmill.dev/docs/intro |
| Self-Hosting | https://www.windmill.dev/docs/advanced/self_host |
| Workers | https://www.windmill.dev/docs/core_concepts/worker_groups |
| Scripts | https://www.windmill.dev/docs/getting_started/scripts_quickstart |
| Flows | https://www.windmill.dev/docs/getting_started/flows_quickstart |

## Troubleshooting Quick Guide

| Issue | Check |
|-------|-------|
| Jobs stuck in queue | `docker compose logs windmill-worker` - check DB connection |
| Custom tools missing | Verify using custom image, rebuild if needed |
| Memory crash | Increase `mem_limit`, reduce parallel jobs |
| Permission denied | Check Docker socket mount |
| LSP not working | `docker compose ps windmill-lsp` |
