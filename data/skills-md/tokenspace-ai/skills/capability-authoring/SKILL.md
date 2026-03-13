---
name: capability-authoring
description: Author new Tokenspace workspace capabilities with action-based APIs, strict domain and input guardrails, and autonomy-first approval policies. Use when creating or revising files in src/capabilities/*, src/credentials.ts, and CAPABILITY.md to ensure capabilities stay safely in-scope.
---

# Capability Authoring

Author capabilities for maximum safe autonomy. Keep clear domain boundaries and strong input gating so actions stay aligned with the intended workspace domain.

Prefer creation workflows over maintenance workflows. Use maintenance guidance only when modifying existing capabilities.

## Creation Workflow

1. Define the capability domain contract before writing code.
- Record allowed tenants, repos/projects, environments, object ID formats, and prohibited targets.
- Record explicit examples of allowed and disallowed requests.
- If scope is unclear, default to narrower boundaries.
- Use [references/domain-gating-checklist.md](references/domain-gating-checklist.md) as the capture template.

2. Design the action surface.
- Define read and write actions from user requirements.
- Keep actions small and composable; avoid broad "do anything" actions.
- Assign each action an autonomy mode:
  - Autonomous by default.
  - Approval-required for selected operations.
  - Rejected when outside defined boundaries.
- Use [references/approval-policy-matrix.md](references/approval-policy-matrix.md) to choose policy per action.

3. Scaffold capability files.
- Create `src/capabilities/<name>/capability.ts`.
- Create `src/capabilities/<name>/CAPABILITY.md`.
- If credentials are needed, add definitions in `src/credentials.ts` and import them.
- If OAuth is needed, define it with `credentials.oauth(...)` in `src/credentials.ts`, and prefer `credentials.ref(...)` for client secret linkage. See [references/oauth-credentials.md](references/oauth-credentials.md) for more details on OAuth credential authoring.
- Use [references/capability-template.md](references/capability-template.md) for the structure.

4. Implement guarded actions.
- Export callable APIs with `export const <actionName> = action(z.object({...}), async (args) => ...)`.
- Do not export raw `export function` actions from capability entrypoints.
- Keep action input/output JSON-serializable.
- Enforce domain boundaries at runtime before external calls.
- Validate and normalize user-provided identifiers before use.
- Handle ambiguous or unsupported input with specific errors.
- Use least-privilege credentials for each operation.

5. Add approval gating where needed.
- Start from user policy: maximize safe autonomous execution.
- Require approval only for operations that are destructive, high-impact, cost-sensitive, or explicitly policy-gated.
- Use namespaced approval actions (`<capability>:<operation>`).
- Include data fields that uniquely scope the approval target.
- Write precise descriptions that reviewers can approve safely.

6. Author CAPABILITY.md for reliable agent behavior.
- Include frontmatter with concise `name` and `description`.
- Add Guidelines that reinforce scope boundaries and safety constraints.
- Add Data Overview with concrete resources and identifiers.
- Add runnable examples that show correct in-domain usage.
- Include at least one example showing expected rejection behavior for unsupported targets.

7. Verify.
- Run `bun typecheck`.
- Run targeted tests if present.
- Confirm compile-time and runtime behavior:
  - Expected read paths run autonomously.
  - Writes follow the intended approval policy.
  - Unsupported targets are rejected before side effects.

## Domain and Input Gating Rules

- Treat user-provided IDs, names, and scopes as untrusted input.
- Validate shape, format, and allowlist membership.
- Normalize before comparison (case sensitivity, prefixes, canonical names).
- Check scope at every mutating boundary, not only at request entry.
- Reject unknown environments, repos, orgs, or resource classes.
- Never let credential breadth replace explicit domain checks.

## Multi-Capability Composition

When workflows span capabilities, preserve boundaries per capability:

- Validate scope in each capability independently.
- Pass only minimal structured data between capabilities.
- Do not assume one capability's scope check covers another.
- If capabilities disagree on scope, stop and surface the conflict.

## Maintenance Guidance (Secondary)

When updating existing capabilities:

- Preserve domain contract unless requirements explicitly expand it.
- Re-evaluate approval and autonomy policy for new operations.
- Keep `CAPABILITY.md` aligned with actual exported actions.
- Add regression tests for previously rejected unsupported-target cases.

## References

- Domain scoping and input gating checklist:
  [references/domain-gating-checklist.md](references/domain-gating-checklist.md)
- Approval strategy and autonomy matrix:
  [references/approval-policy-matrix.md](references/approval-policy-matrix.md)
- Capability and CAPABILITY.md starter template:
  [references/capability-template.md](references/capability-template.md)
- OAuth credential authoring details and examples:
  [references/oauth-credentials.md](references/oauth-credentials.md)
