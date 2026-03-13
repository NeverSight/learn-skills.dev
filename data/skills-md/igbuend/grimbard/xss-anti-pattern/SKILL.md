---
name: "xss-anti-pattern"
description: "Security anti-pattern for Cross-Site Scripting vulnerabilities (CWE-79). Use when generating or reviewing code that renders HTML, handles user input in web pages, uses innerHTML/document.write, or builds dynamic web content. Covers Reflected, Stored, and DOM-based XSS. AI code has 86% XSS failure rate."
---

# Cross-Site Scripting (XSS) Anti-Pattern

**Severity:** Critical

## Summary

Cross-Site Scripting (XSS) occurs when applications include untrusted data in web pages without proper encoding, allowing attackers to inject malicious scripts that steal cookies, hijack sessions, or perform unauthorized actions. AI-generated code has an 86% XSS failure rate.

## The Anti-Pattern

The anti-pattern is directly embedding user-controlled data into HTML content without context-aware encoding or sanitization.

### 1. Reflected XSS

User input reflects malicious scripts immediately in the web browser response.

#### BAD Code Example

```html
<!-- VULNERABLE: User input is directly inserted into the HTML output. -->
<!DOCTYPE html>
<html>
<head><title>Search Results</title></head>
<body>
    <h1>Search results for: <!-- Query: --><?php echo $_GET['query']; ?><!-- --></h1>
    <p>No results found for your search.</p>
</body>
</html>

<!-- Attacker's request URL:
     http://example.com/search.php?query=<script>alert(document.cookie)</script>

     Resulting HTML in victim's browser:
     <h1>Search results for: <script>alert(document.cookie)</script></h1>
     The script executes, displaying the victim's cookies.
-->
```

#### GOOD Code Example

```html
<!-- SECURE: HTML-encode all user input before rendering. -->
<!DOCTYPE html>
<html>
<head><title>Search Results</title></head>
<body>
    <h1>Search results for: <?php echo htmlspecialchars($_GET['query'], ENT_QUOTES, 'UTF-8'); ?></h1>
    <p>No results found for your search.</p>
</body>
</html>

<!-- Resulting HTML in victim's browser:
     <h1>Search results for: &lt;script&gt;alert(document.cookie)&lt;/script&gt;</h1>
     The script is rendered as harmless text, not executable code.
-->
```

### 2. Stored XSS

Malicious script is stored on the server (e.g., in a database) and served to users each time they visit the affected page.

#### BAD Code Example

```python
# VULNERABLE: User-provided comments are stored and displayed without encoding.
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
db = sqlite3.connect('comments.db')
db.execute('CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, content TEXT)')

@app.route('/post_comment', methods=['POST'])
def post_comment():
    comment = request.form['comment']
    # CRITICAL FLAW: Comment is stored directly, no encoding or sanitization.
    db.execute("INSERT INTO comments (content) VALUES (?)", (comment,))
    db.commit()
    return "Comment posted!"

@app.route('/view_comments')
def view_comments():
    comments = db.execute("SELECT content FROM comments").fetchall()
    html_output = "<h1>Comments</h1>"
    for comment in comments:
        # The stored malicious script is now rendered directly to every visitor.
        html_output += f"<p>{comment[0]}</p>"
    return render_template_string(html_output)

# Attacker posts: <script>alert('You have been hacked!');</script>
# Every user viewing comments will now see the alert.
```

#### GOOD Code Example

```python
# SECURE: HTML-encode all data retrieved from the database before rendering.
from flask import Flask, request, render_template_string, escape # Import escape for HTML encoding

app = Flask(__name__)
db = sqlite3.connect('comments_safe.db')
db.execute('CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, content TEXT)')

@app.route('/post_comment_safe', methods=['POST'])
def post_comment_safe():
    comment = request.form['comment']
    # It's generally best practice to store raw user input and escape on output.
    db.execute("INSERT INTO comments (content) VALUES (?)", (comment,))
    db.commit()
    return "Comment posted safely!"

@app.route('/view_comments_safe')
def view_comments_safe():
    comments = db.execute("SELECT content FROM comments").fetchall()
    html_output = "<h1>Comments</h1>"
    for comment in comments:
        # SECURE: Use `escape` (or `htmlspecialchars` in PHP, or a templating engine's auto-escape)
        # to HTML-encode the data before inserting it into the HTML.
        html_output += f"<p>{escape(comment[0])}</p>"
    return render_template_string(html_output)

# Even better: Use a templating engine (like Jinja2 in Flask) with auto-escaping enabled by default.
# return render_template('comments.html', comments=comments)
# In comments.html: {{ comment.content }} (auto-escaped)
```

