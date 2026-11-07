---
name: appsmith
description: >-
  Appsmith is an open-source low-code platform for building internal tools, admin panels, and dashboards. Use when a user asks to create CRUD interfaces, connect to databases or APIs with drag-and-drop widgets, write JSObjects for business logic, or self-host Appsmith with Docker or Kubernetes.
license: Apache-2.0
compatibility: "Self-hosting: Docker 20.10.7+ and about 8 GB RAM, or Kubernetes 1.33+ with Helm 3.14+. Appsmith Cloud needs only a browser."
metadata:
  author: terminal-skills
  version: "1.1.0"
  category: development
  repository: https://github.com/appsmithorg/appsmith
  tags: "internal-tools, low-code, open-source, admin-panel, self-hosted"
---
# Appsmith — Open-Source Internal Tool Builder

## Overview

Appsmith is an open-source low-code platform for internal tools: widgets are dragged onto a canvas, queries talk to databases and APIs, and JavaScript (`{{ }}` bindings and JSObjects) ties them together. It runs on Appsmith Cloud or self-hosted as a single container that bundles the server, MongoDB, Redis and PostgreSQL. Two images exist: `appsmith-ce` (Community, Apache-2.0) and `appsmith-ee` (Commercial edition with a free plan; Business and Enterprise features unlock with a license key). This skill reflects Appsmith v2.4 (September 2026).

## Instructions

### Data Queries

```sql
-- OrdersQuery (PostgreSQL). Bindings read widget values; with prepared statements on, each one is a parameter.
-- Never put a binding inside a SQL comment: it is still counted as a parameter.
SELECT * FROM orders
WHERE status = {{ StatusSelect.selectedOptionValue }}
  AND created_at BETWEEN {{ FromDate.selectedDate }} AND {{ ToDate.selectedDate }}
  AND ({{ SearchInput.text }} = '' OR customer_email ILIKE '%' || {{ SearchInput.text }} || '%')
ORDER BY created_at DESC
LIMIT {{ OrdersTable.pageSize }} OFFSET {{ OrdersTable.pageOffset }}

-- UpdateOrderQuery: values passed at call time arrive as this.params
UPDATE orders SET status = {{ this.params.status }} WHERE id = {{ this.params.orderId }}
```

```
UpdatePlanAPI (REST API datasource; auth headers live in the datasource)
PUT https://api.northwind.io/users/{{ UsersTable.selectedRow.id }}
Body: { "plan": {{ PlanSelect.selectedOptionValue }}, "note": {{ NoteInput.text }} }
```

Widget properties used most: Table `selectedRow`, `pageNo`, `pageSize`, `pageOffset`, `searchText`; Select `selectedOptionValue`; Input `text`; DatePicker `selectedDate`. For server-side pagination turn on the table's **Server side pagination** and run the query from **onPageChange**.

Each query has a **Run behavior** in its settings: *Manual* (only `.run()` or a widget event), *On page load*, or *Automatic* (re-runs whenever a bound value changes). Do not combine Automatic with an event handler that also calls `.run()` — the query executes twice. Other settings there: **Use Prepared Statements** (on by default), **Request confirmation before running**, and **Query timeout** (default 10 000 ms, maximum 60 000 ms).

### JavaScript Objects (JSObjects)

```javascript
// JSObject "Refunds" — reusable business logic
export default {
  // Transform query data for charts (Lodash `_` and `moment` are built in)
  getRevenueByMonth() {
    return OrdersQuery.data.reduce((acc, order) => {
      const month = moment(order.created_at).format("YYYY-MM");
      acc[month] = (acc[month] || 0) + order.amount;
      return acc;
    }, {});
  },

  // Multi-step action, run from the Confirm button inside ConfirmRefundModal
  async processRefund() {
    const order = OrdersTable.selectedRow;       // {} when nothing is selected
    if (!order.id) {
      showAlert("Select an order first", "warning");
      return;
    }
    try {
      await StripeRefundAPI.run({ chargeId: order.stripe_charge_id });        // {{ this.params.chargeId }}
      await UpdateOrderQuery.run({ orderId: order.id, status: "refunded" });
      await SlackNotifyAPI.run({ message: `Refund processed for order #${order.id} ($${order.amount})` });
      showAlert("Refund processed successfully", "success");
      await OrdersQuery.run();                   // refresh the table
    } catch (error) {
      showAlert(`Refund failed: ${error.message}`, "error");
    } finally {
      closeModal(ConfirmRefundModal.name);
    }
  },

  // Form validation
  validateForm() {
    const errors = {};
    if (!EmailInput.text?.includes("@")) errors.email = "Invalid email";
    if (Number(AmountInput.text) <= 0) errors.amount = "Amount must be positive";
    if (!ReasonSelect.selectedOptionValue) errors.reason = "Select a reason";
    return errors;
  },
};
```

Framework functions: `Query.run(params)` returns a promise with the response; `showAlert(message, type)` shows a 5-second toast (`info`, `success`, `warning`, `error`); `showModal(Modal.name)` and `closeModal(Modal.name)` open and close a Modal widget; `storeValue(key, value, persist)` writes to `appsmith.store`. `showModal` only opens the modal — it does not wait for an answer, so put the confirmed action on a button inside the modal (or use the query's confirmation setting).

### Deployment

```yaml
# ~/appsmith/docker-compose.yml — pin a release tag from github.com/appsmithorg/appsmith/releases
services:
  appsmith:
    image: index.docker.io/appsmith/appsmith-ee:v2.4.3   # or appsmith/appsmith-ce:v2.4.3
    container_name: appsmith
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./stacks:/appsmith-stacks
    restart: unless-stopped
