---
name: web-security-expert
description: Expert knowledge of web application security including OWASP Top 10 vulnerabilities, input validation, authentication, authorization, API security, secrets management, security headers, and secure coding practices. Use when implementing security features, reviewing code for vulnerabilities, adding authentication, validating user input, or addressing security concerns.
---

# Web Security Expert

This skill provides comprehensive expert knowledge of web application security for Node.js/Express applications, with emphasis on preventing common vulnerabilities, implementing defense-in-depth strategies, and following security best practices.

## OWASP Top 10 Vulnerabilities

### 1. Broken Access Control

**What it is**: Users can access resources or perform actions they shouldn't be authorized for.

**Examples**:
- Accessing other users' data by changing URL parameters
- Performing admin actions without admin privileges
- Bypassing authentication by directly accessing protected pages

**Prevention**:

```javascript
// BAD - No authorization check
app.get('/api/users/:id/profile', async (req, res) => {
  const profile = await User.findById(req.params.id);
  res.json(profile); // Any user can access any profile!
});

// GOOD - Check authorization
app.get('/api/users/:id/profile', authenticate, async (req, res) => {
  // Verify user can only access their own profile
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Access denied' });
  }

  const profile = await User.findById(req.params.id);
  res.json(profile);
});

// BETTER - Middleware for resource ownership
const requireOwnership = (resourceParam = 'id') => {
  return (req, res, next) => {
    if (req.user.id !== req.params[resourceParam] && !req.user.isAdmin) {
      return res.status(403).json({ error: 'Access denied' });
    }
    next();
  };
};

app.get('/api/users/:id/profile', authenticate, requireOwnership(), getProfile);
```

**Best Practices**:
- Default deny all access, explicitly grant permissions
- Verify authorization on every request (server-side)
- Don't rely on client-side access control
- Use role-based access control (RBAC) or attribute-based access control (ABAC)
- Log access control failures for monitoring

### 2. Cryptographic Failures

**What it is**: Exposure of sensitive data due to weak or missing encryption.

**Examples**:
- Storing passwords in plain text
- Using weak hashing algorithms (MD5, SHA1)
- Transmitting sensitive data over HTTP
- Hardcoding encryption keys

**Prevention**:

```javascript
const bcrypt = require('bcrypt');
const crypto = require('crypto');

// Password Hashing (GOOD)
const hashPassword = async (password) => {
  const saltRounds = 12; // Increase for more security (slower)
  return await bcrypt.hash(password, saltRounds);
};

const verifyPassword = async (password, hash) => {
  return await bcrypt.compare(password, hash);
};

// User registration
app.post('/api/register', async (req, res) => {
  const { email, password } = req.body;

  // Validate password strength
  if (password.length < 12) {
    return res.status(400).json({
      error: 'Password must be at least 12 characters'
    });
  }

  const hashedPassword = await hashPassword(password);

  const user = await User.create({
    email,
    password: hashedPassword // NEVER store plain text
  });

  res.status(201).json({ id: user.id });
});

// Encrypting Sensitive Data
const algorithm = 'aes-256-gcm';
const key = Buffer.from(process.env.ENCRYPTION_KEY, 'hex'); // 32 bytes

const encrypt = (text) => {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algorithm, key, iv);

  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag();

  return {
    encrypted,
    iv: iv.toString('hex'),
    authTag: authTag.toString('hex')
  };
};

const decrypt = (encrypted, iv, authTag) => {
  const decipher = crypto.createDecipheriv(
    algorithm,
    key,
    Buffer.from(iv, 'hex')
  );

  decipher.setAuthTag(Buffer.from(authTag, 'hex'));

  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
};
```

**Best Practices**:
- Use bcrypt, scrypt, or Argon2 for password hashing
- Never use MD5 or SHA1 for passwords
- Use TLS/SSL for all data in transit
- Encrypt sensitive data at rest
- Store encryption keys securely (environment variables, key management services)
- Use strong random values for tokens and IDs
- Implement key rotation

### 3. Injection Attacks

**What it is**: Untrusted data is sent to an interpreter as part of a command or query.

