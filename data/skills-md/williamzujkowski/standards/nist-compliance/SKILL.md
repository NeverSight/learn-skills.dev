---
name: nist-compliance
description: NIST 800-53r5 control implementation, tagging, evidence collection, and compliance automation for security frameworks
---

# NIST Compliance Skill

## Level 1: Quick Start (5 minutes)

### What You'll Learn

Tag code with NIST 800-53r5 controls, track compliance, and generate evidence for security audits.

### Core Principles

- **Traceability**: Link code to security controls
- **Evidence**: Automate compliance documentation
- **Continuous Compliance**: Integrate into CI/CD
- **Defense in Depth**: Multiple control layers

### Quick Start Tagging

```typescript
/**
 * @nist ia-2 "User authentication"
 * @nist ia-5 "Authenticator management"
 * @evidence code, test
 */
export async function authenticateUser(credentials: Credentials) {
  // @nist ia-5.1 "Password complexity validation"
  validatePasswordComplexity(credentials.password);

  // @nist au-2 "Audit authentication events"
  await auditLog.record("auth.attempt", {
    user: credentials.username,
    timestamp: new Date(),
  });

  return authService.verify(credentials);
}
```

```python
# @nist ac-3 "Access enforcement"
# @nist ac-6 "Least privilege"
def check_permissions(user, resource, action):
    """
    @nist-implements ac-3.a "Enforce approved authorizations"
    @evidence test, documentation
    """
    if not user.has_permission(resource, action):
        audit_access_denial(user, resource, action)  # @nist au-2
        raise PermissionDenied()
```

```yaml
# @nist-controls: [sc-8, sc-13, ac-12]
security:
  tls:
    version: "1.3" # @nist sc-8 "Transmission confidentiality"
    ciphers: ["TLS_AES_256_GCM_SHA384"] # @nist sc-13
  session:
    timeout: 1800 # @nist ac-12 "Session termination (30 min)"
```

### Essential Checklist

- [ ] Install pre-commit hooks for NIST validation
- [ ] Tag authentication code (IA family)
- [ ] Tag access control (AC family)
- [ ] Tag audit logging (AU family)
- [ ] Generate initial compliance report

### Common Control Families

| Family | Code | Examples |
|--------|------|----------|
| Access Control | AC | AC-2 (accounts), AC-3 (enforcement), AC-6 (least privilege) |
| Identification & Auth | IA | IA-2 (user auth), IA-5 (authenticators), IA-8 (identification) |
| Audit & Accountability | AU | AU-2 (events), AU-3 (content), AU-6 (review) |
| System & Communications | SC | SC-8 (confidentiality), SC-13 (crypto), SC-28 (data at rest) |
| System & Information Integrity | SI | SI-10 (input validation), SI-11 (error handling) |

---

## Level 2: Implementation (30 minutes)

### Deep Dive Topics

#### 1. Control Family Implementation

**Access Control (AC Family):**

```typescript
// AC-2: Account Management
class UserAccountService {
  /**
   * @nist ac-2.a "Manage system accounts"
   * @nist ac-2.1 "Automated account management"
   * @evidence code, test, automation
   */
  async createAccount(userData: UserData): Promise<Account> {
    // AC-2.c: Specify authorized users
    await this.validateAuthorization(userData);

    // AC-2.f: Create, enable, modify, disable, and remove accounts
    const account = await this.repository.create({
      username: userData.username,
      roles: userData.roles,
      status: "pending_approval", // AC-2.j: Review accounts
      createdAt: new Date(),
    });

    // AU-2: Audit account creation
    await this.auditLog.record("account.created", {
      accountId: account.id,
      createdBy: userData.requestedBy,
    });

    return account;
  }

  /**
   * @nist ac-2.3 "Disable accounts after defined period of inactivity"
   * @evidence automation, monitoring
   */
  async disableInactiveAccounts(): Promise<void> {
    const INACTIVITY_PERIOD_DAYS = 90;
    const threshold = new Date();
    threshold.setDate(threshold.getDate() - INACTIVITY_PERIOD_DAYS);

    const inactiveAccounts = await this.repository.findInactive(threshold);

    for (const account of inactiveAccounts) {
      await this.disableAccount(account.id);
      await this.notifyUser(account, "Account disabled due to inactivity");
    }
  }
}

// AC-3: Access Enforcement
/**
 * @nist ac-3 "Access enforcement"
 * @nist ac-3.7 "Role-based access control"
 * @evidence code, test
 */
class AccessControlMiddleware {
  async enforce(
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> {
    const user = req.user;
    const resource = req.params.resource;
    const action = req.method;

    // AC-3.a: Enforce approved authorizations
    const decision = await this.policyEngine.evaluate({
      subject: user,
      resource: resource,
      action: action,
    });

    if (!decision.allowed) {
      // AU-2: Audit access denials
      await this.auditLog.record("access.denied", {
        user: user.id,
        resource,
        action,
        reason: decision.reason,
      });

      return res.status(403).json({ error: "Access denied" });
    }

    next();
  }
}
```

