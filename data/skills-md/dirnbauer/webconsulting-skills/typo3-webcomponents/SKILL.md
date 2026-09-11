---
name: typo3-webcomponents
description: "Build, review, or migrate TYPO3 v14 backend Web Components with Lit, ES module import maps, AssetCollector/f:asset.module, backend modules, FormEngine/Form Editor integrations, AJAX routes, and reusable TYPO3 backend components. Use whenever the user mentions TYPO3 backend JavaScript, Web Components, Lit, LitElement, custom elements, @typo3/* modules, JavaScriptModules.php, backend module UI, Form Editor stage components, Camp Vienna Lit examples, component performance, or whether TYPO3 backend Web Components should be used in the frontend."
---

# TYPO3 Web Components

> Source: https://github.com/dirnbauer/webconsulting-skills

Use this skill for TYPO3 v14 backend programming with standards-based Web Components and Lit. Treat v14 as the only compatibility target: do not add TYPO3 12/13 fallbacks unless the user explicitly asks for a migration note, and verify current v14 APIs in the official TYPO3 docs before implementing.

This skill was created from the Anthropic-style skill-creator workflow and follows progressive disclosure: keep the top-level workflow short, then read the focused references when code or review depth is needed.

## Related Local Skills

Use these nearby TYPO3 skills together when the task touches their domain:

- `typo3-datahandler`: backend UI triggers record creation, update, move, delete, localization, workspace publishing, or any TCA-managed write.
- `typo3-workspaces`: the component displays or mutates draft/live state, staged records, publish actions, overlays, or workspace previews.
- `typo3-visual-editor`: the task involves inline editing, content-area rendering, or the Visual Editor context panel.
- `typo3-vite`: frontend bundling, frontend Web Components, production asset hashing, or external build pipelines are required.
- `typo3-testing`: add Playwright, acceptance, or backend module tests for interactive components.
- `typo3-translations`: add XLIFF labels, imported label modules, or localized backend strings.

## Concepts

Web Components are browser standards for custom reusable HTML elements. The usual building blocks are Custom Elements, Shadow DOM, and templates/slots. A component can appear in markup like `<vendor-status-card></vendor-status-card>` and the browser connects it to a JavaScript class.

TYPO3 backend Web Components are custom elements used inside the authenticated TYPO3 backend. TYPO3 v14 uses ES modules, import maps, `@typo3/*` module identifiers, backend module configuration, FormEngine/Form Editor JavaScript, and Lit-based components for parts of the backend UI. The right model is "small interactive backend UI islands", not a separate SPA unless the backend feature genuinely needs one.

Lit is a small library on top of Web Components. In the TYPO3 backend, prefer Lit when the element has reactive state, templated rendering, repeated DOM updates, slots, or a reusable public API. Use plain vanilla JavaScript for tiny one-off behavior where a custom element would be ceremony.

## Frontend Decision

Answer frontend questions precisely:

- Do Web Components work in the TYPO3 frontend? Yes, they are browser standards.
- Do TYPO3 backend Web Components and `@typo3/*` backend modules belong in the frontend? No by default. They are backend infrastructure for authenticated backend pages.
- Should a project use Lit/Web Components in the frontend? No by default. Use them only when a reusable interactive island or framework-neutral design-system component is worth the extra dependency/build/runtime contract. Otherwise use semantic HTML, CSS, and small vanilla modules.
- If Lit is used in the frontend, bundle it through the frontend build pipeline, for example Vite. Do not assume the TYPO3 backend import map, `top.TYPO3`, backend CSS, or backend component modules exist in frontend requests.

## Default Workflow

1. Confirm the task is TYPO3 v14 backend work. If it is frontend work, apply the frontend decision above and use `typo3-vite` when bundling is needed.
2. Inspect the extension shape before coding: `Configuration/JavaScriptModules.php`, `Resources/Public/JavaScript`, backend module controllers, Fluid templates, `Configuration/Backend/Modules.php`, `Configuration/Backend/AjaxRoutes.php`, and Form Framework YAML if relevant.
3. Prefer existing TYPO3 backend APIs and components before writing new components. Search current sources for `@customElement(` and verify whether a component is meant to be reused.
4. Choose the smallest viable rendering path:
   - Static backend template plus one small custom element for local interaction.
   - Lit component when reactive state or repeated DOM rendering matters.
   - Existing Core or extension Web Component when it has a documented or stable enough public contract.
   - Backend module `component` or `navigationComponent` only when the module shell itself needs a component.
5. Register ES module imports in `Configuration/JavaScriptModules.php`. Use absolute import-map identifiers such as `@vendor/my-extension/backend/status-card.js`; avoid relative imports in TYPO3-loaded modules.
6. Load modules through `PageRenderer->loadJavaScriptModule()` in controllers or `<f:asset.module identifier="..."/>` in Fluid. Do not add inline scripts for backend component bootstrapping.
7. Pass small scalar configuration via attributes. For larger or privileged data, generate a backend route URL in PHP and let the component fetch it with `@typo3/core/ajax/ajax-request.js`.
8. Keep backend writes server-side and permission-checked. Use `DataHandler` for TCA-managed records and configure `inheritAccessFromModule` on related AJAX routes.
9. Validate UX with a real backend user, not only admin. Check keyboard access, focus behavior, reduced-motion tolerance, loading/error/empty states, and permissions.

## References

Read `references/examples-and-howtos.md` when implementing code. It includes import maps, Lit components, Fluid loading, AJAX routes, Form Editor modernization, and reusable component examples.

Read `references/checklists.md` when reviewing or migrating code. It includes dos and donts, speed guidance, security/accessibility checks, source links, and the related-skill comparison.

## Speed Notice

Lit is fast and small, but it does not make inefficient code fast. Keep `render()` pure and cheap; compute expensive derived data outside render, debounce high-frequency input, replace arrays/objects instead of mutating them in place, abort stale fetches, cache server results where appropriate, and lazy-load backend modules only on pages that need them.

In TYPO3 v14 frontend asset concatenation/compression was removed from Core, so frontend production assets need an external build tool. Backend ES modules are import-mapped and loaded on demand; still avoid shipping large backend bundles to every module.

## Source Baseline

Use these sources when refreshing facts:

- Official TYPO3 docs: ES modules/import maps, backend modules, AssetCollector and `f:asset.module`, backend AJAX, Form Editor, and v14 changelogs.
- Camino: Camp Vienna "Lit it Up!" by ochorocho: `https://dev.ochorocho.dev/camp-vienna#/`.
- Demo extension: `https://github.com/ochorocho/lit_demo`.
- Lit docs: `https://lit.dev/`.
- MDN Web Components reference: `https://developer.mozilla.org/en-US/docs/Web/API/Web_components`.

Special thanks to ochorocho for the Camp Vienna material and `lit_demo` examples that informed the practical TYPO3 backend Lit patterns in this skill.