**Types**:
- SQL Injection
- NoSQL Injection
- Command Injection
- LDAP Injection
- XPath Injection

**SQL Injection Prevention**:

```javascript
// BAD - Vulnerable to SQL injection
app.get('/api/users', async (req, res) => {
  const username = req.query.username;
  const query = `SELECT * FROM users WHERE username = '${username}'`;
  // If username = "admin' OR '1'='1", returns all users!
  const users = await db.query(query);
  res.json(users);
});

// GOOD - Use parameterized queries
app.get('/api/users', async (req, res) => {
  const username = req.query.username;
  const query = 'SELECT * FROM users WHERE username = $1';
  const users = await db.query(query, [username]);
  res.json(users);
});

// GOOD - Use ORM/Query Builder
app.get('/api/users', async (req, res) => {
  const username = req.query.username;
  const users = await User.findAll({
    where: { username } // Sequelize automatically parameterizes
  });
  res.json(users);
});
```

**NoSQL Injection Prevention**:

```javascript
// BAD - Vulnerable to NoSQL injection
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;
  // If req.body = {username: {$ne: null}, password: {$ne: null}}
  // This bypasses authentication!
  const user = await User.findOne({ username, password });
});

// GOOD - Validate input types
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;

  // Ensure inputs are strings
  if (typeof username !== 'string' || typeof password !== 'string') {
    return res.status(400).json({ error: 'Invalid input' });
  }

  const user = await User.findOne({ username });

  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  res.json({ token: generateToken(user) });
});
```

**Command Injection Prevention**:

```javascript
// BAD - Vulnerable to command injection
app.get('/api/ping', (req, res) => {
  const host = req.query.host;
  const { exec } = require('child_process');
  exec(`ping -c 4 ${host}`, (error, stdout) => {
    // If host = "google.com; rm -rf /", executes both commands!
    res.send(stdout);
  });
});

// GOOD - Validate input and use safe alternatives
app.get('/api/ping', (req, res) => {
  const host = req.query.host;

  // Validate hostname format
  const hostnameRegex = /^[a-zA-Z0-9.-]+$/;
  if (!hostnameRegex.test(host)) {
    return res.status(400).json({ error: 'Invalid hostname' });
  }

  // Use parameterized execution
  const { execFile } = require('child_process');
  execFile('ping', ['-c', '4', host], (error, stdout) => {
    if (error) {
      return res.status(500).json({ error: 'Ping failed' });
    }
    res.send(stdout);
  });
});

// BETTER - Use a library instead
const ping = require('ping');

app.get('/api/ping', async (req, res) => {
  const host = req.query.host;

  // Validate hostname
  if (!isValidHostname(host)) {
    return res.status(400).json({ error: 'Invalid hostname' });
  }

  const result = await ping.promise.probe(host);
  res.json(result);
});
```

**Best Practices**:
- Always use parameterized queries or prepared statements
- Validate input data types
- Use ORMs with built-in protection
- Never execute user input as code
- Use allow-lists for validation when possible
- Escape special characters when allow-lists aren't feasible

### 4. Insecure Design

**What it is**: Missing or ineffective security controls by design.

**Examples**:
- No rate limiting on sensitive endpoints
- Missing multi-factor authentication
- Weak password requirements
- No account lockout after failed logins

**Prevention**:

