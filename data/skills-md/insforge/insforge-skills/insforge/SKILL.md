---
name: insforge
description: >-
  Use this skill whenever writing frontend code that talks to a backend for database queries, authentication, file uploads, AI features, real-time messaging, or edge function calls — especially if the project uses InsForge or @insforge/sdk. Trigger on any of these contexts: querying/inserting/updating/deleting database rows from frontend code, adding login/signup/OAuth/password-reset flows, uploading or downloading files to storage, invoking serverless functions, calling AI chat completions or image generation, subscribing to real-time WebSocket channels, or writing RLS policies. If the user asks for these features generically (e.g., "add auth to my React app", "fetch data from my database", "upload files") and you're unsure whether they use InsForge, consult this skill and ask. For backend infrastructure (creating tables via SQL, deploying functions, CLI commands), use insforge-cli instead.
license: MIT
metadata:
  author: insforge
  version: "1.1.0"
  organization: InsForge
  date: February 2026
---

# InsForge SDK Skill

This skill covers **client-side SDK integration** using `@insforge/sdk`. For backend infrastructure operations (creating tables, inspecting schema, deploying functions, secrets, managing storage buckets, website deployments, cron job and schedules, logs, etc.), use the **insforge-cli** skill.

## Quick Setup

```bash
npm install @insforge/sdk@latest
```

```javascript
import { createClient } from '@insforge/sdk'

const insforge = createClient({
  baseUrl: 'https://your-project.region.insforge.app',
  anonKey: 'your-anon-key'
})
```

## Module Reference

| Module | SDK Integration |
|--------|-----------------|
| **Database** | [database/sdk-integration.md](database/sdk-integration.md) |
| **Auth** | [auth/sdk-integration.md](auth/sdk-integration.md) |
| **Storage** | [storage/sdk-integration.md](storage/sdk-integration.md) |
| **Functions** | [functions/sdk-integration.md](functions/sdk-integration.md) |
| **AI** | [ai/sdk-integration.md](ai/sdk-integration.md) |
| **Real-time** | [realtime/sdk-integration.md](realtime/sdk-integration.md) |

### What Each Module Covers

| Module | Content |
|--------|---------|
| **Database** | CRUD operations, filters, pagination, RPC calls |
| **Auth** | Sign up/in, OAuth, sessions, profiles, password reset |
| **Storage** | Upload, download, delete files |
| **Functions** | Invoke edge functions |
| **AI** | Chat completions, image generation, embeddings |
| **Real-time** | Connect, subscribe, publish events |

### Guides

| Guide | When to Use |
|-------|-------------|
| [database/postgres-rls.md](database/postgres-rls.md) | Writing or reviewing RLS policies — covers infinite recursion prevention, `SECURITY DEFINER` patterns, performance tips, and common InsForge RLS patterns |

### Real-time Configuration

For real-time channels and database triggers, use `insforge db query` with SQL to create triggers that publish to channels. The real-time SDK is for frontend event handling and messaging, not backend configuration.

#### Create Database Triggers

Automatically publish events when database records change.

```sql
-- Create trigger function
CREATE OR REPLACE FUNCTION notify_order_changes()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM realtime.publish(
    'order:' || NEW.id::text,    -- channel
    TG_OP || '_order',           -- event: INSERT_order, UPDATE_order
    jsonb_build_object(
      'id', NEW.id,
      'status', NEW.status,
      'total', NEW.total
    )
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Attach to table
CREATE TRIGGER order_realtime
  AFTER INSERT OR UPDATE ON orders
  FOR EACH ROW
  EXECUTE FUNCTION notify_order_changes();
```

#### Conditional Trigger (Status Changes Only)

```sql
CREATE OR REPLACE FUNCTION notify_order_status()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM realtime.publish(
    'order:' || NEW.id::text,
    'status_changed',
    jsonb_build_object('id', NEW.id, 'status', NEW.status)
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER order_status_trigger
  AFTER UPDATE ON orders
  FOR EACH ROW
  WHEN (OLD.status IS DISTINCT FROM NEW.status)
  EXECUTE FUNCTION notify_order_status();
```

