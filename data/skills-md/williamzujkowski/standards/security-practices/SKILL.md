---
name: security-practices
description: Modern security standards including Zero Trust Architecture, supply chain security, DevSecOps integration, and cloud-native protection
---

# Security Practices Skill

## Level 1: Quick Start (5 minutes)

### What You'll Learn

Implement essential security practices to protect applications from common vulnerabilities and attacks.

### Core Principles

- **Zero Trust**: Never trust, always verify
- **Defense in Depth**: Multiple layers of security controls
- **Shift Left**: Integrate security early in development
- **Least Privilege**: Grant minimum necessary permissions

### Quick Security Checklist

- [ ] Enable MFA for all user accounts
- [ ] Use HTTPS/TLS 1.3 for all connections
- [ ] Validate and sanitize all inputs
- [ ] Never commit secrets to version control
- [ ] Run dependency vulnerability scans
- [ ] Implement proper error handling (no sensitive info in errors)

### Common Vulnerabilities to Avoid

```typescript
// ❌ NEVER: Hardcoded secrets
const API_KEY = "sk_live_abc123";

// ✅ ALWAYS: Use environment variables
const API_KEY = process.env.API_KEY;

// ❌ NEVER: SQL injection vulnerability
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ ALWAYS: Parameterized queries
const query = "SELECT * FROM users WHERE id = ?";
db.query(query, [userId]);

// ❌ NEVER: Weak password validation
if (password.length >= 6) { /* valid */ }

// ✅ ALWAYS: Strong password requirements
if (
  password.length >= 12 &&
  /[A-Z]/.test(password) &&
  /[a-z]/.test(password) &&
  /[0-9]/.test(password) &&
  /[^A-Za-z0-9]/.test(password)
) { /* valid */ }
```

### Critical Security Tools

- **Secrets Management**: HashiCorp Vault, AWS Secrets Manager
- **Dependency Scanning**: Snyk, Dependabot, npm audit
- **SAST**: SonarQube, Semgrep, CodeQL
- **DAST**: OWASP ZAP, Burp Suite

---

## Level 2: Implementation (30 minutes)

### Deep Dive Topics

#### 1. Zero Trust Architecture

**Core Components:**

```typescript
// Identity verification with MFA
interface AuthenticationService {
  // Primary authentication
  verifyCredentials(username: string, password: string): Promise<Session>;

  // Multi-factor authentication
  verifyMfaToken(sessionId: string, token: string): Promise<boolean>;

  // Continuous authentication
  verifySessionValidity(sessionId: string): Promise<boolean>;
}

// Policy engine for access decisions
class PolicyEngine {
  async evaluateAccess(
    user: User,
    resource: Resource,
    context: Context
  ): Promise<AccessDecision> {
    const riskScore = await this.calculateRiskScore(user, context);
    const policy = await this.getApplicablePolicy(user, resource);

    return {
      allowed: this.checkPermissions(user, resource, policy),
      requiresStepUp: riskScore > RISK_THRESHOLD,
      auditRequired: true,
    };
  }

  private async calculateRiskScore(
    user: User,
    context: Context
  ): Promise<number> {
    let risk = 0;
    if (context.location !== user.knownLocations) risk += 30;
    if (context.device !== user.knownDevices) risk += 20;
    if (context.timeOfDay < 6 || context.timeOfDay > 22) risk += 10;
    return risk;
  }
}
```

**NIST Mapping:**

- @nist-controls: [ac-2, ac-3, ac-6, ia-2, ia-5, au-2, sc-8]

#### 2. Supply Chain Security

```yaml
# .github/workflows/supply-chain-security.yml
name: Supply Chain Security

on: [push, pull_request]

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Dependency vulnerability scanning
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      # SBOM generation
      - name: Generate SBOM
        run: |
          npm install -g @cyclonedx/cyclonedx-npm
          cyclonedx-npm --output-file sbom.json

      # License compliance
      - name: Check Licenses
        run: |
          npm install -g license-checker
          license-checker --production --failOn "GPL;AGPL"
```

**SBOM Implementation:**

```typescript
// Generate Software Bill of Materials
interface SBOMEntry {
  name: string;
  version: string;
  license: string;
  supplier: string;
  checksum: string;
  vulnerabilities: Vulnerability[];
}

async function generateSBOM(): Promise<SBOM> {
  const dependencies = await analyzeDependencies();
  const vulnerabilities = await scanVulnerabilities(dependencies);

  return {
    components: dependencies.map((dep) => ({
      name: dep.name,
      version: dep.version,
      license: dep.license,
      checksum: calculateChecksum(dep),
      vulnerabilities: vulnerabilities.filter((v) => v.package === dep.name),
    })),
    metadata: {
      timestamp: new Date().toISOString(),
      toolVersion: "1.0.0",
    },
  };
}
```

