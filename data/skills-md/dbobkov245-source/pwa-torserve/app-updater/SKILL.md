---
name: app-updater
description: Specialist in self-hosted APK updates without Google Play.
---

# Self-Hosted App Updater

This skill handles updating the Android TV application (APK) directly from a private server or GitHub Releases, bypassing Google Play.

## 🔄 Update Workflow

1.  **Check Version:** Fetch `version.json` from your server on app launch.
2.  **Prompt User:** If `remoteVersion > localVersion`, show a modal: "Update Available".
3.  **Download APK:** Use `CapacitorHttp` to download the `.apk` file to a temporary location.
4.  **Install:** Trigger the Android Intent to install the package.

## 📱 Implementation Details

### 1. Version Manifest (`version.json`)
Host this file on your server (e.g., GitHub Pages or your API):
```json
{
  "version": "1.2.3",
  "minVersion": "1.0.0", // Force update if critical
  "url": "https://example.com/app-release.apk",
  "notes": "Fixed critical bug with player."
}
```

### 2. Download & Install (Java/Native Plugin)

Since standard web APIs cannot trigger APK installation, you need a Native Plugin method (extend `TVPlayer.java` or create `AppUpdater.java`).

**Required Permissions (AndroidManifest.xml):**
```xml
<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```

**Java Implementation (Snippet):**
```java
// Download logic using DownloadManager or OkHttp...
// Then install:
Intent intent = new Intent(Intent.ACTION_VIEW);
intent.setDataAndType(apkUri, "application/vnd.android.package-archive");
intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION); // Critical for FileProvider
context.startActivity(intent);
```

### 3. FileProvider (Critical for Android 7+)

You cannot just expose `file://` URIs. You MUST use a `FileProvider` in `AndroidManifest.xml`:

```xml
<provider
    android:name="androidx.core.content.FileProvider"
    android:authorities="${applicationId}.fileprovider"
    android:exported="false"
    android:grantUriPermissions="true">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
</provider>
```

**`res/xml/file_paths.xml`:**
```xml
<paths>
    <external-path name="external_files" path="."/>
</paths>
```

## ⚠️ Safety First
- **Signature Verification:** Android automatically verifies that the new APK signature matches the old one. If not, update fails. Ensure you sign with the SAME key.
- **HTTPS Only:** Never download APKs over HTTP.
- **User Consent:** Always ask the user before starting a download (bandwidth) and before installing.