```javascript
const rateLimit = require('express-rate-limit');
const MongoStore = require('rate-limit-mongo');

// Rate limiting for authentication endpoints
const loginLimiter = rateLimit({
  store: new MongoStore({
    uri: process.env.MONGO_URI,
    collectionName: 'rate-limit'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: true, // Don't count successful logins
  skipFailedRequests: false
});

// Account lockout tracking
const loginAttempts = new Map();

app.post('/api/login', loginLimiter, async (req, res) => {
  const { email, password } = req.body;

  // Check if account is locked
  const attempts = loginAttempts.get(email) || { count: 0, lockedUntil: null };

  if (attempts.lockedUntil && attempts.lockedUntil > Date.now()) {
    const minutesLeft = Math.ceil((attempts.lockedUntil - Date.now()) / 60000);
    return res.status(423).json({
      error: `Account locked. Try again in ${minutesLeft} minutes`
    });
  }

  const user = await User.findOne({ email });

  if (!user || !(await bcrypt.compare(password, user.password))) {
    // Increment failed attempts
    attempts.count += 1;

    // Lock account after 5 failed attempts for 30 minutes
    if (attempts.count >= 5) {
      attempts.lockedUntil = Date.now() + 30 * 60 * 1000;
    }

    loginAttempts.set(email, attempts);

    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Reset attempts on successful login
  loginAttempts.delete(email);

  const token = generateToken(user);
  res.json({ token });
});

// Password strength validation
const validatePassword = (password) => {
  const errors = [];

  if (password.length < 12) {
    errors.push('Password must be at least 12 characters');
  }

  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  }

  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  }

  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain at least one number');
  }

  if (!/[^A-Za-z0-9]/.test(password)) {
    errors.push('Password must contain at least one special character');
  }

  // Check against common passwords
  const commonPasswords = ['password123', '12345678', 'qwerty123'];
  if (commonPasswords.includes(password.toLowerCase())) {
    errors.push('Password is too common');
  }

  return errors;
};
```

**Best Practices**:
- Implement rate limiting on all sensitive endpoints
- Require strong passwords (length, complexity, no common passwords)
- Implement account lockout after failed login attempts
- Use multi-factor authentication for sensitive operations
- Design with "security by default" principle
- Implement proper session management
- Use CAPTCHA for public forms

### 5. Security Misconfiguration

**What it is**: Missing security hardening, default configurations, verbose error messages.

**Examples**:
- Default admin passwords
- Directory listing enabled
- Detailed error messages in production
- Unnecessary features enabled

**Prevention**:

```javascript
const express = require('express');
const helmet = require('helmet');
const app = express();

// Security headers with Helmet
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"], // Avoid unsafe-inline in production
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"]
    }
  },
  hsts: {
    maxAge: 31536000, // 1 year
    includeSubDomains: true,
    preload: true
  },
  referrerPolicy: {
    policy: 'strict-origin-when-cross-origin'
  },
  noSniff: true, // X-Content-Type-Options
  xssFilter: true, // X-XSS-Protection
  hidePoweredBy: true // Remove X-Powered-By header
}));

// Disable directory listing
app.use(express.static('public', {
  dotfiles: 'deny',
  index: false // Disable directory indexing
}));

// Environment-based error handling
app.use((err, req, res, next) => {
  // Log full error server-side
  console.error('Error:', err);

  // Send sanitized error to client
  const isProd = process.env.NODE_ENV === 'production';

  res.status(err.status || 500).json({
    error: isProd ? 'Internal Server Error' : err.message,
    // Never expose stack traces in production
    ...(isProd ? {} : { stack: err.stack })
  });
});

// Disable unnecessary HTTP methods
app.use((req, res, next) => {
  const allowedMethods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'];

  if (!allowedMethods.includes(req.method)) {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  next();
});

// Remove fingerprinting headers
app.disable('x-powered-by');
```

**Best Practices**:
- Use security headers (Helmet)
- Disable directory listing
- Remove version disclosure headers
- Use environment variables for configuration
- Never use default credentials
- Disable unnecessary features and endpoints
- Keep dependencies updated
- Run security scans regularly

### 6. Vulnerable and Outdated Components

**What it is**: Using libraries with known vulnerabilities.

**Prevention**:

```bash
# Regular dependency auditing
npm audit
npm audit fix

# Check for outdated packages
npm outdated

# Use automated tools
npm install -g npm-check-updates
ncu -u  # Update package.json
npm install

# Use Snyk for continuous monitoring
npm install -g snyk
snyk test
snyk monitor
```

**Dependency management**:

```javascript
// package.json - Use exact versions or compatible ranges carefully
{
  "dependencies": {
    "express": "^5.2.1",  // Compatible updates (minor/patch)
    "helmet": "~7.1.0",   // Patch updates only
    "axios": "1.13.2"     // Exact version
  }
}
```

