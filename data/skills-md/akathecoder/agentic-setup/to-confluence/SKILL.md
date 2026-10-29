---
name: to-confluence
description: Turn project knowledge into a concise, standalone Confluence page for teammates.
disable-model-invocation: true
---

# To Confluence

Create or update a teammate-facing Confluence page from the current discussion and
the active project's artifacts. The page must stand alone: its readers do not have
access to the local repository, `.agents/projects/<project>/`, or the agent conversation.

Resolve every `.agents/projects/` path from the opened workspace root, including
when the active repository is nested inside it. In a single-repository workspace,
that is the repository root. Keep this artifact root fixed when changing directories;
never use nested repositories or global agent-installation directories for artifacts.

## Process

1. Identify the active project and the requested document purpose. Read the relevant
   project context, links, spec, ticket drafts, implementation notes, review, and ADRs.
   Use an existing Confluence page reference when one is available. Ask only for the
   audience, page location, or purpose that cannot be inferred from project context.

   Done when the source material, intended readers, and target page are known.

2. Synthesize the material into one concise, self-contained page. Lead with the
   problem or purpose, state the recommendation or current outcome, then include only
   the decisions, implementation details, risks, rollout information, and open
   questions that the intended readers need. Use plain language and explain necessary
   project terms on first use.

   Never direct a reader to local files or refer to an earlier agent discussion. Do
   not create empty template sections, copy internal scratch material, or split a
   coherent document into sub-pages. Split only when the user requests it or separate
   audiences or independent lifecycles make separate pages clearly more useful.

   Done when the full draft answers its readers' likely questions without requiring
   private local context.

3. Save the proposed page body under `.agents/projects/<project>/confluence-draft.md` and show
   the user the title, target location, and complete draft. Wait for explicit approval
   before creating or editing any Confluence page.

   Done when the user approves the exact page content and target, or declines it.

4. On approval, use the configured Confluence MCP to create or update only the
   approved page. Preserve useful existing page content unless the approved draft
   explicitly replaces it. If MCP access is unavailable, leave the local draft ready
   to publish and record the limitation in `.agents/projects/<project>/todo.md`.

   Done when the approved page is published or the ready-to-publish draft and
   limitation are recorded.

5. Update `.agents/projects/<project>/LINKS.md` and `CONTEXT.md` with the Confluence page URL,
   title, and purpose. Do not append `Written by AI Agent`; that convention applies to
   conversational tracker comments, not documentation.

   Done when project context links to the published documentation.
