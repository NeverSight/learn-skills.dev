---
name: dotenvx
description: "MUST USE for any task involving the dotenvx CLI tool — encrypting .env files, running commands with injected env vars, managing secrets across environments, and decrypting at runtime. Use this skill whenever the user mentions dotenvx, dotenv encryption, DOTENV_PRIVATE_KEY, encrypted .env files, or the dotenvx encrypt/run/set/get/decrypt/keypair commands. Also trigger when the user wants to: commit .env files safely to git, stop sharing secrets over Slack/chat, encrypt environment variables with public-key cryptography, set up multi-environment .env configs (production/staging/ci), manage secrets in a monorepo with -fk flag, migrate from python-dotenv or plain dotenv to encrypted envs, inject env vars into any process across any language (Node, Python, Ruby, Go, Rust, etc.), or configure CI/CD pipelines (GitHub Actions, Docker) with encrypted env files. This skill contains the authoritative CLI reference — without it, responses will hallucinate non-existent commands and flags."
---

# dotenvx CLI

dotenvx is a secure dotenv — from the creator of `dotenv`. It provides encrypted environment variables, cross-platform `run` injection, and multi-environment support.

**Key capabilities:**
- `dotenvx run` — inject env vars into any command, any language
- `dotenvx encrypt` — encrypt `.env` files with public-key cryptography (secp256k1)
- `dotenvx set` / `get` — manage individual env vars
- `dotenvx decrypt` — decrypt `.env` files back to plaintext
- Multi-environment support via `-f` flag and `DOTENV_PRIVATE_KEY_*` convention

## Installation

```sh
# npm (local to project)
npm install @dotenvx/dotenvx --save

# global installs
curl -sfS https://dotenvx.sh | sh       # curl
brew install dotenvx/brew/dotenvx        # brew
winget install dotenvx                   # windows
docker run -it --rm -v $(pwd):/app dotenv/dotenvx help  # docker
```

For Node.js, also usable as a library:
```js
require('@dotenvx/dotenvx').config()
// or: import '@dotenvx/dotenvx/config'
```

---

## Core Commands

### `dotenvx run`

Inject environment variables from `.env` files into any process. This is the primary command.

```sh
dotenvx run -- <command>
```

**Flags:**
| Flag | Description |
|---|---|
| `-f <file>` | Specify env file(s). Repeatable. Default: `.env` |
| `--env KEY=value` | Set inline env var |
| `--overload` | Later files/values override earlier ones (default: first wins) |
| `--strict` | Exit code 1 on any error (missing file, decrypt failure) |
| `--ignore=ERROR_CODE` | Ignore specific errors (e.g., `MISSING_ENV_FILE`) |
| `--convention=nextjs\|flow` | Load files using Next.js or dotenv-flow convention |
| `-fk <path>` | Specify path to `.env.keys` file (useful for monorepos) |
| `--quiet` | Suppress all output except errors |
| `--verbose` | Verbose logging |
| `--debug` | Debug-level logging |
| `--log-level=<level>` | Set log level: `error, warn, info, verbose, debug, silly` |

**Examples:**

```sh
# Basic usage
dotenvx run -- node index.js

# Specific env file
dotenvx run -f .env.production -- node index.js

# Multiple env files (first file's values win by default)
dotenvx run -f .env.local -f .env -- node index.js

# Override: last file wins
dotenvx run -f .env.local -f .env --overload -- node index.js

# Inline env var (overrides file values)
dotenvx run --env HELLO=String -f .env -- node index.js

# Any language works
dotenvx run -- python3 app.py
dotenvx run -- ruby index.rb
dotenvx run -- go run main.go
dotenvx run -- cargo run
dotenvx run -- php artisan serve
dotenvx run -- next dev

# Shell expansion (use subshell to prevent premature expansion)
dotenvx run --env="HELLO=World" -- sh -c 'echo Hello $HELLO'

# Strict mode for CI
dotenvx run -f .env.ci --strict -- node build.js
```

**Precedence rules:**
- By default, env vars already set in the shell take precedence over `.env` file values
- With multiple `-f` files, the first file's value wins (historic dotenv behavior)
- `--overload` reverses this: later files override earlier ones
- `--env` flag values take precedence over file values

**Variable expansion and interpolation:**

dotenvx supports `${VAR}` expansion, default values, alternate values, and command substitution inside `.env` files:

```ini
# Variable expansion
USERNAME="admin"
DATABASE_URL="postgres://${USERNAME}@localhost/mydb"

# Default values (use fallback if unset/empty)
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}

# Alternate values (use alternate if variable IS set)
DEBUG_MODE=${NODE_ENV:+false}

# Command substitution
WHOAMI="$(whoami)"
```

