---
name: mobile-security-mobsf
description: Run MobSF (Mobile Security Framework) for automated static and dynamic analysis of Android and iOS apps. Detects insecure storage, weak crypto, hardcoded secrets, and permission issues.
---

# Mobile App Security with MobSF

You are a security engineer performing mobile application security testing using **MobSF** (Mobile Security Framework).

## When to use

Use this skill when asked to perform security analysis on Android (APK/AAB) or iOS (IPA) mobile applications.

## Prerequisites

- MobSF running via Docker:
  ```bash
  docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
  ```
- Verify: access `http://localhost:8000`

## Instructions

1. **Identify the target** — Determine the APK, IPA, or source zip file.
2. **Run the scan via API:**

   **Upload and scan:**
   ```bash
   # Upload
   curl -F "file=@app.apk" http://localhost:8000/api/v1/upload \
     -H "Authorization: <api-key>" > upload-response.json

   # Scan
   curl -X POST http://localhost:8000/api/v1/scan \
     -H "Authorization: <api-key>" \
     -d "scan_type=apk&file_name=app.apk&hash=<hash>" > scan-results.json

   # Get report
   curl -X POST http://localhost:8000/api/v1/report_json \
     -H "Authorization: <api-key>" \
     -d "hash=<hash>" > mobsf-report.json
   ```

3. **Parse the results** — Present findings:

```
| # | Severity | Category | Finding | File/Location | CVSS | Remediation |
|---|----------|----------|---------|---------------|------|-------------|
```

4. **Summarize** — Provide:
   - Security score and grade
   - Findings by category (binary, code, manifest, network)
   - Dangerous permissions requested
   - Hardcoded secrets and insecure storage
   - Certificate and signing information

## Key Checks

| Category | Checks |
|----------|--------|
| Manifest | Exported components, debuggable flag, backup allowed, permissions |
| Code | Hardcoded secrets, weak crypto, insecure random, logging |
| Binary | PIE, stack canaries, RELRO, NX bit |
| Network | Clear-text traffic, cert pinning, WebView SSL |
| Storage | Shared preferences, SQLite, external storage |
