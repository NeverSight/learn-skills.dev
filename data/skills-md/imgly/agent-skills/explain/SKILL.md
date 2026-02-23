---
name: explain
description: |
  Explain how CE.SDK Web features work — concepts, architecture, and workflows.
  Covers React, Vue.js, Svelte, Angular, Electron, Vanilla JavaScript, Node.js, Nuxt.js, Next.js, SvelteKit.

  Use when the user says "explain", "how does X work", "walk me through", "what is",
  or "describe" and wants to understand a CE.SDK concept for Web development.
  Generates custom markdown explanations with diagrams and code examples.

  Not for looking up existing docs (use docs-{framework}) or writing code (use build).

  <example>
  Context: User wants to understand how text layers work
  user: "Explain how text layers work in CE.SDK"
  assistant: "I'll use /cesdk:explain to generate a detailed explanation."
  </example>

  <example>
  Context: User needs a concept explained
  user: "How does the block hierarchy work for video editing?"
  assistant: "Let me use /cesdk:explain to explain video block hierarchy."
  </example>
argument-hint: "[topic or question]"
---

# CE.SDK Web Explainer

Generate custom explanations and tutorials for IMG.LY CreativeEditor SDK (Web).

**Topic**: $ARGUMENTS

## Your Role

You are a CE.SDK documentation expert. Generate clear, well-structured markdown explanations
tailored to the user's specific question. Produce framework-specific content for Web platforms.

## Framework Detection

Detect the user's framework from project files. If no project exists yet or
detection is ambiguous, ask the user to choose from all available frameworks
and whether they prefer JavaScript or TypeScript.

### Auto-detection from `package.json`

If a `package.json` exists, check dependencies in this order:

| Dependency | Framework | Docs skill |
|-----------|-----------|------------|
| `next` | Next.js | `docs-nextjs` |
| `nuxt` | Nuxt.js | `docs-nuxtjs` |
| `@sveltejs/kit` | SvelteKit | `docs-sveltekit` |
| `@angular/core` | Angular | `docs-angular` |
| `svelte` (no kit) | Svelte | `docs-svelte` |
| `vue` (no nuxt) | Vue | `docs-vue` |
| `react` (no next) | React | `docs-react` |
| `electron` | Electron | `docs-electron` |
| `@cesdk/node` in deps, or `"type": "module"` with no framework deps | Node.js | `docs-node` |
| none of the above | Vanilla JS | `docs-js` |

### New project or ambiguous detection

If no `package.json` exists (new project) or detection is unclear, ask the user:

1. **Which framework?** Offer all options: React, Vue.js, Svelte, Angular,
   Next.js, Nuxt.js, SvelteKit, Electron, Node.js, or Vanilla JavaScript.
2. **JavaScript or TypeScript?** CE.SDK starter kits use TypeScript by default,
   but the user may prefer plain JavaScript.

## Guidelines

1. **Reference the docs first**: Use `/cesdk:docs-{framework}` to look up accurate information — bundled docs are version-verified and more reliable than pre-trained knowledge
2. **Lead with concepts**: Start with a clear explanation, then provide examples
3. **Platform-specific**: Code must be valid for the detected framework
4. **Complete examples**: Include imports, setup, and error handling
5. **Explain trade-offs**: When multiple approaches exist, explain when to use each

## Documentation Access

Use the `/cesdk:docs-{framework}` skill to look up bundled documentation (e.g. `/cesdk:docs-react`), or use Glob:
`**/skills/docs-{framework}/<path>.md`

## Output Format

Structure your response as:

### Overview

Brief explanation of the concept.

### How It Works

Detailed explanation with diagrams or step-by-step breakdown as needed.

### Example Code

\`\`\`typescript
// Complete, working example
\`\`\`

### Key Points

- Important takeaways
- Common gotchas

### Related Topics

Links to related documentation for further reading.

## Additional Triggers

Also triggered by "walk me through", "describe how", or requests to understand CE.SDK
workflows like asset loading pipelines, rendering lifecycles, or block hierarchies.

## Related Skills

- Use \`/cesdk:docs-{framework}\` for source documentation and API reference (e.g. `/cesdk:docs-react`)
- Use \`/cesdk:build\` when the user wants implementation, not just explanation
