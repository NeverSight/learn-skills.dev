---
name: go-jwt
description: Use when implementing JWT token signing or verification in Go projects. Covers ES256 (ECDSA, recommended), PS256/RS256 (RSA asymmetric), and HS256 (HMAC symmetric) signing methods, with keys loaded from file path or inline string. Places the jwt package under pkg/jwt for new projects.
---

# Go JWT (ES256 / PS256 / RS256 / HS256)

JWT signing and verification using `github.com/golang-jwt/jwt/v5`.
Supports **ES256** (ECDSA P-256, recommended for new projects), **PS256** (RSA-PSS, recommended over RS256), **RS256** (RSA PKCS1v1.5, legacy), and **HS256** (HMAC symmetric).

## Placement

| Project Type | Path / Lookup order |
|---|---|
| **New project** | `pkg/jwt/` |
| **Existing project** | 1) `pkg/jwt` 2) `pkg/utils/jwt` (fallback) |

For **new projects**, **MUST** create the package under `pkg/jwt/`.

## Dependencies

```bash
go get github.com/golang-jwt/jwt/v5
```

## Signing Methods

| Method | Algorithm | Signing Key | Verification Key | Recommendation |
|---|---|---|---|---|
| `MethodES256` | ES256 (ECDSA P-256) | `*ecdsa.PrivateKey` | `*ecdsa.PublicKey` | ⭐ **Recommended for new projects** — small keys, fast, modern |
| `MethodPS256` | PS256 (RSA-PSS) | `*rsa.PrivateKey` | `*rsa.PublicKey` | ✅ **Recommended over RS256** — same key pair, randomised padding |
| `MethodRS256` | RS256 (RSA PKCS1v1.5) | `*rsa.PrivateKey` | `*rsa.PublicKey` | Legacy — safe but superseded by PS256 |
| `MethodHS256` | HS256 (HMAC-SHA256) | `[]byte` (secret) | same secret | Internal / single-service only; never cross-service |

> Key generation:
> ```bash
> # ES256 — EC P-256 (recommended)
> openssl ecparam -name prime256v1 -genkey -noout -out configs/ec-key.pem
> openssl ec -in configs/ec-key.pem -pubout -out configs/ec-public.pem
>
> # RS256 / PS256 — RSA 2048
> openssl genrsa -out configs/key.pem 2048
> openssl rsa -in configs/key.pem -outform PEM -pubout -out configs/public.pem
> ```

## Key Loading Priority

Both `SignerConfig` and `ParserConfig` support two mutually exclusive ways to supply keys:

| Method | Inline field (higher priority) | Path field (lower priority) |
|---|---|---|
| RS256 / PS256 (private) | `PrivateKeyData` (PEM string) | `PrivateKeyPath` (file path) |
| RS256 / PS256 (public) | `PublicKeyData` (PEM string) | `PublicKeyPath` (file path) |
| ES256 (private) | `ECPrivateKeyData` (PEM string) | `ECPrivateKeyPath` (file path) |
| ES256 (public) | `ECPublicKeyData` (PEM string) | `ECPublicKeyPath` (file path) |
| HS256 | `Secret` (plain string, min 32 bytes) | — |

## Config

```go
// SignerConfig holds JWT signing configuration.
type SignerConfig struct {
    Method Method `mapstructure:"method"` // "RS256" | "PS256" | "ES256" | "HS256"; default RS256

    // RSA keys — used for RS256 and PS256
    PrivateKeyPath string `mapstructure:"private_key_path"` // RS256/PS256: path to RSA private key PEM file
    PrivateKeyData string `mapstructure:"private_key_data"` // RS256/PS256: inline PEM string; takes precedence over path

    // EC keys — used for ES256
    ECPrivateKeyPath string `mapstructure:"ec_private_key_path"` // ES256: path to EC private key PEM file
    ECPrivateKeyData string `mapstructure:"ec_private_key_data"` // ES256: inline PEM string; takes precedence over path

    // HMAC — used for HS256
    Secret string `mapstructure:"secret"` // HS256: shared HMAC secret string (min 32 bytes)

    // Common
    Issuer         string   `mapstructure:"issuer"`           // JWT iss claim
    Audiences      []string `mapstructure:"audiences"`        // JWT aud claim
    IDPrefix       string   `mapstructure:"id_prefix"`        // if non-empty, sets jti (random hex)
    MaxLifetimeSec int      `mapstructure:"max_lifetime_sec"` // max token lifetime in seconds (0 = 7 days)
}

// ParserConfig holds JWT parsing/verification configuration.
type ParserConfig struct {
    Method Method `mapstructure:"method"` // "RS256" | "PS256" | "ES256" | "HS256"; default RS256

    // RSA keys — used for RS256 and PS256
    PublicKeyPath string `mapstructure:"public_key_path"` // RS256/PS256: path to RSA public key PEM file
    PublicKeyData string `mapstructure:"public_key_data"` // RS256/PS256: inline PEM string; takes precedence over path

    // EC keys — used for ES256
    ECPublicKeyPath string `mapstructure:"ec_public_key_path"` // ES256: path to EC public key PEM file
    ECPublicKeyData string `mapstructure:"ec_public_key_data"` // ES256: inline PEM string; takes precedence over path

    // HMAC — used for HS256
    Secret string `mapstructure:"secret"` // HS256: shared HMAC secret string (min 32 bytes)

    // Common
    Audience string `mapstructure:"audience"` // expected aud value; empty = skip audience check
}
```

