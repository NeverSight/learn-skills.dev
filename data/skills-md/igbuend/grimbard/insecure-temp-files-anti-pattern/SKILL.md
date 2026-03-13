---
name: "insecure-temp-files-anti-pattern"
description: "Security anti-pattern for insecure temporary files (CWE-377). Use when generating or reviewing code that creates temporary files, handles file caching, or processes uploads through temp storage. Detects predictable paths, insecure permissions, and missing cleanup."
---

# Insecure Temp Files Anti-Pattern

**Severity:** Medium

## Summary

Insecure temporary file creation exposes three attack vectors: predictable file names enabling symlink attacks, insecure permissions allowing unauthorized access, and missing cleanup leaving sensitive data on disk. Attackers exploit these to read sensitive data, inject malicious content, or cause denial of service. AI-generated code frequently suggests simplistic file handling vulnerable to these attacks.

## The Anti-Pattern

Never create temporary files without securing their location, naming, permissions, and lifecycle management.

### 1. Predictable File Names

Using a predictable name for a temporary file creates a race condition. An attacker can guess the file name and create a symbolic link (symlink) at that location pointing to a sensitive system file. When the application writes to its "temporary" file, it is actually overwriting the linked file.

#### BAD Code Example

```python
# VULNERABLE: Predictable temporary file name in a shared directory.
import os

def process_user_data(user_id, data):
    # The filename is easy for an attacker to guess.
    temp_path = f"/tmp/userdata_{user_id}.txt"

    # Attacker's action (done before this code runs):
    # ln -s /etc/passwd /tmp/userdata_123.txt

    # When the application writes to the temp file for user 123,
    # it is actually overwriting the system's password file.
    with open(temp_path, "w") as f:
        f.write(data)

    # ... processing logic ...
    os.remove(temp_path)
```

#### GOOD Code Example

```python
# SECURE: Use a library function that creates a securely named temporary file.
import tempfile

def process_user_data(user_id, data):
    # `tempfile.mkstemp()` creates a temporary file with a random, unpredictable name
    # and returns a low-level file handle and the path.
    # It also ensures the file is created with secure permissions (0600 on Unix).
    fd, temp_path = tempfile.mkstemp(prefix="userdata_", suffix=".txt")
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(data)
        # ... processing logic ...
    finally:
        # Always ensure the file is cleaned up.
        os.remove(temp_path)
```

### 2. Insecure Permissions and Missing Cleanup

Creating a temporary file with default permissions can make it world-readable, allowing other users on the system to access its contents. Failing to delete the temporary file after use means that sensitive data may be left behind on the disk.

#### BAD Code Example

```python
# VULNERABLE: World-readable permissions and no cleanup.
import uuid

def generate_report(data):
    # The name is random, but the permissions are not secure.
    temp_path = f"/tmp/{uuid.uuid4()}.pdf"

    # `open` with mode 'w' often uses default permissions like 0644,
    # which means other users on the system can read the file.
    with open(temp_path, "w") as f:
        f.write(data) # Sensitive report data is written.

    return temp_path # The path is returned, but the file is never deleted.
```

#### GOOD Code Example

```python
# SECURE: Guaranteed cleanup using a context manager.
import tempfile

def generate_report(data):
    # `NamedTemporaryFile` creates a file that is automatically deleted
    # when the context manager is exited.
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdf', delete=True) as temp_f:
        # The file has a secure name and permissions.
        temp_f.write(data)
        temp_f.flush()

        # You can use `temp_f.name` to get the path and pass it to other functions.
        result = send_file_to_storage(temp_f.name)

    # The temporary file is automatically and reliably deleted here,
    # even if an error occurs inside the `with` block.
    return result
```

### Language-Specific Examples

**JavaScript/Node.js:**
```javascript
// VULNERABLE: Predictable name and no cleanup
const fs = require('fs');
const path = require('path');

function processUpload(userId, data) {
  const tempPath = `/tmp/upload_${userId}.dat`; // Predictable!
  fs.writeFileSync(tempPath, data); // World-readable by default
  // ... processing ...
  // File never deleted!
  return tempPath;
}
```

```javascript
// SECURE: Use tmp module with automatic cleanup
const tmp = require('tmp');

function processUpload(userId, data) {
  // Creates file with mode 0600 (owner read/write only)
  const tempFile = tmp.fileSync({ prefix: 'upload-', postfix: '.dat' });

  try {
    fs.writeFileSync(tempFile.name, data);
    // ... processing ...
    return processFile(tempFile.name);
  } finally {
    tempFile.removeCallback(); // Guaranteed cleanup
  }
}
```

