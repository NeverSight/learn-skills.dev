---
name: "debug-mode-production-anti-pattern"
description: "Security anti-pattern for debug mode in production (CWE-215). Use when generating or reviewing code that configures application settings, deployment configurations, or error handling. Detects hardcoded debug flags and development-only features in production."
---

# Debug Mode in Production Anti-Pattern

**Severity:** High

## Summary

Debug mode in production exposes sensitive system information and creates backdoors. Occurs when development settings remain enabled in deployment. Common in AI-generated code that hardcodes debug flags or fails to differentiate environments.

## The Anti-Pattern

This anti-pattern manifests in two primary ways:

1. **Hardcoded Debug Flags:** Global flag `DEBUG = True` never changes, so the application runs in debug mode in all environments.
2. **Unprotected Debug Endpoints:** Debug routes (`/debug/env`, `/_debug/sql`) included in production builds provide attack vectors.

### BAD Code Example

```python
# VULNERABLE: Hardcoded debug flag and unprotected debug routes
import os
from flask import Flask, jsonify

app = Flask(__name__)
app.config['DEBUG'] = True # Hardcoded debug mode

@app.route("/")
def index():
    return "Welcome!"

# This debug route exposes all environment variables, including potential secrets.
# It should never be present in a production environment.
@app.route("/debug/env")
def debug_env():
    if app.config['DEBUG']:
        return jsonify(os.environ.copy())
    return "Not in debug mode."

if __name__ == "__main__":
    app.run()
```

### GOOD Code Example

```python
# SECURE: Environment-based configuration and conditional routes
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Load configuration from the environment. Default to 'production'.
APP_ENV = os.environ.get('APP_ENV', 'production')
app.config['DEBUG'] = APP_ENV == 'development'

@app.route("/")
def index():
    return "Welcome!"

# This debug route is now conditionally registered and will only exist
# if the application is explicitly run in a development environment.
if app.config['DEBUG']:
    @app.route("/debug/env")
    def debug_env():
        return jsonify(os.environ.copy())

# It's also a good practice to add a startup check to prevent accidental
# deployment of debug mode to production.
if APP_ENV == 'production' and app.config['DEBUG']:
    raise ValueError("FATAL: Debug mode is enabled in a production environment. Aborting.")

if __name__ == "__main__":
    app.run()

```

### JavaScript/Node.js Examples

**BAD:**
```javascript
// VULNERABLE: Hardcoded debug flag in Express
const express = require('express');
const app = express();

// Hardcoded debug mode
const DEBUG = true;

app.get('/', (req, res) => {
    res.send('Welcome!');
});

// Debug route exposes environment variables
app.get('/debug/env', (req, res) => {
    if (DEBUG) {
        res.json(process.env);
    } else {
        res.send('Not in debug mode.');
    }
});

app.listen(3000);
```

**GOOD:**
```javascript
// SECURE: Environment-based configuration
const express = require('express');
const app = express();

// Load from environment, default to production
const APP_ENV = process.env.APP_ENV || 'production';
const DEBUG = APP_ENV === 'development';

app.get('/', (req, res) => {
    res.send('Welcome!');
});

// Conditionally register debug route
if (DEBUG) {
    app.get('/debug/env', (req, res) => {
        res.json(process.env);
    });
}

// Startup check prevents production debug mode
if (APP_ENV === 'production' && DEBUG) {
    throw new Error('FATAL: Debug mode enabled in production. Aborting.');
}

app.listen(3000);
```

### Java/Spring Boot Examples

**BAD:**
```java
// VULNERABLE: Hardcoded debug in application.properties
// application.properties:
// debug=true
// logging.level.root=DEBUG

@RestController
public class DebugController {
    @Value("${debug}")
    private boolean debug;

    @GetMapping("/debug/env")
    public Map<String, String> debugEnv() {
        if (debug) {
            return System.getenv();
        }
        return Map.of("error", "Not in debug mode");
    }
}
```

**GOOD:**
```java
// SECURE: Profile-based configuration
// application-dev.properties:
// debug=true
// application-prod.properties:
// debug=false

@RestController
@Profile("dev")  // Only register in development profile
public class DebugController {
    @GetMapping("/debug/env")
    public Map<String, String> debugEnv() {
        return System.getenv();
    }
}

// Application startup check
@Component
public class EnvironmentValidator implements ApplicationRunner {
    @Value("${spring.profiles.active:prod}")
    private String activeProfile;

    @Value("${debug:false}")
    private boolean debug;

    @Override
    public void run(ApplicationArguments args) {
        if ("prod".equals(activeProfile) && debug) {
            throw new IllegalStateException(
                "FATAL: Debug mode enabled in production. Aborting."
            );
        }
    }
}
```