### 3. DOM-based XSS

The XSS vulnerability resides in client-side code rather than server-side code.

#### BAD Code Example

```javascript
// VULNERABLE: Client-side JavaScript directly uses URL parameters in innerHTML.
// http://example.com/page.html?name=<img%20src=x%20onerror=alert(document.cookie)>
window.onload = function() {
    var params = new URLSearchParams(window.location.search);
    var username = params.get('name'); // Gets user input from URL.

    // CRITICAL FLAW: innerHTML interprets the string as HTML, executing the script.
    document.getElementById('welcomeMessage').innerHTML = 'Welcome, ' + username + '!';
};
```

#### GOOD Code Example

```javascript
// SECURE: Use `textContent` which treats input as plain text, not HTML.
window.onload = function() {
    var params = new URLSearchParams(window.location.search);
    var username = params.get('name');

    // SECURE: textContent sets the text content of the node,
    // not parsing it as HTML, preventing script execution.
    document.getElementById('welcomeMessage').textContent = 'Welcome, ' + username + '!';
};

// If you absolutely need to insert HTML from user input, use a robust sanitization library
// like DOMPurify.
// document.getElementById('welcomeMessage').innerHTML = DOMPurify.sanitize(userHtml);
```

## Detection

- **Code Review:** Examine any code that takes user input or data from a database and inserts it into an HTML page. Look for:
  - Direct use of `echo`, `print`, `innerHTML`, `document.write()`, `insertAdjacentHTML()`.
  - Templating engines with auto-escaping disabled.
  - String concatenation to build HTML.
- **Dynamic Analysis (Penetration Testing):**
  - Input common XSS payloads (`<script>alert(1)</script>`, `"><img src=x onerror=alert(1)>`) into all input fields (URL parameters, form fields, headers).
  - Check if the payloads are reflected or stored and executed.
- **Use XSS Scanners:** Automated tools can help identify potential XSS vulnerabilities.

## Prevention

- [ ] **HTML-encode all untrusted data** before inserting it into HTML content. This is the primary defense against XSS. Use functions like `htmlspecialchars` (PHP), `escape` (Python Flask), or templating engine auto-escaping (Jinja2, Handlebars).
- [ ] **Use context-sensitive encoding:** Different contexts (HTML body, HTML attribute, JavaScript, URL, CSS) require different encoding schemes. Do not use a generic encoder for all contexts.
- [ ] **Sanitize HTML if necessary:** If your application *must* allow users to provide rich HTML content, use a robust, well-maintained HTML sanitization library (e.g., [DOMPurify](https://github.com/cure53/DOMPurify) for JavaScript). Never try to write your own HTML sanitizer.
- [ ] **Use `textContent` instead of `innerHTML`** when inserting user-provided strings into the DOM via JavaScript.
- [ ] **Implement a strong Content Security Policy (CSP)** as a defense-in-depth mechanism. A strict CSP can mitigate XSS by restricting which scripts can execute and from where resources can be loaded.
- [ ] **Perform input validation:** While not a primary defense against XSS, validating input to restrict character sets or length can reduce the attack surface.

## Related Security Patterns & Anti-Patterns

- [Mutation XSS Anti-Pattern](../mutation-xss/): A specific type of XSS that bypasses sanitizers due to browser parsing differences.
- [DOM Clobbering Anti-Pattern](../dom-clobbering/): Another client-side attack that abuses how browsers handle DOM elements.
- [Missing Security Headers Anti-Pattern](../missing-security-headers/): CSP is a security header that greatly enhances XSS protection.
- [Missing Input Validation Anti-Pattern](../missing-input-validation/): The root cause of many injection vulnerabilities, including XSS.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM01:2025 - Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')](https://cwe.mitre.org/data/definitions/79.html)
- [CAPEC-86: Cross Site Scripting](https://capec.mitre.org/data/definitions/86.html)
- [PortSwigger: Cross Site Scripting](https://portswigger.net/web-security/cross-site-scripting)
- [CAPEC-591: Reflected XSS](https://capec.mitre.org/data/definitions/591.html)
- [CAPEC-592: Stored XSS](https://capec.mitre.org/data/definitions/592.html)
- [PortSwigger: Cross Site Scripting](https://portswigger.net/web-security/cross-site-scripting)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