**Best Practices**:
- Run `npm audit` regularly
- Update dependencies frequently
- Remove unused dependencies
- Use tools like Snyk or Dependabot
- Review CVE databases
- Monitor security advisories
- Use lock files (package-lock.json)

### 7. Identification and Authentication Failures

**What it is**: Broken authentication and session management.

**Examples**:
- Weak password policies
- Session fixation
- Credential stuffing vulnerabilities
- Missing MFA

**Prevention**:

```javascript
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

// Generate secure tokens
const generateSecureToken = () => {
  return crypto.randomBytes(32).toString('hex');
};

// JWT-based authentication
const JWT_SECRET = process.env.JWT_SECRET; // Store securely
const JWT_EXPIRES_IN = '1h'; // Short-lived tokens

const generateToken = (user) => {
  return jwt.sign(
    {
      id: user.id,
      email: user.email,
      role: user.role
    },
    JWT_SECRET,
    {
      expiresIn: JWT_EXPIRES_IN,
      issuer: 'myapp',
      audience: 'myapp-users'
    }
  );
};

const verifyToken = (token) => {
  try {
    return jwt.verify(token, JWT_SECRET, {
      issuer: 'myapp',
      audience: 'myapp-users'
    });
  } catch (error) {
    return null;
  }
};

// Authentication middleware
const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.substring(7);
  const decoded = verifyToken(token);

  if (!decoded) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }

  req.user = decoded;
  next();
};

// Session management with Redis
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const { createClient } = require('redis');

const redisClient = createClient({
  url: process.env.REDIS_URL
});
redisClient.connect();

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  name: 'sessionId', // Don't use default 'connect.sid'
  cookie: {
    secure: true, // HTTPS only
    httpOnly: true, // No JavaScript access
    sameSite: 'strict',
    maxAge: 1000 * 60 * 60 * 24 // 24 hours
  }
}));

// Password reset with secure tokens
const passwordResetTokens = new Map();

app.post('/api/forgot-password', async (req, res) => {
  const { email } = req.body;
  const user = await User.findOne({ email });

  if (!user) {
    // Don't reveal if user exists
    return res.json({ message: 'If account exists, reset email sent' });
  }

  const resetToken = generateSecureToken();
  const expires = Date.now() + 3600000; // 1 hour

  passwordResetTokens.set(resetToken, {
    userId: user.id,
    expires
  });

  // Send email with reset link
  await sendResetEmail(email, resetToken);

  res.json({ message: 'If account exists, reset email sent' });
});

app.post('/api/reset-password', async (req, res) => {
  const { token, newPassword } = req.body;

  const resetData = passwordResetTokens.get(token);

  if (!resetData || resetData.expires < Date.now()) {
    return res.status(400).json({ error: 'Invalid or expired token' });
  }

  // Validate new password
  const errors = validatePassword(newPassword);
  if (errors.length > 0) {
    return res.status(400).json({ errors });
  }

  const hashedPassword = await hashPassword(newPassword);
  await User.updateOne(
    { _id: resetData.userId },
    { password: hashedPassword }
  );

  // Invalidate token
  passwordResetTokens.delete(token);

  res.json({ message: 'Password reset successful' });
});
```

**Best Practices**:
- Use strong password hashing (bcrypt, scrypt, Argon2)
- Implement multi-factor authentication
- Use secure session management
- Generate cryptographically secure tokens
- Implement proper password reset flow
- Use short-lived tokens with refresh mechanism
- Invalidate sessions on logout
- Protect against brute force attacks

### 8. Software and Data Integrity Failures

**What it is**: Code and infrastructure that doesn't protect against integrity violations.

**Examples**:
- No verification of npm packages
- Insecure CI/CD pipeline
- Auto-updates without verification
- Insecure deserialization

**Prevention**:

