---
name: gather-arcgis-application-requirements
description: "MANDATORY - use before planning, building, or redesigning an ArcGIS application, including requests that do not specify an ArcGIS technology. For existing applications, use when a change could affect architecture, product, technology, data access, or authentication. Review context, clarify consequential unknowns, and route to relevant authentication and build skills."
license: Apache-2.0
---

# Gather ArcGIS application requirements

Use this skill as the shared entry point for application planning and technology selection. Gather enough information to choose an appropriate approach without repeating intake. For existing applications, preserve the current approach unless the requested change requires revisiting it.

## Application requirements

This skill is the shared requirements-review workflow. Use it to review project context and clarify consequential unknowns before applying technology-specific guidance.

## When to use
Must use this skill:

- On any new project initialization involving 2D Maps and 3D scenes, Portal and content management, Data hosting and storage, Data visualization, Spatial analysis, Place search, Geocoding addresses, Routing and directions, Data enrichment, Elevation, Security and authentication, Offline mapping apps. This includes all ArcGIS services, SDKs, APIs, and platform capabilities.
- When an existing codebase needs architectural modifications affecting Esri/ArcGIS dependencies, services, portals, or user identity management.

## Execution rules

### 1. Review context first
Inspect the request and conversation history, establish the work target, then inspect relevant configuration within that project.
- **Establish the work target:** Determine whether the user is creating a new application or script, adding features to an existing one, or updating or migrating an existing one. If unclear, ask the user. For updates or migrations, clarify the current state and intended target. Do not assume that projects sharing a workspace are related.
- If the target is unclear, ask whether to create a separate project or work within an existing one, and clarify the target folder.
- For a new project in a populated workspace, confirm a separate project folder before creating files. Do not modify sibling projects, shared configuration, or workspace-level dependencies without explicit approval.
- Scope subsequent inspection and changes to the confirmed project. Reuse existing code or configuration across projects only when requested or confirmed as shared.
- Reuse confirmed decisions about products, dependencies, resources, authentication, and deployment.
- Treat explicit user statements as authoritative.
- Distinguish confirmed facts from assumptions and unknowns.

### 2. Clarify only consequential unknowns
Ask only for missing information that could affect implementation, prioritized in this exact order:
- **Purpose:** Essential ArcGIS functionality, capabilities, workflows, and what successful completion looks like.
- **Delivery scope:** Clarify whether the user needs a lightweight test, proof of concept, or prototype, or a production-level application when this is not already clear. Identify what must work now and what can be deferred. Scale implementation complexity, testing, deployment, and operational readiness accordingly, without relaxing authentication, authorization, or credential-handling safeguards.
- **Resources and operations:** Required ArcGIS services, queries, editing, analysis, portal or administrative actions; known URLs or item IDs and access requirements.
- **Audience and identity:** Who can use the application (owner only (personal), specific users/organization (private), or the public), whether sign-in is required, and whether operations must run with the account for a specific user.
- **ArcGIS product:** Available product/account type: ArcGIS Location Platform, ArcGIS Online, or ArcGIS Enterprise (use these exact product names). If Enterprise is selected, clarify the Enterprise version.
- **ArcGIS portal:** Product-dependent; Domain is `arcgis.com` for ArcGIS Location Platform and ArcGIS Online. ArcGIS Enterprise deployments have custom configuration, network constraints, and access requirements. Relevant for authentication (non-API key) and portal management tasks.
- **Technology and compatibility:** Required SDK, API, open-source library, framework, or version constraints. Preserve compatible existing dependencies. For new projects without version constraints, use the latest supported compatible version.
- **Platform and deployment:** Target platforms (web, mobile, desktop), hosting, supported devices, and offline requirements when relevant.

#### Progressive clarification
- Break the user's request into the desired outcome, essential workflows,
  known constraints, and consequential unknowns.
- Treat the categories above as an internal checklist, not a questionnaire
  to present all at once.
- Start with the highest-priority unresolved decision. Ask a small group
  of related questions, or one question when its answer determines what
  to ask next.
- After each response, update confirmed requirements, discard irrelevant
  questions, and clarify the next consequential unknown.
- Use plain language. Recommend technical options when the user has asked
  for guidance rather than requiring them to choose unfamiliar technologies.
- Reuse answered questions and confirmed project context.
- Stop clarifying when remaining unknowns will not materially change the
  approach; carry minor assumptions into the handoff summary.

