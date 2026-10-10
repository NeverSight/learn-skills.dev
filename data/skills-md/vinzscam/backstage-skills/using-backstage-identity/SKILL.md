---
name: using-backstage-identity
description: Use when a Backstage frontend plugin needs information about the currently logged-in user — their entity ref, profile info, ownership refs, or auth token. Triggers on phrases like "current user", "logged-in user", "my groups", or imports of identityApiRef.
---

# Backstage Identity Patterns

## When to use this skill

- Plugin needs the current user's entity ref (e.g. `user:default/jdoe`)
- Plugin needs the user's profile info (display name, email, picture)
- Plugin needs ownership entity refs to filter "things owned by me"
- Plugin needs a Backstage token to call backend APIs as the current user

## Choose the right pattern

| Situation                                                  | Pattern                                                              | Reference                  |
| ---------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------- |
| Get the current user (entity ref, ownership refs, profile) | `useApi(identityApiRef).getBackstageIdentity()` / `getProfileInfo()` | references/current-user.md |

## Two invocation modes

- **Standalone** (mid-development): user is editing an existing plugin. Read the reference and apply the pattern to whichever component needs it.
- **Post-scaffold** (called by `creating-backstage-plugin`): apply the pattern to a freshly scaffolded plugin. The reference's "Post-scaffold usage" section names exactly which file to edit and what to insert.

## Common gotchas

- `identityApiRef` is imported from `@backstage/frontend-plugin-api` in NFS plugins. (The same ref is also re-exported from `@backstage/core-plugin-api` for legacy compatibility — for new plugins always use the NFS package.)
- `getBackstageIdentity()` is async and returns a `BackstageUserIdentity` — destructure `userEntityRef` and `ownershipEntityRefs` from it.
- Don't store the result in a top-level variable; call from inside a hook (e.g. inside a React component or a `useAsync` callback) so it re-runs on identity change.

## UI conventions

Use `@backstage/ui` for rendering when possible (`Skeleton`, `Alert`, `Text`, `Flex`, `Button`, …). See `using-backstage-ui` skill for the full component catalog and styling guidance.
