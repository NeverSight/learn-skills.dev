---
name: bro-what
description: Re-explain the last response in plain, easy-to-follow language.
disable-model-invocation: true
---

# Bro What

The last response did not land. Re-pitch it:

When reading project context, resolve `.agents/projects/` from the opened workspace
root, even when the active repository is nested inside it. In a single-repository
workspace, use the repository root. Keep this root fixed when changing directories;
never read project artifacts from nested repositories or global agent installations.

1. Start with the minimum context needed to understand the point.
2. State the main conclusion in plain language.
3. Explain unfamiliar technical terms before using them, including project terms from
   `.agents/projects/<project>/CONTEXT.md` when an active project exists.
4. Use short sentences and a concrete example when one makes the point clearer.

Done when the explanation is understandable without the context assumed by the prior
response.