```javascript
// Verify package integrity
// Use package-lock.json and verify checksums
npm ci --ignore-scripts  // Don't run install scripts automatically

// Input validation for deserialization
app.post('/api/data', express.json({ limit: '10mb' }), (req, res) => {
  // Validate structure before processing
  const schema = {
    name: 'string',
    age: 'number',
    email: 'string'
  };

  for (const [key, expectedType] of Object.entries(schema)) {
    if (typeof req.body[key] !== expectedType) {
      return res.status(400).json({
        error: `Invalid type for ${key}`
      });
    }
  }

  // Process validated data
});

// Avoid eval() and similar dangerous functions
// BAD
app.get('/api/calc', (req, res) => {
  const result = eval(req.query.expression); // NEVER DO THIS
  res.json({ result });
});

// GOOD - Use safe alternatives
const math = require('mathjs');

app.get('/api/calc', (req, res) => {
  try {
    const result = math.evaluate(req.query.expression, {
      // Restrict available functions
    });
    res.json({ result });
  } catch (error) {
    res.status(400).json({ error: 'Invalid expression' });
  }
});
```

**Best Practices**:
- Use package-lock.json or npm shrinkwrap
- Verify package signatures and checksums
- Review code in dependencies
- Implement code signing for releases
- Use CI/CD with security checks
- Never deserialize untrusted data without validation
- Avoid eval(), Function(), and vm module with user input

### 9. Security Logging and Monitoring Failures

**What it is**: Insufficient logging and monitoring to detect breaches.

**Prevention**:

```javascript
const winston = require('winston');
const morgan = require('morgan');

// Winston logger configuration
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'api' },
  transports: [
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error'
    }),
    new winston.transports.File({
      filename: 'logs/combined.log'
    }),
    new winston.transports.File({
      filename: 'logs/security.log',
      level: 'warn'
    })
  ]
});

// Security event logging
const logSecurityEvent = (event, req, details = {}) => {
  logger.warn('Security Event', {
    event,
    ip: req.ip,
    userAgent: req.headers['user-agent'],
    user: req.user?.id || 'anonymous',
    path: req.path,
    method: req.method,
    ...details
  });
};

// Log authentication failures
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });

  if (!user || !(await bcrypt.compare(password, user.password))) {
    logSecurityEvent('LOGIN_FAILED', req, { email });
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  logSecurityEvent('LOGIN_SUCCESS', req, { userId: user.id });
  res.json({ token: generateToken(user) });
});

// Log authorization failures
app.get('/api/admin', authenticate, requireAdmin, (req, res) => {
  res.json({ admin: true });
});

const requireAdmin = (req, res, next) => {
  if (req.user.role !== 'admin') {
    logSecurityEvent('AUTHORIZATION_FAILED', req, {
      requiredRole: 'admin',
      userRole: req.user.role
    });
    return res.status(403).json({ error: 'Access denied' });
  }
  next();
};

// Log data access
app.get('/api/users/:id', authenticate, async (req, res) => {
  logSecurityEvent('USER_DATA_ACCESS', req, {
    targetUserId: req.params.id,
    accessorId: req.user.id
  });

  const user = await User.findById(req.params.id);
  res.json(user);
});

// HTTP request logging with Morgan
app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}));

// Monitor for suspicious patterns
const suspiciousActivityDetector = (req, res, next) => {
  // Detect SQL injection attempts
  const sqlPatterns = /'|--|;|\/\*|\*\/|xp_|sp_|UNION|SELECT|INSERT|DELETE|DROP/i;
  const params = JSON.stringify(req.query) + JSON.stringify(req.body);

  if (sqlPatterns.test(params)) {
    logSecurityEvent('SUSPECTED_SQL_INJECTION', req, { params });
  }

  // Detect path traversal attempts
  if (req.path.includes('..') || req.path.includes('~')) {
    logSecurityEvent('SUSPECTED_PATH_TRAVERSAL', req);
  }

  next();
};

app.use(suspiciousActivityDetector);
```

**Best Practices**:
- Log all authentication events (success and failure)
- Log authorization failures
- Log input validation failures
- Log security-relevant configuration changes
- Include context (IP, user, timestamp, action)
- Protect logs from tampering
- Set up alerts for suspicious patterns
- Retain logs for appropriate period
- Don't log sensitive data (passwords, tokens, PII)

### 10. Server-Side Request Forgery (SSRF)

**What it is**: Application fetches remote resources without validating user-supplied URLs.

