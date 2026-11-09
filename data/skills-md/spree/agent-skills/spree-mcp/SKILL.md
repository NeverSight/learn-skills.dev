---
name: spree-mcp
description: Use when connecting an AI client to a Spree 6 store's Admin MCP server, operating a store through its tools, or adding agent tools. Covers `/api/v3/admin/mcp` (`spree_mcp`), OAuth sign-in and consent (secret keys are refused), the generic tools (`describe_resource`, `search_resources`, `create_resource`/`update_resource`, `query_report`, `curate_products`, `set_stock`, imports, exports), action tools generated from every documented Admin API action, `parent_id`, and custom tools — a documented admin endpoint becomes a tool with no registration (`agent_tool false, reason:`, the contract spec), or a hand-written `Spree::AgentTool` in `Spree.admin_agent_tools`. Common phrasings include "Spree MCP", "admin MCP", "connect Claude to my store", "custom MCP tool", "agent tools", "expose my endpoint to agents", "Spree::AgentTool", "why can't the agent see this tool". Not the docs MCP server (`spree-docs`).
---

# Spree Admin MCP

Spree 6 stores host an MCP server for the back office at:

```text
https://your-store.com/api/v3/admin/mcp
```

It ships in the `spree_mcp` gem, which new projects already have (`spree add mcp` adds it to an older one). There's nothing to deploy or configure.

It's one adapter over a tool registry in `spree_core` (`Spree.admin_agent_tools`). The dashboard's AI assistant reads the same registry, so a tool you add reaches both.

Two separate MCP servers have "Spree" in the name:

| Server | URL | What it does |
|---|---|---|
| **Admin MCP** (this skill) | `https://<store>/api/v3/admin/mcp` | Runs a real store: catalog, orders, reports, settings |
| **Docs MCP** (`spree-docs`) | `https://spreecommerce.org/docs/mcp` | Searches Spree documentation while you write code |

For scheduled or automatic work (nightly syncs, pipelines, storefronts), use the Admin API, the SDK or `spree api` instead of MCP (see `spree-api-v3`, `spree-typescript-sdk`, `spree-cli`).

## Connecting a client

The endpoint accepts **only an OAuth token issued to a person**. A secret API key (`sk_…`) is refused on purpose: an agent acts for a staff member and carries that person's permissions, narrowed to what they approved. Integrations that can't sign in use a secret key against the Admin API instead.

1. Register the client once under **Settings → OAuth clients**. Registering grants nothing by itself.
2. Each staff member connects for themselves. They sign in to the store and tick permissions on a consent screen.

**Claude Code.** Go to **Settings → AI Agents → Connect an agent → Claude**. The dashboard shows a command with the client ID filled in:

```bash
claude mcp add --transport http --client-id <client-id> --callback-port 3118 \
  spree https://your-store.com/api/v3/admin/mcp
```

Keep `--callback-port 3118`. The store only accepts the exact callback port it registered.

**Other clients:**

- Claude Desktop / claude.ai: **Settings → Connectors → Add custom connector**, then paste the URL and the client ID from **Settings → OAuth clients**.
- Cursor: add `{ "mcpServers": { "spree": { "url": "…/api/v3/admin/mcp" } } }` to `.cursor/mcp.json`.
- VS Code: add `{ "servers": { "spree": { "type": "http", "url": "…" } } }` to `.vscode/mcp.json`.

### What a connection can do

- **Consent can't exceed the person's own permissions.** Scopes the person doesn't hold are dropped. The grant is frozen at approval time, so a later promotion doesn't widen it.
- **Two checks apply.** The approved permissions decide which tools are *offered*; a tool the connection can't use isn't listed at all. Each call is then checked again per record and per resource, with the same rules the Admin API applies. For example, a `read_reports` grant can run a report, but a dimension that exposes customers also needs `read_customers`.
- **Some things are never offered.** API keys, integrations, webhooks, roles, staff accounts, OAuth clients, gift card and coupon codes (including exports of them), and customer erasure. These would either widen the agent's own access or can't be undone.
- **Revoke access** under **Settings → AI Agents**. Revoking takes effect on the agent's next request.