### 3. Clarify technology, platform, and SDK/API preferences
Apply these prompts only when relevant to the request and still unresolved, following the progressive clarification process above.
- **Web:** Ask whether the user prefers the *ArcGIS Maps SDK for JavaScript* or an open-source library integrated with ArcGIS services (e.g., *Leaflet, MapLibre GL JS, OpenLayers, CesiumJS*). Use the technology-routing reference to explain relevant tradeoffs.
- **Mobile:** Ask which platforms they need to support (iOS, Android, or both), and whether they prefer native development or a cross-platform framework. If they have a preference, ask which SDK/framework (e.g., *Swift, Kotlin, .NET, Flutter, Qt*); capture any existing application stack, required device capabilities, and offline needs. Recommend only options whose current platform and capability support can be verified.
- **Multiple targets:** Ask separately about web and mobile preferences when both are in scope. Do not assume one SDK or codebase should serve every target.
- **Scripting:** Ask whether the user intends to use scripting for automation, data processing, or custom workflows. Capture the preferred scripting language (e.g., *Python, JavaScript, Shell*) and any relevant libraries or frameworks (e.g., *ArcPy, ArcGIS REST JS, Jupyter Notebooks, Node.js*).

### 4. Resolve choices and route
Recommend an approach based on the confirmed requirements. Treat product, technology, audience, and authentication as related but independent decisions. Revisit a recommendation if resource or security constraints make it unsuitable.

- **ArcGIS Documentation Lookup:** Before making or supporting ArcGIS-specific recommendations, consult the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`) first for SDK, API, product, service, and capability information. Use its results to locate and verify current official Esri documentation. If the MCP server is unavailable or does not cover the topic, consult official Esri documentation directly and disclose that fallback. This documentation lookup is separate from build-skill discovery; use the technology-routing reference and plugin catalog to select skills.
- **Authentication Routing:** Follow `follow-arcgis-authentication-patterns` when authentication is unresolved or the task changes identity, privileges, or protected resource access. Carry confirmed requirements forward. If the skill is unavailable, inspect existing project patterns and consult official ArcGIS authentication documentation.
- **Build Routing:** Consult the `references/technology-routing.md` file to identify the primary `build-with-*` skill, necessary complementary skills, and documentation focus areas. These are routing recommendations, not confirmation that a skill is available or loaded; check availability and client discoverability separately. If the reference is unavailable, consult the Esri Agent Skills plugin catalog if it’s accessible through the current client. Do not substitute a similarly named technology when no matching plugin exists.
- **Plugin Management:** Check catalog availability separately from installation and client discoverability. Install plugins only when the client supports installation and the user authorizes it; verify success before claiming installation. Otherwise, provide client-specific installation guidance. If no matching plugin exists, explicitly state so and utilize official documentation links.

### 5. Security and isolation guidelines
> [!IMPORTANT]
> - Adapt explanation depth to the user without changing technical safeguards or forcing a full checklist.
> - **DO NOT infer authentication from the SDK or audience alone.** Application visibility and ArcGIS resource sharing are completely separate decisions; **never** make private or protected resources public as an access workaround.
> - **DO NOT request secrets, API keys, passwords, or tokens in chat.**
> - **DO NOT expose credentials** found in project files, configuration, logs, or environment variables.

---

## Expected output format

When handing off to the next step, emit a structured Markdown block using this exact schema:

```markdown
### ArcGIS requirements handoff summary

- **Work Target:** [New application or script / Feature addition / Update / Migration]
- **Project Folder:** [Confirmed workspace-relative path]
- **ArcGIS Product Context:** [e.g., ArcGIS Online / ArcGIS Location Platform / ArcGIS Enterprise]
- **Target Platform:** [e.g., Web, Mobile, Desktop]
- **Delivery Scope:** [Prototype / Production; required now and deferred work]
- **Identity & Access Model:** [e.g., Private ArcGIS organization, OAuth 2.0 User Sign-in Required, Public (none)]
- **Core Features and Operations:** [e.g., Maps and scenes, Portal and content management, Data hosting, Data visualization, Spatial analysis, Place search, Geocoding addresses, Routing and directions, Data enrichment, Elevation, Security and authentication, Offline mapping apps]

#### Remaining assumptions
1. [List assumption 1 or state 'None']

#### Next agent actions
- [ ] Route to `[Build skill, if needed]` for implementation.
- [ ] Route to `[Authentication skill, if needed]` if authentication is unresolved or the change affects identity, permissions, or protected resources.
```

## Completion checklist
Before passing control to a subsequent build or authentication skill, verify:
- [ ] Remaining unknowns will not materially change the architecture, technology, or access model.
- [ ] Consequential blockers are fully resolved.
- [ ] Technology-specific setup, authentication implementation, and validation tasks are cleanly deferred to the selected build skill.

## Documentation access

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult [official Esri documentation](https://developers.arcgis.com/documentation/).
