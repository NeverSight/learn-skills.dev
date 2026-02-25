---
name: database-migrations
description: SQLite database migration patterns for SpecFlux. Use when creating new tables, modifying schema, adding indexes, or running migrations. Ensures reversible migrations with UP and DOWN sections.
---

# Database Migration Patterns

## Migration Files

Keep migrations simple and atomic:

```sql
-- migrations/003_add_notifications.sql
-- UP
CREATE TABLE notifications (
  id INTEGER PRIMARY KEY,
  project_id INTEGER NOT NULL,
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  message TEXT,
  task_id INTEGER,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES projects(id),
  FOREIGN KEY (task_id) REFERENCES tasks(id)
);

CREATE INDEX idx_notifications_project_id ON notifications(project_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);

-- DOWN
DROP INDEX IF EXISTS idx_notifications_is_read;
DROP INDEX IF EXISTS idx_notifications_project_id;
DROP TABLE notifications;
```

## Migration Runner

```typescript
// src/db/migrate.ts
import Database from 'better-sqlite3';
import fs from 'fs';
import path from 'path';

export async function runMigrations(db: Database.Database) {
  // Create migrations table
  db.exec(`
    CREATE TABLE IF NOT EXISTS migrations (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL UNIQUE,
      applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Get applied migrations
  const applied = db.prepare('SELECT name FROM migrations').all() as { name: string }[];
  const appliedNames = new Set(applied.map(m => m.name));

  // Read migration files
  const migrationsDir = path.join(__dirname, '../../migrations');
  const files = fs.readdirSync(migrationsDir).filter(f => f.endsWith('.sql')).sort();

  // Apply pending migrations
  for (const file of files) {
    if (appliedNames.has(file)) continue;

    console.log(`Applying migration: ${file}`);
    const sql = fs.readFileSync(path.join(migrationsDir, file), 'utf-8');
    const upSQL = sql.split('-- DOWN')[0].replace('-- UP', '').trim();

    db.exec(upSQL);
    db.prepare('INSERT INTO migrations (name) VALUES (?)').run(file);
  }
}
```

## Testing Migrations

Always test UP and DOWN:

```bash
# Test UP
npm run migrate

# Test DOWN (rollback)
npm run migrate:rollback

# Test UP again
npm run migrate
```