```

```bash
docker compose up -d               # first start takes up to 5 minutes; then open http://localhost
docker compose exec -it appsmith appsmithctl backup     # encrypted archive in ./stacks/data/backup/
# settings: edit ./stacks/configuration/docker.env, then
docker compose restart appsmith

# Kubernetes with Helm (Commercial edition chart; the Community chart is at https://helm.appsmith.com)
helm repo add appsmith-ee https://helm-ee.appsmith.com && helm repo update
helm install appsmith-ee appsmith-ee/appsmith -n appsmith-ee --create-namespace -f values.yaml
kubectl get pods -n appsmith-ee
```

`values.yaml` must set `image.tag` and the ingress `className` and host; the Kubernetes guide also sets `mongodb.enabled: false` and enables `mongodbCommunity` and `mongodbOperator`, replacing the legacy Bitnami MongoDB subchart.

### Git Sync

1. Open the app and click **Connect Git** at the bottom left of the editor. Only SSH remotes work (HTTPS Git URLs are not supported), and the target repository must be empty.
2. Paste the SSH URL, generate a key (ECDSA 256 or RSA 4096), and add it to the repository as a deploy key **with write access**.
3. Work on a feature branch, commit and push from Appsmith, open a pull request, merge, then pull in Appsmith and deploy.

Branch protection, a per-instance default branch and automatic pull-and-deploy after a merge (a deploy URL called by CI with a bearer token) are Enterprise features in Git settings; without them someone pulls the branch in Appsmith by hand.

## Examples

### Example 1: Self-host Appsmith for a team

User: "Set up Appsmith on our Ubuntu server with Docker and make sure we can back it up."

```bash
mkdir -p ~/appsmith && cd ~/appsmith
# write the docker-compose.yml shown above with image tag v2.4.3
docker compose up -d
docker compose ps                  # the appsmith container should be listed as running
until curl -fsS http://localhost/api/v1/health >/dev/null; do sleep 10; done   # server is up (up to 5 minutes)
docker compose exec -it appsmith appsmithctl backup
ls stacks/data/backup/             # appsmith-backup-*.tar.gz.enc
```

After a few minutes the server's address (`http://localhost` on the same machine) shows the setup page where the first visitor creates the administrator account, so open it right away. The backup prompts for a password and cannot be restored without it. To set a custom domain or disable telemetry, edit `stacks/configuration/docker.env` (`APPSMITH_CUSTOM_DOMAIN`, `APPSMITH_DISABLE_TELEMETRY=true`) and restart.

### Example 2: Orders admin panel with a guarded refund

User: "Build an orders page: filter by status, search by email, and let support refund the selected order after confirming."

1. Add the filter widgets `StatusSelect`, `FromDate`, `ToDate` and `SearchInput`, then a Table `OrdersTable` with data `{{ OrdersQuery.data }}` and server-side pagination on.
2. Add a PostgreSQL datasource and create `OrdersQuery` and `UpdateOrderQuery` from the Data Queries section. Set `OrdersQuery` to Automatic so it re-runs when a filter or the table page changes — do not also call it from onPageChange. Create the REST queries `StripeRefundAPI` and `SlackNotifyAPI` (reading `{{ this.params.chargeId }}` and `{{ this.params.message }}`) and the `Refunds` JSObject from above.
3. Add a "Refund" button with onClick `{{ showModal(ConfirmRefundModal.name) }}` and Disabled `{{ !OrdersTable.selectedRow.id || OrdersTable.selectedRow.status === 'refunded' }}`.
4. Add a Modal named `ConfirmRefundModal` and set its Confirm button's onClick to `{{ Refunds.processRefund() }}`.

Selecting order 4812 and confirming runs the three queries in order, shows the toast "Refund processed successfully", reloads the table with the row's status now `refunded` and closes the modal. If Stripe rejects the refund, the toast reads "Refund failed: …", the order is not updated and the modal closes.

## Guidelines

1. **Pin the image tag** — without a tag Docker pulls `latest` and a container recreate becomes an unplanned upgrade.
2. **Upgrade through the checkpoint** — an instance older than v1.96 must first be upgraded to a v1.96–v1.99 release before moving to v2.x (v2 bundles MongoDB 7); instances older than v1.9.2 have an earlier checkpoint. Run `appsmithctl backup` first.
3. **Keep prepared statements on** — they are the SQL-injection defence. A binding is then a value, not SQL text, so it cannot supply a table or column name; build patterns with `'%' || {{ SearchInput.text }} || '%'`.
4. **JSObjects for logic** — keep multi-step logic in JSObjects rather than long inline `{{ }}` handlers; use `async/await` with `try/catch` so a failed query stops the chain.
5. **`selectedRow` is never null** — it is `{}` when nothing is selected, so test a field (`selectedRow.id`), not the object.
6. **Mind the 10-second query timeout** — raise it per query (up to 60 s); self-hosted instances can lift that 60 s ceiling with `APPSMITH_SERVER_TIMEOUT` (in seconds). Move longer work out of the request.
7. **Credentials stay in datasources** — never paste API keys into queries or JSObjects, where every app editor (and the Git repository) can read them.
8. **Paid features** — multiple datasource environments, granular access control, audit logs, reusable Packages and Workflows need the Business plan; Git CI/CD needs Enterprise; the MCP server (beta) is for Business Cloud and self-hosted Enterprise.
9. **Appsmith AI is gone** — the Appsmith AI datasource reached end of life on September 30, 2026; use an OpenAI, Anthropic or Google AI datasource instead.
10. **Network needs** — self-hosted instances call `cs.appsmith.com`; allow it in outbound firewall rules.