**Java:**
```java
// VULNERABLE: Predictable name in shared directory
public void processData(String userId, byte[] data) throws IOException {
    File tempFile = new File("/tmp/data_" + userId + ".tmp"); // Predictable!
    Files.write(tempFile.toPath(), data); // Default permissions may be insecure
    // ... processing ...
    // No cleanup - file persists!
}
```

```java
// SECURE: Use Files.createTempFile with try-with-resources
import java.nio.file.*;
import java.nio.file.attribute.*;

public void processData(String userId, byte[] data) throws IOException {
    // Create with restricted permissions (owner only)
    Set<PosixFilePermission> perms = PosixFilePermissions.fromString("rw-------");
    FileAttribute<Set<PosixFilePermission>> attr =
        PosixFilePermissions.asFileAttribute(perms);

    Path tempFile = Files.createTempFile("data-", ".tmp", attr);

    try {
        Files.write(tempFile, data);
        // ... processing ...
    } finally {
        Files.deleteIfExists(tempFile); // Guaranteed cleanup
    }
}
```

**Go:**
```go
// VULNERABLE: Predictable path and missing cleanup
func processData(userID string, data []byte) error {
    tempPath := fmt.Sprintf("/tmp/data_%s.tmp", userID) // Predictable!
    if err := os.WriteFile(tempPath, data, 0644); err != nil { // World-readable!
        return err
    }
    // ... processing ...
    // No cleanup!
    return nil
}
```

```go
// SECURE: Use os.CreateTemp with defer cleanup
import "os"

func processData(userID string, data []byte) error {
    // Creates file with mode 0600 automatically
    tempFile, err := os.CreateTemp("", "data-*.tmp")
    if err != nil {
        return err
    }
    defer os.Remove(tempFile.Name()) // Guaranteed cleanup
    defer tempFile.Close()

    if _, err := tempFile.Write(data); err != nil {
        return err
    }

    // ... processing ...
    return nil
}
```

## Detection

- **Search for insecure temp directories:** Grep for hardcoded temp paths:
  - `rg 'open\s*\(\s*["\']/(tmp|var/tmp)/'`
  - `rg 'File\.createTempFile|mktemp|tmpfile'` (check if used correctly)
- **Identify predictable file names:** Find patterns based on user IDs or timestamps:
  - `rg 'f"/tmp/{user_id}' 'f"/tmp/{username}'`
  - `rg 'new File\("/tmp/" \+ userId'`
- **Check file permissions:** Audit permission settings:
  - `rg 'os\.chmod.*0o[67]'` (world-readable/writable)
  - Review code for missing `os.umask(0o077)` or tempfile usage
- **Verify cleanup logic:** Ensure files are always deleted:
  - `rg 'open\(' | rg -v 'with|try.*finally|NamedTemporaryFile'`
  - Check for missing `defer f.Close()` (Go) or `using` (C#)

## Prevention

- [ ] **Use a trusted library** for creating temporary files, such as `tempfile` in Python or `Files.createTempFile` in Java. These libraries are designed to handle naming and permissions securely.
- [ ] **Never construct temporary file paths** using predictable names.
- [ ] **Ensure temporary files are created with restrictive permissions** (e.g., only readable and writable by the owner, 0600).
- [ ] **Always clean up temporary files.** Use `try...finally` blocks or language features like context managers (`with` in Python) to guarantee deletion.
- [ ] **Consider using in-memory buffers** (like `io.BytesIO` in Python) instead of temporary files if the data is small enough to fit in memory.

## Related Security Patterns & Anti-Patterns

- [Path Traversal Anti-Pattern](../path-traversal/): An attacker might manipulate input to control where a temporary file is written.
- [Unrestricted File Upload Anti-Pattern](../unrestricted-file-upload/): Applications often use temporary files to process uploads, making this a related risk.

## References

- [OWASP Top 10 A01:2025 - Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/)
- [OWASP GenAI LLM02:2025 - Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm02-sensitive-information-disclosure/)
- [OWASP API Security API1:2023 - Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [CWE-377: Insecure Temporary File](https://cwe.mitre.org/data/definitions/377.html)
- [CAPEC-155: Screen Temporary Files for Sensitive Information](https://capec.mitre.org/data/definitions/155.html)
- [Python tempfile module](https://docs.python.org/3/library/tempfile.html)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
