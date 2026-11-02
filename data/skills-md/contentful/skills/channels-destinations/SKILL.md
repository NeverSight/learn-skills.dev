---
name: channels-destinations
description: Set up and manage Contentful Channels, Destinations, and Destination Nodes through the Destinations Management API. Use for creating or updating channel contracts, destination properties, destination maps, experience/folder/redirect nodes, assigning experiences, routing and path configuration, publishing, unpublishing, migration, or deletion. Verify the current API schema and permissions before acting; use this skill instead of guessing endpoints or payloads.
allowed-tools: Bash(curl *) mcp__contentful-mcp__* mcp__plugin_contentful_contentful-mcp__*
---

# Channels, Destinations, and Nodes

Use the Destinations Management API first. Treat the live API reference as authoritative; bundled guidance is an execution checklist, not a substitute for checking the current contract. Runtime observations in the references are target-specific; re-check them against the current target before writing.

## Read-only fast path

For list, lookup, or tree-only requests, use the relevant read endpoint, follow pagination to completion, filter results as needed, and skip setup and lifecycle steps.

## Before making changes

1. Clarify the intended outcome and identify the exact organization, Channel, space, environment, Destination, and target Experiences. Never infer IDs or production/staging intent from display names alone.
2. Pick the tool path: use `curl` through a shell/exec tool when one is available. If not, make the same calls through the `contentful-mcp` MCP tools. If neither can reach the Destinations Management API, tell the user and stop (see [If the API is unreachable](#if-the-api-is-unreachable)). Never invent a tool.
3. Read the current API operation/schema for every operation you will use. Follow its authentication, content type, version-header, pagination, and response requirements. Never expose or echo access tokens.
4. Read existing state before writing: list Channels, list Destinations in the exact environment, and fetch the Destination tree before changing nodes. Match by stable IDs; check for duplicates and dependencies.
5. Show the proposed resource hierarchy and material properties before applying a multi-resource setup. Ask for missing user-owned choices (for example routing on/off, node paths/types, assigned Experiences, or target environment) rather than silently choosing.

## Model and scope

- A **Channel** is organization-scoped. It declares Destination-level property definitions and node-property definitions; a Channel can define at most one `Path` node property.
- A **Destination** is scoped to a space and environment and implements one Channel. Its Channel is fixed after creation. Each supplied Destination property must match a property ID and value type declared by that Channel.
- A **Destination** contains a tree of **Destination Nodes**. Use the tree endpoint to inspect/enumerate nodes; do not assume a standalone node-list endpoint exists.
- Node variants are `DestinationExperienceNode`, `DestinationFolderNode`, and `DestinationRedirectNode`. Experience nodes serve assigned Experiences; folders group nodes; redirects point to a target. Read the current schema for exact link and property shapes.

## Setup workflow

Consult [API operations and lifecycle](references/api-workflows.md) and [Domain rules and setup checklist](references/domain-rules.md) as needed.

1. **Plan the contract.** Capture Channel purpose, property IDs/names/types, and whether paths are needed. Add a `Path` node property only when path-based routing is intended. Distinguish Channel properties (required configuration values for each Destination) from node properties (per-node values).
2. **Create or reuse the Channel.** Check for an existing equivalent Channel first. Create/update only the intended Channel. Re-read it and validate property IDs are unique, types are supported, node-property names are unique, and no more than one `Path` property exists.
3. **Create or reuse the Destination.** A draft Channel is sufficient to create a draft Destination. Publish the Channel only when the user wants the Destination or its nodes published, and before publishing those resources. Create the Destination in the exact space/environment, supply all required Channel properties with matching types, then re-read it. Do not silently change the Channel association of an existing Destination.
4. **Build the map.** Fetch the tree before each structural plan. Create nodes using the explicit node `type`; attach a parent when needed. Include every required node property declared by the Channel. For experience nodes, resolve the exact Experience and confirm its status before planning publication. For redirects, resolve and validate the target from the live tree/API.
5. **Validate before publish.** Read the Channel, Destination, every ancestor, and the assigned Experience or redirect target. Confirm required prerequisites are published before sending a node publish; a draft Experience or parent can produce the misleading `422 "Some of the referenced entities do not exist."` Do not publish prerequisites without authorization. Also check path uniqueness/shape, assignments, inbound dependencies, and the affected subtree. Confirm the application—not this data model—implements HTTP routing, redirect status codes, target Experience resolution, navigation ordering, and localization behavior.
6. **Verify.** Re-fetch the Channel, Destination, and tree after writes. After node deletion, re-read the tree, GET every deleted node ID expecting `404`, and confirm intended survivors remain. Report IDs, scope, relationships, status, verification reads, and gaps; a write response alone is not proof of success.

## Changes, publishing, and deletion

- Use the current `sys.version`/version header as required. On a version conflict, re-read the resource, compare the latest state with the intended change, then re-plan using the returned version; never blindly retry or overwrite concurrent edits.
- Keep draft setup separate from release. Preview exact targets and blast radius, and get explicit confirmation for publish, unpublish, deletion, live-route changes, or broad Channel changes unless the user already authorized that exact action and scope.
- Publish in dependency order: Channel, Destination, then parents before children; publish an assigned Experience before its Experience Node. Before each node publish, confirm the Channel and Destination are published and every ancestor is published. For an Experience, check that its live `sys.localeStatus` is `published`; confirm the field against the current target schema. Redirect-target published-state requirements were not separately verified in live testing, so check the current contract rather than assuming cascade behavior. Do not publish missing prerequisites without authorization. Use explicit publish calls and verify resulting state.
- **Hard precondition—Destination unpublish:** Before any Destination unpublish call, read the tree. If any node is published, **do not send the Destination unpublish request**, even if the user asked to take the Destination offline; that request does not authorize taking individual node routes offline. List the affected nodes leaf-first and ask for confirmation to unpublish those nodes. After authorized node unpublishes, re-read the tree; call Destination unpublish only when it shows zero published nodes. The live API rejected Destination unpublish while published nodes remained.
- **Node unpublish:** descendant-cascade behavior is unverified. Unpublish leaf-first and re-read the tree; do not rely on cascade behavior.
- **Deletion:** inspect dependencies and inbound redirects first. The live API rejected Destination deletion while nodes remained (`DestinationHasNodes`); remove nodes explicitly, leaf-first, unpublishing each published node first, then delete the Destination. Remove or migrate dependent Destinations before deleting a Channel; the Channel must also be unpublished before deletion. Do not assume deleting a node removes descendants; unless the current contract confirms otherwise, delete explicitly bottom-up. Plan removal/migration of redirects pointing into the affected subtree before deleting targets.
- Do not assume UI-only bulk/cascade options exist in the API. Verify equivalent API behavior before using them.

## If the API is unreachable

If neither a shell/exec tool nor a `contentful-mcp` tool can reach the Destinations Management API, tell the user the API can't be reached and stop. Do not guess at Channel, Destination, or tree state, and do not fabricate API responses, IDs, permissions, or publish status. If the user asks for a plan anyway, label it **not executed and not based on live state**, and list the reads that must run before any of it is applied.