## API Summary

| Function | Purpose |
|---|---|
| `NewSigner(cfg *SignerConfig) (Signer, error)` | Create a signer; validates config and loads keys |
| `signer.Token(sub, data, lifetime) (string, error)` | Sign a token; `lifetime` is capped at `MaxLifetimeSec` |
| `NewParser(cfg *ParserConfig) (Parser, error)` | Create a parser; validates config and loads keys |
| `parser.Parse(tokenString) (*CustomClaims, error)` | Validate and parse a token |
| `Unmarshal[T](claims *CustomClaims) (*T, error)` | Decode `claims.Data` (type `any`) into a concrete struct `T` |

## CustomClaims

```go
// CustomClaims extends standard JWT claims with a custom Data payload.
type CustomClaims struct {
    Data any `json:"data"`
    jwt.RegisteredClaims
}
```

> **Important:** After `Parse`, `claims.Data` is `map[string]any` (JSON roundtrip).
> Use `jwt.Unmarshal[T](claims)` to decode it into your concrete type.

## Usage Pattern

### Signing (ES256 — recommended)

```go
signer, err := jwt.NewSigner(&jwt.SignerConfig{
    Method:           jwt.MethodES256,
    ECPrivateKeyPath: "configs/ec-key.pem",
    Issuer:           "myapp",
    Audiences:        []string{"api.myapp.com"},
    MaxLifetimeSec:   86400, // 1 day cap
})
if err != nil { ... }

token, err := signer.Token(userID, userPayload, 24*time.Hour)
```

### Verification (ES256 — recommended)

```go
parser, err := jwt.NewParser(&jwt.ParserConfig{
    Method:          jwt.MethodES256,
    ECPublicKeyPath: "configs/ec-public.pem",
    Audience:        "api.myapp.com",
})
if err != nil { ... }

claims, err := parser.Parse(tokenString)
if err != nil { ... }

user, err := jwt.Unmarshal[UserToken](claims)
```

### Middleware pattern (Gin)

```go
func JWTMiddleware(parser jwt.Parser) gin.HandlerFunc {
    return func(c *gin.Context) {
        raw := c.GetHeader("Authorization")
        tokenString := strings.TrimPrefix(raw, "Bearer ")
        if tokenString == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing token"})
            return
        }
        claims, err := parser.Parse(tokenString)
        if err != nil {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
            return
        }
        c.Set("claims", claims)
        c.Next()
    }
}
```

## Security Rules (MUST follow)

- **Payload is NOT encrypted** — JWT is only base64-encoded and signed. Never store passwords, phone numbers, ID cards, or any PII in `Data`.
- **Never log the token string** — it is a credential; logging it leaks access.
- **HS256 secret minimum length** — use at least **32 bytes (256 bits)**; short secrets are brute-forceable.
- **Algorithm Confusion** — always validate `token.Method.Alg()` in the keyfunc (already included in the implementation above).
- **Short-lived access tokens** — keep access token lifetime short (minutes to hours); use a refresh token for long sessions.

## Quick Reference

| Scenario | Method | Key supply |
|---|---|---|
| New project, microservices | **ES256** ⭐ | `ECPrivateKeyPath` / `ECPublicKeyPath` (or `ECPrivateKeyData` / `ECPublicKeyData`) |
| Existing RSA infra, upgrade from RS256 | **PS256** ✅ | `PrivateKeyPath` / `PublicKeyPath` — **same RSA key pair, no re-keying needed** |
| Legacy RSA (keep as-is) | RS256 | `PrivateKeyPath` / `PublicKeyPath` |
| Internal / single-service monolith | HS256 | `Secret` (plain string, min 32 bytes) |
| Key from env / secret manager (asymmetric) | ES256 / PS256 / RS256 | `ECPrivateKeyData` / `PrivateKeyData` (inline PEM string) |
| Key from env / secret manager (HMAC) | HS256 | `Secret` field (plain string, min 32 chars) |

## Refresh Token Pattern

For long-lived sessions, issue **two tokens**:

| Token | Lifetime | Storage | Purpose |
|---|---|---|---|
| Access token | Short (15 min – 2 h) | Memory / Authorization header | API authentication |
| Refresh token | Long (7 – 30 days) | HttpOnly cookie or secure DB | Obtain a new access token |

```go
// Issue both tokens on login
accessToken, _ := signer.Token(userID, payload, 15*time.Minute)
refreshToken, _ := refreshSigner.Token(userID, nil, 7*24*time.Hour)

// Refresh endpoint: validate refresh token → issue new access token
claims, err := refreshParser.Parse(refreshTokenString)
if err != nil { /* 401 */ }
newAccessToken, _ := signer.Token(claims.Subject, newPayload, 15*time.Minute)
```

> Use **separate** `SignerConfig` / `ParserConfig` instances for access and refresh tokens (different secrets or key pairs, different `Issuer`/`Audience`).

For complete file-by-file implementation, see [examples.md](examples.md).