**Prevention**:

```javascript
const axios = require('axios');
const { URL } = require('url');

// URL validation
const isValidUrl = (urlString) => {
  try {
    const url = new URL(urlString);

    // Only allow HTTPS
    if (url.protocol !== 'https:') {
      return false;
    }

    // Block private IP ranges
    const hostname = url.hostname;

    // Block localhost
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return false;
    }

    // Block private networks
    const privateRanges = [
      /^10\./,
      /^172\.(1[6-9]|2[0-9]|3[0-1])\./,
      /^192\.168\./,
      /^169\.254\./  // Link-local
    ];

    if (privateRanges.some(pattern => pattern.test(hostname))) {
      return false;
    }

    // Block cloud metadata endpoints
    if (hostname === '169.254.169.254') {
      return false;
    }

    return true;
  } catch (error) {
    return false;
  }
};

// Safe URL fetching
app.post('/api/fetch-url', async (req, res) => {
  const { url } = req.body;

  // Validate URL
  if (!isValidUrl(url)) {
    return res.status(400).json({ error: 'Invalid or unsafe URL' });
  }

  // Use allowlist if possible
  const allowedDomains = ['api.example.com', 'data.example.com'];
  const urlObj = new URL(url);

  if (!allowedDomains.includes(urlObj.hostname)) {
    return res.status(403).json({ error: 'Domain not allowed' });
  }

  try {
    const response = await axios.get(url, {
      timeout: 5000,
      maxRedirects: 0, // Don't follow redirects
      maxContentLength: 1024 * 1024 // 1MB limit
    });

    res.json({ data: response.data });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch URL' });
  }
});

// Proxy endpoint with strict validation
app.post('/api/proxy', async (req, res) => {
  // Only allow specific API endpoints
  const allowedEndpoints = [
    'https://api.usaspending.gov/api/v2/search/spending_by_award/',
    'https://api.usaspending.gov/api/v2/search/spending_by_award_count/'
  ];

  const targetUrl = 'https://api.usaspending.gov/api/v2/search/spending_by_award/';

  if (!allowedEndpoints.includes(targetUrl)) {
    return res.status(403).json({ error: 'Endpoint not allowed' });
  }

  try {
    const response = await axios.post(targetUrl, req.body, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 10000,
      maxRedirects: 0
    });

    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: 'Proxy request failed'
    });
  }
});
```

**Best Practices**:
- Validate and sanitize all URLs
- Use allowlists for allowed domains
- Block private IP ranges and localhost
- Block cloud metadata endpoints (169.254.169.254)
- Disable or limit redirects
- Implement request timeouts
- Use network segmentation

## Input Validation and Sanitization

### Validation Libraries

**express-validator**:

```javascript
const { body, query, param, validationResult } = require('express-validator');

app.post('/api/users',
  // Validation chain
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Invalid email'),

  body('age')
    .isInt({ min: 18, max: 120 })
    .withMessage('Age must be between 18 and 120'),

  body('username')
    .isLength({ min: 3, max: 20 })
    .matches(/^[a-zA-Z0-9_]+$/)
    .withMessage('Username must be 3-20 alphanumeric characters'),

  body('website')
    .optional()
    .isURL()
    .withMessage('Invalid URL'),

  async (req, res) => {
    const errors = validationResult(req);

    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    // Data is validated
    const user = await User.create(req.body);
    res.status(201).json(user);
  }
);
```

**Joi**:

```javascript
const Joi = require('joi');

const userSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(12).required(),
  age: Joi.number().integer().min(18).max(120),
  website: Joi.string().uri().optional(),
  tags: Joi.array().items(Joi.string()).max(10)
});

const validateRequest = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true
    });

    if (error) {
      return res.status(400).json({
        error: 'Validation failed',
        details: error.details.map(d => ({
          field: d.path.join('.'),
          message: d.message
        }))
      });
    }

    req.body = value; // Use validated data
    next();
  };
};

app.post('/api/users', validateRequest(userSchema), async (req, res) => {
  const user = await User.create(req.body);
  res.status(201).json(user);
});
```

### Sanitization

