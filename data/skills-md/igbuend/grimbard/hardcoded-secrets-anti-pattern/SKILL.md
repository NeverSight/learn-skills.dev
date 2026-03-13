---
name: "hardcoded-secrets-anti-pattern"
description: "Security anti-pattern for hardcoded credentials and secrets (CWE-798). Use when generating or reviewing code that handles API keys, passwords, database credentials, encryption keys, or any sensitive configuration. Detects embedded secrets and recommends environment variables or secret managers."
---

# Hardcoded Secrets Anti-Pattern

**Severity:** Critical

## Summary

Hardcoded secrets embed sensitive credentials (API keys, passwords, database credentials) directly in source code. Anyone with code access—developers, version control history, or attackers—can extract these secrets. AI models frequently generate hardcoded secrets, trained on public code with this common bad practice. Secrets committed to public repositories are discovered and exploited by automated bots within minutes.

## The Anti-Pattern

Never store secrets, credentials, or sensitive configuration values in files tracked by version control.

### BAD Code Example

```python
# VULNERABLE: Hardcoded API keys and database credentials in the source code.
import requests
import psycopg2

# 1. Hardcoded API Key
API_KEY = "sk-live-123abc456def789ghi"

def get_weather(city):
    url = f"https://api.weatherprovider.com/v1/current?city={city}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

# 2. Hardcoded Database Password
DB_HOST = "localhost"
DB_USER = "admin"
DB_PASSWORD = "my_super_secret_password_123" # Exposed in the code
DB_NAME = "main_db"

def get_db_connection():
    # The password is right here for any attacker to see.
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn
```

### GOOD Code Example

```python
# SECURE: Load secrets from the environment or a dedicated secrets manager.
import os
import requests
import psycopg2

# 1. API key loaded from an environment variable.
API_KEY = os.environ.get("WEATHER_API_KEY")

def get_weather(city):
    if not API_KEY:
        raise ValueError("WEATHER_API_KEY environment variable not set.")
    url = f"https://api.weatherprovider.com/v1/current?city={city}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

# 2. Database credentials loaded from environment variables.
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

def get_db_connection():
    # The application will fail safely if secrets are not configured in the environment.
    if not all([DB_USER, DB_PASSWORD, DB_NAME]):
        raise ValueError("Database environment variables are not fully configured.")
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn
```

### Language-Specific Examples

**JavaScript/Node.js:**
```javascript
// VULNERABLE: Hardcoded credentials
const stripe = require('stripe')('sk_live_abc123def456ghi789'); // Exposed!

const dbConfig = {
  host: 'localhost',
  user: 'admin',
  password: 'MyP@ssw0rd123', // Never do this!
  database: 'production_db'
};
```

```javascript
// SECURE: Use environment variables
require('dotenv').config(); // Load .env file

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
};

if (!process.env.STRIPE_SECRET_KEY || !process.env.DB_PASSWORD) {
  throw new Error('Required environment variables not set');
}
```

**Java/Spring Boot:**
```java
// VULNERABLE: Hardcoded in application.properties
// application.properties:
// spring.datasource.password=MySecretPassword123
// aws.access.key=AKIAIOSFODNN7EXAMPLE
```

```java
// SECURE: Use environment variables or secret managers
// application.properties:
// spring.datasource.password=${DB_PASSWORD}
// aws.access.key=${AWS_ACCESS_KEY}

// Or use AWS Secrets Manager
@Configuration
public class SecretsConfig {
    @Bean
    public AWSSecretsManager secretsManager() {
        return AWSSecretsManagerClientBuilder.standard()
            .withRegion("us-west-2")
            .build();
    }

    @Bean
    public String dbPassword(AWSSecretsManager secretsManager) {
        GetSecretValueRequest request = new GetSecretValueRequest()
            .withSecretId("prod/db/password");
        GetSecretValueResult result = secretsManager.getSecretValue(request);
        return result.getSecretString();
    }
}
```

**C# (ASP.NET Core):**
```csharp
// VULNERABLE: Hardcoded in appsettings.json
// {
//   "ConnectionStrings": {
//     "Default": "Server=localhost;Database=mydb;User=admin;Password=Secret123;"
//   },
//   "ApiKeys": {
//     "SendGrid": "SG.abc123def456ghi789"
//   }
// }
```

```csharp
// SECURE: Use User Secrets for dev, Azure Key Vault for production
// Startup.cs
public class Startup
{
    public Startup(IConfiguration configuration)
    {
        Configuration = configuration;
    }

    public IConfiguration Configuration { get; }

    public void ConfigureServices(IServiceCollection services)
    {
        // Connection string from environment or User Secrets
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseSqlServer(
                Configuration.GetConnectionString("Default")));

        // API key from Azure Key Vault (production) or User Secrets (dev)
        services.AddSingleton<IEmailService>(sp =>
            new SendGridEmailService(Configuration["ApiKeys:SendGrid"]));
    }
}

// Set secrets:
// dotnet user-secrets set "ConnectionStrings:Default" "Server=..."
// Or use Azure Key Vault in production
```

## Detection

- **Use secret scanning tools:** Scan repository history automatically:
  - `gitleaks detect --source . --verbose`
  - `trufflehog git file://. --only-verified`
  - `git-secrets --scan` (pre-commit hook integration)
- **Search for keywords:** Grep for common patterns:
  - `rg -i '(password|secret|api_?key|token|credential)\s*=\s*["\']'`
  - `rg 'sk-[a-zA-Z0-9]{32,}'` (OpenAI API keys)
- **Detect high-entropy strings:** Identify random 32+ character strings:
  - `trufflehog --entropy=True`
  - `detect-secrets scan --baseline .secrets.baseline`
- **Check configuration files:** Audit committed configs:
  - `git log --all --full-history -- "*.env" "config.json" "settings.py"`
  - Review files that should be in .gitignore

## Prevention

- [ ] **Never hardcode any credentials, API keys, or secrets** in your source code.
- [ ] **Use environment variables** to store secrets in development and other non-production environments.
- [ ] **Use a dedicated secrets management service** for production environments (e.g., AWS Secrets Manager, HashiCorp Vault, Google Secret Manager).
- [ ] **Add a `.env` file** (or similar) to your `.gitignore` to prevent accidental commits of local development secrets.
- [ ] **Integrate secret scanning tools** into your CI/CD pipeline and pre-commit hooks to block commits that contain secrets.
- [ ] **Implement a secret rotation policy** to limit the impact of a compromised secret.

## Related Security Patterns & Anti-Patterns

- [Weak Encryption Anti-Pattern](../weak-encryption/): Secrets, even when stored, need to be encrypted at rest.
- [JWT Misuse Anti-Pattern](../jwt-misuse/): The secret key for signing JWTs is a common hardcoded secret.
- [Verbose Error Messages Anti-Pattern](../verbose-error-messages/): Debug screens can leak environment variables, which may contain secrets.

## References

- [OWASP Top 10 A07:2025 - Authentication Failures](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/)
- [OWASP GenAI LLM02:2025 - Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm02-sensitive-information-disclosure/)
- [OWASP API Security API2:2023 - Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [CAPEC-191: Read Sensitive Constants Within an Executable](https://capec.mitre.org/data/definitions/191.html)
- [PortSwigger: Information Disclosure](https://portswigger.net/web-security/information-disclosure)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