### Troubleshooting a connection

| Symptom | Cause |
|---|---|
| Client says authorization is needed, then nothing happens | The store's configured URL differs from the one the browser reaches (a proxy or tunnel). OAuth discovery has to return an address the browser can open. |
| "I have no tool for that" | The permission wasn't approved. Revoke and reconnect, ticking it this time. |
| Tool is listed but returns a permission error | The record-level check refused. For reports, the dimension needs another `read_*`. A staff member limited to one seller's products is limited the same way through MCP. |
| 401 with an `sk_` key | Expected. Use OAuth, or call the Admin API with the key. |
| "Unknown permission key" raised in development | A custom tool declares a `permission` that was never registered with `Spree.permissions.register_scope`. |

## Using the tools (when you are the agent)

About 100 tools ship: 17 general tools plus one tool per Admin API action. Only the ones the grant allows are listed. The full list is at `https://spreecommerce.org/docs/developer/mcp/tools`.

### Reading

Start with `describe_resource`. With no argument it lists the resources this connection can read. Given a resource, it returns:

- the filterable and sortable fields, and its Ransack scopes (e.g. `out_of_stock`)
- the `expand` options
- the `parent`, for records that live under another record
- the accepted `types` / `nested_types` and their `preferences` schemas
- what each nested list accepts

Then:

- `search_resources` finds records, taking filters, sort and `expand`.
- `get_resource` reads one record. Pass prefixed IDs exactly as search returned them (`or_…`, `prod_…`). Never pass integer IDs.

For numbers (revenue, orders, units, "last month in Germany"), call `describe_reporting` then `query_report`. Don't count search results yourself.

### Writing

| Job | Tool |
|---|---|
| Create, change or delete any of ~38 record kinds | `create_resource`, `update_resource`, `delete_resource` |
| Set which products a category, collection, catalog or price list holds | `curate_products` |
| Set on-hand counts (absolute `count_on_hand` or signed `adjustment`, with a `reason`) | `set_stock` |
| Add an image to a product | `upload_file` → `media_create` with the returned ID |
| Import a CSV | `upload_file` → `propose_import_mapping` / `describe_import_mapping` → `create_import` → `get_import_status` |
| Export | `create_export`, then read the `spree+export://<id>` MCP resource (not the download path) |
| Any other admin action: cancel, approve, capture, refund, clone, receive… | `<resource>_<action>`: `orders_cancel`, `payments_capture`, `returns_refund`, `products_clone`, `products_activate`, `sellers_approve`, … |

Rules for the generic writes:

