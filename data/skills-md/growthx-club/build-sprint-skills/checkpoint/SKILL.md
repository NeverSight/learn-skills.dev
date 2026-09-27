---
name: checkpoint
description: Save the builder's work to git at every point the app works, and get them back to a working version when something breaks. Use the moment a feature works end to end, before any risky change, before a long build step, at the end of a session, and whenever they say something broke, "it worked before", "undo that", or "start over". Also use when they have been building a while with nothing committed.
---

# Checkpoint

A working app that isn't committed is one bad edit away from gone. The builder may not know that yet. You do, so you own it.

Save early, save often, and say what you saved in one plain line. Never make them ask.

## When to save

Commit without being asked when:

- A feature works end to end. They clicked it, it did the thing. **This is the most important one.**
- You're about to touch something risky — auth, the database schema, deleting files, swapping a library, a big refactor. Save *first*, then say "saved a checkpoint first, so we can get back here."
- They're about to step away, or the session is ending.
- You're about to try a second approach after the first one failed.

Don't ask permission for each one. Commit, then one line: `saved: google sign-in works`. Asking every twenty minutes trains them to stop reading what you say.

## Writing the message

Plain language, about what changed for a person using the app. Not internal vocabulary.

| Write this | Not this |
|---|---|
| `add google sign-in` | `implement OAuth provider integration` |
| `show a message when there are no projects yet` | `add empty state component` |
| `fix the crash when the title is blank` | `handle null in title validation` |

They will read this list at demo day and it should still make sense to them.

## Pushing

Commit is local and costs nothing — do it freely.

Push when the app is working, because pushing is also what puts it live. Say that plainly: "pushed — your live site will update in about a minute." They should learn that loop, since it's the one they'll use forever: edit → push → GitHub → Vercel → live.

Don't push mid-broken. A broken commit sitting locally is private; a broken deploy is the URL they're sharing.

## Getting back

When something breaks and they want out, don't lecture — offer the way back.

| They say | You do |
|---|---|
| "undo that" / "forget the last thing" | Discard uncommitted changes, after listing what's about to be lost |
| "it worked before" / "go back" | Show the last few checkpoints in plain language, let them pick, then go there |
| "what did I do today" | Read the log back as a list of sentences |

Before anything that destroys work: say exactly what will be lost, in their words, and wait for a clear yes. "You'll lose the last 40 minutes — the filter you added, but not the sign-in" beats printing a diff.

Never force push. Never rebase. Never rewrite history they've already pushed.

## Secrets

If an API key, a `.env` file, or a credential is about to be committed, stop. Tell them what it is, why it can't go in, and fix the ignore file. A key in a public repo is the one mistake that costs real money.

## Staying out of the way

- One branch. `main`. A solo builder on a two-week sprint does not need branching, and a detached HEAD will cost an hour nobody has.
- No stashing, cherry-picking, or submodules unless they ask by name.
- Never leave them mid-operation — no half-finished merge, no conflict state, no editor waiting on a commit message.

## Teach a little, every time

After a checkpoint, one short line on what just happened, pitched at their level: "that's saved to your history — you can always come back to this exact version."

Skip the lesson when they're mid-flow and it works. Save it for the moment something broke and the checkpoint rescued them, because that's when it lands.

---

Ours. Written for sprint builders who are shipping their first product and need an undo button more than they need a git tutorial.
