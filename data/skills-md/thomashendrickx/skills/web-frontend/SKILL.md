---
name: web-frontend
description: Use for React and Next.js web app changes. Structure, state, React rules.
---

# Web frontend

Before writing Next.js code, read the matching guide in `node_modules/next/dist/docs/`: the installed version may differ from training data.

The server decides: data calls, business rules and checks run on the server or behind the API. Browser checks are live hints only.

Structure: vertical by feature, atomic design inside it. The repo's companion skill names the root folder.
- One folder per feature:
  - `ui/`: its atoms, molecules and organisms. Props only: no data fetching, no store, no API client.
  - `hooks/`: the feature's ports. A hook hides whether data is server or client state and returns only what consumers need.
  - `state/`: containers that connect hooks to `ui/`. Composition only.
  - `services/` (optional): pure frontend logic such as formatters and view-model builders. No React, no API client.
- Dependencies flow inward: `state/` uses `hooks/` and `ui/`; `hooks/` use `services/`.
- Shared atoms, molecules and organisms are props only. A part moves to shared when a second feature needs it.
- Route files (page, layout, `loading`, `error`) only compose features; route layouts are the templates.
- shadcn/ui first; a custom atom needs a PR note why.
- Server components by default; `'use client'` as low as possible.

State:
- Server data via the API client plus TanStack Query, never copied into local state. URL-worthy view state in search params. Forms with React Hook Form. Local UI state in the owning component. No global store.
- Mutations live in their hook, which invalidates. Destructive actions confirm.
- `useEffect` only to sync with outside systems (a WebSocket, a browser API). Derive values in render. No manual memoisation, no index keys, no browser storage for server data.
- The session is an httpOnly cookie; a password lives only in the sign-in form.

Interaction feedback (a must: a control that gives none is a bug, whatever else works):
- Every action answers at once. Within 100 ms of the press the control shows it is working: a spinner on the control and a working label ("Saving..."), disabled so it cannot run twice. Never wait for the server before showing anything; 500 ms of nothing reads as broken.
- Every action ends in a visible outcome. Success says what happened (a toast, or the change shown in place). Failure says what went wrong and what to do next, inline by the control, keeping the input. Never an empty reason, never a silent no-op.
- An optimistic change that fails rolls back visibly and says so.
- Data that loads shows the shape that is coming (a skeleton), never a blank area or a bare spinner for the page.
- Tests: each interactive part has stories for idle, pending, success and failure, and an interaction test that a press shows pending before the answer arrives.

Responsive layout (a must: a page that breaks, cuts off or wastes the screen at any width is a bug):
- Every page works from 360 px to 2560 px: content reflows, nothing scrolls sideways, nothing is cut off, no truncation where there is room.
- The layout follows the window, not a fixed width: columns and grids grow or add columns as the window grows. A max width only for long reading text.
- Build and check at every width the approved mockups draw, plus 375, 1440 and 1920.
- Tests: each page has a story or visual check at 375, 1440 and 1920.

Quality:
- Keyboard reachable, accessible names, status never by colour alone. `data-testid="{area}-{element}"` on elements tests touch.
- Storybook: a story per meaningful state of each `ui/` part.
