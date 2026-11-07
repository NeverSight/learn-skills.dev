---
name: exo-content-bindings
description: Create Data Assemblies (content bindings) in a Contentful Experience Orchestration space, connecting existing entries to component content properties. Covers classifying coded vs. composite component types, judging content vs. design properties, public vs. private (hoisted) properties, slot vs. content-binding scope, and designing, creating, linking, and publishing Data Assemblies via the CMA. Use when asked to create Data Assemblies, wire up content, bind entries to components, hydrate a component, or set up a Binding Set. Also triggers on "content binding", "data assembly", "prebinding", "create DA". Not for placing components into a template's structural slots (assembly, not binding) or attaching bindings to an existing Experience/Fragment instance — this skill creates reusable recipes, not per-instance bindings.
license: MIT
argument-hint: "[space id] [component type or content type]"
allowed-tools: Bash(curl *) mcp__contentful-mcp__* mcp__plugin_contentful-skills_contentful-mcp__*
metadata:
  author: contentful
  version: "1.0.0"
---

# ExO Content Bindings — Data Assembly Creator

## Overview

Creates Data Assemblies that connect existing Contentful entries to Experience Orchestration component types. A Data Assembly is a parametrized query with a known return type — it describes *how* entry fields hydrate a component's content properties.

**Mental model — four layers:**

| Layer | Entity | What it does | Example |
|-------|--------|--------------|---------|
| Schema | Component Type / Template | Declares `contentProperties` — named "holes" expecting content | `heading`, `image`, `ctaLabel` |
| Recipe | Data Assembly (API) / Binding Set (UI) | Describes *how* entries fill those holes (resolvers + return map) | "Product Card from Product" |
| Instance | Experience / Fragment / Inline Component | Stores `contentBindings` — a chosen DA + parameter entries | this card uses `productEntry123` |
| Runtime | Delivery payload | Resolved values written into content properties | `heading = "Spring Sale"` |

This skill operates at the **Recipe layer** — creating and publishing Data Assemblies.

**The invariant that makes the model work:** the component tree **always reads through `$contentProperties/...`** — never directly from an entry, never from `$contentBindings/...`. Every binding strategy exists to fill a content property. *A binding that fills no content property computes data nothing reads.* Use this as a correctness check on any DA you design: trace each `return` key to a declared content property, or delete it.

The practical consequence: from the component's point of view, a manual value and a DA-hydrated value are indistinguishable. It just reads a content property. That is why the DA-vs-literal choice is a modeling decision, not a rendering one.

## Terminology

Precise language prevents misunderstandings between these easily conflated concepts:

