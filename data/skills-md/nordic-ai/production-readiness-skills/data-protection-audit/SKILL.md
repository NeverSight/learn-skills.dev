---
name: data-protection-audit
description: Reviews how data is classified, stored, transmitted, retained, and destroyed. Covers encryption at rest and in transit, PII classification and inventory, retention and deletion policies, data residency, key management, backup integrity, and anonymization / pseudonymization. Use when the user asks about "data protection", "encryption", "PII", "data retention", "key management", "backups", invokes /data-protection-audit, or when the orchestrator delegates. Stack-agnostic, mode-aware, scope-tier-aware.
license: Apache-2.0
metadata:
  version: 0.1.0
  id_prefix: DATA
---

# Data Protection Audit

You review the data lifecycle from ingestion to destruction. You answer: *what data do we have, where does it live, who can reach it, how long does it stick around, and how do we prove any of this*.

This skill overlaps deliberately with `security-audit` (crypto, secrets) and `compliance-check` (GDPR data-subject rights, retention obligations). The orchestrator dedupes cross-skill — focus on data-specific framings here.

## Inputs

From orchestrator: `scope_tier`, `jurisdiction`, `data_sensitivity`, `stack_summary`, `gitnexus_indexed`, and the security + compliance findings.

## Mode detection

- **Plan mode** — report gaps with described remediations.
- **Edit mode** — apply fixes. Encryption at rest changes (enabling TDE, enabling volume encryption) often require migration coordination — require confirmation. Retention cleanup jobs, field-level encryption for new rows, and key rotation automation can often be added safely.

## Thresholds by tier

| Tier | Encryption at rest | Encryption in transit | PII inventory | Retention | Backups |
|---|---|---|---|---|---|
| prototype | advisory | required (TLS for user-facing) | advisory | advisory | basic |
| team | **required** on DB + object storage | **required** everywhere | **required** | **required + enforced programmatically** | **required + tested restore** |
| scalable | **required + customer-managed keys** for regulated data | **required + internal mTLS** for sensitive flows | **required + automated** | **required + auditable** | **required + cross-region + tested** |

## Review surface

### 1. Data classification

**You cannot protect what you haven't classified.**

- Is there a documented classification scheme? e.g. `public / internal / confidential / restricted`.
- Which database columns / object-storage paths / log fields / cache entries fall into each class?
- At scalable tier, classification should be encoded in code: column-level tags (comments, ORM metadata), schema linting rule for new fields, central registry.

Use GitNexus `mcp__gitnexus__query` to enumerate all schema fields if available. Otherwise parse ORM models / SQL migrations / Prisma schema / Drizzle schema / SQLAlchemy models / Hibernate entities / ActiveRecord migrations.

**Check for these often-unclassified PII fields:**
- email, phone, name, address, postcode, IP address, device ID, advertising ID, cookie ID, user-agent with other signals.
- date_of_birth, national_id, passport, driver_license, tax_id, SSN.
- payment_method, card_last_four, bank_account, IBAN.
- health_condition, genetic_data, biometric_template, biometric_hash.
- precise geolocation, travel history.
- religion, political opinion, sexual orientation, trade union membership.
- children's data (especially if younger than jurisdiction-specific age of consent).
- free-form text fields that likely contain PII (user-submitted bio, note, message, support ticket body).

### 2. PII inventory + data flow

- **Data flow diagram**: where does PII enter, where does it live (DB tables, caches, object storage, logs, analytics pipelines, third-party SaaS), where does it leave?
- **Third-party sub-processors**: list every external SaaS that receives user data. Cross-reference compliance-check output.
- **Copies**: dev / staging environments with prod PII? This is a finding unless anonymized.
- **Derived data**: ML feature stores, analytics warehouses, embedding stores — often overlooked.

### 3. Encryption at rest

- **Database**: is disk-level encryption on? (AWS RDS encryption, GCP Cloud SQL encryption, Azure SQL TDE, managed storage encryption). Flag DBs created without encryption at team+ tier.
- **Application-level / field-level encryption** for extra-sensitive fields (health, payment, government IDs). Look for dedicated crypto libraries: `tink`, `age`, `libsodium` / `NaCl`, language wrappers.
- **Object storage** (S3, GCS, Azure Blob): default encryption enabled? Bucket policies enforce server-side encryption? SSE-KMS rather than SSE-S3 at scalable tier for regulated data?
- **Backups**: encrypted? Keys distinct from primary storage keys?
- **Logs**: if logs contain PII (even hashed), the log store must be encrypted with same rigor as primary data.
- **Caches**: Redis / Memcached / in-memory — at-rest encryption of the cache host disk at team+ tier. Field-level if sensitive.
- **Message queues**: Kafka / SQS / Pub/Sub — at-rest encryption of broker storage.
- **Local dev caches**: developers' laptops often accumulate real PII in local SQLite / Redis — flag if prod data syncs to dev.

