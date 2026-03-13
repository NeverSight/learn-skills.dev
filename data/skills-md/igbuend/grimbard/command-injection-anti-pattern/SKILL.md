---
name: "command-injection-anti-pattern"
description: "Security anti-pattern for OS Command Injection vulnerabilities (CWE-78). Use when generating or reviewing code that executes shell commands, runs system processes, or handles user input in command-line operations. Detects shell string concatenation and recommends argument arrays."
---

# Command Injection Anti-Pattern

**Severity:** Critical

## Summary

Command injection allows attackers to execute arbitrary OS commands by manipulating user input. This anti-pattern occurs when applications concatenate user input into shell command strings. Common in AI-generated code. Enables complete system compromise, data exfiltration, malware installation, and lateral movement.

## The Anti-Pattern

User input embedded in shell command strings enables command injection. The shell cannot distinguish between intended commands and attacker-injected commands.

### BAD Code Example

```python
# VULNERABLE: Shell command with user input
import os

def ping_host(hostname):
    # User input is directly concatenated into the command string.
    # An attacker can inject malicious commands separated by a semicolon or other shell metacharacters.
    command = "ping -c 4 " + hostname
    os.system(command)

# Example of a successful attack:
# hostname = "google.com; rm -rf /"
# Resulting command: "ping -c 4 google.com; rm -rf /"
# This executes the ping and then attempts to delete the entire filesystem.
```

### GOOD Code Example

```python
# SECURE: Use argument arrays, avoid shell
import subprocess

def ping_host(hostname):
    # Validate input against allowlist
    import re
    if not re.match(r'^[a-zA-Z0-9.-]+$', hostname):
        raise ValueError("Invalid hostname format")

    # The command and its arguments are passed as a list.
    # The underlying OS API executes the command directly without invoking a shell,
    # so shell metacharacters in `hostname` are treated as a literal string.
    try:
        subprocess.run(["ping", "-c", "4", hostname], check=True, shell=False)
    except subprocess.CalledProcessError as e:
        print(f"Error executing ping: {e}")

```

### JavaScript/Node.js Examples

**BAD:**
```javascript
// VULNERABLE: Shell command with user input
const { exec } = require('child_process');

function pingHost(hostname) {
    // User input concatenated into command string
    exec(`ping -c 4 ${hostname}`, (error, stdout) => {
        console.log(stdout);
    });
}

// Attack: hostname = "google.com; cat /etc/passwd"
// Executes: ping -c 4 google.com; cat /etc/passwd
```

**GOOD:**
```javascript
// SECURE: Use execFile with argument array
const { execFile } = require('child_process');

function pingHost(hostname) {
    // Validate hostname format
    if (!/^[a-zA-Z0-9.-]+$/.test(hostname)) {
        throw new Error('Invalid hostname format');
    }

    // Arguments passed as array, no shell invocation
    execFile('ping', ['-c', '4', hostname], (error, stdout) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        console.log(stdout);
    });
}
```

### Java Examples

**BAD:**
```java
// VULNERABLE: Runtime.exec() with string concatenation
public void pingHost(String hostname) {
    try {
        // String concatenation creates command injection risk
        String command = "ping -c 4 " + hostname;
        Runtime.getRuntime().exec(command);
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

**GOOD:**
```java
// SECURE: ProcessBuilder with argument array
import java.io.IOException;
import java.util.regex.Pattern;

public void pingHost(String hostname) {
    // Validate hostname format
    if (!Pattern.matches("^[a-zA-Z0-9.-]+$", hostname)) {
        throw new IllegalArgumentException("Invalid hostname format");
    }

    try {
        // Arguments in array, no shell interpretation
        ProcessBuilder pb = new ProcessBuilder("ping", "-c", "4", hostname);
        Process process = pb.start();
        process.waitFor();
    } catch (IOException | InterruptedException e) {
        e.printStackTrace();
    }
}
```

## Detection

**Python:**
- `os.system()` with any user input
- `subprocess.run()` or `subprocess.Popen()` with `shell=True`
- String concatenation: `"command " + user_input`
- f-strings: `f"command {user_input}"`

**JavaScript/Node.js:**
- `child_process.exec()` with user input
- Template literals: `` `command ${userInput}` ``
- String concatenation: `"command " + userInput`

**Java:**
- `Runtime.getRuntime().exec()` with string concatenation
- Single string argument to `exec()` instead of string array

**PHP:**
- `exec()`, `system()`, `shell_exec()`, `passthru()` with user input
- String concatenation: `"command " . $userInput`

**Search Patterns:**
- Grep: `shell=True|exec\(|system\(|child_process\.exec`
- Look for user input variables in command construction
- Check for string concatenation or interpolation with command functions

## Prevention

- [ ] **Use argument arrays** instead of shell strings (e.g., `subprocess.run(["command", "arg1", "arg2"], shell=False)`).
- [ ] **Never pass `shell=True`** with user-controlled input to execution functions.
- [ ] **Validate all input** against a strict allowlist of known-good values or formats.
- [ ] **Use language-specific libraries or APIs** instead of external shell commands whenever possible.
- [ ] **Apply the Principle of Least Privilege** to the process executing the command, restricting its permissions to the absolute minimum required.

## Testing for Command Injection

**Manual Testing:**
1. Test shell metacharacters: `;`, `|`, `&`, `$()`, `` ` ``, `&&`, `||`
2. Input payloads: `; ls`, `| whoami`, `& cat /etc/passwd`, `` `id` ``
3. Verify commands execute safely without shell interpretation
4. Confirm metacharacters treated as literal strings

**Automated Testing:**
- **Static Analysis:** Semgrep, Bandit (Python), ESLint security plugins, SpotBugs (Java)
- **DAST:** Burp Suite, OWASP ZAP with command injection payloads
- **Code Review:** Search for detection patterns above

**Example Test:**
```python
# Test that shell metacharacters are treated literally
def test_command_injection_prevention():
    malicious_input = "google.com; rm -rf /"
    try:
        ping_host(malicious_input)  # Should fail validation
        assert False, "Should reject malicious input"
    except ValueError:
        pass  # Expected
```

## Remediation Steps

1. **Identify vulnerable code** - Use detection patterns above
2. **Validate necessity** - Can you avoid shell commands entirely?
3. **Replace with safe API** - Use language-specific libraries when possible
4. **Convert to argument arrays** - Replace string concatenation
5. **Remove shell=True** - Never use with user input
6. **Add input validation** - Allowlist known-good patterns
7. **Test the fix** - Verify shell metacharacters are literal
8. **Review similar code** - Check for pattern across codebase

## Related Security Patterns & Anti-Patterns

- [SQL Injection Anti-Pattern](../sql-injection/): A similar injection pattern targeting databases.
- [Path Traversal Anti-Pattern](../path-traversal/): Often combined with command injection to access or create files in unintended locations.
- [Missing Input Validation Anti-Pattern](../missing-input-validation/): A fundamental weakness that enables command injection.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM01:2025 - Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP OS Command Injection Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)
- [CAPEC-88: OS Command Injection](https://capec.mitre.org/data/definitions/88.html)
- [PortSwigger: Os Command Injection](https://portswigger.net/web-security/os-command-injection)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