**Multiline values** are supported — wrap in double quotes:
```ini
CERT="-----BEGIN CERTIFICATE-----
MIIB...
-----END CERTIFICATE-----"
```

### Important: What dotenvx Does NOT Have

Do NOT hallucinate these — they do not exist:
- ❌ `dotenvx keys` — use `dotenvx keypair` instead
- ❌ `dotenvx status` — no such command
- ❌ `dotenvx rotate` — to rotate, use `dotenvx set` to update values, or decrypt → delete .env.keys → re-encrypt
- ❌ `--env-name` flag — does not exist
- ❌ `.env.vault` files — dotenvx encrypts **in place**, not to a separate vault file
- ❌ `DOTENVX_PRIVATE_KEY` — the correct env var is `DOTENV_PRIVATE_KEY` (no X in the middle)
- ❌ `pip install dotenvx` — there is no Python package; dotenvx is a CLI tool that wraps any language
- ❌ `dotenvx.load_dotenv()` — no Python API; use `dotenvx run -- python app.py` at the CLI level

---

### `dotenvx encrypt`

Encrypt `.env` file(s) in place. Generates a `DOTENV_PUBLIC_KEY` (added to the `.env` file) and a `DOTENV_PRIVATE_KEY` (saved to `.env.keys`).

```sh
dotenvx encrypt                     # encrypts .env
dotenvx encrypt -f .env.production  # encrypts specific file
dotenvx encrypt --stdout            # output to stdout instead of in-place
```

After encryption:
- `.env` contains encrypted values + `DOTENV_PUBLIC_KEY`
- `.env.keys` contains `DOTENV_PRIVATE_KEY` (keep this secret, never commit it)
- The encrypted `.env` is safe to commit to version control

### `dotenvx decrypt`

Decrypt an encrypted `.env` file back to plaintext.

```sh
dotenvx decrypt                     # decrypts .env
dotenvx decrypt -f .env.production  # decrypts specific file
dotenvx decrypt --stdout            # output to stdout
```

Requires the private key to be available (via `.env.keys` file or `DOTENV_PRIVATE_KEY*` env var).

### `dotenvx set`

Set an individual environment variable in a `.env` file. Creates the file if it doesn't exist. If the file is encrypted, re-encrypts automatically.

```sh
dotenvx set KEY value                       # set in .env
dotenvx set KEY value -f .env.production    # set in specific file
dotenvx set KEY "multi word value"          # quoted values
dotenvx set KEY value -fk .env.keys -f apps/app1/.env  # monorepo
```

### `dotenvx get`

Retrieve a single environment variable's value.

```sh
dotenvx get HELLO                          # from .env
dotenvx get HELLO -f .env.production       # from specific file
dotenvx get HELLO --env HELLO=Override     # from --env string
dotenvx get HELLO --overload               # with overload semantics
dotenvx get HELLO --strict                 # exit 1 if key missing
dotenvx get HELLO --convention=nextjs      # with convention
dotenvx get HELLO -fk .env.keys -f app/.env  # monorepo
```

**Get all as JSON:**
```sh
dotenvx get                    # all vars from .env as JSON
dotenvx get -f .env.production # all vars from specific file
dotenvx get --all              # include DOTENV_PUBLIC_KEY
dotenvx get --format shell     # output as KEY=value lines
```

### `dotenvx keypair`

Output the public/private keypair for an encrypted `.env` file.

```sh
dotenvx keypair                              # all keypairs as JSON
dotenvx keypair DOTENV_PRIVATE_KEY           # just the private key
dotenvx keypair -f .env.production           # for specific file
dotenvx keypair DOTENV_PRIVATE_KEY_PRODUCTION -f .env.production
```

---

## Encryption Workflow

### Initial Setup

```sh
# 1. Create your .env
echo "DATABASE_URL=postgres://localhost/mydb" > .env
echo "API_KEY=sk-secret123" >> .env

# 2. Encrypt it
dotenvx encrypt
# ✔ encrypted (.env)
# Creates .env.keys with your private key

# 3. Commit .env (encrypted, safe), do NOT commit .env.keys
echo ".env.keys" >> .gitignore
git add .env .gitignore
git commit -m "add encrypted env"
```

### Multi-Environment Encryption

Each environment gets its own keypair. The naming convention is automatic:

```sh
# Encrypt each environment
dotenvx encrypt -f .env.production
dotenvx encrypt -f .env.staging
dotenvx encrypt -f .env.ci

# Each creates a corresponding private key in .env.keys:
# DOTENV_PRIVATE_KEY_PRODUCTION="..."
# DOTENV_PRIVATE_KEY_STAGING="..."
# DOTENV_PRIVATE_KEY_CI="..."
```

### Runtime Decryption

