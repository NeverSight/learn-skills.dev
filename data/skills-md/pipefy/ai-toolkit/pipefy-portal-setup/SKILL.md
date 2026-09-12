---
name: pipefy-portal-setup
description: >
  Use this skill when the user wants to list, create, or configure Pipefy
  portals (main hub, pages, page elements, sub-portals, publish/unpublish).
  Covers 20 MCP tools on Interfaces + internal_api. Not for pipes/cards.
tags: [pipefy, portal, interfaces, sub-portal, pages, elements]
---

# Portal setup

Configure an organization's Pipefy portal: bootstrap the main hub, add pages and widgets, wire and publish sub-portals. **20 MCP tools** (Interfaces GraphQL + internal_api for sub-portal wiring).

Deep reference: [`docs/mcp/tools/portal.md`](../../../docs/mcp/tools/portal.md). Parity matrix: [`docs/parity.md`](../../../docs/parity.md). Env vars: [`docs/config.md`](../../../docs/config.md).

---

## When to use

- "Create our company portal", "list portals for org X", "publish a sub-portal".
- Add or change portal pages, layout, or page elements (`forms`, `link`, etc.).
- Attach, publish, unpublish, or delete sub-portals on the main portal.

Do **not** use for:

- Pipes, phases, cards, or automations — see `skills/pipes-and-cards/`, `skills/automations/`.
- Raw GraphQL when a portal tool exists — prefer the tools below.
- Bootstrapping a portal via undocumented `createInterface` GraphQL — always use **`create_portal`** / **`pipefy portal create`**.

---

## Prerequisites

- **Organization id:** UUID or **numeric org id** from `pipefy org get` / the Pipefy URL (examples below use fictional `123456789` per [`fixture_ids.py`](../../../packages/sdk/tests/_shared/fixture_ids.py)). SDK resolves numeric ids before Interfaces calls. The org you pass to **`list_portals`** / **`create_portal`** must be the same org your token can write on.
- **Portal writes:** token needs **`create_portal`** and/or **`manage_portals`** on that org. Many service accounts only have pipe/card scope on their default org → `PERMISSION_DENIED` on portal mutations even when reads succeed elsewhere.
- **One main portal per org** — `create_portal` is idempotent (second call returns the same portal UUID).
- **Cursor MCP:** after changing `PIPEFY_*` in `.env`, restart the MCP server so tools pick up the new credentials.

### Confirm access before writes

Reads on the wrong org can succeed while Interfaces writes fail. Before page/element/sub-portal mutations:

1. Call **`list_portals`** with the intended `organization_uuid`.
2. Ensure the token is meant for that org (service account email vs human user on a different org is a common mismatch).
3. Prefer an org where the account has **`manage_portals`** and portal admin in Pipefy (not only `canManagePortals` on a read query from another org).

If **`update_portal`** or **`delete_portal`** returns `PERMISSION_DENIED` but the user insists the org role is correct: Pipefy may require **`joinAsAdmin`** on that portal interface for service accounts (Interfaces mutation, not shipped as MCP/CLI). The user must join as portal admin once in the UI (or via GraphQL) per portal UUID before SA writes succeed.

---

## How portals are organized

| Concept | What to expect |
|--------|----------------|
| **Main portal** | At most **one** per org (`subType: portal`). Created with **`create_portal`** (`findOrCreateInterfaceByTemplate`). |
| **`list_portals`** | Usually **one row** — the main portal only (filter `portal`). Sub-portals do **not** appear here. |
| **Sub-portals** | Separate entities (`create_sub_portal`). Listed under **`get_portal` → `subPortals[]`**. |
| **UI on the main hub** | Creating sub-portals does **not** add tiles to the main page. You must **publish** (or attach) on a **`forms`** element via **`publish_sub_portal`** / **`update_sub_portal_element`**. |
| **End-user visibility** | Sub-portals with **`published: false`** exist in the API but are **invisible to portal visitors** until published. |
| **Public main hub** | Main portal **`published`** is always `true` on `get_portal`. **Public** access = **`update_portal(visibility="public")`**, not the `published` flag. |

### Main portal lifecycle

- **Prefer `update_portal`** on an existing main portal over **delete + `create_portal`** on orgs you reuse for testing.
- **`delete_portal`** on the main removes one interface UUID; **orphan sub-portals** can remain unless deleted first.
- After deleting the main, **`create_portal`** may fail with **`Menu already created`** (org menu state persists while `mainPortal` is null). Recovery: delete orphan sub-portals, use Pipefy admin/support, or bootstrap content on the surviving UUID — do **not** switch to raw **`createInterface`**, which leaves a skeleton main page (`"Page"`, **0 elements**) and a broken builder; idempotent **`create_portal`** will keep returning that UUID.

