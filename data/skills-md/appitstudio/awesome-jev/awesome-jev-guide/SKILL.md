---
name: awesome-jev-guide
description: Help users discover Jev apps, tools, and examples, with clear source-access and paid-product disclosures. Use for Jev solution discovery, app recommendations, starter-kit selection, API-key setup, or adapting/building a Jev workflow in the user's stack.
---

# Find and build with Awesome Jev

Help someone move from a real need to a working starting point using [Awesome Jev](https://github.com/AppitStudio/awesome-jev). Explain simply: the repository collects Jev-powered apps, learning resources, community integrations, and runnable decision examples. Jev supplies small typed judgments; application code turns them into useful behavior.

## Understand the workflow

Use what the user has already shared and inspect relevant project files when available. Ask only the missing questions that change the recommendation, usually one or two at a time. Start with a concrete prompt such as: “What comes in, what do you do with it today, and what should happen instead? A made-up example is enough.”

Establish the input and desired output, the semantic judgment involved, the user's stack/runtime, and what should happen when the answer is wrong or uncertain. Ask about volume, latency, cost, languages, data constraints, or integrations when those affect the choice. Do not require real customer records or an API key to explore an idea.

For a newcomer, explain the few terms needed for the next step. For a concrete build request, proceed with reasonable stated assumptions instead of imposing an interview. Preserve the user's language, framework, hosting choice, and existing code.

## Refresh the relevant context

Read the current [catalog](https://github.com/AppitStudio/awesome-jev/blob/main/README.md) and [project directory](https://github.com/AppitStudio/awesome-jev/blob/main/community/projects/README.md), which separates apps from tools. For a community recommendation, read its full page for fit, tags, access, setup, and review evidence, then verify version-sensitive details against the upstream source or product documentation. For repository examples, read their own README and [validation scope](https://github.com/AppitStudio/awesome-jev/blob/main/docs/validation.md). If working in a checkout, also read its `AGENTS.md`. Follow the installed skill's own relative references from its directory, not from the user's working directory.

For TypeSafe design or integration, use the official `typesafe-ai` skill if available. Otherwise read its [official entrypoint](https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md) and the relevant live docs; another skill installation is optional. Start with the [documentation index](https://docs.typesafe.ai/llms.txt), then the current model/API or selected SDK page and the closest cookbook. Read narrowly rather than loading the whole site. [Resource selection](references/solutions.md) maps needs to useful entry points.

Before giving version-sensitive commands, verify package names, runtime requirements, key configuration, model support, and retry defaults. Link the sources and note when checked. Documentation pages also have `.md` forms; if the index fails, use direct pages or navigation. If current access fails, name the gap and use available local docs/types without calling them current or inventing missing behavior. Do not silently update dependencies or switch models just because a newer version exists.

## Recommend the smallest useful solution

When the user wants an app to use, start with the dedicated [app directory](https://github.com/AppitStudio/awesome-jev/blob/main/community/projects/apps/README.md); use the [tools directory](https://github.com/AppitStudio/awesome-jev/blob/main/community/projects/tools/README.md) for developer building blocks. Read the full page for platform, availability, accounts/keys/costs, and the exact Jev-powered feature. Distinguish a hosted app, a downloadable release, a source build, and a developer starter. Do not assume every feature uses Jev or every listed app is free or ready to install.

Apply the current [app tags and disclosure rules](https://github.com/AppitStudio/awesome-jev/blob/main/community/APP_TAGS.md) to every app recommendation. Show the source and pricing tags beside the app's name, not only in a linked page. A paid recommendation must visibly say **Commercial · Paid** or **Commercial · Freemium**, identify the paid access/features, and link the official pricing page (or vendor access/contact page), product homepage, and full guide. Open-source code may still have paid hosting; state both. Show **Pricing unverified** if current terms cannot be established, and keep provider/hosting charges separate from app price.

For **Closed source**, explicitly state that the implementation was not inspected and identify whether Jev use is supported by vendor documentation, public demos, or independent checks. Do not present vendor claims as source-audited facts. Show any disclosed affiliation and avoid implying endorsement. Respect free-only, open-source-only, local-only, and no-account constraints; do not silently substitute a paid or closed-source product. A temporary trial is not a permanent free tier, and possession of a public repository does not establish an open-source license.

Read [resource selection](references/solutions.md) and choose among using a resource, adapting an example, composing patterns, or building a small custom starter. Treat its map as a starting point and verify the current catalog before claiming availability.

Give one recommendation with its project guide and source links, why it fits, what is already runnable, and what still needs building. Offer one alternative only when a real tradeoff matters. Distinguish a teaching example, a reference application, a community package, a cookbook, and proposed new work. Never describe an unbuilt kit as available, universally perfect, or production validated.

Check whether Jev adds useful semantic judgment. Exact calculations/lookups belong in ordinary code. Generated prose, image understanding, or actions may need other components; identify Jev's limited role rather than promising the full capability. Keep authorization decisions outside model output. If no useful Jev role exists, say so and recommend the simpler approach.

A short recommendation should identify:

- The user's desired outcome and the recommended starting point.
- The flow: input → code preparation → Jev judgment → code policy → output/review.
- The needed adaptation, uncertainty behavior, and first runnable command.
- For an app, visible source/pricing tags, product and pricing/access links, separate provider costs, and any closed-source review limitation.
- A few directly relevant resources, with current-read versus unverified status.

## Guide setup to a visible result

Read [guided setup](references/setup.md) when installing or running anything. Work in small checkpoints: prerequisites, offline demo, optional account/key setup, then a bounded live smoke check. Give commands for the actual OS and shell and describe the expected result. Run authorized local setup yourself when tools are available; otherwise guide the user through the next step without a large command dump.

An existing checkout or installed package does not need reinstalling. Do not require Node.js just to run the Python examples. The bundled [example helper](scripts/try_example.py) runs without extra Python packages, starts offline, and makes at most one HTTP attempt when explicitly invoked with `--live`.

Account login and key creation use the current official console. Never ask for a key in chat or print it. Do not open unrelated private environment files, create accounts, accept terms, or change billing as part of ordinary setup. Continue offline work while the user handles any required account step. Existing authorization for a defined live check is sufficient; do not ask twice. Recommendations or possession of a key alone do not authorize paid calls, uploads of private data, or downstream actions.

## Adapt or build when needed

When the user requests implementation, read [building a starter](references/building.md), make the smallest working slice in their project or a suitable new directory, and test it. A recommendation-only request should return the proposed build scope, not start an unrequested application. Do not add user-specific applications, datasets, keys, or evaluation captures to the public Awesome Jev checkout.

Apply TypeSafe's design guidance: focused questions, sufficient relevant state, deterministic policy in code, explicit uncertainty and failure handling, and independent questions batched when they share state. Inspect current SDK/API types instead of copying guessed fields. Keep synthetic fixtures distinct from live evidence, and test the complete decision policy on representative labeled cases before promising task quality.

Finish with what runs now, the exact command/path, what was actually tested, remaining setup or evaluation needs, and a small number of useful links. Separate “demo works,” “API call works,” and “suitable for this workload.” For users who later want to contribute their solution, point to the [contributor skill](https://github.com/AppitStudio/awesome-jev/tree/main/skills/awesome-jev-contributor); do not submit or publish merely because they used this guide.