**Identification & Authentication (IA Family):**

```typescript
// IA-2: Identification and Authentication
/**
 * @nist ia-2 "Identification and authentication (organizational users)"
 * @nist ia-2.1 "Multi-factor authentication"
 * @nist ia-2.8 "Access to accounts - replay resistant"
 * @evidence code, test, documentation
 */
class AuthenticationService {
  async authenticate(credentials: Credentials): Promise<Session> {
    // IA-2: Primary authentication
    const user = await this.verifyCredentials(credentials);

    // IA-2.1: Multi-factor authentication
    const mfaToken = await this.generateMfaToken(user);
    await this.sendMfaToken(user, mfaToken);

    // Return temporary session pending MFA
    return this.createPendingSession(user);
  }

  /**
   * @nist ia-2.1 "Multi-factor authentication to privileged accounts"
   */
  async verifyMfa(sessionId: string, token: string): Promise<Session> {
    const session = await this.getSession(sessionId);

    if (!this.verifyMfaToken(session.user, token)) {
      // AU-2: Audit failed MFA attempts
      await this.auditLog.record("mfa.failed", {
        userId: session.user.id,
        sessionId,
      });
      throw new AuthenticationError("Invalid MFA token");
    }

    // IA-2.8: Replay resistant (one-time use token)
    await this.invalidateMfaToken(session.user, token);

    return this.upgradeToPrimarySession(session);
  }
}

// IA-5: Authenticator Management
/**
 * @nist ia-5 "Authenticator management"
 * @nist ia-5.1 "Password-based authentication"
 * @evidence code, test, policy
 */
class PasswordService {
  /**
   * @nist ia-5.1.a "Enforce minimum password complexity"
   */
  validatePasswordComplexity(password: string): ValidationResult {
    const requirements = {
      minLength: 12, // IA-5.1.a: Minimum length
      requireUppercase: true,
      requireLowercase: true,
      requireNumbers: true,
      requireSpecialChars: true,
    };

    const errors: string[] = [];

    if (password.length < requirements.minLength) {
      errors.push(`Minimum length: ${requirements.minLength}`);
    }
    if (!/[A-Z]/.test(password)) {
      errors.push("Must contain uppercase letter");
    }
    if (!/[a-z]/.test(password)) {
      errors.push("Must contain lowercase letter");
    }
    if (!/[0-9]/.test(password)) {
      errors.push("Must contain number");
    }
    if (!/[^A-Za-z0-9]/.test(password)) {
      errors.push("Must contain special character");
    }

    return { isValid: errors.length === 0, errors };
  }

  /**
   * @nist ia-5.1.h "Employ automated tools to assist in enforcing restrictions"
   */
  async checkPasswordBreaches(password: string): Promise<boolean> {
    // Check against Have I Been Pwned API
    const hash = sha1(password);
    const prefix = hash.substring(0, 5);
    const suffix = hash.substring(5);

    const response = await fetch(
      `https://api.pwnedpasswords.com/range/${prefix}`
    );
    const hashes = await response.text();

    return hashes.includes(suffix.toUpperCase());
  }

  /**
   * @nist ia-5.1.e "Establish minimum and maximum lifetime restrictions"
   */
  async enforcePasswordExpiration(userId: string): Promise<void> {
    const user = await this.userRepository.findById(userId);
    const passwordAge = Date.now() - user.passwordChangedAt.getTime();
    const MAX_AGE_DAYS = 90;

    if (passwordAge > MAX_AGE_DAYS * 24 * 60 * 60 * 1000) {
      await this.flagPasswordExpired(user);
      await this.notifyUser(user, "Password expired - please reset");
    }
  }
}
```

**Audit & Accountability (AU Family):**

```typescript
// AU-2: Audit Events
/**
 * @nist au-2 "Audit events"
 * @nist au-3 "Content of audit records"
 * @nist au-6 "Audit review, analysis, and reporting"
 * @evidence code, automation, monitoring
 */