## Detection

**Python/Flask/Django:**
- `DEBUG = True` in source code
- `debug=True` in Flask config
- `DEBUG = True` in Django settings.py
- Debug routes: `@app.route("/debug/`

**JavaScript/Node.js/Express:**
- `const DEBUG = true` in source code
- `process.env.NODE_ENV !== 'production'` checks missing
- Debug middleware always enabled
- Routes: `app.get('/debug/`

**Java/Spring Boot:**
- `debug=true` in application.properties
- `logging.level.root=DEBUG` in production
- Debug endpoints without `@Profile("dev")`
- `spring.devtools.restart.enabled=true` in prod

**PHP:**
- `error_reporting(E_ALL)` in production
- `display_errors = On` in php.ini
- `APP_DEBUG=true` in .env

**Configuration Files:**
- `.env` files with `DEBUG=true`
- YAML configs with `debug: true`
- JSON configs with `"debug": true`

**Search Patterns:**
- Grep: `DEBUG.*=.*[Tt]rue|debug.*:.*true|\/debug\/|process\.env\.NODE_ENV`
- Development dependencies in production builds
- Stack traces exposed in error responses
- Verbose error messages with file paths

## Prevention

- [ ] **Use environment variables** to control debug mode and other environment-specific settings.
- [ ] **Never hardcode `DEBUG = True`**.
- [ ] **Conditionally register debug routes** so they are not included in production builds.
- [ ] **Implement a startup check** in the application that aborts if it detects debug mode is enabled in a production environment.
- [ ] **Use separate configuration files** for each environment (development, staging, production) to avoid overlap.
- [ ] **Review your CI/CD pipeline** to ensure that the correct environment variables are being injected and that development artifacts are excluded from the final build.

## Testing for Debug Mode

**Manual Testing:**
1. Check environment variables: `echo $DEBUG`, `echo $APP_ENV`
2. Access debug endpoints: `/debug`, `/_debug`, `/debug/env`
3. Trigger errors and check for stack traces
4. Review HTTP headers for debug information (X-Debug, Server versions)

**Automated Testing:**
- **Static Analysis:** Semgrep, Bandit (Python), ESLint, SonarQube
- **Configuration Scanning:** Detect hardcoded `DEBUG = True` in code
- **Runtime Testing:** Burp Suite, OWASP ZAP to find debug endpoints
- **CI/CD Checks:** Fail builds with debug flags enabled

**Example Test:**
```python
# Test that debug mode is disabled in production
def test_debug_disabled_in_production():
    import os
    os.environ['APP_ENV'] = 'production'

    # This should raise ValueError
    with pytest.raises(ValueError, match="Debug mode is enabled in a production environment"):
        import app  # Import triggers startup check
```

**CI/CD Pipeline Check:**
```yaml
# .github/workflows/deploy.yml
- name: Verify No Debug Mode
  run: |
    if grep -r "DEBUG.*=.*True" app/; then
      echo "ERROR: Hardcoded DEBUG=True found"
      exit 1
    fi

    if [ "$APP_ENV" = "production" ] && [ "$DEBUG" = "true" ]; then
      echo "ERROR: Debug mode enabled for production deployment"
      exit 1
    fi
```

## Remediation Steps

1. **Identify debug configurations** - Use detection patterns above
2. **Check current environment** - Determine if debug mode is active
3. **Create environment-based config** - Use environment variables
4. **Remove hardcoded flags** - Replace `DEBUG = True` with env lookup
5. **Conditional debug routes** - Register only in development
6. **Add startup checks** - Abort if debug mode in production
7. **Test the fix** - Verify debug disabled in production config
8. **Update CI/CD** - Add validation to deployment pipeline

## Related Security Patterns & Anti-Patterns

- [Verbose Error Messages Anti-Pattern](../verbose-error-messages/): A common consequence of running in debug mode.
- [Hardcoded Secrets Anti-Pattern](../hardcoded-secrets/): Secrets are often exposed through debug information.
- [Missing Security Headers Anti-Pattern](../missing-security-headers/): Can provide defense-in-depth by controlling how browsers handle content.

## References

- [OWASP Top 10 A02:2025 - Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/)
- [OWASP GenAI LLM02:2025 - Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm02-sensitive-information-disclosure/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [CWE-215: Debug Information Exposure](https://cwe.mitre.org/data/definitions/215.html)
- [CAPEC-121: Exploit Non-Production Interfaces](https://capec.mitre.org/data/definitions/121.html)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
