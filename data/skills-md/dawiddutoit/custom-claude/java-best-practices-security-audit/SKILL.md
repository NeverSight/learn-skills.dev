---
name: java-best-practices-security-audit
description: |
  Performs comprehensive security audits of Java code against OWASP Top 10 and best practices. Use when auditing security, checking for vulnerabilities, analyzing SQL injection risks, preventing XSS attacks, reviewing authentication/authorization, detecting sensitive data exposure, checking dependency vulnerabilities, ensuring OWASP compliance, or hardening Java applications. Works with Java web applications, REST APIs, Spring applications, and any Java codebase.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Java Security Audit

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Requirements](#requirements)
- [Security Audit Checklist](#security-audit-checklist)
- [Output Format](#output-format)
- [Error Handling](#error-handling)

## Purpose

Conducts comprehensive security audits of Java applications, identifying vulnerabilities based on OWASP Top 10, analyzing code for injection flaws, authentication issues, sensitive data exposure, and dependency vulnerabilities. Provides actionable remediation guidance.

## When to Use

Use this skill when you need to:
- Audit Java applications for security vulnerabilities
- Check for SQL injection vulnerabilities
- Detect XSS (Cross-Site Scripting) risks
- Review authentication and authorization implementation
- Identify sensitive data exposure issues
- Scan dependencies for known CVEs
- Ensure OWASP Top 10 compliance
- Review cryptographic implementations
- Check for insecure deserialization
- Audit session management security
- Detect hardcoded credentials or secrets
- Review access control mechanisms
- Perform pre-deployment security validation
- Conduct security code reviews

## Quick Start
Point to any Java codebase for immediate security analysis:

```bash
# Audit entire project
Perform security audit on this Java project

# Audit specific components
Security audit for src/main/java/com/example/controller/

# Check for specific vulnerability
Check for SQL injection vulnerabilities in this codebase
```

## Instructions

### Step 1: Identify Audit Scope
Determine what to audit:

**Full Application Audit:**
- All Java source files
- Configuration files (application.yml, application.properties)
- Dependencies (pom.xml, build.gradle)
- Database access layers
- Authentication/authorization code
- API endpoints and controllers

**Targeted Audit:**
- Specific vulnerability type (SQL injection, XSS, etc.)
- Specific component (authentication, payment processing)
- Recent changes (git diff for new code)

### Step 2: OWASP Top 10 Checklist

#### A01:2021 - Broken Access Control
**What to Check:**
- Authorization checks on every endpoint
- Horizontal privilege escalation (user accessing other user's data)
- Vertical privilege escalation (user accessing admin functions)
- CORS misconfiguration
- Missing function-level access control

**Red Flags:**
```java
// BAD: No authorization check
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).orElseThrow();
}

// BAD: Using user input directly without validation
@GetMapping("/users/{id}/orders")
public List<Order> getOrders(@PathVariable Long id) {
    return orderRepository.findByUserId(id);  // Any user can access any user's orders!
}
```

**Good Patterns:**
```java
@GetMapping("/users/{id}")
@PreAuthorize("#id == authentication.principal.id or hasRole('ADMIN')")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).orElseThrow();
}

@GetMapping("/users/me/orders")
public List<Order> getMyOrders(@AuthenticationPrincipal UserDetails user) {
    return orderRepository.findByUserId(user.getId());
}
```

#### A02:2021 - Cryptographic Failures
**What to Check:**
- Passwords stored in plaintext
- Weak hashing algorithms (MD5, SHA1)
- Sensitive data transmitted over HTTP
- Hardcoded encryption keys
- Sensitive data in logs

**Red Flags:**
```java
// BAD: Plaintext password
user.setPassword(request.getPassword());

// BAD: Weak hashing
String hash = DigestUtils.md5Hex(password);

// BAD: Hardcoded secret
String secret = "mySecretKey123";
```

**Good Patterns:**
```java
// Use BCrypt for password hashing
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(12);
}

user.setPassword(passwordEncoder.encode(request.getPassword()));

// Externalize secrets
@Value("${jwt.secret}")
private String jwtSecret;

// Encrypt sensitive data at rest
@Convert(converter = SensitiveDataConverter.class)
private String socialSecurityNumber;
```

#### A03:2021 - Injection
**What to Check:**
- SQL injection in dynamic queries
- Command injection in Runtime.exec()
- LDAP injection
- XML injection
- Expression Language injection

**SQL Injection Red Flags:**
```java
// BAD: String concatenation in SQL
String sql = "SELECT * FROM users WHERE email = '" + email + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(sql);

// BAD: Using + in JPA queries
String jpql = "SELECT u FROM User u WHERE u.email = '" + email + "'";
Query query = em.createQuery(jpql);

// BAD: String format in queries
String sql = String.format("SELECT * FROM users WHERE id = %s", userId);
```

**Good Patterns:**
```java
// GOOD: PreparedStatement with parameters
String sql = "SELECT * FROM users WHERE email = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setString(1, email);
ResultSet rs = pstmt.executeQuery();

// GOOD: Named parameters in JPA
@Query("SELECT u FROM User u WHERE u.email = :email")
User findByEmail(@Param("email") String email);

// GOOD: Spring Data JPA method names
User findByEmail(String email);
```

#### A04:2021 - Insecure Design
**What to Check:**
- Missing rate limiting
- No account lockout after failed attempts
- Weak session management
- Missing security headers
- Inadequate logging and monitoring

**Red Flags:**
```java
// BAD: No rate limiting on sensitive endpoints
@PostMapping("/login")
public ResponseEntity<?> login(@RequestBody LoginRequest request) {
    // Attacker can brute force passwords
    return authenticate(request);
}

// BAD: Predictable session IDs
String sessionId = userId + "_" + timestamp;
```

**Good Patterns:**
```java
// Rate limiting with bucket4j
@PostMapping("/login")
@RateLimiter(name = "loginRateLimit", fallbackMethod = "loginFallback")
public ResponseEntity<?> login(@RequestBody LoginRequest request) {
    return authenticate(request);
}

// Account lockout
@Service
public class LoginAttemptService {
    private final LoadingCache<String, Integer> attemptsCache;

    public void loginFailed(String username) {
        int attempts = attemptsCache.get(username);
        attemptsCache.put(username, attempts + 1);
    }

    public boolean isBlocked(String username) {
        return attemptsCache.get(username) >= MAX_ATTEMPTS;
    }
}
```

#### A05:2021 - Security Misconfiguration
**What to Check:**
- Default credentials still active
- Unnecessary features enabled
- Stack traces exposed to users
- Missing security headers
- Outdated framework versions
- Excessive error details in responses

**Red Flags:**
```java
// BAD: Detailed error messages to clients
catch (Exception e) {
    return ResponseEntity.status(500).body(e.getMessage());
}

// BAD: Debug mode in production
spring.devtools.enabled=true

// BAD: Allowing all CORS origins
@CrossOrigin(origins = "*")
```

**Good Patterns:**
```java
// Security headers configuration
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .headers(headers -> headers
                .xssProtection(xss -> xss.headerValue(XXssProtectionHeaderWriter.HeaderValue.ENABLED_MODE_BLOCK))
                .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
                .frameOptions(frame -> frame.deny())
                .httpStrictTransportSecurity(hsts -> hsts
                    .includeSubDomains(true)
                    .maxAgeInSeconds(31536000))
            );
        return http.build();
    }
}

// Generic error responses
@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handleException(Exception e) {
    log.error("Error occurred", e);  // Log details server-side
    return ResponseEntity.status(500)
        .body(new ErrorResponse("An error occurred"));  // Generic message to client
}
```

#### A06:2021 - Vulnerable and Outdated Components
**What to Check:**
- Outdated dependencies with known CVEs
- Unused dependencies
- Transitive dependency vulnerabilities

**How to Check:**
```bash
# Maven: Check for vulnerabilities
mvn dependency-check:check

# Gradle: Using OWASP dependency check plugin
gradle dependencyCheckAnalyze

# Check for outdated versions
mvn versions:display-dependency-updates
```

**Good Practices:**
```xml
<!-- Keep dependencies updated -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
    <version>3.2.0</version>  <!-- Use latest stable version -->
</dependency>

<!-- Use dependency management -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.2.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

#### A07:2021 - Identification and Authentication Failures
**What to Check:**
- Weak password requirements
- Missing multi-factor authentication
- Exposed session IDs in URLs
- Missing session timeout
- Insecure password recovery

**Red Flags:**
```java
// BAD: No password complexity requirements
if (password.length() < 6) {
    throw new IllegalArgumentException("Password too short");
}

// BAD: Session ID in URL
return "redirect:/dashboard?sessionId=" + session.getId();

// BAD: No session timeout
server.servlet.session.timeout=-1
```

**Good Patterns:**
```java
// Strong password validation
@Component
public class PasswordValidator {
    private static final Pattern PASSWORD_PATTERN =
        Pattern.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{12,}$");

    public boolean isValid(String password) {
        return PASSWORD_PATTERN.matcher(password).matches();
    }
}

// Session configuration
server.servlet.session.timeout=30m
server.servlet.session.cookie.http-only=true
server.servlet.session.cookie.secure=true
server.servlet.session.cookie.same-site=strict

// Password reset with token
@Service
public class PasswordResetService {
    public String createResetToken(String email) {
        String token = UUID.randomUUID().toString();
        PasswordResetToken resetToken = new PasswordResetToken(
            token,
            findUserByEmail(email),
            LocalDateTime.now().plusHours(1)  // Expiry
        );
        resetTokenRepository.save(resetToken);
        return token;
    }
}
```

#### A08:2021 - Software and Data Integrity Failures
**What to Check:**
- Unsigned/unverified packages
- Insecure deserialization
- Missing integrity checks
- Auto-update without verification

**Red Flags:**
```java
// BAD: Unsafe deserialization
ObjectInputStream ois = new ObjectInputStream(untrustedInput);
MyObject obj = (MyObject) ois.readObject();

// BAD: Executing unsigned code
Runtime.getRuntime().exec(downloadedScript);
```

**Good Patterns:**
```java
// Use JSON instead of Java serialization
ObjectMapper mapper = new ObjectMapper();
MyObject obj = mapper.readValue(jsonInput, MyObject.class);

// Verify signatures
public boolean verifySignature(byte[] data, byte[] signature, PublicKey publicKey) {
    Signature sig = Signature.getInstance("SHA256withRSA");
    sig.initVerify(publicKey);
    sig.update(data);
    return sig.verify(signature);
}
```

#### A09:2021 - Security Logging and Monitoring Failures
**What to Check:**
- Missing audit logs for sensitive operations
- No alerting on suspicious activities
- Sensitive data in logs
- Insufficient log retention

**Red Flags:**
```java
// BAD: Logging sensitive data
log.info("User login: username={}, password={}", username, password);

// BAD: No audit trail for admin actions
public void deleteUser(Long id) {
    userRepository.deleteById(id);  // Who deleted? When? Why?
}
```

**Good Patterns:**
```java
// Audit logging
@Aspect
@Component
@Slf4j
public class AuditAspect {
    @Around("@annotation(Auditable)")
    public Object auditMethod(ProceedingJoinPoint pjp) throws Throwable {
        String username = SecurityContextHolder.getContext()
            .getAuthentication().getName();
        String method = pjp.getSignature().getName();
        String args = Arrays.toString(pjp.getArgs());

        log.info("AUDIT: user={}, method={}, args={}",
            username, method, maskSensitiveData(args));

        try {
            Object result = pjp.proceed();
            log.info("AUDIT: user={}, method={}, status=SUCCESS",
                username, method);
            return result;
        } catch (Exception e) {
            log.error("AUDIT: user={}, method={}, status=FAILURE, error={}",
                username, method, e.getMessage());
            throw e;
        }
    }
}

@Service
public class UserService {
    @Auditable
    @PreAuthorize("hasRole('ADMIN')")
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
}

// Mask sensitive data
private String maskSensitiveData(String data) {
    return data.replaceAll("password=\\w+", "password=***")
               .replaceAll("ssn=\\d{9}", "ssn=***");
}
```

#### A10:2021 - Server-Side Request Forgery (SSRF)
**What to Check:**
- User-controlled URLs in HTTP requests
- No URL validation/allowlisting
- Internal network access from web tier

**Red Flags:**
```java
// BAD: User-controlled URL without validation
@GetMapping("/fetch")
public String fetchUrl(@RequestParam String url) {
    RestTemplate restTemplate = new RestTemplate();
    return restTemplate.getForObject(url, String.class);  // SSRF vulnerability!
}
```

**Good Patterns:**
```java
// URL validation with allowlist
@Service
public class UrlValidator {
    private static final Set<String> ALLOWED_DOMAINS = Set.of(
        "api.example.com",
        "cdn.example.com"
    );

    public boolean isAllowed(String url) {
        try {
            URL urlObj = new URL(url);
            String host = urlObj.getHost();

            // Check against allowlist
            if (!ALLOWED_DOMAINS.contains(host)) {
                return false;
            }

            // Prevent internal network access
            InetAddress address = InetAddress.getByName(host);
            if (address.isLoopbackAddress() ||
                address.isLinkLocalAddress() ||
                address.isSiteLocalAddress()) {
                return false;
            }

            return true;
        } catch (Exception e) {
            return false;
        }
    }
}

@GetMapping("/fetch")
public String fetchUrl(@RequestParam String url) {
    if (!urlValidator.isAllowed(url)) {
        throw new SecurityException("URL not allowed");
    }
    return restTemplate.getForObject(url, String.class);
}
```

### Step 3: Additional Security Checks

#### XSS (Cross-Site Scripting) Prevention
**Check for:**
- Unescaped user input in HTML
- Missing Content Security Policy
- innerHTML usage with user data

**Good Patterns:**
```java
// Use templating engines with auto-escaping (Thymeleaf)
<p th:text="${userInput}"></p>  <!-- Automatically escaped -->

// For JSON APIs, proper Content-Type prevents XSS
@GetMapping("/api/data")
public ResponseEntity<DataResponse> getData() {
    return ResponseEntity.ok()
        .contentType(MediaType.APPLICATION_JSON)
        .body(data);
}

// Content Security Policy header
content-security-policy: default-src 'self'; script-src 'self' 'nonce-{random}'
```

#### CSRF (Cross-Site Request Forgery) Prevention
```java
// Spring Security enables CSRF protection by default
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf
                .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
            );
        return http.build();
    }
}

// For stateless REST APIs, disable CSRF (use JWT tokens instead)
http.csrf(csrf -> csrf.disable())
    .sessionManagement(session ->
        session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
    );
```

#### Path Traversal Prevention
```java
// BAD: User input in file path
@GetMapping("/files/{filename}")
public ResponseEntity<Resource> getFile(@PathVariable String filename) {
    Path path = Paths.get("/uploads/" + filename);  // Vulnerable!
    // User could use "../../../etc/passwd"
}

// GOOD: Validate and sanitize
@GetMapping("/files/{filename}")
public ResponseEntity<Resource> getFile(@PathVariable String filename) {
    // Remove any path separators
    String sanitized = filename.replaceAll("[^a-zA-Z0-9.-]", "");

    Path path = Paths.get("/uploads/").resolve(sanitized).normalize();

    // Ensure resolved path is still within uploads directory
    if (!path.startsWith("/uploads/")) {
        throw new SecurityException("Invalid file path");
    }

    Resource resource = new FileSystemResource(path);
    if (!resource.exists()) {
        throw new FileNotFoundException();
    }

    return ResponseEntity.ok(resource);
}
```

### Step 4: Dependency Vulnerability Scan
Use automated tools to check dependencies:

```bash
# OWASP Dependency Check
mvn org.owasp:dependency-check-maven:check

# Snyk
snyk test

# GitHub Dependabot (in CI/CD)
# Automatically creates PRs for vulnerable dependencies
```

### Step 5: Generate Security Report
Organize findings by severity:

**CRITICAL** - Immediate action required:
- SQL injection vulnerabilities
- Authentication bypass
- Remote code execution
- Sensitive data exposure

**HIGH** - Fix soon:
- Missing authorization checks
- Weak cryptography
- Known CVEs in dependencies

**MEDIUM** - Plan to fix:
- Missing security headers
- Insufficient logging
- Session management issues

**LOW** - Improve when possible:
- Code quality issues
- Documentation gaps

## Examples

### Example 1: SQL Injection Vulnerability

**Vulnerable Code:**
```java
@RestController
public class UserController {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @GetMapping("/users/search")
    public List<User> searchUsers(@RequestParam String name) {
        String sql = "SELECT * FROM users WHERE name LIKE '%" + name + "%'";
        return jdbcTemplate.query(sql, new UserRowMapper());
    }
}
```

**Security Audit Report:**
```markdown
## CRITICAL: SQL Injection Vulnerability

**Location:** UserController.java:12
**Severity:** CRITICAL
**CWE:** CWE-89 (SQL Injection)
**OWASP:** A03:2021 - Injection

### Vulnerability
User input `name` is directly concatenated into SQL query without sanitization or parameterization, allowing SQL injection attacks.

### Proof of Concept
```bash
# Attacker can inject SQL:
curl "http://localhost:8080/users/search?name=test' OR '1'='1"

# This executes:
SELECT * FROM users WHERE name LIKE '%test' OR '1'='1%'
# Returns all users in database

# Worse:
curl "http://localhost:8080/users/search?name=test'; DROP TABLE users; --"
# This executes:
SELECT * FROM users WHERE name LIKE '%test'; DROP TABLE users; --%'
# Deletes users table!
```

### Impact
- Complete database compromise
- Data exfiltration
- Data modification/deletion
- Potential server compromise

### Remediation
Use parameterized queries:

```java
@GetMapping("/users/search")
public List<User> searchUsers(@RequestParam String name) {
    String sql = "SELECT * FROM users WHERE name LIKE ?";
    return jdbcTemplate.query(sql, new UserRowMapper(), "%" + name + "%");
}
```

Or use Spring Data JPA:

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    @Query("SELECT u FROM User u WHERE u.name LIKE %:name%")
    List<User> searchByName(@Param("name") String name);
}
```

### Verification
```bash
# After fix, SQL injection attempts fail safely
curl "http://localhost:8080/users/search?name=test' OR '1'='1"
# Returns: [] (no results, injection neutralized)
```
```

### Example 2: Missing Authorization Check

**Vulnerable Code:**
```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    @Autowired
    private OrderRepository orderRepository;

    @GetMapping("/{orderId}")
    public Order getOrder(@PathVariable Long orderId) {
        return orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));
    }
}
```

**Security Audit Report:**
```markdown
## HIGH: Missing Authorization Check (IDOR)

**Location:** OrderController.java:8
**Severity:** HIGH
**CWE:** CWE-639 (Authorization Bypass Through User-Controlled Key)
**OWASP:** A01:2021 - Broken Access Control

### Vulnerability
Insecure Direct Object Reference (IDOR): Any authenticated user can access any order by simply changing the orderId in the URL. No verification that the order belongs to the requesting user.

### Proof of Concept
```bash
# User A (id=1) creates order 100
POST /api/orders
{ "items": [...] }
# Response: { "orderId": 100, "userId": 1 }

# User B (id=2) can access User A's order
GET /api/orders/100
# Response: { "orderId": 100, "userId": 1, "items": [...] }
# SUCCESS - User B sees User A's order!
```

### Impact
- Unauthorized data access
- Privacy violation
- Potential data manipulation if PUT/DELETE endpoints have same issue

### Remediation

**Option 1: Check ownership in service layer**
```java
@Service
public class OrderService {
    public Order getOrder(Long orderId, Long requestingUserId) {
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        if (!order.getUserId().equals(requestingUserId)) {
            throw new AccessDeniedException("Not authorized to view this order");
        }

        return order;
    }
}

@GetMapping("/{orderId}")
public Order getOrder(
        @PathVariable Long orderId,
        @AuthenticationPrincipal UserDetails user) {
    Long userId = ((CustomUserDetails) user).getId();
    return orderService.getOrder(orderId, userId);
}
```

**Option 2: Use Spring Security @PreAuthorize**
```java
@GetMapping("/{orderId}")
@PreAuthorize("@orderSecurityService.canAccessOrder(#orderId, authentication.principal.id)")
public Order getOrder(@PathVariable Long orderId) {
    return orderRepository.findById(orderId).orElseThrow();
}

@Service("orderSecurityService")
public class OrderSecurityService {
    public boolean canAccessOrder(Long orderId, Long userId) {
        return orderRepository.findById(orderId)
            .map(order -> order.getUserId().equals(userId))
            .orElse(false);
    }
}
```

**Option 3: Query by user ID instead**
```java
@GetMapping("/my-orders/{orderId}")
public Order getMyOrder(
        @PathVariable Long orderId,
        @AuthenticationPrincipal UserDetails user) {
    Long userId = ((CustomUserDetails) user).getId();
    return orderRepository.findByIdAndUserId(orderId, userId)
        .orElseThrow(() -> new OrderNotFoundException(orderId));
}
```

### Verification
```bash
# User B tries to access User A's order
GET /api/orders/100
Authorization: Bearer {user-b-token}

# Response: 403 Forbidden
{ "error": "Not authorized to view this order" }
```
```

## Requirements

### Tools
```bash
# Static analysis
spotbugs                    # Bug detection
pmd                         # Code analysis
checkstyle                  # Style checking
findsecbugs                 # Security-focused SpotBugs plugin

# Dependency scanning
mvn dependency-check:check  # OWASP Dependency Check
snyk test                   # Snyk vulnerability scanner
npm audit                   # For JavaScript dependencies

# Dynamic analysis
zap                         # OWASP ZAP proxy
burp suite                  # Web application testing
```

### Configuration Files
**SpotBugs with FindSecBugs:**
```xml
<plugin>
    <groupId>com.github.spotbugs</groupId>
    <artifactId>spotbugs-maven-plugin</artifactId>
    <version>4.7.3.6</version>
    <configuration>
        <plugins>
            <plugin>
                <groupId>com.h3xstream.findsecbugs</groupId>
                <artifactId>findsecbugs-plugin</artifactId>
                <version>1.12.0</version>
            </plugin>
        </plugins>
    </configuration>
</plugin>
```

## Security Audit Checklist

**Input Validation:**
- [ ] All user input validated and sanitized
- [ ] Parameterized queries used (no string concatenation)
- [ ] File upload restrictions (type, size)
- [ ] Path traversal prevention

**Authentication:**
- [ ] Strong password requirements enforced
- [ ] Password hashing with BCrypt/Argon2
- [ ] Multi-factor authentication available
- [ ] Account lockout after failed attempts
- [ ] Secure password reset mechanism

**Authorization:**
- [ ] Authorization checks on all endpoints
- [ ] Horizontal privilege escalation prevented
- [ ] Vertical privilege escalation prevented
- [ ] Role-based access control implemented

**Session Management:**
- [ ] Secure session cookies (HttpOnly, Secure, SameSite)
- [ ] Session timeout configured
- [ ] Session invalidation on logout
- [ ] No session ID in URL

**Cryptography:**
- [ ] Strong algorithms (AES-256, RSA-2048+)
- [ ] Secrets externalized (not hardcoded)
- [ ] HTTPS enforced
- [ ] Sensitive data encrypted at rest

**Error Handling:**
- [ ] Generic error messages to users
- [ ] Detailed errors logged server-side only
- [ ] No stack traces exposed
- [ ] Proper exception handling (no empty catches)

**Logging & Monitoring:**
- [ ] Security events logged (login, access control failures)
- [ ] No sensitive data in logs
- [ ] Log integrity protected
- [ ] Alerting on suspicious activities

**Dependencies:**
- [ ] All dependencies up to date
- [ ] No known CVEs in dependencies
- [ ] Unused dependencies removed
- [ ] Dependency scanning in CI/CD

**Configuration:**
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] CORS properly configured
- [ ] Debug mode disabled in production
- [ ] Unnecessary features disabled

