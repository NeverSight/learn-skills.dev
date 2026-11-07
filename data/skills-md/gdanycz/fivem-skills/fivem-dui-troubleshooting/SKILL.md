---
name: fivem-dui-troubleshooting
description: Troubleshooting common DUI issues, version limitations, and hardware-specific bugs.
---

# Troubleshooting DUI

### 1. Version Disparities (Release vs. Beta)
- `ADD_REPLACE_TEXTURE` is **experimental**. It often fails on **Beta/Latest** branches if called before the GPU commits the first frame.
- **Fix**: Always verify `IS_DUI_AVAILABLE` returns true before applying the texture replacement.

### 2. Chromium (CEF) Limitations
- FiveM currently uses a fork of **CEF M103**, which is several years out of date.
- **Constraint**: Avoid modern CSS/JS features not supported by M103. Using arbitrary third-party code poses a security risk due to unpatched vulnerabilities in older Chromium builds.

### 3. AMD Hardware Issues
- Upgrading to modern CEF versions (M140+) has been delayed due to significant **VRAM memory leaks** specifically on AMD hardware during accelerated painting (`OnAcceleratedPaint`).
- If players report stuttering, advise disabling "Full-screen Optimizations" in FiveM properties.

### 4. Delayed Texture Support
- If `ADD_REPLACE_TEXTURE` returns `false`, the DUI handle might not be ready yet. Implement a retry logic or wait until the browser is fully initialized.