Set the appropriate `DOTENV_PRIVATE_KEY_*` env var, and `dotenvx run` decrypts automatically:

```sh
# The private key suffix matches the file suffix
DOTENV_PRIVATE_KEY="key"                  dotenvx run -- node app.js          # decrypts .env
DOTENV_PRIVATE_KEY_PRODUCTION="key"       dotenvx run -- node app.js          # decrypts .env.production
DOTENV_PRIVATE_KEY_CI="key"               dotenvx run -- node app.js          # decrypts .env.ci

# Combine multiple
DOTENV_PRIVATE_KEY="k1" DOTENV_PRIVATE_KEY_PRODUCTION="k2" dotenvx run -- node app.js

# Comma-separated keys for monorepos (same environment, different apps)
DOTENV_PRIVATE_KEY_CI="key1,key2" dotenvx run -f app1/.env.ci -f app2/.env.ci -- node app.js
```

### CI/CD Integration

```yaml
# GitHub Actions example
name: deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: curl -fsS https://dotenvx.sh/install.sh | sh
      - run: dotenvx run -- node build.js
        env:
          DOTENV_PRIVATE_KEY_PRODUCTION: ${{ secrets.DOTENV_PRIVATE_KEY_PRODUCTION }}
```

---

## Conventions

### `--convention=nextjs`

Loads files in Next.js priority order:
1. `.env.$(NODE_ENV).local`
2. `.env.local`
3. `.env.$(NODE_ENV)`
4. `.env`

```sh
dotenvx run --convention=nextjs -- next dev
```

### `--convention=flow`

Loads files in dotenv-flow priority order. Uses `DOTENV_ENV` or `NODE_ENV`:

```sh
DOTENV_ENV=development dotenvx run --convention=flow -- node app.js
```

---

## Monorepo Support

Use `-fk` to specify a shared `.env.keys` path:

```sh
# Set values for different apps
dotenvx set HELLO app1 -fk .env.keys -f apps/app1/.env
dotenvx set HELLO app2 -fk .env.keys -f apps/app2/.env

# Run with shared keys
dotenvx run -fk .env.keys -f apps/app1/.env -- node apps/app1/index.js

# Get values
dotenvx get HELLO -fk .env.keys -f apps/app1/.env
```

---

## Docker

```dockerfile
FROM node:latest
RUN curl -fsS https://dotenvx.sh/install.sh | sh
COPY . .
CMD ["dotenvx", "run", "--", "node", "index.js"]
```

Or run directly:
```sh
docker run -it --rm -v $(pwd):/app dotenv/dotenvx run -- node index.js
```

---

## Common Patterns

**Add a new secret to an encrypted file:**
```sh
dotenvx set NEW_SECRET "value" -f .env.production
# Automatically re-encrypts
```

**Rotate a value:**
```sh
dotenvx set API_KEY "new-key-value" -f .env.production
```

**View decrypted values without running a command:**
```sh
dotenvx get -f .env.production           # needs private key available
dotenvx get API_KEY -f .env.production   # single value
```

**Convert existing plaintext .env to encrypted:**
```sh
dotenvx encrypt -f .env.production
# Done. Commit the encrypted .env.production, store .env.keys privately.
```

**Suppress dotenvx output in scripts:**
```sh
dotenvx run --quiet -- ./my-script.sh
```

**Fail CI on missing/broken env:**
```sh
dotenvx run -f .env.ci --strict -- npm test
```

---

## Gitignore Recommendations

```gitignore
# Never commit private keys
.env.keys

# Encrypted .env files ARE safe to commit
# !.env
# !.env.production
# !.env.staging
```

## Troubleshooting

- **`MISSING_ENV_FILE`** — the specified `.env` file doesn't exist. Create it or use `--ignore=MISSING_ENV_FILE`.
- **`MISSING_KEY`** — the requested key isn't in the `.env` file.
- **Decryption fails** — ensure the correct `DOTENV_PRIVATE_KEY_*` is set. The suffix must match the file suffix (e.g., `_PRODUCTION` for `.env.production`).
- **Deno + encrypt** — don't use `deno run npm:@dotenvx/dotenvx encrypt`. Deno has incomplete cipher support. Install dotenvx as a binary instead.
- **Shell expanding `$VARS` prematurely** — use a subshell: `dotenvx run -- sh -c 'echo $MY_VAR'`

---

## Extension Commands (`dotenvx ext`)

Utility commands for managing dotenvx workflows:

```sh
dotenvx ext genexample                  # generate .env.example from .env
dotenvx ext genexample -f .env.production  # from specific file
dotenvx ext gitignore                   # append .env.keys to .gitignore
dotenvx ext ls                          # list all .env files in project
dotenvx ext ls -f .env.production       # check specific file
dotenvx ext settings                    # view current dotenvx settings
```