### 4. Encryption in transit

Cross-references security-audit's transport checks. Data-protection specifics:

- **Internal service-to-service TLS** — at scalable tier, east-west traffic should be mTLS, not just plaintext inside a VPC.
- **Database connections** use TLS with certificate verification (not `sslmode=disable` or `?ssl=false`).
- **Admin / operator access** (psql, SSH, bastion) over encrypted channels only.
- **Backup transfers** over encrypted channels.
- **Exports / data subject access responses** delivered securely (not unencrypted email attachment).
- **Webhooks outbound**: HTTPS enforced, endpoint verification (signing).

### 5. Key management

- **Where are encryption keys stored?** Not in app config. Use: AWS KMS, GCP KMS, Azure Key Vault, HashiCorp Vault, Hashicorp Consul, sealed-secrets, or HSM for scalable tier.
- **Key rotation**:
  - Periodic rotation for data-encryption keys (typically 1y).
  - Automated rotation preferred over manual.
  - Rotation tested? Last rotation date known?
- **Key access control**: who / what can decrypt?
  - Principle of least privilege on key policies.
  - Separation of duties: the engineer who writes the code doesn't have direct decrypt access in prod.
- **Envelope encryption** pattern: data keys encrypted by a master key — avoid bulk-decrypting all data under one compromised key.
- **Customer-managed keys (BYOK / CMK)** offered at scalable tier for enterprise / regulated customers.

### 6. Retention

- **Documented retention per data class / table**:
  - How long kept?
  - Under what lawful basis (GDPR) / business need?
  - How is it deleted?
- **Programmatic enforcement**: scheduled jobs that actually delete expired data. Flag if "retention" is policy-only with no enforcement.
- Look for cleanup jobs / TTLs: `DELETE FROM ... WHERE created_at < ...`, DynamoDB TTL, S3 lifecycle rules, BigQuery partition expiration, Elasticsearch ILM, log retention config.
- **Soft delete vs. hard delete**: user expects "delete my account" to actually delete. If soft-delete, is there a hard-delete sweeper?
- **Backups**: retention of backups containing deleted records. Crypto-shredding (destroying keys) can satisfy this where backup deletion is infeasible.
- **Audit logs**: retained *at least* as long as any compliance obligation, but not indefinitely without cause.

### 7. Right to erasure (overlap with compliance-check)

For each data store, when user exercises erasure:

- Primary DB: row deleted or field-cleared?
- Derived stores: analytics warehouse, feature store, embeddings, ML models trained on user data — handled?
- Logs: tagged with user ID so logs can be deleted or pseudonymized?
- Backups: policy exists; crypto-shredding if immediate deletion impossible.
- Third-party processors: delete request propagated.
- Caches: invalidated.

### 8. Anonymization and pseudonymization

- **Pseudonymization** (reversible with a separate key): check for tokenization / hashing with pepper / reversible encryption where used.
  - Pseudonymization alone is not anonymization under GDPR — still personal data.
- **Anonymization** (irreversible): k-anonymity, l-diversity, differential privacy where analytics on PII is required.
  - "Hashing the email" is not anonymization — easily reversed via rainbow table + dictionary.
- **Dev/staging data**: anonymize or synthesize. Do not copy prod PII into dev.

### 9. Data residency

- Where is each class of data **stored**?
- Where is it **processed** (including transient)?
- Regulatory requirements (e.g. some EU public-sector data must stay in EU)?
- For CDNs / edge functions: do they cache PII outside allowed regions?
- **Sub-processors**: their regions matter too — check their Trust Center / DPA.

### 10. Backups

- **Exist**: how often, what RPO, what RTO?
- **Encrypted**: see §3.
- **Restore tested**: a backup you haven't restored is schrödinger's backup. Flag if restore hasn't been tested in the last 6 months at team+ tier, quarterly at scalable.
- **Off-site / cross-region**: at scalable tier, backups in a different region than primary.
- **Immutable / append-only backups** at scalable tier for ransomware resilience.
- **Retention windows** balance recoverability vs. compliance obligations.

### 11. Access control to data

- **Who has direct DB access in production?** List by role; confirm principle of least privilege.
- **Break-glass procedures** documented; regular access limited to read-only where possible.
- **Query logging** for admin queries on sensitive tables.
- **Just-in-time access** at scalable tier (Teleport, Boundary, CyberArk, Okta JIT).
- **Row-level security** or tenant isolation for multi-tenant apps — check it's enforced at the DB layer, not only in app code.

### 12. Data minimization

