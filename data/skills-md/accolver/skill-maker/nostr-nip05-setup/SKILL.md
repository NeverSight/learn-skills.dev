---
name: nostr-nip05-setup
description: Set up NIP-05 DNS-based identity verification for Nostr, including the /.well-known/nostr.json endpoint, CORS headers, and kind:0 profile updates. Use when configuring NIP-05, setting up nostr.json, debugging NIP-05 verification failures, adding DNS identity to a Nostr profile, or working with /.well-known/nostr.json files and CORS for Nostr clients.
---

# NIP-05 Identity Setup

## Overview

Set up NIP-05 DNS-based identity verification so Nostr clients can map
human-readable identifiers (like `bob@example.com`) to hex public keys. This
skill covers creating the `/.well-known/nostr.json` endpoint, configuring CORS
headers, updating kind:0 profiles, and debugging verification failures.

## When to Use

- Setting up NIP-05 verification for a domain
- Creating or editing a `/.well-known/nostr.json` file
- Configuring web server CORS headers for Nostr clients
- Updating a kind:0 profile with a `nip05` field
- Debugging why NIP-05 verification is failing
- Setting up the `_@domain` root identifier

**Do NOT use when:**

- Building a Nostr relay (that's relay protocol)
- Working with NIP-19 bech32 encoding (npub/nsec display format)
- Implementing Nostr event signing or key management

## Workflow

### 1. Determine the Setup Type

Ask: "Static file or dynamic server?"

| Scenario                     | Approach                                    | Best For                            |
| ---------------------------- | ------------------------------------------- | ----------------------------------- |
| Few users, rarely changes    | Static `.well-known/nostr.json` file        | Personal sites, small communities   |
| Many users, frequent changes | Dynamic server with `?name=` query handling | NIP-05 providers, large communities |
| Existing web server          | Add location block + CORS headers           | Nginx, Apache, Caddy setups         |

### 2. Create the nostr.json File

The file maps human-readable names to hex public keys.

**Format:**

```json
{
  "names": {
    "bob": "b0635d6a9851d3aed0cd6c495b282167acf761729078d975fc341b22650b07b9"
  },
  "relays": {
    "b0635d6a9851d3aed0cd6c495b282167acf761729078d975fc341b22650b07b9": [
      "wss://relay.example.com",
      "wss://relay2.example.com"
    ]
  }
}
```

**Critical rules:**

- Public keys MUST be **64-character lowercase hex** (NOT npub bech32 format)
- The `names` object is REQUIRED
- The `relays` object is RECOMMENDED — it helps clients discover where to find
  the user
- Local-part (the name) MUST only contain `a-z0-9-_.` (lowercase, no uppercase)
- `_` is the special "root" identifier — `_@example.com` displays as just
  `example.com` in clients

**Root identifier example:**

```json
{
  "names": {
    "_": "b0635d6a9851d3aed0cd6c495b282167acf761729078d975fc341b22650b07b9"
  }
}
```

This lets the user be identified as just `example.com` instead of
`bob@example.com`.

### 3. Serve the File Correctly

The file MUST be served at exactly:

```
https://<domain>/.well-known/nostr.json?name=<local-part>
```

**Three non-negotiable requirements:**

1. **HTTPS only** — HTTP will not work. Clients only fetch over HTTPS.
2. **CORS header** — Response MUST include `Access-Control-Allow-Origin: *`
   because JavaScript Nostr clients run in browsers and are blocked by CORS
   policies without this header.
3. **No redirects** — The endpoint MUST NOT return HTTP redirects (301, 302,
   etc.). Fetchers MUST ignore redirects per the NIP-05 spec. This is a security
   constraint.

The `?name=<local-part>` query string format exists so both static files and
dynamic servers work. A static file ignores the query string and returns all
names; a dynamic server can filter by name.

See [references/server-configs.md](references/server-configs.md) for Nginx,
Apache, Caddy, and Node.js configuration examples.

### 4. Update the Kind:0 Profile

The user's kind:0 metadata event must include the `nip05` field:

```json
{
  "kind": 0,
  "content": "{\"name\":\"bob\",\"nip05\":\"bob@example.com\",\"about\":\"A Nostr user\",\"picture\":\"https://example.com/avatar.jpg\"}"
}
```

The `nip05` value format is `<local-part>@<domain>` — it looks like an email
address but is NOT an email address.

**Verification flow (what clients do):**

1. Client sees `"nip05": "bob@example.com"` in a kind:0 event
2. Client splits into local-part `bob` and domain `example.com`
3. Client fetches `https://example.com/.well-known/nostr.json?name=bob`
4. Client checks if `response.names.bob` matches the event's `pubkey`
5. If match → identity is verified and displayed

### 5. Test the Setup

**Verify the endpoint returns correct JSON:**

```bash
curl -s https://example.com/.well-known/nostr.json?name=bob | jq .
```

**Verify CORS headers are present:**

```bash
curl -sI https://example.com/.well-known/nostr.json?name=bob | grep -i ^access-control
# Expected: Access-Control-Allow-Origin: *
```

**Verify no redirects:**

```bash
curl -sI -o /dev/null -w "%{http_code}" https://example.com/.well-known/nostr.json?name=bob
# Expected: 200 (NOT 301, 302, 307, 308)
```

**Verify the pubkey is hex (not npub):**

```bash
curl -s https://example.com/.well-known/nostr.json?name=bob | jq -r '.names.bob' | grep -E '^[0-9a-f]{64}$'
# Should match — 64 lowercase hex characters
```

## Checklist

- [ ] nostr.json file created with correct `names` mapping
- [ ] Public keys are 64-char lowercase hex (not npub)
- [ ] Local-parts use only `a-z0-9-_.` characters
- [ ] File served over HTTPS
- [ ] `Access-Control-Allow-Origin: *` header present
- [ ] No HTTP redirects on the endpoint
- [ ] `relays` object included (recommended)
- [ ] Kind:0 profile updated with `nip05` field
- [ ] Endpoint tested with curl and returns 200 with correct JSON

## Common Mistakes

| Mistake                                  | Why It Breaks                                             | Fix                                                           |
| ---------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------- |
| Using npub instead of hex pubkey         | NIP-05 requires hex format; npub is only for UI display   | Convert npub to hex using a tool like `nak decode npub1...`   |
| Missing CORS header                      | JavaScript Nostr clients in browsers can't fetch the file | Add `Access-Control-Allow-Origin: *` to server config         |
| HTTP redirects (301/302)                 | NIP-05 spec says fetchers MUST ignore redirects           | Serve directly, no redirects — check trailing slash redirects |
| Uppercase in local-part                  | Spec requires `a-z0-9-_.` only                            | Normalize to lowercase before storing                         |
| Serving over HTTP instead of HTTPS       | Clients only fetch NIP-05 over HTTPS                      | Set up TLS (Let's Encrypt, Cloudflare, etc.)                  |
| Trailing slash redirect on `.well-known` | Nginx/Apache may redirect `/nostr.json` to `/nostr.json/` | Ensure exact match location, not directory                    |
| Wrong Content-Type                       | Some servers don't set `application/json`                 | Add `Content-Type: application/json` header                   |
| Query string breaks static file          | Some servers reject or misroute `?name=` on static files  | Ensure server passes query strings through to static files    |

## Quick Reference

| Item             | Value                                                       |
| ---------------- | ----------------------------------------------------------- |
| Endpoint         | `https://<domain>/.well-known/nostr.json?name=<local-part>` |
| Required header  | `Access-Control-Allow-Origin: *`                            |
| Pubkey format    | 64-char lowercase hex                                       |
| Local-part chars | `a-z0-9-_.`                                                 |
| Root identifier  | `_@domain` (displays as just the domain)                    |
| Profile field    | `"nip05": "name@domain"` in kind:0 content                  |
| Protocol         | HTTPS only (no HTTP)                                        |
| Redirects        | MUST NOT redirect                                           |

## Key Principles

1. **Hex keys, never npub** — The nostr.json file uses raw 64-character
   lowercase hex public keys. npub is a display format (NIP-19) and must never
   appear in nostr.json. This is the single most common mistake.

2. **CORS is mandatory** — Without `Access-Control-Allow-Origin: *`, every
   browser-based Nostr client silently fails to verify the identity. The user
   sees no error — verification just doesn't work.

3. **No redirects, ever** — HTTP redirects are a security risk in this context.
   The spec explicitly requires fetchers to ignore them. Common culprits:
   trailing-slash redirects, HTTP→HTTPS redirects on the endpoint itself, and
   www→non-www redirects.

4. **Identification, not verification** — NIP-05 identifies users (maps
   human-readable names to keys), it does not verify trust. The exception is
   well-known domains (companies, projects) where domain ownership itself
   implies trust.

5. **Clients follow pubkeys, not NIP-05 addresses** — If a user follows
   `bob@example.com`, the client stores the pubkey, not the address. If the
   NIP-05 mapping changes later, the client unfollows the address display but
   keeps following the pubkey.