### Empty main page

If **`get_portal`** shows a main page with **no elements**, call **`create_portal_page`** with **`title` only** (no `elements` in the request). The API typically returns a page with **~14 templated widgets** (text, forms, links, etc.). Use that page for publish slots and element tests. Do **not** pass `type: subPortal` inside **`create_portal_page`** — validation fails at create time.

---

## Schema notes

| Topic | Rule |
|-------|------|
| **Response ids** | GraphQL field is `id`; MCP/CLI expose **`uuid`** (same value). |
| **`published` on list** | **`list_portals` does not return `published`** — call **`get_portal`**. |
| **Sub-portal in layout** | Tiles may appear under **`pages[].elements[]`** with `type: subPortal` even when top-level `subPortals[]` is empty. |
| **Publish wire** | Use **`publish_sub_portal`** / **`update_sub_portal_element`** on an existing **`forms`** element (`updateSubPortalElement` on internal_api). **`create_portal_element` with `type: subPortal`** is not a substitute for publish. |
| **Element metadata** | **`update_portal_element`** is **replace-all** — send the full `metadata` JSON every time. |
| **Metadata keys** | `forms` → `name` (not `formId`); `link` → `linkName` / `linkUrl` (not `url` / `label`). |
| **Layout JSON** | **`update_portal_page_layout`** expects an **array** of row objects (`id`, `type: "row"`, `children: [elementUuid, ...]`). Copy from **`get_portal`**. A wrapper like `{ "rows": [...] }` fails API validation. |
| **Page grid vs elements** | **`create_portal_element`** does not update the layout grid; **`duplicate_portal_element`** appends layout rows; **`delete_portal_element`** does not remove layout refs unless you update layout — orphan refs can break the portal viewer (HTTP 500). |

---

## Tools needed

| Tool (MCP) | CLI equivalent | Read-only |
|------------|----------------|-----------|
| `list_portals` | `pipefy portal list` | Yes |
| `get_portal` | `pipefy portal get` | Yes |
| `create_portal` | `pipefy portal create` | No |
| `update_portal` | `pipefy portal update` | No |
| `delete_portal` | `pipefy portal delete` | No |
| `create_portal_page` | `pipefy portal page create` | No |
| `update_portal_page` | `pipefy portal page update` | No |
| `delete_portal_page` | `pipefy portal page delete` | No |
| `sort_portal_pages` | `pipefy portal page sort` | No |
| `update_portal_page_layout` | `pipefy portal page layout update` | No |
| `create_portal_element` | `pipefy portal element create` | No |
| `update_portal_element` | `pipefy portal element update` | No |
| `delete_portal_element` | `pipefy portal element delete` | No |
| `duplicate_portal_element` | `pipefy portal element duplicate` | No |
| `create_sub_portal` | `pipefy portal sub-portal create` | No |
| `update_sub_portal_element` | `pipefy portal sub-portal attach` | No |
| `publish_sub_portal` | `pipefy portal sub-portal publish` | No |
| `unpublish_sub_portal` | `pipefy portal sub-portal unpublish` | No |
| `delete_sub_portal_element` | `pipefy portal sub-portal detach` | No |
| `delete_sub_portal` | `pipefy portal sub-portal delete` | No |

Element `type` values (15): `text`, `table`, `field`, `embedLink`, `embedVideo`, `embedImage`, `button`, `divider`, `link`, `forms`, `pages`, `subPortal`, `automationButton`, `contentBlock`, `document`.

---

## Steps — happy path (main portal + sub-portal publish)

1. **List or bootstrap the main portal**

   MCP:
   ```
   list_portals organization_uuid="123456789"
   ```

   Expect **at most one** main portal row. If none:

   MCP:
   ```
   create_portal organization_uuid="123456789"
   ```

   CLI:
   ```bash
   pipefy portal list --organization-uuid 123456789
   pipefy portal create --organization-uuid 123456789
   ```

   Capture `uuid` where `subType` is the main portal.