**NIST Mapping:**

- @nist-controls: [sa-10, sr-3, sr-4, sr-6, sr-11]

#### 3. Container Security

```dockerfile
# Secure Dockerfile example
FROM node:20-alpine AS base

# Security: Run as non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Security: Minimal base image, scan for vulnerabilities
FROM base AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

FROM base AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM base AS runner
WORKDIR /app

# Security: Copy only necessary files
COPY --from=dependencies --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist

# Security: Switch to non-root user
USER nodejs

# Security: Expose only necessary port
EXPOSE 3000

# Security: Use exec form for better signal handling
CMD ["node", "dist/index.js"]
```

**Kubernetes Security:**

```yaml
# pod-security-policy.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false # Prevent privileged containers
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - "configMap"
    - "secret"
    - "persistentVolumeClaim"
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: "MustRunAsNonRoot"
  seLinux:
    rule: "RunAsAny"
  supplementalGroups:
    rule: "RunAsAny"
  fsGroup:
    rule: "RunAsAny"
  readOnlyRootFilesystem: true
```

**NIST Mapping:**

- @nist-controls: [cm-2, cm-3, cm-7, si-7]

#### 4. API Security

```typescript
// Rate limiting
import rateLimit from "express-rate-limit";

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: "Too many requests from this IP",
  standardHeaders: true,
  legacyHeaders: false,
});

// Input validation with sanitization
import { z } from "zod";
import sanitizeHtml from "sanitize-html";

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(12).max(128),
  name: z
    .string()
    .min(1)
    .max(100)
    .transform((val) => sanitizeHtml(val, { allowedTags: [] })),
});

// Authentication middleware
async function authenticate(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const token = req.headers.authorization?.split(" ")[1];
    if (!token) {
      throw new UnauthorizedError("No token provided");
    }

    const decoded = await verifyJWT(token);
    const session = await validateSession(decoded.sessionId);

    if (!session.valid) {
      throw new UnauthorizedError("Invalid session");
    }

    req.user = decoded;
    next();
  } catch (error) {
    // @nist au-2 "Audit authentication failures"
    await auditLog.record("auth.failure", {
      ip: req.ip,
      path: req.path,
      error: error.message,
    });
    res.status(401).json({ error: "Unauthorized" });
  }
}

// CORS configuration
const corsOptions = {
  origin: (origin: string, callback: Function) => {
    const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(",") || [];
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error("Not allowed by CORS"));
    }
  },
  credentials: true,
  maxAge: 86400,
};
```

**NIST Mapping:**

- @nist-controls: [ac-2, ac-3, ia-2, sc-8, si-10]

#### 5. DevSecOps Integration

```yaml
# .github/workflows/security-pipeline.yml
name: Security Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Secret scanning
      - name: TruffleHog Secret Scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

      # Static Application Security Testing (SAST)
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
            p/cwe-top-25

      # Dependency scanning
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      # Container scanning
      - name: Trivy Container Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: "myapp:${{ github.sha }}"
          format: "sarif"
          output: "trivy-results.sarif"

      # Upload results to GitHub Security
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: trivy-results.sarif

  # Security gate: block on high/critical vulnerabilities
  security-gate:
    needs: security-scan
    runs-on: ubuntu-latest
    steps:
      - name: Check Security Results
        run: |
          if [ "${{ needs.security-scan.result }}" != "success" ]; then
            echo "Security scan failed - blocking deployment"
            exit 1
          fi
```

### Integration Points

- Links to [Coding Standards](../coding-standards/SKILL.md) for secure code patterns
- Links to [Testing Standards](../testing/SKILL.md) for security testing
- Links to [NIST Compliance](../nist-compliance/SKILL.md) for control implementation

---

## Level 3: Mastery (Extended Learning)

### Advanced Topics

#### 1. Incident Response Automation

```typescript
// Automated incident response workflow
class IncidentResponseOrchestrator {
  async handleSecurityIncident(incident: SecurityIncident): Promise<void> {
    // 1. Immediate containment
    await this.containThreat(incident);

    // 2. Evidence collection
    const evidence = await this.collectEvidence(incident);

    // 3. Analysis and root cause
    const analysis = await this.analyzeIncident(incident, evidence);

    // 4. Remediation
    await this.remediateVulnerability(analysis);

    // 5. Notification
    await this.notifyStakeholders(incident, analysis);

    // 6. Post-incident review
    await this.schedulePostMortem(incident);
  }

  private async containThreat(incident: SecurityIncident): Promise<void> {
    switch (incident.type) {
      case "compromised-credentials":
        await this.revokeAllSessions(incident.userId);
        await this.resetPassword(incident.userId);
        break;
      case "malicious-traffic":
        await this.blockIPAddress(incident.sourceIP);
        break;
      case "data-exfiltration":
        await this.isolateAffectedSystems(incident.systemIds);
        await this.disableExternalConnections();
        break;
    }
  }
}
```

