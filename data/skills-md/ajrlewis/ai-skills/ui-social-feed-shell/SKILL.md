---
name: ui-social-feed-shell
description: Use when adding a reusable social feed UI shell in Next.js; pair with addon-domain-semantic-adaptation.
---

# UI: Social Feed Shell

Use this skill when a Next.js app needs a social timeline UI with a composer and side rails.

## Compatibility

- Best with `architect-nextjs-bun-app`.
- Common pairing: `addon-nostr-client-nextjs` for Nostr-backed timelines.
- Recommended with `addon-domain-semantic-adaptation` for domain-specific copy/labels.
- UI-only skill: do not add infrastructure concerns.

## Inputs

Collect:
- `VISUAL_DIRECTION`: `classic` | `high-contrast` | `minimal`.
- `SHOW_RIGHT_RAIL`: `yes` | `no`.
- `MAX_FEED_ITEMS`: default `50`.
- `FEED_SOURCE_ADAPTER`: existing data adapter/hook to read + publish entries.

## Integration Workflow

1. Add UI files:
```text
src/components/feed/app-shell.tsx
src/components/feed/timeline.tsx
src/components/feed/composer.tsx
src/components/feed/note-card.tsx
src/components/feed/side-rail.tsx
src/app/feed/page.tsx
src/app/feed/feed.css
```
- Import `./feed.css` from `src/app/feed/page.tsx` (route-level import), not from nested components.

2. Integrate existing feed adapter:
- Timeline reads from selected data source adapter/hook.
- Composer submits through selected publish action.

3. Ensure responsive layout:
- 3-column desktop
- single-column mobile

## Required UI Contract

- Left rail: navigation/profile shortcuts.
- Center column: composer + chronological timeline.
- Right rail: trends/suggestions (toggleable).
- Composer submit disabled until user/session is publish-ready.
- Empty/feed-loading/error states are visible and distinct.
- Use `next/link` for internal navigation links (`/feed`, `/`, etc.); avoid raw `<a href="/...">`.

## Minimal Template Snippets

### `src/app/feed/page.tsx`
```typescript
import AppShell from "@/components/feed/app-shell";

export default function FeedPage() {
  return <AppShell />;
}
```

### `src/components/feed/composer.tsx`
```typescript
type ComposerProps = {
  canPost: boolean;
  content: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
};

export default function Composer({ canPost, content, onChange, onSubmit }: ComposerProps) {
  return (
    <section>
      <textarea
        disabled={!canPost}
        onChange={(e) => onChange(e.target.value)}
        placeholder={canPost ? "What's happening?" : "Login to post"}
        value={content}
      />
      <button disabled={!canPost || !content.trim()} onClick={onSubmit} type="button">
        Post
      </button>
    </section>
  );
}
```

## Design Guardrails

- Keep typography, spacing, and hierarchy intentional; avoid generic template look.
- Keep interaction states explicit (hover, disabled, loading).
- Keep secrets and protocol logic out of UI components.
- Keep UI components presentational; protocol/domain logic stays in add-ons.
- Preserve mobile usability at widths down to 360px.
- Keep feed stylesheet import at route level to avoid global CSS import restrictions.
- Use `next/link` for internal route navigation to satisfy Next lint/build rules.

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
test -f src/app/feed/page.tsx
test -f src/app/feed/feed.css
test -f src/components/feed/app-shell.tsx
rg -n \"next/link\" src/components/feed/app-shell.tsx
! rg -n '<a href=\"/' src/components/feed/app-shell.tsx
```
- Manual checks:
- Publish-ready state toggles composer enabled/disabled correctly.
- Feed renders and updates without layout shift spikes.
- Mobile viewport keeps composer and first posts usable.
- Distinct empty/loading/error timeline states are visible.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
