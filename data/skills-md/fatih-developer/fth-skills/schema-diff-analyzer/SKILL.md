---
name: schema-diff-analyzer
description: Detects schema differences between environments (dev vs staging vs prod). Generates actionable migration paths instead of just diff lists.
---

# Schema Diff Analyzer Protocol

This skill takes two schema definitions (Source vs Target, or Environment A vs Environment B) and calculates the correct, safe delta between them. It doesn't blindly apply changes; it evaluates risk.

**Core assumption:** Applying standard ORM or CLI diff outputs directly to production often creates dangerous lock conditions.

---

## 1. Diff Extraction & Categorization
Analyze the two inputs. Group identified changes into three core risk categories:

### 🟢 Safe (Low Risk)
- Adding new tables.
- Adding new nullable columns.
- Adding non-unique indexes (with `CREATE INDEX CONCURRENTLY`).
- Adding new views (if they don't break existing dependencies).

### 🟡 Warning (Medium Risk)
- Modifying column types (e.g., `VARCHAR(50)` to `VARCHAR(100)`).
- Adding missing constraints or foreign keys.
- Dropping unused tables.

### 🔴 Dangerous (High Risk / Blocking)
- Dropping columns or tables actively used.
- Renaming columns or tables (requires Expand-Contract).
- Modifying a column to make it `NOT NULL` without default.
- Adding a `DEFAULT` to a huge table (depends on DB dialect).

## 2. Sync Plan Generation
Do not provide a single monolith transaction if dangerous changes exist. Organize changes logically.

**Required Outputs (Must write BOTH to `docs/database-report/`):**

1. **Human-Readable Markdown (`docs/database-report/schema-diff-report.md`)**
```markdown
## ⚠️ Risk Assessment
- **Safe:** Added table `audit_logs`.
- **Dangerous:** Renamed `customer_id` to `client_id` in `orders` table.

## 🛠️ Sync Execution Plan
Rather than running `prisma db push` or raw alters directly, follow this safe order:

**PHASE 1: (Pre-deployment Safe Alters)**
```sql
CREATE TABLE audit_logs (...);
ALTER TABLE orders ADD COLUMN client_id UUID;
```

*(Delegate to `migration-strategist` for the backfill of `client_id` vs `customer_id`)*

**PHASE 2: (Post-deployment Cleanup)**
```sql
ALTER TABLE orders DROP COLUMN customer_id;
```
```

2. **Machine-Readable JSON (`docs/database-report/schema-diff-output.json`)**
```json
{
  "skill": "schema-diff-analyzer",
  "overall_risk_level": "High",
  "changes": [
    {"type": "Safe", "entity": "audit_logs", "action": "CREATE TABLE"},
    {"type": "Dangerous", "entity": "orders", "action": "RENAME COLUMN", "details": "customer_id to client_id"}
  ],
  "recommended_phases": ["Phase 1 (Safe Alters)", "Backfill", "Phase 2 (Cleanup)"]
}
```

## 3. Tool Handoff
If the diff contains a "🔴 Dangerous" change, explicitly state that the user should engage the `migration-strategist` skill for that specific field to prevent downtime.

---

## Guardrails
- **Data Truncation Warnings:** Always explicitly flag operations where limits are reduced (e.g., `255` down to `50`).
- **Dialect Specific Locks:** Recognize that PostgreSQL 11+ handles `ADD COLUMN ... DEFAULT` instantly, whereas older engines rewrite the table.
- **Dependency Graphs:** Ensure dropping a table or column safely accounts for related views, sequences, or triggers.
