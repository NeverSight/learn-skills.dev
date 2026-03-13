---
name: ui-document-intake-dropzone
description: Use when adding PDF or Markdown intake UI with dropzone, queue states, and ingest actions in Next.js; pair with addon-rag-ingestion-pipeline.
---

# UI: Document Intake Dropzone

Use this skill when a Next.js app needs a clean UI for adding source documents (especially PDF and Markdown) before ingestion/indexing.

## Compatibility

- Best with `architect-nextjs-bun-app`.
- Recommended with `addon-domain-semantic-adaptation` for domain-specific intake wording.
- Common pairings:
- `addon-rag-ingestion-pipeline`
- `addon-docling-legal-chunk-embed`
- UI-only skill: ingestion logic should remain in add-on/backend modules.

## Inputs

Collect:
- `ALLOWED_FORMATS`: default `pdf,md,markdown`.
- `MAX_FILE_MB`: default `25`.
- `INTAKE_MODE`: `upload-only` | `upload+url` | `upload+paste`.
- `STYLE_DIRECTION`: `minimal` | `high-contrast`.

## Integration Workflow

1. Add UI files:
```text
src/app/sources/page.tsx
src/app/sources/sources.css
src/components/sources/intake-shell.tsx
src/components/sources/file-dropzone.tsx
src/components/sources/source-list.tsx
src/components/sources/ingest-actions.tsx
```
- Import `./sources.css` from `src/app/sources/page.tsx`.

2. Wire existing ingestion adapter:
- `onFilesAccepted(files)` dispatches to existing upload/ingest endpoint or queue handler.
- Keep adapter interface explicit and injected via props/hooks.

3. Ensure responsive behavior:
- Desktop: dropzone + queue + action rail.
- Mobile: stacked flow with clear primary action.

## Required UI Contract

- Drag-and-drop + click-to-select path.
- Client-side format/size validation with clear errors.
- Queue list showing filename, size, and status (`queued`, `uploading`, `indexed`, `error`).
- Ingest action disabled unless at least one valid file is queued.
- Internal navigation uses `next/link`.

## Minimal Template Snippets

### `src/app/sources/page.tsx`
```typescript
import IntakeShell from "@/components/sources/intake-shell";
import "./sources.css";

export default function SourcesPage() {
  return <IntakeShell />;
}
```

### `src/components/sources/file-dropzone.tsx`
```typescript
type FileDropzoneProps = {
  onFilesAccepted: (files: File[]) => void;
  accept: string;
};

export default function FileDropzone({ onFilesAccepted, accept }: FileDropzoneProps) {
  return (
    <section>
      <input
        accept={accept}
        multiple
        onChange={(e) => onFilesAccepted(Array.from(e.target.files ?? []))}
        type="file"
      />
    </section>
  );
}
```

## Design Guardrails

- Keep upload states explicit; avoid silent failures.
- Do not place API keys or ingestion secrets in UI code.
- Keep heavy file parsing server-side unless explicitly required.
- Keep components presentational; ingestion/persistence logic lives in add-ons.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
# Use the project's package manager (examples):
bun run lint
bun run build
pnpm run lint
pnpm run build
```
Fallback (`offline-smoke`):
```bash
test -f src/app/sources/page.tsx
test -f src/app/sources/sources.css
test -f src/components/sources/file-dropzone.tsx
rg -n "next/link" src/components/sources || true
```
Manual checks:
- PDF and Markdown files can be queued.
- Invalid file types/sizes are rejected with visible messages.
- Queue status transitions are visible without page reload.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
