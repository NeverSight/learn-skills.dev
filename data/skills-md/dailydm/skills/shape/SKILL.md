---
name: shape
description: "Shape: create a filled Shaping doc from an attached Pitch"
disable-model-invocation: true
---

# Shape: create a filled Shaping doc from an attached Pitch

When the user types `/shape` and attaches a Pitch document, do the following:

## 1) Study the Pitch and the codebase (required)
- Read the Pitch end-to-end.
- Identify the primary user workflow(s) and system boundary.
- Search the repo for the relevant implementation paths (models, controllers, services, jobs, GraphQL, frontend).
- Prefer proposing integration points that match existing patterns (feature flags, async jobs, external service clients, metrics).

## 2) Create a new Shaping markdown file
- **Location**: `projects/<domain-name>/<project-name>/shaping.md`
- **Domain name**: the product area or team domain (e.g., `payments`, `family-messaging`, `attendance-plus`)
- **Project name**: derive a stable folder slug from the attached pitch path when possible (prefer `projects/<domain-name>/<project-name>/pitch.md`).
- **First line**: `# Shaping: <Pitch title>`
- **Source link**: add a line referencing the attached Pitch doc path.

## 3) Populate the Shaping doc with inferred content (no blanks)
Fill every section based on the Pitch + codebase study. If something cannot be inferred, write the smallest explicit note stating what's missing and why.

### Frame (from Pitch)
- **Problem**:
- **Desired outcome**:
- **Appetite**: infer a recommendation from the Pitch constraints and repo complexity; label it as a recommendation if not explicitly approved.

### Solution at the right altitude
- **Approach**: describe the smallest end-to-end slice.
- **Integration points**: list concrete files/classes/modules likely to change.
- **Boundaries**:
- **No-gos**:

### Lo-fi breadboard
- **Places**:
- **Affordances**:
- **Connections**:

### Rabbit holes (de-risk now)
List the top risks and a concrete de-risk plan for each (spikes, data sampling, contracts, perf/latency, failure modes).

### Scope
- **Must-dos**: minimum shippable set aligned to Appetite.
- **Nice-to-haves**: explicitly droppable items to protect the deadline.

### Delivery Gate criteria (draft)
Make this testable and operational:
- **Ship criteria**:
- **Rollout plan** (flags/permissions, pilot scope):
- **Observability** (key dashboards/metrics/logs):
- **Fallback behavior**:

## 4) Ask only for confirmation on true decision inputs
After writing the filled doc, ask the user to confirm:
- **Appetite** (approved or adjust)
- Any policy/legal wording that must be exact
- Pilot rollout constraints (which tenants/roles)
