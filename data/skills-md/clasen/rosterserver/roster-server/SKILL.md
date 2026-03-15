---
name: roster-server
description: Virtual hosting for multiple HTTPS sites with Let's Encrypt SSL automation. Each domain gets isolated VirtualServer instance, supports Express/Socket.IO/custom handlers, local HTTP dev mode with CRC32-based ports, automatic www redirects, and SNI certificate management.
---

## Quick Setup

### Production
```javascript
const Roster = require('roster-server');

const roster = new Roster({
    email: 'admin@example.com',
    wwwPath: '/srv/www',
    greenlockStorePath: '/srv/greenlock.d',
    local: true
});

roster.start();
```

### Local Development
```javascript
const roster = new Roster({
    local: true,  // HTTP mode, no SSL
    wwwPath: './www'
});

roster.start().then(() => {
    console.log('example.com:', roster.getUrl('example.com'));
    // → http://localhost:9465 (deterministic CRC32-based port)
});
```

## Directory Structure

```
project/
├── greenlock.d/        # SSL certificates (auto-generated)
├── www/
│   ├── example.com/
│   │   └── index.js   # Handler for example.com
│   ├── api.example.com/
│   │   └── index.js   # Handler for subdomain
│   └── *.example.com/
│       └── index.js   # Wildcard: one handler for all subdomains
└── server.js          # Your setup
```

## Handler Patterns

Each `www/{domain}/index.js` must export a function that receives `httpsServer` and returns a request handler.

### Pattern 1: Basic HTTP Handler
```javascript
module.exports = (httpsServer) => {
    return (req, res) => {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('Hello World');
    };
};
```

### Pattern 2: Express App
```javascript
const express = require('express');

module.exports = (httpsServer) => {
    const app = express();
    
    app.get('/', (req, res) => res.send('Hello'));
    app.post('/api/data', (req, res) => res.json({ ok: true }));
    
    return app;
};
```

### Pattern 3: Socket.IO
```javascript
const { Server } = require('socket.io');

module.exports = (httpsServer) => {
    const io = new Server(httpsServer);
    
    io.on('connection', (socket) => {
        socket.on('message', (data) => io.emit('message', data));
    });
    
    return (req, res) => {
        if (req.url && req.url.startsWith(io.opts.path)) return;
        res.writeHead(200);
        res.end('Socket.IO running');
    };
};
```

### Pattern 4: Manual Registration
```javascript
// In server.js, before roster.start()
roster.register('example.com', (httpsServer) => {
    return (req, res) => {
        res.writeHead(200);
        res.end('Manual handler');
    };
});

// With custom port
roster.register('api.example.com:8443', handler);

// Wildcard: one handler for all subdomains (default port or custom)
roster.register('*.example.com', handler);
roster.register('*.example.com:8080', handler);
```

## Key Configuration Options

```javascript
new Roster({
    email: 'admin@example.com',      // Required for SSL
    wwwPath: '/srv/www',             // Site handlers directory
    greenlockStorePath: '/srv/greenlock.d',  // SSL storage
    dnsChallenge: { ... },          // Optional override. Default is local/manual DNS-01 (acme-dns-01-cli)
    
    // Environment
    local: false,                    // true = HTTP, false = HTTPS
    staging: false,                  // true = Let's Encrypt staging
    
    // Server
    hostname: '0.0.0.0',
    port: 443,                       // Default HTTPS port (NOT 80!)
    
    // Local mode
    minLocalPort: 4000,
    maxLocalPort: 9999,
    
    // Advanced
    filename: 'index',               // Handler filename (no extension)
    basePath: '/srv'                 // Base for relative paths
})
```

## Core API

### `roster.start()`
Loads sites, generates SSL config, starts servers. Returns `Promise<void>`.

### `roster.register(domain, handler)`
Manually register a domain handler. Domain can include port: `'api.com:8443'`. For wildcards use `'*.example.com'` or `'*.example.com:8080'`.

### `roster.getUrl(domain)`
Get environment-aware URL:
- Local mode: `http://localhost:{port}`
- Production: `https://{domain}` or `https://{domain}:{port}`
- Returns `null` if domain not registered. Supports wildcard-matched hosts (e.g. `getUrl('api.example.com')` when `*.example.com` is registered).

