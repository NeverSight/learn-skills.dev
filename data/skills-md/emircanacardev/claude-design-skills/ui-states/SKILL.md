---
name: ui-states
description: Designs every state a screen or component can reach beyond the happy path, including first-use, user-cleared and no-results empty states, loading with skeletons, spinners and optimistic updates, inline, page and toast errors with recovery, success, partial, offline and permission-denied, with copy, visuals and code. Use when asked to add loading or empty states, or to handle errors and edge cases. Not for form field validation (use form-design).
---

# UI States

Produces a complete, implemented set of states for a screen or component, so users never face a blank area, an endless spinner, or a dead-end error.

## When to use
- "Add loading and empty states to this page."
- "What should happen when the API fails or the user is offline?"
- Planning a new feature: map states before high-fidelity design.
- A mockup or codebase shows only the ideal, data-filled state.
- Reviewing error messages, toasts, and recovery paths.

## Workflow
1. List the screen's data sources and user actions. For each, enumerate loading, empty (first-use, user-cleared, no-results), success, error, partial, stale, offline, and permission-denied.
2. Mark which states are reachable and explicitly drop the rest.
3. For each reachable state, define the visual, the copy (headline, one-line explanation, action), and which controls stay available. Use ux-writing for copy.
4. Pick the loading treatment by expected duration and whether the final layout is known.
5. Place errors by scope: a field or widget gets an inline error, a whole view gets a page state, a background action gets a toast or banner.
6. Model the state in code as one explicit status value, not a set of independent booleans.
7. Make every state previewable (story, fixture, or dev toggle) and review them side by side.

## Rules
**Empty**
- First-use: say what will appear here and why it is useful, with one primary action (create, import, connect) or a template or sample data.
- User-cleared (inbox zero, all tasks done): confirm the good outcome and optionally suggest a next step; no nagging to create more.
- No results: echo the query and filters, suggest a fix (check spelling, remove a filter), and offer Clear filters.

**Loading**
- Show nothing for roughly the first 300ms to avoid flashes; once an indicator appears, keep it for at least about 500ms so it does not flicker.
- Known layout: a skeleton sized like the final content, so nothing shifts when data arrives. Shimmer stops under `prefers-reduced-motion: reduce`.
- Short, unknown-duration actions: a spinner inside the triggering button, which keeps its width and accessible label and blocks repeat clicks. Long or measurable work (uploads, exports): determinate progress with percentage or steps, plus Cancel.
- Optimistic UI only for low-risk, usually successful actions (like, toggle, reorder, rename): update instantly, sync in the background, roll back with a visible message on failure. Never for payments or irreversible actions.
- Set `aria-busy="true"` on regions while they load; announce completion of user-triggered loads through a `role="status"` region.

**Error**
- Every error says what happened, whether data is safe, and offers a recovery action: Retry, Undo, Edit, Go back, or Contact support. No dead ends, no blame, no raw codes alone (add a reference ID for support when available).
- Inline errors sit next to what failed while the rest of the screen keeps working. Page errors (404, 500) keep global navigation, offer a path forward, and receive focus on their heading.
- Toasts are only for transient, non-blocking results. Errors that need action never auto-dismiss; toasts with an action (Undo, Retry) pause on hover and focus and stay long enough to use. Use `role="alert"` for errors and `role="status"` for confirmations.
- Preserve user input through every error.

**Success, partial, offline, permissions**
- Confirm small actions in place (updated item, inline check); use a toast for background actions and a full success screen only for milestones (purchase, submission) with clear next steps.
- Partial or stale: render what loaded, mark failed parts individually, and show "Last updated" for cached data.
- Offline: a persistent banner, cached content stays readable, safe actions queue with a visible "Pending sync" label, network-only actions are disabled with a reason.
- Permission denied: explain what is restricted and who can grant access, and offer Request access. Hide controls a user can never use; disable with an explanation only when access can be granted.

## Output
- A state matrix (markdown table): state, trigger, visual, copy, available actions.
- Final copy for every state.
- Code with a single status type and one render branch per state, plus reusable EmptyState, Skeleton, ErrorState, and Banner components in semantic HTML with CSS custom properties, or React + Tailwind if the project uses it:

```ts
type ViewState<T> =
  | { status: "loading" }
  | { status: "empty"; reason: "first-use" | "cleared" | "no-results" }
  | { status: "error"; message: string; retry: () => void }
  | { status: "forbidden"; requestAccess?: () => void }
  | { status: "ready"; data: T; stale?: boolean; offline?: boolean };
```

## Avoid
- `isLoading`, `isError`, and `isEmpty` booleans that can be true at the same time.
- A full-screen spinner for content that could load in parts.
- Skeletons that do not match the final layout and cause jumps.
- "Something went wrong" with no cause and no action.
- Empty states that are a gray illustration and "No data".
- Auto-dismissing error toasts, or errors that only reach the console.
- Clearing user input when a request fails.

## Final check
- [ ] Every state in the matrix is designed or explicitly marked unreachable.
- [ ] Fast responses show no loading flash; skeletons match the final layout.
- [ ] Every error offers a recovery action and keeps user input.
- [ ] `role="status"` and `role="alert"` are used appropriately; page errors receive focus.
- [ ] Nothing critical appears only in a toast, and action toasts do not vanish before use.
- [ ] Shimmer and transitions respect `prefers-reduced-motion`.
- [ ] Each state can be previewed in a story, fixture, or dev toggle.
