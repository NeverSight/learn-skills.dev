---
name: "ldap-injection-anti-pattern"
description: "Security anti-pattern for LDAP injection vulnerabilities (CWE-90). Use when generating or reviewing code that constructs LDAP filters, queries directory services, or handles user input in LDAP operations. Detects unescaped special characters in LDAP filters."
---

# LDAP Injection Anti-Pattern

**Severity:** High

## Summary

LDAP Injection occurs when user input is insecurely inserted into LDAP queries without escaping special characters. Attackers manipulate query logic through character injection, enabling authentication bypass, unauthorized data access, privilege escalation, and directory structure disclosure.

## The Anti-Pattern

Never build LDAP filters by concatenating unescaped user input. Special characters alter filter structure and meaning.

### BAD Code Example

```python
# VULNERABLE: Unescaped user input concatenated into LDAP filter
import ldap

def find_user_by_name(ldap_connection, username):
    # Username directly inserted into filter string
    # Attacker can inject special LDAP characters: '*', '(', ')', '|'
    search_filter = f"(uid={username})"

    # Attacker input: 'admin*)(uid=*)'
    # Resulting filter: '(uid=admin*)(uid=*)'
    # Returns unintended records or bypasses security checks
    try:
        results = ldap_connection.search_s(
            "ou=users,dc=example,dc=com",
            ldap.SCOPE_SUBTREE,
            search_filter
        )
        return results
    except ldap.LDAPError as e:
        print(f"LDAP search failed: {e}")
        return None
```

### GOOD Code Example

```python
# SECURE: Escape user input before including in filter
import ldap
from ldap.filter import escape_filter_chars

def find_user_by_name_safe(ldap_connection, username):
    # Escape all user input to neutralize special characters
    # `ldap.filter.escape_filter_chars` handles this securely
    safe_username = escape_filter_chars(username)
    search_filter = f"(uid={safe_username})"

    # Attacker input ('admin*)(uid=*)') escaped to:
    # '(uid=admin\2a\28uid=\2a\29)'
    # Searches for user with literal, harmless name
    try:
        results = ldap_connection.search_s(
            "ou=users,dc=example,dc=com",
            ldap.SCOPE_SUBTREE,
            search_filter
        )
        return results
    except ldap.LDAPError as e:
        print(f"LDAP search failed: {e}")
        return None

# For authentication, use BIND operation instead of search filters
def authenticate_ldap_safe(username, password):
    safe_username = escape_filter_chars(username)
    user_dn = f"uid={safe_username},ou=users,dc=example,dc=com"
    try:
        # Bind to directory as user
        # Standard, secure credential verification
        conn = ldap.initialize("ldap://ldap.example.com")
        conn.simple_bind_s(user_dn, password)
        conn.unbind_s()
        return True # Bind successful, authentication passed
    except ldap.INVALID_CREDENTIALS:
        return False # Bind failed, invalid credentials
    except ldap.LDAPError as e:
        print(f"LDAP error: {e}")
        return False
```

### Language-Specific Examples

**Java:**
```java
// VULNERABLE: Unescaped user input in LDAP filter
import javax.naming.directory.*;

public User findUser(String username) throws NamingException {
    DirContext ctx = getContext();

    // Direct concatenation - injection vulnerable!
    String filter = "(uid=" + username + ")";
    // Attacker input: "admin*)(uid=*)" creates: "(uid=admin*)(uid=*)"

    SearchControls controls = new SearchControls();
    NamingEnumeration<SearchResult> results =
        ctx.search("ou=users,dc=example,dc=com", filter, controls);

    return parseUser(results);
}
```

```java
// SECURE: Use proper escaping or parameterized queries
import javax.naming.directory.*;
import org.apache.directory.api.ldap.model.filter.FilterEncoder;

public User findUserSafe(String username) throws NamingException {
    DirContext ctx = getContext();

    // Escape special LDAP characters
    String safeUsername = FilterEncoder.encodeFilterValue(username);
    String filter = "(uid=" + safeUsername + ")";

    SearchControls controls = new SearchControls();
    NamingEnumeration<SearchResult> results =
        ctx.search("ou=users,dc=example,dc=com", filter, controls);

    return parseUser(results);
}

// BEST: Use BIND for authentication instead of search
public boolean authenticateSafe(String username, String password) {
    String escapedUsername = FilterEncoder.encodeFilterValue(username);
    String userDn = "uid=" + escapedUsername + ",ou=users,dc=example,dc=com";

    try {
        DirContext ctx = new InitialDirContext(
            createEnv(userDn, password));
        ctx.close();
        return true; // Bind successful
    } catch (AuthenticationException e) {
        return false; // Invalid credentials
    } catch (NamingException e) {
        throw new RuntimeException("LDAP error", e);
    }
}
```

