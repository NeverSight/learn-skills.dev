---
name: destructive-path-guard
description: Prove a delete, move, or overwrite target is contained before the operation runs, whether the path comes from code or from the agent's own shell command. Use when writing or reviewing cleanup, eviction, temp-dir, cache-purge, or uninstall code, and before any rm, mv, or truncating write whose path was computed from data (an env var, a payload, another process, a string built at runtime) rather than named literally by the user. Do not use for an rm or edit at a literal path the user typed, such as a build or cache directory named in the request.
---

# Destructive Path Guard

A delete is only as safe as the value naming its target. Reading that value from
the kernel, a job payload, an environment variable, or a sibling service proves
where it arrived from, not who wrote it; another process's command line is as
attacker-controlled as a form field. A shape check ("absolute, at least one
directory deep") proves well-formedness and then gets mistaken for authorization.
That is how a cleanup routine removes the root instead of the leaf.

## Require three things, in this order

1. **Containment after resolution.** A symlink leaf is checked as the link:
   resolve its parent, keep the link name, and refuse if the link points outside
   the allowlisted roots; print the link itself. Comparing raw strings, or
   resolving after the check, lets a symlink inside the root point anywhere.
2. **Depth below the root.** Count depth from the nearest listed root containing
   the target, and refuse a target that is or contains any listed root. Require
   at least one level below that root so a root is never itself the target. A
   misderived path usually collapses upward.
3. **Evidence the target is yours**, read from the target itself only for an
   existing directory; read it from the parent for a symlink leaf, an existing
   non-directory, or a not-yet-created leaf, never the root. Check it before the
   operation and before any teardown that would remove the evidence. Without it,
   "absent" and "not mine" are the same observation.

Then act on the resolved path the check returned, not on the original string.

## Run the check

```bash
python3 <this-skill>/scripts/safe_target.py "$TARGET" \
  --root /var/lib/app/sessions --min-depth 1 \
  --owner-file .owner --expect-owner "$WORKER_ID"
```

Exit `0` prints the checked target, `1` refuses, `2` means the check could not
run and proves nothing. Import `resolve_target` for the same rule inside Python;
port it directly in another language rather than weakening it. In the agent's own
shell work, stop on a non-zero exit before the destructive command sees the path:

```bash
target=$(python3 <this-skill>/scripts/safe_target.py "$TARGET" --root ...) || exit 1
rm -rf -- "$target"
```

`rm -rf -- "$(...)"` in one line is wrong: a refusal prints nothing, the
substitution becomes an empty argument, and `rm` exits `0` having done nothing
while the caller believes the cleanup ran.

## Refusal is final

Log the rejected target and stop. A cleanup that falls back to a broader default
root on refusal is exactly the failure this guards against, and a retry loop that
widens the allowlist is the same failure spelled differently.

## Two limits, stated where the rule is copied

- **A marker inside the tree is self-attestation.** Anything that can write in the
  root can write `.owner`. The expected owner has to come from authenticated
  state, and the marker needs integrity protection (restrictive ownership, or a
  MAC) before it is authorization rather than a consistency check.
- **Resolving a path and then operating on the name is a check/use race.** Where an
  untrusted process can swap an ancestor, hold the target by descriptor and use
  no-follow, beneath-the-root operations, or guarantee the hierarchy cannot change
  for the duration.
