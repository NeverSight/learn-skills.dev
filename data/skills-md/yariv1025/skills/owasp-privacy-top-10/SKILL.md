---
name: owasp-privacy-top-10
description: "OWASP Top 10 Privacy Risks - prevention, detection, and remediation for privacy in web applications. Use when addressing app vulnerabilities, data leakage, breach response, consent, transparency, data deletion, data quality, session expiration, user access rights, excessive data collection."
---

# OWASP Top 10 Privacy Risks

This skill encodes the OWASP Top 10 Privacy Risks for privacy-aware design and review. References are loaded per risk. Based on OWASP Top 10 Privacy Risks v2.0 2021.

## When to Read Which Reference

| Risk | Read |
|------|------|
| P1 Web Application Vulnerabilities | [references/p1-web-app-vulnerabilities.md](references/p1-web-app-vulnerabilities.md) |
| P2 Operator-sided Data Leakage | [references/p2-operator-data-leakage.md](references/p2-operator-data-leakage.md) |
| P3 Insufficient Data Breach Response | [references/p3-breach-response.md](references/p3-breach-response.md) |
| P4 Consent on Everything | [references/p4-consent.md](references/p4-consent.md) |
| P5 Non-transparent Policies | [references/p5-non-transparent-policies.md](references/p5-non-transparent-policies.md) |
| P6 Insufficient Deletion of User Data | [references/p6-insufficient-deletion.md](references/p6-insufficient-deletion.md) |
| P7 Insufficient Data Quality | [references/p7-data-quality.md](references/p7-data-quality.md) |
| P8 Missing or Insufficient Session Expiration | [references/p8-session-expiration.md](references/p8-session-expiration.md) |
| P9 Inability to Access and Modify Data | [references/p9-user-access-modify-data.md](references/p9-user-access-modify-data.md) |
| P10 Excessive Data Collection | [references/p10-excessive-collection.md](references/p10-excessive-collection.md) |

## Quick Patterns

- Fix technical vulnerabilities that affect data; prevent operator leakage; have a breach response plan. Obtain valid consent; be transparent; support deletion, access, and portability; minimize collection; expire sessions.

## Quick Reference / Examples

| Task | Approach |
|------|----------|
| Obtain valid consent | Explicit opt-in, granular choices, easy withdrawal. See [P4](references/p4-consent.md). |
| Support data deletion | Implement "right to erasure" across all stores. See [P6](references/p6-insufficient-deletion.md). |
| Provide data access | Export user data in portable format (JSON/CSV). See [P9](references/p9-user-access-modify-data.md). |
| Minimize collection | Collect only what's necessary for the stated purpose. See [P10](references/p10-excessive-collection.md). |
| Breach response | Have a documented plan, notify within required timeframes. See [P3](references/p3-breach-response.md). |

**Data deletion endpoint:**
```python
@app.delete("/api/users/{user_id}/data")
def delete_user_data(user_id: str, current_user: User):
    if current_user.id != user_id:
        raise HTTPException(403)
    # Delete from all data stores
    UserDB.delete(user_id)
    AnalyticsDB.anonymize(user_id)
    SearchIndex.remove(user_id)
    BackupService.schedule_deletion(user_id)
    return {"status": "deletion_scheduled"}
```

**Consent collection (explicit opt-in):**
```javascript
// Require explicit action, no pre-checked boxes
<input type="checkbox" id="marketing" />
<label for="marketing">I agree to receive marketing emails</label>
// Only enable submit when required consents are given
```

**Data export endpoint:**
```python
@app.get("/api/users/{user_id}/export")
def export_user_data(user_id: str):
    data = collect_all_user_data(user_id)
    return Response(
        content=json.dumps(data, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={user_id}_data.json"}
    )
```

## Workflow

Load the reference for the risk you are addressing. See [OWASP Top 10 Privacy Risks](https://owasp.org/www-project-top-10-privacy-risks) for the official list.