For every collected field, can you justify it?
- **Why is this collected?**
- **Who uses it?**
- **How long kept?**

If answers are "we might need it someday", it's over-collection. Trim.

At scalable tier, new fields should require a review gate (schema review, DPIA triggers).

### 13. Data export / portability

- GDPR Art. 20 requires machine-readable export (cross-reference compliance-check).
- Export process:
  - Includes all data, across all stores?
  - Format (JSON, CSV) is reasonably machine-readable?
  - Delivery mechanism is secure (authenticated download link, not plain email)?
  - Rate-limited to prevent enumeration / scraping via repeated export?

### 14. Cross-border transfers

- Any data leaving home jurisdiction?
- Lawful transfer mechanism? (SCCs, adequacy, BCR for EU; APEC CBPR; etc.)
- Transfer impact assessment documented for EU→US after Schrems II (for EU data).

### 15. Telemetry and analytics

- Frontend analytics (GA, Mixpanel, Amplitude, Segment, PostHog): what's collected?
- IP addresses recorded? Masked / truncated?
- Device fingerprinting?
- Consent gate before loading analytics scripts (for EU)?

## Severity classification

| Severity | Meaning |
|---|---|
| critical | Large-scale unencrypted sensitive data. No ability to delete on request. Prod PII in dev. No backups or untested ones for a team+ tier system. |
| high | At-rest encryption missing for PII. No retention enforcement. Keys co-located with data they protect. |
| medium | Field-level encryption missing for sensitive fields. Retention policy exists but only in docs. |
| low | Nice-to-have: customer-managed keys, differential privacy, immutable backups. |
| info | Inventory observations. |

## Output format

```yaml
- id: DATA-<NNN>
  severity: ...
  category: classification | encryption-rest | encryption-transit | keys | retention | erasure | anonymization | residency | backups | access | minimization | portability | transfers | telemetry
  title: ...
  location: <file or system-level>
  description: |
    <what, why, realistic exposure scenario>
  evidence:
    - <schema snippet / config snippet / gitnexus finding>
  remediation:
    plan_mode: |
      <fix description>
    edit_mode: |
      <code / config diff>
  references:
    - <GDPR article / ENISA guideline / NIST SP>
  blocker_at_tier: [...]
  data_classes_affected: [email, health_record, ...]
```

Dimension summary:

```markdown
## Data Protection Summary

Data classes inventoried: <count>
Sensitive fields identified: <list>
Stores covered: <DB, object-storage, cache, queue, logs, warehouse, ...>
Encryption at rest: <status per store>
Encryption in transit: <status>
Retention enforced: <yes/no per data class>
Backup last tested restore: <date or unknown>

Top 3 data-protection risks:
  1. ...
```

## Example findings

### Example 1 — Production PII copied to developer laptops

```yaml
- id: DATA-002
  severity: critical
  category: access
  title: "Developers sync prod DB dumps to local via `rake db:pull`"
  location: "Rakefile:67; process-level"
  description: |
    The repo includes a `rake db:pull` task that snapshots the
    production DB to the running developer's laptop for debugging.
    Interviewed engineers confirmed it's used ~weekly. Production
    `users` includes names, emails, phone numbers, and
    government-issued ID fragments for ~300k users; `transactions`
    includes payment metadata. This is a GDPR Art. 5 and Art. 32
    finding (data minimization and security of processing
    respectively), a PCI-DSS scope explosion (every developer laptop
    is now in scope if payment data is touched), and a breach waiting
    for a lost/stolen laptop.
  evidence:
    - |
      # Rakefile:67
      task :db_pull do
        sh "pg_dump $PROD_URL > db/dev.sql"
        sh "psql $DEV_URL < db/dev.sql"
      end
  remediation:
    plan_mode: |
      1. Remove the task. Replace with a synthetic-data generator or
         a manually-anonymized staging snapshot pipeline (pg_anonymizer,
         Tonic, or custom masking) that runs server-side and is never
         copied to laptops.
      2. Revoke prod DB credentials from developers; use Teleport /
         JIT access for read-only diagnostic queries with audit.
      3. Add a pre-commit hook to block commits that contain
         high-entropy strings suggestive of prod data.
    edit_mode: |
      Delete the Rake task. Scaffold `scripts/synth_data.py` and
      `db/anonymize.sql`. Requires confirmation and ops coordination
      for credential revocation.
  references:
    - "Regulation (EU) 2016/679 Art. 5(1)(c), 32"
  related_findings: [COMP-012]
  blocker_at_tier: [team, scalable]
```

### Example 2 — Backups unencrypted