2. **Inspect structure**

   MCP:
   ```
   get_portal portal_uuid="<MAIN_PORTAL_UUID>"
   ```

   CLI:
   ```bash
   pipefy portal get <MAIN_PORTAL_UUID>
   ```

   Note `pages[]`, `elements[]`, and **`forms`** element ids. If the main page has **zero elements**, run **`create_portal_page`** (title only) on that portal before adding widgets.

3. **Optional — add a `forms` element** (if no templated `forms` slot exists)

   MCP:
   ```
   create_portal_element page_id="<PAGE_ID>" type="forms" metadata={"name": "Request access", "gridMap": {"height": 66, "columns": 4, "minColumns": 4}}
   ```

   If **`create_portal_element`** returns an opaque or `INTERNAL_SERVER_ERROR` from Interfaces, **`duplicate_portal_element`** from an existing link on the **same** `portal_uuid` and `page_id` instead of retrying create blindly.

   CLI:
   ```bash
   pipefy portal element create --page-id <PAGE_ID> --type forms \
     --metadata '{"name":"Request access","gridMap":{"height":66,"columns":4,"minColumns":4}}'
   ```

4. **Create a sub-portal**

   MCP:
   ```
   create_sub_portal main_portal_uuid="<MAIN_PORTAL_UUID>" name="Partner hub"
   ```

   CLI:
   ```bash
   pipefy portal sub-portal create --main-portal-uuid <MAIN_PORTAL_UUID> --name "Partner hub"
   ```

   Capture the sub-portal `uuid`. **`get_portal` will list it under `subPortals[]` with `published: false`** — the main hub UI is unchanged until step 5.

5. **Publish on a `forms` element**

   MCP:
   ```
   publish_sub_portal portal_uuid="<MAIN_PORTAL_UUID>" element_id="<FORMS_ELEMENT_ID>" sub_portal_uuid="<SUB_PORTAL_UUID>"
   ```

   CLI:
   ```bash
   pipefy portal sub-portal publish <MAIN_PORTAL_UUID> <FORMS_ELEMENT_ID> <SUB_PORTAL_UUID>
   ```

6. **Verify publish state**

   MCP:
   ```
   get_portal portal_uuid="<MAIN_PORTAL_UUID>"
   ```

   Success: target **`subPortals[].published`** is **`true`**. End users can see the sub-portal only after this (and hub visibility rules).

7. **Optional — make the main hub public**

   MCP:
   ```
   update_portal portal_uuid="<MAIN_PORTAL_UUID>" visibility="public"
   ```

   CLI:
   ```bash
   pipefy portal update <MAIN_PORTAL_UUID> --visibility public
   ```

---

## Steps — pages, layout, and safe edits

Use a **disposable page** for element/layout experiments on a shared org main portal:

1. **`create_portal_page`** with a unique title (e.g. `Agent smoke 2026-06-01`).
2. Run **`create_portal_element`**, **`update_portal_element`**, **`duplicate_portal_element`**, **`update_portal_page_layout`** on that page only.
3. **`delete_portal_page`** with MCP two-step (`confirmation_token` from the preview, then `confirm=true`), or CLI **`--yes`**.

**`duplicate_portal_element`:** `element_id`, `portal_uuid`, and `page_id` must refer to the **same page** that already contains the source element (duplicate on the same page, not cross-page).

**`update_portal_page_layout`:** read `layout` from **`get_portal`** for that page and send the full array back with intentional edits. Never invent `{ "rows": [ ... ] }` stubs.

**`sort_portal_pages`:** pass a non-empty `page_ids` list with no duplicates. If the raw response exposes nested `success: false`, treat the operation as failed even when the MCP envelope looks ambiguous.

**Link element metadata (create/update, full replace):**

```json
{
  "gridMap": { "height": 64, "columns": 4, "minColumns": 4 },
  "linkUrl": "https://example.com",
  "linkName": "Example link"
}
```

---

## Two-step destructive deletes

MCP deletes (`delete_portal`, `delete_portal_page`, `delete_portal_element`, `delete_sub_portal`, `delete_sub_portal_element`) return a preview with `confirmation_token`. Echo that token with `confirm=true` on the second call. CLI uses `--yes`. `unpublish_sub_portal` is not gated.

---

## Steps — unpublish or remove sub-portal

**Unpublish** (keeps sub-portal entity; visitors lose access):

MCP:
```
unpublish_sub_portal portal_uuid="<MAIN_PORTAL_UUID>" element_id="<FORMS_ELEMENT_ID>"
```

CLI:
```bash
pipefy portal sub-portal unpublish <MAIN_PORTAL_UUID> <FORMS_ELEMENT_ID>
```