## Output Format

Provide structured security audit report:

```markdown
# Security Audit Report

## Executive Summary
- Files audited: X
- Vulnerabilities found: X (Critical: X, High: X, Medium: X, Low: X)
- OWASP Top 10 compliance: X/10

## Critical Vulnerabilities (Fix Immediately)
### 1. SQL Injection in UserController
- Location: UserController.java:45
- CWE: CWE-89
- Impact: Complete database compromise
- Remediation: [detailed fix]

## High Priority Vulnerabilities (Fix This Sprint)
[...]

## Medium Priority Issues (Plan to Fix)
[...]

## Low Priority Issues (Technical Debt)
[...]

## Positive Findings
[List security controls that are correctly implemented]

## Recommendations
1. Immediate actions
2. Short-term improvements
3. Long-term enhancements

## Compliance Status
- OWASP Top 10: [status for each]
- PCI-DSS: [if applicable]
- GDPR: [if applicable]
```

## Error Handling

If audit cannot be completed:

1. **Large codebase:** Prioritize high-risk areas (auth, data access, API endpoints)
2. **Missing context:** Request architecture diagrams, data flow diagrams
3. **Framework-specific:** Ask for framework version and security configuration
4. **Access to dependencies:** Request dependency tree output

Always provide best-effort analysis with clear scope limitations noted in report.