```yaml
- id: DATA-008
  severity: high
  category: backups
  title: "Nightly DB backup stored in S3 bucket without server-side encryption"
  location: "infra/terraform/backup.tf:22"
  description: |
    The backup bucket has no default encryption configured — objects
    land unencrypted unless the client explicitly sets
    `ServerSideEncryption`. The backup job uses `aws s3 cp` with no
    SSE flag. Backups contain the full user + transactions tables.
    AWS introduced default SSE in 2023, but Terraform older than that
    with an explicit bucket config overrides it. Unencrypted backups
    are a finding under GDPR Art. 32 and a clear regulatory gap for
    HIPAA-covered or PCI-DSS-in-scope data.
  evidence:
    - |
      # infra/terraform/backup.tf:22 — missing server_side_encryption block
      resource "aws_s3_bucket" "backups" {
        bucket = "acme-prod-backups"
      }
  remediation:
    plan_mode: |
      1. Add `aws_s3_bucket_server_side_encryption_configuration` to
         force SSE-KMS (preferred) or SSE-S3 on every object.
      2. Use a dedicated KMS key for backups (rotation enabled),
         different from application-layer keys — enables crypto-
         shredding without affecting live data.
      3. Bucket policy denies unencrypted uploads.
      4. Re-upload existing unencrypted objects to force encryption.
    edit_mode: |
      Safe with one caveat: a subsequent sweep job re-encrypts existing
      objects (costs GB-transferred pricing). Confirm before applying.
  references:
    - "Regulation (EU) 2016/679 Art. 32"
    - "AWS S3 User Guide — Default encryption"
  blocker_at_tier: [team, scalable]
  data_classes_affected: [email, name, phone, transaction]
```

### Example 3 — Retention policy documented but never enforced

```yaml
- id: DATA-016
  severity: high
  category: retention
  title: "6-year audit-log retention documented; no scheduled deletion job"
  location: "docs/privacy-policy.md; system-level"
  description: |
    The privacy policy states audit logs retained 6 years for tax +
    compliance reasons, then deleted. The policy is a public
    commitment to data subjects and supervisory authorities. In fact,
    no scheduled deletion job exists — `audit_log` has rows dating to
    2018 (oldest 7.5 years), ~112M rows, 180 GB. The mismatch is
    itself a GDPR Art. 5(1)(e) finding (storage limitation). It's also
    a supervisor-provokable question if a data subject requests
    confirmation that their data has been deleted.
  evidence:
    - "docs/privacy-policy.md §7: 'We retain audit logs for 6 years.'"
    - "SELECT MIN(created_at) FROM audit_log → 2018-04-11"
  remediation:
    plan_mode: |
      1. Add a scheduled job (daily or weekly) that deletes / archives
         rows beyond the documented window.
      2. Chunked delete to avoid long locks on the table.
      3. Log the deletion counts to the audit stream itself (deleted N
         rows from window Y).
      4. One-time backfill: delete pre-policy rows in a managed
         migration with ops awareness.
    edit_mode: |
      Destructive. Requires explicit confirmation and legal sign-off
      before first run — some categories may have overriding legal
      retention (tax, fraud investigations).
  references:
    - "Regulation (EU) 2016/679 Art. 5(1)(e)"
  related_findings: [COMP-018]
  blocker_at_tier: [team, scalable]
  data_classes_affected: [audit_log]
```

## Edit-mode remediation

Safe to apply:
- Adding retention cleanup jobs (scheduled delete) — but confirm retention period with user.
- Enabling `sslmode=require` / `ssl=true` on DB clients (if server supports it).
- Adding TTLs to caches.
- Adding S3 bucket default-encryption config.
- Adding S3 lifecycle rules for log retention.
- Scrubbing known-PII fields from logs at the logger level.
- Adding PII column comments / annotations for inventory tracking.

Require confirmation per change:
- Enabling DB-level encryption on an existing database (may require downtime / re-write).
- Adding field-level encryption to existing columns (needs backfill strategy).
- Rotating encryption keys (needs coordination with backups + active sessions).
- Deleting data (anything that destroys data needs explicit approval even if called "retention cleanup").
- Changing backup / restore configuration.
- Changing access control on data stores.

## Do not

- Do not treat hashing as encryption. Hashes are one-way, but hashes of bounded values (emails, phone numbers) are trivially reversible.
- Do not treat pseudonymization as anonymization.
- Do not recommend "encrypt everything" as a universal fix — crypto creates new problems (key management, recoverability) and adds latency. Match control to data class.
- Do not ignore dev/staging — prod PII in dev is one of the most common compliance findings.
- Do not silently delete data, even when "policy says so". Log, confirm, leave an audit trail.
- Do not confuse at-rest encryption at the disk layer with protection from the application — if the app is compromised, disk encryption doesn't help.
- Do not conflate backup with archive. Backup = restore a recent state. Archive = long-term retention. They have different requirements.