```javascript
const xss = require('xss');
const validator = require('validator');

// HTML sanitization
const sanitizeHtml = (dirty) => {
  return xss(dirty, {
    whiteList: {
      p: [],
      br: [],
      strong: [],
      em: [],
      a: ['href']
    }
  });
};

// Escape HTML entities
const escapeHtml = (unsafe) => {
  return validator.escape(unsafe);
};

app.post('/api/posts', async (req, res) => {
  const { title, content } = req.body;

  const sanitizedPost = {
    title: escapeHtml(title),
    content: sanitizeHtml(content)
  };

  const post = await Post.create(sanitizedPost);
  res.status(201).json(post);
});
```

## Secrets Management

### Environment Variables

```javascript
// .env file (NEVER commit to Git)
JWT_SECRET=your-256-bit-secret-here
DATABASE_URL=postgresql://user:pass@localhost:5432/db
API_KEY=your-api-key-here
ENCRYPTION_KEY=64-char-hex-string-here

// Load environment variables
require('dotenv').config();

// Access secrets
const jwtSecret = process.env.JWT_SECRET;
const dbUrl = process.env.DATABASE_URL;

// Validate required secrets on startup
const requiredSecrets = ['JWT_SECRET', 'DATABASE_URL'];

for (const secret of requiredSecrets) {
  if (!process.env[secret]) {
    console.error(`FATAL: ${secret} environment variable is not set`);
    process.exit(1);
  }
}
```

### Cloud Secret Managers

**Google Secret Manager**:

```javascript
const { SecretManagerServiceClient } = require('@google-cloud/secret-manager');
const client = new SecretManagerServiceClient();

async function getSecret(secretName) {
  const [version] = await client.accessSecretVersion({
    name: `projects/${projectId}/secrets/${secretName}/versions/latest`
  });

  return version.payload.data.toString('utf8');
}

// Usage
const dbPassword = await getSecret('database-password');
```

**AWS Secrets Manager**:

```javascript
const AWS = require('aws-sdk');
const secretsManager = new AWS.SecretsManager({ region: 'us-east-1' });

async function getSecret(secretName) {
  const data = await secretsManager.getSecretValue({
    SecretId: secretName
  }).promise();

  return JSON.parse(data.SecretString);
}

// Usage
const dbCredentials = await getSecret('prod/database/credentials');
```

### Best Practices

- Never hardcode secrets in source code
- Never commit secrets to version control
- Use environment variables or secret managers
- Rotate secrets regularly
- Use different secrets for different environments
- Limit access to secrets (principle of least privilege)
- Audit secret access
- Encrypt secrets at rest and in transit

## Security Headers

### Complete Helmet Configuration

```javascript
const helmet = require('helmet');

app.use(helmet({
  // Content Security Policy
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "trusted-cdn.com"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "api.example.com"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
      baseUri: ["'self'"],
      formAction: ["'self'"],
      frameAncestors: ["'none'"]
    }
  },

  // HTTP Strict Transport Security
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },

  // X-Content-Type-Options
  noSniff: true,

  // X-Frame-Options
  frameguard: {
    action: 'deny'
  },

  // Referrer-Policy
  referrerPolicy: {
    policy: 'strict-origin-when-cross-origin'
  },

  // X-Download-Options
  ieNoOpen: true,

  // X-DNS-Prefetch-Control
  dnsPrefetchControl: {
    allow: false
  },

  // Remove X-Powered-By
  hidePoweredBy: true,

  // X-Permitted-Cross-Domain-Policies
  permittedCrossDomainPolicies: {
    permittedPolicies: 'none'
  }
}));
```

## API Security Best Practices

### API Key Management