| Term | What it is | What it is NOT |
|------|-----------|----------------|
| **Content property** | A named input on a Component Type or Template that receives content | Not a content-type field (those are the *source*) |
| **Content-type field** | A field on a Contentful content type (the CMS data) | Not a content property (those are on ExO components) |
| **Parameter** | One marketer selection input on a DA, constrained to allowed content types | Not a binding — it's the *input* to a binding |
| **Field mapping** | A target content property + source path starting from a parameter | Not the parameter itself |
| **Binding set** | The UI/editor name for an editable data-wiring configuration that corresponds 1:1 with a Data Assembly. Use "Binding Set" when referencing editor UI; use "Data Assembly" when referencing API calls. | Not the DA entity itself — same thing, different contexts |
| **Prebinding** | The ComponentType editor workflow where DAs are defined. This skill automates what Prebinding does in the UI. | Not the runtime resolution step |
| **Content binding** | An instance choosing a DA + providing entry IDs for its parameters (at the Experience/Fragment level) | Not the DA itself (that's the recipe) |
| **Nested binding** | A PropertyMapping that gives a content property the whole output of a child DA through a DataAssemblyResolver | Not a reference field traversal |
| **Reference path** | Zero or more reference fields followed by a terminal value field | Not a display label |
| **Template** | A page-level entity governing Experiences (has channel config). Can be coded or composite, same as component types | Not interchangeable with "component type" — templates have channels/viewports |

## Tool access

This skill calls the Contentful Management API (CMA) directly. Prefer `curl` (via Bash) when a shell is available — the examples in `references/` use it. If no shell/exec tool is available, make the equivalent calls through the `contentful-mcp` MCP tools instead (same endpoints and payloads, translated to whatever tool the server exposes for spaces/component types/data assemblies). If neither `curl` nor `contentful-mcp` is reachable, say so explicitly and stop — do not guess at space state or fabricate a plan without introspecting first.

## Content property vs. design property

A content property is content, not presentation. Before designing any mapping, apply this test to each property:

- Changing the value changes **what is said** → **content property** (bindable; a DA may fill it)
- Changing the value changes **how it looks** → **design property** (never bind it)

**Apply the test explicitly rather than guessing from the property name, and rather than relying on which array the property appears in.** `variant`, `columns`, `backgroundColor`, `showDivider`, `theme`, `alignment` are design properties **even when their values happen to come from the CMS**. A `theme: light|dark` field on a content type is the classic trap: it is CMS-authored, so it looks bindable, but it changes how the component looks, so it is not a content property and must not appear in a DA's `return` map.

The converse also holds: a property whose name sounds decorative (`badgeText`, `eyebrow`, `label`) is a content property if changing it changes what the page says.

This test governs field-mapping inference (`references/api-workflow.md` step 5.3). A source field that fails it is not an unmapped content property — it is *correctly* unmapped, and should be reported that way in the Binding Plan rather than listed as a gap.

## Process overview

1. **Introspect the space** — fetch component types and content types. Check for a reference space with the same components already wired.
2. **Classify each component type** — coded (leaf, all content properties public) vs. composite (tree, mix of direct + hoisted properties). See "Public vs. private" below.
3. **Design DAs** for coded and composite types separately — composites need extra care around hoisting and slot boundaries.
4. **Infer field mappings**, gated by the content-vs-design test and the public/private golden rule, then produce a Binding Plan and **get explicit user approval before creating anything**.
5. **Create, link, and publish** each Data Assembly, then verify and produce a mandatory Complete Binding Map.

Full CMA call sequences, request/response shapes, and exact commands for every step: **[references/api-workflow.md](references/api-workflow.md)**.
Full resolver request bodies (entity, collection, nested-DA, asset/Media, deep binding, polymorphic): **[references/resolver-patterns.md](references/resolver-patterns.md)**.
Pointer expressions, GraphQL conventions, RichText handling, and the type mapping table: **[references/richtext-and-types.md](references/richtext-and-types.md)**.
A complete worked example end to end: **[references/worked-example.md](references/worked-example.md)**.

## Public vs. private

Not every content property in a composite is reachable from outside.

**Public** properties are the subset exposed on the component's surface. Only public properties can be overridden by a parent embedding this component, targeted by a Data Assembly, or seen and edited by a marketer. They are the component's **stable content input contract**.

**Private** properties belong to child components inside the `componentTree` and are not exposed. There is no `privateProperties` array — privacy is defined *by absence*: a child property is private precisely because it was **not hoisted**. Do not go looking for a list of private properties; enumerate the tree's children and subtract what appears in the parent's `contentProperties`.

**The golden rule: never bind, override, or map a property that is not public.** If something must be bound, it has to be hoisted first — which is a component-type change, outside this skill's scope.

### Hoisting rules

1. **Required** child content properties are **automatically hoisted** to the parent's public surface
2. **Optional** child properties are hoisted **intentionally** — only when the designer decides the parent should control them
3. If a needed property isn't in the parent's `contentProperties`, it's private — the component type must be updated first (out of scope)
4. Per-property hoisting and whole-component hoisting (`TypeRef`) are mutually exclusive for the same child
5. **De-hoisting orphans DAs** — if a public property is later un-exposed, every DA referencing it breaks. This is why checking existing DAs before adding another matters.

**Rules 1 and 3 can contradict each other — say so when they do.** If a child property is **required** on the child but **absent** from the parent's `contentProperties`, rule 1 says it should have been hoisted automatically. Do not silently record it as "intentionally private." Report it as a **possible modeling or auto-hoisting defect** for the component-type owner, alongside the blocked mapping. A required-but-unreachable property means the composite cannot render correctly from any binding.

### Should a property be public?

You cannot change hoisting from this skill, but you will be asked *whether* something should be hoisted. Recommend hoisting when **any** of these hold:

- it is **required** by the child (automatic — see the contradiction rule above),
- a **marketer must control it** per instance,
- a **DA needs to fill it** — only public properties are bindable,
- a **parent must override it** when embedding the child.

Recommend keeping it private when:

- it is an internal implementation detail (a computed alt text, a layout-only string),
- exposing it adds noise without editorial value — hoisting every child property produces `text1, text2, url1, url2…` clutter, which is explicitly discouraged,
- nothing outside the child will ever bind to or override it.

**Default posture: hoist the minimum that satisfies the four triggers; leave everything else private.** A small, intentional public surface is the goal.

### Slot boundaries

Slots create a hard DA ownership boundary:

```
Parent DA scope:
├── parent's contentProperties (direct + hoisted) ← DA targets these
├── componentTree children read via $contentProperties/... ← fed by parent DA
└── [SLOT: "main"]
    └── Child components placed here ← SEPARATE DAs, not parent's
```

**Never** attempt to map fields into a slot child's properties from the parent's DA.

### Slot vs. content binding — the distinction that decides scope

Both are reference-shaped. They mean opposite things, and confusing them produces a structurally wrong experience.

| | Slot | Content binding |
|---|---|---|
| Means | "this component **contains** these other visual components" | "this component **reads data from** these records" |
| Referenced thing | becomes a Fragment inside this component | stays content, accessed through a Data Assembly |
| Target shape | presentational — has its own layout, design properties, nested references | data-oriented — flat domain data, no layout |

**How to tell:** look at what the reference actually points to. If the target has its own visual structure (layout fields, design properties, nested presentational references), it is a slot. If it is flat domain data — categories, tags, profiles, events — referenced by many different types as a shared source, it is a binding.

The same distinction routes the request you were given. "Fill the slots" is ambiguous and resolves by context:

- **Assembly** — placing fragments/components into a template's structural slots. Only when the user is actively building or changing a tree.
- **Content binding** — linking CMS entries to binding parameters on an **already-assembled** experience. The signal: the user is not asking to change layout, they want content connected to what already exists.

Phrases like "fill unlinked slots", "populate empty slots", "fill in missing entries" with **no structural intent** mean **content binding on instances**, not assembly — and not this skill either. This skill builds the *recipes*; it does not attach bindings to Experience or Fragment instances (see Limitations).

**So when a request contains that phrasing, name it rather than only declaring it out of scope.** Say which layer it belongs to, confirm that the DAs this skill creates are the prerequisite for it, and state what remains to be done afterwards — per instance, in the editor or via the instance API. Answering "out of scope" without naming the layer leaves the user unable to act.

**You MUST produce a complete binding plan and get user approval before creating any Data Assemblies.** Do not skip this step. Do not create DAs incrementally without a plan. See [references/api-workflow.md](references/api-workflow.md) §5.4–5.5 for the plan format.

## Quick Decision Guide

Steps 0a and 0b decide *whether* to bind. Steps 1–3 decide *how*. Do not start at Step 1.

```
Step 0a: Is this request even about Data Assemblies?
  "Bind entries to components" / "wire up content" / "create DA"
    → YES, this skill. Continue.
  "Fill the empty slots" / "populate this page" / "fill in missing entries"
    → Instance-layer content binding. This skill creates the prerequisite
      recipes but does NOT attach bindings to instances. Name the layer,
      create the DAs, then say what remains per instance.
  "Place these components into the template" / "build the tree"
    → Assembly, not binding. Not this skill.

Step 0b: Is this property a content property?
  Changing the value changes WHAT IS SAID   → content property, continue
  Changing the value changes HOW IT LOOKS   → design property, STOP.
      Never bind it. Report as correctly-unmapped, not as a gap.
      (theme, variant, columns, alignment, backgroundColor, showDivider —
       still design properties when the value comes from the CMS)
  Is it public (present in the component type's contentProperties)?
    NO → STOP. Golden rule: never bind a non-public property.
         Required on the child but absent here? → flag as a possible
         auto-hoisting defect, not as intentionally private.

Step 1: What kind of component type?
  CODED → all contentProperties are public, go to Step 2
  COMPOSITE → check contentProperties list:
    Has contentProperties? → go to Step 2 (they're all public/hoisted)
    No contentProperties? → this composite doesn't need a DA
      (content arrives via slot children, each with their own DA)

Step 2: What feeds this content property?
  Single entry's field(s)?
    YES → Entity resolver (kind: "entity", _node query)
      Needs fields from a linked entry (reference)?
        YES → How complex is the linked entry?
          Simple (1-2 fields) → Scalar deep bind (traverse ref in GraphQL query)
          Complex (own component) → TypeRef deep bind (nested DA)
          Limit: ≤ 3 hops from root entry
        NO  → Single GraphQL resolver (shallow bind)
  Array of entries?
    YES → Collection resolver (kind: "collection", ...Collection query)
  Fixed value?
    YES → Use $literal in return (no resolver needed)
  Polymorphic source (multiple possible types)?
    YES → Use $on to branch on __typename

Step 3: Is this property on a slot child?
  YES → Create a SEPARATE DA for that child (do not include in parent DA)
  NO  → Include in the component's own DA
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Not classifying coded vs. composite first | Always classify — composites may not need a DA at all |
| Building a DA for a composite that only has slot children | If all content comes via slots, each child gets its own DA — parent needs none |
| Trying to hydrate slot children from the parent's DA | Slot boundary is absolute — each slot child needs its own DA |
| Using bare string pointers in `return` without checking reference | Default to `$from` syntax — bare pointers work but aren't editable in BindingPanel. Replicate reference space style if one exists. |
| Missing `__typename` in GraphQL query | Required for `$on` branching at runtime |
| Using CMA field IDs directly in GraphQL | GraphQL uses camelCase (e.g., `internalName` not `internal_name`) |
| Forgetting `kind: "collection"` for array resolvers | Without it, resolver returns single object not array |
| Setting `allowedTypes` to content type *name* instead of *ID* | Must be the programmatic ID (e.g., `topicProduct` not `Topic Product`) |
| Creating DA with same ID without version header | Fetch version first, or use upsert pattern (see [references/api-workflow.md](references/api-workflow.md)) |
| Mapping a property that isn't in `contentProperties` | Only the component's declared public properties are bindable |
| Hoisting per-property AND whole-component for same child | Mutually exclusive — pick one strategy |
| Not linking DA to the component type | After creating, add DA to the component type's `dataAssemblies` array — without this, it won't appear in the binding panel |
| Not publishing the DA after creation | Unpublished DAs not available for binding in editor |
| `sys.dataType` IDs don't match `contentProperties` IDs | They must be identical — the DA's dataType is the contract between resolver output and the component's input |
| Modeling images as bare `String` (URL only) | Use `Record` with url/width/height/alt/contentType |
| Mapping asset `alt` from the asset's `title` | `alt` comes from `description`, falling back to `title` only when `description` is empty across the sample — and say so in the Binding Plan when you fall back |
| Binding a design property because its value comes from the CMS | Apply the what-is-said / how-it-looks test. `theme`, `variant`, `alignment` are design properties regardless of source |
| Recording a required-but-unhoisted child property as "intentionally private" | Required properties are auto-hoisted — absence is a possible modeling defect. Flag it |
| Mapping a low-confidence guess to fill out the plan | Leave it unmapped and name it. A wrong mapping produces plausible content in the right shape, so nobody notices it |
| Answering "out of scope" to a "fill the empty slots" request | Name the layer it belongs to and what remains after the DAs exist |
| Using `$from` syntax for RichText fields | RichText requires bare string pointers to the parent object. `$from` causes "expected RichText, got String" |
| Declaring RichText as `String` dataType to avoid validation | Use `RichText` dataType + `{ document: json }` alias + bare parent pointer. The platform resolves it natively |
| Pointing to `/json` or `/document` leaf for RichText | Point to the parent (e.g., `$resolvers/main/ct/subline`). The platform reads the aliased `document` key itself |
| Omitting `sys.id` from PUT body | API rejects with "Invalid input at sys.id" — always include `"id": "$DA_ID"` in the sys object |
| Creating duplicate DAs for components sharing the same content property IDs | Create ONE DA and link it to multiple component types (see [references/worked-example.md](references/worked-example.md)) |

## Operating Principles

1. **Introspect before designing** — do not invent content-type fields, content properties, or IDs. The space's schemas are the source of truth.
2. **Content properties ≠ content-type fields** — a content property is the *target* (on the component); a content-type field is the *source* (on the entry). They often have different names.
3. **Validate paths against content-type metadata** — a return mapping like `_node/headline` must correspond to an actual field on the source content type.
4. **IDs are stable contracts** — DA IDs, parameter IDs, and dataType IDs form contracts. Display names can change; IDs cannot after publication without a migration.
5. **Reference traversal is typed** — `_node/author/name` means "follow the `author` reference, then read `name`". Each segment must be a valid field on the resolved type at that depth.
6. **Only public properties are bindable** — if a property isn't in the component type's `contentProperties` array, it cannot be targeted regardless of whether it exists internally. Never bind, override, or map a property that is not public.
7. **Propose before creating** — if the mapping between source fields and target properties is ambiguous (similar names, multiple candidates), present options and confirm.
8. **Content, not presentation** — a mapping target must pass the what-is-said / how-it-looks test. CMS-authored design values (`theme`, `variant`) are still design properties.
9. **Every `return` key fills a declared content property** — the tree reads only through `$contentProperties/...`, so a mapping that fills nothing is dead weight, not a spare.
10. **An absent mapping beats a wrong one** — leave low-confidence properties unmapped and name them in the Binding Plan. Wrong mappings produce plausible content in the right shape and are hard to spot.
11. **Never claim to have unbound, replaced, or rewired anything** — existing DAs are reused or extended, never silently displaced.

## Limitations

- This skill creates Data Assemblies and links them to component types — it does not attach content bindings to experience/fragment instances
- GraphQL introspection not available via CMA — field names inferred from content type definitions
- Nested DA composition requires the referenced DA to already exist and be published
- `$on` type discriminator uses GraphQL `__typename` (PascalCase of content type ID)
- If a needed property is not hoisted (private), this skill cannot fix it — component type must be updated first
- Composites with no `contentProperties` don't need DAs — all content flows through slot children
- The pointer language has no coalesce operator, so per-value fallbacks (e.g. asset `description` → `title`) cannot be expressed in a DA. They are resolved at design time by sampling; see [references/resolver-patterns.md](references/resolver-patterns.md) "Asset (Media) fields"
- The CMA returns **both drafts and published entries with no preference between them**. Nothing in a DA's parameter definition can express "prefer published" — `allowedTypes` filters by content type only. If publication state matters for a component, it has to be handled by the marketer at bind time or by the source content model, not here

## Related Skills

- the `contentful-guide` skill — general Contentful concepts and API routing
- the `contentful-migration` skill — content model/schema changes (hoisting a property requires a component-type change, which is out of this skill's scope)

## Provenance

The procedure, resolver patterns, GraphQL conventions, and API call sequences here were developed and validated against live Contentful spaces. The judgment layer — the content-vs-design test, the public/private golden rule, "should a property be public?", the slot-vs-content-binding distinction and request routing, and source-selection confidence — reflects hoisting and content-binding rules defined by Contentful's Experience Orchestration platform. Where this file and the platform's own behavior disagree, the platform wins — report the discrepancy rather than following this file.
