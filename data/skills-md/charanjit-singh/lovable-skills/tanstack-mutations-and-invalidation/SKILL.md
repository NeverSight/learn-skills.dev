---
name: tanstack-mutations-and-invalidation
description: >-
  Use when writing TanStack Query mutations: useMutation, onSuccess invalidation,
  optimistic updates, error rollback, or chained mutations. Not for read-only
  queries (use tanstack-query-alternative).
---

# TanStack mutations and invalidation

Every server write goes through `useMutation`. Treat invalidation as part of the mutation contract, not an afterthought.

Companion skills: [`tanstack-query-alternative`](../tanstack-query-alternative/), [`optimistic-updates`](../optimistic-updates/), [`api-error-handling`](../api-error-handling/).

## Basic mutation

```ts
// src/hooks/mutations/useCreateProject.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createProject } from "@/api/projects";
import { projectKeys } from "../queries/keys";

export function useCreateProject() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createProject,
    onSuccess: (newProject) => {
      qc.invalidateQueries({ queryKey: projectKeys.all });
      qc.setQueryData(projectKeys.detail(newProject.id), newProject);
    },
  });
}
```

Components call it cleanly:

```tsx
const { mutate, isPending, error } = useCreateProject();
<Button disabled={isPending} onClick={() => mutate(values)}>Create</Button>
```

Use `mutateAsync` only when you need to `await` (e.g. inside a form `onSubmit`).

---

## Invalidation strategies

Pick one per mutation:

| Strategy | When | API |
|----------|------|-----|
| **Invalidate** | Lists may change shape | `invalidateQueries({ queryKey })` — marks stale, refetches what's mounted |
| **Set data** | You already have the new value | `setQueryData(key, value)` — instant, no refetch |
| **Remove** | Resource is gone | `removeQueries({ queryKey })` |
| **Reset** | Wipe cache (logout, switch org) | `qc.clear()` or `resetQueries({ queryKey })` |

Combine when both apply: optimistically `setQueryData`, then `invalidateQueries` on settle to reconcile.

### Broad invalidation by prefix

Key factories sort tuples broadest-first so a single invalidation wipes related queries:

```ts
qc.invalidateQueries({ queryKey: projectKeys.all });
// invalidates ["projects"], ["projects", "list", ...], ["projects", "detail", ...]
```

For partial matches, use a predicate:

```ts
qc.invalidateQueries({
  predicate: (q) => q.queryKey[0] === "projects" && q.queryKey[1] === "list",
});
```

---

## Optimistic updates with rollback

```ts
export function useToggleLike(postId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => api.toggleLike(postId),
    onMutate: async () => {
      await qc.cancelQueries({ queryKey: postKeys.detail(postId) });
      const prev = qc.getQueryData<Post>(postKeys.detail(postId));
      qc.setQueryData<Post>(postKeys.detail(postId), (p) =>
        p ? { ...p, liked: !p.liked, like_count: p.like_count + (p.liked ? -1 : 1) } : p,
      );
      return { prev };
    },
    onError: (_err, _vars, ctx) => {
      if (ctx?.prev) qc.setQueryData(postKeys.detail(postId), ctx.prev);
    },
    onSettled: () => {
      qc.invalidateQueries({ queryKey: postKeys.detail(postId) });
    },
  });
}
```

Rules:

- `cancelQueries` **before** writing optimistic data — otherwise in-flight refetches will overwrite it.
- Always implement `onError` rollback.
- Reconcile with `onSettled` invalidation; server can change denormalized counts.

See [`optimistic-updates`](../optimistic-updates/) for the full UX patterns (delete-with-undo, etc.).

---

## Error handling

Mutations should surface errors via the hook return; don't `try/catch` inside the hook unless you can fully recover.

```tsx
const { mutate, error, isPending } = useCreateProject();

useEffect(() => {
  if (error) toast.error("Could not create project", { description: humanize(error) });
}, [error]);
```

Map server error slugs from [`api-error-handling`](../api-error-handling/) to UI copy in a single `humanize(error)` helper — do not branch on `error.message` strings.

---

## Sequencing and dependent mutations

For multi-step writes (e.g. create org → create project → invite members), prefer **one edge function** that does all three atomically and one mutation in the UI. Avoid chained `mutate → onSuccess → mutate` in the client — partial failures leave inconsistent state.

When you must chain, use `mutateAsync` and `try/catch`:

```ts
async function onSubmit(values: FormValues) {
  try {
    const org = await createOrg.mutateAsync(values.org);
    await createProject.mutateAsync({ orgId: org.id, ...values.project });
  } catch (e) {
    toast.error("Setup failed", { description: humanize(e) });
  }
}
```

---

## Avoid

- Mutations without an invalidation plan (lists stay stale).
- Optimistic updates without rollback.
- Calling `qc.clear()` after small mutations (nukes unrelated caches).
- Triggering refetch storms by invalidating with no predicate from inside a high-frequency mutation.
- `onSuccess: () => window.location.reload()` — defeats the cache.

## Checklist

- [ ] Invalidate or `setQueryData` on every mutation.
- [ ] Optimistic mutations implement `onError` rollback and `onSettled` reconcile.
- [ ] `isPending` disables the trigger.
- [ ] Errors surfaced via hook return; mapped to UI copy via a single helper.