## How It Works

### Request Flow
1. Request arrives → Dispatcher extracts `Host` header
2. Strips `www.` prefix (301 redirect if present)
3. Looks up domain → Gets `VirtualServer` instance
4. Routes to handler via `virtualServer.processRequest(req, res)`

### VirtualServer Architecture
Each domain gets isolated server instance that simulates `http.Server`:
- Captures `request` and `upgrade` event listeners
- Complete separation between domains
- No configuration conflicts between apps

### Port Assignment
**Production**: Default 443, custom via `domain:port` syntax  
**Local**: CRC32 hash of domain → deterministic port in range 4000-9999  
**Reserved**: Port 80 for ACME challenges only

### SSL Management
- Automatic Let's Encrypt certificate generation
- Auto-renewal 45 days before expiration
- SNI support for multiple domains
- Custom ports reuse certificates via SNI callback
- **Wildcard** (`*.example.com`): use folder `www/*.example.com/` or `roster.register('*.example.com', handler)`. Default DNS-01 plugin is local/manual `acme-dns-01-cli`; set `dnsChallenge` only when overriding provider integration.

## Common Issues & Solutions

**Port 443 in use**: Use different port `{ port: 8443 }`  
**Certificate failed**: Check firewall (ports 80, 443), verify DNS, try `staging: true`  
**Site not found**: Verify directory name matches domain, check `index.js` exports function  
**Local port conflict**: Adjust `minLocalPort`/`maxLocalPort` range  
**Socket.IO not working**: Ensure handler checks `io.opts.path` and returns properly

## Best Practices

1. **Test with staging first**: `staging: true` to avoid Let's Encrypt rate limits
2. **Use local mode for dev**: `local: true` for faster iteration
3. **Environment variables**: Configure via `process.env` for portability
4. **Error handling**: Wrap handlers with try/catch, don't expose internals
5. **Socket.IO paths**: Always check `req.url.startsWith(io.opts.path)` in returned handler
6. **Port 80**: Never use as HTTPS port (reserved for ACME)

## Quick Examples

### Full Production Setup
```javascript
const Roster = require('roster-server');

const roster = new Roster({
    email: process.env.ADMIN_EMAIL,
    wwwPath: '/srv/www',
    greenlockStorePath: '/srv/greenlock.d',
    staging: process.env.NODE_ENV !== 'production'
});

roster.start().then(() => {
    console.log('RosterServer running');
}).catch(err => {
    console.error('Startup failed:', err);
    process.exit(1);
});
```

### Local Dev with Manual Registration
```javascript
const roster = new Roster({ local: true, wwwPath: './www' });

roster.register('test.local', (server) => {
    return (req, res) => {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok', url: roster.getUrl('test.local') }));
    };
});

roster.start();
```

### Environment-Aware Configuration
```javascript
const isProduction = process.env.NODE_ENV === 'production';

const roster = new Roster({
    email: process.env.ADMIN_EMAIL || 'admin@example.com',
    wwwPath: process.env.WWW_PATH || './www',
    greenlockStorePath: process.env.SSL_PATH || './greenlock.d',
    local: !isProduction,
    staging: !isProduction,
    minLocalPort: parseInt(process.env.MIN_PORT) || 4000,
    maxLocalPort: parseInt(process.env.MAX_PORT) || 9999
});

roster.start();
```

## Implementation Checklist

When implementing RosterServer:

- [ ] Create `www/` directory structure with domain folders
- [ ] Each domain has `index.js` exporting `(httpsServer) => handler`
- [ ] Configure email for Let's Encrypt notifications
- [ ] Test with `local: true` first
- [ ] Test with `staging: true` before production
- [ ] Ensure ports 80 and 443 are open (production)
- [ ] Verify DNS points to server
- [ ] Never use port 80 as HTTPS port
- [ ] Use `roster.getUrl(domain)` for environment-aware URLs
- [ ] Handle Socket.IO paths correctly in returned handler
- [ ] Implement error handling in handlers