- **Nested rows travel with their parent.** Variants carry their options, prices and stock levels inside the product write. A product with two sized variants is one `create_resource` call.
- **A list replaces the existing one.** Sending one variant leaves the product with one variant. Send every row you want to keep.
- **Typed rows take a short `type`, never a class name.** Promotion rules and actions, price list rules and payment method providers use names like `item_total`, `create_item_adjustments` or `check`. `describe_resource` lists the accepted kinds and the schema of their `preferences`.
- **Child records go through the parent.** An order's items, discounts and fees, promotion rules and actions, and an order's payments have no search of their own:
  - Pass the parent's ID as `parent_id`, or read the child records with `get_resource` on the parent using `expand: ["<list>"]`.
  - When the parent accepts the rows as a list attribute (a promotion's `rules`/`actions`), write them through that attribute.
- **Every write is confirmed by the client.** Uploads, imports and exports are marked non-destructive (`additive`). Deletes, refunds, cancels and status changes are marked destructive.
- **Errors are instructions.** A refused call returns `{ error: "…" }` naming the fix, such as the accepted types, the parent to use or the missing field. Read it and retry with the fix rather than giving up.

Tool names and argument names from 6.0.0 (`fulfillments_create`, `refunds_create`, `variants_create`, …) still answer through 6.0.x and say what to send instead. New code should use `create_resource`.

## Adding tools

Choose the path by what the capability is:

| The capability is… | Do this |
|---|---|
| An **Admin API action** on your own endpoint (`POST /suppliers/{id}/sync`, `PATCH /quotes/{id}/send`) | Document the endpoint with an rswag spec. It becomes a tool automatically. |
| Plain **CRUD** on your own resource | Document it too. It's reachable through `create_resource`/`update_resource`/`delete_resource`/`search_resources` and gets no tool of its own. |
| **Not an endpoint**: a lookup in another system, a custom calculation | Subclass `Spree::AgentTool` and register it. |
| A workflow you want agents to run | Put an admin endpoint in front of it and document it. `Spree.admin_agent_tools.expose_workflows` is deprecated and does nothing (removed in 7.0). |

### 1. Documented admin endpoints become tools

Every Admin API action documented in OpenAPI, other than create, read, update and delete, becomes an agent tool. You don't register anything. The tool is built from the operation:

| Tool part | Comes from |
|---|---|
| Name | Resource + action: `PATCH /quotes/{id}/send` → `quotes_send`. An `operationId` overrides it. Use one to resolve a name clash, or to make a create that's really an action (receiving stock against a transfer) into its own tool. |
| Description | The operation's summary, then the first paragraph of its description. **The model chooses tools by this text.** Say what the action does and when to use it. |
| Arguments | Path segments (`id`, and a parent such as `order_id`) plus the request body, from `request_body_for`. |
| Permission | The controller's `scoped_resource` write scope. |

The call goes through the endpoint itself, so authentication, the scope check, record-level permissions and the workflow all apply. The agent gets exactly what an API client gets.

**Opting out.** Opt a write out in its spec, and give the reason. Good reasons are irreversible erasure, platform jobs and wizard steps. "Not done yet" isn't a reason.

```ruby
post 'Erase a supplier' do
  agent_tool false, reason: 'Irreversible, and the supplier contract requires a person to confirm.'
end
```

**Opting in a read.** A custom read becomes a tool only if its spec opts in. Most custom reads are type lists, which `describe_resource` already covers, or file downloads.

```ruby
get 'Supplier lead times' do
  agent_tool true
end
```

**Where documents are read from.** Spree merges core's `admin.yaml` with every engine's and the host app's `openapi/admin.yaml` at runtime, and builds tools from the result. Generating and committing that file is the whole change. How to write the specs and run `spree:openapi:generate` is in `spree-resource` (§ Documenting endpoints).

**Endpoints whose records hold credentials** (API keys, webhooks, gift cards) never become tools.

**The contract spec.** `spec/agent_tools_spec.rb` is written by `spree generate spree_dev_tools:openapi`, and new projects come with it. Keep it in the suite. It fails when:

- an admin action has no documented operation,
- an opt-out has no reason,
- two actions derive one tool name (fix with an `operationId`),
- an action derives the name of a hand-written tool,
- an extension's document conflicts with core's.

```ruby
require 'spree/api/testing_support/agent_tools_contract'

RSpec.describe 'agent tools' do
  it_behaves_like 'an engine whose admin writes are agent tools', MyExtension::Engine  # or Rails.application
end
```

### 2. A hand-written `Spree::AgentTool`

Use this only for something that isn't an endpoint.

```ruby
# app/tools/my_shop/agent_tools/supplier_stock.rb
module MyShop
  module AgentTools
    class SupplierStock < Spree::AgentTool
      tool_name 'supplier_stock'
      description 'Current stock at a supplier, by SKU. Use before raising a purchase order.'
      permission 'read_purchasing'          # a registered permission key; nil = offered to everyone

      param :sku, description: 'The SKU to look up', required: true
      # param :skus, type: :array, items: :string — arrays must say what they hold

      def call(sku:)
        stock = MyShop::SupplierApi.stock_for(sku, store: context.store)
        return { error: "No supplier carries #{sku}. Check the SKU with search_resources on variants." } if stock.nil?

        { summary: "#{sku}: #{stock} available", sku: sku, available: stock }
      end
    end
  end
end
```

```ruby
# config/initializers/spree.rb
Spree.admin_agent_tools << 'MyShop::AgentTools::SupplierStock'
```

**Declaring the tool:**

- `tool_name`, `description`, `permission`, and `param name, type:, description:, required:, items:`. Types are `:string` (the default), `:integer`, `:number`, `:boolean`, `:object` and `:array`.
- **Register by name (a string), not by class.** Edits to the description or params then take effect on the next request without a restart.
- `audience :admin` is the default. Storefront tools use `audience :store` and go in `Spree.store_agent_tools`, which has no client yet. Registering a tool on the wrong surface raises.

**Tools that change data:**

- **Call `mutating!` on any tool that changes data.** Without it, the call runs immediately with no approval card. A mutating tool also defaults to destructive.
- Add `additive!` when the tool only creates and never overwrites, removes or changes state. Clients can then skip the "destructive" warning. `additive!` isn't inherited.
- Override `summary(arguments)` on mutating tools. It's the entire approval card, so write it as an instruction that names the record: "Set Blue Shirt to draft". Don't put IDs or JSON in it.

**Inside `call`:**

- **`context` is the caller.** It has `context.store` (always scope through it), `context.principal` (pass it to workflows as `canceler:`, `approver:` or `created_by:`), and `context.accessible(relation)` to narrow a relation to the records this caller may see.
- **Check each record before changing it.** Holding `write_products` doesn't mean this person may edit *this* product. `return err if (err = unauthorized(:update, product))` refuses with a message the model can read.
- **To run an Admin API endpoint from a tool**, use `Spree::AgentTools::ApiDispatch.new(context).call(method:, path:, body:)`. It repeats the caller's own credential, so the same checks run. See core's `set_stock.rb`.
- **Refuse by returning `{ error: '…' }`, never by raising.** Write the message as the next step to take. When the tool takes a resource key, `unknown_resource(key)` lists the valid ones.
- **Keep results small.** They go into the model's context. Return a `summary` line and the few fields that answer the question.

**Naming.** Hand-written tool names win over generated ones. If you shadow an operation's name, the contract spec fails.

### Testing a custom tool

```ruby
let(:context) { Spree::AgentTools::Context.new(store: store, user: admin_user) }
subject(:tool) { MyShop::AgentTools::SupplierStock.new(context) }

it { expect(tool.call(sku: 'ABC')).to include(available: 4) }
it 'is offered only with read_purchasing' do
  expect(Spree.admin_agent_tools.available_for(context).map(&:tool_name)).to include('supplier_stock')
end
```

## Gotchas

- **Write descriptions for the model.** The operation's summary and description, or the tool's `description`, are how the model picks a tool. Vague text leads to wrong tool choices.
- **An endpoint that isn't a tool** is usually one of these: its spec is missing or not regenerated (`openapi/admin.yaml` not committed), it's plain CRUD, it's a read that didn't opt in, it was opted out, or its controller serves credential records.
- **An extension's gemspec must ship `openapi/*.yaml`.** A `git ls-files` gemspec already does. A hand-listed `s.files` needs `'openapi/*.yaml'` added, or the tools disappear once the gem is installed.
- **A tool with a blank `permission` is offered to everyone.** Gate it per record inside `call`, as the generic tools do.
- The `spree_mcp` gem README still says the endpoint takes a secret key. It doesn't: since 6.0.3 it's OAuth only (`McpController#authenticate_admin!`).

## Where to read further

- Docs: `https://spreecommerce.org/docs/developer/mcp/{overview,quick-start,tools,permissions,custom-tools}` (or the `spree-docs` MCP server)
- Source: `spree/core/lib/spree/agent_tool.rb`, `spree/core/lib/spree/agent_tools/` (registry, context, operation catalog), `spree/core/app/tools/spree/agent_tools/` (built-in tools), `spree/mcp/` (the adapter), `spree/api/lib/spree/api/testing_support/{agent_tools,agent_tools_contract}.rb`
- Related skills: `spree-resource` (documenting endpoints / OpenAPI), `spree-auth-permissions` (permission keys, `register_scope`), `spree-api-v3`, `spree-extensions`, `spree-cli`