#### 2. Cryptographic Implementations

```typescript
// Secure password hashing with Argon2
import argon2 from "argon2";

async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536, // 64 MB
    timeCost: 3,
    parallelism: 4,
  });
}

// Secure token generation
import crypto from "crypto";

function generateSecureToken(length: number = 32): string {
  return crypto.randomBytes(length).toString("base64url");
}

// Encryption at rest
import { createCipheriv, createDecipheriv, randomBytes } from "crypto";

class DataEncryption {
  private algorithm = "aes-256-gcm";
  private key: Buffer;

  constructor(secretKey: string) {
    this.key = crypto.scryptSync(secretKey, "salt", 32);
  }

  encrypt(data: string): { encrypted: string; iv: string; tag: string } {
    const iv = randomBytes(16);
    const cipher = createCipheriv(this.algorithm, this.key, iv);

    let encrypted = cipher.update(data, "utf8", "hex");
    encrypted += cipher.final("hex");

    return {
      encrypted,
      iv: iv.toString("hex"),
      tag: cipher.getAuthTag().toString("hex"),
    };
  }

  decrypt(encrypted: string, iv: string, tag: string): string {
    const decipher = createDecipheriv(
      this.algorithm,
      this.key,
      Buffer.from(iv, "hex")
    );
    decipher.setAuthTag(Buffer.from(tag, "hex"));

    let decrypted = decipher.update(encrypted, "hex", "utf8");
    decrypted += decipher.final("utf8");

    return decrypted;
  }
}
```

#### 3. Security Monitoring and Alerting

```typescript
// Real-time security monitoring
class SecurityMonitor {
  private metrics: MetricsCollector;
  private alerting: AlertingService;

  async monitorAuthenticationPatterns(): Promise<void> {
    const recentAttempts = await this.getRecentAuthAttempts();

    // Detect brute force attacks
    const bruteForceAttempts = recentAttempts.filter(
      (attempt) => attempt.failures > 5 && attempt.timeWindow < 60000
    );

    if (bruteForceAttempts.length > 0) {
      await this.alerting.send({
        severity: "high",
        type: "brute-force-detected",
        details: bruteForceAttempts,
      });
    }

    // Detect credential stuffing
    const stuffingIndicators = await this.detectCredentialStuffing(
      recentAttempts
    );
    if (stuffingIndicators.length > 0) {
      await this.alerting.send({
        severity: "critical",
        type: "credential-stuffing",
        details: stuffingIndicators,
      });
    }
  }
}
```

### Resources

#### Essential Reading

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Zero Trust Architecture (NIST SP 800-207)](https://csrc.nist.gov/publications/detail/sp/800-207/final)

#### Security Tools

- **SAST**: Semgrep, CodeQL, SonarQube
- **DAST**: OWASP ZAP, Burp Suite
- **Secrets Detection**: TruffleHog, GitLeaks, detect-secrets
- **Container Security**: Trivy, Clair, Anchore
- **Dependency Scanning**: Snyk, Dependabot, WhiteSource

#### Compliance Frameworks

- NIST 800-53r5
- ISO 27001
- SOC 2
- PCI DSS
- GDPR

### Templates

#### Security Review Checklist

```markdown
## Security Review Checklist

### Authentication & Authorization
- [ ] MFA implemented for all user accounts
- [ ] Password requirements meet complexity standards
- [ ] Session management secure (timeout, rotation)
- [ ] RBAC properly implemented

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] TLS 1.3 enforced for data in transit
- [ ] PII properly identified and protected
- [ ] Backups encrypted

### Input Validation
- [ ] All inputs validated and sanitized
- [ ] SQL injection prevented
- [ ] XSS prevention implemented
- [ ] CSRF tokens in use

### Infrastructure
- [ ] Containers run as non-root
- [ ] Network segmentation implemented
- [ ] Security groups properly configured
- [ ] Logging and monitoring enabled
```

### Scripts

See `./scripts/` for:

- Vulnerability scanning automation
- Secret detection pre-commit hooks
- SBOM generation scripts
- Security audit reporters

## Examples

### Basic Usage

```python
// TODO: Add basic example for security-practices
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for security-practices
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how security-practices
// works with other systems and services
```

See `examples/security-practices/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring security-practices functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for security-practices
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

## Bundled Resources

- [Full MODERN_SECURITY_STANDARDS.md](../../docs/standards/MODERN_SECURITY_STANDARDS.md)
- [NIST Implementation Guide](../../docs/nist/NIST_IMPLEMENTATION_GUIDE.md)
- Security policy templates in `./templates/`
- Automated security scanning scripts in `./scripts/`
- Example secure configurations in `./resources/`