class AuditService {
  /**
   * @nist au-2.a "Identify types of events to be logged"
   */
  private readonly AUDITABLE_EVENTS = [
    "auth.login",
    "auth.logout",
    "auth.failed",
    "access.granted",
    "access.denied",
    "data.created",
    "data.modified",
    "data.deleted",
    "config.changed",
    "privilege.escalation",
  ];

  /**
   * @nist au-3.a "Ensure audit records contain information"
   */
  async record(
    eventType: string,
    details: Record<string, any>
  ): Promise<void> {
    if (!this.AUDITABLE_EVENTS.includes(eventType)) {
      return; // Only log specified events
    }

    const auditRecord: AuditRecord = {
      // AU-3.a: Event type
      type: eventType,

      // AU-3.b: Time/date
      timestamp: new Date().toISOString(),

      // AU-3.c: Where event occurred
      source: {
        service: process.env.SERVICE_NAME,
        host: os.hostname(),
        ip: details.ip,
      },

      // AU-3.d: Outcome
      outcome: details.success ? "success" : "failure",

      // AU-3.e: Subject identity
      subject: {
        userId: details.userId,
        username: details.username,
        sessionId: details.sessionId,
      },

      // Additional context
      details: this.sanitizeDetails(details),
    };

    // Store immutably
    await this.storage.append(auditRecord);

    // AU-6: Real-time analysis for security incidents
    if (this.isSecurityEvent(eventType)) {
      await this.securityMonitor.analyze(auditRecord);
    }
  }

  /**
   * @nist au-6.1 "Automated audit review analysis and reporting"
   */
  async analyzeAuditTrail(): Promise<SecurityReport> {
    const recentLogs = await this.storage.query({
      since: Date.now() - 24 * 60 * 60 * 1000, // Last 24 hours
    });

    // Detect anomalies
    const failedLogins = recentLogs.filter(
      (log) => log.type === "auth.failed"
    );
    const suspiciousActivity = this.detectBruteForce(failedLogins);

    if (suspiciousActivity.length > 0) {
      await this.alertSecurityTeam(suspiciousActivity);
    }

    return {
      totalEvents: recentLogs.length,
      securityEvents: suspiciousActivity,
      recommendations: this.generateRecommendations(recentLogs),
    };
  }
}
```

#### 2. Evidence Collection

```typescript
/**
 * Automated evidence harvesting for compliance
 * @nist all-families
 * @evidence automation
 */
class EvidenceCollector {
  async collectEvidence(): Promise<EvidencePackage> {
    return {
      // Code-based evidence
      controlImplementations: await this.scanCodeForNistTags(),

      // Test evidence
      testResults: await this.collectTestResults(),

      // Configuration evidence
      securityConfigs: await this.auditSecurityConfigs(),

      // Operational evidence
      auditLogs: await this.exportAuditLogs(),
      accessReviews: await this.generateAccessReports(),

      // Monitoring evidence
      securityMetrics: await this.collectSecurityMetrics(),

      timestamp: new Date().toISOString(),
    };
  }

  private async scanCodeForNistTags(): Promise<ControlMapping[]> {
    const files = await glob("src/**/*.{ts,js,py}");
    const mappings: ControlMapping[] = [];

    for (const file of files) {
      const content = await fs.readFile(file, "utf8");
      const tags = this.extractNistTags(content);

      for (const tag of tags) {
        mappings.push({
          control: tag.control,
          implementation: tag.description,
          file: file,
          lineNumber: tag.lineNumber,
          evidence: tag.evidenceTypes,
        });
      }
    }

    return mappings;
  }
}
```

#### 3. System Security Plan (SSP) Generation

```typescript
/**
 * Automated SSP generation from code annotations
 * @nist pm-9 "Risk management strategy"
 */