#### Access Control (RLS)

RLS is disabled by default. To restrict channel access:

- **Enable RLS**

```sql
ALTER TABLE realtime.channels ENABLE ROW LEVEL SECURITY;
ALTER TABLE realtime.messages ENABLE ROW LEVEL SECURITY;
```

- **Restrict Subscribe (SELECT on channels)**

```sql
CREATE POLICY "users_subscribe_own_orders"
ON realtime.channels FOR SELECT
TO authenticated
USING (
  pattern = 'order:%'
  AND EXISTS (
    SELECT 1 FROM orders
    WHERE id = NULLIF(split_part(realtime.channel_name(), ':', 2), '')::uuid
      AND user_id = auth.uid()
  )
);
```

- **Restrict Publish (INSERT on messages)**

```sql
CREATE POLICY "members_publish_chat"
ON realtime.messages FOR INSERT
TO authenticated
WITH CHECK (
  channel_name LIKE 'chat:%'
  AND EXISTS (
    SELECT 1 FROM chat_members
    WHERE room_id = NULLIF(split_part(channel_name, ':', 2), '')::uuid
      AND user_id = auth.uid()
  )
);
```

- **Quick Reference**

| Task | SQL |
|------|-----|
| Create channel | `INSERT INTO realtime.channels (pattern, description, enabled) VALUES (...)` |
| Create trigger | `CREATE TRIGGER ... EXECUTE FUNCTION ...` |
| Publish from SQL | `PERFORM realtime.publish(channel, event, payload)` |
| Enable RLS | `ALTER TABLE realtime.channels ENABLE ROW LEVEL SECURITY` |


#### Best Practices

1. **Create channel patterns first** before subscribing from frontend
   - Insert channel patterns into `realtime.channels` table
   - Ensure `enabled` is set to `true`

2. **Use specific channel patterns**
   - Use wildcard `%` patterns for dynamic channels (e.g., `order:%` for `order:123`)
   - Use exact patterns for global channels (e.g., `notifications`)

#### Common Mistakes

| Mistake | Solution |
|---------|----------|
| Subscribing to undefined channel pattern | Create channel pattern in `realtime.channels` first |
| Channel not receiving messages | Ensure channel `enabled` is `true` |
| Publishing without trigger | Create database trigger to auto-publish on changes |

#### Recommended Workflow

```text
1. Create channel patterns   → INSERT INTO realtime.channels
2. Ensure enabled = true     → Set enabled to true
3. Create triggers if needed → Auto-publish on database changes
4. Proceed with SDK subscribe → Use channel name matching pattern
```

### Backend Configuration (Not Yet in CLI)

These modules still require HTTP API calls because the CLI does not yet support them:

| Module | Backend Configuration |
|--------|----------------------|
| **Auth** | [auth/backend-configuration.md](auth/backend-configuration.md) |
| **AI** | [ai/backend-configuration.md](ai/backend-configuration.md) |

## SDK Quick Reference

All SDK methods return `{ data, error }`.

| Module | Methods |
|--------|---------|
| `insforge.database` | `.from().select()`, `.insert()`, `.update()`, `.delete()`, `.rpc()` |
| `insforge.auth` | `.signUp()`, `.signInWithPassword()`, `.signInWithOAuth()`, `.signOut()`, `.getCurrentSession()` |
| `insforge.storage` | `.from().upload()`, `.uploadAuto()`, `.download()`, `.remove()` |
| `insforge.functions` | `.invoke()` |
| `insforge.ai` | `.chat.completions.create()`, `.images.generate()`, `.embeddings.create()` |
| `insforge.realtime` | `.connect()`, `.subscribe()`, `.publish()`, `.on()`, `.disconnect()` |

## Important Notes

- **Database inserts require array format**: `insert([{...}])` not `insert({...})`
- **Storage**: Save both `url` AND `key` to database for download/delete operations
- **Functions invoke URL**: `/functions/{slug}` (without `/api` prefix)
- **Use Tailwind CSS v3.4** (do not upgrade to v4)
- **Always local build before deploy**: Prevents wasted build resources and faster debugging