**C# (ASP.NET):**
```csharp
// VULNERABLE: String interpolation in LDAP filter
using System.DirectoryServices;

public User FindUser(string username)
{
    using (var entry = new DirectoryEntry("LDAP://dc=example,dc=com"))
    using (var searcher = new DirectorySearcher(entry))
    {
        // Vulnerable to injection!
        searcher.Filter = $"(sAMAccountName={username})";
        // Attacker: "admin*)(sAMAccountName=*)" bypasses intended logic

        SearchResult result = searcher.FindOne();
        return ParseUser(result);
    }
}
```

```csharp
// SECURE: Escape LDAP special characters
using System.DirectoryServices;
using System.Text.RegularExpressions;

public User FindUserSafe(string username)
{
    // Escape LDAP special characters: \ * ( ) NUL
    string escapedUsername = EscapeLdapFilter(username);

    using (var entry = new DirectoryEntry("LDAP://dc=example,dc=com"))
    using (var searcher = new DirectorySearcher(entry))
    {
        searcher.Filter = $"(sAMAccountName={escapedUsername})";
        SearchResult result = searcher.FindOne();
        return ParseUser(result);
    }
}

private string EscapeLdapFilter(string input)
{
    return input
        .Replace("\\", "\\5c")
        .Replace("*", "\\2a")
        .Replace("(", "\\28")
        .Replace(")", "\\29")
        .Replace("\0", "\\00");
}
```

**Node.js (ldapjs):**
```javascript
// VULNERABLE: Template literal with user input
const ldap = require('ldapjs');

function searchUser(username, callback) {
    const client = ldap.createClient({ url: 'ldap://ldap.example.com' });

    // Direct interpolation - vulnerable!
    const filter = `(uid=${username})`;
    // Attacker: "admin*)(uid=*)" bypasses filter

    client.search('ou=users,dc=example,dc=com', {
        filter: filter,
        scope: 'sub'
    }, callback);
}
```

```javascript
// SECURE: Use ldapjs escape function
const ldap = require('ldapjs');

function searchUserSafe(username, callback) {
    const client = ldap.createClient({ url: 'ldap://ldap.example.com' });

    // Escape LDAP filter characters
    const safeUsername = ldap.filters.escape(username);
    const filter = `(uid=${safeUsername})`;

    client.search('ou=users,dc=example,dc=com', {
        filter: filter,
        scope: 'sub'
    }, callback);
}

// BEST: Use BIND for authentication
function authenticateSafe(username, password, callback) {
    const client = ldap.createClient({ url: 'ldap://ldap.example.com' });
    const safeUsername = ldap.filters.escape(username);
    const userDn = `uid=${safeUsername},ou=users,dc=example,dc=com`;

    client.bind(userDn, password, (err) => {
        client.unbind();
        callback(err ? false : true);
    });
}
```

## Detection

- **Find unescaped LDAP filter construction:** Grep for string concatenation in filters:
  - `rg 'search.*\(.*f["\'].*{|search.*\+.*uid=' --type py`
  - `rg 'SearchRequest.*\+|DirectorySearcher.*\+' --type cs`
  - `rg 'new LdapQuery.*\+|filter.*concat' --type java`
- **Verify escaping function usage:** Check for proper escaping:
  - `rg 'ldap.*search' -A 2 | rg -v 'escape_filter|escape_dn'` (Python)
  - `rg 'DirectorySearcher|SearchRequest' -A 3` (C#)
  - Look for missing escaping before filter construction
- **Audit all LDAP operations:** Find search and bind operations:
  - `rg 'ldap\.search|search_s|search_st' --type py`
  - `rg 'DirectorySearcher|DirectoryEntry' --type cs`
  - `rg 'LdapContext\.search|DirContext\.search' --type java`
- **Test with LDAP metacharacters:** Inject special chars to verify escaping:
  - `*` (wildcard), `(` `)` (filter grouping), `\` (escape), `|` (OR), `&` (AND)
  - Input: `admin*)(uid=*)` should not bypass authentication

## Prevention

- [ ] **Always escape user input:** Use trusted library functions (e.g., `ldap.filter.escape_filter_chars` in Python) before placing in LDAP filters
- [ ] **Use BIND for authentication:** Bind directly instead of search + password comparison. BIND is LDAP's intended credential verification mechanism
- [ ] **Use parameterized queries:** If supported by library/framework. Safest approach—separates query structure from data
- [ ] **Apply Least Privilege:** LDAP service account should have read-only access to only necessary directory parts

## Related Security Patterns & Anti-Patterns

- [SQL Injection Anti-Pattern](../sql-injection/): Same fundamental vulnerability (mixing code and data) for SQL databases
- [XPath Injection Anti-Pattern](../xpath-injection/): Similar injection vulnerability targeting XML databases
- [Missing Input Validation Anti-Pattern](../missing-input-validation/): Root cause enabling many injection attacks

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM01:2025 - Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP LDAP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_Sheet.html)
- [CWE-90: LDAP Injection](https://cwe.mitre.org/data/definitions/90.html)
- [CAPEC-136: LDAP Injection](https://capec.mitre.org/data/definitions/136.html)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