class SSPGenerator {
  async generateSSP(): Promise<SystemSecurityPlan> {
    const evidence = await this.evidenceCollector.collectEvidence();
    const controls = await this.mapToNistControls(evidence);

    return {
      systemInformation: this.getSystemInfo(),
      controlImplementations: controls.map((control) => ({
        controlId: control.id,
        implementationStatus: control.status,
        implementationDetails: control.implementations,
        responsibleRole: control.owner,
        evidence: control.evidence,
      })),
      riskAssessment: await this.generateRiskAssessment(),
      poam: await this.generatePOAM(controls),
      timestamp: new Date().toISOString(),
    };
  }
}
```

### Integration Points

- Links to [Security Practices](../security-practices/SKILL.md) for control implementation
- Links to [Testing Standards](../testing/SKILL.md) for evidence collection
- Links to [Coding Standards](../coding-standards/SKILL.md) for tagging conventions

---

## Level 3: Mastery (Extended Learning)

### Advanced Topics

#### 1. Continuous Compliance Monitoring

```typescript
// Real-time compliance dashboard
class ComplianceMonitor {
  async monitorCompliance(): Promise<ComplianceStatus> {
    return {
      coverage: await this.calculateControlCoverage(),
      gaps: await this.identifyComplianceGaps(),
      risks: await this.assessSecurityRisks(),
      trends: await this.analyzeComplianceTrends(),
    };
  }

  private async calculateControlCoverage(): Promise<CoverageReport> {
    const requiredControls = NIST_800_53_R5_CONTROLS;
    const implementedControls = await this.scanImplementations();

    return {
      total: requiredControls.length,
      implemented: implementedControls.length,
      percentage: (implementedControls.length / requiredControls.length) * 100,
      byFamily: this.groupByFamily(implementedControls),
    };
  }
}
```

#### 2. Automated Control Testing

```yaml
# .github/workflows/nist-compliance.yml
name: NIST Compliance Check

on: [push, pull_request]

jobs:
  compliance-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate NIST Tags
        run: |
          python scripts/validate-nist-tags.py
          if [ $? -ne 0 ]; then
            echo "❌ Invalid NIST tags found"
            exit 1
          fi

      - name: Generate Compliance Report
        run: |
          python scripts/generate-compliance-report.py
          cat compliance-report.md >> $GITHUB_STEP_SUMMARY

      - name: Check Control Coverage
        run: |
          coverage=$(jq '.coverage.percentage' compliance-report.json)
          if (( $(echo "$coverage < 80" | bc -l) )); then
            echo "❌ Control coverage below 80%: $coverage%"
            exit 1
          fi
```

### Resources

#### Essential Reading

- [NIST 800-53r5 Control Catalog](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [NIST Risk Management Framework](https://csrc.nist.gov/projects/risk-management)

#### Tools

- **Compliance Automation**: OpenControl, Compliance-as-Code
- **Evidence Collection**: GRC tools (Vanta, Drata, Secureframe)
- **Audit Tools**: SCAP scanners, OpenSCAP

#### Templates

See `./templates/` for:

- SSP templates
- POAM templates
- Control implementation templates
- Evidence collection checklists

### Scripts

See `./scripts/` for:

- NIST tag validators
- SSP generators
- Evidence collectors
- Compliance reporters

## Examples

### Basic Usage

```python
// TODO: Add basic example for nist-compliance
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for nist-compliance
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how nist-compliance
// works with other systems and services
```

See `examples/nist-compliance/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring nist-compliance functionality
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

- Follow established patterns and conventions for nist-compliance
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

## Bundled Resources

- [Full NIST_IMPLEMENTATION_GUIDE.md](../../docs/nist/NIST_IMPLEMENTATION_GUIDE.md)
- [COMPLIANCE_STANDARDS.md](../../docs/standards/COMPLIANCE_STANDARDS.md)
- [NIST_QUICK_REFERENCE.md](../../docs/nist/NIST_QUICK_REFERENCE.md)
- Control implementation templates in `./templates/`
- Automated compliance scripts in `./scripts/`
- SSP generation tools in `./resources/`