```javascript
const crypto = require('crypto');

// Generate API keys
const generateApiKey = () => {
  return crypto.randomBytes(32).toString('hex');
};

// Middleware to validate API keys
const validateApiKey = async (req, res, next) => {
  const apiKey = req.headers['x-api-key'];

  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }

  // Hash the provided key for comparison
  const hashedKey = crypto
    .createHash('sha256')
    .update(apiKey)
    .digest('hex');

  // Look up in database
  const validKey = await ApiKey.findOne({
    keyHash: hashedKey,
    active: true,
    expiresAt: { $gt: new Date() }
  });

  if (!validKey) {
    return res.status(401).json({ error: 'Invalid API key' });
  }

  // Track usage
  await ApiKey.updateOne(
    { _id: validKey._id },
    { $inc: { usageCount: 1 }, lastUsedAt: new Date() }
  );

  req.apiKey = validKey;
  next();
};

app.get('/api/data', validateApiKey, (req, res) => {
  res.json({ data: [] });
});
```

### Rate Limiting by API Key

```javascript
const rateLimit = require('express-rate-limit');

const createApiLimiter = (maxRequests, windowMs) => {
  return rateLimit({
    windowMs,
    max: maxRequests,
    keyGenerator: (req) => {
      // Use API key as rate limit key
      return req.headers['x-api-key'] || req.ip;
    },
    handler: (req, res) => {
      res.status(429).json({
        error: 'Rate limit exceeded',
        retryAfter: res.getHeader('Retry-After')
      });
    }
  });
};

const apiLimiter = createApiLimiter(1000, 60 * 60 * 1000); // 1000/hour

app.use('/api', validateApiKey, apiLimiter);
```

## Security Testing

### Example Security Tests

```javascript
const request = require('supertest');
const app = require('./server');

describe('Security Tests', () => {
  describe('SQL Injection', () => {
    it('should reject SQL injection in query params', async () => {
      const response = await request(app)
        .get("/api/users?id=1' OR '1'='1")
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });
  });

  describe('XSS Protection', () => {
    it('should sanitize HTML in input', async () => {
      const response = await request(app)
        .post('/api/posts')
        .send({
          title: '<script>alert("xss")</script>Test',
          content: 'Content'
        })
        .expect(201);

      expect(response.body.title).not.toContain('<script>');
    });
  });

  describe('Authentication', () => {
    it('should reject requests without token', async () => {
      await request(app)
        .get('/api/protected')
        .expect(401);
    });

    it('should reject invalid tokens', async () => {
      await request(app)
        .get('/api/protected')
        .set('Authorization', 'Bearer invalid-token')
        .expect(401);
    });
  });

  describe('Rate Limiting', () => {
    it('should enforce rate limits', async () => {
      const requests = Array(10).fill().map(() =>
        request(app).post('/api/login').send({ email: 'test@example.com', password: 'password' })
      );

      const responses = await Promise.all(requests);
      const tooManyRequests = responses.filter(r => r.status === 429);

      expect(tooManyRequests.length).toBeGreaterThan(0);
    });
  });

  describe('Authorization', () => {
    it('should prevent unauthorized access to resources', async () => {
      const userToken = generateToken({ id: 1, role: 'user' });

      await request(app)
        .get('/api/admin')
        .set('Authorization', `Bearer ${userToken}`)
        .expect(403);
    });
  });
});
```

## Security Checklist

### Pre-Deployment Checklist

- [ ] All secrets stored in environment variables or secret managers
- [ ] No secrets committed to version control
- [ ] Security headers configured (Helmet)
- [ ] HTTPS enforced in production
- [ ] CORS properly configured
- [ ] Rate limiting implemented on sensitive endpoints
- [ ] Input validation on all user inputs
- [ ] Output encoding to prevent XSS
- [ ] Parameterized queries to prevent SQL injection
- [ ] Strong password policies enforced
- [ ] Account lockout after failed login attempts
- [ ] Session management secure (httpOnly, secure, sameSite)
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies audited and updated
- [ ] Security logging implemented
- [ ] File upload restrictions (type, size, location)
- [ ] API authentication and authorization
- [ ] SSRF protections for URL fetching
- [ ] Command injection protections
- [ ] Regular security testing

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org/
- Node.js Security Best Practices: https://nodejs.org/en/docs/guides/security/
- Express Security Best Practices: https://expressjs.com/en/advanced/best-practice-security.html
- Snyk Vulnerability Database: https://security.snyk.io/
- npm Security Advisories: https://www.npmjs.com/advisories
