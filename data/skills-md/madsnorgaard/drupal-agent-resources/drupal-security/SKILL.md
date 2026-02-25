---
name: drupal-security
description: Drupal security expertise. Auto-activates when writing forms, controllers, queries, or handling user input. Prevents XSS, SQL injection, and access bypass vulnerabilities.
---

# Drupal Security Expert

You proactively identify security vulnerabilities while code is being written, not after.

## When This Activates

- Writing or editing forms, controllers, or plugins
- Handling user input or query parameters
- Building database queries
- Rendering user-provided content
- Implementing access control

## Critical Security Patterns

### SQL Injection Prevention

**NEVER concatenate user input into queries:**

```php
// VULNERABLE - SQL injection
$query = "SELECT * FROM users WHERE name = '" . $name . "'";
$result = $connection->query($query);

// SAFE - parameterized query
$result = $connection->select('users', 'u')
  ->fields('u')
  ->condition('name', $name)
  ->execute();

// SAFE - placeholder
$result = $connection->query(
  'SELECT * FROM {users} WHERE name = :name',
  [':name' => $name]
);
```

### XSS Prevention

**Always escape output. Trust the render system:**

```php
// VULNERABLE - raw HTML output
return ['#markup' => $user_input];
return ['#markup' => '<div>' . $title . '</div>'];

// SAFE - plain text (auto-escaped)
return ['#plain_text' => $user_input];

// SAFE - use proper render elements
return [
  '#type' => 'html_tag',
  '#tag' => 'div',
  '#value' => $title,  // Escaped automatically
];

// SAFE - Twig auto-escapes
{{ variable }}  // Escaped
{{ variable|raw }}  // DANGEROUS - only for trusted HTML
```

**For admin-only content:**
```php
use Drupal\Component\Utility\Xss;

// Filter but allow safe HTML tags
$safe = Xss::filterAdmin($user_html);
```

### Access Control

**Always verify permissions:**

```php
// In routing.yml
my_module.admin:
  path: '/admin/my-module'
  requirements:
    _permission: 'administer my_module'  # Required!

// In code
if (!$this->currentUser->hasPermission('administer my_module')) {
  throw new AccessDeniedHttpException();
}

// Entity queries - check access!
$query = $this->entityTypeManager
  ->getStorage('node')
  ->getQuery()
  ->accessCheck(TRUE)  // CRITICAL - never FALSE unless intentional
  ->condition('type', 'article');
```

### CSRF Protection

Forms automatically include CSRF tokens. For custom AJAX:

```php
// Include token in AJAX requests
$build['#attached']['drupalSettings']['myModule']['token'] =
  \Drupal::csrfToken()->get('my_module_action');

// Validate in controller
if (!$this->csrfToken->validate($token, 'my_module_action')) {
  throw new AccessDeniedHttpException('Invalid token');
}
```

### File Upload Security

```php
$validators = [
  'file_validate_extensions' => ['pdf doc docx'],  // Whitelist extensions
  'file_validate_size' => [25600000],  // 25MB limit
  'FileSecurity' => [],  // Drupal 10.2+ - blocks dangerous files
];

// NEVER trust file extension alone - check MIME type
$file_mime = $file->getMimeType();
$allowed_mimes = ['application/pdf', 'application/msword'];
if (!in_array($file_mime, $allowed_mimes)) {
  // Reject file
}
```

### Sensitive Data

```php
// NEVER log sensitive data
$this->logger->info('User @user logged in', ['@user' => $username]);
// NOT: $this->logger->info('Login: ' . $username . ':' . $password);

// NEVER expose in error messages
throw new \Exception('Database error');  // Generic
// NOT: throw new \Exception('Query failed: ' . $query);

// Use environment variables for secrets
$api_key = getenv('MY_API_KEY');
// NOT: $api_key = 'hardcoded-secret-key';
```

## Red Flags to Watch For

When you see these patterns, **immediately warn**:

| Pattern | Risk | Fix |
|---------|------|-----|
| String concatenation in SQL | SQL injection | Use query builder |
| `#markup` with variables | XSS | Use `#plain_text` |
| `accessCheck(FALSE)` | Access bypass | Use `accessCheck(TRUE)` |
| Missing `_permission` in routes | Unauthorized access | Add permission |
| `{{ var\|raw }}` in Twig | XSS | Remove `\|raw` |
| Hardcoded passwords/keys | Credential exposure | Use env vars |
| `eval()` or `exec()` | Code injection | Avoid entirely |
| `unserialize()` on user data | Object injection | Use JSON |

## Security Review Prompts

When reviewing code, always ask:

1. "Where does this data come from?" (User input = untrusted)
2. "Where does this data go?" (Output = escape it)
3. "Who should access this?" (Permissions required)
4. "What if this contains malicious input?" (Validate/sanitize)

## Quick Security Checklist

Before any code is committed:

- [ ] All user input validated/sanitized
- [ ] All output properly escaped
- [ ] Routes have permission requirements
- [ ] Entity queries use `accessCheck(TRUE)`
- [ ] No hardcoded credentials
- [ ] File uploads validate type AND extension
- [ ] Forms use Form API (automatic CSRF)
- [ ] Sensitive data not logged

## Resources

- [Drupal Security Best Practices](https://www.drupal.org/docs/security-in-drupal)
- [Writing Secure Code](https://www.drupal.org/docs/security-in-drupal/writing-secure-code-for-drupal)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