**Detach** element wiring (destructive: MCP two-step with `confirmation_token`, `--yes` on CLI):

MCP:
```
delete_sub_portal_element portal_uuid="<MAIN_PORTAL_UUID>" element_id="<FORMS_ELEMENT_ID>" confirm=false
```
Then after approval, echo the preview's `confirmation_token`:

```
delete_sub_portal_element portal_uuid="<MAIN_PORTAL_UUID>" element_id="<FORMS_ELEMENT_ID>" confirm=true confirmation_token="<token from preview>"
```

CLI:
```bash
pipefy portal sub-portal detach <MAIN_PORTAL_UUID> <FORMS_ELEMENT_ID> --yes
```

**Delete sub-portal interface** (irreversible):

MCP two-step `delete_sub_portal` (echo `confirmation_token`) / CLI:
```bash
pipefy portal sub-portal delete <SUB_PORTAL_UUID> --yes
```

---

## MCP response shape

- Read tools return `{ success: true, data: { ... } }` when `PIPEFY_MCP_UNIFIED_ENVELOPE` is enabled (default). Parse **`data`** for `portals`, `pages`, `subPortals`, etc.
- GraphQL/transport failures → `{ success: false, error: { message: "..." } }` — do not treat transport errors as success.
- **`PERMISSION_DENIED`** on portal tools usually names **`create_portal`** or **`manage_portals`**. Re-check org id, token, and SA **`joinAsAdmin`** (see [Confirm access](#confirm-access-before-writes)).
- Only **`PERMISSION_DENIED`** is rewritten to the portal permission hint; other GraphQL codes surface as generic errors with the API message.
- Destructive deletes: default **`confirm=false`** returns a preview (`requires_confirmation: true`, `confirmation_token`); call again with **`confirm=true`** and that token only after explicit human approval.

CLI `--json` prints the raw SDK payload (no `success` wrapper).

---

## Success criteria

- `list_portals` returns the org main portal (typically one row); `create_portal` returns the same UUID on repeat.
- `get_portal` shows expected `pages` / `elements` after writes.
- After **`create_sub_portal`**, sub-portal exists in API but **`published: false`** until publish.
- After publish: **`subPortals[].published`** is `true` and the main page shows the wired **`forms`** slot.
- After unpublish: **`published`** is `false` without deleting the sub-portal entity (unless you called `delete_sub_portal`).
- After layout/element edits on a disposable page, main portal pages used in production still open in the builder (no HTTP 500).

---

## Failure modes

| Symptom | Likely cause | Recovery |
|---------|----------------|----------|
| `PERMISSION_DENIED` on writes | Wrong org, missing `manage_portals`, or SA not joined on interface | Same org as `list_portals`; user runs portal admin join; try human admin token |
| Reads OK, writes fail on `admin` org | Token is human on org A, numeric id is org B | Align `organization_uuid` with token membership |
| `Menu already created` on `create_portal` | Main deleted but org menu state remains | Delete orphan sub-portals; avoid raw `createInterface`; bootstrap with `create_portal_page` on existing UUID |
| Main page empty in builder | Portal created outside `create_portal` template path | `create_portal_page` (title only) for templated elements |
| `published` missing on list | Expected | `get_portal` |
| Many subs in `get_portal`, empty main UI | Sub-portals not published to `forms` slots | `publish_sub_portal` per sub + `forms` `element_id` |
| Publish no effect | Wrong element type or skipped internal_api wire | `get_portal` → `forms` element → `publish_sub_portal` |
| `subPortals[]` empty but UI shows tile | Linked under `pages[].elements` | Inspect `type: subPortal` in `elements[]` |
| `create_portal_element` opaque / 500 | Interfaces instability on some orgs | `duplicate_portal_element` from existing widget on same page |
| Portal viewer HTTP 500 | Orphan `layout` children or wrong layout shape | Copy/fix layout from `get_portal`; delete disposable smoke page |
| Nested `success: false` | API rejected mutation | Read `error.message`; do not assume top-level success |
| Validation on element | Wrong metadata keys or partial update | Full metadata blob; `linkName` / `name` per type |

---

## See also

- [`docs/mcp/tools/portal.md`](../../../docs/mcp/tools/portal.md) — endpoints, wire naming, maintainer introspection
- [`skills/introspection/pipefy-introspection/SKILL.md`](../../introspection/pipefy-introspection/SKILL.md) — verify Interfaces / internal_api mutations before changing tools
